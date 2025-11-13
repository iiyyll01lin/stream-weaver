# Phase 2 API Specification

**Document Version**: 1.0 | **Last Updated**: 2025-11-12  
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
GET /recommend-line-type?work_order_id=WO_A&target_takt=30000
```

| Parameter               | Type    | Required | Description                       |
|-------------------------|---------|----------|-----------------------------------|
| `work_order_id`         | string  | Yes      | Work order ID                     |
| `target_takt`           | integer | Yes      | Target takt time (ms)             |
| `max_workers_available` | integer | No       | Available workforce (default: 10) |

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
    "complexity_distribution": {
      "simple": 20,
      "medium": 10,
      "complex": 5
    },
    "min_theoretical_stations": 5.2,
    "recommended_stations": 6
  },
  "alternatives": [
    {
      "type": "cell",
      "suitability": 0.3,
      "reason": "Task count too high for cell configuration"
    },
    {
      "type": "short_line",
      "suitability": 0.85,
      "reason": "Optimal for 6 stations, moderate complexity"
    },
    {
      "type": "long_line",
      "suitability": 0.55,
      "reason": "Overkill for current workload"
    }
  ],
  "recommendations": [
    "Use short line with 6 stations",
    "Consider offline processing for 3 glue tasks",
    "Group similar screw operations to reduce transitions"
  ]
}
```

**Line Type Definitions**:
- **cell**: 1-3 stations, low task count (<20), flexible workers
- **short_line**: 4-8 stations, medium task count (20-50), dedicated workers
- **long_line**: 9+ stations, high task count (>50), specialized stations

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

## Performance Requirements

### Phase 2 Targets

| Metric                      | Target      | Notes                       |
|-----------------------------|-------------|-----------------------------|
| **Multi-Line Optimization** | < 5 seconds | 2-3 lines, ≤500 tasks total |
| **Fishbone Generation**     | < 2 seconds | ≤100 tasks                  |
| **Layout Save/Load**        | < 500ms     | Single layout operation     |
| **Product Config Query**    | < 200ms     | Single SKU lookup           |
| **Line Recommendation**     | < 1 second  | Analysis + recommendation   |

---

**Document Maintainer:** JASON YY, LIN  
**Last Updated:** 2025-11-12 
**Version:** 2.0.0-phase2
