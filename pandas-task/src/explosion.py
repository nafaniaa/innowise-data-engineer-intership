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

    initial_components = get_components(df, fin_row["produced_material"])

    stack = []

    for _, row in initial_components.iterrows():
        if row["component_material_release_type"] == "PROD":
            stack.append(
                (
                    row["component_material"],
                    fin_row["produced_material_quantity"]
                )
            )

    visited = set()

    while stack:
        current_material, current_qty = stack.pop()

        if current_material in visited:
            continue

        visited.add(current_material)

        components = get_components(df, current_material)

        for _, row in components.iterrows():
            ratio = (
                row["component_material_quantity"]
                / row["produced_material_quantity"]
            )

            component_qty = current_qty * ratio

            result.append({
                "plant": fin_row["plant_id"],
                "year": fin_row["year"],

                "fin_material_id": fin_row["produced_material"],
                "fin_material_release_type": fin_row["produced_material_release_type"],
                "fin_material_production_type": fin_row["produced_material_production_type"],
                "fin_production_quantity": fin_row["produced_material_quantity"],

                "prod_material_id": current_material,
                "prod_material_release_type": row["produced_material_release_type"],
                "prod_material_production_type": row["produced_material_production_type"],
                "prod_material_production_quantity": current_qty,

                "component_id": row["component_material"],
                "component_material_release_type": row["component_material_release_type"],
                "component_material_production_type": row["component_material_production_type"],
                "component_consumption_quantity": component_qty
            })

            if row["component_material_release_type"] == "PROD":
                stack.append(
                    (row["component_material"], component_qty)
                )

    return result
