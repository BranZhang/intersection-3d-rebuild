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
), other_roads AS (
    SELECT way
    FROM target_ways_{timesign}
    WHERE road_code_list NOT LIKE '%{road_id}%'
), touch_points AS (
    SELECT (ST_Dump(ST_Intersection(road.way, other_roads.way))).geom AS point
    FROM road, other_roads
)
SELECT
  DISTINCT ON (touch_points.point)
  ST_X(touch_points.point) AS x,
  ST_Y(touch_points.point) AS y,
  short_lines.osm_id
FROM touch_points
  LEFT JOIN short_lines ON ST_Distance(touch_points.point, short_lines.way) < 1e-14
WHERE NOT ST_IsEmpty(touch_points.point);