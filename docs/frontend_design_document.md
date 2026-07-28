# Modern React Frontend Architecture Document
## AI Data Analysis Platform

**Versi Frontend:** 1.0.0  
**Framework Utama:** React 18 + Vite  
**Estetika UI/UX:** Vercel & Linear Obsidian Dark Mode (Glassmorphism, Clean Borders, Neon Accents)  
**Komponen Library:** TailwindCSS, Framer Motion, Recharts, Lucide Icons  

---

## 1. Struktur Folder Frontend (`frontend/src/`)

```text
frontend/
├── package.json
├── index.html
├── vite.config.js
├── tailwind.config.js
├── postcss.config.js
└── src/
    ├── main.jsx              # React Entrypoint
    ├── App.jsx               # Master Layout Router State
    ├── index.css             # Tailwind Directives & Glassmorphism Utilities
    ├── components/
    │   └── layout/
    │       ├── Sidebar.jsx   # Linear-style Collapsible Sidebar Navigation
    │       └── Navbar.jsx    # Vercel-style Top Navigation & Search Command Palette
    └── pages/
        ├── DashboardPage.jsx     # Executive Overview & Activity Metrics
        ├── DatasetPage.jsx       # Dataset Upload & Preprocessing Inspector
        ├── VisualizationPage.jsx # Interactive EDA & SHAP Bar Charts
        ├── AutoMLPage.jsx        # AutoML Config & 11-Algorithm Leaderboard
        ├── CopilotPage.jsx       # AI Data Science Copilot Chat Interface
        ├── HistoryPage.jsx       # Registered Experiment Log & Model Versions
        ├── ReportPage.jsx        # Executive Report Generator & PDF Preview
        ├── ProfilePage.jsx       # User Credentials & API Token Manager
        └── AdminPage.jsx         # Security Audit Trail & Rate Limit Monitor
```

---

## 2. Rincian Implementasi 9 Halaman UI/UX Reusable

1. **Dashboard Page:**
   * Executive KPI Cards (*Active Datasets, Total Experiments, Best Model F1-Score, AI Copilot Queries*).
   * Visualisasi tren perbaikan akurasi model berbasis *Recharts AreaChart*.
   * Peringkat *Top Performing Models* real-time.

2. **Dataset Manager Page:**
   * Area *Drag-and-Drop* pengunggahan berkas dataset (CSV, XLSX, Parquet).
   * Tabel penjelajah berkas dataset terdaftar.
   * Panel inspeksi konfigurasi pembersihan data (*Missing Values Imputation, Label Encoding, StandardScaler*).

3. **Visualization & EDA Page:**
   * *Scatter Plot* hubungan variabel (*Age vs Income Distribution*).
   * *Horizontal Bar Chart* peringkat bobot fitur global SHAP (*Global Feature Importance*).

4. **AutoML Engine Page:**
   * Panel pengaturan *Target Column*, *Task Type*, dan *Time Budget*.
   * Matriks seleksi **11 Algoritma Supervised Learning** (*RandomForest, ExtraTrees, GradientBoosting, AdaBoost, DecisionTree, LogisticRegression/Ridge, SVM, KNN, XGBoost, LightGBM, CatBoost*).
   * Tabel *Leaderboard Ranking* diperingkat otomatis berdasarkan skor F1/Accuracy.

5. **AI Copilot Page:**
   * Antarmuka percakapan interaktif ber-persona *Senior Data Scientist*.
   * Menjelaskan metrik (*Accuracy, Precision, Recall, F1, ROC AUC*), penafsiran SHAP/LIME, dan justifikasi preprocessing dalam Bahasa Indonesia alami.

6. **History & Version Log Page:**
   * Tabel riwayat eksekusi AutoML dengan id eksperimen, skor utama, dan timestamp.

7. **Report Generator Page:**
   * Pratinjau laporan eksekutif lengkap dengan ringkasan metrik, tabel leaderboard, dan tombol ekspor PDF.

8. **Profile & API Credentials Page:**
   * Informasi profil pengguna dan generator kunci API (*Personal Developer Token*).

9. **Admin & Audit Trail Page:**
   * Pemantauan kesehatan sistem (*Rate Limit Status, DB Connections, Audit Logs*).
