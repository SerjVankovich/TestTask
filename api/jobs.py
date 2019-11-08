import json
import os

import requests

from api.models import Check

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def make_pdf(content, order_id, type_check):
    url = 'http://localhost:32768'

    data = {
        'contents': content
    }
    header = {
        'Content-Type': 'application/json'
    }

    response = requests.post(url, data=json.dumps(data), headers=header)

    with open(os.path.join(BASE_DIR, 'media/pdf/') + order_id + '_' + type_check + '.pdf', 'wb') as f:
        f.write(response.content)

    checks = Check.objects.filter(order__id=int(order_id))
    for ch in checks:
        ch.status = 'rendered'
        ch.save()