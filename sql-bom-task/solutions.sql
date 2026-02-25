CREATE TABLE bom_raw (
    year INT,
    month INT,

    produced_material INT,
    produced_material_production_type TEXT,
	produced_material_release_type TEXT,
    produced_material_quantity NUMERIC,

    component_material INT,
	component_material_production_type TEXT,
    component_material_release_type TEXT,
    component_material_quantity NUMERIC,
	plant_id TEXT
);

