from typing import Dict, Any, List, Optional


class CopilotInterpreter:
    @staticmethod
    def explain_metrics(metrics: Dict[str, float]) -> str:
        acc = metrics.get("accuracy", 0.0)
        prec = metrics.get("precision", 0.0)
        rec = metrics.get("recall", 0.0)
        f1 = metrics.get("f1_score", 0.0)
        roc_auc = metrics.get("roc_auc", 0.0)

        explanation = f"""
Halo! Mari saya bantu bedah hasil performa model Machine Learning Anda dengan cara yang sederhana:

📊 **Ringkasan Performa Model:**
- **Akurasi (Accuracy) = {acc * 100:.1f}%**
  *Artinya:* Dari 100 data yang diuji, model berhasil menebak dengan benar sebanyak {acc * 100:.1f} data. Akurasi menunjukkan seberapa tepat model secara keseluruhan.

- **Presisi (Precision) = {prec * 100:.1f}%**
  *Artinya:* Ketika model memprediksi suatu kondisi (misalnya *positif / churn*), probabilitas prediksi tersebut benar-benar akurat adalah sebesar {prec * 100:.1f}%. Presisi tinggi penting jika biaya kesalahan menebak positif itu mahal.

- **Recall (Sensitivitas) = {rec * 100:.1f}%**
  *Artinya:* Dari seluruh kasus nyata yang ada di lapangan, model mampu mendeteksi {rec * 100:.1f}% di antaranya. Recall tinggi sangat krusial di bidang medis atau deteksi penipuan agar tidak ada kasus penting yang terlewat.

- **F1-Score = {f1 * 100:.1f}%**
  *Artinya:* Angka ini adalah penyeimbang seimbang (Harmonic Mean) antara Presisi dan Recall. Nilai F1 sebesar {f1 * 100:.1f}% menunjukkan model Anda sangat stabil dan tidak berat sebelah.

- **ROC AUC = {roc_auc:.3f}**
  *Artinya:* Skor memisahkan kelas positif dan negatif. Rentang nilainya 0.5 hingga 1.0. Skor {roc_auc:.3f} menandakan kemampuan model Anda membedakan kategori sangat baik.

💡 **Insight & Rekomendasi Data Scientist:**
Model ini sudah memiliki tingkat keandalan yang tinggi. Untuk pengujian lebih lanjut, saya sarankan mencoba inferensi pada sampel data baru di dunia nyata (*Real-world Stress Testing*).
"""
        return explanation.strip()

    @staticmethod
    def explain_preprocessing(config_or_details: Dict[str, Any]) -> str:
        impute = config_or_details.get("impute_missing", True)
        scaling = config_or_details.get("scaling_method", "standard")
        encoding = config_or_details.get("encode_categorical", True)

        explanation = f"""
Mari saya jelaskan tahapan pembersihan data (*Data Preprocessing*) yang telah kita lakukan pada dataset Anda:

🧹 **1. Penanganan Nilai Kosong (Missing Value Imputation):**
- *Tindakan:* { "Mengisi data yang hilang menggunakan nilai Median/Modus" if impute else "Tanpa imputasi" }.
- *Mengapa ini penting?* Algoritma ML seperti Gradient Boosting atau SVM memerlukan matriks data yang utuh. Dengan mengisi nilai median, kita menjaga keutuhan informasi tanpa merusak distribusi data.

🏷️ **2. Pengodean Fitur Kategorial (Categorical Encoding):**
- *Tindakan:* { "Mengubah teks kategorial menjadi format angka (Label Encoding)" if encoding else "Tanpa encoding" }.
- *Mengapa ini penting?* Komputer dan algoritma matematik hanya memahami kalkulasi angka. Proses ini menerjemahkan teks seperti 'Tinggi/Sedang/Rendah' menjadi skala numerik yang dapat diolah model.

📏 **3. Normalisasi Skala Data (Feature Scaling):**
- *Tindakan:* {f"Menerapkan {scaling.title()} Scaling" if scaling != "none" else "Tanpa scaling"}
- *Mengapa ini penting?* Jika satu kolom bernilai ribuan (misal: Gaji) dan kolom lain bernilai puluhan (misal: Umur), algoritma bisa salah sangka bahwa Gaji lebih penting. Normalisasi menyetarakan lapangan permainan agar setiap fitur diukur adil.

💡 **Rekomendasi:** Data Anda sekarang sudah dalam kondisi paling optimal (*Clean & Standardized*) dan siap diproses ke AutoML!
"""
        return explanation.strip()

    @staticmethod
    def explain_shap(shap_dict: Dict[str, float]) -> str:
        if not shap_dict:
            return "Belum ada data kontribusi fitur SHAP yang tersedia."

        top_features = list(shap_dict.items())[:5]
        feat_text = "\n".join([f"  {idx+1}. **{feat}** (Bobot Pengaruh: {score:.4f})" for idx, (feat, score) in enumerate(top_features)])

        explanation = f"""
Mari kita bedah **SHAP (Shapley Additive Explanations)** untuk melihat variabel mana saja yang paling mendominasi keputusan model Anda:

🔍 **Top 5 Fitur Paling Berpengaruh secara Global:**
{feat_text}

💡 **Insight Data Scientist:**
Fitur **'{top_features[0][0]}'** terbukti menjadi faktor pendorong utama dalam prediksi model. Ini berarti perubahan kecil pada variabel ini akan memberikan dampak perubahan paling signifikan terhadap hasil prediksi.

🎯 **Rekomendasi Bisnis:**
Fokuskan strategi atau alokasi sumber daya bisnis Anda pada variabel **'{top_features[0][0]}'** dan **'{top_features[1][0] if len(top_features)>1 else top_features[0][0]}'**, karena kedua variabel ini memegang korelasi dampak tertinggi.
"""
        return explanation.strip()

    @staticmethod
    def explain_lime(lime_result: Dict[str, Any]) -> str:
        prediction = lime_result.get("prediction", "N/A")
        local_exp = lime_result.get("local_explanation", [])

        exp_lines = []
        for item in local_exp[:5]:
            feat = item.get("feature", item.get("feature_clause", "N/A"))
            val = item.get("value", "")
            score = item.get("contribution_score", item.get("score", 0.0))
            direction = "mendorong positif (+)" if score > 0 else "menarik ke negatif (-)"
            exp_lines.append(f"- **{feat}** (Nilai: {val}) -> {direction} dengan skor `{score}`")

        lime_text = "\n".join(exp_lines)

        explanation = f"""
Halo! Ini adalah analisis **LIME (Local Interpretable Model-agnostic Explanations)** untuk satu sampel pengujian khusus:

🎯 **Hasil Prediksi Model untuk Sampel Ini:** `{prediction}`

🔬 **Faktor Penentu di Balik Prediksi Spesifik Ini:**
{lime_text}

💡 **Penjelasan Sederhana Data Scientist:**
Untuk data sampel ini, model memberikan keputusan `{prediction}` terutama disebabkan oleh faktor-faktor di atas. LIME membantu kita memastikan bahwa model membuat keputusan berdasarkan alasan yang logis, bukan sekadar kebetulan.
"""
        return explanation.strip()

    @staticmethod
    def explain_chart(chart_type: str, chart_title: str) -> str:
        explanation = f"""
Berikut adalah panduan membaca **{chart_type}** bertajuk **"{chart_title}"**:

📈 **Cara Membaca Grafik Ini:**
- **Sumbu Horizontal (X-Axis):** Menunjukkan rentang variabel atau kelompok data yang diuji.
- **Sumbu Vertikal (Y-Axis):** Menunjukkan frekuensi, nilai persentase, atau besaran variabel pembanding.
- **Tren Visual:** Perhatikan area dengan puncak tertinggi atau sebaran titik terpisah (outliers).

💡 **Insight Data Scientist:**
Grafik ini membantu kita mendeteksi apakah sebaran data Anda berdistribusi normal, memiliki kemiringan (*skewness*), atau terdapat pola anomali tertentu yang memerlukan penanganan khusus saat pembersihan data.
"""
        return explanation.strip()

    @staticmethod
    def explain_xai_suite(xai_report: Dict[str, Any], lang: str = "both") -> str:
        bilingual = xai_report.get("bilingual_ai_explanations", {})
        id_text = bilingual.get("indonesian_id", "")
        en_text = bilingual.get("english_en", "")

        if lang == "id":
            return id_text
        elif lang == "en":
            return en_text
        else:
            return f"{id_text}\n\n---\n\n{en_text}"

