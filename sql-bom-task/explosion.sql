CREATE OR REPLACE VIEW bom_explosion AS
WITH RECURSIVE bom_tree AS (

    -- 1. Basic level: FIN -> components
    SELECT
        br.plant_id AS plant,
        br.year,

        br.produced_material AS fin_material_id,
        br.produced_material_release_type AS fin_material_release_type,
        br.produced_material_production_type AS fin_material_production_type,
        br.produced_material_quantity AS fin_production_quantity,

        br.component_material AS component_id,
        br.component_material_release_type,
        br.component_material_production_type,
        br.component_material_quantity AS component_consumption_quantity,

        br.produced_material AS prod_material_id,
        br.produced_material_release_type AS prod_material_release_type,
        br.produced_material_production_type AS prod_material_production_type,
        br.produced_material_quantity AS prod_material_production_quantity

    FROM bom_raw br
    WHERE br.produced_material_release_type = 'FIN'

    UNION ALL

    -- 2. Recursive level: PROD -> its components
    SELECT
        parent.plant,
        parent.year,

        parent.fin_material_id,
        parent.fin_material_release_type,
        parent.fin_material_production_type,
        parent.fin_production_quantity,

        child.component_material AS component_id,
        child.component_material_release_type,
        child.component_material_production_type,

      	-- recalculation of quantity 
        parent.component_consumption_quantity
        * (child.component_material_quantity / child.produced_material_quantity)
        AS component_consumption_quantity,

        child.produced_material AS prod_material_id,
        child.produced_material_release_type,
        child.produced_material_production_type,
        parent.component_consumption_quantity AS prod_material_production_quantity

		

    FROM bom_tree parent
    JOIN bom_raw child
      ON child.produced_material = parent.component_id
     AND child.produced_material_release_type = 'PROD'

)

SELECT *
FROM bom_tree;



