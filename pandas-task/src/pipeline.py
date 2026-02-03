import pandas as pd

from src.preprocessing import preprocess_bom
from src.explosion import get_fin_materials, explode_fin
from src.enrich import (
    enrich_fin_attributes,
    enrich_prod_attributes,
    enrich_component_attributes
)


def aggregate_yearly(df: pd.DataFrame) -> pd.DataFrame:
    group_cols = [
        "plant",
        "fin_material_id",
        "fin_material_release_type",
        "fin_material_production_type",
        "prod_material_id",
        "prod_material_release_type",
        "prod_material_production_type",
        "component_id",
        "component_material_release_type",
        "component_material_production_type",
        "year"
    ]

    agg_df = (
        df
        .groupby(group_cols, as_index=False)
        .agg({
            "fin_production_quantity": "sum",
            "prod_material_production_quantity": "sum",
            "component_consumption_quantity": "sum"
        })
    )

    return agg_df


def build_bom_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    df_clean = preprocess_bom(df)
    fin_df = get_fin_materials(df_clean)

    exploded_rows = []
    for _, fin_row in fin_df.iterrows():
        exploded_rows.extend(explode_fin(df_clean, fin_row))

    explosion_df = pd.DataFrame(exploded_rows)

    if explosion_df.empty:
        return explosion_df
    
    final_df = aggregate_yearly(explosion_df)
    return final_df
