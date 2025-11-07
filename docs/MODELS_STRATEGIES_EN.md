# Models & Strategies Explanation

## 📚 Table of Contents
- [Data Structures](#data-structures)
- [Strategy Overview](#strategy-overview)
- [Detailed Model Explanations](#detailed-model-explanations)
- [Multi-Objective Optimization](#multi-objective-optimization)
- [KPI Calculation](#kpi-calculation)
- [CSV Output Formats](#csv-output-formats)
- [Usage Examples](#usage-examples)

---

## 🗂️ Data Structures

### **SectionInfo Class**
```python
class SectionInfo:
    def __init__(self):
        self.value = None              # Single numeric value (e.g., cycle_time, num_tasks)
        self.index_map = {}            # Dictionary mapping (e.g., task_id -> duration)
        self.set_of_pairs = set()      # Set of pairs (e.g., precedence relations)
```

**Purpose**: Unified storage for different types of problem data
- `value`: Stores cycle time, number of tasks, etc.
- `index_map`: Stores task durations as `{task_id: duration}`
- `set_of_pairs`: Stores precedence relations as `{(before_task, after_task)}`

---

## 🎯 Strategy Overview

| Strategy Name        | Algorithm                      | Objective Function          | Uses OR-Tools? | Main Purpose                             |
| -------------------- | ------------------------------ | --------------------------- | -------------- | ---------------------------------------- |
| **Greedy**           | Greedy Heuristic               | Fast Feasible Solution      | ❌              | Initial Solution + Hint                  |
| **Boolean Model**    | CP-SAT (Boolean Variables)     | Minimize Stations           | ✅              | Station Count Optimization               |
| **Scheduling Model** | CP-SAT (Cumulative Constraint) | Minimize Last Station Index | ✅              | Station Count Optimization (Alternative) |
| **Manpower Model**   | CP-SAT (Integer Variables)     | Minimize Total Workers      | ✅              | Workforce Optimization                   |
| **Idle Model**       | CP-SAT (Load Balancing)        | Minimize Bottleneck Load    | ✅              | Load Balancing                           |
| **Multi-Objective**  | Two-Phase Optimization         | Compound Objectives         | ✅              | Multi-Goal Optimization                  |

---

## 📖 Detailed Model Explanations

### 1️⃣ **Greedy Model (Greedy Heuristic)**

#### **Function**: `solve_problem_greedily()`

#### **Algorithm Logic**:
```python
1. Initialize candidate task set (tasks with no predecessors)
2. Current station capacity = cycle_time
3. While there are unassigned tasks:
   a. From candidates, select:
      - Task that fits in current station (duration ≤ remaining capacity)
      - Task that leaves minimum slack (most compact)
   b. If no task fits → open new station
   c. Assign task, update remaining capacity
   d. Update candidate set (tasks whose predecessors are satisfied)
```

#### **Key Data Structures**:
```python
weights = defaultdict(int)       # Number of predecessors for each task
successors = defaultdict(list)   # List of successor tasks for each task
candidates = set()                # Assignable candidate tasks
```

#### **Advantages**:
- ✅ Extremely fast (typically < 1 second)
- ✅ Guarantees feasible solution
- ✅ Serves as warm start hint for other models

#### **Disadvantages**:
- ❌ Non-optimal solution
- ❌ Sensitive to task ordering

---

### 2️⃣ **Boolean Model (Boolean Variable Model)**

#### **Function**: `solve_problem_with_boolean_model()`

#### **Decision Variables**:
```python
assign[t, p]   : BoolVar  # Whether task t is assigned to station p
possible[t, p] : BoolVar  # Whether task t can be assigned to station p (auxiliary)
active[p]      : BoolVar  # Whether station p is active
```

#### **Constraints**:

**1. Unique Assignment Constraint**:
```python
∀t: Σ(assign[t, p] for p) = 1  # Each task assigned to exactly one station
```

**2. Capacity Constraint**:
```python
∀p: Σ(assign[t, p] × duration[t] for t) ≤ cycle_time
```

**3. Precedence Constraint**:
```python
# If before is at station p, then after cannot be at station p-1 or earlier
∀(before, after) ∈ precedences:
  ∀p ∈ [1, num_pods):
    assign[before, p] → ¬possible[after, p-1]
```

**4. Possible Variable Propagation**:
```python
# If task is possible at p, then also possible at p+1 (monotonicity)
∀t, ∀p < num_pods-1:
  possible[t, p] → possible[t, p+1]
```

**5. Active and Assign Linkage**:
```python
∀p:
  (∃t: assign[t, p]) ↔ active[p]  # Station active iff has tasks
```

**6. Contiguity Constraint** (Key Optimization):
```python
∀p > 0:
  ¬active[p-1] → ¬active[p]  # Stations must be used contiguously
```

#### **Objective Function**:
```python
minimize Σ(active[p])  # Minimize number of active stations
```

#### **Hint (Search Starting Point)**:
```python
for t in all_tasks:
    model.add_hint(assign[t, greedy_solution[t]], 1)
```
Uses greedy solution as search starting point to accelerate solving.

#### **Advantages**:
- ✅ Guarantees optimal solution (within time limit)
- ✅ Powerful constraint propagation
- ✅ Contiguity constraint improves lower bound

#### **Disadvantages**:
- ⚠️ May timeout on large-scale problems
- ⚠️ Variable count O(tasks × stations)

---

### 3️⃣ **Scheduling Model (Scheduling Model)**

#### **Function**: `solve_problem_with_scheduling_model()`

#### **Core Concept**:
Transforms assembly line problem into **resource-constrained scheduling problem**:
- **Time axis** = Station index (0, 1, 2, ...)
- **Task** = Fixed-duration interval (duration = 1 station)
- **Resource** = Capacity per station (cycle_time)

#### **Decision Variables**:
```python
pods[t]       : IntVar[0, num_pods-1]  # Station index where task t is located
intervals[t]  : IntervalVar            # Fixed-duration interval (start=pods[t], size=1)
```

#### **Constraints**:

**1. Cumulative Constraint**:
```python
model.add_cumulative(
    intervals,  # All task intervals
    demands,    # Demand for each task (duration)
    cycle_time  # Capacity limit
)
```
This ensures: **At any station p, total duration of all tasks assigned to that station ≤ cycle_time**

**2. Precedence Constraint**:
```python
∀(before, after) ∈ precedences:
  pods[after] ≥ pods[before]  # after must be at or after before
```

**3. Terminating Interval (Objective Trick)**:
```python
obj_interval = new_interval_var(
    start = obj_var,        # Variable to minimize
    size = obj_size,
    end = num_pods + 1
)
# This interval has demand = cycle_time, forcing it to start as early as possible
```

#### **Objective Function**:
```python
minimize obj_var  # Minimize last used station index
```

#### **Advantages**:
- ✅ Natural modeling (suitable for scheduling problems)
- ✅ Leverages OR-Tools powerful Cumulative propagator
- ✅ Fewer variables O(tasks)

#### **Disadvantages**:
- ⚠️ May be slower than Boolean Model (depends on problem)
- ⚠️ Does not guarantee compact solution (may have empty stations)

---

### 4️⃣ **Manpower Model (Workforce Minimization Model)**

#### **Function**: `solve_problem_with_manpower_model()`

#### **Application Scenario**:
Given target takt time (target_takt), find minimum required workforce.

#### **Decision Variables**:
```python
assign[t, p]    : BoolVar              # Whether task t is assigned to station p
workers[p]      : IntVar[0, max_workers]  # Number of workers at station p
station_of[t]   : IntVar[0, num_pods-1]   # Station where task t is located (linearization)
```

#### **Constraints**:

**1. Unique Assignment**:
```python
∀t: Σ(assign[t, p] for p) = 1
```

**2. Capacity Constraint** (Core):
```python
∀p: Σ(assign[t, p] × duration[t] for t) ≤ workers[p] × target_takt
```
**Interpretation**: Total workload at each station ≤ number of workers × takt time
- 1 worker → capacity = 1 × takt
- 2 workers → capacity = 2 × takt (parallel work)

**3. Linearization Constraint**:
```python
∀t: Σ(assign[t, p] × p for p) = station_of[t]
```
Converts boolean variables to integer variables for easier precedence expression.

**4. Precedence Constraint**:
```python
∀(before, after) ∈ precedences:
  station_of[after] ≥ station_of[before]
```

**5. Empty Station Constraint**:
```python
∀p: Σ(assign[t, p] for t) ≤ workers[p] × num_tasks
```
If workers[p] = 0, no tasks can be assigned.

#### **Objective Function**:
```python
minimize Σ(workers[p])  # Minimize total workforce
```

#### **Parameters**:
- `--target_takt`: Must be specified (e.g., 300 seconds)
- `--max_workers_per_station`: Worker limit per station (default 8)

#### **Example**:
```bash
python or-line-balance.py \
  --input data/test_tasks.csv \
  --objective min_manpower \
  --target_takt 300 \
  --max_workers_per_station 5
```

#### **Advantages**:
- ✅ Directly optimizes workforce cost
- ✅ Considers multi-worker parallel operations
- ✅ Suitable for labor-intensive production lines

#### **Disadvantages**:
- ⚠️ Requires accurate target_takt
- ⚠️ Longer solving time (multi-objective characteristics)

---

### 5️⃣ **Idle Time Model (Idle Time Minimization)**

#### **Function**: `solve_problem_with_idle_model()`

#### **Application Scenario**:
Fixed number of stations, find most balanced load distribution (minimize bottleneck).

#### **Decision Variables**:
```python
assign[t, p]    : BoolVar
loads[p]        : IntVar[0, cycle_time]  # Total load at station p
station_of[t]   : IntVar[0, num_pods-1]
max_load        : IntVar[0, cycle_time]  # Bottleneck station load
```

#### **Constraints**:

**1. Load Definition**:
```python
∀p: loads[p] = Σ(assign[t, p] × duration[t] for t)
```

**2. Bottleneck Definition**:
```python
∀p: max_load ≥ loads[p]
```

**3. Other Constraints** (same as Manpower Model):
- Unique assignment
- Precedence relations
- Capacity limit (≤ cycle_time)

#### **Objective Function**:
```python
minimize max_load  # Minimize bottleneck load
```

**Equivalent to**:
```
minimize Σ(idle[p])  where idle[p] = max_load - loads[p]
```

#### **Fixed Station Count Source**:
1. `--fixed_stations N`: Manually specified
2. Auto mode (`fixed_stations=0`): Uses greedy hint's station count

#### **Examples**:
```bash
# Auto-use greedy station count
python or-line-balance.py \
  --input data/test_tasks.csv \
  --objective min_idle

# Fixed 5 stations
python or-line-balance.py \
  --input data/test_tasks.csv \
  --objective min_idle \
  --fixed_stations 5
```

#### **Advantages**:
- ✅ Improves load balancing
- ✅ Reduces bottleneck station pressure
- ✅ Suitable for fixed station count scenarios

#### **Disadvantages**:
- ⚠️ Need to know reasonable station count first
- ⚠️ Does not reduce station count (only optimizes distribution)

---

## 🎯 Multi-Objective Optimization

### **Two-Phase Optimization Strategy**

#### **Mode 1: `stations_then_idle`**
```python
--multi_objective stations_then_idle
```

**Process**:
```
Phase 1: Boolean Model
  ↓ (Minimize station count)
Obtain N-station solution
  ↓
Phase 2: Idle Model (Fixed N stations)
  ↓ (Minimize bottleneck load)
Final solution: Minimum stations + Most balanced load
```

**Use Case**: Prioritize reducing stations, then balance load

---

#### **Mode 2: `manpower_then_idle`**
```python
--multi_objective manpower_then_idle \
  --target_takt 300
```

**Process**:
```
Phase 1: Manpower Model
  ↓ (Minimize total workforce)
Obtain M workers, N stations solution
  ↓
Phase 2: Idle Model (Fixed N stations)
  ↓ (Minimize bottleneck load, maintain workforce)
Final solution: Minimum workforce + Most balanced load
```

**Use Case**: Prioritize reducing workforce, then balance load

---

### **Implementation Details**:
```python
if _MULTI_OBJECTIVE.value == "stations_then_idle":
    # Phase 1
    assignment = solve_problem_with_boolean_model(problem, greedy_solution)
    num_stations = len(set(assignment.values()))
    
    # Phase 2
    assignment = solve_problem_with_idle_model(
        problem, assignment, fixed_stations=num_stations
    )
```

---

## 📊 KPI Calculation

### **Function**: `compute_kpis()`

#### **Calculated Metrics**:

**1. Load Analysis**:
```python
loads = defaultdict(int)
for task, station in assignment.items():
    loads[station] += durations[task]

bottleneck_load = max(loads.values())
bottleneck_station = argmax(loads)
```

**2. Utilization Calculation**:
```python
utilization[p] = (loads[p] / (workers[p] × takt)) × 100%
```
- `workers[p]`: Number of workers at station
- `takt`: Reference takt time (target_takt or cycle_time)

**3. Idle Time**:
```python
idle_vs_bottleneck[p] = bottleneck_load - loads[p]
total_idle = Σ(idle_vs_bottleneck[p])
```

**4. Average Utilization**:
```python
avg_utilization = mean(utilization[p] for all p)
```

#### **Output KPI Structure**:
```python
{
    "stations": [
        {
            "station_index": 0,
            "load": 850,
            "idle_vs_bottleneck": 0,  # Bottleneck station
            "workers": 2,
            "utilization_pct": 94.4
        },
        {
            "station_index": 1,
            "load": 720,
            "idle_vs_bottleneck": 130,
            "workers": 1,
            "utilization_pct": 80.0
        }
    ],
    "bottleneck_station": 0,
    "bottleneck_load": 850,
    "calculated_takt": 850,
    "target_takt": 900,
    "cycle_time": 1000,
    "manpower_total": 3,
    "avg_utilization_pct": 87.2,
    "total_idle_time": 130
}
```

---

## 📝 CSV Output Formats

### **1. solution.csv**
```python
write_solution_csv(filename, assignment, durations, workers)
```

**Fields**:
```csv
task_id,station_index,workers_assigned,task_duration,cumulative_load
1,0,2,274,274
2,0,2,223,497
3,1,1,186,186
```

---

### **2. kpi.csv**
```python
write_kpi_csv(filename, kpis, solve_time)
```

**Fields**:
```csv
metric,value,unit
total_stations,3,stations
total_workers,5,persons
bottleneck_load,850,time_units
avg_utilization,87.2,percent
solve_time,2.345,seconds
```

---

### **3. station.csv**
```python
write_station_csv(filename, kpis, assignment)
```

**Fields**:
```csv
station_index,total_load,idle_vs_bottleneck,workers,utilization_pct,assigned_tasks
0,850,0,2,94.4,"1,2,3"
1,720,130,1,80.0,"4,5"
```

---

## 🚀 Usage Examples

### **Basic Usage**:
```bash
# Minimize stations (Boolean Model)
python or-line-balance.py \
  --input data/test_tasks.csv \
  --objective min_stations \
  --model boolean \
  --csv_output output/solution.csv \
  --kpi_csv output/kpi.csv

# Minimize workforce
python or-line-balance.py \
  --input data/test_tasks.csv \
  --objective min_manpower \
  --target_takt 300 \
  --max_workers_per_station 5

# Multi-objective optimization
python or-line-balance.py \
  --input data/test_tasks.csv \
  --multi_objective stations_then_idle \
  --json_output output/result.json
```

---

## 🎓 Summary

### **Model Selection Guide**:

| Requirement         | Recommended Model | Parameters                                 |
| ------------------- | ----------------- | ------------------------------------------ |
| Minimum stations    | Boolean Model     | `--objective min_stations --model boolean` |
| Minimum workforce   | Manpower Model    | `--objective min_manpower --target_takt N` |
| Load balancing      | Idle Model        | `--objective min_idle`                     |
| Compound objectives | Multi-Objective   | `--multi_objective stations_then_idle`     |
| Quick testing       | Greedy            | `--model greedy`                           |

### **Solving Time Comparison** (Empirical values):

| Model      | 12 Tasks | 50 Tasks | 100 Tasks |
| ---------- | -------- | -------- | --------- |
| Greedy     | < 0.1s   | < 0.5s   | < 1s      |
| Boolean    | 1-5s     | 10-60s   | 60-300s   |
| Scheduling | 1-3s     | 5-30s    | 30-180s   |
| Manpower   | 2-10s    | 20-120s  | 120-600s  |
| Idle       | 1-5s     | 10-60s   | 60-300s   |

**Note**: Actual time depends on problem complexity (number of precedence relations, cycle_time tightness, etc.).

---

## 🔧 Phase 1.5 Extended Models

Phase 1.5 introduces support for REQ #4, #13, and #15 to handle offline tasks and adjustable task optimization.

---

### 6️⃣ **Offline-Aware Model**

#### **Purpose**
Separate online and offline tasks during optimization to accurately model production line workstation allocation.

#### **Application Scenario**
- **REQ #4**: Simulate workstation configuration with offline processing distinction
- **REQ #15**: Mark and handle offline tasks (quality inspection, pre-assembly)
- **Use case**: When tasks have different processing locations (on-line vs. off-line)

#### **Input Extensions**

**tasks.csv** must include `offline_flag` column:
```csv
task_id,duration,offline_flag,predecessors
1,5,0,
2,3,1,1
3,4,0,1
```

#### **Algorithm Modifications**

**1. Task Filtering**:
```python
def filter_offline_tasks(tasks, offline_flags):
    """Separate online and offline tasks"""
    online_tasks = [t for t in tasks if offline_flags.get(t, 0) == 0]
    offline_tasks = [t for t in tasks if offline_flags.get(t, 0) == 1]
    return online_tasks, offline_tasks
```

**2. Precedence Constraint Handling**:
```python
# Only apply precedence constraints for online-to-online relationships
for (before, after) in precedences:
    if before in online_tasks and after in online_tasks:
        # Standard precedence constraint
        for p in range(num_stations):
            model.Add(
                station[after] >= station[before]
            ).OnlyEnforceIf(assign[before, p], assign[after, p])
    elif before in offline_tasks and after in online_tasks:
        # Offline-to-online: assume offline task always completed first
        pass
    elif before in online_tasks and after in offline_tasks:
        # Online-to-offline: offline task scheduled after optimization
        pass
```

**3. Capacity Constraint (Online Tasks Only)**:
```python
for p in range(num_stations):
    model.Add(
        sum(assign[t, p] * duration[t] for t in online_tasks) <= cycle_time
    )
```

**4. Offline Task Post-Processing**:
```python
def assign_offline_tasks(offline_tasks, durations):
    """Assign offline tasks to dedicated offline stations"""
    offline_assignment = {}
    for t in offline_tasks:
        offline_assignment[t] = -1  # Special marker for offline
    return offline_assignment
```

#### **Extended KPI Calculation**

```python
def compute_kpis_with_offline(assignment, durations, offline_tasks):
    """Compute KPIs with offline task metrics"""
    
    # Standard KPIs for online tasks
    online_assignment = {t: s for t, s in assignment.items() if t not in offline_tasks}
    online_kpis = compute_kpis(online_assignment, durations, ...)
    
    # Offline metrics
    offline_total_time = sum(durations[t] for t in offline_tasks)
    offline_count = len(offline_tasks)
    
    return {
        **online_kpis,
        "online_stations": online_kpis["total_stations"],
        "offline_tasks_count": offline_count,
        "offline_total_time": offline_total_time,
        "mixed_operation_mode": True
    }
```

#### **Output Format**

**station.csv (Extended)**:
```csv
station_index,total_load,online_tasks,offline_tasks,online_load,offline_load,workers
0,8,"1,3","2",5,3,2
-1,12,"","4,5,6",0,12,0
```
- Station index `-1` represents offline station(s)
- `online_load` + `offline_load` = `total_load`

#### **Usage Example**

```bash
python sche-algo.py \
  --tasks_csv data/tasks_with_offline.csv \
  --objective min_stations \
  --enable_offline_handling \
  --station_csv output/stations_offline.csv \
  --kpi_csv output/kpi_offline.csv
```

**Expected Output (kpi.csv)**:
```csv
metric,value,unit
total_stations,3,stations
online_stations,2,stations
offline_tasks_count,3,tasks
offline_total_time,12,time_units
mixed_operation_mode,True,
```

---

### 7️⃣ **Adjustable Task Model**

#### **Purpose**
Enable flexible task merging and splitting for tasks marked as adjustable to improve load balancing.

#### **Application Scenario**
- **REQ #13**: Leverage action unit adjustability for optimization
- **Use case**: Tasks of the same type (e.g., multiple screw operations) can be merged
- **Benefit**: Reduce idle time and improve station utilization

#### **Input Extensions**

**tasks.csv** must include `adjustable` and `action_type` columns:
```csv
task_id,duration,adjustable,action_type,predecessors
1,5,1,"screw",
2,3,0,"glue",1
3,4,1,"screw",1
4,2,1,"screw","2,3"
```

#### **Algorithm Modifications**

**1. Identify Merge Candidates**:
```python
def find_merge_candidates(tasks, adjustable_flags, action_types):
    """Find tasks that can be merged"""
    adjustable_tasks = [t for t in tasks if adjustable_flags.get(t, 0) == 1]
    
    # Group by action_type
    merge_groups = {}
    for t in adjustable_tasks:
        action = action_types.get(t, "unknown")
        if action not in merge_groups:
            merge_groups[action] = []
        merge_groups[action].append(t)
    
    return merge_groups
```

**2. Create Merge Decision Variables**:
```python
# For each pair of consecutive adjustable tasks with same action_type
merge_vars = {}
for action, task_list in merge_groups.items():
    for i in range(len(task_list) - 1):
        t1, t2 = task_list[i], task_list[i+1]
        merge_vars[(t1, t2)] = model.NewBoolVar(f'merge_{t1}_{t2}')
```

**3. Merging Constraints**:
```python
# If merged, both tasks must be at same station
for (t1, t2), merge_var in merge_vars.items():
    for p in range(num_stations):
        model.Add(
            assign[t1, p] == assign[t2, p]
        ).OnlyEnforceIf(merge_var)
```

**4. Effective Duration Adjustment**:
```python
# Merged tasks gain efficiency (e.g., 10% reduction)
effective_duration = {}
for t in tasks:
    effective_duration[t] = model.NewIntVar(0, duration[t], f'eff_dur_{t}')

for (t1, t2), merge_var in merge_vars.items():
    # If merged: effective duration = 90% of sum
    merged_duration = int((duration[t1] + duration[t2]) * 0.9)
    model.Add(effective_duration[t1] == merged_duration).OnlyEnforceIf(merge_var)
    
    # If not merged: use original duration
    model.Add(effective_duration[t1] == duration[t1]).OnlyEnforceIf(merge_var.Not())
```

**5. Capacity Constraint with Effective Duration**:
```python
for p in range(num_stations):
    model.Add(
        sum(assign[t, p] * effective_duration[t] for t in tasks) <= cycle_time
    )
```

#### **Objective Function Enhancement**

```python
# Primary objective: minimize stations
# Secondary objective: maximize merges (reduce complexity)
num_stations_var = model.NewIntVar(0, len(tasks), 'num_stations')
merge_count = sum(merge_vars.values())

# Two-phase optimization
model.Minimize(num_stations_var * 1000 - merge_count)
```

#### **Extended KPI Calculation**

```python
def compute_kpis_with_merging(assignment, merge_vars, durations):
    """Compute KPIs including merge efficiency"""
    
    # Count merged pairs
    merged_pairs = [(t1, t2) for (t1, t2), var in merge_vars.items() if var.solution_value() == 1]
    merge_count = len(merged_pairs)
    
    # Calculate efficiency gain
    original_time = sum(durations[t1] + durations[t2] for t1, t2 in merged_pairs)
    merged_time = sum((durations[t1] + durations[t2]) * 0.9 for t1, t2 in merged_pairs)
    efficiency_gain = (original_time - merged_time) / original_time * 100 if original_time > 0 else 0
    
    return {
        **standard_kpis,
        "adjustable_tasks_count": len([t for t in tasks if adjustable[t] == 1]),
        "merged_tasks_count": merge_count,
        "merge_efficiency_gain": round(efficiency_gain, 2)
    }
```

#### **Output Format**

**station.csv (Extended)**:
```csv
station_index,total_load,adjustable_tasks,merged_task_pairs,workers
0,7,"1,3","1-3",1
1,5,"4,5","4-5",1
2,6,"7","",1
```

#### **Usage Example**

```bash
python sche-algo.py \
  --tasks_csv data/tasks_with_adjustable.csv \
  --objective min_stations \
  --enable_task_merging \
  --merge_efficiency_gain 0.10 \
  --station_csv output/stations_merged.csv
```

**Expected Output (kpi.csv)**:
```csv
metric,value,unit
total_stations,3,stations
adjustable_tasks_count,8,tasks
merged_tasks_count,3,pairs
merge_efficiency_gain,10.5,percent
```

---

### 8️⃣ **Combined Model (Offline + Adjustable)**

#### **Purpose**
Combine offline task handling and adjustable task merging for comprehensive optimization.

#### **Algorithm Workflow**

```
1. Read CSV with all extended columns
   ├── offline_flag
   ├── adjustable
   └── action_type

2. Filter Tasks
   ├── Online + Adjustable → Candidates for merging
   ├── Online + Fixed → Normal assignment
   └── Offline → Post-processing

3. Optimize Online Tasks
   ├── Apply merging constraints for adjustable tasks
   ├── Minimize stations
   └── Maximize merge efficiency

4. Assign Offline Tasks
   └── Dedicated offline stations

5. Compute Extended KPIs
   ├── Online/offline metrics
   ├── Merge metrics
   └── Combined efficiency
```

#### **Usage Example**

```bash
python sche-algo.py \
  --tasks_csv data/tasks_full_extended.csv \
  --objective min_stations \
  --enable_offline_handling \
  --enable_task_merging \
  --station_csv output/stations_full.csv \
  --kpi_csv output/kpi_full.csv
```

**Input CSV (Full Extended)**:
```csv
task_id,duration,offline_flag,adjustable,action_type,predecessors
1,5,0,1,"screw",
2,3,1,0,"glue",1
3,4,0,1,"screw",1
4,2,0,0,"test","2,3"
5,6,1,1,"clip",4
6,3,0,1,"screw","4"
```

**Expected Output**:
```csv
station_index,total_load,online_tasks,offline_tasks,adjustable_tasks,merged_task_pairs,online_load,offline_load
0,7,"1,3","","1,3","1-3",7,0
1,5,"4,6","","6","",5,0
-1,9,"","2,5","5","",0,9
```

---

## 📊 Updated Model Selection Guide

| Requirement                 | Recommended Model         | Parameters                                        | Phase   |
| --------------------------- | ------------------------- | ------------------------------------------------- | ------- |
| Minimum stations            | Boolean Model             | `--objective min_stations --model boolean`        | 1       |
| Minimum workforce           | Manpower Model            | `--objective min_manpower --target_takt N`        | 1       |
| Load balancing              | Idle Model                | `--objective min_idle`                            | 1       |
| **Offline task handling**   | **Offline-Aware Model**   | `--enable_offline_handling`                       | **1.5** |
| **Adjustable task merging** | **Adjustable Task Model** | `--enable_task_merging`                           | **1.5** |
| **Combined optimization**   | **Combined Model**        | `--enable_offline_handling --enable_task_merging` | **1.5** |
| Compound objectives         | Multi-Objective           | `--multi_objective stations_then_idle`            | 1       |
| Quick testing               | Greedy                    | `--model greedy`                                  | 1       |


