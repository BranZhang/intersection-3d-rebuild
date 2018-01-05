WITH short_lines AS (
    SELECT osm_id, way
    FROM target_ways_{timesign}
    WHERE road_code_list LIKE '%{road_id}%'
),road AS (
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
  ST_X(cross_points.point) AS x,
  ST_Y(cross_points.point) AS y,
  short_lines.osm_id
FROM cross_points, short_lines
WHERE ST_Touches(short_lines.way, cross_points.point);