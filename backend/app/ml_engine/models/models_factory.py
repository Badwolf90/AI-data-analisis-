from typing import Dict, Any, List
import numpy as np
import pandas as pd
from sklearn.ensemble import (
    RandomForestClassifier, RandomForestRegressor,
    ExtraTreesClassifier, ExtraTreesRegressor,
    GradientBoostingClassifier, GradientBoostingRegressor,
    AdaBoostClassifier, AdaBoostRegressor
)
from sklearn.tree import DecisionTreeClassifier, DecisionTreeRegressor
from sklearn.linear_model import LogisticRegression, Ridge
from sklearn.svm import SVC, SVR
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score,
    mean_squared_error, mean_absolute_error, r2_score
)

# Optional Advanced Gradient Boosting Libraries
try:
    import xgboost as xgb
except ImportError:
    xgb = None

try:
    import lightgbm as lgb
except ImportError:
    lgb = None

try:
    import catboost as cb
except ImportError:
    cb = None


class ModelFactory:
    @staticmethod
    def get_supported_algorithms() -> List[str]:
        algos = [
            "RandomForest",
            "ExtraTrees",
            "GradientBoosting",
            "AdaBoost",
            "DecisionTree",
            "LogisticRegression_Ridge",
            "SVM",
            "KNN"
        ]
        if xgb is not None:
            algos.append("XGBoost")
        if lgb is not None:
            algos.append("LightGBM")
        if cb is not None:
            algos.append("CatBoost")
        return algos

    @staticmethod
    def create_model(algorithm_name: str, task_type: str = "CLASSIFICATION", random_state: int = 42, **kwargs):
        is_class = (task_type.upper() == "CLASSIFICATION")

        if algorithm_name == "RandomForest":
            return RandomForestClassifier(random_state=random_state, **kwargs) if is_class else RandomForestRegressor(random_state=random_state, **kwargs)
        
        elif algorithm_name == "ExtraTrees":
            return ExtraTreesClassifier(random_state=random_state, **kwargs) if is_class else ExtraTreesRegressor(random_state=random_state, **kwargs)

        elif algorithm_name == "GradientBoosting":
            return GradientBoostingClassifier(random_state=random_state, **kwargs) if is_class else GradientBoostingRegressor(random_state=random_state, **kwargs)

        elif algorithm_name == "AdaBoost":
            return AdaBoostClassifier(random_state=random_state, **kwargs) if is_class else AdaBoostRegressor(random_state=random_state, **kwargs)

        elif algorithm_name == "DecisionTree":
            return DecisionTreeClassifier(random_state=random_state, **kwargs) if is_class else DecisionTreeRegressor(random_state=random_state, **kwargs)

        elif algorithm_name == "LogisticRegression_Ridge":
            return LogisticRegression(random_state=random_state, max_iter=1000, **kwargs) if is_class else Ridge(random_state=random_state, **kwargs)

        elif algorithm_name == "SVM":
            return SVC(random_state=random_state, probability=True, **kwargs) if is_class else SVR(**kwargs)

        elif algorithm_name == "KNN":
            return KNeighborsClassifier(**kwargs) if is_class else KNeighborsRegressor(**kwargs)

        elif algorithm_name == "XGBoost" and xgb is not None:
            return xgb.XGBClassifier(random_state=random_state, eval_metric="logloss", **kwargs) if is_class else xgb.XGBRegressor(random_state=random_state, **kwargs)

        elif algorithm_name == "LightGBM" and lgb is not None:
            return lgb.LGBMClassifier(random_state=random_state, verbose=-1, **kwargs) if is_class else lgb.LGBMRegressor(random_state=random_state, verbose=-1, **kwargs)

        elif algorithm_name == "CatBoost" and cb is not None:
            return cb.CatBoostClassifier(random_state=random_state, verbose=0, **kwargs) if is_class else cb.CatBoostRegressor(random_state=random_state, verbose=0, **kwargs)

        else:
            return RandomForestClassifier(random_state=random_state) if is_class else RandomForestRegressor(random_state=random_state)


class ModelEvaluator:
    @staticmethod
    def evaluate(model, X_test: pd.DataFrame, y_test: pd.Series, task_type: str = "CLASSIFICATION") -> Dict[str, float]:
        predictions = model.predict(X_test)
        metrics = {}

        if task_type.upper() == "CLASSIFICATION":
            metrics["accuracy"] = float(accuracy_score(y_test, predictions))
            metrics["precision"] = float(precision_score(y_test, predictions, average="weighted", zero_division=0))
            metrics["recall"] = float(recall_score(y_test, predictions, average="weighted", zero_division=0))
            metrics["f1_score"] = float(f1_score(y_test, predictions, average="weighted", zero_division=0))

            if hasattr(model, "predict_proba"):
                try:
                    proba = model.predict_proba(X_test)
                    if proba.shape[1] == 2:
                        metrics["roc_auc"] = float(roc_auc_score(y_test, proba[:, 1]))
                    else:
                        metrics["roc_auc"] = float(roc_auc_score(y_test, proba, multi_class="ovr"))
                except Exception:
                    metrics["roc_auc"] = 0.0
        else:
            mse = float(mean_squared_error(y_test, predictions))
            metrics["mse"] = mse
            metrics["rmse"] = float(np.sqrt(mse))
            metrics["mae"] = float(mean_absolute_error(y_test, predictions))
            metrics["r2_score"] = float(r2_score(y_test, predictions))

        return metrics
