from src.io import load_bom_excel
from src.preprocessing import preprocess_bom
from src.explosion import get_fin_materials, explode_fin

import pandas as pd


def main():
    df = load_bom_excel("data/task_2_data_ex.xlsx")
    df = preprocess_bom(df)

    fin_df = get_fin_materials(df)

    all_rows = []

    for _, fin_row in fin_df.iterrows():
        exploded = explode_fin(df, fin_row)
        all_rows.extend(exploded)

    result_df = pd.DataFrame(all_rows)
    print(result_df.head())


if __name__ == "__main__":
    main()
