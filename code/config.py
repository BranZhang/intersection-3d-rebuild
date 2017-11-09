import os
import sys

CREATE_INTERSECTION_POINTS_TABLE = ""

CALCULATE_INTERSECTION_POINTS = ""


def init_config():
    CREATE_INTERSECTION_POINTS_TABLE = read_file(sys.path[0] + "\\sql\\01-create_intersection_points_table.sql")
    pass


def read_file(filepath):
    file_object = open(filepath, 'r')
    all_text = file_object.read()
    file_object.close()
    return all_text

