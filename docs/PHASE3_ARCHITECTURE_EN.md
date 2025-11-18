# Phase 3 Architecture Design

**Document Version**: 1.0 | **Last Updated**: 2025-11-12  
**Related Documents**:
- [Phase 3 Implementation Guide](PHASE3_IMPLEMENTATION_EN.md)
- [Phase 3 API Specification](PHASE3_API_SPEC_EN.md)
- [Phase 2 Architecture](PHASE2_ARCHITECTURE_EN.md)
- [Requirements Coverage Analysis](REQUIREMENTS_COVERAGE_ANALYSIS.md)

---

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [System Components](#system-components)
- [3D Simulation Architecture](#3d-simulation-architecture)
- [Natural Language Query Architecture](#natural-language-query-architecture)
- [Body Sensor Data Processing](#body-sensor-data-processing)
- [Version Management & Multi-Site Sharing](#version-management--multi-site-sharing)
- [Collision Detection System](#collision-detection-system)
- [Technology Stack](#technology-stack)
- [Data Flow](#data-flow)
- [Database Schema](#database-schema)
- [Performance Optimization](#performance-optimization)

---

## Architecture Overview

### Design Principles

Phase 3 extends the architecture with advanced AI/ML and 3D capabilities:

1. **Presentation Layer** (Frontend)
   - Technology: React + Three.js + **NVIDIA Omniverse Kit**
   - Components: 3D Viewer, NLP Query Interface, Sensor Dashboard
   - Responsibility: Advanced 3D visualization, interactive simulation

2. **Service Layer** (Backend API)
   - Technology: FastAPI + **LangChain** + **PostgreSQL**
   - Components: NLP Engine, Version Control, Collision Detector
   - Responsibility: AI orchestration, data versioning, physics simulation

3. **AI/ML Layer** (Intelligence Engine)
   - Technology: **OpenAI GPT-4** + **PyTorch** + **MediaPipe**
   - Components: LLM Query Engine, Sensor Data Processor, Motion Analyzer
   - Responsibility: Natural language understanding, motion capture processing

4. **3D Simulation Layer** (Rendering Engine)
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
                       │ WebSocket + REST API
                       ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      Backend API Layer (Phase 3)                     │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  api_server.py (Extended FastAPI Application)                │  │
│  │  ┌─────────────────────────────────────────────────────────┐  │  │
│  │  │  Phase 3 NEW Endpoints                                  │  │  │
│  │  │  - POST /nlp-query           (Natural Language Query)   │  │  │
│  │  │  - GET  /3d-models           (3D Asset Management)      │  │  │
│  │  │  - POST /upload-sensor-data  (Body Sensor Ingestion)    │  │  │
│  │  │  - GET  /versions            (Version Management)       │  │  │
│  │  │  - POST /check-collision     (Interference Detection)   │  │  │
│  │  │  - GET  /omniverse-session   (3D Simulation Session)    │  │  │
│  │  │  - POST /share-configuration (Cross-Site Sharing)       │  │  │
│  │  └─────────────────┬───────────────────────────────────────┘  │  │
│  │                    │                                           │  │
│  │  ┌─────────────────▼───────────────────────────────────────┐  │  │
│  │  │  Service Modules (NEW)                                  │  │  │
│  │  │  - nlp_service.py         (LangChain integration)       │  │  │
│  │  │  - sensor_processor.py    (Motion data analysis)        │  │  │
│  │  │  - version_manager.py     (Git-like versioning)         │  │  │
│  │  │  - collision_detector.py  (Physics collision check)     │  │  │
│  │  │  - omniverse_connector.py (USD scene management)        │  │  │
│  │  └─────────────────┬───────────────────────────────────────┘  │  │
│  └────────────────────┼───────────────────────────────────────────┘  │
└────────────────────────┼───────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────┐
│                      AI/ML Layer (Phase 3)                           │
│  ┌───────────────────────────────────────────────────────────────┐  │
│  │  NLP Engine (LangChain + OpenAI GPT-4)                        │  │
│  │  - Intent Recognition: "Show me the bottleneck station"       │  │
│  │  - Entity Extraction: Work order, SKU, station numbers       │  │
│  │  - Query Translation: NL → API calls                         │  │
│  │  - Response Generation: API results → Natural language       │  │
│  └───────────────────────────────────────────────────────────────┘  │
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

### New Tables (Phase 3)

```sql
-- Sensor motion data
CREATE TABLE sensor_data (
    id SERIAL PRIMARY KEY,
    worker_id VARCHAR(50) NOT NULL,
    session_id VARCHAR(100),
    motion_json JSONB NOT NULL,  -- MediaPipe landmarks
    action_type VARCHAR(50),     -- install, mount, screw, etc.
    reba_score INTEGER,          -- Ergonomic score 1-15
    timestamp TIMESTAMP DEFAULT NOW(),
    video_url TEXT,
    INDEX idx_worker_session (worker_id, session_id),
    INDEX idx_timestamp (timestamp)
);

-- 3D model library
CREATE TABLE model_library (
    id SERIAL PRIMARY KEY,
    model_name VARCHAR(200) NOT NULL,
    usd_path TEXT NOT NULL,           -- Path to USD file
    category VARCHAR(50),              -- workstation, product, tool
    dimensions JSONB,                  -- {width, depth, height}
    thumbnail_url TEXT,
    metadata JSONB,                    -- Additional properties
    created_at TIMESTAMP DEFAULT NOW(),
    INDEX idx_category (category)
);

-- Version control
CREATE TABLE versions (
    id SERIAL PRIMARY KEY,
    config_type VARCHAR(50) NOT NULL,  -- layout, optimization, product_config
    config_data JSONB NOT NULL,
    version_hash VARCHAR(8) UNIQUE NOT NULL,
    author VARCHAR(100) NOT NULL,
    site VARCHAR(100) NOT NULL,
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
