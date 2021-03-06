--create table to store only main roads' intersection points.
CREATE TABLE IF NOT EXISTS intersection_points_{timesign} (
  id       SERIAL PRIMARY KEY,
  LOCATION GEOMETRY(POINT, 3857
           )
);

--clear.
DELETE FROM intersection_points_%s;

--insert data to table.
INSERT INTO intersection_points_{timesign} ( LOCATION )
SELECT DISTINCT (ST_Dump(ST_Intersection(A.way, B.way))).geom
FROM planet_osm_roads AS A, planet_osm_roads AS B
WHERE ST_Crosses(A.way, B.way)
      AND A.highway IN ('motorway', 'motorway_link', 'primary', 'primary_link', 'trunk', 'trunk_link')
      AND B.highway IN ('motorway', 'motorway_link', 'primary', 'primary_link', 'trunk', 'trunk_link');

--rarefy this points.
--todo