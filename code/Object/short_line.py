'''
todo
'''
import geojson
from Object.geomtry_point import GeoPoint


class ShortLine(object):
    '''
    line from one point to another
    '''

    def __init__(self, db_data):
        self.base_data = db_data
        self.geo_data = geojson.loads(self.base_data["st_asgeojson"])
        self.database_id = self.base_data['osm_id']
        self.z_order = self.base_data['z_order']
        self.bridge = self.base_data['bridge'] == 'yes'
        self.point_list = []

        for p in self.geo_data["coordinates"]:
            self.point_list.append(GeoPoint(p))

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

    # 将线性规划得到的有高度值的点与当前直线的点混合在一起。
    def save_z_value(self, road_points_list):
        for point1 in road_points_list:
            for point2 in self.point_list:
                if point1.equal(point2):
                    point2.altitude = point1.altitude
                    break

    