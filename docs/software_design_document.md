# Software Design Document (SDD)
## AI Data Analysis Platform

**Versi:** 1.0.0  
**Tanggal:** 27 Juli 2026  
**Status:** Approved for Architecture & Technical Plan  
**Peran:** Senior Software Architect, Senior ML Engineer, Senior Full Stack Developer, DevOps Engineer, & Dosen Pembimbing Skripsi  

---

## Daftar Isi
1. [Analisis Kebutuhan Sistem](#1-analisis-kebutuhan-sistem)
2. [Functional Requirements (FR)](#2-functional-requirements-fr)
3. [Non-Functional Requirements (NFR)](#3-non-functional-requirements-nfr)
4. [User Roles & Permissions (RBAC)](#4-user-roles--permissions-rbac)
5. [Spesifikasi Use Case](#5-spesifikasi-use-case)
6. [User Journey Map](#6-user-journey-map)
7. [Activity Diagrams](#7-activity-diagrams)
8. [Sequence Diagrams](#8-sequence-diagrams)
9. [Class Diagram](#9-class-diagram)
10. [Entity Relationship Diagram (ERD)](#10-entity-relationship-diagram-erd)
11. [Struktur Folder Frontend & Backend](#11-struktur-folder-frontend--backend)
12. [Rancangan API Endpoint](#12-rancangan-api-endpoint)
13. [Rancangan Database Schema (PostgreSQL DDL)](#13-rancangan-database-schema-postgresql-ddl)
14. [Rancangan Authentication & Authorization Flow](#14-rancangan-authentication--authorization-flow)
15. [Rancangan Machine Learning Pipeline](#15-rancangan-machine-learning-pipeline)
16. [Rancangan Explainable AI (XAI) Pipeline](#16-rancangan-explainable-ai-xai-pipeline)
17. [Rancangan AutoML Pipeline](#17-rancangan-automl-pipeline)
18. [Rancangan AI Copilot Workflow (LLM Engine)](#18-rancangan-ai-copilot-workflow-llm-engine)
19. [Rancangan Deployment Architecture](#19-rancangan-deployment-architecture)
20. [Rancangan Docker Architecture](#20-rancangan-docker-architecture)
21. [Rancangan CI/CD Pipeline](#21-rancangan-cicd-pipeline)
22. [Architectural Decision Records (ADR) & Justifikasi Desain](#22-architectural-decision-records-adr--justifikasi-desain)

---

## 1. Analisis Kebutuhan Sistem

### 1.1 Latar Belakang & Masalah
Dalam era *Data-Driven Decision Making*, banyak organisasi dan peneliti menghadapi kendala teknis (pemrograman Python/R, pemahaman mendalam algoritma ML, interpretasi model kompleks, dan penyusunan laporan teknis). **AI Data Analysis Platform** dirancang sebagai solusi *No-Code/Low-Code Data Science Platform* yang mengintegrasikan pengolahan data, pencarian model terbaik (AutoML), transparansi model (*Explainable AI*), asisten berbasis LLM (*AI Copilot*), serta pembuatan dokumen laporan otomatis (*PDF/DOCX/Jupyter Notebook*).

### 1.2 Tujuan Utama
1. **Demokratisasi Data Science:** Memungkinkan non-programmer melakukan *End-to-End Data Science Lifecycle*.
2. **Otomatisasi Model Building:** Menjalankan AutoML secara otomatis (hyperparameter tuning, ensembling, feature selection).
3. **Transparansi & Kepercayaan (Trustworthy AI):** Menyediakan penjelasan *global* dan *local* (SHAP & LIME) untuk keputusan model.
4. **Interaktivitas Berbasis AI:** Menyediakan AI Copilot kontekstual yang dapat menjawab pertanyaan tentang dataset dan hasil eksekusi model.
5. **Efisiensi Pelaporan:** Menggenerasi laporan profesional siap saji hanya dalam beberapa klik.

---

## 2. Functional Requirements (FR)

| ID | Modul | Deskripsi Kebutuhan Fungsional |
| :--- | :--- | :--- |
| **FR-01** | **Authentication** | Sistem harus mendukung Registrasi, Login, Logout, Refresh Token, Reset Password, dan OAuth2 (Google Login). |
| **FR-02** | **Data Management** | Pengguna dapat mengunggah dataset dalam format CSV, Excel (XLSX), Parquet, dan JSON (maksimal 500MB via UI). |
| **FR-03** | **Data Preprocessing** | Sistem menyediakan fitur pembersihan data: Handling Missing Values (Imputation), Outlier Removal, Normalization/Scaling, Encoding (One-Hot, Label Encoding), dan Feature Selection. |
| **FR-04** | **Exploratory Data Analysis (EDA)** | Sistem menampilkan statistik deskriptif otomatis, distribusi data, analisis korelasi, missing value heatmap, dan visualisasi interaktif (Plotly/Chart.js). |
| **FR-05** | **AutoML Engine** | Sistem dapat melakukan pemodelan otomatis untuk tugas Supervised Learning (Klasifikasi & Regresi), melakukan hyperparameter optimization (Optuna), dan membandingkan performa berbagai algoritma (Random Forest, XGBoost, LightGBM, SVM, Neural Nets). |
| **FR-06** | **Explainable AI (XAI)** | Sistem harus menghasilkan penjelasan model menggunakan SHAP (Summary Plot, Bar Plot, Waterfall Plot, Force Plot) dan LIME untuk sampel data individu. |
| **FR-07** | **AI Copilot (LLM)** | Sistem menyediakan fitur chat interaktif kontekstual yang memahami statistik dataset, hasil AutoML, dan memberikan rekomendasi aksi dalam bahasa alami. |
| **FR-08** | **Auto Report Generation** | Sistem dapat menggenerasi dokumen laporan lengkap dalam format PDF, DOCX, dan Jupyter Notebook (`.ipynb`). |
| **FR-09** | **Real-time Progress Tracking** | Sistem mengirimkan pembaruan status pelatihan model & XAI secara *real-time* ke frontend menggunakan WebSockets/Server-Sent Events (SSE). |
| **FR-10** | **Model Deployment & Inference** | Pengguna dapat mengunduh model (*.pkl / *.onnx*) dan melakukan uji inferensi langsung melalui UI REST API Sandbox. |

---

## 3. Non-Functional Requirements (NFR)

| ID | Kategori | Spesifikasi Kebutuhan Non-Fungsional | Target Metrik |
| :--- | :--- | :--- | :--- |
| **NFR-01** | **Performance** | API Response Time untuk permintaan standar (non-heavy ML). | $\le 200\text{ ms}$ (p95) |
| **NFR-02** | **Scalability** | Asynchronous Task Processing menggunakan Celery & Redis untuk menangani *heavy computation* (AutoML & XAI). | Scale up worker hingga 10 node |
| **NFR-03** | **Security** | Proteksi OWASP Top 10: JWT Auth dengan `HttpOnly` Cookie, CORS restriction, Rate Limiting (100 req/min), Encrypted Storage (AES-256 for credentials). | Pass Vulnerability Scan (Zero High/Critical) |
| **NFR-04** | **Availability** | Ketersediaan layanan platform berbasis containerization & load balancer. | $99.9\%$ Uptime SLA |
| **NFR-05** | **Usability** | Desain Antarmuka Glassmorphism Modern, Dark/Light Mode, Fully Responsive (Mobile, Tablet, Desktop), Accessible (WCAG 2.1 AA). | Usability Score > 85 (SUS) |
| **NFR-06** | **Maintainability** | Clean Architecture (Separation of Concerns), Modular Codebase, Type Annotations (TypeScript & Python Pydantic). | Test Coverage $\ge 80\%$ |

---

## 4. User Roles & Permissions (RBAC)

| Peran (Role) | Hak Akses (Permissions) |
| :--- | :--- |
| **Admin** | Full System Access, User Management, Resource Quota Configuration, Audit Logs Monitoring, Model Registry Cleanup. |
| **Data Analyst / Practitioner** | Upload Dataset, Run Preprocessing, Execute AutoML & XAI, Chat with AI Copilot, Export Reports, Manage Own Projects. |
| **Viewer / Guest** | Read-Only Access pada Dashboard publik/shared, View Visualizations & Generated Reports (Tidak bisa execute AutoML/Copilot). |

---

## 5. Spesifikasi Use Case

### 5.1 Diagram Use Case Utama
```mermaid
graph TD
    User((Data Practitioner))
    Admin((System Admin))

    subgraph AI Data Analysis Platform
        UC1[UC-01: Authentication & Profile Management]
        UC2[UC-02: Upload & Preview Dataset]
        UC3[UC-03: Execute Preprocessing & EDA]
        UC4[UC-04: Run AutoML Experiment]
        UC5[UC-05: Generate XAI Explanations]
        UC6[UC-06: Interact with AI Copilot]
        UC7[UC-07: Export Automated Report]
        UC8[UC-08: Manage System Resources & Users]
    end

    User --> UC1
    User --> UC2
    User --> UC3
    User --> UC4
    User --> UC5
    User --> UC6
    User --> UC7

    Admin --> UC1
    Admin --> UC8
```

### 5.2 Tabel Spesifikasi Use Case Kunci: Run AutoML Experiment (UC-04)

* **Use Case ID:** UC-04
* **Nama Use Case:** Run AutoML Experiment
* **Aktor Utama:** Data Practitioner
* **Deskripsi:** Pengguna menentukan target variable, jenis masalah (Klasifikasi/Regresi), budget waktu, dan memulai proses otomatisasi ML.
* **Pre-condition:** Dataset telah diunggah dan dibersihkan (Preprocessing selesai).
* **Post-condition:** Model-model terlatih tersimpan, metrik evaluasi dihasilkan, dan model terbaik dipilih secara otomatis.
* **Main Flow:**
  1. Pengguna memilih dataset yang telah dipreprocess.
  2. Pengguna memilih kolom target (label) dan jenis tugas ML.
  3. Pengguna mengklik tombol "Start AutoML".
  4. Frontend mengirim permintaan POST `/api/v1/automl/start` ke API Gateway.
  5. API Gateway mengirim pesan tugas ke Celery Queue via Redis Broker.
  6. Celery Worker mengeksekusi pipeline Optuna + Scikit-Learn/XGBoost.
  7. Worker memperbarui status pekerjaan secara real-time via WebSocket.
  8. Setelah selesai, metrik perbandingan ditampilkan pada Leaderboard UI.
* **Alternative Flow:**
  * *4a. Parameter tidak valid:* API mengembalikan HTTP 400 Bad Request, UI menampilkan error notification.
  * *6a. Execution Timeout:* Task dibatalkan oleh Celery timeout handler, pengguna menerima notifikasi "Time Limit Exceeded".

---

## 6. User Journey Map

```mermaid
journey
    title User Journey: End-to-End Analysis on AI Data Analysis Platform
    section 1. Ingestion
      Sign in to Platform: 5: User
      Upload Dataset (CSV/Excel): 4: User
      View Automated EDA & Data Quality: 5: User
    section 2. Preparation
      Configure Imputation & Scaling: 4: User
      Apply Preprocessing Pipeline: 5: User
    section 3. Model Building
      Select Target Column & Criteria: 5: User
      Trigger AutoML Engine: 5: User
      Watch Real-time Training Progress: 4: User
    section 4. Explainability & Insights
      Review Model Leaderboard: 5: User
      Inspect SHAP Global Feature Importance: 5: User
      Run Local Sample Prediction (LIME): 4: User
    section 5. Copilot & Reporting
      Ask AI Copilot for Recommendations: 5: User
      Generate PDF/DOCX/Notebook Report: 5: User
      Download Trained Model Artifacts: 5: User
```

---

## 7. Activity Diagrams

### 7.1 Activity Diagram: Data Ingestion & Preprocessing Pipeline
```mermaid
stateDiagram-v2
    [*] --> UploadFile
    UploadFile --> ValidateFormat
    ValidateFormat --> FileInvalid: Format Error
    FileInvalid --> UploadFile
    ValidateFormat --> ParseData: Format Valid
    
    ParseData --> GenerateAutomatedEDA
    GenerateAutomatedEDA --> DisplayEDAUI
    
    DisplayEDAUI --> SelectPreprocessingOptions
    SelectPreprocessingOptions --> ExecutePipeline
    
    state ExecutePipeline {
        [*] --> HandleMissingValues
        HandleMissingValues --> EncodeCategoricals
        EncodeCategoricals --> ScaleFeatures
        ScaleFeatures --> RemoveOutliers
        RemoveOutliers --> [*]
    }
    
    ExecutePipeline --> SaveCleanedDataset
    SaveCleanedDataset --> [*]
```

---

## 8. Sequence Diagrams

### 8.1 Sequence Diagram: Execution AutoML (Async Processing via Celery & WebSockets)

```mermaid
sequenceDiagram
    autonumber
    actor User as User (Browser)
    participant FE as Next.js Frontend
    participant API as FastAPI Backend
    participant DB as PostgreSQL DB
    participant Broker as Redis Broker
    participant Worker as Celery ML Worker
    participant WS as WebSocket Server

    User->>FE: Click "Start AutoML"
    FE->>API: POST /api/v1/automl/start {dataset_id, target, config}
    API->>DB: Create Experiment Record (status: 'PENDING')
    API->>Broker: Push Task (experiment_id)
    API-->>FE: HTTP 202 Accepted {task_id, experiment_id}
    FE->>WS: Connect WebSocket /ws/experiments/{experiment_id}
    
    Broker->>Worker: Consume Task
    Worker->>DB: Update Status ('RUNNING')
    Worker->>WS: Broadcast Event: "Training Started (0%)"
    WS-->>FE: Real-time UI Update (Progress Bar)

    loop AutoML Optimization (Optuna Trials)
        Worker->>Worker: Train Trial Model & Evaluate
        Worker->>WS: Broadcast Event: "Trial N Completed - Acc: 0.94"
        WS-->>FE: Update Live Training Chart
    end

    Worker->>DB: Save Best Model Artifact Path & Metrics (status: 'COMPLETED')
    Worker->>WS: Broadcast Event: "AutoML Finished"
    WS-->>FE: Render Model Leaderboard UI
```

### 8.2 Sequence Diagram: AI Copilot Interaction Workflow

```mermaid
sequenceDiagram
    autonumber
    actor User as User
    participant FE as Frontend UI
    participant API as FastAPI Backend
    participant Agent as Copilot LLM Agent
    participant DB as Postgres (Vector/Metadata)
    participant LLM as OpenAI / Anthropic / Local LLM

    User->>FE: Ask question: "Why is Feature X important?"
    FE->>API: POST /api/v1/copilot/chat {dataset_id, model_id, prompt}
    API->>DB: Fetch Dataset EDA & SHAP Summaries
    API->>Agent: Construct Prompt Context (Metadata + XAI Summary + User Prompt)
    Agent->>LLM: Send Structured Context Prompt
    LLM-->>Agent: Streaming Tokens Response
    Agent-->>API: Stream Chunk
    API-->>FE: Server-Sent Events (SSE) Stream
    FE-->>User: Render Typographic AI Response Real-time
```

---

## 9. Class Diagram

```mermaid
classDiagram
    class User {
        +UUID id
        +String email
        +String hashed_password
        +Role role
        +DateTime created_at
        +authenticate()
    }

    class Dataset {
        +UUID id
        +UUID user_id
        +String file_name
        +String file_path
        +Int row_count
        +Int column_count
        +JSON metadata_schema
        +get_summary_stats()
    }

    class PreprocessingPipeline {
        +UUID id
        +UUID dataset_id
        +JSON imputation_strategy
        +JSON encoding_strategy
        +JSON scaling_strategy
        +execute_transform()
    }

    class Experiment {
        +UUID id
        +UUID dataset_id
        +String target_column
        +String task_type
        +Status status
        +DateTime created_at
        +run_automl()
    }

    class MLModel {
        +UUID id
        +UUID experiment_id
        +String algorithm_name
        +JSON hyperparameters
        +JSON evaluation_metrics
        +String artifact_path
        +predict(input_data)
    }

    class XAIExplainer {
        +UUID id
        +UUID model_id
        +JSON shap_values
        +JSON feature_importance
        +generate_shap_plots()
        +generate_lime_explanation(sample_id)
    }

    class CopilotSession {
        +UUID id
        +UUID user_id
        +UUID dataset_id
        +List~Message~ history
        +send_message(prompt)
    }

    User "1" -- "0..*" Dataset : owns
    Dataset "1" -- "0..1" PreprocessingPipeline : configures
    Dataset "1" -- "0..*" Experiment : used_in
    Experiment "1" -- "1..*" MLModel : produces
    MLModel "1" -- "1..1" XAIExplainer : explained_by
    User "1" -- "0..*" CopilotSession : participates
```

---

## 10. Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    USERS ||--o{ DATASETS : "uploads"
    USERS ||--o{ COPILOT_SESSIONS : "creates"
    USERS ||--o{ REPORTS : "generates"
    
    DATASETS ||--o| PREPROCESSING_CONFIGS : "has"
    DATASETS ||--o{ EXPERIMENTS : "source_for"
    
    EXPERIMENTS ||--|{ MODELS : "produces"
    MODELS ||--o| XAI_REPORTS : "analyzed_by"
    MODELS ||--o{ PREDICTIONS : "generates"
    
    COPILOT_SESSIONS ||--|{ COPILOT_MESSAGES : "contains"
    
    USERS {
        uuid id PK
        string email UK
        string password_hash
        string full_name
        enum role
        boolean is_active
        timestamp created_at
    }

    DATASETS {
        uuid id PK
        uuid user_id FK
        string name
        string file_path
        bigint file_size
        jsonb columns_schema
        jsonb summary_stats
        timestamp uploaded_at
    }

    PREPROCESSING_CONFIGS {
        uuid id PK
        uuid dataset_id FK
        jsonb imputation_rules
        jsonb scaling_rules
        jsonb encoding_rules
        timestamp updated_at
    }

    EXPERIMENTS {
        uuid id PK
        uuid dataset_id FK
        string target_column
        enum problem_type
        enum status
        int time_budget_seconds
        timestamp created_at
    }

    MODELS {
        uuid id PK
        uuid experiment_id FK
        string algorithm
        jsonb hyperparameters
        jsonb metrics
        string artifact_s3_key
        boolean is_best_model
        timestamp trained_at
    }

    XAI_REPORTS {
        uuid id PK
        uuid model_id FK
        jsonb global_shap_summary
        jsonb feature_importances
        string shap_plot_s3_key
        timestamp generated_at
    }

    COPILOT_SESSIONS {
        uuid id PK
        uuid user_id FK
        uuid dataset_id FK
        string title
        timestamp created_at
    }

    COPILOT_MESSAGES {
        uuid id PK
        uuid session_id FK
        enum sender
        text message_text
        jsonb token_usage
        timestamp sent_at
    }

    REPORTS {
        uuid id PK
        uuid user_id FK
        uuid experiment_id FK
        enum report_format
        string file_s3_key
        timestamp generated_at
    }
```

---

## 11. Struktur Folder Frontend & Backend

```text
ai-data-analysis-platform/
├── docker-compose.yml
├── docker-compose.override.yml
├── README.md
│
├── frontend/                        # Next.js 14+ (App Router) + Vanilla/Tailwind CSS
│   ├── package.json
│   ├── tsconfig.json
│   ├── next.config.js
│   ├── public/
│   │   └── assets/
│   └── src/
│       ├── app/                     # Next.js Pages & Layouts
│       │   ├── (auth)/
│       │   │   ├── login/page.tsx
│       │   │   └── register/page.tsx
│       │   ├── dashboard/
│       │   │   ├── page.tsx
│       │   │   ├── datasets/page.tsx
│       │   │   ├── experiments/page.tsx
│       │   │   ├── xai/page.tsx
│       │   │   └── copilot/page.tsx
│       │   ├── layout.tsx
│       │   └── page.tsx
│       ├── components/              # Modular UI Components
│       │   ├── ui/                  # Buttons, Cards, Inputs, Modals
│       │   ├── charts/              # Plotly & Chart.js Dynamic Wrappers
│       │   ├── dataset/             # Data Grid, EDA Stats Cards
│       │   ├── automl/              # Leaderboard, Progress Bars
│       │   ├── xai/                 # SHAP Waterfalls, LIME Viewers
│       │   └── copilot/             # Chat Drawer & Stream Renderer
│       ├── hooks/                   # React Hooks (useWebSocket, useAuth)
│       ├── services/                # Axios/Fetch API Clients
│       ├── store/                   # Zustand Global State
│       └── styles/                  # Global CSS, Design System Tokens
│
└── backend/                         # FastAPI Modular Application
    ├── requirements.txt
    ├── Dockerfile
    ├── alembic/                     # DB Migration Scripts
    └── app/
        ├── main.py                  # FastAPI Entrypoint & Middleware
        ├── core/                    # Core Infrastructure
        │   ├── config.py            # Environment Variables & Settings
        │   ├── security.py          # JWT, Hashing, OAuth Providers
        │   ├── database.py          # SQLAlchemy Async Engine Session
        │   └── celery_app.py        # Celery Task Queue Initialization
        ├── api/                     # REST API Controllers (v1)
        │   ├── v1/
        │   │   ├── router.py
        │   │   ├── auth.py
        │   │   ├── datasets.py
        │   │   ├── preprocessing.py
        │   │   ├── automl.py
        │   │   ├── xai.py
        │   │   ├── copilot.py
        │   │   └── reports.py
        │   └── websockets/          # WebSocket Handlers
        │       └── progress.py
        ├── models/                  # SQLAlchemy ORM Models
        │   ├── user.py
        │   ├── dataset.py
        │   ├── experiment.py
        │   └── model.py
        ├── schemas/                 # Pydantic Request/Response Schemas
        │   ├── dataset_schema.py
        │   ├── automl_schema.py
        │   └── xai_schema.py
        ├── services/                # Business Logic Services
        │   ├── eda_service.py
        │   ├── preprocessing_service.py
        │   ├── copilot_agent.py
        │   └── report_generator.py
        ├── ml_engine/               # Core Machine Learning & XAI Core
        │   ├── pipelines/
        │   │   ├── feature_engineering.py
        │   │   └── model_trainer.py
        │   ├── automl/
        │   │   ├── optuna_tuner.py
        │   │   └── model_selector.py
        │   └── xai/
        │       ├── shap_explainer.py
        │       └── lime_explainer.py
        └── tasks/                   # Celery Background Workers
            ├── automl_tasks.py
            ├── xai_tasks.py
            └── report_tasks.py
```

---

## 12. Rancangan API Endpoint

| Method | Endpoint | Auth | Request Body / Params | Description |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/auth/register` | No | `{email, password, full_name}` | Registrasi pengguna baru |
| `POST` | `/api/v1/auth/login` | No | `{email, password}` | Login & Dapatkan JWT token |
| `POST` | `/api/v1/datasets/upload` | Bearer | `multipart/form-data (file)` | Unggah file dataset |
| `GET` | `/api/v1/datasets/{id}/eda` | Bearer | `-` | Dapatkan statistik deskriptif & EDA |
| `POST` | `/api/v1/preprocessing/apply` | Bearer | `{dataset_id, config_json}` | Terapkan pembersihan data |
| `POST` | `/api/v1/automl/start` | Bearer | `{dataset_id, target_col, time_budget}` | Mulai eksekusi AutoML |
| `GET` | `/api/v1/automl/experiments/{id}`| Bearer | `-` | Ambil status & leaderboard model |
| `POST` | `/api/v1/xai/shap/explain` | Bearer | `{model_id}` | Hasilkan SHAP global explanation |
| `POST` | `/api/v1/xai/lime/sample` | Bearer | `{model_id, sample_data_json}` | Hasilkan LIME local explanation |
| `POST` | `/api/v1/copilot/chat` | Bearer | `{session_id, message}` | Chat dengan AI Copilot (SSE Stream) |
| `POST` | `/api/v1/reports/generate` | Bearer | `{experiment_id, format: "pdf"}` | Generasi laporan otomatis |
| `WS` | `/ws/experiments/{id}` | Token | `-` | Real-time WebSocket training progress |

---

## 13. Rancangan Database Schema (PostgreSQL DDL)

```sql
-- Extension for UUID generation
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enum Definitions
CREATE TYPE user_role AS ENUM ('ADMIN', 'ANALYST', 'VIEWER');
CREATE TYPE problem_type AS ENUM ('CLASSIFICATION', 'REGRESSION');
CREATE TYPE experiment_status AS ENUM ('PENDING', 'RUNNING', 'COMPLETED', 'FAILED');
CREATE TYPE report_format AS ENUM ('PDF', 'DOCX', 'NOTEBOOK');

-- Users Table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(150) NOT NULL,
    role user_role DEFAULT 'ANALYST',
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Datasets Table
CREATE TABLE datasets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(255) NOT NULL,
    file_path VARCHAR(512) NOT NULL,
    file_size BIGINT NOT NULL,
    row_count INT NOT NULL,
    column_count INT NOT NULL,
    columns_schema JSONB NOT NULL,
    summary_stats JSONB,
    uploaded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Experiments Table
CREATE TABLE experiments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    dataset_id UUID NOT NULL REFERENCES datasets(id) ON DELETE CASCADE,
    target_column VARCHAR(128) NOT NULL,
    task_type problem_type NOT NULL,
    status experiment_status DEFAULT 'PENDING',
    time_budget_seconds INT DEFAULT 300,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Models Table
CREATE TABLE models (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    experiment_id UUID NOT NULL REFERENCES experiments(id) ON DELETE CASCADE,
    algorithm VARCHAR(100) NOT NULL,
    hyperparameters JSONB NOT NULL,
    metrics JSONB NOT NULL,
    artifact_s3_key VARCHAR(512) NOT NULL,
    is_best_model BOOLEAN DEFAULT FALSE,
    trained_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- XAI Reports Table
CREATE TABLE xai_reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_id UUID UNIQUE NOT NULL REFERENCES models(id) ON DELETE CASCADE,
    global_shap_summary JSONB NOT NULL,
    feature_importances JSONB NOT NULL,
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for performance optimization
CREATE INDEX idx_datasets_user_id ON datasets(user_id);
CREATE INDEX idx_experiments_dataset_id ON experiments(dataset_id);
CREATE INDEX idx_models_experiment_id ON models(experiment_id);
```

---

## 14. Rancangan Authentication & Authorization Flow

```mermaid
graph TD
    Client[Client Browser] -->|1. POST /login credentials| API[FastAPI Auth Controller]
    API -->|2. Verify Hash| DB[(PostgreSQL)]
    DB -->|3. Valid User| API
    API -->|4. Generate Access Token JWT 15m & Refresh Token 7d| API
    API -->|5. Return Access Token Body + Refresh Token HttpOnly Cookie| Client
    
    Client -->|6. API Request + Bearer JWT| Gateway[FastAPI Security Middleware]
    Gateway -->|7. Verify RSA Signature & Expire Time| Gateway
    Gateway -->|8. Extract User Role & Check RBAC| Authorization
    Authorization -->|Pass| Resource[Protected Service Endpoint]
    Authorization -->|Fail| HTTP403[HTTP 403 Forbidden]
```

---

## 15. Rancangan Machine Learning Pipeline

```mermaid
flowchart LR
    A[Raw Dataset] --> B[Data Validation & Schema Check]
    B --> C[Imputation Engine]
    C --> D[Categorical Encoder]
    D --> E[Feature Scaler]
    E --> F[Train/Test Split 80:20]
    F --> G[Cross-Validation Folds]
    G --> H[Model Training Core]
    H --> I[Evaluation & Metrics Computation]
    I --> J[Artifact Serialization .pkl/.onnx]
```

---

## 16. Rancangan Explainable AI (XAI) Pipeline

1. **Global Explanations:**
   * **SHAP Summary Plot:** Menghitung TreeSHAP (untuk model berbasis pohon) atau KernelSHAP (untuk model umum) pada test dataset untuk mengukur dampak global setiap fitur terhadap target.
   * **Feature Importance Bar Chart:** Menyusun peringkat fitur berdasarkan $\text{mean}(|\text{SHAP value}|)$.

2. **Local Explanations:**
   * **LIME (Local Interpretable Model-agnostic Explanations):** Membuat model surrogate lokal linier untuk sampel prediksi tertentu, menjelaskan mengapa suatu data individu diklasifikasikan ke kelas tertentu.
   * **SHAP Waterfall/Force Plot:** Menampilkan kontribusi positif/negatif masing-masing variabel terhadap nilai prediksi baseline.

---

## 17. Rancangan AutoML Pipeline

```mermaid
graph TD
    A[Preprocessed Data] --> B[Optuna Study Initialization]
    
    subgraph Hyperparameter Optimization Loop
        B --> C{Trial Allocation}
        C -->|Algorithm 1| D[Random Forest Tuning]
        C -->|Algorithm 2| E[XGBoost Tuning]
        C -->|Algorithm 3| F[LightGBM Tuning]
        C -->|Algorithm 4| G[SVM / Neural Net Tuning]
        
        D --> H[K-Fold Cross Validation]
        E --> H
        F --> H
        G --> H
        
        H --> I[Calculate Objective Score F1/RMSE]
        I --> J[Optuna TPE Sampler Update]
    end
    
    J --> K{Time/Trial Budget Reached?}
    K -->|No| C
    K -->|Yes| L[Select Best Trial per Algorithm]
    L --> M[Build Stacking Ensemble Model]
    M --> N[Save Top Models to Registry]
```

---

## 18. Rancangan AI Copilot Workflow (LLM Engine)

```mermaid
graph TD
    UserQuery[User Prompt] --> ContextManager[Context Builder Engine]
    
    subgraph Dynamic Context Retrieval
        ContextManager --> MetaFetcher[Fetch Dataset Schema & Stats]
        ContextManager --> MetricFetcher[Fetch Model Metrics & Leaderboard]
        ContextManager --> XAIFetcher[Fetch SHAP Importance Rank]
    end
    
    ContextManager --> SystemPrompt[Construct System & User Prompt]
    SystemPrompt --> Guardrail[Safety & Security Guardrail]
    Guardrail --> LLM[LLM Engine API OpenAI/Local Llama3]
    LLM --> Streamer[Server-Sent Events SSE Response]
    Streamer --> UI[Interactive UI Drawer]
```

---

## 19. Rancangan Deployment Architecture

```mermaid
graph TD
    UserClient[User Web Browser] --> Nginx[Nginx Reverse Proxy / Load Balancer]
    
    subgraph App Cluster
        Nginx --> Frontend[Next.js App Container]
        Nginx --> BackendAPI[FastAPI Instances Gunicorn/Uvicorn]
    end

    subgraph Async Processing Infrastructure
        BackendAPI --> RedisBroker[(Redis Queue & Cache)]
        RedisBroker --> Worker1[Celery Worker 1 AutoML]
        RedisBroker --> Worker2[Celery Worker 2 XAI & Reports]
    end

    subgraph Data Layer
        BackendAPI --> PostgresDB[(PostgreSQL Primary DB)]
        Worker1 --> PostgresDB
        Worker2 --> PostgresDB
        Worker1 --> S3Storage[(MinIO / AWS S3 Artifact Storage)]
        Worker2 --> S3Storage
    end
```

---

## 20. Rancangan Docker Architecture

### `docker-compose.yml` (Spesifikasi Multi-Container Infrastructure)
```yaml
version: '3.8'

services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://localhost:8000
    depends_on:
      - backend

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/aidb
      - REDIS_URL=redis://redis:6379/0
      - S3_ENDPOINT=http://minio:9000
    depends_on:
      - postgres
      - redis

  celery_worker:
    build:
      context: ./backend
      dockerfile: Dockerfile
    command: celery -A app.core.celery_app worker --loglevel=info -c 4
    environment:
      - DATABASE_URL=postgresql://user:pass@postgres:5432/aidb
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - backend
      - redis

  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: aidb
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  minio:
    image: minio/minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: minioadmin
      MINIO_ROOT_PASSWORD: minioadminpassword
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - minio_data:/data

volumes:
  postgres_data:
  minio_data:
```

---

## 21. Rancangan CI/CD Pipeline

```mermaid
graph LR
    Push[Git Push / PR to Main] --> LintTest[Stage 1: Lint & Code Style]
    LintTest --> UnitTests[Stage 2: Unit & Integration Tests]
    UnitTests --> DockerBuild[Stage 3: Build & Push Docker Images]
    DockerBuild --> StagingDeploy[Stage 4: Auto Deploy to Staging]
    StagingDeploy --> IntegrationTest[Stage 5: E2E Cypress/Playwright Tests]
    IntegrationTest --> ProdDeploy[Stage 6: Zero Downtime Production Deployment]
```

---

## 22. Architectural Decision Records (ADR) & Justifikasi Desain

### ADR-01: FastAPI untuk Backend Framework
* **Kontek/Keputusan:** Memilih FastAPI dibandingkan Flask atau Django.
* **Alasan:** FastAPI berbasis `asyncio` yang memiliki performa sangat tinggi (sebanding dengan Node.js dan Go), dukungan bawaan OpenAPI/Swagger documentation, serta integrasi Pydantic untuk validasi data otomatis dan ketat.

### ADR-02: Celery & Redis untuk Task Processing Asinkron
* **Kontek/Keputusan:** Pemrosesan AutoML & SHAP XAI membutuhkan waktu tinggi (heavy CPU/GPU computation).
* **Alasan:** Menjalankan ML training di HTTP thread utama akan menyebabkan request timeout dan merusak UX. Celery terbukti robust untuk distributed task queue dengan Redis sebagai in-memory message broker berlatensi rendah.

### ADR-03: SHAP & LIME untuk Explainable AI (XAI)
* **Kontek/Keputusan:** Pemilihan kerangka kerja akuntabilitas model.
* **Alasan:** SHAP memberikan fondasi matematik solid berbasis Shapley Values dari Game Theory (menjamin konsistensi dan alokasi kontribusi yang adil), sedangkan LIME memberikan kecepatan komputasi untuk eksplanasi lokal cepat.

### ADR-04: Optuna untuk AutoML Tuning Engine
* **Kontek/Keputusan:** Memilih Optuna dibandingkan GridSearchCV/RandomizedSearchCV.
* **Alasan:** Optuna menggunakan algoritma *Tree-structured Parzen Estimator (TPE)* yang efisien dalam pencarian ruang hyperparameter, serta mendukung *pruning* (early stopping) untuk trial yang tidak menjaningkan sehingga menghemat waktu komputasi.

### ADR-05: Next.js + Vanilla/Tailwind CSS untuk Frontend
* **Kontek/Keputusan:** Menggunakan Next.js App Router.
* **Alasan:** Next.js mendukung Server-Side Rendering (SSR) & Static Site Generation (SSG) untuk SEO optimal, didukung arsitektur komputasi modern, React Server Components, dan integrasi mudah dengan visualisasi grafik interaktif.

---
*Dokumen SDD ini dirancang secara komprehensif sebagai standar acuan pengembangan perangkat lunak kelas industri dan akademis.*
