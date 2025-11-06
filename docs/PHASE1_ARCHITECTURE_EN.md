# Phase 1 Architecture Design

**Document Version**: 1.0 | **Last Updated**: 2025-11-06  
**Related Documents**:
- [Implementation Guide](PHASE1_IMPLEMENTATION_EN.md)
- [API Specification](PHASE1_API_SPEC_EN.md)
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

Phase 1 adopts a **three-tier architecture** to achieve separation of concerns and modular scalability:

1. **Presentation Layer** (Frontend)
   - Technology: HTML5 + Tailwind CSS + Chart.js
   - Responsibility: User interaction, data visualization

2. **Service Layer** (Backend API)
   - Technology: FastAPI + Pydantic
   - Responsibility: Request validation, business logic orchestration

3. **Algorithm Layer** (Optimization Engine)
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
                         │ subprocess.run()
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Algorithm Layer                            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  sche-algo.py (OR-Tools Solver)                       │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Input Processing                               │  │  │
│  │  │  - CSV Parsing (tasks/precedences/config)       │  │  │
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
│  │  │  - CSV (Station/KPI Details)                    │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

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

| Technology | Purpose | Reason for Selection |
|-----------|---------|---------------------|
| Tailwind CSS | UI Styling | Rapid prototyping, minimal custom CSS |
| Chart.js | Data Visualization | Lightweight, supports Gantt-like bar charts |
| Vanilla JavaScript | Interaction Logic | No framework dependency, low complexity |

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

| Exception Type | HTTP Status | Handling Method |
|---------------|-------------|-----------------|
| `ValueError` | 400 | Invalid parameter, return error message |
| `subprocess.TimeoutExpired` | 500 | Algorithm timeout |
| `FileNotFoundError` | 500 | CSV file not found |
| Generic `Exception` | 500 | Log stack trace, return generic error |

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

| Layer | Component | Technology | Version |
|-------|-----------|-----------|---------|
| **Frontend** | UI Framework | Tailwind CSS | 3.x (CDN) |
| | Charting Library | Chart.js | 4.x (CDN) |
| | HTTP Client | Fetch API | Native Browser |
| **Backend** | Web Framework | FastAPI | 0.104+ |
| | Data Validation | Pydantic | 2.0+ |
| | ASGI Server | Uvicorn | 0.24+ |
| | CORS Middleware | FastAPI Middleware | Built-in |
| **Algorithm** | Solver | Google OR-Tools | 9.7+ |
| | CSV Parsing | pandas | 2.0+ |
| | JSON Output | Python json | Built-in |
| **Infrastructure** | Containerization | Docker | 24+ |
| | Orchestration | Docker Compose | 2.x |
| | Package Management | pip | 23+ |

### Dependency Relationships

```
api_server.py
  ├── FastAPI (Web Framework)
  ├── Pydantic (Validation)
  ├── subprocess (Algorithm Invocation)
  └── dashboard.html (Static File Serving)

sche-algo.py
  ├── ortools (Optimization Solver)
  ├── pandas (CSV I/O)
  └── argparse (CLI Parsing)
```

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

| Risk | Severity | Mitigation Plan (Future) |
|------|----------|-------------------------|
| Unrestricted API Access | High | Implement JWT authentication |
| CSV Injection | Medium | Add file content validation |
| DoS via Large Requests | Medium | Add rate limiting (e.g., 10 req/min) |
| Algorithm Timeout Abuse | Low | Already limited to 30 seconds |

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

| Endpoint | Method | Purpose | Phase |
|----------|--------|---------|-------|
| `/` | GET | Serve frontend HTML | 1 |
| `/optimize` | POST | Core optimization | 1 |
| `/workstations` | GET | Query workstation summary | 1 |
| `/takt-summary` | GET | Query takt analysis | 1 |
| `/health` | GET | Service health check | 1 |
| `/api/docs` | GET | Swagger UI | 1 |

### B. Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `WORKSPACE_ROOT` | `/workspace` | Project root directory |
| `DATA_DIR` | `${WORKSPACE_ROOT}/data` | CSV file storage |
| `ALGO_SCRIPT` | `${WORKSPACE_ROOT}/sche-algo.py` | Algorithm script path |

### C. Log Format

```
[2025-01-14 10:30:45] INFO - [API] Executing command: python3 sche-algo.py --tasks_csv ...
[2025-01-14 10:30:46] INFO - [API] Algorithm completed, time: 0.85 seconds
```

---

**Document End** | For questions contact architecture team
