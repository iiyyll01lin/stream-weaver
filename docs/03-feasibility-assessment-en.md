# Line Balancing System Feasibility Assessment

Reference: `requirements-classification.md`, `stage-specs.md`
Purpose: Assess technical, data, staffing, and risk feasibility of phased specifications and provide adjustment recommendations.

---
## 1. Executive Summary
Phase 1 centers on algorithms + data backbone with a single product family pilot; technical risk is controllable. Phase 2 major risks lie in multi-line configuration performance and layout asset consistency. Phase 3 uncertainty concentrates in 3D modeling cost, sensor data quality, and NLP/ML cold start. Recommendation: retain the three-phase structure but trim initial Phase 3 scope (deploy a minimal 3D viewer first, defer full precision interference checking).

---
## 2. Scoring Dimensions
Scale: 1 (very high risk / low maturity) ~ 5 (mature / controllable).

| Dimension                        | Phase 1 | Phase 2 | Phase 3 | Notes                                                                            |
|----------------------------------|---------|---------|---------|----------------------------------------------------------------------------------|
| Architectural Maturity (Backend) | 4       | 4       | 4       | FastAPI / standard layering, operations controllable                             |
| Data Structure & Quality         | 3       | 3.5     | 3.5     | Baseline in Phase 1; governance needed as scope expands; sensors add uncertainty |
| Algorithm Complexity             | 3.5     | 4       | 4.5     | Multi-line/recommendation adds complexity; interference adds geometric logic     |
| Visualization & Interaction      | 3       | 4       | 4.2     | 2D drag after Phase 2 becomes stable; initial 3D simplified display manageable   |
| 3D/Simulation Maturity           | 1       | 2       | 3.2     | Limited early resources; Phase 3 simplified approach improves feasibility        |
| ML Complexity Classification     | 1       | 2       | 3       | Dataset accumulation later; cold-start risk                                      |
| NLP Query                        | 1       | 1.5     | 3       | Limited intent set feasible; needs iterative corpus                              |
| DevOps/Deployment                | 4       | 4.2     | 4.2     | Containerized standard pipeline, low risk                                        |
| Performance/Scalability          | 3       | 3.5     | 3.8     | Requires caching & pre-segmentation strategies                                   |
| Staffing Flexibility             | 3.5     | 3.2     | 3       | Phase 3 needs new skills (3D, ML, NLP) reducing flexibility                      |

---
## 3. Risk Matrix

| Risk ID | Description                                    | Type        | Probability | Impact | Level    | Mitigation Strategy                              | Monitoring Metric              |
|---------|------------------------------------------------|-------------|-------------|--------|----------|--------------------------------------------------|--------------------------------|
| R1      | High noise in standard time & action-unit data | Data        | Med         | High   | High     | Cleaning rules + baseline sample set             | Missing rate / outlier ratio   |
| R2      | Multi-line configuration compute time too long | Performance | Med         | Med    | Medium   | Layered optimization / cache scenario results    | Average latency                |
| R3      | Layout asset format inconsistency              | Data        | High        | Med    | High     | Naming / coordinate spec + validation tool       | Layout validation failure rate |
| R4      | 3D model build cycle too long                  | Capacity    | Med         | High   | High     | Simplified models + outsourced batch modeling    | Model completion rate          |
| R5      | Insufficient labeled sensor data               | Data/ML     | High        | High   | Critical | Limited pilot stations; semi-auto labeling       | Labeled sample count           |
| R6      | Low complexity classification accuracy         | ML          | Med         | Med    | Medium   | Hybrid rules + ML; iterative feature engineering | F1 / Kappa                     |
| R7      | NLP intent misclassification                   | NLP         | Med         | Med    | Medium   | Top-K + GUI fallback                             | Intent Top-1 accuracy          |
| R8      | Interference geometric precision insufficient  | Algo/3D     | Low         | Med    | Low      | Coarse detection + detailed recomputation        | False pos / false neg rate     |
| R9      | Algorithm non-reproducibility                  | Process     | Low         | High   | Medium   | Version snapshots + parameter logging            | Reproduction success rate      |

---
## 4. Detailed Mitigation Strategies
### R1 Data Quality
- Strategy: ETL validation (nulls, extremes, unit normalization ms).
- Tools: Python + Great Expectations or Pandera.
- Gate: Data quality report ready before Phase 1 M1.

### R2 Performance
- Strategy: Split algorithm: coarse allocation → local refinement; Redis cache repeat queries; limit max lines (<=5).
- Metric: P95 latency < 5 seconds.

### R3 Layout Assets
- Strategy: Define JSON layout schema; build validation CLI; block deployment on failures.
- Metric: Validation failure rate < 2%.

### R4 3D Models
- Strategy: Use low-poly (decimation); start with 10 core devices; create outsourcing spec pack.
- Metric: First 10 models complete before Phase 3 M6.

### R5 Sensor Labeling
- Strategy: Focus station selection; record → semi-auto segmentation → human correction; build lightweight annotation tool.
- Metric: 1000+ labeled samples; weekly growth > 10%.

(Other risks R6–R9 follow same iterative governance—details in risk matrix.)

---
## 5. Staffing vs Effort Variance Analysis

| Role   | Phase 1 Effort | Suggested FTE | Phase 2 Effort | Suggested FTE | Phase 3 Effort | Suggested FTE | Notes                                    |
|--------|----------------|---------------|----------------|---------------|----------------|---------------|------------------------------------------|
| BE     | 24 PD          | 2 FTE         | 21 PD          | 2 FTE         | 14 PD          | 1–2 FTE       | After algorithm stabilization can reduce |
| FE     | 13 PD          | 1 FTE         | 20 PD          | 2 FTE         | 11 PD          | 1 FTE         | Peak in Phase 2 then declines            |
| DE     | 16 PD          | 1 FTE         | 15 PD          | 1 FTE         | 14 PD          | 1 FTE         | Continuous data governance               |
| DA     | 9 PD           | 0.5 FTE       | 11 PD          | 0.5 FTE       | 11 PD          | 0.5 FTE       | Focus on validation & feature iteration  |
| Algo   | 29 PD          | 1–1.5 FTE     | 12 PD          | 1 FTE         | 12 PD          | 1 FTE         | Intensive early algorithm design         |
| 3D     | 0              | 0             | 8 PD           | 0.5 FTE       | 16 PD          | 1 FTE         | Incremental investment in Phase 3        |
| UX     | 8 PD           | 0.5 FTE       | 15 PD          | 1 FTE         | 11 PD          | 0.5–1 FTE     | Complexity peak in Phase 2               |
| DevOps | 6 PD           | 0.5 FTE       | 10 PD          | 0.5 FTE       | 6 PD           | 0.5 FTE       | Mostly steady ops                        |
| ML     | 0              | 0             | 0              | 0             | 17 PD          | 1 FTE         | Starts Phase 3                           |
| NLP    | 0              | 0             | 0              | 0             | 5 PD           | 0.5 FTE       | Can share resource with ML               |

> If constrained, combine FE/UX Phase 1; Phase 3 early ML/NLP can start part-time.

---
## 6. Performance & Architecture Feasibility
### Core Computation Pattern
- Input: Work order → action-unit sequence + standard times + constraints (max CT, max line count).
- Steps:
  1. Preprocessing: merge standard times, offline flags.
  2. Coarse allocation: greedy or heuristic workstation slicing.
  3. Refinement: move actions around bottleneck stations (local search / simulated annealing deferred to Phase 2).
  4. Output metrics: manpower, UPH, workstation utilization, idle times, bottleneck.

### Complexity
- Phase 1: O(N) ~ O(N log N) (greedy + limited adjustments).
- Phase 2: Multi-line + scenario combinations → need pruning (limit candidate line types).
- Phase 3: Interference adds geometric computation (use Bounding Volume Hierarchy to reduce cost).

### Architectural Feasibility
| Aspect      | Assessment                                | Recommendation                                   |
|-------------|-------------------------------------------|--------------------------------------------------|
| Scalability | Horizontal API scaling; queueable compute | Dispatch tasks to background workers (Celery/RQ) |
| Caching     | Repeat queries on same work order         | Redis key: hash(work_order_id + params)          |
| Monitoring  | Need execution time & errors              | FastAPI + Prometheus metrics                     |

---
## 7. Scope Cut Options
| Item                              | Phase | Cut Strategy                                          | Impact                        |
|-----------------------------------|-------|-------------------------------------------------------|-------------------------------|
| Offline processing detail (Req 4) | 1     | Only station-level flag, skip fine-grain action logic | Slight precision drop         |
| Line type recommendation (Req 6)  | 2     | Rule-based only (length / complexity thresholds)      | Lower accuracy, faster usable |
| Version sharing (Req 25)          | 2     | Defer to end of Phase 2                               | Collaboration delayed         |
| Interference check (Req 26)       | 3     | Coarse voxel / bounding box only                      | Reduced geometric fidelity    |
| NLP (Req 23)                      | 3     | Limit to 5 intents, no dialogue context               | Simplified experience         |

---
## 8. Milestone Feasibility Review
| Milestone | Risk                          | Suggested Adjustment                                    |
|-----------|-------------------------------|---------------------------------------------------------|
| M1        | Extended data cleaning time   | Build early data profiling scripts                      |
| M3        | MVP acceptance delay          | Introduce internal alpha checklist for early validation |
| M5        | Layout/version tight coupling | Separate version mgmt API and layout UI cycles          |
| M6        | Insufficient 3D models ready  | Start with 5 core models + monthly expansion            |
| M7        | Insufficient ML/NLP data      | Use rules + baseline first, iterate                     |

---
## 9. Recommendations
1. Enforce data governance priority: If R1 persists, delay all advanced features.
2. Define algorithm output JSON schema early to unify visualization & NLP/ML integration.
3. Capture algorithm parameter snapshots from Phase 1 for future traceability & analytic modeling.
4. Adopt gradual expansion strategy for 3D & sensing to avoid front-loaded cost.
5. Design NLP/ML with replaceable fallback—GUI ensures task completion on failure.

---
## 10. Next Actions
| Action                         | Owner   | Timeframe | Output                               |
|--------------------------------|---------|-----------|--------------------------------------|
| Build data profiling script    | DE      | 1 week    | profiling_report_v1.md               |
| Define algorithm output schema | BE/Algo | 3 days    | `schema/optimization_output_v1.json` |
| Action-unit labeling rules doc | DA/Algo | 1 week    | action_units_guideline.md            |
| Cache strategy PoC             | BE      | 3 days    | cache_strategy_note.md               |
| Layout naming/coordinate spec  | UX/FE   | 3 days    | layout_naming_convention.md          |

---
## 11. Conclusion
Three-phase planning shows logical consistency and balanced resource assumptions. Key success factors:
1. Phase 1 credibility of data quality and algorithm results.
2. Phase 2 elevation of user experience and operational efficiency so it becomes daily tooling.
3. Phase 3 differentiated capabilities (3D + intelligence) must be incremental—avoid early high precision targets.

Recommendation: Deliver this assessment with prior spec documents for leadership scope confirmation and resource allocation.

---
## Appendix A: Suggested Algorithm Output Fields (Draft)
| Field                        | Type          | Description                                         |
|------------------------------|---------------|-----------------------------------------------------|
| work_order_id                | string        | Work order identifier                               |
| objectives                   | object        | Selected goals (min_manpower / min_lines / balance) |
| stations                     | array<object> | Workstation configuration list                      |
| stations[i].id               | string        | Workstation ID                                      |
| stations[i].assigned_actions | array         | Action-unit list                                    |
| stations[i].total_time_ms    | number        | Total time                                          |
| stations[i].idle_time_ms     | number        | Idle time                                           |
| takt_time_ms                 | number        | Computed takt time                                  |
| bottleneck_station_id        | string        | Longest workstation                                 |
| manpower_total               | number        | Total manpower estimate                             |
| line_count                   | number        | Number of lines used                                |
| utilization_avg              | number        | Average workstation utilization                     |

---
## Appendix B: Initial Intent Set (NLP)
| Intent               | Example Query (English Equivalent)         |
|----------------------|--------------------------------------------|
| manpower_estimate    | How many people does this work order need? |
| takt_time            | What is the takt time?                     |
| line_recommend       | How many lines are recommended?            |
| bottleneck           | Which station is the bottleneck?           |
| optimize_goal_change | Recalculate with minimum stations goal     |

---

