from celery import task
import requests
from django.conf import settings


@task
def get_location(language_code, ip_address):
    response = requests.get('http://api.ipstack.com/{}'.format(ip_address),
                            timeout=2,
                            verify=False,
                            params={'access_key': settings.IPSTACK_ACCESS_KEY,
                                    'language': language_code}
                            )

    geodata = response.json()
    try:
        city = geodata['city']
    except KeyError:
        return ''
    return city
