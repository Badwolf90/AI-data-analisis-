from typing import Dict, Any, Optional
from app.copilot_engine.interpreter import CopilotInterpreter


class AICopilotService:
    @staticmethod
    def ask_copilot(prompt: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        context = context or {}

        # 1. Metrics Query
        if any(term in prompt_lower for term in ["metrik", "accuracy", "precision", "recall", "f1", "roc", "auc", "evaluasi"]):
            metrics = context.get("metrics", {"accuracy": 0.92, "precision": 0.89, "recall": 0.94, "f1_score": 0.91, "roc_auc": 0.965})
            answer = CopilotInterpreter.explain_metrics(metrics)

        # 2. SHAP Query
        elif "shap" in prompt_lower or "importance" in prompt_lower or "fitur penting" in prompt_lower:
            shap_dict = context.get("shap_summary", {"age": 0.42, "income": 0.31, "credit_score": 0.18, "tenure": 0.09})
            answer = CopilotInterpreter.explain_shap(shap_dict)

        # 3. LIME Query
        elif "lime" in prompt_lower or "sampel" in prompt_lower or "lokal" in prompt_lower:
            lime_res = context.get("lime_result", {
                "prediction": 1,
                "local_explanation": [
                    {"feature": "Income > 50000", "value": 65000, "contribution_score": 0.35},
                    {"feature": "Age <= 30", "value": 26, "contribution_score": -0.12}
                ]
            })
            answer = CopilotInterpreter.explain_lime(lime_res)

        # 4. Preprocessing Query
        elif "preprocess" in prompt_lower or "pembersihan" in prompt_lower or "missing" in prompt_lower or "scale" in prompt_lower:
            prep_info = context.get("preprocessing_info", {"impute_missing": True, "scaling_method": "standard", "encode_categorical": True})
            answer = CopilotInterpreter.explain_preprocessing(prep_info)

        # 5. Chart / Graph Query
        elif "grafik" in prompt_lower or "chart" in prompt_lower or "visualisasi" in prompt_lower:
            c_type = context.get("chart_type", "Confusion Matrix")
            c_title = context.get("chart_title", "Hasil Evaluasi Klasifikasi Model")
            answer = CopilotInterpreter.explain_chart(c_type, c_title)

        # 6. General Conversational Fallback
        else:
            answer = f"""
Halo! Saya AI Data Science Copilot Anda. 🤖

Saya siap membantu Anda memahami seluruh siklus analisis data:
1. 📊 **Penjelasan Metrik Evaluasi** (Accuracy, Precision, Recall, F1-Score, ROC AUC).
2. 🔍 **Penjelasan Transparansi AI** (SHAP Global Feature Importance & LIME Local Explanation).
3. 🧹 **Penjelasan Preprocessing Data** (Imputasi, Encoding, Scaling).
4. 📈 **Penjelasan Visualisasi & Grafik**.
5. 💡 **Insight & Rekomendasi Bisnis**.

Ada hal khusus dari dataset atau hasil AutoML Anda yang ingin kita diskusikan bersama?
"""

        return {
            "prompt": prompt,
            "response": answer.strip(),
            "sender": "AI Copilot",
            "suggested_questions": [
                "Jelaskan hasil SHAP feature importance model ini.",
                "Apa arti nilai F1-Score dan Recall untuk bisnis saya?",
                "Mengapa kita perlu melakukan Feature Scaling pada preprocessing?",
                "Berikan rekomendasi langkah selanjutnya dari hasil model ini."
            ]
        }
