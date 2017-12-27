'''
todo
'''
import geojson
from Object.geomtry_point import GeoPoint
from Object.gistools import get_bearing_angle


class ShortLine(object):
    '''
    line from one point to another
    '''

    def __init__(self, db_data):
        self.base_data = db_data
        self.geo_data = geojson.loads(self.base_data["st_asgeojson"])
        self.database_id = self.base_data['osm_id']
        self.point_list = []

        for p in self.geo_data["coordinates"]:
            self.point_list.append(GeoPoint('location', p))

        self.start_point = self.point_list[0]
        self.end_point = self.point_list[len(self.point_list) - 1]

        self.check_tag = ""

    def get_vector(self):
        if self.check_tag == "start":
            return ((self.point_list[0].longitude - self.point_list[1].longitude) * 10000,
                    (self.point_list[0].latitude - self.point_list[1].latitude) * 10000)
        else:
            return ((self.point_list[len(self.point_list) - 1].longitude
                     - self.point_list[len(self.point_list) - 2].longitude) * 10000,
                    (self.point_list[len(self.point_list) - 1].latitude
                     - self.point_list[len(self.point_list) - 2].latitude) * 10000)


    def get_analyse_point(self):
        if self.check_tag == "start":
            return self.point_list[0]
        else:
            return self.point_list[len(self.point_list) - 1]


    def match(self, point):
        if self.start_point.equal(point):
            self.check_tag = "start"
            return "start"
        elif self.end_point.equal(point):
            self.check_tag = "end"
            return "end"
        else:
            return ""