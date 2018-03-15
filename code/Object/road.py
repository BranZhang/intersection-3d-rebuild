'''
todo
'''
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
        pass