import optuna
import pandas as pd
from typing import Dict, Any, Tuple
from sklearn.model_selection import cross_val_score, StratifiedKFold, KFold
from app.ml_engine.models import ModelFactory

optuna.logging.set_verbosity(optuna.logging.WARNING)


class OptunaHyperparameterTuner:
    def __init__(self, task_type: str = "CLASSIFICATION", n_trials: int = 5, random_state: int = 42):
        self.task_type = task_type
        self.n_trials = n_trials
        self.random_state = random_state

    def tune_algorithm(self, algorithm_name: str, X_train: pd.DataFrame, y_train: pd.Series) -> Tuple[Dict[str, Any], float]:
        is_class = (self.task_type.upper() == "CLASSIFICATION")
        scoring_metric = "f1_weighted" if is_class else "r2"
        cv = StratifiedKFold(n_splits=3, shuffle=True, random_state=self.random_state) if is_class else KFold(n_splits=3, shuffle=True, random_state=self.random_state)

        def objective(trial):
            params = {}
            if algorithm_name in ["RandomForest", "ExtraTrees"]:
                params["n_estimators"] = trial.suggest_int("n_estimators", 50, 150)
                params["max_depth"] = trial.suggest_int("max_depth", 3, 12)
            elif algorithm_name in ["GradientBoosting", "AdaBoost"]:
                params["n_estimators"] = trial.suggest_int("n_estimators", 30, 100)
                params["learning_rate"] = trial.suggest_float("learning_rate", 0.01, 0.2)
            elif algorithm_name == "DecisionTree":
                params["max_depth"] = trial.suggest_int("max_depth", 3, 15)
            elif algorithm_name == "LogisticRegression_Ridge":
                params["C"] = trial.suggest_float("C", 0.1, 10.0, log=True) if is_class else trial.suggest_float("alpha", 0.1, 10.0)
            elif algorithm_name == "SVM":
                params["C"] = trial.suggest_float("C", 0.1, 5.0)
            elif algorithm_name == "KNN":
                params["n_neighbors"] = trial.suggest_int("n_neighbors", 3, 9)
            elif algorithm_name == "XGBoost":
                params["n_estimators"] = trial.suggest_int("n_estimators", 50, 150)
                params["max_depth"] = trial.suggest_int("max_depth", 3, 8)
                params["learning_rate"] = trial.suggest_float("learning_rate", 0.01, 0.2)
            elif algorithm_name == "LightGBM":
                params["n_estimators"] = trial.suggest_int("n_estimators", 50, 150)
                params["num_leaves"] = trial.suggest_int("num_leaves", 15, 63)
                params["learning_rate"] = trial.suggest_float("learning_rate", 0.01, 0.2)
            elif algorithm_name == "CatBoost":
                params["iterations"] = trial.suggest_int("iterations", 50, 100)
                params["depth"] = trial.suggest_int("depth", 4, 8)

            model = ModelFactory.create_model(algorithm_name, self.task_type, self.random_state, **params)
            scores = cross_val_score(model, X_train, y_train, cv=cv, scoring=scoring_metric)
            return float(scores.mean())

        study = optuna.create_study(direction="maximize")
        study.optimize(objective, n_trials=self.n_trials)

        return study.best_params, float(study.best_value)
