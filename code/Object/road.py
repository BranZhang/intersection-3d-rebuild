import gistools

class Road(object):

    def __init__(self, short_line_list):
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
        self.distance = gistools.get_distance(self.start_point, self.end_point)
