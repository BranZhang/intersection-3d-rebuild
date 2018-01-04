WITH road AS (
    SELECT ST_LineMerge(ST_Union(way)) AS way
    FROM target_ways_{timesign}
    WHERE road_code_list LIKE '%{road_id}%'
)
SELECT
  ST_AsGeoJSON(ST_StartPoint(road.way)) AS start_point,
  ST_AsGeoJSON(ST_EndPoint(road.way))   AS end_point
FROM road;