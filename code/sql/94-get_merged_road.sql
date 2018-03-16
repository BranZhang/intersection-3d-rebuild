-- other_points like ST_GeomFromText('POINT(123 456)', 3857),ST_GeomFromText('POINT(123 457)', 3857)
-- Although I use 'UNION' instead of 'UNION ALL', result still contains duplicate row. 
-- this problem may be caused by postgis accuracy.
-- useing 'st_removerepeatedpoints()' to solve problem above. 
WITH road AS (
    SELECT (ST_DumpPoints(way)).geom AS point
    FROM target_ways_{timesign}
    WHERE road_code_list LIKE '%{road_id}%'
), other_points AS (
    SELECT unnest(
               ARRAY [{other_points}]) AS point
), all_points AS (
    SELECT point
    FROM road
    UNION SELECT point
          FROM other_points
), ordered_points AS (
    SELECT point
    FROM all_points
    GROUP BY point
    ORDER BY st_closestpoint(point, point)
)
SELECT st_asgeojson(st_removerepeatedpoints(st_makeline(point), 8))
FROM ordered_points;