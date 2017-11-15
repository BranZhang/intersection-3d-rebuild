'''
todo
'''

import geojson

class GeoPoint(object):
    '''
    geopoint
    '''
    def __init__(self, parameter_type, args):
        if parameter_type == 'database':
            self.base_data = args
            self.geo_data = geojson.loads(self.base_data["cross_point"])

            self.latitude = self.geo_data['coordinates'][0]
            self.longitude = self.geo_data['coordinates'][1]
            self.parent_line_ids = []
            self.parent_line_ids.append(self.base_data['first_way_id'])
            self.parent_line_ids.append(self.base_data['second_way_id'])
        elif parameter_type == 'location':
            self.latitude = args[0]
            self.longitude = args[1]