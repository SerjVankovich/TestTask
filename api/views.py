import os

from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Printer, Check
from .responses import ok_response, checks_made, no_printer, authorization_error_response, check_doesnt_exists, check_is_not_rendered
from .jobs import make_pdf
import json
import django_rq
import base64

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Create your views here.
@csrf_exempt
def create_check(request):
    queue = django_rq.get_queue('default', autocommit=True, is_async=True, default_timeout=360)
    if request.method == 'POST':

        body = json.loads(request.body)
        printers = Printer.objects.filter(point_id=body['point_id'])
        checks = Check.objects.filter(order__id=body['id'])
        if len(checks) > 0:
            return checks_made

        if len(printers) == 0:
            return no_printer
        else:
            for printer in printers:
                check_types = printer.check_type.split('|')
                for check_type in check_types:
                    printer.check_set.create(order=body, status="new", type=check_type)
            order_id = str(body['id'])
            content = base64.b64encode(render(request, 'api/check_template.html', {'body': body}).content).decode(
                'utf-8')
            content2 = base64.b64encode(render(request, 'api/kitchen_template.html', {'body': body}).content).decode(
                'utf-8')

            queue.enqueue(make_pdf, content=content, order_id=order_id, type_check='client')
            queue.enqueue(make_pdf, content=content2, order_id=order_id, type_check='kitchen')

    return ok_response


def new_checks(request):
    api_key = request.GET.get('api_key')
    if api_key is None:
        return authorization_error_response

    try:
        printer = Printer.objects.get(api_key=api_key)
    except Printer.DoesNotExist:
        return authorization_error_response

    checks = printer.check_set.filter(status='rendered')
    ids = [{'id': ch.id} for ch in checks]
    data = json.dumps({'checks': ids})
    return HttpResponse(data, content_type='application/json')


def check(request):
    api_key = request.GET.get('api_key')
    check_id = request.GET.get('check_id')

    if api_key is None:
        return authorization_error_response

    try:
        Printer.objects.get(api_key=api_key)
    except Printer.DoesNotExist:
        return authorization_error_response

    if check_id is None:
        return check_doesnt_exists

    try:
        ch = Check.objects.get(id=int(check_id))
    except Check.DoesNotExist:
        return check_doesnt_exists

    if ch.status == 'new':
        return check_is_not_rendered

    file_path = os.path.join(BASE_DIR, 'media/pdf', ch.pdf_file.url)

    response = HttpResponse(ch.pdf_file, content_type='application/pdf')
    response['Content-Description'] = 'attachment; filename=' + file_path
    ch.status = 'printed'
    ch.save()

    return response
