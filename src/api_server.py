#!/usr/bin/env python3
"""
Line Balance System - Phase 1 MVP API Server

Provides core optimization endpoints: /optimize, /workstations, /takt-summary
Reference documents: docs/stage-specs.md, docs/feasibility-assessment.md
"""

import json
import os
import subprocess
import tempfile
import time
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Optional, Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field, validator

# ============================================================================
# Configuration
# ============================================================================

WORKSPACE_ROOT = Path(__file__).parent.parent
DATA_DIR = WORKSPACE_ROOT / "data"
ALGO_SCRIPT = WORKSPACE_ROOT / "src" / "sche-algo.py"

# Work Order to CSV mapping (simulation data mapping)
WORK_ORDER_MAPPING = {
    "WO_A": {
        "tasks_csv": "test_tasks.csv",
        "precedences_csv": "test_precedences.csv",
        "config_csv": "test_config.csv",
        "description": "Simple test work order (1200s total time)"
    },
    "WO_B": {
        "tasks_csv": "test_tasks.csv",  # Temporarily shared
        "precedences_csv": "test_precedences.csv",
        "config_csv": "test_config.csv",
        "description": "Medium work order (3400s total time)"
    },
    "WO_C": {
        "tasks_csv": "test_tasks.csv",  # Temporarily shared
        "precedences_csv": "test_precedences.csv",
        "config_csv": "test_config.csv",
        "description": "Large work order (8000s total time)"
    }
}

# ============================================================================
# Pydantic Models (compliant with feasibility-assessment.md Appendix A)
# ============================================================================

class OptimizeRequest(BaseModel):
    """Optimization request model"""
    work_order_id: str = Field(..., description="Work order ID (WO_A, WO_B, WO_C)")
    target_takt: int = Field(..., gt=0, description="Target takt time (milliseconds)")
    optimization_goal: str = Field(
        "min_stations",
        description="Optimization objective: min_stations | min_manpower | min_idle"
    )
    max_workers_per_station: int = Field(8, ge=1, le=20, description="Maximum workers per station")
    fixed_stations: int = Field(0, ge=0, description="Fixed number of stations (for min_idle only)")
    
    @validator('optimization_goal')
    def validate_goal(cls, v):
        allowed = ['min_stations', 'min_manpower', 'min_idle']
        if v not in allowed:
            raise ValueError(f'optimization_goal must be one of {allowed}')
        return v
    
    @validator('work_order_id')
    def validate_work_order(cls, v):
        if v not in WORK_ORDER_MAPPING:
            raise ValueError(f'work_order_id must be one of {list(WORK_ORDER_MAPPING.keys())}')
        return v


class StationInfo(BaseModel):
    """Workstation information"""
    id: str = Field(..., description="Station ID (WS-001)")
    total_time_ms: int = Field(..., description="Total load time (milliseconds)")
    idle_time_ms: int = Field(0, description="Idle time relative to bottleneck")
    workers: int = Field(1, description="Number of assigned workers")
    utilization_pct: float = Field(..., description="Utilization rate (%)")
    assigned_tasks: List[int] = Field(default_factory=list, description="Assigned task IDs")


class OptimizeResponse(BaseModel):
    """Optimization response model (compliant with feasibility-assessment.md Appendix A)"""
    work_order_id: str
    objectives: Dict[str, Any] = Field(..., description="Optimization objectives and parameters")
    stations: List[StationInfo] = Field(..., description="Workstation configuration details")
    
    # KPIs (corresponding to dashboard.html KPI cards)
    takt_time_ms: int = Field(..., description="Achieved takt time (bottleneck station time)")
    bottleneck_station_id: str = Field(..., description="Bottleneck workstation ID")
    manpower_total: int = Field(..., description="Total manpower requirement")
    line_count: int = Field(..., description="Number of workstations")
    utilization_avg: float = Field(..., description="Average utilization rate (%)")
    total_idle_time_ms: int = Field(..., description="Total idle time")
    
    # Metadata
    solve_time_sec: float = Field(..., description="Solve time (seconds)")
    algorithm_used: str = Field(..., description="Algorithm used")


class WorkstationSummary(BaseModel):
    """Workstation summary (for /workstations API)"""
    station_id: str
    load_ms: int
    utilization_pct: float
    workers: int
    task_count: int


class TaktSummary(BaseModel):
    """Takt time summary (for /takt-summary API)"""
    work_order_id: str
    theoretical_min_takt: int
    achieved_takt: int
    bottleneck_station: str
    efficiency_pct: float


# ============================================================================
# FastAPI Application
# ============================================================================

app = FastAPI(
    title="Line Balance System API",
    description="Line Balance System - Phase 1 MVP (Reference: docs/stage-specs.md)",
    version="1.0.0-phase1",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# CORS configuration (development environment allows all origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Production should restrict to specific domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================================================================
# Helper Functions
# ============================================================================

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
    Execute sche-algo.py algorithm
    
    Reference: IO_SPECIFICATION_ZH.md usage examples
    """
    start_time = time.time()
    
    # Create temporary output files
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_json:
        json_output_path = tmp_json.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_csv:
        csv_output_path = tmp_csv.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_kpi:
        kpi_csv_path = tmp_kpi.name
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp_station:
        station_csv_path = tmp_station.name
    
    try:
        # Build command-line arguments
        cmd = [
            "python3", str(ALGO_SCRIPT),
            "--tasks_csv", str(DATA_DIR / tasks_csv),
            "--objective", objective,
            "--json_output", json_output_path,
            "--csv_output", csv_output_path,
            "--kpi_csv", kpi_csv_path,
            "--station_csv", station_csv_path,
            "--model", "boolean" if objective == "min_stations" else "boolean"  # Phase 1 uses boolean model
        ]
        
        # Add optional parameters
        if precedences_csv:
            cmd.extend(["--precedences_csv", str(DATA_DIR / precedences_csv)])
        
        if config_csv:
            cmd.extend(["--config_csv", str(DATA_DIR / config_csv)])
        
        if objective == "min_manpower":
            cmd.extend(["--target_takt", str(target_takt)])
            cmd.extend(["--max_workers_per_station", str(max_workers)])
        
        if objective == "min_idle" and fixed_stations > 0:
            cmd.extend(["--fixed_stations", str(fixed_stations)])
        
        # Execute algorithm
        print(f"[API] Executing command: {' '.join(cmd)}")
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30  # 30 second timeout (Phase 1 acceptance criteria: < 3 seconds)
        )
        
        if result.returncode != 0:
            raise RuntimeError(f"Algorithm execution failed:\n{result.stderr}")
        
        # Read JSON results
        with open(json_output_path, 'r', encoding='utf-8') as f:
            algo_result = json.load(f)
        
        solve_time = time.time() - start_time
        algo_result['solve_time_sec'] = solve_time
        
        print(f"[API] Algorithm completed, time: {solve_time:.2f} seconds")
        
        return algo_result
        
    except subprocess.TimeoutExpired:
        raise RuntimeError("Algorithm execution timeout (>30 seconds)")
    
    except Exception as e:
        raise RuntimeError(f"Algorithm execution error: {str(e)}")
    
    finally:
        # Clean up temporary files
        for tmp_file in [json_output_path, csv_output_path, kpi_csv_path, station_csv_path]:
            try:
                os.unlink(tmp_file)
            except:
                pass


def parse_algorithm_output(algo_result: Dict[str, Any], work_order_id: str) -> OptimizeResponse:
    """
    Convert algorithm output to API response format
    
    Corresponds to: KPI structure in feasibility-assessment.md Appendix A
    """
    kpis = algo_result.get('kpis', {})
    assignment = algo_result.get('assignment', {})
    
    # Parse stations information
    stations_data = kpis.get('stations', [])
    stations = []
    
    for station_info in stations_data:
        station_idx = station_info['station_index']
        load = station_info['load']
        idle = station_info['idle_vs_bottleneck']
        workers = station_info.get('workers', 1)
        
        # Calculate utilization
        takt = kpis.get('calculated_takt', load)
        util = (load / takt * 100) if takt > 0 else 0
        
        # Find tasks assigned to this station
        assigned_tasks = [
            int(task_id) for task_id, assigned_station in assignment.items()
            if assigned_station == station_idx
        ]
        
        stations.append(StationInfo(
            id=f"WS-{str(station_idx + 1).zfill(3)}",
            total_time_ms=load,
            idle_time_ms=idle,
            workers=workers,
            utilization_pct=round(util, 2),
            assigned_tasks=sorted(assigned_tasks)
        ))
    
    # Find bottleneck station
    bottleneck_idx = kpis.get('bottleneck_station', 0)
    bottleneck_id = f"WS-{str(bottleneck_idx + 1).zfill(3)}"
    
    # Calculate total manpower
    total_manpower = sum(s.workers for s in stations)
    
    return OptimizeResponse(
        work_order_id=work_order_id,
        objectives={
            "goal": algo_result.get('objective', 'min_stations'),
            "target_takt": algo_result.get('target_takt', 0),
            "model": algo_result.get('model', 'boolean')
        },
        stations=stations,
        takt_time_ms=kpis.get('calculated_takt', 0),
        bottleneck_station_id=bottleneck_id,
        manpower_total=total_manpower,
        line_count=len(stations),
        utilization_avg=round(kpis.get('avg_utilization_pct', 0.0), 2),
        total_idle_time_ms=kpis.get('total_idle', 0),
        solve_time_sec=algo_result.get('solve_time_sec', 0.0),
        algorithm_used=algo_result.get('model', 'boolean')
    )


# ============================================================================
# API Endpoints (compliant with stage-specs.md Phase 1)
# ============================================================================

@app.get("/", response_class=HTMLResponse)
async def serve_dashboard():
    """Serve frontend Dashboard HTML"""
    dashboard_path = Path(__file__).parent / "dashboard.html"
    
    if not dashboard_path.exists():
        raise HTTPException(status_code=404, detail="Dashboard not found")
    
    with open(dashboard_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    return HTMLResponse(content=html_content)


@app.post("/optimize", response_model=OptimizeResponse)
async def optimize_line_balance(request: OptimizeRequest):
    """
    Core optimization endpoint (Phase 1 core API)
    
    Reference documents:
    - docs/stage-specs.md Phase 1 scope
    - docs/feasibility-assessment.md Appendix A
    - IO_SPECIFICATION_ZH.md
    
    Acceptance criteria:
    - API Latency < 3 seconds (data volume <= 500 actions)
    - Correctness: deviation from manual calculation < ±5%
    """
    try:
        # Get CSV file paths for work order
        wo_config = WORK_ORDER_MAPPING[request.work_order_id]
        
        # Execute algorithm
        algo_result = run_optimization_algorithm(
            tasks_csv=wo_config["tasks_csv"],
            precedences_csv=wo_config.get("precedences_csv", ""),
            config_csv=wo_config.get("config_csv", ""),
            objective=request.optimization_goal,
            target_takt=request.target_takt,
            max_workers=request.max_workers_per_station,
            fixed_stations=request.fixed_stations
        )
        
        # Convert output format
        response = parse_algorithm_output(algo_result, request.work_order_id)
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Parameter error: {str(e)}")
    
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=f"Algorithm execution failed: {str(e)}")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")


@app.get("/workstations", response_model=List[WorkstationSummary])
async def get_workstations(
    work_order_id: str = Query(..., description="Work order ID"),
    target_takt: int = Query(..., description="Target takt time (milliseconds)")
):
    """
    Query workstation configuration summary (Phase 1 basic API)
    
    Simplified version: executes optimization then returns workstation summary
    """
    try:
        # Create optimization request
        request = OptimizeRequest(
            work_order_id=work_order_id,
            target_takt=target_takt,
            optimization_goal="min_stations"
        )
        
        # Execute optimization
        result = await optimize_line_balance(request)
        
        # Convert to summary format
        summaries = [
            WorkstationSummary(
                station_id=station.id,
                load_ms=station.total_time_ms,
                utilization_pct=station.utilization_pct,
                workers=station.workers,
                task_count=len(station.assigned_tasks)
            )
            for station in result.stations
        ]
        
        return summaries
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/takt-summary", response_model=TaktSummary)
async def get_takt_summary(
    work_order_id: str = Query(..., description="Work order ID"),
    target_takt: int = Query(..., description="Target takt time (milliseconds)")
):
    """
    Query takt time summary (Phase 1 basic API)
    """
    try:
        # Create optimization request
        request = OptimizeRequest(
            work_order_id=work_order_id,
            target_takt=target_takt,
            optimization_goal="min_stations"
        )
        
        # Execute optimization
        result = await optimize_line_balance(request)
        
        # Calculate efficiency
        efficiency = (target_takt / result.takt_time_ms * 100) if result.takt_time_ms > 0 else 0
        
        return TaktSummary(
            work_order_id=work_order_id,
            theoretical_min_takt=target_takt,
            achieved_takt=result.takt_time_ms,
            bottleneck_station=result.bottleneck_station_id,
            efficiency_pct=round(efficiency, 2)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": "1.0.0-phase1",
        "algo_available": ALGO_SCRIPT.exists(),
        "data_dir": str(DATA_DIR),
        "available_work_orders": list(WORK_ORDER_MAPPING.keys())
    }


# ============================================================================
# Application Startup
# ============================================================================

if __name__ == "__main__":
    import uvicorn
    
    print("=" * 80)
    print("Line Balance System API Service - Phase 1 MVP")
    print("=" * 80)
    print(f"Workspace: {WORKSPACE_ROOT}")
    print(f"Data directory: {DATA_DIR}")
    print(f"Algorithm: {ALGO_SCRIPT}")
    print(f"Available work orders: {list(WORK_ORDER_MAPPING.keys())}")
    print("=" * 80)
    print("Server running at http://localhost:8000")
    print("API documentation: http://localhost:8000/api/docs")
    print("=" * 80)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        access_log=True
    )
