# reading excel + basic check
import pandas as pd

def load_bom_excel(path: str) -> pd.DataFrame:
    df = pd.read_excel(path)
    df.columns = df.columns.str.lower()
    return df