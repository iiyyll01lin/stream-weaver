# Input/Output Column Specification

## 📥 Input Format

### 1. tasks.csv (Required)

Task definition file containing basic information for all tasks.

| Column Name        | Data Type | Required     | Description                                                                                    | Example                         | Phase Support |
|--------------------|-----------|--------------|------------------------------------------------------------------------------------------------|---------------------------------|---------------|
| `task_id`          | Integer   | ✅ Required   | Unique task identifier                                                                         | 1, 2, 3                         | Phase 1       |
| `duration`         | Integer   | ✅ Required   | Task execution time (seconds/minutes/any time unit)                                            | 5, 10, 15                       | Phase 1       |
| `predecessors`     | String    | ❌ Optional   | Comma-separated list of predecessor task IDs, leave empty if none                              | "1,2,3" or ""                   | Phase 1       |
| `offline_flag`     | Integer   | ⚠️ Phase 1.5 | Offline processing indicator: 0=online (on production line), 1=offline (off-line processing)   | 0, 1                            | Phase 1.5     |
| `adjustable`       | Integer   | ⚠️ Phase 1.5 | Task adjustability: 0=fixed duration (cannot be merged/split), 1=adjustable (can be optimized) | 0, 1                            | Phase 1.5     |
| `action_type`      | String    | ❌ Optional   | Action classification for grouping similar tasks                                               | "screw", "glue", "clip", "test" | Phase 1.5     |
| `motion_type`      | String    | ❌ Optional   | Detailed motion classification (MOST/MTM) ⚠️ **REQ #14**                                        | "finger", "wrist", "elbow", "arm", "body" | Phase 1.5 Ext |
| `equipment_id`     | String    | ❌ Optional   | Equipment used for action (scanner, torque driver, etc.) ⚠️ **REQ #14**                         | "SCANNER_01", "TORQUE_DRV_M3" | Phase 1.5 Ext |
| `non_divisible`    | Integer   | ❌ Optional   | Task cannot be split across stations (0=divisible, 1=non-divisible) ⚠️ **REQ #42**              | 0, 1                            | Phase 1.5 Ext |
| `exclude_from_balance` | Integer | ❌ Optional | Exclude from line balancing (e.g., packaging materials) ⚠️ **REQ #43b**                        | 0, 1                            | Phase 1.5 Ext |
| `expected_cycle_time` | Integer | ❌ Optional  | Expected/target cycle time for alerting (from BDC) ⚠️ **REQ #44b**                             | 5000, 8000                      | Phase 2       |
| `complexity_level` | String    | ❌ Optional   | Assembly complexity: simple/medium/complex/super_complex (REQ #10)                             | "simple", "complex"             | Phase 1.5 Ext |
| `part_id`          | String    | ❌ Optional   | Part number for BOM integration (REQ #12)                                                      | "GPU_GTX3080", "HDD_2TB"        | Phase 1.5 Ext |

**Example File (Phase 1 - Basic):**
```csv
task_id,duration,predecessors
1,5,
2,3,1
3,4,1
4,2,"2,3"
5,6,4
```

**Example File (Phase 1.5 - Extended):**
```csv
task_id,duration,offline_flag,adjustable,action_type,complexity_level,part_id,predecessors
1,5000,0,1,"screw","simple","GPU_BRACKET",
2,3000,1,0,"glue","medium","THERMAL_PAD",1
3,4000,0,1,"screw","simple","FAN_MOUNT",1
4,2000,0,0,"test","medium","POST_TEST","2,3"
5,6000,1,1,"clip","complex","CABLE_ASSY",4
```

**Notes:**
- `task_id`: Recommended to start from 1 with consecutive numbering
- `duration`: Must be a positive integer, unit should be consistent with `cycle_time`
- `predecessors`: Can define precedence relationships in this column or use a separate `precedences.csv`
- `offline_flag` (Phase 1.5): 
  - **0 (online)**: Task is performed on the production line and included in station optimization
  - **1 (offline)**: Task is performed offline (e.g., pre-assembly, quality inspection) and excluded from line balancing
  - **Use case**: REQ #4 & #15 - Separate online/offline operations for accurate workstation configuration
- `adjustable` (Phase 1.5):
  - **0 (fixed)**: Task duration is fixed and cannot be modified during optimization
  - **1 (adjustable)**: Task can be merged with similar tasks or split for better load balancing
  - **Use case**: REQ #13 - Enable flexible task grouping to improve station utilization
- `action_type` (Phase 1.5):
  - Classifies tasks by action category (screw, glue, clip, test, etc.)
  - Used for identifying merge candidates (e.g., two "screw" tasks can be merged)
  - Supports future ML-based complexity classification (REQ #10)
- `motion_type` (⚠️ Phase 1.5 Extended - REQ #14):
  - **MOST/MTM-based motion classification** for accurate time study:
    - `finger`: Fine motor movements (picking small parts, pressing buttons)
    - `wrist`: Wrist rotation (turning screws, adjusting orientation)
    - `elbow`: Forearm movements (reaching nearby, short carries)
    - `arm`: Full arm movements (reaching far, long carries)
    - `body`: Trunk/leg movements (bending, walking, heavy lifting)
  - **Use case**: More accurate time estimation based on motion complexity
  - **MVS Integration**: Maps to Method Time Measurement (MTM) codes
- `equipment_id` (⚠️ Phase 1.5 Extended - REQ #14):
  - Equipment identifier for actions requiring tools/devices:
    - `SCANNER_01`: Barcode scanner
    - `TORQUE_DRV_M3`: Torque driver for M3 screws
    - `THERMAL_CAM`: Thermal imaging camera
    - `LABEL_PRINTER`: Label printer
  - **Use case**: Equipment capacity planning, maintenance scheduling
  - **Constraint**: Tasks with same equipment cannot overlap in time
- `non_divisible` (⚠️ Phase 1.5 Extended - REQ #42):
  - **0 (divisible)**: Task can be split across stations if needed
  - **1 (non-divisible)**: Task must remain whole at one station
  - **Use case**: Class Code or 12-digit part number based constraints
  - **Example**: GPU installation must be done at single station
- `exclude_from_balance` (⚠️ Phase 1.5 Extended - REQ #43b):
  - **0 (include)**: Normal task included in line balancing
  - **1 (exclude)**: Excluded from optimization (packaging materials, etc.)
  - **Use case**: Filter out non-assembly materials from line balance
- `complexity_level` (⚠️ Phase 1.5 Extended):
  - Assembly complexity classification: `simple`, `medium`, `complex`, `super_complex`
  - Auto-classified based on part characteristics (e.g., graphics card = complex, screw = simple)
  - **Use case**: REQ #10 - BOO Rack complexity classification for scheduling and line balancing
  - **Implementation**: Can be auto-generated from part_id using lookup table or ML model
- `part_id` (⚠️ Phase 1.5 Extended):
  - Part number or component identifier (e.g., "GPU_GTX3080", "HDD_2TB", "CABLE_SATA")
  - Maps action units to physical parts for BOM integration
  - **Use case**: REQ #12 - Link action units to parts for material tracking
  - **Optional**: Leave empty for non-part-specific actions (e.g., "quality_check")

---

### 2. precedences.csv (Optional)

Precedence relationship definition file. This file can be omitted if precedence relationships are already defined in the `predecessors` column of `tasks.csv`.

| Column Name   | Data Type | Required   | Description                                        | Example |
|---------------|-----------|------------|----------------------------------------------------|---------|
| `before_task` | Integer   | ✅ Required | Predecessor task ID                                | 1       |
| `after_task`  | Integer   | ✅ Required | Successor task ID (must execute after before_task) | 2       |

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

| Column Name | Data Type      | Required   | Description     | Example    |
|-------------|----------------|------------|-----------------|------------|
| `parameter` | String         | ✅ Required | Parameter name  | cycle_time |
| `value`     | String/Integer | ✅ Required | Parameter value | 20         |

**Supported Parameters:**
- `cycle_time`: Maximum cycle time limit for workstations
- `max_workers_per_station`: Maximum workers per station (default: 8) ⚠️ **REQ #45b - per factory override**
- `site_id`: Site/factory identifier for per-site configuration
- `station_type`: Station type configuration (`fixed`, `adjustable`, `multi_person`) ⚠️ **REQ #46b**
- `available_production_hours`: Available production hours per day (for UPH calculation)

**Example File:**
```csv
parameter,value
cycle_time,20
max_workers_per_station,4
site_id,TAO_FACTORY_A
station_type,adjustable
available_production_hours,8
```

**Per-Site Configuration** (⚠️ REQ #45b):
- Different factories may have different maximum workers per station
- Use `site_id` to identify the factory and apply site-specific rules
- Example: `TAO_FACTORY_A` allows max 6 workers, `MEX_FACTORY_B` allows max 4

**Station Type Definitions** (⚠️ REQ #46b):
| Type          | Description                                       | Max Workers |
|---------------|---------------------------------------------------|-------------|
| `fixed`       | Single-person fixed station, no adjustment        | 1           |
| `adjustable`  | Adjustable workload, can absorb overflow          | 2-4         |
| `multi_person`| Designed for multiple workers, parallel tasks OK  | 4-8         |

**Notes:**
- If `cycle_time` is not provided, the system will auto-estimate: `Total Duration ÷ (Number of Tasks ÷ 3)`
- Command-line parameters take precedence over this file

---

## 📤 Output Format

### 1. solution.csv (Task Assignment Results)

Specify output path using `--csv_output` parameter.

| Column Name        | Data Type | Description                                 | Example |
|--------------------|-----------|---------------------------------------------|---------|
| `task_id`          | Integer   | Task ID                                     | 1       |
| `station_index`    | Integer   | Assigned workstation number (starts from 0) | 0       |
| `workers_assigned` | Integer   | Number of workers assigned to this station  | 2       |
| `task_duration`    | Integer   | Task execution time                         | 5       |
| `cumulative_load`  | Integer   | Cumulative workload at this station         | 8       |

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

| Column Name | Data Type      | Description             | Unit |
|-------------|----------------|-------------------------|------|
| `metric`    | String         | Performance metric name | -    |
| `value`     | Numeric/String | Metric value            | -    |
| `unit`      | String         | Value unit              | -    |

**Included Metrics:**

| metric                   | Description                               | Unit       | Phase |
|--------------------------|-------------------------------------------|------------|-------|
| `total_stations`         | Total number of stations used             | stations   | 1     |
| `total_workers`          | Total workforce assigned                  | persons    | 1     |
| `bottleneck_station`     | Bottleneck station index (highest load)   | -          | 1     |
| `bottleneck_load`        | Workload at bottleneck station            | time_units | 1     |
| `calculated_takt`        | Actual takt time (= bottleneck load)      | time_units | 1     |
| `target_takt`            | Target takt time (from parameters)        | time_units | 1     |
| `cycle_time`             | Cycle time limit                          | time_units | 1     |
| `avg_utilization`        | Average utilization rate                  | percent    | 1     |
| `total_idle_time`        | Total idle time (relative to bottleneck)  | time_units | 1     |
| `solve_time`             | Solving time                              | seconds    | 1     |
| `online_stations`        | Number of stations with online tasks only | stations   | 1.5   |
| `offline_tasks_count`    | Total number of offline tasks             | tasks      | 1.5   |
| `offline_total_time`     | Total time for all offline tasks          | time_units | 1.5   |
| `adjustable_tasks_count` | Number of adjustable tasks                | tasks      | 1.5   |
| `merged_tasks_count`     | Number of successfully merged task pairs  | pairs      | 1.5   |
| `merge_efficiency_gain`  | Time saved through task merging           | percent    | 1.5   |

**Example File (Phase 1):**
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

**Example File (Phase 1.5 - Extended):**
```csv
metric,value,unit
total_stations,3,stations
total_workers,4,persons
bottleneck_station,0,
bottleneck_load,8,time_units
calculated_takt,8,time_units
target_takt,60,time_units
cycle_time,20,time_units
avg_utilization,73.33,percent
total_idle_time,6,time_units
solve_time,0.125,seconds
online_stations,2,stations
offline_tasks_count,3,tasks
offline_total_time,12,time_units
adjustable_tasks_count,5,tasks
merged_tasks_count,2,pairs
merge_efficiency_gain,8.5,percent
```

---

### 3. station.csv (Workstation Details)

Specify output path using `--station_csv` parameter.

| Column Name          | Data Type | Description                                | Example   | Phase |
|----------------------|-----------|--------------------------------------------|-----------|-------|
| `station_index`      | Integer   | Station number (starts from 0)             | 0         | 1     |
| `total_load`         | Integer   | Total workload at this station             | 8         | 1     |
| `idle_vs_bottleneck` | Integer   | Idle time relative to bottleneck station   | 0         | 1     |
| `workers`            | Integer   | Number of workers assigned                 | 2         | 1     |
| `utilization_pct`    | Float     | Utilization percentage                     | 100.0     | 1     |
| `assigned_tasks`     | String    | Comma-separated list of assigned tasks     | "1,2"     | 1     |
| `online_tasks`       | String    | Comma-separated list of online tasks only  | "1,3"     | 1.5   |
| `offline_tasks`      | String    | Comma-separated list of offline tasks only | "2"       | 1.5   |
| `adjustable_tasks`   | String    | Tasks that can be merged/split             | "1,3,5"   | 1.5   |
| `merged_task_pairs`  | String    | Pairs of merged tasks                      | "1-2,3-4" | 1.5   |
| `online_load`        | Integer   | Workload from online tasks only            | 6         | 1.5   |
| `offline_load`       | Integer   | Workload from offline tasks only           | 2         | 1.5   |

**Example File (Phase 1 - Basic):**
```csv
station_index,total_load,idle_vs_bottleneck,workers,utilization_pct,assigned_tasks
0,8,0,2,100.0,"1,2"
1,6,2,1,75.0,"3,4"
2,6,2,1,75.0,"5"
```

**Example File (Phase 1.5 - Extended):**
```csv
station_index,total_load,idle_vs_bottleneck,workers,utilization_pct,assigned_tasks,online_tasks,offline_tasks,adjustable_tasks,merged_task_pairs,online_load,offline_load
0,8,0,2,100.0,"1,2","1","2","1","1-2",5,3
1,6,2,1,75.0,"3,4,5","3,4","5","3,4","3-4",4,2
2,4,4,1,50.0,"6,7","6,7","","6,7","",4,0
```

**Notes:**
- `idle_vs_bottleneck`: 0 indicates this is the bottleneck station, positive values indicate idle time relative to bottleneck
- `utilization_pct`: Calculated as `(total_load / (workers × target_takt)) × 100`
- `online_tasks` (Phase 1.5): Tasks performed on production line (offline_flag=0)
- `offline_tasks` (Phase 1.5): Tasks performed off-line (offline_flag=1), excluded from line balancing
- `adjustable_tasks` (Phase 1.5): Tasks with adjustable=1 that can be optimized
- `merged_task_pairs` (Phase 1.5): Format "taskA-taskB,taskC-taskD" shows which tasks were merged
- `online_load` / `offline_load` (Phase 1.5): Separate workload metrics for better capacity planning

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
| File              | Required   | Required Columns            | Optional Columns |
|-------------------|------------|-----------------------------|------------------|
| `tasks.csv`       | ✅ Required | `task_id`, `duration`       | `predecessors`   |
| `precedences.csv` | ❌ Optional | `before_task`, `after_task` | -                |
| `config.csv`      | ❌ Optional | `parameter`, `value`        | -                |

### Output Files
All output files are optional and depend on command-line parameters:
- `--csv_output`: Generates solution.csv
- `--kpi_csv`: Generates kpi.csv
- `--station_csv`: Generates station.csv
- `--json_output`: Generates output.json

---

## ⚙️ Complete Command-Line Parameters

### Input Parameters
| Parameter           | Type   | Default | Description                                  |
|---------------------|--------|---------|----------------------------------------------|
| `--input`           | String | ""      | Input file path (tasks.csv)                  |
| `--tasks_csv`       | String | ""      | Tasks CSV file path, uses `--input` if empty |
| `--precedences_csv` | String | ""      | Precedences CSV file path (optional)         |
| `--config_csv`      | String | ""      | Configuration CSV file path (optional)       |

### Solver Parameters
| Parameter                   | Type    | Default        | Options                                | Description                                     |
|-----------------------------|---------|----------------|----------------------------------------|-------------------------------------------------|
| `--objective`               | String  | "min_stations" | min_stations, min_manpower, min_idle   | Optimization objective                          |
| `--model`                   | String  | "boolean"      | boolean, scheduling, greedy            | Solver model (for min_stations only)            |
| `--target_takt`             | Integer | 0              | > 0                                    | Target takt time (required for min_manpower)    |
| `--max_workers_per_station` | Integer | 8              | > 0                                    | Maximum workers per station (for min_manpower)  |
| `--fixed_stations`          | Integer | 0              | ≥ 0                                    | Fixed number of stations (for min_idle, 0=auto) |
| `--multi_objective`         | String  | ""             | stations_then_idle, manpower_then_idle | Multi-objective optimization mode               |
| `--params`                  | String  | ""             | -                                      | OR-Tools CP-SAT solver parameters               |

### Output Parameters
| Parameter        | Type   | Default | Description                                     |
|------------------|--------|---------|-------------------------------------------------|
| `--csv_output`   | String | ""      | Task assignment CSV output path                 |
| `--kpi_csv`      | String | ""      | KPI summary CSV output path                     |
| `--station_csv`  | String | ""      | Station details CSV output path                 |
| `--json_output`  | String | ""      | Complete result JSON output path                |
| `--output_proto` | String | ""      | CP model proto file output path (for debugging) |

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
