from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,HttpResponse
from yumi.models import *
import json
# Create your views here.

def get_daily_yumi_price(yumi_type_id):
    daily_price_result = {
        'date_list': [],
        'yumi_data_list': [],
    }
    try:
        res = YumiDailyPriceQuanguoAvg.objects.values().filter(yumipricetype_id=yumi_type_id,daily_price__gt=0)
        for index in res:
            daily_price_result['date_list'].append(index['date'].strftime('%Y-%m-%d'))
            daily_price_result['yumi_data_list'].append(round(index['daily_price']))
    except Exception as e:
        print('get_daily_yumi_price -->', str(e))
    return daily_price_result


def ajax_daily_yumi_price(request):
    if request.is_ajax():
        print('request.GET',request.GET)
        if request.method == 'GET' and 'yumi_type_id' in request.GET.dict():
            yumi_type_id = request.GET.get('yumi_type_id')
            result_yumi = get_daily_yumi_price(3)
            content = {
                'date_list':result_yumi['date_list'],
                'yumi_data_list':result_yumi['yumi_data_list'],
            }
            print('content',content)
            return HttpResponse(json.dumps(content), content_type='application/json')


