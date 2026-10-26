# QSR Queue Management System

**AI-Powered Queue Monitoring and Analytics for Quick Service Restaurants**

A computer-vision-based queue management system designed to process restaurant video footage, detect people, collect queue analytics, store records, and display operational information through a web dashboard.

> **Project status:** Working prototype with video processing, a FastAPI backend, a React dashboard, PostgreSQL storage, MongoDB data-copy tooling, and preliminary DeepStream integration files. Production-grade queue tracking and validated waiting-time estimation remain future improvements.

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Objectives](#2-project-objectives)
3. [Features](#3-features)
4. [Technology Stack](#4-technology-stack)
5. [System Architecture](#5-system-architecture)
6. [Project Folder Structure](#6-project-folder-structure)
7. [End-to-End Workflow](#7-end-to-end-workflow)
8. [Video Processing Pipeline](#8-video-processing-pipeline)
9. [Database Architecture](#9-database-architecture)
10. [PostgreSQL to MongoDB Migration](#10-postgresql-to-mongodb-migration)
11. [Backend API Architecture](#11-backend-api-architecture)
12. [Frontend Dashboard](#12-frontend-dashboard)
13. [Installation and Setup](#13-installation-and-setup)
14. [Running the Project](#14-running-the-project)
15. [Processing Videos](#15-processing-videos)
16. [Development Phases](#16-development-phases)
17. [Testing and Verification](#17-testing-and-verification)
18. [DeepStream Integration](#18-deepstream-integration)
19. [Current Limitations](#19-current-limitations)
20. [Future Enhancements](#20-future-enhancements)
21. [Git Workflow](#21-git-workflow)
22. [Troubleshooting](#22-troubleshooting)

---

## 1. Project Overview

Quick Service Restaurants (QSRs) need visibility into queue lengths, customer congestion, and service efficiency.

This project provides a prototype architecture for processing video footage, running people detection, sending analytics to a backend, storing records in a database, and displaying the results in a web dashboard.

The system combines computer vision, REST APIs, relational data storage, and a web-based user interface.

### Main goals

- Process recorded restaurant videos.
- Detect people using a YOLO object detection model.
- Register video sources as cameras.
- Send queue analytics to the backend.
- Store camera and queue records in PostgreSQL.
- Copy database records to MongoDB when required.
- View camera status, queue information, and alerts through a dashboard.
- Establish a foundation for future NVIDIA DeepStream integration.

---

## 2. Project Objectives

| Objective | Description |
|---|---|
| Video analytics | Run person detection on video frames |
| Camera management | Register and manage video sources |
| Backend services | Provide REST APIs using FastAPI |
| Data persistence | Store application records in PostgreSQL |
| Data migration | Copy PostgreSQL records into MongoDB |
| Dashboard | Present operational information through React |
| Edge processing | Prepare integration files for DeepStream |
| Extensibility | Support future live camera streams and advanced analytics |

---

## 3. Features

### Implemented in the prototype

- YOLO-based person detection using Ultralytics.
- Video processing with OpenCV.
- FastAPI backend and REST API endpoints.
- React frontend using Vite.
- PostgreSQL database integration.
- Camera registration and queue record storage.
- Dashboard connectivity and session status.
- MongoDB connectivity through PyMongo.
- PostgreSQL-to-MongoDB one-time copy script.
- Multiple recorded video inputs.
- Initial analytics abstraction and mock provider.
- Starter files for DeepStream integration.

### Planned improvements

- Persistent tracking of individual people.
- Actual queue-region detection.
- Calibrated waiting-time prediction.
- Live RTSP camera processing.
- NVIDIA DeepStream pipeline integration.
- Production authentication, monitoring, and deployment.

---

## 4. Technology Stack

| Layer | Technology | Purpose |
|---|---|---|
| Programming language | Python | Backend and video processing |
| Object detection | Ultralytics YOLO | Detect people in frames |
| Video processing | OpenCV | Read and sample video frames |
| Backend framework | FastAPI | REST APIs |
| ORM | SQLAlchemy | PostgreSQL data access |
| Primary database | PostgreSQL | Relational application records |
| Secondary database | MongoDB | Document storage and copied records |
| MongoDB driver | PyMongo | Python-to-MongoDB connectivity |
| Frontend | React | Dashboard interface |
| Frontend tooling | Vite | Development server and build tooling |
| API testing | Swagger UI | Interactive API documentation |
| Version control | Git | Source code history |
| Repository hosting | GitHub | Remote source code repository |
| Edge analytics | NVIDIA DeepStream | Planned video analytics integration |

---

## 5. System Architecture

The following diagram describes the current prototype architecture and the intended direction of data flow.

```mermaid
flowchart TB
    subgraph INPUT["Video Input Layer"]
        V1["V1.mp4"]
        V2["V2.mp4"]
        V3["V3.mp4"]
        V4["V4.mp4"]
        V5["V5.mp4"]
    end

    subgraph CV["Computer Vision Layer"]
        VP["Python Video Processor"]
        CV2["OpenCV Frame Sampling"]
        YOLO["YOLO Person Detection"]
        AR["Queue Analytics Result"]
    end

    subgraph BACKEND["Backend Layer"]
        API["FastAPI REST API"]
        AUTH["Authentication"]
        CAM["Camera Management"]
        QUEUE["Queue Records"]
        ALERT["Alert Management"]
    end

    subgraph DATABASE["Data Layer"]
        PG[("PostgreSQL")]
        MG[("MongoDB")]
    end

    subgraph UI["Presentation Layer"]
        REACT["React + Vite Dashboard"]
    end

    INPUT --> VP
    VP --> CV2
    CV2 --> YOLO
    YOLO --> AR
    AR --> API
    API --> AUTH
    API --> CAM
    API --> QUEUE
    API --> ALERT
    API --> PG
    PG -. "One-time copy script" .-> MG
    REACT <--> API
```

**Important:** PostgreSQL is the application's primary relational database in the current implementation. MongoDB is connected separately, and the migration script copies records into MongoDB. Automatic, continuous synchronization is not implemented.

---

## 6. Project Folder Structure

```text
qsr-queue-management/
│
├── analytics/
│   ├── __init__.py
│   ├── base.py
│   ├── deepstream_adapter.py
│   └── mock_analytics.py
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   └── schemas.py
│   │
│   ├── copy_postgres_to_mongo.py
│   └── requirements.txt
│
├── deepstream/
│   ├── README.md
│   ├── config.py
│   ├── edge_agent.py
│   └── metadata_client.py
│
├── frontend/
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   └── src/
│       ├── App.jsx
│       ├── api.js
│       ├── main.jsx
│       └── style.css
│
├── tests/
│   └── test_analytics.py
│
├── videos/
│   ├── V1.mp4
│   ├── V2.mp4
│   ├── V3.mp4
│   ├── V4.mp4
│   └── V5.mp4
│
├── process_videos.py
├── requirements.txt
├── yolo11n.pt
└── .gitignore
```

The structure above describes the intended repository layout. Confirm that `V5.mp4` is present in the repository before publishing this README.

### Folder responsibilities

**`analytics/`**

Contains the analytics abstraction, mock implementation, and starter adapter for DeepStream.

**`backend/app/`**

Contains FastAPI application configuration, database access, ORM models, request/response schemas, and API routes.

**`backend/copy_postgres_to_mongo.py`**

Copies records from PostgreSQL tables into MongoDB collections.

**`deepstream/`**

Contains initial configuration and edge-agent integration files. These files are not, by themselves, a complete DeepStream inference pipeline.

**`frontend/`**

Contains the React dashboard, API client, styles, and Vite configuration.

**`tests/`**

Contains automated tests for analytics components.

**`videos/`**

Stores recorded video inputs for offline processing.

**`process_videos.py`**

Runs the current Python-based video processing workflow.

---

## 7. End-to-End Workflow

```mermaid
flowchart TD
    A["Start Project"] --> B["Start PostgreSQL and MongoDB"]
    B --> C["Start FastAPI Backend"]
    C --> D["Start React Dashboard"]
    D --> E["Authenticate"]
    E --> F["Register Video as Camera"]
    F --> G["Read Video Frames"]
    G --> H["Run YOLO Detection"]
    H --> I["Generate Prototype Analytics"]
    I --> J["Send Records to FastAPI"]
    J --> K["Store Records in PostgreSQL"]
    K --> L["Fetch Data through API"]
    L --> M["Display Dashboard"]
    K -. "Optional one-time migration" .-> N["Copy Records to MongoDB"]
```

### Workflow explanation

1. Start the required database services.
2. Launch the FastAPI backend.
3. Launch the React frontend.
4. Authenticate through the application.
5. Register the video source as a camera.
6. Sample frames from the video.
7. Detect people using YOLO.
8. Generate the prototype queue analytics record.
9. Send the record to the backend API.
10. Store the record in PostgreSQL.
11. Retrieve camera and queue information for the dashboard.
12. Optionally copy PostgreSQL records into MongoDB.

---

## 8. Video Processing Pipeline

The current video-processing implementation uses a Python script, OpenCV, and an Ultralytics YOLO model.

```mermaid
flowchart LR
    A["MP4 Video"] --> B["OpenCV Video Capture"]
    B --> C["Sample Frames"]
    C --> D["YOLO Inference"]
    D --> E["Person Detection"]
    E --> F["Prototype Queue Count"]
    F --> G["Estimate Waiting Time"]
    G --> H["Build API Payload"]
    H --> I["POST Queue Record"]
    I --> J["PostgreSQL"]
```

### Processing stages

**Stage 1 — Video input**

The processor reads recorded video files from the project's `videos/` directory.

**Stage 2 — Frame sampling**

OpenCV reads the video and selects frames at configured intervals.

**Stage 3 — Object detection**

The YOLO model detects objects. The prototype uses the person class for its people-counting logic.

**Stage 4 — Analytics generation**

The current prototype uses the detected-person count as a queue-length estimate.

**Stage 5 — Waiting-time estimate**

The prototype estimates waiting time using a fixed multiplier of 30 seconds per detected person.

Conceptually:

\[
\text{Estimated Wait} =
\text{Detected Person Count} \times 30
\]

The resulting value is a preliminary estimate, not a validated measurement of actual customer waiting time.

**Stage 6 — API submission**

The script authenticates with the backend, registers camera sources, and sends queue records through the API.

**Stage 7 — Persistence**

The backend stores the received records in PostgreSQL.

### Important distinction

Person detection is not the same as queue detection. A person detected anywhere in a frame may not be waiting in a service queue. Accurate queue analytics require queue-region configuration, tracking, and suitable validation.

---

## 9. Database Architecture

### PostgreSQL

PostgreSQL is the primary relational database used by the FastAPI application.

The current database contains these tables:

| Table | Responsibility |
|---|---|
| `users` | User accounts and authentication-related data |
| `alert_thresholds` | Alert threshold configuration |
| `cameras` | Registered camera/video sources |
| `queue_records` | Recorded queue analytics |
| `alerts` | Application alert records |

### Entity relationship diagram

The following is a conceptual representation. Verify exact foreign-key constraints against the SQLAlchemy models before treating every relationship as a formal database constraint.

```mermaid
erDiagram
    USERS {
        int id PK
    }

    CAMERAS {
        int id PK
        string name
    }

    QUEUE_RECORDS {
        int id PK
        int camera_id FK
        datetime recorded_at
    }

    ALERT_THRESHOLDS {
        int id PK
    }

    ALERTS {
        int id PK
    }

    CAMERAS ||--o{ QUEUE_RECORDS : produces
```

### MongoDB

MongoDB is used as a separate document database.

The one-time migration script maps PostgreSQL table names to MongoDB collection names:

| PostgreSQL table | MongoDB collection |
|---|---|
| `users` | `users` |
| `alert_thresholds` | `alert_thresholds` |
| `cameras` | `cameras` |
| `queue_records` | `queue_records` |
| `alerts` | `alerts` |

Database name: `qsr_db`

MongoDB connection string for a local instance:

```text
mongodb://localhost:27017/
```

### MongoDB document flow

```mermaid
flowchart TD
    A[("PostgreSQL qsr_db")] --> B["Read Tables"]
    B --> C["Convert Rows to Documents"]
    C --> D["Connect to MongoDB"]
    D --> E[("MongoDB qsr_db")]
    E --> F["Verify Collection Counts"]
```

---

## 10. PostgreSQL to MongoDB Migration

The migration utility is located at:

```text
backend/copy_postgres_to_mongo.py
```

Run it from the `backend/` directory:

```powershell
python .\copy_postgres_to_mongo.py
```

### What the script does

1. Connects to PostgreSQL using the backend settings.
2. Discovers the PostgreSQL tables.
3. Reads the records from each table.
4. Connects to the local MongoDB server.
5. Converts the records into MongoDB documents.
6. Replaces the corresponding MongoDB collections with the copied records.
7. Prints the number of documents copied for each collection.

### Important data-safety warning

The current script uses `delete_many({})` on each destination collection before inserting the copied records.

**Do not run it against MongoDB collections containing data that must be preserved without first backing them up.**

This is a one-time copy operation. Changes made later in PostgreSQL are not automatically synchronized to MongoDB.

The migration utility also requires review if the database contains unsupported values, binary data, or data types requiring explicit conversion.

---

## 11. Backend API Architecture

The backend is implemented using FastAPI.

Main application entry point:

```text
backend/app/main.py
```

### API request flow

```mermaid
sequenceDiagram
    participant UI as React Dashboard
    participant API as FastAPI
    participant DB as PostgreSQL

    UI->>API: HTTP request
    API->>API: Validate request
    API->>API: Authenticate if required
    API->>DB: Execute database operation
    DB-->>API: Return data
    API-->>UI: JSON response
    UI->>UI: Update dashboard
```

### API capabilities

The existing application includes routes for:

- User registration and login.
- Current-user information.
- Camera creation, listing, retrieval, status, and deletion.
- Queue-record creation, latest record, and history.
- Alert listing and acknowledgement.
- Threshold retrieval and updates.
- Dashboard summary information.

### API documentation

When the backend is running, open:

- Swagger UI: `http://127.0.0.1:8000/docs`
- OpenAPI schema: `http://127.0.0.1:8000/openapi.json`

The exact endpoint paths, HTTP methods, request bodies, and authentication requirements can be inspected in Swagger UI.

---

## 12. Frontend Dashboard

The dashboard is implemented with React and Vite.

### Dashboard responsibilities

- Display application status.
- Communicate with the FastAPI backend.
- Authenticate users.
- Present camera information.
- Show available queue analytics and alerts.
- Provide an interface for operational monitoring.

### Frontend request flow

```mermaid
flowchart TD
    A["React Components"] --> B["API Client: src/api.js"]
    B --> C["HTTP Request"]
    C --> D["FastAPI Backend"]
    D --> E["JSON Response"]
    E --> F["Update React State"]
    F --> G["Render Dashboard"]
```

### Local dashboard URL

```text
http://127.0.0.1:5173/
```

This is a local development URL. It is not a publicly hosted dashboard.

---

## 13. Installation and Setup

### Prerequisites

Install or configure:

- Python compatible with the project's dependencies.
- Node.js and npm.
- PostgreSQL.
- MongoDB Community Server.
- Git.
- A compatible environment for the installed PyTorch and Ultralytics packages.

The YOLO model file `yolo11n.pt` should be present in the project root.

### Step 1 — Clone the repository

```powershell
git clone https://github.com/AkramKhan543719/qsr-queue-management.git
cd qsr-queue-management
```

### Step 2 — Configure the backend environment

```powershell
cd backend
```

Create and activate a virtual environment if one is not already available:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

If PowerShell blocks virtual-environment activation, use an approved alternative shell or configure the environment according to your organization's policies.

### Step 3 — Configure environment variables

Create `backend/.env` using the configuration expected by `backend/app/config.py`.

Example template:

```dotenv
APP_NAME=QSR Queue Management
APP_ENV=development
DATABASE_URL=postgresql+psycopg://USERNAME:PASSWORD@localhost:5432/qsr_db
SECRET_KEY=REPLACE_WITH_A_SECURE_RANDOM_SECRET
ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
```

Replace the database username and password with your own values. Ensure the database URL uses the variable name expected by the application; the current settings class defines `database_url`.

**Never commit the actual `.env` file, database passwords, tokens, or secret keys.**

### Step 4 — Prepare PostgreSQL

Create the `qsr_db` database in PostgreSQL if it does not already exist.

Ensure the configured database user has the necessary permissions.

Database tables must be created using the project's existing initialization or migration procedure. Inspect the backend setup before running database initialization commands.

### Step 5 — Confirm MongoDB is running

On Windows, check the MongoDB service:

```powershell
Get-Service *Mongo*
```

Test connectivity:

```powershell
python -c "from pymongo import MongoClient; c=MongoClient('mongodb://localhost:27017/', serverSelectionTimeoutMS=3000); print(c.admin.command('ping'))"
```

A successful response normally contains:

```text
{'ok': 1.0}
```

### Step 6 — Install frontend dependencies

Open a second PowerShell terminal:

```powershell
cd frontend
npm install
```

---

## 14. Running the Project

Run the services in separate terminals.

### Terminal 1 — Backend

From the `backend/` directory:

```powershell
uvicorn app.main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

### Terminal 2 — Frontend

From the `frontend/` directory:

```powershell
npm run dev
```

If PowerShell blocks the npm script, use:

```powershell
npm.cmd run dev
```

Dashboard:

```text
http://127.0.0.1:5173/
```

### Terminal 3 — Video processing

From the project root, with the required Python dependencies installed:

```powershell
python process_videos.py
```

Run video processing only after the backend, database configuration, authentication configuration, and video paths are ready.

---

## 15. Processing Videos

Recorded videos are stored in:

```text
videos/
```

Current intended inputs:

- `V1.mp4`
- `V2.mp4`
- `V3.mp4`
- `V4.mp4`
- `V5.mp4`

Check that each file exists before processing.

```powershell
Get-ChildItem .\videos -File
```

Run the processor:

```powershell
python process_videos.py
```

### Processing checklist

- [ ] Required video files are present.
- [ ] YOLO model is available.
- [ ] Python dependencies are installed.
- [ ] PostgreSQL is running.
- [ ] FastAPI backend is running.
- [ ] API credentials are configured.
- [ ] Video processing completes without errors.
- [ ] Queue records are received by the API.
- [ ] Database records are verified.
- [ ] Dashboard reflects the latest records.

The actual number of records produced depends on the video contents, processing interval, script behavior, and existing database state.

---

## 16. Development Phases

The project can be organized into the following development phases.

```mermaid
flowchart TD
    P1["Phase 1: Project Setup"] --> P2["Phase 2: Backend and PostgreSQL"]
    P2 --> P3["Phase 3: API and Authentication"]
    P3 --> P4["Phase 4: React Dashboard"]
    P4 --> P5["Phase 5: YOLO Video Processing"]
    P5 --> P6["Phase 6: MongoDB Connectivity and Copy"]
    P6 --> P7["Phase 7: DeepStream Integration"]
    P7 --> P8["Phase 8: Accurate Queue Analytics"]
    P8 --> P9["Phase 9: Testing and Deployment"]
```

### Phase 1 — Project setup

- Establish the repository structure.
- Configure Python and frontend dependencies.
- Prepare the video and model directories.
- Initialize Git and publish the repository.

### Phase 2 — Backend and PostgreSQL

- Configure SQLAlchemy.
- Define database models and schemas.
- Prepare tables for users, cameras, queue records, alerts, and thresholds.
- Verify database connectivity.

### Phase 3 — REST API and authentication

- Implement registration and login.
- Add camera management.
- Add queue-record endpoints.
- Add alert and threshold endpoints.
- Verify requests through Swagger UI.

### Phase 4 — Frontend dashboard

- Create the React application.
- Configure the API client.
- Connect the dashboard to FastAPI.
- Display camera and analytics information.

### Phase 5 — YOLO video processing

- Load the YOLO model.
- Read video frames with OpenCV.
- Detect people.
- Generate preliminary analytics.
- Send queue records to FastAPI.

### Phase 6 — MongoDB integration

- Install PyMongo.
- Confirm MongoDB server connectivity.
- Create the migration utility.
- Copy PostgreSQL records to MongoDB.
- Verify document counts.

### Phase 7 — DeepStream integration

- Review the analytics abstraction.
- Define inference configuration.
- Implement the DeepStream pipeline and metadata extraction.
- Connect edge analytics output to the backend.
- Test performance on the target NVIDIA hardware.

This phase is not complete merely because the starter files exist.

### Phase 8 — Accurate queue analytics

- Define queue regions of interest.
- Track people across frames.
- Reduce duplicate counts.
- Measure entry, waiting, and service events.
- Estimate waiting time using observed service rates.
- Validate results against manually measured ground truth.

### Phase 9 — Testing and deployment

- Test API routes and database operations.
- Validate video processing.
- Add error handling and observability.
- Secure credentials and access controls.
- Deploy the frontend and backend.
- Configure production database connections.
- Verify the deployed system end to end.

---

## 17. Testing and Verification

### Verify PostgreSQL tables

From the backend directory:

```powershell
python -c "from sqlalchemy import create_engine, inspect; from app.config import settings; e=create_engine(settings.database_url); print(inspect(e).get_table_names())"
```

Expected table names include:

```text
users
alert_thresholds
cameras
queue_records
alerts
```

### Verify MongoDB

```powershell
python -c "from pymongo import MongoClient; d=MongoClient('mongodb://localhost:27017/')['qsr_db']; print({c:d[c].count_documents({}) for c in d.list_collection_names()})"
```

### Run automated tests

From the project root:

```powershell
python -m pytest tests/
```

Test results depend on the installed dependencies and test configuration.

### Verify the dashboard

1. Start the backend.
2. Start the frontend.
3. Log in.
4. Confirm backend connectivity.
5. Confirm cameras and records are visible.
6. Process a test video.
7. Confirm the newly generated records appear.

---

## 18. DeepStream Integration

NVIDIA DeepStream is intended to provide an accelerated video analytics pipeline for compatible NVIDIA hardware.

### Proposed edge architecture

```mermaid
flowchart LR
    A["Camera or RTSP Stream"] --> B["DeepStream Pipeline"]
    B --> C["Hardware-Accelerated Inference"]
    C --> D["Object Tracking"]
    D --> E["Queue Analytics"]
    E --> F["Metadata Client"]
    F --> G["FastAPI Backend"]
    G --> H[("PostgreSQL")]
    G --> I["React Dashboard"]
```

### Intended benefits

- Hardware-accelerated inference.
- Support for continuous camera streams.
- More efficient processing of multiple video sources.
- Metadata-driven analytics.
- A path toward real-time queue monitoring.

The current `deepstream/` files are starter integration components. A working pipeline, compatible inference configuration, model integration, metadata extraction, and hardware validation are still required.

---

## 19. Current Limitations

The current implementation is a prototype rather than a production-ready queue management platform.

1. **Queue detection:** Detected people are used as a preliminary queue-length estimate; actual queue membership is not established.
2. **Waiting-time accuracy:** The fixed 30-second multiplier is not calibrated to actual service times.
3. **Object tracking:** Persistent tracking across frames is not yet established by the current processing description.
4. **Video processing:** Recorded-video processing does not by itself provide live camera analytics.
5. **MongoDB synchronization:** The migration is one-time, not continuous.
6. **MongoDB data replacement:** The migration script clears destination collections before copying.
7. **DeepStream:** Starter files do not constitute a complete inference pipeline.
8. **Deployment:** The local development URLs are not publicly accessible production endpoints.
9. **Testing:** Production-scale load, reliability, and accuracy testing remain necessary.

---

## 20. Future Enhancements

### Computer vision

- Queue-region detection.
- Multi-object tracking.
- Customer entry and exit counting.
- Queue abandonment detection.
- Service counter occupancy.
- Congestion detection.

### Analytics

- Average and percentile waiting times.
- Queue-length trends.
- Service-rate analysis.
- Peak-hour reports.
- Per-camera performance comparisons.

### Backend and data

- Scheduled database backups.
- Reliable event processing.
- Incremental or event-based synchronization where required.
- Database migration management.
- API rate limiting and improved audit logging.

### Frontend

- Real-time dashboard updates.
- Queue history charts.
- Camera health monitoring.
- Configurable alert thresholds.
- Date and camera filters.
- Downloadable reports.

### Production deployment

- Containerized services.
- Secure secret management.
- HTTPS.
- Monitoring and structured logs.
- Automated testing and deployment.
- NVIDIA edge-device integration.

---

## 21. Git Workflow

### Repository

[QSR Queue Management — GitHub](https://github.com/AkramKhan543719/qsr-queue-management)

### Check current changes

```powershell
git status
```

### Add and commit changes

```powershell
git add .
git commit -m "Describe your changes"
```

### Push to GitHub

```powershell
git push
```

### Important repository practices

- Keep `.env` and real credentials out of Git.
- Avoid committing virtual environments and `node_modules/`.
- Check video and model file sizes before uploading.
- Confirm that all intended video files are tracked.
- Back up database data separately from source code.
- Review staged changes before committing.

---

## 22. Troubleshooting

| Problem | What to check |
|---|---|
| PostgreSQL connection failure | Database service, credentials, database name, and URL |
| MongoDB connection refused | MongoDB service and local connection string |
| `mongosh` not recognized | MongoDB Shell installation and PATH |
| `DATABASE_URL` attribute error | Use the actual settings attribute `database_url` |
| Frontend API errors | Backend URL, CORS settings, authentication, and backend logs |
| npm script blocked | Try `npm.cmd run dev` in PowerShell |
| YOLO model not found | Confirm `yolo11n.pt` exists at the configured path |
| Video not processed | Check the video filename, path, processor logic, and console output |
| MongoDB collections empty | Confirm migration completion and collection names |
| GitHub push rejected | Check remote URL, authentication, file-size limits, and branch status |

---

## Conclusion

The QSR Queue Management System establishes a foundation for AI-assisted restaurant queue monitoring by combining video processing, YOLO-based person detection, FastAPI services, PostgreSQL storage, MongoDB migration tooling, and a React dashboard.

The next major engineering priorities are accurate queue-region tracking, validated waiting-time estimation, complete DeepStream integration, and reliable production deployment.

**Repository:** [github.com/AkramKhan543719/qsr-queue-management](https://github.com/AkramKhan543719/qsr-queue-management)

