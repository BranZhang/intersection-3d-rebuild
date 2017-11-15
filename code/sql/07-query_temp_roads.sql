--query target_ways_XXX table
select osm_id, bridge, oneway, layer, highway, z_order, ST_AsGeoJSON(way) from target_ways_%s 
where highway IN ('motorway','motorway_link','primary','primary_link','trunk','trunk_link');