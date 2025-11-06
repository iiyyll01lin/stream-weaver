# Line Balancing System Stage Specifications

Based on `requirements-classification.md`, this document defines Phase 1 / 2 / 3 goals, scope, deliverables, data readiness, and acceptance criteria.

---
## Global Product Vision Summary
Build a decision platform for line balancing that starts from standard time and action-unit data, enabling multi-objective optimization (manpower / workstation count / line type / takt), then evolves toward 2D/3D visualization, version sharing, intelligent classification, and natural language interaction as a central factory configuration decision hub.

---
## Phase 1 – Core Minimum Viable Product (MVP)
### Goals
- Establish reliable and repeatable core line balancing algorithms (manpower, workstation count, takt).
- Define and implement standard time & action-unit data models creating a stable data backbone.
- Provide basic multi-goal query interface and takt / time distribution visualization.

### In-Scope
- Algorithms: Requirements 1,2,3,4,7 (baseline support for offline flag).
- Data: 8,9,13,14,15 (single product family + single plant pilot).
- Visualization: 22 (simple charts: takt bars, workstation load stacked).
- APIs: /optimize, /workstations, /takt-summary.
- Access: Single tenant / single plant; no cross-plant sharing.

### Out-of-Scope
- Line type recommendation (6), multi-line complex scenarios (5) advanced combinations.
- 2D/3D Layout (18,19,20...), natural language query (23).
- ML complexity classification (10), sensing data (17).

### Data Readiness
| Dataset                        | Source                     | Processing                      | Completion Standard                  |
|--------------------------------|----------------------------|---------------------------------|--------------------------------------|
| STD Class Code (8)             | Existing Cookbook CSV      | Format normalization & encoding | Fields: ClassCode, StdTime(ms)       |
| Part-Station Time (9)          | Same / manual supplement   | Null filling & outlier check    | Missing rate < 5%                    |
| Action Unit Decomposition (13) | SOP / preliminary fishbone | Manual label 50~100 samples     | Define action_type + adjustable_flag |
| Default CT (14)                | Standard tables            | Map to action units             | Each type > 5 reference samples      |
| Offline Flag (15)              | Engineering tagging        | Build station mapping table     | Sample validation accuracy > 95%     |

### Deliverables
- Data schema: `schema/core_data_model_v1.json` (fields & constraints).
- Core algorithm module: `core/line_balance_engine.py`.
- Query service API: `services/optimization_service.py`.
- Minimal visualization frontend: load/takt page + basic result table.
- Documentation: Usage guide, abbreviated algorithm whitepaper, data dictionary.

### Acceptance Criteria
| Aspect       | Metric                                     | Threshold                       |
|--------------|--------------------------------------------|---------------------------------|
| Accuracy     | Algorithm vs manual calculation deviation  | < ±5% (sample 10 work orders)   |
| Performance  | Single work order optimization API latency | < 3s (data size <= 500 actions) |
| Stability    | Continuous stress (100 calls)              | Error rate < 0.5%               |
| Data Quality | Missing / anomaly ratio                    | < 5% / < 1%                     |
| Usability    | User task completion (query scenario)      | 5 pilot users success rate 100% |

### Rough Effort (Person-Days)
BE 24 / FE 13 / DE 16 / DA 9 / Algo 29 / UX 8 / DevOps 6  (≈ 105 PD)

### Key Risks & Mitigation
| Risk                               | Impact                | Mitigation                                            |
|------------------------------------|-----------------------|-------------------------------------------------------|
| Standard time inconsistency        | Untrustworthy results | Establish cleaning rules + baseline sample set        |
| Action decomposition unclear       | Hard to optimize      | Restrict initial action_type set, iterative expansion |
| Algorithm performance insufficient | Query latency         | Early caching + pre-segmented computation             |

---
## Phase 2 – Expansion & Operational Efficiency
### Goals
- Enhance multi-line configuration & line type recommendation.
- Introduce Layout / 2D configuration & drag operations; support version management & cross-plant sharing.
- Build finer assembly sequence data and component/action mapping.

### In-Scope
- Functions: 5,6,11,12,16,18,20,21,22 (enhanced),25,27.
- Data: Extend to second product family or second plant.
- Versioning: Store configuration & algorithm parameter snapshots (JSON + metadata).
- Layout: 2D plane (SVG / Canvas) + drag to reconfigure stations.

### Out-of-Scope
- Omniverse / advanced 3D (24,26).
- ML complexity auto classification (10) only planning, not full model.
- NLP (23).

### New Data Readiness
| Dataset                   | Source                 | Processing                    | Completion Standard                     |
|---------------------------|------------------------|-------------------------------|-----------------------------------------|
| Fishbone Sequence (11)    | Engineering docs       | Structured JSON               | 70% station mapping completion          |
| Action-Component Map (12) | Parts list + SOP       | Semi-automatic matching rules | Top 50 parts coverage 90%               |
| CTO/BTO Mapping (16)      | Product structure      | Maintain difference table     | DL360 G11 full coverage                 |
| 2D Layout (18,21)         | AutoCAD / Sketch       | Simplified node/edge model    | All major workstations have coordinates |
| Version/Sharing (25)      | Stakeholder interviews | Design metadata schema        | At least 2 version round-trip tests     |

### Deliverables
- Algorithm extension: multi-line & line type recommendation strategy module `core/line_type_recommender.py`.
- 2D Layout frontend: canvas, station drag, save & load.
- Version management APIs: `/config/version/save`, `/config/version/list`, `/config/version/apply`.
- Assembly sequence data: `data/assembly_sequence_v2.json`.
- Operational docs: Layout maintenance manual, version management process guide.

### Acceptance Criteria
| Aspect                 | Metric                                          | Threshold                |
|------------------------|-------------------------------------------------|--------------------------|
| Recommendation         | Line type recommendation human review pass rate | > 80% (sample 20 cases)  |
| Multi-line Performance | 5-line configuration compute time               | < 8s (medium scale)      |
| Layout Operation       | Drag operation failure rate                     | < 2%                     |
| Version Management     | Save / load consistency                         | 100%                     |
| UX Efficiency          | User task completion time                       | -20% vs Phase 1 baseline |

### Rough Effort
BE 21 / FE 20 / DE 15 / DA 11 / Algo 12 / UX 15 / DevOps 10 / 3D 8  (≈ 112 PD)

### Risks & Mitigation
| Risk                               | Impact               | Mitigation                                                                      |
|------------------------------------|----------------------|---------------------------------------------------------------------------------|
| Multi-line combinatorial explosion | Performance pressure | Layered approach: line type first then local optimization; limit max line count |
| Layout asset inconsistency         | Runtime failures     | Standard for station naming + coordinate conventions                            |
| Version sharing permissions        | Data misuse          | Simple role-based rules & approval workflow                                     |

---
## Phase 3 – Differentiated & Intelligent Capabilities
### Goals
- Introduce 3D models & Omniverse integration (based on Phase 2 Layout foundation).
- Interference checking & assembly sequence simulation.
- Sensing/posture data & complexity ML classification.
- Natural language query endpoint & UI.

### In-Scope
- Functions: 10,17,19,23,24,26 + stabilization of previous phases.
- 3D Models: Product / workstation library minimal set (1~2 product families).
- ML: Complexity classification model v1 (simple features: part count, part types, assembly step depth).
- NLP: Query → intent → transform to API request (Top 5 intents: manpower, takt, lines, bottleneck, recommend line type).

### Out-of-Scope
- High-fidelity physical simulation (geometry interference only; no physics).
- Advanced motion detection (full-body multi-camera); only initial sensing framework.

### New Data Readiness
| Dataset                | Source                  | Processing                | Completion Standard     |
|------------------------|-------------------------|---------------------------|-------------------------|
| 3D Library (19)        | CAD / STEP simplified   | Polygon decimation        | Each model < 50k faces  |
| Sensor Motion (17)     | Pilot workstation       | Timestamp + motion labels | 1000+ labeled samples   |
| Complexity Labels (10) | Engineering review      | Grading indicator sheet   | Consistency Kappa > 0.7 |
| NLP Corpus (23)        | User queries collection | Intent labeling           | 500+ labeled sentences  |

### Deliverables
- 3D viewer / Omniverse connection module.
- Interference check service: `services/interference_check.py`.
- Complexity classification model: `models/complexity_classifier_v1.pkl` + inference API.
- NLP pipeline: `nlp/intent_classifier.py` + `/query` API.
- Natural language frontend input & result highlighting.
- Sensor data ETL: `pipelines/sensor_ingest.py`.

### Acceptance Criteria
| Aspect         | Metric                       | Threshold                 |
|----------------|------------------------------|---------------------------|
| 3D Performance | Single scene load time       | < 5s                      |
| Interference   | Detection accuracy           | > 85% (30 test scenarios) |
| Complexity ML  | Macro F1                     | > 0.75                    |
| NLP Intent     | Top-1 accuracy               | > 80%                     |
| Sensor Data    | Daily ingestion success rate | > 99%                     |

### Rough Effort
BE 14 / FE 11 / DE 14 / DA 11 / Algo 12 / UX 11 / DevOps 6 / ML 17 / NLP 5 / 3D 16  (≈ 121 PD)

### Risks & Mitigation
| Risk                             | Impact                    | Mitigation                                           |
|----------------------------------|---------------------------|------------------------------------------------------|
| 3D modeling cost too high        | Delivery delay            | Use simplified models + lazy loading                 |
| Sensor data noise quality        | Poor ML performance       | Pre-feature filtering + action template library      |
| NLP domain semantic variety      | Query misclassification   | Iterative corpus collection + fallback GUI           |
| Interference geometry inaccuracy | False positives/negatives | Use bounding volume pre-check + refined verification |

---
## Milestones & Gate Checks
| Milestone | Phase | Content                           | Gate Metric                               |
|-----------|-------|-----------------------------------|-------------------------------------------|
| M1        | 1     | Data backbone & cleaning complete | Data quality thresholds met               |
| M2        | 1     | Core algorithm alpha              | Accuracy deviation < ±10%                 |
| M3        | 1     | MVP launch                        | User acceptance 100%                      |
| M4        | 2     | Multi-line & recommendation beta  | Performance/latency metrics passed        |
| M5        | 2     | Layout + version management       | Version round-trip 100% success           |
| M6        | 3     | 3D + interference alpha           | Initial interference detection set passed |
| M7        | 3     | ML/NLP beta                       | F1 / intent >= targets                    |
| M8        | 3     | Full enhanced release             | Ops handover docs complete                |

---
## Resourcing Strategy
- Phase 1: Focus on Algo & data foundation; minimal FE UI; no dedicated ML/NLP/3D roles.
- Phase 2: Increase FE/UX proportion; introduce part-time or outsourced 3D modeling.
- Phase 3: Add dedicated ML/NLP or shared resources; full-time 3D support for a period.

---
## Technical Baseline
| Layer        | Suggested Choice                                              |
|--------------|---------------------------------------------------------------|
| Backend      | Python FastAPI + Async (performance + ecosystem)              |
| Data Storage | PostgreSQL (structured) + MinIO/Blob (3D assets)              |
| Caching      | Redis (algorithm result caching)                              |
| Frontend     | React + TypeScript + Ant Design / Chakra                      |
| 2D Layout    | SVG/Canvas + custom coordinate system                         |
| 3D           | three.js (Phase 2 lightweight) / Omniverse (Phase 3)          |
| ML/NLP       | scikit-learn baseline → HuggingFace (intent classification)   |
| DevOps       | Docker + GitHub Actions (CI) + IaC (Terraform optional later) |

---
## Assumptions & Boundaries
| ID | Assumption                                                    | Impact                                |
|----|---------------------------------------------------------------|---------------------------------------|
| A1 | Phase 1 limits to a single product family                     | Reduces data complexity               |
| A2 | No real-time streaming (batch calc acceptable 1–2 min window) | Architecture skips event streaming    |
| A3 | Standard time source can be manually adjusted                 | Avoids early ML introduction          |
| A4 | 3D models need no physical precision                          | Use lightweight visual representation |
| A5 | NLP queries are assistive, not GUI replacement                | Allows phased rollout                 |

---
## Next Documents
Next: `feasibility-assessment.md` will include:
1. Technical maturity scoring (Architecture / Data / Algo / UX / 3D / ML/NLP).
2. Risk matrix & mitigation plan.
3. Milestone feasibility assessment & suggested adjustments.
4. Staffing allocation vs effort variance analysis.

---
Further breakdown (EPIC → Story → Tasks) for Phase 1 can proceed after confirming this specification.
