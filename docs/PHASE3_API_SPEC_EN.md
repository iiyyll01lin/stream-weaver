# Phase 3 API Specification

**Document Version**: 1.0 | **Last Updated**: 2025-11-12  
**Related Documents**:
- [Phase 3 Architecture](PHASE3_ARCHITECTURE_EN.md)
- [Phase 3 Implementation Guide](PHASE3_IMPLEMENTATION_EN.md)
- [Phase 2 API Specification](PHASE2_API_SPEC_EN.md)

---

## Table of Contents

- [Overview](#overview)
- [New API Endpoints](#new-api-endpoints)
  - [Natural Language Query](#1-natural-language-query)
  - [3D Model Management](#2-3d-model-management)
  - [Body Sensor Data](#3-body-sensor-data)
  - [Version Management](#4-version-management)
  - [Collision Detection](#5-collision-detection)
  - [Omniverse Integration](#6-omniverse-integration)
  - [Multi-Site Sharing](#7-multi-site-sharing)
- [Data Models](#data-models)
- [WebSocket Events](#websocket-events)
- [Error Handling](#error-handling)
- [Usage Examples](#usage-examples)

---

## Overview

Phase 3 API extends Phase 2 with advanced AI/ML and 3D capabilities:

1. **Natural Language Query**: Ask questions in plain English
2. **3D Model Management**: Browse and manage USD asset library
3. **Body Sensor Data**: Upload and analyze motion capture data
4. **Version Management**: Git-like configuration versioning
5. **Collision Detection**: Automated interference checking
6. **Omniverse Integration**: Real-time 3D simulation
7. **Multi-Site Sharing**: Cross-factory collaboration

### API Version

```
Version: 3.0.0-phase3
Base URL: http://localhost:8000
WebSocket: ws://localhost:8000/ws
```

---

## New API Endpoints

### 1. Natural Language Query

#### `POST /nlp-query`

Process natural language queries and execute corresponding API calls.

**Request Body**:
```json
{
  "query": "Which station has the highest load in WO_A?",
  "context": {
    "current_work_order": "WO_A",
    "current_view": "dashboard"
  },
  "options": {
    "return_visualization": true,
    "max_results": 10
  }
}
```

**Parameters**:

| Field                          | Type    | Required | Description                               |
|--------------------------------|---------|----------|-------------------------------------------|
| `query`                        | string  | Yes      | Natural language question or command      |
| `context`                      | object  | No       | Current application context               |
| `options.return_visualization` | boolean | No       | Include chart/graph data (default: false) |
| `options.max_results`          | integer | No       | Limit results (default: 10)               |

**Response (200 OK)**:
```json
{
  "query": "Which station has the highest load in WO_A?",
  "intent": "query_station_load",
  "confidence": 0.95,
  "entities": {
    "work_order": "WO_A",
    "metric": "load",
    "aggregation": "max"
  },
  "api_calls": [
    {
      "endpoint": "/workstations",
      "params": {"work_order_id": "WO_A", "target_takt": 30000},
      "result": { /* API response */ }
    }
  ],
  "answer": "Station 3 has the highest load of 28,500ms in WO_A, which is 95% of the target takt time of 30,000ms.",
  "visualization": {
    "type": "bar_chart",
    "data": [/* chart data */],
    "title": "Station Load Distribution - WO_A"
  },
  "suggestions": [
    "Show me the task breakdown for station 3",
    "How can I reduce the load on station 3?"
  ],
  "processing_time_ms": 1250
}
```

**Supported Query Types**:

| Category             | Example Queries                                                                       |
|----------------------|---------------------------------------------------------------------------------------|
| **Optimization**     | "Optimize WO_A with 40s takt time"<br>"What's the minimum number of stations needed?" |
| **Analysis**         | "Which station is the bottleneck?"<br>"What's the average utilization?"               |
| **Layout**           | "Show me the factory A layout"<br>"Load the latest saved layout"                      |
| **3D Visualization** | "Show 3D model of station 5"<br>"Simulate the production line in 3D"                  |
| **Sensor Data**      | "What's the REBA score for worker 1?"<br>"Analyze motion data from last week"         |
| **Comparison**       | "Compare WO_A and WO_B efficiency"<br>"What changed between version 1 and 2?"         |
| **Recommendations**  | "How can I improve line balance?"<br>"Suggest layout modifications"                   |

**Error Response (400 Bad Request)**:
```json
{
  "detail": "Unable to understand query. Please rephrase.",
  "intent": "unknown",
  "confidence": 0.23,
  "suggestions": [
    "Try: 'Which station has the highest load?'",
    "Try: 'Show me the optimization result for WO_A'"
  ]
}
```

---

### 2. 3D Model Management

#### 2.1 `GET /3d-models`

List available 3D models in the asset library.

**Query Parameters**:
```
GET /3d-models?category=workstation&limit=50
```

| Parameter  | Type    | Required | Description                                                       |
|------------|---------|----------|-------------------------------------------------------------------|
| `category` | string  | No       | Filter by category (`workstation`, `product`, `tool`, `conveyor`) |
| `search`   | string  | No       | Search model name                                                 |
| `limit`    | integer | No       | Max results (default: 50)                                         |

**Response (200 OK)**:
```json
{
  "models": [
    {
      "id": 1,
      "model_name": "Workstation_Standard_v2",
      "usd_path": "omniverse://nucleus/models/workstations/standard_v2.usd",
      "category": "workstation",
      "dimensions": {
        "width": 2.0,
        "depth": 1.5,
        "height": 2.2
      },
      "thumbnail_url": "https://cdn.example.com/thumbs/ws_standard_v2.png",
      "metadata": {
        "polygons": 12500,
        "materials": 8,
        "animations": ["idle", "assembly"]
      },
      "created_at": "2025-10-01T00:00:00Z"
    },
    {
      "id": 2,
      "model_name": "DL360_G10_Assembly",
      "usd_path": "omniverse://nucleus/models/products/dl360_g10.usd",
      "category": "product",
      "dimensions": {
        "width": 0.45,
        "depth": 0.7,
        "height": 0.088
      },
      "thumbnail_url": "https://cdn.example.com/thumbs/dl360.png",
      "created_at": "2025-09-15T00:00:00Z"
    }
  ],
  "total_count": 2,
  "categories": {
    "workstation": 15,
    "product": 28,
    "tool": 42,
    "conveyor": 8
  }
}
```

---

#### 2.2 `GET /3d-models/{model_id}`

Retrieve specific 3D model details.

**Path Parameters**:
- `model_id` (integer): Model ID

**Response (200 OK)**:
```json
{
  "id": 1,
  "model_name": "Workstation_Standard_v2",
  "usd_path": "omniverse://nucleus/models/workstations/standard_v2.usd",
  "category": "workstation",
  "dimensions": {
    "width": 2.0,
    "depth": 1.5,
    "height": 2.2
  },
  "thumbnail_url": "https://cdn.example.com/thumbs/ws_standard_v2.png",
  "metadata": {
    "polygons": 12500,
    "materials": 8,
    "animations": ["idle", "assembly"],
    "physics_enabled": true,
    "collision_mesh": "simplified"
  },
  "created_at": "2025-10-01T00:00:00Z",
  "updated_at": "2025-10-15T10:30:00Z",
  "download_url": "https://cdn.example.com/models/ws_standard_v2.usd",
  "preview_url": "https://cdn.example.com/previews/ws_standard_v2.html"
}
```

---

#### 2.3 `POST /3d-models`

Upload new 3D model to library.

**Request Body** (multipart/form-data):
```
model_file: (binary USD file)
model_name: "Custom_Workstation_A"
category: "workstation"
dimensions: {"width": 2.5, "depth": 1.8, "height": 2.0}
thumbnail: (binary PNG/JPG file)
```

**Response (200 OK)**:
```json
{
  "model_id": 45,
  "model_name": "Custom_Workstation_A",
  "usd_path": "omniverse://nucleus/models/workstations/custom_workstation_a.usd",
  "status": "uploaded",
  "message": "3D model uploaded successfully"
}
```

---

### 3. Body Sensor Data

#### 3.1 `POST /upload-sensor-data`

Upload motion capture video or sensor data for analysis.

**Request Body** (multipart/form-data):
```
video_file: (binary MP4/AVI file)
worker_id: "worker_001"
session_id: "session_20251112_001"
metadata: {"task": "DL360_assembly", "duration_sec": 120}
```

**Response (200 OK)**:
```json
{
  "upload_id": "upload_abc123",
  "worker_id": "worker_001",
  "session_id": "session_20251112_001",
  "status": "processing",
  "estimated_completion_sec": 45,
  "message": "Video uploaded successfully. Processing motion data..."
}
```

---

#### 3.2 `GET /sensor-data/{upload_id}`

Retrieve processed sensor data analysis.

**Path Parameters**:
- `upload_id` (string): Upload ID from POST request

**Response (200 OK)**:
```json
{
  "upload_id": "upload_abc123",
  "worker_id": "worker_001",
  "session_id": "session_20251112_001",
  "status": "completed",
  "processing_time_sec": 42,
  "motion_analysis": {
    "total_frames": 3600,
    "fps": 30,
    "duration_sec": 120,
    "tasks_detected": [
      {
        "task_id": "auto_1",
        "action_type": "install",
        "start_time_sec": 0.5,
        "end_time_sec": 8.2,
        "duration_ms": 7700,
        "avg_reba_score": 4,
        "risk_level": "medium"
      },
      {
        "task_id": "auto_2",
        "action_type": "screw",
        "start_time_sec": 8.5,
        "end_time_sec": 15.3,
        "duration_ms": 6800,
        "avg_reba_score": 2,
        "risk_level": "low"
      }
    ],
    "ergonomic_summary": {
      "avg_reba_score": 3.2,
      "max_reba_score": 7,
      "high_risk_moments": 2,
      "recommendations": [
        "Reduce trunk bending at 45s mark",
        "Improve workpiece positioning to avoid overhead reach"
      ]
    },
    "fatigue_analysis": {
      "fatigue_index": 0.35,
      "estimated_fatigue_time_min": 45,
      "rest_recommendation": "5-minute break recommended after 40 minutes"
    }
  },
  "time_study_export": {
    "csv_url": "/downloads/time_study_upload_abc123.csv",
    "format": "csv",
    "tasks_count": 15,
    "total_productive_time_ms": 98500
  },
  "video_url": "/videos/upload_abc123.mp4",
  "annotated_video_url": "/videos/upload_abc123_annotated.mp4"
}
```

**Ergonomic Risk Levels**:
- **Low** (REBA 1-3): Acceptable posture
- **Medium** (REBA 4-7): Investigate and change soon
- **High** (REBA 8-10): Investigate and change immediately
- **Very High** (REBA 11-15): Unacceptable, change now

---

#### 3.3 `GET /sensor-data/worker/{worker_id}`

Retrieve historical sensor data for a specific worker.

**Query Parameters**:
```
GET /sensor-data/worker/worker_001?from=2025-11-01&to=2025-11-12&limit=50
```

| Parameter | Type    | Required | Description                |
|-----------|---------|----------|----------------------------|
| `from`    | date    | No       | Start date (YYYY-MM-DD)    |
| `to`      | date    | No       | End date (YYYY-MM-DD)      |
| `limit`   | integer | No       | Max sessions (default: 50) |

**Response (200 OK)**:
```json
{
  "worker_id": "worker_001",
  "sessions": [
    {
      "session_id": "session_20251112_001",
      "upload_id": "upload_abc123",
      "timestamp": "2025-11-12T09:15:00Z",
      "duration_sec": 120,
      "avg_reba_score": 3.2,
      "tasks_count": 15
    }
  ],
  "total_sessions": 1,
  "statistics": {
    "total_work_hours": 24.5,
    "avg_reba_score": 3.5,
    "injury_risk_trend": "stable",
    "efficiency_trend": "improving"
  }
}
```

---

#### 3.4 `POST /motion/compare-efficiency` (NEW)

Compare worker motion efficiency against expert baseline.

**Request Body**:
```json
{
  "novice_upload_id": "upload_abc123",
  "expert_baseline_id": "expert_001_baseline",
  "task_type": "DL360_assembly",
  "generate_report": true
}
```

**Response (200 OK)**:
```json
{
  "comparison_id": "comp_xyz789",
  "novice_worker_id": "worker_005",
  "expert_baseline_id": "expert_001_baseline",
  "task_type": "DL360_assembly",
  "timestamp": "2025-11-12T10:30:00Z",
  "efficiency_score": 62,
  "expert_cycle_time_sec": 45.2,
  "novice_cycle_time_sec": 63.5,
  "time_difference_sec": 18.3,
  "productivity_gap_percent": 40.5,
  "gaps": [
    {
      "metric": "hand_coordination_ratio",
      "expert": 0.78,
      "novice": 0.23,
      "gap": 0.55,
      "time_loss_sec": 8.5,
      "priority": "high",
      "recommendation": "Practice using both hands simultaneously during assembly tasks"
    },
    {
      "metric": "motion_smoothness",
      "expert": 0.85,
      "novice": 0.52,
      "gap": 0.33,
      "time_loss_sec": 5.2,
      "priority": "high",
      "recommendation": "Focus on smooth, controlled movements. Avoid jerky motions"
    },
    {
      "metric": "path_efficiency",
      "expert": 0.72,
      "novice": 0.48,
      "gap": 0.24,
      "time_loss_sec": 4.6,
      "priority": "medium",
      "recommendation": "Take more direct paths to parts. Minimize detours"
    }
  ],
  "training_priority": [
    "hand_coordination_ratio",
    "motion_smoothness", 
    "path_efficiency"
  ],
  "efficiency_features": {
    "expert": {
      "hand_coordination_ratio": 0.78,
      "motion_smoothness": 0.85,
      "path_efficiency": 0.72,
      "unnecessary_reaches": 1,
      "trunk_angle_stability": 0.91,
      "arm_extension_ratio": 0.65,
      "avg_reba_score": 2.8
    },
    "novice": {
      "hand_coordination_ratio": 0.23,
      "motion_smoothness": 0.52,
      "path_efficiency": 0.48,
      "unnecessary_reaches": 7,
      "trunk_angle_stability": 0.67,
      "arm_extension_ratio": 0.82,
      "avg_reba_score": 4.5
    }
  },
  "report_url": "/reports/efficiency_comp_xyz789.pdf",
  "radar_chart_url": "data:image/png;base64,iVBORw0KGgo...",
  "timeline_chart_url": "data:image/png;base64,iVBORw0KGgo..."
}
```

**Error Responses**:
- `404 Not Found`: Upload ID or baseline not found
- `400 Bad Request`: Task type mismatch between uploads
- `500 Internal Server Error`: Processing error

---

#### 3.5 `GET /motion/expert-baselines`

List available expert baselines for comparison.

**Query Parameters**:
```
GET /motion/expert-baselines?task_type=DL360_assembly&min_score=75
```

| Parameter    | Type    | Required | Description                     |
|--------------|---------|----------|---------------------------------|
| `task_type`  | string  | No       | Filter by task type             |
| `min_score`  | integer | No       | Minimum efficiency score (0-100)|

**Response (200 OK)**:
```json
{
  "baselines": [
    {
      "baseline_id": "expert_001_baseline",
      "expert_worker_id": "worker_099",
      "task_type": "DL360_assembly",
      "efficiency_score": 95,
      "cycle_time_sec": 45.2,
      "recording_date": "2025-10-15",
      "samples_count": 50,
      "features": {
        "hand_coordination_ratio": 0.78,
        "motion_smoothness": 0.85,
        "path_efficiency": 0.72,
        "avg_reba_score": 2.8
      }
    }
  ],
  "total_count": 1
}
```

---

#### 3.6 `POST /motion/create-expert-baseline`

Create new expert baseline from high-performing worker.

**Request Body**:
```json
{
  "worker_id": "worker_099",
  "upload_ids": [
    "upload_xyz001",
    "upload_xyz002",
    "upload_xyz003"
  ],
  "task_type": "DL360_assembly",
  "baseline_name": "Expert DL360 Assembly - Jason Lin"
}
```

**Response (201 Created)**:
```json
{
  "baseline_id": "expert_001_baseline",
  "worker_id": "worker_099",
  "task_type": "DL360_assembly",
  "baseline_name": "Expert DL360 Assembly - Jason Lin",
  "samples_analyzed": 3,
  "avg_efficiency_score": 95,
  "avg_cycle_time_sec": 45.2,
  "created_at": "2025-11-12T11:00:00Z",
  "features": {
    "hand_coordination_ratio": 0.78,
    "motion_smoothness": 0.85,
    "path_efficiency": 0.72,
    "unnecessary_reaches": 1,
    "trunk_angle_stability": 0.91,
    "arm_extension_ratio": 0.65,
    "avg_reba_score": 2.8
  }
}
```

---

#### 3.7 `GET /motion/efficiency-report/{comparison_id}`

Retrieve detailed efficiency comparison report.

**Path Parameters**:
- `comparison_id` (string): Comparison ID from POST /motion/compare-efficiency

**Response (200 OK)**:
```json
{
  "comparison_id": "comp_xyz789",
  "generated_at": "2025-11-12T10:35:00Z",
  "report_type": "efficiency_comparison",
  "summary": {
    "novice_worker": "worker_005",
    "expert_baseline": "expert_001_baseline",
    "efficiency_score": 62,
    "productivity_gap_percent": 40.5,
    "estimated_improvement_potential": "15% efficiency gain possible with targeted training"
  },
  "detailed_analysis": {
    "top_3_improvements": [
      {
        "area": "Hand Coordination",
        "current_score": 0.23,
        "target_score": 0.78,
        "time_saving_potential_sec": 8.5,
        "training_exercises": [
          "Practice parallel hand movements with dummy parts",
          "Watch expert video focusing on simultaneous actions",
          "Start with simple 2-hand tasks, progress to complex"
        ]
      }
    ],
    "strength_areas": [
      {
        "area": "Trunk Stability",
        "score": 0.67,
        "note": "Good posture maintenance, minimal rework needed"
      }
    ]
  },
  "visualizations": {
    "radar_chart": "data:image/png;base64,...",
    "timeline_comparison": "data:image/png;base64,...",
    "improvement_roadmap": "data:image/png;base64,..."
  },
  "export_formats": {
    "pdf_url": "/reports/efficiency_comp_xyz789.pdf",
    "csv_url": "/reports/efficiency_comp_xyz789.csv",
    "json_url": "/reports/efficiency_comp_xyz789.json"
  }
}
```

---

### 4. Version Management

#### 4.1 `GET /versions`

List configuration versions.

**Query Parameters**:
```
GET /versions?config_type=layout&site=factory_A&limit=20
```

| Parameter     | Type    | Required | Description                                                 |
|---------------|---------|----------|-------------------------------------------------------------|
| `config_type` | string  | No       | Filter by type (`layout`, `optimization`, `product_config`) |
| `site`        | string  | No       | Filter by site                                              |
| `author`      | string  | No       | Filter by author                                            |
| `limit`       | integer | No       | Max results (default: 50)                                   |

**Response (200 OK)**:
```json
{
  "versions": [
    {
      "version_hash": "a3f2c184",
      "config_type": "layout",
      "author": "john.doe",
      "site": "factory_A",
      "message": "Updated station 5 position to reduce material travel",
      "created_at": "2025-11-12T14:30:00Z",
      "parent_hash": "b1e4d672"
    },
    {
      "version_hash": "b1e4d672",
      "config_type": "layout",
      "author": "john.doe",
      "site": "factory_A",
      "message": "Initial layout for WO_A production line",
      "created_at": "2025-11-10T10:00:00Z",
      "parent_hash": null
    }
  ],
  "total_count": 2
}
```

---

#### 4.2 `GET /versions/{version_hash}`

Retrieve specific version details.

**Path Parameters**:
- `version_hash` (string): 8-character version hash

**Response (200 OK)**:
```json
{
  "version_hash": "a3f2c184",
  "config_type": "layout",
  "config_data": {
    "layout_id": 5,
    "site": "factory_A",
    "stations": [
      {
        "station_id": "station_0",
        "position": {"x": 0, "y": 0, "z": 0},
        "dimensions": {"width": 2.0, "depth": 1.5, "height": 2.2}
      }
    ]
  },
  "author": "john.doe",
  "site": "factory_A",
  "message": "Updated station 5 position to reduce material travel",
  "created_at": "2025-11-12T14:30:00Z",
  "parent_hash": "b1e4d672"
}
```

---

#### 4.3 `POST /versions`

Create new configuration version.

**Request Body**:
```json
{
  "config_type": "layout",
  "config_data": {
    "layout_id": 5,
    "site": "factory_A",
    "stations": [/* ... */]
  },
  "author": "john.doe",
  "site": "factory_A",
  "message": "Updated station 5 position"
}
```

**Response (200 OK)**:
```json
{
  "version_hash": "c8k3m567",
  "status": "created",
  "created_at": "2025-11-12T15:00:00Z",
  "message": "Version created successfully"
}
```

---

#### 4.4 `GET /versions/diff`

Compare two versions.

**Query Parameters**:
```
GET /versions/diff?version_a=a3f2c184&version_b=b1e4d672
```

**Response (200 OK)**:
```json
{
  "version_a": "a3f2c184",
  "version_b": "b1e4d672",
  "changes": {
    "added": {
      "stations[5].position": {"x": 10, "y": 5, "z": 0}
    },
    "removed": {},
    "modified": {
      "stations[3].position": {
        "old": {"x": 5, "y": 0, "z": 0},
        "new": {"x": 5, "y": 2, "z": 0}
      }
    }
  },
  "summary": {
    "total_changes": 2,
    "added_count": 1,
    "removed_count": 0,
    "modified_count": 1
  }
}
```

---

### 5. Collision Detection

#### 5.1 `POST /check-collision`

Check for collisions in layout configuration.

**Request Body**:
```json
{
  "layout_data": {
    "stations": [
      {
        "station_id": "station_0",
        "position": {"x": 0, "y": 0, "z": 0},
        "dimensions": {"width": 2.0, "depth": 1.5, "height": 2.2}
      },
      {
        "station_id": "station_1",
        "position": {"x": 1.5, "y": 0, "z": 0},
        "dimensions": {"width": 2.0, "depth": 1.5, "height": 2.2}
      }
    ]
  },
  "clearance": 0.5,
  "check_worker_reach": true
}
```

**Parameters**:

| Field                | Type    | Required | Description                                 |
|----------------------|---------|----------|---------------------------------------------|
| `layout_data`        | object  | Yes      | Layout configuration to check               |
| `clearance`          | float   | No       | Minimum clearance (meters, default: 0.5)    |
| `check_worker_reach` | boolean | No       | Also check ergonomic reach (default: false) |

**Response (200 OK - No Collisions)**:
```json
{
  "status": "ok",
  "collisions": [],
  "warnings": [],
  "summary": {
    "total_objects": 2,
    "collision_count": 0,
    "warning_count": 0
  }
}
```

**Response (200 OK - Collisions Found)**:
```json
{
  "status": "collision_detected",
  "collisions": [
    {
      "object_a": "station_0",
      "object_b": "station_1",
      "type": "space_conflict",
      "clearance_violation": 0.3,
      "overlap_volume": 0.9,
      "severity": "high"
    }
  ],
  "warnings": [
    {
      "object": "station_2",
      "type": "ergonomic_risk",
      "message": "Worker may have difficulty reaching workpiece",
      "severity": "medium"
    }
  ],
  "suggestions": [
    {
      "type": "move_station",
      "station_id": "station_1",
      "current_position": {"x": 1.5, "y": 0, "z": 0},
      "suggested_position": {"x": 2.8, "y": 0, "z": 0},
      "reason": "Resolve collision with station_0"
    }
  ],
  "summary": {
    "total_objects": 3,
    "collision_count": 1,
    "warning_count": 1
  }
}
```

---

#### 5.2 `GET /collision-cache/{layout_id}`

Retrieve cached collision check results.

**Path Parameters**:
- `layout_id` (integer): Layout ID

**Response (200 OK)**:
```json
{
  "layout_id": 5,
  "collision_pairs": [
    {
      "object_a": "station_0",
      "object_b": "station_1",
      "type": "space_conflict"
    }
  ],
  "clearance_used": 0.5,
  "checked_at": "2025-11-12T14:00:00Z",
  "is_valid": true
}
```

---

### 6. Omniverse Integration

#### 6.1 `POST /omniverse-session`

Start new Omniverse 3D simulation session.

**Request Body**:
```json
{
  "work_order_id": "WO_A",
  "layout_id": 5,
  "include_workers": true,
  "simulation_speed": 1.0,
  "users": ["john.doe", "jane.smith"]
}
```

**Parameters**:

| Field              | Type    | Required | Description                               |
|--------------------|---------|----------|-------------------------------------------|
| `work_order_id`    | string  | Yes      | Work order to simulate                    |
| `layout_id`        | integer | No       | Layout configuration ID                   |
| `include_workers`  | boolean | No       | Add worker digital twins (default: false) |
| `simulation_speed` | float   | No       | Playback speed multiplier (default: 1.0)  |
| `users`            | array   | No       | List of collaborators                     |

**Response (200 OK)**:
```json
{
  "session_id": "omni_session_abc123",
  "scene_url": "omniverse://nucleus/scenes/WO_A_20251112.usd",
  "streaming_url": "wss://omniverse.example.com/stream/omni_session_abc123",
  "collaboration_enabled": true,
  "users": ["john.doe", "jane.smith"],
  "status": "ready",
  "created_at": "2025-11-12T15:30:00Z",
  "expires_at": "2025-11-12T17:30:00Z"
}
```

---

#### 6.2 `GET /omniverse-session/{session_id}`

Retrieve Omniverse session status.

**Path Parameters**:
- `session_id` (string): Session ID

**Response (200 OK)**:
```json
{
  "session_id": "omni_session_abc123",
  "scene_url": "omniverse://nucleus/scenes/WO_A_20251112.usd",
  "streaming_url": "wss://omniverse.example.com/stream/omni_session_abc123",
  "status": "active",
  "users": ["john.doe", "jane.smith"],
  "active_users": ["john.doe"],
  "created_at": "2025-11-12T15:30:00Z",
  "expires_at": "2025-11-12T17:30:00Z",
  "statistics": {
    "total_frames_rendered": 18000,
    "avg_fps": 60,
    "total_users": 2,
    "total_edits": 15
  }
}
```

---

#### 6.3 `DELETE /omniverse-session/{session_id}`

Close Omniverse session.

**Path Parameters**:
- `session_id` (string): Session ID

**Response (200 OK)**:
```json
{
  "session_id": "omni_session_abc123",
  "status": "closed",
  "closed_at": "2025-11-12T16:45:00Z",
  "message": "Session closed successfully"
}
```

---

### 7. Multi-Site Sharing

#### 7.1 `POST /share-configuration`

Share configuration to another site.

**Request Body**:
```json
{
  "version_hash": "a3f2c184",
  "target_site": "factory_B",
  "shared_by": "john.doe",
  "message": "Sharing optimized layout for review"
}
```

**Response (200 OK)**:
```json
{
  "share_id": "share_xyz789",
  "version_hash": "a3f2c184",
  "source_site": "factory_A",
  "target_site": "factory_B",
  "shared_by": "john.doe",
  "status": "shared",
  "shared_at": "2025-11-12T16:00:00Z",
  "message": "Configuration shared successfully"
}
```

---

#### 7.2 `GET /shared-configurations`

List configurations shared with current site.

**Query Parameters**:
```
GET /shared-configurations?status=pending&limit=20
```

| Parameter | Type    | Required | Description                                          |
|-----------|---------|----------|------------------------------------------------------|
| `status`  | string  | No       | Filter by status (`pending`, `accepted`, `rejected`) |
| `limit`   | integer | No       | Max results (default: 50)                            |

**Response (200 OK)**:
```json
{
  "shared_configs": [
    {
      "share_id": "share_xyz789",
      "version_hash": "a3f2c184",
      "config_type": "layout",
      "source_site": "factory_A",
      "shared_by": "john.doe",
      "message": "Sharing optimized layout for review",
      "status": "pending",
      "shared_at": "2025-11-12T16:00:00Z"
    }
  ],
  "total_count": 1
}
```

---

#### 7.3 `POST /shared-configurations/{share_id}/accept`

Accept shared configuration.

**Path Parameters**:
- `share_id` (string): Share ID

**Response (200 OK)**:
```json
{
  "share_id": "share_xyz789",
  "new_version_hash": "d9n2p789",
  "status": "accepted",
  "accepted_at": "2025-11-12T16:30:00Z",
  "message": "Configuration accepted and imported"
}
```

---

## Data Models

### NLPQueryRequest

```python
class NLPQueryRequest(BaseModel):
    """Natural language query request"""
    query: str = Field(..., min_length=1, max_length=500)
    context: Optional[Dict[str, Any]] = None
    options: Optional[Dict[str, Any]] = None
```

### NLPQueryResponse

```python
class NLPQueryResponse(BaseModel):
    """Natural language query response"""
    query: str
    intent: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    entities: Dict[str, Any]
    api_calls: List[Dict[str, Any]]
    answer: str
    visualization: Optional[Dict[str, Any]] = None
    suggestions: List[str] = []
    processing_time_ms: int
```

### Model3D

```python
class Model3D(BaseModel):
    """3D model metadata"""
    id: int
    model_name: str
    usd_path: str
    category: str  # workstation, product, tool, conveyor
    dimensions: Dict[str, float]  # width, depth, height
    thumbnail_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
```

### SensorDataUpload

```python
class SensorDataUpload(BaseModel):
    """Body sensor data upload"""
    worker_id: str
    session_id: str
    metadata: Optional[Dict[str, Any]] = None
```

### MotionAnalysis

```python
class MotionAnalysis(BaseModel):
    """Motion capture analysis result"""
    upload_id: str
    worker_id: str
    session_id: str
    status: str  # processing, completed, failed
    processing_time_sec: Optional[int] = None
    motion_analysis: Optional[Dict[str, Any]] = None
    time_study_export: Optional[Dict[str, Any]] = None
    video_url: Optional[str] = None
    annotated_video_url: Optional[str] = None
```

### TaskDetection

```python
class TaskDetection(BaseModel):
    """Detected task from motion data"""
    task_id: str
    action_type: str  # install, mount, screw, test, etc.
    start_time_sec: float
    end_time_sec: float
    duration_ms: int
    avg_reba_score: int = Field(..., ge=1, le=15)
    risk_level: str  # low, medium, high, very_high
```

### Version

```python
class Version(BaseModel):
    """Configuration version"""
    version_hash: str = Field(..., min_length=8, max_length=8)
    config_type: str  # layout, optimization, product_config
    config_data: Dict[str, Any]
    author: str
    site: str
    message: str
    parent_hash: Optional[str] = None
    created_at: datetime
```

### VersionDiff

```python
class VersionDiff(BaseModel):
    """Difference between two versions"""
    version_a: str
    version_b: str
    changes: Dict[str, Any]  # added, removed, modified
    summary: Dict[str, int]  # total_changes, added_count, etc.
```

### CollisionCheck

```python
class CollisionCheck(BaseModel):
    """Collision detection request"""
    layout_data: Dict[str, Any]
    clearance: float = Field(default=0.5, ge=0.0)
    check_worker_reach: bool = False
```

### CollisionResult

```python
class CollisionResult(BaseModel):
    """Collision detection result"""
    status: str  # ok, collision_detected
    collisions: List[Dict[str, Any]]
    warnings: List[Dict[str, Any]]
    suggestions: List[Dict[str, Any]] = []
    summary: Dict[str, int]
```

### OmniverseSession

```python
class OmniverseSession(BaseModel):
    """Omniverse simulation session"""
    session_id: str
    scene_url: str
    streaming_url: str
    collaboration_enabled: bool = False
    users: List[str] = []
    status: str  # ready, active, closed
    created_at: datetime
    expires_at: datetime
```

### ShareConfiguration

```python
class ShareConfiguration(BaseModel):
    """Configuration sharing request"""
    version_hash: str
    target_site: str
    shared_by: str
    message: Optional[str] = None
```

---

## WebSocket Events

### Connection

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/sensor-stream');
```

### Event: Sensor Data Stream

**Server → Client**:
```json
{
  "event": "sensor_data",
  "worker_id": "worker_001",
  "timestamp": "2025-11-12T15:45:32.123Z",
  "landmarks": {
    "point_0": [0.5, 0.8, 0.2, 0.95],
    "point_1": [0.52, 0.75, 0.21, 0.93]
  },
  "action_type": "install",
  "reba_score": 4
}
```

### Event: Omniverse Live Sync

**Client → Server**:
```json
{
  "event": "scene_update",
  "session_id": "omni_session_abc123",
  "changes": {
    "modified": [
      {
        "prim_path": "/World/Station_0",
        "attributes": {
          "xformOp:translate": [5.0, 0.0, 0.0]
        }
      }
    ]
  }
}
```

**Server → All Clients**:
```json
{
  "event": "scene_updated",
  "session_id": "omni_session_abc123",
  "updated_by": "john.doe",
  "changes": {/* same as above */}
}
```

### Event: Collaboration Notification

**Server → Client**:
```json
{
  "event": "user_joined",
  "session_id": "omni_session_abc123",
  "user": "jane.smith",
  "timestamp": "2025-11-12T15:50:00Z"
}
```

---

## Error Handling

### Error Response Format

```json
{
  "detail": "Error message describing what went wrong",
  "error_code": "NLP_QUERY_FAILED",
  "timestamp": "2025-11-12T16:00:00Z",
  "request_id": "req_abc123"
}
```

### Error Codes

| Code                      | HTTP Status | Description                               |
|---------------------------|-------------|-------------------------------------------|
| `NLP_QUERY_FAILED`        | 400         | Unable to process natural language query  |
| `MODEL_NOT_FOUND`         | 404         | 3D model not found                        |
| `SENSOR_UPLOAD_FAILED`    | 500         | Sensor data upload failed                 |
| `VERSION_NOT_FOUND`       | 404         | Configuration version not found           |
| `COLLISION_CHECK_FAILED`  | 500         | Collision detection error                 |
| `OMNIVERSE_SESSION_ERROR` | 500         | Omniverse session creation failed         |
| `SHARE_FAILED`            | 500         | Configuration sharing failed              |
| `INSUFFICIENT_GPU_MEMORY` | 503         | Not enough GPU resources for 3D rendering |
| `LLM_RATE_LIMIT`          | 429         | Too many NLP queries                      |

---

## Usage Examples

### Example 1: Natural Language Query

```bash
curl -X POST "http://localhost:8000/nlp-query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Which station has the highest load in WO_A?",
    "options": {
      "return_visualization": true
    }
  }'
```

### Example 2: Upload Motion Capture Video

```bash
curl -X POST "http://localhost:8000/upload-sensor-data" \
  -F "video_file=@worker_001_session.mp4" \
  -F "worker_id=worker_001" \
  -F "session_id=session_20251112_001" \
  -F 'metadata={"task": "DL360_assembly"}'
```

### Example 3: Check Layout Collision

```bash
curl -X POST "http://localhost:8000/check-collision" \
  -H "Content-Type: application/json" \
  -d '{
    "layout_data": {
      "stations": [
        {
          "station_id": "station_0",
          "position": {"x": 0, "y": 0, "z": 0},
          "dimensions": {"width": 2.0, "depth": 1.5, "height": 2.2}
        },
        {
          "station_id": "station_1",
          "position": {"x": 1.5, "y": 0, "z": 0},
          "dimensions": {"width": 2.0, "depth": 1.5, "height": 2.2}
        }
      ]
    },
    "clearance": 0.5
  }'
```

### Example 4: Start Omniverse Session

```bash
curl -X POST "http://localhost:8000/omniverse-session" \
  -H "Content-Type: application/json" \
  -d '{
    "work_order_id": "WO_A",
    "layout_id": 5,
    "include_workers": true,
    "users": ["john.doe", "jane.smith"]
  }'
```

### Example 5: Share Configuration

```bash
curl -X POST "http://localhost:8000/share-configuration" \
  -H "Content-Type: application/json" \
  -d '{
    "version_hash": "a3f2c184",
    "target_site": "factory_B",
    "shared_by": "john.doe",
    "message": "Sharing optimized layout"
  }'
```

### Example 6: WebSocket Sensor Stream

```javascript
const ws = new WebSocket('ws://localhost:8000/ws/sensor-stream');

ws.onopen = () => {
  console.log('Connected to sensor stream');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Sensor data:', data);
  
  if (data.reba_score > 7) {
    alert('High ergonomic risk detected!');
  }
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};
```

---

**Document Maintainer:** JASON YY, LIN  
**Last Updated:** 2025-11-13
**Version:** 3.0.0-phase3
