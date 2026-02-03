#data preprocessing
import pandas as pd
from pandas.api.types import is_numeric_dtype
from src.explosion import get_components

def preprocess_bom(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    numeric_cols = []

    for col in df.columns:
        if(
            is_numeric_dtype(df[col])
            or any(
                key in col
                for key in ["quantity", "year", "month", "production_type"]
            )
        ):
            numeric_cols.append(col)
    
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df
