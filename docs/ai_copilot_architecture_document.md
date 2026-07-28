# AI Data Science Copilot Module Architecture Document
## AI Data Analysis Platform

**Versi Modul:** 1.0.0  
**Gaya Komunikasi:** Bahasa Indonesia Komunikatif & Natural (Senior Data Scientist Persona)  
**Tujuan Modul:** Memberikan penjelasan intuitif, interpretasi hasil AutoML/XAI, dan rekomendasi bisnis strategis bagi pengguna.  

---

## 1. Struktur Modul AI Copilot Engine (`app/copilot_engine/`)

```text
backend/app/copilot_engine/
├── __init__.py               # Core Package Exports
├── prompts.py                # System Prompts & Senior Data Scientist Persona
├── interpreter.py            # Domain Interpreter untuk Metrik, SHAP, LIME, Grafik, & Preprocessing
└── copilot_service.py        # Conversational Orchestrator & Contextual QA Router
```

---

## 2. Kapabilitas Utama AI Copilot

### 2.1 Penjelasan Metrik Evaluasi Model
Mengonversi angka statistik teknis menjadi bahasa sehari-hari yang mudah dipahami:
* **Accuracy (Akurasi):** Menjelaskan persentase total tebakan benar model dari keseluruhan dataset pengujian.
* **Precision (Presisi):** Menjelaskan tingkat ketepatan model saat memprediksi kelas positif (mencegah *false alarm*).
* **Recall (Sensitivitas):** Menjelaskan sejauh mana model mampu menjaring seluruh kasus positif di lapangan (mencegah *missed case*).
* **F1-Score:** Menjelaskan keseimbangan harmonis antara Presisi dan Recall.
* **ROC AUC:** Menjelaskan kemampuan diferensiasi model dalam memisahkan kelas positif dan negatif.

### 2.2 Penjelasan Explainable AI (SHAP & LIME)
* **SHAP Global Importance:** Mengidentifikasi 5 fitur teratas yang memegang peranan paling dominan dalam menentukan hasil prediksi model secara keseluruhan.
* **LIME Local Sample Explanation:** Menganalisis keputusan spesifik model pada satu baris sampel data individual, menjelaskan variabel pendorong (+)/penarik (-).

### 2.3 Penjelasan Preprocessing & Cleaning Data
Memberikan justifikasi teknis di balik tindakan pembersihan data:
* **Missing Value Imputation:** Mengapa nilai hilang diisi median/modus dan dampaknya bagi model.
* **Categorical Encoding:** Mengapa variabel teks harus diubah menjadi skala angka (*Label Encoding*).
* **Feature Scaling:** Mengapa penyetaraan skala (*StandardScaler*) mencegah pembobotan tidak adil.

### 2.4 Penjelasan Grafik & Visualisasi
Panduan membaca grafik secara intuitif (Histogram, Scatter Plot, Confusion Matrix, ROC Curve) beserta identifikasi tren dan anomali.

### 2.5 Data Insights & Rekomendasi Bisnis Strategis
Setiap jawaban AI Copilot dilengkapi dengan **Insight Data Scientist** dan **Rekomendasi Aksi Konkret** yang dapat langsung dieksekusi oleh tim bisnis/manajemen.
