'''
todo
'''
import geojson

class EndPoint(object):

    def __init__(self, db_data):
        self.base_data = geojson.loads(db_data)

        self.longitude = self.base_data['coordinates'][0]
        self.latitude = self.base_data['coordinates'][1]
        self.parent_line_ids = []

    def get_location(self):
        return (self.longitude, self.latitude)