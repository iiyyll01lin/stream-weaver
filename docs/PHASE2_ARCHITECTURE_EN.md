# Phase 2 Architecture Design

**Document Version**: 2.0 | **Last Updated**: 2025-11-20  
**Related Documents**:
- [Phase 2 Implementation Guide](PHASE2_IMPLEMENTATION_EN.md)
- [Phase 2 API Specification](PHASE2_API_SPEC_EN.md)
- [Phase 1 Architecture](PHASE1_ARCHITECTURE_EN.md)
- [Database & API Design](DATABASE_API_DESIGN_SPEC_EN.md)

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [System Components](#system-components)
- [Multi-Line Optimization Architecture](#multi-line-optimization-architecture)
- [Layout Management Architecture](#layout-management-architecture)
- [Fishbone Diagram Generator](#fishbone-diagram-generator)
- [Technology Stack](#technology-stack)
- [Data Flow](#data-flow)
- [Database Schema](#database-schema)
- [Performance Optimization](#performance-optimization)

---

## Architecture Overview

### Design Principles

Phase 2 extends the four-tier architecture with advanced manufacturing capabilities:

1. **Presentation Layer** (Frontend)
   - Technology: HTML5 + Tailwind CSS + Chart.js + **Canvas API**
   - New Features: 2D layout editor, fishbone diagram viewer
   - Responsibility: User interaction, advanced visualization

2. **Service Layer** (Backend API)
   - Technology: FastAPI + Pydantic + **PostgreSQL** + **JWT Auth**
   - New Features: Multi-line endpoints, layout management, product config
   - Responsibility: Request validation, business logic, data persistence

3. **Data Layer** (Enhanced Persistence)
   - Technology: PostgreSQL + **Layout Tables** + **Product Configs** + Redis Cache
   - New Features: 2D spatial data, CTO/BTO mappings, version control
   - Responsibility: Complex data relationships, layout storage, configuration management

4. **Algorithm Layer** (Advanced Optimization Engine)
   - Technology: Google OR-Tools (CP-SAT Solver) + **NetworkX**
   - New Features: Multi-line model, fishbone graph generator, line type recommender
   - Responsibility: Advanced optimization, graph generation

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend Layer                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  dashboard.html (Enhanced UI)                         │  │
│  │  - Multi-line Optimization Panel                      │  │
│  │  - 2D Layout Editor (Canvas API)                      │  │
│  │  - Fishbone Diagram Viewer                            │  │
│  │  - Product Configuration Manager                      │  │
│  └─────────────────────┬───────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────┘
                         │ HTTP POST/GET
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend API Layer                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  api_server.py (Extended FastAPI Application)         │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Phase 2 NEW Endpoints                          │  │  │
│  │  │  - POST /optimize (multi-line support)          │  │  │
│  │  │  - GET  /recommend-line-type                    │  │  │
│  │  │  - GET  /fishbone-diagram                       │  │  │
│  │  │  - GET  /layout                                 │  │  │
│  │  │  - POST /save-layout                            │  │  │
│  │  │  - GET  /load-layout                            │  │  │
│  │  │  - GET  /product-config                         │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  │                    │                                   │  │
│  │  ┌─────────────────▼───────────────────────────────┐  │  │
│  │  │  Database Access Layer (ENHANCED)               │  │  │
│  │  │  - Layout Storage (PostgreSQL)                  │  │  │
│  │  │  - Product Config (CTO/BTO)                     │  │  │
│  │  │  - Multi-line Optimization History              │  │  │
│  │  │  - Version Control & Configuration Management   │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  └────────────────────┼───────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────┘
                         │ SQL queries / subprocess.run()
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                Data Layer (ENHANCED)                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  PostgreSQL Database                                  │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Phase 2 Extended Tables                        │  │  │
│  │  │  - layouts (spatial data, stations, connections)│  │  │
│  │  │  - layout_stations (positioning, dimensions)    │  │  │
│  │  │  - layout_connections (conveyors, AGVs)         │  │  │
│  │  │  - product_configs (CTO/BTO mappings)           │  │  │
│  │  │  - configurations (version control)             │  │  │
│  │  │  + All Phase 1 tables (extended)                │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  │                    │                                   │  │
│  │  ┌─────────────────▼───────────────────────────────┐  │  │
│  │  │  Redis Cache (ENHANCED)                         │  │  │
│  │  │  - Layout data (24hr TTL)                       │  │  │
│  │  │  - Multi-line optimization results (2hr TTL)    │  │  │
│  │  │  - Fishbone diagram cache (1hr TTL)             │  │  │
│  │  │  - Product config cache (1 week TTL)            │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  └────────────────────┼───────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────┘
                         │ CSV generation / Multi-line models
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Algorithm Layer                            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  sche-algo-v2.py (Multi-Line Solver)                  │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Multi-Line Model                               │  │  │
│  │  │  - Line assignment variables                    │  │  │
│  │  │  - Cross-line balancing constraints             │  │  │
│  │  │  - Line type recommendation logic               │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  │                    │                                   │  │
│  │  ┌─────────────────▼───────────────────────────────┐  │  │
│  │  │  fishbone-generator.py (NEW)                    │  │  │
│  │  │  - Task precedence graph (NetworkX)             │  │  │
│  │  │  - SVG/PNG export                               │  │  │
│  │  │  - Interactive diagram generation               │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## System Components

### 1. Frontend Component (Enhanced `dashboard.html`)

**Phase 2 Additions**:

#### 1.1 Multi-Line Optimization Panel
```html
<div id="multi-line-panel">
  <h3>Multi-Line Configuration</h3>
  <div>
    <label>Number of Lines:</label>
    <input type="number" id="num-lines" min="1" max="5" value="1">
  </div>
  <div id="line-configs">
    <!-- Dynamically generated line configs -->
    <div class="line-config">
      <label>Line A Target Takt:</label>
      <input type="number" id="line-a-takt" value="30000">
    </div>
    <div class="line-config">
      <label>Line B Target Takt:</label>
      <input type="number" id="line-b-takt" value="25000">
    </div>
  </div>
</div>
```

#### 1.2 Layout Editor (Canvas-based)
```javascript
class LayoutEditor {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.stations = [];
    this.connections = [];
  }

  addStation(x, y, stationId) {
    this.stations.push({ x, y, id: stationId });
    this.render();
  }

  addConnection(fromId, toId) {
    this.connections.push({ from: fromId, to: toId });
    this.render();
  }

  exportLayout() {
    return {
      stations: this.stations,
      connections: this.connections
    };
  }

  importLayout(layoutData) {
    this.stations = layoutData.stations;
    this.connections = layoutData.connections;
    this.render();
  }
}
```

#### 1.3 Fishbone Diagram Viewer
```javascript
async function displayFishboneDiagram(workOrderId) {
  const response = await fetch(`/fishbone-diagram?work_order_id=${workOrderId}`);
  const svgData = await response.text();
  
  document.getElementById('fishbone-container').innerHTML = svgData;
}
```

**Technology Choices**:

| Technology        | Purpose                    | Reason for Selection                     |
|-------------------|----------------------------|------------------------------------------|
| Canvas API        | 2D layout editor           | Native browser support, high performance |
| SVG               | Fishbone diagram rendering | Scalable, exportable, interactive        |
| Fetch API (async) | Multi-endpoint calls       | Concurrent requests for multi-line data  |

---

### 2. Backend API Component (Extended `api_server.py`)

**Phase 2 Additions**:

#### 2.1 Multi-Line Configuration Management
```python
class MultiLineRequest(BaseModel):
    """Multi-line optimization request"""
    work_order_id: str
    optimization_goal: str
    lines: List[LineConfig]  # NEW: List of line configurations
    enable_cross_line_balancing: bool = True
    
class LineConfig(BaseModel):
    """Individual line configuration"""
    line_id: str  # A, B, C, etc.
    target_takt: int
    max_workers_per_station: int = 3
    task_filter: Optional[List[str]] = None  # Filter tasks for this line
```

#### 2.2 Layout Management Endpoints
```python
@app.post("/save-layout")
async def save_layout(layout: LayoutData):
    """Save layout to database"""
    layout_id = db.insert_layout(
        name=layout.name,
        data_json=json.dumps(layout.to_dict()),
        created_at=datetime.now()
    )
    return {"layout_id": layout_id, "status": "saved"}

@app.get("/load-layout")
async def load_layout(layout_id: int):
    """Load layout from database"""
    layout_data = db.get_layout(layout_id)
    return LayoutData.from_dict(json.loads(layout_data['data_json']))

@app.get("/layout")
async def list_layouts():
    """List all saved layouts"""
    return db.get_all_layouts()
```

#### 2.3 Product Configuration Endpoints
```python
@app.get("/product-config")
async def get_product_config(sku: Optional[str] = None):
    """Retrieve CTO/BTO mapping"""
    if sku:
        return db.get_product_config_by_sku(sku)
    else:
        return db.get_all_product_configs()

@app.post("/product-config")
async def create_product_config(config: ProductConfig):
    """Create/update product configuration"""
    config_id = db.upsert_product_config(config)
    return {"config_id": config_id, "status": "saved"}
```

#### 2.4 Fishbone Diagram Endpoint
```python
@app.get("/fishbone-diagram")
async def generate_fishbone(
    work_order_id: str,
    format: str = "svg"  # svg or png
):
    """Generate fishbone diagram"""
    result = subprocess.run(
        [
            "python3", "src/fishbone_generator.py",
            "--work_order_id", work_order_id,
            "--format", format,
            "--output", f"/tmp/fishbone_{work_order_id}.{format}"
        ],
        capture_output=True,
        timeout=10
    )
    
    with open(f"/tmp/fishbone_{work_order_id}.{format}", "rb") as f:
        diagram_data = f.read()
    
    if format == "svg":
        return Response(content=diagram_data, media_type="image/svg+xml")
    else:
        return Response(content=diagram_data, media_type="image/png")
```

#### 2.5 Line Type Recommendation Endpoint
```python
@app.get("/recommend-line-type")
async def recommend_line_type(
    work_order_id: str,
    target_takt: int
):
    """Recommend optimal line type"""
    # Load task data
    tasks_df = pd.read_csv(get_work_order_tasks(work_order_id))
    
    # Calculate metrics
    total_work = tasks_df['duration'].sum()
    task_count = len(tasks_df)
    avg_complexity = tasks_df['complexity_level'].value_counts().to_dict()
    
    # Recommendation logic
    if task_count < 20 and total_work < target_takt * 3:
        recommendation = "cell"
    elif task_count < 50:
        recommendation = "short_line"
    else:
        recommendation = "long_line"
    
    return {
        "recommended_type": recommendation,
        "reasoning": {
            "task_count": task_count,
            "total_work_ms": total_work,
            "target_takt_ms": target_takt,
            "complexity_distribution": avg_complexity
        },
        "alternatives": ["cell", "short_line", "long_line"]
    }
```

---

### 3. Algorithm Component (Multi-Line Solver)

**Phase 2 Additions**:

#### 3.1 Multi-Line Optimization Model
```python
def solve_multi_line_problem(
    tasks_df: pd.DataFrame,
    precedences_df: pd.DataFrame,
    lines: List[LineConfig],
    enable_cross_line_balancing: bool
) -> Dict[str, Any]:
    """
    Multi-line optimization model
    
    Decision Variables:
    - x[i][j][l] = 1 if task i is assigned to station j on line l
    - line_used[l] = 1 if line l is used
    
    Constraints:
    1. Each task assigned to exactly one station on one line
    2. Precedence constraints (within same line)
    3. Takt time constraints (per line)
    4. Cross-line balancing (if enabled)
    """
    model = cp_model.CpModel()
    
    num_tasks = len(tasks_df)
    num_lines = len(lines)
    max_stations_per_line = 20
    
    # Decision variables: x[i][j][l]
    x = {}
    for i in range(num_tasks):
        for l in range(num_lines):
            for j in range(max_stations_per_line):
                x[(i, j, l)] = model.NewBoolVar(f'x_t{i}_s{j}_l{l}')
    
    # Line usage variables
    line_used = [model.NewBoolVar(f'line_{l}_used') for l in range(num_lines)]
    
    # Constraint 1: Each task to exactly one (station, line) pair
    for i in range(num_tasks):
        model.Add(
            sum(x[(i, j, l)] 
                for l in range(num_lines) 
                for j in range(max_stations_per_line)
            ) == 1
        )
    
    # Constraint 2: Precedence (same line only)
    for _, row in precedences_df.iterrows():
        pred = int(row['predecessor'])
        succ = int(row['successor'])
        
        for l in range(num_lines):
            for j in range(max_stations_per_line - 1):
                # If pred at (j, l), succ must be at (j', l) where j' >= j
                model.Add(
                    sum(x[(succ, jp, l)] for jp in range(j + 1, max_stations_per_line))
                    >= x[(pred, j, l)]
                )
    
    # Constraint 3: Takt time per line
    for l, line_config in enumerate(lines):
        for j in range(max_stations_per_line):
            station_load = sum(
                tasks_df.loc[i, 'duration'] * x[(i, j, l)]
                for i in range(num_tasks)
            )
            model.Add(station_load <= line_config.target_takt)
    
    # Constraint 4: Cross-line balancing (optional)
    if enable_cross_line_balancing:
        # Balance workload across lines
        line_loads = []
        for l in range(num_lines):
            line_load = sum(
                tasks_df.loc[i, 'duration'] * x[(i, j, l)]
                for i in range(num_tasks)
                for j in range(max_stations_per_line)
            )
            line_loads.append(line_load)
        
        # Minimize max(line_loads) - min(line_loads)
        max_load = model.NewIntVar(0, 1000000, 'max_load')
        min_load = model.NewIntVar(0, 1000000, 'min_load')
        
        for load in line_loads:
            model.Add(max_load >= load)
            model.Add(min_load <= load)
        
        load_imbalance = model.NewIntVar(0, 1000000, 'imbalance')
        model.Add(load_imbalance == max_load - min_load)
    
    # Objective: Minimize total lines used + total stations
    total_stations = model.NewIntVar(0, num_lines * max_stations_per_line, 'total_stations')
    model.Add(
        total_stations == sum(
            model.NewBoolVar(f'station_{j}_line_{l}_used')
            for l in range(num_lines)
            for j in range(max_stations_per_line)
        )
    )
    
    model.Minimize(
        sum(line_used) * 1000 + total_stations
    )
    
    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 8
    solver.parameters.max_time_in_seconds = 60
    
    status = solver.Solve(model)
    
    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        return extract_multi_line_solution(solver, x, tasks_df, lines)
    else:
        raise ValueError(f"Solver failed with status: {status}")
```

#### 3.2 Fishbone Diagram Generator
```python
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import patches

def generate_fishbone_diagram(
    tasks_df: pd.DataFrame,
    precedences_df: pd.DataFrame,
    output_file: str,
    format: str = "svg"
):
    """
    Generate fishbone (assembly sequence) diagram
    
    Uses NetworkX to create directed graph, then renders as fishbone
    """
    # Build directed graph
    G = nx.DiGraph()
    
    # Add nodes (tasks)
    for _, row in tasks_df.iterrows():
        G.add_node(
            row['task_id'],
            duration=row['duration'],
            action_type=row.get('action_type', 'unknown')
        )
    
    # Add edges (precedences)
    for _, row in precedences_df.iterrows():
        G.add_edge(row['predecessor'], row['successor'])
    
    # Calculate levels (topological sort)
    levels = {}
    for node in nx.topological_sort(G):
        predecessors = list(G.predecessors(node))
        if not predecessors:
            levels[node] = 0
        else:
            levels[node] = max(levels[p] for p in predecessors) + 1
    
    # Fishbone layout (custom positioning)
    pos = fishbone_layout(G, levels)
    
    # Render
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Draw spine (main line)
    max_level = max(levels.values())
    ax.plot([0, max_level + 1], [0, 0], 'k-', linewidth=3, zorder=1)
    
    # Draw bones (tasks)
    for node, (x, y) in pos.items():
        # Task node
        circle = patches.Circle((x, y), 0.3, 
                                color=get_action_color(G.nodes[node]['action_type']),
                                zorder=3)
        ax.add_patch(circle)
        
        # Label
        ax.text(x, y, str(node), ha='center', va='center', 
                fontsize=8, fontweight='bold', zorder=4)
        
        # Bone line to spine
        ax.plot([x, x], [y, 0], 'k-', linewidth=1.5, zorder=2)
    
    # Draw precedence arrows
    for u, v in G.edges():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', lw=1, color='gray'))
    
    ax.set_xlim(-1, max_level + 2)
    ax.set_ylim(-5, 5)
    ax.axis('off')
    ax.set_title('Assembly Sequence Fishbone Diagram', fontsize=16, fontweight='bold')
    
    # Save
    if format == "svg":
        plt.savefig(output_file, format='svg', bbox_inches='tight')
    else:
        plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight')
    
    plt.close()

def fishbone_layout(G, levels):
    """Custom fishbone layout positioning"""
    pos = {}
    level_counts = {}
    
    for node, level in levels.items():
        if level not in level_counts:
            level_counts[level] = 0
        
        # Alternate above/below spine
        y_offset = (level_counts[level] % 2) * 2 - 1  # -1 or 1
        y_position = y_offset * (1 + level_counts[level] // 2)
        
        pos[node] = (level, y_position)
        level_counts[level] += 1
    
    return pos

def get_action_color(action_type):
    """Color mapping for action types"""
    colors = {
        'screw': '#3498db',
        'glue': '#e74c3c',
        'clip': '#2ecc71',
        'mount': '#f39c12',
        'test': '#9b59b6',
        'unknown': '#95a5a6'
    }
    return colors.get(action_type, colors['unknown'])
```

---

## Technology Stack

### Phase 2 Extended Stack

| Component           | Technology | Version | Purpose                          | New in Phase 2 |
|---------------------|------------|---------|----------------------------------|----------------|
| **Frontend**        | Canvas API | Native  | 2D layout editor                 | ✅              |
|                     | SVG        | Native  | Fishbone diagram rendering       | ✅              |
| **Backend**         | SQLAlchemy | 2.0+    | ORM for database                 | ✅              |
|                     | SQLite     | 3.x     | Embedded database (dev)          | ✅              |
|                     | PostgreSQL | 14+     | Production database (optional)   | ✅              |
| **Algorithm**       | NetworkX   | 3.0+    | Graph algorithms (fishbone)      | ✅              |
|                     | Matplotlib | 3.7+    | Diagram rendering                | ✅              |
| **Data Processing** | pandas     | 2.0+    | CSV + multi-line data processing | (existing)     |

---

## Data Flow

### Multi-Line Optimization Flow

```
┌──────────┐
│  User    │  (1) Configure 3 lines with different takt times
└────┬─────┘
     │
     ▼
┌─────────────────────────────────────────┐
│  Frontend: Multi-Line Panel             │
│  Line A: takt=30000ms, tasks=[1,2,3,4]  │
│  Line B: takt=25000ms, tasks=[5,6,7]    │
│  Line C: takt=35000ms, tasks=[8,9,10]   │
└────┬────────────────────────────────────┘
     │ POST /optimize (multi-line request)
     ▼
┌─────────────────────────────────────────┐
│  API Server: Multi-Line Handler         │
│  1. Validate line configurations        │
│  2. Merge task CSVs with line_id column │
│  3. Call sche-algo-v2.py                │
└────┬────────────────────────────────────┘
     │ python3 sche-algo-v2.py --multi_line
     ▼
┌─────────────────────────────────────────┐
│  Algorithm: Multi-Line Solver           │
│  1. Build 3D assignment model x[i][j][l]│
│  2. Add cross-line balancing            │
│  3. Solve with CP-SAT                   │
│  4. Return per-line assignments         │
└────┬────────────────────────────────────┘
     │ JSON output (multi-line results)
     ▼
┌─────────────────────────────────────────┐
│  API Server: Response Transform         │
│  {                                      │
│    "lines": [                           │
│      {"line_id": "A", "stations": 2},   │
│      {"line_id": "B", "stations": 2},   │
│      {"line_id": "C", "stations": 3}    │
│    ],                                   │
│    "total_lines_used": 3                │
│  }                                      │
└────┬────────────────────────────────────┘
     │ HTTP 200 OK
     ▼
┌─────────────────────────────────────────┐
│  Frontend: Multi-Line Gantt Chart       │
│  Render 3 separate Gantt charts stacked │
└─────────────────────────────────────────┘
```

---

## Database Schema

### Phase 2 Extended PostgreSQL Schema

Phase 2 extends the Phase 1 schema with spatial data, layout management, and product configuration:

```sql
-- Phase 2: Layout management tables
CREATE TABLE layouts (
    id SERIAL PRIMARY KEY,
    site_id INTEGER REFERENCES sites(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    layout_type VARCHAR(20) DEFAULT '2d',    -- 2d, 3d
    
    -- Layout metadata  
    dimensions_json JSONB,                   -- {"width": 100, "depth": 50, "height": 10}
    units VARCHAR(10) DEFAULT 'meters',      -- meters, feet, inches
    
    -- Version control
    version VARCHAR(50) NOT NULL,
    parent_layout_id INTEGER REFERENCES layouts(id),
    
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Station definitions within layouts
CREATE TABLE layout_stations (
    id SERIAL PRIMARY KEY,
    layout_id INTEGER REFERENCES layouts(id),
    station_code VARCHAR(50) NOT NULL,      -- WS-001, WS-002, etc.
    station_type VARCHAR(50) NOT NULL,      -- assembly, test, packaging
    
    -- Positioning
    position_x DECIMAL(8,3) NOT NULL,
    position_y DECIMAL(8,3) NOT NULL, 
    position_z DECIMAL(8,3) DEFAULT 0,
    
    -- Dimensions
    width DECIMAL(6,3) NOT NULL,
    depth DECIMAL(6,3) NOT NULL,
    height DECIMAL(6,3) DEFAULT 2,
    
    -- Multi-line assignment
    line_id VARCHAR(10),                     -- A, B, C for multi-line
    
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(layout_id, station_code)
);

-- Connections between stations (conveyors, AGVs)
CREATE TABLE layout_connections (
    id SERIAL PRIMARY KEY,
    layout_id INTEGER REFERENCES layouts(id),
    from_station_id INTEGER REFERENCES layout_stations(id),
    to_station_id INTEGER REFERENCES layout_stations(id),
    connection_type VARCHAR(50) NOT NULL,   -- conveyor, agv, manual
    
    -- Connection properties
    length_meters DECIMAL(6,3),
    speed_mps DECIMAL(5,3),                 -- meters per second
    capacity INTEGER,                       -- max items in transit
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Phase 2: Product configuration for CTO/BTO
CREATE TABLE product_configs (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(100) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    complexity_level VARCHAR(20) DEFAULT 'medium',
    cto_bto_mapping JSONB,                  -- Configure-to-Order mappings
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Enhanced task table (extends Phase 1)
ALTER TABLE tasks ADD COLUMN line_id VARCHAR(10);  -- Multi-line support

-- Enhanced optimization table (extends Phase 1) 
ALTER TABLE optimizations ADD COLUMN multi_line_enabled BOOLEAN DEFAULT FALSE;
ALTER TABLE optimizations ADD COLUMN cross_line_balancing BOOLEAN DEFAULT FALSE;
ALTER TABLE optimizations ADD COLUMN layout_id INTEGER REFERENCES layouts(id);

-- Enhanced station table (extends Phase 1)
ALTER TABLE stations ADD COLUMN line_id VARCHAR(10);
ALTER TABLE stations ADD COLUMN position_x DECIMAL(8,3);
ALTER TABLE stations ADD COLUMN position_y DECIMAL(8,3);
ALTER TABLE stations ADD COLUMN position_z DECIMAL(8,3) DEFAULT 0;
```

### Phase 2 API Endpoints (Extensions)

```yaml
# Layout Management APIs
POST   /api/v2/layouts                      # Create new factory layout
GET    /api/v2/layouts                      # List all layouts for site
GET    /api/v2/layouts/{id}                 # Get specific layout
PUT    /api/v2/layouts/{id}                 # Update existing layout
DELETE /api/v2/layouts/{id}                 # Soft delete layout

# Product Configuration APIs
GET    /api/v2/product-configs              # List product configs (CTO/BTO)
POST   /api/v2/product-configs              # Create product config
PUT    /api/v2/product-configs/{sku}        # Update product config

# Multi-line Optimization APIs (Enhanced)
POST   /api/v2/optimizations                # Multi-line optimization
GET    /api/v2/optimizations/{id}/lines     # Get line-specific results

# Fishbone Diagram APIs
GET    /api/v2/fishbone-diagram/{opt_id}    # Generate fishbone diagram
GET    /api/v2/recommend-line-type          # Line type recommendation

# Configuration Management APIs
POST   /api/v2/configurations               # Save configuration version
GET    /api/v2/configurations               # List configuration versions
GET    /api/v2/configurations/{id}/restore  # Restore configuration version
```

### ORM Models (SQLAlchemy)

```python
from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime

class Layout(Base):
    __tablename__ = 'layouts'
    
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey('sites.id'))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    layout_type = Column(String(20), default='2d')
    
    # Metadata
    dimensions_json = Column(JSONB)
    units = Column(String(10), default='meters')
    
    # Version control
    version = Column(String(50), nullable=False)
    parent_layout_id = Column(Integer, ForeignKey('layouts.id'))
    
    # Audit
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    stations = relationship("LayoutStation", back_populates="layout")
    connections = relationship("LayoutConnection", back_populates="layout")

class LayoutStation(Base):
    __tablename__ = 'layout_stations'
    
    id = Column(Integer, primary_key=True)
    layout_id = Column(Integer, ForeignKey('layouts.id'))
    station_code = Column(String(50), nullable=False)
    station_type = Column(String(50), nullable=False)
    
    # Positioning
    position_x = Column(DECIMAL(8,3), nullable=False)
    position_y = Column(DECIMAL(8,3), nullable=False)
    position_z = Column(DECIMAL(8,3), default=0)
    
    # Dimensions
    width = Column(DECIMAL(6,3), nullable=False)
    depth = Column(DECIMAL(6,3), nullable=False)
    height = Column(DECIMAL(6,3), default=2)
    
    # Multi-line
    line_id = Column(String(10))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    layout = relationship("Layout", back_populates="stations")

class ProductConfig(Base):
    __tablename__ = 'product_configs'
    
    id = Column(Integer, primary_key=True)
    sku = Column(String(100), nullable=False)
    product_name = Column(String(255), nullable=False)
    complexity_level = Column(String(20), default='medium')
    cto_bto_mapping = Column(JSONB)  # {"CPU": {"option_1": "Intel Xeon Silver"}}
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### Data Input Schema Evolution

Phase 2 extends CSV schemas to support multi-line operations:

#### Enhanced `tasks_multi_line.csv` (Phase 2)
```csv
task_id,duration,offline_flag,adjustable,action_type,complexity_level,part_id,line_id,predecessors
1,274,0,1,"screw","simple","GPU_GTX3080","A",
2,223,1,0,"glue","medium","HDD_2TB","A",1
5,186,0,1,"clip","simple","RAM_16GB","B",
6,298,0,1,"screw","medium","CPU_XEON","B",5
```

#### Product Configuration JSON
```json
{
  "sku": "DL360_GEN10",
  "product_name": "HPE ProLiant DL360 Gen10",
  "cto_bto_mapping": {
    "CPU": {
      "option_1": "Intel Xeon Silver 4210",
      "option_2": "Intel Xeon Gold 6230"
    },
    "RAM": {
      "option_1": "16GB DDR4",
      "option_2": "32GB DDR4",
      "option_3": "64GB DDR4"
    },
    "STORAGE": {
      "option_1": "1TB HDD",
      "option_2": "500GB SSD",
      "option_3": "1TB SSD"
    }
  },
  "default_complexity": "medium"
}
```

#### Layout Definition JSON
```json
{
  "name": "Factory A Multi-Line Layout",
  "layout_type": "2d",
  "dimensions": {"width": 100, "depth": 50, "height": 10},
  "units": "meters",
  "stations": [
    {
      "station_code": "WS-001",
      "station_type": "assembly",
      "position": {"x": 0, "y": 0, "z": 0},
      "dimensions": {"width": 2, "depth": 1.5, "height": 2},
      "line_id": "A"
    },
    {
      "station_code": "WS-002",
      "station_type": "assembly", 
      "position": {"x": 4, "y": 0, "z": 0},
      "dimensions": {"width": 2, "depth": 1.5, "height": 2},
      "line_id": "A"
    }
  ],
  "connections": [
    {
      "from": "WS-001",
      "to": "WS-002", 
      "type": "conveyor",
      "length_meters": 3.5,
      "speed_mps": 0.5
    }
  ]
}
```
    description = Column(Text)
    data_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class ProductConfig(Base):
    __tablename__ = 'product_configs'
    
    id = Column(Integer, primary_key=True)
    sku = Column(String(100), unique=True, nullable=False)
    product_name = Column(String(255))
    cto_bto_map = Column(Text)
    default_complexity = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)

class OptimizationHistory(Base):
    __tablename__ = 'optimization_history'
    
    id = Column(Integer, primary_key=True)
    work_order_id = Column(String(100), nullable=False)
    optimization_goal = Column(String(50))
    num_lines = Column(Integer, default=1)
    result_json = Column(Text, nullable=False)
    solve_time_sec = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
```

---

## Performance Optimization

### Multi-Line Solver Optimization

**Challenge**: 3D decision variables x[i][j][l] exponentially increase search space

**Solutions**:

1. **Symmetry Breaking**:
   ```python
   # Force line ordering: if line l is unused, line l+1 must be unused
   for l in range(num_lines - 1):
       model.Add(line_used[l] >= line_used[l + 1])
   ```

2. **Warm Start**:
   ```python
   # Use single-line solution as initial hint for multi-line
   single_line_solution = solve_single_line(tasks_df)
   
   # Distribute tasks across lines based on precedence clusters
   clusters = identify_precedence_clusters(precedences_df)
   for cluster_id, cluster_tasks in enumerate(clusters):
       suggested_line = cluster_id % num_lines
       for task in cluster_tasks:
           # Set hint for solver
           model.AddHint(x[(task, 0, suggested_line)], 1)
   ```

3. **Parallel Search**:
   ```python
   solver.parameters.num_search_workers = min(8, num_lines * 2)
   ```

### Database Query Optimization

```python
# Index on frequently queried columns
CREATE INDEX idx_layouts_name ON layouts(name);
CREATE INDEX idx_product_configs_sku ON product_configs(sku);
CREATE INDEX idx_optimization_history_work_order ON optimization_history(work_order_id);
```

---

## Security Design

### Phase 2 Security Additions

1. **Database Access Control**:
   ```python
   # Use environment variables for credentials
   DATABASE_URL = os.getenv(
       'DATABASE_URL',
       'sqlite:///./line_balance.db'  # Default dev database
   )
   ```

2. **Layout Data Validation**:
   ```python
   class LayoutData(BaseModel):
       name: str = Field(max_length=255)
       stations: List[StationPosition]
       connections: List[Connection]
       
       @validator('stations')
       def validate_stations(cls, v):
           if len(v) > 100:
               raise ValueError("Max 100 stations allowed")
           return v
   ```

3. **SQL Injection Prevention**:
   ```python
   # Use ORM (SQLAlchemy) for all database queries
   # Parameterized queries only
   session.query(Layout).filter(Layout.name == user_input).first()
   ```

---

**Document Maintainer:** JASON YY, LIN  
**Last Updated:** 2025-11-12 
**Version:** 2.0.0-phase2
