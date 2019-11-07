import json

from django.http import HttpResponse

ok_response = HttpResponse(json.dumps({
    "ok": "чеки успешно созданы"
}), content_type='application/json')

checks_made = HttpResponse(json.dumps({
    "error": "Для данного заказа уже созданы чеки"
}), content_type='application/json', status=400)

no_printer = HttpResponse(json.dumps({
    "error": "для данной точки не настроено ни одного принтера"
}), content_type='application/json', status=400)

authorization_error_response = HttpResponse(json.dumps({
    "error": "ошибка авторизации"
}), content_type='application/json', status=401)

check_doesnt_exists = HttpResponse(json.dumps({
    "error": "Данного чека не существует"
}), content_type='application/json', status=401)

check_is_not_rendered = HttpResponse(json.dumps({
    "error": "Для данного чека не сгенерирован PDF-файл"
}), content_type='application/json', status=401)

