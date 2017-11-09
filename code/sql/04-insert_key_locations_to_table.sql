--insert key locations calculate by python code to table
INSERT INTO test_ways 
SELECT osm_id, access, "addr:housename", "addr:housenumber", "addr:interpolation", admin_level, aerialway, 
aeroway, amenity, area, barrier, bicycle, brand, bridge, boundary, building , construction,covered,culvert,
cutting,denomination,disused,embankment,foot,"generator:source",
harbour,highway,historic,horse,intermittent,junction,landuse,layer,leisure,lock,man_made,military,motorcar,
name,"natural",office,oneway,operator,place,population,power,power_source,public_transport,railway,ref,
religion,route,service,shop,sport,surface,toll,tourism,"tower:type",tracktype,tunnel,water,waterway,wetland,
width,wood,z_order,way_area, ST_Intersection(
P.way, 
ST_Buffer('SRID=3857;POINT(-13615199 5989472)'::geometry, 2500, 'quad_segs=8'))
from planet_osm_line AS P
where ST_Crosses(P.way, ST_Buffer('SRID=3857;POINT(-13615199 5989472)'::geometry, 2500, 'quad_segs=8'))
OR ST_Contains(ST_Buffer('SRID=3857;POINT(-13615199 5989472)'::geometry, 2500, 'quad_segs=8'), P.way);