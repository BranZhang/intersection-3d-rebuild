--query target_ways_XXX table
select osm_id, bridge, oneway, layer, highway, z_order, ST_AsGeoJSON(way) from target_ways_%s 
where highway IN ('trunk','trunk_link');