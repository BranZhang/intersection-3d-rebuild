'''
main process.

'''
import math
import config
import dbmanager


def main():
    config.init_config()
    dbmanager.connect_to_database()
    # dbmanager.create_temp_roads_table()
    # dbmanager.insert_target_data_to_temp_roads_table()

    # load data from database, include road data and their intersection points.
    original_road_string_data = dbmanager.query_temp_roads()
    # intersection_point_data = dbmanager.query_total_intersection_points()

    # get complete road data from original road data.
    complete_road_string_data = get_complete_road_string_list(
        original_road_string_data)

    update_road_code_to_database(complete_road_string_data)
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
    already_deal_roads_id_list = []

    for single_string in original_road_string_data:
        if single_string.base_data['osm_id'] in already_deal_roads_id_list:
            continue

        single_road = []
        single_road.append(single_string)

        current_string = (single_string, "start")
        while True:
            next_string = get_next_single_road_string(
                current_string, original_road_string_data)
            if next_string:
                current_string = next_string
                single_road.append(next_string[0])
            else:
                break

        current_string = (single_string, "end")
        while True:
            next_string = get_next_single_road_string(
                current_string, original_road_string_data)
            if next_string:
                current_string = next_string
                single_road.insert(0, next_string[0])
            else:
                break

        result.append(single_road)
        for temp in single_road:
            if temp.base_data['osm_id'] not in already_deal_roads_id_list:
                already_deal_roads_id_list.append(temp.base_data['osm_id'])

    if len(already_deal_roads_id_list) != len(original_road_string_data):
        print 'bad deal.'

    return result


def get_next_single_road_string(current_string, original_road_string_data):

    target_dict = {}

    for single_string in original_road_string_data:
        if single_string.database_id == current_string[0].database_id:
            continue
        # notice differ between 'end' and 'start'
        if current_string[1] == 'start':
            if single_string.start_point.equal(current_string[0].start_point):
                target_dict[(single_string, 'end')] = single_string.start_angle
            elif single_string.end_point.equal(current_string[0].start_point):
                target_dict[(single_string, 'start')] = single_string.end_angle
        elif current_string[1] == 'end':
            if single_string.start_point.equal(current_string[0].end_point):
                target_dict[(single_string, 'end')] = single_string.start_angle
            elif single_string.end_point.equal(current_string[0].end_point):
                target_dict[(single_string, 'start')] = single_string.end_angle

    if len(target_dict) == 1:
        return target_dict.items()[0][0]

    if current_string[1] == 'start':
        target_angle = current_string[0].start_angle
    elif current_string[1] == 'end':
        target_angle = current_string[0].end_angle

    for single_string in sorted(target_dict.iteritems(), key=lambda x: abs(x[1] - target_angle)):
        return single_string[0]

    return None


def update_road_code_to_database(complete_road_string_data):

    road_code_dict = {}
    road_count = 0

    for road in complete_road_string_data:
        for single_string in road:
            if road_code_dict.has_key(single_string.database_id):
                road_code_dict[single_string.database_id] = road_code_dict[single_string.database_id] + "[A%s]" % (road_count)
            else:
                road_code_dict[single_string.database_id] = "[A%s]" % (road_count)
        
        road_count += 1

    dbmanager.update_temp_road_code_list("", "")

if __name__ == '__main__':
    main()
