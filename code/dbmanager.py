import psycopg2
import psycopg2.extras

import config
import datetime
from Object.short_line import ShortLine 

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
    except psycopg2.Error as e:
        print e.pgerror

    if CONN:
        return True
    else:
        return False


def disconnect_to_database():
    CONN.close()


def create_insert_intersection_points_table():
    global CONN
    global TIME_SIGN

    cur = CONN.cursor()
    cur.execute(config.CREATE_INSERT_INTERSECTION_POINTS_TABLE % (TIME_SIGN))
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
    cur.execute(config.CREATE_TEMP_ROADS_TABLE % (""))
    CONN.commit()


def insert_target_data_to_temp_roads_table():
    global CONN
    global TIME_SIGN

    cur = CONN.cursor()
    cur.execute(config.INSERT_TARGET_DATA_TO_TEMP_ROADS_TABLE % ("", ""))
    CONN.commit()


def query_temp_roads():
    '''
    tested.
    '''
    global CONN
    global TIME_SIGN

    cur = CONN.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cur.execute(config.QUERY_TEMP_ROADS % (""))

    result = []

    for row in cur:
        result.append(ShortLine(row))

    return result


def query_total_intersection_points():
    global CONN
    global TIME_SIGN

    cur = CONN.cursor()
    cur.execute(config.QUERY_TOTAL_INTERSECTION_POINTS)
    CONN.commit()


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
