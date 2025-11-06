# Models & Strategies Explanation (English)

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

| Strategy Name | Algorithm | Objective Function | Uses OR-Tools? | Main Purpose |
|--------------|-----------|-------------------|----------------|--------------|
| **Greedy** | Greedy Heuristic | Fast Feasible Solution | ❌ | Initial Solution + Hint |
| **Boolean Model** | CP-SAT (Boolean Variables) | Minimize Stations | ✅ | Station Count Optimization |
| **Scheduling Model** | CP-SAT (Cumulative Constraint) | Minimize Last Station Index | ✅ | Station Count Optimization (Alternative) |
| **Manpower Model** | CP-SAT (Integer Variables) | Minimize Total Workers | ✅ | Workforce Optimization |
| **Idle Model** | CP-SAT (Load Balancing) | Minimize Bottleneck Load | ✅ | Load Balancing |
| **Multi-Objective** | Two-Phase Optimization | Compound Objectives | ✅ | Multi-Goal Optimization |

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

| Requirement | Recommended Model | Parameters |
|-------------|-------------------|------------|
| Minimum stations | Boolean Model | `--objective min_stations --model boolean` |
| Minimum workforce | Manpower Model | `--objective min_manpower --target_takt N` |
| Load balancing | Idle Model | `--objective min_idle` |
| Compound objectives | Multi-Objective | `--multi_objective stations_then_idle` |
| Quick testing | Greedy | `--model greedy` |

### **Solving Time Comparison** (Empirical values):

| Model | 12 Tasks | 50 Tasks | 100 Tasks |
|-------|----------|----------|-----------|
| Greedy | < 0.1s | < 0.5s | < 1s |
| Boolean | 1-5s | 10-60s | 60-300s |
| Scheduling | 1-3s | 5-30s | 30-180s |
| Manpower | 2-10s | 20-120s | 120-600s |
| Idle | 1-5s | 10-60s | 60-300s |

**Note**: Actual time depends on problem complexity (number of precedence relations, cycle_time tightness, etc.).
