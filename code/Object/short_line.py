'''
todo
'''
from geomtry_point import GeoPoint
import geojson


class ShortLine(object):
    '''
    line from one point to another????wrong
    '''

    def __init__(self, db_data):
        self.base_data = db_data
        self.geo_data = geojson.loads(self.base_data["st_asgeojson"])
        self.start_point = GeoPoint('location', self.geo_data["coordinates"][0])
        self.end_point = GeoPoint(
            'location', self.geo_data["coordinates"][len(self.geo_data["coordinates"]) - 1])

