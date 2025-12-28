# Stream Weaver - Line Balance System

[![Version](https://img.shields.io/badge/version-3.1.0--phase3-blue.svg)](CHANGELOG.md)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

> **Production line balancing optimization powered by OR-Tools CP-SAT solver**

An intelligent system for optimizing assembly line configurations, balancing workloads, and maximizing production efficiency.

---

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the server
python src/api_server.py

# 3. Open dashboard
# Navigate to http://localhost:8000 in your browser

# 4. Run optimization
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{"work_order_id": "WO_A", "optimization_goal": "min_stations", "target_takt": 30000}'
```

**Docker Alternative:**
```bash
docker compose up --build
```

---

## Key Features

### Core Optimization (Phase 1)
- **3 Optimization Goals**: Minimize stations, manpower, or idle time
- **CP-SAT Solver**: Google OR-Tools constraint programming
- **Precedence Constraints**: Respects task dependencies
- **< 3 second** solve time for 500+ tasks

### Extended Capabilities (Phase 1.5)
- **Offline Task Handling**: Separate preparation tasks from main line
- **Task Merging**: Combine compatible tasks for efficiency
- **Complexity Classification**: Auto-categorize tasks (simple/medium/complex)
- **Part-Level Tracking**: BOM integration with material flow visualization

### Multi-Line & Visualization (Phase 2)
- **Multi-Line Optimization**: Balance across multiple production lines
- **Line Type Recommendation**: AI suggests cell/short_line/long_line
- **Fishbone Diagrams**: NetworkX-generated assembly sequences (SVG/PNG)
- **2D Layout Editor**: Canvas-based drag-and-drop station placement
- **Product Configuration**: CTO/BTO variant management

### AI/ML & 3D Simulation (Phase 3)
- **Natural Language Queries**: "Show me bottleneck stations" via GPT-4
- **Body Sensor Processing**: MediaPipe motion capture with REBA scoring
- **3D Model Library**: USD asset management for workstations/tools
- **Omniverse Integration**: NVIDIA platform for physics simulation
- **Version Control**: Git-like configuration management with diff viewer
- **Collision Detection**: AABB/OBB/Mesh interference checking
- **Multilingual UI**: EN, zh-TW, ES, zh-CN support

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/optimize` | POST | Run line balance optimization |
| `/workstations/{work_order_id}` | GET | Get workstation assignments |
| `/takt-summary/{work_order_id}` | GET | Get takt time analysis |
| `/recommend-line-type` | GET | Get line type recommendation |
| `/fishbone-diagram` | GET | Generate assembly diagram |
| `/layout` | GET/POST/DELETE | Layout CRUD operations |
| `/product-config` | GET/POST | Product configuration |
| `/nlp-query` | POST | Natural language queries |
| `/3d-models` | GET/POST | 3D asset management |
| `/health` | GET | Health check |

📖 **Full API documentation**: [Phase 1](docs/PHASE1_API_SPEC_EN.md) | [Phase 2](docs/PHASE2_API_SPEC_EN.md) | [Phase 3](docs/PHASE3_API_SPEC_EN.md)

---

## CSV Input Formats

### Basic Format (3 columns)
```csv
task_id,time_ms,predecessors
T1,15000,
T2,12000,T1
T3,8000,T1
```

### Standard Format (6 columns)
```csv
task_id,time_ms,predecessors,category,offline_flag,merge_group
T1,15000,,Assembly,false,
T2,12000,T1,Assembly,false,MG1
```

### Full Extended Format (8 columns)
```csv
task_id,time_ms,predecessors,category,offline_flag,merge_group,complexity,part_ids
T1,15000,,Assembly,false,,complex,P001;P002
```

📖 **Format details**: [IO Specification](docs/IO_SPECIFICATION_EN.md)

---

## Technology Stack

| Layer | Technology |
|-------|------------|
| **Backend** | FastAPI, Pydantic, Python 3.10+ |
| **Algorithm** | Google OR-Tools CP-SAT |
| **Database** | PostgreSQL + SQLAlchemy 2.0 |
| **Frontend** | React 18, Three.js, Canvas API |
| **3D/AI** | NVIDIA Omniverse, LangChain + GPT-4, MediaPipe |
| **Visualization** | Chart.js, NetworkX, Matplotlib |
| **Deployment** | Docker, docker-compose |

---

## Project Structure

```
line-balance/
├── src/
│   ├── api_server.py         # FastAPI backend
│   ├── dashboard.html        # Web UI
│   ├── sche-algo.py          # Single-line solver
│   ├── sche-algo-v2.py       # Multi-line solver
│   ├── fishbone_generator.py # Diagram generator
│   ├── models/               # Database models
│   ├── services/             # Business logic
│   ├── ml/                   # ML models (Phase 3)
│   └── utils/                # Utilities
├── frontend/                 # React app (Phase 3)
├── data/                     # CSV input files
├── docs/                     # Documentation
├── test/                     # Test suites
├── storage/                  # File storage
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## Deployment

### Bare Metal
```bash
pip install -r requirements.txt
python3 -c "from src.utils.db import init_db; init_db()"
python3 src/api_server.py
```

### Docker
```bash
docker compose up --build -d
docker compose logs -f
```

📖 **Deployment guides**: [Phase 1](docs/PHASE1_IMPLEMENTATION_EN.md#5-deployment-guide) | [Phase 2](docs/PHASE2_IMPLEMENTATION_EN.md#deployment)

---

## Testing

```bash
# Run all tests
pytest test/ -v

# Phase 1 integration tests
bash test/test_phase1_integration.sh

# Phase 2 tests
pytest test/test_multi_line.py test/test_fishbone.py test/test_layout_api.py -v
```

📖 **Test commands**: [TEST_COMMANDS_LINUX.md](TEST_COMMANDS_LINUX.md)

---

## Target Performance

| Metric | Target | Result |
|--------|--------|--------|
| API Latency | < 3 sec | ✅ 0.8-2.5 sec |
| Correctness | ±5% | ✅ < 3% deviation |
| Dataset Size | ≤ 500 tasks | ✅ Supported |
| Multi-Line | 5 lines | ✅ 200 tasks/line |

---

## Roadmap

| Phase | Status | Highlights |
|-------|--------|------------|
| **Phase 1** | ✅ Spec Complete | Core optimization, 3 objectives, Docker |
| **Phase 1.5** | ✅ Spec Complete | Offline tasks, merging, complexity, parts |
| **Phase 2** | ✅ Spec Complete | Multi-line, fishbone, layouts, CTO/BTO |
| **Phase 3** | ✅ Spec Complete | NLP, sensors, 3D, Omniverse, versioning |

---

## Known Limitations

- **No Authentication**: Development use only (no security)
- **Multi-Line Scaling**: Performance degrades beyond 5 lines
- **Omniverse**: Requires NVIDIA license for 3D features
- **OpenAI API**: NLP queries require paid GPT-4 access
- **GPU Required**: Body sensor processing needs CUDA

📖 **Mitigation plans**: [Architecture Design](docs/PHASE1_ARCHITECTURE_EN.md#security-design)

---

## Documentation

### Getting Started
- [Quick Start Guide](docs/QUICKSTART_EN.md)
- [Usage Examples](docs/EXAMPLES.md)
- [IO Specification](docs/IO_SPECIFICATION_EN.md)

### Architecture & API
- **Phase 1**: [Architecture](docs/PHASE1_ARCHITECTURE_EN.md) | [API](docs/PHASE1_API_SPEC_EN.md) | [Implementation](docs/PHASE1_IMPLEMENTATION_EN.md)
- **Phase 2**: [Architecture](docs/PHASE2_ARCHITECTURE_EN.md) | [API](docs/PHASE2_API_SPEC_EN.md) | [Implementation](docs/PHASE2_IMPLEMENTATION_EN.md)
- **Phase 3**: [Architecture](docs/PHASE3_ARCHITECTURE_EN.md) | [API](docs/PHASE3_API_SPEC_EN.md) | [Implementation](docs/PHASE3_IMPLEMENTATION_EN.md)

### Reference
- [Models & Strategies](docs/MODELS_STRATEGIES_EN.md)

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| Algorithm timeout | Reduce tasks (< 500) or increase `max_time_in_seconds` |
| Dashboard not found | Verify `src/dashboard.html` exists |

📖 **More FAQs**: [Implementation Guide](docs/PHASE1_IMPLEMENTATION_EN.md#7-troubleshooting)

---

## Acknowledgments

- **[Google OR-Tools](https://developers.google.com/optimization)** - CP-SAT solver
- **[FastAPI](https://fastapi.tiangolo.com/)** - Web framework
- **[NetworkX](https://networkx.org/)** - Graph algorithms
- **[NVIDIA Omniverse](https://www.nvidia.com/omniverse)** - 3D simulation
- **[LangChain](https://langchain.com/)** - LLM orchestration
- **[MediaPipe](https://mediapipe.dev/)** - Pose estimation

---

**Maintainer:** JASON YY, LIN  
**Version:** 3.1.0-phase3  
**Last Updated:** 2025-12-14
