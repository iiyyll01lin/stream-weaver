# Phase 3 Architecture Design

**Document Version**: 2.0 | **Last Updated**: 2025-12-12  
**Related Documents**:
- [Phase 3 Implementation Guide](PHASE3_IMPLEMENTATION_EN.md)
- [Phase 3 API Specification](PHASE3_API_SPEC_EN.md)
- [Phase 2 Architecture](PHASE2_ARCHITECTURE_EN.md)
- [Database & API Design](DATABASE_API_DESIGN_SPEC_EN.md)
- [Requirements Coverage Analysis](REQUIREMENTS_COVERAGE_ANALYSIS.md)
- [REQ Gap Remediation](REQ_GAP_REMEDIATION.md)

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [System Components](#system-components)
- [3D Simulation Architecture](#3d-simulation-architecture)
- [Natural Language Query Architecture](#natural-language-query-architecture)
- [Body Sensor Data Processing](#body-sensor-data-processing)
- [Version Management & Multi-Site Sharing](#version-management--multi-site-sharing)
- [Collision Detection System](#collision-detection-system)
- [Multilingual Support (REQ #37)](#multilingual-support-new)
- [Interactive 3D (REQ #38)](#interactive-3d-new)
- [Live Monitoring & Alerts (REQ #39)](#live-monitoring--alerts-new)
- [APS Integration (REQ #40)](#aps-integration-new)
- [Automatic WI Generation (REQ #52)](#automatic-wi-generation-new)
- [Technology Stack](#technology-stack)
- [Data Flow](#data-flow)
- [Database Schema](#database-schema)
- [Performance Optimization](#performance-optimization)

---

## Architecture Overview

### Design Principles

Phase 3 extends the four-tier architecture with advanced AI/ML and 3D capabilities:

1. **Presentation Layer** (Frontend)
   - Technology: React + Three.js + **NVIDIA Omniverse Kit**
   - Components: 3D Viewer, NLP Query Interface, Sensor Dashboard
   - Responsibility: Advanced 3D visualization, interactive simulation

2. **Service Layer** (Backend API)
   - Technology: FastAPI + **LangChain** + **PostgreSQL** + **JWT Auth**
   - Components: NLP Engine, Version Control, Collision Detector, Database Management
   - Responsibility: AI orchestration, data versioning, physics simulation

3. **Data Layer** (Advanced Persistence)
   - Technology: PostgreSQL + **Sensor Data Tables** + **3D Model Catalog** + Redis Cache
   - Components: Motion capture storage, NLP query history, 3D model metadata, version control
   - Responsibility: Complex AI data relationships, sensor data storage, multi-modal data management

4. **AI/ML Layer** (Intelligence Engine)
   - Technology: **OpenAI GPT-4** + **PyTorch** + **MediaPipe**
   - Components: LLM Query Engine, Sensor Data Processor, Motion Analyzer
   - Responsibility: Natural language understanding, motion capture processing

5. **3D Simulation Layer** (Rendering Engine)
   - Technology: **NVIDIA Omniverse** + **USD (Universal Scene Description)**
   - Components: 3D Asset Library, Physics Engine, Collaboration Platform
   - Responsibility: Photorealistic rendering, real-time simulation, multi-user collaboration

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         Frontend Layer (Phase 3)                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  React Application                                            │  │
│  │  ┌────────────────┬────────────────┬────────────────────────┐ │  │
│  │  │ 3D Viewer      │ NLP Interface  │ Sensor Dashboard       │ │  │
│  │  │ (Three.js)     │ (Voice/Text)   │ (Motion Analytics)     │ │  │
│  │  │ - 3D Preview   │ - Query Input  │ - Body Tracking       │ │  │
│  │  │ - Orbit Control│ - Auto-complete│ - Ergonomic Analysis  │ │  │
│  │  │ - Collision    │ - Suggestions  │ - Fatigue Prediction  │ │  │
│  │  └────────────────┴────────────────┴────────────────────────┘ │  │
│  │                                                                 │  │
│  │  ┌───────────────────────────────────────────────────────────┐ │  │
│  │  │ Omniverse Connector (USD Viewport)                        │ │  │
│  │  │ - Real-time 3D Simulation                                 │ │  │
│  │  │ - Multi-user Collaboration                                │ │  │
│  │  │ - Physics-based Animation                                 │ │  │
│  │  └───────────────────────────────────────────────────────────┘ │  │
│  └───────────────────────────────────────────────────────────────┘  │
└──────────────────────┬──────────────────────────────────────────────┘
                       │ WebSocket + REST API (HTTPS + JWT)
                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Backend API Layer (Phase 3)                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  api_server.py (Extended FastAPI Application)                │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │  Phase 3 NEW Endpoints                                  │  │  │
│  │  │  - POST /api/v3/nlp-query          (Natural Language)   │  │  │
│  │  │  - GET  /api/v3/3d-models          (3D Asset Management)│  │  │
│  │  │  - POST /api/v3/sensor-data        (Body Sensor Data)   │  │  │
│  │  │  - GET  /api/v3/versions           (Version Management) │  │  │
│  │  │  - POST /api/v3/check-collision    (Interference Check) │  │  │
│  │  │  - GET  /api/v3/omniverse-session  (3D Simulation)      │  │  │
│  │  │  - POST /api/v3/share-config       (Cross-Site Sharing) │  │  │
│  │  └─────────────────┬───────────────────────────────────────┘  │  │
│  │                    │                                           │  │
│  │  ┌─────────────────▼───────────────────────────────────────┐  │  │
│  │  │  Service Modules (NEW)                                  │  │  │
│  │  │  - nlp_service.py         (LangChain + GPT-4)           │  │  │
│  │  │  - sensor_processor.py    (Motion data analysis)        │  │  │
│  │  │  - version_manager.py     (Git-like versioning)         │  │  │
│  │  │  - collision_detector.py  (Physics collision check)     │  │  │
│  │  │  - omniverse_connector.py (USD scene management)        │  │  │
│  │  │  - database_manager.py    (ORM & data persistence)      │  │  │
│  │  └─────────────────┬───────────────────────────────────────┘  │  │
│  └────────────────────┼───────────────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────────────┘
                         │ SQL queries + AI/ML API calls
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    Data Layer (Phase 3 Enhanced)                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  PostgreSQL Database (Extended Schema)                        │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │  Phase 3 Advanced Tables                                │  │  │
│  │  │  - sensor_sessions (video uploads, worker tracking)     │  │  │
│  │  │  - motion_captures (pose landmarks, REBA scores)        │  │  │
│  │  │  - ergonomic_analyses (efficiency, fatigue prediction)  │  │  │
│  │  │  - nlp_queries (query history, intent classification)   │  │  │
│  │  │  - model_3d_catalog (USD files, 3D asset metadata)     │  │  │
│  │  │  - configurations (git-like version control)           │  │  │
│  │  │  - config_snapshots (rollback capability)              │  │  │
│  │  │  + All Phase 1 & 2 tables (inherited and extended)     │  │  │
│  │  └─────────────────┬───────────────────────────────────────┘  │  │
│  │                    │                                           │  │
│  │  ┌─────────────────▼───────────────────────────────────────┐  │  │
│  │  │  Redis Cache (Phase 3 Enhanced)                        │  │  │
│  │  │  - NLP query responses (5min TTL)                       │  │  │
│  │  │  - 3D model metadata (1 week TTL)                      │  │  │
│  │  │  - Sensor analysis results (1 day TTL)                 │  │  │
│  │  │  - Version control snapshots (1 hour TTL)              │  │  │
│  │  │  - Collision detection cache (24 hour TTL)             │  │  │
│  │  └─────────────────┬───────────────────────────────────────┘  │  │
│  └────────────────────┼───────────────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────────────┘
                         │ AI/ML model execution + 3D rendering
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      AI/ML Layer (Phase 3)                           │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  NLP Engine (LangChain + OpenAI GPT-4)                        │  │
│  │  - Intent Recognition: "Show me the bottleneck station"       │  │
│  │  - Entity Extraction: Work order, SKU, station numbers       │  │
│  │  - Query Translation: Natural Language → SQL/API calls       │  │
│  │  - Response Generation: Data results → Natural language      │  │
│  └───────────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Sensor Data Processor (PyTorch + MediaPipe)                  │  │
│  │  - Pose Estimation: 33-point body landmark detection         │  │
│  │  - Motion Classification: Install/Mount/Screw/Test           │  │
│  │  - Motion Efficiency Analysis: Expert vs. Novice comparison  │  │
│  │  - REBA Score Calculation: Ergonomic risk assessment         │  │
│  │  - Fatigue Prediction: Movement pattern analysis             │  │
│  │  - Training Recommendations: Personalized improvement        │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   3D Simulation Layer (Phase 3)                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  NVIDIA Omniverse Platform                                    │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │  USD Scene Graph (from Database)                        │  │  │
│  │  │  - Workstation 3D Models (.usd files)                   │  │  │
│  │  │  - Product Assembly Models (.usd files)                 │  │  │
│  │  │  - Worker Digital Twins (.usd files)                    │  │  │
│  │  │  - Layout Configurations (spatial positioning)          │  │  │
│  │  └─────────────────┬───────────────────────────────────────┘  │  │
│  │                    │                                           │  │
│  │  ┌─────────────────▼───────────────────────────────────────┐  │  │
│  │  │  PhysX Physics Engine (Database-driven)                │  │  │
│  │  │  - Collision Detection (cached in Redis)                │  │  │
│  │  │  - Reach Analysis (from sensor data)                    │  │  │
│  │  │  - Space Optimization (layout validation)               │  │  │
│  │  └─────────────────┬───────────────────────────────────────┘  │  │
│  │                    │                                           │  │
│  │  ┌─────────────────▼───────────────────────────────────────┐  │  │
│  │  │  Nucleus Collaboration Server (Multi-tenant)           │  │  │
│  │  │  - Multi-user simultaneous editing                      │  │  │
│  │  │  - Real-time synchronization                            │  │  │
│  │  │  - Version control (database-backed)                    │  │  │
│  │  │  - Cross-site configuration sharing                     │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Sensor Data Processor (PyTorch + MediaPipe)                  │  │
│  │  - Pose Estimation: 33-point body landmark detection         │  │
│  │  - Motion Classification: Install/Mount/Screw/Test           │  │
│  │  - Motion Efficiency Analysis: Expert vs. Novice comparison  │  │
│  │    * Hand coordination ratio (parallel vs. sequential work)  │  │
│  │    * Motion smoothness (velocity jerk analysis)              │  │
│  │    * Path efficiency (trajectory optimization)               │  │
│  │    * Unnecessary reach detection (wasted movements)          │  │
│  │    * Trunk angle stability (balance assessment)              │  │
│  │    * Arm extension ratio (reach optimization)                │  │
│  │    * Overall efficiency score (0-100%)                       │  │
│  │  - Expert Baseline Management: Store reference patterns      │  │
│  │  - Efficiency Gap Analysis: Identify improvement areas       │  │
│  │  - Training Recommendations: Personalized improvement tips   │  │
│  │  - Time Study: Automated task duration measurement           │  │
│  │  - Ergonomic Analysis: REBA score (safety) + efficiency      │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                   3D Simulation Layer (Phase 3)                      │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  NVIDIA Omniverse Platform                                    │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │  USD Scene Graph                                        │  │  │
│  │  │  - Workstation 3D Models (.usd)                         │  │  │
│  │  │  - Product Assembly Models (.usd)                       │  │  │
│  │  │  - Worker Digital Twins (.usd)                          │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │  PhysX Physics Engine                                   │  │  │
│  │  │  - Collision Detection (AABB, OBB, Mesh)                │  │  │
│  │  │  - Reach Analysis (Worker ergonomics)                   │  │  │
│  │  │  - Space Optimization (Layout verification)             │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │  Nucleus Collaboration Server                           │  │  │
│  │  │  - Multi-user simultaneous editing                      │  │  │
│  │  │  - Real-time synchronization                            │  │  │
│  │  │  - Version control (Git-like)                           │  │  │
│  │  └─────────────────────────────────────────────────────────┘  │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     Database Layer (Phase 3)                         │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  PostgreSQL (Extended Schema)                                 │  │
│  │  Tables:                                                      │  │
│  │  - sensor_data (id, worker_id, motion_json, timestamp)       │  │
│  │  - model_library (id, model_name, usd_path, category)        │  │
│  │  - versions (id, config_id, version_hash, author, site)      │  │
│  │  - collaboration_sessions (id, users, scene_url, status)     │  │
│  │  - collision_cache (id, layout_id, collision_pairs)          │  │
│  │  - nlp_query_log (id, query_text, intent, api_calls)         │  │
│  └───────────────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  Vector Database (Pinecone/Milvus)                            │  │
│  │  - NLP Query Embeddings (for semantic search)                │  │
│  │  - 3D Model Metadata (for similarity search)                 │  │
│  └───────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## System Components

### 1. Frontend Component (React + Omniverse)

**Phase 3 Additions**:

#### 1.1 3D Viewer Component
```jsx
import { Canvas } from '@react-three/fiber';
import { OrbitControls, useGLTF } from '@react-three/drei';

function WorkstationViewer({ modelUrl, highlightCollisions }) {
  const { scene } = useGLTF(modelUrl);
  
  return (
    <Canvas camera={{ position: [5, 5, 5] }}>
      <ambientLight intensity={0.5} />
      <spotLight position={[10, 10, 10]} />
      <primitive object={scene} />
      <OrbitControls />
      {highlightCollisions && <CollisionMarkers />}
    </Canvas>
  );
}
```

#### 1.2 Natural Language Query Interface
```jsx
function NLPQueryPanel() {
  const [query, setQuery] = useState('');
  const [result, setResult] = useState(null);
  
  const handleQuery = async () => {
    const response = await fetch('/nlp-query', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ query })
    });
    const data = await response.json();
    setResult(data);
  };
  
  return (
    <div className="nlp-panel">
      <input 
        type="text"
        placeholder="Ask me anything... e.g., 'Which station is the bottleneck?'"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
      />
      <button onClick={handleQuery}>Ask</button>
      {result && <ResultDisplay data={result} />}
    </div>
  );
}
```

#### 1.3 Body Sensor Dashboard
```jsx
function SensorDashboard({ workerId }) {
  const [motionData, setMotionData] = useState([]);
  
  useEffect(() => {
    // WebSocket connection for real-time sensor data
    const ws = new WebSocket('ws://localhost:8000/sensor-stream');
    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      setMotionData(prev => [...prev, data]);
    };
    return () => ws.close();
  }, []);
  
  return (
    <div className="sensor-dashboard">
      <MotionTimeline data={motionData} />
      <ErgonomicScore rebaScore={calculateREBA(motionData)} />
      <FatigueIndicator level={analyzeFatigue(motionData)} />
    </div>
  );
}
```

**Technology Choices**:

| Technology         | Purpose          | Reason for Selection                               |
|--------------------|------------------|----------------------------------------------------|
| React 18           | UI Framework     | Component reusability, hooks, concurrent rendering |
| Three.js           | 3D Rendering     | WebGL abstraction, extensive ecosystem             |
| @react-three/fiber | React + Three.js | Declarative 3D scenes, React integration           |
| Omniverse Kit      | High-fidelity 3D | NVIDIA RTX rendering, physics simulation           |
| WebSocket          | Real-time data   | Bi-directional streaming for sensor data           |

---

### 2. Backend API Component (Extended `api_server.py`)

**Phase 3 Additions**:

#### 2.1 Natural Language Processing Service
```python
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class NLPService:
    """Natural language query service"""
    
    def __init__(self):
        self.llm = ChatOpenAI(model="gpt-4", temperature=0)
        self.intent_classifier = self._build_intent_classifier()
        
    def _build_intent_classifier(self):
        """Build intent recognition chain"""
        template = """
        Classify the following user query into one of these intents:
        - query_bottleneck: Ask about bottleneck stations
        - query_utilization: Ask about station utilization
        - optimize_layout: Request layout optimization
        - show_3d_model: Request 3D visualization
        - analyze_sensor: Request sensor data analysis
        
        User query: {query}
        Intent:
        """
        prompt = PromptTemplate(template=template, input_variables=["query"])
        return LLMChain(llm=self.llm, prompt=prompt)
    
    async def process_query(self, query: str) -> Dict[str, Any]:
        """Process natural language query"""
        # 1. Intent recognition
        intent = await self.intent_classifier.arun(query=query)
        
        # 2. Entity extraction
        entities = self._extract_entities(query)
        
        # 3. Generate API call
        api_call = self._intent_to_api(intent, entities)
        
        # 4. Execute API
        result = await self._execute_api_call(api_call)
        
        # 5. Generate natural language response
        response = await self._generate_response(query, result)
        
        return {
            "intent": intent,
            "entities": entities,
            "api_call": api_call,
            "result": result,
            "response": response
        }
    
    def _extract_entities(self, query: str) -> Dict[str, Any]:
        """Extract entities (work order, station, etc.)"""
        # Use NER or regex patterns
        entities = {}
        if "WO_" in query:
            entities["work_order"] = re.search(r'WO_[A-Z]', query).group()
        if "station" in query.lower():
            entities["station"] = re.search(r'\d+', query).group()
        return entities
    
    def _intent_to_api(self, intent: str, entities: Dict) -> Dict[str, Any]:
        """Map intent to API endpoint"""
        intent_mapping = {
            "query_bottleneck": {
                "endpoint": "/workstations",
                "params": {"work_order_id": entities.get("work_order", "WO_A")}
            },
            "optimize_layout": {
                "endpoint": "/optimize",
                "params": {"work_order_id": entities.get("work_order", "WO_A")}
            }
            # ... more mappings
        }
        return intent_mapping.get(intent, {})
```

#### 2.2 Body Sensor Data Processor
```python
import cv2
import mediapipe as mp
import numpy as np
from typing import List, Dict

class SensorDataProcessor:
    """Process body sensor motion capture data"""
    
    def __init__(self):
        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(
            static_image_mode=False,
            model_complexity=2,
            enable_segmentation=False
        )
        
    def process_video(self, video_path: str) -> List[Dict]:
        """Extract motion data from video"""
        cap = cv2.VideoCapture(video_path)
        motion_data = []
        
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # Process frame
            results = self.pose.process(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            
            if results.pose_landmarks:
                # Extract 33 body landmarks
                landmarks = self._extract_landmarks(results.pose_landmarks)
                
                # Classify motion
                action_type = self._classify_action(landmarks)
                
                # Calculate ergonomic score
                reba_score = self._calculate_reba(landmarks)
                
                motion_data.append({
                    "timestamp": cap.get(cv2.CAP_PROP_POS_MSEC),
                    "landmarks": landmarks,
                    "action_type": action_type,
                    "reba_score": reba_score
                })
        
        cap.release()
        return motion_data
    
    def _extract_landmarks(self, pose_landmarks) -> Dict[str, List[float]]:
        """Extract landmark coordinates"""
        landmarks = {}
        for idx, landmark in enumerate(pose_landmarks.landmark):
            landmarks[f"point_{idx}"] = [
                landmark.x,
                landmark.y,
                landmark.z,
                landmark.visibility
            ]
        return landmarks
    
    def _classify_action(self, landmarks: Dict) -> str:
        """Classify assembly action from pose"""
        # Rule-based classification
        shoulder_angle = self._calculate_angle(
            landmarks["point_11"],  # Left shoulder
            landmarks["point_13"],  # Left elbow
            landmarks["point_15"]   # Left wrist
        )
        
        if shoulder_angle > 160:
            return "reaching"
        elif shoulder_angle < 90:
            return "installing"
        elif self._is_screwing_motion(landmarks):
            return "screwing"
        else:
            return "positioning"
    
    def _calculate_reba(self, landmarks: Dict) -> int:
        """Calculate REBA ergonomic score (1-15)"""
        # Simplified REBA calculation
        neck_score = self._assess_neck(landmarks)
        trunk_score = self._assess_trunk(landmarks)
        leg_score = self._assess_legs(landmarks)
        arm_score = self._assess_arms(landmarks)
        
        # REBA formula (simplified)
        score_a = neck_score + trunk_score + leg_score
        score_b = arm_score
        total_score = self._reba_lookup(score_a, score_b)
        
        return total_score
    
    def generate_time_study(self, motion_data: List[Dict]) -> Dict[str, Any]:
        """Generate automated time study from sensor data"""
        tasks = []
        current_task = None
        
        for frame in motion_data:
            action = frame["action_type"]
            
            if current_task is None or current_task["action_type"] != action:
                # New task detected
                if current_task:
                    tasks.append(current_task)
                
                current_task = {
                    "action_type": action,
                    "start_time": frame["timestamp"],
                    "end_time": frame["timestamp"],
                    "avg_reba": frame["reba_score"]
                }
            else:
                # Continue current task
                current_task["end_time"] = frame["timestamp"]
        
        # Add last task
        if current_task:
            tasks.append(current_task)
        
        # Calculate durations
        for task in tasks:
            task["duration_ms"] = task["end_time"] - task["start_time"]
        
        return {
            "tasks": tasks,
            "total_time": sum(t["duration_ms"] for t in tasks),
            "avg_reba_score": np.mean([t["avg_reba"] for t in tasks])
        }
```

#### 2.3 Version Management Service
```python
import hashlib
import json
from datetime import datetime
from typing import List, Dict, Optional

class VersionManager:
    """Git-like version control for configurations"""
    
    def __init__(self, db_session):
        self.db = db_session
    
    def create_version(
        self,
        config_type: str,  # "layout", "optimization", "product_config"
        config_data: Dict,
        author: str,
        site: str,
        message: str
    ) -> str:
        """Create new configuration version"""
        # Calculate hash
        config_json = json.dumps(config_data, sort_keys=True)
        version_hash = hashlib.sha256(config_json.encode()).hexdigest()[:8]
        
        # Check if version exists
        existing = self.db.query(Version).filter_by(
            version_hash=version_hash
        ).first()
        
        if existing:
            return existing.version_hash
        
        # Create new version
        version = Version(
            config_type=config_type,
            config_data=config_data,
            version_hash=version_hash,
            author=author,
            site=site,
            message=message,
            created_at=datetime.utcnow()
        )
        
        self.db.add(version)
        self.db.commit()
        
        return version_hash
    
    def get_version(self, version_hash: str) -> Optional[Dict]:
        """Retrieve specific version"""
        version = self.db.query(Version).filter_by(
            version_hash=version_hash
        ).first()
        
        if not version:
            return None
        
        return {
            "version_hash": version.version_hash,
            "config_type": version.config_type,
            "config_data": version.config_data,
            "author": version.author,
            "site": version.site,
            "message": version.message,
            "created_at": version.created_at.isoformat()
        }
    
    def list_versions(
        self,
        config_type: Optional[str] = None,
        site: Optional[str] = None,
        limit: int = 50
    ) -> List[Dict]:
        """List configuration versions"""
        query = self.db.query(Version)
        
        if config_type:
            query = query.filter_by(config_type=config_type)
        if site:
            query = query.filter_by(site=site)
        
        versions = query.order_by(Version.created_at.desc()).limit(limit).all()
        
        return [
            {
                "version_hash": v.version_hash,
                "config_type": v.config_type,
                "author": v.author,
                "site": v.site,
                "message": v.message,
                "created_at": v.created_at.isoformat()
            }
            for v in versions
        ]
    
    def share_to_site(
        self,
        version_hash: str,
        target_site: str,
        shared_by: str
    ) -> bool:
        """Share configuration to another site"""
        version = self.get_version(version_hash)
        if not version:
            return False
        
        # Create copy for target site
        new_hash = self.create_version(
            config_type=version["config_type"],
            config_data=version["config_data"],
            author=shared_by,
            site=target_site,
            message=f"Shared from {version['site']} by {shared_by}"
        )
        
        return True
    
    def diff_versions(
        self,
        version_hash_a: str,
        version_hash_b: str
    ) -> Dict[str, Any]:
        """Compare two versions"""
        version_a = self.get_version(version_hash_a)
        version_b = self.get_version(version_hash_b)
        
        if not version_a or not version_b:
            return {"error": "Version not found"}
        
        # Deep diff
        diff = self._deep_diff(
            version_a["config_data"],
            version_b["config_data"]
        )
        
        return {
            "version_a": version_hash_a,
            "version_b": version_hash_b,
            "changes": diff
        }
    
    def _deep_diff(self, obj1: Dict, obj2: Dict) -> Dict:
        """Calculate deep difference between two dicts"""
        diff = {
            "added": {},
            "removed": {},
            "modified": {}
        }
        
        all_keys = set(obj1.keys()) | set(obj2.keys())
        
        for key in all_keys:
            if key not in obj1:
                diff["added"][key] = obj2[key]
            elif key not in obj2:
                diff["removed"][key] = obj1[key]
            elif obj1[key] != obj2[key]:
                diff["modified"][key] = {
                    "old": obj1[key],
                    "new": obj2[key]
                }
        
        return diff
```

#### 2.4 Collision Detection Service
```python
import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass

@dataclass
class BoundingBox:
    """3D Axis-Aligned Bounding Box"""
    min_x: float
    min_y: float
    min_z: float
    max_x: float
    max_y: float
    max_z: float
    object_id: str

class CollisionDetector:
    """3D collision detection for layout interference checking"""
    
    def __init__(self):
        self.collision_cache = {}
    
    def check_layout_collision(
        self,
        layout_data: Dict,
        clearance: float = 0.5  # meters
    ) -> List[Dict]:
        """Check for collisions in 2D/3D layout"""
        # Extract bounding boxes from layout
        bboxes = self._extract_bounding_boxes(layout_data)
        
        # Check all pairs
        collisions = []
        for i, bbox1 in enumerate(bboxes):
            for bbox2 in bboxes[i+1:]:
                if self._aabb_intersect(bbox1, bbox2, clearance):
                    collisions.append({
                        "object_a": bbox1.object_id,
                        "object_b": bbox2.object_id,
                        "type": "space_conflict",
                        "clearance_violation": self._calculate_overlap(bbox1, bbox2)
                    })
        
        return collisions
    
    def _extract_bounding_boxes(self, layout_data: Dict) -> List[BoundingBox]:
        """Extract bounding boxes from layout stations"""
        bboxes = []
        
        for station in layout_data.get("stations", []):
            pos = station.get("position", {})
            dimensions = station.get("dimensions", {})
            
            bbox = BoundingBox(
                min_x=pos.get("x", 0),
                min_y=pos.get("y", 0),
                min_z=pos.get("z", 0),
                max_x=pos.get("x", 0) + dimensions.get("width", 1),
                max_y=pos.get("y", 0) + dimensions.get("depth", 1),
                max_z=pos.get("z", 0) + dimensions.get("height", 2),
                object_id=station.get("station_id", "unknown")
            )
            bboxes.append(bbox)
        
        return bboxes
    
    def _aabb_intersect(
        self,
        box1: BoundingBox,
        box2: BoundingBox,
        clearance: float
    ) -> bool:
        """Check if two AABBs intersect (with clearance)"""
        return (
            box1.min_x - clearance < box2.max_x and
            box1.max_x + clearance > box2.min_x and
            box1.min_y - clearance < box2.max_y and
            box1.max_y + clearance > box2.min_y and
            box1.min_z - clearance < box2.max_z and
            box1.max_z + clearance > box2.min_z
        )
    
    def _calculate_overlap(
        self,
        box1: BoundingBox,
        box2: BoundingBox
    ) -> float:
        """Calculate overlap volume"""
        overlap_x = max(0, min(box1.max_x, box2.max_x) - max(box1.min_x, box2.min_x))
        overlap_y = max(0, min(box1.max_y, box2.max_y) - max(box1.min_y, box2.min_y))
        overlap_z = max(0, min(box1.max_z, box2.max_z) - max(box1.min_z, box2.min_z))
        
        return overlap_x * overlap_y * overlap_z
    
    def check_worker_reach(
        self,
        worker_position: Dict,
        workpiece_position: Dict,
        max_reach: float = 0.8  # meters
    ) -> bool:
        """Check if worker can reach workpiece"""
        distance = np.sqrt(
            (worker_position["x"] - workpiece_position["x"]) ** 2 +
            (worker_position["y"] - workpiece_position["y"]) ** 2 +
            (worker_position["z"] - workpiece_position["z"]) ** 2
        )
        
        return distance <= max_reach
    
    def suggest_layout_improvement(
        self,
        layout_data: Dict,
        collisions: List[Dict]
    ) -> List[Dict]:
        """Suggest layout modifications to resolve collisions"""
        suggestions = []
        
        for collision in collisions:
            obj_a = collision["object_a"]
            obj_b = collision["object_b"]
            
            # Find stations
            station_a = next(
                (s for s in layout_data["stations"] if s["station_id"] == obj_a),
                None
            )
            station_b = next(
                (s for s in layout_data["stations"] if s["station_id"] == obj_b),
                None
            )
            
            if station_a and station_b:
                # Calculate required separation
                required_distance = self._calculate_safe_distance(
                    station_a, station_b
                )
                
                suggestions.append({
                    "type": "move_station",
                    "station_id": obj_b,
                    "current_position": station_b["position"],
                    "suggested_position": self._calculate_new_position(
                        station_a["position"],
                        station_b["position"],
                        required_distance
                    ),
                    "reason": f"Collision with {obj_a}"
                })
        
        return suggestions
```

#### 2.5 Omniverse Connector
```python
from pxr import Usd, UsdGeom, Gf
import omni.client
from typing import Dict, List

class OmniverseConnector:
    """NVIDIA Omniverse USD scene management"""
    
    def __init__(self, nucleus_server: str):
        self.nucleus_server = nucleus_server
        omni.client.initialize()
    
    def create_scene(
        self,
        work_order_id: str,
        layout_data: Dict,
        optimization_result: Dict
    ) -> str:
        """Create USD scene from optimization result"""
        # Create stage
        scene_path = f"{self.nucleus_server}/scenes/{work_order_id}.usd"
        stage = Usd.Stage.CreateNew(scene_path)
        
        # Set up scene
        UsdGeom.SetStageUpAxis(stage, UsdGeom.Tokens.z)
        UsdGeom.SetStageMetersPerUnit(stage, 1.0)
        
        # Create workstations
        for station in optimization_result["stations"]:
            self._create_workstation(
                stage,
                station,
                layout_data.get("stations", [])[station["station_index"]]
            )
        
        # Create conveyor/material flow
        self._create_material_flow(stage, layout_data)
        
        # Save stage
        stage.Save()
        
        return scene_path
    
    def _create_workstation(
        self,
        stage: Usd.Stage,
        station_data: Dict,
        layout_position: Dict
    ):
        """Create workstation in USD"""
        station_id = f"station_{station_data['station_index']}"
        xform = UsdGeom.Xform.Define(stage, f"/World/{station_id}")
        
        # Set position
        pos = layout_position.get("position", {"x": 0, "y": 0, "z": 0})
        xform.AddTranslateOp().Set(Gf.Vec3d(pos["x"], pos["y"], pos["z"]))
        
        # Create geometry (simple box for now)
        cube = UsdGeom.Cube.Define(stage, f"/World/{station_id}/geometry")
        dimensions = layout_position.get("dimensions", {"width": 1, "depth": 1, "height": 1})
        cube.GetSizeAttr().Set(1.0)
        cube.AddScaleOp().Set(Gf.Vec3f(
            dimensions["width"],
            dimensions["depth"],
            dimensions["height"]
        ))
        
        # Add metadata
        xform.GetPrim().SetMetadata("station_index", station_data["station_index"])
        xform.GetPrim().SetMetadata("assigned_tasks", station_data["assigned_tasks"])
        xform.GetPrim().SetMetadata("load_ms", station_data["load_ms"])
    
    def start_collaboration_session(
        self,
        scene_path: str,
        users: List[str]
    ) -> str:
        """Start multi-user collaboration session"""
        # Create session checkpoint
        session_id = f"session_{datetime.utcnow().timestamp()}"
        checkpoint_path = f"{scene_path}.{session_id}"
        
        # Copy scene to checkpoint
        result = omni.client.copy(scene_path, checkpoint_path)
        
        if result != omni.client.Result.OK:
            raise Exception(f"Failed to create session: {result}")
        
        return session_id
    
    def live_sync_update(
        self,
        scene_path: str,
        layer_name: str,
        changes: Dict
    ):
        """Push live updates to Omniverse scene"""
        stage = Usd.Stage.Open(scene_path)
        
        # Apply changes
        for change in changes.get("modified", []):
            prim_path = change["prim_path"]
            prim = stage.GetPrimAtPath(prim_path)
            
            if prim:
                for attr_name, attr_value in change["attributes"].items():
                    attr = prim.GetAttribute(attr_name)
                    if attr:
                        attr.Set(attr_value)
        
        stage.Save()
```

---

## 3D Simulation Architecture

### USD Scene Structure

```
/World                          # Root
├── /Environment                # Lighting, background
│   ├── /DomeLight
│   └── /GroundPlane
├── /ProductionLine             # Main assembly line
│   ├── /Station_0              # Workstation 0
│   │   ├── /Geometry          # 3D model
│   │   ├── /Tasks             # Task visualizations
│   │   └── /Worker            # Worker digital twin
│   ├── /Station_1
│   └── ...
├── /MaterialFlow               # Conveyors, AGVs
│   ├── /Conveyor_Main
│   └── /AGV_01
└── /Products                   # Product assemblies
    ├── /DL360_Assembly
    └── /ML350_Assembly
```

### PhysX Integration

```python
# Enable physics simulation
from pxr import UsdPhysics

def setup_physics(stage: Usd.Stage):
    """Enable PhysX physics"""
    # Create physics scene
    scene = UsdPhysics.Scene.Define(stage, "/physicsScene")
    scene.CreateGravityDirectionAttr().Set(Gf.Vec3f(0, 0, -1))
    scene.CreateGravityMagnitudeAttr().Set(9.81)
    
    # Add collision groups
    collision_api = UsdPhysics.CollisionAPI.Apply(stage.GetPrimAtPath("/World/ProductionLine"))
```

---

## Natural Language Query Architecture

### Query Processing Pipeline

```
User Query: "Which station has the highest load in WO_A?"
    │
    ▼
┌─────────────────────────────┐
│ Intent Classification       │
│ → "query_station_load"      │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Entity Extraction           │
│ - work_order: "WO_A"        │
│ - metric: "load"            │
│ - aggregation: "max"        │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ API Call Generation         │
│ GET /workstations?          │
│   work_order_id=WO_A        │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Response Processing         │
│ Parse JSON, find max load   │
└─────────────┬───────────────┘
              │
              ▼
┌─────────────────────────────┐
│ Natural Language Generation │
│ "Station 3 has the highest  │
│  load of 28,500ms in WO_A"  │
└─────────────────────────────┘
```

### Supported Query Types

| Query Type           | Example                               | API Mapping                           |
|----------------------|---------------------------------------|---------------------------------------|
| Bottleneck Detection | "Show me the bottleneck"              | `GET /workstations` + max load filter |
| Utilization Analysis | "What's the average utilization?"     | `GET /takt-summary`                   |
| Layout Retrieval     | "Load the factory A layout"           | `GET /layout?site=factory_A`          |
| 3D Visualization     | "Show 3D model of station 5"          | `GET /3d-models?station_id=5`         |
| Sensor Analysis      | "What's the REBA score for worker 1?" | `GET /sensor-data?worker_id=1`        |
| Version Control      | "List all versions by John"           | `GET /versions?author=John`           |

---

## Body Sensor Data Processing

### Data Pipeline

```
Motion Capture Video/Stream
    │
    ▼
┌──────────────────────────┐
│ MediaPipe Pose Detection │
│ - 33 body landmarks      │
│ - 3D coordinates         │
│ - Visibility scores      │
└───────────┬──────────────┘
            │
            ▼
┌──────────────────────────┐
│ Motion Classification    │
│ - Install / Mount        │
│ - Screw / Test           │
│ - Reach / Position       │
└───────────┬──────────────┘
            │
            ├─────────────────────────────────────┐
            │                                     │
            ▼                                     ▼
┌──────────────────────────┐         ┌──────────────────────────┐
│ Ergonomic Analysis       │         │ Motion Efficiency        │
│ (Safety Assessment)      │         │ (Productivity Analysis)  │
│ - REBA score (1-15)      │         │ - Expert vs Novice       │
│ - Fatigue prediction     │         │ - Efficiency score (0-100)│
│ - Injury risk            │         │ - Gap identification     │
└───────────┬──────────────┘         │ - Training suggestions   │
            │                         └───────────┬──────────────┘
            │                                     │
            └─────────────────┬───────────────────┘
                              │
                              ▼
                  ┌──────────────────────────┐
                  │ Time Study Generation    │
                  │ - Task durations         │
                  │ - Efficiency metrics     │
                  │ - Improvement potential  │
                  │ - CSV export             │
                  └──────────────────────────┘
```

### Dual-Purpose Analysis System

Phase 3 body sensor processing serves two critical functions:

1. **Safety Assessment (REBA)**: Identify ergonomic risks and prevent injuries
2. **Productivity Optimization (Motion Efficiency)**: Compare workers to expert baseline and accelerate training

### REBA Score Calculation

```python
def calculate_reba_score(landmarks: Dict) -> int:
    """
    REBA (Rapid Entire Body Assessment)
    Score 1: Negligible risk
    Score 2-3: Low risk
    Score 4-7: Medium risk
    Score 8-10: High risk
    Score 11-15: Very high risk
    """
    # Step A: Neck, Trunk, Legs
    neck_score = assess_neck_posture(landmarks)      # 1-3
    trunk_score = assess_trunk_posture(landmarks)    # 1-5
    leg_score = assess_leg_posture(landmarks)        # 1-2
    
    score_a = reba_table_a[neck_score][trunk_score][leg_score]
    
    # Step B: Upper arms, Lower arms, Wrists
    upper_arm_score = assess_upper_arm(landmarks)    # 1-6
    lower_arm_score = assess_lower_arm(landmarks)    # 1-2
    wrist_score = assess_wrist(landmarks)            # 1-3
    
    score_b = reba_table_b[upper_arm_score][lower_arm_score][wrist_score]
    
    # Step C: Combined score
    reba_score = reba_table_c[score_a][score_b]
    
    # Add activity score (force, repetition)
    activity_score = 0  # Can add +1 for static posture, etc.
    
    return reba_score + activity_score
```

### Motion Efficiency Analysis (NEW)

```python
class MotionEfficiencyAnalyzer:
    """
    Analyzes worker motion efficiency by comparing to expert baseline.
    Identifies improvement opportunities for faster onboarding and productivity gains.
    """
    
    def extract_efficiency_features(self, pose_sequence: List[Dict]) -> Dict[str, float]:
        """
        Extract 7 key efficiency metrics from pose sequence
        
        Returns:
            {
                "hand_coordination_ratio": 0.78,      # 0-1, higher = more parallel work
                "motion_smoothness": 0.85,             # 0-1, lower jerk = smoother
                "path_efficiency": 0.72,               # 0-1, straighter paths = better
                "unnecessary_reaches": 3,              # count of wasted movements
                "trunk_angle_stability": 0.91,         # 0-1, less swaying = better
                "arm_extension_ratio": 0.65,           # 0-1, optimal reach distance
                "avg_reba_score": 4.2                  # 1-15, lower = safer posture
            }
        """
        left_hand = [p["point_15"] for p in pose_sequence]   # Left wrist
        right_hand = [p["point_16"] for p in pose_sequence]  # Right wrist
        
        # 1. Hand Coordination Ratio
        hand_coord_ratio = self._calculate_hand_coordination(left_hand, right_hand)
        
        # 2. Motion Smoothness (inverse of jerk)
        smoothness = self._calculate_smoothness(left_hand, right_hand)
        
        # 3. Path Efficiency
        path_eff = self._calculate_path_efficiency(left_hand, right_hand)
        
        # 4. Unnecessary Reaches
        wasted_moves = self._detect_unnecessary_reaches(pose_sequence)
        
        # 5. Trunk Stability
        trunk_stability = self._calculate_trunk_stability(pose_sequence)
        
        # 6. Arm Extension Ratio
        arm_extension = self._calculate_arm_extension_ratio(pose_sequence)
        
        # 7. Average REBA Score
        avg_reba = np.mean([calculate_reba_score(p) for p in pose_sequence])
        
        return {
            "hand_coordination_ratio": hand_coord_ratio,
            "motion_smoothness": smoothness,
            "path_efficiency": path_eff,
            "unnecessary_reaches": wasted_moves,
            "trunk_angle_stability": trunk_stability,
            "arm_extension_ratio": arm_extension,
            "avg_reba_score": avg_reba
        }
    
    def _calculate_hand_coordination(self, left_hand: List, right_hand: List) -> float:
        """
        Measure parallel work vs sequential work.
        Expert workers use both hands simultaneously more often.
        """
        # Calculate velocity magnitude for each hand
        left_velocity = np.diff([np.linalg.norm(p[:3]) for p in left_hand])
        right_velocity = np.diff([np.linalg.norm(p[:3]) for p in right_hand])
        
        # Count frames where both hands are moving (velocity > threshold)
        threshold = 0.01
        both_moving = np.sum((left_velocity > threshold) & (right_velocity > threshold))
        total_frames = len(left_velocity)
        
        return both_moving / total_frames  # Higher = more parallel work
    
    def _calculate_smoothness(self, left_hand: List, right_hand: List) -> float:
        """
        Measure motion smoothness using jerk (3rd derivative of position).
        Expert workers have smoother, less jerky movements.
        """
        def calculate_jerk(trajectory: List) -> float:
            positions = np.array([p[:3] for p in trajectory])
            velocity = np.diff(positions, axis=0)
            acceleration = np.diff(velocity, axis=0)
            jerk = np.diff(acceleration, axis=0)
            return np.mean(np.linalg.norm(jerk, axis=1))
        
        left_jerk = calculate_jerk(left_hand)
        right_jerk = calculate_jerk(right_hand)
        avg_jerk = (left_jerk + right_jerk) / 2
        
        # Normalize to 0-1 (lower jerk = higher smoothness)
        max_jerk = 0.05  # Empirically determined threshold
        return max(0, 1 - (avg_jerk / max_jerk))
    
    def _calculate_path_efficiency(self, left_hand: List, right_hand: List) -> float:
        """
        Compare actual path length to straight-line distance.
        Expert workers take more direct paths.
        """
        def path_efficiency(trajectory: List) -> float:
            positions = np.array([p[:3] for p in trajectory])
            # Actual path length
            actual_distance = np.sum(np.linalg.norm(np.diff(positions, axis=0), axis=1))
            # Straight-line distance
            straight_distance = np.linalg.norm(positions[-1] - positions[0])
            return straight_distance / actual_distance if actual_distance > 0 else 0
        
        left_eff = path_efficiency(left_hand)
        right_eff = path_efficiency(right_hand)
        return (left_eff + right_eff) / 2

    def _detect_unnecessary_reaches(self, pose_sequence: List[Dict]) -> int:
        """
        Detect movements that return to same position without accomplishing work.
        Expert workers minimize these wasted motions.
        """
        wrist_positions = np.array([
            [p["point_15"][:3], p["point_16"][:3]] for p in pose_sequence
        ])
        
        unnecessary_count = 0
        position_threshold = 0.05  # 5cm threshold
        
        for i in range(2, len(wrist_positions) - 1):
            # Check if hand returns to previous position
            prev_pos = wrist_positions[i-2]
            curr_pos = wrist_positions[i]
            dist = np.linalg.norm(curr_pos - prev_pos, axis=1)
            
            if np.any(dist < position_threshold):
                unnecessary_count += 1
        
        return unnecessary_count

    def _calculate_trunk_stability(self, pose_sequence: List[Dict]) -> float:
        """
        Measure trunk angle variation. Expert workers maintain stable posture.
        """
        trunk_angles = []
        for pose in pose_sequence:
            hip = np.array(pose["point_23"][:3])    # Left hip
            shoulder = np.array(pose["point_11"][:3])  # Left shoulder
            trunk_vector = shoulder - hip
            # Calculate angle from vertical (z-axis)
            vertical = np.array([0, 0, 1])
            angle = np.arccos(np.dot(trunk_vector, vertical) / 
                            (np.linalg.norm(trunk_vector) * np.linalg.norm(vertical)))
            trunk_angles.append(np.degrees(angle))
        
        # Lower standard deviation = more stable
        stability = 1.0 / (1.0 + np.std(trunk_angles))
        return min(1.0, stability)

    def _calculate_arm_extension_ratio(self, pose_sequence: List[Dict]) -> float:
        """
        Measure arm extension distance relative to optimal reach zone.
        Expert workers stay in comfortable reach zone (40-60% of max reach).
        """
        arm_extensions = []
        for pose in pose_sequence:
            shoulder = np.array(pose["point_11"][:3])
            elbow = np.array(pose["point_13"][:3])
            wrist = np.array(pose["point_15"][:3])
            
            # Calculate arm extension percentage
            upper_arm_len = np.linalg.norm(elbow - shoulder)
            forearm_len = np.linalg.norm(wrist - elbow)
            full_reach = np.linalg.norm(wrist - shoulder)
            max_reach = upper_arm_len + forearm_len
            
            extension_ratio = full_reach / max_reach if max_reach > 0 else 0
            arm_extensions.append(extension_ratio)
        
        # Optimal range: 0.4-0.6 (40-60% extension)
        avg_extension = np.mean(arm_extensions)
        if 0.4 <= avg_extension <= 0.6:
            return 1.0
        elif avg_extension < 0.4:
            return avg_extension / 0.4
        else:
            return 1.0 - (avg_extension - 0.6) / 0.4


class ExpertNoviceComparator:
    """
    Compare novice worker performance against expert baseline.
    Generate actionable training recommendations.
    """
    
    def compare_workers(
        self, 
        expert_features: Dict[str, float],
        novice_features: Dict[str, float]
    ) -> Dict:
        """
        Compare feature differences and estimate productivity gap.
        
        Returns:
            {
                "efficiency_score": 62,  # 0-100 scale
                "gaps": [
                    {
                        "metric": "hand_coordination_ratio",
                        "expert": 0.78,
                        "novice": 0.23,
                        "gap": 0.55,
                        "time_loss_sec": 8.5,
                        "recommendation": "Practice using both hands simultaneously"
                    },
                    ...
                ],
                "estimated_cycle_time_increase": 18.3,  # seconds slower than expert
                "training_priority": ["hand_coordination", "motion_smoothness", "path_efficiency"]
            }
        """
        gaps = []
        total_time_loss = 0
        
        # Compare each metric
        for metric, expert_value in expert_features.items():
            novice_value = novice_features.get(metric, 0)
            gap = abs(expert_value - novice_value)
            
            # Estimate time impact (empirically calibrated)
            time_impact = self._estimate_time_impact(metric, gap)
            total_time_loss += time_impact
            
            if gap > 0.1 or (metric == "unnecessary_reaches" and gap > 2):
                gaps.append({
                    "metric": metric,
                    "expert": round(expert_value, 2),
                    "novice": round(novice_value, 2),
                    "gap": round(gap, 2),
                    "time_loss_sec": round(time_impact, 1),
                    "recommendation": self._generate_recommendation(metric, gap)
                })
        
        # Sort by time impact (highest priority first)
        gaps.sort(key=lambda x: x["time_loss_sec"], reverse=True)
        
        # Calculate overall efficiency score (0-100)
        efficiency_score = max(0, 100 - (total_time_loss / 30 * 100))  # 30sec = 0% efficiency
        
        return {
            "efficiency_score": int(efficiency_score),
            "gaps": gaps[:5],  # Top 5 gaps
            "estimated_cycle_time_increase": round(total_time_loss, 1),
            "training_priority": [g["metric"] for g in gaps[:3]]
        }
    
    def _estimate_time_impact(self, metric: str, gap: float) -> float:
        """Estimate time loss in seconds based on metric gap"""
        impact_factors = {
            "hand_coordination_ratio": 15.0,    # 15 sec per 1.0 gap
            "motion_smoothness": 8.0,
            "path_efficiency": 12.0,
            "unnecessary_reaches": 2.0,         # 2 sec per extra reach
            "trunk_angle_stability": 3.0,
            "arm_extension_ratio": 5.0,
            "avg_reba_score": 1.5
        }
        return gap * impact_factors.get(metric, 5.0)
    
    def _generate_recommendation(self, metric: str, gap: float) -> str:
        """Generate training recommendation based on gap"""
        recommendations = {
            "hand_coordination_ratio": "Practice using both hands simultaneously during assembly tasks",
            "motion_smoothness": "Focus on smooth, controlled movements. Avoid jerky motions",
            "path_efficiency": "Take more direct paths to parts. Minimize detours",
            "unnecessary_reaches": "Plan movements in advance. Minimize returns to same position",
            "trunk_angle_stability": "Maintain stable posture. Avoid excessive leaning or swaying",
            "arm_extension_ratio": "Work within comfortable reach zone (40-60% arm extension)",
            "avg_reba_score": "Improve ergonomics: keep back straight, elbows at 90 degrees"
        }
        return recommendations.get(metric, "Review expert video for best practices")


class EfficiencyReportGenerator:
    """Generate visual reports comparing expert vs novice performance"""
    
    def generate_radar_chart(
        self, 
        expert_features: Dict[str, float],
        novice_features: Dict[str, float]
    ) -> str:
        """
        Create radar chart comparing 5 key metrics.
        Returns: base64-encoded PNG image
        """
        import matplotlib.pyplot as plt
        from math import pi
        
        # Select top 5 metrics for visualization
        metrics = [
            "hand_coordination_ratio",
            "motion_smoothness", 
            "path_efficiency",
            "trunk_angle_stability",
            "arm_extension_ratio"
        ]
        
        expert_values = [expert_features[m] for m in metrics]
        novice_values = [novice_features[m] for m in metrics]
        
        # Create radar chart
        angles = [n / len(metrics) * 2 * pi for n in range(len(metrics))]
        expert_values += expert_values[:1]
        novice_values += novice_values[:1]
        angles += angles[:1]
        
        fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
        ax.plot(angles, expert_values, 'o-', linewidth=2, label='Expert', color='green')
        ax.fill(angles, expert_values, alpha=0.25, color='green')
        ax.plot(angles, novice_values, 'o-', linewidth=2, label='Novice', color='red')
        ax.fill(angles, novice_values, alpha=0.25, color='red')
        
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels([m.replace('_', ' ').title() for m in metrics])
        ax.set_ylim(0, 1)
        ax.legend(loc='upper right')
        ax.set_title("Motion Efficiency Comparison", size=16, y=1.08)
        
        # Convert to base64
        import io, base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        
        return f"data:image/png;base64,{img_base64}"
    
    def generate_timeline_comparison(
        self,
        expert_reba_timeline: List[int],
        novice_reba_timeline: List[int]
    ) -> str:
        """
        Create timeline chart showing REBA scores over time.
        Returns: base64-encoded PNG image
        """
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(12, 5))
        
        frames = range(len(expert_reba_timeline))
        ax.plot(frames, expert_reba_timeline, label='Expert', color='green', linewidth=2)
        ax.plot(frames, novice_reba_timeline, label='Novice', color='red', linewidth=2)
        
        # Add risk zones
        ax.axhspan(0, 3, alpha=0.1, color='green', label='Low Risk')
        ax.axhspan(3, 7, alpha=0.1, color='yellow', label='Medium Risk')
        ax.axhspan(7, 15, alpha=0.1, color='red', label='High Risk')
        
        ax.set_xlabel('Frame Number', fontsize=12)
        ax.set_ylabel('REBA Score', fontsize=12)
        ax.set_title('Ergonomic Risk Timeline Comparison', fontsize=14)
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Convert to base64
        import io, base64
        buf = io.BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.read()).decode('utf-8')
        plt.close()
        
        return f"data:image/png;base64,{img_base64}"
```

### Value

| Metric                          |
|---------------------------------|
| Worker Efficiency Improvement   | 
| Training Time Reduction         | 
| REBA Score Calculation Accuracy | 

---

## Version Management & Multi-Site Sharing

### Version Control Model

```
Site A (Factory 1)              Site B (Factory 2)
    │                               │
    ▼                               ▼
┌──────────────┐              ┌──────────────┐
│ Layout v1.0  │              │ Layout v1.0  │ (Shared from A)
│ Author: John │              │ Author: John │
│ Hash: a3f2c1 │─────share────>│ Hash: a3f2c1 │
└──────────────┘              └──────────────┘
    │                               │
    │ (Local edit)                  │ (Local edit)
    ▼                               ▼
┌──────────────┐              ┌──────────────┐
│ Layout v1.1  │              │ Layout v1.1  │
│ Author: John │              │ Author: Mary │
│ Hash: b4e7d2 │              │ Hash: c8k3m5 │
└──────────────┘              └──────────────┘
    │                               │
    └───────────merge───────────────┘
                │
                ▼
         ┌──────────────┐
         │ Layout v2.0  │
         │ Merged       │
         │ Hash: d9n2p7 │
         └──────────────┘
```

### Sharing Workflow

1. **Export Version**: `POST /versions` → Create version snapshot
2. **Share**: `POST /share-configuration` → Send to target site
3. **Import**: Target site receives notification
4. **Review**: Compare with local version (`GET /versions/diff`)
5. **Merge**: Accept changes or resolve conflicts

---

## Collision Detection System

### Detection Methods

| Method                           | Use Case             | Performance | Accuracy  |
|----------------------------------|----------------------|-------------|-----------|
| AABB (Axis-Aligned Bounding Box) | Quick pre-check      | Very Fast   | Low       |
| OBB (Oriented Bounding Box)      | Rotated objects      | Fast        | Medium    |
| Mesh-Mesh                        | Precise detection    | Slow        | Very High |
| PhysX (GPU-accelerated)          | Real-time simulation | Fast (GPU)  | High      |

### Interference Types

```python
COLLISION_TYPES = {
    "space_conflict": "Physical overlap between objects",
    "clearance_violation": "Insufficient safety clearance",
    "reach_issue": "Worker cannot reach workpiece",
    "ergonomic_risk": "Awkward posture required",
    "material_flow_block": "Conveyor path blocked"
}
```

---

## Multilingual Support (NEW) ⚠️ REQ #37

### Overview

Support for multiple languages across the entire application: English (EN), Traditional Chinese (zh-TW), Spanish (ES), and Simplified Chinese (zh-CN).

> **📋 SCOPE UPDATE (2025-12-13):**  
> Spanish (ES) and Simplified Chinese (zh-CN) support have been **added to scope** per project requirements (REQ #37).  
> The system will support **English (EN)**, **Traditional Chinese (zh-TW)**, **Spanish (ES)**, and **Simplified Chinese (zh-CN)**.  
> Full multilingual support for all target factory regions is now included.

### Supported Languages

| Code | Language | Status | Target Users | Phase |
|------|----------|--------|--------------|-------|
| `en` | English | ✅ Supported | Global users, documentation | P3 |
| `zh-TW` | Traditional Chinese | ✅ Supported | Taiwan factories, 中文使用者 | P3 |
| `es` | Spanish | ✅ Supported | Mexico factories, Latin America | P3 |
| `zh-CN` | Simplified Chinese | ✅ Supported | Mainland China factories, 简体中文用户 | P3 |

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  i18n Architecture                          │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  react-intl / react-i18next (Frontend)                │  │
│  │  - Language detection (browser, user preference)      │  │
│  │  - Dynamic locale switching                           │  │
│  │  - Formatted numbers, dates, currencies               │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Babel / gettext (Backend)                            │  │
│  │  - API error messages                                 │  │
│  │  - Email notifications                                │  │
│  │  - Generated reports (PDF/Excel)                      │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Translation Files (EN + zh-TW + ES + zh-CN)          │  │
│  │  - locales/en.json                                    │  │
│  │  - locales/zh-TW.json                                 │  │
│  │  - locales/es.json (Spanish - Mexico factories)       │  │
│  │  - locales/zh-CN.json (Simplified Chinese - Mainland) │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Implementation

```typescript
// Frontend: react-intl setup
import { IntlProvider, FormattedMessage, useIntl } from 'react-intl';
import messages_en from './locales/en.json';
import messages_tw from './locales/zh-TW.json';
import messages_es from './locales/es.json';
import messages_cn from './locales/zh-CN.json';

const messages = {
  'en': messages_en,
  'zh-TW': messages_tw,
  'es': messages_es,
  'zh-CN': messages_cn
};

// Supported locales
const SUPPORTED_LOCALES = ['en', 'zh-TW', 'es', 'zh-CN'] as const;
type SupportedLocale = typeof SUPPORTED_LOCALES[number];

// Usage in components
<FormattedMessage id="optimization.title" defaultMessage="Line Balance Optimization" />

// API endpoint for locale
GET /api/user/locale
PUT /api/user/locale { "locale": "zh-CN" }  // Accepts 'en', 'zh-TW', 'es', or 'zh-CN'
```

### Translation Coverage

| Area | Keys | EN Status | zh-TW Status | ES Status | zh-CN Status |
|------|------|-----------|--------------|-----------|---------------|
| UI Labels | ~500 | ✅ Ready | ✅ Ready | 📋 Planned | 📋 Planned |
| Error Messages | ~100 | ✅ Ready | ✅ Ready | 📋 Planned | 📋 Planned |
| Help Text | ~200 | ✅ Ready | 📋 Planned | 📋 Planned | 📋 Planned |
| Reports | ~150 | ✅ Ready | 📋 Planned | 📋 Planned | 📋 Planned |
| Notifications | ~50 | ✅ Ready | 📋 Planned | 📋 Planned | 📋 Planned |

### Spanish Translation Service (Placeholder)

```python
# src/services/translation_service.py
from typing import Dict, List, Optional
from enum import Enum

class SupportedLocale(str, Enum):
    """Supported UI languages"""
    EN = "en"
    ZH_TW = "zh-TW"
    ES = "es"
    ZH_CN = "zh-CN"

class TranslationService:
    """
    Translation service for multilingual support.
    Placeholder implementation - integrate with translation management system.
    """
    
    def __init__(self, config: dict):
        self.default_locale = SupportedLocale.EN
        self.translation_cache: Dict[str, Dict[str, str]] = {}
        self._load_translations()
    
    def _load_translations(self):
        """Load translation files for all supported locales"""
        # Placeholder: Load from JSON files or translation management API
        self.translation_cache = {
            "en": self._load_locale_file("locales/en.json"),
            "zh-TW": self._load_locale_file("locales/zh-TW.json"),
            "es": self._load_locale_file("locales/es.json"),
            "zh-CN": self._load_locale_file("locales/zh-CN.json"),
        }
    
    def _load_locale_file(self, path: str) -> Dict[str, str]:
        """Load translations from file (placeholder)"""
        # TODO: Replace with actual file loading
        return {}
    
    def translate(
        self,
        key: str,
        locale: SupportedLocale,
        params: Optional[Dict] = None
    ) -> str:
        """Get translated string for key"""
        translations = self.translation_cache.get(locale.value, {})
        text = translations.get(key, key)  # Fallback to key if not found
        
        if params:
            for k, v in params.items():
                text = text.replace(f"{{{k}}}", str(v))
        
        return text
    
    def get_missing_translations(
        self,
        locale: SupportedLocale
    ) -> List[str]:
        """Get list of keys missing translation for a locale"""
        en_keys = set(self.translation_cache.get("en", {}).keys())
        locale_keys = set(self.translation_cache.get(locale.value, {}).keys())
        return list(en_keys - locale_keys)

# Spanish-specific formatting helpers
class SpanishFormatter:
    """Locale-specific formatting for Spanish (Mexico)"""
    
    @staticmethod
    def format_number(value: float) -> str:
        """Format number with Mexican Spanish conventions"""
        # Mexico uses comma for thousands, period for decimal
        return f"{value:,.2f}"
    
    @staticmethod
    def format_date(date) -> str:
        """Format date in Mexican Spanish format (DD/MM/YYYY)"""
        return date.strftime("%d/%m/%Y")
    
    @staticmethod
    def format_currency(value: float) -> str:
        """Format currency in Mexican Peso"""
        return f"${value:,.2f} MXN"

# Simplified Chinese-specific formatting helpers
class SimplifiedChineseFormatter:
    """Locale-specific formatting for Simplified Chinese (Mainland China)"""
    
    @staticmethod
    def format_number(value: float) -> str:
        """Format number with Chinese conventions"""
        # China uses comma for thousands, period for decimal
        return f"{value:,.2f}"
    
    @staticmethod
    def format_date(date) -> str:
        """Format date in Chinese format (YYYY年MM月DD日)"""
        return date.strftime("%Y年%m月%d日")
    
    @staticmethod
    def format_currency(value: float) -> str:
        """Format currency in Chinese Yuan (RMB)"""
        return f"¥{value:,.2f} CNY"
    
    @staticmethod
    def format_percentage(value: float) -> str:
        """Format percentage with Chinese suffix"""
        return f"{value:.1f}%"
```

### Spanish Translation File Structure (Placeholder)

```json
// locales/es.json (Placeholder - to be completed by translation team)
{
  "common": {
    "save": "Guardar",
    "cancel": "Cancelar",
    "delete": "Eliminar",
    "edit": "Editar",
    "search": "Buscar",
    "loading": "Cargando...",
    "error": "Error",
    "success": "Éxito"
  },
  "optimization": {
    "title": "Optimización de Balance de Línea",
    "run": "Ejecutar Optimización",
    "results": "Resultados",
    "stations": "Estaciones",
    "workers": "Trabajadores",
    "takt_time": "Tiempo Takt",
    "utilization": "Utilización",
    "bottleneck": "Cuello de Botella"
  },
  "dashboard": {
    "overview": "Resumen",
    "production_lines": "Líneas de Producción",
    "current_status": "Estado Actual",
    "performance": "Rendimiento"
  },
  "alerts": {
    "cycle_time_warning": "Advertencia: Tiempo de ciclo excedido",
    "cycle_time_critical": "Crítico: Tiempo de ciclo muy alto",
    "station_idle": "Estación inactiva",
    "quality_issue": "Problema de calidad detectado"
  },
  "reports": {
    "export_excel": "Exportar a Excel",
    "export_pdf": "Exportar a PDF",
    "date_range": "Rango de Fechas",
    "generated_by": "Generado por"
  }
}
```

### Simplified Chinese Translation File Structure (Placeholder)

```json
// locales/zh-CN.json (Placeholder - to be completed by translation team)
{
  "common": {
    "save": "保存",
    "cancel": "取消",
    "delete": "删除",
    "edit": "编辑",
    "search": "搜索",
    "loading": "加载中...",
    "error": "错误",
    "success": "成功"
  },
  "optimization": {
    "title": "线平衡优化",
    "run": "运行优化",
    "results": "结果",
    "stations": "工位",
    "workers": "工人",
    "takt_time": "节拍时间",
    "utilization": "利用率",
    "bottleneck": "瓶颈"
  },
  "dashboard": {
    "overview": "概览",
    "production_lines": "生产线",
    "current_status": "当前状态",
    "performance": "性能"
  },
  "alerts": {
    "cycle_time_warning": "警告: 周期时间超标",
    "cycle_time_critical": "严重: 周期时间过高",
    "station_idle": "工位空闲",
    "quality_issue": "检测到质量问题"
  },
  "reports": {
    "export_excel": "导出Excel",
    "export_pdf": "导出PDF",
    "date_range": "日期范围",
    "generated_by": "生成者"
  }
}
```

### Translation Management API (Placeholder)

```yaml
# Translation management endpoints (future integration)
GET /api/i18n/locales:
  description: List supported locales
  response:
    locales:
      - code: "en"
        name: "English"
        rtl: false
        completion: 100
      - code: "zh-TW"
        name: "繁體中文"
        rtl: false
        completion: 85
      - code: "es"
        name: "Español (México)"
        rtl: false
        completion: 60
      - code: "zh-CN"
        name: "简体中文"
        rtl: false
        completion: 60

GET /api/i18n/translations/{locale}:
  description: Get all translations for a locale
  response:
    locale: string
    translations: object
    last_updated: datetime

POST /api/i18n/translations/{locale}:
  description: Update translations (admin only)
  request:
    translations: object
  response:
    updated_count: integer
    status: string

GET /api/i18n/missing/{locale}:
  description: Get missing translation keys for a locale
  response:
    locale: string
    missing_keys: string[]
    total_missing: integer
```

### Implementation Timeline

| Sprint | Deliverable | Status |
|--------|-------------|--------|
| Sprint 5 | i18n framework setup (react-intl) | Planned |
| Sprint 5 | English (EN) complete translations | Planned |
| Sprint 6 | Traditional Chinese (zh-TW) translations | Planned |
| Sprint 6 | Spanish (ES) core UI translations | Planned |
| Sprint 7 | Spanish (ES) reports & notifications | Planned |
| Sprint 7 | Translation management admin portal | Planned |

---

## Interactive 3D (NEW) ⚠️ REQ #38

### Part-Level 3D Interaction

Enable users to rotate, move, and interact with individual parts in the 3D viewer.

### Features

| Feature | Description | Technology |
|---------|-------------|------------|
| **Select Part** | Click to select individual components | Three.js Raycaster |
| **Rotate Part** | Free rotation with gizmo controls | TransformControls |
| **Move Part** | Translate part in 3D space | TransformControls |
| **Scale Part** | Resize components | TransformControls |
| **Part Info** | Show part details on hover | Custom tooltip |
| **Explode View** | Separate parts for inspection | Animation system |
| **Assembly Sequence** | Animated assembly order | Timeline animation |

### Implementation

```typescript
// Three.js Transform Controls
import { TransformControls } from 'three/examples/jsm/controls/TransformControls';

const transformControl = new TransformControls(camera, renderer.domElement);
transformControl.attach(selectedObject);
transformControl.setMode('translate'); // 'rotate', 'scale'

// Part selection with Raycaster
const raycaster = new THREE.Raycaster();
const mouse = new THREE.Vector2();

function onMouseClick(event) {
  mouse.x = (event.clientX / window.innerWidth) * 2 - 1;
  mouse.y = -(event.clientY / window.innerHeight) * 2 + 1;
  
  raycaster.setFromCamera(mouse, camera);
  const intersects = raycaster.intersectObjects(scene.children, true);
  
  if (intersects.length > 0) {
    selectPart(intersects[0].object);
  }
}

// Explosion view animation
function explodeView(explodeDistance: number) {
  parts.forEach((part, index) => {
    const direction = part.position.clone().normalize();
    part.userData.originalPosition = part.position.clone();
    part.position.add(direction.multiplyScalar(explodeDistance));
  });
}
```

### API Endpoints

```
GET /3d-models/{model_id}/parts           # List all parts in model
GET /3d-models/{model_id}/parts/{part_id} # Get part details
POST /3d-models/{model_id}/explode        # Generate exploded view
POST /3d-models/{model_id}/sequence       # Get assembly sequence animation
```

---

## Live Monitoring & Alerts (NEW) ⚠️ REQ #39

**Phase Assignment:** Phase 3 - Advanced Features  
**Implementation Priority:** High  
**Target Sprint:** Sprint 5-6 (Phase 3)  
**Dependencies:** MES Integration (REQ #44), BDC Integration (REQ #44b)

### Overview

Real-time monitoring of production cycle times with intelligent alerting for anomalies. This feature enables factory supervisors and line leaders to receive immediate notifications when cycle times deviate from expected values (sourced from BDC).

### Real-Time Cycle Time Monitoring

Monitor actual cycle times against expected values and trigger alerts for anomalies.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                Live Monitoring Architecture                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Data Sources                                         │  │
│  │  - MES/SCADA systems (cycle time data)                │  │
│  │  - IoT sensors (station status)                       │  │
│  │  - Barcode scanners (production counts)               │  │
│  └─────────────────────┬─────────────────────────────────┘  │
│                        │ MQTT / Kafka / WebSocket            │
│  ┌─────────────────────▼─────────────────────────────────┐  │
│  │  Stream Processing (Real-Time)                        │  │
│  │  - Apache Kafka Streams / Flink                       │  │
│  │  - Moving average calculation                         │  │
│  │  - Anomaly detection (Z-score, IQR)                   │  │
│  └─────────────────────┬─────────────────────────────────┘  │
│                        │ Alert trigger                       │
│  ┌─────────────────────▼─────────────────────────────────┐  │
│  │  Alert Service                                        │  │
│  │  - Email notifications                                │  │
│  │  - Push notifications (mobile app)                    │  │
│  │  - Dashboard alerts (WebSocket)                       │  │
│  │  - Slack/Teams integration                            │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Alert Types

| Alert Type | Trigger Condition | Severity | Action |
|------------|-------------------|----------|--------|
| **Cycle Time Exceeded** | Actual > Expected × 1.2 | Warning | Notify supervisor |
| **Cycle Time Critical** | Actual > Expected × 1.5 | Critical | Stop line, investigate |
| **Station Idle** | No activity > 5 min | Warning | Check worker status |
| **Quality Issue** | Defect rate > threshold | Critical | Quality hold |
| **Ergonomic Risk** | REBA score > 7 | Warning | Suggest break/rotation |

### API Endpoints

```
WebSocket: /ws/live-monitoring/{site_id}

# REST endpoints for configuration
POST /alerts/rules                    # Create alert rule
GET  /alerts/rules                    # List alert rules
PUT  /alerts/rules/{rule_id}          # Update rule
DELETE /alerts/rules/{rule_id}        # Delete rule

POST /alerts/acknowledge/{alert_id}   # Acknowledge alert
GET  /alerts/history                  # Get alert history
```

### Alert Rule Schema

```json
{
  "rule_id": "alert_001",
  "name": "Cycle Time Warning",
  "condition": {
    "metric": "cycle_time_ms",
    "operator": "gt",
    "threshold": 36000,
    "duration_seconds": 60
  },
  "severity": "warning",
  "notifications": {
    "email": ["supervisor@company.com"],
    "slack_channel": "#production-alerts",
    "dashboard": true
  },
  "enabled": true
}
```

### Alert Escalation Matrix

| Alert Level | Trigger Condition | Notification Recipients | Response Time |
|-------------|-------------------|------------------------|---------------|
| **Level 1** | 10-20% over expected CT | Line Leader (dashboard) | 5 minutes |
| **Level 2** | 20-50% over expected CT | Supervisor (email + push) | 15 minutes |
| **Level 3** | >50% over expected CT | Plant Manager (SMS + email) | 30 minutes |
| **Critical** | Station stopped / quality hold | All stakeholders | Immediate |

### BDC-Linked Threshold Configuration

```python
# src/services/alert_threshold_service.py
class AlertThresholdService:
    """Dynamic thresholds linked to BDC Expected CT"""
    
    async def calculate_dynamic_threshold(
        self, 
        station_id: str,
        product_id: str
    ) -> AlertThreshold:
        """Calculate alert thresholds based on BDC Expected CT"""
        # Fetch expected CT from BDC
        expected_ct = await self.bdc_adapter.get_expected_cycle_time(
            product_id, station_id
        )
        
        return AlertThreshold(
            station_id=station_id,
            product_id=product_id,
            expected_ct_seconds=expected_ct["value"],
            warning_threshold=expected_ct["value"] * 1.2,   # +20%
            critical_threshold=expected_ct["value"] * 1.5,  # +50%
            source="BDC",
            last_updated=datetime.utcnow()
        )
    
    async def refresh_all_thresholds(self, site_id: str) -> Dict:
        """Refresh all thresholds from BDC for a site"""
        bdc_data = await self.bdc_adapter.sync_cycle_times(site_id)
        updated_count = 0
        for item in bdc_data["items"]:
            await self.update_threshold(item)
            updated_count += 1
        return {"updated_count": updated_count}
```

### Implementation Timeline

| Sprint | Deliverable | Status |
|--------|-------------|--------|
| Sprint 5 | WebSocket real-time dashboard | Planned |
| Sprint 5 | Basic alert rules engine | Planned |
| Sprint 6 | Email/Slack notification integration | Planned |
| Sprint 6 | BDC threshold synchronization | Planned |
| Sprint 7 | Historical alert analytics | Planned |

---

## APS Integration (NEW) ⚠️ REQ #40

### Advanced Planning & Scheduling Integration

Interface with external APS systems for production planning integration.

### Integration Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                   APS Integration Layer                      │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  APS Adapter Service                                  │  │
│  │  - SAP PP/DS adapter                                  │  │
│  │  - Oracle APS adapter                                 │  │
│  │  - Kinaxis RapidResponse adapter                      │  │
│  │  - Custom APS adapter (REST/SOAP)                     │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Data Exchange                                        │  │
│  │  - Receive: Work orders, due dates, priorities        │  │
│  │  - Send: Capacity, cycle times, constraints           │  │
│  │  - Sync frequency: Real-time / Batch (configurable)   │  │
│  └───────────────────────────────────────────────────────┘  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Line Balance ↔ APS Feedback Loop                     │  │
│  │  - APS sends demand → LB optimizes lines              │  │
│  │  - LB sends capacity → APS adjusts schedule           │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### API Endpoints

```
# APS Configuration
GET  /aps/connections                 # List configured APS systems
POST /aps/connections                 # Add APS connection
PUT  /aps/connections/{conn_id}       # Update connection
DELETE /aps/connections/{conn_id}     # Remove connection
POST /aps/connections/{conn_id}/test  # Test connection

# Data Exchange
POST /aps/sync/work-orders            # Import work orders from APS
POST /aps/sync/capacity               # Send capacity data to APS
GET  /aps/sync/status                 # Get sync status

# Webhooks (APS → Line Balance)
POST /aps/webhook/order-created       # New order notification
POST /aps/webhook/order-updated       # Order update notification
POST /aps/webhook/priority-changed    # Priority change notification
```

### Connection Configuration

```json
{
  "connection_id": "sap_pp_prod",
  "name": "SAP PP/DS Production",
  "type": "sap",
  "config": {
    "host": "sap.company.com",
    "port": 8080,
    "client": "100",
    "user": "integration_user",
    "password_secret": "vault://sap-pp-password"
  },
  "sync_config": {
    "mode": "real_time",
    "batch_interval_minutes": null,
    "import_work_orders": true,
    "export_capacity": true
  },
  "enabled": true
}
```

---

## Automatic WI Generation (NEW) ⚠️ REQ #52

### Work Instruction Auto-Generation

Automatically generate Work Instructions (WI) from assembly sequence database.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                WI Generation Pipeline                        │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Input Sources                                        │  │
│  │  - Assembly sequence database                         │  │
│  │  - Class code definitions                             │  │
│  │  - Part information (images, specs)                   │  │
│  │  - Touch time data                                    │  │
│  │  - 3D model library                                   │  │
│  └─────────────────────┬─────────────────────────────────┘  │
│                        │                                     │
│  ┌─────────────────────▼─────────────────────────────────┐  │
│  │  WI Generator Engine                                  │  │
│  │  - Template engine (Jinja2 / Docxtpl)                 │  │
│  │  - LLM-assisted text generation                       │  │
│  │  - Image extraction from 3D models                    │  │
│  │  - Multi-language support                             │  │
│  └─────────────────────┬─────────────────────────────────┘  │
│                        │                                     │
│  ┌─────────────────────▼─────────────────────────────────┐  │
│  │  Output Formats                                       │  │
│  │  - PDF Work Instructions                              │  │
│  │  - HTML (tablet-friendly)                             │  │
│  │  - DOCX (editable)                                    │  │
│  │  - Video animation (from 3D sequence)                 │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### API Endpoints

```
# WI Generation
POST /wi/generate                     # Generate WI for work order
GET  /wi/{wi_id}                      # Get generated WI
GET  /wi/{wi_id}/download             # Download WI (PDF/DOCX/HTML)

# WI Templates
GET  /wi/templates                    # List WI templates
POST /wi/templates                    # Create custom template
PUT  /wi/templates/{template_id}      # Update template

# WI Review & Approval
POST /wi/{wi_id}/submit-review        # Submit for review
POST /wi/{wi_id}/approve              # Approve WI
POST /wi/{wi_id}/reject               # Reject with comments
```

### WI Generation Request

```json
{
  "work_order_id": "WO_DL360_G11",
  "template_id": "standard_assembly_v2",
  "output_format": "pdf",
  "language": "en",
  "options": {
    "include_images": true,
    "include_3d_snapshots": true,
    "include_safety_warnings": true,
    "include_quality_checkpoints": true,
    "video_animation": false
  },
  "station_filter": [1, 2, 3]
}
```

### WI Output Structure

```json
{
  "wi_id": "WI_DL360_G11_001",
  "work_order_id": "WO_DL360_G11",
  "generated_at": "2025-12-12T10:00:00Z",
  "pages": [
    {
      "station": 1,
      "tasks": [
        {
          "step": 1,
          "task_id": 1,
          "instruction": "Unpack chassis from shipping container",
          "image_url": "/images/wi/chassis_unpack.png",
          "duration_sec": 30,
          "tools_required": ["Cutting pliers"],
          "safety_notes": ["Wear gloves", "Check for damage"]
        }
      ]
    }
  ],
  "download_url": "/wi/WI_DL360_G11_001/download?format=pdf",
  "status": "generated"
}
```

---

## MVS Time Study Module (REQ #9) ⚠️ **IMPLEMENTATION**

### Overview

Method Time Measurement (MTM) / MOST calculation module for accurate operation time estimation per part per workstation.

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MVS Time Study Module                     │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Input Analysis                                       │  │
│  │  - Video recording of operation                       │  │
│  │  - Body sensor data (MediaPipe)                       │  │
│  │  - Equipment usage logs                               │  │
│  └─────────────────────┬─────────────────────────────────┘  │
│                        │                                     │
│  ┌─────────────────────▼─────────────────────────────────┐  │
│  │  Motion Analysis Engine                               │  │
│  │  - Auto-detect motion_type (finger/wrist/elbow/arm)   │  │
│  │  - Classify TMU (Time Measurement Units)              │  │
│  │  - Apply MOST sequence models                         │  │
│  └─────────────────────┬─────────────────────────────────┘  │
│                        │                                     │
│  ┌─────────────────────▼─────────────────────────────────┐  │
│  │  Time Calculation                                     │  │
│  │  - Base MTM time per motion                           │  │
│  │  - Apply fatigue allowance (10-15%)                   │  │
│  │  - Apply skill factor (0.8-1.2x)                      │  │
│  │  - Generate standard time                             │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### MTM/MOST Motion Codes

| Motion Type | TMU Base | Description | Example Actions |
|-------------|----------|-------------|-----------------|
| `finger` | 2-5 TMU | Fine motor | Pick SMD, press button |
| `wrist` | 5-10 TMU | Rotation | Turn screw, adjust knob |
| `elbow` | 10-20 TMU | Forearm | Reach nearby, short carry |
| `arm` | 20-40 TMU | Full arm | Reach far, long carry |
| `body` | 40-80 TMU | Trunk/legs | Bend, walk, lift |

> 1 TMU = 0.036 seconds

### API Endpoints

```
# Time Study
POST /mvs/analyze-video                # Upload video for analysis
GET  /mvs/analysis/{analysis_id}       # Get analysis results
POST /mvs/calculate-time               # Calculate standard time from motions

# Motion Library
GET  /mvs/motion-library               # List all motion codes
POST /mvs/motion-library               # Add custom motion code
```

### Implementation: Motion Analyzer

```python
# src/services/mvs_analyzer.py
from enum import Enum
from typing import List, Dict
import mediapipe as mp

class MotionType(Enum):
    FINGER = "finger"
    WRIST = "wrist"
    ELBOW = "elbow"
    ARM = "arm"
    BODY = "body"

# TMU lookup table (1 TMU = 0.036 sec)
TMU_BASE = {
    MotionType.FINGER: {"reach": 2, "grasp": 4, "release": 2},
    MotionType.WRIST: {"turn": 6, "apply_pressure": 8},
    MotionType.ELBOW: {"reach": 12, "move": 15, "position": 10},
    MotionType.ARM: {"reach": 25, "move": 30, "position": 20},
    MotionType.BODY: {"bend": 45, "walk_step": 15, "lift": 60}
}

class MVSAnalyzer:
    def __init__(self):
        self.pose = mp.solutions.pose.Pose()
        
    def analyze_video(self, video_path: str) -> Dict:
        """Analyze video and extract motion sequences"""
        motions = []
        # Process video frames with MediaPipe
        # Classify each motion by joint displacement
        # Return motion sequence with TMU calculations
        return {
            "motions": motions,
            "total_tmu": sum(m["tmu"] for m in motions),
            "standard_time_sec": sum(m["tmu"] for m in motions) * 0.036
        }
    
    def calculate_standard_time(
        self, 
        motions: List[Dict],
        fatigue_allowance: float = 0.12,
        skill_factor: float = 1.0
    ) -> Dict:
        """Calculate standard time with allowances"""
        base_tmu = sum(m["tmu"] for m in motions)
        adjusted_tmu = base_tmu * (1 + fatigue_allowance) * skill_factor
        return {
            "base_tmu": base_tmu,
            "fatigue_allowance": fatigue_allowance,
            "skill_factor": skill_factor,
            "adjusted_tmu": adjusted_tmu,
            "standard_time_sec": adjusted_tmu * 0.036,
            "standard_time_ms": int(adjusted_tmu * 36)
        }
```

---

## External System Integration Hub ⚠️ **IMPLEMENTATION**

### Overview

Central integration hub for connecting with external enterprise systems (BDC, APS, PDM, SO/MPS).

### Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    External System Integration Hub                       │
│  ┌─────────────────────────────────────────────────────────────────────┐│
│  │                         Adapter Registry                            ││
│  │  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────────┐   ││
│  │  │   BDC   │ │   APS   │ │   PDM   │ │  SO/MPS │ │  Inventory  │   ││
│  │  │ Adapter │ │ Adapter │ │ Adapter │ │ Adapter │ │   Adapter   │   ││
│  │  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └──────┬──────┘   ││
│  └───────┼──────────┼──────────┼──────────┼───────────────┼───────────┘│
│          │          │          │          │               │             │
│  ┌───────▼──────────▼──────────▼──────────▼───────────────▼───────────┐│
│  │                    Integration Service Layer                        ││
│  │  - Connection pooling                                               ││
│  │  - Request/response transformation                                  ││
│  │  - Error handling & retry logic                                     ││
│  │  - Data caching (Redis)                                             ││
│  │  - Audit logging                                                    ││
│  └─────────────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────────────┘
                    │                │               │
          ┌────────▼────────┐ ┌─────▼─────┐ ┌──────▼──────┐
          │   SAP S/4HANA   │ │   Oracle  │ │  Custom ERP │
          │    (BDC, SO)    │ │   (APS)   │ │    (MES)    │
          └─────────────────┘ └───────────┘ └─────────────┘
```

### BDC Integration (REQ #44b)

Basic Data Catalog - Expected cycle time and production standards.

**Phase Assignment:** Phase 3 - External Integration  
**Implementation Priority:** High (Core dependency for Live Monitoring)  
**Target Sprint:** Sprint 5 (Phase 3)

```python
# src/integrations/bdc_adapter.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import httpx

class BDCAdapter:
    """BDC (Basic Data Catalog) Integration Adapter"""
    
    def __init__(self, config: Dict):
        self.base_url = config["bdc_api_url"]
        self.api_key = config["bdc_api_key"]
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def get_expected_cycle_time(
        self, 
        part_id: str, 
        station_type: str
    ) -> Dict:
        """Retrieve expected cycle time from BDC"""
        response = await self.client.get(
            f"{self.base_url}/cycle-times",
            params={"part_id": part_id, "station_type": station_type},
            headers={"Authorization": f"Bearer {self.api_key}"}
        )
        return response.json()
    
    async def sync_cycle_times(self, site_id: str) -> Dict:
        """Sync all cycle times for a site"""
        response = await self.client.get(
            f"{self.base_url}/sites/{site_id}/cycle-times/bulk"
        )
        return {
            "synced_count": len(response.json()["items"]),
            "last_sync": datetime.utcnow().isoformat()
        }
```

**API Endpoints:**
```
POST /integrations/bdc/sync              # Sync cycle times from BDC
GET  /integrations/bdc/cycle-time/{part_id}  # Get expected cycle time
POST /integrations/bdc/alerts            # Configure cycle time alerts
```

### BDC Alert Configuration ⚠️ REQ #44 (Enhanced)

**Purpose**: Configure alerts based on Expected Cycle Time from BDC to notify when actual production deviates from standards.

#### Expected CT Alert Data Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│              BDC → Alert Configuration Flow (REQ #44)                   │
│                                                                          │
│  ┌─────────────┐                ┌─────────────────────────┐             │
│  │    BDC      │                │  Line Balance System    │             │
│  │  (External) │                │                         │             │
│  └──────┬──────┘                │  ┌──────────────────┐  │             │
│         │                       │  │ Expected CT Cache│  │             │
│         │ 1. Sync Expected CT   │  │ (Redis)          │  │             │
│         ├──────────────────────►│  └────────┬─────────┘  │             │
│         │                       │           │             │             │
│         │                       │  ┌────────▼─────────┐  │             │
│  ┌──────▼──────┐                │  │ Alert Threshold  │  │             │
│  │    MES      │                │  │ Calculator       │  │             │
│  │  (External) │                │  │ (+20%, +50%)     │  │             │
│  └──────┬──────┘                │  └────────┬─────────┘  │             │
│         │                       │           │             │             │
│         │ 2. Actual CT Stream   │  ┌────────▼─────────┐  │             │
│         ├──────────────────────►│  │ Alert Evaluator  │  │             │
│         │   (MQTT/Kafka)        │  │ (Compare Actual  │  │             │
│         │                       │  │  vs Expected)    │  │             │
│                                 │  └────────┬─────────┘  │             │
│                                 │           │             │             │
│                                 │  ┌────────▼─────────┐  │             │
│                                 │  │ Notification     │◄─┼── Email     │
│                                 │  │ Service          │◄─┼── Slack     │
│                                 │  │                  │◄─┼── Dashboard │
│                                 │  └──────────────────┘  │             │
│                                 └─────────────────────────┘             │
└─────────────────────────────────────────────────────────────────────────┘
```

#### BDC Expected CT Data Schema (Placeholder)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "BDC Expected Cycle Time",
  "description": "Expected cycle time data from Basic Data Catalog",
  "type": "object",
  "required": ["part_id", "station_type", "expected_ct_seconds"],
  "properties": {
    "part_id": {
      "type": "string",
      "description": "Product/Part identifier from BDC"
    },
    "station_type": {
      "type": "string",
      "description": "Station category (assembly, test, pack)"
    },
    "expected_ct_seconds": {
      "type": "number",
      "description": "Standard cycle time in seconds"
    },
    "tolerance_percent": {
      "type": "number",
      "default": 10,
      "description": "Acceptable variance percentage"
    },
    "effective_date": {
      "type": "string",
      "format": "date"
    },
    "source_system": {
      "type": "string",
      "default": "BDC",
      "description": "Source system identifier"
    }
  }
}
```

#### Alert Configuration Service

```python
# src/services/bdc_alert_service.py
from typing import Dict, List, Optional
from pydantic import BaseModel
from datetime import datetime

class BDCAlertConfig(BaseModel):
    """Configuration for BDC-linked cycle time alerts"""
    config_id: str
    site_id: str
    product_family: str
    
    # Threshold multipliers (applied to BDC Expected CT)
    warning_multiplier: float = 1.2      # +20% triggers warning
    critical_multiplier: float = 1.5     # +50% triggers critical
    
    # Notification settings
    warning_recipients: List[str] = []   # email addresses
    critical_recipients: List[str] = []
    slack_channel: Optional[str] = None
    teams_webhook: Optional[str] = None
    
    # Alert behavior
    cooldown_seconds: int = 300          # 5 min between repeated alerts
    require_acknowledgment: bool = True
    auto_escalate_after_minutes: int = 15
    
    enabled: bool = True
    created_at: datetime = None
    updated_at: datetime = None


class BDCAlertService:
    """Service for managing BDC-linked alerts (REQ #44)"""
    
    def __init__(self, bdc_adapter, notification_service, cache):
        self.bdc = bdc_adapter
        self.notify = notification_service
        self.cache = cache  # Redis cache
    
    async def configure_product_alerts(
        self,
        site_id: str,
        product_family: str,
        config: BDCAlertConfig
    ) -> Dict:
        """Configure alerts for a product family based on BDC Expected CT"""
        # 1. Fetch expected CT from BDC
        expected_cts = await self.bdc.get_expected_cycle_times(
            site_id=site_id,
            product_family=product_family
        )
        
        # 2. Calculate thresholds per station
        thresholds = []
        for ct_data in expected_cts:
            thresholds.append({
                "station_type": ct_data["station_type"],
                "expected_ct": ct_data["expected_ct_seconds"],
                "warning_threshold": ct_data["expected_ct_seconds"] * config.warning_multiplier,
                "critical_threshold": ct_data["expected_ct_seconds"] * config.critical_multiplier
            })
        
        # 3. Store in cache for real-time evaluation
        cache_key = f"bdc_thresholds:{site_id}:{product_family}"
        await self.cache.set(cache_key, thresholds, ex=3600)
        
        return {
            "config_id": config.config_id,
            "thresholds_configured": len(thresholds),
            "status": "active"
        }
    
    async def evaluate_cycle_time(
        self,
        site_id: str,
        product_family: str,
        station_type: str,
        actual_ct_seconds: float
    ) -> Optional[Dict]:
        """Evaluate actual CT against BDC thresholds and trigger alerts"""
        cache_key = f"bdc_thresholds:{site_id}:{product_family}"
        thresholds = await self.cache.get(cache_key)
        
        if not thresholds:
            return None  # No configuration
        
        station_threshold = next(
            (t for t in thresholds if t["station_type"] == station_type),
            None
        )
        
        if not station_threshold:
            return None
        
        # Evaluate
        expected = station_threshold["expected_ct"]
        deviation_pct = ((actual_ct_seconds - expected) / expected) * 100
        
        if actual_ct_seconds >= station_threshold["critical_threshold"]:
            await self._trigger_alert(
                level="critical",
                site_id=site_id,
                station_type=station_type,
                expected=expected,
                actual=actual_ct_seconds,
                deviation_pct=deviation_pct
            )
            return {"alert_level": "critical", "deviation_pct": deviation_pct}
        
        elif actual_ct_seconds >= station_threshold["warning_threshold"]:
            await self._trigger_alert(
                level="warning",
                site_id=site_id,
                station_type=station_type,
                expected=expected,
                actual=actual_ct_seconds,
                deviation_pct=deviation_pct
            )
            return {"alert_level": "warning", "deviation_pct": deviation_pct}
        
        return {"alert_level": "ok", "deviation_pct": deviation_pct}
```

#### BDC Alert API Endpoints

```
# BDC Alert Configuration APIs
POST /integrations/bdc/alerts/configure      # Configure product alerts
GET  /integrations/bdc/alerts/config/{id}    # Get alert configuration
PUT  /integrations/bdc/alerts/config/{id}    # Update configuration
DELETE /integrations/bdc/alerts/config/{id}  # Disable alerts

# Threshold Management
GET  /integrations/bdc/thresholds/{site_id}  # Get all thresholds for site
POST /integrations/bdc/thresholds/refresh    # Force refresh from BDC
GET  /integrations/bdc/thresholds/history    # Threshold change history

# Alert Status & History
GET  /integrations/bdc/alerts/active         # List active alerts
POST /integrations/bdc/alerts/{id}/acknowledge  # Acknowledge alert
GET  /integrations/bdc/alerts/history        # Alert history with filters
```

#### BDC Connection Placeholder Configuration

```yaml
# config/integrations/bdc.yaml (Placeholder)
bdc:
  enabled: true
  connection:
    # Replace with actual BDC endpoint when available
    base_url: "${BDC_API_URL:-http://bdc-placeholder.local/api/v1}"
    api_key: "${BDC_API_KEY}"
    timeout_seconds: 30
  
  sync:
    # Schedule for syncing Expected CT from BDC
    cron_schedule: "0 */4 * * *"  # Every 4 hours
    full_sync_on_startup: true
    retry_attempts: 3
    retry_delay_seconds: 60
  
  cache:
    ttl_seconds: 14400  # 4 hours
    refresh_on_miss: true
  
  # Placeholder: BDC system not yet integrated
  placeholder_mode: true
  placeholder_data_path: "data/bdc_expected_ct_mock.json"
```

---

### SO/MPS Integration (Product Demand - Unassigned REQ)

Sales Order / Master Production Schedule integration for demand data.

```python
# src/integrations/so_mps_adapter.py
class SOMPSAdapter:
    """SO/MPS Integration for Product Demand"""
    
    async def get_demand_forecast(
        self, 
        site_id: str, 
        product_family: str,
        date_range: tuple
    ) -> Dict:
        """Get demand forecast from SO/MPS"""
        response = await self.client.post(
            f"{self.base_url}/demand-forecast",
            json={
                "site_id": site_id,
                "product_family": product_family,
                "start_date": date_range[0],
                "end_date": date_range[1]
            }
        )
        return response.json()
    
    async def get_work_order_priority(
        self, 
        work_order_ids: List[str]
    ) -> Dict:
        """Get priority rankings for work orders"""
        response = await self.client.post(
            f"{self.base_url}/work-orders/priority",
            json={"work_order_ids": work_order_ids}
        )
        return response.json()
```

**API Endpoints:**
```
GET  /integrations/so/demand            # Get demand from SO
POST /integrations/mps/sync             # Sync with MPS
GET  /integrations/mps/capacity-plan    # Get capacity plan
```

### PDM Integration (Technical Specs) ⚠️ **PLACEHOLDER**

Product Data Management for technical specifications, process standards, and assembly documentation.

**Phase Assignment:** Phase 3 - External Integration  
**Implementation Priority:** Medium  
**Target Sprint:** Sprint 7-8 (Phase 3)  
**Status:** Placeholder - Awaiting PDM system API specification

#### Overview

The PDM (Product Data Management) integration enables the Line Balance system to:
- Retrieve technical specifications for products and components
- Access process standards and quality requirements
- Import assembly instructions and work element details
- Sync CAD metadata for workstation layout planning

#### PDM Data Model

```python
# src/models/pdm_data.py
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime

class ESDClass(str, Enum):
    """Electrostatic Discharge sensitivity classification"""
    CLASS_0 = "class_0"      # <250V - Most sensitive
    CLASS_1 = "class_1"      # <500V
    CLASS_2 = "class_2"      # <1000V
    CLASS_3 = "class_3"      # <2000V
    NOT_SENSITIVE = "none"   # No ESD requirements

class ProcessStandard(str, Enum):
    """Industry process standards"""
    IPC_A_610 = "IPC-A-610"         # Acceptability of Electronic Assemblies
    IPC_J_STD_001 = "J-STD-001"     # Soldering Standards
    IPC_7711_7721 = "IPC-7711/7721" # Rework Standards
    ISO_9001 = "ISO-9001"           # Quality Management
    ISO_14001 = "ISO-14001"         # Environmental Management
    IATF_16949 = "IATF-16949"       # Automotive Quality

class ProductTechnicalSpec(BaseModel):
    """Technical specifications from PDM"""
    part_id: str
    part_number: str
    revision: str
    description: str
    
    # Physical dimensions
    dimensions: Dict[str, float] = {
        "length_mm": 0.0,
        "width_mm": 0.0,
        "height_mm": 0.0
    }
    weight_kg: float = 0.0
    
    # Material properties
    primary_material: str = ""
    material_code: str = ""
    surface_finish: str = ""
    
    # Quality requirements
    tolerance_mm: float = 0.1
    esd_class: ESDClass = ESDClass.NOT_SENSITIVE
    special_handling: List[str] = []
    
    # Standards compliance
    process_standards: List[ProcessStandard] = []
    test_requirements: List[str] = []
    
    # PDM metadata
    pdm_document_id: str = ""
    last_modified: Optional[datetime] = None
    change_notice: Optional[str] = None

class ProcessRequirement(BaseModel):
    """Process requirements from PDM for a part"""
    part_id: str
    
    # Tool requirements
    required_tools: List[Dict[str, str]] = []  # [{"tool_id": "T001", "name": "Torque Driver M3"}]
    
    # Operator requirements
    required_certifications: List[str] = []
    min_skill_level: int = 1  # 1-5 scale
    
    # Quality checkpoints
    quality_checkpoints: List[Dict[str, str]] = []
    measurement_points: List[Dict[str, float]] = []
    
    # Test requirements
    test_sequence: List[str] = []
    test_duration_seconds: float = 0.0
    
    # Assembly instructions
    work_instruction_id: Optional[str] = None
    assembly_video_url: Optional[str] = None

class CADMetadata(BaseModel):
    """CAD file metadata from PDM for layout planning"""
    part_id: str
    cad_file_type: str = "STEP"  # STEP, IGES, DXF, etc.
    file_path: str = ""
    
    # Bounding box for layout planning
    bounding_box: Dict[str, float] = {}
    
    # Assembly points
    assembly_origin: Dict[str, float] = {}
    fixture_points: List[Dict[str, float]] = []
    
    # Visualization
    thumbnail_url: Optional[str] = None
    viewer_url: Optional[str] = None
```

#### PDM Adapter (Placeholder)

```python
# src/integrations/pdm_adapter.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import httpx

class PDMAdapterBase(ABC):
    """Base class for PDM system integration"""
    
    @abstractmethod
    async def get_product_specs(self, part_id: str) -> ProductTechnicalSpec:
        """Get technical specifications for a part"""
        pass
    
    @abstractmethod
    async def get_process_requirements(self, part_id: str) -> ProcessRequirement:
        """Get process/assembly requirements for a part"""
        pass
    
    @abstractmethod
    async def get_cad_metadata(self, part_id: str) -> CADMetadata:
        """Get CAD file metadata for layout planning"""
        pass
    
    @abstractmethod
    async def sync_product_catalog(self, product_family: str) -> Dict:
        """Sync all products in a family from PDM"""
        pass

class StubPDMAdapter(PDMAdapterBase):
    """
    Placeholder adapter for development/testing.
    Replace with actual PDM integration (e.g., Teamcenter, Windchill, Arena).
    """
    
    def __init__(self, config: dict):
        self.config = config
        self._mock_data = self._load_mock_data()
    
    def _load_mock_data(self) -> Dict:
        """Load mock PDM data for development"""
        return {
            "DL360_G11": {
                "specs": {
                    "part_id": "DL360_G11",
                    "part_number": "P56951-B21",
                    "revision": "A02",
                    "description": "ProLiant DL360 Gen11 Server",
                    "dimensions": {"length_mm": 650, "width_mm": 450, "height_mm": 44},
                    "weight_kg": 15.5,
                    "esd_class": "class_2",
                    "process_standards": ["IPC-A-610", "J-STD-001"],
                    "special_handling": ["ESD_SENSITIVE", "FRAGILE_COMPONENTS"]
                },
                "process": {
                    "required_tools": [
                        {"tool_id": "TORQ_T10", "name": "Torque Driver T10 5Nm"},
                        {"tool_id": "ESD_STRAP", "name": "ESD Wrist Strap"},
                        {"tool_id": "THERMAL_PASTE", "name": "Thermal Paste Applicator"}
                    ],
                    "required_certifications": ["IPC_CERTIFIED", "ESD_CERTIFIED"],
                    "min_skill_level": 3,
                    "quality_checkpoints": [
                        {"id": "QC001", "type": "visual", "desc": "Visual inspection"},
                        {"id": "QC002", "type": "torque", "desc": "Torque verification"},
                        {"id": "QC003", "type": "test", "desc": "POST test"}
                    ],
                    "test_sequence": ["POWER_ON_TEST", "BIOS_CONFIG", "BURN_IN_4H"],
                    "test_duration_seconds": 14400
                },
                "cad": {
                    "cad_file_type": "STEP",
                    "bounding_box": {"x": 650, "y": 450, "z": 44},
                    "fixture_points": [
                        {"x": 50, "y": 50, "z": 0},
                        {"x": 600, "y": 50, "z": 0}
                    ]
                }
            },
            "DL380_G11": {
                "specs": {
                    "part_id": "DL380_G11",
                    "part_number": "P56959-B21",
                    "revision": "A01",
                    "description": "ProLiant DL380 Gen11 Server",
                    "dimensions": {"length_mm": 750, "width_mm": 450, "height_mm": 88},
                    "weight_kg": 28.0,
                    "esd_class": "class_2",
                    "process_standards": ["IPC-A-610", "J-STD-001"],
                    "special_handling": ["ESD_SENSITIVE", "HEAVY_LIFT"]
                },
                "process": {
                    "required_tools": [
                        {"tool_id": "TORQ_T10", "name": "Torque Driver T10 5Nm"},
                        {"tool_id": "TORQ_T15", "name": "Torque Driver T15 8Nm"},
                        {"tool_id": "ESD_STRAP", "name": "ESD Wrist Strap"},
                        {"tool_id": "LIFT_ASSIST", "name": "Lift Assist Device"}
                    ],
                    "required_certifications": ["IPC_CERTIFIED", "ESD_CERTIFIED", "LIFT_CERTIFIED"],
                    "min_skill_level": 4,
                    "test_sequence": ["POWER_ON_TEST", "BIOS_CONFIG", "RAID_CONFIG", "BURN_IN_24H"],
                    "test_duration_seconds": 86400
                }
            }
        }
    
    async def get_product_specs(self, part_id: str) -> Dict:
        """Return mock specifications (placeholder)"""
        if part_id in self._mock_data:
            return self._mock_data[part_id]["specs"]
        return {
            "part_id": part_id,
            "status": "not_found",
            "message": f"Part {part_id} not in mock data. Add to PDM when integrated."
        }
    
    async def get_process_requirements(self, part_id: str) -> Dict:
        """Return mock process requirements (placeholder)"""
        if part_id in self._mock_data:
            return self._mock_data[part_id]["process"]
        return {
            "part_id": part_id,
            "required_tools": [],
            "status": "placeholder"
        }
    
    async def get_cad_metadata(self, part_id: str) -> Dict:
        """Return mock CAD metadata (placeholder)"""
        if part_id in self._mock_data:
            return self._mock_data[part_id].get("cad", {})
        return {"part_id": part_id, "status": "cad_not_available"}
    
    async def sync_product_catalog(self, product_family: str) -> Dict:
        """Mock sync operation (placeholder)"""
        return {
            "product_family": product_family,
            "synced_count": len(self._mock_data),
            "status": "placeholder_mode",
            "last_sync": datetime.utcnow().isoformat()
        }
```

#### PDM Service Layer

```python
# src/services/pdm_service.py
class PDMService:
    """Service layer for PDM integration"""
    
    def __init__(self, pdm_adapter: PDMAdapterBase, cache):
        self.pdm = pdm_adapter
        self.cache = cache
    
    async def get_assembly_constraints(self, part_id: str) -> Dict:
        """
        Get assembly constraints for line balance optimization.
        Translates PDM data into optimizer constraints.
        """
        specs = await self.pdm.get_product_specs(part_id)
        process = await self.pdm.get_process_requirements(part_id)
        
        return {
            "part_id": part_id,
            "constraints": {
                "requires_esd_workstation": specs.get("esd_class") not in ["none", None],
                "requires_heavy_lift": "HEAVY_LIFT" in specs.get("special_handling", []),
                "min_operator_skill": process.get("min_skill_level", 1),
                "required_certifications": process.get("required_certifications", []),
                "test_duration_seconds": process.get("test_duration_seconds", 0),
                "tool_requirements": [t["tool_id"] for t in process.get("required_tools", [])]
            },
            "workstation_requirements": {
                "min_width_mm": specs.get("dimensions", {}).get("width_mm", 0) + 200,
                "min_depth_mm": specs.get("dimensions", {}).get("length_mm", 0) + 100,
                "esd_mat_required": specs.get("esd_class") in ["class_0", "class_1", "class_2"],
                "lift_assist_required": specs.get("weight_kg", 0) > 20
            }
        }
    
    async def validate_station_capability(
        self,
        station_id: str,
        part_id: str,
        station_config: Dict
    ) -> Dict:
        """
        Validate if a station can handle a part based on PDM requirements.
        Used in line balance optimization validation.
        """
        constraints = await self.get_assembly_constraints(part_id)
        
        validations = []
        is_capable = True
        
        # Check ESD
        if constraints["constraints"]["requires_esd_workstation"]:
            has_esd = station_config.get("esd_capable", False)
            validations.append({
                "check": "esd_workstation",
                "required": True,
                "station_has": has_esd,
                "pass": has_esd
            })
            if not has_esd:
                is_capable = False
        
        # Check size
        ws_req = constraints["workstation_requirements"]
        station_width = station_config.get("width_mm", 0)
        station_depth = station_config.get("depth_mm", 0)
        
        if station_width < ws_req["min_width_mm"]:
            validations.append({
                "check": "width",
                "required": ws_req["min_width_mm"],
                "station_has": station_width,
                "pass": False
            })
            is_capable = False
        
        return {
            "station_id": station_id,
            "part_id": part_id,
            "is_capable": is_capable,
            "validations": validations
        }
```

#### API Endpoints for PDM Integration

```yaml
# PDM Integration APIs
GET /integrations/pdm/specs/{part_id}:
  description: Get technical specifications from PDM
  response:
    part_id: string
    part_number: string
    dimensions: object
    weight_kg: number
    esd_class: string
    process_standards: string[]

GET /integrations/pdm/process/{part_id}:
  description: Get process requirements from PDM
  response:
    required_tools: object[]
    required_certifications: string[]
    min_skill_level: integer
    quality_checkpoints: object[]
    test_sequence: string[]

GET /integrations/pdm/cad/{part_id}:
  description: Get CAD metadata for layout planning
  response:
    cad_file_type: string
    bounding_box: object
    fixture_points: object[]
    viewer_url: string

GET /integrations/pdm/constraints/{part_id}:
  description: Get translated assembly constraints for optimizer
  response:
    constraints: object
    workstation_requirements: object

POST /integrations/pdm/sync:
  description: Sync product catalog from PDM
  request:
    product_family: string
  response:
    synced_count: integer
    status: string
    last_sync: datetime

POST /integrations/pdm/validate-station:
  description: Validate station capability for a part
  request:
    station_id: string
    part_id: string
    station_config: object
  response:
    is_capable: boolean
    validations: object[]
```

#### PDM Configuration (Placeholder)

```yaml
# config/integrations/pdm.yaml
pdm:
  enabled: true
  adapter_type: "stub"  # Change to actual PDM type when available
  
  # Supported PDM systems (future)
  # adapter_type: "teamcenter" | "windchill" | "arena" | "enovia"
  
  # Placeholder mode
  placeholder_mode: true
  mock_data_path: "data/pdm_mock_catalog.json"
  
  # Connection settings (placeholder)
  connection:
    base_url: "${PDM_API_URL:-http://pdm-placeholder.local/api/v1}"
    api_key: "${PDM_API_KEY}"
    timeout_seconds: 60
  
  sync:
    cron_schedule: "0 2 * * *"  # Daily at 2 AM
    product_families: ["DL360", "DL380", "ML350"]
    include_cad_metadata: true
  
  cache:
    ttl_seconds: 86400  # 24 hours
    refresh_on_miss: true
  
  # Field mappings from PDM to Line Balance
  field_mappings:
    part_number: "item_number"
    dimensions: "physical_attributes.dimensions"
    weight: "physical_attributes.weight"
    esd_class: "handling.esd_classification"
```

---

### MPS Capacity Algorithm (Unassigned REQ)

Master Production Schedule capacity calculation.

```python
# src/services/mps_capacity_service.py
class MPSCapacityService:
    """MPS-based Capacity Planning"""
    
    def calculate_capacity_load(
        self,
        demand: List[Dict],
        available_hours: float,
        available_workers: int,
        uph_by_product: Dict[str, float]
    ) -> Dict:
        """Calculate capacity load vs available capacity"""
        total_required_hours = 0
        for item in demand:
            uph = uph_by_product.get(item["product"], 10)
            hours_needed = item["quantity"] / uph
            total_required_hours += hours_needed
        
        available_capacity = available_hours * available_workers
        load_pct = (total_required_hours / available_capacity) * 100
        
        return {
            "total_required_hours": total_required_hours,
            "available_capacity_hours": available_capacity,
            "load_percentage": load_pct,
            "status": "overload" if load_pct > 100 else "ok",
            "gap_hours": max(0, total_required_hours - available_capacity),
            "recommendations": self._generate_recommendations(load_pct)
        }
    
    def _generate_recommendations(self, load_pct: float) -> List[str]:
        if load_pct > 120:
            return ["Add shift", "Hire temporary workers", "Outsource"]
        elif load_pct > 100:
            return ["Overtime", "Rebalance lines"]
        else:
            return ["Capacity sufficient"]
```

**API Endpoints:**
```
POST /capacity/calculate                # Calculate capacity load
GET  /capacity/analysis/{site_id}       # Get capacity analysis
POST /capacity/what-if                  # What-if scenario analysis
```

### Equipment & Material Availability (Unassigned REQs)

```python
# src/integrations/equipment_adapter.py
class EquipmentAdapter:
    """Equipment availability and scheduling"""
    
    async def get_equipment_status(self, equipment_ids: List[str]) -> Dict:
        """Get real-time equipment status"""
        return {
            "equipment": [
                {
                    "id": "TORQUE_DRV_01",
                    "status": "available",
                    "location": "station_3",
                    "next_maintenance": "2026-01-15"
                }
            ]
        }
    
    async def check_equipment_conflicts(
        self, 
        schedule: List[Dict]
    ) -> Dict:
        """Check for equipment scheduling conflicts"""
        # Detect if same equipment needed at same time
        return {"conflicts": [], "warnings": []}

# src/integrations/inventory_adapter.py
class InventoryAdapter:
    """Raw material availability check"""
    
    async def check_material_availability(
        self, 
        bom: List[Dict],
        quantity: int
    ) -> Dict:
        """Check if materials available for production"""
        return {
            "all_available": True,
            "shortages": [],
            "lead_time_days": 0
        }
```

**API Endpoints:**
```
GET  /integrations/equipment/status          # Equipment status
POST /integrations/equipment/schedule        # Schedule equipment
GET  /integrations/inventory/check           # Check material availability
POST /integrations/inventory/reserve         # Reserve materials
```

---

## Work Order Priority Scheduling (Unassigned REQ) ⚠️ **IMPLEMENTATION**

### Priority Algorithm

```python
# src/services/priority_scheduler.py
from enum import IntEnum
from typing import List, Dict
from datetime import datetime

class PriorityLevel(IntEnum):
    CRITICAL = 1    # Customer escalation, production stop
    HIGH = 2        # Key customer, tight deadline  
    MEDIUM = 3      # Normal production
    LOW = 4         # Internal, flexible deadline

class PriorityScheduler:
    """Work order priority scheduling"""
    
    def calculate_priority_score(self, work_order: Dict) -> float:
        """Calculate composite priority score (lower = higher priority)"""
        base_priority = work_order.get("priority", PriorityLevel.MEDIUM)
        
        # Due date urgency (0-100 scale)
        due_date = datetime.fromisoformat(work_order["due_date"])
        days_until_due = (due_date - datetime.now()).days
        urgency = max(0, 100 - days_until_due * 5)
        
        # Customer importance weight
        customer_weight = work_order.get("customer_weight", 1.0)
        
        # Quantity factor (larger orders slightly higher priority)
        quantity_factor = min(1.2, 1 + work_order.get("quantity", 0) / 1000)
        
        score = (base_priority * 100 - urgency) / customer_weight / quantity_factor
        return score
    
    def sort_work_orders(self, work_orders: List[Dict]) -> List[Dict]:
        """Sort work orders by priority"""
        for wo in work_orders:
            wo["priority_score"] = self.calculate_priority_score(wo)
        return sorted(work_orders, key=lambda x: x["priority_score"])
```

### API Endpoints

```
POST /scheduling/prioritize             # Calculate priorities
GET  /scheduling/queue                  # Get prioritized queue
PUT  /scheduling/override/{wo_id}       # Manual priority override
```

---

## Testing Stage Definition (Unassigned REQ) ⚠️ **IMPLEMENTATION**

### Test Stage Schema

```python
# src/models/test_stage.py
from sqlalchemy import Column, Integer, String, JSON, Boolean
from src.utils.db import Base

class TestStage(Base):
    __tablename__ = "test_stages"
    
    id = Column(Integer, primary_key=True)
    stage_name = Column(String(100), nullable=False)
    stage_type = Column(String(50))  # functional, stress, burn_in, qa
    duration_sec = Column(Integer)
    required_equipment = Column(JSON)  # ["ICT_TESTER", "THERMAL_CHAMBER"]
    pass_criteria = Column(JSON)
    is_mandatory = Column(Boolean, default=True)
    sequence_order = Column(Integer)

# Test stage definitions
TEST_STAGES = {
    "POST": {
        "type": "functional",
        "duration_sec": 30,
        "equipment": ["POST_TESTER"],
        "criteria": {"bios_boot": True, "memory_detect": True}
    },
    "BURN_IN": {
        "type": "stress",
        "duration_sec": 86400,  # 24 hours
        "equipment": ["BURN_IN_RACK"],
        "criteria": {"temp_stable": True, "no_errors": True}
    },
    "QA_VISUAL": {
        "type": "qa",
        "duration_sec": 120,
        "equipment": [],
        "criteria": {"cosmetic_pass": True, "label_correct": True}
    }
}
```

### API Endpoints

```
GET  /test-stages                       # List all test stages
POST /test-stages                       # Create test stage
GET  /test-stages/{product_family}      # Get stages for product
POST /test-stages/assign                # Assign stages to work order
```

---

## Product Support Matrix (REQ #47b, #48b) ⚠️ **IMPLEMENTATION**

### Product Extension Roadmap Assumptions

| Product Family | Status | Target Phase | Data Files | Notes |
|---------------|--------|--------------|------------|-------|
| DL360 G10 | ✅ Supported | Phase 1 | Available | Base model |
| DL360 G11 | ✅ Supported | Phase 1 | Available | Current |
| DL360 G12 | 🚧 Planned | Phase 1.5 | Pending | REQ #47b |
| ML350 G11 | ✅ Supported | Phase 1 | Available | |
| DL320 G11 | ✅ Supported | Phase 1 | Available | Extra hard |
| DL325 G11 | ✅ Supported | Phase 1 | Available | Extra hard |
| TAO Products | 🚧 Planned | Phase 2+ | Pending | REQ #48b |

### Product Configuration

```python
# src/config/product_support.py
SUPPORTED_PRODUCTS = {
    "DL360_G10": {
        "family": "DL360",
        "generation": "G10",
        "status": "active",
        "complexity": "medium",
        "data_files": ["SWS DL360 G10 (Easy)", "SWS DL360 G10 (Hard)"],
        "variants": ["Easy", "Hard"]
    },
    "DL360_G11": {
        "family": "DL360",
        "generation": "G11",
        "status": "active",
        "complexity": "medium",
        "data_files": ["TOUCHTIME ML350 G11"],
        "variants": ["Assembly", "Kitting", "Packing", "Tests"]
    },
    "DL360_G12": {
        "family": "DL360",
        "generation": "G12",
        "status": "planned",
        "target_release": "2026-Q1",
        "data_files": [],
        "notes": "REQ #47b - Awaiting product data"
    }
}

# Product extension API
async def register_new_product(product_config: Dict) -> Dict:
    """Register a new product for line balance support"""
    required_fields = ["family", "generation", "data_files"]
    # Validate config
    # Add to product registry
    # Trigger data validation
    return {"status": "registered", "product_id": f"{product_config['family']}_{product_config['generation']}"}
```

### API Endpoints

```
GET  /products                          # List supported products
POST /products                          # Register new product
GET  /products/{product_id}/status      # Get product support status
POST /products/{product_id}/data        # Upload product data files
```

---

## 2D Layout Image Management (REQ #18b) ⚠️ **IMPLEMENTATION**

### Image Storage Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  2D Layout Image Management                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Image Upload Service                                 │  │
│  │  - Accept: PNG, JPG, SVG, DXF, DWG                    │  │
│  │  - Max size: 50MB                                     │  │
│  │  - Auto-resize for thumbnails                         │  │
│  └─────────────────────┬─────────────────────────────────┘  │
│                        │                                     │
│  ┌─────────────────────▼─────────────────────────────────┐  │
│  │  Storage Layer                                        │  │
│  │  - S3/MinIO for images                                │  │
│  │  - PostgreSQL for metadata                            │  │
│  │  - Redis for cache                                    │  │
│  └─────────────────────┬─────────────────────────────────┘  │
│                        │                                     │
│  ┌─────────────────────▼─────────────────────────────────┐  │
│  │  Layout Overlay Service                               │  │
│  │  - Station hotspots on image                          │  │
│  │  - Clickable regions                                  │  │
│  │  - Real-time status overlay                           │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Database Schema

```sql
CREATE TABLE layout_images (
    id SERIAL PRIMARY KEY,
    site_id VARCHAR(50) NOT NULL,
    layout_name VARCHAR(100) NOT NULL,
    image_url VARCHAR(500) NOT NULL,
    thumbnail_url VARCHAR(500),
    file_type VARCHAR(10),
    file_size_bytes INTEGER,
    dimensions JSONB,  -- {"width": 1920, "height": 1080}
    scale_factor FLOAT,  -- pixels per meter
    station_hotspots JSONB,  -- [{"station_id": 1, "x": 100, "y": 200, "radius": 30}]
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    created_by VARCHAR(100)
);
```

### API Endpoints

```
POST /layouts/images/upload             # Upload layout image
GET  /layouts/images/{site_id}          # Get layout images for site
PUT  /layouts/images/{image_id}/hotspots  # Update station hotspots
DELETE /layouts/images/{image_id}       # Delete layout image
```

---

## Station Type Configuration (REQ #46b) ⚠️ **IMPLEMENTATION**

### Station Type Definitions

```python
# src/models/station_type.py
from enum import Enum
from typing import Dict

class StationType(Enum):
    FIXED = "fixed"           # Single-person, fixed workload
    ADJUSTABLE = "adjustable"  # Flexible workload, can absorb overflow
    MULTI_PERSON = "multi_person"  # Designed for multiple workers
    AUTOMATED = "automated"    # Robot/machine station
    HYBRID = "hybrid"          # Human + automation

STATION_TYPE_CONFIG = {
    StationType.FIXED: {
        "max_workers": 1,
        "can_absorb_overflow": False,
        "parallel_tasks": False,
        "requires_certification": False
    },
    StationType.ADJUSTABLE: {
        "max_workers": 4,
        "can_absorb_overflow": True,
        "parallel_tasks": False,
        "requires_certification": False
    },
    StationType.MULTI_PERSON: {
        "max_workers": 8,
        "can_absorb_overflow": True,
        "parallel_tasks": True,
        "requires_certification": True
    },
    StationType.AUTOMATED: {
        "max_workers": 0,
        "can_absorb_overflow": False,
        "parallel_tasks": True,
        "requires_certification": False,
        "requires_maintenance_schedule": True
    },
    StationType.HYBRID: {
        "max_workers": 2,
        "can_absorb_overflow": True,
        "parallel_tasks": True,
        "requires_certification": True
    }
}
```

### CSV Extension

Add to `config.csv`:
```csv
parameter,value
station_1_type,fixed
station_2_type,adjustable
station_3_type,multi_person
station_4_type,automated
```

### API Endpoints

```
GET  /stations/types                    # List station types
PUT  /stations/{station_id}/type        # Set station type
GET  /stations/{site_id}/config         # Get station configuration
```

---

## Per-Site Station Configuration (REQ #41) ⚠️ **IMPLEMENTATION**

### Site-Station Configuration Workflow

```
┌─────────────────────────────────────────────────────────────┐
│              Per-Site Station Configuration                  │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  Site Configuration Manager                           │  │
│  │  - Define stations per site                           │  │
│  │  - Set station types, capacities                      │  │
│  │  - Configure equipment assignments                    │  │
│  └─────────────────────┬─────────────────────────────────┘  │
│                        │                                     │
│  ┌─────────────────────▼─────────────────────────────────┐  │
│  │  Station Template Library                             │  │
│  │  - Pre-defined station templates                      │  │
│  │  - Copy from other sites                              │  │
│  │  - Bulk import/export                                 │  │
│  └─────────────────────┬─────────────────────────────────┘  │
│                        │                                     │
│  ┌─────────────────────▼─────────────────────────────────┐  │
│  │  Validation & Constraints                             │  │
│  │  - Equipment availability check                       │  │
│  │  - Worker capacity validation                         │  │
│  │  - Layout consistency check                           │  │
│  └───────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Database Schema

```sql
CREATE TABLE site_station_configs (
    id SERIAL PRIMARY KEY,
    site_id VARCHAR(50) NOT NULL,
    station_id VARCHAR(50) NOT NULL,
    station_name VARCHAR(100),
    station_type VARCHAR(20) NOT NULL,
    max_workers INTEGER DEFAULT 1,
    equipment_ids JSONB,  -- ["TORQUE_DRV_01", "SCANNER_02"]
    position JSONB,  -- {"x": 100, "y": 200, "rotation": 0}
    dimensions JSONB,  -- {"width": 2.0, "depth": 1.5}
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(site_id, station_id)
);
```

### API Endpoints

```
GET  /sites/{site_id}/stations          # List stations for site
POST /sites/{site_id}/stations          # Add station to site
PUT  /sites/{site_id}/stations/{station_id}  # Update station config
DELETE /sites/{site_id}/stations/{station_id}  # Remove station
POST /sites/{site_id}/stations/import   # Bulk import stations
GET  /sites/{site_id}/stations/export   # Export station config
POST /sites/{site_id}/stations/copy-from/{source_site_id}  # Copy from another site
```

---

## Skill & Manpower Mapping (Unassigned REQ) ⚠️ **IMPLEMENTATION**

### Worker Skill Model

```python
# src/models/worker_skill.py
from sqlalchemy import Column, Integer, String, JSON, Boolean, ForeignKey
from src.utils.db import Base

class WorkerSkill(Base):
    __tablename__ = "worker_skills"
    
    id = Column(Integer, primary_key=True)
    worker_id = Column(String(50), nullable=False)
    skill_code = Column(String(50), nullable=False)  # SOLDERING, IPC_610, ESD
    proficiency_level = Column(Integer)  # 1-5
    certified = Column(Boolean, default=False)
    certification_date = Column(DateTime)
    expiry_date = Column(DateTime)

class TaskSkillRequirement(Base):
    __tablename__ = "task_skill_requirements"
    
    id = Column(Integer, primary_key=True)
    task_id = Column(Integer, ForeignKey("tasks.id"))
    skill_code = Column(String(50), nullable=False)
    min_proficiency = Column(Integer, default=1)
    is_mandatory = Column(Boolean, default=True)
```

### Skill Matching Service

```python
# src/services/skill_matcher.py
class SkillMatcher:
    """Match workers to tasks based on skills"""
    
    def find_qualified_workers(
        self, 
        task_id: int, 
        available_workers: List[str]
    ) -> List[Dict]:
        """Find workers qualified for a task"""
        requirements = self.get_task_requirements(task_id)
        qualified = []
        for worker_id in available_workers:
            skills = self.get_worker_skills(worker_id)
            if self._meets_requirements(skills, requirements):
                qualified.append({
                    "worker_id": worker_id,
                    "match_score": self._calculate_match_score(skills, requirements)
                })
        return sorted(qualified, key=lambda x: x["match_score"], reverse=True)
    
    def get_skill_gaps(self, site_id: str) -> Dict:
        """Identify skill gaps at a site"""
        required_skills = self.get_site_required_skills(site_id)
        available_skills = self.get_site_available_skills(site_id)
        gaps = []
        for skill, count_needed in required_skills.items():
            count_available = available_skills.get(skill, 0)
            if count_available < count_needed:
                gaps.append({
                    "skill": skill,
                    "needed": count_needed,
                    "available": count_available,
                    "gap": count_needed - count_available
                })
        return {"gaps": gaps, "training_recommendations": self._recommend_training(gaps)}
```

### API Endpoints

```
GET  /workers/{worker_id}/skills        # Get worker skills
POST /workers/{worker_id}/skills        # Add skill to worker
GET  /tasks/{task_id}/skill-requirements  # Get task requirements
POST /skill-matching/qualified-workers  # Find qualified workers
GET  /sites/{site_id}/skill-gaps        # Identify skill gaps
```

---

## Production Scheduling with Gantt Output ⚠️ **IMPLEMENTATION**

### Overview

Detailed production scheduling with start/end time estimation per work order and Gantt chart data format for visualization.

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   Production Scheduling Flow                                │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Input:                                                               │  │
│  │    - Work Orders with quantities & due dates                          │  │
│  │    - Line capacity (UPH per line)                                     │  │
│  │    - Available shifts & hours                                         │  │
│  │    - Priority constraints                                             │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                               │                                             │
│                               ▼                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Scheduling Engine                                                    │  │
│  │    - Sort by priority + due date                                      │  │
│  │    - Allocate to lines based on capacity                              │  │
│  │    - Calculate start/end times                                        │  │
│  │    - Handle changeover times                                          │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                               │                                             │
│                               ▼                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Output:                                                              │  │
│  │    - Gantt chart data (JSON)                                          │  │
│  │    - Work order timeline                                              │  │
│  │    - Resource utilization                                             │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Data Models

```python
from datetime import datetime, timedelta
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class ScheduleStatus(str, Enum):
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    DELAYED = "delayed"
    ON_HOLD = "on_hold"

class WorkOrderSchedule(BaseModel):
    work_order_id: str
    product_sku: str
    quantity: int
    line_id: str
    
    # Timing
    scheduled_start: datetime
    scheduled_end: datetime
    actual_start: Optional[datetime] = None
    actual_end: Optional[datetime] = None
    
    # Duration breakdown
    setup_time_minutes: int = 0
    production_time_minutes: int
    changeover_time_minutes: int = 0
    
    # Status
    status: ScheduleStatus = ScheduleStatus.SCHEDULED
    completion_percentage: float = 0.0

class GanttTask(BaseModel):
    """Single task for Gantt chart rendering"""
    id: str
    name: str
    resource: str  # Line ID
    start: datetime
    end: datetime
    progress: float  # 0-100
    dependencies: List[str] = []
    color: Optional[str] = None
    tooltip: Optional[str] = None

class GanttChartData(BaseModel):
    """Complete Gantt chart data structure"""
    tasks: List[GanttTask]
    resources: List[dict]  # Lines/stations
    time_range: dict  # {start, end}
    metadata: dict
```

### Scheduling Service

```python
# src/services/production_scheduler.py
from datetime import datetime, timedelta
from typing import List, Dict

class ProductionScheduler:
    """Schedule work orders and generate Gantt data"""
    
    def __init__(self, site_config: dict):
        self.site_config = site_config
        self.shift_hours = site_config.get("shift_hours", 8)
        self.shifts_per_day = site_config.get("shifts_per_day", 2)
        self.changeover_minutes = site_config.get("default_changeover", 30)
    
    def schedule_work_orders(
        self,
        work_orders: List[dict],
        lines: List[dict],
        start_date: datetime
    ) -> List[WorkOrderSchedule]:
        """Schedule work orders across available lines"""
        
        # Sort by priority (critical first) then due date
        sorted_orders = sorted(
            work_orders,
            key=lambda x: (
                -self._priority_value(x.get("priority", "medium")),
                x.get("due_date", datetime.max)
            )
        )
        
        # Track line availability
        line_availability = {
            line["line_id"]: start_date for line in lines
        }
        
        schedules = []
        for order in sorted_orders:
            # Find best line (earliest available)
            best_line = min(line_availability, key=line_availability.get)
            line_start = line_availability[best_line]
            
            # Get line capacity
            line_uph = next(
                l["uph"] for l in lines if l["line_id"] == best_line
            )
            
            # Calculate production time
            production_hours = order["quantity"] / line_uph
            production_minutes = int(production_hours * 60)
            
            # Calculate end time (respecting shift boundaries)
            end_time = self._calculate_end_time(
                line_start,
                production_minutes + self.changeover_minutes
            )
            
            schedule = WorkOrderSchedule(
                work_order_id=order["work_order_id"],
                product_sku=order["sku"],
                quantity=order["quantity"],
                line_id=best_line,
                scheduled_start=line_start,
                scheduled_end=end_time,
                production_time_minutes=production_minutes,
                changeover_time_minutes=self.changeover_minutes
            )
            schedules.append(schedule)
            
            # Update line availability
            line_availability[best_line] = end_time
        
        return schedules
    
    def generate_gantt_data(
        self,
        schedules: List[WorkOrderSchedule]
    ) -> GanttChartData:
        """Convert schedules to Gantt chart format"""
        
        tasks = []
        for schedule in schedules:
            task = GanttTask(
                id=schedule.work_order_id,
                name=f"{schedule.work_order_id} ({schedule.product_sku})",
                resource=schedule.line_id,
                start=schedule.scheduled_start,
                end=schedule.scheduled_end,
                progress=schedule.completion_percentage,
                color=self._status_color(schedule.status),
                tooltip=f"Qty: {schedule.quantity}, Duration: {schedule.production_time_minutes}min"
            )
            tasks.append(task)
        
        # Extract unique resources
        resources = [
            {"id": r, "name": f"Line {r}"} 
            for r in set(s.line_id for s in schedules)
        ]
        
        # Calculate time range
        if schedules:
            time_range = {
                "start": min(s.scheduled_start for s in schedules),
                "end": max(s.scheduled_end for s in schedules)
            }
        else:
            time_range = {"start": datetime.now(), "end": datetime.now()}
        
        return GanttChartData(
            tasks=tasks,
            resources=resources,
            time_range=time_range,
            metadata={"total_orders": len(schedules)}
        )
    
    def _priority_value(self, priority: str) -> int:
        return {"critical": 4, "high": 3, "medium": 2, "low": 1}.get(priority, 2)
    
    def _status_color(self, status: ScheduleStatus) -> str:
        colors = {
            ScheduleStatus.SCHEDULED: "#3498db",
            ScheduleStatus.IN_PROGRESS: "#f39c12",
            ScheduleStatus.COMPLETED: "#27ae60",
            ScheduleStatus.DELAYED: "#e74c3c",
            ScheduleStatus.ON_HOLD: "#95a5a6"
        }
        return colors.get(status, "#3498db")
    
    def _calculate_end_time(
        self, 
        start: datetime, 
        duration_minutes: int
    ) -> datetime:
        """Calculate end time respecting shift boundaries"""
        # Simplified: add duration directly
        # Production implementation should handle shift breaks
        return start + timedelta(minutes=duration_minutes)
```

### API Endpoints

```yaml
POST /production-schedule:
  description: Generate production schedule for work orders
  request:
    site_id: string
    work_orders:
      - work_order_id: string
        sku: string
        quantity: integer
        due_date: date
        priority: string
    start_date: datetime
  response:
    schedules: WorkOrderSchedule[]
    gantt_data: GanttChartData
    summary:
      total_orders: integer
      total_production_hours: float
      utilization_by_line: object

GET /production-schedule/{site_id}/gantt:
  description: Get Gantt chart data for site
  parameters:
    start_date: date
    end_date: date
    line_ids: string[] (optional)
  response:
    gantt_data: GanttChartData

PUT /production-schedule/{work_order_id}:
  description: Update schedule status
  request:
    status: ScheduleStatus
    actual_start: datetime (optional)
    actual_end: datetime (optional)
```

### Gantt Chart JSON Output Example

```json
{
  "tasks": [
    {
      "id": "WO_001",
      "name": "WO_001 (DL360-G11-001)",
      "resource": "LINE_A",
      "start": "2025-12-15T08:00:00Z",
      "end": "2025-12-15T16:30:00Z",
      "progress": 0,
      "color": "#3498db",
      "tooltip": "Qty: 150, Duration: 480min"
    },
    {
      "id": "WO_002",
      "name": "WO_002 (DL360-G11-002)",
      "resource": "LINE_A",
      "start": "2025-12-15T17:00:00Z",
      "end": "2025-12-16T09:30:00Z",
      "progress": 0,
      "color": "#3498db",
      "tooltip": "Qty: 200, Duration: 600min"
    }
  ],
  "resources": [
    {"id": "LINE_A", "name": "Line A"},
    {"id": "LINE_B", "name": "Line B"}
  ],
  "time_range": {
    "start": "2025-12-15T08:00:00Z",
    "end": "2025-12-20T18:00:00Z"
  },
  "metadata": {
    "total_orders": 2,
    "generated_at": "2025-12-13T10:00:00Z"
  }
}
```

---

## Equipment Availability & Monitoring ⚠️ **IMPLEMENTATION**

### Overview

Track equipment idle rate, cycle time per machine, and real-time equipment status for capacity planning.

### Data Models

```python
from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List
from enum import Enum

class EquipmentStatus(str, Enum):
    RUNNING = "running"
    IDLE = "idle"
    MAINTENANCE = "maintenance"
    BREAKDOWN = "breakdown"
    SETUP = "setup"

class Equipment(BaseModel):
    equipment_id: str
    equipment_type: str  # conveyor, robot, tester, etc.
    station_code: str
    line_id: str
    
    # Capacity
    rated_cycle_time_seconds: float
    actual_cycle_time_seconds: Optional[float] = None
    
    # Availability
    status: EquipmentStatus = EquipmentStatus.IDLE
    last_status_change: datetime
    
    # Metrics (rolling 24h)
    idle_rate_pct: float = 0.0
    utilization_pct: float = 0.0
    oee_pct: float = 0.0  # Overall Equipment Effectiveness

class EquipmentMetrics(BaseModel):
    equipment_id: str
    timestamp: datetime
    
    # Time breakdown (minutes in last hour)
    running_time: float
    idle_time: float
    maintenance_time: float
    breakdown_time: float
    
    # Performance
    cycle_count: int
    avg_cycle_time: float
    min_cycle_time: float
    max_cycle_time: float
    
    # Derived
    idle_rate: float  # idle_time / total_time
    performance_rate: float  # rated_cycle / actual_cycle
```

### Equipment Monitoring Service

```python
# src/services/equipment_monitor.py
from datetime import datetime, timedelta
from typing import Dict, List

class EquipmentMonitor:
    """Monitor equipment status and calculate availability metrics"""
    
    def __init__(self, db_session):
        self.db = db_session
    
    def get_equipment_status(self, equipment_id: str) -> Equipment:
        """Get current equipment status"""
        # Query from database
        pass
    
    def update_status(
        self, 
        equipment_id: str, 
        new_status: EquipmentStatus,
        reason: Optional[str] = None
    ):
        """Update equipment status and log transition"""
        equipment = self.get_equipment_status(equipment_id)
        old_status = equipment.status
        
        # Log status transition
        self._log_status_change(equipment_id, old_status, new_status, reason)
        
        # Update current status
        equipment.status = new_status
        equipment.last_status_change = datetime.now()
        self.db.commit()
    
    def calculate_metrics(
        self, 
        equipment_id: str, 
        period_hours: int = 24
    ) -> EquipmentMetrics:
        """Calculate equipment metrics for time period"""
        
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=period_hours)
        
        # Get status logs for period
        logs = self._get_status_logs(equipment_id, start_time, end_time)
        
        # Calculate time in each status
        time_breakdown = self._calculate_time_breakdown(logs, start_time, end_time)
        total_time = sum(time_breakdown.values())
        
        # Get cycle data
        cycles = self._get_cycle_data(equipment_id, start_time, end_time)
        
        return EquipmentMetrics(
            equipment_id=equipment_id,
            timestamp=end_time,
            running_time=time_breakdown.get("running", 0),
            idle_time=time_breakdown.get("idle", 0),
            maintenance_time=time_breakdown.get("maintenance", 0),
            breakdown_time=time_breakdown.get("breakdown", 0),
            cycle_count=len(cycles),
            avg_cycle_time=sum(cycles) / len(cycles) if cycles else 0,
            min_cycle_time=min(cycles) if cycles else 0,
            max_cycle_time=max(cycles) if cycles else 0,
            idle_rate=time_breakdown.get("idle", 0) / total_time if total_time > 0 else 0,
            performance_rate=self._calculate_performance_rate(equipment_id, cycles)
        )
    
    def get_line_availability(self, line_id: str) -> Dict:
        """Get aggregated availability for all equipment on a line"""
        equipment_list = self._get_line_equipment(line_id)
        
        metrics = []
        for eq in equipment_list:
            metrics.append(self.calculate_metrics(eq.equipment_id))
        
        return {
            "line_id": line_id,
            "equipment_count": len(equipment_list),
            "avg_idle_rate": sum(m.idle_rate for m in metrics) / len(metrics) if metrics else 0,
            "avg_utilization": 1 - sum(m.idle_rate for m in metrics) / len(metrics) if metrics else 0,
            "bottleneck_equipment": max(metrics, key=lambda m: m.avg_cycle_time).equipment_id if metrics else None,
            "equipment_metrics": metrics
        }
    
    def _calculate_performance_rate(self, equipment_id: str, cycles: List[float]) -> float:
        """Calculate performance rate vs rated cycle time"""
        equipment = self.get_equipment_status(equipment_id)
        if not cycles or not equipment.rated_cycle_time_seconds:
            return 0.0
        avg_actual = sum(cycles) / len(cycles)
        return equipment.rated_cycle_time_seconds / avg_actual if avg_actual > 0 else 0
```

### API Endpoints

```yaml
GET /equipment/{equipment_id}:
  description: Get equipment details and current status
  response:
    equipment: Equipment
    current_metrics: EquipmentMetrics

PUT /equipment/{equipment_id}/status:
  description: Update equipment status
  request:
    status: EquipmentStatus
    reason: string (optional)
  response:
    success: boolean
    previous_status: EquipmentStatus

GET /equipment/{equipment_id}/metrics:
  description: Get equipment metrics for time period
  parameters:
    period_hours: integer (default: 24)
  response:
    metrics: EquipmentMetrics
    trend: object  # Comparison with previous period

GET /lines/{line_id}/equipment-availability:
  description: Get aggregated equipment availability for line
  response:
    line_id: string
    equipment_count: integer
    avg_idle_rate: float
    avg_utilization: float
    bottleneck_equipment: string
    equipment_list: Equipment[]

POST /equipment/cycle-complete:
  description: Record equipment cycle completion (from MES/PLC)
  request:
    equipment_id: string
    cycle_time_seconds: float
    timestamp: datetime
    unit_id: string (optional)
```

### Database Schema

```sql
CREATE TABLE equipment (
    id SERIAL PRIMARY KEY,
    equipment_id VARCHAR(50) UNIQUE NOT NULL,
    equipment_type VARCHAR(50) NOT NULL,
    station_code VARCHAR(50),
    line_id VARCHAR(50),
    rated_cycle_time_seconds DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'idle',
    last_status_change TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE equipment_status_log (
    id SERIAL PRIMARY KEY,
    equipment_id VARCHAR(50) REFERENCES equipment(equipment_id),
    old_status VARCHAR(20),
    new_status VARCHAR(20),
    reason TEXT,
    changed_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE equipment_cycles (
    id SERIAL PRIMARY KEY,
    equipment_id VARCHAR(50) REFERENCES equipment(equipment_id),
    cycle_time_seconds DECIMAL(10,3),
    unit_id VARCHAR(50),
    recorded_at TIMESTAMP DEFAULT NOW()
);

-- Index for time-series queries
CREATE INDEX idx_equipment_cycles_time ON equipment_cycles(equipment_id, recorded_at);
```

---

## Raw Material Availability (MRP/WMS Integration) ⚠️ **IMPLEMENTATION** (Placeholder)

### Overview

Integration stub for MRP (Material Requirements Planning) and WMS (Warehouse Management System) to check raw material availability and procurement status.

### Integration Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   Raw Material Integration (Stub)                           │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Line Balance System                                                  │  │
│  │    └─→ Material Availability Adapter                                  │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                               │                                             │
│               ┌───────────────┴───────────────┐                             │
│               ▼                               ▼                             │
│  ┌─────────────────────────┐     ┌─────────────────────────┐               │
│  │  MRP System (External)  │     │  WMS System (External)  │               │
│  │  - SAP MM              │     │  - Oracle WMS           │               │
│  │  - Oracle MRP          │     │  - Manhattan WMS        │               │
│  │  - Custom ERP          │     │  - Custom WMS           │               │
│  └─────────────────────────┘     └─────────────────────────┘               │
│                                                                             │
│  Note: Actual integration requires customer-specific configuration          │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Data Models

```python
from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from enum import Enum

class ProcurementStatus(str, Enum):
    AVAILABLE = "available"        # In stock
    ORDERED = "ordered"            # PO created, awaiting delivery
    IN_TRANSIT = "in_transit"      # Shipped, en route
    PARTIAL = "partial"            # Partial quantity available
    NOT_AVAILABLE = "not_available"  # Not in stock, no PO

class MaterialAvailability(BaseModel):
    material_id: str
    material_name: str
    unit_of_measure: str
    
    # Quantity
    required_quantity: float
    available_quantity: float
    shortage_quantity: float
    
    # Procurement
    procurement_status: ProcurementStatus
    expected_delivery_date: Optional[date] = None
    
    # Impact
    can_start_production: bool
    blocking_reason: Optional[str] = None

class BOMComponent(BaseModel):
    """Bill of Materials component"""
    component_id: str
    component_name: str
    quantity_per_unit: float
    lead_time_days: int
    availability: Optional[MaterialAvailability] = None
```

### Material Availability Adapter (Stub)

```python
# src/adapters/material_adapter.py
from typing import List, Dict, Optional
from abc import ABC, abstractmethod

class MaterialAdapterBase(ABC):
    """Base class for MRP/WMS integration adapters"""
    
    @abstractmethod
    def check_availability(
        self, 
        material_ids: List[str], 
        quantities: Dict[str, float],
        site_id: str
    ) -> List[MaterialAvailability]:
        """Check material availability for production"""
        pass
    
    @abstractmethod
    def get_procurement_status(
        self, 
        material_id: str
    ) -> ProcurementStatus:
        """Get current procurement status"""
        pass

class StubMaterialAdapter(MaterialAdapterBase):
    """
    Stub adapter for development/testing.
    Replace with actual MRP/WMS integration in production.
    """
    
    def __init__(self, config: dict):
        self.config = config
        # Simulated inventory data
        self._mock_inventory = {
            "MAT_001": {"available": 1000, "status": "available"},
            "MAT_002": {"available": 50, "status": "partial"},
            "MAT_003": {"available": 0, "status": "ordered", "eta": "2025-12-20"},
        }
    
    def check_availability(
        self, 
        material_ids: List[str], 
        quantities: Dict[str, float],
        site_id: str
    ) -> List[MaterialAvailability]:
        """Stub: Return mock availability data"""
        results = []
        for mat_id in material_ids:
            inv = self._mock_inventory.get(mat_id, {"available": 0, "status": "not_available"})
            required = quantities.get(mat_id, 0)
            available = inv["available"]
            
            results.append(MaterialAvailability(
                material_id=mat_id,
                material_name=f"Material {mat_id}",
                unit_of_measure="EA",
                required_quantity=required,
                available_quantity=available,
                shortage_quantity=max(0, required - available),
                procurement_status=ProcurementStatus(inv["status"]),
                expected_delivery_date=inv.get("eta"),
                can_start_production=available >= required,
                blocking_reason="Insufficient inventory" if available < required else None
            ))
        
        return results
    
    def get_procurement_status(self, material_id: str) -> ProcurementStatus:
        """Stub: Return mock procurement status"""
        inv = self._mock_inventory.get(material_id, {})
        return ProcurementStatus(inv.get("status", "not_available"))

# Factory function for adapter selection
def get_material_adapter(adapter_type: str, config: dict) -> MaterialAdapterBase:
    """
    Factory to create appropriate material adapter.
    
    Supported types:
    - 'stub': Development/testing stub
    - 'sap': SAP MM integration (TODO)
    - 'oracle': Oracle MRP integration (TODO)
    - 'custom': Custom ERP integration (TODO)
    """
    adapters = {
        "stub": StubMaterialAdapter,
        # Future integrations:
        # "sap": SAPMaterialAdapter,
        # "oracle": OracleMaterialAdapter,
    }
    
    adapter_class = adapters.get(adapter_type, StubMaterialAdapter)
    return adapter_class(config)
```

### API Endpoints

```yaml
POST /materials/check-availability:
  description: Check material availability for work order
  request:
    work_order_id: string
    bom_components:
      - component_id: string
        quantity_required: float
    site_id: string
  response:
    work_order_id: string
    overall_status: string  # ready, partial, blocked
    material_availability: MaterialAvailability[]
    blocking_materials: string[]
    earliest_start_date: date

GET /materials/{material_id}/status:
  description: Get material procurement status
  response:
    material_id: string
    procurement_status: ProcurementStatus
    available_quantity: float
    pending_orders: object[]
    expected_deliveries: object[]
```

### Integration Configuration

```yaml
# config/integrations.yaml
material_integration:
  adapter_type: "stub"  # Change to 'sap', 'oracle', etc. for production
  
  # SAP MM configuration (placeholder)
  sap:
    host: "sap-server.example.com"
    client: "100"
    username: "${SAP_USERNAME}"
    password: "${SAP_PASSWORD}"
    rfc_function: "BAPI_MATERIAL_AVAILABILITY"
  
  # Oracle MRP configuration (placeholder)
  oracle:
    connection_string: "${ORACLE_CONN_STRING}"
    schema: "MRP"
    availability_query: "SELECT * FROM material_availability WHERE ..."
```

---

## MES Real-Time Integration ⚠️ **IMPLEMENTATION**

### Overview

Define MES data JSON schema and WebSocket/MQTT protocol for real-time production data integration.

### Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   MES Integration Architecture                              │
│                                                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  MES / SCADA Systems                                                │    │
│  │  - Ignition, Wonderware, AVEVA                                      │    │
│  │  - Custom PLC integrations                                          │    │
│  └────────────────────────────┬────────────────────────────────────────┘    │
│                               │ MQTT / OPC-UA                               │
│                               ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Message Broker                                                     │    │
│  │  - MQTT Broker (Mosquitto, HiveMQ)                                  │    │
│  │  - Kafka (for high-volume)                                          │    │
│  └────────────────────────────┬────────────────────────────────────────┘    │
│                               │                                             │
│                               ▼                                             │
│  ┌─────────────────────────────────────────────────────────────────────┐    │
│  │  Line Balance MES Adapter                                           │    │
│  │  - Message parsing & validation                                     │    │
│  │  - Data normalization                                               │    │
│  │  - Event routing                                                    │    │
│  └────────────────────────────┬────────────────────────────────────────┘    │
│                               │                                             │
│               ┌───────────────┼───────────────┐                             │
│               ▼               ▼               ▼                             │
│  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐               │
│  │ Cycle Time      │ │ Equipment       │ │ Production      │               │
│  │ Tracking        │ │ Status          │ │ Counts          │               │
│  └─────────────────┘ └─────────────────┘ └─────────────────┘               │
│                                                                             │
│  WebSocket → Frontend Dashboard (Real-time updates)                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### MES Data JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "MES Event Schema",
  "type": "object",
  "required": ["event_type", "timestamp", "source_id", "payload"],
  "properties": {
    "event_type": {
      "type": "string",
      "enum": [
        "cycle_complete",
        "unit_started",
        "unit_completed",
        "equipment_status_change",
        "quality_check",
        "defect_reported",
        "station_alarm"
      ]
    },
    "timestamp": {
      "type": "string",
      "format": "date-time"
    },
    "source_id": {
      "type": "string",
      "description": "Station or equipment identifier"
    },
    "site_id": {
      "type": "string"
    },
    "line_id": {
      "type": "string"
    },
    "payload": {
      "type": "object",
      "description": "Event-specific data"
    }
  }
}
```

### Event Payload Schemas

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

class CycleCompletePayload(BaseModel):
    """Payload for cycle_complete event"""
    station_code: str
    cycle_time_seconds: float
    unit_id: str
    work_order_id: str
    operator_id: Optional[str] = None
    
class UnitStartedPayload(BaseModel):
    """Payload for unit_started event"""
    station_code: str
    unit_id: str
    work_order_id: str
    expected_cycle_time: Optional[float] = None

class UnitCompletedPayload(BaseModel):
    """Payload for unit_completed event"""
    station_code: str
    unit_id: str
    work_order_id: str
    total_cycle_time: float
    passed_quality: bool
    
class EquipmentStatusPayload(BaseModel):
    """Payload for equipment_status_change event"""
    equipment_id: str
    previous_status: str
    new_status: str
    reason_code: Optional[str] = None
    reason_text: Optional[str] = None

class QualityCheckPayload(BaseModel):
    """Payload for quality_check event"""
    unit_id: str
    check_type: str  # visual, measurement, functional
    result: str  # pass, fail, rework
    measurements: Optional[Dict[str, Any]] = None
    defect_codes: Optional[list] = None
```

### MQTT Protocol

```yaml
# MQTT Topic Structure
topics:
  # Production events (from MES)
  mes/production/{site_id}/{line_id}/cycle:
    description: Cycle completion events
    qos: 1
    payload: CycleCompletePayload
    
  mes/production/{site_id}/{line_id}/unit:
    description: Unit tracking events
    qos: 1
    payload: UnitStartedPayload | UnitCompletedPayload
    
  mes/equipment/{site_id}/{equipment_id}/status:
    description: Equipment status changes
    qos: 1
    payload: EquipmentStatusPayload
    retain: true  # Keep last status
    
  mes/quality/{site_id}/{line_id}/check:
    description: Quality check results
    qos: 1
    payload: QualityCheckPayload
    
  # Commands (to MES)
  linebalance/command/{site_id}/{line_id}:
    description: Commands from Line Balance to MES
    qos: 2
    payload:
      command: string  # start_order, pause_line, etc.
      parameters: object
```

### WebSocket Protocol (Frontend)

```python
# src/websocket/mes_handler.py
from fastapi import WebSocket
from typing import Dict, Set
import json

class MESWebSocketManager:
    """Manage WebSocket connections for MES real-time data"""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, site_id: str):
        await websocket.accept()
        if site_id not in self.active_connections:
            self.active_connections[site_id] = set()
        self.active_connections[site_id].add(websocket)
    
    async def disconnect(self, websocket: WebSocket, site_id: str):
        self.active_connections[site_id].discard(websocket)
    
    async def broadcast_to_site(self, site_id: str, message: dict):
        """Broadcast MES event to all connected clients for a site"""
        if site_id in self.active_connections:
            for connection in self.active_connections[site_id]:
                await connection.send_json(message)
    
    async def process_mes_event(self, event: dict):
        """Process incoming MES event and broadcast to frontend"""
        site_id = event.get("site_id")
        
        # Transform to frontend format
        frontend_message = {
            "type": event["event_type"],
            "timestamp": event["timestamp"],
            "data": event["payload"],
            "source": event["source_id"]
        }
        
        await self.broadcast_to_site(site_id, frontend_message)

# FastAPI WebSocket endpoint
mes_manager = MESWebSocketManager()

@app.websocket("/ws/mes/{site_id}")
async def mes_websocket(websocket: WebSocket, site_id: str):
    await mes_manager.connect(websocket, site_id)
    try:
        while True:
            # Keep connection alive, receive any client messages
            data = await websocket.receive_text()
            # Handle client commands if needed
    except WebSocketDisconnect:
        await mes_manager.disconnect(websocket, site_id)
```

### API Endpoints

```yaml
POST /mes/events:
  description: Receive MES events (webhook endpoint)
  request:
    events: MESEvent[]
  response:
    received: integer
    processed: integer
    errors: string[]

GET /mes/status/{site_id}:
  description: Get current MES connection status
  response:
    connected: boolean
    last_event: datetime
    event_rate: float  # events per minute
    connection_health: string

WebSocket /ws/mes/{site_id}:
  description: Real-time MES event stream
  messages:
    - type: cycle_complete
    - type: equipment_status
    - type: production_count
```

---

## MES CTO/BTO Work Order Integration ⚠️ **PLACEHOLDER**

### Overview

Integration specification for Configure-to-Order (CTO) and Build-to-Order (BTO) work orders from MES systems. This integration enables the Line Balance system to understand product variants, customization options, and their impact on cycle times.

**Phase Assignment:** Phase 3 - External Integration  
**Implementation Priority:** Medium  
**Target Sprint:** Sprint 6-7 (Phase 3)  
**Status:** Placeholder - Awaiting MES API specification

### CTO/BTO Work Order Data Model

```python
# src/models/cto_bto_work_order.py
from pydantic import BaseModel, Field
from typing import Dict, List, Optional
from enum import Enum
from datetime import datetime

class ProductType(str, Enum):
    """Product type classification"""
    STANDARD = "standard"       # Build-to-Stock (BTS)
    CTO = "cto"                 # Configure-to-Order
    BTO = "bto"                 # Build-to-Order
    ETO = "eto"                 # Engineer-to-Order

class OptionCategory(str, Enum):
    """Component option categories for CTO/BTO"""
    CPU = "cpu"
    MEMORY = "memory"
    STORAGE = "storage"
    GPU = "gpu"
    POWER_SUPPLY = "power_supply"
    CHASSIS = "chassis"
    NIC = "network_interface"
    RAILS = "rails"
    SOFTWARE = "software"
    CUSTOM = "custom"

class ComponentOption(BaseModel):
    """Single component option for CTO/BTO configuration"""
    option_id: str
    option_code: str
    description: str
    category: OptionCategory
    cycle_time_delta_seconds: float = 0.0  # Added CT vs base model
    special_tools_required: List[str] = []
    skill_level_required: int = 1  # 1-5 scale
    is_default: bool = False

class CTOBTOConfiguration(BaseModel):
    """Complete CTO/BTO configuration for a work order"""
    config_id: str
    base_product_id: str
    base_product_name: str
    product_type: ProductType
    
    # Selected options
    selected_options: Dict[OptionCategory, ComponentOption]
    
    # Calculated fields
    total_cycle_time_delta: float = 0.0  # Sum of all option deltas
    total_additional_tools: List[str] = []
    max_skill_level_required: int = 1
    
    def calculate_adjusted_cycle_time(self, base_ct: float) -> float:
        """Calculate total CT including all option deltas"""
        return base_ct + self.total_cycle_time_delta

class CTOBTOWorkOrder(BaseModel):
    """Work order with CTO/BTO configuration from MES"""
    work_order_id: str
    work_order_number: str
    customer_id: Optional[str] = None
    customer_name: Optional[str] = None
    
    # Product configuration
    configuration: CTOBTOConfiguration
    
    # Scheduling
    quantity: int = 1
    priority: int = 5  # 1=highest, 10=lowest
    due_date: Optional[datetime] = None
    
    # MES metadata
    mes_system_id: str
    mes_work_order_status: str
    received_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Line Balance fields
    assigned_line_id: Optional[str] = None
    estimated_completion: Optional[datetime] = None
    adjusted_cycle_time: Optional[float] = None
```

### MES CTO/BTO Data Schema (Placeholder)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "MES CTO/BTO Work Order",
  "description": "Placeholder schema for MES work order with CTO/BTO configuration",
  "type": "object",
  "required": ["work_order_id", "product_type", "base_product"],
  "properties": {
    "work_order_id": {
      "type": "string",
      "description": "Unique work order identifier from MES"
    },
    "work_order_number": {
      "type": "string",
      "description": "Human-readable work order number"
    },
    "product_type": {
      "type": "string",
      "enum": ["standard", "cto", "bto", "eto"]
    },
    "base_product": {
      "type": "object",
      "properties": {
        "product_id": { "type": "string" },
        "product_name": { "type": "string" },
        "base_cycle_time_seconds": { "type": "number" }
      }
    },
    "options": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "category": { "type": "string" },
          "option_code": { "type": "string" },
          "description": { "type": "string" },
          "cycle_time_delta": { "type": "number" }
        }
      }
    },
    "scheduling": {
      "type": "object",
      "properties": {
        "quantity": { "type": "integer" },
        "priority": { "type": "integer" },
        "due_date": { "type": "string", "format": "date-time" }
      }
    }
  }
}
```

### MES Adapter for CTO/BTO (Placeholder)

```python
# src/integrations/mes_cto_bto_adapter.py
from abc import ABC, abstractmethod
from typing import Dict, List, Optional
import httpx

class MESCTOBTOAdapterBase(ABC):
    """Base class for MES CTO/BTO integration"""
    
    @abstractmethod
    async def get_work_orders(
        self,
        site_id: str,
        status: Optional[str] = None,
        product_type: Optional[str] = None
    ) -> List[CTOBTOWorkOrder]:
        """Retrieve work orders from MES"""
        pass
    
    @abstractmethod
    async def get_configuration(
        self,
        work_order_id: str
    ) -> CTOBTOConfiguration:
        """Get detailed configuration for a work order"""
        pass
    
    @abstractmethod
    async def sync_work_orders(
        self,
        site_id: str,
        since: Optional[datetime] = None
    ) -> Dict:
        """Sync work orders from MES"""
        pass

class StubMESCTOBTOAdapter(MESCTOBTOAdapterBase):
    """
    Placeholder adapter for development/testing.
    Replace with actual MES integration when API is available.
    """
    
    def __init__(self, config: dict):
        self.config = config
        # Mock work orders for testing
        self._mock_work_orders = self._load_mock_data()
    
    def _load_mock_data(self) -> List[Dict]:
        """Load mock CTO/BTO work orders for development"""
        return [
            {
                "work_order_id": "WO_CTO_001",
                "work_order_number": "WO-2025-12345",
                "product_type": "cto",
                "base_product": {
                    "product_id": "DL360_G11",
                    "product_name": "ProLiant DL360 Gen11",
                    "base_cycle_time_seconds": 1800
                },
                "options": [
                    {"category": "cpu", "option_code": "XEON_GOLD_6454S", "delta": 120},
                    {"category": "memory", "option_code": "DDR5_256GB", "delta": 180},
                    {"category": "storage", "option_code": "NVME_3TB_RAID", "delta": 300}
                ],
                "scheduling": {
                    "quantity": 5,
                    "priority": 2,
                    "due_date": "2026-01-15T00:00:00Z"
                }
            },
            {
                "work_order_id": "WO_BTO_002",
                "work_order_number": "WO-2025-12346",
                "product_type": "bto",
                "base_product": {
                    "product_id": "DL380_G11",
                    "product_name": "ProLiant DL380 Gen11",
                    "base_cycle_time_seconds": 2400
                },
                "options": [
                    {"category": "gpu", "option_code": "NVIDIA_A100", "delta": 600},
                    {"category": "power_supply", "option_code": "1600W_REDUNDANT", "delta": 120}
                ],
                "scheduling": {
                    "quantity": 2,
                    "priority": 1,
                    "due_date": "2026-01-10T00:00:00Z"
                }
            }
        ]
    
    async def get_work_orders(
        self,
        site_id: str,
        status: Optional[str] = None,
        product_type: Optional[str] = None
    ) -> List[Dict]:
        """Return mock work orders (placeholder)"""
        results = self._mock_work_orders.copy()
        if product_type:
            results = [wo for wo in results if wo["product_type"] == product_type]
        return results
    
    async def get_configuration(self, work_order_id: str) -> Dict:
        """Return mock configuration (placeholder)"""
        for wo in self._mock_work_orders:
            if wo["work_order_id"] == work_order_id:
                return wo
        return None
    
    async def sync_work_orders(
        self,
        site_id: str,
        since: Optional[datetime] = None
    ) -> Dict:
        """Mock sync operation (placeholder)"""
        return {
            "synced_count": len(self._mock_work_orders),
            "new_orders": 2,
            "updated_orders": 0,
            "last_sync": datetime.utcnow().isoformat(),
            "status": "placeholder_mode"
        }
```

### CTO/BTO Cycle Time Adjustment Service

```python
# src/services/cto_bto_cycle_time_service.py
class CTOBTOCycleTimeService:
    """Calculate adjusted cycle times for CTO/BTO work orders"""
    
    def __init__(self, bdc_adapter, mes_adapter):
        self.bdc = bdc_adapter
        self.mes = mes_adapter
    
    async def calculate_adjusted_cycle_time(
        self,
        work_order_id: str,
        station_type: str
    ) -> Dict:
        """
        Calculate adjusted CT for CTO/BTO work order.
        
        Flow:
        1. Get base CT from BDC (Expected CT)
        2. Get work order configuration from MES
        3. Sum all option cycle time deltas
        4. Return adjusted CT
        """
        # Get base CT from BDC
        wo_config = await self.mes.get_configuration(work_order_id)
        base_product_id = wo_config["base_product"]["product_id"]
        
        base_ct = await self.bdc.get_expected_cycle_time(
            part_id=base_product_id,
            station_type=station_type
        )
        
        # Calculate total delta from options
        total_delta = sum(
            opt.get("delta", 0) or opt.get("cycle_time_delta", 0)
            for opt in wo_config.get("options", [])
        )
        
        # Adjusted CT
        adjusted_ct = base_ct["value"] + total_delta
        
        return {
            "work_order_id": work_order_id,
            "base_product_id": base_product_id,
            "product_type": wo_config["product_type"],
            "base_ct_seconds": base_ct["value"],
            "options_delta_seconds": total_delta,
            "adjusted_ct_seconds": adjusted_ct,
            "options_applied": len(wo_config.get("options", []))
        }
```

### API Endpoints for CTO/BTO

```yaml
# CTO/BTO Work Order APIs
GET /integrations/mes/cto-bto/work-orders:
  description: List CTO/BTO work orders from MES
  query_params:
    site_id: string
    product_type: string  # cto, bto, eto
    status: string
  response:
    work_orders: CTOBTOWorkOrder[]
    total_count: integer

GET /integrations/mes/cto-bto/work-orders/{work_order_id}:
  description: Get detailed CTO/BTO configuration
  response:
    work_order_id: string
    configuration: CTOBTOConfiguration
    adjusted_cycle_time: number

POST /integrations/mes/cto-bto/sync:
  description: Sync CTO/BTO work orders from MES
  request:
    site_id: string
    since: datetime (optional)
  response:
    synced_count: integer
    new_orders: integer
    updated_orders: integer

POST /integrations/mes/cto-bto/cycle-time/calculate:
  description: Calculate adjusted CT for work order
  request:
    work_order_id: string
    station_type: string
  response:
    base_ct_seconds: number
    options_delta_seconds: number
    adjusted_ct_seconds: number
```

### MES Integration Configuration (Placeholder)

```yaml
# config/integrations/mes_cto_bto.yaml
mes_cto_bto:
  enabled: true
  adapter_type: "stub"  # Change to actual MES type when available
  
  # Placeholder configuration
  placeholder_mode: true
  mock_data_path: "data/mes_cto_bto_mock.json"
  
  # Future MES connection (placeholder)
  connection:
    base_url: "${MES_API_URL:-http://mes-placeholder.local/api/v1}"
    api_key: "${MES_API_KEY}"
    timeout_seconds: 30
  
  sync:
    cron_schedule: "*/15 * * * *"  # Every 15 minutes
    batch_size: 100
    retry_attempts: 3
  
  # Mapping from MES option codes to Line Balance
  option_mappings:
    cpu:
      field: "processor_type"
      default_delta_seconds: 60
    memory:
      field: "ram_config"
      default_delta_seconds: 45
    storage:
      field: "disk_config"
      default_delta_seconds: 120
```

---

## Work Order Priority Optimizer Integration ⚠️ **IMPLEMENTATION**

### Overview

Integrate the `PriorityScheduler` with the main `/optimize` endpoint to consider work order priorities in line balance optimization.

### Integration Flow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   Priority-Aware Optimization Flow                          │
│                                                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  POST /optimize                                                       │  │
│  │    Input: tasks, config, work_orders (with priorities)                │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                               │                                             │
│                               ▼                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Step 1: Priority Pre-processing                                     │  │
│  │    - Sort work orders by priority                                     │  │
│  │    - Calculate priority weights                                       │  │
│  │    - Identify critical path constraints                               │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                               │                                             │
│                               ▼                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Step 2: CP-SAT Model Enhancement                                    │  │
│  │    - Add priority-weighted objective terms                            │  │
│  │    - Add ordering constraints for critical orders                     │  │
│  │    - Adjust takt time bounds based on priority                        │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
│                               │                                             │
│                               ▼                                             │
│  ┌───────────────────────────────────────────────────────────────────────┐  │
│  │  Step 3: Solve & Generate Schedule                                   │  │
│  │    - Run CP-SAT solver                                                │  │
│  │    - Generate priority-respecting schedule                            │  │
│  │    - Validate critical order deadlines met                            │  │
│  └───────────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Enhanced Optimizer Integration

```python
# src/optimizer/priority_optimizer.py
from ortools.sat.python import cp_model
from typing import List, Dict, Optional
from enum import IntEnum

class PriorityLevel(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

class PriorityAwareOptimizer:
    """Extend base optimizer with priority handling"""
    
    def __init__(self, base_optimizer):
        self.base_optimizer = base_optimizer
        self.priority_weights = {
            PriorityLevel.CRITICAL: 100,
            PriorityLevel.HIGH: 50,
            PriorityLevel.MEDIUM: 20,
            PriorityLevel.LOW: 5
        }
    
    def optimize_with_priorities(
        self,
        tasks: List[dict],
        work_orders: List[dict],
        config: dict
    ) -> dict:
        """Run optimization considering work order priorities"""
        
        model = cp_model.CpModel()
        
        # Group tasks by work order
        wo_tasks = self._group_tasks_by_work_order(tasks, work_orders)
        
        # Create base optimization variables
        task_vars = self._create_task_variables(model, tasks)
        
        # Add priority-weighted objective
        objective_terms = []
        
        for wo in work_orders:
            wo_id = wo["work_order_id"]
            priority = PriorityLevel(wo.get("priority_level", 2))
            weight = self.priority_weights[priority]
            
            # Higher priority = minimize completion time more aggressively
            wo_completion = self._get_wo_completion_var(model, wo_id, task_vars)
            objective_terms.append(wo_completion * weight)
            
            # Critical orders: add hard constraint on takt
            if priority == PriorityLevel.CRITICAL:
                max_takt = wo.get("max_takt_time", config.get("max_takt"))
                if max_takt:
                    model.Add(self.takt_var <= max_takt)
        
        # Add priority ordering constraints
        self._add_priority_ordering(model, work_orders, task_vars)
        
        # Combine with base objective (minimize takt, balance utilization)
        base_objective = self.base_optimizer.get_objective(model)
        priority_objective = sum(objective_terms)
        
        # Weighted combination
        model.Minimize(base_objective + priority_objective // 10)
        
        # Solve
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = config.get("timeout", 30)
        status = solver.Solve(model)
        
        if status in [cp_model.OPTIMAL, cp_model.FEASIBLE]:
            return self._extract_solution(solver, task_vars, work_orders)
        else:
            return {"error": "No feasible solution found"}
    
    def _add_priority_ordering(
        self, 
        model: cp_model.CpModel, 
        work_orders: List[dict],
        task_vars: dict
    ):
        """Add constraints to prioritize critical orders"""
        
        sorted_orders = sorted(
            work_orders, 
            key=lambda x: -x.get("priority_level", 2)
        )
        
        # Critical orders should start before lower priority ones
        critical_orders = [wo for wo in sorted_orders 
                         if wo.get("priority_level", 2) >= PriorityLevel.HIGH]
        
        for i, critical_wo in enumerate(critical_orders):
            for lower_wo in sorted_orders[i+1:]:
                if lower_wo.get("priority_level", 2) < PriorityLevel.HIGH:
                    # Add soft constraint: critical should have earlier slot
                    # (Implemented via objective weights, not hard constraint)
                    pass

# Integration with main optimize endpoint
@app.post("/optimize")
async def optimize_line_balance(request: OptimizeRequest):
    """Enhanced /optimize with priority support"""
    
    # Extract work orders with priorities
    work_orders = request.work_orders or []
    
    if work_orders and any(wo.get("priority_level") for wo in work_orders):
        # Use priority-aware optimizer
        optimizer = PriorityAwareOptimizer(base_optimizer)
        result = optimizer.optimize_with_priorities(
            tasks=request.tasks,
            work_orders=work_orders,
            config=request.config
        )
    else:
        # Use standard optimizer
        result = base_optimizer.optimize(request.tasks, request.config)
    
    return result
```

### API Schema Extension

```yaml
POST /optimize:
  request:
    tasks: Task[]
    config: OptimizeConfig
    work_orders:  # NEW: Optional work order context
      - work_order_id: string
        priority_level: integer  # 1=low, 2=medium, 3=high, 4=critical
        due_date: date
        max_takt_time: float  # Optional override
        customer_code: string  # For customer-priority rules
  response:
    result: OptimizeResult
    priority_analysis:  # NEW
      critical_orders_scheduled: integer
      priority_violations: string[]
      schedule_order: string[]  # Work orders in scheduled order
```

---

## Test Stage Scheduling Integration ⚠️ **IMPLEMENTATION**

### Overview

Integrate test stage durations into production scheduling to provide complete end-to-end time estimates.

### Test Stage Time Framework

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                   Production Timeline with Test Stages                      │
│                                                                             │
│  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐       │
│  │ Kitting │ → │ Assembly│ → │ Testing │ → │ Packing │ → │ Shipping│       │
│  │ Stage   │   │ Stage   │   │ Stage   │   │ Stage   │   │ Stage   │       │
│  │ 30 min  │   │ 120 min │   │ 45 min  │   │ 15 min  │   │ 10 min  │       │
│  └─────────┘   └─────────┘   └─────────┘   └─────────┘   └─────────┘       │
│                                                                             │
│  Total Production Time = 220 minutes per unit                               │
│  Bottleneck = Assembly Stage (determines line takt)                         │
└─────────────────────────────────────────────────────────────────────────────┘
```

### Data Models

```python
from pydantic import BaseModel
from typing import List, Optional
from enum import Enum

class StageType(str, Enum):
    KITTING = "kitting"
    ASSEMBLY = "assembly"
    TESTING = "testing"
    PACKING = "packing"
    SHIPPING = "shipping"
    AUDIT = "audit"
    REWORK = "rework"

class ProductionStage(BaseModel):
    stage_type: StageType
    stage_name: str
    sequence: int
    
    # Timing
    standard_duration_minutes: float
    min_duration_minutes: Optional[float] = None
    max_duration_minutes: Optional[float] = None
    
    # Resources
    station_codes: List[str]
    parallel_capacity: int = 1  # How many units can be processed simultaneously
    
    # Constraints
    requires_previous_complete: bool = True
    can_batch: bool = False
    batch_size: Optional[int] = None

class TestStageDefinition(BaseModel):
    test_stage_id: str
    test_name: str
    
    # Timing
    test_duration_minutes: float
    setup_time_minutes: float = 0
    cooldown_time_minutes: float = 0
    
    # Equipment
    test_equipment_ids: List[str]
    equipment_capacity: int  # Units per equipment
    
    # Scheduling
    is_blocking: bool = True  # Must complete before next stage
    can_parallel: bool = False
    failure_rework_time: float = 0  # Additional time if test fails
```

### Test Stage Scheduler

```python
# src/services/test_stage_scheduler.py
from datetime import datetime, timedelta
from typing import List, Dict

class TestStageScheduler:
    """Schedule test stages within production timeline"""
    
    def __init__(self, site_config: dict):
        self.site_config = site_config
    
    def calculate_total_production_time(
        self,
        product_sku: str,
        quantity: int
    ) -> Dict:
        """Calculate total time including all stages"""
        
        stages = self._get_product_stages(product_sku)
        
        stage_times = []
        total_time = 0
        bottleneck_stage = None
        bottleneck_time = 0
        
        for stage in stages:
            # Calculate effective time considering parallel capacity
            effective_time = (
                stage.standard_duration_minutes * quantity / stage.parallel_capacity
            )
            
            stage_times.append({
                "stage": stage.stage_type.value,
                "per_unit_minutes": stage.standard_duration_minutes,
                "total_minutes": effective_time,
                "parallel_capacity": stage.parallel_capacity
            })
            
            # Track bottleneck (longest per-unit time)
            if stage.standard_duration_minutes > bottleneck_time:
                bottleneck_time = stage.standard_duration_minutes
                bottleneck_stage = stage.stage_type.value
            
            total_time += effective_time
        
        return {
            "product_sku": product_sku,
            "quantity": quantity,
            "stages": stage_times,
            "total_production_minutes": total_time,
            "bottleneck_stage": bottleneck_stage,
            "bottleneck_time_minutes": bottleneck_time,
            "effective_takt_minutes": bottleneck_time
        }
    
    def schedule_with_tests(
        self,
        work_order_id: str,
        product_sku: str,
        quantity: int,
        start_time: datetime
    ) -> Dict:
        """Generate complete schedule including test stages"""
        
        stages = self._get_product_stages(product_sku)
        test_stages = self._get_test_stages(product_sku)
        
        schedule = []
        current_time = start_time
        
        for stage in stages:
            # Production stage
            stage_duration = timedelta(
                minutes=stage.standard_duration_minutes * quantity / stage.parallel_capacity
            )
            
            schedule.append({
                "type": "production",
                "stage": stage.stage_type.value,
                "start": current_time,
                "end": current_time + stage_duration,
                "duration_minutes": stage_duration.total_seconds() / 60
            })
            
            current_time += stage_duration
            
            # Check for test stage after this production stage
            test = next(
                (t for t in test_stages if t.after_stage == stage.stage_type),
                None
            )
            
            if test:
                test_duration = timedelta(
                    minutes=(test.test_duration_minutes + test.setup_time_minutes) 
                    * quantity / test.equipment_capacity
                )
                
                schedule.append({
                    "type": "testing",
                    "stage": test.test_name,
                    "start": current_time,
                    "end": current_time + test_duration,
                    "duration_minutes": test_duration.total_seconds() / 60,
                    "equipment": test.test_equipment_ids
                })
                
                current_time += test_duration
        
        return {
            "work_order_id": work_order_id,
            "schedule": schedule,
            "total_start": start_time,
            "total_end": current_time,
            "total_duration_hours": (current_time - start_time).total_seconds() / 3600
        }
```

### API Endpoints

```yaml
GET /products/{sku}/production-time:
  description: Get total production time including all stages
  parameters:
    quantity: integer (default: 1)
  response:
    product_sku: string
    quantity: integer
    stages: ProductionStage[]
    total_production_minutes: float
    bottleneck_stage: string
    effective_takt_minutes: float

POST /schedule/with-tests:
  description: Generate complete schedule including test stages
  request:
    work_order_id: string
    product_sku: string
    quantity: integer
    start_time: datetime
  response:
    work_order_id: string
    schedule: ScheduleEntry[]
    total_start: datetime
    total_end: datetime
    total_duration_hours: float

GET /test-stages/{product_sku}:
  description: Get test stage definitions for a product
  response:
    product_sku: string
    test_stages: TestStageDefinition[]
    total_test_time_minutes: float
```

### Database Schema

```sql
CREATE TABLE production_stages (
    id SERIAL PRIMARY KEY,
    product_family VARCHAR(50),
    stage_type VARCHAR(30) NOT NULL,
    stage_name VARCHAR(100),
    sequence INTEGER NOT NULL,
    standard_duration_minutes DECIMAL(10,2),
    parallel_capacity INTEGER DEFAULT 1,
    requires_previous_complete BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE test_stage_definitions (
    id SERIAL PRIMARY KEY,
    product_family VARCHAR(50),
    test_stage_id VARCHAR(50) UNIQUE,
    test_name VARCHAR(100),
    after_stage VARCHAR(30),  # Which production stage it follows
    test_duration_minutes DECIMAL(10,2),
    setup_time_minutes DECIMAL(10,2) DEFAULT 0,
    equipment_capacity INTEGER DEFAULT 1,
    is_blocking BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Insert example test stages
INSERT INTO test_stage_definitions 
(product_family, test_stage_id, test_name, after_stage, test_duration_minutes, setup_time_minutes)
VALUES 
('DL360_G11', 'TEST_BURN_IN', 'Burn-In Test', 'assembly', 240, 5),
('DL360_G11', 'TEST_DIAG', 'Diagnostic Test', 'assembly', 30, 2),
('DL360_G11', 'TEST_FINAL', 'Final QA', 'packing', 15, 0);
```

---

## Technology Stack

### Frontend Stack

| Technology                 | Version | Purpose                      |
|----------------------------|---------|------------------------------|
| React                      | 18.2+   | UI Framework                 |
| Three.js                   | r150+   | 3D WebGL Rendering           |
| @react-three/fiber         | 8.0+    | React + Three.js integration |
| Omniverse Streaming Client | Latest  | Remote Omniverse rendering   |
| WebRTC                     | -       | Real-time communication      |
| Socket.IO                  | 4.5+    | WebSocket management         |

### Backend Stack

| Technology      | Version | Purpose                     |
|-----------------|---------|-----------------------------|
| Python          | 3.10+   | Core language               |
| FastAPI         | 0.104+  | Web framework               |
| LangChain       | 0.1+    | LLM orchestration           |
| OpenAI API      | GPT-4   | Natural language processing |
| MediaPipe       | 0.10+   | Body pose estimation        |
| PyTorch         | 2.0+    | Deep learning               |
| PostgreSQL      | 15+     | Relational database         |
| Pinecone/Milvus | Latest  | Vector database             |

### 3D Simulation Stack

| Technology                        | Version | Purpose              |
|-----------------------------------|---------|----------------------|
| NVIDIA Omniverse                  | 2023.2+ | 3D platform          |
| USD (Universal Scene Description) | 23.11+  | Scene format         |
| PhysX                             | 5.0+    | Physics engine       |
| Nucleus Server                    | Latest  | Collaboration server |
| RTX Renderer                      | Latest  | Ray tracing          |

### ML/AI Stack

| Technology      | Version | Purpose                   |
|-----------------|---------|---------------------------|
| MediaPipe Pose  | 0.10+   | Pose estimation           |
| OpenCV          | 4.8+    | Video processing          |
| scikit-learn    | 1.3+    | Classical ML              |
| TensorFlow Lite | 2.13+   | Edge inference (optional) |

---

## Data Flow

### End-to-End Query Flow

```
User: "Show me the 3D simulation of the optimized layout for WO_A"
    │
    ▼
┌─────────────────────────┐
│ React NLP Interface     │
│ POST /nlp-query         │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ LangChain Processing    │
│ Intent: "3d_simulation" │
│ Entity: work_order=WO_A │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ API Orchestration       │
│ 1. GET /optimize?wo=WO_A│
│ 2. GET /layout          │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Omniverse Connector     │
│ create_scene(WO_A)      │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ USD Scene Generation    │
│ /scenes/WO_A.usd        │
└───────────┬─────────────┘
            │
            ▼
┌─────────────────────────┐
│ Streaming to Frontend   │
│ WebRTC + Omniverse Kit  │
└───────────┬─────────────┘
            │
            ▼
        User sees 3D scene
```

---

## Database Schema

### Phase 3 Advanced PostgreSQL Schema

Phase 3 extends the database with AI/ML data structures, sensor data, and 3D model management. For the complete database schema, refer to [Database & API Design Specification](DATABASE_API_DESIGN_SPEC_EN.md).

#### Core Phase 3 Tables

```sql
-- Phase 3: Motion capture sessions
CREATE TABLE sensor_sessions (
    id SERIAL PRIMARY KEY,
    site_id INTEGER REFERENCES sites(id),
    worker_id VARCHAR(50) NOT NULL,
    session_id VARCHAR(100) NOT NULL,
    
    -- Session context
    task_id INTEGER,
    station_code VARCHAR(50),
    work_order_id INTEGER REFERENCES work_orders(id),
    
    -- Recording metadata
    video_file_path VARCHAR(255),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP,
    camera_position VARCHAR(50),
    
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Motion capture frame-by-frame data
CREATE TABLE motion_captures (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES sensor_sessions(id),
    frame_number INTEGER NOT NULL,
    timestamp_ms INTEGER NOT NULL,
    
    -- MediaPipe pose landmarks (33 points)
    pose_landmarks JSONB NOT NULL,
    
    -- Derived ergonomic metrics
    reba_score INTEGER,
    neck_angle DECIMAL(5,2),
    back_angle DECIMAL(5,2),
    shoulder_elevation DECIMAL(5,2),
    
    -- Motion classification
    action_type VARCHAR(50),
    confidence_score DECIMAL(4,3),
    
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(session_id, frame_number)
);

-- Aggregated ergonomic analysis
CREATE TABLE ergonomic_analyses (
    id SERIAL PRIMARY KEY,
    session_id INTEGER REFERENCES sensor_sessions(id),
    
    -- REBA scores
    avg_reba_score DECIMAL(4,2),
    max_reba_score INTEGER,
    high_risk_duration_ms INTEGER,
    
    -- Efficiency metrics
    movement_smoothness DECIMAL(4,3),
    repetitive_strain_risk DECIMAL(4,3),
    efficiency_score DECIMAL(5,2),
    
    -- Recommendations
    recommended_break_intervals INTEGER,
    ergonomic_improvements JSONB,
    
    analyzed_at TIMESTAMP DEFAULT NOW()
);

-- NLP query history
CREATE TABLE nlp_queries (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    query_text TEXT NOT NULL,
    
    -- Intent classification
    intent VARCHAR(100),
    entities JSONB,
    
    -- Generated API calls
    api_endpoint VARCHAR(255),
    api_parameters JSONB,
    
    -- Response
    response_text TEXT,
    response_data JSONB,
    
    -- Performance tracking
    processing_time_ms INTEGER,
    confidence_score DECIMAL(4,3),
    
    created_at TIMESTAMP DEFAULT NOW()
);

-- 3D model catalog
CREATE TABLE model_3d_catalog (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(255) NOT NULL,
    category VARCHAR(100) NOT NULL,
    
    -- File references
    usd_file_path VARCHAR(255) NOT NULL,
    thumbnail_path VARCHAR(255),
    
    -- Metadata
    dimensions JSONB,
    vertex_count INTEGER,
    file_size_mb DECIMAL(8,2),
    
    -- Version control
    version VARCHAR(50) NOT NULL,
    parent_model_id INTEGER REFERENCES model_3d_catalog(id),
    
    created_by INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Enhanced configuration management
CREATE TABLE configurations (
    id SERIAL PRIMARY KEY,
    site_id INTEGER REFERENCES sites(id),
    config_type VARCHAR(50) NOT NULL,
    config_name VARCHAR(255) NOT NULL,
    
    -- Configuration data
    config_data JSONB NOT NULL,
    
    -- Version control
    version VARCHAR(50) NOT NULL,
    parent_config_id INTEGER REFERENCES configurations(id),
    commit_message TEXT,
    
    -- Metadata
    author INTEGER REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),
    is_active BOOLEAN DEFAULT TRUE,
    
    UNIQUE(site_id, config_type, config_name, version)
);

-- Configuration snapshots for rollback
CREATE TABLE config_snapshots (
    id SERIAL PRIMARY KEY,
    configuration_id INTEGER REFERENCES configurations(id),
    snapshot_data JSONB NOT NULL,
    snapshot_hash VARCHAR(64) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
```

### Phase 3 API Endpoints

```yaml
# Natural Language Query APIs
POST   /api/v3/nlp-query                    # Process natural language query
GET    /api/v3/nlp-query/history            # Query history for user

# Sensor Data APIs
POST   /api/v3/sensor-data                  # Upload motion capture video
GET    /api/v3/sensor-data/{session_id}     # Get session details
GET    /api/v3/sensor-data/{session_id}/analysis  # Ergonomic analysis

# 3D Model Management APIs
GET    /api/v3/3d-models                    # List available 3D models
POST   /api/v3/3d-models                    # Upload new 3D model
GET    /api/v3/3d-models/{id}               # Get model metadata
POST   /api/v3/3d-models/{id}/render        # Request model rendering

# Version Control APIs
GET    /api/v3/versions                     # List configuration versions
POST   /api/v3/versions                     # Create new version
GET    /api/v3/versions/{id}/restore        # Restore previous version
GET    /api/v3/versions/compare             # Compare two versions

# Collision Detection APIs
POST   /api/v3/check-collision              # Run collision detection
GET    /api/v3/collision-report/{opt_id}    # Get collision report

# Multi-site Sharing APIs
POST   /api/v3/share-configuration          # Share config across sites
GET    /api/v3/shared-configurations        # List shared configs
```

### Data Input Schema Evolution (Phase 3)

Phase 3 supports advanced data types including video uploads, 3D models, and natural language queries:

#### Sensor Data Upload Request
```json
{
  "worker_id": "W001",
  "session_id": "session_20250114_101",
  "video_file": "<binary_data>",
  "metadata": {
    "task_id": 5,
    "start_time": "2025-01-14T10:30:00Z",
    "camera_position": "overhead",
    "station_code": "WS-001"
  }
}
```

#### Natural Language Query Request
```json
{
  "query": "Show me the bottleneck station in WO_A",
  "context": {
    "work_order_id": "WO_A",
    "user_id": "engineer_123",
    "site_id": 1
  }
}
```

#### 3D Model Upload Request
```json
{
  "model_name": "Workstation_Type_A",
  "category": "workstation",
  "usd_file": "<binary_data>",
  "dimensions": {
    "width": 2.0,
    "depth": 1.5,
    "height": 2.0
  },
  "metadata": {
    "manufacturer": "HPE",
    "model_year": 2025,
    "capacity": 3
  }
}
```

#### Version Control Request
```json
{
  "config_type": "layout",
  "config_data": {
    "stations": [...],
    "connections": [...]
  },
  "author": "john_doe",
  "site": "factory_A",
  "message": "Updated conveyor layout for Line A",
  "create_snapshot": true
}
```

### ORM Models (SQLAlchemy - Phase 3)

```python
from sqlalchemy import Column, Integer, String, Text, DECIMAL, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime

class SensorSession(Base):
    __tablename__ = 'sensor_sessions'
    
    id = Column(Integer, primary_key=True)
    site_id = Column(Integer, ForeignKey('sites.id'))
    worker_id = Column(String(50), nullable=False)
    session_id = Column(String(100), nullable=False)
    
    # Context
    task_id = Column(Integer)
    station_code = Column(String(50))
    work_order_id = Column(Integer, ForeignKey('work_orders.id'))
    
    # Metadata
    video_file_path = Column(String(255))
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime)
    camera_position = Column(String(50))
    
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    motion_captures = relationship("MotionCapture", back_populates="session")
    analysis = relationship("ErgonomicAnalysis", back_populates="session", uselist=False)

class MotionCapture(Base):
    __tablename__ = 'motion_captures'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(Integer, ForeignKey('sensor_sessions.id'))
    frame_number = Column(Integer, nullable=False)
    timestamp_ms = Column(Integer, nullable=False)
    
    # Pose data
    pose_landmarks = Column(JSONB, nullable=False)
    
    # Metrics
    reba_score = Column(Integer)
    neck_angle = Column(DECIMAL(5,2))
    back_angle = Column(DECIMAL(5,2))
    shoulder_elevation = Column(DECIMAL(5,2))
    
    # Classification
    action_type = Column(String(50))
    confidence_score = Column(DECIMAL(4,3))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    session = relationship("SensorSession", back_populates="motion_captures")

class NLPQuery(Base):
    __tablename__ = 'nlp_queries'
    
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    query_text = Column(Text, nullable=False)
    
    # Intent
    intent = Column(String(100))
    entities = Column(JSONB)
    
    # API execution
    api_endpoint = Column(String(255))
    api_parameters = Column(JSONB)
    
    # Response
    response_text = Column(Text)
    response_data = Column(JSONB)
    
    # Performance
    processing_time_ms = Column(Integer)
    confidence_score = Column(DECIMAL(4,3))
    
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User")

class Model3D(Base):
    __tablename__ = 'model_3d_catalog'
    
    id = Column(Integer, primary_key=True)
    model_name = Column(String(255), nullable=False)
    category = Column(String(100), nullable=False)
    
    # Files
    usd_file_path = Column(String(255), nullable=False)
    thumbnail_path = Column(String(255))
    
    # Metadata
    dimensions = Column(JSONB)
    vertex_count = Column(Integer)
    file_size_mb = Column(DECIMAL(8,2))
    
    # Version
    version = Column(String(50), nullable=False)
    parent_model_id = Column(Integer, ForeignKey('model_3d_catalog.id'))
    
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    creator = relationship("User")
    parent = relationship("Model3D", remote_side=[id])
```

### Performance Optimizations (Phase 3)

```sql
-- Sensor data partitioning by month
CREATE TABLE motion_captures_2025_01 PARTITION OF motion_captures
FOR VALUES FROM (1704067200) TO (1706745600);

-- Indexing for common queries
CREATE INDEX idx_sensor_worker_task ON sensor_sessions(worker_id, task_id);
CREATE INDEX idx_motion_session_time ON motion_captures(session_id, timestamp_ms);
CREATE INDEX idx_nlp_user_time ON nlp_queries(user_id, created_at DESC);
CREATE INDEX idx_model_category ON model_3d_catalog(category);

-- Full-text search for NLP queries
CREATE INDEX idx_nlp_query_text ON nlp_queries USING gin(to_tsvector('english', query_text));
```
    message TEXT,
    parent_hash VARCHAR(8),            -- For branching
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_type_site (config_type, site),
    INDEX idx_hash (version_hash)
);

-- Collaboration sessions
CREATE TABLE collaboration_sessions (
    id SERIAL PRIMARY KEY,
    session_id VARCHAR(100) UNIQUE NOT NULL,
    scene_url TEXT NOT NULL,
    users JSONB,                       -- Array of user IDs
    status VARCHAR(20) DEFAULT 'active', -- active, closed
    started_at TIMESTAMP DEFAULT NOW(),
    ended_at TIMESTAMP,
    INDEX idx_status (status)
);

-- Collision cache
CREATE TABLE collision_cache (
    id SERIAL PRIMARY KEY,
    layout_id INTEGER REFERENCES layouts(id),
    collision_pairs JSONB,             -- Array of collision objects
    clearance_used FLOAT,
    checked_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_layout (layout_id)
);

-- NLP query log
CREATE TABLE nlp_query_log (
    id SERIAL PRIMARY KEY,
    query_text TEXT NOT NULL,
    intent VARCHAR(50),
    entities JSONB,
    api_calls JSONB,                   -- Array of executed APIs
    response_time_ms INTEGER,
    user_id VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_intent (intent),
    INDEX idx_user (user_id)
);
```

---

## Performance Optimization

### 3D Rendering Optimization

| Technique             | Description                          | Impact           |
|-----------------------|--------------------------------------|------------------|
| Level of Detail (LOD) | Multiple model resolutions           | faster rendering |
| Instancing            | Reuse geometry for identical objects | memory reduction |
| Frustum Culling       | Only render visible objects          | GPU reduction    |
| Occlusion Culling     | Skip hidden objects                  | GPU reduction    |
| GPU-accelerated PhysX | Collision detection on GPU           | faster collision |

### NLP Query Optimization

```python
# Cache common queries
@lru_cache(maxsize=1000)
def process_nlp_query(query: str) -> Dict:
    # LLM call only if not cached
    pass

# Batch processing
async def batch_process_queries(queries: List[str]):
    # Process multiple queries in one LLM call
    prompt = "Process these queries:\n" + "\n".join(
        f"{i+1}. {q}" for i, q in enumerate(queries)
    )
    # Single API call instead of N calls
```

### Sensor Data Optimization

```python
# Downsampling for real-time processing
def downsample_video(video_path: str, target_fps: int = 10):
    """Reduce frame rate for faster processing"""
    # Process every Nth frame instead of all frames
    
# Parallel processing
from concurrent.futures import ThreadPoolExecutor

def process_multiple_videos(video_paths: List[str]):
    with ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(process_video, video_paths)
    return list(results)
```

---

## Deployment Architecture

### Cloud Infrastructure (analogy)

```
┌─────────────────────────────────────────────────────────────┐
│                     AWS / Azure Cloud                        │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────────────┐  ┌───────────────────┐              │
│  │ ECS / AKS Cluster │  │ Omniverse Farm    │              │
│  │ - API Containers  │  │ - GPU Instances   │              │
│  │ - NLP Service     │  │ - USD Rendering   │              │
│  │ - Sensor Proc.    │  │ - PhysX Sim       │              │
│  └─────────┬─────────┘  └─────────┬─────────┘              │
│            │                       │                         │
│  ┌─────────▼───────────────────────▼─────────┐              │
│  │ Load Balancer (ALB / App Gateway)         │              │
│  └─────────┬───────────────────────┬─────────┘              │
│            │                       │                         │
│  ┌─────────▼─────────┐  ┌─────────▼─────────┐              │
│  │ RDS PostgreSQL    │  │ S3 / Blob Storage │              │
│  │ - Versions        │  │ - USD Files       │              │
│  │ - Sensor Data     │  │ - Videos          │              │
│  │ - Model Library   │  │ - Exports         │              │
│  └───────────────────┘  └───────────────────┘              │
└─────────────────────────────────────────────────────────────┘
```

### Scaling Strategy

- **Horizontal Scaling**: Auto-scale API containers based on CPU/memory
- **GPU Scaling**: Elastic GPU instances for Omniverse rendering
- **Database Sharding**: Partition sensor data by time/worker
- **CDN**: Cache 3D models and static assets
- **Edge Computing**: Process sensor data on-premise, sync to cloud

---

## Security Considerations

### Data Protection

- **Encryption**: TLS 1.3 for API, AES-256 for database
- **Authentication**: OAuth 2.0 + JWT tokens
- **Authorization**: RBAC with site-level permissions
- **Audit Logging**: Track all configuration changes

### 3D Asset Security

- **Access Control**: Omniverse Nucleus ACLs
- **Watermarking**: Embed company IDs in USD files
- **DRM**: Prevent unauthorized model export

---

## Future Enhancements

### Phase 3.5 (Potential)

- **AR/VR Integration**: HoloLens / Quest support for layout review
- **Digital Twin**: Real-time production line monitoring
- **Predictive Maintenance**: AI-based equipment failure prediction
- **Autonomous Optimization**: Self-tuning line balance algorithms

---

**Document Maintainer:** JASON YY, LIN  
**Last Updated:** 2025-11-13
**Version:** 3.0.0-phase3
