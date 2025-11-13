# Phase 3 Implementation Guide

**Document Version**: 1.0 | **Last Updated**: 2025-11-12  
**Related Documents**:
- [Phase 3 Architecture](PHASE3_ARCHITECTURE_EN.md)
- [Phase 3 API Specification](PHASE3_API_SPEC_EN.md)
- [Phase 2 Implementation Guide](PHASE2_IMPLEMENTATION_EN.md)

---

## Table of Contents

- [Phase 3 Implementation Guide](#phase-3-implementation-guide)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Environment Setup](#environment-setup)
    - [1. Install Phase 3 Dependencies](#1-install-phase-3-dependencies)
    - [2. Environment Configuration](#2-environment-configuration)
    - [3. Project Structure](#3-project-structure)
  - [Feature Implementation](#feature-implementation)
    - [1. Natural Language Query System](#1-natural-language-query-system)
      - [Step 1: Create NLP Service (`src/services/nlp_service.py`)](#step-1-create-nlp-service-srcservicesnlp_servicepy)
      - [Step 2: Integrate NLP Service into API](#step-2-integrate-nlp-service-into-api)
      - [Step 3: Test NLP Service](#step-3-test-nlp-service)
    - [2. Body Sensor Data Processing](#2-body-sensor-data-processing)
      - [Step 1: Create Sensor Processor (`src/services/sensor_processor.py`)](#step-1-create-sensor-processor-srcservicessensor_processorpy)
      - [Step 2: Add API Endpoints for Sensor Data](#step-2-add-api-endpoints-for-sensor-data)
    - [3. 3D Model Management](#3-3d-model-management)
    - [4. Version Control System](#4-version-control-system)
    - [5. Collision Detection](#5-collision-detection)
    - [6. Omniverse Integration](#6-omniverse-integration)
    - [7. Multi-Site Sharing](#7-multi-site-sharing)
  - [Database Setup](#database-setup)
  - [Testing](#testing)
  - [Deployment](#deployment)
    - [Docker Deployment](#docker-deployment)
  - [Performance Tuning](#performance-tuning)
    - [1. LLM Query Caching](#1-llm-query-caching)
    - [2. Sensor Processing Optimization](#2-sensor-processing-optimization)
    - [3. Database Indexing](#3-database-indexing)

---

## Overview

Phase 3 builds upon Phase 2 infrastructure to add advanced AI/ML and 3D simulation capabilities:

- **Natural Language Query**: LLM-powered conversational interface
- **Body Sensor Processing**: Motion capture and ergonomic analysis
- **3D Simulation**: NVIDIA Omniverse integration
- **Version Management**: Git-like configuration control
- **Collision Detection**: Automated layout interference checking
- **Multi-Site Collaboration**: Cross-factory sharing

---

## Environment Setup

### 1. Install Phase 3 Dependencies

**Update `requirements.txt`**:
```txt
# Phase 1 & 2 dependencies
fastapi>=0.104.0
uvicorn[standard]>=0.24.0
pydantic>=2.0.0
ortools>=9.7.0
pandas>=2.0.0
sqlalchemy>=2.0.0
networkx>=3.0
matplotlib>=3.7.0
alembic>=1.12.0

# Phase 3 NEW dependencies
# LLM & NLP
langchain>=0.1.0
openai>=1.3.0
tiktoken>=0.5.0
anthropic>=0.7.0          # Optional: Claude API
chromadb>=0.4.0           # Vector store for embeddings

# Computer Vision & ML
mediapipe>=0.10.0
opencv-python>=4.8.0
torch>=2.0.0
torchvision>=0.15.0
scikit-learn>=1.3.0

# 3D & Simulation
pxr>=23.11                # USD Python bindings
omni-client>=1.0.0        # Omniverse client library

# Additional utilities
websockets>=12.0
python-multipart>=0.0.6   # File uploads
pillow>=10.0.0
numpy>=1.24.0
scipy>=1.11.0
```

**Install**:
```bash
pip install -r requirements.txt
```

**Install Omniverse Launcher** (for development):
```bash
# Download from https://www.nvidia.com/en-us/omniverse/download/
# Install Nucleus Server and Kit SDK
```

---

### 2. Environment Configuration

Create/Update `.env` file:
```bash
# Database configuration
DATABASE_URL=postgresql://user:password@localhost:5432/line_balance_db
# For development:
# DATABASE_URL=sqlite:///./line_balance.db

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG_MODE=True

# OpenAI API (for NLP)
OPENAI_API_KEY=sk-your-api-key-here
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2000

# Omniverse Configuration
OMNIVERSE_NUCLEUS_SERVER=omniverse://localhost/Projects
OMNIVERSE_KIT_PATH=/path/to/omniverse/kit

# File Storage
LAYOUT_STORAGE_PATH=./storage/layouts
FISHBONE_OUTPUT_PATH=./output/fishbone
SENSOR_DATA_PATH=./storage/sensor_data
MODEL_LIBRARY_PATH=./storage/3d_models

# WebSocket
WS_MAX_CONNECTIONS=100

# Performance
MAX_UPLOAD_SIZE_MB=500
SENSOR_PROCESSING_WORKERS=4
```

---

### 3. Project Structure

```
line-balance/
├── src/
│   ├── api_server.py               # Extended API (Phase 1+2+3)
│   ├── dashboard.html              # Enhanced UI with React
│   ├── sche-algo.py                # Phase 1 solver
│   ├── sche-algo-v2.py             # Phase 2 multi-line solver
│   ├── fishbone_generator.py       # Phase 2 fishbone
│   ├── models/                     # Database models
│   │   ├── __init__.py
│   │   ├── layout.py
│   │   ├── product_config.py
│   │   ├── sensor_data.py          # NEW
│   │   ├── model_library.py        # NEW
│   │   ├── version.py              # NEW
│   │   └── collaboration.py        # NEW
│   ├── services/                   # Business logic
│   │   ├── __init__.py
│   │   ├── layout_service.py
│   │   ├── product_service.py
│   │   ├── nlp_service.py          # NEW
│   │   ├── sensor_processor.py     # NEW
│   │   ├── version_manager.py      # NEW
│   │   ├── collision_detector.py   # NEW
│   │   └── omniverse_connector.py  # NEW
│   ├── ml/                         # NEW: ML models
│   │   ├── __init__.py
│   │   ├── pose_estimator.py       # MediaPipe wrapper
│   │   ├── action_classifier.py    # Task classification
│   │   └── ergonomic_analyzer.py   # REBA calculator
│   └── utils/
│       ├── __init__.py
│       ├── db.py
│       └── validators.py
├── frontend/                       # NEW: React app
│   ├── src/
│   │   ├── components/
│   │   │   ├── NLPQueryPanel.jsx
│   │   │   ├── ThreeDViewer.jsx
│   │   │   ├── SensorDashboard.jsx
│   │   │   └── VersionControl.jsx
│   │   ├── App.jsx
│   │   └── index.js
│   ├── package.json
│   └── webpack.config.js
├── data/                           # CSV input files
├── output/                         # Algorithm outputs
├── storage/                        # File storage
│   ├── layouts/
│   ├── sensor_data/                # NEW
│   │   ├── videos/
│   │   └── processed/
│   └── 3d_models/                  # NEW
│       ├── workstations/
│       ├── products/
│       └── tools/
├── migrations/                     # Alembic migrations
├── tests/                          # Test suites
│   ├── test_nlp_service.py         # NEW
│   ├── test_sensor_processor.py    # NEW
│   ├── test_collision_detector.py  # NEW
│   └── test_version_manager.py     # NEW
└── docs/                           # Documentation
```

---

## Feature Implementation

### 1. Natural Language Query System

#### Step 1: Create NLP Service (`src/services/nlp_service.py`)

```python
#!/usr/bin/env python3
"""
Natural Language Processing Service
Phase 3 - LangChain Integration
"""

import os
import re
from typing import Dict, Any, List, Optional
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain.memory import ConversationBufferMemory
from langchain.agents import Tool, AgentExecutor, create_react_agent

class NLPService:
    """Natural language query processing service"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        self.model = os.getenv('OPENAI_MODEL', 'gpt-4')
        
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not found in environment")
        
        self.llm = ChatOpenAI(
            model=self.model,
            temperature=0,
            openai_api_key=self.api_key
        )
        
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True
        )
        
        self.intent_classifier = self._build_intent_classifier()
        self.entity_extractor = self._build_entity_extractor()
        self.response_generator = self._build_response_generator()
    
    def _build_intent_classifier(self) -> LLMChain:
        """Build intent recognition chain"""
        template = """
        You are an expert at understanding user queries for a production line balancing system.
        
        Classify the following user query into ONE of these intents:
        - query_bottleneck: User asking about bottleneck stations
        - query_utilization: User asking about station utilization or efficiency
        - query_workstation: User asking about specific workstation details
        - optimize_layout: User requesting layout optimization
        - show_3d_model: User requesting 3D visualization
        - analyze_sensor: User requesting sensor/ergonomic data analysis
        - compare_versions: User comparing different configurations
        - recommend: User asking for recommendations or suggestions
        - unknown: Cannot determine intent
        
        User query: {query}
        
        Return ONLY the intent name, nothing else.
        Intent:
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["query"]
        )
        
        return LLMChain(llm=self.llm, prompt=prompt)
    
    def _build_entity_extractor(self) -> LLMChain:
        """Build entity extraction chain"""
        template = """
        Extract entities from the following user query for a production line system.
        
        Possible entities:
        - work_order: Work order ID (e.g., WO_A, WO_B, WO_C)
        - station: Station number or ID
        - metric: Performance metric (load, utilization, takt, idle, etc.)
        - aggregation: Aggregation function (max, min, avg, sum, etc.)
        - worker_id: Worker identifier
        - time_range: Time period mentioned
        - version: Version hash or identifier
        
        User query: {query}
        
        Return a JSON object with extracted entities. Use null for missing entities.
        Example: {{"work_order": "WO_A", "metric": "load", "aggregation": "max", "station": null}}
        
        Entities:
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["query"]
        )
        
        return LLMChain(llm=self.llm, prompt=prompt)
    
    def _build_response_generator(self) -> LLMChain:
        """Build natural language response generator"""
        template = """
        You are a helpful assistant for a production line balancing system.
        
        User asked: {query}
        
        API returned this data:
        {api_result}
        
        Generate a clear, concise natural language response answering the user's question.
        Be specific with numbers and metrics. Keep it under 3 sentences.
        
        Response:
        """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["query", "api_result"]
        )
        
        return LLMChain(llm=self.llm, prompt=prompt)
    
    async def process_query(
        self,
        query: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process natural language query
        
        Args:
            query: User's natural language query
            context: Optional context (current work order, etc.)
        
        Returns:
            Dict with intent, entities, API calls, and response
        """
        import time
        start_time = time.time()
        
        # Step 1: Classify intent
        intent_result = await self.intent_classifier.arun(query=query)
        intent = intent_result.strip()
        
        # Step 2: Extract entities
        entities_result = await self.entity_extractor.arun(query=query)
        entities = self._parse_json_entities(entities_result)
        
        # Apply context defaults
        if context:
            for key, value in context.items():
                if key not in entities or entities[key] is None:
                    entities[key] = value
        
        # Step 3: Map to API call
        api_call = self._intent_to_api(intent, entities)
        
        # Step 4: Execute API call (simulated here, real implementation would call actual API)
        api_result = await self._execute_api_call(api_call)
        
        # Step 5: Generate natural language response
        response_text = await self.response_generator.arun(
            query=query,
            api_result=str(api_result)
        )
        
        # Step 6: Generate suggestions
        suggestions = self._generate_suggestions(intent, entities)
        
        processing_time = int((time.time() - start_time) * 1000)
        
        return {
            "query": query,
            "intent": intent,
            "confidence": 0.95,  # Could be calculated from LLM logprobs
            "entities": entities,
            "api_calls": [api_call],
            "answer": response_text.strip(),
            "suggestions": suggestions,
            "processing_time_ms": processing_time
        }
    
    def _parse_json_entities(self, entities_str: str) -> Dict[str, Any]:
        """Parse JSON entities from LLM response"""
        import json
        try:
            # Extract JSON from potential markdown code blocks
            if "```json" in entities_str:
                entities_str = entities_str.split("```json")[1].split("```")[0]
            elif "```" in entities_str:
                entities_str = entities_str.split("```")[1].split("```")[0]
            
            return json.loads(entities_str.strip())
        except:
            return {}
    
    def _intent_to_api(
        self,
        intent: str,
        entities: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Map intent and entities to API endpoint"""
        
        intent_mapping = {
            "query_bottleneck": {
                "endpoint": "/workstations",
                "method": "GET",
                "params": {
                    "work_order_id": entities.get("work_order", "WO_A"),
                    "target_takt": 30000
                }
            },
            "query_utilization": {
                "endpoint": "/takt-summary",
                "method": "GET",
                "params": {
                    "work_order_id": entities.get("work_order", "WO_A"),
                    "target_takt": 30000
                }
            },
            "query_workstation": {
                "endpoint": "/workstations",
                "method": "GET",
                "params": {
                    "work_order_id": entities.get("work_order", "WO_A"),
                    "station_id": entities.get("station")
                }
            },
            "optimize_layout": {
                "endpoint": "/optimize",
                "method": "POST",
                "params": {
                    "work_order_id": entities.get("work_order", "WO_A"),
                    "optimization_goal": "min_stations",
                    "target_takt": 30000
                }
            },
            "show_3d_model": {
                "endpoint": "/3d-models",
                "method": "GET",
                "params": {
                    "station_id": entities.get("station")
                }
            },
            "analyze_sensor": {
                "endpoint": "/sensor-data/worker/{worker_id}",
                "method": "GET",
                "params": {
                    "worker_id": entities.get("worker_id", "worker_001")
                }
            }
        }
        
        return intent_mapping.get(intent, {
            "endpoint": "/health",
            "method": "GET",
            "params": {}
        })
    
    async def _execute_api_call(self, api_call: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute API call (placeholder - in real implementation, 
        this would call the actual FastAPI endpoints)
        """
        # Simulated response
        if api_call["endpoint"] == "/workstations":
            return {
                "stations": [
                    {"station_index": 0, "load_ms": 25000, "utilization_pct": 83.3},
                    {"station_index": 1, "load_ms": 27500, "utilization_pct": 91.7},
                    {"station_index": 2, "load_ms": 28500, "utilization_pct": 95.0}
                ]
            }
        
        return {"status": "ok"}
    
    def _generate_suggestions(
        self,
        intent: str,
        entities: Dict[str, Any]
    ) -> List[str]:
        """Generate follow-up query suggestions"""
        suggestions = {
            "query_bottleneck": [
                "Show me the task breakdown for the bottleneck station",
                "How can I reduce the load on that station?"
            ],
            "query_utilization": [
                "Compare utilization with other work orders",
                "Show me a Gantt chart of the stations"
            ],
            "optimize_layout": [
                "Show the 3D simulation of this layout",
                "Check for collisions in this layout"
            ]
        }
        
        return suggestions.get(intent, [
            "What's the bottleneck station?",
            "Show me the optimization result"
        ])


# Example usage
async def main():
    nlp = NLPService()
    
    result = await nlp.process_query(
        "Which station has the highest load in WO_A?"
    )
    
    print(f"Intent: {result['intent']}")
    print(f"Answer: {result['answer']}")
    print(f"Processing time: {result['processing_time_ms']}ms")


if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
```

#### Step 2: Integrate NLP Service into API

Add to `src/api_server.py`:

```python
from services.nlp_service import NLPService

# Initialize NLP service
nlp_service = NLPService()

@app.post("/nlp-query")
async def nlp_query(request: NLPQueryRequest):
    """Process natural language query"""
    try:
        result = await nlp_service.process_query(
            query=request.query,
            context=request.context
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"NLP query processing failed: {str(e)}"
        )
```

#### Step 3: Test NLP Service

```bash
# Test with curl
curl -X POST "http://localhost:8000/nlp-query" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "Which station has the highest load in WO_A?",
    "context": {"current_work_order": "WO_A"}
  }'
```

---

### 2. Body Sensor Data Processing

#### Step 1: Create Sensor Processor (`src/services/sensor_processor.py`)

```python
#!/usr/bin/env python3
"""
Body Sensor Data Processor
Phase 3 - Motion Capture Analysis
"""

import cv2
import mediapipe as mp
import numpy as np
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import json

@dataclass
class Landmark:
    """3D landmark point"""
    x: float
    y: float
    z: float
    visibility: float


class SensorDataProcessor:
    """Process body sensor motion capture data using MediaPipe"""
    
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.mp_drawing = mp.solutions.drawing_utils
        
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            enable_segmentation=False,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        
        # REBA lookup tables (simplified)
        self.reba_table_a = self._init_reba_table_a()
        self.reba_table_b = self._init_reba_table_b()
        self.reba_table_c = self._init_reba_table_c()
    
    def process_video(
        self,
        video_path: str,
        output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process video and extract motion data
        
        Args:
            video_path: Path to input video
            output_path: Optional path to save annotated video
        
        Returns:
            Dict with motion analysis results
        """
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            raise ValueError(f"Cannot open video: {video_path}")
        
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration_sec = frame_count / fps
        
        # Prepare video writer if output requested
        if output_path:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        else:
            out = None
        
        motion_data = []
        frame_idx = 0
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert BGR to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            image.flags.writeable = False
            
            # Process frame
            results = self.pose.process(image)
            
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            
            if results.pose_landmarks:
                # Extract landmarks
                landmarks = self._extract_landmarks(results.pose_landmarks)
                
                # Classify action
                action_type = self._classify_action(landmarks)
                
                # Calculate REBA score
                reba_score = self._calculate_reba(landmarks)
                
                # Store frame data
                motion_data.append({
                    "frame": frame_idx,
                    "timestamp_ms": int(frame_idx * 1000 / fps),
                    "landmarks": landmarks,
                    "action_type": action_type,
                    "reba_score": reba_score
                })
                
                # Draw annotations if output requested
                if out:
                    self.mp_drawing.draw_landmarks(
                        image,
                        results.pose_landmarks,
                        self.mp_pose.POSE_CONNECTIONS
                    )
                    
                    # Add REBA score overlay
                    color = self._get_reba_color(reba_score)
                    cv2.putText(
                        image,
                        f"REBA: {reba_score} - {action_type}",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        1,
                        color,
                        2
                    )
                    
                    out.write(image)
            
            frame_idx += 1
        
        cap.release()
        if out:
            out.release()
        
        # Generate analysis
        analysis = self._generate_analysis(motion_data, fps, duration_sec)
        
        return analysis
    
    def _extract_landmarks(self, pose_landmarks) -> Dict[str, Landmark]:
        """Extract landmark coordinates"""
        landmarks = {}
        for idx, landmark in enumerate(pose_landmarks.landmark):
            landmarks[f"point_{idx}"] = Landmark(
                x=landmark.x,
                y=landmark.y,
                z=landmark.z,
                visibility=landmark.visibility
            )
        return landmarks
    
    def _classify_action(self, landmarks: Dict[str, Landmark]) -> str:
        """Classify assembly action from pose"""
        # Get key points
        left_shoulder = landmarks.get("point_11")
        left_elbow = landmarks.get("point_13")
        left_wrist = landmarks.get("point_15")
        right_shoulder = landmarks.get("point_12")
        right_elbow = landmarks.get("point_14")
        right_wrist = landmarks.get("point_16")
        
        if not all([left_shoulder, left_elbow, left_wrist]):
            return "unknown"
        
        # Calculate arm angles
        left_angle = self._calculate_angle(
            [left_shoulder.x, left_shoulder.y],
            [left_elbow.x, left_elbow.y],
            [left_wrist.x, left_wrist.y]
        )
        
        # Simple rule-based classification
        if left_angle > 160:
            return "reaching"
        elif left_angle < 90:
            if left_wrist.y < left_elbow.y:
                return "installing"
            else:
                return "mounting"
        elif self._is_repetitive_motion(landmarks):
            return "screwing"
        else:
            return "positioning"
    
    def _calculate_angle(self, a, b, c):
        """Calculate angle between three points"""
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        
        radians = np.arctan2(c[1]-b[1], c[0]-b[0]) - \
                  np.arctan2(a[1]-b[1], a[0]-b[0])
        angle = np.abs(radians*180.0/np.pi)
        
        if angle > 180.0:
            angle = 360 - angle
        
        return angle
    
    def _is_repetitive_motion(self, landmarks: Dict[str, Landmark]) -> bool:
        """Detect repetitive wrist motion (simplified)"""
        # This would require temporal analysis across frames
        # Placeholder implementation
        return False
    
    def _calculate_reba(self, landmarks: Dict[str, Landmark]) -> int:
        """
        Calculate REBA (Rapid Entire Body Assessment) score
        Score 1: Negligible risk
        Score 2-3: Low risk, change may be needed
        Score 4-7: Medium risk, investigate and change soon
        Score 8-10: High risk, investigate and change immediately
        Score 11-15: Very high risk, implement change now
        """
        # Step A: Neck, Trunk, Legs
        neck_score = self._assess_neck(landmarks)
        trunk_score = self._assess_trunk(landmarks)
        leg_score = self._assess_legs(landmarks)
        
        score_a = self.reba_table_a.get((neck_score, trunk_score, leg_score), 1)
        
        # Step B: Upper arms, Lower arms, Wrists
        upper_arm_score = self._assess_upper_arm(landmarks)
        lower_arm_score = self._assess_lower_arm(landmarks)
        wrist_score = self._assess_wrist(landmarks)
        
        score_b = self.reba_table_b.get((upper_arm_score, lower_arm_score, wrist_score), 1)
        
        # Step C: Combined score
        reba_score = self.reba_table_c.get((score_a, score_b), 1)
        
        return reba_score
    
    def _assess_neck(self, landmarks: Dict[str, Landmark]) -> int:
        """Assess neck posture (1-3)"""
        # Simplified: check neck flexion
        nose = landmarks.get("point_0")
        left_shoulder = landmarks.get("point_11")
        
        if not nose or not left_shoulder:
            return 1
        
        # If nose is significantly below shoulder level, neck is bent
        if nose.y > left_shoulder.y + 0.1:
            return 2
        else:
            return 1
    
    def _assess_trunk(self, landmarks: Dict[str, Landmark]) -> int:
        """Assess trunk posture (1-5)"""
        # Simplified: check trunk angle
        left_shoulder = landmarks.get("point_11")
        left_hip = landmarks.get("point_23")
        
        if not left_shoulder or not left_hip:
            return 1
        
        # Calculate trunk angle (simplified)
        vertical_diff = abs(left_shoulder.y - left_hip.y)
        
        if vertical_diff < 0.3:
            return 3  # Bent > 60 degrees
        elif vertical_diff < 0.5:
            return 2  # Bent 20-60 degrees
        else:
            return 1  # Upright
    
    def _assess_legs(self, landmarks: Dict[str, Landmark]) -> int:
        """Assess leg posture (1-2)"""
        # Simplified: check if standing
        return 1  # Assume standing for now
    
    def _assess_upper_arm(self, landmarks: Dict[str, Landmark]) -> int:
        """Assess upper arm posture (1-6)"""
        left_shoulder = landmarks.get("point_11")
        left_elbow = landmarks.get("point_13")
        
        if not left_shoulder or not left_elbow:
            return 1
        
        # Check if arm is raised
        if left_elbow.y < left_shoulder.y:
            return 3  # Arm raised
        else:
            return 2  # Arm at side
    
    def _assess_lower_arm(self, landmarks: Dict[str, Landmark]) -> int:
        """Assess lower arm posture (1-2)"""
        return 1  # Simplified
    
    def _assess_wrist(self, landmarks: Dict[str, Landmark]) -> int:
        """Assess wrist posture (1-3)"""
        return 1  # Simplified
    
    def _init_reba_table_a(self) -> Dict:
        """Initialize REBA Table A (simplified)"""
        # (neck, trunk, legs) -> score_a
        return {
            (1, 1, 1): 1,
            (1, 2, 1): 2,
            (2, 2, 1): 3,
            (2, 3, 1): 4,
            (3, 3, 1): 5
        }
    
    def _init_reba_table_b(self) -> Dict:
        """Initialize REBA Table B (simplified)"""
        # (upper_arm, lower_arm, wrist) -> score_b
        return {
            (1, 1, 1): 1,
            (2, 1, 1): 2,
            (3, 1, 1): 3,
            (3, 2, 1): 4
        }
    
    def _init_reba_table_c(self) -> Dict:
        """Initialize REBA Table C (simplified)"""
        # (score_a, score_b) -> final_reba
        return {
            (1, 1): 1,
            (2, 1): 2,
            (2, 2): 3,
            (3, 2): 4,
            (3, 3): 5,
            (4, 3): 6,
            (4, 4): 7,
            (5, 4): 8
        }
    
    def _get_reba_color(self, score: int) -> tuple:
        """Get color for REBA score visualization"""
        if score <= 3:
            return (0, 255, 0)  # Green - Low risk
        elif score <= 7:
            return (0, 255, 255)  # Yellow - Medium risk
        elif score <= 10:
            return (0, 165, 255)  # Orange - High risk
        else:
            return (0, 0, 255)  # Red - Very high risk
    
    def _generate_analysis(
        self,
        motion_data: List[Dict],
        fps: int,
        duration_sec: float
    ) -> Dict[str, Any]:
        """Generate comprehensive analysis from motion data"""
        if not motion_data:
            return {"error": "No motion data captured"}
        
        # Detect tasks (segments with consistent action)
        tasks = self._detect_tasks(motion_data, fps)
        
        # Calculate ergonomic metrics
        reba_scores = [frame["reba_score"] for frame in motion_data]
        avg_reba = np.mean(reba_scores)
        max_reba = np.max(reba_scores)
        
        # Determine risk level
        if avg_reba <= 3:
            risk_level = "low"
        elif avg_reba <= 7:
            risk_level = "medium"
        elif avg_reba <= 10:
            risk_level = "high"
        else:
            risk_level = "very_high"
        
        # Generate recommendations
        recommendations = self._generate_recommendations(tasks, avg_reba)
        
        return {
            "total_frames": len(motion_data),
            "fps": fps,
            "duration_sec": duration_sec,
            "tasks_detected": tasks,
            "ergonomic_summary": {
                "avg_reba_score": round(avg_reba, 2),
                "max_reba_score": max_reba,
                "risk_level": risk_level,
                "high_risk_moments": sum(1 for s in reba_scores if s > 7),
                "recommendations": recommendations
            },
            "fatigue_analysis": {
                "fatigue_index": min(avg_reba / 15.0, 1.0),
                "estimated_fatigue_time_min": int(45 * (1 - avg_reba / 15.0)),
                "rest_recommendation": self._get_rest_recommendation(avg_reba)
            }
        }
    
    def _detect_tasks(self, motion_data: List[Dict], fps: int) -> List[Dict]:
        """Detect individual tasks from motion sequence"""
        tasks = []
        current_task = None
        
        for frame in motion_data:
            action = frame["action_type"]
            
            if current_task is None or current_task["action_type"] != action:
                # New task detected
                if current_task:
                    current_task["duration_ms"] = \
                        current_task["end_time_ms"] - current_task["start_time_ms"]
                    tasks.append(current_task)
                
                current_task = {
                    "task_id": f"auto_{len(tasks) + 1}",
                    "action_type": action,
                    "start_time_ms": frame["timestamp_ms"],
                    "end_time_ms": frame["timestamp_ms"],
                    "frames": [frame],
                    "reba_scores": [frame["reba_score"]]
                }
            else:
                # Continue current task
                current_task["end_time_ms"] = frame["timestamp_ms"]
                current_task["frames"].append(frame)
                current_task["reba_scores"].append(frame["reba_score"])
        
        # Add last task
        if current_task:
            current_task["duration_ms"] = \
                current_task["end_time_ms"] - current_task["start_time_ms"]
            tasks.append(current_task)
        
        # Calculate metrics for each task
        for task in tasks:
            task["avg_reba_score"] = int(np.mean(task["reba_scores"]))
            task["risk_level"] = self._get_risk_level(task["avg_reba_score"])
            # Remove raw frames to reduce size
            del task["frames"]
            del task["reba_scores"]
        
        return tasks
    
    def _get_risk_level(self, reba_score: int) -> str:
        """Map REBA score to risk level"""
        if reba_score <= 3:
            return "low"
        elif reba_score <= 7:
            return "medium"
        elif reba_score <= 10:
            return "high"
        else:
            return "very_high"
    
    def _generate_recommendations(
        self,
        tasks: List[Dict],
        avg_reba: float
    ) -> List[str]:
        """Generate ergonomic recommendations"""
        recommendations = []
        
        if avg_reba > 7:
            recommendations.append(
                "High ergonomic risk detected. Consider workstation redesign."
            )
        
        # Check for specific risky actions
        risky_tasks = [t for t in tasks if t["avg_reba_score"] > 7]
        if risky_tasks:
            for task in risky_tasks[:2]:  # Top 2
                recommendations.append(
                    f"Reduce strain during '{task['action_type']}' operation"
                )
        
        if avg_reba > 4:
            recommendations.append(
                "Improve workpiece positioning to reduce reaching and bending"
            )
        
        return recommendations
    
    def _get_rest_recommendation(self, avg_reba: float) -> str:
        """Generate rest break recommendation"""
        if avg_reba > 10:
            return "Immediate rest break recommended. Task unsustainable."
        elif avg_reba > 7:
            return "5-minute break recommended after 30 minutes"
        elif avg_reba > 4:
            return "5-minute break recommended after 45 minutes"
        else:
            return "Standard break schedule (60 minutes)"


# Example usage
def main():
    processor = SensorDataProcessor()
    
    result = processor.process_video(
        video_path="storage/sensor_data/videos/worker_001.mp4",
        output_path="storage/sensor_data/processed/worker_001_annotated.mp4"
    )
    
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
```

#### Step 2: Add API Endpoints for Sensor Data

Add to `src/api_server.py`:

```python
from services.sensor_processor import SensorDataProcessor
from fastapi import UploadFile, File
import shutil
import os

sensor_processor = SensorDataProcessor()

@app.post("/upload-sensor-data")
async def upload_sensor_data(
    video_file: UploadFile = File(...),
    worker_id: str = Form(...),
    session_id: str = Form(...),
    metadata: str = Form("{}")
):
    """Upload and process sensor video"""
    upload_id = f"upload_{uuid.uuid4().hex[:8]}"
    
    # Save video file
    video_dir = "storage/sensor_data/videos"
    os.makedirs(video_dir, exist_ok=True)
    video_path = os.path.join(video_dir, f"{upload_id}.mp4")
    
    with open(video_path, "wb") as buffer:
        shutil.copyfileobj(video_file.file, buffer)
    
    # Process asynchronously (in production, use task queue like Celery)
    annotated_path = video_path.replace("videos", "processed").replace(".mp4", "_annotated.mp4")
    
    try:
        result = sensor_processor.process_video(
            video_path=video_path,
            output_path=annotated_path
        )
        
        # Save to database
        # ... (database code here)
        
        return {
            "upload_id": upload_id,
            "worker_id": worker_id,
            "session_id": session_id,
            "status": "completed",
            **result
        }
    except Exception as e:
        return {
            "upload_id": upload_id,
            "status": "failed",
            "error": str(e)
        }
```

---

### 3. 3D Model Management

Create `src/models/model_library.py`:

```python
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Model3D(Base):
    """3D model library table"""
    __tablename__ = "model_library"
    
    id = Column(Integer, primary_key=True)
    model_name = Column(String(200), nullable=False, index=True)
    usd_path = Column(Text, nullable=False)
    category = Column(String(50), index=True)  # workstation, product, tool, conveyor
    dimensions = Column(JSON)  # {width, depth, height}
    thumbnail_url = Column(Text)
    metadata = Column(JSON)  # Additional properties
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

Add API endpoints:

```python
@app.get("/3d-models")
async def get_3d_models(
    category: Optional[str] = None,
    search: Optional[str] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List 3D models"""
    query = db.query(Model3D)
    
    if category:
        query = query.filter(Model3D.category == category)
    if search:
        query = query.filter(Model3D.model_name.ilike(f"%{search}%"))
    
    models = query.limit(limit).all()
    
    return {
        "models": [model_to_dict(m) for m in models],
        "total_count": query.count()
    }
```

---

### 4. Version Control System

Already covered in architecture document. Implement `src/services/version_manager.py` as shown in Phase 3 Architecture.

---

### 5. Collision Detection

Already covered in architecture document. Implement `src/services/collision_detector.py` as shown in Phase 3 Architecture.

---

### 6. Omniverse Integration

Create `src/services/omniverse_connector.py` as shown in Phase 3 Architecture document.

---

### 7. Multi-Site Sharing

Add to `src/api_server.py`:

```python
@app.post("/share-configuration")
async def share_configuration(
    request: ShareConfiguration,
    db: Session = Depends(get_db)
):
    """Share configuration to another site"""
    success = version_manager.share_to_site(
        version_hash=request.version_hash,
        target_site=request.target_site,
        shared_by=request.shared_by
    )
    
    if success:
        return {
            "share_id": f"share_{uuid.uuid4().hex[:8]}",
            "version_hash": request.version_hash,
            "target_site": request.target_site,
            "status": "shared",
            "shared_at": datetime.utcnow().isoformat()
        }
    else:
        raise HTTPException(status_code=404, detail="Version not found")
```

---

## Database Setup

Run migrations:

```bash
# Create migration for Phase 3 tables
alembic revision --autogenerate -m "Add Phase 3 tables"

# Apply migration
alembic upgrade head
```

---

## Testing

Create comprehensive tests:

```bash
# Test NLP service
pytest tests/test_nlp_service.py -v

# Test sensor processing
pytest tests/test_sensor_processor.py -v

# Test collision detection
pytest tests/test_collision_detector.py -v

# Integration tests
pytest tests/test_phase3_integration.py -v
```

---

## Deployment

### Docker Deployment

Update `Dockerfile`:

```dockerfile
FROM nvidia/cuda:12.1.0-cudnn8-runtime-ubuntu22.04

# Install Python and system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    ffmpeg \
    libsm6 \
    libxext6 \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt /app/
RUN pip3 install -r /app/requirements.txt

# Copy application
COPY src/ /app/src/
WORKDIR /app

# Expose ports
EXPOSE 8000

CMD ["uvicorn", "src.api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

Update `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/line_balance
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./storage:/app/storage
    depends_on:
      - db
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=line_balance
    volumes:
      - postgres_data:/var/lib/postgresql/data
  
  omniverse:
    image: nvcr.io/nvidia/omniverse/nucleus-server:latest
    ports:
      - "3180:3180"
      - "3181:3181"
    volumes:
      - nucleus_data:/var/lib/omni/nucleus

volumes:
  postgres_data:
  nucleus_data:
```

---

## Performance Tuning

### 1. LLM Query Caching

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def process_cached_query(query: str):
    return nlp_service.process_query(query)
```

### 2. Sensor Processing Optimization

```python
# Use GPU acceleration
import torch

if torch.cuda.is_available():
    device = torch.device("cuda")
else:
    device = torch.device("cpu")
```

### 3. Database Indexing

```sql
CREATE INDEX idx_sensor_worker_timestamp ON sensor_data(worker_id, timestamp);
CREATE INDEX idx_versions_type_site ON versions(config_type, site);
CREATE INDEX idx_nlp_intent ON nlp_query_log(intent);
```

---

**Document Maintainer:** JASON YY, LIN  
**Last Updated:** 2025-11-13
**Version:** 3.0.0-phase3
