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

| Technology    | Version | Purpose              | Rationale                    |
|---------------|---------|----------------------|------------------------------|
| HTML5         | -       | Page structure       | Standard, lightweight, no build |
| Tailwind CSS  | 3.x     | UI styling           | Rapid development, modern design |
| Chart.js      | 4.x     | Data visualization   | Easy to use, comprehensive docs |
| Vanilla JS    | ES6+    | Interactive logic    | No framework needed, reduced complexity |

### Backend Technologies

| Technology    | Version | Purpose              | Rationale                    |
|---------------|---------|----------------------|------------------------------|
| Python        | 3.10+   | Main language        | Rich ecosystem, OR-Tools support |
| FastAPI       | 0.104+  | Web framework        | High performance, auto docs, type safety |
| Uvicorn       | 0.24+   | ASGI server          | Asynchronous, high performance |
| Pydantic      | 2.0+    | Data validation      | Strong typing, automatic validation |

### Algorithm Technologies

| Technology    | Version | Purpose              | Rationale                    |
|---------------|---------|----------------------|------------------------------|
| OR-Tools      | 9.7+    | CP-SAT solver        | Google official, mature and stable |
| absl-py       | 2.0+    | Command-line args    | Good integration with OR-Tools |

### Deployment Technologies (Optional)

| Technology    | Version | Purpose              | Rationale                    |
|---------------|---------|----------------------|------------------------------|
| Docker        | 24+     | Containerization     | Environment consistency, easy deployment |
| Docker Compose| 2.x     | Multi-container orchestration | Simplified local dev environment |

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

## Next Steps (Phase 2 Preview)

After Phase 1 completion, the next phase will include:

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
**Last Updated:** 2025-11-06  
**Version:** 1.0.0-phase1
