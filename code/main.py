'''
main process.
'''
import config
import dbmanager
import Object.gistools as gistools
from Object.road import Road
from Object.touch_point import TouchPoint


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

    # get CROSS type point
    cross_points = get_each_road_cross_points(complete_road_string_data)

    # get TOUCH type point
    touch_points = get_each_road_touch_points(complete_road_string_data)

    # get END type point
    end_points = get_each_road_end_points(
        complete_road_string_data, touch_points)

    # check points
    insert_type_points_to_database(cross_points, touch_points, end_points)

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


def get_each_road_cross_points(complete_road_string_data):
    intersection_points = dbmanager.query_main_road_intersection_points()
    cross_point_list = {}

    for point in intersection_points:
        for line_id in intersection_points[point]:
            cross_point_list[(point, line_id)] = []

    for k in cross_point_list:
        for road in complete_road_string_data:
            if road.is_line_id_in_line_list(k[1]):
                cross_point_list[k].append(road.road_id)

    return cross_point_list


def get_each_road_touch_points(complete_road_string_data):
    touch_points = {}
    for road in complete_road_string_data:
        single_road_touch_point = dbmanager.query_main_road_touch_points(
            road.road_id)
        for point in single_road_touch_point:
            if touch_points.has_key(point):
                touch_points[point][1].append(str(road.road_id))
            else:
                touch_points[point] = (
                    single_road_touch_point[point], [str(road.road_id)])

    # touch_points_list = []

    # for (location, road_id_list) in touch_points:
    #     touch_points_list.append(TouchPoint(location[0], location[1], road_id_list))

    return touch_points


def get_each_road_end_points(complete_road_string_data, touch_points):
    end_points = {}
    for road in complete_road_string_data:
        single_road_end_points = dbmanager.query_main_road_end_points(
            road.road_id)

        for point in single_road_end_points:
            if touch_points.has_key(point.get_location()) and \
                    (road.road_id not in touch_points[point.get_location()]):
                touch_points[point.get_location()][1].append(str(road.road_id))
            else:
                end_points[point.get_location()] = (
                    point.parent_line_id, [str(road.road_id)])

    return end_points


def insert_type_points_to_database(cross_points, touch_points, end_points):
    insert_list = []

    insert_data = "(ST_GeomFromText('POINT({longitude} {latitude})', 3857), ARRAY [{road_list}], ARRAY [{line_list}], '{point_type}')"

    for (location, line_id) in cross_points:
        road_id_list = cross_points[(location, line_id)]
        insert_list.append(insert_data.format(
            longitude=location[0], latitude=location[1], point_type='cross',
            road_list=turn_list_to_sql_array(road_id_list),
            line_list=turn_list_to_sql_array(line_id)))

    for (lon, lat) in touch_points:
        line_id_list = touch_points[(lon, lat)][0]
        road_id_list = touch_points[(lon, lat)][1]
        insert_list.append(insert_data.format(
            longitude=lon, latitude=lat, point_type='touch',
            road_list=turn_list_to_sql_array(road_id_list),
            line_list=turn_list_to_sql_array(line_id_list)))

    for (lon, lat) in end_points:
        line_id_list = end_points[(lon, lat)][0]
        road_id_list = end_points[(lon, lat)][1]
        insert_list.append(insert_data.format(
            longitude=lon, latitude=lat, point_type='end',
            road_list=turn_list_to_sql_array(road_id_list),
            line_list=turn_list_to_sql_array(line_id_list)))

    dbmanager.insert_each_point_code_list(','.join(insert_list))


def turn_list_to_sql_array(_list):
    if isinstance(_list, list):
        return "'" + "','".join(_list) + "'"
    else:
        return "'" + str(_list) + "'"


if __name__ == '__main__':
    main()
