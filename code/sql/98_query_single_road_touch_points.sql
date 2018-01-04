WITH road AS (
    SELECT ST_LineMerge(ST_Union(way)) AS way
    FROM target_ways_{timesign}
    WHERE road_code_list LIKE '%{road_id}%'
), other_roads AS (
    SELECT way
    FROM target_ways_{timesign}
    WHERE road_code_list NOT LIKE '%{road_id}%'
), cross_points AS (
    SELECT ST_Intersection(road.way, other_roads.way) AS point
    FROM road, other_roads
    WHERE ST_Relate(road.way, other_roads.way, 'F0*FF****')
)
SELECT
  ST_X(point) AS x,
  ST_Y(point) AS y
FROM cross_points;