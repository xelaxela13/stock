from django.core.management.base import BaseCommand
import configparser
import os


class Command(BaseCommand):
    help = 'Get environment variables from file and put they in environ'

    def add_arguments(self, parser):
        parser.add_argument('file', nargs='+', type=str)

    def handle(self, *args, **options):
        config = configparser.ConfigParser()
        try:
            for file in options['file']:
                config.read(file)
                for section in config.sections():
                    for key in config[section]:
                        os.environ.setdefault(key.upper(), config[section][key])
        except KeyError:
            pass
        except configparser.MissingSectionHeaderError:
            print('File contains no section headers')
