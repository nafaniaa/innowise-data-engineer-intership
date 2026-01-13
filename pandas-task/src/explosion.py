#business logic BoM explosion
import pandas as pd

def get_fin_materials(df: pd.DataFrame) -> pd.DataFrame:
    return df[df['produced_material_release_type'] == 'FIN']

def get_components(
        df: pd.DataFrame,
        material_id: int
)-> pd.DataFrame:
    return df[df['produced_material'] == material_id]

def explode_fin(df: pd.DataFrame, fin_row: pd.Series) -> list[dict]:
    result = []
    stack = []

    initial_components = get_components(df, fin_row["produced_material"])

    for _, row in initial_components.iterrows():
        if row["component_material_release_type"] == "PROD":
            stack.append(row["component_material"])

    visited = set()

    while stack:
        current_material = stack.pop()

        if current_material in visited:
            continue

        visited.add(current_material)

        components = get_components(df, current_material)

        for _, row in components.iterrows():
            result.append({
                "fin_material_id": fin_row["produced_material"],
                "prod_material_id": current_material,
                "component_id": row["component_material"],
                "component_release_type": row["component_material_release_type"],
                "year": fin_row["year"],
                "plant": fin_row["plant_id"]
            })

            if row["component_material_release_type"] == "PROD":
                stack.append(row["component_material"])

    return result
