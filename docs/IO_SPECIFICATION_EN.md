# Input/Output Column Specification

## 📥 Input Format

### 1. tasks.csv (Required)

Task definition file containing basic information for all tasks.

| Column Name | Data Type | Required | Description | Example |
|------------|-----------|----------|-------------|---------|
| `task_id` | Integer | ✅ Required | Unique task identifier | 1, 2, 3 |
| `duration` | Integer | ✅ Required | Task execution time (seconds/minutes/any time unit) | 5, 10, 15 |
| `predecessors` | String | ❌ Optional | Comma-separated list of predecessor task IDs, leave empty if none | "1,2,3" or "" |

**Example File:**
```csv
task_id,duration,predecessors
1,5,
2,3,1
3,4,1
4,2,"2,3"
5,6,4
```

**Notes:**
- `task_id`: Recommended to start from 1 with consecutive numbering
- `duration`: Must be a positive integer, unit should be consistent with `cycle_time`
- `predecessors`: Can define precedence relationships in this column or use a separate `precedences.csv`

---

### 2. precedences.csv (Optional)

Precedence relationship definition file. This file can be omitted if precedence relationships are already defined in the `predecessors` column of `tasks.csv`.

| Column Name | Data Type | Required | Description | Example |
|------------|-----------|----------|-------------|---------|
| `before_task` | Integer | ✅ Required | Predecessor task ID | 1 |
| `after_task` | Integer | ✅ Required | Successor task ID (must execute after before_task) | 2 |

**Example File:**
```csv
before_task,after_task
1,2
1,3
2,4
3,4
4,5
```

**Notes:**
- Each row defines one precedence constraint: `after_task` must start after `before_task` is completed
- Circular dependencies are not allowed (e.g., A→B→C→A)

---

### 3. config.csv (Optional)

System parameter configuration file. If not provided, command-line parameters or default values will be used.

| Column Name | Data Type | Required | Description | Example |
|------------|-----------|----------|-------------|---------|
| `parameter` | String | ✅ Required | Parameter name | cycle_time |
| `value` | String/Integer | ✅ Required | Parameter value | 20 |

**Supported Parameters:**
- `cycle_time`: Maximum cycle time limit for workstations

**Example File:**
```csv
parameter,value
cycle_time,20
```

**Notes:**
- If `cycle_time` is not provided, the system will auto-estimate: `Total Duration ÷ (Number of Tasks ÷ 3)`
- Command-line parameters take precedence over this file

---

## 📤 Output Format

### 1. solution.csv (Task Assignment Results)

Specify output path using `--csv_output` parameter.

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| `task_id` | Integer | Task ID | 1 |
| `station_index` | Integer | Assigned workstation number (starts from 0) | 0 |
| `workers_assigned` | Integer | Number of workers assigned to this station | 2 |
| `task_duration` | Integer | Task execution time | 5 |
| `cumulative_load` | Integer | Cumulative workload at this station | 8 |

**Example File:**
```csv
task_id,station_index,workers_assigned,task_duration,cumulative_load
1,0,2,5,5
2,0,2,3,8
3,1,1,4,4
4,1,1,2,6
5,2,1,6,6
```

**Notes:**
- Tasks at the same station are sorted by `task_id`
- `cumulative_load` is the cumulative time from the first task to the current task within the station

---

### 2. kpi.csv (Performance Metrics Summary)

Specify output path using `--kpi_csv` parameter.

| Column Name | Data Type | Description | Unit |
|------------|-----------|-------------|------|
| `metric` | String | Performance metric name | - |
| `value` | Numeric/String | Metric value | - |
| `unit` | String | Value unit | - |

**Included Metrics:**

| metric | Description | Unit |
|--------|-------------|------|
| `total_stations` | Total number of stations used | stations |
| `total_workers` | Total workforce assigned | persons |
| `bottleneck_station` | Bottleneck station index (highest load) | - |
| `bottleneck_load` | Workload at bottleneck station | time_units |
| `calculated_takt` | Actual takt time (= bottleneck load) | time_units |
| `target_takt` | Target takt time (from parameters) | time_units |
| `cycle_time` | Cycle time limit | time_units |
| `avg_utilization` | Average utilization rate | percent |
| `total_idle_time` | Total idle time (relative to bottleneck) | time_units |
| `solve_time` | Solving time | seconds |

**Example File:**
```csv
metric,value,unit
total_stations,3,stations
total_workers,4,persons
bottleneck_station,0,
bottleneck_load,8,time_units
calculated_takt,8,time_units
target_takt,0,time_units
cycle_time,20,time_units
avg_utilization,73.33,percent
total_idle_time,6,time_units
solve_time,0.125,seconds
```

---

### 3. station.csv (Workstation Details)

Specify output path using `--station_csv` parameter.

| Column Name | Data Type | Description | Example |
|------------|-----------|-------------|---------|
| `station_index` | Integer | Station number (starts from 0) | 0 |
| `total_load` | Integer | Total workload at this station | 8 |
| `idle_vs_bottleneck` | Integer | Idle time relative to bottleneck station | 0 |
| `workers` | Integer | Number of workers assigned | 2 |
| `utilization_pct` | Float | Utilization percentage | 100.0 |
| `assigned_tasks` | String | Comma-separated list of assigned tasks | "1,2" |

**Example File:**
```csv
station_index,total_load,idle_vs_bottleneck,workers,utilization_pct,assigned_tasks
0,8,0,2,100.0,"1,2"
1,6,2,1,75.0,"3,4"
2,6,2,1,75.0,"5"
```

**Notes:**
- `idle_vs_bottleneck`: 0 indicates this is the bottleneck station, positive values indicate idle time relative to bottleneck
- `utilization_pct`: Calculated as `(total_load / (workers × target_takt)) × 100`

---

### 4. output.json (Complete Output)

Specify output path using `--json_output` parameter. JSON format file containing all solution information.

**Structure:**
```json
{
  "input_file": "data/test_tasks.csv",
  "objective": "min_stations",
  "multi_objective": "",
  "model": "boolean",
  "assignment": {
    "1": 0,
    "2": 0,
    "3": 1,
    "4": 1,
    "5": 2
  },
  "workers": {
    "0": 2,
    "1": 1,
    "2": 1
  },
  "kpis": {
    "stations": [...],
    "bottleneck_station": 0,
    "bottleneck_load": 8,
    "calculated_takt": 8,
    "target_takt": 0,
    "cycle_time": 20,
    "manpower_total": 4,
    "avg_utilization_pct": 73.33,
    "total_idle_time": 6
  },
  "solve_time_seconds": 0.125
}
```

---

## 🎯 Usage Examples

### Basic Usage
```bash
# Minimal configuration (use --input to specify tasks.csv)
python or-line-balance.py \
  --input data/tasks.csv

# Use --tasks_csv parameter (more explicit)
python or-line-balance.py \
  --tasks_csv data/tasks.csv

# Full configuration
python or-line-balance.py \
  --tasks_csv data/tasks.csv \
  --precedences_csv data/precedences.csv \
  --config_csv data/config.csv \
  --csv_output output/solution.csv \
  --kpi_csv output/kpi.csv \
  --station_csv output/station.csv \
  --json_output output/result.json
```

### Different Objective Functions
```bash
# Minimize number of stations (default objective)
python or-line-balance.py \
  --input data/tasks.csv \
  --objective min_stations

# Minimize manpower (requires target_takt)
python or-line-balance.py \
  --input data/tasks.csv \
  --objective min_manpower \
  --target_takt 10 \
  --max_workers_per_station 8

# Minimize idle time (requires fixed station count)
python or-line-balance.py \
  --input data/tasks.csv \
  --objective min_idle \
  --fixed_stations 3

# Multi-objective optimization
python or-line-balance.py \
  --input data/tasks.csv \
  --multi_objective stations_then_idle
```

---

## 📋 Column Requirements Summary

### Input Files
| File | Required | Required Columns | Optional Columns |
|------|----------|------------------|------------------|
| `tasks.csv` | ✅ Required | `task_id`, `duration` | `predecessors` |
| `precedences.csv` | ❌ Optional | `before_task`, `after_task` | - |
| `config.csv` | ❌ Optional | `parameter`, `value` | - |

### Output Files
All output files are optional and depend on command-line parameters:
- `--csv_output`: Generates solution.csv
- `--kpi_csv`: Generates kpi.csv
- `--station_csv`: Generates station.csv
- `--json_output`: Generates output.json

---

## ⚙️ Complete Command-Line Parameters

### Input Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--input` | String | "" | Input file path (tasks.csv) |
| `--tasks_csv` | String | "" | Tasks CSV file path, uses `--input` if empty |
| `--precedences_csv` | String | "" | Precedences CSV file path (optional) |
| `--config_csv` | String | "" | Configuration CSV file path (optional) |

### Solver Parameters
| Parameter | Type | Default | Options | Description |
|-----------|------|---------|---------|-------------|
| `--objective` | String | "min_stations" | min_stations, min_manpower, min_idle | Optimization objective |
| `--model` | String | "boolean" | boolean, scheduling, greedy | Solver model (for min_stations only) |
| `--target_takt` | Integer | 0 | > 0 | Target takt time (required for min_manpower) |
| `--max_workers_per_station` | Integer | 8 | > 0 | Maximum workers per station (for min_manpower) |
| `--fixed_stations` | Integer | 0 | ≥ 0 | Fixed number of stations (for min_idle, 0=auto) |
| `--multi_objective` | String | "" | stations_then_idle, manpower_then_idle | Multi-objective optimization mode |
| `--params` | String | "" | - | OR-Tools CP-SAT solver parameters |

### Output Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `--csv_output` | String | "" | Task assignment CSV output path |
| `--kpi_csv` | String | "" | KPI summary CSV output path |
| `--station_csv` | String | "" | Station details CSV output path |
| `--json_output` | String | "" | Complete result JSON output path |
| `--output_proto` | String | "" | CP model proto file output path (for debugging) |

### Parameter Combination Rules
1. **min_stations**: Can specify `--model` (boolean/scheduling/greedy)
2. **min_manpower**: Must specify `--target_takt > 0`
3. **min_idle**: Can specify `--fixed_stations` (0=use greedy result)
4. **multi_objective**: Overrides `--objective` and `--model` settings

### Example: Full Parameters
```bash
python or-line-balance.py \
  --input data/tasks.csv \
  --precedences_csv data/precedences.csv \
  --config_csv data/config.csv \
  --objective min_manpower \
  --target_takt 300 \
  --max_workers_per_station 4 \
  --csv_output output/solution.csv \
  --kpi_csv output/kpi.csv \
  --station_csv output/stations.csv \
  --json_output output/result.json \
  --params "max_time_in_seconds:60.0"
```
