# Phase 1 Implementation Guide

## Overview

This document explains the implementation architecture, deployment steps, and verification methods for the Line Balance System Phase 1 MVP.

**Reference Documents:**
- `docs/stage-specs.md` - Stage Specifications
- `docs/feasibility-assessment.md` - Feasibility Assessment
- `IO_SPECIFICATION_ZH.md` - Input/Output Specifications

**Build Date:** 2025-11-06  
**Phase:** Phase 1 - Minimum Viable Product (MVP)

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      User Interface Layer                    │
│  ┌────────────────────────────────────────────────────┐     │
│  │  dashboard.html (Frontend UI)                      │     │
│  │  - Work order selection (WO_A, WO_B, WO_C)        │     │
│  │  - Takt time slider (40~200 seconds)              │     │
│  │  - Optimization objective selection                │     │
│  │  - KPI dashboard + load charts                    │     │
│  └────────────────────────────────────────────────────┘     │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/JSON
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                      API Service Layer                       │
│  ┌────────────────────────────────────────────────────┐     │
│  │  api_server.py (FastAPI)                           │     │
│  │                                                     │     │
│  │  Endpoints:                                        │     │
│  │  - POST /optimize (core optimization)              │     │
│  │  - GET  /workstations (query stations)            │     │
│  │  - GET  /takt-summary (takt summary)              │     │
│  │  - GET  /health (health check)                    │     │
│  └────────────────────────────────────────────────────┘     │
└──────────────────────┬──────────────────────────────────────┘
                       │ subprocess
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                    Algorithm Core Layer                      │
│  ┌────────────────────────────────────────────────────┐     │
│  │  sche-algo.py (Google OR-Tools)                    │     │
│  │                                                     │     │
│  │  Models:                                           │     │
│  │  - Boolean Model (min_stations)                   │     │
│  │  - Manpower Model (min_manpower)                  │     │
│  │  - Idle Model (min_idle)                          │     │
│  │                                                     │     │
│  │  Input: CSV (tasks, precedences, config)          │     │
│  │  Output: JSON (assignment + KPIs)                 │     │
│  └────────────────────────────────────────────────────┘     │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                      Data Layer                              │
│  data/                                                       │
│  ├── test_tasks.csv (task definitions)                      │
│  ├── test_precedences.csv (precedence relations)            │
│  └── test_config.csv (configuration parameters)             │
└─────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

### Frontend Technologies

| Technology   | Version | Purpose            | Rationale                               |
|--------------|---------|--------------------|-----------------------------------------|
| HTML5        | -       | Page structure     | Standard, lightweight, no build         |
| Tailwind CSS | 3.x     | UI styling         | Rapid development, modern design        |
| Chart.js     | 4.x     | Data visualization | Easy to use, comprehensive docs         |
| Vanilla JS   | ES6+    | Interactive logic  | No framework needed, reduced complexity |

### Backend Technologies

| Technology | Version | Purpose         | Rationale                                |
|------------|---------|-----------------|------------------------------------------|
| Python     | 3.10+   | Main language   | Rich ecosystem, OR-Tools support         |
| FastAPI    | 0.104+  | Web framework   | High performance, auto docs, type safety |
| Uvicorn    | 0.24+   | ASGI server     | Asynchronous, high performance           |
| Pydantic   | 2.0+    | Data validation | Strong typing, automatic validation      |

### Algorithm Technologies

| Technology | Version | Purpose           | Rationale                          |
|------------|---------|-------------------|------------------------------------|
| OR-Tools   | 9.7+    | CP-SAT solver     | Google official, mature and stable |
| absl-py    | 2.0+    | Command-line args | Good integration with OR-Tools     |

### Deployment Technologies (Optional)

| Technology     | Version | Purpose                       | Rationale                                |
|----------------|---------|-------------------------------|------------------------------------------|
| Docker         | 24+     | Containerization              | Environment consistency, easy deployment |
| Docker Compose | 2.x     | Multi-container orchestration | Simplified local dev environment         |

---

## Quick Start

### 1. Environment Setup

```bash
# Create virtual environment
cd /mnt/d/workspace/line-balance
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or .\venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

**requirements.txt contents:**
```
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
ortools>=9.7.0
absl-py>=2.0.0
```

### 2. Verify Algorithm

```bash
# Test algorithm execution
python3 src/sche-algo.py \
  --tasks_csv data/test_tasks.csv \
  --precedences_csv data/test_precedences.csv \
  --objective min_stations \
  --json_output output/test_result.json

# Check output
cat output/test_result.json
```

### 3. Start API Service

```bash
# Method 1: Direct execution
python3 src/api_server.py

# Method 2: Use uvicorn (adjustable parameters)
uvicorn src.api_server:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload  # Auto-reload in development mode
```

**Success indicators:**
```
================================================================================
Line Balance System API Service - Phase 1 MVP
================================================================================
Workspace: /mnt/d/workspace/line-balance
Data directory: /mnt/d/workspace/line-balance/data
Algorithm: /mnt/d/workspace/line-balance/src/sche-algo.py
Available work orders: ['WO_A', 'WO_B', 'WO_C']
================================================================================
Server running at http://localhost:8000
API documentation: http://localhost:8000/api/docs
================================================================================
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### 4. Access Frontend Interface

Open browser and visit: **http://localhost:8000**

---

## API Usage Examples

### Endpoint 1: POST /optimize (Core Optimization)

**Request Example:**
```bash
curl -X POST "http://localhost:8000/optimize" \
  -H "Content-Type: application/json" \
  -d '{
    "work_order_id": "WO_A",
    "target_takt": 80000,
    "optimization_goal": "min_stations",
    "max_workers_per_station": 8,
    "fixed_stations": 0
  }'
```

**Response Example (simplified):**
```json
{
  "work_order_id": "WO_A",
  "objectives": {
    "goal": "min_stations",
    "target_takt": 80000,
    "model": "boolean"
  },
  "stations": [
    {
      "id": "WS-001",
      "total_time_ms": 75234,
      "idle_time_ms": 4766,
      "workers": 1,
      "utilization_pct": 94.04,
      "assigned_tasks": [1, 2, 3, 5]
    },
    {
      "id": "WS-002",
      "total_time_ms": 80000,
      "idle_time_ms": 0,
      "workers": 1,
      "utilization_pct": 100.0,
      "assigned_tasks": [4, 6, 7]
    }
  ],
  "takt_time_ms": 80000,
  "bottleneck_station_id": "WS-002",
  "manpower_total": 2,
  "line_count": 2,
  "utilization_avg": 97.02,
  "total_idle_time_ms": 4766,
  "solve_time_sec": 1.234,
  "algorithm_used": "boolean"
}
```

See full API specification: [`docs/PHASE1_API_SPEC.md`](PHASE1_API_SPEC.md)

---

## Acceptance Testing

### Test Case 1: Basic Functionality Verification

**Objective:** Verify API responds correctly to optimization requests

```bash
# Test script
python3 << 'EOF'
import requests
import json

response = requests.post("http://localhost:8000/optimize", json={
    "work_order_id": "WO_A",
    "target_takt": 80000,
    "optimization_goal": "min_stations"
})

assert response.status_code == 200, f"API failed: {response.status_code}"
data = response.json()

# Acceptance criteria checks
assert data["solve_time_sec"] < 3.0, f"Solve time too long: {data['solve_time_sec']}s"
assert data["line_count"] > 0, "Station count abnormal"
assert 0 <= data["utilization_avg"] <= 100, "Utilization range abnormal"

print("✓ Test passed")
print(f"  Stations: {data['line_count']}")
print(f"  Manpower: {data['manpower_total']}")
print(f"  Solve time: {data['solve_time_sec']:.2f}s")
print(f"  Avg utilization: {data['utilization_avg']:.1f}%")
EOF
```

### Test Case 2: Performance Verification

**Acceptance Criteria (stage-specs.md):**
- API Latency < 3 seconds (data volume <= 500 actions)

```bash
# Stress test (100 consecutive requests)
python3 << 'EOF'
import requests
import time

times = []
for i in range(100):
    start = time.time()
    response = requests.post("http://localhost:8000/optimize", json={
        "work_order_id": "WO_A",
        "target_takt": 80000,
        "optimization_goal": "min_stations"
    })
    elapsed = time.time() - start
    times.append(elapsed)
    
    if response.status_code != 200:
        print(f"✗ Request {i+1} failed")

p50 = sorted(times)[50]
p95 = sorted(times)[95]
p99 = sorted(times)[99]

print(f"P50 Latency: {p50:.2f}s")
print(f"P95 Latency: {p95:.2f}s")
print(f"P99 Latency: {p99:.2f}s")

assert p95 < 3.0, f"P95 exceeds 3 seconds: {p95:.2f}s"
print("✓ Performance test passed")
EOF
```

---

## Troubleshooting

### Problem 1: API Startup Failure

**Symptom:** `ModuleNotFoundError: No module named 'fastapi'`

**Solution:**
```bash
pip install fastapi uvicorn ortools absl-py pydantic
```

### Problem 2: Algorithm Execution Failure

**Symptom:** API returns 500 error, logs show "Algorithm execution failed"

**Checklist:**
1. Do CSV files exist?
   ```bash
   ls data/test_tasks.csv
   ```

2. Test algorithm manually
   ```bash
   python3 src/sche-algo.py \
     --tasks_csv data/test_tasks.csv \
     --objective min_stations \
     --json_output /tmp/test.json
   ```

3. Check error messages
   ```bash
   tail -f /var/log/api_server.log
   ```

### Problem 3: Frontend Cannot Connect to API

**Symptom:** "Optimization failed" appears after clicking button

**Solution:**
1. Confirm API service is running
   ```bash
   curl http://localhost:8000/health
   ```

2. Check browser Console (F12) for error messages

3. Verify same-origin policy (CORS):
   - Frontend must be loaded from `http://localhost:8000`
   - Cannot use `file://` protocol

---

## Deployment Guide (Docker - Optional)

### Dockerfile

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy code
COPY src/ ./src/
COPY data/ ./data/

# Create output directory
RUN mkdir -p output

EXPOSE 8000

CMD ["python", "src/api_server.py"]
```

### Build and Run

```bash
# Build image
docker build -t line-balance-api:phase1 .

# Run container
docker run -d \
  --name line-balance \
  -p 8000:8000 \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/output:/app/output \
  line-balance-api:phase1

# View logs
docker logs -f line-balance

# Stop service
docker stop line-balance
```

---

## Phase 1.5 Core Features

### Feature Overview

Phase 1.5 extends Phase 1 MVP with four major capabilities:

1. **Offline Task Handling** (REQ #4, #15)
2. **Adjustable Task Merging** (REQ #13)
3. **Assembly Complexity Classification** (REQ #10)
4. **Part-Action Mapping & BOM Integration** (REQ #12) ⭐ **PRIORITY**

---

## Feature 4: Part-Action Mapping & BOM Integration (REQ #12)

### **Objective**
Establish the link between assembly actions (tasks) and BOM parts to enable:
- **Line-side inventory planning** (station-level BOM)
- **Material flow tracking** (part movement across stations)
- **MES/ERP integration** (backflush point configuration)
- **Work instruction generation** (part-action SOPs)

### **Implementation Steps**

#### **Step 1: Update CSV Schema**

Create extended tasks CSV file with `part_id`, `action_type`, and `complexity_level` columns:

```csv
task_id,duration,part_id,action_type,complexity_level,offline_flag,adjustable,predecessors
1,5000,"SCREW_M3","screw","simple",0,1,
2,8000,"GPU_GTX3080","install","complex",0,1,1
3,3000,"THERMAL_PAD","apply","medium",1,0,1
4,4000,"GPU_GTX3080","test","complex",0,1,2
5,6000,"CABLE_BUNDLE","route","medium",0,1,2
6,2000,"SCREW_M3","screw","simple",0,1,"4,5"
```

Save as `data/tasks_with_parts.csv`

**Column Definitions:**
- `part_id`: Part number from BOM (e.g., GPU_GTX3080, SCREW_M3)
- `action_type`: Action performed on the part (screw, glue, mount, test, etc.)
- `complexity_level`: Assembly complexity (simple/medium/complex/super_complex)

#### **Step 2: Modify Algorithm (`sche-algo.py`)**

Add part tracking data structures:

```python
from typing import Dict, List, Set
from dataclasses import dataclass

@dataclass
class PartInfo:
    """Information about a BOM part"""
    part_id: str
    tasks: List[int]  # Task IDs that work on this part
    actions: List[str]  # Actions performed on this part
    complexity: str  # Complexity level
    stations: Set[int] = None  # Stations where this part is processed (populated after solving)

def read_problem_with_parts(tasks_file, precedences_file, config_file):
    """
    Read CSV with part_id, action_type, and complexity_level columns.
    
    Returns:
        problem: Standard problem dict
        part_map: Dict[str, PartInfo] - Maps part_id to PartInfo
        task_parts: Dict[int, str] - Maps task_id to part_id
    """
    df_tasks = pd.read_csv(tasks_file)
    
    # Validate extended columns
    required_cols = ['task_id', 'duration', 'part_id', 'action_type', 'complexity_level']
    missing = set(required_cols) - set(df_tasks.columns)
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    
    # Build part mapping
    part_map = {}
    task_parts = {}
    
    for _, row in df_tasks.iterrows():
        task_id = int(row['task_id'])
        part_id = str(row['part_id'])
        action = str(row['action_type'])
        complexity = str(row['complexity_level'])
        
        # Update part_map
        if part_id not in part_map:
            part_map[part_id] = PartInfo(
                part_id=part_id,
                tasks=[],
                actions=[],
                complexity=complexity,
                stations=set()
            )
        
        part_map[part_id].tasks.append(task_id)
        if action not in part_map[part_id].actions:
            part_map[part_id].actions.append(action)
        
        # Update task_parts
        task_parts[task_id] = part_id
    
    # Read standard problem
    problem = read_problem_from_csv(tasks_file, precedences_file, config_file)
    
    return problem, part_map, task_parts

def generate_part_station_matrix(assignment, part_map, task_parts):
    """
    Generate part-station mapping after optimization.
    
    Args:
        assignment: Dict[int, int] - Maps task_id to station_index
        part_map: Dict[str, PartInfo]
        task_parts: Dict[int, str]
    
    Returns:
        part_flow_summary: Dict[str, List[int]] - Maps part_id to station indices
        station_parts: Dict[int, List[Dict]] - Maps station to parts_involved
    """
    # Update part_map with station assignments
    for task_id, station_idx in assignment.items():
        if task_id in task_parts:
            part_id = task_parts[task_id]
            if part_id in part_map:
                part_map[part_id].stations.add(station_idx)
    
    # Build part_flow_summary
    part_flow_summary = {
        part_id: sorted(list(info.stations))
        for part_id, info in part_map.items()
    }
    
    # Build station_parts (reverse mapping)
    station_parts = {}
    for part_id, info in part_map.items():
        for station_idx in info.stations:
            if station_idx not in station_parts:
                station_parts[station_idx] = []
            
            # Find tasks at this station for this part
            station_task_ids = [
                tid for tid in info.tasks
                if assignment.get(tid) == station_idx
            ]
            
            # Find actions performed at this station
            station_actions = []
            for tid in station_task_ids:
                # Get action from original CSV or use generic
                station_actions.extend(info.actions)  # Simplified for now
            
            station_parts[station_idx].append({
                "part_id": part_id,
                "actions": list(set(station_actions)),  # Deduplicate
                "task_ids": station_task_ids,
                "complexity": info.complexity
            })
    
    return part_flow_summary, station_parts
```

#### **Step 3: Update JSON Output**

```python
def build_response_with_parts(assignment, problem, part_map, task_parts, kpis):
    """
    Build JSON response with part tracking data.
    """
    part_flow_summary, station_parts = generate_part_station_matrix(
        assignment, part_map, task_parts
    )
    
    # Build station info with parts_involved
    stations = []
    num_stations = max(assignment.values()) + 1
    
    for station_idx in range(num_stations):
        station_tasks = [tid for tid, sidx in assignment.items() if sidx == station_idx]
        total_time = sum(problem['durations'][tid] for tid in station_tasks)
        
        # Get parts involved at this station
        parts_involved = station_parts.get(station_idx, [])
        
        # Build part_operations quick lookup
        part_operations = {
            p["part_id"]: p["actions"]
            for p in parts_involved
        }
        
        # Find max complexity at this station
        complexity_order = {"simple": 0, "medium": 1, "complex": 2, "super_complex": 3}
        complexity_max = "simple"
        for p in parts_involved:
            if complexity_order.get(p["complexity"], 0) > complexity_order[complexity_max]:
                complexity_max = p["complexity"]
        
        stations.append({
            "id": f"WS-{station_idx:03d}",
            "total_time_ms": total_time,
            "utilization_pct": round((total_time / kpis['takt_time_ms']) * 100, 1),
            "workers": 1,  # Simplified
            "assigned_tasks": station_tasks,
            
            # Phase 1.5 Part Tracking
            "parts_involved": parts_involved,
            "part_operations": part_operations,
            "complexity_max": complexity_max
        })
    
    # Calculate complexity distribution
    complexity_dist = {"simple": 0, "medium": 0, "complex": 0, "super_complex": 0}
    for part_info in part_map.values():
        complexity_dist[part_info.complexity] += len(part_info.tasks)
    
    return {
        "work_order_id": problem.get('work_order_id', 'WO_UNKNOWN'),
        "stations": stations,
        "takt_time_ms": kpis['takt_time_ms'],
        "line_count": num_stations,
        "manpower_total": num_stations,  # Simplified
        "utilization_avg": kpis.get('utilization_avg', 0),
        
        # Phase 1.5 Part Tracking
        "part_flow_summary": part_flow_summary,
        "part_count": len(part_map),
        "complexity_distribution": complexity_dist
    }
```

#### **Step 4: Generate Part-Station Matrix Export**

```python
def export_part_station_matrix(part_flow_summary, station_parts, output_file):
    """
    Export detailed part-station matrix for MES/ERP integration.
    """
    matrix_data = {
        "part_flow_summary": part_flow_summary,
        "stations": [
            {
                "station_index": station_idx,
                "parts_involved": parts
            }
            for station_idx, parts in sorted(station_parts.items())
        ],
        "metadata": {
            "total_parts": len(part_flow_summary),
            "total_stations": len(station_parts),
            "generated_at": datetime.now().isoformat()
        }
    }
    
    with open(output_file, 'w') as f:
        json.dump(matrix_data, f, indent=2)
    
    print(f"Part-station matrix exported to: {output_file}")
```

#### **Step 5: Update API Server (`api_server.py`)**

Add part tracking parameter:

```python
class OptimizeRequest(BaseModel):
    work_order_id: str
    optimization_goal: str
    target_takt: int
    max_workers_per_station: int = 3
    fixed_stations: int = 0
    
    # Phase 1.5 extensions
    enable_offline_handling: bool = False
    enable_task_merging: bool = False
    merge_efficiency_gain: float = 0.10
    enable_part_tracking: bool = False  # NEW
    export_part_matrix: bool = False    # NEW

@app.post("/optimize")
async def optimize(request: OptimizeRequest):
    # ... existing code ...
    
    # Add part tracking flag to algorithm command
    cmd = [
        "python3", algo_path,
        "--tasks_csv", tasks_csv,
        "--precedences_csv", precedences_csv,
        "--config_csv", config_csv,
        "--optimization_goal", request.optimization_goal,
        "--target_takt", str(request.target_takt),
        "--json_output", json_output
    ]
    
    if request.enable_part_tracking:
        cmd.append("--enable_part_tracking")
    
    if request.export_part_matrix:
        matrix_file = f"output/part_matrix_{request.work_order_id}.json"
        cmd.extend(["--part_station_matrix", matrix_file])
    
    # ... rest of code ...
```

#### **Step 6: Test Part Tracking**

```bash
# Test with part tracking enabled
python3 src/sche-algo.py \
  --tasks_csv data/tasks_with_parts.csv \
  --precedences_csv data/test_precedences.csv \
  --config_csv data/test_config.csv \
  --optimization_goal min_stations \
  --target_takt 30000 \
  --enable_part_tracking \
  --part_station_matrix output/part_matrix.json \
  --json_output output/result_with_parts.json

# Verify part_flow_summary in output
cat output/result_with_parts.json | jq '.part_flow_summary'

# Verify parts_involved per station
cat output/result_with_parts.json | jq '.stations[0].parts_involved'

# Check part-station matrix export
cat output/part_matrix.json | jq
```

**Expected Output:**
```json
{
  "work_order_id": "WO_A",
  "part_flow_summary": {
    "GPU_GTX3080": [0, 1],
    "SCREW_M3": [0, 2],
    "THERMAL_PAD": [0],
    "CABLE_BUNDLE": [1]
  },
  "part_count": 4,
  "complexity_distribution": {
    "simple": 2,
    "medium": 2,
    "complex": 2
  },
  "stations": [
    {
      "id": "WS-001",
      "parts_involved": [
        {
          "part_id": "SCREW_M3",
          "actions": ["screw"],
          "task_ids": [1],
          "complexity": "simple"
        },
        {
          "part_id": "GPU_GTX3080",
          "actions": ["install"],
          "task_ids": [2],
          "complexity": "complex"
        }
      ],
      "part_operations": {
        "SCREW_M3": ["screw"],
        "GPU_GTX3080": ["install"]
      },
      "complexity_max": "complex"
    }
  ]
}
```

#### **Verification Checklist**

- [ ] CSV schema includes `part_id`, `action_type`, `complexity_level` columns
- [ ] Algorithm reads and parses part data correctly
- [ ] `part_flow_summary` generated with correct station mappings
- [ ] `parts_involved` populated for each station
- [ ] `part_operations` quick lookup map is accurate
- [ ] `complexity_max` correctly identifies highest complexity per station
- [ ] `part_count` matches unique BOM items
- [ ] Part-station matrix export file generated
- [ ] API parameter `enable_part_tracking` functional
- [ ] Performance acceptable (< 5s for 50 tasks with parts)

---

## Phase 1.5 Extended Implementation Guide

Phase 1.5 adds support for offline task handling (REQ #4, #15) and adjustable task merging (REQ #13).

### Feature 1: Offline Task Handling

#### **Objective**
Separate online and offline tasks to accurately model production line workstation allocation and off-line operations.

#### **Implementation Steps**

**Step 1: Update CSV Schema**

Create extended tasks CSV file with `offline_flag` column:

```csv
task_id,duration,offline_flag,predecessors
1,5000,0,
2,3000,1,1
3,4000,0,1
4,2000,0,"2,3"
5,6000,1,4
```

Save as `data/tasks_with_offline.csv`

**Step 2: Modify Algorithm (`sche-algo.py`)**

Add offline task filtering logic:

```python
def read_problem_from_csv_extended(tasks_file, precedences_file, config_file):
    """Read CSV with extended offline_flag column"""
    problem = read_problem_from_csv(tasks_file, precedences_file, config_file)
    
    # Read offline_flag column
    df = pd.read_csv(tasks_file)
    offline_tasks = []
    
    for idx, row in df.iterrows():
        if 'offline_flag' in row and int(row.get('offline_flag', 0)) == 1:
            offline_tasks.append(int(row['task_id']))
    
    # Store offline tasks in problem dict
    problem["offline_tasks"] = SectionInfo()
    problem["offline_tasks"].value = offline_tasks
    
    return problem

def filter_online_tasks(problem):
    """Separate online and offline tasks"""
    all_tasks = list(problem["tasks"].index_map.keys())
    offline_tasks = problem.get("offline_tasks", SectionInfo()).value or []
    online_tasks = [t for t in all_tasks if t not in offline_tasks]
    
    return online_tasks, offline_tasks

def solve_with_offline_handling(problem, hint=None):
    """Solve optimization with offline task handling"""
    online_tasks, offline_tasks = filter_online_tasks(problem)
    
    # Create filtered problem with online tasks only
    problem_online = {
        "tasks": SectionInfo(),
        "precedences": problem["precedences"],
        "cycle_time": problem["cycle_time"],
        "num_workers_limit": problem["num_workers_limit"]
    }
    
    # Copy only online tasks
    problem_online["tasks"].index_map = {
        t: problem["tasks"].index_map[t] 
        for t in online_tasks
    }
    
    # Solve for online tasks
    assignment = solve_problem_with_boolean_model(problem_online, hint)
    
    # Assign offline tasks to special station (-1)
    for t in offline_tasks:
        assignment[t] = -1
    
    return assignment, online_tasks, offline_tasks
```

**Step 3: Update KPI Calculation**

```python
def compute_kpis_with_offline(assignment, durations, online_tasks, offline_tasks):
    """
    Compute KPIs with offline metrics.
    
    Args:
        assignment: Dict[int, int] - Maps task_id to station_index
        durations: Dict[int, int] - Task durations in ms
        online_tasks: List[int] - Online task IDs
        offline_tasks: List[int] - Offline task IDs
    
    Returns:
        extended_kpis: Dict with offline metrics
    """
    # Compute standard KPIs for online tasks only
    online_assignment = {tid: sid for tid, sid in assignment.items() if tid in online_tasks}
    standard_kpis = compute_standard_kpis(online_assignment, durations)
    
    # Add offline metrics
    offline_total_time = sum(durations[tid] for tid in offline_tasks)
    
    extended_kpis = {
        **standard_kpis,
        'online_stations': max(online_assignment.values()) + 1 if online_assignment else 0,
        'offline_tasks_count': len(offline_tasks),
        'offline_total_time_ms': offline_total_time
    }
    
    return extended_kpis
```

**Step 4: Update API Server (`api_server.py`)**

Add support for offline handling parameter:

```python
class OptimizeRequest(BaseModel):
    work_order_id: str
    optimization_goal: str
    target_takt: int
    max_workers_per_station: int = 3
    fixed_stations: int = 0
    
    # Phase 1.5 NEW fields
    enable_offline_handling: bool = False

@app.post("/optimize")
async def optimize(request: OptimizeRequest):
    # ... existing code ...
    
    # Add offline handling flag to algorithm command
    cmd = [
        "python3", algo_path,
        "--tasks_csv", tasks_csv,
        "--precedences_csv", precedences_csv,
        "--config_csv", config_csv,
        "--optimization_goal", request.optimization_goal,
        "--target_takt", str(request.target_takt),
        "--json_output", json_output
    ]
    
    if request.enable_offline_handling:
        cmd.append("--enable_offline_handling")
    
    # ... rest of code ...
```

**Step 5: Test**

```bash
# Test with offline handling
python3 src/sche-algo.py \
  --tasks_csv data/tasks_with_offline.csv \
  --precedences_csv data/test_precedences.csv \
  --config_csv data/test_config.csv \
  --optimization_goal min_stations \
  --target_takt 30000 \
  --enable_offline_handling \
  --json_output output/result_offline.json

# Verify output
cat output/result_offline.json
```

**Expected Output:**
```json
{
  "kpis": {
    "online_stations": 2,
    "offline_tasks_count": 3,
    "offline_total_time_ms": 15000,
    "line_count": 2,
    "takt_time_ms": 28500
  },
  "stations": [
    {
      "id": "WS-001",
      "online_tasks": [1, 3, 5],
      "offline_tasks": []
    },
    {
      "id": "OFFLINE-001",
      "online_tasks": [],
      "offline_tasks": [2, 4, 6]
    }
  ]
}
```

---

### Feature 2: Adjustable Task Merging

#### **Objective**
Enable merging of similar tasks at the same station to achieve efficiency gains and reduce total line time.

#### **Implementation Steps**

**Step 1: Update CSV Schema**

Create extended tasks CSV file with `adjustable` and `action_type` columns:

```csv
task_id,duration,adjustable,action_type,predecessors
1,5000,1,"screw",
2,3000,0,"glue",1
3,4000,1,"screw",1
4,2000,1,"clip","2,3"
5,6000,1,"screw",4
```

Save as `data/tasks_with_adjustable.csv`

**Column Definitions:**
- `adjustable`: 0=fixed (cannot merge), 1=adjustable (can merge)
- `action_type`: Type of action (screw, glue, clip, mount, test, etc.)

**Step 2: Modify Algorithm (`sche-algo.py`)**

Add merge candidate identification:

```python
def find_merge_candidates(tasks, assignment):
    """
    Identify tasks that can be merged at the same station.
    
    Args:
        tasks: List of task dictionaries with 'id', 'adjustable', 'action_type'
        assignment: Dict[int, int] - Maps task_id to station_index
    
    Returns:
        merge_candidates: Dict[int, List[Tuple[int, int]]] - station_id → [(task1, task2), ...]
    """
    merge_candidates = {}
    
    # Group tasks by station
    station_tasks = {}
    for task_id, station_id in assignment.items():
        if station_id not in station_tasks:
            station_tasks[station_id] = []
        station_tasks[station_id].append(task_id)
    
    # Find mergeable pairs at each station
    for station_id, task_ids in station_tasks.items():
        adjustable_tasks = [tid for tid in task_ids if tasks[tid]['adjustable'] == 1]
        
        # Group by action_type
        action_groups = {}
        for tid in adjustable_tasks:
            action = tasks[tid]['action_type']
            if action not in action_groups:
                action_groups[action] = []
            action_groups[action].append(tid)
        
        # Generate merge pairs
        merge_pairs = []
        for action, task_list in action_groups.items():
            if len(task_list) >= 2:
                # Pair consecutive tasks
                for i in range(0, len(task_list) - 1, 2):
                    merge_pairs.append((task_list[i], task_list[i+1]))
        
        if merge_pairs:
            merge_candidates[station_id] = merge_pairs
    
    return merge_candidates

def apply_merge_efficiency(duration1, duration2, efficiency_gain):
    """
    Calculate merged duration with efficiency gain.
    
    Args:
        duration1: Duration of first task (ms)
        duration2: Duration of second task (ms)
        efficiency_gain: Efficiency gain factor (0.0-0.5)
    
    Returns:
        merged_duration: Combined duration after efficiency gain
    """
    raw_total = duration1 + duration2
    time_saved = raw_total * efficiency_gain
    merged_duration = raw_total - time_saved
    return int(merged_duration)

def solve_with_task_merging(problem, merge_efficiency_gain=0.10):
    """
    Solve optimization with task merging enabled.
    
    Args:
        problem: Standard problem dict
        merge_efficiency_gain: Efficiency gain from merging (0.0-0.5)
    
    Returns:
        assignment: Task to station mapping
        merge_candidates: Identified merge opportunities
        time_saved: Total time saved from merging
    """
    # Step 1: Run standard optimization
    assignment = run_standard_solver(problem)
    
    # Step 2: Identify merge candidates
    merge_candidates = find_merge_candidates(problem['tasks'], assignment)
    
    # Step 3: Apply merging and recalculate durations
    merged_durations = problem['durations'].copy()
    total_time_saved = 0
    
    for station_id, merge_pairs in merge_candidates.items():
        for task1, task2 in merge_pairs:
            original_total = problem['durations'][task1] + problem['durations'][task2]
            merged_duration = apply_merge_efficiency(
                problem['durations'][task1],
                problem['durations'][task2],
                merge_efficiency_gain
            )
            time_saved = original_total - merged_duration
            total_time_saved += time_saved
            
            # Update merged duration (assign to first task, mark second as merged)
            merged_durations[task1] = merged_duration
            merged_durations[task2] = 0  # Merged into task1
    
    return assignment, merge_candidates, total_time_saved, merged_durations
```

**Step 3: Add CP-SAT Merge Constraints (Optional Advanced)**

For solver-level merging optimization:

```python
def add_merge_constraints_to_model(model, tasks, assignment_vars, merge_efficiency_gain):
    """
    Add merge decision variables and constraints to CP-SAT model.
    
    Args:
        model: CP-SAT model
        tasks: List of tasks with 'adjustable' and 'action_type'
        assignment_vars: Dict[(task_id, station_id)] → BoolVar
        merge_efficiency_gain: Efficiency gain factor
    
    Returns:
        merge_vars: Dict[(task1_id, task2_id)] → BoolVar
    """
    merge_vars = {}
    
    # Group adjustable tasks by action_type
    action_groups = {}
    for task in tasks:
        if task['adjustable'] == 1:
            action = task['action_type']
            if action not in action_groups:
                action_groups[action] = []
            action_groups[action].append(task['id'])
    
    # Create merge decision variables for each pair
    for action, task_ids in action_groups.items():
        for i in range(len(task_ids)):
            for j in range(i+1, len(task_ids)):
                task1, task2 = task_ids[i], task_ids[j]
                merge_var = model.NewBoolVar(f'merge_{task1}_{task2}')
                merge_vars[(task1, task2)] = merge_var
                
                # Constraint: Can only merge if both at same station
                for station_id in range(num_stations):
                    model.Add(
                        assignment_vars[(task1, station_id)] == assignment_vars[(task2, station_id)]
                    ).OnlyEnforceIf(merge_var)
    
    return merge_vars
```

**Step 4: Update JSON Output**

```python
def build_response_with_merging(assignment, merge_candidates, durations, merged_durations, time_saved):
    """
    Build JSON response with merge information.
    
    Returns:
        response: Dict with merge metrics
    """
    stations = []
    num_stations = max(assignment.values()) + 1
    
    for station_id in range(num_stations):
        station_tasks = [tid for tid, sid in assignment.items() if sid == station_id]
        
        # Identify which tasks are adjustable
        adjustable_tasks = [tid for tid in station_tasks if tasks[tid]['adjustable'] == 1]
        
        # Get merge pairs for this station
        merged_pairs = merge_candidates.get(station_id, [])
        
        # Calculate load with merged durations
        total_time = sum(merged_durations[tid] for tid in station_tasks)
        
        stations.append({
            'id': f'WS-{station_id:03d}',
            'total_time_ms': total_time,
            'assigned_tasks': station_tasks,
            'adjustable_tasks': adjustable_tasks,
            'merged_task_pairs': merged_pairs,
            'merge_time_saved_ms': sum(
                durations[t1] + durations[t2] - merged_durations[t1]
                for t1, t2 in merged_pairs
            )
        })
    
    return {
        'stations': stations,
        'merged_tasks_count': sum(len(pairs) * 2 for pairs in merge_candidates.values()),
        'total_time_saved_ms': time_saved,
        'merge_efficiency_gain_pct': merge_efficiency_gain * 100
    }
```

**Step 5: Update API Server (`api_server.py`)**

```python
class OptimizeRequest(BaseModel):
    work_order_id: str
    optimization_goal: str
    target_takt: int
    max_workers_per_station: int = 3
    fixed_stations: int = 0
    
    # Phase 1.5 NEW fields
    enable_offline_handling: bool = False
    enable_task_merging: bool = False
    merge_efficiency_gain: float = Field(default=0.10, ge=0.0, le=0.5)

@app.post("/optimize")
async def optimize(request: OptimizeRequest):
    # ... existing code ...
    
    cmd = [
        "python3", algo_path,
        "--tasks_csv", tasks_csv,
        "--precedences_csv", precedences_csv,
        "--config_csv", config_csv,
        "--optimization_goal", request.optimization_goal,
        "--target_takt", str(request.target_takt),
        "--json_output", json_output
    ]
    
    if request.enable_task_merging:
        cmd.extend([
            "--enable_task_merging",
            "--merge_efficiency_gain", str(request.merge_efficiency_gain)
        ])
    
    # ... rest of code ...
```

**Step 6: Test Task Merging**

```bash
# Test with task merging
python3 src/sche-algo.py \
  --tasks_csv data/tasks_with_adjustable.csv \
  --precedences_csv data/test_precedences.csv \
  --config_csv data/test_config.csv \
  --optimization_goal min_stations \
  --target_takt 30000 \
  --enable_task_merging \
  --merge_efficiency_gain 0.15 \
  --json_output output/result_merged.json

# Verify output
cat output/result_merged.json | jq '.merged_tasks_count'
cat output/result_merged.json | jq '.stations[0].merged_task_pairs'
```

**Expected Output:**
```json
{
  "stations": [
    {
      "id": "WS-001",
      "adjustable_tasks": [1, 3, 5],
      "merged_task_pairs": [[1, 3], [5, 7]],
      "merge_time_saved_ms": 1350
    }
  ],
  "merged_tasks_count": 4,
  "total_time_saved_ms": 2100,
  "merge_efficiency_gain_pct": 15.0
}
```

#### **Verification Checklist**

- [ ] CSV schema includes `adjustable` and `action_type` columns
- [ ] Algorithm identifies merge candidates correctly
- [ ] Merged tasks are at the same station
- [ ] Efficiency gain applied correctly
- [ ] `merged_task_pairs` populated in output
- [ ] `merge_time_saved_ms` calculated per station
- [ ] `total_time_saved_ms` matches sum of station savings
- [ ] API parameter `enable_task_merging` functional
- [ ] Performance acceptable (< 5s for 50 tasks)

---

### Feature 3: Assembly Complexity Classification

#### **Objective**
Classify tasks by assembly complexity and balance complexity distribution across stations for optimal operator skill assignment.

#### **Implementation Steps**

**Step 1: Update CSV Schema**

Create extended tasks CSV file with `complexity_level` column:

```csv
task_id,duration,complexity_level,part_id,action_type,predecessors
1,5000,"simple","SCREW_M3","screw",
2,3000,"medium","FAN_120MM","mount",1
3,8000,"complex","GPU_GTX3080","install",1
4,4000,"complex","GPU_GTX3080","test","2,3"
5,6000,"super_complex","CTO_CUSTOM","configure",4
```

Save as `data/tasks_with_complexity.csv`

**Column Definitions:**
- `complexity_level`: simple | medium | complex | super_complex

**Step 2: Implement Auto-Classification**

```python
def auto_classify_complexity(task):
    """
    Auto-classify task complexity based on part_id keywords.
    
    Args:
        task: Dict with 'part_id' and optionally 'complexity_level'
    
    Returns:
        complexity_level: str (simple/medium/complex/super_complex)
    """
    # If already classified, return existing
    if 'complexity_level' in task and task['complexity_level']:
        return task['complexity_level']
    
    part_id = task.get('part_id', '').lower()
    
    # Classification rules
    simple_keywords = ['screw', 'clip', 'bracket', 'foam', 'label', 'tape']
    medium_keywords = ['fan', 'cable', 'thermal', 'mount', 'tray', 'panel']
    complex_keywords = ['gpu', 'cpu', 'hdd', 'ssd', 'raid', 'nic', 'pcie', 'memory']
    super_complex_keywords = ['cto', 'custom', 'special', 'bto', 'configure']
    
    # Match keywords
    if any(kw in part_id for kw in super_complex_keywords):
        return 'super_complex'
    elif any(kw in part_id for kw in complex_keywords):
        return 'complex'
    elif any(kw in part_id for kw in medium_keywords):
        return 'medium'
    elif any(kw in part_id for kw in simple_keywords):
        return 'simple'
    else:
        return 'medium'  # Default

def get_complexity_weight(complexity_level):
    """
    Get numeric weight for complexity level.
    
    Returns:
        weight: int (1, 2, 4, or 8)
    """
    weights = {
        'simple': 1,
        'medium': 2,
        'complex': 4,
        'super_complex': 8
    }
    return weights.get(complexity_level, 2)
```

**Step 3: Add Complexity Balancing to CP-SAT Model**

```python
def add_complexity_constraints(model, tasks, assignment_vars, num_stations):
    """
    Add complexity balancing constraints to CP-SAT model.
    
    Args:
        model: CP-SAT model
        tasks: List of tasks with 'complexity_level'
        assignment_vars: Dict[(task_id, station_id)] → BoolVar
        num_stations: int
    
    Returns:
        complexity_vars: Dict[station_id] → IntVar (complexity score)
    """
    complexity_vars = {}
    
    for station_id in range(num_stations):
        # Calculate complexity score for this station
        complexity_score = model.NewIntVar(
            0, 
            sum(get_complexity_weight(t['complexity_level']) for t in tasks),
            f'complexity_score_{station_id}'
        )
        
        # Score = sum of weights of assigned tasks
        model.Add(
            complexity_score == sum(
                get_complexity_weight(tasks[tid]['complexity_level']) * 
                assignment_vars[(tid, station_id)]
                for tid in range(len(tasks))
            )
        )
        
        complexity_vars[station_id] = complexity_score
    
    # Add variance minimization
    max_complexity = model.NewIntVar(0, 100, 'max_complexity')
    min_complexity = model.NewIntVar(0, 100, 'min_complexity')
    variance = model.NewIntVar(0, 100, 'complexity_variance')
    
    model.AddMaxEquality(max_complexity, list(complexity_vars.values()))
    model.AddMinEquality(min_complexity, list(complexity_vars.values()))
    model.Add(variance == max_complexity - min_complexity)
    
    # Add to objective (lower weight than primary objective)
    return complexity_vars, variance
```

**Step 4: Update JSON Output**

```python
def build_response_with_complexity(assignment, tasks, complexity_scores):
    """
    Build JSON response with complexity information.
    
    Returns:
        response: Dict with complexity metrics
    """
    stations = []
    num_stations = max(assignment.values()) + 1
    
    # Calculate complexity distribution
    complexity_dist = {'simple': 0, 'medium': 0, 'complex': 0, 'super_complex': 0}
    
    for station_id in range(num_stations):
        station_tasks = [tid for tid, sid in assignment.items() if sid == station_id]
        
        # Find max complexity at this station
        complexities = [tasks[tid]['complexity_level'] for tid in station_tasks]
        complexity_order = {'simple': 0, 'medium': 1, 'complex': 2, 'super_complex': 3}
        complexity_max = max(complexities, key=lambda c: complexity_order[c]) if complexities else 'simple'
        
        # Update distribution
        for complexity in complexities:
            complexity_dist[complexity] += 1
        
        stations.append({
            'id': f'WS-{station_id:03d}',
            'assigned_tasks': station_tasks,
            'complexity_max': complexity_max,
            'complexity_score': complexity_scores[station_id]
        })
    
    return {
        'stations': stations,
        'complexity_distribution': complexity_dist,
        'complexity_variance': max(complexity_scores.values()) - min(complexity_scores.values()),
        'avg_complexity_score': sum(complexity_scores.values()) / len(complexity_scores)
    }
```

**Step 5: Update API Server**

```python
class OptimizeRequest(BaseModel):
    # ... existing fields ...
    enable_complexity_classification: bool = False

@app.post("/optimize")
async def optimize(request: OptimizeRequest):
    # ... existing code ...
    
    if request.enable_complexity_classification:
        cmd.append("--enable_complexity_classification")
    
    # ... rest of code ...
```

**Step 6: Test Complexity Classification**

```bash
# Test with complexity classification
python3 src/sche-algo.py \
  --tasks_csv data/tasks_with_complexity.csv \
  --precedences_csv data/test_precedences.csv \
  --config_csv data/test_config.csv \
  --optimization_goal min_stations \
  --target_takt 30000 \
  --enable_complexity_classification \
  --json_output output/result_complexity.json

# Verify output
cat output/result_complexity.json | jq '.complexity_distribution'
cat output/result_complexity.json | jq '.stations[] | {id, complexity_max, complexity_score}'
```

**Expected Output:**
```json
{
  "stations": [
    {
      "id": "WS-001",
      "complexity_max": "medium",
      "complexity_score": 4
    },
    {
      "id": "WS-002",
      "complexity_max": "complex",
      "complexity_score": 6
    }
  ],
  "complexity_distribution": {
    "simple": 3,
    "medium": 2,
    "complex": 2,
    "super_complex": 1
  },
  "complexity_variance": 2,
  "avg_complexity_score": 5.0
}
```

#### **Verification Checklist**

- [ ] CSV schema includes `complexity_level` column
- [ ] Auto-classification works for missing complexity_level
- [ ] Complexity weights applied correctly (1/2/4/8)
- [ ] `complexity_max` correctly identifies highest complexity per station
- [ ] `complexity_distribution` matches task count by level
- [ ] `complexity_variance` calculated correctly
- [ ] API parameter `enable_complexity_classification` functional
- [ ] Performance acceptable (< 5s for 50 tasks)

---

```python
def compute_kpis_with_offline(assignment, durations, online_tasks, offline_tasks):
    """Compute KPIs with offline metrics"""
    
    # Filter online assignments
    online_assignment = {t: s for t, s in assignment.items() if t in online_tasks}
    
    # Compute standard KPIs for online tasks
    online_kpis = compute_kpis(online_assignment, durations, ...)
    
    # Compute offline metrics
    offline_total_time = sum(durations.get(t, 0) for t in offline_tasks)
    offline_count = len(offline_tasks)
    
    # Merge results
    extended_kpis = {
        **online_kpis,
        "online_stations": online_kpis["total_stations"],
        "offline_tasks_count": offline_count,
        "offline_total_time": offline_total_time,
        "mixed_operation_mode": True
    }
    
    return extended_kpis
```

**Step 4: Update API Server (`api_server.py`)**

Add support for offline handling parameter:

```python
class OptimizeRequest(BaseModel):
    work_order_id: str
    optimization_goal: str
    target_takt: int
    max_workers_per_station: int = 3
    fixed_stations: int = 0
    
    # Phase 1.5 NEW
    enable_offline_handling: bool = False

@app.post("/optimize")
async def optimize(request: OptimizeRequest):
    # ... existing code ...
    
    # Add offline handling flag to command
    cmd = [
        "python3", algo_script,
        "--tasks_csv", tasks_csv,
        "--objective", request.optimization_goal,
        "--json_output", json_output
    ]
    
    if request.enable_offline_handling:
        cmd.extend(["--enable_offline_handling"])
    
    # ... rest of code ...
```

**Step 5: Test**

```bash
# Test with offline handling
python3 src/sche-algo.py \
  --tasks_csv data/tasks_with_offline.csv \
  --precedences_csv data/test_precedences.csv \
  --objective min_stations \
  --enable_offline_handling \
  --json_output output/result_offline.json

# Verify output
cat output/result_offline.json
```

**Expected Output:**
```json
{
  "kpis": {
    "total_stations": 2,
    "online_stations": 1,
    "offline_tasks_count": 2,
    "offline_total_time": 9000
  },
  "assignment": {
    "1": 0,
    "2": -1,
    "3": 0,
    "4": 1,
    "5": -1
  }
}
```

---

### Feature 2: Adjustable Task Merging

#### **Objective**
Enable flexible task merging for tasks marked as adjustable to improve load balancing and reduce idle time.

#### **Implementation Steps**

**Step 1: Update CSV Schema**

Create extended tasks CSV with `adjustable` and `action_type` columns:

```csv
task_id,duration,adjustable,action_type,predecessors
1,5000,1,"screw",
2,3000,0,"glue",1
3,4000,1,"screw",1
4,2000,1,"screw","2,3"
5,6000,0,"test",4
```

Save as `data/tasks_with_adjustable.csv`

**Step 2: Modify Algorithm**

Add task merging logic:

```python
def find_merge_candidates(problem):
    """Identify tasks that can be merged"""
    df = pd.read_csv(tasks_file)
    
    # Group by action_type
    adjustable = df[df['adjustable'] == 1]
    merge_groups = adjustable.groupby('action_type')['task_id'].apply(list).to_dict()
    
    # Create merge pairs (consecutive tasks of same type)
    merge_candidates = []
    for action_type, task_list in merge_groups.items():
        for i in range(len(task_list) - 1):
            merge_candidates.append((task_list[i], task_list[i+1]))
    
    return merge_candidates

def solve_with_task_merging(problem, merge_efficiency=0.10):
    """Solve with task merging enabled"""
    model = cp_model.CpModel()
    
    # ... standard variables ...
    
    # Create merge decision variables
    merge_candidates = find_merge_candidates(problem)
    merge_vars = {}
    for (t1, t2) in merge_candidates:
        merge_vars[(t1, t2)] = model.NewBoolVar(f'merge_{t1}_{t2}')
    
    # Effective duration variables
    durations = problem["tasks"].index_map
    effective_duration = {}
    
    for t in tasks:
        max_dur = max(durations.values())
        effective_duration[t] = model.NewIntVar(0, max_dur * 2, f'eff_dur_{t}')
    
    # Merge constraints
    for (t1, t2), merge_var in merge_vars.items():
        # If merged, both at same station
        for p in range(num_stations):
            model.Add(
                assign[t1, p] == assign[t2, p]
            ).OnlyEnforceIf(merge_var)
        
        # Effective duration when merged (with efficiency gain)
        merged_dur = int((durations[t1] + durations[t2]) * (1 - merge_efficiency))
        model.Add(
            effective_duration[t1] + effective_duration[t2] == merged_dur
        ).OnlyEnforceIf(merge_var)
        
        # Original duration when not merged
        model.Add(
            effective_duration[t1] == durations[t1]
        ).OnlyEnforceIf(merge_var.Not())
        model.Add(
            effective_duration[t2] == durations[t2]
        ).OnlyEnforceIf(merge_var.Not())
    
    # Update capacity constraints to use effective duration
    for p in range(num_stations):
        model.Add(
            sum(assign[t, p] * effective_duration[t] for t in tasks) 
            <= cycle_time
        )
    
    # Objective: minimize stations, maximize merges
    merge_count = sum(merge_vars.values())
    model.Minimize(num_stations_var * 1000 - merge_count)
    
    # ... solve and return ...
```

**Step 3: Test**

```bash
python3 src/sche-algo.py \
  --tasks_csv data/tasks_with_adjustable.csv \
  --objective min_stations \
  --enable_task_merging \
  --merge_efficiency_gain 0.10 \
  --json_output output/result_merged.json
```

**Expected Output:**
```json
{
  "kpis": {
    "total_stations": 2,
    "adjustable_tasks_count": 3,
    "merged_tasks_count": 1,
    "merge_efficiency_gain": 10.0
  },
  "assignment": {
    "1": 0,
    "2": 1,
    "3": 0,
    "4": 0
  },
  "merged_pairs": [[1, 3]]
}
```

---

### Combined Feature Test

Test both offline handling and task merging together:

```bash
python3 src/sche-algo.py \
  --tasks_csv data/tasks_full_extended.csv \
  --objective min_stations \
  --enable_offline_handling \
  --enable_task_merging \
  --merge_efficiency_gain 0.10 \
  --json_output output/result_full.json
```

**Input CSV (Full Extended):**
```csv
task_id,duration,offline_flag,adjustable,action_type,predecessors
1,5000,0,1,"screw",
2,3000,1,0,"glue",1
3,4000,0,1,"screw",1
4,2000,0,0,"test","2,3"
5,6000,1,1,"clip",4
6,3000,0,1,"screw",4
```

---

### Verification Checklist

Phase 1.5 feature verification:

- [ ] **Offline Task Handling**
  - [ ] Tasks with `offline_flag=1` excluded from optimization
  - [ ] Offline tasks assigned to station index `-1`
  - [ ] KPIs include `offline_tasks_count` and `offline_total_time`
  - [ ] Precedence constraints handle online-offline relationships

- [ ] **Task Merging**
  - [ ] Adjustable tasks with same `action_type` can merge
  - [ ] Merged tasks assigned to same station
  - [ ] Effective duration calculated with efficiency gain
  - [ ] KPIs include `merged_tasks_count` and `merge_efficiency_gain`

- [ ] **API Integration**
  - [ ] `enable_offline_handling` parameter works
  - [ ] `enable_task_merging` parameter works
  - [ ] Extended StationInfo fields populated correctly
  - [ ] Response includes Phase 1.5 KPIs

- [ ] **Performance**
  - [ ] Solving time < 5 seconds for 50 tasks with extensions
  - [ ] Memory usage acceptable (< 500MB)

- [ ] **Extended Features (REQ #10, #12)**
  - [ ] `complexity_level` column parsed correctly
  - [ ] `part_id` column links actions to parts
  - [ ] Complexity classification impacts optimization (if enabled)
  - [ ] Part-level reporting available in output

---

## Phase 1.5 Extended Features Implementation

### Feature 3: Assembly Complexity Classification (REQ #10)

**Purpose:** Auto-classify tasks by complexity level for better resource allocation

**Implementation Steps:**

1. **Update CSV Schema**
   ```csv
   task_id,duration,action_type,complexity_level,part_id,predecessors
   1,5000,"mount","simple","FAN_BRACKET",
   2,8000,"install","complex","GPU_GTX3080",1
   3,3000,"screw","simple","SCREW_M3",2
   ```

2. **Add Complexity Lookup Table**
   ```python
   # In sche-algo.py or new module
   COMPLEXITY_RULES = {
       "simple": ["screw", "clip", "bracket"],
       "medium": ["mount", "cable", "thermal"],
       "complex": ["gpu", "hdd", "raid"],
       "super_complex": ["custom", "cto", "special"]
   }
   
   def auto_classify_complexity(part_id: str, action_type: str) -> str:
       """Auto-classify based on part keywords"""
       part_lower = part_id.lower()
       
       # Check part-based rules
       for complexity, keywords in COMPLEXITY_RULES.items():
           if any(kw in part_lower for kw in keywords):
               return complexity
       
       # Fallback to action-based
       if action_type in ["screw", "clip"]:
           return "simple"
       elif action_type in ["glue", "mount"]:
           return "medium"
       else:
           return "complex"
   ```

3. **Integrate into Optimization**
   ```python
   def read_problem_with_complexity(csv_path):
       df = pd.read_csv(csv_path)
       
       # Auto-fill missing complexity
       if 'complexity_level' not in df.columns:
           df['complexity_level'] = df.apply(
               lambda row: auto_classify_complexity(
                   row.get('part_id', ''),
                   row.get('action_type', '')
               ),
               axis=1
           )
       
       # Adjust durations based on complexity (optional)
       complexity_multipliers = {
           "simple": 1.0,
           "medium": 1.2,
           "complex": 1.5,
           "super_complex": 2.0
       }
       
       df['adjusted_duration'] = df.apply(
           lambda row: int(row['duration'] * 
                         complexity_multipliers.get(row['complexity_level'], 1.0)),
           axis=1
       )
       
       return df
   ```

4. **Add Complexity-Aware KPIs**
   ```python
   def compute_complexity_kpis(solution, task_data):
       complexity_distribution = task_data.groupby('complexity_level').agg({
           'task_id': 'count',
           'duration': 'sum'
       }).to_dict()
       
       return {
           "complexity_distribution": complexity_distribution,
           "avg_complexity_per_station": calculate_station_complexity(solution),
           "high_complexity_stations": identify_bottleneck_stations(solution)
       }
   ```

**Output Example:**
```json
{
  "complexity_distribution": {
    "simple": {"count": 8, "total_time": 12000},
    "medium": {"count": 5, "total_time": 18000},
    "complex": {"count": 3, "total_time": 24000}
  }
}
```

---

### Feature 4: Part-Action Mapping (REQ #12)

**Purpose:** Link action units to physical parts for BOM integration

**Implementation Steps:**

1. **Update Data Model**
   ```python
   @dataclass
   class TaskWithPart:
       task_id: int
       duration: int
       action_type: str
       part_id: Optional[str] = None  # New field
       part_quantity: int = 1         # New field
       offline_flag: int = 0
       adjustable: int = 1
       predecessors: List[int] = field(default_factory=list)
   ```

2. **Add Part-Level Grouping**
   ```python
   def group_tasks_by_part(tasks: List[TaskWithPart]) -> Dict[str, List[int]]:
       """Group task IDs by part_id"""
       part_map = defaultdict(list)
       
       for task in tasks:
           if task.part_id:
               part_map[task.part_id].append(task.task_id)
       
       return dict(part_map)
   ```

3. **Generate Part-Station Matrix**
   ```python
   def generate_part_station_matrix(solution, tasks):
       """Create matrix showing which parts are worked on at each station"""
       part_station = defaultdict(set)
       
       for station_id, task_ids in solution.items():
           for task_id in task_ids:
               task = tasks[task_id]
               if task.part_id:
                   part_station[task.part_id].add(station_id)
       
       return {
           part: sorted(stations) 
           for part, stations in part_station.items()
       }
   ```

4. **Add to Station Output**
   ```python
   # Extended station.csv format
   station_index,assigned_tasks,parts_involved,part_operations
   0,"1,2,3","GPU_GTX3080,FAN_BRACKET","GPU_GTX3080:install,FAN_BRACKET:mount+screw"
   1,"4,5","HDD_2TB,CABLE_SATA","HDD_2TB:install,CABLE_SATA:route"
   ```

**API Response Extension:**
```json
{
  "stations": [
    {
      "station_index": 0,
      "assigned_tasks": [1, 2, 3],
      "parts_involved": [
        {"part_id": "GPU_GTX3080", "actions": ["install", "test"]},
        {"part_id": "FAN_BRACKET", "actions": ["mount", "screw"]}
      ]
    }
  ],
  "part_flow_summary": {
    "GPU_GTX3080": [0, 1],  // Stations where this part is worked on
    "HDD_2TB": [1, 2]
  }
}
```

---

## Next Steps (Phase 2 Preview)

After Phase 1.5 completion, the next phase will include:

- ✅ Multi-line configuration (requirements 5, 6)
- ✅ 2D Layout drag-and-drop (requirements 18, 20, 21)
- ✅ Version management and sharing (requirements 25, 27)
- ✅ Assembly sequence data (requirements 11, 12)

See `docs/stage-specs.md` Phase 2 specifications for details.

---

## References

- [FastAPI Official Documentation](https://fastapi.tiangolo.com/)
- [Google OR-Tools CP-SAT](https://developers.google.com/optimization/cp/cp_solver)
- [Chart.js Documentation](https://www.chartjs.org/)
- [Tailwind CSS](https://tailwindcss.com/)

---

**Document Maintainer:** JASON YY, LIN  
**Last Updated:** 2025-11-07  
**Version:** 1.1.0-phase1.5

