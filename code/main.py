'''
main process.
'''
import config
import dbmanager
import Object.gistools as gistools
from Object.road import Road


def main():
    config.init_config()
    dbmanager.connect_to_database()
    # dbmanager.create_temp_roads_table()
    # dbmanager.insert_target_data_to_temp_roads_table()

    # load data from database, include road data and their intersection points.
    original_road_string_data = dbmanager.query_temp_roads()
    # intersection_point_data = dbmanager.query_total_intersection_points()

    # get complete road data from original road data.
    # complete_road_string_data must be checked on QGIS.
    complete_road_string_data = get_complete_road_string_list(
        original_road_string_data)

    # just for check
    update_road_code_to_database(complete_road_string_data)

    # get all CROSS, TOUCH, END type points
    # points data must be checked on QGIS.

    # get CROSS type
    intersection_points = dbmanager.query_main_road_intersection_points()

    # get TOUCH type
    

    # get END type


    # calculate each point's height.


    # interpolate each complete road.

    # smooth each complete road in its z axis.

    # save road data with z value to database.

    # disconnect to database.
    dbmanager.disconnect_to_database()


def get_complete_road_string_list(original_road_string_data):
    '''
    return Road Class List,order by distance of road's start point to end point.
    '''
    result = []
    already_deal_roads_id_list = []

    for (id, single_string) in original_road_string_data.items():
        if id in already_deal_roads_id_list:
            continue

        single_road = []
        single_road.append(single_string)

        current_string = single_string
        while True:
            current_string.check_tag = "end"
            next_string = get_next_single_road_string(
                current_string, original_road_string_data)
            if next_string:
                current_string = next_string
                single_road.append(next_string)
            else:
                break

        current_string = single_string
        while True:
            current_string.check_tag = "start"
            next_string = get_next_single_road_string(
                current_string, original_road_string_data)
            if next_string:
                current_string = next_string
                single_road.insert(0, next_string)
            else:
                break

        result.append(Road(single_road))
        for temp in single_road:
            if temp.base_data['osm_id'] not in already_deal_roads_id_list:
                already_deal_roads_id_list.append(temp.base_data['osm_id'])

    if len(already_deal_roads_id_list) != len(original_road_string_data):
        print 'bad deal.'

    result.sort(key=lambda r: r.distance, reverse=True)
    return result


def get_next_single_road_string(current_string, original_road_string_data):

    target_dict = {}
    target_point = current_string.get_analyse_point()

    for (id, single_string) in original_road_string_data.items():
        if (id != current_string.database_id) and single_string.match(target_point):
            target_dict[single_string] = gistools.get_angle_by_vector(
                current_string, single_string)

    if len(target_dict) == 0:
        return None

    for single_string in sorted(target_dict.iteritems(), key=lambda x: 180 - x[1]):
        if single_string[1] < 90:
            return None
        else:
            return single_string[0]


def update_road_code_to_database(complete_road_string_data):

    road_code_dict = {}
    road_count = 0

    for road in complete_road_string_data:
        for single_string in road.short_line_list:
            if road_code_dict.has_key(single_string.database_id):
                road_code_dict[single_string.database_id] = road_code_dict[single_string.database_id] + \
                    "[A%s]" % (road_count)
            else:
                road_code_dict[single_string.database_id] = "[A%s]" % (
                    road_count)
        road.road_id = "[A%s]" % (road_count)
        road_count += 1

    for id in road_code_dict:
        dbmanager.update_temp_road_code_list(id, road_code_dict[id])




def order_road_by_z_order(intersection_points, original_short_line_data, complete_road_string_data):
    for point in intersection_points:
        if len(point.parent_line_ids) != 2:
            continue
        if original_short_line_data.has_key(point.parent_line_ids[0]) and \
            original_short_line_data.has_key(point.parent_line_ids[1]):
            short_line1 = original_short_line_data[point.parent_line_ids[0]]
            short_line2 = original_short_line_data[point.parent_line_ids[1]]
            if short_line1.z_order > short_line2.z_order:
                for road in complete_road_string_data:
                    if short_line1 in road.short_line_list:
                        road.hight_score += 1
                    if short_line2 in road.short_line_list:
                        road.hight_score -= 1
            else:
                for road in complete_road_string_data:
                    if short_line1 in road.short_line_list:
                        road.hight_score -= 1
                    if short_line2 in road.short_line_list:
                        road.hight_score += 1

    complete_road_string_data.sort(key=lambda r: r.hight_score)
    return complete_road_string_data

if __name__ == '__main__':
    main()
