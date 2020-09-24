from django.shortcuts import render,HttpResponse
from doupo.models import *
import json
# Create your views here.

def get_daily_doupo_price(doupolevel_id):
    daily_price_result = {
        'date_list': [],
        'doupo_data_list': [],
    }
    try:
        res = DoupoDailyPriceQuanguoAvg.objects.values().filter(doupolevel_id=doupolevel_id,daily_price__gt=0)
        for index in res:
            daily_price_result['date_list'].append(index['date'].strftime('%Y-%m-%d'))
            daily_price_result['doupo_data_list'].append(round(index['daily_price']))
    except Exception as e:
        print('get_daily_doupo_price -->', str(e))
    return daily_price_result


def ajax_daily_doupo_price(request):
    if request.is_ajax():
        print('request.GET',request.GET)
        if request.method == 'GET' and 'doupolevel_id' in request.GET.dict():
            doupolevel_id = request.GET.get('doupolevel_id')
            result_pt = get_daily_doupo_price(1)
            result_gd = get_daily_doupo_price(2)
            content = {
                'date_list':result_pt['date_list'],
                'pt_doupo_data_list':result_pt['doupo_data_list'],
                'gd_doupo_data_list':result_gd['doupo_data_list']
            }
            print('content',content)
            return HttpResponse(json.dumps(content), content_type='application/json')


