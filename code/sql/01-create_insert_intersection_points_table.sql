--create table to store only main roads' intersection points.
CREATE TABLE intersection_points_%s (
    id SERIAL PRIMARY KEY, 
    location GEOMETRY(POINT,3857)
    );

--insert data to table.
INSERT INTO intersection_points_%s (location) 
SELECT DISTINCT (ST_Dump(ST_Intersection(A.way, B.way))).geom 
FROM planet_osm_roads AS A,planet_osm_roads AS B 
WHERE ST_Crosses(A.way, B.way) 
AND A.highway  IN ('motorway','motorway_link','primary','primary_link','trunk','trunk_link')
AND B.highway  IN ('motorway','motorway_link','primary','primary_link','trunk','trunk_link');

--rarefy this points.
--todo