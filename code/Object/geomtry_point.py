'''
todo
'''

# import geojson


class GeoPoint(object):
    '''
    geopoint
    '''

    def __init__(self, location):
        self.longitude = location[0]
        self.latitude = location[1]

    def equal(self, other_geopoint):
        return other_geopoint.latitude == self.latitude and other_geopoint.longitude == self.longitude
