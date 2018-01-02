'''
configuration parameters
'''
import sys

SQL_FILE = {"create_insert_intersection_points_table":
            "\\sql\\01-create_insert_intersection_points_table.sql",
            "query_intersection_points": "\\sql\\02-query_intersection_points.sql",
            "create_insert_key_locations_table": "\\sql\\03-create_insert_key_locations_table.sql",
            "query_key_locations": "\\sql\\04-query_key_locations.sql",
            "create_temp_roads_table": "\\sql\\05-create_temp_roads_table.sql",
            "insert_target_data_to_temp_roads_table":
            "\\sql\\06-insert_target_data_to_temp_roads_table.sql",
            "query_temp_roads":"\\sql\\07-query_temp_roads.sql",
            "query_main_road_intersection_points":"\\sql\\08-query_main_road_intersection_points.sql",
            "create_final_roads_table": "\\sql\\09-create_final_roads_table.sql",
            "insert_final_roads_data_to_table": "\\sql\\10-insert_final_roads_data_to_table.sql",
            "update_temp_road_code_list": "\\sql\\99_update_temp_road_code_list.sql"}

CREATE_INSERT_INTERSECTION_POINTS_TABLE = ""

QUERY_INTERSECTION_POINTS = ""

CREATE_INSERT_KEY_LOCATIONS_TABLE = ""

QUERY_KEY_LOCATIONS = ""

CREATE_TEMP_ROADS_TABLE = ""

INSERT_TARGET_DATA_TO_TEMP_ROADS_TABLE = ""

QUERY_TEMP_ROADS = ""

QUERY_MAIN_ROAD_INTERSECTION_POINTS = ""

CREATE_FINAL_ROADS_TABLE = ""

INSERT_FINAL_ROADS_DATA_TO_TABLE = ""

UPDATE_TEMP_ROAD_CODE_LIST = ""

POSTGREDB = {
    "database":"shanghai_test_data",
    "user":"postgres",
    "password":"qq281134181",
    "host":"localhost",
    "port":"5432"
}

def init_config():
    '''
    init config,some sql scripts.
    '''
    global CREATE_INSERT_INTERSECTION_POINTS_TABLE
    global QUERY_INTERSECTION_POINTS
    global CREATE_INSERT_KEY_LOCATIONS_TABLE
    global QUERY_KEY_LOCATIONS
    global CREATE_TEMP_ROADS_TABLE
    global INSERT_TARGET_DATA_TO_TEMP_ROADS_TABLE
    global QUERY_TEMP_ROADS
    global QUERY_MAIN_ROAD_INTERSECTION_POINTS
    global CREATE_FINAL_ROADS_TABLE
    global INSERT_FINAL_ROADS_DATA_TO_TABLE
    global UPDATE_TEMP_ROAD_CODE_LIST

    CREATE_INSERT_INTERSECTION_POINTS_TABLE = read_file(
        sys.path[0] + SQL_FILE["create_insert_intersection_points_table"])
    QUERY_INTERSECTION_POINTS = read_file(
        sys.path[0] + SQL_FILE["query_intersection_points"])
    CREATE_INSERT_KEY_LOCATIONS_TABLE = read_file(
        sys.path[0] + SQL_FILE["create_insert_key_locations_table"])
    QUERY_KEY_LOCATIONS = read_file(
        sys.path[0] + SQL_FILE["query_key_locations"])
    CREATE_TEMP_ROADS_TABLE = read_file(
        sys.path[0] + SQL_FILE["create_temp_roads_table"])
    INSERT_TARGET_DATA_TO_TEMP_ROADS_TABLE = read_file(
        sys.path[0] + SQL_FILE["insert_target_data_to_temp_roads_table"])
    QUERY_TEMP_ROADS = read_file(
        sys.path[0] + SQL_FILE["query_temp_roads"])
    QUERY_MAIN_ROAD_INTERSECTION_POINTS = read_file(
        sys.path[0] + SQL_FILE["query_main_road_intersection_points"])
    CREATE_FINAL_ROADS_TABLE = read_file(
        sys.path[0] + SQL_FILE["create_final_roads_table"])
    INSERT_FINAL_ROADS_DATA_TO_TABLE = read_file(
        sys.path[0] + SQL_FILE["insert_final_roads_data_to_table"])
    UPDATE_TEMP_ROAD_CODE_LIST = read_file(
        sys.path[0] + SQL_FILE["update_temp_road_code_list"])

def read_file(filepath):
    '''
    read file
    '''
    file_object = open(filepath, 'r')
    all_text = file_object.read()
    file_object.close()
    return all_text
