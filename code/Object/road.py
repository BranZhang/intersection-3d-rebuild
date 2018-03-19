'''
todo
'''
import geojson

from Object.geomtry_point import GeoPoint
from Object.gistools import get_distance


class Road(object):
    '''
    road of several short lines
    '''

    def __init__(self, short_line_list):
        self.road_id = ""
        self.short_line_list = short_line_list
        if len(short_line_list) == 1:
            self.start_point = short_line_list[0].start_point
            self.end_point = short_line_list[0].end_point
        else:
            if short_line_list[0].start_point.equal(
                    short_line_list[1].start_point) or short_line_list[0].start_point.equal(
                        short_line_list[1].end_point):
                self.start_point = short_line_list[0].end_point
            else:
                self.start_point = short_line_list[0].start_point

            if short_line_list[len(short_line_list) - 1].start_point.equal(
                    short_line_list[len(short_line_list) - 2].start_point) or short_line_list[len(
                        short_line_list) - 1].start_point.equal(
                            short_line_list[len(short_line_list) - 2].end_point):
                self.end_point = short_line_list[len(
                    short_line_list) - 1].end_point
            else:
                self.end_point = short_line_list[len(
                    short_line_list) - 1].start_point
        self.distance = get_distance(self.start_point, self.end_point)


    def is_line_id_in_line_list(self, line_id):
        for line in self.short_line_list:
            if line_id == line.database_id:
                return True

        return False

    def smooth_z_axis(self, road_point_data, points_z_value):
        for short_line in self.short_line_list:
            for point in short_line.point_list:
                if point.altitude != -99:
                    points_z_value[(point.longitude,point.latitude)] = point.altitude

        road_point_json = geojson.loads(road_point_data)
        points_list = []
        for location in road_point_json['coordinates']:
            z_value = -99
            if (location[0], location[1]) in points_z_value:
                z_value = points_z_value[(location[0], location[1])]
            points_list.append(GeoPoint(location, z_value))
        
        distance_list = []
        index_list = []
        last_point = None
        for i,point in enumerate(points_list):
            if point.altitude != -99:
                index_list.append(i)
            if last_point:
                distance_list.append(get_distance(point, last_point))
            last_point = point

            sum_distance = sum(distance_list)
            if len(index_list) == 2:
                distance_accumulate = 0
                for m in range(index_list[0]+1, index_list[1]):
                    distance_accumulate += distance_list[m-(index_list[0]+1)]
                    points_list[m].altitude = points_list[index_list[0]].altitude + (points_list[index_list[1]].altitude - points_list[index_list[0]].altitude) * distance_accumulate / sum_distance
                distance_list.clear()
                del index_list[0]

        self.points_with_z_value_list = points_list
        for short_line in self.short_line_list:
            short_line.save_z_value(points_list)