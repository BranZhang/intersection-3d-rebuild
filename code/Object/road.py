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

        points_list = []
        for location in self.merge_other_points([GeoPoint(p) for p in points_z_value.keys()]):
            z_value = -99
            if (location.longitude,location.latitude) in points_z_value:
                z_value = points_z_value[(location.longitude,location.latitude)]
            points_list.append(GeoPoint((location.longitude,location.latitude), z_value))
        
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

    def merge_other_points(self, other_points):
        point_list = []

        if self.short_line_list[0].start_point.equal(self.start_point):
            point_list += self.short_line_list[0].point_list
        else:
            point_list += self.short_line_list[0].point_list[::-1]

        for short_line in self.short_line_list[1:]:
            if short_line.start_point.equal(point_list[-1]):
                del point_list[-1]
                point_list += short_line.point_list
            else:
                del point_list[-1]
                point_list += short_line.point_list[::-1]
        
        for point in other_points:
            next_point = False
            for p in point_list:
                if p.equal(point):
                    next_point = True
                    break
            if next_point:
                continue
            distance_list = []
            distance_list.append(get_distance(point, point_list[0]) * 2)
            for n in range(0, len(point_list) - 1):
                distance_list.append(get_distance(point, point_list[n]) + get_distance(point, point_list[n+1]) - get_distance(point_list[n], point_list[n+1]))
            distance_list.append(get_distance(point, point_list[-1]) * 2)

            point_list.insert(distance_list.index(min(distance_list)), point)

        return point_list
# ','.join(["ST_GeomFromText('POINT({0} {1})', 3857)".format(p.longitude, p.latitude) for p in point_list])