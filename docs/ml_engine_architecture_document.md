# Modular Machine Learning Engine Architecture Document
## AI Data Analysis Platform

**Versi Modul:** 1.0.0  
**Desain Arsitektur:** Clean Architecture & Design Patterns (Factory, Strategy, Orchestrator)  
**Teknologi ML Utama:** Scikit-learn, XGBoost, LightGBM, CatBoost, Optuna, Joblib, SHAP, LIME, MLflow  

---

## 1. Struktur Folder Modul ML Engine (`app/ml_engine/`)

```text
backend/app/ml_engine/
├── __init__.py               # Core Package Exports
├── config.py                 # ML Engine & Artifact Storage Settings
├── data/
│   ├── loader.py             # CSV, XLSX, Parquet Data Loader
│   └── validator.py          # Schema & Data Quality Checks
├── preprocessing/
│   ├── cleaner.py            # Imputation (Median/Mode) & Outlier handling
│   ├── encoder.py            # Categorical Label Encoding
│   └── scaler.py             # StandardScaler, MinMaxScaler, RobustScaler
├── features/
│   ├── engineer.py           # Interaction Features & Polynomial Features
│   └── selector.py           # VarianceThreshold Feature Selection
├── models/
│   ├── models_factory.py     # Factory Pattern: Scikit-learn, XGBoost, LightGBM, CatBoost
│   └── evaluator.py          # Metrics Evaluator (Accuracy, F1, ROC-AUC, MSE, R2)
├── tuning/
│   └── optuna_tuner.py       # Optuna Bayesian Hyperparameter Optimization
├── xai/
│   ├── shap_explainer.py     # TreeSHAP & KernelSHAP Global Feature Importance
│   └── lime_explainer.py     # LIME Local Sample Explanations
├── tracking/
│   └── mlflow_tracker.py     # MLflow Experiment Tracking & Model Versioning
└── pipeline.py               # Master Orchestrator (16 Pipeline Stages)
```

---

## 2. Implementasi 16 Tahapan Pipeline Machine Learning

1. **Upload Dataset & Data Loading:** `DataLoader` membaca file format `.csv`, `.xlsx`, `.parquet`.
2. **Data Validation:** `DataValidator` memeriksa keberadaan kolom target, nilai null, baris duplikat, dan kecukupan sampel.
3. **Data Cleaning:** `DataCleaner` melakukan imputasi *missing values* secara otomatis (*median* untuk numerik, *mode* untuk kategorial).
4. **Encoding:** `DataEncoder` mengonversi fitur kategorial menjadi numerik menggunakan `LabelEncoder`.
5. **Scaling:** `DataScaler` menormalisasi distribusi fitur menggunakan `StandardScaler`.
6. **Feature Engineering:** `FeatureEngineer` membuat fitur interaksi produk antar variabel numerik (`x1 * x2`).
7. **Feature Selection:** `FeatureSelector` mengeliminasi fitur dengan varians rendah di bawah ambang batas (*VarianceThreshold*).
8. **Train-Test Split:** Membagi dataset menjadi data latih (80%) dan data uji (20%) secara acak dengan *seed reproducible*.
9. **Cross Validation:** Evaluasi performa model menggunakan 3-Fold hingga 5-Fold Cross Validation.
10. **Hyperparameter Tuning:** `OptunaHyperparameterTuner` mengoptimalkan parameter model (seperti `n_estimators`, `max_depth`, `learning_rate`) secara otomatis.
11. **Model Training:** `ModelFactory` melatih multiple algoritma berkinerja tinggi: **RandomForest, ExtraTrees, XGBoost, LightGBM, CatBoost**.
12. **Model Comparison:** Membandingkan hasil metrik antar model untuk menghasilkan *Leaderboard* peringkat.
13. **Model Evaluation:** Menghitung metrik lengkap (Accuracy, Precision, Recall, F1, ROC-AUC untuk Klasifikasi; MSE, RMSE, MAE, R2 untuk Regresi).
14. **Explainable AI (XAI):** `SHAPExplainer` menghasilkan bobot kontribusi fitur global dan `LIMEExplainer` menghasilkan penjelasan sampel lokal.
15. **Prediction & Inference:** API inferensi batch/single instance untuk pengujian model terlatih.
16. **Model Saving & Versioning:** Serialisasi biner model `.joblib` dan registrasi versi eksperimen ke **MLflow Tracking**.
