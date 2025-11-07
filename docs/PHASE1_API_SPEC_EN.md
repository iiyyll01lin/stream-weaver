# Phase 1 API Specification

**Document Version**: 1.0 | **Last Updated**: 2025-11-07  
**Related Documents**:
- [Phase 1 Architecture](PHASE1_ARCHITECTURE_EN.md)
- [Implementation Guide](PHASE1_IMPLEMENTATION_EN.md)
- [IO Specification](../IO_SPECIFICATION_EN.md)

---

## Table of Contents

- [Overview](#overview)
- [Base Information](#base-information)
- [Authentication & Authorization](#authentication--authorization)
- [API Endpoints](#api-endpoints)
  - [Core Optimization Endpoint](#1-core-optimization-endpoint)
  - [Query Workstations](#2-query-workstations)
  - [Query Takt Summary](#3-query-takt-summary)
  - [Health Check](#4-health-check)
- [Data Models](#data-models)
- [Error Handling](#error-handling)
- [Usage Examples](#usage-examples)

---

## Overview

The Phase 1 API provides a RESTful interface for line balance optimization, supporting the following core features:

1. **Optimization Execution**: Submit work order data to receive optimal workstation allocation
2. **Workstation Query**: Retrieve current workstation configuration and load information
3. **Takt Analysis**: Calculate takt time and efficiency metrics
4. **System Status**: Monitor service health and availability

### Design Principles

- **RESTful Architecture**: Standard HTTP methods (GET/POST)
- **JSON Format**: All requests and responses use JSON
- **Type Safety**: Pydantic v2 validation ensures data correctness
- **Auto-Documentation**: Swagger UI at `/api/docs`

---

## Base Information

### Service URL

**Development Environment**:
```
http://localhost:8000
```

**Docker Environment**:
```
http://localhost:8000  # Port mapping can be modified in docker-compose.yml
```

### Request Headers

All requests should include:
```http
Content-Type: application/json
Accept: application/json
```

---

## Authentication & Authorization

**Phase 1**: No authentication mechanism implemented (development use only)

**Future Phases** (planned):
- JWT Token authentication
- Role-based access control (RBAC)
- API Key management

---

## API Endpoints

### 1. Core Optimization Endpoint

#### `POST /optimize`

Submit optimization request and receive workstation allocation results.

**Request Body**:
```json
{
  "work_order_id": "WO_A",
  "optimization_goal": "min_stations",
  "target_takt": 30000,
  "max_workers_per_station": 3,
  "fixed_stations": 0
}
```

**Parameters**:

| Field                     | Type    | Required | Description                                                         | Default | Phase |
| ------------------------- | ------- | -------- | ------------------------------------------------------------------- | ------- | ----- |
| `work_order_id`           | string  | Yes      | Work order ID (`WO_A`, `WO_B`, `WO_C`)                              | -       | 1     |
| `optimization_goal`       | string  | Yes      | Optimization objective (`min_stations`, `min_manpower`, `min_idle`) | -       | 1     |
| `target_takt`             | integer | Yes      | Target takt time (milliseconds)                                     | -       | 1     |
| `max_workers_per_station` | integer | No       | Maximum workers per station                                         | 3       | 1     |
| `fixed_stations`          | integer | No       | Fixed number of stations (for `min_idle`)                           | 0       | 1     |
| `enable_offline_handling` | boolean | No       | Enable offline task separation (REQ #4, #15)                        | false   | 1.5   |
| `enable_task_merging`     | boolean | No       | Enable adjustable task merging (REQ #13)                            | false   | 1.5   |
| `merge_efficiency_gain`   | float   | No       | Efficiency gain from merging (0.0-0.5)                              | 0.10    | 1.5   |

**Field Descriptions**:

**Phase 1 Fields**:
- `work_order_id`: Must exist in WORK_ORDER_MAPPING configuration
- `optimization_goal`: Determines solver objective function
- `target_takt`: Must be > 0, used for `min_manpower` and capacity constraints
- `max_workers_per_station`: Limits workforce per station (≥ 1)
- `fixed_stations`: Required for `min_idle` objective (≥ 1)

**Phase 1.5 Fields (Extended)**:
- `enable_offline_handling`: When true, tasks with `offline_flag=1` are:
  - Excluded from line balancing optimization
  - Assigned to separate offline stations (station_index = -1)
  - Reported separately in KPIs (`offline_tasks_count`, `offline_total_time`)
  - **Use case**: Pre-assembly, quality inspection, off-line testing
  
- `enable_task_merging`: When true, tasks with `adjustable=1` and same `action_type`:
  - Can be merged to same station for efficiency
  - Effective duration reduced by `merge_efficiency_gain` percentage
  - Merge decisions optimized in solver
  - **Use case**: Consolidate similar operations (multiple screw tasks)
  
- `merge_efficiency_gain`: Percentage time reduction for merged tasks
  - Range: 0.0 (no gain) to 0.5 (50% max gain)
  - Example: Two 10s tasks merged = 18s (10% gain) instead of 20s
  - Validation: Must be in [0.0, 0.5]

**Optimization Objectives**:

1. **`min_stations`**: Minimize number of workstations
   - Suitable for: Small production volume, high space cost
   - Constraint: No fixed takt limit

2. **`min_manpower`**: Minimize total manpower
   - Suitable for: High labor cost scenarios
   - Constraint: Must meet `target_takt`

3. **`min_idle`**: Minimize total idle time
   - Suitable for: Balanced line load
   - Constraint: `fixed_stations` must be > 0

**Response (200 OK)**:
```json
{
  "work_order_id": "WO_A",
  "objectives": {
    "goal": "min_stations",
    "target_takt": 30000,
    "model": "boolean"
  },
  "stations": [
    {
      "id": "WS-001",
      "total_time_ms": 28500,
      "idle_time_ms": 1500,
      "workers": 1,
      "utilization_pct": 95.0,
      "assigned_tasks": [1, 2, 5],
      
      // Phase 1.5 NEW fields (when enabled)
      "online_tasks": [1, 5],
      "offline_tasks": [2],
      "adjustable_tasks": [1, 5],
      "merged_task_pairs": [[1, 5]],
      "online_load_ms": 25500,
      "offline_load_ms": 3000
    },
    {
      "id": "WS-002",
      "total_time_ms": 29800,
      "idle_time_ms": 200,
      "workers": 1,
      "utilization_pct": 99.33,
      "assigned_tasks": [3, 4, 6],
      "online_tasks": [3, 4, 6],
      "offline_tasks": [],
      "adjustable_tasks": [3, 6],
      "merged_task_pairs": [[3, 6]],
      "online_load_ms": 29800,
      "offline_load_ms": 0
    },
    {
      "id": "OFFLINE-001",  // Phase 1.5 NEW: Offline station
      "total_time_ms": 15000,
      "workers": 0,
      "assigned_tasks": [7, 8, 9],
      "online_tasks": [],
      "offline_tasks": [7, 8, 9],
      "offline_load_ms": 15000
    }
  ],
  "takt_time_ms": 30000,
  "bottleneck_station_id": "WS-002",
  "manpower_total": 2,
  "line_count": 2,
  "utilization_avg": 97.17,
  "total_idle_time_ms": 1700,
  
  // Phase 1.5 NEW fields (when enabled)
  "online_stations": 2,
  "offline_tasks_count": 3,
  "offline_total_time_ms": 15000,
  "merged_tasks_count": 2,
  "merge_efficiency_gain_pct": 10.5,
  "solve_time_sec": 0.85,
  "algorithm_used": "boolean"
}
```

**Error Response (400 Bad Request)**:
```json
{
  "detail": "Parameter error: Invalid work_order_id"
}
```

**Error Response (500 Internal Server Error)**:
```json
{
  "detail": "Algorithm execution failed: Timeout"
}
```

**Performance Requirements**:
- **Latency**: < 3 seconds (dataset with ≤500 actions)
- **Accuracy**: ±5% deviation from manual calculation

---

### 2. Query Workstations

#### `GET /workstations`

Retrieve workstation configuration summary.

**Query Parameters**:
```
GET /workstations?work_order_id=WO_A&target_takt=30000
```

| Parameter       | Type    | Required | Description           |
| --------------- | ------- | -------- | --------------------- |
| `work_order_id` | string  | Yes      | Work order ID         |
| `target_takt`   | integer | Yes      | Target takt time (ms) |

**Response (200 OK)**:
```json
[
  {
    "station_id": "WS-001",
    "load_ms": 28500,
    "utilization_pct": 95.0,
    "workers": 1,
    "task_count": 3
  },
  {
    "station_id": "WS-002",
    "load_ms": 29800,
    "utilization_pct": 99.33,
    "workers": 1,
    "task_count": 3
  }
]
```

---

### 3. Query Takt Summary

#### `GET /takt-summary`

Retrieve takt time analysis summary.

**Query Parameters**:
```
GET /takt-summary?work_order_id=WO_A&target_takt=30000
```

**Response (200 OK)**:
```json
{
  "work_order_id": "WO_A",
  "theoretical_min_takt": 30000,
  "achieved_takt": 29800,
  "bottleneck_station": "WS-002",
  "efficiency_pct": 100.67
}
```

**Field Descriptions**:
- `theoretical_min_takt`: User-specified target takt
- `achieved_takt`: Actual achieved takt (bottleneck station load)
- `efficiency_pct`: `(theoretical / achieved) * 100`

---

### 4. Health Check

#### `GET /health`

Check service health status.

**Response (200 OK)**:
```json
{
  "status": "healthy",
  "version": "1.0.0-phase1",
  "algo_available": true,
  "data_dir": "/workspace/data",
  "available_work_orders": ["WO_A", "WO_B", "WO_C"]
}
```

**Field Descriptions**:
- `algo_available`: Whether `sche-algo.py` exists
- `available_work_orders`: List of work orders configured in `WORK_ORDER_MAPPING`

---

## Data Models

### OptimizeRequest

```python
class OptimizeRequest(BaseModel):
    """Phase 1 + 1.5 Optimization Request"""
    
    # Phase 1 fields
    work_order_id: str                    # Work order ID
    optimization_goal: str                # Optimization objective
    target_takt: int                      # Target takt (ms)
    max_workers_per_station: int = 3      # Max workers per station
    fixed_stations: int = 0               # Fixed stations (for min_idle)
    
    # Phase 1.5 NEW fields
    enable_offline_handling: bool = False  # Enable offline task separation
    enable_task_merging: bool = False      # Enable adjustable task merging
    merge_efficiency_gain: float = 0.10    # Merge efficiency (0.0-0.5)
    
    @validator('merge_efficiency_gain')
    def validate_merge_gain(cls, v):
        if not 0.0 <= v <= 0.5:
            raise ValueError('merge_efficiency_gain must be in [0.0, 0.5]')
        return v
    
    @validator('optimization_goal')
    def validate_goal(cls, v):
        valid_goals = ['min_stations', 'min_manpower', 'min_idle']
        if v not in valid_goals:
            raise ValueError(f'optimization_goal must be one of {valid_goals}')
        return v
```

### StationInfo

```python
class StationInfo(BaseModel):
    """Phase 1 + 1.5 Station Information"""
    
    # Phase 1 fields
    id: str                    # Station ID (e.g., WS-001, OFFLINE-001)
    total_time_ms: int        # Total load time (ms)
    idle_time_ms: int         # Idle time relative to bottleneck (ms)
    workers: int              # Number of workers
    utilization_pct: float    # Utilization percentage
    assigned_tasks: List[int] # All assigned task IDs
    
    # Phase 1.5 NEW fields
    online_tasks: List[int] = []              # Online task IDs only
    offline_tasks: List[int] = []             # Offline task IDs only
    adjustable_tasks: List[int] = []          # Adjustable task IDs
    merged_task_pairs: List[List[int]] = []   # Merged pairs e.g., [[1,3], [5,7]]
    online_load_ms: int = 0                   # Load from online tasks
    offline_load_ms: int = 0                  # Load from offline tasks
```

### OptimizeResponse

```python
class OptimizeResponse(BaseModel):
    """Phase 1 + 1.5 Optimization Response"""
    
    # Phase 1 fields
    work_order_id: str
    objectives: dict          # Optimization parameters
    stations: List[StationInfo]
    takt_time_ms: int        # Achieved takt
    bottleneck_station_id: str
    manpower_total: int      # Total manpower (online stations)
    line_count: int          # Number of stations
    utilization_avg: float   # Average utilization
    total_idle_time_ms: int  # Total idle time
    solve_time_sec: float    # Algorithm execution time
    algorithm_used: str      # Model used
    
    # Phase 1.5 NEW fields
    online_stations: int = 0              # Number of online stations
    offline_tasks_count: int = 0          # Total offline tasks
    offline_total_time_ms: int = 0        # Total offline task time
    merged_tasks_count: int = 0           # Number of merged task pairs
    merge_efficiency_gain_pct: float = 0.0  # Actual efficiency gain achieved
```

### WorkstationSummary

```python
class WorkstationSummary(BaseModel):
    station_id: str
    load_ms: int
    utilization_pct: float
    workers: int
    task_count: int
```

### TaktSummary

```python
class TaktSummary(BaseModel):
    work_order_id: str
    theoretical_min_takt: int
    achieved_takt: int
    bottleneck_station: str
    efficiency_pct: float
```

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Error description message"
}
```

### HTTP Status Codes

| Code | Meaning               | Common Scenarios                              |
| ---- | --------------------- | --------------------------------------------- |
| 200  | Success               | Request processed successfully                |
| 400  | Bad Request           | Invalid `work_order_id`, parameter type error |
| 404  | Not Found             | Dashboard file missing                        |
| 500  | Internal Server Error | Algorithm timeout, execution failure          |

### Common Error Messages

1. **"Parameter error: Invalid work_order_id"**
   - Cause: `work_order_id` not in `WORK_ORDER_MAPPING`
   - Solution: Use `WO_A`, `WO_B`, or `WO_C`

2. **"Algorithm execution failed: Timeout"**
   - Cause: Algorithm execution exceeded 30 seconds
   - Solution: Reduce dataset size or optimize algorithm

3. **"Algorithm execution failed: File not found"**
   - Cause: CSV file path error in `WORK_ORDER_MAPPING`
   - Solution: Check file exists in `data/` directory

---

## Usage Examples

### Example 1: Minimize Workstation Count

**Request**:
```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "work_order_id": "WO_A",
    "optimization_goal": "min_stations",
    "target_takt": 30000
  }'
```

**Response**:
```json
{
  "work_order_id": "WO_A",
  "line_count": 2,
  "takt_time_ms": 29800,
  "manpower_total": 2,
  "utilization_avg": 97.17
}
```

---

### Example 2: Minimize Manpower

**Request**:
```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "work_order_id": "WO_B",
    "optimization_goal": "min_manpower",
    "target_takt": 25000,
    "max_workers_per_station": 2
  }'
```

**Response**:
```json
{
  "work_order_id": "WO_B",
  "manpower_total": 3,
  "line_count": 2,
  "takt_time_ms": 24800
}
```

---

### Example 3: Minimize Idle Time

**Request**:
```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "work_order_id": "WO_C",
    "optimization_goal": "min_idle",
    "target_takt": 28000,
    "fixed_stations": 3
  }'
```

**Response**:
```json
{
  "work_order_id": "WO_C",
  "line_count": 3,
  "total_idle_time_ms": 450,
  "utilization_avg": 98.5
}
```

---

### Example 4: Query Workstation Status

**Request**:
```bash
curl "http://localhost:8000/workstations?work_order_id=WO_A&target_takt=30000"
```

**Response**:
```json
[
  {
    "station_id": "WS-001",
    "load_ms": 28500,
    "utilization_pct": 95.0,
    "workers": 1,
    "task_count": 3
  }
]
```

---

### Example 5: Health Check

**Request**:
```bash
curl http://localhost:8000/health
```

**Response**:
```json
{
  "status": "healthy",
  "version": "1.0.0-phase1",
  "algo_available": true
}
```

---

## Testing Recommendations

### Functional Testing

1. **Valid Input Test**
   ```python
   def test_valid_optimization():
       response = client.post("/optimize", json={
           "work_order_id": "WO_A",
           "optimization_goal": "min_stations",
           "target_takt": 30000
       })
       assert response.status_code == 200
       assert response.json()["line_count"] >= 1
   ```

2. **Invalid Parameter Test**
   ```python
   def test_invalid_work_order():
       response = client.post("/optimize", json={
           "work_order_id": "INVALID_WO",
           "optimization_goal": "min_stations",
           "target_takt": 30000
       })
       assert response.status_code == 400
   ```

### Performance Testing

```bash
# Use Apache Bench for load testing
ab -n 100 -c 10 -p request.json -T application/json \
   http://localhost:8000/optimize
```

**Acceptance Criteria**:
- 95th percentile latency < 3 seconds
- Error rate < 1%

---

## Appendix

### A. Work Order Mapping Table

| `work_order_id` | `tasks_csv`      | `precedences_csv`      | `config_csv`      |
| --------------- | ---------------- | ---------------------- | ----------------- |
| `WO_A`          | `test_tasks.csv` | `test_precedences.csv` | `test_config.csv` |
| `WO_B`          | `test_tasks.csv` | `test_precedences.csv` | -                 |
| `WO_C`          | `test_tasks.csv` | -                      | `test_config.csv` |

### B. Algorithm Invocation Example

```bash
python3 sche-algo.py \
  --tasks_csv data/test_tasks.csv \
  --precedences_csv data/test_precedences.csv \
  --config_csv data/test_config.csv \
  --objective min_stations \
  --json_output /tmp/result.json \
  --csv_output /tmp/result.csv \
  --kpi_csv /tmp/kpi.csv \
  --station_csv /tmp/station.csv \
  --model boolean
```

### C. Swagger UI Access

After starting the service, visit:
```
http://localhost:8000/api/docs
```

Features:
- Interactive API testing
- Auto-generated request examples
- Schema validation

---
