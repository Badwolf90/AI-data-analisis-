import numpy as np
import pandas as pd
from typing import Dict, Any, List, Optional
import os
import requests
from app.core.config import settings
from app.core.logging import logger


class DatasetReviewerEngine:
    """
    Automated Senior Data Scientist Audit Engine.
    Performs comprehensive statistical diagnostic checks on raw datasets:
    - Missing Values
    - Duplicates
    - Data Leakage
    - Outliers (IQR)
    - Class Imbalance
    - Correlation & Multicollinearity
    - Target Validation
    - Data Quality Score (0-100)
    - AI Senior Data Scientist Recommendations
    """

    @staticmethod
    def audit_dataset(df: pd.DataFrame, target_column: Optional[str] = None) -> Dict[str, Any]:
        total_rows, total_cols = df.shape

        # 1. Missing Value Audit
        null_counts = df.isnull().sum()
        total_missing = int(null_counts.sum())
        missing_percentage = float(round((total_missing / (total_rows * total_cols)) * 100, 2)) if total_rows * total_cols > 0 else 0.0

        missing_details = {}
        high_missing_cols = []
        for col in df.columns:
            cnt = int(null_counts[col])
            pct = float(round((cnt / total_rows) * 100, 2))
            if cnt > 0:
                missing_details[col] = {"missing_count": cnt, "percentage": pct}
            if pct > 50.0:
                high_missing_cols.append(col)

        # 2. Duplicate Audit
        duplicate_count = int(df.duplicated().sum())
        duplicate_percentage = float(round((duplicate_count / total_rows) * 100, 2)) if total_rows > 0 else 0.0

        # 3. Target Validation & Problem Type Inference
        target_info = {"status": "NOT_SPECIFIED"}
        problem_type = None

        if target_column:
            if target_column not in df.columns:
                target_info = {
                    "status": "INVALID",
                    "error": f"Target column '{target_column}' not found in dataset."
                }
            else:
                target_missing = int(df[target_column].isnull().sum())
                unique_target_vals = df[target_column].nunique(dropna=True)
                target_dtype = str(df[target_column].dtype)

                if unique_target_vals <= 20 or df[target_column].dtype == "object":
                    problem_type = "CLASSIFICATION"
                else:
                    problem_type = "REGRESSION"

                target_info = {
                    "status": "VALID",
                    "target_column": target_column,
                    "problem_type": problem_type,
                    "unique_values": int(unique_target_vals),
                    "missing_count": target_missing,
                    "target_dtype": target_dtype
                }

        # 4. Outlier Audit (IQR Method for Numeric Columns)
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if target_column and target_column in numeric_cols:
            feature_numeric_cols = [c for c in numeric_cols if c != target_column]
        else:
            feature_numeric_cols = numeric_cols

        outlier_details = {}
        total_outlier_instances = 0

        for col in feature_numeric_cols:
            col_data = df[col].dropna()
            if len(col_data) > 0:
                q1 = float(col_data.quantile(0.25))
                q3 = float(col_data.quantile(0.75))
                iqr = q3 - q1
                lower_bound = q1 - (1.5 * iqr)
                upper_bound = q3 + (1.5 * iqr)
                outliers = col_data[(col_data < lower_bound) | (col_data > upper_bound)]
                out_cnt = int(len(outliers))
                if out_cnt > 0:
                    outlier_details[col] = {
                        "outlier_count": out_cnt,
                        "percentage": float(round((out_cnt / len(col_data)) * 100, 2)),
                        "lower_bound": round(lower_bound, 4),
                        "upper_bound": round(upper_bound, 4)
                    }
                    total_outlier_instances += out_cnt

        outlier_summary = {
            "total_outliers": total_outlier_instances,
            "columns_with_outliers_count": len(outlier_details),
            "details": outlier_details
        }

        # 5. Class Imbalance Audit
        imbalance_info = {"is_imbalanced": False}
        if target_column and target_column in df.columns and problem_type == "CLASSIFICATION":
            val_counts = df[target_column].value_counts(dropna=True).to_dict()
            total_valid_target = sum(val_counts.values())

            if total_valid_target > 0:
                class_distribution = {str(k): int(v) for k, v in val_counts.items()}
                percentages = {str(k): float(round((v / total_valid_target) * 100, 2)) for k, v in val_counts.items()}

                min_class_cnt = min(val_counts.values())
                max_class_cnt = max(val_counts.values())
                imbalance_ratio = float(round(min_class_cnt / max_class_cnt, 4)) if max_class_cnt > 0 else 1.0

                is_severe_imbalance = imbalance_ratio < 0.20

                imbalance_info = {
                    "is_imbalanced": is_severe_imbalance,
                    "imbalance_ratio": imbalance_ratio,
                    "class_distribution": class_distribution,
                    "class_percentages": percentages,
                    "recommendation": "Use SMOTE oversampling or Class Weight adjustment." if is_severe_imbalance else "Class balance is acceptable."
                }

        # 6. Correlation & Multicollinearity Audit
        high_multicollinearity_pairs = []
        target_correlation = {}

        if len(numeric_cols) > 1:
            corr_matrix = df[numeric_cols].corr()

            # Multicollinearity between features
            for i in range(len(numeric_cols)):
                for j in range(i + 1, len(numeric_cols)):
                    col1, col2 = numeric_cols[i], numeric_cols[j]
                    if col1 != target_column and col2 != target_column:
                        val = float(corr_matrix.loc[col1, col2])
                        if abs(val) > 0.85:
                            high_multicollinearity_pairs.append({
                                "feature_1": col1,
                                "feature_2": col2,
                                "correlation": round(val, 4)
                            })

            # Target Correlation
            if target_column and target_column in numeric_cols:
                target_corr_series = corr_matrix[target_column].drop(labels=[target_column]).abs().sort_values(ascending=False)
                target_correlation = {str(k): float(round(v, 4)) for k, v in target_corr_series.to_dict().items()}

        # 7. Data Leakage Audit
        potential_leakage_features = []
        constant_columns = []
        id_like_columns = []

        for col in df.columns:
            if col == target_column:
                continue

            nunique = df[col].nunique(dropna=True)
            # Constant columns
            if nunique <= 1:
                constant_columns.append(col)
                potential_leakage_features.append({
                    "column": col,
                    "reason": "Constant column (0 variance, useless predictor)."
                })

            # High cardinality ID columns
            elif df[col].dtype == "object" and nunique == total_rows:
                id_like_columns.append(col)
                potential_leakage_features.append({
                    "column": col,
                    "reason": "Unique identifier column (100% unique strings - risk of overfitting)."
                })

            # Perfect correlation leakage
            elif target_column and col in target_correlation:
                if target_correlation[col] >= 0.98:
                    potential_leakage_features.append({
                        "column": col,
                        "reason": f"Extremely high correlation ({target_correlation[col]}) with target variable (potential target leakage)."
                    })

        leakage_info = {
            "has_leakage_risk": len(potential_leakage_features) > 0,
            "potential_leakage_count": len(potential_leakage_features),
            "constant_columns": constant_columns,
            "id_like_columns": id_like_columns,
            "leakage_details": potential_leakage_features
        }

        # 8. Data Quality Score Calculation (0 - 100)
        quality_score = 100.0

        # Deduct for Missing Values (Max -25)
        missing_penalty = min(25.0, missing_percentage * 1.5)
        quality_score -= missing_penalty

        # Deduct for Duplicates (Max -15)
        duplicate_penalty = min(15.0, duplicate_percentage * 2.0)
        quality_score -= duplicate_penalty

        # Deduct for Data Leakage (Max -20)
        if leakage_info["has_leakage_risk"]:
            quality_score -= min(20.0, len(potential_leakage_features) * 7.0)

        # Deduct for Outliers (Max -15)
        if total_rows > 0:
            outlier_ratio = (total_outlier_instances / (total_rows * max(1, len(feature_numeric_cols)))) * 100
            quality_score -= min(15.0, outlier_ratio * 1.2)

        # Deduct for Class Imbalance (Max -15)
        if imbalance_info.get("is_imbalanced"):
            quality_score -= 12.0

        # Deduct for Target Issues (Max -30)
        if target_info.get("status") == "INVALID":
            quality_score -= 30.0
        elif target_info.get("missing_count", 0) > 0:
            quality_score -= 15.0

        quality_score = max(0.0, min(100.0, round(quality_score, 1)))

        # Determine Quality Grade
        if quality_score >= 90:
            grade = "A+ (Excellent Data Quality)"
        elif quality_score >= 80:
            grade = "A (Good Quality - Minor Cleanup Required)"
        elif quality_score >= 70:
            grade = "B (Fair - Moderate Cleaning Required)"
        elif quality_score >= 50:
            grade = "C (Needs Attention - High Risk)"
        else:
            grade = "D (Poor Quality - Action Required Before Modeling)"

        # 9. Senior Data Scientist AI Recommendation Generation
        ai_recommendation = DatasetReviewerEngine._generate_senior_ds_recommendation(
            df_cols=list(df.columns),
            total_rows=total_rows,
            quality_score=quality_score,
            grade=grade,
            missing_percentage=missing_percentage,
            high_missing_cols=high_missing_cols,
            duplicate_count=duplicate_count,
            leakage_info=leakage_info,
            imbalance_info=imbalance_info,
            multicollinearity=high_multicollinearity_pairs,
            target_info=target_info
        )

        return {
            "summary": {
                "total_rows": total_rows,
                "total_columns": total_cols,
                "data_quality_score": quality_score,
                "quality_grade": grade
            },
            "missing_values": {
                "total_missing_cells": total_missing,
                "missing_percentage": missing_percentage,
                "high_missing_columns": high_missing_cols,
                "details": missing_details
            },
            "duplicates": {
                "duplicate_count": duplicate_count,
                "duplicate_percentage": duplicate_percentage
            },
            "target_validation": target_info,
            "data_leakage": leakage_info,
            "outliers": outlier_summary,
            "class_imbalance": imbalance_info,
            "correlation_analysis": {
                "high_multicollinearity_pairs": high_multicollinearity_pairs,
                "target_correlation": target_correlation
            },
            "ai_senior_ds_recommendation": ai_recommendation
        }

    @staticmethod
    def _generate_senior_ds_recommendation(
        df_cols: List[str],
        total_rows: int,
        quality_score: float,
        grade: str,
        missing_percentage: float,
        high_missing_cols: List[str],
        duplicate_count: int,
        leakage_info: Dict[str, Any],
        imbalance_info: Dict[str, Any],
        multicollinearity: List[Dict[str, Any]],
        target_info: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Acts as a Lead Senior Data Scientist auditing dataset for production ML pipelines.
        Can seamlessly connect to 9Router LLM gateway if active, or output deterministic expert recommendations.
        """
        # Attempt 9Router gateway call if enabled
        if settings.NINEROUTER_ENABLED:
            try:
                headers = {"Content-Type": "application/json"}
                prompt_text = f"""You are a Lead Senior Data Scientist auditing a dataset for production Machine Learning pipelines.
Dataset Specs:
- Total Samples: {total_rows}
- Columns: {df_cols}
- Computed Data Quality Score: {quality_score}/100 ({grade})
- Missing Values Ratio: {missing_percentage}%
- High Missing Columns (>50%): {high_missing_cols}
- Duplicate Rows: {duplicate_count}
- Target Info: {target_info}
- Data Leakage Risks: {leakage_info}
- Class Imbalance Info: {imbalance_info}
- Multicollinearity Pairs: {multicollinearity}

Provide expert Senior Data Scientist recommendations in structured JSON format with keys:
1. 'executive_summary': Short strategic summary of dataset readiness.
2. 'critical_risks': Bulleted list of top risks (Leakage, Imbalance, Missing Data).
3. 'preprocessing_blueprint': Concrete recommended preprocessing steps.
4. 'recommended_algorithms': Ideal ML algorithms for this dataset profile.
"""
                payload = {
                    "model": settings.NINEROUTER_MODEL,
                    "messages": [
                        {"role": "system", "content": "You are a world-class Lead Senior Data Scientist & ML Architect."},
                        {"role": "user", "content": prompt_text}
                    ],
                    "temperature": 0.3
                }
                resp = requests.post(f"{settings.NINEROUTER_BASE_URL}/chat/completions", json=payload, headers=headers, timeout=5)
                if resp.status_code == 200:
                    ai_text = resp.json()["choices"][0]["message"]["content"]
                    return {
                        "source": "9Router AI Gateway (Senior Data Scientist Model)",
                        "executive_summary": f"Audit Completed. Quality Score: {quality_score}/100 ({grade}).",
                        "expert_review": ai_text
                    }
            except Exception as e:
                logger.warning(f"9Router LLM call skipped or timed out: {e}. Falling back to Senior DS Rule Engine.")

        # Deterministic Expert Rule Engine (Senior Data Scientist Persona)
        critical_risks = []
        blueprint_steps = []
        algo_suggestions = []

        if leakage_info.get("has_leakage_risk"):
            cols = [item["column"] for item in leakage_info["leakage_details"]]
            critical_risks.append(f"⚠️ **DATA LEAKAGE DETECTED**: Columns {cols} contain target leakage, constant values, or unique identifiers that will cause model overfitting.")
            blueprint_steps.append(f"Drop leakage columns: {cols} before feature matrix build.")

        if high_missing_cols:
            critical_risks.append(f"⚠️ **CRITICAL MISSING DATA**: Columns {high_missing_cols} have >50% missing values.")
            blueprint_steps.append(f"Drop columns {high_missing_cols} or apply IterativeImputer (MICE).")
        elif missing_percentage > 0:
            blueprint_steps.append(f"Apply Median Imputation for numerical features and Most-Frequent for categorical features.")

        if duplicate_count > 0:
            critical_risks.append(f"⚠️ **DUPLICATE SAMPLES**: Found {duplicate_count} exact duplicate rows.")
            blueprint_steps.append(f"Execute `df.drop_duplicates()` to eliminate train/test set data contamination.")

        if imbalance_info.get("is_imbalanced"):
            critical_risks.append(f"⚠️ **SEVERE CLASS IMBALANCE**: Target minority class ratio is {imbalance_info.get('imbalance_ratio')}.")
            blueprint_steps.append("Apply SMOTE oversampling on training split or configure `class_weight='balanced'`.")
            algo_suggestions.append("XGBoost / LightGBM with scale_pos_weight tuning, or Random Forest with balanced subsampling.")
        else:
            algo_suggestions.append("Gradient Boosting (XGBoost/LightGBM), Random Forest, Logistic Regression with L2 regularization.")

        if multicollinearity:
            pairs = [f"{p['feature_1']} & {p['feature_2']}" for p in multicollinearity]
            blueprint_steps.append(f"High collinearity detected between {pairs}. Apply VIF filtering or PCA dimensionality reduction.")

        readiness_msg = "Dataset is production-ready after recommended preprocessing." if quality_score >= 80 else "Dataset requires preprocessing remediation before AutoML model training."

        return {
            "source": "Senior Data Scientist Audit Engine",
            "executive_summary": f"Dataset audited with Quality Score of {quality_score}/100 ({grade}). {readiness_msg}",
            "critical_risks": critical_risks if critical_risks else ["No critical data hygiene risks detected."],
            "preprocessing_blueprint": blueprint_steps if blueprint_steps else ["Dataset is clean. Direct standard scaling and encoding recommended."],
            "recommended_algorithms": algo_suggestions
        }

