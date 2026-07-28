# Production-Ready PostgreSQL Database Schema & Migration Document
## AI Data Analysis Platform

**Versi Schema:** 1.0.0  
**RDBMS Engine:** PostgreSQL 15+  
**Migration Tool:** Alembic Async  
**Fitur Utama Schema:**  
- **UUID Primary Keys:** Format String(36) UUIDv4 untuk identifikasi unik terdistribusi tanpa masalah auto-increment sequential risk.  
- **Soft Delete Support:** Kolom `deleted_at` (nullable timezone-aware timestamp) pada seluruh entitas utama.  
- **Automatic Timestamps:** Kolom `created_at` dan `updated_at` bawaan dengan `UTC` timezone.  
- **Integritas Data:** Enforcing Foreign Key Constraints (`ON DELETE CASCADE` / `ON DELETE SET NULL`) & Check Constraints.  
- **Optimasi Performa Query:** B-Tree Indexes & Composite Indexes pada kolom relasi yang sering difilter.  

---

## 1. Spesifikasi 11 Tabel Database

### 1.1 Tabel `users`
* **Fungsi:** Menyimpan data kredensial, peran (*role*), dan status akun pengguna.
* **Kolom Utama:** `id` (PK), `email` (UK), `password_hash`, `full_name`, `role` (Enum: ADMIN, ANALYST, VIEWER), `is_active`, `created_at`, `updated_at`, `deleted_at`.
* **Indeks:** `idx_users_email` (Unique), `idx_users_email_active`, `idx_users_deleted_at`.

### 1.2 Tabel `projects`
* **Fungsi:** Menyimpan ruang kerja (*workspace/project*) yang dimiliki oleh pengguna.
* **Kolom Utama:** `id` (PK), `user_id` (FK -> `users.id` CASCADE), `name`, `description`, `created_at`, `updated_at`, `deleted_at`.
* **Indeks:** `idx_projects_user_id`, `idx_projects_user_deleted`.

### 1.3 Tabel `datasets`
* **Fungsi:** Menyimpan berkas dataset (`CSV`, `Parquet`, `XLSX`) beserta ringkasan metadata dan statistik EDA.
* **Kolom Utama:** `id` (PK), `user_id` (FK -> `users.id` CASCADE), `project_id` (FK -> `projects.id` CASCADE), `name`, `file_path`, `file_size`, `row_count`, `col_count`, `columns_schema` (JSON), `summary_stats` (JSON), `created_at`, `updated_at`, `deleted_at`.
* **Constraints:** `CHECK (file_size >= 0)`.
* **Indeks:** `idx_datasets_user_id`, `idx_datasets_project_id`, `idx_datasets_user_deleted`.

### 1.4 Tabel `experiments` (History)
* **Fungsi:** Menyimpan riwayat eksekusi AutoML (*task type, target column, status*).
* **Kolom Utama:** `id` (PK), `dataset_id` (FK -> `datasets.id` CASCADE), `target_column`, `task_type` (Enum: CLASSIFICATION, REGRESSION), `status` (Enum: PENDING, RUNNING, COMPLETED, FAILED), `time_budget_seconds`, `created_at`, `updated_at`, `deleted_at`.
* **Indeks:** `idx_experiments_dataset_id`, `idx_experiments_status`, `idx_experiments_dataset_status`.

### 1.5 Tabel `models`
* **Fungsi:** Menyimpan artefak model terlatih, metrik performa (*accuracy, f1, mse*), hyperparameter, dan SHAP feature importance summary.
* **Kolom Utama:** `id` (PK), `experiment_id` (FK -> `experiments.id` CASCADE), `algorithm`, `hyperparameters` (JSON), `metrics` (JSON), `artifact_path`, `is_best_model`, `shap_summary` (JSON), `created_at`, `updated_at`, `deleted_at`.
* **Indeks:** `idx_models_experiment_id`, `idx_models_is_best`, `idx_models_experiment_best`.

### 1.6 Tabel `predictions`
* **Fungsi:** Menyimpan riwayat pengujian inferensi model dan sampel data masukan beserta hasil prediksinya.
* **Kolom Utama:** `id` (PK), `model_id` (FK -> `models.id` CASCADE), `input_data` (JSON), `prediction_result` (JSON), `created_at`, `updated_at`, `deleted_at`.
* **Indeks:** `idx_predictions_model_id`.

### 1.7 Tabel `reports`
* **Fungsi:** Menyimpan metadata dan file laporan hasil analisis otomatis (*PDF, DOCX, JSON*).
* **Kolom Utama:** `id` (PK), `user_id` (FK -> `users.id` CASCADE), `experiment_id` (FK -> `experiments.id` CASCADE), `title`, `format`, `file_path`, `content_json` (JSON), `created_at`, `updated_at`, `deleted_at`.
* **Indeks:** `idx_reports_user_id`, `idx_reports_experiment_id`.

### 1.8 Tabel `logs` (Audit Log)
* **Fungsi:** Catatan jejak audit (*audit trail*) keamanan dan aktivitas sistem.
* **Kolom Utama:** `id` (PK), `user_id` (FK -> `users.id` SET NULL), `action`, `resource`, `details` (JSON), `ip_address`, `created_at`.
* **Indeks:** `idx_logs_user_id`, `idx_logs_action`, `idx_logs_created_at`.

### 1.9 Tabel `api_keys`
* **Fungsi:** Kunci API (*API Tokens*) untuk integrasi programmatic pengguna.
* **Kolom Utama:** `id` (PK), `user_id` (FK -> `users.id` CASCADE), `key_name`, `hashed_key` (UK), `prefix`, `expires_at`, `is_active`, `created_at`, `updated_at`, `deleted_at`.
* **Indeks:** `idx_api_keys_user_id`, `idx_api_keys_prefix`, `idx_api_keys_prefix_active`.

### 1.10 Tabel `sessions`
* **Fungsi:** Sesi aktif pengguna (*Refresh Tokens*) dengan pencatatan IP dan User Agent.
* **Kolom Utama:** `id` (PK), `user_id` (FK -> `users.id` CASCADE), `refresh_token` (UK), `ip_address`, `user_agent`, `expires_at`, `is_revoked`, `created_at`, `updated_at`.
* **Indeks:** `idx_sessions_user_id`, `idx_sessions_refresh_token`.

### 1.11 Tabel `notifications`
* **Fungsi:** Notifikasi *real-time* atau pesan status pelatihan model pengguna.
* **Kolom Utama:** `id` (PK), `user_id` (FK -> `users.id` CASCADE), `title`, `message`, `type` (Enum: INFO, SUCCESS, WARNING, ERROR), `is_read`, `created_at`, `updated_at`, `deleted_at`.
* **Indeks:** `idx_notifications_user_id`, `idx_notifications_is_read`.

---

## 2. Menjalankan Migrasi Database Alembic

```bash
# 1. Navigasi ke direktori backend
cd backend

# 2. Jalankan migrasi ke versi terbaru (PostgreSQL / SQLite)
alembic upgrade head

# 3. Pembatalan migrasi jika diperlukan (Rollback)
alembic downgrade -1
```
