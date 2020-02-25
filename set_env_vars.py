import random
import string
import os.path


def run():
    config = {}
    while True:
        try:
            config['common'] = {
                'COMPOSE_PROJECT_NAME': 'stock',
                'COMPOSE_FILE': 'docker-compose.yml:docker-compose.dev.yml',
                'PROJECT_ROOT': '/home/user/stock',
                'IMAGE': 'xelaxela13/stock:latest',
                'ADMIN_EMAIL': 'dummy@mail.com',
            }
            config['SETTINGS'] = {
                'SECRET_KEY': random_string(),
                'ALLOWED_HOSTS': '*',
                'DEBUG': True,
                'GMAIL_PASSWORD': '',
                'GMAIL_USER': '',
                'MEMCACHED_HOST': 'memcached',
                'MEMCACHED_PORT': '11211'

            }
            config['DB'] = {
                'name': 'postgres',
                'USER': 'postgres',
                'HOST': 'db',
                'PORT': '5432'
            }
            config['UWSGI'] = {
                'UWSGI_PORT': '8100',
                'UWSGI_PORT_RANGE': '8100-8101',
            }
            break
        except ValueError:
            continue
    file = '.env'
    if os.path.isfile(file):
        print('File {} already exist, cannot rewrite it. '.format(file))
        return
    try:
        with open(file, 'w') as f:

            for title, conf in config.items():
                f.writelines('[' + str(title).upper() + ']\n')
                for key, value in conf.items():
                    f.writelines('\t' + str(key).upper() + '=' + str(value) + '\n')
            print('Config file was created success')
            return
    except Exception as err:
        if os.path.isfile(file):
            os.remove(file)
        print(err)
        return


def random_string():
    return "".join(
        [random.SystemRandom().choice("{}{}{}".format(string.ascii_letters, string.digits, string.punctuation))
         for _ in range(50)])


if __name__ == '__main__':
    run()
