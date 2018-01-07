WITH road AS (
    SELECT ST_LineMerge(ST_Union(way)) AS way
    FROM target_ways_{timesign}
    WHERE road_code_list LIKE '%{road_id}%'
), other_roads AS (
    SELECT
      target_ways_{timesign}.osm_id,
      target_ways_{timesign}.way
    FROM target_ways_{timesign}, road
    WHERE target_ways_{timesign}.highway IN ('trunk', 'trunk_link')
          AND
          road_code_list NOT LIKE '%{road_id}%'
), other_roads_collection AS (
    SELECT ST_Union(other_roads.way) AS multi_line
    FROM other_roads
), split_string AS (
    SELECT (ST_Dump(ST_Split(road.way, other_roads_collection.multi_line))).geom AS short_line
    FROM road, other_roads_collection
)
SELECT DISTINCT ON (split_string.short_line)
  ST_AsGeoJSON(ST_StartPoint(split_string.short_line)),
  ST_AsGeoJSON(ST_EndPoint(split_string.short_line)),
  ST_Length(split_string.short_line)
FROM split_string;