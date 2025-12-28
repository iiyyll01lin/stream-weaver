# Phase 2 API Specification

**Document Version**: 2.1 | **Last Updated**: 2025-12-13  
**Related Documents**:
- [Phase 2 Architecture](PHASE2_ARCHITECTURE_EN.md)
- [Phase 2 Implementation Guide](PHASE2_IMPLEMENTATION_EN.md)
- [Phase 1 API Specification](PHASE1_API_SPEC_EN.md)

---

## Table of Contents

- [Overview](#overview)
- [New API Endpoints](#new-api-endpoints)
  - [Multi-Line Optimization](#1-multi-line-optimization)
  - [Line Type Recommendation](#2-line-type-recommendation)
  - [Fishbone Diagram Generation](#3-fishbone-diagram-generation)
  - [Layout Management](#4-layout-management)
  - [Product Configuration](#5-product-configuration)
  - [Cross-Line Task Benchmark](#6-cross-line-task-benchmark)
  - [Site Configuration (REQ #6)](#7-site-configuration-new)
  - [Demand Input (REQ #51)](#8-demand-input-new)
  - [Sequence Adjustment (REQ #49)](#9-sequence-adjustment-new)
  - [NPI/MP Stage (REQ #50)](#10-npimp-stage-new)
- [Data Models](#data-models)
- [Error Handling](#error-handling)
- [Usage Examples](#usage-examples)

---

## Overview

Phase 2 API extends Phase 1 with:

1. **Multi-Line Optimization**: Optimize multiple production lines simultaneously
2. **Line Type Recommendation**: Automatic suggestion of optimal line configuration
3. **Fishbone Diagram**: Visual assembly sequence representation
4. **Layout Management**: Save/load 2D production line layouts
5. **Product Configuration**: CTO/BTO mapping database
6. **Site Configuration**: Per-plant threshold management ⚠️ **NEW - REQ #6**
7. **Demand Input**: Customer demand and capacity planning ⚠️ **NEW - REQ #51**
8. **Sequence Adjustment**: Manual assembly order override ⚠️ **NEW - REQ #49**
9. **NPI/MP Stage**: Production stage differentiation ⚠️ **NEW - REQ #50**

### API Version

```
Version: 2.0.0-phase2
Base URL: http://localhost:8000
```

---

## New API Endpoints

### 1. Multi-Line Optimization

#### `POST /optimize` (Extended)

**Phase 2 Enhancement**: Now supports multi-line optimization

**Request Body**:
```json
{
  "work_order_id": "WO_MULTI",
  "optimization_goal": "min_stations",
  "multi_line_config": {
    "enabled": true,
    "lines": [
      {
        "line_id": "A",
        "target_takt": 30000,
        "max_workers_per_station": 3,
        "task_filter": [1, 2, 3, 4, 5]
      },
      {
        "line_id": "B",
        "target_takt": 25000,
        "max_workers_per_station": 2,
        "task_filter": [6, 7, 8, 9, 10]
      }
    ],
    "enable_cross_line_balancing": true
  }
}
```

**Parameters**:

| Field                                   | Type    | Required | Description                     | Phase |
|-----------------------------------------|---------|----------|---------------------------------|-------|
| `multi_line_config.enabled`             | boolean | No       | Enable multi-line mode          | 2     |
| `multi_line_config.lines`               | array   | No       | Array of line configurations    | 2     |
| `multi_line_config.lines[].line_id`     | string  | Yes*     | Line identifier (A, B, C, ...)  | 2     |
| `multi_line_config.lines[].target_takt` | integer | Yes*     | Target takt for this line (ms)  | 2     |
| `multi_line_config.lines[].task_filter` | array   | No       | Task IDs to assign to this line | 2     |
| `enable_cross_line_balancing`           | boolean | No       | Balance workload across lines   | 2     |

**Response (200 OK)**:
```json
{
  "work_order_id": "WO_MULTI",
  "multi_line_results": {
    "total_lines_used": 2,
    "lines": [
      {
        "line_id": "A",
        "stations": [
          {
            "id": "A-WS-001",
            "tasks": [1, 2, 3],
            "load_ms": 28500,
            "utilization": 95.0
          },
          {
            "id": "A-WS-002",
            "tasks": [4, 5],
            "load_ms": 27800,
            "utilization": 92.7
          }
        ],
        "station_count": 2,
        "manpower": 2,
        "takt_time_ms": 30000,
        "utilization_avg": 93.85
      },
      {
        "line_id": "B",
        "stations": [
          {
            "id": "B-WS-001",
            "tasks": [6, 7, 8],
            "load_ms": 24200,
            "utilization": 96.8
          },
          {
            "id": "B-WS-002",
            "tasks": [9, 10],
            "load_ms": 23500,
            "utilization": 94.0
          }
        ],
        "station_count": 2,
        "manpower": 2,
        "takt_time_ms": 25000,
        "utilization_avg": 95.4
      }
    ],
    "cross_line_balance_score": 0.92,
    "total_stations": 4,
    "total_manpower": 4
  },
  "solve_time_sec": 2.3,
  "algorithm_used": "multi_line_cpsat"
}
```

**Field Descriptions**:
- `cross_line_balance_score`: 0-1 score indicating workload balance (1 = perfectly balanced)
- `total_lines_used`: Number of lines actually utilized
- `lines[].utilization_avg`: Average utilization across stations on this line

---

### 2. Line Type Recommendation

#### `GET /recommend-line-type`

Recommend optimal line configuration based on workload analysis.

**Query Parameters**:
```
GET /recommend-line-type?work_order_id=WO_A&target_takt=30000&daily_demand=100
```

| Parameter               | Type    | Required | Description                                                        |
|-------------------------|---------|----------|--------------------------------------------------------------------|
| `work_order_id`         | string  | Yes      | Work order ID                                                      |
| `target_takt`           | integer | Yes      | Target takt time (ms)                                              |
| `max_workers_available` | integer | No       | Available workforce (default: 10)                                  |
| `optimization_goal`     | string  | No       | `min_stations`, `min_manpower`, `min_idle` (default: `min_stations`) |
| `daily_demand`          | integer | No       | Daily production demand (units/day). High demand favors long_line  |
| `product_mix_count`     | integer | No       | Number of product variants (SKUs). High mix favors cell            |
| `changeover_time_ms`    | integer | No       | Product changeover time (ms). High changeover favors cell          |
| `equipment_available`   | array   | No       | List of available equipment IDs (e.g., `["conveyor", "agv", "auto_screwdriver"]`) |
| `product_family`        | string  | No       | Product family code for historical accuracy lookup (e.g., `"DL360"`, `"ML350"`) |

**Input Parameter Details**:
- `optimization_goal`: Different goals favor different line types:
  - `min_stations` → Favors cells or short lines
  - `min_manpower` → Favors long lines with specialized workers
  - `min_idle` → Favors short lines with balanced workload
- `daily_demand`: Critical for capacity planning:
  - Low demand (<50/day) → Cell recommended
  - Medium demand (50-200/day) → Short line recommended
  - High demand (>200/day) → Long line recommended
- `product_mix_count`: Indicates production flexibility needs:
  - High-mix (>10 variants) → Cell for quick changeovers
  - Low-mix (1-3 variants) → Long line for efficiency
- `available_space_sqm`: Physical space constraint validation:
  - Cell: ~20-50 m² per station
  - Short line: ~150-400 m² total
  - Long line: ~500+ m² required
- `multi_skill_worker_count`: Skill availability check:
  - Cell requires workers who can perform all tasks
  - Long line allows single-skill specialists
- `quality_target_dppm`: Quality-driven decision:
  - < 100 DPPM → Fewer handoffs preferred (cell)
  - > 500 DPPM → Long line acceptable
- `demand_variability_pct`: Flexibility requirement:
  - > 30% variability → Cell for demand swings
  - < 10% variability → Long line efficiency OK
- `is_new_product`: Learning curve consideration:
  - NPI phase → Cell for rapid iteration/debugging
  - Mature product → Long line for efficiency
- `equipment_available`: Equipment constraint validation:
  - Cell: Requires flexible tooling, multi-purpose fixtures
  - Short line: Requires dedicated fixtures, conveyors
  - Long line: Requires automated stations, AGVs, specialized equipment
  - Missing equipment → Line type marked as infeasible
- `product_family`: Historical accuracy lookup:
  - Used to query past recommendations for similar products
  - Enables learning from override patterns
  - Example: `"DL360"` → retrieves DL360 G10/G11 recommendation history

**Response (200 OK)**:
```json
{
  "work_order_id": "WO_A",
  "recommended_type": "short_line",
  "confidence": 0.85,
  "reasoning": {
    "task_count": 35,
    "total_work_ms": 156000,
    "target_takt_ms": 30000,
    "theoretical_min_stations": 6,
    "recommended_stations": 6,
    "complexity_distribution": {
      "simple": 20,
      "medium": 10,
      "complex": 5
    },
    "decision_factors": [
      "Task count (35) fits short_line range (20-50)",
      "Theoretical 6 stations within short_line definition (4-8)",
      "Medium complexity dominates - dedicated workers efficient",
      "Daily demand (120) matches short_line capacity"
    ]
  },
  "alternatives": [
    {
      "type": "cell",
      "feasible": false,
      "suitability": 0.3,
      "reason": "Would require 6 stations; exceeds cell max (3)",
      "estimated_workers": null,
      "estimated_efficiency": null
    },
    {
      "type": "short_line",
      "feasible": true,
      "suitability": 0.85,
      "reason": "Optimal fit for workload and demand",
      "estimated_workers": 6,
      "estimated_efficiency": 0.82
    },
    {
      "type": "long_line",
      "feasible": true,
      "suitability": 0.55,
      "reason": "Possible but underutilized for current demand",
      "estimated_workers": 9,
      "estimated_efficiency": 0.58
    }
  ],
  "manpower_estimates": {
    "cell": null,
    "short_line": 6,
    "long_line": 9
  },
  "warnings": [
    "5 complex tasks may create bottleneck at single station",
    "Consider splitting task 9 (GPU mount) if takt is tight"
  ],
  "recommendations": [
    "Use short line with 6 stations",
    "Consider offline processing for 3 glue tasks",
    "Group similar screw operations to reduce transitions"
  ],
  "cost_analysis": {
    "cell": {
      "cost_per_unit": 12.50,
      "labor_cost": 10.00,
      "overhead_cost": 2.50,
      "annual_operating_cost": 456000
    },
    "short_line": {
      "cost_per_unit": 9.80,
      "labor_cost": 7.50,
      "overhead_cost": 2.30,
      "annual_operating_cost": 520000
    },
    "long_line": {
      "cost_per_unit": 8.20,
      "labor_cost": 5.80,
      "overhead_cost": 2.40,
      "annual_operating_cost": 680000
    }
  },
  "implementation": {
    "cell": {
      "setup_days": 1,
      "training_days": 0.5,
      "equipment_ready": true,
      "space_required_sqm": 45
    },
    "short_line": {
      "setup_days": 3,
      "training_days": 1,
      "equipment_ready": true,
      "space_required_sqm": 180
    },
    "long_line": {
      "setup_days": 7,
      "training_days": 2,
      "equipment_ready": false,
      "space_required_sqm": 520
    }
  },
  "risk_assessment": {
    "cell": {
      "bottleneck_risk": "low",
      "single_point_failure": "low",
      "quality_risk": "low",
      "flexibility_score": 0.95
    },
    "short_line": {
      "bottleneck_risk": "medium",
      "single_point_failure": "medium",
      "quality_risk": "medium",
      "flexibility_score": 0.70
    },
    "long_line": {
      "bottleneck_risk": "high",
      "single_point_failure": "high",
      "quality_risk": "medium",
      "flexibility_score": 0.40
    }
  },
  "constraints_check": {
    "space_sufficient": {
      "cell": true,
      "short_line": true,
      "long_line": false
    },
    "workers_qualified": {
      "cell": false,
      "short_line": true,
      "long_line": true
    },
    "quality_achievable": {
      "cell": true,
      "short_line": true,
      "long_line": false
    },
    "equipment_available": {
      "cell": true,
      "short_line": true,
      "long_line": false
    }
  },
  "equipment_check": {
    "cell": {
      "feasible": true,
      "required_equipment": ["flexible_tooling"],
      "missing_equipment": []
    },
    "short_line": {
      "feasible": true,
      "required_equipment": ["conveyor", "dedicated_fixture"],
      "missing_equipment": []
    },
    "long_line": {
      "feasible": false,
      "required_equipment": ["conveyor", "agv", "automated_station"],
      "missing_equipment": ["agv", "automated_station"]
    }
  },
  "scenario_comparison": {
    "current_demand": {
      "best_type": "short_line",
      "efficiency": 0.82
    },
    "peak_demand_150pct": {
      "best_type": "long_line",
      "efficiency": 0.78
    },
    "low_demand_50pct": {
      "best_type": "cell",
      "efficiency": 0.75
    }
  }
}
```

**Line Type Definitions**:

| Line Type    | Station Count | Task Count | Worker Type  | Daily Demand | Key Characteristics                                      |
|--------------|---------------|------------|--------------|--------------|----------------------------------------------------------|
| `cell`       | 1 - 3         | < 20       | Flexible     | < 50/day     | High flexibility; suitable for low-volume, high-mix      |
| `short_line` | 4 - 8         | 20 - 50    | Dedicated    | 50-200/day   | Balanced efficiency; standardized task sets              |
| `long_line`  | 9+            | > 50       | Specialized  | > 200/day    | High specialization; maximizes output, minimizes idle    |

**Response Field Descriptions**:

| Field                           | Type    | Description                                                        |
|---------------------------------|---------|--------------------------------------------------------------------|
| `recommended_type`              | string  | `cell`, `short_line`, or `long_line`                               |
| `confidence`                    | float   | 0-1 score indicating recommendation certainty                     |
| `reasoning.theoretical_min_stations` | integer | `ceil(total_work_ms / target_takt_ms)`                      |
| `reasoning.decision_factors`    | array   | Human-readable explanations for the recommendation                 |
| `alternatives[].feasible`       | boolean | Whether this line type is feasible for the workload                |
| `alternatives[].estimated_workers` | integer | Estimated workforce required for this line type                 |
| `alternatives[].estimated_efficiency` | float | Predicted line efficiency (0-1)                               |
| `manpower_estimates`            | object  | Quick lookup of worker count per line type                         |
| `warnings`                      | array   | Potential issues or risks with the recommendation                  |
| `cost_analysis`                 | object  | Operating cost breakdown per line type (NEW)                       |
| `cost_analysis[type].cost_per_unit` | float | Estimated cost per unit produced                              |
| `cost_analysis[type].annual_operating_cost` | float | Projected annual operating cost                      |
| `implementation`                | object  | Setup effort per line type (NEW)                                   |
| `implementation[type].setup_days` | integer | Days to set up and configure the line                           |
| `implementation[type].training_days` | float | Days required for worker training                             |
| `implementation[type].space_required_sqm` | float | Floor space required (m²)                               |
| `risk_assessment`               | object  | Risk analysis per line type (NEW)                                  |
| `risk_assessment[type].bottleneck_risk` | string | `low`, `medium`, `high`                                  |
| `risk_assessment[type].flexibility_score` | float | 0-1 ability to handle changes                           |
| `constraints_check`             | object  | Feasibility validation results (NEW)                               |
| `constraints_check.space_sufficient` | object | Per-type space feasibility boolean                            |
| `constraints_check.workers_qualified` | object | Per-type skill availability boolean                          |
| `constraints_check.quality_achievable` | object | Per-type quality target feasibility boolean                 |
| `constraints_check.equipment_available` | object | Per-type equipment feasibility boolean (NEW)            |
| `equipment_check`               | object  | Detailed equipment validation per line type (NEW)                  |
| `equipment_check[type].feasible` | boolean | Whether required equipment is available                          |
| `equipment_check[type].required_equipment` | array | List of required equipment for this line type           |
| `equipment_check[type].missing_equipment` | array | List of required equipment that is not available         |
| `scenario_comparison`           | object  | What-if analysis for demand scenarios (NEW)                        |
| `confidence_interval`           | object  | Statistical confidence range (NEW)                                 |
| `confidence_interval.low`       | float   | Lower bound of confidence (e.g., 0.78)                             |
| `confidence_interval.high`      | float   | Upper bound of confidence (e.g., 0.92)                             |
| `confidence_interval.sample_size` | integer | Number of similar past recommendations used                     |
| `historical_accuracy`           | object  | Learning from past recommendations (NEW)                           |
| `historical_accuracy.product_family` | string | Product family used for lookup                              |
| `historical_accuracy.past_recommendations` | integer | Number of historical recommendations found           |
| `historical_accuracy.accuracy_rate` | float | Accuracy of past recommendations (0-1)                       |
| `historical_accuracy.common_override_reason` | string | Most frequent reason for user override             |

**Confidence Score Calculation**:
- Base score from task count / station count alignment
- Adjusted by complexity distribution match
- Penalized if constraints are borderline (e.g., 19 tasks for cell)
- Range: 0.0 (uncertain) to 1.0 (highly confident)

---

### 2.1 Line Type Recommendation Feedback (NEW)

#### `POST /recommend-line-type/feedback`

Record user decision on line type recommendation for continuous learning.

**Request Body**:
```json
{
  "recommendation_id": "rec_20251212_WO_A_001",
  "work_order_id": "WO_A",
  "recommended_type": "short_line",
  "user_decision": "overridden",
  "actual_type": "cell",
  "override_reason": "space_constraint",
  "comments": "Factory floor space limited, cell fits better",
  "user_id": "engineer_001"
}
```

**Parameters**:

| Field               | Type   | Required | Description                                                            |
|---------------------|--------|----------|------------------------------------------------------------------------|
| `recommendation_id` | string | Yes      | Unique ID from recommendation response                                 |
| `work_order_id`     | string | Yes      | Work order ID                                                          |
| `recommended_type`  | string | Yes      | Original recommendation (`cell`, `short_line`, `long_line`)            |
| `user_decision`     | string | Yes      | `accepted` or `overridden`                                             |
| `actual_type`       | string | No*      | Actual line type used (required if `overridden`)                       |
| `override_reason`   | string | No*      | Reason category (required if `overridden`)                             |
| `comments`          | string | No       | Free-text explanation                                                  |
| `user_id`           | string | No       | User who made the decision                                             |

**Override Reason Categories**:
- `space_constraint` - Physical space limitation
- `worker_availability` - Insufficient skilled workers
- `equipment_unavailable` - Required equipment not available
- `quality_requirement` - Stricter quality target than analyzed
- `demand_change` - Demand forecast changed
- `cost_constraint` - Budget limitations
- `management_decision` - Strategic/policy override
- `other` - Other reason (specify in comments)

**Response (200 OK)**:
```json
{
  "feedback_id": "fb_20251212_001",
  "recommendation_id": "rec_20251212_WO_A_001",
  "status": "recorded",
  "accuracy_impact": {
    "previous_accuracy": 0.82,
    "updated_accuracy": 0.80,
    "total_recommendations": 16
  },
  "message": "Feedback recorded. Thank you for helping improve recommendations."
}
```

**Response (400 Bad Request)**:
```json
{
  "detail": "actual_type required when user_decision is 'overridden'",
  "error_code": "MISSING_REQUIRED_FIELD"
}
```

---

#### `GET /recommend-line-type/history`

Retrieve historical recommendations and their outcomes.

**Query Parameters**:
```
GET /recommend-line-type/history?product_family=DL360&limit=50
```

| Parameter        | Type    | Required | Description                              |
|------------------|---------|----------|------------------------------------------|
| `product_family` | string  | No       | Filter by product family                 |
| `work_order_id`  | string  | No       | Filter by work order                     |
| `from_date`      | date    | No       | Start date (YYYY-MM-DD)                  |
| `to_date`        | date    | No       | End date (YYYY-MM-DD)                    |
| `decision`       | string  | No       | Filter by decision: `accepted`, `overridden` |
| `limit`          | integer | No       | Max results (default: 50)                |

**Response (200 OK)**:
```json
{
  "total_count": 45,
  "recommendations": [
    {
      "recommendation_id": "rec_20251212_WO_A_001",
      "work_order_id": "WO_A",
      "product_family": "DL360",
      "recommended_type": "short_line",
      "confidence": 0.85,
      "user_decision": "accepted",
      "actual_type": "short_line",
      "created_at": "2025-12-12T10:30:00Z",
      "decided_at": "2025-12-12T14:00:00Z"
    }
  ],
  "summary": {
    "acceptance_rate": 0.82,
    "top_override_reasons": [
      {"reason": "space_constraint", "count": 5},
      {"reason": "worker_availability", "count": 3}
    ]
  }
}
```

---

### 2.5 Batch Recommendation (Optional Enhancement)

#### `POST /recommend-line-type/batch`

Generate recommendations for multiple work orders simultaneously.

**Request Body**:
```json
{
  "work_order_ids": ["WO_A", "WO_B", "WO_C"],
  "common_params": {
    "site_id": "TPE_SITE_01",
    "product_family": "DL360"
  }
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `work_order_ids` | array | Yes | List of work order IDs to process |
| `common_params` | object | No | Common parameters applied to all requests |
| `common_params.site_id` | string | No | Site ID for site-specific thresholds |
| `common_params.product_family` | string | No | Product family for historical context |

**Response (200 OK)**:
```json
{
  "results": [
    {
      "work_order_id": "WO_A",
      "recommended_type": "cell",
      "confidence_score": 0.88,
      "processing_time_ms": 45
    },
    {
      "work_order_id": "WO_B",
      "recommended_type": "short_line",
      "confidence_score": 0.76,
      "processing_time_ms": 52
    },
    {
      "work_order_id": "WO_C",
      "error": "Work order not found",
      "status": "failed"
    }
  ],
  "summary": {
    "total": 3,
    "succeeded": 2,
    "failed": 1,
    "total_processing_time_ms": 150
  },
  "cached_count": 1
}
```

---

### 2.6 Export Recommendation Report (Optional Enhancement)

#### `GET /recommend-line-type/export`

Export recommendation report in PDF or Excel format.

**Query Parameters**:
```
GET /recommend-line-type/export?work_order_id=WO_A&format=pdf&include_charts=true
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `work_order_id` | string | Yes | Work order ID |
| `format` | string | No | Export format: `pdf` or `xlsx` (default: `pdf`) |
| `include_charts` | boolean | No | Include comparison charts (default: `true`) |
| `language` | string | No | Report language: `en` or `zh` (default: `en`) |

**Response (200 OK)**:
```http
Content-Type: application/pdf  (or application/vnd.openxmlformats-officedocument.spreadsheetml.sheet)
Content-Disposition: attachment; filename="recommendation_WO_A_20240115.pdf"

[Binary file content]
```

**Report Contents**:
| Section | Description |
|---------|-------------|
| Executive Summary | Recommended line type with confidence score |
| Input Parameters | All 14 input parameters used |
| Comparison Matrix | Score breakdown for all line types |
| Cost Analysis | Per-line-type cost breakdown with charts |
| Risk Assessment | Risk scores visualization |
| Constraints Check | Pass/fail status with details |
| Historical Context | Accuracy metrics for product family |
| Appendix | Data sources and methodology |

---

### 2.7 Configurable Thresholds API (Optional Enhancement)

#### `GET /recommend-line-type/thresholds`

Retrieve current scoring thresholds.

**Query Parameters**:
```
GET /recommend-line-type/thresholds?site_id=TPE_SITE_01
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `site_id` | string | No | Site ID for site-specific thresholds |
| `product_family` | string | No | Product family for specific thresholds |

**Response (200 OK)**:
```json
{
  "site_id": "TPE_SITE_01",
  "product_family": null,
  "thresholds": {
    "task_count": {
      "cell_max": 20,
      "short_line_min": 15,
      "short_line_max": 50,
      "long_line_min": 40
    },
    "daily_demand": {
      "low_max": 50,
      "medium_max": 200
    },
    "quality_level": {
      "premium_threshold": 0.9,
      "standard_threshold": 0.7
    },
    "cost_weights": {
      "labor_factor": 0.4,
      "equipment_factor": 0.35,
      "space_factor": 0.15,
      "transition_factor": 0.1
    }
  },
  "source": "site_config",
  "last_updated": "2024-01-15T10:30:00Z",
  "updated_by": "admin@example.com"
}
```

#### `PUT /recommend-line-type/thresholds`

Update scoring thresholds for a site or product family.

**Request Body**:
```json
{
  "site_id": "TPE_SITE_01",
  "product_family": "DL360",
  "thresholds": {
    "task_count": {
      "cell_max": 25,
      "short_line_min": 20,
      "short_line_max": 60,
      "long_line_min": 45
    },
    "daily_demand": {
      "low_max": 60,
      "medium_max": 250
    },
    "quality_level": {
      "premium_threshold": 0.95,
      "standard_threshold": 0.8
    }
  },
  "reason": "Adjusted for new DL360 G11 product launch"
}
```

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `site_id` | string | Yes | Target site ID |
| `product_family` | string | No | Target product family (null = site-wide) |
| `thresholds` | object | Yes | Threshold configuration object |
| `reason` | string | No | Change reason for audit trail |

**Response (200 OK)**:
```json
{
  "status": "updated",
  "site_id": "TPE_SITE_01",
  "product_family": "DL360",
  "effective_from": "2024-01-15T10:35:00Z",
  "previous_version_id": "thresh_v12",
  "new_version_id": "thresh_v13"
}
```

#### `DELETE /recommend-line-type/thresholds`

Reset thresholds to default values.

**Query Parameters**:
```
DELETE /recommend-line-type/thresholds?site_id=TPE_SITE_01&product_family=DL360
```

**Response (200 OK)**:
```json
{
  "status": "reset_to_default",
  "site_id": "TPE_SITE_01",
  "product_family": "DL360"
}
```

---

### 2.8 A/B Testing Framework (Optional Enhancement)

Enable algorithm variation testing in production for continuous improvement.

#### `GET /recommend-line-type/experiments`

List active and completed A/B experiments.

**Query Parameters**:
```
GET /recommend-line-type/experiments?status=active
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `status` | string | No | Filter: `active`, `completed`, `paused` (default: all) |

**Response (200 OK)**:
```json
{
  "experiments": [
    {
      "experiment_id": "exp_algo_v2_2024",
      "name": "Enhanced Scoring Algorithm v2",
      "status": "active",
      "start_date": "2024-01-01T00:00:00Z",
      "end_date": null,
      "variants": [
        {
          "variant_id": "control",
          "name": "Current Algorithm (v1.0)",
          "traffic_percent": 50,
          "description": "Baseline multi-factor scoring"
        },
        {
          "variant_id": "treatment_a",
          "name": "ML-Enhanced Scoring (v2.0)",
          "traffic_percent": 50,
          "description": "Machine learning weight optimization"
        }
      ],
      "metrics": {
        "primary": "acceptance_rate",
        "secondary": ["confidence_accuracy", "override_rate", "user_satisfaction"]
      },
      "current_results": {
        "control": {
          "sample_size": 1250,
          "acceptance_rate": 0.78,
          "avg_confidence": 0.82
        },
        "treatment_a": {
          "sample_size": 1248,
          "acceptance_rate": 0.85,
          "avg_confidence": 0.88
        }
      },
      "statistical_significance": {
        "p_value": 0.023,
        "is_significant": true,
        "confidence_level": 0.95
      }
    }
  ],
  "total": 1
}
```

#### `POST /recommend-line-type/experiments`

Create a new A/B experiment.

**Request Body**:
```json
{
  "name": "Cost Weight Optimization",
  "description": "Test different cost factor weights",
  "variants": [
    {
      "variant_id": "control",
      "name": "Current Weights",
      "traffic_percent": 50,
      "config": {
        "cost_weights": {
          "labor_factor": 0.4,
          "equipment_factor": 0.35
        }
      }
    },
    {
      "variant_id": "treatment_a",
      "name": "Labor-Heavy Weights",
      "traffic_percent": 50,
      "config": {
        "cost_weights": {
          "labor_factor": 0.55,
          "equipment_factor": 0.25
        }
      }
    }
  ],
  "target_sample_size": 2000,
  "metrics": {
    "primary": "acceptance_rate",
    "secondary": ["user_satisfaction"]
  },
  "targeting": {
    "site_ids": ["TPE_SITE_01", "TPE_SITE_02"],
    "product_families": null
  }
}
```

**Response (201 Created)**:
```json
{
  "experiment_id": "exp_cost_2024_q1",
  "status": "active",
  "created_at": "2024-01-15T10:00:00Z",
  "estimated_completion": "2024-02-15T10:00:00Z"
}
```

#### `PUT /recommend-line-type/experiments/{experiment_id}`

Update experiment status (pause, resume, conclude).

**Request Body**:
```json
{
  "action": "conclude",
  "winner_variant": "treatment_a",
  "apply_winner": true,
  "notes": "Treatment A showed 9% improvement in acceptance rate"
}
```

**Response (200 OK)**:
```json
{
  "experiment_id": "exp_algo_v2_2024",
  "status": "completed",
  "concluded_at": "2024-01-15T15:00:00Z",
  "winner": "treatment_a",
  "applied_to_production": true,
  "final_results": {
    "control": {
      "sample_size": 1250,
      "acceptance_rate": 0.78
    },
    "treatment_a": {
      "sample_size": 1248,
      "acceptance_rate": 0.85,
      "improvement": "+8.97%"
    }
  }
}
```

---

### 2.9 Recommendation Explanation NLP (Optional Enhancement - Phase 3 Prep)

Generate natural language explanations for recommendations.

#### `GET /recommend-line-type/explain`

Get human-readable explanation for a recommendation.

**Query Parameters**:
```
GET /recommend-line-type/explain?work_order_id=WO_A&language=en&detail_level=standard
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `work_order_id` | string | Yes | Work order ID |
| `language` | string | No | `en` or `zh` (default: `en`) |
| `detail_level` | string | No | `brief`, `standard`, `detailed` (default: `standard`) |
| `audience` | string | No | `operator`, `engineer`, `manager` (default: `engineer`) |

**Response (200 OK)**:
```json
{
  "work_order_id": "WO_A",
  "recommendation": {
    "type": "cell",
    "confidence": 0.88
  },
  "explanation": {
    "summary": "Based on your work order analysis, we recommend a **Cell Production** layout with 88% confidence.",
    "key_factors": [
      {
        "factor": "Task Count",
        "value": 15,
        "impact": "positive",
        "explanation": "With only 15 tasks, a cell layout allows one or two skilled workers to complete the entire assembly, reducing handoff delays."
      },
      {
        "factor": "Daily Demand",
        "value": 35,
        "impact": "positive",
        "explanation": "Low daily demand (35 units) doesn't justify the overhead of a longer production line."
      },
      {
        "factor": "Product Mix",
        "value": 8,
        "impact": "strong_positive",
        "explanation": "With 8 product variants, cell production provides the flexibility needed for quick changeovers without reconfiguring the entire line."
      }
    ],
    "alternatives_considered": [
      {
        "type": "short_line",
        "score": 0.72,
        "why_not": "A short line would require more workers (5-6) for similar output, increasing labor costs by approximately 40% without proportional efficiency gains."
      },
      {
        "type": "long_line",
        "score": 0.45,
        "why_not": "Long line production is not recommended due to low demand volume. The line would operate at only 35% utilization, wasting equipment and floor space."
      }
    ],
    "risks_mentioned": [
      "Worker skill dependency: Ensure at least 2 cross-trained workers are available for cell operation.",
      "Quality checkpoint: Consider adding inline inspection at the cell to maintain DPPM targets."
    ],
    "action_items": [
      "Verify multi-skilled worker availability (minimum 2 required)",
      "Allocate 40-50 m² floor space for cell setup",
      "Prepare flexible tooling kit for 8 product variants"
    ]
  },
  "generated_at": "2024-01-15T10:30:00Z",
  "generation_model": "gpt-4-turbo",
  "tokens_used": 450
}
```

**Detail Level Examples**:

| Level | Output Length | Use Case |
|-------|---------------|----------|
| `brief` | 2-3 sentences | Quick overview for operators |
| `standard` | Full structured explanation | Engineer decision-making |
| `detailed` | Extended with calculations | Management reports, audits |

**Audience Adaptation**:

| Audience | Language Style | Technical Depth |
|----------|----------------|-----------------|
| `operator` | Simple, action-focused | Low - what to do |
| `engineer` | Technical, data-driven | Medium - why it works |
| `manager` | Business-focused, ROI | High - cost/risk impact |

---

### 2.10 Audit Trail API (Optional Enhancement)

Track complete decision history for compliance and debugging.

#### `GET /recommend-line-type/audit`

Retrieve audit trail for a recommendation.

**Query Parameters**:
```
GET /recommend-line-type/audit?recommendation_id=rec_abc123
```

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `recommendation_id` | string | Yes* | Specific recommendation ID |
| `work_order_id` | string | Yes* | Work order ID (returns all related) |
| `from_date` | string | No | Start date filter (ISO 8601) |
| `to_date` | string | No | End date filter (ISO 8601) |
| `actor` | string | No | Filter by user/system |

*At least one of `recommendation_id` or `work_order_id` required.

**Response (200 OK)**:
```json
{
  "recommendation_id": "rec_abc123",
  "work_order_id": "WO_A",
  "audit_trail": [
    {
      "event_id": "evt_001",
      "timestamp": "2024-01-15T10:00:00Z",
      "action": "recommendation_created",
      "actor": "system",
      "details": {
        "algorithm_version": "v2.1.0",
        "experiment_variant": "treatment_a",
        "input_hash": "sha256:abc123..."
      }
    },
    {
      "event_id": "evt_002",
      "timestamp": "2024-01-15T10:05:00Z",
      "action": "recommendation_viewed",
      "actor": "engineer@example.com",
      "details": {
        "client_ip": "192.168.1.100",
        "user_agent": "Mozilla/5.0..."
      }
    },
    {
      "event_id": "evt_003",
      "timestamp": "2024-01-15T10:10:00Z",
      "action": "recommendation_overridden",
      "actor": "engineer@example.com",
      "details": {
        "original_recommendation": "cell",
        "override_to": "short_line",
        "override_reason": "space_constraint",
        "notes": "Cell area under renovation until Q2"
      }
    },
    {
      "event_id": "evt_004",
      "timestamp": "2024-01-15T10:15:00Z",
      "action": "recommendation_approved",
      "actor": "supervisor@example.com",
      "details": {
        "approval_level": "supervisor",
        "final_decision": "short_line"
      }
    },
    {
      "event_id": "evt_005",
      "timestamp": "2024-01-15T10:20:00Z",
      "action": "recommendation_applied",
      "actor": "system",
      "details": {
        "line_id": "LINE_B",
        "configuration_id": "cfg_xyz789"
      }
    }
  ],
  "input_snapshot": {
    "captured_at": "2024-01-15T10:00:00Z",
    "parameters": {
      "work_order_id": "WO_A",
      "target_takt": 60000,
      "daily_demand": 35,
      "product_mix_count": 8
    }
  },
  "decision_factors": {
    "scores": {
      "cell": 0.88,
      "short_line": 0.72,
      "long_line": 0.45
    },
    "constraints_at_time": {
      "space_constraint": {"passed": true},
      "worker_constraint": {"passed": true}
    },
    "thresholds_version": "thresh_v13"
  },
  "compliance": {
    "retention_policy": "7_years",
    "data_classification": "internal",
    "gdpr_relevant": false
  }
}
```

---

### 3. Fishbone Diagram Generation

#### `GET /fishbone-diagram`

Generate assembly sequence fishbone diagram.

**Query Parameters**:
```
GET /fishbone-diagram?work_order_id=WO_A&format=svg
```

| Parameter                 | Type    | Required | Description                                    |
|---------------------------|---------|----------|------------------------------------------------|
| `work_order_id`           | string  | Yes      | Work order ID                                  |
| `format`                  | string  | No       | Output format: `svg` or `png` (default: `svg`) |
| `highlight_critical_path` | boolean | No       | Highlight critical path (default: `false`)     |

**Response (200 OK)**:
```http
Content-Type: image/svg+xml

<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="1000">
  <!-- Fishbone diagram SVG content -->
  <line x1="0" y1="500" x2="1600" y2="500" stroke="black" stroke-width="3"/>
  <circle cx="200" cy="300" r="30" fill="#3498db"/>
  <text x="200" y="305" text-anchor="middle">1</text>
  <!-- ... more elements ... -->
</svg>
```

**Download Example**:
```bash
curl "http://localhost:8000/fishbone-diagram?work_order_id=WO_A&format=png" \
  -o fishbone_WO_A.png
```

---

### 4. Layout Management

#### 4.1 `GET /layout`

List all saved layouts.

**Query Parameters**:
```
GET /layout?site=factory_A
```

| Parameter | Type    | Required | Description               |
|-----------|---------|----------|---------------------------|
| `site`    | string  | No       | Filter by site name       |
| `limit`   | integer | No       | Max results (default: 50) |

**Response (200 OK)**:
```json
{
  "layouts": [
    {
      "id": 1,
      "name": "Factory A - Line 1",
      "description": "Standard assembly line layout",
      "site": "factory_A",
      "created_at": "2025-11-10T10:30:00Z",
      "updated_at": "2025-11-12T14:20:00Z"
    },
    {
      "id": 2,
      "name": "Factory B - Cell Configuration",
      "description": "U-shaped cell for custom builds",
      "site": "factory_B",
      "created_at": "2025-11-11T09:15:00Z",
      "updated_at": "2025-11-11T09:15:00Z"
    }
  ],
  "total_count": 2
}
```

---

#### 4.2 `GET /layout/{layout_id}`

Retrieve specific layout data.

**Path Parameters**:
- `layout_id` (integer): Layout ID

**Response (200 OK)**:
```json
{
  "id": 1,
  "name": "Factory A - Line 1",
  "description": "Standard assembly line layout",
  "site": "factory_A",
  "data": {
    "stations": [
      {
        "id": "WS-001",
        "x": 100,
        "y": 200,
        "width": 80,
        "height": 60,
        "type": "assembly"
      },
      {
        "id": "WS-002",
        "x": 250,
        "y": 200,
        "width": 80,
        "height": 60,
        "type": "assembly"
      },
      {
        "id": "QC-001",
        "x": 400,
        "y": 200,
        "width": 60,
        "height": 60,
        "type": "quality_check"
      }
    ],
    "connections": [
      {
        "from": "WS-001",
        "to": "WS-002",
        "type": "conveyor"
      },
      {
        "from": "WS-002",
        "to": "QC-001",
        "type": "manual_transfer"
      }
    ],
    "dimensions": {
      "width": 1000,
      "height": 600
    }
  },
  "created_at": "2025-11-10T10:30:00Z",
  "updated_at": "2025-11-12T14:20:00Z"
}
```

---

#### 4.3 `POST /save-layout`

Save new or update existing layout.

**Request Body**:
```json
{
  "id": null,
  "name": "Factory C - New Line",
  "description": "High-volume production line",
  "site": "factory_C",
  "data": {
    "stations": [
      {
        "id": "WS-001",
        "x": 100,
        "y": 200,
        "width": 80,
        "height": 60,
        "type": "assembly"
      }
    ],
    "connections": [],
    "dimensions": {
      "width": 1200,
      "height": 800
    }
  }
}
```

**Response (200 OK)**:
```json
{
  "layout_id": 3,
  "status": "saved",
  "message": "Layout saved successfully",
  "created_at": "2025-11-12T15:00:00Z"
}
```

**Response (200 OK - Update)**:
```json
{
  "layout_id": 1,
  "status": "updated",
  "message": "Layout updated successfully",
  "updated_at": "2025-11-12T15:05:00Z"
}
```

---

#### 4.4 `DELETE /layout/{layout_id}`

Delete a layout.

**Path Parameters**:
- `layout_id` (integer): Layout ID

**Response (200 OK)**:
```json
{
  "layout_id": 3,
  "status": "deleted",
  "message": "Layout deleted successfully"
}
```

---

### 5. Product Configuration

#### 5.1 `GET /product-config`

Retrieve product configurations (CTO/BTO mappings).

**Query Parameters**:
```
GET /product-config?sku=DL360_G10
```

| Parameter    | Type   | Required | Description                                          |
|--------------|--------|----------|------------------------------------------------------|
| `sku`        | string | No       | Product SKU filter                                   |
| `complexity` | string | No       | Filter by complexity (`simple`, `medium`, `complex`) |

**Response (200 OK - Single SKU)**:
```json
{
  "sku": "DL360_G10",
  "product_name": "HP ProLiant DL360 Gen10",
  "default_complexity": "medium",
  "cto_bto_map": {
    "cpu": {
      "intel_xeon_silver": {
        "part_id": "CPU_XEON_SILVER_4214",
        "assembly_time_ms": 8000,
        "complexity": "medium"
      },
      "intel_xeon_gold": {
        "part_id": "CPU_XEON_GOLD_6248",
        "assembly_time_ms": 8500,
        "complexity": "complex"
      }
    },
    "memory": {
      "16gb_ddr4": {
        "part_id": "MEM_16GB_DDR4",
        "assembly_time_ms": 3000,
        "complexity": "simple"
      },
      "32gb_ddr4": {
        "part_id": "MEM_32GB_DDR4",
        "assembly_time_ms": 3500,
        "complexity": "simple"
      }
    },
    "storage": {
      "ssd_480gb": {
        "part_id": "SSD_480GB",
        "assembly_time_ms": 5000,
        "complexity": "simple"
      },
      "hdd_2tb": {
        "part_id": "HDD_2TB",
        "assembly_time_ms": 6000,
        "complexity": "medium"
      }
    }
  },
  "created_at": "2025-11-01T00:00:00Z"
}
```

**Response (200 OK - All Products)**:
```json
{
  "products": [
    {
      "sku": "DL360_G10",
      "product_name": "HP ProLiant DL360 Gen10",
      "default_complexity": "medium",
      "config_count": 3
    },
    {
      "sku": "ML350_G11",
      "product_name": "HP ProLiant ML350 Gen11",
      "default_complexity": "complex",
      "config_count": 5
    }
  ],
  "total_count": 2
}
```

---

#### 5.2 `POST /product-config`

Create or update product configuration.

**Request Body**:
```json
{
  "sku": "DL320_G11",
  "product_name": "HP ProLiant DL320 Gen11",
  "default_complexity": "simple",
  "cto_bto_map": {
    "cpu": {
      "intel_xeon_bronze": {
        "part_id": "CPU_XEON_BRONZE_3204",
        "assembly_time_ms": 7000,
        "complexity": "simple"
      }
    },
    "memory": {
      "8gb_ddr4": {
        "part_id": "MEM_8GB_DDR4",
        "assembly_time_ms": 2500,
        "complexity": "simple"
      }
    }
  }
}
```

**Response (200 OK)**:
```json
{
  "config_id": 3,
  "sku": "DL320_G11",
  "status": "created",
  "message": "Product configuration saved successfully"
}
```

---

#### 5.3 `DELETE /product-config/{sku}`

Delete product configuration.

**Path Parameters**:
- `sku` (string): Product SKU

**Response (200 OK)**:
```json
{
  "sku": "DL320_G11",
  "status": "deleted",
  "message": "Product configuration deleted successfully"
}
```

---

### 6. Cross-Line Task Benchmark

Compare task execution times across different production lines to identify efficiency gaps and best practices.

#### 6.1 `GET /benchmark/cross-line-tasks`

Retrieve cross-line task time comparison report.

**Query Parameters**:
```
GET /benchmark/cross-line-tasks?line_ids=L1,L2,L3&date_from=2025-12-01&date_to=2025-12-31
```

| Parameter   | Type   | Required | Description                                |
|-------------|--------|----------|--------------------------------------------|
| `line_ids`  | string | Yes      | Comma-separated line IDs to compare        |
| `task_ids`  | string | No       | Comma-separated task IDs (optional filter) |
| `date_from` | string | No       | Start date (ISO 8601 format)               |
| `date_to`   | string | No       | End date (ISO 8601 format)                 |

**Response (200 OK)**:
```json
{
  "benchmark_id": "BM-20251202-001",
  "generated_at": "2025-12-02T10:30:00Z",
  "lines_compared": ["L1", "L2", "L3"],
  "task_benchmarks": [
    {
      "task_id": "T001",
      "task_name": "Install RAM",
      "line_stats": {
        "L1": {
          "avg_ms": 12500,
          "std_ms": 850,
          "min_ms": 10200,
          "max_ms": 15800,
          "samples": 45
        },
        "L2": {
          "avg_ms": 11800,
          "std_ms": 720,
          "min_ms": 9800,
          "max_ms": 14200,
          "samples": 52
        },
        "L3": {
          "avg_ms": 13200,
          "std_ms": 1100,
          "min_ms": 10500,
          "max_ms": 17000,
          "samples": 38
        }
      },
      "best_line": "L2",
      "worst_line": "L3",
      "variance_percent": 11.9,
      "severity": "warning",
      "recommendation": "L3 is 11.9% slower than best line L2. Review work instructions and tooling."
    },
    {
      "task_id": "T002",
      "task_name": "Mount CPU",
      "line_stats": {
        "L1": {"avg_ms": 8500, "std_ms": 620, "samples": 45},
        "L2": {"avg_ms": 9100, "std_ms": 880, "samples": 52},
        "L3": {"avg_ms": 8200, "std_ms": 550, "samples": 38}
      },
      "best_line": "L3",
      "worst_line": "L2",
      "variance_percent": 11.0,
      "severity": "warning",
      "recommendation": "L2 is 11.0% slower than best line L3. Review work instructions and tooling."
    }
  ],
  "summary": {
    "total_tasks_compared": 25,
    "high_variance_tasks": 3,
    "warning_variance_tasks": 5,
    "normal_variance_tasks": 17,
    "avg_cross_line_variance_percent": 8.5,
    "best_overall_line": "L2",
    "worst_overall_line": "L3",
    "improvement_potential_percent": 12.3,
    "improvement_potential_ms": 45600
  }
}
```

**Field Descriptions**:
- `variance_percent`: Percentage difference between best and worst line for this task
- `severity`: `normal` (<5%), `warning` (5-15%), `critical` (>15%)
- `improvement_potential_percent`: Total efficiency gain if all lines match best practices
- `improvement_potential_ms`: Time savings per cycle in milliseconds

---

#### 6.2 `POST /benchmark/cross-line-tasks/generate`

Generate a new cross-line benchmark report.

**Request Body**:
```json
{
  "line_ids": ["L1", "L2", "L3"],
  "task_ids": ["T001", "T002", "T003"],
  "date_range": {
    "from": "2025-12-01",
    "to": "2025-12-31"
  },
  "include_worker_analysis": true,
  "include_time_of_day_analysis": false,
  "variance_threshold_warning": 10.0,
  "variance_threshold_critical": 15.0
}
```

**Parameters**:

| Field                          | Type    | Required | Description                              |
|--------------------------------|---------|----------|------------------------------------------|
| `line_ids`                     | array   | Yes      | Line IDs to compare (min 2, max 10)      |
| `task_ids`                     | array   | No       | Specific tasks to analyze (all if empty) |
| `date_range.from`              | string  | No       | Start date for data collection           |
| `date_range.to`                | string  | No       | End date for data collection             |
| `include_worker_analysis`      | boolean | No       | Include per-worker breakdown             |
| `include_time_of_day_analysis` | boolean | No       | Analyze shift performance patterns       |
| `variance_threshold_warning`   | float   | No       | Warning threshold % (default: 10.0)      |
| `variance_threshold_critical`  | float   | No       | Critical threshold % (default: 15.0)     |

**Response (202 Accepted)**:
```json
{
  "benchmark_id": "BM-20251202-002",
  "status": "generating",
  "estimated_completion_sec": 15,
  "poll_url": "/benchmark/cross-line-tasks/BM-20251202-002/status"
}
```

---

#### 6.3 `GET /benchmark/cross-line-tasks/{benchmark_id}`

Retrieve a specific benchmark report by ID.

**Path Parameters**:
- `benchmark_id` (string): Benchmark report ID

**Response (200 OK)**:
```json
{
  "benchmark_id": "BM-20251202-001",
  "status": "completed",
  "generated_at": "2025-12-02T10:30:00Z",
  "lines_compared": ["L1", "L2", "L3"],
  "task_benchmarks": [...],
  "summary": {...},
  "worker_analysis": {
    "L1": {
      "W001": {"avg_efficiency": 98.5, "tasks_completed": 125},
      "W002": {"avg_efficiency": 95.2, "tasks_completed": 118}
    },
    "L2": {
      "W005": {"avg_efficiency": 101.2, "tasks_completed": 142},
      "W006": {"avg_efficiency": 99.8, "tasks_completed": 138}
    }
  }
}
```

---

#### 6.4 `GET /benchmark/cross-line-tasks/{benchmark_id}/export`

Export benchmark report in various formats.

**Query Parameters**:
```
GET /benchmark/cross-line-tasks/BM-20251202-001/export?format=csv
```

| Parameter | Type   | Required | Description                         |
|-----------|--------|----------|-------------------------------------|
| `format`  | string | No       | Export format: `csv`, `xlsx`, `pdf` |

**Response (200 OK)**:
```http
Content-Type: text/csv
Content-Disposition: attachment; filename="benchmark_BM-20251202-001.csv"

task_id,task_name,L1_avg_ms,L2_avg_ms,L3_avg_ms,best_line,worst_line,variance_percent,severity
T001,Install RAM,12500,11800,13200,L2,L3,11.9,warning
T002,Mount CPU,8500,9100,8200,L3,L2,11.0,warning
...
```

---

#### 6.5 `DELETE /benchmark/cross-line-tasks/{benchmark_id}`

Delete a benchmark report.

**Path Parameters**:
- `benchmark_id` (string): Benchmark report ID

**Response (200 OK)**:
```json
{
  "benchmark_id": "BM-20251202-001",
  "status": "deleted",
  "message": "Benchmark report deleted successfully"
}
```

---

### 7. Site Configuration (NEW) ⚠️ REQ #6

Per-plant threshold configuration for line type recommendations.

#### 7.1 `GET /site-config/{site_id}`

Retrieve site-specific configuration.

**Path Parameters**:
- `site_id` (string): Site identifier (e.g., `TAO_FACTORY_A`, `MEX_FACTORY_B`)

**Response (200 OK)**:
```json
{
  "site_id": "TAO_FACTORY_A",
  "site_name": "Taoyuan Factory A",
  "line_type_thresholds": {
    "cell": {
      "max_tasks": 15,
      "max_stations": 2,
      "max_daily_demand": 50,
      "min_product_mix": 5,
      "space_limit_sqm": 100
    },
    "short_line": {
      "min_tasks": 15,
      "max_tasks": 60,
      "max_stations": 10,
      "max_daily_demand": 200,
      "min_product_mix": 2,
      "space_limit_sqm": 400
    },
    "long_line": {
      "min_tasks": 40,
      "min_stations": 8,
      "min_daily_demand": 150,
      "max_product_mix": 5,
      "space_limit_sqm": 1000
    }
  },
  "equipment_constraints": {
    "conveyor_available": true,
    "agv_available": false,
    "automated_stations": 2
  },
  "worker_constraints": {
    "max_workers_per_station": 4,
    "multi_skill_workers": 12,
    "single_skill_workers": 30
  },
  "created_at": "2025-01-15T10:00:00Z",
  "updated_at": "2025-12-12T08:00:00Z"
}
```

---

#### 7.2 `PUT /site-config/{site_id}`

Update site-specific configuration.

**Request Body**:
```json
{
  "line_type_thresholds": {
    "cell": {
      "max_tasks": 20,
      "max_stations": 3
    }
  },
  "worker_constraints": {
    "max_workers_per_station": 6
  }
}
```

**Response (200 OK)**:
```json
{
  "site_id": "TAO_FACTORY_A",
  "status": "updated",
  "updated_fields": ["line_type_thresholds.cell", "worker_constraints.max_workers_per_station"],
  "updated_at": "2025-12-12T10:30:00Z"
}
```

---

#### 7.3 `GET /site-config`

List all site configurations.

**Query Parameters**:
```
GET /site-config?region=APAC&limit=50
```

**Response (200 OK)**:
```json
{
  "sites": [
    {"site_id": "TAO_FACTORY_A", "site_name": "Taoyuan Factory A", "region": "APAC"},
    {"site_id": "MEX_FACTORY_B", "site_name": "Mexico Factory B", "region": "AMER"}
  ],
  "total_count": 2
}
```

---

#### 7.4 `POST /site-config` ⚠️ REQ #41 (Enhanced)

Create a new site configuration.

**Request Body**:
```json
{
  "site_id": "SG_FACTORY_C",
  "site_name": "Singapore Factory C",
  "region": "APAC",
  "timezone": "Asia/Singapore",
  "line_type_thresholds": {
    "cell": { "max_tasks": 15, "max_stations": 2, "max_daily_demand": 50 },
    "short_line": { "min_tasks": 15, "max_tasks": 60, "max_stations": 10 },
    "long_line": { "min_tasks": 40, "min_stations": 8, "min_daily_demand": 150 }
  },
  "equipment_constraints": {
    "conveyor_available": true,
    "agv_available": false
  },
  "worker_constraints": {
    "max_workers_per_station": 4,
    "multi_skill_workers": 10,
    "single_skill_workers": 25
  }
}
```

**Response (201 Created)**:
```json
{
  "site_id": "SG_FACTORY_C",
  "status": "created",
  "created_at": "2025-12-12T10:30:00Z"
}
```

**Validation Rules**:
- `site_id` must be unique and follow pattern `[A-Z]{2,4}_[A-Z]+_[A-Z]`
- Region must be one of: `APAC`, `AMER`, `EMEA`
- Threshold values must be positive integers

---

#### 7.5 `DELETE /site-config/{site_id}` ⚠️ REQ #41 (Enhanced)

Delete a site configuration (soft delete with audit trail).

**Path Parameters**:
- `site_id` (string): Site identifier to delete

**Response (200 OK)**:
```json
{
  "site_id": "SG_FACTORY_C",
  "status": "deleted",
  "deleted_at": "2025-12-12T15:00:00Z",
  "deleted_by": "admin@company.com",
  "audit_id": "audit_20251212_001"
}
```

**Response (409 Conflict)** - Site has active line configurations:
```json
{
  "error": "site_has_active_configurations",
  "message": "Cannot delete site with active line configurations",
  "active_lines": ["LINE_A", "LINE_B"],
  "suggestion": "Archive or migrate line configurations first"
}
```

---

#### 7.6 Site Configuration Admin Portal ⚠️ REQ #41 (Enhanced)

**Purpose**: Self-service maintenance portal for plant administrators to manage site-specific thresholds without developer intervention.

**Portal Features**:

| Feature | Description | User Role |
|---------|-------------|-----------|
| **View Sites** | List all site configurations with search/filter | All users |
| **Create Site** | Add new factory/site with default thresholds | Site Admin |
| **Edit Thresholds** | Modify line type thresholds per site | Site Admin |
| **Clone Site** | Copy existing site config as template | Site Admin |
| **Delete Site** | Soft delete with confirmation | Super Admin |
| **Audit Log** | View all changes to site configurations | Super Admin |

**UI Wireframe Specification**:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Site Configuration Management                           [+ Add Site]   │
├─────────────────────────────────────────────────────────────────────────┤
│  🔍 Search: [________________]  Region: [All ▼]  Status: [Active ▼]     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ TAO_FACTORY_A          Taoyuan Factory A          APAC           │   │
│  │ Last Updated: 2025-12-12    [Edit] [Clone] [Delete]              │   │
│  │ ─────────────────────────────────────────────────────────        │   │
│  │ Cell: max 15 tasks, 2 stations                                   │   │
│  │ Short Line: 15-60 tasks, 10 stations max                         │   │
│  │ Long Line: 40+ tasks, 8+ stations                                │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │ MEX_FACTORY_B          Mexico Factory B           AMER           │   │
│  │ Last Updated: 2025-12-10    [Edit] [Clone] [Delete]              │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  Page 1 of 5  [< Prev] [Next >]                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

**Edit Site Modal**:

```
┌─────────────────────────────────────────────────────────────────────────┐
│  Edit Site Configuration: TAO_FACTORY_A                         [X]    │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  Basic Information                                                       │
│  ─────────────────                                                       │
│  Site Name:    [Taoyuan Factory A_________]                             │
│  Region:       [APAC ▼]                                                  │
│  Timezone:     [Asia/Taipei ▼]                                           │
│                                                                          │
│  Line Type Thresholds                                                    │
│  ────────────────────                                                    │
│                                                                          │
│  ┌─ Cell Line ──────────────────────────────────────────────────────┐   │
│  │  Max Tasks: [15___]  Max Stations: [2___]  Max Demand: [50___]   │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌─ Short Line ─────────────────────────────────────────────────────┐   │
│  │  Min Tasks: [15___]  Max Tasks: [60___]  Max Stations: [10__]    │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│  ┌─ Long Line ──────────────────────────────────────────────────────┐   │
│  │  Min Tasks: [40___]  Min Stations: [8___]  Min Demand: [150_]    │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
│                                      [Cancel]  [Save Changes]            │
└─────────────────────────────────────────────────────────────────────────┘
```

**API Endpoints for Admin Portal**:

```
# Admin Portal APIs
GET  /admin/site-configs                    # List with pagination
POST /admin/site-configs                    # Create new site
PUT  /admin/site-configs/{site_id}          # Update site
DELETE /admin/site-configs/{site_id}        # Soft delete
POST /admin/site-configs/{site_id}/clone    # Clone configuration
GET  /admin/site-configs/{site_id}/audit    # Get audit history
GET  /admin/site-configs/export             # Export all configs (CSV/JSON)
POST /admin/site-configs/import             # Import configs (CSV/JSON)
```

---

### 8. Demand Input (NEW) ⚠️ REQ #51

Customer demand input and capacity planning.

#### 8.1 `POST /demand-input`

Submit customer demand for capacity analysis.

**Request Body**:
```json
{
  "site_id": "TAO_FACTORY_A",
  "product_family": "DL360_G11",
  "demands": [
    {
      "sku": "DL360-G11-001",
      "daily_demand": 150,
      "priority": "high",
      "due_date": "2026-01-15"
    },
    {
      "sku": "DL360-G11-002",
      "daily_demand": 80,
      "priority": "medium",
      "due_date": "2026-01-20"
    }
  ],
  "available_hours_per_day": 16,
  "available_shifts": 2,
  "available_workers": 45
}
```

**Response (200 OK)**:
```json
{
  "demand_id": "demand_20251212_001",
  "site_id": "TAO_FACTORY_A",
  "total_daily_demand": 230,
  "capacity_analysis": {
    "current_capacity_uph": 25,
    "required_capacity_uph": 28.75,
    "capacity_gap": -3.75,
    "gap_percent": -15.0,
    "feasible": false,
    "recommended_action": "Add 1 line or increase workers per station"
  },
  "line_recommendations": [
    {
      "option": "Add Line C",
      "additional_workers": 6,
      "new_capacity_uph": 37.5,
      "utilization": 0.77
    },
    {
      "option": "Add overtime",
      "additional_hours": 4,
      "new_capacity_uph": 31.25,
      "utilization": 0.92
    }
  ],
  "created_at": "2025-12-12T10:00:00Z"
}
```

---

#### 8.2 `GET /capacity-analysis/{site_id}`

Get current capacity analysis for a site.

**Query Parameters**:
```
GET /capacity-analysis/TAO_FACTORY_A?product_family=DL360_G11
```

**Response (200 OK)**:
```json
{
  "site_id": "TAO_FACTORY_A",
  "product_family": "DL360_G11",
  "current_lines": 2,
  "current_capacity_uph": 25,
  "current_utilization": 0.85,
  "available_capacity_uph": 4.5,
  "bottleneck_line": "Line_A",
  "bottleneck_station": "WS-003"
}
```

---

### 9. Sequence Adjustment (NEW) ⚠️ REQ #49

Manual assembly order adjustment with validation.

#### 9.1 `POST /adjust-sequence`

Manually adjust assembly sequence.

**Request Body**:
```json
{
  "work_order_id": "WO_A",
  "adjustments": [
    {
      "task_id": 5,
      "action": "move_after",
      "target_task_id": 3,
      "reason": "Ergonomic consideration - heavy part first"
    },
    {
      "task_id": 8,
      "action": "assign_to_station",
      "target_station": 2,
      "reason": "Equipment availability"
    }
  ],
  "validate_precedence": true,
  "simulate_only": false
}
```

**Parameters**:

| Field                | Type    | Required | Description                                    |
|----------------------|---------|----------|------------------------------------------------|
| `work_order_id`      | string  | Yes      | Work order ID                                  |
| `adjustments`        | array   | Yes      | Array of adjustment operations                 |
| `adjustments[].task_id` | int  | Yes      | Task to adjust                                 |
| `adjustments[].action` | string | Yes     | `move_after`, `move_before`, `assign_to_station` |
| `adjustments[].target_task_id` | int | No | Target task for move operations               |
| `adjustments[].target_station` | int | No | Target station for assignment                 |
| `adjustments[].reason` | string | No      | Reason for adjustment (for audit trail)        |
| `validate_precedence` | boolean | No      | Validate precedence constraints (default: true)|
| `simulate_only`      | boolean | No       | Only simulate, don't apply (default: false)    |

**Response (200 OK)**:
```json
{
  "adjustment_id": "adj_001",
  "work_order_id": "WO_A",
  "adjustments_applied": 2,
  "precedence_violations": [],
  "new_sequence": [1, 2, 3, 5, 4, 6, 7, 8, 9],
  "impact_analysis": {
    "takt_change_ms": 750,
    "takt_change_pct": 2.5,
    "utilization_change_pct": -1.2,
    "stations_affected": [2, 3]
  },
  "warnings": [
    "Task 5 move increases station 2 load by 15%"
  ],
  "applied_at": "2025-12-12T10:30:00Z"
}
```

**Error Response (400 Bad Request)**:
```json
{
  "detail": "Precedence violation detected",
  "violations": [
    {
      "task_id": 5,
      "required_predecessor": 4,
      "message": "Task 5 cannot be placed before task 4 (precedence constraint)"
    }
  ]
}
```

---

#### 9.2 `GET /adjustment-history/{work_order_id}`

Get adjustment history for a work order.

**Response (200 OK)**:
```json
{
  "work_order_id": "WO_A",
  "adjustments": [
    {
      "adjustment_id": "adj_001",
      "user": "john.doe@company.com",
      "timestamp": "2025-12-12T10:30:00Z",
      "changes": [
        {"task_id": 5, "action": "move_after", "target": 3}
      ],
      "reason": "Ergonomic consideration"
    }
  ],
  "total_adjustments": 1
}
```

---

#### 9.3 `POST /adjustment-rollback/{adjustment_id}`

Rollback a sequence adjustment.

**Response (200 OK)**:
```json
{
  "adjustment_id": "adj_001",
  "status": "rolled_back",
  "restored_sequence": [1, 2, 3, 4, 5, 6, 7, 8, 9]
}
```

---

### 10. NPI/MP Stage (NEW) ⚠️ REQ #50

Production stage differentiation for New Product Introduction (NPI) vs Mass Production (MP).

#### Extended `POST /optimize` Parameters

Add `stage` and `stage_config` to optimization request:

| Field                       | Type    | Required | Description                                | Phase |
|-----------------------------|---------|----------|--------------------------------------------|-------|
| `stage`                     | string  | No       | Production stage: `npi`, `mp`              | 2     |
| `stage_config`              | object  | No       | Stage-specific configuration               | 2     |
| `stage_config.learning_curve_factor` | float | No | Time multiplier for NPI (1.0-2.0)       | 2     |
| `stage_config.target_efficiency` | float | No   | Target efficiency (0.5-1.0)                | 2     |
| `stage_config.allow_overtime` | boolean | No    | Allow overtime for capacity                | 2     |
| `stage_config.flexibility_weight` | float | No  | Weight for flexibility in optimization     | 2     |

**Request Body Example**:
```json
{
  "work_order_id": "WO_DL360_G12",
  "optimization_goal": "min_stations",
  "stage": "npi",
  "stage_config": {
    "learning_curve_factor": 1.25,
    "target_efficiency": 0.70,
    "allow_overtime": true,
    "flexibility_weight": 0.8,
    "max_rework_rate": 0.05,
    "line_type_preference": "cell"
  }
}
```

**Response includes stage-specific fields**:
```json
{
  "work_order_id": "WO_DL360_G12",
  "stage": "npi",
  "stage_adjustments": {
    "learning_curve_applied": true,
    "time_factor": 1.25,
    "adjusted_takt_ms": 37500,
    "original_takt_ms": 30000
  },
  "npi_recommendations": [
    "Use cell line for flexibility during debugging",
    "Plan for 25% longer cycle times in first 100 units",
    "Consider additional QC station for defect tracking"
  ],
  "stations": [ ... ],
  "kpis": { ... }
}
```

---

## Data Models

### MultiLineConfig

```python
class LineConfig(BaseModel):
    """Individual line configuration"""
    line_id: str = Field(pattern=r'^[A-Z]$')  # A, B, C, etc.
    target_takt: int = Field(gt=0)
    max_workers_per_station: int = Field(ge=1, le=10, default=3)
    task_filter: Optional[List[int]] = None

class MultiLineConfig(BaseModel):
    """Multi-line optimization configuration"""
    enabled: bool = False
    lines: List[LineConfig]
    enable_cross_line_balancing: bool = True
    
    @validator('lines')
    def validate_lines(cls, v):
        if len(v) < 2:
            raise ValueError("Multi-line requires at least 2 lines")
        if len(v) > 5:
            raise ValueError("Maximum 5 lines supported")
        
        # Check unique line_ids
        line_ids = [line.line_id for line in v]
        if len(line_ids) != len(set(line_ids)):
            raise ValueError("Duplicate line_id detected")
        
        return v
```

### LayoutData

```python
class StationPosition(BaseModel):
    """Station position in 2D layout"""
    id: str
    x: int = Field(ge=0)
    y: int = Field(ge=0)
    width: int = Field(ge=20, le=200, default=80)
    height: int = Field(ge=20, le=200, default=60)
    type: str = Field(default="assembly")  # assembly, quality_check, packaging

class Connection(BaseModel):
    """Connection between stations"""
    from_station: str = Field(alias="from")
    to_station: str = Field(alias="to")
    type: str = Field(default="conveyor")  # conveyor, manual_transfer, robotic

class LayoutData(BaseModel):
    """Complete layout data"""
    id: Optional[int] = None
    name: str = Field(max_length=255)
    description: Optional[str] = Field(max_length=1000)
    site: str = Field(max_length=100)
    data: Dict[str, Any]  # Contains stations, connections, dimensions
    
    @validator('data')
    def validate_data(cls, v):
        required_keys = ['stations', 'connections', 'dimensions']
        for key in required_keys:
            if key not in v:
                raise ValueError(f"Missing required key: {key}")
        return v
```

### ProductConfig

```python
class ComponentOption(BaseModel):
    """CTO/BTO component option"""
    part_id: str
    assembly_time_ms: int = Field(gt=0)
    complexity: str = Field(pattern=r'^(simple|medium|complex|super_complex)$')

class ProductConfig(BaseModel):
    """Product configuration (CTO/BTO)"""
    sku: str = Field(max_length=100)
    product_name: str = Field(max_length=255)
    default_complexity: str = Field(pattern=r'^(simple|medium|complex|super_complex)$')
    cto_bto_map: Dict[str, Dict[str, ComponentOption]]
    
    @validator('cto_bto_map')
    def validate_cto_bto_map(cls, v):
        if not v:
            raise ValueError("CTO/BTO map cannot be empty")
        return v
```

### CrossLineBenchmark

```python
class TaskLineStats(BaseModel):
    """Statistics for a task on a specific line"""
    avg_ms: float = Field(ge=0)
    std_ms: float = Field(ge=0)
    min_ms: float = Field(ge=0)
    max_ms: float = Field(ge=0)
    samples: int = Field(ge=1)

class TaskBenchmark(BaseModel):
    """Benchmark data for a single task across lines"""
    task_id: str
    task_name: str
    line_stats: Dict[str, TaskLineStats]
    best_line: str
    worst_line: str
    variance_percent: float = Field(ge=0)
    severity: str = Field(pattern=r'^(normal|warning|critical)$')
    recommendation: Optional[str] = None

class BenchmarkSummary(BaseModel):
    """Summary statistics for benchmark report"""
    total_tasks_compared: int = Field(ge=0)
    high_variance_tasks: int = Field(ge=0)
    warning_variance_tasks: int = Field(ge=0)
    normal_variance_tasks: int = Field(ge=0)
    avg_cross_line_variance_percent: float = Field(ge=0)
    best_overall_line: str
    worst_overall_line: str
    improvement_potential_percent: float = Field(ge=0)
    improvement_potential_ms: int = Field(ge=0)

class CrossLineBenchmarkReport(BaseModel):
    """Complete cross-line benchmark report"""
    benchmark_id: str
    generated_at: datetime
    status: str = Field(pattern=r'^(generating|completed|failed)$')
    lines_compared: List[str]
    task_benchmarks: List[TaskBenchmark]
    summary: BenchmarkSummary
    worker_analysis: Optional[Dict[str, Dict[str, Any]]] = None

class BenchmarkRequest(BaseModel):
    """Request to generate new benchmark"""
    line_ids: List[str] = Field(min_items=2, max_items=10)
    task_ids: Optional[List[str]] = None
    date_range: Optional[Dict[str, str]] = None
    include_worker_analysis: bool = False
    include_time_of_day_analysis: bool = False
    variance_threshold_warning: float = Field(default=10.0, ge=1.0, le=50.0)
    variance_threshold_critical: float = Field(default=15.0, ge=5.0, le=100.0)
    
    @validator('variance_threshold_critical')
    def validate_thresholds(cls, v, values):
        if 'variance_threshold_warning' in values and v <= values['variance_threshold_warning']:
            raise ValueError("Critical threshold must be greater than warning threshold")
        return v
```

---

## Error Handling

### Phase 2 Specific Errors

#### Multi-Line Errors

**400 Bad Request**:
```json
{
  "detail": "Multi-line error: Line IDs must be unique (duplicate: A)"
}
```

```json
{
  "detail": "Multi-line error: Task 5 assigned to multiple lines"
}
```

#### Layout Errors

**400 Bad Request**:
```json
{
  "detail": "Layout validation error: Station overlap detected (WS-001, WS-002)"
}
```

**404 Not Found**:
```json
{
  "detail": "Layout not found: id=99"
}
```

#### Product Config Errors

**400 Bad Request**:
```json
{
  "detail": "Product config error: Invalid complexity level 'ultra_complex'"
}
```

**409 Conflict**:
```json
{
  "detail": "Product config conflict: SKU 'DL360_G10' already exists"
}
```

#### Cross-Line Benchmark Errors

**400 Bad Request**:
```json
{
  "detail": "Benchmark error: At least 2 line IDs required for comparison"
}
```

```json
{
  "detail": "Benchmark error: No task data found for lines [L1, L2] in specified date range"
}
```

**404 Not Found**:
```json
{
  "detail": "Benchmark report not found: BM-20251202-999"
}
```

**422 Unprocessable Entity**:
```json
{
  "detail": "Benchmark error: Critical threshold (10%) must be greater than warning threshold (15%)"
}
```

---

## Usage Examples

### Example 1: Multi-Line Optimization

**Request**:
```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "work_order_id": "WO_MULTI",
    "optimization_goal": "min_stations",
    "multi_line_config": {
      "enabled": true,
      "lines": [
        {
          "line_id": "A",
          "target_takt": 30000,
          "max_workers_per_station": 3
        },
        {
          "line_id": "B",
          "target_takt": 25000,
          "max_workers_per_station": 2
        }
      ],
      "enable_cross_line_balancing": true
    }
  }'
```

**Response**:
```json
{
  "multi_line_results": {
    "total_lines_used": 2,
    "total_stations": 4,
    "total_manpower": 4,
    "cross_line_balance_score": 0.92,
    "lines": [
      {
        "line_id": "A",
        "station_count": 2,
        "utilization_avg": 93.85
      },
      {
        "line_id": "B",
        "station_count": 2,
        "utilization_avg": 95.4
      }
    ]
  }
}
```

---

### Example 2: Get Line Type Recommendation

**Request**:
```bash
curl "http://localhost:8000/recommend-line-type?work_order_id=WO_A&target_takt=30000"
```

**Response**:
```json
{
  "recommended_type": "short_line",
  "confidence": 0.85,
  "reasoning": {
    "task_count": 35,
    "min_theoretical_stations": 5.2,
    "recommended_stations": 6
  }
}
```

---

### Example 3: Generate Fishbone Diagram

**Request**:
```bash
curl "http://localhost:8000/fishbone-diagram?work_order_id=WO_A&format=svg&highlight_critical_path=true" \
  -o fishbone_WO_A.svg
```

---

### Example 4: Save Layout

**Request**:
```bash
curl -X POST http://localhost:8000/save-layout \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Factory A - Line 1",
    "site": "factory_A",
    "data": {
      "stations": [
        {"id": "WS-001", "x": 100, "y": 200, "width": 80, "height": 60}
      ],
      "connections": [],
      "dimensions": {"width": 1000, "height": 600}
    }
  }'
```

**Response**:
```json
{
  "layout_id": 1,
  "status": "saved",
  "message": "Layout saved successfully"
}
```

---

### Example 5: Query Product Config

**Request**:
```bash
curl "http://localhost:8000/product-config?sku=DL360_G10"
```

**Response**:
```json
{
  "sku": "DL360_G10",
  "product_name": "HP ProLiant DL360 Gen10",
  "cto_bto_map": {
    "cpu": {
      "intel_xeon_silver": {
        "part_id": "CPU_XEON_SILVER_4214",
        "assembly_time_ms": 8000
      }
    }
  }
}
```

---

### Example 6: Generate Cross-Line Task Benchmark

**Request**:
```bash
curl -X POST http://localhost:8000/benchmark/cross-line-tasks/generate \
  -H "Content-Type: application/json" \
  -d '{
    "line_ids": ["L1", "L2", "L3"],
    "date_range": {
      "from": "2025-12-01",
      "to": "2025-12-31"
    },
    "include_worker_analysis": true,
    "variance_threshold_warning": 10.0,
    "variance_threshold_critical": 15.0
  }'
```

**Response**:
```json
{
  "benchmark_id": "BM-20251202-001",
  "status": "generating",
  "estimated_completion_sec": 15,
  "poll_url": "/benchmark/cross-line-tasks/BM-20251202-001/status"
}
```

---

### Example 7: Query Cross-Line Benchmark Report

**Request**:
```bash
curl "http://localhost:8000/benchmark/cross-line-tasks?line_ids=L1,L2,L3&date_from=2025-12-01"
```

**Response**:
```json
{
  "benchmark_id": "BM-20251202-001",
  "lines_compared": ["L1", "L2", "L3"],
  "task_benchmarks": [
    {
      "task_id": "T001",
      "task_name": "Install RAM",
      "best_line": "L2",
      "worst_line": "L3",
      "variance_percent": 11.9,
      "severity": "warning"
    }
  ],
  "summary": {
    "total_tasks_compared": 25,
    "high_variance_tasks": 3,
    "avg_cross_line_variance_percent": 8.5,
    "best_overall_line": "L2",
    "improvement_potential_percent": 12.3
  }
}
```

---

### Example 8: Export Benchmark to CSV

**Request**:
```bash
curl "http://localhost:8000/benchmark/cross-line-tasks/BM-20251202-001/export?format=csv" \
  -o benchmark_report.csv
```

---

## Performance Requirements

### Phase 2 Targets

| Metric                       | Target      | Notes                       |
|------------------------------|-------------|-----------------------------||
| **Multi-Line Optimization**  | < 5 seconds | 2-3 lines, ≤500 tasks total |
| **Fishbone Generation**      | < 2 seconds | ≤100 tasks                  |
| **Layout Save/Load**         | < 500ms     | Single layout operation     |
| **Product Config Query**     | < 200ms     | Single SKU lookup           |
| **Line Recommendation**      | < 1 second  | Analysis + recommendation   |
| **Benchmark Generation**     | < 30 seconds| 3 lines, 50 tasks, 30 days  |
| **Benchmark Query**          | < 500ms     | Cached report retrieval     |
| **Benchmark Export (CSV)**   | < 2 seconds | Full report export          |

---

**Document Maintainer:** JASON YY, LIN  
**Last Updated:** 2025-11-12 
**Version:** 2.0.0-phase2
