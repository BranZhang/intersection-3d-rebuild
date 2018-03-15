'''
main process.
'''

import collections

from ortools.linear_solver import linear_solver_pb2, pywraplp

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
    touch_points = get_each_road_touch_points(
        complete_road_string_data, cross_points)

    # get END type point
    end_points = get_each_road_end_points(
        complete_road_string_data, touch_points)

    # check points
    insert_type_points_to_database(cross_points, touch_points, end_points)

    # get distance between two points
    roads_distance_map = calculate_roads_distance(complete_road_string_data)

    type_points_dict_by_road_id = dict_by_road_id(
        complete_road_string_data, cross_points, touch_points, end_points)

    # calculate each point's height.
    key_points_z_value = calculate(original_road_string_data, type_points_dict_by_road_id,
                                   roads_distance_map, cross_points, touch_points, end_points)

    # interpolate each complete road.

    # smooth each complete road in its z axis.
    smooth_z_axis(complete_road_string_data, key_points_z_value)

    # save road data with z value to database or file.

    # disconnect to database.
    dbmanager.disconnect_to_database()


def get_complete_road_string_list(original_road_string_data):
    '''
    return Road Class List,order by distance of road's start point to end point.
    '''
    result = []
    already_deal_roads_id_list = []

    for (road_id, single_string) in original_road_string_data.items():
        if road_id in already_deal_roads_id_list:
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
        print('bad deal.')

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

    for single_string in sorted(target_dict.items(), key=lambda x: 180 - x[1]):
        if single_string[1] < 90:
            return None
        else:
            return single_string[0]


def update_road_code_to_database(complete_road_string_data):

    road_code_dict = {}
    road_count = 0

    for road in complete_road_string_data:
        for single_string in road.short_line_list:
            if single_string.database_id in road_code_dict.keys():
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
    cross_point_list = collections.OrderedDict()

    for point in intersection_points:
        for line_id in intersection_points[point]:
            cross_point_list[(point, line_id)] = []

    for k in cross_point_list:
        for road in complete_road_string_data:
            if road.is_line_id_in_line_list(k[1]):
                cross_point_list[k].append(road.road_id)

    return cross_point_list


def get_each_road_touch_points(complete_road_string_data, cross_points):
    cross_points_list = []
    for point in cross_points:
        cross_points_list.append(point[0])

    touch_points = {}
    for road in complete_road_string_data:
        single_road_touch_point = dbmanager.query_main_road_touch_points(
            road.road_id)
        for point in single_road_touch_point:
            if point in cross_points_list:
                continue
            if point in touch_points.keys():
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
            if point.get_location() in touch_points.keys() and \
                    (road.road_id not in touch_points[point.get_location()]):
                touch_points[point.get_location()][1].append(str(road.road_id))
            elif point.get_location() in end_points.keys():
                end_points[point.get_location()][1].append(str(road.road_id))
            else:
                end_points[point.get_location()] = (
                    point.parent_line_id, [str(road.road_id)])

    return end_points


def insert_type_points_to_database(cross_points, touch_points, end_points):
    insert_list = []

    insert_data = ("(ST_GeomFromText('POINT({longitude} {latitude})', 3857), "
                   "ARRAY [{road_list}], ARRAY [{line_list}], '{point_type}')")

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


def calculate_roads_distance(complete_road_string_data):
    roads_distance_map = {}
    for road in complete_road_string_data:
        roads_distance_map.update(
            dbmanager.get_distance_of_a_road(road.road_id))

    return roads_distance_map


def dict_by_road_id(complete_road_string_data, cross_points, touch_points, end_points):
    type_points_dict_by_road_id = {}

    for road in complete_road_string_data:
        type_points_dict_by_road_id[road.road_id] = []

    for point in cross_points:
        for road_id in cross_points[point]:
            type_points_dict_by_road_id[road_id].append(
                ('cp', point, point[0]))

    for point in touch_points:
        for road_id in touch_points[point][1]:
            type_points_dict_by_road_id[road_id].append(('tp', point))

    for point in end_points:
        for road_id in end_points[point][1]:
            type_points_dict_by_road_id[road_id].append(('ep', point))

    return type_points_dict_by_road_id


def calculate(original_road_string_data, type_points_dict_by_road_id, roads_distance_map, cross_points, touch_points, end_points):
    '''
    max slope: 6%.
    each floor:3 metre
    '''
    elevation_difference = 3
    slope = 0.06

    solver = pywraplp.Solver(
        'road_3D', pywraplp.Solver.GLOP_LINEAR_PROGRAMMING)
    objective = solver.Objective()
    objective.SetMinimization()

    cp_list = []  # cross_points
    tp_list = []  # touch_points
    ep_list = []  # end_points

    for _n in range(0, len(cross_points)):
        cp_list.append(solver.NumVar(0, solver.infinity(),
                                     'cp_{id:02d}'.format(id=_n)))
        objective.SetCoefficient(cp_list[_n], 1)

    for _n in range(0, len(touch_points)):
        tp_list.append(solver.NumVar(0, solver.infinity(),
                                     'tp_{id:02d}'.format(id=_n)))
        objective.SetCoefficient(tp_list[_n], 1)

    for _n in range(0, len(end_points)):
        ep_list.append(solver.NumVar(0, solver.infinity(),
                                     'ep_{id:02d}'.format(id=_n)))
        objective.SetCoefficient(ep_list[_n], 1)

    # Constraint series 1: P(high) - P(low) >= 3
    for _n in range(0, len(cross_points), 2):
        if original_road_string_data[list(cross_points.items())[_n][0][1]].z_order \
                > original_road_string_data[list(cross_points.items())[_n + 1][0][1]].z_order:
            param = 1
        else:
            param = -1
        constraint1 = solver.Constraint(
            elevation_difference, solver.infinity())
        constraint1.SetCoefficient(cp_list[_n], param)
        constraint1.SetCoefficient(cp_list[_n + 1], -param)

    # Constraint series 2: Is bridge?
    for _n in range(0, len(cross_points)):
        if original_road_string_data[list(cross_points.items())[_n][0][1]].bridge:
            constraint2 = solver.Constraint(
                elevation_difference, solver.infinity())
            constraint2.SetCoefficient(cp_list[_n], 1)

    for _n in range(0, len(touch_points)):
        if original_road_string_data[int(list(touch_points.items())[_n][1][0][0])].bridge:
            constraint2 = solver.Constraint(
                elevation_difference, solver.infinity())
            constraint2.SetCoefficient(tp_list[_n], 1)

    for _n in range(0, len(end_points)):
        if original_road_string_data[list(end_points.items())[_n][1][0]].bridge:
            constraint2 = solver.Constraint(
                elevation_difference, solver.infinity())
            constraint2.SetCoefficient(ep_list[_n], 1)

    # Constraint series 3: ABS(P(i) - P(i+1)) <= slope * length
    for road_id in type_points_dict_by_road_id:
        point_couples = [((m[-1], n[-1]), m, n) for m in type_points_dict_by_road_id[road_id]
                         for n in type_points_dict_by_road_id[road_id]]
        for point_couple in point_couples:
            if point_couple[0] in roads_distance_map:
                if point_couple[1][0] == 'cp':
                    m = cp_list[list(cross_points.keys()).index(
                        point_couple[1][1])]
                elif point_couple[1][0] == 'tp':
                    m = tp_list[list(touch_points.keys()).index(
                        point_couple[1][1])]
                elif point_couple[1][0] == 'ep':
                    m = ep_list[list(end_points.keys()).index(
                        point_couple[1][1])]

                if point_couple[2][0] == 'cp':
                    n = cp_list[list(cross_points.keys()).index(
                        point_couple[2][1])]
                elif point_couple[2][0] == 'tp':
                    n = tp_list[list(touch_points.keys()).index(
                        point_couple[2][1])]
                elif point_couple[2][0] == 'ep':
                    n = ep_list[list(end_points.keys()).index(
                        point_couple[2][1])]

                distance = roads_distance_map[point_couple[0]]
                constraint3 = solver.Constraint(-distance *
                                                slope, distance * slope)
                constraint3.SetCoefficient(m, 1)
                constraint3.SetCoefficient(n, -1)

    solver.Solve()

    solver_answer = {}
    for _n in range(len(cross_points)):
        for road_id in list(cross_points.items())[_n][1]:
            if road_id not in solver_answer:
                solver_answer[road_id] = []
            solver_answer[road_id].append(
                (list(cross_points.items())[_n][0][0], cp_list[_n].solution_value()))

    for _n in range(len(touch_points)):
        for road_id in list(touch_points.items())[_n][1][1]:
            if road_id not in solver_answer:
                solver_answer[road_id] = []
            solver_answer[road_id].append(
                (list(touch_points.items())[_n][0], tp_list[_n].solution_value()))

    for _n in range(len(end_points)):
        for road_id in list(end_points.items())[_n][1][1]:
            if road_id not in solver_answer:
                solver_answer[road_id] = []
            solver_answer[road_id].append(
                (list(end_points.items())[_n][0], ep_list[_n].solution_value()))

    # 将线性规划得到的带高度的点与 short_line （也就是 original_road_string_data）融合起来，
    # 融合需要借助postgis。做高度上的插值，插值后输出到kml。
    return solver_answer


def smooth_z_axis(complete_road_string_data, key_points_z_value):
    for road in complete_road_string_data:
        if road.road_id not in key_points_z_value:
            continue
        points_z_value = key_points_z_value[road.road_id]
        road.smooth_z_axis(dbmanager.get_merged_road(road.road_id), points_z_value)


if __name__ == '__main__':
    main()
