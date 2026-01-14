from src.io import load_bom_excel
from src.pipeline import build_bom_pipeline


def main():
    df = load_bom_excel("data/task_2_data_ex.xlsx")
    final_df = build_bom_pipeline(df)

    print(final_df.tail())


if __name__ == "__main__":
    main()
