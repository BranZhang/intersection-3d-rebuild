WITH short_lines AS (
    SELECT
      osm_id,
      way
    FROM target_ways_{timesign}
    WHERE road_code_list LIKE '%{road_id}%'
), road AS (
    SELECT ST_LineMerge(ST_Union(way)) AS way
    FROM target_ways_{timesign}
    WHERE road_code_list LIKE '%{road_id}%'
), start_point AS (
    SELECT ST_StartPoint(way) AS point
    FROM road
), end_point AS (
    SELECT ST_EndPoint(way) AS point
    FROM road
)
SELECT
  ST_AsGeoJSON(start_point.point) AS start_point,
  A.osm_id,
  ST_AsGeoJSON(end_point.point)   AS end_point,
  B.osm_id
FROM start_point, end_point, short_lines AS A, short_lines AS B
WHERE ST_Touches(A.way, start_point.point) AND ST_Touches(B.way, end_point.point);