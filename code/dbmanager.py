'''
todo
'''
import datetime

import psycopg2
import psycopg2.extras

import config
from Object.short_line import ShortLine
from Object.intersection_point import IntersectionPoint
from Object.touch_point import TouchPoint
from Object.end_point import EndPoint

CONN = ""
TIME_SIGN = ""


def connect_to_database():
    global CONN
    global TIME_SIGN

    time = datetime.datetime.now()
    TIME_SIGN = '%s_%s_%s_%s_%s_%s' % (
        time.month, time.day, time.hour, time.minute, time.second, time.microsecond)

    try:
        CONN = psycopg2.connect(
            dbname=config.POSTGREDB["database"],
            user=config.POSTGREDB["user"],
            password=config.POSTGREDB["password"],
            host=config.POSTGREDB["host"])
    except psycopg2.Error as exception:
        print(exception.pgerror)
        return False


    return True


def disconnect_to_database():
    CONN.close()


def create_insert_intersection_points_table():
    global CONN
    global TIME_SIGN

    cur = CONN.cursor()
    cur.execute(config.CREATE_INSERT_INTERSECTION_POINTS_TABLE.format(
        timesign=TIME_SIGN))
    CONN.commit()


def query_intersection_points():
    global CONN
    global TIME_SIGN

    cur = CONN.cursor()
    cur.execute(config.QUERY_INTERSECTION_POINTS)
    CONN.commit()


def create_insert_key_locations_table():
    global CONN
    global TIME_SIGN

    cur = CONN.cursor()
    cur.execute(config.CREATE_INSERT_KEY_LOCATIONS_TABLE)
    CONN.commit()


def query_key_locations():
    global CONN
    global TIME_SIGN

    cur = CONN.cursor()
    cur.execute(config.QUERY_KEY_LOCATIONS)
    CONN.commit()


def create_temp_roads_table():
    global CONN
    global TIME_SIGN

    cur = CONN.cursor()
    cur.execute(config.CREATE_TEMP_ROADS_TABLE.format(timesign=''))
    CONN.commit()


def insert_target_data_to_temp_roads_table():
    global CONN
    global TIME_SIGN

    cur = CONN.cursor()
    cur.execute(
        config.INSERT_TARGET_DATA_TO_TEMP_ROADS_TABLE.format(timesign=''))
    CONN.commit()


def query_temp_roads():
    '''
    tested.
    '''
    global CONN
    global TIME_SIGN

    cur = CONN.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(config.QUERY_TEMP_ROADS.format(timesign=''))

    result = {}

    for row in cur:
        result[row['osm_id']] = ShortLine(row)

    return result


def query_main_road_intersection_points():
    '''
    tested.
    '''
    global CONN
    global TIME_SIGN

    cur = CONN.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(config.QUERY_MAIN_ROAD_INTERSECTION_POINTS.format(timesign=''))
    result = []

    for row in cur:
        result.append(IntersectionPoint(row))

    cross_point_list = {}

    for point in result:
        cross_point_list[point.get_location()] = point.parent_line_ids

    return cross_point_list


def query_main_road_touch_points(road_id):
    global CONN
    global TIME_SIGN

    cur = CONN.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(config.QUERY_SINGLE_ROAD_TOUCH_POINTS.format(
        timesign='', road_id=road_id))
    result = {}

    for row in cur:
        if (row['x'], row['y']) in result.keys():
            result[(row['x'], row['y'])].append(str(row['osm_id']))
        else:
            result[(row['x'], row['y'])] = [str(row['osm_id'])]

    return result


def query_main_road_end_points(road_id):
    global CONN
    global TIME_SIGN

    cur = CONN.cursor()
    cur.execute(config.QUERY_SINGLE_ROAD_END_POINTS.format(
        timesign='', road_id=road_id))
    result = []

    for row in cur:
        result.append(EndPoint(row[0], row[1]))
        result.append(EndPoint(row[2], row[3]))

    return result


def create_final_roads_table():
    global CONN
    global TIME_SIGN

    cur = CONN.cursor()
    cur.execute(config.CREATE_FINAL_ROADS_TABLE)
    CONN.commit()


def insert_final_roads_data_to_table():
    global CONN
    global TIME_SIGN

    cur = CONN.cursor()
    cur.execute(config.INSERT_FINAL_ROADS_DATA_TO_TABLE)
    CONN.commit()


def update_temp_road_code_list(short_line_id, road_code_list):
    global CONN
    global TIME_SIGN

    cur = CONN.cursor()
    cur.execute(config.UPDATE_TEMP_ROAD_CODE_LIST.format(
        timesign='', osm_id=short_line_id, code_list=road_code_list))
    CONN.commit()


def insert_each_point_code_list(insert_data):
    global CONN
    global TIME_SIGN

    cur = CONN.cursor()
    cur.execute(config.INSERT_TYPE_POINTS.format(
        timesign='',
        insert_data=insert_data))
    CONN.commit()


def get_distance_of_a_road(road_id):
    global CONN
    global TIME_SIGN

    cur = CONN.cursor()
    cur.execute(config.GET_DISTANCE_OF_A_ROAD.format(
        timesign='',
        road_id=road_id))

    result = {}
    for row in cur:
        result[((row[0], row[1]),
                (row[2], row[3]))] = row[4]
        # result[((row['start_x'], row['start_y']),
        #         (row['end_x'], row['end_y']))] = row['length']

    return result
