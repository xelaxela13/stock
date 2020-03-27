import configparser
from os import path
from django.conf import settings


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


def rel(*x):
    #  For example: rel('log', 'file.log') will to returned /var/www/stock/log/file.log
    return path.join(settings.BASE_DIR, *x)
