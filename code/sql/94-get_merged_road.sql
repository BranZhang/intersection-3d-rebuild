-- useless
WITH road AS (
    SELECT ST_LineMerge(ST_Union(way)) AS way
    FROM target_ways_{timesign}
    WHERE road_code_list LIKE '%{road_id}%'
)
SELECT ST_AsGeoJSON(way) AS way_json
FROM road;