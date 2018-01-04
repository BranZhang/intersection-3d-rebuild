'''
todo
'''
import geojson

class TouchPoint(object):

    def __init__(self, longitude, latitude, parent_line_ids):
        self.longitude = longitude
        self.latitude = latitude
        self.parent_line_ids = parent_line_ids
