import config
import dbmanager


def main():
    config.init_config()
    dbmanager.connect_to_database()
    # dbmanager.create_temp_roads_table()
    # dbmanager.insert_target_data_to_temp_roads_table()

    road_data = dbmanager.query_temp_roads()

    dbmanager.disconnect_to_database()

if __name__ == '__main__':
    main()