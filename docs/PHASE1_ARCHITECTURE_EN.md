# Phase 1 Architecture Design

**Document Version**: 2.0 | **Last Updated**: 2025-11-20  
**Related Documents**:
- [Implementation Guide](PHASE1_IMPLEMENTATION_EN.md)
- [API Specification](PHASE1_API_SPEC_EN.md)
- [Database & API Design](DATABASE_API_DESIGN_SPEC_EN.md)
- [Stage Specifications](stage-specs.md)

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [System Components](#system-components)
- [Technology Stack](#technology-stack)
- [Data Flow](#data-flow)
- [Deployment Architecture](#deployment-architecture)
- [Security Design](#security-design)
- [Performance Optimization](#performance-optimization)

---

## Architecture Overview

### Design Principles

Phase 1 adopts a **four-tier architecture** to achieve separation of concerns and modular scalability:

1. **Presentation Layer** (Frontend)
   - Technology: HTML5 + Tailwind CSS + Chart.js
   - Responsibility: User interaction, data visualization

2. **Service Layer** (Backend API)
   - Technology: FastAPI + Pydantic + JWT Authentication
   - Responsibility: Request validation, business logic orchestration

3. **Data Layer** (Persistence)
   - Technology: PostgreSQL + SQLAlchemy + Redis Cache
   - Responsibility: Data storage, versioning, multi-tenant support

4. **Algorithm Layer** (Optimization Engine)
   - Technology: Google OR-Tools (CP-SAT Solver)
   - Responsibility: Line balance optimization computation

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend Layer                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  dashboard.html (Static HTML)                         │  │
│  │  - Tailwind CSS (UI Styling)                          │  │
│  │  - Chart.js (Gantt Chart Visualization)              │  │
│  │  - Fetch API (HTTP Communication)                     │  │
│  └─────────────────────┬───────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────┘
                         │ HTTP POST /optimize
                         │ HTTP GET /workstations
                         │ HTTP GET /takt-summary
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend API Layer                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  api_server.py (FastAPI Application)                  │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Endpoint Handlers                              │  │  │
│  │  │  - POST /optimize                               │  │  │
│  │  │  - GET /workstations                            │  │  │
│  │  │  - GET /takt-summary                            │  │  │
│  │  │  - GET /health                                  │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  │                    │                                   │  │
│  │  ┌─────────────────▼───────────────────────────────┐  │  │
│  │  │  Business Logic                                 │  │  │
│  │  │  - Work Order Mapping (WO_A/B/C)                │  │  │
│  │  │  - Parameter Validation (Pydantic)              │  │  │
│  │  │  - Response Transformation                      │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  └────────────────────┼───────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────┘
                         │ SQL Queries / subprocess.run()
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Data Layer (NEW)                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  PostgreSQL Database                                  │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Core Tables                                    │  │  │
│  │  │  - work_orders (WO_A/B/C data)                  │  │  │
│  │  │  - tasks (CSV task data + precedences)          │  │  │
│  │  │  - optimizations (solver results)               │  │  │
│  │  │  - stations (workstation assignments)           │  │  │
│  │  │  - users (authentication)                       │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  │                    │                                   │  │
│  │  ┌─────────────────▼───────────────────────────────┐  │  │
│  │  │  Redis Cache                                    │  │  │
│  │  │  - Optimization results (1hr TTL)               │  │  │
│  │  │  - Workstation details (1hr TTL)                │  │  │
│  │  │  - Authentication tokens                        │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  └────────────────────┼───────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────┘
                         │ CSV generation / Model execution
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Algorithm Layer                            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  sche-algo.py (OR-Tools Solver)                       │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Input Processing                               │  │  │
│  │  │  - DB Query Results → CSV Format                │  │  │
│  │  │  - Data Validation                              │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  │                    │                                   │  │
│  │  ┌─────────────────▼───────────────────────────────┐  │  │
│  │  │  CP-SAT Solver                                  │  │  │
│  │  │  - Objective: min_stations / min_manpower / ... │  │  │
│  │  │  - Constraints: Precedence, Takt, Workers       │  │  │
│  │  │  - Model: Boolean Assignment                    │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  │                    │                                   │  │
│  │  ┌─────────────────▼───────────────────────────────┐  │  │
│  │  │  Output Generation                              │  │  │
│  │  │  - JSON (API Response)                          │  │  │
│  │  │  - DB Storage (Persistent Results)              │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## Extended Data Flow (Phase 1.5) - Part Tracking

### Part-Aware Processing Architecture

Phase 1.5 introduces **Part Tracking** capability to link assembly actions with BOM (Bill of Materials) parts, enabling material flow analysis and line-side inventory planning.

```
┌─────────────────────────────────────────────────────────────┐
│                    CSV Input Layer                          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  tasks.csv (Extended Schema)                          │  │
│  │  - task_id, duration, predecessors (Phase 1)          │  │
│  │  - part_id (NEW): Part number from BOM                │  │
│  │  - action_type (NEW): screw, glue, mount, test, etc. │  │
│  │  - complexity_level (NEW): simple/medium/complex      │  │
│  │  - offline_flag (NEW): 0=online, 1=offline            │  │
│  └─────────────────┬─────────────────────────────────────┘  │
└────────────────────┼─────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              Task Classification Layer                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Part-Task Mapping Engine                             │  │
│  │  - Group tasks by part_id                             │  │
│  │  - Extract action_type for each task                  │  │
│  │  - Build part dependency graph                        │  │
│  │  - Classify complexity (auto-detect if missing)       │  │
│  └─────────────────┬─────────────────────────────────────┘  │
└────────────────────┼─────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│           CP-SAT Optimization Layer                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Part-Aware Solver                                    │  │
│  │  - Standard constraints (precedence, takt, workers)   │  │
│  │  - Part locality optimization (minimize part travel)  │  │
│  │  - Complexity balancing across stations              │  │
│  └─────────────────┬─────────────────────────────────────┘  │
└────────────────────┼─────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│            Post-Processing Layer                            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Part Flow Analysis                                   │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  For each station:                              │  │  │
│  │  │  1. Collect all part_ids from assigned tasks    │  │  │
│  │  │  2. Group actions by part_id                    │  │  │
│  │  │  3. Generate parts_involved list                │  │  │
│  │  │  4. Build part_operations map                   │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  │                                                         │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Global Part-Station Matrix Generation:         │  │  │
│  │  │  - part_flow_summary: {part_id → [stations]}   │  │  │
│  │  │  - Station-level BOM (for line-side inventory)  │  │  │
│  │  │  - Part travel distance analysis                │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   Output Layer                              │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  JSON Response (Extended)                             │  │
│  │  {                                                    │  │
│  │    "stations": [                                      │  │
│  │      {                                                │  │
│  │        "id": "WS-001",                                │  │
│  │        "parts_involved": [                            │  │
│  │          {"part_id": "GPU_GTX3080",                   │  │
│  │           "actions": ["install", "test"],            │  │
│  │           "task_ids": [2, 5]}                         │  │
│  │        ],                                             │  │
│  │        "complexity_max": "complex"                    │  │
│  │      }                                                │  │
│  │    ],                                                 │  │
│  │    "part_flow_summary": {                             │  │
│  │      "GPU_GTX3080": [0, 1],  // Stations 0 & 1       │  │
│  │      "SCREW_M3": [0, 1, 2]   // Stations 0, 1, 2     │  │
│  │    },                                                 │  │
│  │    "part_count": 15                                   │  │
│  │  }                                                    │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Part Tracking Use Cases

| Use Case                         | Description                                      | Output Data                       |
|----------------------------------|--------------------------------------------------|-----------------------------------|
| **Line-Side Inventory Planning** | Determine which parts are needed at each station | `stations[].parts_involved`       |
| **BOM Verification**             | Ensure all BOM items are assigned to stations    | `part_count`, `part_flow_summary` |
| **Material Flow Analysis**       | Track part movement across stations              | `part_flow_summary`               |
| **Backflush Point Setup**        | Configure MES/ERP backflush locations            | `part_station_matrix.json`        |
| **Complexity Balancing**         | Distribute complex assembly tasks evenly         | `stations[].complexity_max`       |
| **Work Instruction Generation**  | Auto-generate SOPs with part-action mapping      | `stations[].part_operations`      |

### Data Model Extensions

#### Input Schema (CSV)
```csv
task_id,duration,part_id,action_type,complexity_level,offline_flag,predecessors
1,5000,"SCREW_M3","screw","simple",0,
2,8000,"GPU_GTX3080","install","complex",0,1
3,3000,"THERMAL_PAD","apply","medium",1,1
4,4000,"GPU_GTX3080","test","complex",0,2
```

#### Output Schema (JSON)
```python
# Station-level part information
class PartOperation(BaseModel):
    part_id: str                    # Part number from BOM
    actions: List[str]              # Actions performed on this part
    task_ids: List[int]             # Associated task IDs
    complexity: str                 # simple/medium/complex/super_complex

class StationInfo(BaseModel):
    id: str
    total_time_ms: int
    workers: int
    assigned_tasks: List[int]
    
    # Phase 1.5 Part Tracking (NEW)
    parts_involved: List[PartOperation] = []     # Parts at this station
    part_operations: Dict[str, List[str]] = {}   # part_id → [actions]
    complexity_max: str = "simple"               # Highest complexity level

# Global part flow summary
class OptimizeResponse(BaseModel):
    # ... existing fields ...
    
    # Phase 1.5 Part Tracking (NEW)
    part_flow_summary: Dict[str, List[int]] = {}  # part_id → [station_indices]
    part_count: int = 0                           # Total unique parts
    complexity_distribution: Dict[str, int] = {}  # complexity → count
```

---

## Extended Data Flow (Phase 1.5) - Complexity Classification

### Complexity-Aware Processing Architecture

Phase 1.5 introduces **Assembly Complexity Classification** (REQ #10) to balance workload difficulty across stations and support operator skill assignment.

```
┌─────────────────────────────────────────────────────────────┐
│                Complexity Classification Layer               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Auto-Classification Engine                           │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Input: task with complexity_level (optional)   │  │  │
│  │  │                                                  │  │  │
│  │  │  If complexity_level is missing:                │  │  │
│  │  │    1. Extract keywords from part_id             │  │  │
│  │  │    2. Match against classification rules:       │  │  │
│  │  │       - simple: screw, clip, bracket, foam      │  │  │
│  │  │       - medium: fan, cable, thermal, mount      │  │  │
│  │  │       - complex: gpu, hdd, raid, nic, pcie      │  │  │
│  │  │       - super_complex: cto, custom, special     │  │  │
│  │  │    3. Assign complexity_level                   │  │  │
│  │  │                                                  │  │  │
│  │  │  Output: task with classified complexity        │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
│                                                             │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Complexity Balancing Solver                          │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Constraints:                                   │  │  │
│  │  │  1. Complexity score per station ≤ threshold    │  │  │
│  │  │     Score = Σ(weight[complexity] * task_count)  │  │  │
│  │  │     Weights: simple=1, medium=2,                │  │  │
│  │  │              complex=4, super_complex=8         │  │  │
│  │  │                                                  │  │  │
│  │  │  2. Minimize complexity variance across stations│  │  │
│  │  │     variance = max(score) - min(score)          │  │  │
│  │  │                                                  │  │  │
│  │  │  Objective: balance + minimize stations         │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    Output Generation                        │
│  {                                                          │
│    "stations": [                                            │
│      {                                                      │
│        "id": "WS-001",                                      │
│        "complexity_max": "complex",  // Highest complexity  │
│        "complexity_score": 12         // Weighted score     │
│      }                                                      │
│    ],                                                       │
│    "complexity_distribution": {                             │
│      "simple": 5, "medium": 3, "complex": 2               │
│    }                                                        │
│  }                                                          │
└─────────────────────────────────────────────────────────────┘
```

### Complexity Classification Use Cases

| Use Case                      | Description                                          | Benefits                              |
|-------------------------------|------------------------------------------------------|---------------------------------------|
| **Operator Skill Assignment** | Match station complexity to operator skill level     | Improve quality, reduce training time |
| **Training Planning**         | Identify simple stations for new operators           | Gradual skill development pathway     |
| **Quality Risk Management**   | Distribute complex tasks to prevent error clustering | Reduce defect rates                   |
| **Capacity Planning**         | Estimate manpower needs by complexity tier           | Better resource allocation            |
| **Process Improvement**       | Identify super_complex tasks for simplification      | Continuous improvement targets        |

---

## Combined Model Architecture (Phase 1.5)

### Integrated Processing Flow

Phase 1.5 **Combined Model** integrates all four extended features for comprehensive optimization:

```
┌─────────────────────────────────────────────────────────────┐
│               Combined Model Processing Flow                │
│                                                             │
│  CSV Input (with all extended columns)                      │
│    ↓                                                        │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Feature 1: Offline Task Filtering                   │  │
│  │  - Separate online (optimize) vs offline (fixed)     │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     ↓                                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Feature 3: Complexity Classification                │  │
│  │  - Auto-classify missing complexity_level            │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     ↓                                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Feature 4: Part-Task Mapping                        │  │
│  │  - Group tasks by part_id                            │  │
│  │  - Build part dependency graph                       │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     ↓                                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  CP-SAT Solver with Multi-Objective                  │  │
│  │  1. Standard: precedence, takt, workers              │  │
│  │  2. Part locality (minimize part travel)            │  │
│  │  3. Complexity balancing (variance)                 │  │
│  │  4. Merge opportunities (Feature 2)                 │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     ↓                                       │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Feature 2: Task Merging Post-Processing            │  │
│  │  - Identify merge candidates (same station + type)  │  │
│  │  - Apply efficiency gain                            │  │
│  └──────────────────┬───────────────────────────────────┘  │
│                     ↓                                       │
│  Comprehensive JSON Output (all KPIs)                       │
└─────────────────────────────────────────────────────────────┘
```

### Combined Model Benefits

- **Holistic Optimization**: Considers all factors simultaneously
- **Trade-off Analysis**: Balances part locality vs complexity vs merging
- **Realistic Modeling**: Accurately reflects production constraints
- **Maximum Efficiency**: Achieves best possible line balance

---

## System Components

### 1. Frontend Component (`dashboard.html`)

**Responsibility**:
- Display work order selection interface
- Collect user input (optimization objectives, takt time, etc.)
- Call backend API
- Render workstation allocation results (Gantt chart)

**Key Features**:
- **Responsive Design**: Adapts to 1024px+ screen resolution
- **Real-time Validation**: Client-side parameter checking
- **Interactive Charts**: Hover to view task details

**Technology Choices**:

| Technology         | Purpose            | Reason for Selection                        |
|--------------------|--------------------|---------------------------------------------|
| Tailwind CSS       | UI Styling         | Rapid prototyping, minimal custom CSS       |
| Chart.js           | Data Visualization | Lightweight, supports Gantt-like bar charts |
| Vanilla JavaScript | Interaction Logic  | No framework dependency, low complexity     |

**Code Structure**:
```html
<!DOCTYPE html>
<html>
<head>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
  <!-- Parameter Input Form -->
  <form id="optimizeForm">...</form>
  
  <!-- KPI Display Area -->
  <div id="kpiDisplay">...</div>
  
  <!-- Gantt Chart Container -->
  <canvas id="ganttChart"></canvas>
  
  <script>
    // API Call Logic
    async function callOptimizeAPI(formData) { ... }
    
    // Chart Rendering
    function renderChart(stations) { ... }
  </script>
</body>
</html>
```

---

### 2. Backend API Component (`api_server.py`)

**Responsibility**:
- Expose RESTful API endpoints
- Validate request parameters
- Invoke algorithm subprocess
- Transform algorithm output to frontend format

**Core Modules**:

#### 2.1 Configuration Management
```python
# Work Order Mapping Table
WORK_ORDER_MAPPING = {
    "WO_A": {
        "tasks_csv": "test_tasks.csv",
        "precedences_csv": "test_precedences.csv",
        "config_csv": "test_config.csv"
    },
    # ...
}
```

#### 2.2 Data Validation Layer
```python
from pydantic import BaseModel, Field

class OptimizeRequest(BaseModel):
    work_order_id: str
    optimization_goal: str
    target_takt: int = Field(gt=0)
    max_workers_per_station: int = Field(default=3, ge=1)
    fixed_stations: int = Field(default=0, ge=0)
```

**Validation Rules**:
- `target_takt`: Must be > 0
- `max_workers_per_station`: Must be ≥ 1
- `work_order_id`: Must exist in `WORK_ORDER_MAPPING`

#### 2.3 Algorithm Invocation Layer
```python
def run_optimization_algorithm(
    tasks_csv: str,
    precedences_csv: str,
    config_csv: str,
    objective: str,
    target_takt: int,
    max_workers: int,
    fixed_stations: int
) -> Dict[str, Any]:
    """
    Execute sche-algo.py via subprocess
    
    Timeout: 30 seconds
    Retry Policy: None (Phase 1)
    """
    cmd = [
        "python3", "sche-algo.py",
        "--tasks_csv", tasks_csv,
        "--objective", objective,
        # ... other parameters
    ]
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=30
    )
    
    # Parse JSON output
    return json.loads(result.stdout)
```

#### 2.4 Response Transformation Layer
```python
def parse_algorithm_output(
    algo_result: Dict[str, Any],
    work_order_id: str
) -> OptimizeResponse:
    """
    Convert algorithm output to API response format
    
    Transformations:
    - station_index → WS-001 format
    - Calculate utilization percentage
    - Extract bottleneck station
    """
    # ... implementation
```

**Error Handling Strategy**:

| Exception Type              | HTTP Status | Handling Method                         |
|-----------------------------|-------------|-----------------------------------------|
| `ValueError`                | 400         | Invalid parameter, return error message |
| `subprocess.TimeoutExpired` | 500         | Algorithm timeout                       |
| `FileNotFoundError`         | 500         | CSV file not found                      |
| Generic `Exception`         | 500         | Log stack trace, return generic error   |

---

### 3. Algorithm Component (`sche-algo.py`)

**Responsibility**:
- Parse CSV input files
- Build CP-SAT optimization model
- Execute solver
- Output results (JSON + CSV)

**Key Algorithms**:

#### 3.1 Boolean Assignment Model
```python
from ortools.sat.python import cp_model

model = cp_model.CpModel()

# Decision Variables: x[i][j] = 1 if task i is assigned to station j
x = {}
for i in range(num_tasks):
    for j in range(num_stations):
        x[(i, j)] = model.NewBoolVar(f'x_{i}_{j}')

# Constraints
# 1. Each task assigned to exactly one station
for i in range(num_tasks):
    model.Add(sum(x[(i, j)] for j in range(num_stations)) == 1)

# 2. Precedence constraints
for (pred, succ) in precedence_pairs:
    for j in range(num_stations):
        model.Add(
            sum(x[(pred, k)] for k in range(j+1)) >=
            x[(succ, j)]
        )

# 3. Takt time constraints (for min_manpower)
for j in range(num_stations):
    model.Add(
        sum(x[(i, j)] * task_durations[i] for i in range(num_tasks))
        <= target_takt * workers[j]
    )
```

**Optimization Objectives**:

1. **min_stations**: `minimize(num_stations)`
2. **min_manpower**: `minimize(sum(workers))`
3. **min_idle**: `minimize(sum(idle_time))`

**Performance Tuning**:
- **Search Parameters**: `num_search_workers=4` (multi-threading)
- **Time Limit**: `max_time_in_seconds=30`
- **Symmetry Breaking**: Add station ordering constraints

---

## Technology Stack

### Full Stack Overview

| Layer              | Component          | Technology         | Version        |
|--------------------|--------------------|--------------------|----------------|
| **Frontend**       | UI Framework       | Tailwind CSS       | 3.x (CDN)      |
|                    | Charting Library   | Chart.js           | 4.x (CDN)      |
|                    | HTTP Client        | Fetch API          | Native Browser |
| **Backend**        | Web Framework      | FastAPI            | 0.104+         |
|                    | Data Validation    | Pydantic           | 2.0+           |
|                    | Authentication     | JWT + OAuth2       | PyJWT 2.8+     |
|                    | ORM                | SQLAlchemy         | 2.0+           |
|                    | Migrations         | Alembic            | 1.12+          |
|                    | ASGI Server        | Uvicorn            | 0.24+          |
|                    | CORS Middleware    | FastAPI Middleware | Built-in       |
| **Data**           | Database           | PostgreSQL         | 15+            |
|                    | Cache              | Redis              | 7+             |
|                    | Connection Pool    | SQLAlchemy Pool    | Built-in       |
| **Algorithm**      | Solver             | Google OR-Tools    | 9.7+           |
|                    | CSV Parsing        | pandas             | 2.0+           |
|                    | JSON Output        | Python json        | Built-in       |
| **Infrastructure** | Containerization   | Docker             | 24+            |
|                    | Orchestration      | Docker Compose     | 2.x            |
|                    | Package Management | pip                | 23+            |

### Dependency Relationships

```
api_server.py
  ├── FastAPI (Web Framework)
  ├── Pydantic (Validation)
  ├── SQLAlchemy (Database ORM)
  ├── JWT (Authentication)
  ├── Redis (Caching)
  ├── subprocess (Algorithm Invocation)
  └── dashboard.html (Static File Serving)

sche-algo.py
  ├── ortools (Optimization Solver)
  ├── pandas (CSV I/O)
  └── argparse (CLI Parsing)

database/
  ├── PostgreSQL (Primary Storage)
  ├── Redis (Session & Cache)
  └── Alembic (Schema Migrations)
```

### New Database Dependencies

```python
# requirements.txt additions for Phase 1 database integration
psycopg2-binary>=2.9.7    # PostgreSQL adapter
redis>=5.0.0              # Redis client
sqlalchemy>=2.0.0         # ORM
alembic>=1.12.0           # Database migrations
pyjwt>=2.8.0              # JWT authentication
passlib>=1.7.4            # Password hashing
python-multipart>=0.0.6   # File upload support
```

---

## Database Integration & API Design

### Core Database Schema (Phase 1)

The Phase 1 database schema supports multi-tenant manufacturing data with the following core entities:

```sql
-- Multi-tenant organization structure
organizations (id, name, slug, created_at)
  └── sites (id, organization_id, name, location)
      └── users (id, organization_id, email, role, site_access[])
      └── work_orders (id, site_id, work_order_id, product_sku, status)
          └── tasks (id, work_order_id, task_id, duration_ms, action_type)
          └── optimizations (id, work_order_id, solver_status, total_stations)
              └── stations (id, optimization_id, station_id, total_load_ms)
                  └── task_assignments (id, station_id, task_id, sequence_order)
```

### Key API Endpoints (Phase 1)

```yaml
# Authentication
POST /auth/login                    # User authentication with JWT
POST /auth/refresh                  # Token refresh

# Work Order Management
POST /api/v1/work-orders            # Create work order
POST /api/v1/work-orders/{id}/tasks/bulk  # Upload CSV task data

# Optimization
POST /api/v1/optimizations          # Execute line balancing
GET  /api/v1/optimizations/{id}     # Get optimization results
GET  /api/v1/optimizations/{id}/workstations  # Get station details
GET  /api/v1/optimizations/{id}/takt-summary  # Get KPI summary
```

### Data Input Schema Support

Phase 1 supports progressive CSV schema evolution:

| Schema Version         | Columns                                | Support |
|------------------------|----------------------------------------|---------|
| **Phase 1 Basic**      | task_id, duration, predecessors        | ✅ Full  |
| **Phase 1.5 Extended** | +offline_flag, adjustable, action_type | ✅ Full  |
| **Phase 1.5 Complete** | +complexity_level, part_id             | ✅ Full  |

### Database Performance Features

- **Connection Pooling**: SQLAlchemy with 20 connection pool size
- **Query Optimization**: Strategic indexing for optimization lookups
- **Caching Layer**: Redis for 1-hour TTL on optimization results  
- **Multi-tenant Isolation**: Row Level Security (RLS) policies
- **Migration Support**: Alembic for schema versioning

---

## Data Flow

### Complete Request Flow

```
┌─────────┐  (1) User Input      ┌─────────────┐
│ Browser │ ──────────────────── │ dashboard.  │
│         │                      │   html      │
└────┬────┘                      └──────┬──────┘
     │                                  │
     │ (2) HTTP POST /optimize          │
     │    {                             │
     │      "work_order_id": "WO_A",    │
     │      "optimization_goal": "...", │
     │      "target_takt": 30000        │
     │    }                             │
     │                                  │
     └──────────────────────────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │   FastAPI Request Handler    │
     │  ┌────────────────────────┐  │
     │  │ (3) Pydantic Validation│  │  ──┐
     │  │  - Type Checking       │  │    │ 400 Bad Request
     │  │  - Range Validation    │  │  ◄─┘ (if validation fails)
     │  └────────────────────────┘  │
     │  ┌────────────────────────┐  │
     │  │ (4) Work Order Lookup  │  │
     │  │  WO_A → CSV Files      │  │
     │  └────────────────────────┘  │
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │   subprocess.run()           │
     │  ┌────────────────────────┐  │
     │  │ (5) Build Command      │  │
     │  │  python3 sche-algo.py  │  │
     │  │    --tasks_csv ...     │  │
     │  │    --objective ...     │  │
     │  └────────────────────────┘  │
     │  ┌────────────────────────┐  │
     │  │ (6) Execute (30s max)  │  │  ──┐
     │  │  - Parse CSV           │  │    │ 500 Timeout
     │  │  - Build CP-SAT Model  │  │  ◄─┘
     │  │  - Solve               │  │
     │  │  - Generate JSON       │  │
     │  └────────────────────────┘  │
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │  parse_algorithm_output()    │
     │  ┌────────────────────────┐  │
     │  │ (7) Transform Data     │  │
     │  │  - station_index → ID  │  │
     │  │  - Calculate KPIs      │  │
     │  │  - Build Response DTO  │  │
     │  └────────────────────────┘  │
     └──────────────┬───────────────┘
                    │
                    ▼
     ┌──────────────────────────────┐
     │   HTTP Response (JSON)       │
     │  {                           │
     │    "work_order_id": "WO_A",  │
     │    "stations": [...],        │
     │    "takt_time_ms": 30000,    │
     │    "solve_time_sec": 0.85    │
     │  }                           │
     └──────────────┬───────────────┘
                    │
                    ▼
┌────────────────────────────────────┐
│  Frontend Rendering               │
│  ┌──────────────────────────────┐ │
│  │ (8) Update KPI Display       │ │
│  │  - Takt Time                 │ │
│  │  - Manpower                  │ │
│  │  - Utilization               │ │
│  └──────────────────────────────┘ │
│  ┌──────────────────────────────┐ │
│  │ (9) Render Gantt Chart       │ │
│  │  - Chart.js Bar Chart        │ │
│  │  - Color by Utilization      │ │
│  └──────────────────────────────┘ │
└────────────────────────────────────┘
```

### Data Format Transformations

**Stage 1: Frontend → Backend**
```javascript
// Frontend Form Data
{
  workOrderId: "WO_A",
  optimizationGoal: "min_stations",
  targetTakt: 30000
}

// ↓ JSON Serialization ↓

// HTTP Request Body
{
  "work_order_id": "WO_A",
  "optimization_goal": "min_stations",
  "target_takt": 30000
}
```

**Stage 2: Backend → Algorithm**
```bash
# Command-line Arguments
python3 sche-algo.py \
  --tasks_csv data/test_tasks.csv \
  --objective min_stations \
  --json_output /tmp/result.json
```

**Stage 3: Algorithm → Backend**
```json
// sche-algo.py Output (JSON)
{
  "objective": "min_stations",
  "kpis": {
    "calculated_takt": 30000,
    "stations": [
      {
        "station_index": 0,
        "load": 28500,
        "idle_vs_bottleneck": 1500,
        "workers": 1
      }
    ]
  },
  "assignment": {
    "0": 0,  // Task 0 → Station 0
    "1": 0
  }
}
```

**Stage 4: Backend → Frontend**
```json
// API Response (Transformed)
{
  "work_order_id": "WO_A",
  "stations": [
    {
      "id": "WS-001",              // Formatted ID
      "total_time_ms": 28500,
      "idle_time_ms": 1500,
      "workers": 1,
      "utilization_pct": 95.0,     // Calculated
      "assigned_tasks": [0, 1]
    }
  ],
  "takt_time_ms": 30000,
  "solve_time_sec": 0.85
}
```

---

## 📐 Extended Data Flow (Phase 1.5)

Phase 1.5 adds support for offline task handling (REQ #4, #15) and adjustable task merging (REQ #13).

### Extended Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│  CSV Input Processing (Extended)                            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  read_problem_from_csv_extended()                     │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Parse Extended Columns                         │  │  │
│  │  │  - offline_flag (0=online, 1=offline)           │  │  │
│  │  │  - adjustable (0=fixed, 1=adjustable)           │  │  │
│  │  │  - action_type (screw, glue, clip, test)        │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  └────────────────────┼───────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Task Classification Layer (NEW)                            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  filter_and_classify_tasks()                          │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Separate Tasks by Type                         │  │  │
│  │  │  ├── online_tasks = [t for t if offline==0]     │  │  │
│  │  │  ├── offline_tasks = [t for t if offline==1]    │  │  │
│  │  │  ├── adjustable_tasks = [t for t if adj==1]     │  │  │
│  │  │  └── fixed_tasks = [t for t if adj==0]          │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  │                    │                                   │  │
│  │  ┌─────────────────▼───────────────────────────────┐  │  │
│  │  │  Identify Merge Candidates                      │  │  │
│  │  │  - Group adjustable tasks by action_type        │  │  │
│  │  │  - Create merge pairs (same action_type)        │  │  │
│  │  │  - Example: tasks [1,3,6] all "screw" → pairs  │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  CP-SAT Solver (Modified for Phase 1.5)                     │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  solve_with_extensions()                              │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Decision Variables (Extended)                  │  │  │
│  │  │  - assign[t, p]: task → station (online only)   │  │  │
│  │  │  - merge[(t1,t2)]: merge decision vars          │  │  │
│  │  │  - effective_duration[t]: adjusted duration     │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  │                    │                                   │  │
│  │  ┌─────────────────▼───────────────────────────────┐  │  │
│  │  │  Constraints (Extended)                         │  │  │
│  │  │  1. Assignment (online tasks only)              │  │  │
│  │  │     model.Add(sum(assign[t,p] for p) == 1)      │  │  │
│  │  │                                                  │  │  │
│  │  │  2. Precedence (online-to-online only)          │  │  │
│  │  │     if both tasks online: apply constraint      │  │  │
│  │  │     if before offline: assume satisfied         │  │  │
│  │  │                                                  │  │  │
│  │  │  3. Capacity (with effective duration)          │  │  │
│  │  │     sum(assign[t,p] * eff_dur[t]) <= cycle_time │  │  │
│  │  │                                                  │  │  │
│  │  │  4. Merge Constraints (NEW)                     │  │  │
│  │  │     If merge[(t1,t2)] == 1:                     │  │  │
│  │  │       → assign[t1,p] == assign[t2,p]            │  │  │
│  │  │       → eff_dur[t1] = 0.9*(dur[t1]+dur[t2])     │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  │                    │                                   │  │
│  │  ┌─────────────────▼───────────────────────────────┐  │  │
│  │  │  Objective Function (Enhanced)                  │  │  │
│  │  │  - Primary: minimize num_stations               │  │  │
│  │  │  - Secondary: maximize merge_count              │  │  │
│  │  │  - Formulation: min(stations*1000 - merges)     │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  Post-Processing (Offline Task Assignment)                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  assign_offline_tasks()                               │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  For each offline task:                         │  │  │
│  │  │    assignment[t] = -1  (special marker)         │  │  │
│  │  │    offline_station["tasks"].append(t)           │  │  │
│  │  │    offline_station["load"] += duration[t]       │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  KPI Calculation (Extended)                                 │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  compute_kpis_extended()                              │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Standard KPIs (for online tasks)               │  │  │
│  │  │  - total_stations, bottleneck_load, etc.        │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  │                    │                                   │  │
│  │  ┌─────────────────▼───────────────────────────────┐  │  │
│  │  │  Offline Metrics (NEW)                          │  │  │
│  │  │  - offline_tasks_count = len(offline_tasks)     │  │  │
│  │  │  - offline_total_time = sum(durations)          │  │  │
│  │  │  - online_stations = stations with online only  │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  │                    │                                   │  │
│  │  ┌─────────────────▼───────────────────────────────┐  │  │
│  │  │  Merge Metrics (NEW)                            │  │  │
│  │  │  - merged_pairs = [(t1,t2) where merge==1]      │  │  │
│  │  │  - merge_count = len(merged_pairs)              │  │  │
│  │  │  - efficiency_gain = time_saved / original * 100│  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│  JSON Output (Extended Format)                              │
│  {                                                           │
│    "kpis": {                                                 │
│      "total_stations": 3,                                    │
│      "online_stations": 2,                                   │
│      "offline_tasks_count": 3,                               │
│      "merged_tasks_count": 2,                                │
│      "merge_efficiency_gain": 10.5                           │
│    },                                                        │
│    "stations": [                                             │
│      {                                                       │
│        "station_index": 0,                                   │
│        "online_tasks": [1, 3],                               │
│        "offline_tasks": [],                                  │
│        "adjustable_tasks": [1, 3],                           │
│        "merged_task_pairs": ["1-3"],                         │
│        "online_load": 7,                                     │
│        "offline_load": 0                                     │
│      },                                                      │
│      {                                                       │
│        "station_index": -1,  // Offline station marker      │
│        "offline_tasks": [2, 5, 8],                           │
│        "offline_load": 12                                    │
│      }                                                       │
│    ]                                                         │
│  }                                                           │
└─────────────────────────────────────────────────────────────┘
```

### Extended API Request/Response

**Phase 1.5 API Request (Extended)**:
```json
POST /optimize
{
  "work_order_id": "WO_A",
  "optimization_goal": "min_stations",
  "target_takt": 60,
  "max_workers_per_station": 3,
  
  // Phase 1.5 NEW fields
  "enable_offline_handling": true,
  "enable_task_merging": true,
  "merge_efficiency_gain": 0.10
}
```

**Phase 1.5 API Response (Extended)**:
```json
{
  "work_order_id": "WO_A",
  "optimization_goal": "min_stations",
  "stations": [
    {
      "id": "WS-001",
      "total_time_ms": 45000,
      "idle_time_ms": 15000,
      "workers": 2,
      "utilization_pct": 75.0,
      "assigned_tasks": [1, 2, 3],
      
      // Phase 1.5 NEW fields
      "online_tasks": [1, 3],
      "offline_tasks": [2],
      "adjustable_tasks": [1, 3],
      "merged_task_pairs": [[1, 3]],
      "online_load_ms": 42000,
      "offline_load_ms": 3000
    },
    {
      "id": "OFFLINE-001",
      "total_time_ms": 18000,
      "workers": 0,
      "assigned_tasks": [4, 5, 6],
      "online_tasks": [],
      "offline_tasks": [4, 5, 6],
      "offline_load_ms": 18000
    }
  ],
  "takt_time_ms": 60000,
  "total_workers": 2,
  "solve_time_sec": 1.25,
  
  // Phase 1.5 NEW fields
  "online_stations": 1,
  "offline_tasks_count": 4,
  "offline_total_time_ms": 21000,
  "merged_tasks_count": 1,
  "merge_efficiency_gain_pct": 10.5
}
```

### Data Validation Flow (Phase 1.5)

```
┌────────────────────────────────────┐
│  Frontend Form Validation         │
│  - Check target_takt > 0           │
│  - Check work_order_id exists      │
│  - Validate boolean flags          │
└──────────────┬─────────────────────┘
               │
               ▼
┌────────────────────────────────────┐
│  Pydantic Validation (Extended)    │
│  class OptimizeRequest:            │
│    enable_offline_handling: bool   │
│    enable_task_merging: bool       │
│    merge_efficiency_gain: float    │
│                                    │
│  Validators:                       │
│  - 0 <= merge_efficiency <= 0.5    │
└──────────────┬─────────────────────┘
               │
               ▼
┌────────────────────────────────────┐
│  CSV Schema Validation             │
│  - Check offline_flag in {0, 1}    │
│  - Check adjustable in {0, 1}      │
│  - Validate action_type not empty  │
└──────────────┬─────────────────────┘
               │
               ▼
┌────────────────────────────────────┐
│  Business Logic Validation         │
│  - Warn if all tasks offline       │
│  - Warn if no adjustable tasks     │
│  - Check merge candidates exist    │
└────────────────────────────────────┘
```

---


## Deployment Architecture

### Development Environment

**Local Deployment** (Bare Metal):
```bash
# Terminal 1: Start API Server
cd /workspace/line-balance
python3 src/api_server.py

# Terminal 2: Open Browser
http://localhost:8000
```

**File Structure**:
```
/workspace/line-balance/
├── src/
│   ├── api_server.py       # FastAPI Application
│   └── dashboard.html      # Frontend Page
├── data/                   # CSV Input Files
├── sche-algo.py            # Algorithm Script
└── requirements.txt        # Dependencies
```

---

### Docker Deployment

**Architecture Diagram**:
```
┌─────────────────────────────────────┐
│   Docker Host (Linux/WSL2)          │
│  ┌───────────────────────────────┐  │
│  │  Container: line-balance      │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │  Uvicorn (Port 8000)    │  │  │ ◄─── HTTP Requests
│  │  │   ├── api_server.py     │  │  │      (from host)
│  │  │   └── sche-algo.py      │  │  │
│  │  └─────────────────────────┘  │  │
│  │  ┌─────────────────────────┐  │  │
│  │  │  Volume Mounts          │  │  │
│  │  │   - ./data → /data      │  │  │
│  │  │   - ./output → /output  │  │  │
│  │  └─────────────────────────┘  │  │
│  └───────────────────────────────┘  │
└─────────────────────────────────────┘
         │
         │ Port Mapping: 8000:8000
         ▼
    http://localhost:8000
```

**Key Configuration** (`docker-compose.yml`):
```yaml
version: '3.8'
services:
  line-balance:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./data:/workspace/data
      - ./output:/workspace/output
    environment:
      - PYTHONUNBUFFERED=1
    command: python3 src/api_server.py
```

**Dockerfile**:
```dockerfile
FROM python:3.10-slim

WORKDIR /workspace

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000

CMD ["python3", "src/api_server.py"]
```

---

## Security Design

### Phase 1 Security Posture

**Current Status**:
- ❌ No authentication
- ❌ No authorization
- ✅ CORS enabled (allow all origins for development)
- ✅ Input validation (Pydantic)

**Known Risks**:

| Risk                    | Severity | Mitigation Plan (Future)             |
|-------------------------|----------|--------------------------------------|
| Unrestricted API Access | High     | Implement JWT authentication         |
| CSV Injection           | Medium   | Add file content validation          |
| DoS via Large Requests  | Medium   | Add rate limiting (e.g., 10 req/min) |
| Algorithm Timeout Abuse | Low      | Already limited to 30 seconds        |

### Input Validation Mechanisms

**Pydantic Validation**:
```python
class OptimizeRequest(BaseModel):
    target_takt: int = Field(gt=0, le=1000000)  # Range: 1-1,000,000 ms
    max_workers_per_station: int = Field(ge=1, le=10)
    
    @validator('work_order_id')
    def validate_work_order(cls, v):
        if v not in WORK_ORDER_MAPPING:
            raise ValueError(f'Invalid work_order_id: {v}')
        return v
```

**File Path Sanitization**:
```python
# Prevent directory traversal
def safe_file_path(filename: str) -> Path:
    base_dir = Path("/workspace/data")
    target = (base_dir / filename).resolve()
    
    if not target.is_relative_to(base_dir):
        raise ValueError("Invalid file path")
    
    return target
```

---

## Performance Optimization

### Backend Performance

**Target Metrics**:
- **API Latency**: < 3 seconds (95th percentile)
- **Throughput**: ≥ 10 requests/minute
- **Memory Usage**: < 512 MB per request

**Optimization Strategies**:

1. **Subprocess Reuse** (Future):
   ```python
   # Use process pool instead of subprocess.run()
   from concurrent.futures import ProcessPoolExecutor
   
   executor = ProcessPoolExecutor(max_workers=4)
   future = executor.submit(run_algo, ...)
   result = future.result(timeout=30)
   ```

2. **Response Caching** (Future):
   ```python
   from functools import lru_cache
   
   @lru_cache(maxsize=128)
   def optimize_cached(work_order_id, target_takt, ...):
       # Cache identical requests
       ...
   ```

3. **Async I/O**:
   ```python
   # Already using FastAPI's async handlers
   @app.post("/optimize")
   async def optimize(...):
       # Non-blocking request handling
   ```

### Algorithm Performance

**CP-SAT Tuning**:
```python
solver = cp_model.CpSolver()

# Multi-threading
solver.parameters.num_search_workers = 4

# Time limit
solver.parameters.max_time_in_seconds = 30

# Search strategy
solver.parameters.search_branching = cp_model.FIXED_SEARCH
```

**Data Volume Limits**:
- Phase 1: ≤ 500 tasks
- Memory: ~100 MB per 500 tasks
- Solve Time: ~1-3 seconds (typical case)

---

## Appendix

### A. API Endpoint Mapping Table

| Endpoint        | Method | Purpose                   | Phase |
|-----------------|--------|---------------------------|-------|
| `/`             | GET    | Serve frontend HTML       | 1     |
| `/optimize`     | POST   | Core optimization         | 1     |
| `/workstations` | GET    | Query workstation summary | 1     |
| `/takt-summary` | GET    | Query takt analysis       | 1     |
| `/health`       | GET    | Service health check      | 1     |
| `/api/docs`     | GET    | Swagger UI                | 1     |
| `/export`       | GET    | Export results (CSV/XLSX) | 1 ⚠️ NEW |
| `/basic-data/*` | CRUD   | Basic data maintenance    | 1 ⚠️ NEW |

---

## Basic Data Maintenance Portal (REQ #33) ⚠️ NEW

### Portal Overview

A web-based maintenance interface for managing core data elements:

1. **Class Code Management**: CRUD operations for action class codes
2. **Touch Time (TT) Maintenance**: Standard time updates per action
3. **Assembly Sequence Editing**: Precedence relationship management

### Portal Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                 Basic Data Maintenance Portal               │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  portal.html (Maintenance UI)                         │  │
│  │  ┌─────────────────┬─────────────────┬──────────────┐ │  │
│  │  │ Class Code Tab  │ Touch Time Tab  │ Sequence Tab │ │  │
│  │  │ - List/Filter   │ - List/Filter   │ - Graph View │ │  │
│  │  │ - Add/Edit/Del  │ - Add/Edit/Del  │ - Drag/Drop  │ │  │
│  │  │ - Import CSV    │ - Import CSV    │ - Validate   │ │  │
│  │  └─────────────────┴─────────────────┴──────────────┘ │  │
│  └───────────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                         │ REST API
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Basic Data API Layer                      │
│  - GET/POST/PUT/DELETE /basic-data/class-codes              │
│  - GET/POST/PUT/DELETE /basic-data/touch-times              │
│  - GET/POST/PUT/DELETE /basic-data/sequences                │
│  - POST /basic-data/import (CSV bulk import)                │
│  - GET /basic-data/export (CSV bulk export)                 │
└─────────────────────────────────────────────────────────────┘
```

### API Endpoints for Basic Data Maintenance

#### Class Code Management

```
GET    /basic-data/class-codes              # List all class codes
GET    /basic-data/class-codes/{code_id}    # Get single class code
POST   /basic-data/class-codes              # Create class code
PUT    /basic-data/class-codes/{code_id}    # Update class code
DELETE /basic-data/class-codes/{code_id}    # Delete class code
```

**Class Code Schema**:
```json
{
  "code_id": "SCREW_M3_INSTALL",
  "code_name": "Install M3 Screw",
  "category": "screw",
  "motion_type": "wrist",
  "default_duration_ms": 3500,
  "complexity_level": "simple",
  "equipment_required": ["TORQUE_DRV_M3"],
  "part_families": ["SCREW_M3", "SCREW_M4"],
  "description": "Standard M3 screw installation with torque verification",
  "created_at": "2025-12-12T10:00:00Z",
  "updated_by": "john.doe@company.com"
}
```

#### Touch Time Management

```
GET    /basic-data/touch-times              # List all touch times
GET    /basic-data/touch-times/{tt_id}      # Get single touch time
POST   /basic-data/touch-times              # Create touch time
PUT    /basic-data/touch-times/{tt_id}      # Update touch time
DELETE /basic-data/touch-times/{tt_id}      # Delete touch time
```

**Touch Time Schema**:
```json
{
  "tt_id": "TT_001",
  "class_code": "SCREW_M3_INSTALL",
  "part_id": "SCREW_M3_BRACKET",
  "product_family": "DL360_G11",
  "site_id": "TAO_FACTORY_A",
  "touch_time_ms": 3200,
  "measurement_date": "2025-11-15",
  "sample_size": 50,
  "std_deviation_ms": 350,
  "min_time_ms": 2800,
  "max_time_ms": 4100,
  "notes": "Measured during MP phase, experienced workers",
  "created_at": "2025-11-16T10:00:00Z"
}
```

#### Sequence Management

```
GET    /basic-data/sequences/{work_order_id}    # Get sequence for WO
POST   /basic-data/sequences                    # Create/update sequence
PUT    /basic-data/sequences/{work_order_id}    # Update sequence
DELETE /basic-data/sequences/{seq_id}           # Delete sequence entry
```

**Sequence Schema**:
```json
{
  "work_order_id": "WO_DL360_G11",
  "sequence": [
    {
      "task_id": 1,
      "class_code": "UNPACK_CHASSIS",
      "predecessors": [],
      "position": 1
    },
    {
      "task_id": 2,
      "class_code": "INSTALL_PSU",
      "predecessors": [1],
      "position": 2
    }
  ],
  "total_tasks": 45,
  "version": "1.2",
  "updated_at": "2025-12-12T10:00:00Z"
}
```

#### Bulk Import/Export

```
POST /basic-data/import
Content-Type: multipart/form-data
- file: CSV file
- type: "class_codes" | "touch_times" | "sequences"
- mode: "append" | "replace"

GET /basic-data/export?type=class_codes&format=csv
```

### UI Components

| Component | Technology | Features |
|-----------|------------|----------|
| Data Grid | AG-Grid or Tabulator | Sorting, filtering, inline edit |
| Form Dialog | Modal with validation | Add/edit with real-time validation |
| CSV Import | File upload + preview | Preview before commit, error highlighting |
| Sequence Editor | D3.js or Vis.js graph | Visual precedence graph, drag-drop |
| Audit Trail | Timeline view | Track all changes with user/timestamp |

---

### B. Environment Variables

| Variable         | Default                          | Description            |
|------------------|----------------------------------|------------------------|
| `WORKSPACE_ROOT` | `/workspace`                     | Project root directory |
| `DATA_DIR`       | `${WORKSPACE_ROOT}/data`         | CSV file storage       |
| `ALGO_SCRIPT`    | `${WORKSPACE_ROOT}/sche-algo.py` | Algorithm script path  |

### C. Log Format

```
[2025-01-14 10:30:45] INFO - [API] Executing command: python3 sche-algo.py --tasks_csv ...
[2025-01-14 10:30:46] INFO - [API] Algorithm completed, time: 0.85 seconds
```

---

**Document Maintainer:** JASON YY, LIN  
**Last Updated:** 2025-11-06
**Version:** 1.5.0-phase1
