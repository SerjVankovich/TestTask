import subprocess
import sys

import requests


def get_new_checks(api_key):
    url = 'http://localhost:8000/new_checks/?api_key=' + api_key
    response = requests.get(url)
    status = response.status_code
    if status == 401:
        return response.json()['error'], None

    return None, response.json()['checks']


def get_check(api_key, check_id):
    url = 'http://localhost:8000/check/?api_key=' + api_key + '&check_id=' + str(check_id)
    response = requests.get(url)
    status = response.status_code
    if status in [400, 401]:
        return response.json()['error'], None

    return None, response.content


def print_new_checks(api_key):
    err, new_checks = get_new_checks(api_key)
    if err is not None:
        print('Ошибка:', err)
        return

    for check in new_checks:
        err, ch = get_check(api_key, check['id'])
        if err is not None:
            print('Произошла ошибка при печати чека', check['id'] + ':', err)
        else:
            lpr = subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
            lpr.stdin.write(ch)


a_key = sys.argv[1]
print_new_checks(a_key)
