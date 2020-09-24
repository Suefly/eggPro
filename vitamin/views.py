#-*- coding: utf-8 -*-

from django.shortcuts import render,HttpResponse
from vitamin.models import *
import json
# Create your views here.

def get_vitamin_weekly_price(vi_type_id):
    week_price_result = {
        'week_list':[],
        'data_list':[]
    }
    try:
        res = VitaminWeeklyPrice.objects.values().filter(vitamintype_id=vi_type_id)
        for index in res:
            week_price_result['week_list'].append(str(index['year'])+'年第'+str(index['weekNum'])+'周')
            week_price_result['data_list'].append(round(index['weeklyprice']))
    except Exception as e:
        print('get_vitamin_weekly_price -->',str(e))
    return week_price_result


def ajax_get_vitamin_weekly_price(request):
    if request.is_ajax():
        if request.method == 'GET' and 'vitamin_type_id' in request.GET.dict():
            vitamin_type_id = request.GET.get('vitamin_type_id')
            result = get_vitamin_weekly_price(vitamin_type_id)
            content = {
                'week_list':result['week_list'],
                'data_list':result['data_list']
            }
            return HttpResponse(json.dumps(content), content_type='application/json')