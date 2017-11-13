'''
todo
'''

import geojson

class ShortLine(object):
    '''
    line from one point to another????wrong
    '''
    def __init__(self, line_string):
        self.base_data = line_string
        self.geo_data = geojson.loads(self.base_data["st_asgeojson"])
