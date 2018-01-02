--update target_ways_XXX table of road_code_list
UPDATE target_ways_{timesign}
SET road_code_list = '{code_list}'
WHERE osm_id = '{osm_id}';