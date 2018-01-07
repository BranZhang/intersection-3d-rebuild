DELETE FROM target_points_{timesign};

INSERT INTO target_points_{timesign} (location, road_id_list, line_id_list, type)
VALUES {insert_data};