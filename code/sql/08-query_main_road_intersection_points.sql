--not test.
-- maybe data project has problem.
SELECT DISTINCT ON (C.cross_point) C.*
FROM (
       SELECT
         ST_AsGeoJSON((ST_Dump(ST_Intersection(A.way, B.way))).geom) AS cross_point,
         A.osm_id                                                    AS first_way_id,
         B.osm_id                                                    AS second_way_id
       FROM target_ways_{timesign} AS A, target_ways_{timesign} AS B
       WHERE ST_Crosses(A.way, B.way)
             AND A.highway IN ('trunk', 'trunk_link')
             AND B.highway IN ('trunk', 'trunk_link')
     ) AS C;