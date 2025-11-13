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

