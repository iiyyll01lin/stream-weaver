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
  - [Cross-Line Task Benchmark](#6-cross-line-task-benchmark)
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
- Cross-line task benchmark analysis

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
import math
import pandas as pd
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

# Configurable thresholds (can be overridden via config)
LINE_TYPE_THRESHOLDS = {
    "cell": {"max_stations": 3, "max_tasks": 20, "max_demand": 50},
    "short_line": {"max_stations": 8, "max_tasks": 50, "max_demand": 200},
    "long_line": {"min_stations": 9, "min_tasks": 50, "min_demand": 200}
}

@dataclass
class LineTypeRecommendationRequest:
    """Request parameters for line type recommendation"""
    work_order_id: str
    target_takt: int
    max_workers_available: int = 10
    optimization_goal: str = "min_stations"
    daily_demand: Optional[int] = None
    product_mix_count: Optional[int] = None
    changeover_time_ms: Optional[int] = None
    # NEW constraint parameters
    available_space_sqm: Optional[float] = None
    multi_skill_worker_count: Optional[int] = None
    quality_target_dppm: Optional[int] = None
    demand_variability_pct: Optional[float] = None
    is_new_product: bool = False
    # NEW Phase 2.1 parameters
    equipment_available: Optional[List[str]] = None  # e.g., ["conveyor", "agv", "auto_screwdriver"]
    product_family: Optional[str] = None  # e.g., "DL360" for historical lookup


class RecommendationService:
    """
    Line type recommendation logic with enhanced multi-factor analysis.
    
    NEW in Phase 2 Enhancement:
    - Multi-factor scoring algorithm
    - Configurable thresholds
    - Decision factor explanations
    - Feasibility checks per line type
    - Warning generation
    - Manpower estimation
    - Constraint validation (space, skills, quality)
    - Cost analysis comparison
    - Risk assessment
    - Implementation effort estimation
    - Scenario comparison (what-if analysis)
    
    NEW in Phase 2.1 Enhancement:
    - Equipment availability validation
    - Historical accuracy tracking (learning from past recommendations)
    - Confidence interval calculation (statistical uncertainty range)
    """
    
    @staticmethod
    def recommend_line_type(
        tasks_df: pd.DataFrame,
        target_takt: int,
        max_workers_available: int = 10,
        optimization_goal: str = "min_stations",
        daily_demand: Optional[int] = None,
        product_mix_count: Optional[int] = None,
        changeover_time_ms: Optional[int] = None,
        available_space_sqm: Optional[float] = None,
        multi_skill_worker_count: Optional[int] = None,
        quality_target_dppm: Optional[int] = None,
        demand_variability_pct: Optional[float] = None,
        is_new_product: bool = False,
        equipment_available: Optional[List[str]] = None,
        product_family: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Recommend optimal line type with enhanced analysis.
        
        Args:
            tasks_df: DataFrame with task data
            target_takt: Target takt time in ms
            max_workers_available: Available workforce
            optimization_goal: "min_stations", "min_manpower", or "min_idle"
            daily_demand: Units per day (affects line type choice)
            product_mix_count: Number of product variants (high mix favors cell)
            changeover_time_ms: Product changeover time
        
        Returns:
            Complete recommendation with confidence, alternatives, and warnings
        """
        # Calculate core metrics
        task_count = len(tasks_df)
        total_work = tasks_df['duration'].sum()
        theoretical_min_stations = math.ceil(total_work / target_takt)
        
        # Complexity analysis
        if 'complexity_level' in tasks_df.columns:
            complexity_dist = tasks_df['complexity_level'].value_counts().to_dict()
        else:
            complexity_dist = {"unknown": task_count}
        
        # Calculate multi-factor scores for each line type
        scores = RecommendationService._calculate_line_type_scores(
            task_count=task_count,
            theoretical_min_stations=theoretical_min_stations,
            daily_demand=daily_demand,
            product_mix_count=product_mix_count,
            optimization_goal=optimization_goal,
            complexity_dist=complexity_dist
        )
        
        # Determine best recommendation
        recommendation = max(scores, key=lambda x: scores[x]["score"])
        confidence = scores[recommendation]["score"]
        
        # Build decision factors
        decision_factors = RecommendationService._build_decision_factors(
            task_count, theoretical_min_stations, daily_demand,
            product_mix_count, recommendation
        )
        
        # Calculate manpower estimates
        manpower_estimates = {
            "cell": RecommendationService._estimate_workers("cell", theoretical_min_stations) 
                    if scores["cell"]["feasible"] else None,
            "short_line": RecommendationService._estimate_workers("short_line", theoretical_min_stations) 
                          if scores["short_line"]["feasible"] else None,
            "long_line": RecommendationService._estimate_workers("long_line", theoretical_min_stations) 
                         if scores["long_line"]["feasible"] else None
        }
        
        # Generate warnings
        warnings = RecommendationService._generate_warnings(
            tasks_df, theoretical_min_stations, target_takt,
            complexity_dist, recommendation
        )
        
        # Generate recommendations
        recommendations = RecommendationService._generate_recommendations(
            recommendation, tasks_df, complexity_dist
        )
        
        # NEW: Validate constraints
        constraints_check = RecommendationService._validate_constraints(
            recommendation, theoretical_min_stations,
            available_space_sqm, multi_skill_worker_count,
            quality_target_dppm, is_new_product
        )
        
        # NEW: Calculate cost analysis
        cost_analysis = RecommendationService._calculate_cost_analysis(
            recommendation, theoretical_min_stations,
            target_takt, daily_demand
        )
        
        # NEW: Calculate risk assessment
        risk_assessment = RecommendationService._calculate_risk_assessment(
            recommendation, theoretical_min_stations,
            complexity_dist, tasks_df
        )
        
        # NEW: Calculate implementation effort
        implementation = RecommendationService._calculate_implementation_effort(
            recommendation, theoretical_min_stations, is_new_product
        )
        
        # NEW: Generate scenario comparison
        scenario_comparison = RecommendationService._generate_scenario_comparison(
            tasks_df, target_takt, theoretical_min_stations,
            demand_variability_pct
        )
        
        # NEW Phase 2.1: Validate equipment
        equipment_check = RecommendationService._validate_equipment(
            recommendation, equipment_available
        )
        
        # NEW Phase 2.1: Get historical accuracy
        historical_accuracy = RecommendationService._get_historical_accuracy(
            product_family, recommendation
        )
        
        # NEW Phase 2.1: Calculate confidence interval
        confidence_interval = RecommendationService._calculate_confidence_interval(
            confidence, historical_accuracy,
            constraints_check.get("passed", True)
        )
        
        return {
            "recommended_type": recommendation,
            "confidence": round(confidence, 2),
            "confidence_interval": confidence_interval,
            "historical_accuracy": historical_accuracy,
            "reasoning": {
                "task_count": task_count,
                "total_work_ms": int(total_work),
                "target_takt_ms": target_takt,
                "theoretical_min_stations": theoretical_min_stations,
                "recommended_stations": theoretical_min_stations,
                "complexity_distribution": complexity_dist,
                "decision_factors": decision_factors
            },
            "alternatives": [
                {
                    "type": line_type,
                    "feasible": data["feasible"],
                    "suitability": round(data["score"], 2),
                    "reason": data["reason"],
                    "estimated_workers": manpower_estimates.get(line_type),
                    "estimated_efficiency": data.get("efficiency")
                }
                for line_type, data in scores.items()
            ],
            "manpower_estimates": manpower_estimates,
            "warnings": warnings,
            "recommendations": recommendations,
            # NEW fields
            "constraints_check": constraints_check,
            "equipment_check": equipment_check,
            "cost_analysis": cost_analysis,
            "risk_assessment": risk_assessment,
            "implementation": implementation,
            "scenario_comparison": scenario_comparison
        }
    
    @staticmethod
    def _calculate_line_type_scores(
        task_count: int,
        theoretical_min_stations: int,
        daily_demand: Optional[int],
        product_mix_count: Optional[int],
        optimization_goal: str,
        complexity_dist: Dict[str, int]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Calculate suitability scores for each line type.
        
        Factors considered:
        1. Task count alignment with line type range
        2. Theoretical stations vs line type station range
        3. Daily demand matching
        4. Product mix (high mix favors cell)
        5. Optimization goal preference
        """
        scores = {}
        
        for line_type in ["cell", "short_line", "long_line"]:
            score = 0.5  # Base score
            feasible = True
            reasons = []
            
            # Factor 1: Station count alignment
            if line_type == "cell":
                if theoretical_min_stations <= 3:
                    score += 0.3
                    reasons.append("Station count fits cell range (1-3)")
                else:
                    feasible = False
                    reasons.append(f"Would require {theoretical_min_stations} stations; exceeds cell max (3)")
            elif line_type == "short_line":
                if 4 <= theoretical_min_stations <= 8:
                    score += 0.3
                    reasons.append("Station count optimal for short_line (4-8)")
                elif theoretical_min_stations < 4:
                    score += 0.1
                    reasons.append("Could work but underutilizes short_line capacity")
                elif theoretical_min_stations > 8:
                    score -= 0.1
                    reasons.append("Station count exceeds short_line typical range")
            else:  # long_line
                if theoretical_min_stations >= 9:
                    score += 0.3
                    reasons.append("Station count matches long_line range (9+)")
                else:
                    score -= 0.2
                    reasons.append("Overkill for current station requirement")
            
            # Factor 2: Task count alignment
            if line_type == "cell" and task_count < 20:
                score += 0.1
            elif line_type == "short_line" and 20 <= task_count <= 50:
                score += 0.1
            elif line_type == "long_line" and task_count > 50:
                score += 0.1
            
            # Factor 3: Daily demand
            if daily_demand:
                if line_type == "cell" and daily_demand < 50:
                    score += 0.15
                    reasons.append(f"Low demand ({daily_demand}/day) suits cell flexibility")
                elif line_type == "short_line" and 50 <= daily_demand <= 200:
                    score += 0.15
                    reasons.append(f"Demand ({daily_demand}/day) matches short_line capacity")
                elif line_type == "long_line" and daily_demand > 200:
                    score += 0.15
                    reasons.append(f"High demand ({daily_demand}/day) justifies long_line")
            
            # Factor 4: Product mix
            if product_mix_count:
                if line_type == "cell" and product_mix_count > 10:
                    score += 0.1
                    reasons.append("High product mix benefits from cell flexibility")
                elif line_type == "long_line" and product_mix_count <= 3:
                    score += 0.1
                    reasons.append("Low product mix enables long_line specialization")
            
            # Factor 5: Optimization goal preference
            if optimization_goal == "min_stations" and line_type == "cell":
                score += 0.05
            elif optimization_goal == "min_manpower" and line_type == "long_line":
                score += 0.05
            elif optimization_goal == "min_idle" and line_type == "short_line":
                score += 0.05
            
            # Calculate efficiency estimate
            if feasible:
                efficiency = 0.7 + (score - 0.5) * 0.3
            else:
                efficiency = None
            
            scores[line_type] = {
                "score": min(score, 1.0),
                "feasible": feasible,
                "reason": reasons[0] if reasons else "Standard fit",
                "efficiency": round(efficiency, 2) if efficiency else None
            }
        
        return scores
    
    @staticmethod
    def _build_decision_factors(
        task_count: int,
        theoretical_min_stations: int,
        daily_demand: Optional[int],
        product_mix_count: Optional[int],
        recommendation: str
    ) -> List[str]:
        """Build human-readable decision factors."""
        factors = []
        
        if recommendation == "cell":
            factors.append(f"Task count ({task_count}) fits cell range (<20)")
            factors.append(f"Theoretical {theoretical_min_stations} stations within cell max (3)")
        elif recommendation == "short_line":
            factors.append(f"Task count ({task_count}) fits short_line range (20-50)")
            factors.append(f"Theoretical {theoretical_min_stations} stations within short_line definition (4-8)")
        else:
            factors.append(f"Task count ({task_count}) requires long_line (>50 tasks)")
            factors.append(f"Theoretical {theoretical_min_stations} stations matches long_line (9+)")
        
        if daily_demand:
            factors.append(f"Daily demand ({daily_demand}) matches {recommendation} capacity")
        
        if product_mix_count:
            mix_level = "high" if product_mix_count > 10 else "low"
            factors.append(f"{mix_level.capitalize()} product mix ({product_mix_count} SKUs)")
        
        return factors
    
    @staticmethod
    def _generate_warnings(
        tasks_df: pd.DataFrame,
        theoretical_min_stations: int,
        target_takt: int,
        complexity_dist: Dict[str, int],
        recommendation: str
    ) -> List[str]:
        """Generate warnings for potential issues."""
        warnings = []
        
        # Check for complex task concentration
        complex_count = complexity_dist.get("complex", 0) + complexity_dist.get("super_complex", 0)
        if complex_count > theoretical_min_stations:
            warnings.append(
                f"{complex_count} complex tasks may create bottleneck at single station"
            )
        
        # Check for tasks exceeding takt
        over_takt = tasks_df[tasks_df['duration'] > target_takt]
        if len(over_takt) > 0:
            warnings.append(
                f"{len(over_takt)} task(s) exceed target takt - may need splitting"
            )
        
        # Check for offline task ratio
        if 'offline_flag' in tasks_df.columns:
            offline_count = tasks_df['offline_flag'].sum()
            if offline_count > len(tasks_df) * 0.3:
                warnings.append(
                    f"High offline task ratio ({offline_count}/{len(tasks_df)}) - consider parallel processing"
                )
        
        return warnings
    
    @staticmethod
    def _estimate_workers(line_type: str, theoretical_min_stations: int) -> int:
        """Estimate worker count based on line type and stations."""
        if line_type == "cell":
            return theoretical_min_stations  # 1 worker per station, flexible
        elif line_type == "short_line":
            return theoretical_min_stations  # Dedicated workers
        else:  # long_line
            return int(theoretical_min_stations * 1.2)  # Specialized + backup
    
    @staticmethod
    def _generate_recommendations(
        recommendation: str,
        tasks_df: pd.DataFrame,
        complexity_dist: Dict[str, int]
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []
        
        task_count = len(tasks_df)
        
        if recommendation == "cell":
            recommendations.append("Use cell configuration for maximum flexibility")
            if task_count > 15:
                recommendations.append("Consider splitting into 2 cells if demand increases")
        elif recommendation == "short_line":
            stations = max(4, min(8, math.ceil(task_count / 6)))
            recommendations.append(f"Use short line with {stations} stations")
        else:
            recommendations.append("Use long line for high-volume production")
            recommendations.append("Assign specialized workers to complex tasks")
        
        # Check for offline tasks
        if 'offline_flag' in tasks_df.columns:
            offline_count = tasks_df['offline_flag'].sum()
            if offline_count > 0:
                recommendations.append(f"Consider offline processing for {offline_count} offline tasks")
        
        # Check for similar action types
        if 'action_type' in tasks_df.columns:
            action_counts = tasks_df['action_type'].value_counts()
            for action, count in action_counts.items():
                if count >= 3:
                    recommendations.append(f"Group similar {action} operations to reduce transitions")
                    break
        
        return recommendations
    
    @staticmethod
    def _validate_constraints(
        line_type: str,
        theoretical_min_stations: int,
        available_space_sqm: Optional[float],
        multi_skill_worker_count: Optional[int],
        quality_target_dppm: Optional[int],
        is_new_product: bool
    ) -> Dict[str, Any]:
        """
        Validate physical and organizational constraints for each line type.
        
        Returns:
            Dict with pass/fail status for each constraint type
        """
        # Space requirements per line type (sqm per station)
        SPACE_PER_STATION = {
            "cell": 6.0,      # Compact, multi-purpose
            "short_line": 8.0, # Dedicated stations
            "long_line": 10.0  # Full equipment + buffers
        }
        
        # Quality capability per line type (achievable DPPM)
        QUALITY_CAPABILITY = {
            "cell": 800,       # Higher due to flexibility
            "short_line": 500, # Better process control
            "long_line": 300   # Best process consistency
        }
        
        # Skill requirements
        SKILL_REQUIREMENTS = {
            "cell": {"multi_skill_min_ratio": 0.8},  # Cell needs multi-skilled workers
            "short_line": {"multi_skill_min_ratio": 0.3},
            "long_line": {"multi_skill_min_ratio": 0.1}
        }
        
        constraints_result = {
            "passed": True,
            "details": {}
        }
        
        # Check space constraint
        if available_space_sqm is not None:
            required_space = theoretical_min_stations * SPACE_PER_STATION[line_type]
            space_ok = available_space_sqm >= required_space
            constraints_result["details"]["space"] = {
                "passed": space_ok,
                "required_sqm": required_space,
                "available_sqm": available_space_sqm,
                "message": f"Space {'sufficient' if space_ok else 'insufficient'}: need {required_space:.1f} sqm, have {available_space_sqm:.1f} sqm"
            }
            if not space_ok:
                constraints_result["passed"] = False
        
        # Check skill availability
        if multi_skill_worker_count is not None:
            required_ratio = SKILL_REQUIREMENTS[line_type]["multi_skill_min_ratio"]
            required_multi_skill = int(theoretical_min_stations * required_ratio)
            skill_ok = multi_skill_worker_count >= required_multi_skill
            constraints_result["details"]["skill"] = {
                "passed": skill_ok,
                "required_multi_skill": required_multi_skill,
                "available_multi_skill": multi_skill_worker_count,
                "message": f"Multi-skill workers {'sufficient' if skill_ok else 'insufficient'}: need {required_multi_skill}, have {multi_skill_worker_count}"
            }
            if not skill_ok:
                constraints_result["passed"] = False
        
        # Check quality capability
        if quality_target_dppm is not None:
            achievable = QUALITY_CAPABILITY[line_type]
            quality_ok = achievable <= quality_target_dppm
            constraints_result["details"]["quality"] = {
                "passed": quality_ok,
                "target_dppm": quality_target_dppm,
                "achievable_dppm": achievable,
                "message": f"Quality target {'achievable' if quality_ok else 'may be difficult'}: {line_type} typically achieves {achievable} DPPM"
            }
            if not quality_ok:
                constraints_result["passed"] = False
        
        # Check NPI suitability
        if is_new_product:
            npi_suitable = line_type in ["cell", "short_line"]
            constraints_result["details"]["npi"] = {
                "passed": npi_suitable,
                "message": f"{'Suitable' if npi_suitable else 'Not recommended'} for NPI: {line_type} {'allows' if npi_suitable else 'limits'} process refinement"
            }
            if not npi_suitable:
                constraints_result["passed"] = False
        
        return constraints_result
    
    @staticmethod
    def _calculate_cost_analysis(
        line_type: str,
        theoretical_min_stations: int,
        target_takt: int,
        daily_demand: Optional[int]
    ) -> Dict[str, Any]:
        """
        Calculate cost comparison for different line types.
        
        Returns:
            Dict with cost breakdown and comparison
        """
        # Base costs per station (example values - should be configurable)
        LABOR_COST_PER_HOUR = {
            "cell": 25.0,       # Multi-skilled = higher wage
            "short_line": 22.0,
            "long_line": 20.0
        }
        
        OVERHEAD_RATE = {
            "cell": 1.2,       # Lower overhead
            "short_line": 1.4,
            "long_line": 1.6   # Higher overhead (equipment, space)
        }
        
        EQUIPMENT_COST_PER_STATION = {
            "cell": 5000,       # Minimal dedicated equipment
            "short_line": 8000,
            "long_line": 12000
        }
        
        workers = theoretical_min_stations
        if line_type == "long_line":
            workers = int(workers * 1.2)  # Buffer staff
        
        # Daily operating cost
        hours_per_day = 8
        labor_daily = workers * LABOR_COST_PER_HOUR[line_type] * hours_per_day
        overhead_daily = labor_daily * (OVERHEAD_RATE[line_type] - 1)
        total_daily = labor_daily + overhead_daily
        
        # Cost per unit
        if daily_demand and daily_demand > 0:
            cost_per_unit = total_daily / daily_demand
        else:
            # Estimate from takt time
            units_per_day = (hours_per_day * 3600 * 1000) // target_takt
            cost_per_unit = total_daily / max(1, units_per_day)
            daily_demand = units_per_day
        
        # Annual cost
        working_days = 250
        annual_operating = total_daily * working_days
        equipment_amortized = (theoretical_min_stations * EQUIPMENT_COST_PER_STATION[line_type]) / 5  # 5-year amortization
        annual_total = annual_operating + equipment_amortized
        
        return {
            "cost_per_unit": round(cost_per_unit, 2),
            "daily_labor_cost": round(labor_daily, 2),
            "daily_overhead": round(overhead_daily, 2),
            "daily_total": round(total_daily, 2),
            "annual_operating_cost": round(annual_operating, 2),
            "equipment_cost_annual": round(equipment_amortized, 2),
            "annual_total": round(annual_total, 2),
            "workers_required": workers
        }
    
    @staticmethod
    def _calculate_risk_assessment(
        line_type: str,
        theoretical_min_stations: int,
        complexity_dist: Dict[str, int],
        tasks_df: pd.DataFrame
    ) -> Dict[str, Any]:
        """
        Assess operational risks for each line type.
        
        Returns:
            Dict with risk scores and descriptions
        """
        risks = []
        total_risk_score = 0
        
        # Bottleneck risk (complex task concentration)
        complex_count = complexity_dist.get("complex", 0) + complexity_dist.get("super_complex", 0)
        if complex_count > 0:
            bottleneck_risk = min(1.0, complex_count / theoretical_min_stations)
            if line_type == "cell":
                bottleneck_risk *= 0.7  # Cells can redistribute work
            total_risk_score += bottleneck_risk * 30
            if bottleneck_risk > 0.5:
                risks.append({
                    "type": "bottleneck",
                    "severity": "high" if bottleneck_risk > 0.8 else "medium",
                    "description": f"{complex_count} complex tasks may cause bottlenecks"
                })
        
        # Single point of failure risk
        if line_type == "long_line":
            spof_risk = 0.6  # Long lines have high SPOF
            total_risk_score += spof_risk * 25
            risks.append({
                "type": "single_point_of_failure",
                "severity": "medium",
                "description": "Long line has sequential dependency - one station failure stops all"
            })
        elif line_type == "short_line":
            spof_risk = 0.4
            total_risk_score += spof_risk * 25
        else:
            spof_risk = 0.2  # Cells are most resilient
            total_risk_score += spof_risk * 25
        
        # Quality risk based on line type
        QUALITY_RISK = {"cell": 0.4, "short_line": 0.25, "long_line": 0.2}
        quality_risk = QUALITY_RISK[line_type]
        total_risk_score += quality_risk * 20
        
        # Flexibility score (inverse of risk)
        FLEXIBILITY = {"cell": 0.9, "short_line": 0.6, "long_line": 0.3}
        flexibility = FLEXIBILITY[line_type]
        
        # Normalize risk score to 0-100
        total_risk_score = min(100, total_risk_score)
        
        return {
            "overall_risk_score": round(total_risk_score, 1),
            "risk_level": "high" if total_risk_score > 60 else ("medium" if total_risk_score > 30 else "low"),
            "flexibility_score": flexibility,
            "identified_risks": risks,
            "spof_risk": round(spof_risk, 2),
            "quality_risk": round(quality_risk, 2)
        }
    
    @staticmethod
    def _calculate_implementation_effort(
        line_type: str,
        theoretical_min_stations: int,
        is_new_product: bool
    ) -> Dict[str, Any]:
        """
        Estimate implementation effort for each line type.
        
        Returns:
            Dict with setup time, training, and space requirements
        """
        # Base setup days per station
        SETUP_DAYS_PER_STATION = {
            "cell": 2,        # Quick to set up
            "short_line": 3,
            "long_line": 5    # More equipment, more complex
        }
        
        # Training days per worker
        TRAINING_DAYS = {
            "cell": 10,       # Multi-skill training takes longer
            "short_line": 5,
            "long_line": 3    # Specialized single-task training
        }
        
        # Space per station (sqm)
        SPACE_PER_STATION = {
            "cell": 6,
            "short_line": 8,
            "long_line": 10
        }
        
        setup_days = theoretical_min_stations * SETUP_DAYS_PER_STATION[line_type]
        if is_new_product:
            setup_days = int(setup_days * 1.5)  # NPI needs more setup time
        
        workers = theoretical_min_stations
        if line_type == "long_line":
            workers = int(workers * 1.2)
        
        training_days = TRAINING_DAYS[line_type]
        if is_new_product:
            training_days = int(training_days * 1.3)
        
        space_required = theoretical_min_stations * SPACE_PER_STATION[line_type]
        
        return {
            "setup_days": setup_days,
            "training_days_per_worker": training_days,
            "total_training_effort": training_days * workers,
            "space_required_sqm": space_required,
            "workers_to_train": workers,
            "estimated_go_live_days": setup_days + training_days,
            "npi_adjustment_applied": is_new_product
        }
    
    @staticmethod
    def _generate_scenario_comparison(
        tasks_df: pd.DataFrame,
        target_takt: int,
        theoretical_min_stations: int,
        demand_variability_pct: Optional[float]
    ) -> Dict[str, Any]:
        """
        Generate what-if scenario comparisons.
        
        Returns:
            Dict with scenarios for demand variations
        """
        scenarios = {}
        
        # Base scenario
        base_demand = (8 * 3600 * 1000) // target_takt  # 8-hour day
        
        # Define variation percentages
        variations = [
            ("demand_down_20", -0.2, "20% demand decrease"),
            ("demand_up_20", 0.2, "20% demand increase"),
            ("demand_up_50", 0.5, "50% demand increase")
        ]
        
        if demand_variability_pct:
            variations.append(
                ("expected_variation", demand_variability_pct / 100, f"Expected {demand_variability_pct}% variation")
            )
        
        for scenario_key, variation, description in variations:
            adjusted_demand = int(base_demand * (1 + variation))
            adjusted_takt = (8 * 3600 * 1000) // adjusted_demand if adjusted_demand > 0 else target_takt
            
            # Determine best line type for this scenario
            if adjusted_takt > target_takt * 1.3:
                recommended = "cell"  # Lower demand = smaller setup
            elif adjusted_takt < target_takt * 0.8:
                recommended = "long_line"  # Higher demand = scale up
            else:
                recommended = "short_line"
            
            scenarios[scenario_key] = {
                "description": description,
                "adjusted_daily_demand": adjusted_demand,
                "adjusted_takt_ms": adjusted_takt,
                "recommended_line_type": recommended,
                "stations_needed": max(1, math.ceil(theoretical_min_stations * (1 + variation * 0.5)))
            }
        
        return {
            "base_demand": base_demand,
            "base_takt": target_takt,
            "scenarios": scenarios,
            "recommendation": "Consider flexible line design if high variability expected" if demand_variability_pct and demand_variability_pct > 30 else "Current recommendation stable across scenarios"
        }
    
    @staticmethod
    def _validate_equipment(
        line_type: str,
        equipment_available: Optional[List[str]]
    ) -> Dict[str, Any]:
        """
        Validate equipment availability for each line type.
        
        Returns:
            Dict with equipment feasibility and missing items
        """
        # Equipment requirements per line type
        EQUIPMENT_REQUIREMENTS = {
            "cell": {
                "required": ["flexible_tooling"],
                "optional": ["multi_purpose_fixture", "portable_tools"]
            },
            "short_line": {
                "required": ["conveyor", "dedicated_fixture"],
                "optional": ["auto_screwdriver", "barcode_scanner"]
            },
            "long_line": {
                "required": ["conveyor", "agv", "automated_station"],
                "optional": ["vision_system", "robotic_arm", "plc_controller"]
            }
        }
        
        if equipment_available is None:
            return {
                "passed": True,
                "check_skipped": True,
                "message": "Equipment check skipped - no equipment list provided"
            }
        
        required = set(EQUIPMENT_REQUIREMENTS[line_type]["required"])
        available = set(equipment_available)
        missing = required - available
        
        # Check optional equipment
        optional = set(EQUIPMENT_REQUIREMENTS[line_type]["optional"])
        optional_available = optional & available
        
        return {
            "passed": len(missing) == 0,
            "required_equipment": list(required),
            "available_equipment": equipment_available,
            "missing_equipment": list(missing),
            "optional_available": list(optional_available),
            "optional_missing": list(optional - available),
            "message": f"Equipment {'sufficient' if len(missing) == 0 else 'insufficient'}: missing {list(missing)}" if missing else "All required equipment available"
        }
    
    @staticmethod
    def _get_historical_accuracy(
        product_family: Optional[str],
        line_type: str
    ) -> Dict[str, Any]:
        """
        Query historical recommendation accuracy for similar products.
        
        In production, this would query from database.
        Returns learning from past recommendations.
        """
        if product_family is None:
            return {
                "available": False,
                "message": "No product family specified - historical lookup skipped"
            }
        
        # TODO: In production, query from database
        # SELECT * FROM recommendation_history 
        # WHERE product_family = ? AND recommended_type = ?
        # ORDER BY created_at DESC LIMIT 100
        
        # Mock historical data (replace with actual DB query)
        HISTORICAL_DATA = {
            "DL360": {
                "past_recommendations": 15,
                "accuracy_rate": 0.82,
                "common_override_reason": "space_constraint",
                "successful_types": {"cell": 2, "short_line": 10, "long_line": 3},
                "last_recommendation_date": "2025-11-28"
            },
            "ML350": {
                "past_recommendations": 8,
                "accuracy_rate": 0.88,
                "common_override_reason": "worker_availability",
                "successful_types": {"cell": 5, "short_line": 3, "long_line": 0},
                "last_recommendation_date": "2025-12-05"
            },
            "DL320": {
                "past_recommendations": 12,
                "accuracy_rate": 0.75,
                "common_override_reason": "quality_requirement",
                "successful_types": {"cell": 8, "short_line": 2, "long_line": 2},
                "last_recommendation_date": "2025-12-01"
            }
        }
        
        if product_family in HISTORICAL_DATA:
            data = HISTORICAL_DATA[product_family]
            type_success = data["successful_types"].get(line_type, 0)
            total = sum(data["successful_types"].values())
            type_accuracy = type_success / total if total > 0 else 0
            
            return {
                "available": True,
                "product_family": product_family,
                "past_recommendations": data["past_recommendations"],
                "accuracy_rate": data["accuracy_rate"],
                "type_specific_accuracy": round(type_accuracy, 2),
                "common_override_reason": data["common_override_reason"],
                "last_recommendation_date": data["last_recommendation_date"],
                "message": f"Found {data['past_recommendations']} historical recommendations for {product_family}"
            }
        else:
            return {
                "available": False,
                "product_family": product_family,
                "message": f"No historical data found for product family '{product_family}'"
            }
    
    @staticmethod
    def _calculate_confidence_interval(
        base_confidence: float,
        historical_accuracy: Dict[str, Any],
        constraints_passed: bool,
        sample_size: int = 0
    ) -> Dict[str, Any]:
        """
        Calculate statistical confidence interval for the recommendation.
        
        Returns:
            Dict with confidence range and sample size
        """
        # Base interval width (narrower = more certain)
        base_width = 0.15
        
        # Adjust based on historical data availability
        if historical_accuracy.get("available", False):
            sample_size = historical_accuracy.get("past_recommendations", 0)
            # More samples = narrower interval
            sample_adjustment = min(0.05, sample_size * 0.002)
            base_width -= sample_adjustment
            
            # Adjust base confidence based on historical accuracy
            hist_accuracy = historical_accuracy.get("accuracy_rate", 0.5)
            confidence_adjustment = (hist_accuracy - 0.5) * 0.2  # ±10% max adjustment
            base_confidence = min(0.99, max(0.1, base_confidence + confidence_adjustment))
        
        # Widen interval if constraints not passed
        if not constraints_passed:
            base_width += 0.1
        
        # Calculate bounds
        low = max(0.0, base_confidence - base_width / 2)
        high = min(1.0, base_confidence + base_width / 2)
        
        return {
            "confidence": round(base_confidence, 2),
            "low": round(low, 2),
            "high": round(high, 2),
            "interval_width": round(high - low, 2),
            "sample_size": sample_size,
            "reliability": "high" if sample_size >= 20 else ("medium" if sample_size >= 5 else "low"),
            "message": f"Confidence {base_confidence:.0%} (range: {low:.0%} - {high:.0%}) based on {sample_size} samples"
        }
```

#### Step 2: Test Line Type Recommendation

```bash
# Test via API
curl "http://localhost:8000/recommend-line-type?work_order_id=WO_A&target_takt=30000&daily_demand=120&product_mix_count=5"

# Expected response includes:
# - recommended_type with confidence score
# - theoretical_min_stations in reasoning
# - decision_factors explaining the choice
# - feasibility flags per alternative
# - manpower_estimates per line type
# - warnings for potential issues
```

#### Step 3: Create Recommendation Feedback Service (`src/services/recommendation_feedback_service.py`)

```python
#!/usr/bin/env python3
"""
Recommendation Feedback Service
Phase 2.1 - Learning from user decisions
"""

from typing import Dict, Any, Optional, List
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy.orm import Session
from sqlalchemy import func
import uuid
import json


@dataclass
class FeedbackRequest:
    """User feedback on a recommendation"""
    recommendation_id: str
    work_order_id: str
    recommended_type: str
    user_decision: str  # "accepted" or "overridden"
    actual_type: Optional[str] = None
    override_reason: Optional[str] = None
    comments: Optional[str] = None
    user_id: Optional[str] = None


class RecommendationFeedbackService:
    """
    Service for recording and analyzing recommendation feedback.
    
    Responsibilities:
    - Record user decisions (accept/override)
    - Update accuracy metrics
    - Query historical accuracy for future recommendations
    """
    
    VALID_DECISIONS = ["accepted", "overridden"]
    VALID_OVERRIDE_REASONS = [
        "space_constraint",
        "worker_availability",
        "equipment_unavailable",
        "quality_requirement",
        "demand_change",
        "cost_constraint",
        "management_decision",
        "other"
    ]
    
    @staticmethod
    def record_feedback(
        db: Session,
        feedback: FeedbackRequest
    ) -> Dict[str, Any]:
        """
        Record user feedback on a recommendation.
        
        Args:
            db: Database session
            feedback: FeedbackRequest with user decision
        
        Returns:
            Dict with feedback_id and accuracy impact
        """
        # Validate
        if feedback.user_decision not in RecommendationFeedbackService.VALID_DECISIONS:
            raise ValueError(f"Invalid user_decision: {feedback.user_decision}")
        
        if feedback.user_decision == "overridden":
            if not feedback.actual_type:
                raise ValueError("actual_type required when user_decision is 'overridden'")
            if not feedback.override_reason:
                raise ValueError("override_reason required when user_decision is 'overridden'")
            if feedback.override_reason not in RecommendationFeedbackService.VALID_OVERRIDE_REASONS:
                raise ValueError(f"Invalid override_reason: {feedback.override_reason}")
        
        # Get previous accuracy for impact calculation
        previous_metrics = RecommendationFeedbackService.get_accuracy_metrics(
            db, product_family=None  # TODO: Extract from recommendation
        )
        
        # Update recommendation_history table
        db.execute(
            """
            UPDATE recommendation_history
            SET user_decision = :decision,
                actual_type = :actual_type,
                override_reason = :reason,
                comments = :comments,
                user_id = :user_id,
                decided_at = NOW()
            WHERE recommendation_id = :rec_id
            """,
            {
                "rec_id": feedback.recommendation_id,
                "decision": feedback.user_decision,
                "actual_type": feedback.actual_type,
                "reason": feedback.override_reason,
                "comments": feedback.comments,
                "user_id": feedback.user_id
            }
        )
        db.commit()
        
        # Get updated accuracy
        updated_metrics = RecommendationFeedbackService.get_accuracy_metrics(
            db, product_family=None
        )
        
        feedback_id = f"fb_{datetime.now().strftime('%Y%m%d')}_{uuid.uuid4().hex[:6]}"
        
        return {
            "feedback_id": feedback_id,
            "recommendation_id": feedback.recommendation_id,
            "status": "recorded",
            "accuracy_impact": {
                "previous_accuracy": previous_metrics.get("accuracy_rate", 0),
                "updated_accuracy": updated_metrics.get("accuracy_rate", 0),
                "total_recommendations": updated_metrics.get("total_recommendations", 0)
            },
            "message": "Feedback recorded. Thank you for helping improve recommendations."
        }
    
    @staticmethod
    def get_accuracy_metrics(
        db: Session,
        product_family: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get accuracy metrics, optionally filtered by product family.
        """
        if product_family:
            result = db.execute(
                "SELECT * FROM recommendation_accuracy_metrics WHERE product_family = :pf",
                {"pf": product_family}
            ).fetchone()
        else:
            # Aggregate across all families
            result = db.execute(
                """
                SELECT 
                    SUM(total_recommendations) as total_recommendations,
                    SUM(accepted_count) as accepted_count,
                    SUM(overridden_count) as overridden_count,
                    SUM(accepted_count)::DECIMAL / NULLIF(SUM(accepted_count) + SUM(overridden_count), 0) as accuracy_rate
                FROM recommendation_accuracy_metrics
                """
            ).fetchone()
        
        if result:
            return dict(result)
        return {"total_recommendations": 0, "accuracy_rate": 0}
    
    @staticmethod
    def get_recommendation_history(
        db: Session,
        product_family: Optional[str] = None,
        work_order_id: Optional[str] = None,
        decision: Optional[str] = None,
        limit: int = 50
    ) -> Dict[str, Any]:
        """
        Query historical recommendations with filters.
        """
        query = "SELECT * FROM recommendation_history WHERE 1=1"
        params = {}
        
        if product_family:
            query += " AND product_family = :pf"
            params["pf"] = product_family
        if work_order_id:
            query += " AND work_order_id = :wo"
            params["wo"] = work_order_id
        if decision:
            query += " AND user_decision = :decision"
            params["decision"] = decision
        
        query += " ORDER BY created_at DESC LIMIT :limit"
        params["limit"] = limit
        
        results = db.execute(query, params).fetchall()
        
        recommendations = [dict(r) for r in results]
        
        # Calculate summary
        accepted = sum(1 for r in recommendations if r.get("user_decision") == "accepted")
        overridden = sum(1 for r in recommendations if r.get("user_decision") == "overridden")
        
        return {
            "total_count": len(recommendations),
            "recommendations": recommendations,
            "summary": {
                "acceptance_rate": accepted / max(1, accepted + overridden),
                "top_override_reasons": RecommendationFeedbackService._count_override_reasons(recommendations)
            }
        }
    
    @staticmethod
    def _count_override_reasons(recommendations: List[Dict]) -> List[Dict]:
        """Count and rank override reasons."""
        reasons = {}
        for r in recommendations:
            reason = r.get("override_reason")
            if reason:
                reasons[reason] = reasons.get(reason, 0) + 1
        
        return sorted(
            [{"reason": k, "count": v} for k, v in reasons.items()],
            key=lambda x: x["count"],
            reverse=True
        )
```

#### Step 4: Add Feedback API Endpoints

Add to `src/api_server.py`:

```python
from services.recommendation_feedback_service import (
    RecommendationFeedbackService,
    FeedbackRequest
)

@app.post("/recommend-line-type/feedback")
async def submit_recommendation_feedback(
    feedback: FeedbackRequest,
    db: Session = Depends(get_db)
):
    """Record user decision on line type recommendation."""
    try:
        result = RecommendationFeedbackService.record_feedback(db, feedback)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/recommend-line-type/history")
async def get_recommendation_history(
    product_family: Optional[str] = None,
    work_order_id: Optional[str] = None,
    decision: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Retrieve historical recommendations and their outcomes."""
    return RecommendationFeedbackService.get_recommendation_history(
        db, product_family, work_order_id, decision, limit
    )
```

---

### 5.1 Line Type Recommendation Testing Strategy (NEW)

Comprehensive test suite for the Line Type Recommendation feature.

#### Step 1: Create Test File (`tests/test_recommendation_service.py`)

```python
#!/usr/bin/env python3
"""
Unit and Integration Tests for Line Type Recommendation Service
Phase 2.1 - Quality Assurance
"""

import pytest
import pandas as pd
import math
from typing import Dict, Any
from services.recommendation_service import RecommendationService


class TestLineTypeRecommendation:
    """Test suite for line type recommendation logic."""
    
    @pytest.fixture
    def small_task_df(self) -> pd.DataFrame:
        """12 tasks, simple complexity - should recommend cell."""
        return pd.DataFrame({
            "task_id": [f"T{i}" for i in range(1, 13)],
            "duration": [2000] * 12,  # 24000 ms total
            "complexity_level": ["simple"] * 8 + ["medium"] * 4,
            "offline_flag": [False] * 12
        })
    
    @pytest.fixture
    def medium_task_df(self) -> pd.DataFrame:
        """35 tasks, mixed complexity - should recommend short_line."""
        return pd.DataFrame({
            "task_id": [f"T{i}" for i in range(1, 36)],
            "duration": [4000] * 35,  # 140000 ms total
            "complexity_level": ["simple"] * 20 + ["medium"] * 10 + ["complex"] * 5,
            "offline_flag": [False] * 35
        })
    
    @pytest.fixture
    def large_task_df(self) -> pd.DataFrame:
        """80 tasks, high complexity - should recommend long_line."""
        return pd.DataFrame({
            "task_id": [f"T{i}" for i in range(1, 81)],
            "duration": [5000] * 80,  # 400000 ms total
            "complexity_level": ["simple"] * 30 + ["medium"] * 30 + ["complex"] * 20,
            "offline_flag": [False] * 80
        })
    
    # ==================== Core Recommendation Tests ====================
    
    def test_cell_recommendation_low_task_count(self, small_task_df):
        """12 tasks with low demand → expect cell recommendation."""
        result = RecommendationService.recommend_line_type(
            tasks_df=small_task_df,
            target_takt=30000,
            daily_demand=30
        )
        
        assert result["recommended_type"] == "cell"
        assert result["confidence"] >= 0.7
        assert result["reasoning"]["theoretical_min_stations"] <= 3
    
    def test_short_line_recommendation_medium_demand(self, medium_task_df):
        """35 tasks with medium demand → expect short_line recommendation."""
        result = RecommendationService.recommend_line_type(
            tasks_df=medium_task_df,
            target_takt=30000,
            daily_demand=100
        )
        
        assert result["recommended_type"] == "short_line"
        assert 4 <= result["reasoning"]["theoretical_min_stations"] <= 8
    
    def test_long_line_recommendation_high_demand(self, large_task_df):
        """80 tasks with high demand → expect long_line recommendation."""
        result = RecommendationService.recommend_line_type(
            tasks_df=large_task_df,
            target_takt=30000,
            daily_demand=300
        )
        
        assert result["recommended_type"] == "long_line"
        assert result["reasoning"]["theoretical_min_stations"] >= 9
    
    # ==================== Constraint Validation Tests ====================
    
    def test_space_constraint_blocks_infeasible(self, medium_task_df):
        """Insufficient space → feasible=false for larger line types."""
        result = RecommendationService.recommend_line_type(
            tasks_df=medium_task_df,
            target_takt=30000,
            available_space_sqm=30  # Very limited space
        )
        
        constraints = result["constraints_check"]
        assert constraints["details"]["space"]["passed"] == False
    
    def test_skill_constraint_affects_recommendation(self, medium_task_df):
        """Low multi-skill workers → cell less feasible."""
        result = RecommendationService.recommend_line_type(
            tasks_df=medium_task_df,
            target_takt=30000,
            multi_skill_worker_count=1  # Only 1 multi-skilled worker
        )
        
        # Cell requires high multi-skill ratio
        cell_feasibility = next(
            (a for a in result["alternatives"] if a["type"] == "cell"),
            None
        )
        # Should have warning about skill constraint
        assert any("skill" in str(result).lower() or "worker" in str(result).lower())
    
    def test_equipment_constraint_validation(self, medium_task_df):
        """Missing equipment → line type infeasible."""
        result = RecommendationService.recommend_line_type(
            tasks_df=medium_task_df,
            target_takt=30000,
            equipment_available=["flexible_tooling"]  # Only cell equipment
        )
        
        equipment_check = result["equipment_check"]
        assert equipment_check["cell"]["feasible"] == True
        assert equipment_check["long_line"]["feasible"] == False
        assert "agv" in equipment_check["long_line"]["missing_equipment"]
    
    def test_npi_favors_cell(self, medium_task_df):
        """New product introduction → cell recommended for flexibility."""
        result = RecommendationService.recommend_line_type(
            tasks_df=medium_task_df,
            target_takt=30000,
            is_new_product=True
        )
        
        # NPI should boost cell score
        cell_alt = next(a for a in result["alternatives"] if a["type"] == "cell")
        assert cell_alt["suitability"] > 0.3  # Should have reasonable score
    
    # ==================== Confidence Interval Tests ====================
    
    def test_confidence_interval_present(self, small_task_df):
        """Confidence interval should be calculated."""
        result = RecommendationService.recommend_line_type(
            tasks_df=small_task_df,
            target_takt=30000
        )
        
        ci = result["confidence_interval"]
        assert "low" in ci
        assert "high" in ci
        assert ci["low"] <= result["confidence"] <= ci["high"]
    
    def test_confidence_narrows_with_history(self, small_task_df):
        """More historical data → narrower confidence interval."""
        result = RecommendationService.recommend_line_type(
            tasks_df=small_task_df,
            target_takt=30000,
            product_family="DL360"  # Has historical data
        )
        
        ci = result["confidence_interval"]
        interval_width = ci["high"] - ci["low"]
        
        # With historical data, interval should be reasonably narrow
        assert interval_width <= 0.2
    
    # ==================== Cost Analysis Tests ====================
    
    def test_cost_analysis_present(self, medium_task_df):
        """Cost analysis should be calculated for recommended type."""
        result = RecommendationService.recommend_line_type(
            tasks_df=medium_task_df,
            target_takt=30000,
            daily_demand=100
        )
        
        cost = result["cost_analysis"]
        assert "cost_per_unit" in cost
        assert "annual_operating_cost" in cost
        assert cost["cost_per_unit"] > 0
    
    # ==================== Warning Generation Tests ====================
    
    def test_bottleneck_warning_generated(self):
        """Complex task concentration → bottleneck warning."""
        df = pd.DataFrame({
            "task_id": [f"T{i}" for i in range(1, 11)],
            "duration": [50000] * 10,  # Very long tasks
            "complexity_level": ["super_complex"] * 10  # All complex
        })
        
        result = RecommendationService.recommend_line_type(
            tasks_df=df,
            target_takt=30000
        )
        
        assert any("bottleneck" in w.lower() for w in result["warnings"])
    
    def test_over_takt_warning_generated(self):
        """Tasks exceeding takt → warning generated."""
        df = pd.DataFrame({
            "task_id": ["T1", "T2", "T3"],
            "duration": [50000, 10000, 10000]  # T1 exceeds 30s takt
        })
        
        result = RecommendationService.recommend_line_type(
            tasks_df=df,
            target_takt=30000
        )
        
        assert any("exceed" in w.lower() or "takt" in w.lower() for w in result["warnings"])


class TestRecommendationFeedback:
    """Test suite for recommendation feedback functionality."""
    
    def test_valid_feedback_accepted(self, mock_db):
        """Valid acceptance feedback should be recorded."""
        from services.recommendation_feedback_service import (
            RecommendationFeedbackService,
            FeedbackRequest
        )
        
        feedback = FeedbackRequest(
            recommendation_id="rec_test_001",
            work_order_id="WO_A",
            recommended_type="short_line",
            user_decision="accepted"
        )
        
        result = RecommendationFeedbackService.record_feedback(mock_db, feedback)
        
        assert result["status"] == "recorded"
        assert "feedback_id" in result
    
    def test_override_requires_actual_type(self, mock_db):
        """Override without actual_type should raise error."""
        from services.recommendation_feedback_service import (
            RecommendationFeedbackService,
            FeedbackRequest
        )
        
        feedback = FeedbackRequest(
            recommendation_id="rec_test_002",
            work_order_id="WO_A",
            recommended_type="short_line",
            user_decision="overridden"
            # Missing actual_type
        )
        
        with pytest.raises(ValueError, match="actual_type required"):
            RecommendationFeedbackService.record_feedback(mock_db, feedback)
    
    def test_override_requires_reason(self, mock_db):
        """Override without reason should raise error."""
        from services.recommendation_feedback_service import (
            RecommendationFeedbackService,
            FeedbackRequest
        )
        
        feedback = FeedbackRequest(
            recommendation_id="rec_test_003",
            work_order_id="WO_A",
            recommended_type="short_line",
            user_decision="overridden",
            actual_type="cell"
            # Missing override_reason
        )
        
        with pytest.raises(ValueError, match="override_reason required"):
            RecommendationFeedbackService.record_feedback(mock_db, feedback)


# ==================== Test Fixtures ====================

@pytest.fixture
def mock_db():
    """Mock database session for testing."""
    from unittest.mock import MagicMock
    return MagicMock()
```

#### Step 2: Run Tests

```bash
# Run all recommendation tests
pytest tests/test_recommendation_service.py -v

# Run with coverage
pytest tests/test_recommendation_service.py --cov=services.recommendation_service --cov-report=html

# Run specific test class
pytest tests/test_recommendation_service.py::TestLineTypeRecommendation -v

# Run specific test
pytest tests/test_recommendation_service.py::TestLineTypeRecommendation::test_cell_recommendation_low_task_count -v
```

#### Step 3: Test Coverage Requirements

| Category | Test Count | Coverage Target |
|----------|------------|----------------|
| Core recommendation logic | 3 | 100% |
| Constraint validation | 4 | 100% |
| Confidence interval | 2 | 100% |
| Cost analysis | 1 | 80% |
| Warning generation | 2 | 90% |
| Feedback recording | 3 | 100% |
| **Total** | **15** | **95%** |

---

### 5.1 Batch Recommendation Implementation (Optional Enhancement)

Implement batch processing for multiple work orders with parallel execution.

#### Step 1: Create Batch Service (`src/services/batch_recommendation_service.py`)

```python
"""
Batch recommendation service for processing multiple work orders.
"""
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
import logging

from services.recommendation_service import RecommendationService

logger = logging.getLogger(__name__)


@dataclass
class BatchWorkOrderRequest:
    """Individual work order in a batch request."""
    work_order_id: str
    # Optional per-work-order overrides
    target_takt: Optional[int] = None
    daily_demand: Optional[int] = None


@dataclass
class BatchRecommendationRequest:
    """Batch recommendation request model."""
    work_order_ids: List[str]
    common_params: Optional[Dict[str, Any]] = None
    max_parallel: int = 5  # Limit concurrent processing


class BatchRecommendationService:
    """
    Service for processing batch line type recommendations.
    
    Features:
    - Parallel processing with configurable concurrency
    - Graceful error handling per work order
    - Cache integration for deduplication
    - Progress tracking
    """
    
    def __init__(
        self, 
        db_session,
        cache: Optional['RecommendationCache'] = None
    ):
        self.db = db_session
        self.cache = cache
    
    def process_batch(
        self,
        request: BatchRecommendationRequest
    ) -> Dict[str, Any]:
        """
        Process multiple work orders in parallel.
        
        Args:
            request: Batch request with work order IDs
        
        Returns:
            Results with per-work-order outcomes and summary
        """
        start_time = time.time()
        results = []
        cached_count = 0
        failed_count = 0
        
        # Prepare individual requests
        work_orders = self._prepare_requests(request)
        
        # Process in parallel
        with ThreadPoolExecutor(max_workers=request.max_parallel) as executor:
            future_to_wo = {
                executor.submit(
                    self._process_single,
                    wo_id,
                    params
                ): wo_id
                for wo_id, params in work_orders.items()
            }
            
            for future in as_completed(future_to_wo):
                wo_id = future_to_wo[future]
                try:
                    result = future.result()
                    results.append(result)
                    if result.get("from_cache"):
                        cached_count += 1
                except Exception as e:
                    logger.error(f"Failed to process {wo_id}: {e}")
                    results.append({
                        "work_order_id": wo_id,
                        "error": str(e),
                        "status": "failed"
                    })
                    failed_count += 1
        
        total_time = (time.time() - start_time) * 1000
        
        return {
            "results": results,
            "summary": {
                "total": len(work_orders),
                "succeeded": len(work_orders) - failed_count,
                "failed": failed_count,
                "total_processing_time_ms": round(total_time)
            },
            "cached_count": cached_count
        }
    
    def _prepare_requests(
        self,
        request: BatchRecommendationRequest
    ) -> Dict[str, Dict]:
        """Prepare individual request parameters."""
        work_orders = {}
        common = request.common_params or {}
        
        for wo_id in request.work_order_ids:
            params = {
                "work_order_id": wo_id,
                **common
            }
            work_orders[wo_id] = params
        
        return work_orders
    
    def _process_single(
        self,
        work_order_id: str,
        params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Process a single work order."""
        start = time.time()
        
        # Check cache first
        if self.cache:
            cached = self.cache.get_cached_recommendation(params)
            if cached:
                return {
                    **cached,
                    "work_order_id": work_order_id,
                    "from_cache": True,
                    "processing_time_ms": 0
                }
        
        # Load tasks for work order
        tasks_df, precedences_df = self._load_work_order_data(work_order_id)
        
        # Generate recommendation
        result = RecommendationService.recommend(
            tasks_df=tasks_df,
            precedences_df=precedences_df,
            **params
        )
        
        # Cache result
        if self.cache:
            self.cache.cache_recommendation(params, result)
        
        processing_time = (time.time() - start) * 1000
        
        return {
            "work_order_id": work_order_id,
            "recommended_type": result["recommended_type"],
            "confidence_score": result["confidence_score"],
            "processing_time_ms": round(processing_time),
            "from_cache": False
        }
    
    def _load_work_order_data(self, work_order_id: str):
        """Load task and precedence data for work order."""
        # Implementation depends on data source
        # Return (tasks_df, precedences_df)
        pass
```

#### Step 2: Add Batch API Endpoint (`src/api/recommendation_routes.py`)

```python
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from services.batch_recommendation_service import (
    BatchRecommendationService,
    BatchRecommendationRequest
)

router = APIRouter()


class BatchRequest(BaseModel):
    """Batch recommendation API request model."""
    work_order_ids: List[str]
    common_params: Optional[Dict[str, Any]] = None


@router.post("/recommend-line-type/batch")
async def batch_recommend(
    request: BatchRequest,
    db = Depends(get_db),
    cache = Depends(get_cache)
):
    """
    Generate line type recommendations for multiple work orders.
    
    - Processes in parallel for performance
    - Returns individual results and summary
    - Utilizes cache for identical parameters
    """
    if len(request.work_order_ids) > 100:
        raise HTTPException(
            status_code=400,
            detail="Maximum 100 work orders per batch"
        )
    
    if len(request.work_order_ids) == 0:
        raise HTTPException(
            status_code=400,
            detail="At least one work order required"
        )
    
    service = BatchRecommendationService(db, cache)
    batch_request = BatchRecommendationRequest(
        work_order_ids=request.work_order_ids,
        common_params=request.common_params
    )
    
    return service.process_batch(batch_request)
```

---

### 5.2 Export to PDF/Excel Implementation (Optional Enhancement)

Implement recommendation report export functionality.

#### Step 1: Create Export Service (`src/services/export_service.py`)

```python
"""
Export service for generating PDF and Excel recommendation reports.
"""
from typing import Dict, Any, Optional
from io import BytesIO
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend

# PDF generation
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, 
    Image, PageBreak
)
from reportlab.lib.units import inch

# Excel generation
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.chart import RadarChart, Reference


class RecommendationExportService:
    """
    Service for exporting recommendation reports.
    
    Supported formats:
    - PDF: Full report with charts and analysis
    - Excel: Tabular data with embedded charts
    """
    
    def __init__(self, language: str = "en"):
        self.language = language
        self.translations = self._load_translations()
    
    def export_pdf(
        self,
        recommendation: Dict[str, Any],
        include_charts: bool = True
    ) -> BytesIO:
        """
        Generate PDF report for recommendation.
        
        Args:
            recommendation: Full recommendation result
            include_charts: Whether to include comparison charts
        
        Returns:
            BytesIO buffer containing PDF content
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=72
        )
        
        styles = getSampleStyleSheet()
        story = []
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30
        )
        story.append(Paragraph(
            self._t("Line Type Recommendation Report"),
            title_style
        ))
        
        # Work Order Info
        story.append(Paragraph(
            f"Work Order: {recommendation['work_order_id']}",
            styles['Normal']
        ))
        story.append(Paragraph(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            styles['Normal']
        ))
        story.append(Spacer(1, 20))
        
        # Executive Summary
        story.append(Paragraph(
            self._t("Executive Summary"),
            styles['Heading2']
        ))
        
        rec_type = recommendation['recommended_type']
        confidence = recommendation['confidence_score']
        
        summary_data = [
            [self._t("Recommended Type"), self._format_type_name(rec_type)],
            [self._t("Confidence Score"), f"{confidence * 100:.0f}%"],
            [self._t("Confidence Interval"), 
             f"{recommendation['confidence_interval']['low']*100:.0f}% - "
             f"{recommendation['confidence_interval']['high']*100:.0f}%"],
        ]
        
        summary_table = Table(summary_data, colWidths=[2.5*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('PADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(summary_table)
        story.append(Spacer(1, 20))
        
        # Comparison Table
        story.append(Paragraph(
            self._t("Line Type Comparison"),
            styles['Heading2']
        ))
        
        comparison = recommendation['comparison']
        comp_data = [
            [self._t("Criteria"), self._t("Cell"), 
             self._t("Short Line"), self._t("Long Line")],
            [self._t("Score"), 
             f"{comparison['cell']['score']:.2f}",
             f"{comparison['short_line']['score']:.2f}",
             f"{comparison['long_line']['score']:.2f}"],
            [self._t("Efficiency"),
             f"{comparison['cell']['efficiency']*100:.0f}%",
             f"{comparison['short_line']['efficiency']*100:.0f}%",
             f"{comparison['long_line']['efficiency']*100:.0f}%"],
            [self._t("Flexibility"),
             f"{comparison['cell']['flexibility']*100:.0f}%",
             f"{comparison['short_line']['flexibility']*100:.0f}%",
             f"{comparison['long_line']['flexibility']*100:.0f}%"],
        ]
        
        comp_table = Table(comp_data, colWidths=[1.5*inch, 1.3*inch, 1.3*inch, 1.3*inch])
        comp_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#4CAF50')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(comp_table)
        story.append(Spacer(1, 20))
        
        # Charts
        if include_charts:
            chart_img = self._generate_radar_chart(comparison)
            story.append(Image(chart_img, width=4*inch, height=3*inch))
            story.append(Spacer(1, 20))
        
        # Cost Analysis
        story.append(Paragraph(
            self._t("Cost Analysis"),
            styles['Heading2']
        ))
        
        cost = recommendation['cost_analysis']
        cost_data = [
            [self._t("Cost Type"), self._t("Cell"), 
             self._t("Short Line"), self._t("Long Line")],
            [self._t("Labor"), 
             f"${cost['cell']['labor']:,.0f}",
             f"${cost['short_line']['labor']:,.0f}",
             f"${cost['long_line']['labor']:,.0f}"],
            [self._t("Equipment"),
             f"${cost['cell']['equipment']:,.0f}",
             f"${cost['short_line']['equipment']:,.0f}",
             f"${cost['long_line']['equipment']:,.0f}"],
            [self._t("Total"),
             f"${cost['cell']['total']:,.0f}",
             f"${cost['short_line']['total']:,.0f}",
             f"${cost['long_line']['total']:,.0f}"],
        ]
        
        cost_table = Table(cost_data, colWidths=[1.5*inch, 1.3*inch, 1.3*inch, 1.3*inch])
        cost_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2196F3')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(cost_table)
        story.append(Spacer(1, 20))
        
        # Constraints Check
        story.append(Paragraph(
            self._t("Constraints Validation"),
            styles['Heading2']
        ))
        
        constraints = recommendation['constraints_validation']
        for constraint_name, constraint_data in constraints.items():
            status = "✓ Pass" if constraint_data['passed'] else "✗ Fail"
            color = colors.green if constraint_data['passed'] else colors.red
            story.append(Paragraph(
                f"{constraint_name.replace('_', ' ').title()}: {status}",
                styles['Normal']
            ))
        
        story.append(Spacer(1, 20))
        
        # Warnings
        if recommendation.get('warnings'):
            story.append(Paragraph(
                self._t("Warnings"),
                styles['Heading2']
            ))
            for warning in recommendation['warnings']:
                story.append(Paragraph(
                    f"⚠️ {warning['message']}",
                    styles['Normal']
                ))
        
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def export_excel(
        self,
        recommendation: Dict[str, Any],
        include_charts: bool = True
    ) -> BytesIO:
        """
        Generate Excel report for recommendation.
        
        Args:
            recommendation: Full recommendation result
            include_charts: Whether to include comparison charts
        
        Returns:
            BytesIO buffer containing Excel content
        """
        buffer = BytesIO()
        wb = openpyxl.Workbook()
        
        # Summary Sheet
        ws_summary = wb.active
        ws_summary.title = "Summary"
        
        # Title
        ws_summary['A1'] = "Line Type Recommendation Report"
        ws_summary['A1'].font = Font(size=18, bold=True)
        ws_summary.merge_cells('A1:D1')
        
        # Work Order Info
        ws_summary['A3'] = "Work Order:"
        ws_summary['B3'] = recommendation['work_order_id']
        ws_summary['A4'] = "Generated:"
        ws_summary['B4'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Recommendation
        ws_summary['A6'] = "Recommended Type"
        ws_summary['B6'] = self._format_type_name(recommendation['recommended_type'])
        ws_summary['B6'].font = Font(size=14, bold=True, color='00AA00')
        
        ws_summary['A7'] = "Confidence Score"
        ws_summary['B7'] = f"{recommendation['confidence_score']*100:.0f}%"
        
        # Comparison Sheet
        ws_comparison = wb.create_sheet("Comparison")
        
        headers = ["Criteria", "Cell", "Short Line", "Long Line"]
        for col, header in enumerate(headers, 1):
            cell = ws_comparison.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True, color='FFFFFF')
            cell.fill = PatternFill(start_color='4CAF50', end_color='4CAF50', fill_type='solid')
        
        comparison = recommendation['comparison']
        rows = [
            ["Score", comparison['cell']['score'], 
             comparison['short_line']['score'], comparison['long_line']['score']],
            ["Efficiency", comparison['cell']['efficiency'], 
             comparison['short_line']['efficiency'], comparison['long_line']['efficiency']],
            ["Flexibility", comparison['cell']['flexibility'],
             comparison['short_line']['flexibility'], comparison['long_line']['flexibility']],
        ]
        
        for row_idx, row_data in enumerate(rows, 2):
            for col_idx, value in enumerate(row_data, 1):
                ws_comparison.cell(row=row_idx, column=col_idx, value=value)
        
        # Cost Analysis Sheet
        ws_cost = wb.create_sheet("Cost Analysis")
        
        cost_headers = ["Cost Type", "Cell", "Short Line", "Long Line"]
        for col, header in enumerate(cost_headers, 1):
            cell = ws_cost.cell(row=1, column=col, value=header)
            cell.font = Font(bold=True, color='FFFFFF')
            cell.fill = PatternFill(start_color='2196F3', end_color='2196F3', fill_type='solid')
        
        cost = recommendation['cost_analysis']
        cost_rows = [
            ["Labor", cost['cell']['labor'], 
             cost['short_line']['labor'], cost['long_line']['labor']],
            ["Equipment", cost['cell']['equipment'],
             cost['short_line']['equipment'], cost['long_line']['equipment']],
            ["Space", cost['cell']['space'],
             cost['short_line']['space'], cost['long_line']['space']],
            ["Total", cost['cell']['total'],
             cost['short_line']['total'], cost['long_line']['total']],
        ]
        
        for row_idx, row_data in enumerate(cost_rows, 2):
            for col_idx, value in enumerate(row_data, 1):
                cell = ws_cost.cell(row=row_idx, column=col_idx, value=value)
                if col_idx > 1:
                    cell.number_format = '$#,##0'
        
        wb.save(buffer)
        buffer.seek(0)
        return buffer
    
    def _generate_radar_chart(self, comparison: Dict) -> BytesIO:
        """Generate radar chart comparing line types."""
        categories = ['Efficiency', 'Flexibility', 'Quality', 'Space', 'Cost']
        
        fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
        
        angles = [n / float(len(categories)) * 2 * 3.14159 for n in range(len(categories))]
        angles += angles[:1]
        
        for line_type, color in [('cell', '#4CAF50'), ('short_line', '#2196F3'), ('long_line', '#FF9800')]:
            values = [
                comparison[line_type].get('efficiency', 0.5),
                comparison[line_type].get('flexibility', 0.5),
                comparison[line_type].get('quality', 0.5),
                comparison[line_type].get('space_score', 0.5),
                1 - comparison[line_type].get('cost_normalized', 0.5)
            ]
            values += values[:1]
            ax.plot(angles, values, 'o-', linewidth=2, label=line_type.replace('_', ' ').title(), color=color)
            ax.fill(angles, values, alpha=0.25, color=color)
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories)
        ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.0))
        
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='png', bbox_inches='tight', dpi=100)
        plt.close()
        img_buffer.seek(0)
        
        return img_buffer
    
    def _t(self, key: str) -> str:
        """Get translated string."""
        return self.translations.get(self.language, {}).get(key, key)
    
    def _format_type_name(self, type_name: str) -> str:
        """Format line type name for display."""
        names = {
            'cell': 'Cell Production',
            'short_line': 'Short Line',
            'long_line': 'Long Line'
        }
        return names.get(type_name, type_name)
    
    def _load_translations(self) -> Dict:
        """Load translation strings."""
        return {
            "en": {
                "Line Type Recommendation Report": "Line Type Recommendation Report",
                "Executive Summary": "Executive Summary",
                "Recommended Type": "Recommended Type",
                "Confidence Score": "Confidence Score",
                # ... more translations
            },
            "zh": {
                "Line Type Recommendation Report": "產線類型建議報告",
                "Executive Summary": "執行摘要",
                "Recommended Type": "建議類型",
                "Confidence Score": "信心分數",
                # ... more translations
            }
        }
```

#### Step 2: Add Export API Endpoint

```python
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse

from services.export_service import RecommendationExportService


@router.get("/recommend-line-type/export")
async def export_recommendation(
    work_order_id: str = Query(..., description="Work order ID"),
    format: str = Query("pdf", description="Export format: pdf or xlsx"),
    include_charts: bool = Query(True, description="Include comparison charts"),
    language: str = Query("en", description="Report language: en or zh"),
    db = Depends(get_db)
):
    """
    Export recommendation report as PDF or Excel.
    """
    # Validate format
    if format not in ["pdf", "xlsx"]:
        raise HTTPException(
            status_code=400,
            detail="Format must be 'pdf' or 'xlsx'"
        )
    
    # Get recommendation (from cache or regenerate)
    recommendation = await get_or_generate_recommendation(work_order_id, db)
    
    # Generate export
    export_service = RecommendationExportService(language=language)
    
    if format == "pdf":
        buffer = export_service.export_pdf(recommendation, include_charts)
        media_type = "application/pdf"
        filename = f"recommendation_{work_order_id}_{datetime.now().strftime('%Y%m%d')}.pdf"
    else:
        buffer = export_service.export_excel(recommendation, include_charts)
        media_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        filename = f"recommendation_{work_order_id}_{datetime.now().strftime('%Y%m%d')}.xlsx"
    
    return StreamingResponse(
        buffer,
        media_type=media_type,
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"'
        }
    )
```

---

### 5.3 Configurable Thresholds Implementation (Optional Enhancement)

Implement site and product-family specific threshold configuration.

#### Step 1: Create Thresholds Database Model (`src/models/thresholds.py`)

```python
"""
Database model for configurable recommendation thresholds.
"""
from sqlalchemy import Column, Integer, String, JSON, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


class RecommendationThreshold(Base):
    """
    Configurable thresholds for line type recommendation.
    
    Supports:
    - Site-specific thresholds
    - Product family-specific thresholds
    - Versioning for audit trail
    """
    __tablename__ = "recommendation_thresholds"
    
    id = Column(Integer, primary_key=True, index=True)
    site_id = Column(String(50), index=True, nullable=False)
    product_family = Column(String(50), index=True, nullable=True)  # null = site-wide
    
    # Threshold configuration (JSON)
    thresholds = Column(JSON, nullable=False)
    
    # Audit fields
    version = Column(Integer, default=1)
    reason = Column(String(500), nullable=True)
    created_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Soft delete
    is_active = Column(Boolean, default=True)


# Default thresholds template
DEFAULT_THRESHOLDS = {
    "task_count": {
        "cell_max": 20,
        "short_line_min": 15,
        "short_line_max": 50,
        "long_line_min": 40
    },
    "daily_demand": {
        "low_max": 50,
        "medium_max": 200
    },
    "quality_level": {
        "premium_threshold": 0.9,
        "standard_threshold": 0.7
    },
    "cost_weights": {
        "labor_factor": 0.4,
        "equipment_factor": 0.35,
        "space_factor": 0.15,
        "transition_factor": 0.1
    },
    "risk_weights": {
        "bottleneck_weight": 0.3,
        "spof_weight": 0.25,
        "quality_weight": 0.25,
        "flexibility_weight": 0.2
    }
}
```

#### Step 2: Create Thresholds Service (`src/services/threshold_service.py`)

```python
"""
Service for managing configurable recommendation thresholds.
"""
from typing import Dict, Any, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from models.thresholds import RecommendationThreshold, DEFAULT_THRESHOLDS


class ThresholdService:
    """
    Service for CRUD operations on recommendation thresholds.
    """
    
    @staticmethod
    def get_thresholds(
        db: Session,
        site_id: str,
        product_family: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get applicable thresholds for site/product combination.
        
        Resolution order:
        1. Product family + site specific
        2. Site-wide
        3. Default
        """
        # Try product family specific first
        if product_family:
            threshold = db.query(RecommendationThreshold).filter(
                RecommendationThreshold.site_id == site_id,
                RecommendationThreshold.product_family == product_family,
                RecommendationThreshold.is_active == True
            ).first()
            
            if threshold:
                return {
                    "site_id": site_id,
                    "product_family": product_family,
                    "thresholds": threshold.thresholds,
                    "source": "product_family_config",
                    "last_updated": threshold.updated_at.isoformat(),
                    "updated_by": threshold.created_by
                }
        
        # Try site-wide
        threshold = db.query(RecommendationThreshold).filter(
            RecommendationThreshold.site_id == site_id,
            RecommendationThreshold.product_family == None,
            RecommendationThreshold.is_active == True
        ).first()
        
        if threshold:
            return {
                "site_id": site_id,
                "product_family": product_family,
                "thresholds": threshold.thresholds,
                "source": "site_config",
                "last_updated": threshold.updated_at.isoformat(),
                "updated_by": threshold.created_by
            }
        
        # Return defaults
        return {
            "site_id": site_id,
            "product_family": product_family,
            "thresholds": DEFAULT_THRESHOLDS,
            "source": "default",
            "last_updated": None,
            "updated_by": None
        }
    
    @staticmethod
    def update_thresholds(
        db: Session,
        site_id: str,
        thresholds: Dict[str, Any],
        product_family: Optional[str] = None,
        reason: Optional[str] = None,
        updated_by: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create or update thresholds for site/product.
        
        Maintains version history.
        """
        # Get existing threshold
        existing = db.query(RecommendationThreshold).filter(
            RecommendationThreshold.site_id == site_id,
            RecommendationThreshold.product_family == product_family,
            RecommendationThreshold.is_active == True
        ).first()
        
        previous_version_id = None
        new_version = 1
        
        if existing:
            # Mark old version as inactive
            previous_version_id = f"thresh_v{existing.version}"
            new_version = existing.version + 1
            existing.is_active = False
            db.add(existing)
        
        # Create new threshold
        new_threshold = RecommendationThreshold(
            site_id=site_id,
            product_family=product_family,
            thresholds=thresholds,
            version=new_version,
            reason=reason,
            created_by=updated_by,
            is_active=True
        )
        db.add(new_threshold)
        db.commit()
        
        return {
            "status": "updated",
            "site_id": site_id,
            "product_family": product_family,
            "effective_from": datetime.utcnow().isoformat(),
            "previous_version_id": previous_version_id,
            "new_version_id": f"thresh_v{new_version}"
        }
    
    @staticmethod
    def reset_thresholds(
        db: Session,
        site_id: str,
        product_family: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Reset thresholds to defaults by deactivating custom config.
        """
        existing = db.query(RecommendationThreshold).filter(
            RecommendationThreshold.site_id == site_id,
            RecommendationThreshold.product_family == product_family,
            RecommendationThreshold.is_active == True
        ).first()
        
        if existing:
            existing.is_active = False
            db.add(existing)
            db.commit()
        
        return {
            "status": "reset_to_default",
            "site_id": site_id,
            "product_family": product_family
        }
```

#### Step 3: Add Thresholds API Endpoints

```python
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from typing import Dict, Any, Optional

from services.threshold_service import ThresholdService


class ThresholdUpdateRequest(BaseModel):
    """Threshold update request model."""
    site_id: str
    product_family: Optional[str] = None
    thresholds: Dict[str, Any]
    reason: Optional[str] = None


@router.get("/recommend-line-type/thresholds")
async def get_thresholds(
    site_id: str = Query(..., description="Site ID"),
    product_family: Optional[str] = Query(None, description="Product family"),
    db = Depends(get_db)
):
    """
    Get current thresholds for site/product combination.
    """
    return ThresholdService.get_thresholds(db, site_id, product_family)


@router.put("/recommend-line-type/thresholds")
async def update_thresholds(
    request: ThresholdUpdateRequest,
    db = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    Update thresholds for site/product combination.
    
    - Maintains version history
    - Invalidates cache for affected site
    """
    result = ThresholdService.update_thresholds(
        db=db,
        site_id=request.site_id,
        product_family=request.product_family,
        thresholds=request.thresholds,
        reason=request.reason,
        updated_by=current_user.email
    )
    
    # Invalidate cache for site
    cache = get_cache()
    cache.invalidate_by_site(request.site_id)
    
    return result


@router.delete("/recommend-line-type/thresholds")
async def reset_thresholds(
    site_id: str = Query(..., description="Site ID"),
    product_family: Optional[str] = Query(None, description="Product family"),
    db = Depends(get_db)
):
    """
    Reset thresholds to default values.
    """
    return ThresholdService.reset_thresholds(db, site_id, product_family)
```

---

### 5.4 A/B Testing Framework Implementation (Optional Enhancement)

Implement algorithm variation testing for production optimization.

#### Step 1: Create Experiment Database Model (`src/models/experiment.py`)

```python
"""
A/B Testing experiment models for recommendation algorithm variations.
"""
from sqlalchemy import Column, Integer, String, JSON, DateTime, Float, Boolean, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

from database import Base


class ExperimentStatus(enum.Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"


class Experiment(Base):
    """
    A/B Test experiment configuration.
    """
    __tablename__ = "recommendation_experiments"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(String(100), unique=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(String(1000), nullable=True)
    status = Column(Enum(ExperimentStatus), default=ExperimentStatus.DRAFT)
    
    # Variant configuration (JSON)
    variants = Column(JSON, nullable=False)
    
    # Targeting rules
    targeting = Column(JSON, nullable=True)  # site_ids, product_families
    
    # Metrics
    primary_metric = Column(String(50), default="acceptance_rate")
    secondary_metrics = Column(JSON, nullable=True)
    target_sample_size = Column(Integer, default=1000)
    
    # Results
    current_results = Column(JSON, nullable=True)
    statistical_significance = Column(JSON, nullable=True)
    
    # Winner
    winner_variant = Column(String(50), nullable=True)
    applied_to_production = Column(Boolean, default=False)
    
    # Audit
    created_by = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    concluded_at = Column(DateTime, nullable=True)


class ExperimentAssignment(Base):
    """
    Track which variant each recommendation was assigned to.
    """
    __tablename__ = "experiment_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(String(100), index=True)
    recommendation_id = Column(String(100), index=True)
    variant_id = Column(String(50))
    
    # Outcome tracking
    accepted = Column(Boolean, nullable=True)
    override_reason = Column(String(200), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### Step 2: Create A/B Testing Service (`src/services/ab_testing_service.py`)

```python
"""
A/B Testing service for recommendation algorithm experiments.
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
import hashlib
import random
from sqlalchemy.orm import Session
from scipy import stats
import numpy as np

from models.experiment import Experiment, ExperimentAssignment, ExperimentStatus


class ABTestingService:
    """
    Service for managing A/B experiments on recommendation algorithms.
    
    Features:
    - Deterministic variant assignment (same user/WO = same variant)
    - Statistical significance calculation
    - Automatic winner detection
    - Production rollout capability
    """
    
    @staticmethod
    def get_active_experiments(
        db: Session,
        site_id: Optional[str] = None,
        product_family: Optional[str] = None
    ) -> List[Experiment]:
        """Get active experiments matching targeting criteria."""
        query = db.query(Experiment).filter(
            Experiment.status == ExperimentStatus.ACTIVE
        )
        
        experiments = query.all()
        
        # Filter by targeting
        matching = []
        for exp in experiments:
            targeting = exp.targeting or {}
            
            # Check site targeting
            if targeting.get("site_ids"):
                if site_id not in targeting["site_ids"]:
                    continue
            
            # Check product family targeting
            if targeting.get("product_families"):
                if product_family not in targeting["product_families"]:
                    continue
            
            matching.append(exp)
        
        return matching
    
    @staticmethod
    def assign_variant(
        db: Session,
        experiment: Experiment,
        recommendation_id: str,
        work_order_id: str
    ) -> str:
        """
        Deterministically assign a variant based on work order ID.
        
        Uses consistent hashing to ensure same WO always gets same variant.
        """
        # Check existing assignment
        existing = db.query(ExperimentAssignment).filter(
            ExperimentAssignment.experiment_id == experiment.experiment_id,
            ExperimentAssignment.recommendation_id == recommendation_id
        ).first()
        
        if existing:
            return existing.variant_id
        
        # Deterministic assignment via consistent hashing
        hash_input = f"{experiment.experiment_id}:{work_order_id}"
        hash_value = int(hashlib.md5(hash_input.encode()).hexdigest(), 16)
        
        # Calculate cumulative traffic percentages
        variants = experiment.variants
        cumulative = 0
        hash_percent = hash_value % 100
        
        assigned_variant = variants[0]["variant_id"]  # default
        for variant in variants:
            cumulative += variant["traffic_percent"]
            if hash_percent < cumulative:
                assigned_variant = variant["variant_id"]
                break
        
        # Record assignment
        assignment = ExperimentAssignment(
            experiment_id=experiment.experiment_id,
            recommendation_id=recommendation_id,
            variant_id=assigned_variant
        )
        db.add(assignment)
        db.commit()
        
        return assigned_variant
    
    @staticmethod
    def get_variant_config(
        experiment: Experiment,
        variant_id: str
    ) -> Dict[str, Any]:
        """Get configuration overrides for a specific variant."""
        for variant in experiment.variants:
            if variant["variant_id"] == variant_id:
                return variant.get("config", {})
        return {}
    
    @staticmethod
    def record_outcome(
        db: Session,
        recommendation_id: str,
        accepted: bool,
        override_reason: Optional[str] = None
    ) -> None:
        """Record outcome for experiment assignment."""
        assignment = db.query(ExperimentAssignment).filter(
            ExperimentAssignment.recommendation_id == recommendation_id
        ).first()
        
        if assignment:
            assignment.accepted = accepted
            assignment.override_reason = override_reason
            db.add(assignment)
            db.commit()
    
    @staticmethod
    def calculate_results(
        db: Session,
        experiment_id: str
    ) -> Dict[str, Any]:
        """
        Calculate current experiment results with statistical significance.
        """
        assignments = db.query(ExperimentAssignment).filter(
            ExperimentAssignment.experiment_id == experiment_id,
            ExperimentAssignment.accepted != None
        ).all()
        
        # Group by variant
        variant_data = {}
        for a in assignments:
            if a.variant_id not in variant_data:
                variant_data[a.variant_id] = {"accepted": 0, "total": 0}
            variant_data[a.variant_id]["total"] += 1
            if a.accepted:
                variant_data[a.variant_id]["accepted"] += 1
        
        # Calculate metrics
        results = {}
        for variant_id, data in variant_data.items():
            results[variant_id] = {
                "sample_size": data["total"],
                "acceptance_rate": data["accepted"] / data["total"] if data["total"] > 0 else 0,
                "accepted_count": data["accepted"]
            }
        
        # Calculate statistical significance (chi-square test)
        significance = ABTestingService._calculate_significance(variant_data)
        
        return {
            "results": results,
            "statistical_significance": significance
        }
    
    @staticmethod
    def _calculate_significance(variant_data: Dict) -> Dict[str, Any]:
        """Calculate statistical significance using chi-square test."""
        if len(variant_data) < 2:
            return {"is_significant": False, "reason": "insufficient_variants"}
        
        variants = list(variant_data.keys())
        if any(v["total"] < 30 for v in variant_data.values()):
            return {"is_significant": False, "reason": "insufficient_sample_size"}
        
        # Build contingency table
        observed = []
        for v in variants:
            data = variant_data[v]
            observed.append([data["accepted"], data["total"] - data["accepted"]])
        
        observed = np.array(observed)
        
        try:
            chi2, p_value, dof, expected = stats.chi2_contingency(observed)
            
            return {
                "chi_square": round(chi2, 4),
                "p_value": round(p_value, 4),
                "degrees_of_freedom": dof,
                "is_significant": p_value < 0.05,
                "confidence_level": 0.95
            }
        except Exception as e:
            return {"is_significant": False, "error": str(e)}
    
    @staticmethod
    def conclude_experiment(
        db: Session,
        experiment_id: str,
        winner_variant: str,
        apply_to_production: bool = False,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Conclude experiment and optionally apply winner to production.
        """
        experiment = db.query(Experiment).filter(
            Experiment.experiment_id == experiment_id
        ).first()
        
        if not experiment:
            raise ValueError(f"Experiment {experiment_id} not found")
        
        # Calculate final results
        final_results = ABTestingService.calculate_results(db, experiment_id)
        
        # Update experiment
        experiment.status = ExperimentStatus.COMPLETED
        experiment.concluded_at = datetime.utcnow()
        experiment.winner_variant = winner_variant
        experiment.current_results = final_results["results"]
        experiment.statistical_significance = final_results["statistical_significance"]
        
        if apply_to_production:
            # Apply winner config to production thresholds
            winner_config = ABTestingService.get_variant_config(experiment, winner_variant)
            if winner_config:
                # Update production thresholds with winner config
                from services.threshold_service import ThresholdService
                targeting = experiment.targeting or {}
                for site_id in targeting.get("site_ids", ["default"]):
                    ThresholdService.update_thresholds(
                        db=db,
                        site_id=site_id,
                        thresholds=winner_config,
                        reason=f"Applied from experiment {experiment_id}"
                    )
            experiment.applied_to_production = True
        
        db.add(experiment)
        db.commit()
        
        return {
            "experiment_id": experiment_id,
            "status": "completed",
            "winner": winner_variant,
            "applied_to_production": apply_to_production,
            "final_results": final_results
        }
```

#### Step 3: Integrate A/B Testing into Recommendation Service

```python
# Add to RecommendationService.recommend()

def recommend_with_experiment(
    db: Session,
    request: LineTypeRequest,
    cache: Optional[RecommendationCache] = None
) -> Dict[str, Any]:
    """
    Generate recommendation with A/B experiment support.
    """
    recommendation_id = f"rec_{uuid.uuid4().hex[:12]}"
    
    # Check for active experiments
    experiments = ABTestingService.get_active_experiments(
        db,
        site_id=request.site_id,
        product_family=request.product_family
    )
    
    experiment_info = None
    config_overrides = {}
    
    if experiments:
        # Use first matching experiment
        experiment = experiments[0]
        variant_id = ABTestingService.assign_variant(
            db,
            experiment,
            recommendation_id,
            request.work_order_id
        )
        config_overrides = ABTestingService.get_variant_config(experiment, variant_id)
        experiment_info = {
            "experiment_id": experiment.experiment_id,
            "variant_id": variant_id
        }
    
    # Apply config overrides to recommendation logic
    result = RecommendationService.recommend(
        tasks_df=tasks_df,
        precedences_df=precedences_df,
        config_overrides=config_overrides,
        **request.dict()
    )
    
    result["recommendation_id"] = recommendation_id
    if experiment_info:
        result["experiment"] = experiment_info
    
    return result
```

---

### 5.5 Recommendation Explanation NLP Implementation (Optional Enhancement)

Generate natural language explanations for recommendations (Phase 3 preparation).

#### Step 1: Create Explanation Service (`src/services/explanation_service.py`)

```python
"""
Natural Language Explanation Service for Line Type Recommendations.
Phase 2.2 implementation with Phase 3 LLM preparation.
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
import json

# Phase 2: Template-based generation
# Phase 3: LLM-enhanced generation (OpenAI/Claude)
ENABLE_LLM = False  # Set to True in Phase 3

if ENABLE_LLM:
    from langchain.chat_models import ChatOpenAI
    from langchain.prompts import ChatPromptTemplate


class ExplanationService:
    """
    Generate human-readable explanations for recommendations.
    
    Phase 2: Template-based explanations
    Phase 3: LLM-enhanced contextual explanations
    """
    
    # Factor impact templates
    FACTOR_TEMPLATES = {
        "en": {
            "task_count": {
                "positive": "With only {value} tasks, a {rec_type} layout allows {benefit}.",
                "negative": "The {value} tasks may be challenging for a {rec_type} due to {concern}.",
                "neutral": "The task count of {value} is within acceptable range for {rec_type}."
            },
            "daily_demand": {
                "positive": "{demand_level} daily demand ({value} units) {reason}.",
                "negative": "Daily demand of {value} units {concern}."
            },
            "product_mix_count": {
                "positive": "With {value} product variants, {rec_type} production provides {benefit}.",
                "negative": "Managing {value} variants in a {rec_type} may {concern}."
            },
            "quality_target": {
                "positive": "Quality target of {value} DPPM is achievable with {rec_type} due to {reason}.",
                "negative": "Meeting {value} DPPM target may be challenging because {concern}."
            }
        },
        "zh": {
            "task_count": {
                "positive": "僅有 {value} 個任務，{rec_type} 佈局可以 {benefit}。",
                "negative": "{value} 個任務對於 {rec_type} 可能具有挑戰性，因為 {concern}。",
                "neutral": "{value} 個任務數量在 {rec_type} 的可接受範圍內。"
            },
            "daily_demand": {
                "positive": "{demand_level}日需求量（{value} 單位）{reason}。",
                "negative": "日需求量 {value} 單位 {concern}。"
            }
        }
    }
    
    AUDIENCE_STYLES = {
        "operator": {
            "tone": "simple",
            "focus": "actions",
            "technical_depth": "low"
        },
        "engineer": {
            "tone": "technical",
            "focus": "reasoning",
            "technical_depth": "medium"
        },
        "manager": {
            "tone": "business",
            "focus": "impact",
            "technical_depth": "high"
        }
    }
    
    LINE_TYPE_NAMES = {
        "en": {
            "cell": "Cell Production",
            "short_line": "Short Line",
            "long_line": "Long Line"
        },
        "zh": {
            "cell": "單元式生產",
            "short_line": "短線",
            "long_line": "長線"
        }
    }
    
    def __init__(self, language: str = "en", audience: str = "engineer"):
        self.language = language
        self.audience = audience
        self.style = self.AUDIENCE_STYLES.get(audience, self.AUDIENCE_STYLES["engineer"])
        
        if ENABLE_LLM:
            self.llm = ChatOpenAI(model="gpt-4-turbo", temperature=0.3)
    
    def generate_explanation(
        self,
        recommendation: Dict[str, Any],
        detail_level: str = "standard"
    ) -> Dict[str, Any]:
        """
        Generate complete explanation for a recommendation.
        """
        rec_type = recommendation["recommended_type"]
        confidence = recommendation["confidence_score"]
        
        # Generate summary
        summary = self._generate_summary(rec_type, confidence)
        
        # Analyze key factors
        key_factors = self._analyze_factors(recommendation)
        
        # Explain alternatives
        alternatives = self._explain_alternatives(recommendation)
        
        # Extract risks
        risks = self._extract_risks(recommendation)
        
        # Generate action items
        actions = self._generate_actions(rec_type, recommendation)
        
        explanation = {
            "summary": summary,
            "key_factors": key_factors,
            "alternatives_considered": alternatives,
            "risks_mentioned": risks,
            "action_items": actions
        }
        
        # Enhance with LLM if enabled
        if ENABLE_LLM and detail_level == "detailed":
            explanation = self._enhance_with_llm(explanation, recommendation)
        
        return {
            "work_order_id": recommendation.get("work_order_id"),
            "recommendation": {
                "type": rec_type,
                "confidence": confidence
            },
            "explanation": explanation,
            "generated_at": datetime.utcnow().isoformat(),
            "generation_model": "template" if not ENABLE_LLM else "gpt-4-turbo",
            "tokens_used": 0 if not ENABLE_LLM else self._count_tokens(explanation)
        }
    
    def _generate_summary(self, rec_type: str, confidence: float) -> str:
        """Generate executive summary."""
        type_name = self.LINE_TYPE_NAMES[self.language].get(rec_type, rec_type)
        confidence_pct = int(confidence * 100)
        
        if self.language == "en":
            return f"Based on your work order analysis, we recommend a **{type_name}** layout with {confidence_pct}% confidence."
        else:
            return f"根據您的工單分析，我們建議採用 **{type_name}** 佈局，信心度為 {confidence_pct}%。"
    
    def _analyze_factors(self, recommendation: Dict) -> List[Dict]:
        """Analyze and explain key decision factors."""
        factors = []
        comparison = recommendation.get("comparison", {})
        rec_type = recommendation["recommended_type"]
        
        # Task count factor
        task_count = recommendation.get("task_count", 0)
        if task_count > 0:
            if task_count < 20:
                impact = "positive" if rec_type == "cell" else "negative"
                benefit = "one or two skilled workers to complete the entire assembly, reducing handoff delays"
            elif task_count > 50:
                impact = "positive" if rec_type == "long_line" else "negative"
                benefit = "specialized workers to handle complex assembly sequences efficiently"
            else:
                impact = "positive" if rec_type == "short_line" else "neutral"
                benefit = "balanced workload distribution across stations"
            
            factors.append({
                "factor": "Task Count",
                "value": task_count,
                "impact": impact,
                "explanation": self._format_factor_explanation(
                    "task_count", impact, value=task_count, 
                    rec_type=self.LINE_TYPE_NAMES[self.language][rec_type],
                    benefit=benefit
                )
            })
        
        # Daily demand factor
        daily_demand = recommendation.get("daily_demand", 0)
        if daily_demand > 0:
            if daily_demand < 50:
                impact = "positive" if rec_type == "cell" else "negative"
                demand_level = "Low"
                reason = "doesn't justify the overhead of a longer production line"
            elif daily_demand > 200:
                impact = "positive" if rec_type == "long_line" else "negative"
                demand_level = "High"
                reason = "requires high-throughput configuration for efficiency"
            else:
                impact = "positive" if rec_type == "short_line" else "neutral"
                demand_level = "Moderate"
                reason = "balances flexibility with throughput requirements"
            
            factors.append({
                "factor": "Daily Demand",
                "value": daily_demand,
                "impact": impact,
                "explanation": self._format_factor_explanation(
                    "daily_demand", impact, value=daily_demand,
                    demand_level=demand_level, reason=reason
                )
            })
        
        # Product mix factor
        product_mix = recommendation.get("product_mix_count", 0)
        if product_mix > 0:
            if product_mix > 5:
                impact = "strong_positive" if rec_type == "cell" else "negative"
                benefit = "the flexibility needed for quick changeovers without reconfiguring the entire line"
            else:
                impact = "positive" if rec_type in ["short_line", "long_line"] else "neutral"
                benefit = "standardized processes across limited variants"
            
            factors.append({
                "factor": "Product Mix",
                "value": product_mix,
                "impact": impact,
                "explanation": self._format_factor_explanation(
                    "product_mix_count", impact, value=product_mix,
                    rec_type=self.LINE_TYPE_NAMES[self.language][rec_type],
                    benefit=benefit
                )
            })
        
        return factors
    
    def _explain_alternatives(self, recommendation: Dict) -> List[Dict]:
        """Explain why alternatives were not recommended."""
        alternatives = []
        rec_type = recommendation["recommended_type"]
        comparison = recommendation.get("comparison", {})
        
        for line_type in ["cell", "short_line", "long_line"]:
            if line_type == rec_type:
                continue
            
            type_data = comparison.get(line_type, {})
            score = type_data.get("score", 0)
            
            # Generate "why not" explanation
            why_not = self._generate_why_not(line_type, rec_type, type_data, recommendation)
            
            alternatives.append({
                "type": line_type,
                "score": round(score, 2),
                "why_not": why_not
            })
        
        return alternatives
    
    def _generate_why_not(
        self, 
        alt_type: str, 
        rec_type: str,
        alt_data: Dict,
        recommendation: Dict
    ) -> str:
        """Generate explanation for why an alternative wasn't chosen."""
        type_name = self.LINE_TYPE_NAMES[self.language][alt_type]
        
        # Analyze the primary disadvantage
        if alt_type == "long_line" and rec_type == "cell":
            demand = recommendation.get("daily_demand", 50)
            return f"Long line production is not recommended due to low demand volume. The line would operate at only {int(demand/200*100)}% utilization, wasting equipment and floor space."
        
        elif alt_type == "cell" and rec_type == "long_line":
            demand = recommendation.get("daily_demand", 200)
            return f"Cell production cannot meet the high demand of {demand} units/day. Multiple cells would be needed, increasing coordination complexity and floor space."
        
        elif alt_type == "short_line":
            if rec_type == "cell":
                return "A short line would require more workers (5-6) for similar output, increasing labor costs by approximately 40% without proportional efficiency gains."
            else:
                return "A short line lacks the throughput capacity needed for high-volume production, creating bottlenecks."
        
        return f"{type_name} scored lower due to suboptimal fit with current requirements."
    
    def _extract_risks(self, recommendation: Dict) -> List[str]:
        """Extract and format risk warnings."""
        risks = []
        rec_type = recommendation["recommended_type"]
        warnings = recommendation.get("warnings", [])
        
        for warning in warnings:
            risks.append(warning.get("message", str(warning)))
        
        # Add type-specific risks
        if rec_type == "cell":
            risks.append("Worker skill dependency: Ensure at least 2 cross-trained workers are available for cell operation.")
        elif rec_type == "long_line":
            risks.append("Line rigidity: Consider buffer stations for demand fluctuations.")
        
        return risks[:5]  # Limit to 5 risks
    
    def _generate_actions(self, rec_type: str, recommendation: Dict) -> List[str]:
        """Generate actionable next steps."""
        actions = []
        
        if rec_type == "cell":
            actions.extend([
                "Verify multi-skilled worker availability (minimum 2 required)",
                "Allocate 40-50 m² floor space for cell setup",
                f"Prepare flexible tooling kit for {recommendation.get('product_mix_count', 1)} product variants"
            ])
        elif rec_type == "short_line":
            actions.extend([
                "Verify 5-8 workstations available with conveyor access",
                "Train dedicated workers for each station role",
                "Set up quality checkpoints between stations"
            ])
        else:  # long_line
            actions.extend([
                "Confirm AGV/conveyor system availability",
                "Plan specialized worker training program",
                "Establish buffer inventory between zones"
            ])
        
        return actions
    
    def _format_factor_explanation(
        self, 
        factor: str, 
        impact: str, 
        **kwargs
    ) -> str:
        """Format factor explanation using templates."""
        templates = self.FACTOR_TEMPLATES.get(self.language, {})
        factor_templates = templates.get(factor, {})
        
        template = factor_templates.get(impact, factor_templates.get("neutral", ""))
        
        try:
            return template.format(**kwargs)
        except KeyError:
            return f"{factor}: {kwargs.get('value', 'N/A')}"
    
    def _enhance_with_llm(
        self, 
        explanation: Dict, 
        recommendation: Dict
    ) -> Dict:
        """Enhance explanation with LLM for detailed mode."""
        if not ENABLE_LLM:
            return explanation
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", """You are an expert manufacturing engineer explaining 
            production line recommendations. Enhance the following explanation 
            with more specific technical details and business context."""),
            ("user", f"""
            Recommendation: {recommendation['recommended_type']}
            Confidence: {recommendation['confidence_score']}
            
            Current explanation:
            {json.dumps(explanation, indent=2)}
            
            Enhance with:
            1. More specific technical reasoning
            2. Industry best practices references
            3. Potential ROI indicators
            """)
        ])
        
        response = self.llm.invoke(prompt.format_messages())
        # Parse and merge enhanced content
        return explanation  # Simplified for Phase 2
    
    def _count_tokens(self, content: Dict) -> int:
        """Estimate token count for response."""
        text = json.dumps(content)
        return len(text) // 4  # Rough estimate
```

#### Step 2: Add Explanation API Endpoint

```python
from services.explanation_service import ExplanationService


@router.get("/recommend-line-type/explain")
async def explain_recommendation(
    work_order_id: str = Query(..., description="Work order ID"),
    language: str = Query("en", description="Language: en or zh"),
    detail_level: str = Query("standard", description="brief, standard, or detailed"),
    audience: str = Query("engineer", description="operator, engineer, or manager"),
    db = Depends(get_db)
):
    """
    Generate natural language explanation for a recommendation.
    """
    # Get or generate recommendation
    recommendation = await get_or_generate_recommendation(work_order_id, db)
    
    # Generate explanation
    service = ExplanationService(language=language, audience=audience)
    explanation = service.generate_explanation(recommendation, detail_level)
    
    return explanation
```

---

### 5.6 Audit Trail Implementation (Optional Enhancement)

Track complete decision history for compliance and debugging.

#### Step 1: Create Audit Model (`src/models/audit.py`)

```python
"""
Audit trail models for recommendation tracking.
"""
from sqlalchemy import Column, Integer, String, JSON, DateTime, Text
from datetime import datetime

from database import Base


class RecommendationAuditEvent(Base):
    """
    Audit event for recommendation lifecycle tracking.
    """
    __tablename__ = "recommendation_audit_events"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String(100), unique=True, index=True)
    recommendation_id = Column(String(100), index=True)
    work_order_id = Column(String(100), index=True)
    
    # Event details
    action = Column(String(50), nullable=False)  # created, viewed, overridden, approved, applied
    actor = Column(String(100), nullable=False)  # user email or "system"
    actor_type = Column(String(20), default="user")  # user, system, api
    
    # Context
    details = Column(JSON, nullable=True)
    client_ip = Column(String(45), nullable=True)
    user_agent = Column(Text, nullable=True)
    
    # Timestamp
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)


class RecommendationSnapshot(Base):
    """
    Immutable snapshot of recommendation at creation time.
    """
    __tablename__ = "recommendation_snapshots"
    
    id = Column(Integer, primary_key=True, index=True)
    recommendation_id = Column(String(100), unique=True, index=True)
    
    # Input snapshot
    input_parameters = Column(JSON, nullable=False)
    
    # Decision factors at time of recommendation
    scores = Column(JSON, nullable=False)
    constraints_result = Column(JSON, nullable=True)
    thresholds_version = Column(String(50), nullable=True)
    algorithm_version = Column(String(20), nullable=True)
    experiment_variant = Column(String(50), nullable=True)
    
    # Compliance
    data_classification = Column(String(20), default="internal")
    retention_days = Column(Integer, default=2555)  # 7 years
    
    created_at = Column(DateTime, default=datetime.utcnow)
```

#### Step 2: Create Audit Service (`src/services/audit_service.py`)

```python
"""
Audit trail service for recommendation compliance tracking.
"""
from typing import Dict, Any, Optional, List
from datetime import datetime
import uuid
from sqlalchemy.orm import Session

from models.audit import RecommendationAuditEvent, RecommendationSnapshot


class AuditService:
    """
    Service for tracking recommendation audit trail.
    """
    
    ACTIONS = [
        "recommendation_created",
        "recommendation_viewed", 
        "recommendation_overridden",
        "recommendation_approved",
        "recommendation_applied",
        "recommendation_exported"
    ]
    
    @staticmethod
    def log_event(
        db: Session,
        recommendation_id: str,
        work_order_id: str,
        action: str,
        actor: str,
        details: Optional[Dict] = None,
        client_ip: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> str:
        """Log an audit event."""
        event_id = f"evt_{uuid.uuid4().hex[:12]}"
        
        event = RecommendationAuditEvent(
            event_id=event_id,
            recommendation_id=recommendation_id,
            work_order_id=work_order_id,
            action=action,
            actor=actor,
            actor_type="system" if actor == "system" else "user",
            details=details,
            client_ip=client_ip,
            user_agent=user_agent
        )
        
        db.add(event)
        db.commit()
        
        return event_id
    
    @staticmethod
    def create_snapshot(
        db: Session,
        recommendation_id: str,
        input_params: Dict,
        scores: Dict,
        constraints: Optional[Dict] = None,
        thresholds_version: Optional[str] = None,
        algorithm_version: str = "v2.1.0",
        experiment_variant: Optional[str] = None
    ) -> None:
        """Create immutable snapshot of recommendation."""
        snapshot = RecommendationSnapshot(
            recommendation_id=recommendation_id,
            input_parameters=input_params,
            scores=scores,
            constraints_result=constraints,
            thresholds_version=thresholds_version,
            algorithm_version=algorithm_version,
            experiment_variant=experiment_variant
        )
        
        db.add(snapshot)
        db.commit()
    
    @staticmethod
    def get_audit_trail(
        db: Session,
        recommendation_id: Optional[str] = None,
        work_order_id: Optional[str] = None,
        from_date: Optional[datetime] = None,
        to_date: Optional[datetime] = None,
        actor: Optional[str] = None
    ) -> Dict[str, Any]:
        """Retrieve audit trail for a recommendation."""
        if not recommendation_id and not work_order_id:
            raise ValueError("Either recommendation_id or work_order_id required")
        
        query = db.query(RecommendationAuditEvent)
        
        if recommendation_id:
            query = query.filter(
                RecommendationAuditEvent.recommendation_id == recommendation_id
            )
        if work_order_id:
            query = query.filter(
                RecommendationAuditEvent.work_order_id == work_order_id
            )
        if from_date:
            query = query.filter(RecommendationAuditEvent.timestamp >= from_date)
        if to_date:
            query = query.filter(RecommendationAuditEvent.timestamp <= to_date)
        if actor:
            query = query.filter(RecommendationAuditEvent.actor == actor)
        
        events = query.order_by(RecommendationAuditEvent.timestamp).all()
        
        # Get snapshot
        snapshot = None
        if recommendation_id:
            snapshot = db.query(RecommendationSnapshot).filter(
                RecommendationSnapshot.recommendation_id == recommendation_id
            ).first()
        
        return {
            "recommendation_id": recommendation_id,
            "work_order_id": work_order_id or (events[0].work_order_id if events else None),
            "audit_trail": [
                {
                    "event_id": e.event_id,
                    "timestamp": e.timestamp.isoformat(),
                    "action": e.action,
                    "actor": e.actor,
                    "details": e.details
                }
                for e in events
            ],
            "input_snapshot": {
                "captured_at": snapshot.created_at.isoformat() if snapshot else None,
                "parameters": snapshot.input_parameters if snapshot else None
            } if snapshot else None,
            "decision_factors": {
                "scores": snapshot.scores if snapshot else None,
                "constraints_at_time": snapshot.constraints_result if snapshot else None,
                "thresholds_version": snapshot.thresholds_version if snapshot else None
            } if snapshot else None,
            "compliance": {
                "retention_policy": "7_years",
                "data_classification": snapshot.data_classification if snapshot else "internal",
                "gdpr_relevant": False
            }
        }
```

#### Step 3: Add Audit API Endpoint

```python
from services.audit_service import AuditService


@router.get("/recommend-line-type/audit")
async def get_audit_trail(
    recommendation_id: Optional[str] = Query(None),
    work_order_id: Optional[str] = Query(None),
    from_date: Optional[str] = Query(None),
    to_date: Optional[str] = Query(None),
    actor: Optional[str] = Query(None),
    db = Depends(get_db)
):
    """
    Retrieve audit trail for compliance and debugging.
    """
    if not recommendation_id and not work_order_id:
        raise HTTPException(
            status_code=400,
            detail="Either recommendation_id or work_order_id is required"
        )
    
    from_dt = datetime.fromisoformat(from_date) if from_date else None
    to_dt = datetime.fromisoformat(to_date) if to_date else None
    
    return AuditService.get_audit_trail(
        db=db,
        recommendation_id=recommendation_id,
        work_order_id=work_order_id,
        from_date=from_dt,
        to_date=to_dt,
        actor=actor
    )
```

---

### 5.7 Integration Tests for Optional Enhancements

```python
# tests/test_optional_enhancements.py

import pytest
from unittest.mock import MagicMock, patch
from io import BytesIO

from services.batch_recommendation_service import BatchRecommendationService
from services.export_service import RecommendationExportService
from services.threshold_service import ThresholdService


# ==================== Batch API Tests ====================

class TestBatchRecommendation:
    """Tests for batch recommendation endpoint."""
    
    def test_batch_empty_list(self, mock_db, mock_cache):
        """Test batch with empty work order list."""
        from fastapi.testclient import TestClient
        
        response = client.post("/recommend-line-type/batch", json={
            "work_order_ids": []
        })
        
        assert response.status_code == 400
        assert "at least one" in response.json()["detail"].lower()
    
    def test_batch_exceeds_limit(self, mock_db, mock_cache):
        """Test batch exceeding 100 work order limit."""
        response = client.post("/recommend-line-type/batch", json={
            "work_order_ids": [f"WO_{i}" for i in range(101)]
        })
        
        assert response.status_code == 400
        assert "maximum 100" in response.json()["detail"].lower()
    
    def test_batch_partial_failure(self, mock_db, mock_cache):
        """Test batch with some failed work orders."""
        service = BatchRecommendationService(mock_db, mock_cache)
        
        # Mock to fail on specific work order
        with patch.object(service, '_load_work_order_data') as mock_load:
            def side_effect(wo_id):
                if wo_id == "WO_FAIL":
                    raise ValueError("Work order not found")
                return (MagicMock(), MagicMock())
            
            mock_load.side_effect = side_effect
            
            result = service.process_batch(
                BatchRecommendationRequest(
                    work_order_ids=["WO_A", "WO_FAIL", "WO_B"]
                )
            )
        
        assert result["summary"]["total"] == 3
        assert result["summary"]["failed"] == 1
        assert result["summary"]["succeeded"] == 2
    
    def test_batch_cache_hit(self, mock_db, mock_cache):
        """Test batch utilizes cache for duplicate requests."""
        mock_cache.get_cached_recommendation.return_value = {
            "recommended_type": "cell",
            "confidence_score": 0.85
        }
        
        service = BatchRecommendationService(mock_db, mock_cache)
        result = service.process_batch(
            BatchRecommendationRequest(work_order_ids=["WO_A"])
        )
        
        assert result["cached_count"] >= 1


# ==================== Export Tests ====================

class TestExportService:
    """Tests for PDF/Excel export functionality."""
    
    @pytest.fixture
    def sample_recommendation(self):
        return {
            "work_order_id": "WO_TEST",
            "recommended_type": "cell",
            "confidence_score": 0.88,
            "confidence_interval": {"low": 0.80, "high": 0.95},
            "comparison": {
                "cell": {"score": 0.88, "efficiency": 0.85, "flexibility": 0.9},
                "short_line": {"score": 0.72, "efficiency": 0.8, "flexibility": 0.6},
                "long_line": {"score": 0.65, "efficiency": 0.9, "flexibility": 0.4}
            },
            "cost_analysis": {
                "cell": {"labor": 5000, "equipment": 2000, "space": 1000, "total": 8000},
                "short_line": {"labor": 4000, "equipment": 3000, "space": 1500, "total": 8500},
                "long_line": {"labor": 3000, "equipment": 5000, "space": 2000, "total": 10000}
            },
            "constraints_validation": {
                "space_constraint": {"passed": True},
                "worker_constraint": {"passed": True}
            },
            "warnings": []
        }
    
    def test_export_pdf_generation(self, sample_recommendation):
        """Test PDF generation produces valid content."""
        service = RecommendationExportService(language="en")
        buffer = service.export_pdf(sample_recommendation, include_charts=False)
        
        assert isinstance(buffer, BytesIO)
        content = buffer.read()
        assert len(content) > 0
        assert content[:4] == b'%PDF'  # PDF magic bytes
    
    def test_export_excel_generation(self, sample_recommendation):
        """Test Excel generation produces valid content."""
        service = RecommendationExportService(language="en")
        buffer = service.export_excel(sample_recommendation, include_charts=False)
        
        assert isinstance(buffer, BytesIO)
        content = buffer.read()
        assert len(content) > 0
        # Check for XLSX magic bytes (PK header for ZIP)
        assert content[:2] == b'PK'
    
    def test_export_chinese_language(self, sample_recommendation):
        """Test export with Chinese language."""
        service = RecommendationExportService(language="zh")
        buffer = service.export_pdf(sample_recommendation, include_charts=False)
        
        assert isinstance(buffer, BytesIO)
        assert len(buffer.read()) > 0


# ==================== Thresholds API Tests ====================

class TestThresholdService:
    """Tests for configurable thresholds."""
    
    def test_get_default_thresholds(self, mock_db):
        """Test getting defaults when no custom config exists."""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = ThresholdService.get_thresholds(mock_db, "SITE_A")
        
        assert result["source"] == "default"
        assert "thresholds" in result
        assert "task_count" in result["thresholds"]
    
    def test_get_site_specific_thresholds(self, mock_db):
        """Test getting site-specific thresholds."""
        mock_threshold = MagicMock()
        mock_threshold.thresholds = {"task_count": {"cell_max": 25}}
        mock_threshold.updated_at.isoformat.return_value = "2024-01-15T10:00:00"
        mock_threshold.created_by = "admin@test.com"
        
        mock_db.query.return_value.filter.return_value.first.return_value = mock_threshold
        
        result = ThresholdService.get_thresholds(mock_db, "SITE_A")
        
        assert result["source"] == "site_config"
        assert result["thresholds"]["task_count"]["cell_max"] == 25
    
    def test_update_thresholds_creates_version(self, mock_db):
        """Test updating thresholds creates new version."""
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        result = ThresholdService.update_thresholds(
            mock_db,
            site_id="SITE_A",
            thresholds={"task_count": {"cell_max": 30}},
            reason="Test update"
        )
        
        assert result["status"] == "updated"
        assert result["new_version_id"] == "thresh_v1"
        mock_db.add.assert_called()
        mock_db.commit.assert_called()
    
    def test_reset_thresholds(self, mock_db):
        """Test resetting thresholds to default."""
        mock_existing = MagicMock()
        mock_db.query.return_value.filter.return_value.first.return_value = mock_existing
        
        result = ThresholdService.reset_thresholds(mock_db, "SITE_A")
        
        assert result["status"] == "reset_to_default"
        assert mock_existing.is_active == False


# ==================== Cache Tests ====================

class TestRecommendationCache:
    """Tests for Redis caching."""
    
    def test_cache_key_generation(self, mock_redis):
        """Test deterministic cache key generation."""
        from services.cache_service import RecommendationCache
        
        cache = RecommendationCache(mock_redis)
        
        params1 = {"work_order_id": "WO_A", "target_takt": 60}
        params2 = {"target_takt": 60, "work_order_id": "WO_A"}  # Different order
        
        key1 = cache._generate_cache_key(params1)
        key2 = cache._generate_cache_key(params2)
        
        assert key1 == key2  # Should be same despite different order
    
    def test_cache_invalidation_by_site(self, mock_redis):
        """Test cache invalidation for site."""
        from services.cache_service import RecommendationCache
        
        mock_redis.scan_iter.return_value = ["rec:abc123", "rec:def456"]
        mock_redis.get.side_effect = [
            '{"site_id": "SITE_A"}',
            '{"site_id": "SITE_B"}'
        ]
        
        cache = RecommendationCache(mock_redis)
        count = cache.invalidate_by_site("SITE_A")
        
        assert count == 1
        mock_redis.delete.assert_called_once()
```

---

### 6. Cross-Line Task Benchmark

Implement cross-line task time comparison and analysis system.

#### Step 1: Create Database Models (`src/models/benchmark.py`)

```python
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from .base import Base

class TaskExecutionRecord(Base):
    """Individual task execution record for benchmarking"""
    __tablename__ = 'task_execution_records'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    task_id = Column(String(50), nullable=False, index=True)
    task_name = Column(String(255))
    line_id = Column(String(10), nullable=False, index=True)
    worker_id = Column(String(50), index=True)
    duration_ms = Column(Integer, nullable=False)
    recorded_at = Column(DateTime, nullable=False, index=True)
    shift = Column(String(20))  # morning, afternoon, night
    work_order_id = Column(String(50), index=True)
    
    def __repr__(self):
        return f"<TaskExecution(task={self.task_id}, line={self.line_id}, duration={self.duration_ms}ms)>"


class BenchmarkReport(Base):
    """Cross-line benchmark analysis report"""
    __tablename__ = 'benchmark_reports'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    benchmark_id = Column(String(50), unique=True, nullable=False, index=True)
    status = Column(String(20), default='completed')  # generating, completed, failed
    generated_at = Column(DateTime, nullable=False)
    lines_compared = Column(JSONB, nullable=False)  # ["L1", "L2", "L3"]
    date_range_start = Column(DateTime)
    date_range_end = Column(DateTime)
    report_json = Column(JSONB, nullable=False)
    summary_json = Column(JSONB)
    
    # Configuration
    warning_threshold = Column(Float, default=10.0)
    critical_threshold = Column(Float, default=15.0)
    include_worker_analysis = Column(Boolean, default=False)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<BenchmarkReport(id={self.benchmark_id}, status={self.status})>"
```

#### Step 2: Create Benchmark Service (`src/services/benchmark_service.py`)

```python
import statistics
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from sqlalchemy.orm import Session
from models.benchmark import TaskExecutionRecord, BenchmarkReport
import uuid

@dataclass
class TaskLineStats:
    """Statistics for a task on a specific line"""
    avg_ms: float
    std_ms: float
    min_ms: float
    max_ms: float
    samples: int

@dataclass
class TaskBenchmark:
    """Benchmark result for a single task"""
    task_id: str
    task_name: str
    line_stats: Dict[str, Dict]
    best_line: str
    worst_line: str
    variance_percent: float
    severity: str
    recommendation: str


class BenchmarkService:
    """Cross-line task benchmark service"""
    
    def __init__(self, db_session: Session):
        self.db = db_session
    
    def generate_benchmark(
        self,
        line_ids: List[str],
        task_ids: Optional[List[str]] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        warning_threshold: float = 10.0,
        critical_threshold: float = 15.0,
        include_worker_analysis: bool = False
    ) -> Dict[str, Any]:
        """
        Generate cross-line benchmark report
        
        Args:
            line_ids: Lines to compare (min 2)
            task_ids: Specific tasks to analyze (None = all)
            date_from: Start date for data
            date_to: End date for data
            warning_threshold: Variance % for warning
            critical_threshold: Variance % for critical
            include_worker_analysis: Include per-worker breakdown
        
        Returns:
            Complete benchmark report
        """
        if len(line_ids) < 2:
            raise ValueError("At least 2 line IDs required for comparison")
        
        # Query execution records
        query = self.db.query(TaskExecutionRecord).filter(
            TaskExecutionRecord.line_id.in_(line_ids)
        )
        
        if task_ids:
            query = query.filter(TaskExecutionRecord.task_id.in_(task_ids))
        
        if date_from:
            query = query.filter(TaskExecutionRecord.recorded_at >= date_from)
        
        if date_to:
            query = query.filter(TaskExecutionRecord.recorded_at <= date_to)
        
        records = query.all()
        
        if not records:
            raise ValueError("No task execution data found for specified criteria")
        
        # Group records by (task_id, line_id)
        grouped = {}
        task_names = {}
        for record in records:
            key = (record.task_id, record.line_id)
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(record.duration_ms)
            task_names[record.task_id] = record.task_name or record.task_id
        
        # Analyze each task
        task_benchmarks = []
        unique_tasks = set(r.task_id for r in records)
        
        for task_id in unique_tasks:
            benchmark = self._analyze_task(
                task_id=task_id,
                task_name=task_names.get(task_id, task_id),
                grouped=grouped,
                line_ids=line_ids,
                warning_threshold=warning_threshold,
                critical_threshold=critical_threshold
            )
            if benchmark:
                task_benchmarks.append(benchmark)
        
        # Calculate summary
        summary = self._calculate_summary(task_benchmarks, line_ids)
        
        # Generate benchmark ID
        benchmark_id = f"BM-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
        
        # Build report
        report = {
            "benchmark_id": benchmark_id,
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "status": "completed",
            "lines_compared": line_ids,
            "task_benchmarks": [asdict(tb) for tb in task_benchmarks],
            "summary": summary
        }
        
        # Add worker analysis if requested
        if include_worker_analysis:
            report["worker_analysis"] = self._analyze_workers(records, line_ids)
        
        # Save to database
        self._save_report(report, warning_threshold, critical_threshold, include_worker_analysis)
        
        return report
    
    def _analyze_task(
        self,
        task_id: str,
        task_name: str,
        grouped: Dict,
        line_ids: List[str],
        warning_threshold: float,
        critical_threshold: float
    ) -> Optional[TaskBenchmark]:
        """Analyze a single task across all lines"""
        line_stats = {}
        
        for line_id in line_ids:
            key = (task_id, line_id)
            if key in grouped:
                durations = grouped[key]
                line_stats[line_id] = {
                    "avg_ms": round(statistics.mean(durations), 1),
                    "std_ms": round(statistics.stdev(durations), 1) if len(durations) > 1 else 0,
                    "min_ms": min(durations),
                    "max_ms": max(durations),
                    "samples": len(durations)
                }
        
        if len(line_stats) < 2:
            return None  # Need at least 2 lines to compare
        
        # Find best and worst lines
        sorted_lines = sorted(
            line_stats.items(),
            key=lambda x: x[1]["avg_ms"]
        )
        best_line = sorted_lines[0][0]
        worst_line = sorted_lines[-1][0]
        
        # Calculate variance
        best_avg = sorted_lines[0][1]["avg_ms"]
        worst_avg = sorted_lines[-1][1]["avg_ms"]
        variance_percent = ((worst_avg - best_avg) / best_avg) * 100 if best_avg > 0 else 0
        
        # Determine severity
        if variance_percent >= critical_threshold:
            severity = "critical"
        elif variance_percent >= warning_threshold:
            severity = "warning"
        else:
            severity = "normal"
        
        # Generate recommendation
        if severity == "critical":
            recommendation = (
                f"{worst_line} is {variance_percent:.1f}% slower than best line {best_line}. "
                f"Immediate investigation required. Check equipment, training, and work instructions."
            )
        elif severity == "warning":
            recommendation = (
                f"{worst_line} is {variance_percent:.1f}% slower than best line {best_line}. "
                f"Review work instructions and tooling."
            )
        else:
            recommendation = "Performance is consistent across lines."
        
        return TaskBenchmark(
            task_id=task_id,
            task_name=task_name,
            line_stats=line_stats,
            best_line=best_line,
            worst_line=worst_line,
            variance_percent=round(variance_percent, 1),
            severity=severity,
            recommendation=recommendation
        )
    
    def _calculate_summary(self, task_benchmarks: List[TaskBenchmark], line_ids: List[str]) -> Dict:
        """Calculate summary statistics"""
        if not task_benchmarks:
            return {}
        
        # Count by severity
        critical_count = sum(1 for tb in task_benchmarks if tb.severity == "critical")
        warning_count = sum(1 for tb in task_benchmarks if tb.severity == "warning")
        normal_count = sum(1 for tb in task_benchmarks if tb.severity == "normal")
        
        # Average variance
        avg_variance = statistics.mean(tb.variance_percent for tb in task_benchmarks)
        
        # Find overall best/worst lines
        line_scores = {lid: [] for lid in line_ids}
        for tb in task_benchmarks:
            for lid, stats in tb.line_stats.items():
                line_scores[lid].append(stats["avg_ms"])
        
        line_averages = {
            lid: statistics.mean(scores) if scores else float('inf')
            for lid, scores in line_scores.items()
        }
        best_overall = min(line_averages, key=line_averages.get)
        worst_overall = max(line_averages, key=line_averages.get)
        
        # Calculate improvement potential
        improvement_ms = 0
        for tb in task_benchmarks:
            if tb.best_line in tb.line_stats and tb.worst_line in tb.line_stats:
                best_avg = tb.line_stats[tb.best_line]["avg_ms"]
                worst_avg = tb.line_stats[tb.worst_line]["avg_ms"]
                improvement_ms += (worst_avg - best_avg)
        
        total_best_time = sum(
            tb.line_stats[tb.best_line]["avg_ms"] 
            for tb in task_benchmarks 
            if tb.best_line in tb.line_stats
        )
        improvement_percent = (improvement_ms / total_best_time * 100) if total_best_time > 0 else 0
        
        return {
            "total_tasks_compared": len(task_benchmarks),
            "high_variance_tasks": critical_count,
            "warning_variance_tasks": warning_count,
            "normal_variance_tasks": normal_count,
            "avg_cross_line_variance_percent": round(avg_variance, 1),
            "best_overall_line": best_overall,
            "worst_overall_line": worst_overall,
            "improvement_potential_percent": round(improvement_percent, 1),
            "improvement_potential_ms": int(improvement_ms)
        }
    
    def _analyze_workers(self, records: List[TaskExecutionRecord], line_ids: List[str]) -> Dict:
        """Analyze performance by worker"""
        worker_data = {}
        
        for record in records:
            if not record.worker_id:
                continue
            
            line_id = record.line_id
            worker_id = record.worker_id
            
            if line_id not in worker_data:
                worker_data[line_id] = {}
            
            if worker_id not in worker_data[line_id]:
                worker_data[line_id][worker_id] = {
                    "durations": [],
                    "tasks_completed": 0
                }
            
            worker_data[line_id][worker_id]["durations"].append(record.duration_ms)
            worker_data[line_id][worker_id]["tasks_completed"] += 1
        
        # Calculate efficiency scores
        result = {}
        for line_id, workers in worker_data.items():
            result[line_id] = {}
            line_avg = statistics.mean(
                statistics.mean(w["durations"]) for w in workers.values()
            )
            
            for worker_id, data in workers.items():
                worker_avg = statistics.mean(data["durations"])
                efficiency = (line_avg / worker_avg) * 100  # >100 = faster than average
                result[line_id][worker_id] = {
                    "avg_efficiency": round(efficiency, 1),
                    "tasks_completed": data["tasks_completed"]
                }
        
        return result
    
    def _save_report(self, report: Dict, warning_threshold: float, critical_threshold: float, include_worker: bool):
        """Save benchmark report to database"""
        db_report = BenchmarkReport(
            benchmark_id=report["benchmark_id"],
            status=report["status"],
            generated_at=datetime.utcnow(),
            lines_compared=report["lines_compared"],
            report_json=report["task_benchmarks"],
            summary_json=report["summary"],
            warning_threshold=warning_threshold,
            critical_threshold=critical_threshold,
            include_worker_analysis=include_worker
        )
        self.db.add(db_report)
        self.db.commit()
    
    def get_benchmark(self, benchmark_id: str) -> Optional[Dict]:
        """Retrieve benchmark report by ID"""
        report = self.db.query(BenchmarkReport).filter(
            BenchmarkReport.benchmark_id == benchmark_id
        ).first()
        
        if not report:
            return None
        
        return {
            "benchmark_id": report.benchmark_id,
            "status": report.status,
            "generated_at": report.generated_at.isoformat() + "Z",
            "lines_compared": report.lines_compared,
            "task_benchmarks": report.report_json,
            "summary": report.summary_json
        }
    
    def export_to_csv(self, benchmark_id: str) -> str:
        """Export benchmark report to CSV format"""
        report = self.get_benchmark(benchmark_id)
        if not report:
            raise ValueError(f"Benchmark not found: {benchmark_id}")
        
        lines = ["task_id,task_name," + ",".join(
            f"{lid}_avg_ms" for lid in report["lines_compared"]
        ) + ",best_line,worst_line,variance_percent,severity"]
        
        for tb in report["task_benchmarks"]:
            line_values = ",".join(
                str(tb["line_stats"].get(lid, {}).get("avg_ms", ""))
                for lid in report["lines_compared"]
            )
            lines.append(
                f"{tb['task_id']},{tb['task_name']},{line_values},"
                f"{tb['best_line']},{tb['worst_line']},{tb['variance_percent']},{tb['severity']}"
            )
        
        return "\n".join(lines)
```

#### Step 3: Add API Endpoints (`src/api_server.py`)

```python
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from typing import List, Optional
from datetime import datetime
from services.benchmark_service import BenchmarkService
from utils.db import get_db

benchmark_router = APIRouter(prefix="/benchmark", tags=["benchmark"])

@benchmark_router.get("/cross-line-tasks")
async def get_cross_line_benchmark(
    line_ids: str = Query(..., description="Comma-separated line IDs"),
    task_ids: Optional[str] = Query(None, description="Comma-separated task IDs"),
    date_from: Optional[str] = Query(None, description="Start date (YYYY-MM-DD)"),
    date_to: Optional[str] = Query(None, description="End date (YYYY-MM-DD)"),
    db: Session = Depends(get_db)
):
    """Get cross-line task benchmark report"""
    service = BenchmarkService(db)
    
    line_list = [lid.strip() for lid in line_ids.split(",")]
    task_list = [tid.strip() for tid in task_ids.split(",")] if task_ids else None
    
    date_from_dt = datetime.strptime(date_from, "%Y-%m-%d") if date_from else None
    date_to_dt = datetime.strptime(date_to, "%Y-%m-%d") if date_to else None
    
    try:
        report = service.generate_benchmark(
            line_ids=line_list,
            task_ids=task_list,
            date_from=date_from_dt,
            date_to=date_to_dt
        )
        return report
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@benchmark_router.post("/cross-line-tasks/generate")
async def generate_benchmark(
    request: BenchmarkRequest,
    db: Session = Depends(get_db)
):
    """Generate new cross-line benchmark report"""
    service = BenchmarkService(db)
    
    try:
        report = service.generate_benchmark(
            line_ids=request.line_ids,
            task_ids=request.task_ids,
            date_from=request.date_range.get("from") if request.date_range else None,
            date_to=request.date_range.get("to") if request.date_range else None,
            warning_threshold=request.variance_threshold_warning,
            critical_threshold=request.variance_threshold_critical,
            include_worker_analysis=request.include_worker_analysis
        )
        return {
            "benchmark_id": report["benchmark_id"],
            "status": "completed",
            "message": "Benchmark report generated successfully"
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@benchmark_router.get("/cross-line-tasks/{benchmark_id}")
async def get_benchmark_by_id(
    benchmark_id: str,
    db: Session = Depends(get_db)
):
    """Get specific benchmark report"""
    service = BenchmarkService(db)
    report = service.get_benchmark(benchmark_id)
    
    if not report:
        raise HTTPException(status_code=404, detail=f"Benchmark not found: {benchmark_id}")
    
    return report


@benchmark_router.get("/cross-line-tasks/{benchmark_id}/export")
async def export_benchmark(
    benchmark_id: str,
    format: str = Query("csv", regex="^(csv|xlsx|pdf)$"),
    db: Session = Depends(get_db)
):
    """Export benchmark report"""
    service = BenchmarkService(db)
    
    try:
        if format == "csv":
            csv_content = service.export_to_csv(benchmark_id)
            return Response(
                content=csv_content,
                media_type="text/csv",
                headers={
                    "Content-Disposition": f"attachment; filename=benchmark_{benchmark_id}.csv"
                }
            )
        else:
            raise HTTPException(status_code=501, detail=f"Format {format} not yet implemented")
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@benchmark_router.delete("/cross-line-tasks/{benchmark_id}")
async def delete_benchmark(
    benchmark_id: str,
    db: Session = Depends(get_db)
):
    """Delete benchmark report"""
    report = db.query(BenchmarkReport).filter(
        BenchmarkReport.benchmark_id == benchmark_id
    ).first()
    
    if not report:
        raise HTTPException(status_code=404, detail=f"Benchmark not found: {benchmark_id}")
    
    db.delete(report)
    db.commit()
    
    return {
        "benchmark_id": benchmark_id,
        "status": "deleted",
        "message": "Benchmark report deleted successfully"
    }


# Register router in main app
app.include_router(benchmark_router)
```

#### Step 4: Create Test Data and Test

```bash
# Create test execution records
curl -X POST http://localhost:8000/task-executions/batch \
  -H "Content-Type: application/json" \
  -d '{
    "records": [
      {"task_id": "T001", "task_name": "Install RAM", "line_id": "L1", "duration_ms": 12500, "recorded_at": "2025-12-01T10:00:00Z"},
      {"task_id": "T001", "task_name": "Install RAM", "line_id": "L2", "duration_ms": 11800, "recorded_at": "2025-12-01T10:05:00Z"},
      {"task_id": "T001", "task_name": "Install RAM", "line_id": "L3", "duration_ms": 13200, "recorded_at": "2025-12-01T10:10:00Z"},
      {"task_id": "T002", "task_name": "Mount CPU", "line_id": "L1", "duration_ms": 8500, "recorded_at": "2025-12-01T10:15:00Z"},
      {"task_id": "T002", "task_name": "Mount CPU", "line_id": "L2", "duration_ms": 9100, "recorded_at": "2025-12-01T10:20:00Z"},
      {"task_id": "T002", "task_name": "Mount CPU", "line_id": "L3", "duration_ms": 8200, "recorded_at": "2025-12-01T10:25:00Z"}
    ]
  }'

# Generate benchmark report
curl -X POST http://localhost:8000/benchmark/cross-line-tasks/generate \
  -H "Content-Type: application/json" \
  -d '{
    "line_ids": ["L1", "L2", "L3"],
    "variance_threshold_warning": 10.0,
    "variance_threshold_critical": 15.0
  }'

# Query benchmark
curl "http://localhost:8000/benchmark/cross-line-tasks?line_ids=L1,L2,L3"

# Export to CSV
curl "http://localhost:8000/benchmark/cross-line-tasks/BM-20251202-ABC123/export?format=csv" \
  -o benchmark_report.csv
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

### Acceptance Criteria

Phase 2 is complete when all the following criteria are met:

| Feature | Acceptance Criteria | Status |
|---------|---------------------|--------|
| Multi-Line Optimization | Can optimize and visualize multiple lines in one request | Planned |
| Line Type Recommendation | Accurate for sample datasets | Planned |
| Per-Plant Thresholds (REQ #6) | Correctly applied per site | Planned |
| Fishbone Diagram | Generated and downloadable (SVG/PNG) | Planned |
| Layout Editor | Supports drag-and-drop and save/load | Planned |
| Product Config API | Returns correct CTO/BTO mapping | Planned |
| NPI/MP Stage (REQ #50) | Differentiation works correctly | Planned |
| Customer Demand (REQ #51) | Capacity analysis functional | Planned |
| Sequence Adjustment (REQ #49) | Validation and override works | Planned |

---

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


def test_cross_line_benchmark():
    """Test cross-line task benchmark"""
    # Generate benchmark
    generate_response = requests.post(f"{BASE_URL}/benchmark/cross-line-tasks/generate", json={
        "line_ids": ["L1", "L2", "L3"],
        "variance_threshold_warning": 10.0,
        "variance_threshold_critical": 15.0,
        "include_worker_analysis": False
    })
    
    assert generate_response.status_code == 200
    data = generate_response.json()
    assert "benchmark_id" in data
    assert data["status"] == "completed"
    
    benchmark_id = data["benchmark_id"]
    
    # Query benchmark
    query_response = requests.get(f"{BASE_URL}/benchmark/cross-line-tasks/{benchmark_id}")
    assert query_response.status_code == 200
    report = query_response.json()
    assert "task_benchmarks" in report
    assert "summary" in report
    
    # Export to CSV
    export_response = requests.get(
        f"{BASE_URL}/benchmark/cross-line-tasks/{benchmark_id}/export?format=csv"
    )
    assert export_response.status_code == 200
    assert "text/csv" in export_response.headers['Content-Type']
    
    # Delete benchmark
    delete_response = requests.delete(f"{BASE_URL}/benchmark/cross-line-tasks/{benchmark_id}")
    assert delete_response.status_code == 200


def test_benchmark_validation():
    """Test benchmark input validation"""
    # Test with less than 2 lines (should fail)
    response = requests.post(f"{BASE_URL}/benchmark/cross-line-tasks/generate", json={
        "line_ids": ["L1"],  # Only 1 line - should fail
        "variance_threshold_warning": 10.0
    })
    
    assert response.status_code == 400
    assert "At least 2 line IDs" in response.json()["detail"]
    
    # Test with invalid thresholds (critical < warning)
    response = requests.post(f"{BASE_URL}/benchmark/cross-line-tasks/generate", json={
        "line_ids": ["L1", "L2"],
        "variance_threshold_warning": 15.0,
        "variance_threshold_critical": 10.0  # Invalid: should be greater than warning
    })
    
    assert response.status_code == 422
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
