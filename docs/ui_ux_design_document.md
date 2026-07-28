# UI/UX Specification & Wireframe Document
## AI Data Analysis Platform

**Versi:** 1.0.0  
**Peran:** Senior UI/UX Designer & Product Designer  
**Inspirasi Design System:** ChatGPT (Conversational UX), Notion (Minimalist & Block Layout), Vercel (Dark Mode & Sleek Micro-interactions), Linear (Keyboard-first & Sub-pixel Borders), GitHub (Data Density & Activity Tracking)  
**Tech Stack Design:** TailwindCSS, Shadcn UI, Framer Motion  

---

## 1. Design System & Tokens (Dark & Light Mode)

### 1.1 Color Palette & Tokens (Tailwind CSS)

| Token Name | Dark Mode (Default) | Light Mode | Penggunaan |
| :--- | :--- | :--- | :--- |
| `bg-primary` | `#09090B` (Zinc 950) | `#FAFAFA` (Zinc 50) | Background halaman utama |
| `bg-surface` | `#18181B` (Zinc 900) | `#FFFFFF` (White) | Cards, Modals, Sidebar |
| `bg-elevated` | `#27272A` (Zinc 800) | `#F4F4F5` (Zinc 100) | Hover states, Active items, Input fields |
| `border-subtle` | `rgba(255,255,255,0.08)` | `rgba(0,0,0,0.08)` | Linear-style sub-pixel borders |
| `text-main` | `#F4F4F5` (Zinc 100) | `#09090B` (Zinc 950) | Primary Headings & Body Text |
| `text-muted` | `#A1A1AA` (Zinc 400) | `#71717A` (Zinc 500) | Subtitles, Labels, Icons |
| `accent-primary`| `#6366F1` (Indigo 500) | `#4F46E5` (Indigo 600) | Primary Buttons, Active Tabs, Progress Bars |
| `accent-glow` | `rgba(99,102,241,0.15)` | `rgba(79,70,229,0.10)` | Vercel-style glowing blur gradients |
| `status-success`| `#10B981` (Emerald 500) | `#059669` (Emerald 600) | Completed tasks, high accuracy badge |
| `status-warning`| `#F59E0B` (Amber 500) | `#D97706` (Amber 600) | Running tasks, warnings |
| `status-error` | `#EF4444` (Red 500) | `#DC2626` (Red 600) | Failed tasks, validation errors |

### 1.2 Typography System
* **Primary Font:** `Inter` / `Geist Sans` (San-serif modern dengan legibilitas tinggi pada density data padat).
* **Code & Data Grid Font:** `JetBrains Mono` / `Geist Mono` (Untuk matriks, angka statistik, dan kueri data).

### 1.3 Motion Design System (Framer Motion Guidelines)
* **Page Transition:** Fade & Slide Up (`opacity: 0, y: 8` $\rightarrow$ `opacity: 1, y: 0`, `duration: 0.25s, ease: [0.16, 1, 0.3, 1]`).
* **Command Palette (Cmd+K):** Scale & Overlay Blur (`scale: 0.96` $\rightarrow$ `scale: 1`, `duration: 0.15s`).
* **Micro-interactions:** Scale down on button press (`whileTap={{ scale: 0.98 }}`), smooth badge hover glow.

---

## 2. Wireframe & Layout Specifications (15 Halaman/State)

---

### Halaman 1: Landing Page

```text
+-----------------------------------------------------------------------------------+
|  [Logo] AI Platform      Features   Solutions   Docs   Pricing      [Login] [Get Started] |
+-----------------------------------------------------------------------------------+
|                                                                                   |
|         Demokratisasi Data Science dengan AutoML & Explainable AI                 |
|       Platform All-in-One: Preprocessing, Modeling, XAI, & Dynamic Copilot        |
|                                                                                   |
|                     [ Try Demo Free -> ]   [ View GitHub ]                        |
|                                                                                   |
|  +-----------------------------------------------------------------------------+  |
|  | [Interactive Product Preview Video / Animated Vercel Glassmorphic Dashboard]|  |
|  +-----------------------------------------------------------------------------+  |
|                                                                                   |
|  +--------------------------- BENTO GRID FEATURES -----------------------------+  |
|  | +-----------------------+ +-----------------------+ +---------------------+ |  |
|  | | ⚡ AutoML Engine      | | 🧠 SHAP & LIME XAI    | | 💬 AI Copilot Chat | |  |
|  | | Optuna Hyperparameter | | Transparansi Model    | | Asisten LLM Context | |  |
|  | +-----------------------+ +-----------------------+ +---------------------+ |  |
|  +-----------------------------------------------------------------------------+  |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

* **UX Rationale:** 
  * **Header Floating Blur (Vercel-style):** Header transparan fixed di atas memberikan kesan modern dan navigasi cepat.
  * **Hero CTA & Live Interactive Mockup:** Memberikan instant visual proof capability platform sebelum pengguna mendaftar.
  * **Bento Grid Layout (Linear & Notion style):** Menyajikan fitur-fitur kompleks secara terstruktur dan mudah dipahami dalam 3 detik.

---

### Halaman 2: Login Page

```text
+-----------------------------------------------------------------------------------+
|                                                                                   |
|                          +-----------------------------------+                    |
|                          |    [Logo] AI Data Platform        |                    |
|                          |    Welcome back to your workspace |                    |
|                          |                                   |                    |
|                          |  [ Continue with Google        ]  |                    |
|                          |  [ Continue with GitHub        ]  |                    |
|                          |                                   |                    |
|                          |  -------------- OR -------------- |                    |
|                          |                                   |                    |
|                          |  Email Address                    |                    |
|                          |  [ name@company.com            ]  |                    |
|                          |                                   |                    |
|                          |  Password            Forgot?      |                    |
|                          |  [ •••••••••••••••••••••••••• ]  |                    |
|                          |                                   |                    |
|                          |  [ Sign In with Email  ->      ]  |                    |
|                          |                                   |                    |
|                          |  Don't have an account? Sign up   |                    |
|                          +-----------------------------------+                    |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

* **UX Rationale:**
  * **Centered Glassmorphic Card (Shadcn UI Card):** Fokus penuh pada input tanpa distraksi latar belakang.
  * **One-click OAuth (Google/GitHub):** Mengurangi gesekan (*friction*) saat login sebesar 60%.

---

### Halaman 3: Register Page

```text
+-----------------------------------------------------------------------------------+
|                                                                                   |
|                          +-----------------------------------+                    |
|                          |    Create your Free Account       |                    |
|                          |    Step 1 of 2: Basic Info        |                    |
|                          |    [======               ] 50%    |                    |
|                          |                                   |                    |
|                          |  Full Name                        |                    |
|                          |  [ John Doe                    ]  |                    |
|                          |                                   |                    |
|                          |  Work Email                       |                    |
|                          |  [ john@company.com            ]  |                    |
|                          |                                   |                    |
|                          |  Password (Min 8 characters)      |                    |
|                          |  [ •••••••••••••••••••••••••• ]  |                    |
|                          |                                   |                    |
|                          |  Role / Usage Objective           |                    |
|                          |  ( ) Data Analyst  ( ) Student    |                    |
|                          |                                   |                    |
|                          |  [ Create Account & Continue ->]  |                    |
|                          +-----------------------------------+                    |
|                                                                                   |
+-----------------------------------------------------------------------------------+
```

* **UX Rationale:**
  * **Progress Indicator Bar:** Mengelola ekspektasi durasi onboarding pengguna.
  * **Role Badge Selection:** Mengizinkan sistem menyesuaikan default template workspace sesuai preferensi pengguna.

---

### Halaman 4: Dashboard Page

```text
+-----------------------------------------------------------------------------------+
| [Sidebar]    |  [Search / Cmd+K...]                 [Notifications]  (User Avatar) |
|--------------+--------------------------------------------------------------------|
| 🏠 Home      |  Good morning, Alex 👋                                              |
| 📁 Workspaces|  +---------------------------------------------------------------+ |
| 📊 Datasets  |  | Active Project: Customer Churn Analytics 2026                 | |
| ⚡ AutoML    |  +---------------------------------------------------------------+ |
| 🧠 XAI       |                                                                    |
| 💬 Copilot   |  +--------------- STATS BADGES (Vercel-style) -------------------+ |
| 📑 Reports   |  | Total Datasets | Total Models | Best Metric | Worker Status| |
| ⚙️ Settings  |  | 14 Files       | 42 Trained   | 96.4% Acc   | 🟢 Idle      | |
|              |  +---------------------------------------------------------------+ |
|              |                                                                    |
|              |  Recent Datasets & Experiments                             + New   |
|              |  +---------------------------------------------------------------+ |
|              |  | Name               | Rows  | Status     | Best Model  | Actions| |
|              |  |--------------------+-------+------------+-------------+--------| |
|              |  | churn_telco.csv    | 7,043 | COMPLETED  | XGBoost     | [View] | |
|              |  | credit_risk.csv    | 12.5k | RUNNING 65%| LightGBM    | [View] | |
|              |  +---------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

* **UX Rationale:**
  * **Collapsible Notion Sidebar:** Navigasi bersih yang memberikan ruang kerja luas.
  * **Linear Command Palette (`Cmd+K`):** Memungkinkan pencarian dataset, eksekusi aksi, dan navigasi cepat via keyboard.

---

### Halaman 5: Workspace Page

```text
+-----------------------------------------------------------------------------------+
| [Sidebar]    | Workspaces / Data Science Team Workspace           [+ New Project] |
|--------------+--------------------------------------------------------------------|
|              | Search projects...                              [Filter: All v]    |
|              |                                                                    |
|              | +-----------------------+  +-----------------------+               |
|              | | 📁 Telco Churn 2026   |  | 📁 Fraud Detection    |               |
|              | | 3 Datasets · 8 Models |  | 5 Datasets · 12 Models|               |
|              | | Updated 2 hours ago   |  | Updated 1 day ago     |               |
|              | | [Avatars: 👤👤👤]     |  | [Avatars: 👤👤]       |               |
|              | +-----------------------+  +-----------------------+               |
|              | +-----------------------+  +-----------------------+               |
|              | | 📁 Retail Demand Fcst |  | 📁 Medical Diagnosis  |               |
|              | | 1 Dataset · 4 Models  |  | 2 Datasets · 6 Models |               |
|              | +-----------------------+  +-----------------------+               |
+-----------------------------------------------------------------------------------+
```

* **UX Rationale:**
  * **Modular Project Cards (Notion-style):** Informasi tingkat tinggi ditampilkan dalam blok teratur dengan avatar kolaborator.

---

### Halaman 6: Dataset Page (Data Grid & Preprocessing)

```text
+-----------------------------------------------------------------------------------+
| [Sidebar]    | Workspaces / Telco Churn / churn_telco.csv       [Clean Data Wizard] |
|--------------+--------------------------------------------------------------------|
|              | [ Preview ]  [ Statistics ]  [ Missing Values ]  [ Correlation ]   |
|              |                                                                    |
|              | +----------------------------------------------------------------+ |
|              | | customerID | Gender | SeniorCitizen | Tenure | MonthlyCharges  | |
|              | |------------+--------+---------------+--------+-----------------| |
|              | | 7590-VHVEG | Female | 0             | 1      | $29.85          | |
|              | | 5575-GNVDE | Male   | 0             | 34     | $56.95          | |
|              | | 3668-QPYBK | Male   | 0             | 2      | $53.85          | |
|              | +----------------------------------------------------------------+ |
|              |  Showing 1-10 of 7,043 rows                       [<] 1 2 3 4 [>]  |
+-----------------------------------------------------------------------------------+
```

* **UX Rationale:**
  * **Density Data Grid (GitHub / Linear style):** Menampilkan kolom data dengan tipe font monospace untuk presisi numerik.
  * **Tabbed Exploration Bar:** Memisahkan pratinjau data mentah, statistik, dan missing values dalam satu tampilan tanpa reload.

---

### Halaman 7: Visualization Page

```text
+-----------------------------------------------------------------------------------+
| [Sidebar]    | Visualizations / Customer Churn EDA                               |
|--------------+--------------------------------------------------------------------|
| Chart Type   |                                                                    |
| [Bar Chart v]|  Distribution of Monthly Charges by Churn Status                   |
| X-Axis       |  +--------------------------------------------------------------+ |
| [Churn    v] |  |  700 |      [====]                                           | |
| Y-Axis       |  |  500 |      [====]          [====]                           | |
| [Monthly  v] |  |  300 |      [====]          [====]                           | |
| Color Group  |  |    0 +---------------------------------------------           | |
| [Gender   v] |  |             No Churn         Yes Churn                        | |
|              |  +--------------------------------------------------------------+ |
| [Export SVG] |  [Legend: 🟦 Male  🟪 Female]                                    | |
+-----------------------------------------------------------------------------------+
```

* **UX Rationale:**
  * **Split Controls Panel & Canvas (Plotly Integration):** Panel kontrol variabel di sebelah kiri merender grafik secara *instant reactive*.

---

### Halaman 8: AutoML Page

```text
+-----------------------------------------------------------------------------------+
| [Sidebar]    | AutoML Experiment Builder                              [Run AutoML]|
|--------------+--------------------------------------------------------------------|
| Config Panel | Training Status & Live Progress                                    |
| Target Col   | [=======================================..........] 78% (Trial 15)  |
| [ Churn  v]  | Live Best Accuracy: 84.6% (XGBoost)                                |
| Task Type    |                                                                    |
| (•) Classify | Leaderboard Model Comparison                                       |
| ( ) Regression| +---------------------------------------------------------------+ |
| Time Budget  | | Rank | Model        | Accuracy | F1-Score | AUC   | Actions   | |
| [ 5 Mins  v] | |------|--------------|----------|----------|-------|-----------| |
| Algorithms   | | 🥇 1 | XGBoost      | 0.846    | 0.812    | 0.891 | [Explain] | |
| [x] XGBoost  | | 🥈 2 | LightGBM     | 0.839    | 0.801    | 0.885 | [Explain] | |
| [x] RF       | | 🥉 3 | Random Forest| 0.821    | 0.785    | 0.862 | [Explain] | |
| [x] SVM      | +---------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

* **UX Rationale:**
  * **Real-time Live Training Bar:** Progress bar aktif dan leaderboard terupdate secara dinamis (via WebSocket) memberikan kepastian proses pada pengguna.

---

### Halaman 9: AI Copilot Page (ChatGPT Style Chat Drawer)

```text
+-----------------------------------------------------------------------------------+
| [Sidebar]    | AI Copilot Assistant -- Dataset: churn_telco.csv                   |
|--------------+--------------------------------------------------------------------|
| Main Panel   | Chat Conversation Drawer (ChatGPT Style)                           |
| (SHAP Charts | +----------------------------------------------------------------+ |
|  & Analysis) | | 👤 User: Why is 'Contract_Month-to-month' the most important   | |
|              | |       feature in XGBoost?                                       | |
|              | |                                                                | |
|              | | 🤖 Copilot: Based on TreeSHAP analysis, Month-to-month          | |
|              | | contract types contribute +0.42 to the log-odds of churning.    | |
|              | | Customers with short-term contracts are 3.4x more likely to... | |
|              | | 💡 Recommendation: Offer 15% discount for 1-year renewals.     | |
|              | +----------------------------------------------------------------+ |
|              | [ Ask Copilot about data insights or suggest actions...  ] [Send]  |
+-----------------------------------------------------------------------------------+
```

* **UX Rationale:**
  * **Conversational Context-Aware Drawer:** Pengguna dapat menanyakan pertanyaan spesifik dalam bahasa alami dan mendapatkan saran tindakan konkret secara streaming.

---

### Halaman 10: History Page

```text
+-----------------------------------------------------------------------------------+
| [Sidebar]    | Execution & Experiment History                                    |
|--------------+--------------------------------------------------------------------|
|              | Filter: [ Status: All v ] [ Date: Last 30 Days v ]                 |
|              |                                                                    |
|              | +----------------------------------------------------------------+ |
|              | | Timestamp       | Experiment Name     | Duration | Status      | |
|              | |-----------------|---------------------|----------|-------------| |
|              | | 2026-07-27 10:15| Churn_Optuna_Trial3 | 4m 12s   | 🟢 SUCCESS  | |
|              | | 2026-07-27 09:40| Preprocess_Scaling  | 0m 15s   | 🟢 SUCCESS  | |
|              | | 2026-07-26 18:20| NeuralNet_Trial1    | 10m 00s  | 🔴 FAILED   | |
|              | +----------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

* **UX Rationale:**
  * **Linear-style Compact Audit History:** Menyajikan jejak riwayat eksekusi sistem dengan indikator warna status yang kontras.

---

### Halaman 11: Report Page (Notion Block Style Report Generator)

```text
+-----------------------------------------------------------------------------------+
| [Sidebar]    | Report Generator / Telco Churn Final Report      [Export PDF/DOCX] |
|--------------+--------------------------------------------------------------------|
| Sections     | Document Canvas Preview                                            |
| [x] Exec Sum | # Executive Summary                                                |
| [x] Data EDA | Analysis performed on 7,043 records identified top churn drivers.  |
| [x] Models   |                                                                    |
| [x] XAI SHAP | ## Model Performance Leaderboard                                   |
| [x] Action   | XGBoost achieved highest accuracy (84.6%) and AUC (0.891).         |
|              |                                                                    |
|              | ## Explainable AI Insights (SHAP Summary)                          |
|              | ![SHAP Chart Preview Placeholder]                                  |
+-----------------------------------------------------------------------------------+
```

* **UX Rationale:**
  * **Modular Block Toggle (Notion-style):** Pengguna dapat menyertakan/mengecualikan bagian laporan tertentu secara interaktif sebelum mengekspor dokumen.

---

### Halaman 12: Admin Page

```text
+-----------------------------------------------------------------------------------+
| [Sidebar]    | System Administration & Metrics Monitoring                         |
|--------------+--------------------------------------------------------------------|
|              | +------------------ SYSTEM METRICS ------------------------------+ |
|              | | CPU Utilization | GPU Memory (CUDA) | Active Celery Workers     | |
|              | | [====    ] 42%  | [======  ] 65%   | 4 / 4 Nodes Active 🟢     | |
|              | +----------------------------------------------------------------+ |
|              |                                                                    |
|              | User Management                                     [+ Add User]  |
|              | +----------------------------------------------------------------+ |
|              | | Name        | Email           | Role     | Quota | Actions     | |
|              | |-------------|-----------------|----------|-------|-------------| |
|              | | Alex Dev    | alex@comp.com   | ANALYST  | 50 GB | [Edit] [Del]| |
|              | +----------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

* **UX Rationale:**
  * **Vercel Admin Health Dashboard:** Memberikan visibilitas langsung terhadap penggunaan GPU/CPU dan manajemen resource pengguna.

---

### Halaman 13: Profile Page

```text
+-----------------------------------------------------------------------------------+
| [Sidebar]    | Account Profile Settings                                           |
|--------------+--------------------------------------------------------------------|
|              | [Avatar]  Alex Developer                                           |
|              |           alex.developer@company.com · Senior Data Scientist       |
|              |                                                                    |
|              | Personal Info                                                      |
|              | Full Name: [ Alex Developer                   ]                    |
|              | Bio:       [ Senior Data Analyst exploring AutoML     ]            |
|              |                                                                    |
|              | API Tokens & Keys                                   [+ Create New] |
|              | +----------------------------------------------------------------+ |
|              | | Token Name  | Created    | Last Used   | Scope     | Action    | |
|              | |-------------|------------|-------------|-----------|-----------| |
|              | | CLI-Token   | 2 days ago | 1 hour ago  | Read/Write| [Revoke]  | |
|              | +----------------------------------------------------------------+ |
+-----------------------------------------------------------------------------------+
```

* **UX Rationale:**
  * **GitHub-style API Token Management:** Memudahkan integrasi skrip eksternal dengan akses token aman.

---

### Halaman 14: Settings Page

```text
+-----------------------------------------------------------------------------------+
| [Sidebar]    | Platform Preferences & Settings                                    |
|--------------+--------------------------------------------------------------------|
|              | [ General ]  [ Appearance ]  [ Notifications ]  [ Billing ]       |
|              |                                                                    |
|              | Theme Mode                                                         |
|              | (•) Dark Mode (Vercel Obsidian)                                    |
|              | ( ) Light Mode (Clean Slate)                                       |
|              | ( ) System Default                                                 |
|              |                                                                    |
|              | Compute Budget Limits                                              |
|              | Default AutoML Timeout: [ 10 Minutes v ]                           |
|              | Concurrent Worker limit: [ 4 Workers   v ]                         |
|              |                                                                    |
|              | [ Save Changes ]                                                   |
+-----------------------------------------------------------------------------------+
```

* **UX Rationale:**
  * **Tabbed Settings Navigation:** Pengelompokan opsi konfigurasi sistem secara bersih dan teratur.

---

### Halaman 15: Dark Mode vs Light Mode System Specifications

```text
DARK MODE (Vercel Obsidian Slate)           LIGHT MODE (Pure Daylight White)
+---------------------------------------+   +---------------------------------------+
| #09090B Background                    |   | #FAFAFA Background                    |
| +-----------------------------------+ |   | +-----------------------------------+ |
| | #18181B Surface Card              | |   | | #FFFFFF Surface Card              | |
| | Border: rgba(255,255,255,0.08)    | |   | | Border: rgba(0,0,0,0.08)          | |
| | Text: #F4F4F5 (Zinc 100)          | |   | | Text: #09090B (Zinc 950)          | |
| | Accent Glow: Indigo 500           | |   | | Accent Glow: Indigo 600           | |
| +-----------------------------------+ |   | +-----------------------------------+ |
+---------------------------------------+   +---------------------------------------+
```

* **UX Rationale:**
  * **Perbandingan Kontras Rasio:** Memenuhi WCAG 2.1 AA standar (kontras rasio minimal 4.5:1 untuk teks biasa dan 3:1 untuk komponen UI).

---

## 3. Ringkasan Alasan Keputusan UI/UX (UX Rationale Summary)

1. **Efisiensi Pengoperasian (Linear Keyboard-first):** Penggunaan `Cmd+K` Command Palette meminimalkan navigasi mouse hingga 40%.
2. **Keterbacaan Data Padat (GitHub Data Density):** Penggunaan font monospace `JetBrains Mono` pada angka dan tabel meningkatkan akurasi analisis data pengguna.
3. **Kenyamanan Visual (Vercel Dark Mode):** Palet warna obsidian zinc mengurangi kelelahan mata (*eye strain*) pengembang dan data scientist saat bekerja dalam durasi panjang.
4. **Kejelasan Konteks AI (ChatGPT Drawer):** Integrasi AI Copilot sebagai *drawer overlay* mencegah hilangnya konteks analisis data pengguna saat berinteraksi dengan AI.
5. **Modularity & Reusability (Shadcn UI):** Komponen atomik Shadcn menjamin konsistensi antarmuka pengguna di seluruh 15 halaman platform.
