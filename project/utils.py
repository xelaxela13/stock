import configparser


def get_db_settings(database_dict, file):
    try:
        data = database_dict['default']
    except KeyError:
        return
    config = configparser.ConfigParser()
    try:
        config.read(file)
        for key in config['DB']:
            data[key.upper().strip()] = config['DB'][key].strip()
    except KeyError:
        pass
    except configparser.MissingSectionHeaderError:
        return
