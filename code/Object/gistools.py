'''
todo
'''
import math


def get_bearing_angle(start_geo_point, end_geo_point):
    '''
    calculate angle between two points.
    '''
    return math.atan(
        (end_geo_point.latitude - start_geo_point.latitude)
        / (end_geo_point.longitude - start_geo_point.longitude)) * 180.0 / math.pi
