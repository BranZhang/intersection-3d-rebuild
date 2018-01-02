'''
todo
'''
import geojson

class IntersectionPoint(object):

    def __init__(self, db_data):
        self.base_data = db_data
        self.geo_data = geojson.loads(self.base_data["cross_point"])

        self.longitude = self.geo_data['coordinates'][0]
        self.latitude = self.geo_data['coordinates'][1]
        self.parent_line_ids = []
        self.parent_line_ids.append(self.base_data['first_way_id'])
        self.parent_line_ids.append(self.base_data['second_way_id'])
