--update target_ways_XXX table of road_code_list
UPDATE target_ways_%s 
SET road_code_list=%s
WHERE id=%s;