# Phase 1 Quick Start Guide

This guide helps you start and test the Line Balance System Phase 1 MVP in 5 minutes.

---

## 📋 Prerequisites

- Python 3.10+ installed
- Git installed (if cloning the project)
- Command-line terminal (Linux/Mac: Terminal, Windows: PowerShell/WSL)
- 8GB+ RAM (recommended)

---

## 🚀 Quick Start (3 Steps)

### Step 1: Install Dependencies

```bash
# Navigate to project directory
cd /mnt/d/workspace/line-balance

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or .\venv\Scripts\activate  # Windows PowerShell

# Install packages
pip install -r requirements.txt
```

**Expected output:**
```
Successfully installed fastapi-0.104.0 uvicorn-0.24.0 ortools-9.7.0 ...
```

---

### Step 2: Start API Service

```bash
# Run API server
python3 src/api_server.py
```

**Expected output:**
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

✅ **Service is running!** Keep this terminal window open.

---

### Step 3: Open Frontend Interface

**Option 1: Browser**

Open browser and visit: **http://localhost:8000**

**Option 2: Test API with curl**

Open a new terminal and run:

```bash
curl "http://localhost:8000/health"
```

**Expected output:**
```json
{
  "status": "healthy",
  "version": "1.0.0-phase1",
  "algo_available": true,
  "data_dir": "/mnt/d/workspace/line-balance/data",
  "available_work_orders": ["WO_A", "WO_B", "WO_C"]
}
```

---

## 🎯 Run Your First Optimization

### Using Frontend Interface

1. Open http://localhost:8000
2. Select work order: **WO_A**
3. Adjust takt time: **80000 ms** (use slider)
4. Select objective: **Minimize Stations**
5. Click **Run Optimization**
6. Wait 1-3 seconds, view results

**Expected results:**
- KPI cards display: takt time, manpower, station count, utilization
- Chart shows workstation load distribution

---

### Using API Test

```bash
curl -X POST "http://localhost:8000/optimize" \
  -H "Content-Type: application/json" \
  -d '{
    "work_order_id": "WO_A",
    "target_takt": 80000,
    "optimization_goal": "min_stations"
  }'
```

**Expected output example:**
```json
{
  "work_order_id": "WO_A",
  "line_count": 2,
  "manpower_total": 2,
  "takt_time_ms": 80000,
  "utilization_avg": 97.02,
  "bottleneck_station_id": "WS-002",
  "solve_time_sec": 1.234,
  ...
}
```

---

## ✅ Verify Installation

Run automatic verification script:

```bash
python3 << 'EOF'
import requests
import sys

print("🔍 Starting installation verification...")

# 1. Health check
try:
    r = requests.get("http://localhost:8000/health", timeout=5)
    assert r.status_code == 200
    print("✓ Health check passed")
except Exception as e:
    print(f"✗ Health check failed: {e}")
    sys.exit(1)

# 2. API functionality test
try:
    r = requests.post("http://localhost:8000/optimize", json={
        "work_order_id": "WO_A",
        "target_takt": 80000,
        "optimization_goal": "min_stations"
    }, timeout=10)
    assert r.status_code == 200
    data = r.json()
    assert data["line_count"] > 0
    print(f"✓ API test passed (stations: {data['line_count']})")
except Exception as e:
    print(f"✗ API test failed: {e}")
    sys.exit(1)

# 3. Performance test
try:
    assert data["solve_time_sec"] < 5.0
    print(f"✓ Performance test passed (solve time: {data['solve_time_sec']:.2f}s)")
except Exception as e:
    print(f"⚠ Performance warning: solve time {data['solve_time_sec']:.2f}s exceeds 5 seconds")

print("\n🎉 All verifications passed! System is ready.")
EOF
```

**Expected output:**
```
🔍 Starting installation verification...
✓ Health check passed
✓ API test passed (stations: 2)
✓ Performance test passed (solve time: 1.23s)

🎉 All verifications passed! System is ready.
```

---

## 🐛 Troubleshooting

### Issue 1: `ModuleNotFoundError: No module named 'fastapi'`

**Cause:** Dependencies not installed

**Solution:**
```bash
pip install -r requirements.txt
```

---

### Issue 2: `Address already in use (port 8000)`

**Cause:** Port already occupied

**Solution A: Kill the occupying process**
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows PowerShell
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Solution B: Use a different port**
```bash
uvicorn src.api_server:app --host 0.0.0.0 --port 8080
```

---

### Issue 3: API returns 500 error

**Checklist:**

1. Do CSV files exist?
   ```bash
   ls data/test_tasks.csv
   ```

2. Test algorithm directly:
   ```bash
   python3 src/sche-algo.py \
     --tasks_csv data/test_tasks.csv \
     --objective min_stations \
     --json_output /tmp/test.json
   ```

3. View detailed error:
   ```bash
   # Restart service and check logs
   python3 src/api_server.py
   ```

---

### Issue 4: Frontend cannot connect to API

**Symptom:** "Optimization failed" appears after clicking button

**Solution:**

1. Confirm API service is running:
   ```bash
   curl http://localhost:8000/health
   ```

2. Ensure browser accesses `http://localhost:8000` (not `file://`)

3. Check browser Console (F12) for error messages

---

## 📚 Next Steps

### Explore More Features

1. **Try different work orders:**
   - WO_A: Simple test (1200s)
   - WO_B: Medium work order (3400s)
   - WO_C: Large work order (8000s)

2. **Test different objectives:**
   - Minimize stations (min_stations)
   - Minimize manpower (min_manpower)
   - Minimize idle time (min_idle)

3. **Adjust parameters:**
   - Try different takt times (40000 ~ 200000 ms)
   - Adjust max workers per station

### Consult Documentation

- **API Specification:** `docs/PHASE1_API_SPEC.md`
- **Implementation Guide:** `docs/PHASE1_IMPLEMENTATION.md`
- **Stage Specifications:** `docs/stage-specs.md`
- **Feasibility Assessment:** `docs/feasibility-assessment.md`

### Interactive API Documentation

Visit **http://localhost:8000/api/docs** to view Swagger UI

---

## 🔄 Stop Service

Press `Ctrl+C` in the terminal running the API

```bash
# Deactivate virtual environment (optional)
deactivate
```

---

## 🐳 Docker Quick Start (Optional)

### Using Docker Compose

```bash
# Build and start
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop service
docker-compose down
```

Service will run at **http://localhost:8000**

---

## 📞 Get Help

- **View logs:** Output in API service terminal window
- **Check /health endpoint:** `curl http://localhost:8000/health`
- **Reference documentation:** `docs/` directory
- **Test examples:** `docs/PHASE1_API_SPEC.md`

---

**Maintainer:** JASON YY, LIN  
**Version:** 1.0.0-phase1  
**Last Updated:** 2025-11-06
