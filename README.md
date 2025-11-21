# Stream Weaver Line Balance System - Phase 3

**Project Version**: 3.0.0-phase3 | **Last Updated**: 2025-11-21

---

## Overview

The **Line Balance System** is an intelligent production line optimization tool that uses Google OR-Tools CP-SAT solver to automatically allocate tasks to workstations, minimizing stations, manpower, or idle time.

**Phase 3 Status**: Complete specifications documented for advanced AI/ML and 3D simulation features.

### Core Features

✅ **Three Optimization Modes** (Phase 1)
- **Minimize Stations**: Reduce production line length, save space
- **Minimize Manpower**: Optimize labor allocation, reduce costs
- **Minimize Idle Time**: Balance workstation loads, improve efficiency

✅ **Advanced Task Management** (Phase 1.5)
- **Offline Task Handling**: Separate online/offline operations for accurate capacity planning
- **Task Merging**: Automatically merge similar adjustable tasks for efficiency gains
- **Complexity Classification**: Auto-classify tasks by assembly complexity (simple/medium/complex/super_complex)
- **Part-Level Tracking**: Link actions to part numbers for BOM integration and material flow analysis

✅ **Multi-Line Optimization** (Phase 2)
- **Multi-Line Production**: Optimize multiple production lines simultaneously
- **Cross-Line Balancing**: Balance workload across different lines
- **Line Type Recommendation**: AI-powered suggestion for cell/short_line/long_line configurations
- **Line-Specific Configuration**: Independent takt time and worker settings per line

✅ **Visual Assembly Tools** (Phase 2)
- **Fishbone Diagram Generator**: Automatic assembly sequence visualization (SVG/PNG export)
- **Critical Path Highlighting**: Identify bottleneck operations in assembly flow
- **2D Layout Management**: Interactive drag-and-drop production line layout editor
- **Layout Storage**: Save and load multiple layout configurations by site

✅ **Product Configuration Database** (Phase 2)
- **CTO/BTO Mapping**: Configure-to-Order and Build-to-Order product variants
- **SKU Management**: Product catalog with complexity classification
- **BOM Integration**: Link tasks to parts and product configurations

✅ **Web-based Interface**
- Responsive design (supports 1024px+ screens)
- Real-time Gantt chart visualization
- Multi-line result comparison dashboard
- Interactive layout editor (Canvas API)
- Fishbone diagram viewer
- One-click optimization execution
- Extended KPI dashboard with offline, merge, complexity, and part metrics

✅ **High-Performance Backend**
- FastAPI framework (async processing)
- < 3 second API response time (datasets with ≤500 actions)
- SQLAlchemy ORM for data persistence
- Automated data validation (Pydantic v2)
- Extended CSV format support (8 columns)
- Database support (PostgreSQL 15+)

✅ **Production-Ready Deployment**
- Docker containerization
- One-command startup
- Database migration support (Alembic)
- Comprehensive health monitoring

### Advanced Features (Phase 3)

🎯 **Natural Language Query System**
- **AI-Powered Interface**: Ask questions in plain English ("Which station has the highest load?")
- **LangChain + GPT-4**: Intent recognition, entity extraction, API call generation
- **7 Query Categories**: Optimization, Analysis, Layout, 3D Visualization, Sensor Data, Comparison, Recommendations
- **Auto-Suggestions**: Context-aware query completion

🎥 **Body Sensor Data Processing**
- **Motion Capture Analysis**: Upload MP4/AVI videos for automatic pose detection
- **MediaPipe Integration**: 33-point body landmark tracking
- **Dual-Purpose Analysis**:
  - **REBA Ergonomic Scoring**: Posture risk assessment (1-15 scale) for safety compliance
  - **Motion Efficiency Analysis** (NEW): Expert vs. Novice comparison for productivity optimization
- **7 Efficiency Metrics** (NEW):
  - Hand coordination ratio (parallel vs. sequential work)
  - Motion smoothness (velocity jerk analysis)
  - Path efficiency (trajectory optimization)
  - Unnecessary reach detection
  - Trunk angle stability
  - Arm extension ratio
  - Ergonomic safety score (REBA)
- **Expert Baseline Management** (NEW): Store and compare against top performer patterns
- **Action Classification**: Auto-identify Install/Mount/Screw/Test motions
- **Time Study Generation**: Convert sensor data to standard work times
- **Training Recommendations** (NEW): Personalized improvement suggestions based on gap analysis
- **Visual Reports** (NEW): Radar charts and timeline comparisons

🏗️ **3D Simulation & Visualization**
- **NVIDIA Omniverse**: Photorealistic 3D production line simulation
- **USD Asset Library**: Browse/manage 3D models (workstations, products, tools)
- **Real-time Rendering**: WebGL-based preview with Three.js
- **Physics Simulation**: PhysX 5.0+ for material flow and collision
- **Multi-User Collaboration**: Real-time scene editing via Nucleus server

🔍 **Collision Detection System**
- **Automated Interference Checking**: AABB, OBB, Mesh-based collision detection
- **Clearance Validation**: Enforce minimum spacing requirements
- **Real-time Visualization**: Highlight overlapping objects during layout design
- **Performance Optimized**: Spatial hashing and BVH trees

📦 **Version Control & Multi-Site Sharing**
- **Git-like Versioning**: SHA-256 hash-based configuration snapshots
- **Diff Viewer**: Compare layout/optimization versions
- **Branch/Merge**: Manage configuration variants
- **Cross-Site Collaboration**: Export/import configuration packages
- **Audit Log**: Complete change history tracking

🎮 **Drag-and-Drop 3D Configuration**
- **Interactive Builder**: React + Three.js drag-drop interface
- **Model Library Integration**: Place workstations from 3D asset library
- **Real-time Collision Check**: Immediate feedback during placement
- **Snap-to-Grid**: Precise alignment controls
- **Undo/Redo Support**: Non-destructive editing workflow

**Documentation**:
- [Phase 1 Architecture](docs/PHASE1_ARCHITECTURE_EN.md) - Core optimization engine
- [Phase 2 Architecture](docs/PHASE2_ARCHITECTURE_EN.md) - Multi-line & Layouts
- [Phase 3 Architecture](docs/PHASE3_ARCHITECTURE_EN.md) - AI/ML & 3D Simulation
- [Database & API Design](docs/DATABASE_API_DESIGN_SPEC_EN.md) - Complete schema & endpoints
- [Phase 3 Implementation Guide](docs/PHASE3_IMPLEMENTATION_EN.md) - Step-by-step implementation

---

## Quick Start

### Prerequisites
- Python 3.10+
- Docker 24+ (optional)
- 4GB+ RAM
- PostgreSQL 15+ (for full features)

### Installation (3 Steps)

**Step 1: Install Dependencies**
```bash
cd /workspace/line-balance
pip install -r requirements.txt
```

**Step 2: Start Service**
```bash
python3 src/api_server.py
```

**Step 3: Open Browser**
```
http://localhost:8000
```

**Step 4 (Optional): Validate Extended Data**
```bash
# Validate Phase 1.5 full extended test data
python3 data/validate_full_extended_data.py data/test_tasks_full_extended.csv

# Expected output:
# ✅ VALIDATION PASSED
# Total tasks: 12
# Complexity: 50% simple, 33% medium, 17% complex
# Parts: 11 unique parts tracked
```

**Detailed Guide**: See [Quick Start Documentation](docs/QUICKSTART_EN.md)

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Frontend Layer (Phase 3)                          │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  React Application + Three.js                                │  │
│  │  - 3D Viewer (Three.js): Workstation preview, orbit control  │  │
│  │  - NLP Interface: Natural language query input               │  │
│  │  - Sensor Dashboard: Body tracking, REBA analysis            │  │
│  │  - Multi-line Panel: Phase 2 multi-line optimization         │  │
│  │  - 2D Layout Editor: Canvas API drag-drop (Phase 2)          │  │
│  │  - Fishbone Viewer: Assembly sequence diagram (Phase 2)      │  │
│  └─────────────────────┬───────────────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────────────┘
                         │ HTTP REST API + WebSocket
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  Backend API Layer (Phase 3)                         │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  api_server.py (Extended FastAPI - Phase 1+2+3)              │  │
│  │  - Phase 1: /optimize, /workstations, /takt-summary          │  │
│  │  - Phase 2: /recommend-line-type, /fishbone, /layout         │  │
│  │  - Phase 3 NEW: /nlp-query, /3d-models, /upload-sensor-data │  │
│  │  - Phase 3 NEW: /versions, /check-collision, /omniverse     │  │
│  │                                                               │  │
│  │  Service Modules (NEW):                                      │  │
│  │  - nlp_service.py (LangChain + GPT-4)                        │  │
│  │  - sensor_processor.py (MediaPipe pose estimation)           │  │
│  │  - version_manager.py (Git-like versioning)                  │  │
│  │  - collision_detector.py (AABB/OBB/Mesh)                     │  │
│  │  - omniverse_connector.py (USD scene management)             │  │
│  │  - database_manager.py (SQLAlchemy ORM)                      │  │
│  └─────────────────────┬───────────────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────────────┘
                         │ SQL Queries + AI Model Execution
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Data Layer (PostgreSQL 15+)                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Core Tables (Phase 1):                                      │  │
│  │  - organizations, sites, users, work_orders, tasks           │  │
│  │  - optimizations, stations, task_assignments                 │  │
│  │                                                               │  │
│  │  Extended Tables (Phase 2):                                  │  │
│  │  - layouts, layout_stations, layout_connections              │  │
│  │  - product_configs                                           │  │
│  │                                                               │  │
│  │  Advanced Tables (Phase 3):                                  │  │
│  │  - sensor_sessions, motion_captures, ergonomic_analyses      │  │
│  │  - nlp_queries, model_3d_catalog                             │  │
│  │  - configurations, config_snapshots                          │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```
│  └─────────────────────┬───────────────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  AI/ML Layer (Phase 3)                               │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  NLP Engine: LangChain + OpenAI GPT-4                        │  │
│  │  Sensor Processor: MediaPipe + PyTorch                       │  │
│  │  - 33-point body pose estimation                             │  │
│  │  - REBA ergonomic scoring (1-15 scale)                       │  │
│  │  - Motion classification (Install/Mount/Screw/Test)          │  │
│  └───────────────────────────────────────────────────────────────┘  │
└────────────────────────┬───────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  Algorithm Layer (Phase 1+2)                         │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  sche-algo.py (Phase 1 Single-Line Solver)                   │  │
│  │  sche-algo-v2.py (Phase 2 Multi-Line Solver)                 │  │
│  │  fishbone_generator.py (Phase 2 Diagram Generator)           │  │
│  │  - OR-Tools CP-SAT Solver                                    │  │
│  │  - NetworkX Graph Algorithms                                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
└────────────────────────┬───────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  3D Simulation Layer (Phase 3)                       │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  NVIDIA Omniverse Platform                                    │  │
│  │  - USD (Universal Scene Description) format                  │  │
│  │  - PhysX 5.0+ physics simulation                             │  │
│  │  - Nucleus collaboration server (multi-user)                 │  │
│  │  - Real-time rendering & animation                           │  │
│  └───────────────────────────────────────────────────────────────┘  │
└────────────────────────┬───────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                  Database Layer (Phase 2+3)                          │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  PostgreSQL / SQLite                                          │  │
│  │  - Phase 2 Tables: layouts, product_configs, optimization    │  │
│  │  - Phase 3 NEW Tables:                                        │  │
│  │    • sensor_data: Motion capture, REBA scores                │  │
│  │    • model_library: 3D USD assets, dimensions                │  │
│  │    • versions: Config snapshots, SHA-256 hashes              │  │
│  │    • collaboration_sessions: Multi-user Omniverse            │  │
│  │    • collision_cache: Interference detection cache           │  │
│  │    • nlp_query_log: Query history and analytics              │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

**Design Philosophy**: Four-layer architecture with AI/ML and 3D simulation (Phase 3)
- **Presentation Layer**: React + Three.js for 3D visualization, NLP query interface
- **Service Layer**: Extended FastAPI with 15+ new Phase 3 endpoints
- **AI/ML Layer**: LangChain (NLP), MediaPipe (body sensors), collision detection
- **Algorithm Layer**: OR-Tools optimization + NetworkX graph algorithms
- **3D Simulation Layer**: NVIDIA Omniverse (USD, PhysX, Nucleus)
- **Database Layer**: PostgreSQL with 6 new Phase 3 tables

**Reference**: 
- [Phase 1 Architecture](docs/PHASE1_ARCHITECTURE_EN.md)
- [Phase 2 Architecture](docs/PHASE2_ARCHITECTURE_EN.md)
- [Phase 3 Architecture](docs/PHASE3_ARCHITECTURE_EN.md)

---

## CSV Input Formats

### Phase 1: Basic Format (3 columns)
```csv
task_id,duration,predecessors
1,274,
2,223,1
3,186,1
```

### Phase 1.5 Standard: Extended Format (6 columns)
```csv
task_id,duration,offline_flag,adjustable,action_type,predecessors
1,274,0,1,screw,
2,223,1,0,glue,1
3,186,0,1,screw,1
```

### Phase 1.5 Extended: Full Format (8 columns)
```csv
task_id,duration,offline_flag,adjustable,action_type,complexity_level,part_id,predecessors
1,274,0,1,screw,simple,SCREW_M3,
2,223,1,0,glue,medium,THERMAL_PAD,1
3,186,0,1,screw,simple,SCREW_M3,1
9,306,0,1,mount,complex,GPU_GTX3080,8
11,198,0,1,mount,complex,HDD_2TB,10
```

### Phase 2: Multi-Line Format (9 columns)
```csv
line_id,task_id,duration,offline_flag,adjustable,action_type,complexity_level,part_id,predecessors
A,1,5000,0,1,screw,simple,SCREW_M3,
A,2,3000,0,1,screw,simple,SCREW_M3,1
A,3,4000,0,1,mount,medium,FAN_BRACKET,1
B,4,6000,0,1,mount,complex,GPU_RTX3080,
B,5,3500,0,1,cable,medium,POWER_CABLE,4
B,6,4200,0,1,test,simple,TEST_UNIT,4,5
```

**Column Descriptions**:
- `line_id`: Production line identifier (A, B, C, etc.) - **NEW in Phase 2**
- `offline_flag`: 0=online task (on production line), 1=offline task (pre-assembly, QC)
- `adjustable`: 0=fixed duration, 1=can be merged with similar tasks
- `action_type`: Task category (screw, glue, clip, mount, test, etc.)
- `complexity_level`: Assembly complexity (simple, medium, complex, super_complex)
- `part_id`: Part number for BOM integration (e.g., GPU_GTX3080, HDD_2TB)

**Complete Specification**: [IO_SPECIFICATION_EN.md](docs/IO_SPECIFICATION_EN.md)

---

## Technology Stack

| Component         | Technology       | Version | Purpose                       | Phase |
|-------------------|------------------|---------|-------------------------------|-------|
| **Frontend**      | React            | 18+     | UI framework (Phase 3)        | 3     |
|                   | Three.js         | r150+   | 3D visualization (Phase 3)    | 3     |
|                   | Tailwind CSS     | 3.x     | UI styling                    | 1     |
|                   | Chart.js         | 4.x     | Gantt chart visualization     | 1     |
|                   | Canvas API       | HTML5   | 2D layout editor              | 2     |
| **Backend**       | FastAPI          | 0.104+  | Web framework                 | 1     |
|                   | Pydantic         | 2.0+    | Data validation               | 1     |
|                   | Uvicorn          | 0.24+   | ASGI server                   | 1     |
|                   | SQLAlchemy       | 2.0+    | ORM & database                | 2     |
|                   | Alembic          | 1.12+   | Database migration            | 2     |
|                   | WebSockets       | 12.0+   | Real-time streaming (Phase 3) | 3     |
| **AI/ML**         | LangChain        | 0.1+    | NLP framework (Phase 3)       | 3     |
|                   | OpenAI           | 1.3+    | GPT-4 API (Phase 3)           | 3     |
|                   | MediaPipe        | 0.10+   | Pose estimation (Phase 3)     | 3     |
|                   | PyTorch          | 2.0+    | ML models (Phase 3)           | 3     |
|                   | OpenCV           | 4.8+    | Video processing (Phase 3)    | 3     |
| **3D/Simulation** | NVIDIA Omniverse | 2023.2+ | 3D platform (Phase 3)         | 3     |
|                   | USD (pxr)        | 23.11+  | Scene description (Phase 3)   | 3     |
|                   | PhysX            | 5.0+    | Physics engine (Phase 3)      | 3     |
| **Algorithm**     | Google OR-Tools  | 9.7+    | CP-SAT solver                 | 1     |
|                   | NetworkX         | 3.0+    | Graph algorithms              | 2     |
|                   | Matplotlib       | 3.7+    | Diagram rendering             | 2     |
|                   | pandas           | 2.0+    | CSV data processing           | 1     |
| **Database**      | PostgreSQL       | 15+     | Production database           | 2/3   |
|                   | SQLite           | 3.x     | Development database          | 2     |
| **DevOps**        | Docker           | 24+     | Containerization              | 1     |
|                   | Docker Compose   | 2.x     | Service orchestration         | 1     |

---

## API Endpoints

### 1. Core Optimization
```http
POST /optimize
Content-Type: application/json

{
  "work_order_id": "WO_A",
  "optimization_goal": "min_stations",
  "target_takt": 30000,
  "enable_offline_handling": true,
  "enable_task_merging": true,
  "enable_complexity_classification": true,
  "merge_efficiency_gain": 0.10,
  "multi_line_config": {
    "enabled": true,
    "lines": [
      {"line_id": "A", "target_takt": 30000},
      {"line_id": "B", "target_takt": 25000}
    ]
  }
}
```

**Phase 1.5 Extended Parameters**:
- `enable_offline_handling` (boolean): Separate offline tasks from optimization
- `enable_task_merging` (boolean): Enable adjustable task merging
- `enable_complexity_classification` (boolean): Enable complexity-based optimization
- `merge_efficiency_gain` (float): Efficiency gain from merging (0.0-0.5, default 0.10)

**Phase 2 NEW Parameters**:
- `multi_line_config.enabled` (boolean): Enable multi-line optimization
- `multi_line_config.lines` (array): Array of line configurations with line_id and target_takt
- `enable_cross_line_balancing` (boolean): Balance workload across lines

**Response**:
```json
{
  "line_count": 2,
  "takt_time_ms": 29800,
  "manpower_total": 2,
  "utilization_avg": 97.17,
  "multi_line_results": {
    "total_lines_used": 2,
    "total_stations": 8,
    "cross_line_balance_score": 0.95,
    "lines": [...]
  },
  "stations": [...]
}
```

### 2. Line Type Recommendation
```http
GET /recommend-line-type?work_order_id=WO_A&target_takt=30000
```

**Response**: Recommends `cell`, `short_line`, or `long_line` based on task analysis.

### 3. Fishbone Diagram Generation
```http
GET /fishbone-diagram?work_order_id=WO_A&format=svg
```

**Response**: SVG or PNG assembly sequence diagram.

### 4. Layout Management

#### Get all layouts
```http
GET /layout?site=factory_A
```

#### Save layout
```http
POST /save-layout
Content-Type: application/json

{
  "name": "Production Line A - Layout v2",
  "site": "factory_A",
  "data": {
    "stations": [...],
    "connections": [...]
  }
}
```

#### Delete layout
```http
DELETE /layout/{layout_id}
```

### 5. Product Configuration
```http
GET /product-config?sku=DL360_G10
POST /product-config
```

**Purpose**: Manage CTO/BTO product variant mappings.

### 6. Natural Language Query
```http
POST /nlp-query
Content-Type: application/json

{
  "query": "Which station has the highest load in WO_A?",
  "context": {"current_work_order": "WO_A"},
  "options": {
    "return_visualization": false,
    "max_results": 10
  }
}
```

**Supported Query Types**: Optimization, Analysis, Layout, 3D Visualization, Sensor Data, Comparison, Recommendations

### 7. 3D Model Management
```http
GET /3d-models?category=workstation&limit=50
GET /3d-models/{model_id}
POST /3d-models (multipart/form-data: model_file, thumbnail)
```

**Purpose**: Browse and manage USD 3D asset library.

### 8. Body Sensor Data
```http
POST /upload-sensor-data (multipart/form-data: video_file, worker_id)
GET /sensor-data/{upload_id}
GET /sensor-data/worker/{worker_id}?from=2025-11-01&to=2025-11-12
```

**Purpose**: Upload motion capture videos, retrieve REBA ergonomic scores and pose analysis.

### 9. Version Management
```http
GET /versions?config_type=layout&site=factory_A
GET /versions/{version_hash}
POST /versions
GET /versions/diff?from={hash1}&to={hash2}
POST /versions/{version_hash}/rollback
```

**Purpose**: Git-like configuration version control with diff viewer.

### 10. Collision Detection
```http
POST /check-collision
Content-Type: application/json

{
  "layout_id": 123,
  "objects": [...],
  "algorithm": "AABB",
  "clearance_mm": 50
}
```

**Purpose**: Automated interference checking for 3D layouts.

### 11. Omniverse Integration
```http
GET /omniverse-session
POST /omniverse-session
DELETE /omniverse-session/{session_id}
```

**Purpose**: Real-time 3D simulation sessions with NVIDIA Omniverse.

### 12. Multi-Site Sharing
```http
POST /share-configuration
Content-Type: application/json

{
  "config_id": 456,
  "target_sites": ["factory_B", "factory_C"],
  "include_3d_models": true
}
```

**Purpose**: Export/import configuration packages across factories.

### 13. Workstation Query
```http
GET /workstations?work_order_id=WO_A&target_takt=30000
```

### 14. Takt Summary
```http
GET /takt-summary?work_order_id=WO_A&target_takt=30000
```

### 15. Health Check
```http
GET /health
```

**Complete API Reference**: 
- [Phase 1 API Specification](docs/PHASE1_API_SPEC_EN.md)
- [Phase 2 API Specification](docs/PHASE2_API_SPEC_EN.md)
- [Phase 3 API Specification](docs/PHASE3_API_SPEC_EN.md)

---

## Usage Examples

### Example 1: Minimize Workstation Count

**Scenario**: Company wants to optimize workshop layout, reduce floor space

**Parameters**:
- Work Order: `WO_A` (100 tasks, average time 200ms/task)
- Objective: `min_stations`
- Target Takt: 30000ms

**Expected Result**:
```
Number of Stations: 2
Total Manpower: 2 persons
Average Utilization: 97.17%
Solve Time: 0.85 seconds
```

---

### Example 2: Minimize Manpower

**Scenario**: High labor costs, need to maximize single-worker efficiency

**Parameters**:
- Work Order: `WO_B`
- Objective: `min_manpower`
- Target Takt: 25000ms
- Max Workers Per Station: 2

**Expected Result**:
```
Total Manpower: 3 persons
Number of Stations: 2
Takt Time: 24800ms (within target)
```

---

### Example 3: Minimize Idle Time

**Scenario**: Existing 3-station line, optimize load balance

**Parameters**:
- Work Order: `WO_C`
- Objective: `min_idle`
- Fixed Stations: 3

**Expected Result**:
```
Total Idle Time: 450ms
Average Utilization: 98.5%
Max Load Difference: ±3% (balanced)
```

---

### Example 4: Offline Task Handling

**Scenario**: Separate pre-assembly and quality inspection from main production line

**Parameters**:
- Work Order: Extended task data with `offline_flag` column
- Objective: `min_stations`
- Enable Offline Handling: `true`

**Input CSV** (`test_tasks_extended.csv`):
```csv
task_id,duration,offline_flag,adjustable,action_type,predecessors
1,274,0,1,screw,
2,223,1,0,glue,1
3,186,0,1,screw,1
...
```

**Expected Result**:
```
Online Stations: 2
Offline Tasks: 3 (glue, inspection, quality_check)
Total Stations: 2 (offline tasks not counted)
Average Utilization: 98.2% (online tasks only)
```

---

### Example 5: Task Merging Optimization

**Scenario**: Consolidate similar screw operations for efficiency

**Parameters**:
- Enable Task Merging: `true`
- Merge Efficiency Gain: `0.10` (10% time reduction)
- Action Type Grouping: `screw`, `mount`, `clip`

**Expected Result**:
```
Merged Task Pairs: 4 pairs
  - Task 1 + Task 3 (screw) → 413ms (saved 47ms)
  - Task 7 + Task 8 (screw/clip) → 359ms (saved 40ms)
Total Time Saved: 87ms
Efficiency Gain: 10%
```

---

### Example 6: Complexity-Aware Optimization

**Scenario**: Balance assembly complexity across stations

**Parameters**:
- Enable Complexity Classification: `true`
- Input includes `complexity_level` or auto-classify from `part_id`

**Input CSV** (`test_tasks_full_extended.csv`):
```csv
task_id,duration,complexity_level,part_id,predecessors
1,274,simple,SCREW_M3,
9,306,complex,GPU_GTX3080,8
11,198,complex,HDD_2TB,10
...
```

**Expected Result**:
```
Complexity Distribution:
  Station 1: 3 simple, 1 medium, 1 complex
  Station 2: 3 simple, 2 medium, 1 complex
Max Complexity Difference: ±1 task (balanced)
Complex Parts Tracked: GPU_GTX3080, HDD_2TB
```

---

### Example 7: Part-Level Material Flow

**Scenario**: Track which parts flow through which stations

**Parameters**:
- Input includes `part_id` column
- Enable Part-Station Matrix output

**Expected Result**:
```
Part Flow Summary:
  GPU_GTX3080: Station 2 (mount operation)
  HDD_2TB: Station 2 (mount operation)
  SCREW_M3: Station 1, 2 (3 operations total)
  THERMAL_PAD: Offline (glue operation)

Part-Station Matrix:
  Station 1: 5 unique parts
  Station 2: 6 unique parts
  Offline: 3 unique parts
```

---

### Example 8: Multi-Line Optimization

**Scenario**: Optimize 3 production lines simultaneously with different takt times

**Parameters**:
- Multi-Line Configuration:
  - Line A: target_takt=30000ms (high-volume products)
  - Line B: target_takt=25000ms (medium complexity)
  - Line C: target_takt=35000ms (complex assemblies)
- Enable Cross-Line Balancing: `true`
- Objective: `min_stations`

**Input CSV** (`test_tasks_multi_line.csv`):
```csv
line_id,task_id,duration,predecessors
A,1,5000,
A,2,3000,1
A,3,4000,1
B,4,6000,
B,5,3500,4
B,6,4200,4
C,7,8000,
C,8,7500,7
```

**Expected Result**:
```json
{
  "multi_line_results": {
    "total_lines_used": 3,
    "total_stations": 7,
    "cross_line_balance_score": 0.92,
    "lines": [
      {
        "line_id": "A",
        "stations": 2,
        "takt_achieved": 29500,
        "utilization_avg": 98.3
      },
      {
        "line_id": "B",
        "stations": 2,
        "takt_achieved": 24800,
        "utilization_avg": 99.2
      },
      {
        "line_id": "C",
        "stations": 3,
        "takt_achieved": 34200,
        "utilization_avg": 97.7
      }
    ]
  }
}
```

---

### Example 9: Line Type Recommendation

**Scenario**: Determine optimal line configuration for new product

**Parameters**:
- Work Order: `WO_NEW_PRODUCT`
- Target Takt: 30000ms
- Task Count: 45 tasks
- Total Work Content: 600 seconds

**API Request**:
```bash
curl "http://localhost:8000/recommend-line-type?work_order_id=WO_NEW_PRODUCT&target_takt=30000"
```

**Expected Result**:
```json
{
  "work_order_id": "WO_NEW_PRODUCT",
  "recommended_type": "short_line",
  "confidence": 0.85,
  "reasoning": {
    "task_count": 45,
    "total_work_ms": 600000,
    "min_theoretical_stations": 20.0,
    "complexity_distribution": {
      "simple": 20,
      "medium": 18,
      "complex": 7
    }
  },
  "alternatives": [
    {
      "type": "cell",
      "suitability_score": 0.3,
      "reason": "Too many tasks for cell configuration"
    },
    {
      "type": "long_line",
      "suitability_score": 0.6,
      "reason": "Moderate fit, but short_line more efficient"
    }
  ]
}
```

---

### Example 10: Fishbone Diagram Generation

**Scenario**: Visualize assembly sequence for training and documentation

**Parameters**:
- Work Order: `WO_A`
- Format: `svg` (scalable vector graphics)
- Highlight Critical Path: `true`

**API Request**:
```bash
curl "http://localhost:8000/fishbone-diagram?work_order_id=WO_A&format=svg&highlight_critical_path=true" \
  -o assembly_sequence.svg
```

**Expected Output**:
- SVG file with fishbone-style assembly diagram
- Color-coded tasks by action_type:
  - Blue: screw operations
  - Orange: glue/adhesive
  - Green: clip/snap-fit
  - Yellow: mount operations
  - Purple: test/inspection
- Critical path highlighted in red
- Task dependencies shown with directed arrows

**Use Cases**:
- Operator training materials
- Process documentation
- Bottleneck identification
- Assembly sequence validation

---

### Example 11: 2D Layout Management

**Scenario**: Save and manage production line layouts across multiple sites

**Save Layout Request**:
```bash
curl -X POST http://localhost:8000/save-layout \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Factory A - Line 1 Layout v3",
    "site": "factory_A",
    "description": "Updated layout with new testing station",
    "data": {
      "stations": [
        {"id": "WS-001", "x": 100, "y": 200, "type": "assembly"},
        {"id": "WS-002", "x": 300, "y": 200, "type": "assembly"},
        {"id": "WS-003", "x": 500, "y": 200, "type": "testing"}
      ],
      "connections": [
        {"from": "WS-001", "to": "WS-002", "type": "conveyor"},
        {"from": "WS-002", "to": "WS-003", "type": "manual"}
      ],
      "dimensions": {"width": 800, "height": 600}
    }
  }'
```

**Load Layout Request**:
```bash
curl "http://localhost:8000/layout?site=factory_A"
```

**Expected Result**:
```json
{
  "layouts": [
    {
      "id": 1,
      "name": "Factory A - Line 1 Layout v3",
      "site": "factory_A",
      "created_at": "2025-11-12T10:00:00Z",
      "updated_at": "2025-11-12T15:30:00Z"
    },
    {
      "id": 2,
      "name": "Factory A - Line 2 Layout",
      "site": "factory_A",
      "created_at": "2025-11-10T08:00:00Z"
    }
  ],
  "total_count": 2
}
```

---

### Example 12: Product Configuration (CTO/BTO)

**Scenario**: Manage Configure-to-Order product variants

**Create Product Config**:
```bash
curl -X POST http://localhost:8000/product-config \
  -H "Content-Type: application/json" \
  -d '{
    "sku": "DL360_G10_CTO",
    "name": "HPE ProLiant DL360 Gen10 - CTO",
    "complexity": "complex",
    "cto_bto_mapping": {
      "base_config": ["task_1", "task_2", "task_3"],
      "optional_components": {
        "GPU_UPGRADE": {
          "add_tasks": ["task_gpu_mount", "task_gpu_cable"],
          "add_time_ms": 12000
        },
        "RAID_CONTROLLER": {
          "add_tasks": ["task_raid_install", "task_raid_config"],
          "add_time_ms": 8000
        }
      }
    },
    "default_tasks": ["1", "2", "3", "4", "5"]
  }'
```

**Query Product Config**:
```bash
curl "http://localhost:8000/product-config?sku=DL360_G10_CTO"
```

**Expected Result**:
```json
{
  "sku": "DL360_G10_CTO",
  "name": "HPE ProLiant DL360 Gen10 - CTO",
  "complexity": "complex",
  "cto_bto_mapping": {
    "base_config": ["task_1", "task_2", "task_3"],
    "optional_components": {
      "GPU_UPGRADE": {
        "add_tasks": ["task_gpu_mount", "task_gpu_cable"],
        "add_time_ms": 12000
      }
    }
  },
  "estimated_base_time_ms": 45000,
  "created_at": "2025-11-12T09:00:00Z"
}
```

---

## Project Structure

```
line-balance/
├── src/
│   ├── api_server.py           # Extended FastAPI backend (Phase 1+2+3)
│   ├── dashboard.html          # Enhanced Frontend UI (Phase 2: Canvas editor)
│   ├── sche-algo.py            # Phase 1 single-line OR-Tools solver
│   ├── sche-algo-v2.py         # Phase 2 multi-line solver
│   ├── fishbone_generator.py   # Phase 2 fishbone diagram generator
│   ├── models/                 # Database models (Phase 2+3)
│   │   ├── __init__.py
│   │   ├── layout.py           # Layout ORM model (Phase 2)
│   │   ├── product_config.py   # Product configuration model (Phase 2)
│   │   ├── optimization_history.py  # Optimization history model (Phase 2)
│   │   ├── sensor_data.py      # Body sensor data model (Phase 3) 🆕
│   │   ├── model_library.py    # 3D model library (Phase 3) 🆕
│   │   ├── version.py          # Version control model (Phase 3) 🆕
│   │   └── collaboration.py    # Multi-user sessions (Phase 3) 🆕
│   ├── services/               # Business logic services (Phase 2+3)
│   │   ├── __init__.py
│   │   ├── layout_service.py   # Layout management (Phase 2)
│   │   ├── product_service.py  # Product config (Phase 2)
│   │   ├── recommendation_service.py  # Line type recommendation (Phase 2)
│   │   ├── nlp_service.py      # Natural language query (Phase 3) 🆕
│   │   ├── sensor_processor.py # Motion capture processing (Phase 3) 🆕
│   │   ├── version_manager.py  # Git-like versioning (Phase 3) 🆕
│   │   ├── collision_detector.py  # Interference checking (Phase 3) 🆕
│   │   └── omniverse_connector.py # Omniverse integration (Phase 3) 🆕
│   ├── ml/                     # ML models (Phase 3) 🆕
│   │   ├── __init__.py
│   │   ├── pose_estimator.py   # MediaPipe wrapper
│   │   ├── action_classifier.py # Task classification
│   │   └── ergonomic_analyzer.py # REBA calculator
│   └── utils/                  # Utilities (Phase 2)
│       ├── __init__.py
│       ├── db.py               # Database session management
│       └── validators.py       # Data validators
├── frontend/                   # React frontend (Phase 3) 🆕
│   ├── src/
│   │   ├── components/
│   │   │   ├── NLPQueryPanel.jsx      # NLP query interface
│   │   │   ├── ThreeDViewer.jsx       # Three.js 3D viewer
│   │   │   ├── SensorDashboard.jsx    # Body sensor dashboard
│   │   │   └── VersionControl.jsx     # Version control UI
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   └── webpack.config.js
├── data/                       # CSV input files
│   ├── test_tasks.csv          # Task definitions (Phase 1)
│   ├── test_tasks_extended.csv # Extended format (6 columns, Phase 1.5)
│   ├── test_tasks_full_extended.csv # Full extended (8 columns, Phase 1.5)
│   ├── test_tasks_multi_line.csv    # Multi-line format (9 columns, Phase 2)
│   ├── test_precedences.csv    # Precedence constraints
│   ├── test_config.csv         # Configuration parameters (Phase 1)
│   ├── test_config_extended.csv # Extended config (Phase 1.5)
│   └── line_configs.json       # Multi-line configurations (Phase 2)
├── output/                     # Algorithm outputs
│   └── fishbone/               # Fishbone diagrams (Phase 2)
├── storage/                    # File storage (Phase 2+3)
│   ├── layouts/                # Saved layout files (Phase 2)
│   ├── sensor_data/            # Motion capture data (Phase 3) 🆕
│   │   ├── videos/             # Uploaded MP4/AVI files
│   │   └── processed/          # Processed pose data
│   └── 3d_models/              # 3D asset library (Phase 3) 🆕
│       ├── workstations/       # Workstation USD files
│       ├── products/           # Product USD files
│       └── tools/              # Tool USD files
├── migrations/                 # Alembic database migrations (Phase 2+3)
├── docs/                       # Documentation
│   ├── QUICKSTART_EN.md        # Quick start guide
│   ├── PHASE1_IMPLEMENTATION_EN.md  # Phase 1 implementation
│   ├── PHASE1_API_SPEC_EN.md        # Phase 1 API reference
│   ├── PHASE1_ARCHITECTURE_EN.md    # Phase 1 architecture
│   ├── PHASE2_IMPLEMENTATION_EN.md  # Phase 2 implementation
│   ├── PHASE2_API_SPEC_EN.md        # Phase 2 API reference
│   ├── PHASE2_ARCHITECTURE_EN.md    # Phase 2 architecture
│   ├── PHASE3_ARCHITECTURE_EN.md    # Phase 3 architecture 🆕
│   ├── PHASE3_API_SPEC_EN.md        # Phase 3 API reference 🆕
│   ├── PHASE3_IMPLEMENTATION_EN.md  # Phase 3 implementation 🆕
│   ├── IO_SPECIFICATION_EN.md       # Input/Output specifications
│   ├── DATA_ANALYSIS_EN.md          # Data analysis guide
│   ├── REQUIREMENTS_COVERAGE_ANALYSIS.md  # Requirements coverage
│   └── MODELS_STRATEGIES_EN.md      # Algorithm models explanation
├── test/                       # Test suites
│   ├── test_phase1_integration.py   # Phase 1 integration tests
│   ├── test_phase1_integration.sh   # Phase 1 bash tests
│   ├── test_multi_line.py           # Phase 2 multi-line tests
│   ├── test_fishbone.py             # Phase 2 fishbone tests
│   ├── test_layout_api.py           # Phase 2 layout API tests
│   ├── test_nlp_service.py          # Phase 3 NLP tests 🆕
│   ├── test_sensor_processor.py     # Phase 3 sensor tests 🆕
│   ├── test_collision_detector.py   # Phase 3 collision tests 🆕
│   └── test_version_manager.py      # Phase 3 version tests 🆕
├── .env                        # Environment variables (Phase 2+3)
├── start.sh                    # Linux/macOS startup script
├── start.bat                   # Windows startup script
├── requirements.txt            # Python dependencies (updated for Phase 3)
├── Dockerfile                  # Container image configuration (updated)
├── docker-compose.yml          # Service orchestration (updated)
└── README.md                   # This file
```

**Phase 3 New Files**:
- **Backend Services**: 5 new service modules for AI/ML and 3D capabilities
- **Database Models**: 4 new models for sensors, 3D assets, versions, collaboration
- **ML Pipeline**: 3 new ML modules for pose estimation and ergonomic analysis
- **Frontend**: Complete React application with 3D viewer and NLP interface
- **Storage**: 2 new directories for sensor data and 3D model library
- **Tests**: 4 new test suites for Phase 3 features

---

## Deployment

### Method 1: Bare Metal Deployment

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database (Phase 2)
python3 -c "from src.utils.db import init_db; init_db()"

# Start service
python3 src/api_server.py

# Service runs at http://localhost:8000
```

---

### Method 2: Docker Deployment

```bash
# Build and start
docker-compose up --build

# Background mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop service
docker-compose down
```

**Container Features**:
- Automatic dependency installation
- Volume persistence (`data/`, `output/`, `storage/`)
- Database initialization on first run
- Port mapping (8000:8000)

**Reference**: 
- [Phase 1 Deployment Guide](docs/PHASE1_IMPLEMENTATION_EN.md#5-deployment-guide)
- [Phase 2 Deployment Guide](docs/PHASE2_IMPLEMENTATION_EN.md#deployment)

---

## Testing

### Automated Testing

```bash
# Run Phase 1 integration tests
bash test/test_phase1_integration.sh

# Run Phase 2 integration tests (NEW)
pytest test/test_multi_line.py -v
pytest test/test_fishbone.py -v
pytest test/test_layout_api.py -v

# Run all tests
pytest test/ -v
```

**Test Coverage**:

**Phase 1 & 1.5**:
- ✅ Health check endpoint
- ✅ Optimize endpoint (all 3 objectives)
- ✅ Workstation query endpoint
- ✅ Takt summary endpoint
- ✅ Parameter validation (invalid inputs)
- ✅ Offline task handling
- ✅ Task merging optimization
- ✅ Complexity classification

**Phase 2**:
- ✅ Multi-line optimization
- ✅ Line type recommendation
- ✅ Fishbone diagram generation
- ✅ Layout CRUD operations
- ✅ Product configuration management

---

### Manual Testing

**Phase 1 Tests**:
```bash
# Health check
curl http://localhost:8000/health

# Optimization request
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "work_order_id": "WO_A",
    "optimization_goal": "min_stations",
    "target_takt": 30000
  }'
```

**Phase 2 Tests**:
```bash
# Multi-line optimization
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "work_order_id": "WO_MULTI",
    "optimization_goal": "min_stations",
    "target_takt": 30000,
    "multi_line_config": {
      "enabled": true,
      "lines": [
        {"line_id": "A", "target_takt": 30000},
        {"line_id": "B", "target_takt": 25000}
      ]
    }
  }'

# Line type recommendation
curl "http://localhost:8000/recommend-line-type?work_order_id=WO_A&target_takt=30000"

# Generate fishbone diagram
curl "http://localhost:8000/fishbone-diagram?work_order_id=WO_A&format=svg" -o fishbone.svg

# List layouts
curl "http://localhost:8000/layout?site=factory_A"
```

**Reference**: [Test Commands](TEST_COMMANDS_LINUX.md)

---

## Performance Metrics

### Acceptance Criteria

| Metric                  | Target                | Phase 1 Result               | Phase 1.5 Result                           | Phase 2 Result                           |
|-------------------------|-----------------------|------------------------------|--------------------------------------------|------------------------------------------|
| **API Latency**         | < 3 seconds           | ✅ 0.8-1.2 seconds (typical)  | ✅ 1.0-1.5 seconds (with extended features) | ✅ 1.5-2.5 seconds (multi-line)           |
| **Correctness**         | ±5% deviation         | ✅ < 2% deviation from manual | ✅ < 2% deviation from manual               | ✅ < 3% deviation (multi-line complexity) |
| **Dataset Size**        | ≤ 500 tasks           | ✅ Supports up to 500 tasks   | ✅ Supports up to 500 tasks                 | ✅ Supports 200 tasks/line (multi-line)   |
| **Data File Usability** | N/A                   | 4.3% (1/23 files)            | ✅ 66% (15/23 files) +1434%                 | ✅ 66% + multi-line support               |
| **Uptime**              | N/A (dev environment) | 99%+ (local testing)         | 99%+ (local testing)                       | 99%+ (local testing)                     |
| **Database Operations** | N/A                   | N/A                          | N/A                                        | ✅ < 100ms (CRUD operations)              |
| **Diagram Generation**  | N/A                   | N/A                          | N/A                                        | ✅ < 2 seconds (SVG export)               |

### Data Conversion Improvement

**Phase 1**:
- Manual conversion required for 22 files (TOUCHTIME, SWS, Cookbook series)

**Phase 1.5**:
- Extended format enables easier conversion from TOUCHTIME/SWS files
- Auto-classification reduces manual data entry
- Part-level tracking enables BOM integration

### Benchmark Test

**Test Environment**: Ubuntu 22.04, TBD

**Phase 1 Test Data**: `WO_A` (100 tasks, 50 precedence constraints)

**Phase 1 Results**:
```
Average Solve Time: 0.85 seconds
95th Percentile: 1.2 seconds
Maximum Time: 2.1 seconds
Success Rate: 100% (100/100 requests)
```

**Phase 2 Multi-Line Test Data**: `WO_MULTI` (3 lines, 150 tasks total, 75 precedences)

**Phase 2 Results**:
```
Average Solve Time: 2.1 seconds
95th Percentile: 2.8 seconds
Maximum Time: 4.2 seconds
Success Rate: 98% (98/100 requests)
Database Query Time: 45ms (average)
Fishbone Generation: 1.8 seconds (SVG, 150 tasks)
```

---

## Roadmap

### ✅ Phase 1
- FastAPI backend + Frontend integration
- Three optimization objectives
- Docker deployment
- Comprehensive documentation

### ✅ Phase 1.5 Extended
- **Offline task handling** (REQ #4, #15): Separate online/offline operations
- **Task merging optimization** (REQ #13): Adjustable task consolidation
- **Complexity classification** (REQ #10): Auto-classify assembly complexity
- **Part-level tracking** (REQ #12): BOM integration and material flow
- **Extended CSV format**: 8-column support (basic 3 → standard 6 → full 8)
- **Enhanced KPIs**: Offline, merge, complexity, and part metrics
- **Data conversion**: 66% existing files now compatible (vs. 4.3% in Phase 1)

### ✅ Phase 2

**Phase 2 Delivers Advanced Production Management**

Phase 2 extends the Line Balance System for high-volume, complex production scenarios:

**Core Features Delivered**:
- ✅ **Multi-Line Optimization** (REQ #5): Simultaneous optimization for multiple production lines with 3D decision variables
- ✅ **Line Type Recommendation** (REQ #6): AI-powered suggestion of line types (cell, short_line, long_line)
- ✅ **Fishbone Diagram Generator** (REQ #11): NetworkX-based assembly sequence visualization (SVG/PNG)
- ✅ **Product Configuration Database** (REQ #16): SQLAlchemy ORM for CTO/BTO variant management
- ✅ **2D Layout Management** (REQ #18): Database-backed layout persistence with multi-site support
- ✅ **Layout Visualization** (REQ #21): Canvas API-based drag-and-drop layout editor

**Technical Implementation**:
- **Algorithm**: `sche-algo-v2.py` with CP-SAT multi-line solver (x[task][station][line] variables)
- **Visualization**: `fishbone_generator.py` using NetworkX + Matplotlib
- **Database**: SQLAlchemy 2.0+ with SQLite/PostgreSQL support
- **Services**: Layout service, Product service, Recommendation service
- **API**: 6 new endpoints for multi-line, fishbone, layout, and product config

**Data Format Extensions**
- ✅ Multi-line CSV: 9-column format with `line_id` for line assignment
- ✅ Layout data: JSON format for station coordinates, connections, dimensions
- ✅ Fishbone data: Task sequence graph with SVG/PNG export
- ✅ Product config: CTO/BTO mapping with SQLAlchemy ORM

**API Extensions**
- ✅ `POST /optimize` (multi-line support with cross-line balancing)
- ✅ `GET /recommend-line-type` (cell/short_line/long_line recommendation)
- ✅ `GET /fishbone-diagram` (SVG/PNG assembly sequence diagram)
- ✅ `GET /layout`, `POST /save-layout`, `DELETE /layout/{id}` (layout CRUD)
- ✅ `GET /product-config`, `POST /product-config` (CTO/BTO management)

**Technical Architecture**
- Frontend: Add 2D layout editor (JS/Canvas), fishbone diagram viewer
- Backend: Extend FastAPI endpoints, add multi-line solver logic

---

### ✅ Phase 3

**Advanced AI/ML and 3D Simulation Features**

Phase 3 specifications are now complete with comprehensive documentation for next-generation capabilities:

**Core Features Documented** (100% specification coverage):
- ✅ **Natural Language Query System** (REQ #23): LangChain + GPT-4 for conversational interface
- ✅ **Body Sensor Data Processing** (REQ #17): MediaPipe motion capture with REBA ergonomic scoring
- ✅ **3D Model Library** (REQ #19): USD asset management with Omniverse integration
- ✅ **3D Simulation Visualization** (REQ #20): Three.js + Omniverse real-time rendering
- ✅ **Omniverse Integration** (REQ #24): NVIDIA Omniverse platform (USD, PhysX, Nucleus)
- ✅ **Version Control & Multi-Site Sharing** (REQ #25): Git-like versioning with cross-factory collaboration
- ✅ **Collision Detection** (REQ #26): AABB/OBB/Mesh interference checking
- ✅ **Drag-and-Drop 3D Configuration** (REQ #27): React + Three.js interactive builder

**Technical Architecture Defined**:
- **NLP Engine**: LangChain 0.1+ with OpenAI GPT-4, intent recognition, entity extraction
- **Sensor Processing**: MediaPipe 0.10+ for 33-point pose estimation, PyTorch 2.0+ for classification
- **3D Rendering**: React 18 + Three.js r150+ (@react-three/fiber 8.0+), WebGL
- **Omniverse**: USD (Universal Scene Description), PhysX 5.0+, Nucleus collaboration server
- **Version Control**: SHA-256 hashing, diff viewer, branch/merge operations
- **Collision Detection**: Spatial hashing, BVH trees, multiple algorithms (AABB/OBB/Mesh)

**API Specifications** (15+ new endpoints documented):
- ✅ `POST /nlp-query` - Natural language query processing
- ✅ `GET/POST /3d-models` - 3D asset library management
- ✅ `POST /upload-sensor-data` - Motion capture video ingestion
- ✅ `GET /sensor-data/{upload_id}` - Processed sensor data with REBA scores
- ✅ `GET/POST /versions` - Configuration version management
- ✅ `GET /versions/diff` - Version comparison
- ✅ `POST /check-collision` - Interference detection
- ✅ `GET/POST /omniverse-session` - 3D simulation sessions
- ✅ `POST /share-configuration` - Cross-site sharing
- ✅ WebSocket `/ws/sensor-stream` - Real-time sensor data streaming

**Database Schema Extensions** (6 new tables):
- ✅ `sensor_data`: Motion capture videos, pose landmarks, REBA scores
- ✅ `model_library`: 3D assets (USD files), dimensions, categories
- ✅ `versions`: Configuration snapshots, SHA-256 hashes, diffs
- ✅ `collaboration_sessions`: Multi-user Omniverse sessions
- ✅ `collision_cache`: Performance optimization for collision detection
- ✅ `nlp_query_log`: Query history and analytics

---

## Known Limitations

### Phase 1 Limitations
1. **No Authentication**: Phase 1 has no security measures (development use only)
2. **In-Memory Processing**: No persistent storage, service restart loses data
3. **Single-Threaded Algorithm**: Does not support concurrent optimization requests
4. **Fixed Work Orders**: Only supports pre-configured `WO_A/B/C`

### Phase 1.5 Limitations
1. **Complexity Auto-Classification**: Keyword-based only, no ML model yet (planned for Phase 3)
2. **Part-Station Matrix**: Read-only output, no interactive editing
3. **Merge Efficiency**: Fixed gain percentage, no dynamic calculation
4. **Offline Tasks**: Cannot be re-optimized after initial separation

### Phase 2 Limitations
1. **Multi-Line Scaling**: Performance degrades beyond 5 production lines (solver complexity)
2. **Database**: Development uses SQLite (single-user), production needs PostgreSQL
3. **Layout Editor**: Canvas-based 2D only, no 3D visualization yet (Phase 3 will address)
4. **Authentication**: Still no security implementation (development/testing only)
5. **Fishbone Diagram**: Static SVG/PNG only, no interactive manipulation
6. **Cross-Line Dependencies**: Tasks cannot have precedence constraints across different lines

### Phase 3 Limitations (Pre-Implementation)
1. **Omniverse License**: Requires NVIDIA Omniverse license for 3D simulation features
2. **OpenAI API Cost**: Natural language queries require paid OpenAI GPT-4 API access
3. **Hardware Requirements**: Body sensor processing needs GPU (CUDA-compatible) for real-time analysis
4. **Database Migration**: Requires PostgreSQL (6 new tables) - SQLite not suitable for production

**Mitigation Plans**: 
- Phase 1 & 2: See [Architecture Design](docs/PHASE1_ARCHITECTURE_EN.md#security-design)
- Phase 3: See [Implementation Guide](docs/PHASE3_IMPLEMENTATION_EN.md#environment-setup)

---

## Troubleshooting

### Problem 1: `ModuleNotFoundError: No module named 'fastapi'`
**Solution**:
```bash
pip install -r requirements.txt
```

### Problem 2: `Algorithm execution timeout`
**Cause**: Dataset too large or solver parameters misconfigured  
**Solution**:
- Reduce task count (< 500)
- Increase `max_time_in_seconds` in `sche-algo.py`

### Problem 3: `Dashboard not found`
**Cause**: `dashboard.html` path incorrect  
**Solution**:
```bash
# Ensure file exists
ls -la src/dashboard.html

# Check api_server.py configuration
grep "dashboard.html" src/api_server.py
```

**More FAQs**: [Implementation Guide](docs/PHASE1_IMPLEMENTATION_EN.md#7-troubleshooting)

---

## Acknowledgments

- **Google OR-Tools**: Powerful CP-SAT solver for line balancing optimization
- **FastAPI Community**: High-performance web framework and excellent documentation
- **Chart.js Project**: Lightweight visualization library for Gantt charts
- **NetworkX**: Graph algorithms library for fishbone diagram generation (Phase 2)
- **SQLAlchemy**: Robust ORM for database management (Phase 2)
- **Matplotlib**: Diagram rendering and export (Phase 2)
- **NVIDIA Omniverse**: 3D simulation platform for production line visualization (Phase 3)
- **LangChain**: LLM orchestration framework for natural language queries (Phase 3)
- **MediaPipe**: Computer vision library for body pose estimation (Phase 3)

---

## Documentation Index

### Phase 1 Documentation
- [Quick Start Guide](docs/QUICKSTART_EN.md)
- [Phase 1 Architecture](docs/PHASE1_ARCHITECTURE_EN.md)
- [Phase 1 API Specification](docs/PHASE1_API_SPEC_EN.md)
- [Phase 1 Implementation Guide](docs/PHASE1_IMPLEMENTATION_EN.md)

### Phase 2 Documentation
- [Phase 2 Architecture Design](docs/PHASE2_ARCHITECTURE_EN.md)
- [Phase 2 API Specification](docs/PHASE2_API_SPEC_EN.md)
- [Phase 2 Implementation Guide](docs/PHASE2_IMPLEMENTATION_EN.md)

### Phase 3 Documentation
- [Phase 3 Architecture Design](docs/PHASE3_ARCHITECTURE_EN.md) - Complete 4-layer architecture
- [Phase 3 API Specification](docs/PHASE3_API_SPEC_EN.md) - 15+ new endpoints
- [Phase 3 Implementation Guide](docs/PHASE3_IMPLEMENTATION_EN.md) - Step-by-step guide

### General Documentation
- [IO Specification](docs/IO_SPECIFICATION_EN.md)
- [Models & Strategies](docs/MODELS_STRATEGIES_EN.md)

---

**Document Maintainer:** JASON YY, LIN  
**Last Updated:** 2025-11-13
**Version:** 3.0.0-phase3
