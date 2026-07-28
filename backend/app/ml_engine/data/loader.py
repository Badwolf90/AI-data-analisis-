import os
import pandas as pd
from typing import Tuple, Dict, Any


class DataLoader:
    @staticmethod
    def load(file_path: str) -> pd.DataFrame:
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Dataset file not found at {file_path}")
        
        ext = os.path.splitext(file_path)[1].lower()
        if ext == ".csv":
            return pd.read_csv(file_path)
        elif ext in [".xlsx", ".xls"]:
            return pd.read_excel(file_path)
        elif ext == ".parquet":
            return pd.read_parquet(file_path)
        else:
            raise ValueError(f"Unsupported file format: {ext}")


class DataValidator:
    @staticmethod
    def validate(df: pd.DataFrame, target_column: str) -> Dict[str, Any]:
        if df.empty:
            raise ValueError("Dataset is empty.")
        if target_column not in df.columns:
            raise ValueError(f"Target column '{target_column}' is missing from the dataset.")

        total_rows, total_cols = df.shape
        null_counts = df.isnull().sum().to_dict()
        duplicate_rows = int(df.duplicated().sum())

        is_valid = total_rows >= 10 and total_cols >= 2
        
        return {
            "is_valid": is_valid,
            "total_rows": total_rows,
            "total_cols": total_cols,
            "duplicate_rows": duplicate_rows,
            "null_summary": null_counts,
            "target_column": target_column
        }
