import pandas as pd

def enrich_fin_attributes(
        explosion_df: pd.DataFrame,
        fin_df: pd.DataFrame
) -> pd.DataFrame:
    fin_attrs = fin_df[[
        "produced_material",
        "produced_material_release_type",
        "produced_material_production_type",
        "produced_material_quantity",
        "plant_id",
        "year"
    ]].drop_duplicates()

    result = explosion_df.merge(
        fin_attrs,
        left_on=["fin_material_id", "plant", "year"],
        right_on=["produced_material", "plant_id", "year"],
        how="left"
    )

    result = result.rename(columns={
        "produced_material_release_type": "fin_material_release_type",
        "produced_material_production_type": "fin_material_production_type",
        "produced_material_quantity": "fin_production_quantity"
    })

    return result

def enrich_prod_attributes(
    bom_df: pd.DataFrame,
    explosion_df: pd.DataFrame
) -> pd.DataFrame:

    prod_attrs = bom_df[[
        "produced_material",
        "produced_material_release_type",
        "produced_material_production_type",
        "produced_material_quantity"
    ]].drop_duplicates()

    prod_attrs = prod_attrs.rename(columns={
        "produced_material": "prod_material_id",
        "produced_material_release_type": "prod_material_release_type",
        "produced_material_production_type": "prod_material_production_type",
        "produced_material_quantity": "prod_material_production_quantity"
    })

    return explosion_df.merge(
        prod_attrs,
        on="prod_material_id",
        how="left"
    )



def enrich_component_attributes(
    df: pd.DataFrame,
    explosion_df: pd.DataFrame
) -> pd.DataFrame:
    component_attrs = df[[
        "component_material",
        "component_material_release_type",
        "component_material_production_type",
        "component_material_quantity"
    ]].drop_duplicates()

    result = explosion_df.merge(
        component_attrs,
        left_on="component_id",
        right_on="component_material",
        how="left"
    )

    result = result.rename(columns={
        "component_material_quantity": "component_consumption_quantity"
    })

    return result
    
