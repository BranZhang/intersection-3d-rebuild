'''
main process.
'''
import config
import dbmanager


def main():
    config.init_config()
    dbmanager.connect_to_database()
    # dbmanager.create_temp_roads_table()
    # dbmanager.insert_target_data_to_temp_roads_table()

    # load data from database, include road data and their intersection points.
    original_road_string_data = dbmanager.query_temp_roads()
    intersection_point_data = dbmanager.query_total_intersection_points()

    # get complete road data from original road data.
    complete_road_string_data = get_complete_road_string_list(
        original_road_string_data)
    '''
    complete_road_string_data must be checked by QGIS.
    '''

    # confirm each intersection point's matching road height at this point.

    # assign each complete road of their intersection points.

    # interpolate each complete road.

    # smooth each complete road in its z axis.

    # save road data with z value to database.

    # disconnect to database.
    dbmanager.disconnect_to_database()


def get_complete_road_string_list(original_road_string_data):
    '''
    todo
    '''
    result = []
    roads_id_list = []

    for single_string in original_road_string_data:
        if single_string.base_data['osm_id'] in roads_id_list:
            continue

        single_road = []
        # do something.

        result.append(single_road)
        for temp in single_road:
            if temp.base_data['osm_id'] not in roads_id_list:
                roads_id_list.append(temp.base_data['osm_id'])

    return result


if __name__ == '__main__':
    main()
