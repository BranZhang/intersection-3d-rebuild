import sys

SQL_FILE = {"create_intersection_points_table": "\\sql\\01-create_intersection_points_table.sql",
            "calculate_intersection_points": "\\sql\\02-calculate_intersection_points.sql",
            "create_key_locations_table": "\\sql\\03-create_key_locations_table.sql",
            "insert_key_locations_to_table": "\\sql\\04-insert_key_locations_to_table.sql",
            "create_temp_roads_table": "\\sql\\05-create_temp_roads_table.sql",
            "insert_target_data_to_temp_roads_table":
            "\\sql\\06-insert_target_data_to_temp_roads_table.sql",
            "create_final_roads_table": "\\sql\\07-create_final_roads_table.sql",
            "insert_final_roads_data_to_table": "\\sql\\08-insert_final_roads_data_to_table.sql"}

CREATE_INTERSECTION_POINTS_TABLE = ""

CALCULATE_INTERSECTION_POINTS = ""

CREATE_KEY_LOCATIONS_TABLE = ""

INSERT_KEY_LOCATIONS_TO_TABLE = ""

CREATE_TEMP_ROADS_TABLE = ""

INSERT_TARGET_DATA_TO_TEMP_DATA_TABLE = ""

CREATE_FINAL_ROADS_TABLE = ""

INSERT_FINAL_ROADS_DATA_TO_TABLE = ""


def init_config():
    '''
    init config,some sql scripts.
    '''
    global CREATE_INTERSECTION_POINTS_TABLE
    global CALCULATE_INTERSECTION_POINTS
    global CREATE_KEY_LOCATIONS_TABLE
    global INSERT_KEY_LOCATIONS_TO_TABLE
    global CREATE_TEMP_ROADS_TABLE
    global INSERT_TARGET_DATA_TO_TEMP_DATA_TABLE
    global CREATE_FINAL_ROADS_TABLE
    global INSERT_FINAL_ROADS_DATA_TO_TABLE

    CREATE_INTERSECTION_POINTS_TABLE = read_file(
        sys.path[0] + SQL_FILE["create_intersection_points_table"])
    CALCULATE_INTERSECTION_POINTS = read_file(
        sys.path[0] + SQL_FILE["calculate_intersection_points"])
    CREATE_KEY_LOCATIONS_TABLE = read_file(
        sys.path[0] + SQL_FILE["create_key_locations_table"])
    INSERT_KEY_LOCATIONS_TO_TABLE = read_file(
        sys.path[0] + SQL_FILE["insert_key_locations_to_table"])
    CREATE_TEMP_ROADS_TABLE = read_file(
        sys.path[0] + SQL_FILE["create_temp_roads_table"])
    INSERT_TARGET_DATA_TO_TEMP_DATA_TABLE = read_file(
        sys.path[0] + SQL_FILE["insert_target_data_to_temp_roads_table"])
    CREATE_FINAL_ROADS_TABLE = read_file(
        sys.path[0] + SQL_FILE["create_final_roads_table"])
    INSERT_FINAL_ROADS_DATA_TO_TABLE = read_file(
        sys.path[0] + SQL_FILE["insert_final_roads_data_to_table"])

def read_file(filepath):
    '''
    read file
    '''
    file_object = open(filepath, 'r')
    all_text = file_object.read()
    file_object.close()
    return all_text
