'''
todo
'''
import geojson
from Object.geomtry_point import GeoPoint
from Object.gistools import get_bearing_angle


class ShortLine(object):
    '''
    line from one point to another????wrong
    '''

    def __init__(self, db_data):
        self.base_data = db_data
        self.geo_data = geojson.loads(self.base_data["st_asgeojson"])
        self.database_id = self.geo_data["id"]
        self.start_point = GeoPoint(
            'location', self.geo_data["coordinates"][0])
        self.end_point = GeoPoint(
            'location', self.geo_data["coordinates"][len(self.geo_data["coordinates"]) - 1])

        self.start_angle = get_bearing_angle(
            GeoPoint('location', self.geo_data["coordinates"][1]), self.start_point)
        self.end_angle = get_bearing_angle(GeoPoint(
            'location', self.geo_data["coordinates"][len(self.geo_data["coordinates"]) - 2]), self.end_point)
