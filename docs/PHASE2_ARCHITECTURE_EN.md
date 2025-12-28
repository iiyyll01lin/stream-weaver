# Phase 2 Architecture Design

**Document Version**: 2.0 | **Last Updated**: 2025-11-20  
**Related Documents**:
- [Phase 2 Implementation Guide](PHASE2_IMPLEMENTATION_EN.md)
- [Phase 2 API Specification](PHASE2_API_SPEC_EN.md)
- [Phase 1 Architecture](PHASE1_ARCHITECTURE_EN.md)
- [Database & API Design](DATABASE_API_DESIGN_SPEC_EN.md)

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [System Components](#system-components)
- [Multi-Line Optimization Architecture](#multi-line-optimization-architecture)
- [Layout Management Architecture](#layout-management-architecture)
- [Fishbone Diagram Generator](#fishbone-diagram-generator)
- [Cross-Line Task Benchmark Architecture](#cross-line-task-benchmark-architecture)
- [Technology Stack](#technology-stack)
- [Data Flow](#data-flow)
- [Database Schema](#database-schema)
- [Performance Optimization](#performance-optimization)

---

## Architecture Overview

### Design Principles

Phase 2 extends the four-tier architecture with advanced manufacturing capabilities:

1. **Presentation Layer** (Frontend)
   - Technology: HTML5 + Tailwind CSS + Chart.js + **Canvas API**
   - New Features: 2D layout editor, fishbone diagram viewer
   - Responsibility: User interaction, advanced visualization

2. **Service Layer** (Backend API)
   - Technology: FastAPI + Pydantic + **PostgreSQL** + **JWT Auth**
   - New Features: Multi-line endpoints, layout management, product config
   - Responsibility: Request validation, business logic, data persistence

3. **Data Layer** (Enhanced Persistence)
   - Technology: PostgreSQL + **Layout Tables** + **Product Configs** + Redis Cache
   - New Features: 2D spatial data, CTO/BTO mappings, version control
   - Responsibility: Complex data relationships, layout storage, configuration management

4. **Algorithm Layer** (Advanced Optimization Engine)
   - Technology: Google OR-Tools (CP-SAT Solver) + **NetworkX**
   - New Features: Multi-line model, fishbone graph generator, line type recommender
   - Responsibility: Advanced optimization, graph generation

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend Layer                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  dashboard.html (Enhanced UI)                         │  │
│  │  - Multi-line Optimization Panel                      │  │
│  │  - 2D Layout Editor (Canvas API)                      │  │
│  │  - Fishbone Diagram Viewer                            │  │
│  │  - Product Configuration Manager                      │  │
│  │  - Cross-Line Task Benchmark Dashboard                │  │
│  └─────────────────────┬───────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────┘
                         │ HTTP POST/GET
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                   Backend API Layer                         │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  api_server.py (Extended FastAPI Application)         │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Phase 2 NEW Endpoints                          │  │  │
│  │  │  - POST /optimize (multi-line support)          │  │  │
│  │  │  - GET  /recommend-line-type                    │  │  │
│  │  │  - GET  /fishbone-diagram                       │  │  │
│  │  │  - GET  /layout                                 │  │  │
│  │  │  - POST /save-layout                            │  │  │
│  │  │  - GET  /load-layout                            │  │  │
│  │  │  - GET  /product-config                         │  │  │
│  │  │  - GET  /benchmark/cross-line-tasks             │  │  │
│  │  │  - POST /benchmark/cross-line-tasks/generate    │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  │                    │                                   │  │
│  │  ┌─────────────────▼───────────────────────────────┐  │  │
│  │  │  Database Access Layer (ENHANCED)               │  │  │
│  │  │  - Layout Storage (PostgreSQL)                  │  │  │
│  │  │  - Product Config (CTO/BTO)                     │  │  │
│  │  │  - Multi-line Optimization History              │  │  │
│  │  │  - Version Control & Configuration Management   │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  └────────────────────┼───────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────┘
                         │ SQL queries / subprocess.run()
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                Data Layer (ENHANCED)                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  PostgreSQL Database                                  │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Phase 2 Extended Tables                        │  │  │
│  │  │  - layouts (spatial data, stations, connections)│  │  │
│  │  │  - layout_stations (positioning, dimensions)    │  │  │
│  │  │  - layout_connections (conveyors, AGVs)         │  │  │
│  │  │  - product_configs (CTO/BTO mappings)           │  │  │
│  │  │  - task_execution_records (benchmark data)      │  │  │
│  │  │  - benchmark_reports (analysis results)         │  │  │
│  │  │  - configurations (version control)             │  │  │
│  │  │  + All Phase 1 tables (extended)                │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  │                    │                                   │  │
│  │  ┌─────────────────▼───────────────────────────────┐  │  │
│  │  │  Redis Cache (ENHANCED)                         │  │  │
│  │  │  - Layout data (24hr TTL)                       │  │  │
│  │  │  - Multi-line optimization results (2hr TTL)    │  │  │
│  │  │  - Fishbone diagram cache (1hr TTL)             │  │  │
│  │  │  - Product config cache (1 week TTL)            │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  └────────────────────┼───────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────┘
                         │ CSV generation / Multi-line models
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  Algorithm Layer                            │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  sche-algo-v2.py (Multi-Line Solver)                  │  │
│  │  ┌─────────────────────────────────────────────────┐  │  │
│  │  │  Multi-Line Model                               │  │  │
│  │  │  - Line assignment variables                    │  │  │
│  │  │  - Cross-line balancing constraints             │  │  │
│  │  │  - Line type recommendation logic               │  │  │
│  │  └─────────────────┬───────────────────────────────┘  │  │
│  │                    │                                   │  │
│  │  ┌─────────────────▼───────────────────────────────┐  │  │
│  │  │  fishbone-generator.py (NEW)                    │  │  │
│  │  │  - Task precedence graph (NetworkX)             │  │  │
│  │  │  - SVG/PNG export                               │  │  │
│  │  │  - Interactive diagram generation               │  │  │
│  │  └─────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

---

## System Components

### 1. Frontend Component (Enhanced `dashboard.html`)

**Phase 2 Additions**:

#### 1.1 Multi-Line Optimization Panel
```html
<div id="multi-line-panel">
  <h3>Multi-Line Configuration</h3>
  <div>
    <label>Number of Lines:</label>
    <input type="number" id="num-lines" min="1" max="5" value="1">
  </div>
  <div id="line-configs">
    <!-- Dynamically generated line configs -->
    <div class="line-config">
      <label>Line A Target Takt:</label>
      <input type="number" id="line-a-takt" value="30000">
    </div>
    <div class="line-config">
      <label>Line B Target Takt:</label>
      <input type="number" id="line-b-takt" value="25000">
    </div>
  </div>
</div>
```

#### 1.2 Layout Editor (Canvas-based)
```javascript
class LayoutEditor {
  constructor(canvasId) {
    this.canvas = document.getElementById(canvasId);
    this.ctx = this.canvas.getContext('2d');
    this.stations = [];
    this.connections = [];
  }

  addStation(x, y, stationId) {
    this.stations.push({ x, y, id: stationId });
    this.render();
  }

  addConnection(fromId, toId) {
    this.connections.push({ from: fromId, to: toId });
    this.render();
  }

  exportLayout() {
    return {
      stations: this.stations,
      connections: this.connections
    };
  }

  importLayout(layoutData) {
    this.stations = layoutData.stations;
    this.connections = layoutData.connections;
    this.render();
  }
}
```

#### 1.3 Fishbone Diagram Viewer
```javascript
async function displayFishboneDiagram(workOrderId) {
  const response = await fetch(`/fishbone-diagram?work_order_id=${workOrderId}`);
  const svgData = await response.text();
  
  document.getElementById('fishbone-container').innerHTML = svgData;
}
```

**Technology Choices**:

| Technology        | Purpose                    | Reason for Selection                     |
|-------------------|----------------------------|------------------------------------------|
| Canvas API        | 2D layout editor           | Native browser support, high performance |
| SVG               | Fishbone diagram rendering | Scalable, exportable, interactive        |
| Fetch API (async) | Multi-endpoint calls       | Concurrent requests for multi-line data  |

---

### 2. Backend API Component (Extended `api_server.py`)

**Phase 2 Additions**:

#### 2.1 Multi-Line Configuration Management
```python
class MultiLineRequest(BaseModel):
    """Multi-line optimization request"""
    work_order_id: str
    optimization_goal: str
    lines: List[LineConfig]  # NEW: List of line configurations
    enable_cross_line_balancing: bool = True
    
class LineConfig(BaseModel):
    """Individual line configuration"""
    line_id: str  # A, B, C, etc.
    target_takt: int
    max_workers_per_station: int = 3
    task_filter: Optional[List[str]] = None  # Filter tasks for this line
```

#### 2.2 Layout Management Endpoints
```python
@app.post("/save-layout")
async def save_layout(layout: LayoutData):
    """Save layout to database"""
    layout_id = db.insert_layout(
        name=layout.name,
        data_json=json.dumps(layout.to_dict()),
        created_at=datetime.now()
    )
    return {"layout_id": layout_id, "status": "saved"}

@app.get("/load-layout")
async def load_layout(layout_id: int):
    """Load layout from database"""
    layout_data = db.get_layout(layout_id)
    return LayoutData.from_dict(json.loads(layout_data['data_json']))

@app.get("/layout")
async def list_layouts():
    """List all saved layouts"""
    return db.get_all_layouts()
```

#### 2.3 Product Configuration Endpoints
```python
@app.get("/product-config")
async def get_product_config(sku: Optional[str] = None):
    """Retrieve CTO/BTO mapping"""
    if sku:
        return db.get_product_config_by_sku(sku)
    else:
        return db.get_all_product_configs()

@app.post("/product-config")
async def create_product_config(config: ProductConfig):
    """Create/update product configuration"""
    config_id = db.upsert_product_config(config)
    return {"config_id": config_id, "status": "saved"}
```

#### 2.4 Fishbone Diagram Endpoint
```python
@app.get("/fishbone-diagram")
async def generate_fishbone(
    work_order_id: str,
    format: str = "svg"  # svg or png
):
    """Generate fishbone diagram"""
    result = subprocess.run(
        [
            "python3", "src/fishbone_generator.py",
            "--work_order_id", work_order_id,
            "--format", format,
            "--output", f"/tmp/fishbone_{work_order_id}.{format}"
        ],
        capture_output=True,
        timeout=10
    )
    
    with open(f"/tmp/fishbone_{work_order_id}.{format}", "rb") as f:
        diagram_data = f.read()
    
    if format == "svg":
        return Response(content=diagram_data, media_type="image/svg+xml")
    else:
        return Response(content=diagram_data, media_type="image/png")
```

#### 2.5 Line Type Recommendation Endpoint
```python
from dataclasses import dataclass
from typing import Optional, List, Dict, Any
import math

# Configurable thresholds (can be overridden via config)
LINE_TYPE_THRESHOLDS = {
    "cell": {"max_stations": 3, "max_tasks": 20, "max_demand": 50},
    "short_line": {"max_stations": 8, "max_tasks": 50, "max_demand": 200},
    "long_line": {"min_stations": 9, "min_tasks": 50, "min_demand": 200}
}

@dataclass
class LineTypeRecommendationRequest:
    work_order_id: str
    target_takt: int
    max_workers_available: int = 10
    optimization_goal: str = "min_stations"  # NEW
    daily_demand: Optional[int] = None       # NEW
    product_mix_count: Optional[int] = None  # NEW
    changeover_time_ms: Optional[int] = None # NEW

@app.get("/recommend-line-type")
async def recommend_line_type(
    work_order_id: str,
    target_takt: int,
    max_workers_available: int = 10,
    optimization_goal: str = "min_stations",
    daily_demand: Optional[int] = None,
    product_mix_count: Optional[int] = None,
    changeover_time_ms: Optional[int] = None
):
    """
    Recommend optimal line type with enhanced analysis.
    
    NEW Input Parameters:
    - optimization_goal: Affects line type preference
    - daily_demand: High demand favors long_line
    - product_mix_count: High mix favors cell
    - changeover_time_ms: High changeover favors cell
    """
    # Load task data
    tasks_df = pd.read_csv(get_work_order_tasks(work_order_id))
    
    # Calculate core metrics
    total_work = tasks_df['duration'].sum()
    task_count = len(tasks_df)
    complexity_dist = tasks_df['complexity_level'].value_counts().to_dict()
    
    # NEW: Calculate theoretical minimum stations
    theoretical_min_stations = math.ceil(total_work / target_takt)
    
    # NEW: Enhanced recommendation logic with multiple factors
    scores = calculate_line_type_scores(
        task_count=task_count,
        theoretical_min_stations=theoretical_min_stations,
        daily_demand=daily_demand,
        product_mix_count=product_mix_count,
        optimization_goal=optimization_goal,
        complexity_dist=complexity_dist
    )
    
    # Determine recommendation and feasibility
    recommendation = max(scores, key=lambda x: scores[x]["score"])
    confidence = scores[recommendation]["score"]
    
    # NEW: Build decision factors (human-readable explanations)
    decision_factors = build_decision_factors(
        task_count, theoretical_min_stations, daily_demand, 
        product_mix_count, recommendation
    )
    
    # NEW: Calculate manpower estimates per line type
    manpower_estimates = {
        "cell": estimate_workers("cell", theoretical_min_stations) if scores["cell"]["feasible"] else None,
        "short_line": estimate_workers("short_line", theoretical_min_stations) if scores["short_line"]["feasible"] else None,
        "long_line": estimate_workers("long_line", theoretical_min_stations) if scores["long_line"]["feasible"] else None
    }
    
    # NEW: Generate warnings for potential issues
    warnings = generate_warnings(
        tasks_df, theoretical_min_stations, target_takt, 
        complexity_dist, recommendation
    )
    
    return {
        "work_order_id": work_order_id,
        "recommended_type": recommendation,
        "confidence": round(confidence, 2),
        "reasoning": {
            "task_count": task_count,
            "total_work_ms": total_work,
            "target_takt_ms": target_takt,
            "theoretical_min_stations": theoretical_min_stations,  # NEW
            "recommended_stations": theoretical_min_stations,
            "complexity_distribution": complexity_dist,
            "decision_factors": decision_factors  # NEW
        },
        "alternatives": [
            {
                "type": line_type,
                "feasible": data["feasible"],           # NEW
                "suitability": round(data["score"], 2),
                "reason": data["reason"],
                "estimated_workers": manpower_estimates.get(line_type),  # NEW
                "estimated_efficiency": data.get("efficiency")           # NEW
            }
            for line_type, data in scores.items()
        ],
        "manpower_estimates": manpower_estimates,  # NEW
        "warnings": warnings,                      # NEW
        "recommendations": generate_recommendations(
            recommendation, tasks_df, complexity_dist
        )
    }

def calculate_line_type_scores(
    task_count: int,
    theoretical_min_stations: int,
    daily_demand: Optional[int],
    product_mix_count: Optional[int],
    optimization_goal: str,
    complexity_dist: Dict[str, int]
) -> Dict[str, Dict[str, Any]]:
    """
    Calculate suitability scores for each line type.
    
    Factors considered:
    1. Task count alignment with line type range
    2. Theoretical stations vs line type station range
    3. Daily demand matching
    4. Product mix (high mix favors cell)
    5. Optimization goal preference
    """
    scores = {}
    
    for line_type in ["cell", "short_line", "long_line"]:
        score = 0.5  # Base score
        feasible = True
        reasons = []
        
        # Factor 1: Station count alignment
        if line_type == "cell":
            if theoretical_min_stations <= 3:
                score += 0.3
                reasons.append("Station count fits cell range (1-3)")
            else:
                feasible = False
                reasons.append(f"Would require {theoretical_min_stations} stations; exceeds cell max (3)")
        elif line_type == "short_line":
            if 4 <= theoretical_min_stations <= 8:
                score += 0.3
                reasons.append("Station count optimal for short_line (4-8)")
            elif theoretical_min_stations < 4:
                score += 0.1
                reasons.append("Could work but underutilizes short_line capacity")
            elif theoretical_min_stations > 8:
                score -= 0.1
                reasons.append("Station count exceeds short_line typical range")
        else:  # long_line
            if theoretical_min_stations >= 9:
                score += 0.3
                reasons.append("Station count matches long_line range (9+)")
            else:
                score -= 0.2
                reasons.append("Overkill for current station requirement")
        
        # Factor 2: Task count alignment
        if line_type == "cell" and task_count < 20:
            score += 0.1
        elif line_type == "short_line" and 20 <= task_count <= 50:
            score += 0.1
        elif line_type == "long_line" and task_count > 50:
            score += 0.1
        
        # Factor 3: Daily demand (NEW)
        if daily_demand:
            if line_type == "cell" and daily_demand < 50:
                score += 0.15
                reasons.append(f"Low demand ({daily_demand}/day) suits cell flexibility")
            elif line_type == "short_line" and 50 <= daily_demand <= 200:
                score += 0.15
                reasons.append(f"Demand ({daily_demand}/day) matches short_line capacity")
            elif line_type == "long_line" and daily_demand > 200:
                score += 0.15
                reasons.append(f"High demand ({daily_demand}/day) justifies long_line")
        
        # Factor 4: Product mix (NEW)
        if product_mix_count:
            if line_type == "cell" and product_mix_count > 10:
                score += 0.1
                reasons.append("High product mix benefits from cell flexibility")
            elif line_type == "long_line" and product_mix_count <= 3:
                score += 0.1
                reasons.append("Low product mix enables long_line specialization")
        
        # Factor 5: Optimization goal preference (NEW)
        if optimization_goal == "min_stations" and line_type == "cell":
            score += 0.05
        elif optimization_goal == "min_manpower" and line_type == "long_line":
            score += 0.05  # Specialized workers = fewer total
        elif optimization_goal == "min_idle" and line_type == "short_line":
            score += 0.05  # Balanced workload
        
        # Estimate efficiency
        if feasible:
            efficiency = 0.7 + (score - 0.5) * 0.3  # Scale to 0.55-0.85 range
        else:
            efficiency = None
        
        scores[line_type] = {
            "score": min(score, 1.0),
            "feasible": feasible,
            "reason": reasons[0] if reasons else "Standard fit",
            "efficiency": round(efficiency, 2) if efficiency else None
        }
    
    return scores

def generate_warnings(
    tasks_df: pd.DataFrame,
    theoretical_min_stations: int,
    target_takt: int,
    complexity_dist: Dict[str, int],
    recommendation: str
) -> List[str]:
    """Generate warnings for potential issues."""
    warnings = []
    
    # Check for complex task concentration
    complex_count = complexity_dist.get("complex", 0) + complexity_dist.get("super_complex", 0)
    if complex_count > theoretical_min_stations:
        warnings.append(
            f"{complex_count} complex tasks may create bottleneck at single station"
        )
    
    # Check for tasks exceeding takt
    over_takt = tasks_df[tasks_df['duration'] > target_takt]
    if len(over_takt) > 0:
        warnings.append(
            f"{len(over_takt)} task(s) exceed target takt - may need splitting"
        )
    
    # Check for offline task ratio
    if 'offline_flag' in tasks_df.columns:
        offline_count = tasks_df['offline_flag'].sum()
        if offline_count > len(tasks_df) * 0.3:
            warnings.append(
                f"High offline task ratio ({offline_count}/{len(tasks_df)}) - consider parallel processing"
            )
    
    return warnings

def estimate_workers(line_type: str, theoretical_min_stations: int) -> int:
    """Estimate worker count based on line type and stations."""
    if line_type == "cell":
        return theoretical_min_stations  # 1 worker per station, flexible
    elif line_type == "short_line":
        return theoretical_min_stations  # Dedicated workers
    else:  # long_line
        return int(theoretical_min_stations * 1.2)  # Specialized + backup

def build_decision_factors(
    task_count: int, 
    theoretical_min_stations: int,
    daily_demand: Optional[int],
    product_mix_count: Optional[int],
    recommendation: str
) -> List[str]:
    """Build human-readable decision factors."""
    factors = []
    
    thresholds = LINE_TYPE_THRESHOLDS[recommendation]
    
    if recommendation == "cell":
        factors.append(f"Task count ({task_count}) fits cell range (<20)")
        factors.append(f"Theoretical {theoretical_min_stations} stations within cell max (3)")
    elif recommendation == "short_line":
        factors.append(f"Task count ({task_count}) fits short_line range (20-50)")
        factors.append(f"Theoretical {theoretical_min_stations} stations within short_line definition (4-8)")
    else:
        factors.append(f"Task count ({task_count}) requires long_line (>50 tasks)")
        factors.append(f"Theoretical {theoretical_min_stations} stations matches long_line (9+)")
    
    if daily_demand:
        factors.append(f"Daily demand ({daily_demand}) matches {recommendation} capacity")
    
    if product_mix_count:
        mix_level = "high" if product_mix_count > 10 else "low"
        factors.append(f"{mix_level.capitalize()} product mix ({product_mix_count} SKUs)")
    
    return factors


def validate_constraints(
    theoretical_min_stations: int,
    available_space_sqm: Optional[float],
    multi_skill_worker_count: Optional[int],
    quality_target_dppm: Optional[int],
    is_new_product: bool = False
) -> Dict[str, Dict[str, bool]]:
    """
    Validate physical and operational constraints for each line type.
    
    Returns:
        {
            "space_sufficient": {"cell": True, "short_line": True, "long_line": False},
            "workers_qualified": {"cell": False, "short_line": True, "long_line": True},
            "quality_achievable": {"cell": True, "short_line": True, "long_line": False}
        }
    """
    # Space requirements (m²)
    SPACE_REQUIREMENTS = {
        "cell": 50 * 3,        # ~150 m² max for 3 stations
        "short_line": 50 * 8,  # ~400 m² max for 8 stations
        "long_line": 50 * 15   # ~750 m² for large lines
    }
    
    # Multi-skill requirements (minimum flexible workers needed)
    SKILL_REQUIREMENTS = {
        "cell": theoretical_min_stations,  # All workers must be multi-skilled
        "short_line": max(1, theoretical_min_stations // 3),  # Some flexibility needed
        "long_line": 0  # Single-skill specialists OK
    }
    
    # Quality handoff penalty (more stations = more handoffs = more defects)
    QUALITY_HANDOFF_FACTOR = {
        "cell": 1.0,       # Baseline
        "short_line": 1.5, # 50% more defect risk
        "long_line": 2.5   # 150% more defect risk
    }
    
    constraints = {
        "space_sufficient": {},
        "workers_qualified": {},
        "quality_achievable": {},
        "npi_suitable": {}
    }
    
    for line_type in ["cell", "short_line", "long_line"]:
        # Space check
        if available_space_sqm:
            constraints["space_sufficient"][line_type] = (
                available_space_sqm >= SPACE_REQUIREMENTS[line_type]
            )
        else:
            constraints["space_sufficient"][line_type] = True  # Assume OK if not specified
        
        # Worker skill check
        if multi_skill_worker_count is not None:
            constraints["workers_qualified"][line_type] = (
                multi_skill_worker_count >= SKILL_REQUIREMENTS[line_type]
            )
        else:
            constraints["workers_qualified"][line_type] = True  # Assume OK if not specified
        
        # Quality check
        if quality_target_dppm:
            # Stricter quality target requires fewer handoffs
            max_acceptable_dppm = quality_target_dppm * QUALITY_HANDOFF_FACTOR[line_type]
            constraints["quality_achievable"][line_type] = (
                quality_target_dppm >= 100 or line_type == "cell"  # Only cell for <100 DPPM
            )
        else:
            constraints["quality_achievable"][line_type] = True
        
        # NPI suitability (new product introduction)
        if is_new_product:
            constraints["npi_suitable"][line_type] = (line_type == "cell")
        else:
            constraints["npi_suitable"][line_type] = True
    
    return constraints


def calculate_cost_analysis(
    theoretical_min_stations: int,
    daily_demand: int = 100,
    labor_rate_per_hour: float = 25.0,
    overhead_rate_pct: float = 0.25
) -> Dict[str, Dict[str, float]]:
    """
    Calculate operating cost comparison for each line type.
    
    Returns cost breakdown per line type.
    """
    HOURS_PER_DAY = 8
    WORKING_DAYS_PER_YEAR = 250
    
    # Worker count estimates
    workers = {
        "cell": max(1, min(theoretical_min_stations, 3)),
        "short_line": min(theoretical_min_stations, 8),
        "long_line": int(theoretical_min_stations * 1.2)
    }
    
    # Efficiency factors (affects units per worker)
    efficiency = {
        "cell": 0.75,       # Lower efficiency but flexible
        "short_line": 0.85, # Balanced
        "long_line": 0.92   # High efficiency, specialized
    }
    
    cost_analysis = {}
    
    for line_type in ["cell", "short_line", "long_line"]:
        worker_count = workers[line_type]
        eff = efficiency[line_type]
        
        # Daily labor cost
        daily_labor = worker_count * HOURS_PER_DAY * labor_rate_per_hour
        
        # Overhead (equipment, utilities, etc.)
        daily_overhead = daily_labor * overhead_rate_pct
        
        # Total daily cost
        daily_total = daily_labor + daily_overhead
        
        # Effective units per day (adjusted by efficiency)
        effective_units = daily_demand * eff
        
        # Cost per unit
        cost_per_unit = daily_total / effective_units if effective_units > 0 else float('inf')
        
        # Annual operating cost
        annual_cost = daily_total * WORKING_DAYS_PER_YEAR
        
        cost_analysis[line_type] = {
            "cost_per_unit": round(cost_per_unit, 2),
            "labor_cost": round(daily_labor / effective_units, 2) if effective_units > 0 else None,
            "overhead_cost": round(daily_overhead / effective_units, 2) if effective_units > 0 else None,
            "annual_operating_cost": round(annual_cost, 0),
            "workers_required": worker_count
        }
    
    return cost_analysis


def calculate_risk_assessment(
    theoretical_min_stations: int,
    complexity_dist: Dict[str, int]
) -> Dict[str, Dict[str, Any]]:
    """
    Calculate risk profile for each line type.
    """
    total_tasks = sum(complexity_dist.values())
    complex_ratio = (complexity_dist.get("complex", 0) + complexity_dist.get("super_complex", 0)) / total_tasks if total_tasks > 0 else 0
    
    risk_assessment = {}
    
    for line_type in ["cell", "short_line", "long_line"]:
        # Bottleneck risk increases with line length
        if line_type == "cell":
            bottleneck = "low"
            spof = "low"
            flexibility = 0.95
        elif line_type == "short_line":
            bottleneck = "medium" if complex_ratio > 0.2 else "low"
            spof = "medium"
            flexibility = 0.70
        else:  # long_line
            bottleneck = "high" if complex_ratio > 0.1 else "medium"
            spof = "high"
            flexibility = 0.40
        
        # Quality risk based on handoff count
        handoff_count = theoretical_min_stations - 1
        if handoff_count <= 2:
            quality_risk = "low"
        elif handoff_count <= 7:
            quality_risk = "medium"
        else:
            quality_risk = "high"
        
        risk_assessment[line_type] = {
            "bottleneck_risk": bottleneck,
            "single_point_failure": spof,
            "quality_risk": quality_risk,
            "flexibility_score": flexibility,
            "handoff_count": handoff_count if line_type != "cell" else min(handoff_count, 2)
        }
    
    return risk_assessment


def calculate_implementation_effort(
    theoretical_min_stations: int
) -> Dict[str, Dict[str, Any]]:
    """
    Estimate implementation effort for each line type.
    """
    implementation = {}
    
    for line_type in ["cell", "short_line", "long_line"]:
        if line_type == "cell":
            setup_days = 1
            training_days = 0.5
            equipment_ready = True
            space_sqm = 45
        elif line_type == "short_line":
            setup_days = 3
            training_days = 1
            equipment_ready = True
            space_sqm = 50 * min(theoretical_min_stations, 8)
        else:  # long_line
            setup_days = 7
            training_days = 2
            equipment_ready = False  # May need additional equipment
            space_sqm = 50 * theoretical_min_stations
        
        implementation[line_type] = {
            "setup_days": setup_days,
            "training_days": training_days,
            "equipment_ready": equipment_ready,
            "space_required_sqm": space_sqm,
            "total_lead_time_days": setup_days + training_days
        }
    
    return implementation


def generate_scenario_comparison(
    scores: Dict[str, Dict],
    daily_demand: int
) -> Dict[str, Dict[str, Any]]:
    """
    Compare performance across different demand scenarios.
    """
    scenarios = {
        "current_demand": daily_demand,
        "peak_demand_150pct": int(daily_demand * 1.5),
        "low_demand_50pct": int(daily_demand * 0.5)
    }
    
    comparison = {}
    
    for scenario_name, demand in scenarios.items():
        # Re-evaluate best type for this demand level
        if demand < 50:
            best = "cell"
        elif demand <= 200:
            best = "short_line"
        else:
            best = "long_line"
        
        comparison[scenario_name] = {
            "demand": demand,
            "best_type": best,
            "efficiency": scores.get(best, {}).get("efficiency", 0.75)
        }
    
    return comparison


def validate_equipment(
    theoretical_min_stations: int,
    equipment_available: Optional[List[str]] = None
) -> Dict[str, Dict[str, Any]]:
    """
    Validate equipment availability for each line type.
    
    NEW in Phase 2.1: Equipment constraint check prevents recommending
    line types that require unavailable equipment.
    
    Args:
        theoretical_min_stations: Calculated minimum station count
        equipment_available: List of available equipment IDs
    
    Returns:
        Per-type equipment feasibility with missing items
    """
    # Equipment requirements per line type
    EQUIPMENT_REQUIREMENTS = {
        "cell": {
            "required": ["flexible_tooling"],
            "optional": ["multi_purpose_fixture", "portable_tools"]
        },
        "short_line": {
            "required": ["conveyor", "dedicated_fixture"],
            "optional": ["auto_screwdriver", "barcode_scanner"]
        },
        "long_line": {
            "required": ["conveyor", "agv", "automated_station"],
            "optional": ["vision_system", "robotic_arm", "plc_controller"]
        }
    }
    
    equipment_check = {}
    available = set(equipment_available) if equipment_available else set()
    
    for line_type in ["cell", "short_line", "long_line"]:
        required = set(EQUIPMENT_REQUIREMENTS[line_type]["required"])
        missing = required - available
        
        equipment_check[line_type] = {
            "feasible": len(missing) == 0 or not equipment_available,
            "required_equipment": list(required),
            "missing_equipment": list(missing),
            "check_performed": equipment_available is not None
        }
    
    return equipment_check


def get_historical_accuracy(
    product_family: Optional[str] = None
) -> Dict[str, Any]:
    """
    Query historical recommendation accuracy for a product family.
    
    NEW in Phase 2.1: Learning from past recommendations enables
    accuracy improvement and identifies common override patterns.
    
    Args:
        product_family: Product family code (e.g., "DL360", "ML350")
    
    Returns:
        Historical accuracy metrics and common override reasons
    """
    if not product_family:
        return {
            "available": False,
            "message": "No product family specified"
        }
    
    # Query database for historical recommendations
    # SELECT COUNT(*), 
    #        SUM(CASE WHEN was_overridden = FALSE THEN 1 ELSE 0 END) as accepted,
    #        override_reason
    # FROM recommendation_history
    # WHERE product_family = ?
    # GROUP BY override_reason
    
    # Return structure (from DB query)
    return {
        "available": True,
        "product_family": product_family,
        "past_recommendations": 15,  # From DB
        "accuracy_rate": 0.82,       # accepted / total
        "common_override_reason": "space_constraint",  # Most frequent
        "successful_types": {
            "cell": 2,
            "short_line": 10,
            "long_line": 3
        },
        "last_recommendation_date": "2025-11-28"
    }


def calculate_confidence_interval(
    base_confidence: float,
    historical_data: Dict[str, Any],
    constraints_passed: bool
) -> Dict[str, Any]:
    """
    Calculate statistical confidence interval for recommendation.
    
    NEW in Phase 2.1: Provides uncertainty range to help users
    understand recommendation reliability.
    
    Args:
        base_confidence: Initial confidence score (0-1)
        historical_data: Result from get_historical_accuracy()
        constraints_passed: Whether all constraints are satisfied
    
    Returns:
        Confidence interval with bounds and reliability indicator
    """
    # Base interval width (narrows with more data)
    base_width = 0.15
    sample_size = 0
    
    if historical_data.get("available", False):
        sample_size = historical_data.get("past_recommendations", 0)
        # More samples = narrower interval (Wilson score interval concept)
        sample_adjustment = min(0.05, sample_size * 0.002)
        base_width -= sample_adjustment
        
        # Adjust confidence based on historical accuracy
        hist_accuracy = historical_data.get("accuracy_rate", 0.5)
        base_confidence = min(0.99, max(0.1, base_confidence + (hist_accuracy - 0.5) * 0.2))
    
    # Widen interval if constraints failed
    if not constraints_passed:
        base_width += 0.1
    
    low = max(0.0, base_confidence - base_width / 2)
    high = min(1.0, base_confidence + base_width / 2)
    
    return {
        "confidence": round(base_confidence, 2),
        "low": round(low, 2),
        "high": round(high, 2),
        "sample_size": sample_size,
        "reliability": "high" if sample_size >= 20 else ("medium" if sample_size >= 5 else "low")
    }
```

---

### 2.8 Caching Strategy (Optional Enhancement)

Redis-based caching for recommendation performance optimization.

```python
import hashlib
import json
from typing import Optional
from redis import Redis

class RecommendationCache:
    """
    Cache recommendations for identical input parameters.
    
    Cache Key Structure:
        rec:{hash(sorted(input_params))}
    
    TTL Strategy:
        - Default: 1 hour
        - Historical data updated: 15 minutes
        - Site threshold changed: Invalidate all site keys
    """
    
    def __init__(self, redis_client: Redis, default_ttl: int = 3600):
        self.redis = redis_client
        self.default_ttl = default_ttl
    
    def _generate_cache_key(self, params: dict) -> str:
        """Generate deterministic cache key from input parameters."""
        # Sort keys for consistent hashing
        sorted_params = json.dumps(params, sort_keys=True)
        param_hash = hashlib.md5(sorted_params.encode()).hexdigest()[:16]
        return f"rec:{param_hash}"
    
    def get_cached_recommendation(self, params: dict) -> Optional[dict]:
        """Retrieve cached recommendation if available."""
        key = self._generate_cache_key(params)
        cached = self.redis.get(key)
        if cached:
            return json.loads(cached)
        return None
    
    def cache_recommendation(
        self, 
        params: dict, 
        result: dict,
        ttl: Optional[int] = None
    ) -> None:
        """Cache recommendation result."""
        key = self._generate_cache_key(params)
        self.redis.setex(
            key,
            ttl or self.default_ttl,
            json.dumps(result)
        )
    
    def invalidate_by_site(self, site_id: str) -> int:
        """Invalidate all cached recommendations for a site."""
        pattern = f"rec:*"
        count = 0
        for key in self.redis.scan_iter(pattern):
            cached = self.redis.get(key)
            if cached:
                data = json.loads(cached)
                if data.get("site_id") == site_id:
                    self.redis.delete(key)
                    count += 1
        return count
    
    def get_cache_stats(self) -> dict:
        """Return cache statistics."""
        keys = list(self.redis.scan_iter("rec:*"))
        return {
            "cached_recommendations": len(keys),
            "memory_usage_bytes": sum(
                self.redis.memory_usage(k) or 0 for k in keys
            )
        }
```

**Cache Integration in API**:
```python
@app.post("/recommend-line-type")
async def recommend_line_type(
    request: LineTypeRequest,
    cache: RecommendationCache = Depends(get_cache)
):
    # Check cache first
    cache_params = request.dict(exclude_none=True)
    cached = cache.get_cached_recommendation(cache_params)
    if cached:
        cached["from_cache"] = True
        return cached
    
    # Generate recommendation
    result = RecommendationService.recommend(request)
    
    # Cache result
    cache.cache_recommendation(cache_params, result)
    result["from_cache"] = False
    return result
```

---

### 2.9 Frontend UI Component: Visual Recommendation Wizard (Optional Enhancement)

Interactive 4-step wizard guiding users through line type recommendation.

#### Component Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    LineTypeRecommendationWizard                     │
├─────────────────────────────────────────────────────────────────────┤
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │  Step 1  │→│  Step 2  │→│  Step 3  │→│  Step 4  │           │
│  │  Input   │  │ Preview  │  │ Compare  │  │ Confirm  │           │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘           │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    WizardStepContent                         │   │
│  │  - InputParametersForm (Step 1)                              │   │
│  │  - LivePreviewPanel (Step 2)                                 │   │
│  │  - ComparisonChartPanel (Step 3)                             │   │
│  │  - ConfirmationPanel (Step 4)                                │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    SharedComponents                          │   │
│  │  - ProgressIndicator                                         │   │
│  │  - ValidationFeedback                                        │   │
│  │  - CostComparisonChart (D3.js/Chart.js)                      │   │
│  │  - RiskRadarChart                                            │   │
│  │  - LineTypeVisualizer                                        │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

#### Step 1: Input Parameters Form

```javascript
// components/wizard/InputParametersForm.js
class InputParametersForm {
    constructor(container) {
        this.container = container;
        this.params = {};
        this.validationErrors = [];
    }
    
    render() {
        this.container.innerHTML = `
            <div class="wizard-step input-form">
                <h3>Step 1: Configure Parameters</h3>
                
                <div class="form-section">
                    <h4>📊 Work Order Information</h4>
                    <div class="form-group">
                        <label for="workOrderId">Work Order ID *</label>
                        <input type="text" id="workOrderId" required />
                    </div>
                    <div class="form-group">
                        <label for="productFamily">Product Family</label>
                        <select id="productFamily">
                            <option value="">-- Select --</option>
                            <option value="DL360">DL360 Series</option>
                            <option value="DL380">DL380 Series</option>
                            <option value="ML350">ML350 Series</option>
                        </select>
                    </div>
                </div>
                
                <div class="form-section">
                    <h4>⏱️ Time & Demand</h4>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="targetTakt">Target Takt Time (sec) *</label>
                            <input type="number" id="targetTakt" min="1" required />
                        </div>
                        <div class="form-group">
                            <label for="dailyDemand">Daily Demand *</label>
                            <input type="number" id="dailyDemand" min="1" required />
                        </div>
                    </div>
                </div>
                
                <div class="form-section">
                    <h4>👷 Constraints</h4>
                    <div class="form-row">
                        <div class="form-group">
                            <label for="spaceAvailable">Available Space (m²)</label>
                            <input type="number" id="spaceAvailable" min="0" />
                        </div>
                        <div class="form-group">
                            <label for="availableWorkers">Available Workers</label>
                            <input type="number" id="availableWorkers" min="1" />
                        </div>
                    </div>
                </div>
                
                <div class="form-section">
                    <h4>🔧 Equipment Available</h4>
                    <div class="checkbox-group" id="equipmentCheckboxes">
                        <!-- Dynamically populated -->
                    </div>
                </div>
                
                <div class="validation-feedback" id="validationFeedback"></div>
                
                <div class="wizard-actions">
                    <button type="button" class="btn-secondary" disabled>Back</button>
                    <button type="button" class="btn-primary" id="nextStep1">
                        Next: Preview Recommendation →
                    </button>
                </div>
            </div>
        `;
        
        this.bindEvents();
        this.loadEquipmentOptions();
    }
    
    async loadEquipmentOptions() {
        const response = await fetch('/api/equipment-types');
        const equipment = await response.json();
        const container = document.getElementById('equipmentCheckboxes');
        
        equipment.forEach(eq => {
            container.innerHTML += `
                <label class="checkbox-label">
                    <input type="checkbox" name="equipment" value="${eq.id}" />
                    ${eq.name}
                </label>
            `;
        });
    }
    
    validateAndProceed() {
        this.validationErrors = [];
        
        const workOrderId = document.getElementById('workOrderId').value;
        const targetTakt = parseInt(document.getElementById('targetTakt').value);
        const dailyDemand = parseInt(document.getElementById('dailyDemand').value);
        
        if (!workOrderId) this.validationErrors.push('Work Order ID is required');
        if (!targetTakt || targetTakt < 1) this.validationErrors.push('Valid Target Takt Time is required');
        if (!dailyDemand || dailyDemand < 1) this.validationErrors.push('Valid Daily Demand is required');
        
        if (this.validationErrors.length > 0) {
            this.showValidationErrors();
            return false;
        }
        
        this.collectParams();
        return true;
    }
}
```

#### Step 2: Live Preview Panel

```javascript
// components/wizard/LivePreviewPanel.js
class LivePreviewPanel {
    constructor(container, params) {
        this.container = container;
        this.params = params;
        this.previewResult = null;
    }
    
    async render() {
        this.container.innerHTML = `
            <div class="wizard-step preview-panel">
                <h3>Step 2: Preview Recommendation</h3>
                <div class="preview-loading">
                    <div class="spinner"></div>
                    <p>Analyzing your parameters...</p>
                </div>
            </div>
        `;
        
        await this.fetchPreview();
    }
    
    async fetchPreview() {
        try {
            const response = await fetch('/api/recommend-line-type', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.params)
            });
            
            this.previewResult = await response.json();
            this.renderPreview();
        } catch (error) {
            this.renderError(error);
        }
    }
    
    renderPreview() {
        const result = this.previewResult;
        
        this.container.innerHTML = `
            <div class="wizard-step preview-panel">
                <h3>Step 2: Preview Recommendation</h3>
                
                <div class="recommendation-hero">
                    <div class="recommended-type ${result.recommended_type}">
                        <span class="type-icon">${this.getTypeIcon(result.recommended_type)}</span>
                        <h2>${this.formatTypeName(result.recommended_type)}</h2>
                        <div class="confidence-badge">
                            <span class="score">${(result.confidence_score * 100).toFixed(0)}%</span>
                            <span class="label">Confidence</span>
                        </div>
                    </div>
                </div>
                
                <div class="preview-cards">
                    <div class="preview-card constraints">
                        <h4>Constraints Check</h4>
                        ${this.renderConstraintStatus(result.constraints_validation)}
                    </div>
                    
                    <div class="preview-card cost">
                        <h4>Estimated Cost</h4>
                        <p class="cost-value">$${result.cost_analysis[result.recommended_type].total.toLocaleString()}</p>
                        <p class="cost-label">per unit</p>
                    </div>
                    
                    <div class="preview-card risk">
                        <h4>Overall Risk</h4>
                        <p class="risk-score ${result.risk_assessment[result.recommended_type].overall_risk}">
                            ${result.risk_assessment[result.recommended_type].overall_risk.toUpperCase()}
                        </p>
                    </div>
                </div>
                
                <div class="warnings-section">
                    ${result.warnings.map(w => `
                        <div class="warning-item ${w.severity}">
                            <span class="warning-icon">⚠️</span>
                            <span>${w.message}</span>
                        </div>
                    `).join('')}
                </div>
                
                <div class="wizard-actions">
                    <button type="button" class="btn-secondary" id="backStep2">← Back</button>
                    <button type="button" class="btn-primary" id="nextStep2">
                        Next: Compare All Options →
                    </button>
                </div>
            </div>
        `;
    }
    
    getTypeIcon(type) {
        const icons = {
            'cell': '🔲',
            'short_line': '📏',
            'long_line': '🔗'
        };
        return icons[type] || '❓';
    }
}
```

#### Step 3: Comparison Chart Panel

```javascript
// components/wizard/ComparisonChartPanel.js
class ComparisonChartPanel {
    constructor(container, result) {
        this.container = container;
        this.result = result;
    }
    
    render() {
        this.container.innerHTML = `
            <div class="wizard-step comparison-panel">
                <h3>Step 3: Compare All Line Types</h3>
                
                <div class="comparison-tabs">
                    <button class="tab active" data-tab="scores">Scores</button>
                    <button class="tab" data-tab="cost">Cost</button>
                    <button class="tab" data-tab="risk">Risk</button>
                </div>
                
                <div class="chart-container">
                    <canvas id="comparisonChart"></canvas>
                </div>
                
                <div class="comparison-table">
                    <table>
                        <thead>
                            <tr>
                                <th>Criteria</th>
                                <th>Cell</th>
                                <th>Short Line</th>
                                <th>Long Line</th>
                            </tr>
                        </thead>
                        <tbody id="comparisonTableBody">
                        </tbody>
                    </table>
                </div>
                
                <div class="wizard-actions">
                    <button type="button" class="btn-secondary" id="backStep3">← Back</button>
                    <button type="button" class="btn-primary" id="nextStep3">
                        Confirm Selection →
                    </button>
                </div>
            </div>
        `;
        
        this.renderComparisonChart();
        this.renderComparisonTable();
    }
    
    renderComparisonChart() {
        const ctx = document.getElementById('comparisonChart').getContext('2d');
        const comparison = this.result.comparison;
        
        new Chart(ctx, {
            type: 'radar',
            data: {
                labels: ['Efficiency', 'Flexibility', 'Quality', 'Space', 'Cost'],
                datasets: [
                    {
                        label: 'Cell',
                        data: [
                            comparison.cell.efficiency * 100,
                            comparison.cell.flexibility * 100,
                            comparison.cell.quality * 100,
                            comparison.cell.space_score * 100,
                            (1 - comparison.cell.cost_normalized) * 100
                        ],
                        borderColor: '#4CAF50',
                        backgroundColor: 'rgba(76, 175, 80, 0.2)'
                    },
                    {
                        label: 'Short Line',
                        data: [
                            comparison.short_line.efficiency * 100,
                            comparison.short_line.flexibility * 100,
                            comparison.short_line.quality * 100,
                            comparison.short_line.space_score * 100,
                            (1 - comparison.short_line.cost_normalized) * 100
                        ],
                        borderColor: '#2196F3',
                        backgroundColor: 'rgba(33, 150, 243, 0.2)'
                    },
                    {
                        label: 'Long Line',
                        data: [
                            comparison.long_line.efficiency * 100,
                            comparison.long_line.flexibility * 100,
                            comparison.long_line.quality * 100,
                            comparison.long_line.space_score * 100,
                            (1 - comparison.long_line.cost_normalized) * 100
                        ],
                        borderColor: '#FF9800',
                        backgroundColor: 'rgba(255, 152, 0, 0.2)'
                    }
                ]
            },
            options: {
                scales: {
                    r: {
                        beginAtZero: true,
                        max: 100
                    }
                }
            }
        });
    }
}
```

#### Step 4: Confirmation Panel

```javascript
// components/wizard/ConfirmationPanel.js
class ConfirmationPanel {
    constructor(container, result, selectedType) {
        this.container = container;
        this.result = result;
        this.selectedType = selectedType || result.recommended_type;
    }
    
    render() {
        const isOverride = this.selectedType !== this.result.recommended_type;
        
        this.container.innerHTML = `
            <div class="wizard-step confirmation-panel">
                <h3>Step 4: Confirm Your Selection</h3>
                
                <div class="selection-summary">
                    <div class="selected-type ${this.selectedType}">
                        <h2>Selected: ${this.formatTypeName(this.selectedType)}</h2>
                        ${isOverride ? `
                            <div class="override-notice">
                                <span>⚠️ You are overriding the recommendation</span>
                                <p>Recommended was: ${this.formatTypeName(this.result.recommended_type)}</p>
                            </div>
                        ` : ''}
                    </div>
                </div>
                
                ${isOverride ? `
                    <div class="override-reason-form">
                        <label for="overrideReason">Please provide a reason for your selection:</label>
                        <select id="overrideReason" required>
                            <option value="">-- Select Reason --</option>
                            <option value="space_constraint">Space constraints not in data</option>
                            <option value="equipment_availability">Equipment availability</option>
                            <option value="worker_skill">Worker skill requirements</option>
                            <option value="customer_requirement">Customer requirement</option>
                            <option value="other">Other</option>
                        </select>
                        <textarea id="overrideNotes" placeholder="Additional notes (optional)"></textarea>
                    </div>
                ` : ''}
                
                <div class="action-buttons">
                    <button class="btn-secondary" id="exportPdf">
                        📄 Export PDF
                    </button>
                    <button class="btn-secondary" id="exportExcel">
                        📊 Export Excel
                    </button>
                </div>
                
                <div class="wizard-actions">
                    <button type="button" class="btn-secondary" id="backStep4">← Back</button>
                    <button type="button" class="btn-success" id="confirmSelection">
                        ✓ Confirm & Apply
                    </button>
                </div>
            </div>
        `;
        
        this.bindEvents();
    }
    
    async confirmSelection() {
        const payload = {
            work_order_id: this.result.work_order_id,
            recommended_type: this.result.recommended_type,
            actual_type: this.selectedType,
            accepted: this.selectedType === this.result.recommended_type
        };
        
        if (!payload.accepted) {
            payload.override_reason = document.getElementById('overrideReason').value;
            payload.notes = document.getElementById('overrideNotes').value;
        }
        
        await fetch('/api/recommend-line-type/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });
        
        // Navigate to line configuration
        window.location.href = `/configure-line?type=${this.selectedType}&wo=${this.result.work_order_id}`;
    }
}
```

#### Main Wizard Controller

```javascript
// components/wizard/LineTypeWizard.js
class LineTypeWizard {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        this.currentStep = 1;
        this.params = {};
        this.result = null;
        this.selectedType = null;
        
        this.steps = {
            1: InputParametersForm,
            2: LivePreviewPanel,
            3: ComparisonChartPanel,
            4: ConfirmationPanel
        };
    }
    
    init() {
        this.renderProgressBar();
        this.goToStep(1);
    }
    
    renderProgressBar() {
        const progressHtml = `
            <div class="wizard-progress">
                <div class="progress-step active" data-step="1">
                    <span class="step-number">1</span>
                    <span class="step-label">Input</span>
                </div>
                <div class="progress-line"></div>
                <div class="progress-step" data-step="2">
                    <span class="step-number">2</span>
                    <span class="step-label">Preview</span>
                </div>
                <div class="progress-line"></div>
                <div class="progress-step" data-step="3">
                    <span class="step-number">3</span>
                    <span class="step-label">Compare</span>
                </div>
                <div class="progress-line"></div>
                <div class="progress-step" data-step="4">
                    <span class="step-number">4</span>
                    <span class="step-label">Confirm</span>
                </div>
            </div>
            <div id="wizardContent"></div>
        `;
        
        this.container.innerHTML = progressHtml;
    }
    
    goToStep(step) {
        this.currentStep = step;
        this.updateProgressBar();
        
        const contentContainer = document.getElementById('wizardContent');
        const StepClass = this.steps[step];
        
        let stepInstance;
        switch(step) {
            case 1:
                stepInstance = new StepClass(contentContainer);
                break;
            case 2:
                stepInstance = new StepClass(contentContainer, this.params);
                break;
            case 3:
                stepInstance = new StepClass(contentContainer, this.result);
                break;
            case 4:
                stepInstance = new StepClass(contentContainer, this.result, this.selectedType);
                break;
        }
        
        stepInstance.render();
    }
}

// Initialize wizard
document.addEventListener('DOMContentLoaded', () => {
    const wizard = new LineTypeWizard('recommendation-wizard');
    wizard.init();
});
```

---

### 2.10 A/B Testing Framework Architecture (Optional Enhancement)

Algorithm variation testing system for continuous improvement.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    A/B Testing Architecture                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐  │
│  │   Experiment    │    │    Traffic      │    │    Variant      │  │
│  │   Manager       │───▶│    Router       │───▶│    Executor     │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘  │
│         │                       │                       │            │
│         ▼                       ▼                       ▼            │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐  │
│  │   Targeting     │    │   Consistent    │    │   Config        │  │
│  │   Rules         │    │   Hashing       │    │   Overrides     │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘  │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                    Metrics Collection                            │ │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────────┐ │ │
│  │  │Acceptance│  │ Override │  │Confidence│  │User Satisfaction │ │ │
│  │  │  Rate    │  │  Rate    │  │ Accuracy │  │    Score         │ │ │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────────────┘ │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                 │                                     │
│                                 ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                Statistical Analysis Engine                       │ │
│  │  - Chi-Square Test for significance                              │ │
│  │  - Confidence interval calculation                               │ │
│  │  - Sample size validation                                        │ │
│  │  - Automatic winner detection                                    │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                 │                                     │
│                                 ▼                                     │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                Production Rollout                                │ │
│  │  - Winner config application                                     │ │
│  │  - Threshold updates                                             │ │
│  │  - Cache invalidation                                            │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

**Experiment Lifecycle**:

```
DRAFT ──▶ ACTIVE ──▶ COMPLETED
             │            │
             ▼            ▼
          PAUSED    (Applied to Production)
```

**Database Schema**:

```sql
-- A/B Testing tables
CREATE TABLE recommendation_experiments (
    id SERIAL PRIMARY KEY,
    experiment_id VARCHAR(100) UNIQUE NOT NULL,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'draft',
    variants JSONB NOT NULL,
    targeting JSONB,
    primary_metric VARCHAR(50) DEFAULT 'acceptance_rate',
    secondary_metrics JSONB,
    target_sample_size INTEGER DEFAULT 1000,
    current_results JSONB,
    statistical_significance JSONB,
    winner_variant VARCHAR(50),
    applied_to_production BOOLEAN DEFAULT FALSE,
    created_by VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    started_at TIMESTAMP,
    concluded_at TIMESTAMP
);

CREATE TABLE experiment_assignments (
    id SERIAL PRIMARY KEY,
    experiment_id VARCHAR(100) NOT NULL,
    recommendation_id VARCHAR(100) NOT NULL,
    variant_id VARCHAR(50) NOT NULL,
    accepted BOOLEAN,
    override_reason VARCHAR(200),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(experiment_id, recommendation_id)
);

CREATE INDEX idx_exp_assignments_experiment ON experiment_assignments(experiment_id);
CREATE INDEX idx_exp_assignments_recommendation ON experiment_assignments(recommendation_id);
```

---

### 2.11 NLP Explanation Architecture (Optional Enhancement - Phase 3 Prep)

Natural language explanation generation system.

```
┌─────────────────────────────────────────────────────────────────────┐
│                 Explanation Generation Pipeline                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────┐                                                 │
│  │  Recommendation │                                                 │
│  │     Result      │                                                 │
│  └────────┬────────┘                                                 │
│           │                                                           │
│           ▼                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                   Factor Analysis Engine                         │ │
│  │  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │ │
│  │  │ Task Count   │  │ Daily Demand │  │ Product Mix Analysis │   │ │
│  │  │ Analyzer     │  │ Analyzer     │  │                      │   │ │
│  │  └──────────────┘  └──────────────┘  └──────────────────────┘   │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│           │                                                           │
│           ▼                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                   Template Engine (Phase 2)                      │ │
│  │  - Multi-language support (EN/ZH)                                │ │
│  │  - Audience adaptation (operator/engineer/manager)               │ │
│  │  - Detail level scaling (brief/standard/detailed)                │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│           │                                                           │
│           ▼ (Phase 3 Enhancement)                                     │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                   LLM Enhancement Layer                          │ │
│  │  ┌───────────────────────────────────────────────────────────┐  │ │
│  │  │  OpenAI GPT-4 / Claude Integration                        │  │ │
│  │  │  - Contextual explanation enhancement                      │  │ │
│  │  │  - Industry best practices injection                       │  │ │
│  │  │  - ROI estimation generation                               │  │ │
│  │  └───────────────────────────────────────────────────────────┘  │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│           │                                                           │
│           ▼                                                           │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                   Structured Output                              │ │
│  │  {                                                               │ │
│  │    "summary": "...",                                             │ │
│  │    "key_factors": [...],                                         │ │
│  │    "alternatives_considered": [...],                             │ │
│  │    "risks_mentioned": [...],                                     │ │
│  │    "action_items": [...]                                         │ │
│  │  }                                                               │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

**Audience Adaptation Matrix**:

| Audience | Language Style | Focus | Technical Depth | Example Phrase |
|----------|----------------|-------|-----------------|----------------|
| Operator | Simple, direct | Actions | Low | "Set up the cell workstation" |
| Engineer | Technical, precise | Reasoning | Medium | "Task count of 15 enables single-operator flow" |
| Manager | Business-focused | Impact | High | "Estimated 40% labor cost reduction vs. long line" |

---

### 2.12 Audit Trail Architecture (Optional Enhancement)

Compliance and debugging tracking system.

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Audit Trail Architecture                          │
├─────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐  │
│  │  Recommendation │───▶│ Audit Logger    │───▶│  Event Store    │  │
│  │     Service     │    │                 │    │  (Immutable)    │  │
│  └─────────────────┘    └─────────────────┘    └─────────────────┘  │
│                                │                        │            │
│                                │                        │            │
│  ┌─────────────────────────────┴────────────────────────┴──────────┐ │
│  │                      Event Types                                 │ │
│  │  ┌────────────┐ ┌────────────┐ ┌────────────┐ ┌──────────────┐  │ │
│  │  │  created   │ │   viewed   │ │ overridden │ │   approved   │  │ │
│  │  └────────────┘ └────────────┘ └────────────┘ └──────────────┘  │ │
│  │  ┌────────────┐ ┌────────────┐                                   │ │
│  │  │  applied   │ │  exported  │                                   │ │
│  │  └────────────┘ └────────────┘                                   │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                   Snapshot Store                                 │ │
│  │  - Input parameters at creation time                             │ │
│  │  - Scores and algorithm version                                  │ │
│  │  - Thresholds version used                                       │ │
│  │  - Experiment variant (if applicable)                            │ │
│  └─────────────────────────────────────────────────────────────────┘ │
│                                                                       │
│  ┌─────────────────────────────────────────────────────────────────┐ │
│  │                   Compliance Features                            │ │
│  │  - 7-year retention policy                                       │ │
│  │  - Data classification tagging                                   │ │
│  │  - GDPR relevance flagging                                       │ │
│  │  - Actor tracking (user/system)                                  │ │
│  └─────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

**Database Schema**:

```sql
-- Audit tables
CREATE TABLE recommendation_audit_events (
    id SERIAL PRIMARY KEY,
    event_id VARCHAR(100) UNIQUE NOT NULL,
    recommendation_id VARCHAR(100) NOT NULL,
    work_order_id VARCHAR(100) NOT NULL,
    action VARCHAR(50) NOT NULL,
    actor VARCHAR(100) NOT NULL,
    actor_type VARCHAR(20) DEFAULT 'user',
    details JSONB,
    client_ip VARCHAR(45),
    user_agent TEXT,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE recommendation_snapshots (
    id SERIAL PRIMARY KEY,
    recommendation_id VARCHAR(100) UNIQUE NOT NULL,
    input_parameters JSONB NOT NULL,
    scores JSONB NOT NULL,
    constraints_result JSONB,
    thresholds_version VARCHAR(50),
    algorithm_version VARCHAR(20),
    experiment_variant VARCHAR(50),
    data_classification VARCHAR(20) DEFAULT 'internal',
    retention_days INTEGER DEFAULT 2555,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for efficient querying
CREATE INDEX idx_audit_recommendation ON recommendation_audit_events(recommendation_id);
CREATE INDEX idx_audit_work_order ON recommendation_audit_events(work_order_id);
CREATE INDEX idx_audit_timestamp ON recommendation_audit_events(timestamp);
CREATE INDEX idx_audit_actor ON recommendation_audit_events(actor);
```

---

### 3. Algorithm Component (Multi-Line Solver)

**Phase 2 Additions**:

#### 3.1 Multi-Line Optimization Model
```python
def solve_multi_line_problem(
    tasks_df: pd.DataFrame,
    precedences_df: pd.DataFrame,
    lines: List[LineConfig],
    enable_cross_line_balancing: bool
) -> Dict[str, Any]:
    """
    Multi-line optimization model
    
    Decision Variables:
    - x[i][j][l] = 1 if task i is assigned to station j on line l
    - line_used[l] = 1 if line l is used
    
    Constraints:
    1. Each task assigned to exactly one station on one line
    2. Precedence constraints (within same line)
    3. Takt time constraints (per line)
    4. Cross-line balancing (if enabled)
    """
    model = cp_model.CpModel()
    
    num_tasks = len(tasks_df)
    num_lines = len(lines)
    max_stations_per_line = 20
    
    # Decision variables: x[i][j][l]
    x = {}
    for i in range(num_tasks):
        for l in range(num_lines):
            for j in range(max_stations_per_line):
                x[(i, j, l)] = model.NewBoolVar(f'x_t{i}_s{j}_l{l}')
    
    # Line usage variables
    line_used = [model.NewBoolVar(f'line_{l}_used') for l in range(num_lines)]
    
    # Constraint 1: Each task to exactly one (station, line) pair
    for i in range(num_tasks):
        model.Add(
            sum(x[(i, j, l)] 
                for l in range(num_lines) 
                for j in range(max_stations_per_line)
            ) == 1
        )
    
    # Constraint 2: Precedence (same line only)
    for _, row in precedences_df.iterrows():
        pred = int(row['predecessor'])
        succ = int(row['successor'])
        
        for l in range(num_lines):
            for j in range(max_stations_per_line - 1):
                # If pred at (j, l), succ must be at (j', l) where j' >= j
                model.Add(
                    sum(x[(succ, jp, l)] for jp in range(j + 1, max_stations_per_line))
                    >= x[(pred, j, l)]
                )
    
    # Constraint 3: Takt time per line
    for l, line_config in enumerate(lines):
        for j in range(max_stations_per_line):
            station_load = sum(
                tasks_df.loc[i, 'duration'] * x[(i, j, l)]
                for i in range(num_tasks)
            )
            model.Add(station_load <= line_config.target_takt)
    
    # Constraint 4: Cross-line balancing (optional)
    if enable_cross_line_balancing:
        # Balance workload across lines
        line_loads = []
        for l in range(num_lines):
            line_load = sum(
                tasks_df.loc[i, 'duration'] * x[(i, j, l)]
                for i in range(num_tasks)
                for j in range(max_stations_per_line)
            )
            line_loads.append(line_load)
        
        # Minimize max(line_loads) - min(line_loads)
        max_load = model.NewIntVar(0, 1000000, 'max_load')
        min_load = model.NewIntVar(0, 1000000, 'min_load')
        
        for load in line_loads:
            model.Add(max_load >= load)
            model.Add(min_load <= load)
        
        load_imbalance = model.NewIntVar(0, 1000000, 'imbalance')
        model.Add(load_imbalance == max_load - min_load)
    
    # Objective: Minimize total lines used + total stations
    total_stations = model.NewIntVar(0, num_lines * max_stations_per_line, 'total_stations')
    model.Add(
        total_stations == sum(
            model.NewBoolVar(f'station_{j}_line_{l}_used')
            for l in range(num_lines)
            for j in range(max_stations_per_line)
        )
    )
    
    model.Minimize(
        sum(line_used) * 1000 + total_stations
    )
    
    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.num_search_workers = 8
    solver.parameters.max_time_in_seconds = 60
    
    status = solver.Solve(model)
    
    if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
        return extract_multi_line_solution(solver, x, tasks_df, lines)
    else:
        raise ValueError(f"Solver failed with status: {status}")
```

#### 3.2 Fishbone Diagram Generator
```python
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import patches

def generate_fishbone_diagram(
    tasks_df: pd.DataFrame,
    precedences_df: pd.DataFrame,
    output_file: str,
    format: str = "svg"
):
    """
    Generate fishbone (assembly sequence) diagram
    
    Uses NetworkX to create directed graph, then renders as fishbone
    """
    # Build directed graph
    G = nx.DiGraph()
    
    # Add nodes (tasks)
    for _, row in tasks_df.iterrows():
        G.add_node(
            row['task_id'],
            duration=row['duration'],
            action_type=row.get('action_type', 'unknown')
        )
    
    # Add edges (precedences)
    for _, row in precedences_df.iterrows():
        G.add_edge(row['predecessor'], row['successor'])
    
    # Calculate levels (topological sort)
    levels = {}
    for node in nx.topological_sort(G):
        predecessors = list(G.predecessors(node))
        if not predecessors:
            levels[node] = 0
        else:
            levels[node] = max(levels[p] for p in predecessors) + 1
    
    # Fishbone layout (custom positioning)
    pos = fishbone_layout(G, levels)
    
    # Render
    fig, ax = plt.subplots(figsize=(16, 10))
    
    # Draw spine (main line)
    max_level = max(levels.values())
    ax.plot([0, max_level + 1], [0, 0], 'k-', linewidth=3, zorder=1)
    
    # Draw bones (tasks)
    for node, (x, y) in pos.items():
        # Task node
        circle = patches.Circle((x, y), 0.3, 
                                color=get_action_color(G.nodes[node]['action_type']),
                                zorder=3)
        ax.add_patch(circle)
        
        # Label
        ax.text(x, y, str(node), ha='center', va='center', 
                fontsize=8, fontweight='bold', zorder=4)
        
        # Bone line to spine
        ax.plot([x, x], [y, 0], 'k-', linewidth=1.5, zorder=2)
    
    # Draw precedence arrows
    for u, v in G.edges():
        x1, y1 = pos[u]
        x2, y2 = pos[v]
        ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                   arrowprops=dict(arrowstyle='->', lw=1, color='gray'))
    
    ax.set_xlim(-1, max_level + 2)
    ax.set_ylim(-5, 5)
    ax.axis('off')
    ax.set_title('Assembly Sequence Fishbone Diagram', fontsize=16, fontweight='bold')
    
    # Save
    if format == "svg":
        plt.savefig(output_file, format='svg', bbox_inches='tight')
    else:
        plt.savefig(output_file, format='png', dpi=300, bbox_inches='tight')
    
    plt.close()

def fishbone_layout(G, levels):
    """Custom fishbone layout positioning"""
    pos = {}
    level_counts = {}
    
    for node, level in levels.items():
        if level not in level_counts:
            level_counts[level] = 0
        
        # Alternate above/below spine
        y_offset = (level_counts[level] % 2) * 2 - 1  # -1 or 1
        y_position = y_offset * (1 + level_counts[level] // 2)
        
        pos[node] = (level, y_position)
        level_counts[level] += 1
    
    return pos

def get_action_color(action_type):
    """Color mapping for action types"""
    colors = {
        'screw': '#3498db',
        'glue': '#e74c3c',
        'clip': '#2ecc71',
        'mount': '#f39c12',
        'test': '#9b59b6',
        'unknown': '#95a5a6'
    }
    return colors.get(action_type, colors['unknown'])
```

---

## Cross-Line Task Benchmark Architecture

### Overview

The Cross-Line Task Benchmark system compares task execution times across different production lines to identify efficiency gaps, best practices, and improvement opportunities.

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    Cross-Line Task Benchmark Architecture                    │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  Data Collection Layer                                                      │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Task Execution Records                                              │   │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                  │   │
│  │  │   Line L1   │  │   Line L2   │  │   Line L3   │                  │   │
│  │  │  T001: 12.5s│  │  T001: 11.8s│  │  T001: 13.2s│                  │   │
│  │  │  T002: 8.5s │  │  T002: 9.1s │  │  T002: 8.2s │                  │   │
│  │  │  T003: 6.2s │  │  T003: 6.0s │  │  T003: 6.8s │                  │   │
│  │  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                  │   │
│  │         │                │                │                          │   │
│  │         └────────────────┼────────────────┘                          │   │
│  │                          ▼                                           │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │  task_execution_records (PostgreSQL)                        │    │   │
│  │  │  - task_id, line_id, worker_id, duration_ms, recorded_at   │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  Analysis Engine                                                            │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  benchmark_analyzer.py                                               │   │
│  │  ┌─────────────────────────────────────────────────────────────┐    │   │
│  │  │  1. Group by task_id + line_id                              │    │   │
│  │  │  2. Calculate statistics (avg, std, min, max, samples)      │    │   │
│  │  │  3. Identify best/worst performing lines per task           │    │   │
│  │  │  4. Calculate variance percentage                           │    │   │
│  │  │  5. Determine severity (normal/warning/critical)            │    │   │
│  │  │  6. Generate recommendations                                │    │   │
│  │  └─────────────────────────────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  Report Generation                                                          │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  benchmark_reports (PostgreSQL)                                      │   │
│  │  - benchmark_id, generated_at, lines_compared, report_json          │   │
│  │                                                                      │   │
│  │  Export Formats:                                                     │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                           │   │
│  │  │   JSON   │  │   CSV    │  │   PDF    │                           │   │
│  │  └──────────┘  └──────────┘  └──────────┘                           │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                    │                                        │
│                                    ▼                                        │
│  Visualization Layer                                                        │
│  ┌─────────────────────────────────────────────────────────────────────┐   │
│  │  Dashboard Components                                                │   │
│  │  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐      │   │
│  │  │ Grouped Bar     │  │ Variance Heat   │  │ Trend Line      │      │   │
│  │  │ Chart           │  │ Map             │  │ Chart           │      │   │
│  │  │ (per task)      │  │ (task x line)   │  │ (over time)     │      │   │
│  │  └─────────────────┘  └─────────────────┘  └─────────────────┘      │   │
│  └─────────────────────────────────────────────────────────────────────┘   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Core Components

#### 1. Benchmark Analyzer (`benchmark_analyzer.py`)

```python
import statistics
from typing import List, Dict, Any
from dataclasses import dataclass
from datetime import datetime

@dataclass
class TaskLineStats:
    """Statistics for a task on a specific line"""
    line_id: str
    avg_ms: float
    std_ms: float
    min_ms: float
    max_ms: float
    samples: int

@dataclass
class TaskBenchmark:
    """Benchmark result for a single task across lines"""
    task_id: str
    task_name: str
    line_stats: Dict[str, TaskLineStats]
    best_line: str
    worst_line: str
    variance_percent: float
    severity: str  # normal, warning, critical
    recommendation: str

class BenchmarkAnalyzer:
    """Cross-line task benchmark analysis engine"""
    
    def __init__(
        self,
        warning_threshold: float = 10.0,
        critical_threshold: float = 15.0
    ):
        self.warning_threshold = warning_threshold
        self.critical_threshold = critical_threshold
    
    def analyze(
        self,
        task_records: List[Dict],
        line_ids: List[str]
    ) -> Dict[str, Any]:
        """
        Analyze task execution times across lines
        
        Args:
            task_records: List of {task_id, line_id, duration_ms, ...}
            line_ids: Lines to compare
        
        Returns:
            Complete benchmark report
        """
        # Group records by (task_id, line_id)
        grouped = self._group_records(task_records)
        
        # Calculate statistics per task
        task_benchmarks = []
        for task_id in self._get_unique_tasks(task_records):
            benchmark = self._analyze_task(task_id, grouped, line_ids)
            if benchmark:
                task_benchmarks.append(benchmark)
        
        # Calculate summary
        summary = self._calculate_summary(task_benchmarks, line_ids)
        
        return {
            "benchmark_id": self._generate_benchmark_id(),
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "lines_compared": line_ids,
            "task_benchmarks": [tb.__dict__ for tb in task_benchmarks],
            "summary": summary
        }
    
    def _analyze_task(
        self,
        task_id: str,
        grouped: Dict,
        line_ids: List[str]
    ) -> TaskBenchmark:
        """Analyze a single task across all lines"""
        line_stats = {}
        
        for line_id in line_ids:
            key = (task_id, line_id)
            if key in grouped:
                durations = grouped[key]
                line_stats[line_id] = TaskLineStats(
                    line_id=line_id,
                    avg_ms=statistics.mean(durations),
                    std_ms=statistics.stdev(durations) if len(durations) > 1 else 0,
                    min_ms=min(durations),
                    max_ms=max(durations),
                    samples=len(durations)
                )
        
        if len(line_stats) < 2:
            return None  # Need at least 2 lines to compare
        
        # Find best and worst lines
        sorted_lines = sorted(
            line_stats.items(),
            key=lambda x: x[1].avg_ms
        )
        best_line = sorted_lines[0][0]
        worst_line = sorted_lines[-1][0]
        
        # Calculate variance
        best_avg = sorted_lines[0][1].avg_ms
        worst_avg = sorted_lines[-1][1].avg_ms
        variance_percent = ((worst_avg - best_avg) / best_avg) * 100
        
        # Determine severity
        if variance_percent >= self.critical_threshold:
            severity = "critical"
        elif variance_percent >= self.warning_threshold:
            severity = "warning"
        else:
            severity = "normal"
        
        # Generate recommendation
        recommendation = self._generate_recommendation(
            task_id, best_line, worst_line, variance_percent, severity
        )
        
        return TaskBenchmark(
            task_id=task_id,
            task_name=self._get_task_name(task_id),
            line_stats={k: v.__dict__ for k, v in line_stats.items()},
            best_line=best_line,
            worst_line=worst_line,
            variance_percent=round(variance_percent, 1),
            severity=severity,
            recommendation=recommendation
        )
    
    def _calculate_summary(
        self,
        task_benchmarks: List[TaskBenchmark],
        line_ids: List[str]
    ) -> Dict:
        """Calculate summary statistics"""
        if not task_benchmarks:
            return {}
        
        # Count by severity
        critical_count = sum(1 for tb in task_benchmarks if tb.severity == "critical")
        warning_count = sum(1 for tb in task_benchmarks if tb.severity == "warning")
        normal_count = sum(1 for tb in task_benchmarks if tb.severity == "normal")
        
        # Average variance
        avg_variance = statistics.mean(tb.variance_percent for tb in task_benchmarks)
        
        # Find overall best/worst lines
        line_scores = {lid: [] for lid in line_ids}
        for tb in task_benchmarks:
            for lid, stats in tb.line_stats.items():
                if isinstance(stats, dict):
                    line_scores[lid].append(stats['avg_ms'])
        
        line_averages = {
            lid: statistics.mean(scores) if scores else float('inf')
            for lid, scores in line_scores.items()
        }
        best_overall = min(line_averages, key=line_averages.get)
        worst_overall = max(line_averages, key=line_averages.get)
        
        # Calculate improvement potential
        improvement_potential = self._calculate_improvement_potential(task_benchmarks)
        
        return {
            "total_tasks_compared": len(task_benchmarks),
            "high_variance_tasks": critical_count,
            "warning_variance_tasks": warning_count,
            "normal_variance_tasks": normal_count,
            "avg_cross_line_variance_percent": round(avg_variance, 1),
            "best_overall_line": best_overall,
            "worst_overall_line": worst_overall,
            "improvement_potential_percent": improvement_potential["percent"],
            "improvement_potential_ms": improvement_potential["ms"]
        }
```

#### 2. Database Schema (Extended)

```sql
-- Task execution records (data collection)
CREATE TABLE task_execution_records (
    id SERIAL PRIMARY KEY,
    task_id VARCHAR(50) NOT NULL,
    task_name VARCHAR(255),
    line_id VARCHAR(10) NOT NULL,
    worker_id VARCHAR(50),
    duration_ms INTEGER NOT NULL,
    recorded_at TIMESTAMP NOT NULL,
    shift VARCHAR(20),  -- morning, afternoon, night
    work_order_id VARCHAR(50),
    
    -- Indexes for efficient querying
    INDEX idx_task_line (task_id, line_id),
    INDEX idx_recorded_at (recorded_at),
    INDEX idx_work_order (work_order_id)
);

-- Benchmark reports (analysis results)
CREATE TABLE benchmark_reports (
    id SERIAL PRIMARY KEY,
    benchmark_id VARCHAR(50) UNIQUE NOT NULL,
    status VARCHAR(20) DEFAULT 'completed',  -- generating, completed, failed
    generated_at TIMESTAMP NOT NULL,
    lines_compared JSONB NOT NULL,  -- ["L1", "L2", "L3"]
    date_range_start DATE,
    date_range_end DATE,
    report_json JSONB NOT NULL,
    summary_json JSONB,
    
    -- Configuration
    warning_threshold DECIMAL(5,2) DEFAULT 10.0,
    critical_threshold DECIMAL(5,2) DEFAULT 15.0,
    include_worker_analysis BOOLEAN DEFAULT FALSE,
    
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    
    INDEX idx_benchmark_id (benchmark_id),
    INDEX idx_generated_at (generated_at)
);
```

#### 3. Frontend Dashboard Component

```javascript
class CrossLineBenchmarkDashboard {
  constructor(containerId) {
    this.container = document.getElementById(containerId);
    this.chartInstances = {};
  }

  async loadBenchmark(lineIds, dateFrom, dateTo) {
    const params = new URLSearchParams({
      line_ids: lineIds.join(','),
      date_from: dateFrom,
      date_to: dateTo
    });
    
    const response = await fetch(`/benchmark/cross-line-tasks?${params}`);
    const data = await response.json();
    
    this.renderDashboard(data);
  }

  renderDashboard(data) {
    // Render summary cards
    this.renderSummaryCards(data.summary);
    
    // Render grouped bar chart
    this.renderTaskComparisonChart(data.task_benchmarks, data.lines_compared);
    
    // Render variance table
    this.renderVarianceTable(data.task_benchmarks);
    
    // Render line load comparison
    this.renderLineLoadChart(data.task_benchmarks, data.lines_compared);
  }

  renderTaskComparisonChart(taskBenchmarks, lineIds) {
    const ctx = document.getElementById('taskComparisonChart').getContext('2d');
    
    const datasets = lineIds.map((lineId, idx) => ({
      label: `Line ${lineId}`,
      data: taskBenchmarks.map(tb => 
        tb.line_stats[lineId]?.avg_ms || 0
      ),
      backgroundColor: this.getLineColor(idx),
      borderWidth: 1
    }));
    
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: taskBenchmarks.map(tb => tb.task_name),
        datasets: datasets
      },
      options: {
        responsive: true,
        plugins: {
          title: {
            display: true,
            text: 'Task Execution Time Comparison by Line'
          }
        },
        scales: {
          y: {
            title: {
              display: true,
              text: 'Duration (ms)'
            }
          }
        }
      }
    });
  }

  renderVarianceTable(taskBenchmarks) {
    const tableHtml = `
      <table class="w-full border-collapse">
        <thead>
          <tr class="bg-gray-100">
            <th class="p-2 text-left">Task ID</th>
            <th class="p-2 text-left">Task Name</th>
            <th class="p-2 text-center">Best Line</th>
            <th class="p-2 text-center">Worst Line</th>
            <th class="p-2 text-center">Variance %</th>
            <th class="p-2 text-center">Status</th>
          </tr>
        </thead>
        <tbody>
          ${taskBenchmarks.map(tb => `
            <tr class="border-b hover:bg-gray-50">
              <td class="p-2">${tb.task_id}</td>
              <td class="p-2">${tb.task_name}</td>
              <td class="p-2 text-center text-green-600 font-semibold">${tb.best_line}</td>
              <td class="p-2 text-center text-red-600 font-semibold">${tb.worst_line}</td>
              <td class="p-2 text-center">${tb.variance_percent.toFixed(1)}%</td>
              <td class="p-2 text-center">${this.getSeverityBadge(tb.severity)}</td>
            </tr>
          `).join('')}
        </tbody>
      </table>
    `;
    
    document.getElementById('varianceTable').innerHTML = tableHtml;
  }

  getSeverityBadge(severity) {
    const badges = {
      normal: '<span class="px-2 py-1 bg-green-100 text-green-800 rounded">✅ Normal</span>',
      warning: '<span class="px-2 py-1 bg-yellow-100 text-yellow-800 rounded">⚠️ Warning</span>',
      critical: '<span class="px-2 py-1 bg-red-100 text-red-800 rounded">🔴 Critical</span>'
    };
    return badges[severity] || badges.normal;
  }

  getLineColor(index) {
    const colors = [
      'rgba(52, 152, 219, 0.7)',   // Blue
      'rgba(46, 204, 113, 0.7)',   // Green
      'rgba(231, 76, 60, 0.7)',    // Red
      'rgba(241, 196, 15, 0.7)',   // Yellow
      'rgba(155, 89, 182, 0.7)'    // Purple
    ];
    return colors[index % colors.length];
  }
}
```

### Severity Thresholds

| Severity     | Variance Range | Color     | Action Required          |
|--------------|----------------|-----------|--------------------------|
| **Normal**   | < 5%           | 🟢 Green  | No action needed         |
| **Warning**  | 5% - 15%       | 🟡 Yellow | Review work instructions |
| **Critical** | > 15%          | 🔴 Red    | Immediate investigation  |

### Use Cases

1. **Best Practice Identification**: Find which line performs best for each task
2. **Training Gap Analysis**: Identify lines/workers needing additional training
3. **Standard Time Calibration**: Validate and adjust standard work times
4. **Continuous Improvement**: Track efficiency gains over time
5. **Root Cause Analysis**: Investigate causes of high variance tasks

---

## Technology Stack

### Phase 2 Extended Stack

| Component           | Technology | Version | Purpose                          | New in Phase 2 |
|---------------------|------------|---------|----------------------------------|----------------|
| **Frontend**        | Canvas API | Native  | 2D layout editor                 | ✅              |
|                     | SVG        | Native  | Fishbone diagram rendering       | ✅              |
| **Backend**         | SQLAlchemy | 2.0+    | ORM for database                 | ✅              |
|                     | SQLite     | 3.x     | Embedded database (dev)          | ✅              |
|                     | PostgreSQL | 14+     | Production database (optional)   | ✅              |
| **Algorithm**       | NetworkX   | 3.0+    | Graph algorithms (fishbone)      | ✅              |
|                     | Matplotlib | 3.7+    | Diagram rendering                | ✅              |
| **Data Processing** | pandas     | 2.0+    | CSV + multi-line data processing | (existing)     |

---

## Data Flow

### Multi-Line Optimization Flow

```
┌──────────┐
│  User    │  (1) Configure 3 lines with different takt times
└────┬─────┘
     │
     ▼
┌─────────────────────────────────────────┐
│  Frontend: Multi-Line Panel             │
│  Line A: takt=30000ms, tasks=[1,2,3,4]  │
│  Line B: takt=25000ms, tasks=[5,6,7]    │
│  Line C: takt=35000ms, tasks=[8,9,10]   │
└────┬────────────────────────────────────┘
     │ POST /optimize (multi-line request)
     ▼
┌─────────────────────────────────────────┐
│  API Server: Multi-Line Handler         │
│  1. Validate line configurations        │
│  2. Merge task CSVs with line_id column │
│  3. Call sche-algo-v2.py                │
└────┬────────────────────────────────────┘
     │ python3 sche-algo-v2.py --multi_line
     ▼
┌─────────────────────────────────────────┐
│  Algorithm: Multi-Line Solver           │
│  1. Build 3D assignment model x[i][j][l]│
│  2. Add cross-line balancing            │
│  3. Solve with CP-SAT                   │
│  4. Return per-line assignments         │
└────┬────────────────────────────────────┘
     │ JSON output (multi-line results)
     ▼
┌─────────────────────────────────────────┐
│  API Server: Response Transform         │
│  {                                      │
│    "lines": [                           │
│      {"line_id": "A", "stations": 2},   │
│      {"line_id": "B", "stations": 2},   │
│      {"line_id": "C", "stations": 3}    │
│    ],                                   │
│    "total_lines_used": 3                │
│  }                                      │
└────┬────────────────────────────────────┘
     │ HTTP 200 OK
     ▼
┌─────────────────────────────────────────┐
│  Frontend: Multi-Line Gantt Chart       │
│  Render 3 separate Gantt charts stacked │
└─────────────────────────────────────────┘
```

---

## Database Schema

### Phase 2 Extended PostgreSQL Schema

Phase 2 extends the Phase 1 schema with spatial data, layout management, and product configuration:

```sql
-- Phase 2: Layout management tables
CREATE TABLE layouts (
    id SERIAL PRIMARY KEY,
    site_id INTEGER REFERENCES sites(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    layout_type VARCHAR(20) DEFAULT '2d',    -- 2d, 3d
    
    -- Layout metadata  
    dimensions_json JSONB,                   -- {"width": 100, "depth": 50, "height": 10}
    units VARCHAR(10) DEFAULT 'meters',      -- meters, feet, inches
    
    -- Version control
    version VARCHAR(50) NOT NULL,
    parent_layout_id INTEGER REFERENCES layouts(id),
    
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE
);

-- Station definitions within layouts
CREATE TABLE layout_stations (
    id SERIAL PRIMARY KEY,
    layout_id INTEGER REFERENCES layouts(id),
    station_code VARCHAR(50) NOT NULL,      -- WS-001, WS-002, etc.
    station_type VARCHAR(50) NOT NULL,      -- assembly, test, packaging
    
    -- Positioning
    position_x DECIMAL(8,3) NOT NULL,
    position_y DECIMAL(8,3) NOT NULL, 
    position_z DECIMAL(8,3) DEFAULT 0,
    
    -- Dimensions
    width DECIMAL(6,3) NOT NULL,
    depth DECIMAL(6,3) NOT NULL,
    height DECIMAL(6,3) DEFAULT 2,
    
    -- Multi-line assignment
    line_id VARCHAR(10),                     -- A, B, C for multi-line
    
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(layout_id, station_code)
);

-- Connections between stations (conveyors, AGVs)
CREATE TABLE layout_connections (
    id SERIAL PRIMARY KEY,
    layout_id INTEGER REFERENCES layouts(id),
    from_station_id INTEGER REFERENCES layout_stations(id),
    to_station_id INTEGER REFERENCES layout_stations(id),
    connection_type VARCHAR(50) NOT NULL,   -- conveyor, agv, manual
    
    -- Connection properties
    length_meters DECIMAL(6,3),
    speed_mps DECIMAL(5,3),                 -- meters per second
    capacity INTEGER,                       -- max items in transit
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- Phase 2: Product configuration for CTO/BTO
CREATE TABLE product_configs (
    id SERIAL PRIMARY KEY,
    sku VARCHAR(100) NOT NULL,
    product_name VARCHAR(255) NOT NULL,
    complexity_level VARCHAR(20) DEFAULT 'medium',
    cto_bto_mapping JSONB,                  -- Configure-to-Order mappings
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Enhanced task table (extends Phase 1)
ALTER TABLE tasks ADD COLUMN line_id VARCHAR(10);  -- Multi-line support

-- Enhanced optimization table (extends Phase 1) 
ALTER TABLE optimizations ADD COLUMN multi_line_enabled BOOLEAN DEFAULT FALSE;
ALTER TABLE optimizations ADD COLUMN cross_line_balancing BOOLEAN DEFAULT FALSE;
ALTER TABLE optimizations ADD COLUMN layout_id INTEGER REFERENCES layouts(id);

-- Enhanced station table (extends Phase 1)
ALTER TABLE stations ADD COLUMN line_id VARCHAR(10);
ALTER TABLE stations ADD COLUMN position_x DECIMAL(8,3);
ALTER TABLE stations ADD COLUMN position_y DECIMAL(8,3);
ALTER TABLE stations ADD COLUMN position_z DECIMAL(8,3) DEFAULT 0;

-- Phase 2.1: Recommendation feedback and historical tracking (NEW)
CREATE TABLE recommendation_history (
    id SERIAL PRIMARY KEY,
    recommendation_id VARCHAR(100) UNIQUE NOT NULL,
    work_order_id VARCHAR(100) NOT NULL,
    product_family VARCHAR(50),
    
    -- Recommendation details
    recommended_type VARCHAR(20) NOT NULL,  -- cell, short_line, long_line
    confidence DECIMAL(4,3) NOT NULL,
    confidence_low DECIMAL(4,3),
    confidence_high DECIMAL(4,3),
    
    -- Input parameters snapshot
    input_params_json JSONB NOT NULL,       -- All input parameters for reproducibility
    reasoning_json JSONB,                   -- decision_factors, complexity_dist, etc.
    
    -- User feedback
    user_decision VARCHAR(20),              -- accepted, overridden, NULL (pending)
    actual_type VARCHAR(20),                -- Actual line type used (if overridden)
    override_reason VARCHAR(50),            -- space_constraint, worker_availability, etc.
    comments TEXT,
    user_id VARCHAR(100),
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    decided_at TIMESTAMP,
    
    -- Indexes for querying
    INDEX idx_rec_product_family (product_family),
    INDEX idx_rec_work_order (work_order_id),
    INDEX idx_rec_decision (user_decision),
    INDEX idx_rec_created (created_at)
);

-- Aggregated accuracy metrics per product family (materialized for performance)
CREATE TABLE recommendation_accuracy_metrics (
    id SERIAL PRIMARY KEY,
    product_family VARCHAR(50) UNIQUE NOT NULL,
    
    -- Counts
    total_recommendations INTEGER DEFAULT 0,
    accepted_count INTEGER DEFAULT 0,
    overridden_count INTEGER DEFAULT 0,
    pending_count INTEGER DEFAULT 0,
    
    -- Accuracy metrics
    accuracy_rate DECIMAL(4,3),             -- accepted / (accepted + overridden)
    
    -- Override reason distribution
    override_reasons_json JSONB,            -- {"space_constraint": 5, "worker_availability": 3}
    
    -- Type-specific accuracy
    type_accuracy_json JSONB,               -- {"cell": 0.85, "short_line": 0.80, "long_line": 0.75}
    
    -- Timestamps
    last_recommendation_at TIMESTAMP,
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Function to update accuracy metrics after feedback
CREATE OR REPLACE FUNCTION update_recommendation_accuracy()
RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO recommendation_accuracy_metrics (product_family, total_recommendations, accepted_count, overridden_count)
    VALUES (NEW.product_family, 1, 
            CASE WHEN NEW.user_decision = 'accepted' THEN 1 ELSE 0 END,
            CASE WHEN NEW.user_decision = 'overridden' THEN 1 ELSE 0 END)
    ON CONFLICT (product_family) DO UPDATE SET
        total_recommendations = recommendation_accuracy_metrics.total_recommendations + 1,
        accepted_count = recommendation_accuracy_metrics.accepted_count + 
                        CASE WHEN NEW.user_decision = 'accepted' THEN 1 ELSE 0 END,
        overridden_count = recommendation_accuracy_metrics.overridden_count + 
                          CASE WHEN NEW.user_decision = 'overridden' THEN 1 ELSE 0 END,
        accuracy_rate = (recommendation_accuracy_metrics.accepted_count + 
                        CASE WHEN NEW.user_decision = 'accepted' THEN 1 ELSE 0 END)::DECIMAL / 
                        NULLIF(recommendation_accuracy_metrics.accepted_count + 
                               recommendation_accuracy_metrics.overridden_count + 1, 0),
        last_recommendation_at = NEW.created_at,
        updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_recommendation_accuracy
AFTER INSERT OR UPDATE ON recommendation_history
FOR EACH ROW
WHEN (NEW.user_decision IS NOT NULL)
EXECUTE FUNCTION update_recommendation_accuracy();
```

### Phase 2 API Endpoints (Extensions)

```yaml
# Layout Management APIs
POST   /api/v2/layouts                      # Create new factory layout
GET    /api/v2/layouts                      # List all layouts for site
GET    /api/v2/layouts/{id}                 # Get specific layout
PUT    /api/v2/layouts/{id}                 # Update existing layout
DELETE /api/v2/layouts/{id}                 # Soft delete layout

# Product Configuration APIs
GET    /api/v2/product-configs              # List product configs (CTO/BTO)
POST   /api/v2/product-configs              # Create product config
PUT    /api/v2/product-configs/{sku}        # Update product config

# Multi-line Optimization APIs (Enhanced)
POST   /api/v2/optimizations                # Multi-line optimization
GET    /api/v2/optimizations/{id}/lines     # Get line-specific results

# Fishbone Diagram APIs
GET    /api/v2/fishbone-diagram/{opt_id}    # Generate fishbone diagram
GET    /api/v2/recommend-line-type          # Line type recommendation

# Cross-Line Task Benchmark APIs
GET    /api/v2/benchmark/cross-line-tasks              # Get benchmark report
POST   /api/v2/benchmark/cross-line-tasks/generate     # Generate new benchmark
GET    /api/v2/benchmark/cross-line-tasks/{id}         # Get specific report
GET    /api/v2/benchmark/cross-line-tasks/{id}/export  # Export report (CSV/XLSX/PDF)
DELETE /api/v2/benchmark/cross-line-tasks/{id}         # Delete benchmark report

# Configuration Management APIs
POST   /api/v2/configurations               # Save configuration version
GET    /api/v2/configurations               # List configuration versions
GET    /api/v2/configurations/{id}/restore  # Restore configuration version
```

### ORM Models (SQLAlchemy)

```python
from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime

class Layout(Base):
    __tablename__ = 'layouts'
    
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey('sites.id'))
    name = Column(String(255), nullable=False)
    description = Column(Text)
    layout_type = Column(String(20), default='2d')
    
    # Metadata
    dimensions_json = Column(JSONB)
    units = Column(String(10), default='meters')
    
    # Version control
    version = Column(String(50), nullable=False)
    parent_layout_id = Column(Integer, ForeignKey('layouts.id'))
    
    # Audit
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    stations = relationship("LayoutStation", back_populates="layout")
    connections = relationship("LayoutConnection", back_populates="layout")

class LayoutStation(Base):
    __tablename__ = 'layout_stations'
    
    id = Column(Integer, primary_key=True)
    layout_id = Column(Integer, ForeignKey('layouts.id'))
    station_code = Column(String(50), nullable=False)
    station_type = Column(String(50), nullable=False)
    
    # Positioning
    position_x = Column(DECIMAL(8,3), nullable=False)
    position_y = Column(DECIMAL(8,3), nullable=False)
    position_z = Column(DECIMAL(8,3), default=0)
    
    # Dimensions
    width = Column(DECIMAL(6,3), nullable=False)
    depth = Column(DECIMAL(6,3), nullable=False)
    height = Column(DECIMAL(6,3), default=2)
    
    # Multi-line
    line_id = Column(String(10))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    layout = relationship("Layout", back_populates="stations")

class ProductConfig(Base):
    __tablename__ = 'product_configs'
    
    id = Column(Integer, primary_key=True)
    sku = Column(String(100), nullable=False)
    product_name = Column(String(255), nullable=False)
    complexity_level = Column(String(20), default='medium')
    cto_bto_mapping = Column(JSONB)  # {"CPU": {"option_1": "Intel Xeon Silver"}}
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### Data Input Schema Evolution

Phase 2 extends CSV schemas to support multi-line operations:

#### Enhanced `tasks_multi_line.csv` (Phase 2)
```csv
task_id,duration,offline_flag,adjustable,action_type,complexity_level,part_id,line_id,predecessors
1,274,0,1,"screw","simple","GPU_GTX3080","A",
2,223,1,0,"glue","medium","HDD_2TB","A",1
5,186,0,1,"clip","simple","RAM_16GB","B",
6,298,0,1,"screw","medium","CPU_XEON","B",5
```

#### Product Configuration JSON
```json
{
  "sku": "DL360_GEN10",
  "product_name": "HPE ProLiant DL360 Gen10",
  "cto_bto_mapping": {
    "CPU": {
      "option_1": "Intel Xeon Silver 4210",
      "option_2": "Intel Xeon Gold 6230"
    },
    "RAM": {
      "option_1": "16GB DDR4",
      "option_2": "32GB DDR4",
      "option_3": "64GB DDR4"
    },
    "STORAGE": {
      "option_1": "1TB HDD",
      "option_2": "500GB SSD",
      "option_3": "1TB SSD"
    }
  },
  "default_complexity": "medium"
}
```

#### Layout Definition JSON
```json
{
  "name": "Factory A Multi-Line Layout",
  "layout_type": "2d",
  "dimensions": {"width": 100, "depth": 50, "height": 10},
  "units": "meters",
  "stations": [
    {
      "station_code": "WS-001",
      "station_type": "assembly",
      "position": {"x": 0, "y": 0, "z": 0},
      "dimensions": {"width": 2, "depth": 1.5, "height": 2},
      "line_id": "A"
    },
    {
      "station_code": "WS-002",
      "station_type": "assembly", 
      "position": {"x": 4, "y": 0, "z": 0},
      "dimensions": {"width": 2, "depth": 1.5, "height": 2},
      "line_id": "A"
    }
  ],
  "connections": [
    {
      "from": "WS-001",
      "to": "WS-002", 
      "type": "conveyor",
      "length_meters": 3.5,
      "speed_mps": 0.5
    }
  ]
}
```
    description = Column(Text)
    data_json = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

class ProductConfig(Base):
    __tablename__ = 'product_configs'
    
    id = Column(Integer, primary_key=True)
    sku = Column(String(100), unique=True, nullable=False)
    product_name = Column(String(255))
    cto_bto_map = Column(Text)
    default_complexity = Column(String(50))
    created_at = Column(DateTime, default=datetime.now)

class OptimizationHistory(Base):
    __tablename__ = 'optimization_history'
    
    id = Column(Integer, primary_key=True)
    work_order_id = Column(String(100), nullable=False)
    optimization_goal = Column(String(50))
    num_lines = Column(Integer, default=1)
    result_json = Column(Text, nullable=False)
    solve_time_sec = Column(Float)
    created_at = Column(DateTime, default=datetime.now)
```

---

## Performance Optimization

### Multi-Line Solver Optimization

**Challenge**: 3D decision variables x[i][j][l] exponentially increase search space

**Solutions**:

1. **Symmetry Breaking**:
   ```python
   # Force line ordering: if line l is unused, line l+1 must be unused
   for l in range(num_lines - 1):
       model.Add(line_used[l] >= line_used[l + 1])
   ```

2. **Warm Start**:
   ```python
   # Use single-line solution as initial hint for multi-line
   single_line_solution = solve_single_line(tasks_df)
   
   # Distribute tasks across lines based on precedence clusters
   clusters = identify_precedence_clusters(precedences_df)
   for cluster_id, cluster_tasks in enumerate(clusters):
       suggested_line = cluster_id % num_lines
       for task in cluster_tasks:
           # Set hint for solver
           model.AddHint(x[(task, 0, suggested_line)], 1)
   ```

3. **Parallel Search**:
   ```python
   solver.parameters.num_search_workers = min(8, num_lines * 2)
   ```

### Database Query Optimization

```python
# Index on frequently queried columns
CREATE INDEX idx_layouts_name ON layouts(name);
CREATE INDEX idx_product_configs_sku ON product_configs(sku);
CREATE INDEX idx_optimization_history_work_order ON optimization_history(work_order_id);
```

---

## Due Date → UPH Conversion Algorithm (REQ #51 Extension)

### Overview

Convert customer `due_date` and `quantity` into minimum required UPH (Units Per Hour) for optimizer constraints. This ensures the optimizer generates solutions that meet delivery deadlines.

### Algorithm Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   Due Date → UPH Conversion Flow                            │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Input:                                                               │  │
│  │    - due_date: "2026-01-15"                                           │  │
│  │    - quantity: 500                                                    │  │
│  │    - available_hours_per_day: 16                                      │  │
│  │    - available_shifts: 2                                              │  │
│  │    - current_date: "2025-12-12"                                       │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                               │                                             │
│                               ▼                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Step 1: Calculate Available Production Days                         │  │
│  │    working_days = business_days(current_date, due_date)              │  │
│  │    # Excludes weekends, holidays per site calendar                   │  │
│  │    # Example: 2025-12-12 → 2026-01-15 = 23 working days              │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                               │                                             │
│                               ▼                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Step 2: Calculate Total Available Hours                             │  │
│  │    total_hours = working_days × available_hours_per_day              │  │
│  │    # 23 days × 16 hours = 368 hours                                  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                               │                                             │
│                               ▼                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Step 3: Calculate Minimum Required UPH                              │  │
│  │    min_required_uph = quantity / total_hours                         │  │
│  │    # 500 / 368 = 1.36 UPH (minimum)                                  │  │
│  │    # Add safety margin: min_required_uph × 1.1 = 1.50 UPH            │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                               │                                             │
│                               ▼                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Step 4: Convert to Optimizer Constraint                             │  │
│  │    max_takt_time = 3600 / min_required_uph                           │  │
│  │    # 3600 / 1.50 = 2400 seconds (40 minutes max takt)                │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Core Classes

```python
from datetime import datetime, date, timedelta
from typing import Optional, List
from pydantic import BaseModel

class DemandConstraint(BaseModel):
    sku: str
    quantity: int
    due_date: date
    priority: str = "medium"  # low, medium, high, critical

class UPHCalculationResult(BaseModel):
    sku: str
    quantity: int
    due_date: date
    working_days: int
    total_available_hours: float
    min_required_uph: float
    min_required_uph_with_margin: float
    max_takt_time_seconds: float
    feasibility: str  # "feasible", "at_risk", "infeasible"
```

### Optimizer Integration

```python
def apply_due_date_constraints(model, demands, site_config):
    """Add due date constraints to CP-SAT model."""
    
    converter = DueDateToUPHConverter(site_config["calendar"])
    constraint_data = converter.generate_optimizer_constraints(
        demands,
        site_config["available_hours_per_day"],
        site_config["site_id"]
    )
    
    # Add takt time upper bound constraint
    global_max_takt = constraint_data["global_max_takt"]
    
    # model.Add(takt_time <= global_max_takt)
    # This ensures solution meets all due dates
    
    # Priority-weighted objective
    for constraint in constraint_data["due_date_constraints"]:
        weight = constraint["priority_weight"]
        # Add to objective function with priority weight
```

---

## Offline Processing Architecture (REQ #4)

### Offline Task Management

Detailed architecture for offline task handling:

1. **Offline Task Identification**
   - `offline_flag=1` in tasks.csv
   - Separate optimization path
   
2. **Offline Station Assignment**
   - Assigned to virtual station `OFFLINE-001`
   - Not included in line takt calculation
   
3. **Offline Scheduling**
   - Can specify `offline_lead_time` (hours before assembly)
   - Integration with pre-assembly area

### Configuration Schema

```json
{
  "work_order_id": "WO_A",
  "enable_offline_handling": true,
  "offline_config": {
    "pre_assembly_hours": 4,
    "offline_station_capacity": 3,
    "parallel_offline": true
  }
}
```

---

## Phase 2 Roadmap

| Quarter | Milestone | Features |
|---------|-----------|----------|
| Q1 2026 | Core Phase 2 | Multi-line optimization, layout management, fishbone diagrams, product config |
| Q2 2026 | Advanced Features | NPI/MP workflow, demand input, per-plant thresholds |
| Q3 2026 | Integration | Advanced layout visualization, dashboard integration |

---

## Security Design

### Phase 2 Security Additions

1. **Database Access Control**:
   ```python
   # Use environment variables for credentials
   DATABASE_URL = os.getenv(
       'DATABASE_URL',
       'sqlite:///./line_balance.db'  # Default dev database
   )
   ```

2. **Layout Data Validation**:
   ```python
   class LayoutData(BaseModel):
       name: str = Field(max_length=255)
       stations: List[StationPosition]
       connections: List[Connection]
       
       @validator('stations')
       def validate_stations(cls, v):
           if len(v) > 100:
               raise ValueError("Max 100 stations allowed")
           return v
   ```

3. **SQL Injection Prevention**:
   ```python
   # Use ORM (SQLAlchemy) for all database queries
   # Parameterized queries only
   session.query(Layout).filter(Layout.name == user_input).first()
   ```

---

**Document Maintainer:** JASON YY, LIN  
**Last Updated:** 2025-11-12 
**Version:** 2.0.0-phase2
