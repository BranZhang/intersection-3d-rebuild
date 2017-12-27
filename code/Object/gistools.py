'''
todo
'''
import math
from pyproj import Proj, transform

def get_bearing_angle(start_geo_point, end_geo_point):
    '''
    calculate angle between two points.
    '''
    return math.atan(
        (end_geo_point.latitude - start_geo_point.latitude)
        / (end_geo_point.longitude - start_geo_point.longitude)) * 180.0 / math.pi


def get_angle_by_vector(line1, line2):
    '''
    calculate angle between two vectors.
    '''
    vector1 = line1.get_vector()
    vector2 = line2.get_vector()

    sin = vector1[0] * vector2[1] - vector2[0] * vector1[1]
    cos = vector1[0] * vector2[0] + vector1[1] * vector2[1]

    return abs(math.atan2(sin, cos) * (180 / math.pi))


def get_distance(geo_point1, geo_point2):
    '''
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    '''
    point1 = turn_3857_project_to_4326(geo_point1.longitude, geo_point1.latitude)
    point2 = turn_3857_project_to_4326(geo_point2.longitude, geo_point2.latitude)

    lon1, lat1, lon2, lat2 = map(
        math.radians, [point1[0], point1[1], point2[0], point2[1]])

    dlon = lon2 - lon1
    dlat = lat2 - lat1
    _a = math.sin(dlat / 2)**2 + math.cos(lat1) * \
        math.cos(lat2) * math.sin(dlon / 2)**2
    _c = 2 * math.asin(math.sqrt(_a))
    return _c * 6371 * 1000


def turn_3857_project_to_4326(longitude, latitude):
    in_proj = Proj(init='epsg:3857')
    out_proj = Proj(init='epsg:4326')
    _x2, _y2 = transform(in_proj, out_proj, longitude, latitude)
    return (_x2, _y2)
