# Line Balancing System Requirements Classification

Source: `User Requirements_Line Balance__User_Requirement.csv`
Purpose: Support scope confirmation, phased rollout strategy, and rough effort estimation with stakeholders/product owner.

---
## Dimension Definitions
- Category: Original CSV tags (Function / Basic Data / Advanced Data / Platform).
- Theme Group: Regrouped by value chain: Basic Data, Core Algorithm, Configuration & Visualization, Interaction & Experience, Advanced Expansion.
- Requirement Name: English (original bilingual items preserved conceptually).
- Type: Simulation / Data Modeling / UI/UX / Integration / Analytics / Infra / 3D / NLP.
- Priority: P0 critical must-have; P1 important; P2 deferrable.
- Phase Suggestion: Phase 1 / 2 / 3.
- Dependencies: Pre‑requisite data or other function modules.
- Role Effort: Rough person‑day estimate by role: BE / FE / DE / DA / Algo / 3D / UX / DevOps / ML / NLP. Blank or 0 if not used.
- Risk (Short): Data / technical / requirement uncertainty highlights.

> Effort values are comparative rough sizing only. Later refinement can move to Story Points or T‑Shirt sizes. 1 person‑day = 8 hours. No management/testing buffer included (recommend +15~25% buffer later).

---
## Role Legend

| Role       | Description                                                           |
|:-----------|:----------------------------------------------------------------------|
| **BE**     | Backend Engineering (APIs, services, scheduling, algorithm packaging) |
| **FE**     | Frontend Engineering (Web UI)                                         |
| **DE**     | Data Engineering (cleanup, ETL, schema design)                        |
| **DA**     | Data Analysis (validating standard times, classification logic)       |
| **Algo**   | Algorithm Engineer (Line balancing, scheduling, optimization)         |
| **3D**     | 3D/Simulation (Omniverse / layout)                                    |
| **UX**     | Experience & process design                                           |
| **DevOps** | CI/CD, deployment, environment management                             |
| **ML**     | Machine Learning (complexity auto classification, posture/sensor)     |
| **NLP**    | Natural Language Query (domain intents)                               |

---
## Overview of Tasks (Role Focus)

| Theme Group (English)             | Requirement Name                                                       | Key Role Focus |
|:----------------------------------|:-----------------------------------------------------------------------|:---------------|
| **Core Algorithm**                | (1) Multi optimization goals                                           | Algo, BE       |
|                                   | (2) Workstation count simulation                                       | Algo, BE       |
|                                   | (3) Minimum manpower allocation                                        | Algo, BE       |
|                                   | (4) Workstation configuration & offline processing decision simulation | Algo, BE, DE   |
|                                   | (5) Multiple lines & multi-workstation configuration                   | Algo, BE       |
|                                   | (6) Recommend line type (cell / short / long)                          | Algo, BE       |
|                                   | (7) Takt & manpower simulation under different configurations          | Algo, BE       |
| **Basic Data**                    | (8) STD time by class code                                             | DE             |
|                                   | (9) Part workstation task time maintenance                             | DE             |
|                                   | (11) Assembly sequence fishbone diagram                                | DE, DA, BE     |
|                                   | (12) Action unit to component mapping                                  | DE             |
|                                   | (13) Action unit decomposition & adjustability judgment                | BE, DE         |
|                                   | (14) Default cycle time per action unit                                | BE, DE, DA     |
|                                   | (15) Offline processing flag                                           | BE, DE         |
|                                   | (16) CTO/BTO mapping table                                             | BE, DE         |
| **Advanced Data**                 | (10) Automatic assembly complexity classification                      | ML             |
| **Advanced Expansion**            | (17) Body sensor assembly motion data                                  | ML, DE         |
|                                   | (19) 3D product/workstation/device library                             | 3D             |
|                                   | (24) Omniverse 3D simulation                                           | 3D             |
|                                   | (26) Interference check & assembly sequence simulation                 | 3D, BE, DE     |
| **Configuration & Visualization** | (18) 2D layout by site                                                 | BE, FE, DE, UX |
|                                   | (21) Display layout & plant-specific adjustment                        | BE             |
|                                   | (22) Combine takt chart & time distribution visualization              | BE, FE         |
| **Interaction Experience**        | (20) Simple maintenance UI + simplified 3D model                       | BE, FE, 3D, UX |
|                                   | (23) Natural language query                                            | NLP            |
|                                   | (25) Module version storage & cross-plant sharing                      | BE             |
|                                   | (27) Drag-and-drop equipment & workstation configuration               | BE, FE, UX     |

---
## Detailed Requirements Table

| ID | Category      | Theme Group                   | Requirement Name                                        | Type              | Priority | Phase | Dependencies | Risk (Short)                                | BE | FE | DE | DA | Algo | 3D | UX | DevOps | ML | NLP |
|----|---------------|-------------------------------|---------------------------------------------------------|-------------------|----------|-------|--------------|---------------------------------------------|----|----|----|----|------|----|----|--------|----|-----|
| 1  | Function      | Core Algorithm                | Multi optimization goals                                | Simulation/Algo   | P0       | 1     | 2,3,7        | Parameter boundary definitions              | 4  | 2  | 1  | 1  | 6    | 0  | 1  | 1      | 0  | 0   |
| 2  | Function      | Core Algorithm                | Workstation count simulation                            | Simulation        | P0       | 1     | 8,9,13,14    | Standard time quality                       | 4  | 1  | 2  | 1  | 5    | 0  | 1  | 1      | 0  | 0   |
| 3  | Function      | Core Algorithm                | Minimum manpower allocation                             | Optimization      | P0       | 1     | 2,8,9,13     | Optimization model complexity               | 5  | 1  | 2  | 1  | 6    | 0  | 1  | 1      | 0  | 0   |
| 4  | Function      | Core Algorithm                | Workstation configuration & offline decision simulation | Simulation        | P0       | 1     | 15,13,14     | Offline definition variance                 | 4  | 2  | 3  | 1  | 5    | 0  | 1  | 1      | 0  | 0   |
| 5  | Function      | Core Algorithm                | Multi-line & multi-workstation configuration            | Simulation        | P1       | 2     | 1,2,3        | Computational complexity growth             | 3  | 1  | 2  | 1  | 4    | 0  | 1  | 1      | 0  | 0   |
| 6  | Function      | Core Algorithm                | Line type recommendation (cell/short/long)              | Recommendation    | P1       | 2     | 1,2,3,8      | Classification rule clarity                 | 4  | 1  | 2  | 1  | 4    | 0  | 1  | 1      | 0  | 0   |
| 7  | Function      | Core Algorithm                | Takt & manpower simulation across configurations        | Simulation        | P0       | 1     | 1,2,3,8,9    | Performance under large scenario counts     | 4  | 2  | 2  | 1  | 6    | 0  | 1  | 1      | 0  | 0   |
| 8  | Basic Data    | Basic Data                    | STD time by class code                                  | Data Modeling     | P0       | 1     | Raw Cookbook | Standard time format differences            | 2  | 0  | 3  | 2  | 0    | 0  | 1  | 1      | 0  | 0   |
| 9  | Basic Data    | Basic Data                    | Part workstation task time maintenance                  | Data Modeling     | P0       | 1     | 8            | Granularity consistency                     | 2  | 0  | 3  | 2  | 0    | 0  | 1  | 1      | 0  | 0   |
| 10 | Basic Data    | Advanced Data                 | Automatic assembly complexity classification            | ML Classification | P2       | 3     | 9,12         | Insufficient labeled dataset                | 2  | 1  | 2  | 2  | 0    | 0  | 1  | 1      | 5  | 0   |
| 11 | Basic Data    | Basic Data                    | Assembly sequence fishbone diagram                      | Data Struct       | P1       | 2     | 9,13         | Decomposition rule uncertainty              | 2  | 1  | 2  | 2  | 0    | 0  | 1  | 1      | 0  | 0   |
| 12 | Basic Data    | Basic Data                    | Action unit to component mapping                        | Data Mapping      | P1       | 2     | 9            | Mapping difficulty                          | 2  | 1  | 3  | 2  | 0    | 0  | 1  | 1      | 0  | 0   |
| 13 | Basic Data    | Basic Data                    | Action unit decomposition & adjustability               | Data/Algo         | P0       | 1     | 8,9          | Adjustability logic clarity                 | 3  | 1  | 3  | 2  | 2    | 0  | 1  | 1      | 0  | 0   |
| 14 | Basic Data    | Basic Data                    | Default cycle time per action unit                      | Data Modeling     | P0       | 1     | 13           | Source standard definition                  | 2  | 0  | 2  | 2  | 0    | 0  | 1  | 1      | 0  | 0   |
| 15 | Basic Data    | Basic Data                    | Offline processing flag                                 | Data Attribute    | P0       | 1     | 13,14        | Definition variance                         | 2  | 0  | 2  | 1  | 0    | 0  | 1  | 1      | 0  | 0   |
| 16 | Basic Data    | Basic Data                    | CTO/BTO mapping table                                   | Data Mapping      | P1       | 2     | 8,9          | Maintenance cost                            | 2  | 0  | 2  | 1  | 0    | 0  | 1  | 1      | 0  | 0   |
| 17 | Advanced Data | Advanced Expansion            | Body sensor assembly motion data                        | Sensor/ML         | P2       | 3     | 13,14        | Hardware & labeling overhead                | 2  | 1  | 3  | 2  | 0    | 0  | 1  | 1      | 6  | 0   |
| 18 | Basic Data    | Configuration & Visualization | 2D layout by site                                       | UI/Layout         | P1       | 2     | 8,9          | Layout asset format variance                | 2  | 2  | 2  | 1  | 0    | 0  | 2  | 1      | 0  | 0   |
| 19 | Advanced Data | Advanced Expansion            | 3D product/workstation/device library                   | 3D Library        | P2       | 3     | 18           | Modeling cost                               | 2  | 2  | 2  | 1  | 0    | 5  | 2  | 1      | 0  | 0   |
| 20 | Platform      | Interaction Experience        | Simple maintenance UI + simplified 3D models            | UI/3D             | P1       | 2     | 18           | 3D fidelity trade-offs                      | 3  | 3  | 2  | 1  | 0    | 3  | 3  | 1      | 0  | 0   |
| 21 | Platform      | Configuration & Visualization | Display layout & plant adjustments                      | UI/Layout         | P1       | 2     | 18           | Large inter-plant layout differences        | 3  | 2  | 2  | 1  | 0    | 0  | 2  | 1      | 0  | 0   |
| 22 | Platform      | Configuration & Visualization | Takt & time distribution visualization                  | Visualization     | P0       | 1     | 1,2,7,8      | Visualization performance                   | 3  | 3  | 2  | 2  | 0    | 0  | 2  | 1      | 0  | 0   |
| 23 | Platform      | Interaction Experience        | Natural language query                                  | NLP               | P2       | 3     | 1,2,7,8      | Domain intents & vocabulary                 | 2  | 2  | 2  | 1  | 0    | 0  | 2  | 1      | 0  | 5   |
| 24 | Platform      | Advanced Expansion            | Omniverse 3D simulation                                 | 3D/Simulation     | P2       | 3     | 19,20        | Platform integration & licensing            | 2  | 2  | 2  | 1  | 0    | 5  | 2  | 1      | 0  | 0   |
| 25 | Platform      | Interaction Experience        | Module version storage & cross-plant sharing            | Infra/Data        | P1       | 2     | 8,9,18       | Permissions & variance                      | 3  | 2  | 2  | 1  | 0    | 0  | 2  | 2      | 0  | 0   |
| 26 | Platform      | Advanced Expansion            | Interference check & assembly sequence simulation       | 3D/Algo           | P2       | 3     | 19,11,13     | Interference detection algorithm complexity | 3  | 2  | 3  | 2  | 2    | 4  | 2  | 1      | 0  | 0   |
| 27 | Platform      | Interaction Experience        | Drag-and-drop equipment & workstation configuration     | UI/Layout         | P1       | 2     | 18,21        | Interaction complexity                      | 3  | 3  | 2  | 1  | 0    | 0  | 3  | 1      | 0  | 0   |

---
## Phase Summary (Concise)
- Phase 1 Core: Minimal viable algorithms (1,2,3,4,7) + data skeleton (8,9,13,14,15) + essential visualization (22).
- Phase 2 Expansion: Multi-line/recommendation (5,6) + assembly granularity/sequence (11,12,16) + layout / 2D / interaction (18,20,21,25,27).
- Phase 3 Advanced: Complexity auto classification (10) + sensing (17) + high-fidelity 3D (19,24,26) + NLP (23).

---
## Dependency Chains
- Data Skeleton: 8 → 9 → (13 → 14 → 15) → 11/12 → 16.
- Algorithm Core: 2,3 depend on standard times 8,9; configuration/takt 7 depends on 1,2,3; line type recommendation 6 depends on 1~3 + 8.
- Visualization: 22 depends on algorithm outputs; 18 forms 2D base → 21/27; 19 → 24/26.
- Advanced Intelligence: 10 needs 9,12; 17 needs 13,14; 23 needs stable core output APIs.

---
## Top Risks
1. Standard time quality (8,9) inconsistency → impacts algorithm accuracy.
2. Action unit decomposition logic (13) unclear → hampers automation & optimization.
3. Multi-line configuration (5,7) scenario explosion → requires performance & caching strategy.
4. 3D & Omniverse (19,24) modeling cost & licensing lead time.
5. Sensing & ML (10,17) long data collection/labeling cycles → defer recommended.
6. NLP (23) domain vocabulary & intent iteration—avoid full version too early.

---
## Strategic Notes
- First lock Phase 1: reliable algorithms + stable data structures + minimal visualization panel.
- Phase 2 shifts to operation efficiency & layout maintenance; prepare versioning and sharing.
- Phase 3 delivers differentiation: advanced 3D simulation, sensing, NLP.
- Delay ML / NLP until operational data volume reduces cold-start risk.

---
## Rough Effort Totals (Indicative Only)
- Phase 1: (BE 24 + FE 13 + DE 16 + DA 9 + Algo 29 + UX 8 + DevOps 6) ≈ 105 person-days
- Phase 2: (BE 21 + FE 20 + DE 15 + DA 11 + Algo 12 + UX 15 + DevOps 10 + 3D 8) ≈ 112 person-days
- Phase 3: (BE 14 + FE 11 + DE 14 + DA 11 + Algo 12 + UX 11 + DevOps 6 + ML 17 + NLP 5 + 3D 16) ≈ 121 person-days
> Possible reduction: If Phase 1 limits to simplest query set (remove offline detail in 4 / reduce scenario combinatorics in 7) save ~8–12 person-days.

---
## Next Documents
Next: `stage-specs.md` will derive objectives, deliverables, acceptance, data prerequisites, boundaries. A third document will cover feasibility & risk mitigation strategies.

---
Further granularity (Story / Epic / Capability mapping) can expand after classification confirmation.
