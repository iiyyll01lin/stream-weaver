# Phase 2 Implementation Guide

**Document Version**: 1.0 | **Last Updated**: 2025-11-12  
**Related Documents**:
- [Phase 2 Architecture](PHASE2_ARCHITECTURE_EN.md)
- [Phase 2 API Specification](PHASE2_API_SPEC_EN.md)
- [Phase 1 Implementation Guide](PHASE1_IMPLEMENTATION_EN.md)

---

## Table of Contents

- [Overview](#overview)
- [Environment Setup](#environment-setup)
- [Feature Implementation](#feature-implementation)
  - [Multi-Line Optimization](#1-multi-line-optimization)
  - [Fishbone Diagram Generator](#2-fishbone-diagram-generator)
  - [Layout Management System](#3-layout-management-system)
  - [Product Configuration Database](#4-product-configuration-database)
  - [Line Type Recommendation](#5-line-type-recommendation)
- [Database Setup](#database-setup)
- [Testing](#testing)
- [Deployment](#deployment)

---

## Overview

Phase 2 builds upon Phase 1 infrastructure to add:
- Multi-line production optimization
- Visual assembly sequence diagrams
- Interactive layout management
- Product configuration database
- Intelligent line type recommendations

---

## Environment Setup

### 1. Install Phase 2 Dependencies

**Update `requirements.txt`**:
```txt
# Phase 1 dependencies
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
ortools>=9.7.0
absl-py>=2.0.0
pandas>=2.0.0

# Phase 2 NEW dependencies
sqlalchemy>=2.0.0          # ORM for database
networkx>=3.0              # Graph algorithms (fishbone)
matplotlib>=3.7.0          # Diagram rendering
pillow>=10.0.0             # Image processing
alembic>=1.12.0            # Database migrations
python-dotenv>=1.0.0       # Environment variables
```

**Install**:
```bash
pip install -r requirements.txt
```

---

### 2. Environment Configuration

Create `.env` file:
```bash
# Database configuration
DATABASE_URL=sqlite:///./line_balance.db
# For production:
# DATABASE_URL=postgresql://user:password@localhost/line_balance_db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG_MODE=True

# File Storage
LAYOUT_STORAGE_PATH=./storage/layouts
FISHBONE_OUTPUT_PATH=./output/fishbone
```

---

### 3. Project Structure

```
line-balance/
├── src/
│   ├── api_server.py           # Extended API (Phase 1 + 2)
│   ├── dashboard.html          # Enhanced UI
│   ├── sche-algo.py            # Phase 1 solver
│   ├── sche-algo-v2.py         # NEW: Multi-line solver
│   ├── fishbone_generator.py   # NEW: Fishbone diagram
│   ├── models/                 # NEW: Database models
│   │   ├── __init__.py
│   │   ├── layout.py
│   │   ├── product_config.py
│   │   └── optimization_history.py
│   ├── services/               # NEW: Business logic
│   │   ├── __init__.py
│   │   ├── layout_service.py
│   │   ├── product_service.py
│   │   └── recommendation_service.py
│   └── utils/                  # NEW: Utilities
│       ├── __init__.py
│       ├── db.py               # Database session
│       └── validators.py
├── data/                       # CSV input files
├── output/                     # Algorithm outputs
│   └── fishbone/               # NEW: Fishbone diagrams
├── storage/                    # NEW: File storage
│   └── layouts/
├── migrations/                 # NEW: Alembic migrations
├── tests/                      # Test suites
│   ├── test_multi_line.py      # NEW
│   ├── test_fishbone.py        # NEW
│   └── test_layout_api.py      # NEW
└── docs/                       # Documentation
```

---

## Feature Implementation

### 1. Multi-Line Optimization

#### Step 1: Create Multi-Line Solver (`sche-algo-v2.py`)

```python
#!/usr/bin/env python3
"""
Multi-Line Production Line Balancing Solver
Phase 2 - Extended Optimization
"""

import argparse
import json
import pandas as pd
from ortools.sat.python import cp_model
from typing import Dict, List, Any

def parse_multi_line_csv(csv_file: str) -> pd.DataFrame:
    """
    Parse extended CSV with line_id column
    
    Expected columns:
    line_id, task_id, duration, offline_flag, adjustable, action_type, 
    complexity_level, part_id, predecessors
    """
    df = pd.read_csv(csv_file)
    
    # Validate required columns
    required_cols = ['line_id', 'task_id', 'duration']
    for col in required_cols:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")
    
    return df

def solve_multi_line(
    tasks_df: pd.DataFrame,
    precedences_df: pd.DataFrame,
    line_configs: List[Dict],
    objective: str = "min_stations",
    enable_cross_line_balancing: bool = True
) -> Dict[str, Any]:
    """
    Multi-line optimization solver
    
    Args:
        tasks_df: DataFrame with columns [line_id, task_id, duration, ...]
        precedences_df: DataFrame with [predecessor, successor]
        line_configs: List of {line_id, target_takt, max_workers}
        objective: "min_stations", "min_manpower", "min_idle"
        enable_cross_line_balancing: Balance workload across lines
    
    Returns:
        Dict with multi-line solution
    """
    model = cp_model.CpModel()
    
    # Extract parameters
    num_tasks = len(tasks_df)
    num_lines = len(line_configs)
    max_stations_per_line = 20
    
    # Map line_id to index
    line_id_map = {config['line_id']: i for i, config in enumerate(line_configs)}
    
    # Decision variables: x[i][j][l] = 1 if task i assigned to station j on line l
    x = {}
    for i in range(num_tasks):
        task_line_id = tasks_df.loc[i, 'line_id'] if 'line_id' in tasks_df.columns else None
        
        for l in range(num_lines):
            # Skip if task has specific line assignment
            if task_line_id and task_line_id != line_configs[l]['line_id']:
                continue
            
            for j in range(max_stations_per_line):
                x[(i, j, l)] = model.NewBoolVar(f'x_t{i}_s{j}_l{l}')
    
    # Station usage variables
    station_used = {}
    for l in range(num_lines):
        for j in range(max_stations_per_line):
            station_used[(j, l)] = model.NewBoolVar(f'station_s{j}_l{l}_used')
    
    # Constraint 1: Each task to exactly one (station, line) pair
    for i in range(num_tasks):
        model.Add(
            sum(x[(i, j, l)] 
                for (ti, j, l) in x.keys() 
                if ti == i
            ) == 1
        )
    
    # Constraint 2: Station usage linkage
    for l in range(num_lines):
        for j in range(max_stations_per_line):
            # If any task at (j, l), then station_used[(j, l)] = 1
            tasks_at_station = [
                x[(i, j, l)] 
                for (i, jp, lp) in x.keys() 
                if jp == j and lp == l
            ]
            if tasks_at_station:
                model.Add(station_used[(j, l)] >= max(tasks_at_station))
    
    # Constraint 3: Precedence (same line only)
    for _, row in precedences_df.iterrows():
        pred = int(row['predecessor'])
        succ = int(row['successor'])
        
        for l in range(num_lines):
            for j in range(max_stations_per_line - 1):
                # If pred at (j, l), succ must be at (j', l) where j' >= j
                if (pred, j, l) in x and (succ, j, l) in x:
                    for jp in range(j + 1, max_stations_per_line):
                        if (succ, jp, l) in x:
                            model.Add(
                                x[(succ, jp, l)] >= x[(pred, j, l)]
                            )
    
    # Constraint 4: Takt time per line per station
    for l, config in enumerate(line_configs):
        target_takt = config['target_takt']
        
        for j in range(max_stations_per_line):
            station_load = 0
            for i in range(num_tasks):
                if (i, j, l) in x:
                    station_load += tasks_df.loc[i, 'duration'] * x[(i, j, l)]
            
            model.Add(station_load <= target_takt)
    
    # Constraint 5: Cross-line balancing (optional)
    if enable_cross_line_balancing:
        line_loads = []
        for l in range(num_lines):
            line_load = sum(
                tasks_df.loc[i, 'duration'] * x[(i, j, l)]
                for (i, j, lp) in x.keys() if lp == l
            )
            line_loads.append(line_load)
        
        # Minimize load imbalance
        if line_loads:
            max_load = model.NewIntVar(0, 10000000, 'max_load')
            min_load = model.NewIntVar(0, 10000000, 'min_load')
            
            for load in line_loads:
                model.Add(max_load >= load)
                model.Add(min_load <= load)
    
    # Objective
    if objective == "min_stations":
        total_stations = sum(station_used.values())
        model.Minimize(total_stations)
    elif objective == "min_manpower":
        # Assume 1 worker per station for simplicity
        total_manpower = sum(station_used.values())
        model.Minimize(total_manpower)
    else:  # min_idle
        total_idle = 0
        for l, config in enumerate(line_configs):
            for j in range(max_stations_per_line):
                station_load = sum(
                    tasks_df.loc[i, 'duration'] * x[(i, j, l)]
                    for (i, jp, lp) in x.keys() 
                    if jp == j and lp == l
                )
                idle_time = model.NewIntVar(0, config['target_takt'], f'idle_s{j}_l{l}')
                model.Add(idle_time == config['target_takt'] - station_load)
                total_idle += idle_time
        
        model.Minimize(total_idle)
    
    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 8
    solver.parameters.max_time_in_seconds = 60
    
    status = solver.Solve(model)
    
    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        return extract_solution(solver, x, station_used, tasks_df, line_configs)
    else:
        raise ValueError(f"Solver failed with status: {solver.StatusName(status)}")

def extract_solution(
    solver, 
    x, 
    station_used, 
    tasks_df, 
    line_configs
) -> Dict[str, Any]:
    """Extract multi-line solution from solver"""
    
    lines_result = []
    total_stations = 0
    
    for l, config in enumerate(line_configs):
        line_stations = []
        
        for j in range(20):  # max_stations_per_line
            if (j, l) in station_used and solver.Value(station_used[(j, l)]) == 1:
                # Find tasks at this station
                station_tasks = []
                station_load = 0
                
                for i in range(len(tasks_df)):
                    if (i, j, l) in x and solver.Value(x[(i, j, l)]) == 1:
                        station_tasks.append(int(tasks_df.loc[i, 'task_id']))
                        station_load += int(tasks_df.loc[i, 'duration'])
                
                if station_tasks:
                    line_stations.append({
                        "id": f"{config['line_id']}-WS-{j+1:03d}",
                        "tasks": station_tasks,
                        "load_ms": station_load,
                        "utilization": round(station_load / config['target_takt'] * 100, 2)
                    })
                    total_stations += 1
        
        if line_stations:
            avg_util = sum(s['utilization'] for s in line_stations) / len(line_stations)
            
            lines_result.append({
                "line_id": config['line_id'],
                "stations": line_stations,
                "station_count": len(line_stations),
                "manpower": len(line_stations),  # Simplified: 1 worker per station
                "takt_time_ms": config['target_takt'],
                "utilization_avg": round(avg_util, 2)
            })
    
    # Calculate cross-line balance score
    if len(lines_result) > 1:
        line_loads = [
            sum(s['load_ms'] for s in line['stations'])
            for line in lines_result
        ]
        avg_load = sum(line_loads) / len(line_loads)
        max_deviation = max(abs(load - avg_load) for load in line_loads)
        balance_score = max(0, 1 - (max_deviation / avg_load)) if avg_load > 0 else 1.0
    else:
        balance_score = 1.0
    
    return {
        "multi_line_results": {
            "total_lines_used": len(lines_result),
            "total_stations": total_stations,
            "total_manpower": sum(line['manpower'] for line in lines_result),
            "cross_line_balance_score": round(balance_score, 2),
            "lines": lines_result
        }
    }

def main():
    parser = argparse.ArgumentParser(description='Multi-Line Optimization Solver')
    parser.add_argument('--tasks_csv', required=True, help='Tasks CSV with line_id column')
    parser.add_argument('--precedences_csv', required=True, help='Precedences CSV')
    parser.add_argument('--line_configs_json', required=True, help='Line configs JSON')
    parser.add_argument('--objective', default='min_stations', 
                       choices=['min_stations', 'min_manpower', 'min_idle'])
    parser.add_argument('--enable_cross_line_balancing', action='store_true')
    parser.add_argument('--json_output', required=True, help='Output JSON file')
    
    args = parser.parse_args()
    
    # Load data
    tasks_df = parse_multi_line_csv(args.tasks_csv)
    precedences_df = pd.read_csv(args.precedences_csv)
    
    with open(args.line_configs_json, 'r') as f:
        line_configs = json.load(f)
    
    # Solve
    result = solve_multi_line(
        tasks_df,
        precedences_df,
        line_configs,
        args.objective,
        args.enable_cross_line_balancing
    )
    
    # Output
    with open(args.json_output, 'w') as f:
        json.dump(result, f, indent=2)
    
    print(f"✓ Multi-line optimization completed")
    print(f"  Lines used: {result['multi_line_results']['total_lines_used']}")
    print(f"  Total stations: {result['multi_line_results']['total_stations']}")

if __name__ == '__main__':
    main()
```

#### Step 2: Test Multi-Line Solver

Create test data `data/test_tasks_multi_line.csv`:
```csv
line_id,task_id,duration,predecessors
A,1,5000,
A,2,3000,1
A,3,4000,1
B,4,6000,
B,5,3500,4
B,6,4200,4
```

Create line configs `data/line_configs.json`:
```json
[
  {
    "line_id": "A",
    "target_takt": 15000,
    "max_workers_per_station": 3
  },
  {
    "line_id": "B",
    "target_takt": 18000,
    "max_workers_per_station": 2
  }
]
```

Test execution:
```bash
python3 src/sche-algo-v2.py \
  --tasks_csv data/test_tasks_multi_line.csv \
  --precedences_csv data/test_precedences.csv \
  --line_configs_json data/line_configs.json \
  --objective min_stations \
  --enable_cross_line_balancing \
  --json_output output/multi_line_result.json

# Verify output
cat output/multi_line_result.json
```

---

### 2. Fishbone Diagram Generator

#### Step 1: Create Fishbone Generator (`fishbone_generator.py`)

```python
#!/usr/bin/env python3
"""
Fishbone (Assembly Sequence) Diagram Generator
Phase 2 - Visualization Tool
"""

import argparse
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import patches
import json

def generate_fishbone_diagram(
    tasks_csv: str,
    precedences_csv: str,
    output_file: str,
    format: str = "svg",
    highlight_critical_path: bool = False
):
    """
    Generate fishbone diagram from task and precedence data
    
    Args:
        tasks_csv: Path to tasks CSV
        precedences_csv: Path to precedences CSV
        output_file: Output file path
        format: "svg" or "png"
        highlight_critical_path: Highlight longest path
    """
    # Load data
    tasks_df = pd.read_csv(tasks_csv)
    precedences_df = pd.read_csv(precedences_csv)
    
    # Build directed graph
    G = nx.DiGraph()
    
    # Add nodes
    for _, row in tasks_df.iterrows():
        G.add_node(
            int(row['task_id']),
            duration=int(row['duration']),
            action_type=row.get('action_type', 'unknown')
        )
    
    # Add edges
    for _, row in precedences_df.iterrows():
        pred = int(row['predecessor'])
        succ = int(row['successor'])
        if pred in G.nodes and succ in G.nodes:
            G.add_edge(pred, succ)
    
    # Calculate levels (topological layers)
    levels = {}
    for node in nx.topological_sort(G):
        predecessors = list(G.predecessors(node))
        if not predecessors:
            levels[node] = 0
        else:
            levels[node] = max(levels[p] for p in predecessors) + 1
    
    # Find critical path if requested
    critical_path = []
    if highlight_critical_path:
        critical_path = nx.dag_longest_path(G, weight='duration')
    
    # Generate layout
    pos = fishbone_layout(G, levels)
    
    # Render
    fig, ax = plt.subplots(figsize=(16, 10))
    ax.set_facecolor('white')
    
    # Draw spine (main assembly line)
    max_level = max(levels.values())
    ax.plot([0, max_level + 1], [0, 0], 'k-', linewidth=4, zorder=1, label='Assembly Flow')
    
    # Draw tasks (bones)
    for node, (x, y) in pos.items():
        # Determine color
        action_type = G.nodes[node].get('action_type', 'unknown')
        color = get_action_color(action_type)
        
        if node in critical_path:
            color = '#e74c3c'  # Red for critical path
            edge_color = '#c0392b'
            linewidth = 3
        else:
            edge_color = '#34495e'
            linewidth = 1.5
        
        # Draw task node
        circle = patches.Circle((x, y), 0.25, 
                                color=color,
                                edgecolor=edge_color,
                                linewidth=linewidth,
                                zorder=3)
        ax.add_patch(circle)
        
        # Label
        ax.text(x, y, str(node), 
               ha='center', va='center', 
               fontsize=10, fontweight='bold', 
               color='white', zorder=4)
        
        # Bone line to spine
        ax.plot([x, x], [y, 0], 'k-', linewidth=1.5, alpha=0.6, zorder=2)
        
        # Duration label
        duration = G.nodes[node]['duration']
        ax.text(x + 0.1, y + 0.15, f'{duration}ms', 
               fontsize=7, style='italic', zorder=4)
    
    # Draw precedence arrows
    for u, v in G.edges():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        
        if u in critical_path and v in critical_path:
            arrow_color = '#e74c3c'
            linewidth = 2
        else:
            arrow_color = '#95a5a6'
            linewidth = 1
        
        ax.annotate('', 
                   xy=(x2 - 0.25 if x2 > x1 else x2, y2), 
                   xytext=(x1 + 0.25 if x2 > x1 else x1, y1),
                   arrowprops=dict(
                       arrowstyle='->',
                       lw=linewidth,
                       color=arrow_color,
                       alpha=0.7
                   ),
                   zorder=2)
    
    # Styling
    ax.set_xlim(-0.5, max_level + 1.5)
    ax.set_ylim(-6, 6)
    ax.axis('off')
    ax.set_title('Assembly Sequence Fishbone Diagram', 
                fontsize=18, fontweight='bold', pad=20)
    
    # Legend
    legend_elements = [
        patches.Patch(color=get_action_color('screw'), label='Screw Operations'),
        patches.Patch(color=get_action_color('glue'), label='Glue/Adhesive'),
        patches.Patch(color=get_action_color('mount'), label='Mount/Install'),
        patches.Patch(color=get_action_color('test'), label='Test/QC')
    ]
    if critical_path:
        legend_elements.append(
            patches.Patch(color='#e74c3c', label='Critical Path')
        )
    
    ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
    
    # Save
    if format == "svg":
        plt.savefig(output_file, format='svg', bbox_inches='tight', dpi=150)
    else:
        plt.savefig(output_file, format='png', bbox_inches='tight', dpi=300)
    
    plt.close()
    
    print(f"✓ Fishbone diagram saved: {output_file}")
    print(f"  Nodes: {len(G.nodes)}")
    print(f"  Edges: {len(G.edges)}")
    if critical_path:
        print(f"  Critical path length: {len(critical_path)} tasks")

def fishbone_layout(G, levels):
    """Generate fishbone-style layout positions"""
    pos = {}
    level_counts = {}
    
    for node, level in levels.items():
        if level not in level_counts:
            level_counts[level] = 0
        
        # Alternate above/below spine
        side = (level_counts[level] % 2) * 2 - 1  # -1 or 1
        offset_index = level_counts[level] // 2
        y_position = side * (1.2 + offset_index * 0.8)
        
        pos[node] = (level, y_position)
        level_counts[level] += 1
    
    return pos

def get_action_color(action_type):
    """Map action type to color"""
    colors = {
        'screw': '#3498db',      # Blue
        'glue': '#e67e22',       # Orange
        'clip': '#2ecc71',       # Green
        'mount': '#f39c12',      # Yellow
        'test': '#9b59b6',       # Purple
        'install': '#1abc9c',    # Turquoise
        'unknown': '#95a5a6'     # Gray
    }
    return colors.get(action_type.lower(), colors['unknown'])

def main():
    parser = argparse.ArgumentParser(description='Fishbone Diagram Generator')
    parser.add_argument('--tasks_csv', required=True)
    parser.add_argument('--precedences_csv', required=True)
    parser.add_argument('--output', required=True)
    parser.add_argument('--format', default='svg', choices=['svg', 'png'])
    parser.add_argument('--highlight_critical_path', action='store_true')
    
    args = parser.parse_args()
    
    generate_fishbone_diagram(
        args.tasks_csv,
        args.precedences_csv,
        args.output,
        args.format,
        args.highlight_critical_path
    )

if __name__ == '__main__':
    main()
```

#### Step 2: Test Fishbone Generator

```bash
python3 src/fishbone_generator.py \
  --tasks_csv data/test_tasks_extended.csv \
  --precedences_csv data/test_precedences.csv \
  --output output/fishbone/test_fishbone.svg \
  --format svg \
  --highlight_critical_path

# View the generated SVG
open output/fishbone/test_fishbone.svg  # macOS
# or xdg-open output/fishbone/test_fishbone.svg  # Linux
```

---

### 3. Layout Management System

#### Step 1: Database Models (`src/models/layout.py`)

```python
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Layout(Base):
    """Layout database model"""
    __tablename__ = 'layouts'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    site = Column(String(100), nullable=False)
    data_json = Column(Text, nullable=False)  # JSON string
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    def __repr__(self):
        return f"<Layout(id={self.id}, name='{self.name}', site='{self.site}')>"
```

#### Step 2: Layout Service (`src/services/layout_service.py`)

```python
import json
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from models.layout import Layout

class LayoutService:
    """Business logic for layout management"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def get_all_layouts(self, site: Optional[str] = None, limit: int = 50) -> List[Dict]:
        """Retrieve all layouts"""
        query = self.db.query(Layout)
        
        if site:
            query = query.filter(Layout.site == site)
        
        layouts = query.limit(limit).all()
        
        return [
            {
                "id": layout.id,
                "name": layout.name,
                "description": layout.description,
                "site": layout.site,
                "created_at": layout.created_at.isoformat(),
                "updated_at": layout.updated_at.isoformat()
            }
            for layout in layouts
        ]
    
    def get_layout(self, layout_id: int) -> Optional[Dict]:
        """Retrieve specific layout"""
        layout = self.db.query(Layout).filter(Layout.id == layout_id).first()
        
        if not layout:
            return None
        
        return {
            "id": layout.id,
            "name": layout.name,
            "description": layout.description,
            "site": layout.site,
            "data": json.loads(layout.data_json),
            "created_at": layout.created_at.isoformat(),
            "updated_at": layout.updated_at.isoformat()
        }
    
    def save_layout(self, layout_data: Dict) -> int:
        """Save new or update existing layout"""
        layout_id = layout_data.get('id')
        
        if layout_id:
            # Update existing
            layout = self.db.query(Layout).filter(Layout.id == layout_id).first()
            if not layout:
                raise ValueError(f"Layout not found: id={layout_id}")
            
            layout.name = layout_data['name']
            layout.description = layout_data.get('description')
            layout.site = layout_data['site']
            layout.data_json = json.dumps(layout_data['data'])
            layout.updated_at = datetime.now()
        else:
            # Create new
            layout = Layout(
                name=layout_data['name'],
                description=layout_data.get('description'),
                site=layout_data['site'],
                data_json=json.dumps(layout_data['data'])
            )
            self.db.add(layout)
        
        self.db.commit()
        return layout.id
    
    def delete_layout(self, layout_id: int) -> bool:
        """Delete layout"""
        layout = self.db.query(Layout).filter(Layout.id == layout_id).first()
        
        if not layout:
            return False
        
        self.db.delete(layout)
        self.db.commit()
        return True
```

#### Step 3: Database Setup (`src/utils/db.py`)

```python
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from models.layout import Base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./line_balance.db')

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Initialize database (create tables)"""
    Base.metadata.create_all(bind=engine)
    print("✓ Database initialized")

def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

Initialize database:
```bash
python3 -c "from src.utils.db import init_db; init_db()"
```

---

### 4. Product Configuration Database

Create similar structure for product configs (`src/models/product_config.py` + `src/services/product_service.py`).

---

### 5. Line Type Recommendation

Implement in `src/services/recommendation_service.py`:

```python
import pandas as pd
from typing import Dict, List

class RecommendationService:
    """Line type recommendation logic"""
    
    @staticmethod
    def recommend_line_type(
        tasks_df: pd.DataFrame,
        target_takt: int,
        max_workers_available: int = 10
    ) -> Dict:
        """
        Recommend optimal line type
        
        Returns:
            {
                "recommended_type": "cell" | "short_line" | "long_line",
                "confidence": 0.0-1.0,
                "reasoning": {...},
                "alternatives": [...]
            }
        """
        task_count = len(tasks_df)
        total_work = tasks_df['duration'].sum()
        min_theoretical_stations = total_work / target_takt
        
        # Complexity analysis
        if 'complexity_level' in tasks_df.columns:
            complexity_dist = tasks_df['complexity_level'].value_counts().to_dict()
            complex_ratio = complexity_dist.get('complex', 0) / task_count
        else:
            complex_ratio = 0
        
        # Recommendation logic
        if task_count < 20 and min_theoretical_stations < 3:
            recommended = "cell"
            confidence = 0.9 - (complex_ratio * 0.3)
        elif task_count < 50 and min_theoretical_stations < 8:
            recommended = "short_line"
            confidence = 0.85
        else:
            recommended = "long_line"
            confidence = 0.8
        
        return {
            "recommended_type": recommended,
            "confidence": round(confidence, 2),
            "reasoning": {
                "task_count": task_count,
                "total_work_ms": int(total_work),
                "target_takt_ms": target_takt,
                "min_theoretical_stations": round(min_theoretical_stations, 1),
                "recommended_stations": int(min_theoretical_stations) + 1
            },
            "alternatives": [
                {"type": "cell", "suitability": 0.3 if recommended != "cell" else 0.9},
                {"type": "short_line", "suitability": 0.5 if recommended != "short_line" else 0.85},
                {"type": "long_line", "suitability": 0.4 if recommended != "long_line" else 0.8}
            ]
        }
```

---

## Database Setup

### Migration with Alembic

```bash
# Initialize Alembic
alembic init migrations

# Create migration
alembic revision --autogenerate -m "Add layouts and product_configs tables"

# Apply migration
alembic upgrade head
```

---

## Testing

### Integration Tests

Create `tests/test_phase2_integration.py`:

```python
import pytest
import requests

BASE_URL = "http://localhost:8000"

def test_multi_line_optimization():
    """Test multi-line optimization endpoint"""
    response = requests.post(f"{BASE_URL}/optimize", json={
        "work_order_id": "WO_MULTI",
        "optimization_goal": "min_stations",
        "multi_line_config": {
            "enabled": True,
            "lines": [
                {"line_id": "A", "target_takt": 30000},
                {"line_id": "B", "target_takt": 25000}
            ]
        }
    })
    
    assert response.status_code == 200
    data = response.json()
    assert "multi_line_results" in data
    assert data["multi_line_results"]["total_lines_used"] >= 1

def test_fishbone_generation():
    """Test fishbone diagram generation"""
    response = requests.get(f"{BASE_URL}/fishbone-diagram", params={
        "work_order_id": "WO_A",
        "format": "svg"
    })
    
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'image/svg+xml'

def test_layout_crud():
    """Test layout CRUD operations"""
    # Create
    create_response = requests.post(f"{BASE_URL}/save-layout", json={
        "name": "Test Layout",
        "site": "factory_test",
        "data": {
            "stations": [{"id": "WS-001", "x": 100, "y": 200}],
            "connections": [],
            "dimensions": {"width": 1000, "height": 600}
        }
    })
    
    assert create_response.status_code == 200
    layout_id = create_response.json()['layout_id']
    
    # Read
    get_response = requests.get(f"{BASE_URL}/layout/{layout_id}")
    assert get_response.status_code == 200
    
    # Delete
    delete_response = requests.delete(f"{BASE_URL}/layout/{layout_id}")
    assert delete_response.status_code == 200
```

Run tests:
```bash
# Start server in background
python3 src/api_server.py &

# Run tests
pytest tests/test_phase2_integration.py -v

# Stop server
kill %1
```

---

## Deployment

### Docker Setup

Update `Dockerfile`:
```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY src/ ./src/
COPY data/ ./data/
COPY migrations/ ./migrations/

# Create necessary directories
RUN mkdir -p output/fishbone storage/layouts

# Initialize database
RUN python3 -c "from src.utils.db import init_db; init_db()"

EXPOSE 8000

CMD ["python3", "src/api_server.py"]
```

Build and run:
```bash
docker build -t line-balance-api:phase2 .

docker run -d \
  --name line-balance-phase2 \
  -p 8000:8000 \
  -v $(pwd)/storage:/app/storage \
  -v $(pwd)/output:/app/output \
  --env-file .env \
  line-balance-api:phase2
```

---

**Document Maintainer:** JASON YY, LIN  
**Last Updated:** 2025-11-12 
**Version:** 2.0.0-phase2
