--insert main roads' intersection points to table
--rarefy this points
INSERT INTO intersection_points (location) 
SELECT DISTINCT (ST_Dump(ST_Intersection(A.way, B.way))).geom 
FROM planet_osm_roads AS A,planet_osm_roads AS B 
WHERE ST_Crosses(A.way, B.way) 
AND A.highway  IN ('motorway','motorway_link','primary','primary_link','trunk','trunk_link')
AND B.highway  IN ('motorway','motorway_link','primary','primary_link','trunk','trunk_link');