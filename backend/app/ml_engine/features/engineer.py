import pandas as pd
import numpy as np
from sklearn.feature_selection import VarianceThreshold


class FeatureEngineer:
    @staticmethod
    def add_interaction_features(df: pd.DataFrame) -> pd.DataFrame:
        df_feat = df.copy()
        num_cols = df_feat.select_dtypes(include=[np.number]).columns
        
        # Add basic pairwise ratios or products for numeric columns if col count is small
        if 2 <= len(num_cols) <= 10:
            for i in range(len(num_cols)):
                for j in range(i + 1, len(num_cols)):
                    col_a = num_cols[i]
                    col_b = num_cols[j]
                    df_feat[f"{col_a}_x_{col_b}"] = df_feat[col_a] * df_feat[col_b]

        return df_feat


class FeatureSelector:
    def __init__(self, variance_threshold: float = 0.01):
        self.selector = VarianceThreshold(threshold=variance_threshold)

    def fit_transform(self, X: pd.DataFrame) -> pd.DataFrame:
        num_cols = X.select_dtypes(include=[np.number]).columns
        if len(num_cols) == 0:
            return X.copy()

        self.selector.fit(X[num_cols])
        selected_cols = num_cols[self.selector.get_support()]
        
        # Keep non-numeric columns and selected numeric columns
        other_cols = [col for col in X.columns if col not in num_cols]
        return X[list(selected_cols) + other_cols]
