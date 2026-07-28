# Backend Clean Architecture Document
## AI Data Analysis Platform

**Versi:** 1.0.0  
**Framework:** FastAPI + Python 3.11+  
**Database ORM:** SQLAlchemy 2.0 (Async Engine) & Alembic Migrations  
**Arsitektur:** Clean Architecture (Repository Pattern + Service Layer)  
**Keamanan:** JWT Authentication (Access + Refresh Token), Password Hashing (bcrypt), Role-Based Access Control (RBAC), & Rate Limiting Middleware  

---

## 1. Structure Codebase

```text
backend/
├── Dockerfile                  # Production Container Setup
├── alembic.ini                 # DB Migration Configuration
├── alembic/                    # Async Alembic Scripts
│   ├── env.py
│   └── script.py.mako
├── requirements.txt            # Dependency Specifications
├── .env.example                # Environment Variable Template
├── .env                        # Active Environment Settings
├── main.py                     # Root Launcher
└── app/
    ├── main.py                 # FastAPI Application Initialization & Middleware
    ├── core/                   # Core Infrastructure & Security
    │   ├── config.py           # Pydantic BaseSettings
    │   ├── security.py         # JWT Token & Password Hashing
    │   ├── database.py         # Async SQLAlchemy Engine & Session
    │   ├── dependencies.py     # JWT & RBAC Injectors
    │   ├── logging.py          # Structured Logger
    │   └── rate_limiter.py     # Custom Sliding-Window Rate Limiter Middleware
    ├── models/                 # SQLAlchemy ORM Models (Base & Tables)
    │   └── __init__.py         # User, Project, Dataset, Experiment, MLModel, Prediction, Report, AuditLog
    ├── schemas/                # Pydantic Request/Response Data Validation
    │   ├── __init__.py
    │   └── all_schemas.py
    ├── repositories/           # Data Access Layer (Repository Pattern)
    │   ├── __init__.py
    │   ├── base.py             # Generic BaseRepository[T]
    │   └── all_repositories.py # UserRepository, ProjectRepository, DatasetRepository, etc.
    ├── services/               # Business Logic Layer
    │   ├── __init__.py
    │   └── services.py         # AuthService, ProjectService, DatasetService, AutoMLService, XAIService, etc.
    └── api/                    # Controllers / REST API Endpoints
        ├── router.py           # API Router Aggregator
        └── endpoints/          # Endpoint Controllers
            ├── auth.py
            ├── users.py
            ├── projects.py
            ├── datasets.py
            ├── automl.py
            ├── xai.py
            ├── predictions.py
            ├── reports.py
            └── audit_logs.py
```

---

## 2. Ringkasan Fitur Backend Berhasil Terimplementasi

1. **Authentication & User Management:**
   * Registrasi pengguna baru dengan hash sandi `bcrypt`.
   * Login dengan verifikasi kredensial & penerbitan token JWT (`Access Token` 60m & `Refresh Token` 7d).
   * Middleware autentikasi `get_current_user` dan kontrol akses peran `require_role([ADMIN, ANALYST, VIEWER])`.

2. **Project & Workspace Management:**
   * API CRUD untuk memisahkan ruang kerja dan dataset pengguna.

3. **Dataset & Preprocessing Service:**
   * Endpoint upload file (`CSV`, `XLSX`, `Parquet`).
   * Penghitungan otomatis statistik deskriptif EDA (*mean, std, min, max, null_count, dtypes*).
   * Pipeline pembersihan data otomatis: imputasi *missing values*, *label encoding*, dan *standard scaling*.

4. **AutoML Engine:**
   * Eksekusi otomatis algoritma Supervised Learning (Random Forest & Gradient Boosting).
   * Pembagian data train/test (80:20), evaluasi metrik (Accuracy, F1-Score, MSE, R2-Score), serta serialisasi model terbaik ke registri `.joblib`.

5. **Explainable AI (XAI) Engine:**
   * Fitur transparansi model global via SHAP importance summary.
   * Eksplanasi sampel lokal menggunakan surrogate model LIME contribution scores.

6. **Inference & Prediction API:**
   * Inference Sandbox API untuk menguji model terdaftar secara langsung dan mengembalikan hasil prediksi beserta nilai probabilitasnya.

7. **Report Generation & Audit Logging:**
   * Generasi otomatis dokumen laporan JSON/PDF untuk eksperimen ML.
   * Catatan jejak audit (*Audit Logging*) untuk melacak aktivitas pengguna dan IP Address.

8. **Keamanan & Rate Limiting:**
   * `RateLimiterMiddleware` bawaan untuk mencegah penyalahgunaan API (Limit: 100 req/menit per Client IP).
   * Dokumentasi interaktif Swagger OpenAPI di `/docs` dan ReDoc di `/redoc`.

---

## 3. Cara Menjalankan Backend secara Lokal

```bash
# 1. Navigasi ke folder backend
cd backend

# 2. Buat virtual environment (opsional)
python -m venv venv
source venv/bin/activate  # On Linux/macOS
# venv\Scripts\activate   # On Windows

# 3. Install dependensi
pip install -r requirements.txt

# 4. Jalankan Server FastAPI dengan Uvicorn
python main.py
```

Setelah server berjalan, dokumentasi Swagger OpenAPI dapat diakses di: **`http://localhost:8000/docs`**.
