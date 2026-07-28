import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, LabelEncoder


class DataCleaner:
    def __init__(self, num_strategy: str = "median", cat_strategy: str = "most_frequent"):
        self.num_imputer = SimpleImputer(strategy=num_strategy)
        self.cat_imputer = SimpleImputer(strategy=cat_strategy)

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_clean = df.copy()
        num_cols = df_clean.select_dtypes(include=[np.number]).columns
        cat_cols = df_clean.select_dtypes(exclude=[np.number]).columns

        if len(num_cols) > 0:
            df_clean[num_cols] = self.num_imputer.fit_transform(df_clean[num_cols])
        if len(cat_cols) > 0:
            df_clean[cat_cols] = self.cat_imputer.fit_transform(df_clean[cat_cols].astype(str))

        return df_clean


class DataEncoder:
    def __init__(self):
        self.encoders: Dict[str, LabelEncoder] = {}

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        df_encoded = df.copy()
        cat_cols = df_encoded.select_dtypes(exclude=[np.number]).columns

        for col in cat_cols:
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            self.encoders[col] = le

        return df_encoded


class DataScaler:
    def __init__(self, method: str = "standard"):
        self.method = method
        if method == "standard":
            self.scaler = StandardScaler()
        elif method == "minmax":
            self.scaler = MinMaxScaler()
        elif method == "robust":
            self.scaler = RobustScaler()
        else:
            self.scaler = None

    def fit_transform(self, df: pd.DataFrame) -> pd.DataFrame:
        if self.scaler is None:
            return df.copy()

        df_scaled = df.copy()
        num_cols = df_scaled.select_dtypes(include=[np.number]).columns
        if len(num_cols) > 0:
            df_scaled[num_cols] = self.scaler.fit_transform(df_scaled[num_cols])
        return df_scaled
