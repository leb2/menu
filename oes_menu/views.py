from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings
import datetime
import json


def menu(request):
    path = os.path.join(settings.BASE_DIR, 'oes_menu/menu/menu_json.json')
    with open(path, 'r') as file:
        menu = json.loads(file.read())[0]

    day = datetime.date.today().isoweekday()
    days_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    return render(request, 'oes_menu/menu.html', {
        'menu': menu,
        'day': day,
        'days_list': days_list
    })


def menu_json(request):
    with open(os.path.join(settings.BASE_DIR, 'oes_menu/menu/menu_json.json'), 'r') as file:
        menu = str(json.loads(file.read())[0]['days'])

    return HttpResponse(json.dumps(menu), content_type='application/json')
