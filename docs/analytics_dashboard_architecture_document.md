# Interactive Plotly Analytics Dashboard Architecture Document
## AI Data Analysis Platform

**Versi Dashboard:** 1.0.0  
**Library Visualisasi:** Plotly.js Interactive Graphics  
**Jumlah Widget KPI:** 9 Resource & Performance Telemetry Widgets  
**Jumlah Chart Plotly:** 7 Tipe Grafik Interaktif (Zoom, Pan, Hover, Legend Filtering)  

---

## 1. Matriks 9 Resource KPI Widgets (`AnalyticsDashboard.jsx`)

| Widget Name | Telemetry Metric | Default Value | Status & Detail |
|---|---|---|---|
| **Total User** | Jumlah Pengguna Terdaftar | `1,420 Users` | +14% Pertumbuhan Bulanan |
| **Datasets** | Total File Terdaftar | `342 Datasets` | CSV, Parquet, Excel, JSON |
| **Training** | Eksperimen AutoML Aktif | `18 Runs` | Optuna Hyperparameter Tuning |
| **Prediction** | Total Permintaan Inferensi | `1,482,900` | +120k requests/day |
| **Accuracy** | Akurasi Model Terbaik | `96.4%` | GradientBoosting (#1 Leaderboard) |
| **Storage** | Kapasitas Storage Digunakan | `42.8 GB` | 42.8% dari Total 100 GB |
| **CPU Usage** | Utilisasi Processor | `34%` | 8 Core Multi-processing |
| **RAM Usage** | Utilisasi Memory Utama | `48%` | 15.3 GB / 32 GB RAM |
| **GPU VRAM** | Utilisasi Memory GPU | `62%` | NVIDIA RTX 4090 (24GB VRAM) |

---

## 2. Rincian 7 Grafik Interaktif Plotly

1. **Line Chart (`Scatter + Lines`):**
   * **Deskripsi:** Visualisasi real-time pergerakan akurasi model (%) dan penurunan *Validation Loss* selama proses pelatihan AutoML.
2. **Pie Chart (`Donut Hole 0.5`):**
   * **Deskripsi:** Distribusi format dataset yang tersimpan (*CSV 45%, Parquet 30%, Excel 15%, JSON 10%*).
3. **Heatmap Chart (`5x5 Viridis Color Scale`):**
   * **Deskripsi:** Matriks korelasi antar fitur (*Age, Income, Tenure, Support_Calls, Churn_Prob*) untuk mendeteksi multikolinearitas.
4. **Radar Chart (`Polar Scatter`):**
   * **Deskripsi:** Evaluasi multi-dimensi model terbaik (*Accuracy, Precision, Recall, F1-Score, ROC-AUC, Latency Speed*).
5. **Scatter Plot (`2D Markers Distribution`):**
   * **Deskripsi:** Sebaran titik sampel pelanggan (*Age vs Annual Income*) dikategorikan berdasarkan warna pelanggan *Retained (Hijau)* dan *Churned (Merah)*.
6. **Boxplot Chart (`Multi-Series Box`):**
   * **Deskripsi:** Distribusi *latency* waktu respons inferensi (dalam milidetik) untuk setiap algoritma (*RandomForest, XGBoost, LightGBM, CatBoost*).
7. **Bar Chart (`Leaderboard Performance Bar`):**
   * **Deskripsi:** Peringkat komparatif skor F1 dari **11 kandidat algoritma ML** dalam matriks visualisasi penuh.
