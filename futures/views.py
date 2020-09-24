from django.shortcuts import render,HttpResponse
from futures.models import *
from egg.models import DailyPriceQGAvg
import json
# Create your views here.

def get_daily_futures_price():
    result = {
        'date_list':[],
        'xianhuo_price_list':[],
        'qihuo_price_list':[]
    }
    try:
        # futures_date_list = []

        res = EggMainPrice.objects.values()
        for index in res:
            result['date_list'].append(index['date'].strftime('%Y-%m-%d'))
            result['qihuo_price_list'].append(index['eggFuturePrice'])
            result['xianhuo_price_list'].append(index['xianhuoPrice'])
        print(result['date_list'])
    except Exception as e:
        print('get_daily_futures_price',str(e))

    return result


def get_futures_price_datelist():
    try:
        futures_date_list = []
        res = EggMainPrice.objects.values()
        for index in res:
            futures_date_list.append(index['date'].strftime('%Y-%m-%d'))
        print(futures_date_list)
    except Exception as e:
        print('get_daily_futures_price',str(e))

    return futures_date_list


def get_xianhuo_price_by_futures(date_list):
    try:
        print(date_list)
        xianhuo_price_list = []
        for index in date_list:
            tmp_price = DailyPriceQGAvg.objects.values().filter(date=index,pricetype_id=1)[0]['daily_price']
            xianhuo_price_list.append(round(tmp_price,2)*1000)
    except Exception as e:
        print('get_xianhuo_price_by_futures',str(e))

    return xianhuo_price_list




def ajax_get_futures_info(request):
    if request.is_ajax():
        print('request.GET',request.GET)
        if request.method == 'GET' and 'futures_id' in request.GET.dict():
            price_dict = get_daily_futures_price()

            if len(price_dict['xianhuo_price_list']) == len(price_dict['qihuo_price_list']):
                jicha_list = list(map(lambda x, y: x - y, price_dict['qihuo_price_list'], price_dict['xianhuo_price_list']))
            content = {
                'date_list':price_dict['date_list'],
                'futures_price_list':price_dict['qihuo_price_list'],
                'xianhuo_price_list':price_dict['xianhuo_price_list'],
                'jicha':jicha_list
            }
            print('content',content)
            return HttpResponse(json.dumps(content), content_type='application/json')


def get_eggFutures_chicang_info(today,duo_kong_flag):
    ret_dict = {
        'company_name_list':[],
        'chicang_value_list':[],
        'fluctuate_list':[]
    }
    try:
        result = ChicangInfo.objects.values('futurescompany__companyName','chicang_value','fluctuate').filter(date=today,duo_kong_flag=duo_kong_flag)
        for index in result:
            ret_dict['company_name_list'].append(index['futurescompany__companyName'])
            ret_dict['chicang_value_list'].append(index['chicang_value'])
            ret_dict['fluctuate_list'].append(index['fluctuate'])
    except Exception as e:
        print(str(e))

    return ret_dict

