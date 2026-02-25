CREATE OR REPLACE VIEW bom_final AS
SELECT
    plant,
    fin_material_id,
    fin_material_release_type,
    fin_material_production_type,
    fin_production_quantity,

    prod_material_id,
    prod_material_release_type,
    prod_material_production_type,
    prod_material_production_quantity,

    component_id,
    component_material_release_type,
    component_material_production_type,
    component_consumption_quantity,

    year
FROM bom_explosion;

SELECT *
FROM bom_final
WHERE plant = 'RLT_10'
  AND year = 2024;