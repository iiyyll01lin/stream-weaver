# Line Balance System - Usage Examples

> **Complete examples for all API endpoints and optimization scenarios**

---

## Table of Contents

- [Line Balance System - Usage Examples](#line-balance-system---usage-examples)
  - [Table of Contents](#table-of-contents)
  - [Example 1: Minimize Workstation Count](#example-1-minimize-workstation-count)
    - [Request](#request)
    - [Response](#response)
  - [Example 2: Minimize Manpower](#example-2-minimize-manpower)
    - [Request](#request-1)
    - [Response](#response-1)
  - [Example 3: Minimize Idle Time](#example-3-minimize-idle-time)
    - [Request](#request-2)
    - [Response](#response-2)
  - [Example 4: Offline Task Handling](#example-4-offline-task-handling)
    - [Request](#request-3)
    - [Response](#response-3)
  - [Example 5: Task Merging Optimization](#example-5-task-merging-optimization)
    - [Request](#request-4)
    - [Response](#response-4)
  - [Example 6: Complexity-Aware Optimization](#example-6-complexity-aware-optimization)
    - [Request](#request-5)
    - [Response](#response-5)
  - [Example 7: Part-Level Material Flow](#example-7-part-level-material-flow)
    - [Request](#request-6)
    - [Response](#response-6)
  - [Example 8: Multi-Line Optimization](#example-8-multi-line-optimization)
    - [Request](#request-7)
    - [Response](#response-7)
  - [Example 9: Line Type Recommendation](#example-9-line-type-recommendation)
    - [Request](#request-8)
    - [Response](#response-8)
  - [Example 10: Fishbone Diagram Generation](#example-10-fishbone-diagram-generation)
    - [Request (SVG Format)](#request-svg-format)
    - [Request (PNG Format)](#request-png-format)
    - [Response (JSON Metadata)](#response-json-metadata)
  - [Example 11: 2D Layout Management](#example-11-2d-layout-management)
    - [Save Layout](#save-layout)
    - [Response](#response-9)
    - [List Layouts](#list-layouts)
    - [Get Layout Details](#get-layout-details)
    - [Delete Layout](#delete-layout)
  - [Example 12: Product Configuration (CTO/BTO)](#example-12-product-configuration-ctobto)
    - [Create Product Configuration](#create-product-configuration)
    - [Response](#response-10)
    - [List Product Configurations](#list-product-configurations)
    - [Get Configuration Details](#get-configuration-details)
  - [Quick Reference](#quick-reference)
  - [See Also](#see-also)

---

## Example 1: Minimize Workstation Count

**Objective**: Use the fewest number of stations while respecting takt time constraints.

### Request

```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "work_order_id": "WO_A",
    "optimization_goal": "min_stations",
    "target_takt": 30000
  }'
```

### Response

```json
{
  "stations": [
    {"station_id": 1, "tasks": ["T1", "T2"], "total_time_ms": 28500},
    {"station_id": 2, "tasks": ["T3", "T4", "T5"], "total_time_ms": 29000},
    {"station_id": 3, "tasks": ["T6"], "total_time_ms": 25000}
  ],
  "summary": {
    "num_stations": 3,
    "efficiency": 0.92,
    "line_balance_rate": 91.7
  }
}
```

---

## Example 2: Minimize Manpower

**Objective**: Reduce total manpower (operators) required for all stations.

### Request

```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "work_order_id": "WO_A",
    "optimization_goal": "min_manpower",
    "target_takt": 30000
  }'
```

### Response

```json
{
  "stations": [
    {"station_id": 1, "tasks": ["T1", "T2", "T3"], "total_time_ms": 35000, "manpower": 2},
    {"station_id": 2, "tasks": ["T4", "T5", "T6"], "total_time_ms": 47500, "manpower": 2}
  ],
  "summary": {
    "total_manpower": 4,
    "num_stations": 2,
    "efficiency": 0.88
  }
}
```

---

## Example 3: Minimize Idle Time

**Objective**: Balance workloads to minimize idle (waiting) time across stations.

### Request

```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "work_order_id": "WO_A",
    "optimization_goal": "min_idle",
    "target_takt": 30000
  }'
```

### Response

```json
{
  "stations": [
    {"station_id": 1, "tasks": ["T1", "T2"], "total_time_ms": 28500, "idle_time_ms": 1500},
    {"station_id": 2, "tasks": ["T3", "T4"], "total_time_ms": 29500, "idle_time_ms": 500},
    {"station_id": 3, "tasks": ["T5", "T6"], "total_time_ms": 24500, "idle_time_ms": 5500}
  ],
  "summary": {
    "total_idle_time_ms": 7500,
    "idle_time_variance": 2567,
    "line_balance_rate": 91.7
  }
}
```

---

## Example 4: Offline Task Handling

**Objective**: Separate offline (preparation) tasks from the main production line.

### Request

```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "work_order_id": "WO_A",
    "optimization_goal": "min_stations",
    "target_takt": 30000,
    "enable_offline_separation": true
  }'
```

### Response

```json
{
  "online_stations": [
    {"station_id": 1, "tasks": ["T1", "T2"], "total_time_ms": 28000},
    {"station_id": 2, "tasks": ["T4", "T5"], "total_time_ms": 29000}
  ],
  "offline_stations": [
    {"station_id": "OFFLINE-1", "tasks": ["T3_offline"], "total_time_ms": 15000, "type": "preparation"}
  ],
  "summary": {
    "online_stations": 2,
    "offline_stations": 1,
    "offline_time_saved_ms": 15000,
    "line_balance_rate_improvement": "+8.5%"
  }
}
```

---

## Example 5: Task Merging Optimization

**Objective**: Merge compatible tasks to improve efficiency.

### Request

```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "work_order_id": "WO_A",
    "optimization_goal": "min_stations",
    "target_takt": 30000,
    "enable_task_merging": true,
    "merge_threshold_ms": 5000
  }'
```

### Response

```json
{
  "stations": [
    {"station_id": 1, "tasks": ["T1+T2_merged"], "total_time_ms": 27000, "merged": true},
    {"station_id": 2, "tasks": ["T3", "T4"], "total_time_ms": 29000},
    {"station_id": 3, "tasks": ["T5+T6_merged"], "total_time_ms": 23000, "merged": true}
  ],
  "merge_summary": {
    "original_tasks": 6,
    "merged_tasks": 4,
    "time_saved_ms": 3000,
    "efficiency_gain": "+5.2%"
  }
}
```

---

## Example 6: Complexity-Aware Optimization

**Objective**: Auto-classify tasks by complexity and optimize station assignments accordingly.

### Request

```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "work_order_id": "WO_A",
    "optimization_goal": "min_stations",
    "target_takt": 30000,
    "enable_complexity_classification": true
  }'
```

### Response

```json
{
  "stations": [
    {"station_id": 1, "tasks": ["T1", "T2"], "complexity_distribution": {"simple": 2, "complex": 0}},
    {"station_id": 2, "tasks": ["T3", "T4"], "complexity_distribution": {"simple": 1, "complex": 1}},
    {"station_id": 3, "tasks": ["T5", "T6"], "complexity_distribution": {"simple": 0, "complex": 2}}
  ],
  "complexity_summary": {
    "simple_tasks": 3,
    "medium_tasks": 0,
    "complex_tasks": 3,
    "skill_level_recommendation": {
      "station_1": "junior",
      "station_2": "intermediate",
      "station_3": "senior"
    }
  }
}
```

---

## Example 7: Part-Level Material Flow

**Objective**: Track part-level material flow and generate part-station matrices.

### Request

```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "work_order_id": "WO_A",
    "optimization_goal": "min_stations",
    "target_takt": 30000,
    "enable_part_tracking": true
  }'
```

### Response

```json
{
  "stations": [
    {"station_id": 1, "tasks": ["T1", "T2"], "parts_used": ["P001", "P002"]},
    {"station_id": 2, "tasks": ["T3", "T4"], "parts_used": ["P002", "P003", "P004"]},
    {"station_id": 3, "tasks": ["T5", "T6"], "parts_used": ["P004", "P005"]}
  ],
  "part_station_matrix": {
    "P001": [1],
    "P002": [1, 2],
    "P003": [2],
    "P004": [2, 3],
    "P005": [3]
  },
  "material_flow": {
    "total_parts": 5,
    "multi_station_parts": 2,
    "kitting_zones": ["zone_1", "zone_2"]
  }
}
```

---

## Example 8: Multi-Line Optimization

**Objective**: Optimize multiple production lines simultaneously with cross-line balancing.

### Request

```bash
curl -X POST http://localhost:8000/optimize \
  -H "Content-Type: application/json" \
  -d '{
    "work_order_id": "WO_MULTI",
    "optimization_goal": "min_stations",
    "target_takt": 30000,
    "multi_line_config": {
      "enabled": true,
      "lines": [
        {"line_id": "LINE_A", "target_takt": 30000, "max_stations": 5},
        {"line_id": "LINE_B", "target_takt": 25000, "max_stations": 6}
      ],
      "cross_line_balancing": true
    }
  }'
```

### Response

```json
{
  "lines": [
    {
      "line_id": "LINE_A",
      "stations": [
        {"station_id": "A1", "tasks": ["T1", "T2"], "total_time_ms": 28000},
        {"station_id": "A2", "tasks": ["T3", "T4"], "total_time_ms": 29500}
      ],
      "line_summary": {"num_stations": 2, "efficiency": 0.95}
    },
    {
      "line_id": "LINE_B",
      "stations": [
        {"station_id": "B1", "tasks": ["T5", "T6"], "total_time_ms": 24000},
        {"station_id": "B2", "tasks": ["T7", "T8"], "total_time_ms": 24500}
      ],
      "line_summary": {"num_stations": 2, "efficiency": 0.97}
    }
  ],
  "global_summary": {
    "total_stations": 4,
    "total_efficiency": 0.96,
    "cross_line_balance_index": 0.98
  }
}
```

---

## Example 9: Line Type Recommendation

**Objective**: Get AI-powered recommendation for optimal line type based on production parameters.

### Request

```bash
curl "http://localhost:8000/recommend-line-type?work_order_id=WO_A&target_takt=30000&volume=1000"
```

### Response

```json
{
  "recommendation": {
    "line_type": "short_line",
    "confidence": 0.87,
    "alternatives": [
      {"type": "cell", "score": 0.72},
      {"type": "long_line", "score": 0.45}
    ]
  },
  "analysis": {
    "task_count": 25,
    "total_time_ms": 450000,
    "complexity_score": 3.2,
    "volume_factor": "medium"
  },
  "rationale": "Short line recommended due to moderate task count (25) and medium production volume. Cell layout would be less efficient for this volume. Long line not recommended due to lower task variety."
}
```

---

## Example 10: Fishbone Diagram Generation

**Objective**: Generate visual assembly sequence diagrams for production documentation.

### Request (SVG Format)

```bash
curl "http://localhost:8000/fishbone-diagram?work_order_id=WO_A&format=svg" -o fishbone.svg
```

### Request (PNG Format)

```bash
curl "http://localhost:8000/fishbone-diagram?work_order_id=WO_A&format=png" -o fishbone.png
```

### Response (JSON Metadata)

```bash
curl "http://localhost:8000/fishbone-diagram?work_order_id=WO_A&format=json"
```

```json
{
  "work_order_id": "WO_A",
  "diagram_type": "fishbone",
  "nodes": [
    {"id": "T1", "label": "Install Chassis", "time_ms": 15000, "level": 1},
    {"id": "T2", "label": "Mount CPU", "time_ms": 12000, "level": 2},
    {"id": "T3", "label": "Install Memory", "time_ms": 8000, "level": 2}
  ],
  "edges": [
    {"from": "T1", "to": "T2", "type": "precedence"},
    {"from": "T1", "to": "T3", "type": "precedence"}
  ],
  "export_formats": ["svg", "png", "pdf"]
}
```

---

## Example 11: 2D Layout Management

**Objective**: Save and retrieve production line layouts with drag-and-drop positioning.

### Save Layout

```bash
curl -X POST http://localhost:8000/save-layout \
  -H "Content-Type: application/json" \
  -d '{
    "site": "factory_A",
    "layout_name": "Line_1_Config_v2",
    "elements": [
      {"type": "station", "id": "S1", "x": 100, "y": 200, "width": 150, "height": 100},
      {"type": "station", "id": "S2", "x": 300, "y": 200, "width": 150, "height": 100},
      {"type": "conveyor", "id": "C1", "start": {"x": 250, "y": 250}, "end": {"x": 300, "y": 250}}
    ],
    "connections": [
      {"from": "S1", "to": "S2", "via": "C1"}
    ]
  }'
```

### Response

```json
{
  "layout_id": 42,
  "site": "factory_A",
  "layout_name": "Line_1_Config_v2",
  "created_at": "2025-01-15T10:30:00Z",
  "version": 1
}
```

### List Layouts

```bash
curl "http://localhost:8000/layout?site=factory_A"
```

```json
{
  "layouts": [
    {"id": 42, "name": "Line_1_Config_v2", "site": "factory_A", "updated_at": "2025-01-15T10:30:00Z"},
    {"id": 38, "name": "Line_1_Config_v1", "site": "factory_A", "updated_at": "2025-01-10T14:00:00Z"}
  ],
  "total": 2
}
```

### Get Layout Details

```bash
curl "http://localhost:8000/layout/42"
```

### Delete Layout

```bash
curl -X DELETE "http://localhost:8000/layout/42"
```

---

## Example 12: Product Configuration (CTO/BTO)

**Objective**: Manage product configurations for Configure-to-Order (CTO) and Build-to-Order (BTO) scenarios.

### Create Product Configuration

```bash
curl -X POST http://localhost:8000/product-config \
  -H "Content-Type: application/json" \
  -d '{
    "product_family": "DL380_Gen10",
    "variant_id": "DL380_8SFF_2P",
    "description": "DL380 Gen10 8-bay SFF with dual processors",
    "base_configuration": {
      "chassis": "DL380_8SFF",
      "processors": 2,
      "memory_slots": 24
    },
    "optional_modules": [
      {"module_id": "GPU_A100", "compatible": true, "add_time_ms": 15000},
      {"module_id": "NVME_SSD", "compatible": true, "add_time_ms": 8000}
    ],
    "time_adjustments": {
      "base_time_ms": 45000,
      "per_processor_ms": 12000,
      "per_memory_slot_ms": 500
    }
  }'
```

### Response

```json
{
  "config_id": 15,
  "product_family": "DL380_Gen10",
  "variant_id": "DL380_8SFF_2P",
  "created_at": "2025-01-15T11:00:00Z",
  "estimated_base_time_ms": 69000
}
```

### List Product Configurations

```bash
curl "http://localhost:8000/product-config?product_family=DL380_Gen10"
```

```json
{
  "configurations": [
    {"config_id": 15, "variant_id": "DL380_8SFF_2P", "base_time_ms": 69000},
    {"config_id": 12, "variant_id": "DL380_24SFF_4P", "base_time_ms": 125000}
  ],
  "total": 2
}
```

### Get Configuration Details

```bash
curl "http://localhost:8000/product-config/15"
```

```json
{
  "config_id": 15,
  "product_family": "DL380_Gen10",
  "variant_id": "DL380_8SFF_2P",
  "description": "DL380 Gen10 8-bay SFF with dual processors",
  "base_configuration": {
    "chassis": "DL380_8SFF",
    "processors": 2,
    "memory_slots": 24
  },
  "optional_modules": {
    "GPU_A100": {
      "compatible": true,
      "add_time_ms": 15000
    },
    "NVME_SSD": {
      "compatible": true,
      "add_time_ms": 8000
    }
  },
  "time_adjustments": {
    "base_time_ms": 45000,
    "per_processor_ms": 12000,
    "per_memory_slot_ms": 500
  },
  "estimated_base_time_ms": 69000,
  "created_at": "2025-01-15T11:00:00Z"
}
```

---

## Quick Reference

| Example | Endpoint | Use Case |
|---------|----------|----------|
| 1-3 | `POST /optimize` | Basic optimization (stations/manpower/idle) |
| 4 | `POST /optimize` | Offline task separation |
| 5 | `POST /optimize` | Task merging |
| 6 | `POST /optimize` | Complexity classification |
| 7 | `POST /optimize` | Part tracking |
| 8 | `POST /optimize` | Multi-line optimization |
| 9 | `GET /recommend-line-type` | Line type recommendation |
| 10 | `GET /fishbone-diagram` | Diagram generation |
| 11 | `POST /save-layout` | Layout management |
| 12 | `POST /product-config` | Product configuration |

---

## See Also

- [Phase 1 API Specification](PHASE1_API_SPEC_EN.md) - Core optimization endpoints
- [Phase 2 API Specification](PHASE2_API_SPEC_EN.md) - Multi-line and layout endpoints
- [Phase 3 API Specification](PHASE3_API_SPEC_EN.md) - AI/ML and 3D endpoints
- [Quick Start Guide](QUICKSTART_EN.md) - Getting started

---

**Document Maintainer:** JASON YY, LIN  
**Last Updated:** 2025-12-14
