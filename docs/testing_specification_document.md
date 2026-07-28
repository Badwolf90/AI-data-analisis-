# Comprehensive Testing & QA Specification Document
## AI Data Analysis Platform

**Versi QA:** 1.0.0  
**Framework Testing Utama:** Pytest + Pytest-Cov  
**Target Coverage Minimal:** >= 90% Code Coverage  
**Kategori Testing:** Unit Test, Integration Test, API Test, Machine Learning Test, Frontend Test  

---

## 1. Matriks Cakupan Pengujian (`backend/tests/`)

```text
backend/tests/
├── conftest.py                   # Pytest Session Fixtures (Classification Dataset, FastAPI TestClient)
├── test_unit_services.py        # Unit Testing (Security Hashing, JWT Tokens, Copilot Interpreter)
├── test_integration_db.py       # Integration Testing (Async SQLAlchemy Models & Services)
├── test_api_endpoints.py        # API Endpoint Testing (Root Health, Swagger Docs, Auth Routes)
└── test_ml_engine.py            # ML Pipeline Testing (Validator, Cleaner, Encoder, Scaler, 11 Algos, Optuna, SHAP, AutoML)
```

---

## 2. Rincian Kategori Test Suite

### 2.1 Unit Testing (`test_unit_services.py`)
* **Password Hashing:** Menguji fungsi `get_password_hash` dan `verify_password` menggunakan algoritma `bcrypt`.
* **JWT Security Tokens:** Menguji pembentukan dan pendokodean token akses JWT (`create_access_token`, `decode_token`).
* **Copilot Interpreter:** Menguji regenerasi narasi komunikasi Bahasa Indonesia untuk metrik (*Accuracy, F1-Score, ROC-AUC*).

### 2.2 Machine Learning & AutoML Engine Testing (`test_ml_engine.py`)
* **Data Loader & Validation:** Memastikan matriks dataset tervalidasi dengan kolom target yang sesuai.
* **Preprocessing Pipeline:** Menguji `DataCleaner` (median imputation), `DataEncoder` (label encoding), dan `DataScaler` (StandardScaler).
* **11 Candidate Algorithms:** Menguji instantiasi dan pelatihan 11 algoritma supervised learning (*RandomForest, ExtraTrees, GradientBoosting, AdaBoost, DecisionTree, LogisticRegression/Ridge, SVM, KNN, XGBoost, LightGBM, CatBoost*).
* **Optuna Hyperparameter Optimization:** Menguji fungsi pencarian Bayesian *N-Trials* Optuna.
* **SHAP Explainable AI:** Menguji kalkulasi *Shapley Values* untuk pengurutan pengaruh fitur global.
* **Full AutoML Pipeline:** Menguji orchestrasi utuh engine AutoML dari dataset mentah hingga *Leaderboard Ranking*.

### 2.3 API Endpoint Testing (`test_api_endpoints.py`)
* **Root Health Check (`GET /`):** Memastikan status layanan bernilai `"online"`.
* **OpenAPI Documentation (`GET /docs`):** Memastikan dokumentasi Swagger UI dapat diakses.
* **Auth Validation (`POST /api/v1/auth/login`):** Memastikan penanganan error input tidak valid.

---

## 3. Cara Menjalankan Seluruh Suite Pengujian

### 3.1 Menjalankan Testing Backend via Pytest
Buka terminal dan navigasikan ke direktori `backend/`:

```bash
cd backend
python -m pytest tests/ -v
```

### 3.2 Menjalankan Testing dengan Coverage Report (Minimal 90%)
Untuk menghasilkan laporan persentase cakupan kode (*Code Coverage Report*):

```bash
python -m pytest tests/ --cov=app --cov-report=term-missing
```

### 3.3 Menjalankan Testing Frontend React Component
Navigasikan ke direktori `frontend/` dan jalankan script pengujian:

```bash
cd frontend
npm test
```
