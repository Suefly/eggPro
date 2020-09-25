from django.shortcuts import render,HttpResponse
from egg.price.dailyEggPrice import *
from futures.views import *
from basic.models import *
from django.contrib import messages
from django.http import JsonResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from geetest import GeetestLib
from django.contrib.auth.decorators import login_required
import json
from django.db.models import Q
# import copy
import datetime
import time
# Create your views here.
# 请在官网申请ID使用，示例ID不可使用
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"

def acc_login(request):
    if request.method == "POST":
        print(request.POST)
        res = {"status": 0, "msg": ""}
        username = request.POST.get("username")
        password = request.POST.get("pwd")
        # 获取极验 滑动验证码相关的参数
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        print("####################", result)
        if result:
            user = authenticate(username=username, password=password)
            print('user',user)
            if user:
                login(request, user)
                res["msg"] = "/index/"
            else:
                res["status"] =1
                res["msg"] = "认证失败,请检查用户名及密码是否正确"
        else:
            res["status"] = 1
            res["msg"] = "验证码错误"
        print("**************", res)
        return JsonResponse(res)
    return render(request, 'login.html')

def index(request):
    return render(request,'index.html')

def qihuo_zijin_info(request):

    today = '2020-09-09'
    DUO_FLAG = 1
    KONG_FlAG = 2
    duo_list = get_eggFutures_chicang_info(today, DUO_FLAG)
    kong_list = get_eggFutures_chicang_info(today,KONG_FlAG)

    #### 价格预测
    today = datetime.date.today().strftime('%Y-%m-%d')
    res_week = WeekDateStandard.objects.values().filter(startDate__lte=today, endDate__gte=today)[0]
    year = res_week['Year']
    week = res_week['WeekNum']
    # week = 20
    exist_date_list = []
    exist_data_list = []
    exist_date = WeeklyPriceQGAvg.objects.values().filter(pricetype_id=1, weekly_price__gt=0).filter(
        Q(year__lt=year) | Q(year=year, weekNum__lte=week))
    for index in exist_date:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        exist_date_list.append(date_index)
        exist_data_list.append(round(index['weekly_price'], 2))

    date_list = []
    data_list = []
    res = WeeklyPriceQGAvg.objects.values().filter(pricetype_id=1, weekly_price__gt=0)
    for index in res:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        data_index = round(index['weekly_price'], 2)
        date_list.append(date_index)
        data_list.append(data_index)
    yuce_price_list = []
    yuce_price = data_list[len(exist_date) - 1:]

    for i in range(len(res) - len(exist_date)):
        exist_data_list.append('-')

    for i in range(len(exist_date) - 1):
        yuce_price_list.append('-')

    yuce_price_list.extend(yuce_price)

    price_dict = get_daily_futures_price()

    if len(price_dict['xianhuo_price_list']) == len(price_dict['qihuo_price_list']):
        print('##'*100)
        jicha_list = list(map(lambda x, y: x - y, price_dict['qihuo_price_list'], price_dict['xianhuo_price_list']))
    print('jicha_list',jicha_list)
    content = {
        'duo_company_list':duo_list['company_name_list'],
        'duo_chicang_value_list':duo_list['chicang_value_list'],
        'duo_fluctuate_list':duo_list['fluctuate_list'],
        'kong_company_list': kong_list['company_name_list'],
        'kong_chicang_value_list': kong_list['chicang_value_list'],
        'kong_fluctuate_list': kong_list['fluctuate_list'],
        'data_list': data_list,
        'date_list': date_list,
        'exist_date_list': exist_date_list,
        'exist_data_list': exist_data_list,
        'yuce_price_list': yuce_price_list,
        'jicha_date_list': price_dict['date_list'],
        'jicha_list':jicha_list
    }
    return render(request,'welcome1.html',content)

def welcome(request):

    #### 价格预测
    today = datetime.date.today().strftime('%Y-%m-%d')
    res_week = WeekDateStandard.objects.values().filter(startDate__lte=today, endDate__gte=today)[0]
    year = res_week['Year']
    week = res_week['WeekNum']
    # week = 20
    exist_date_list = []
    exist_data_list = []
    chanliang_exist_data_list = []
    exist_date = WeeklyPriceQGAvg.objects.values().filter(pricetype_id=1, weekly_price__gt=0).filter(
        Q(year__lt=year) | Q(year=year, weekNum__lte=week))

    chanliang_exist_date = WeeklyCunchulanOutput.objects.values().filter(chanliang_type = 9).filter(
        Q(year__lt=year) | Q(year=year, weekNum__lte=week))
    for index in exist_date:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        exist_date_list.append(date_index)
        exist_data_list.append(round(index['weekly_price'], 2))

    for index in chanliang_exist_date:
        chanliang_exist_data_list.append(round(index['chanliang_value']))

    date_list = []
    data_list = []
    res = WeeklyPriceQGAvg.objects.values().filter(pricetype_id=1, weekly_price__gt=0)
    for index in res:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        data_index = round(index['weekly_price'], 2)
        date_list.append(date_index)
        data_list.append(data_index)
    yuce_price_list = []
    yuce_price = data_list[len(exist_date) - 1:]


    for i in range(len(res) - len(exist_date)):
        exist_data_list.append('-')

    for i in range(len(exist_date) - 1):
        yuce_price_list.append('-')

    yuce_price_list.extend(yuce_price)

    chanliang_data_list = []
    res = WeeklyCunchulanOutput.objects.values().filter(chanliang_type=9)
    for index in res:
        data_index = index['chanliang_value']
        chanliang_data_list.append(data_index)

    price_dict = get_daily_futures_price()
    print('price_dict',price_dict)
    if len(price_dict['xianhuo_price_list']) == len(price_dict['qihuo_price_list']):
        jicha_list = list(
            map(lambda x, y: x - y, price_dict['qihuo_price_list'], price_dict['xianhuo_price_list']))

    output_type_id_yucheng = 6
    output_type_id_chandan = 7
    yucheng_date_list, yucheng_data_list = get_week_cunchulan_output(output_type_id_yucheng)
    chandan_date_list, chandan_data_list = get_week_cunchulan_output(output_type_id_chandan)

    output_type_id_yucheng_fmd = 2
    output_type_id_chandan_fmd = 3
    yucheng_date_list_fmd, yucheng_data_list_fmd = get_week_cunchulan_output(output_type_id_yucheng_fmd)
    chandan_date_list_fmd, chandan_data_list_fmd = get_week_cunchulan_output(output_type_id_chandan_fmd)

    content = {
        'data_list': data_list,
        'date_list': date_list,
        'exist_date_list': exist_date_list,
        'exist_data_list': exist_data_list,
        'yuce_price_list': yuce_price_list,

        'jicha_date_list': price_dict['date_list'],
        'jicha_list':jicha_list,
        'futures_price_list': price_dict['qihuo_price_list'],
        'xianhuo_price_list': price_dict['xianhuo_price_list'],

        'chanliang_data_list':chanliang_data_list,
        'chanliang_exist_data_list':chanliang_exist_data_list,

        'yucheng_date_list': yucheng_date_list,
        'yucheng_data_list': yucheng_data_list,
        'chandan_data_list': chandan_data_list,

        'yucheng_date_list_fmd': yucheng_date_list_fmd,
        'yucheng_data_list_fmd': yucheng_data_list_fmd,
        'chandan_data_list_fmd': chandan_data_list_fmd
    }
    return render(request,'welcome.html',content)

def daily_egg_price(request):
    current_day = get_lastday_egg_daily_table()
    egg_dailyprice_res = get_egg_quanguo_dailyprice(1)
    # egg_dailyprice_province_map = gen_egg_province_dprice_map(current_day)
    # egg_dailyprice_province_map.sort(key=lambda k: (k.get('value', 0)))
    # egg_max_price = egg_dailyprice_province_map[-1:][0]["value"]
    # egg_min_price = egg_dailyprice_province_map[0]["value"]
    chanxiao_compare = get_egg_chanxiao_dailyprice()
    content = {
        'current_day': json.dumps(current_day),
        'egg_date_list': egg_dailyprice_res[0],
        # 'egg_max_price': egg_max_price,
        # 'egg_min_price': egg_min_price,
        'egg_quanguo_avg_daily_price': egg_dailyprice_res[1],
        # 'egg_dailyprice_province_map': egg_dailyprice_province_map,
        'chanxiao_compare': json.dumps(chanxiao_compare)
    }
    return render(request, 'daily_egg_price.html', content)


def ajax_select_daily_price(request):
    print('ajax select daily price ~~~')
    pig_type_id = int(request.GET['pig_type_id'])
    current_day = get_lastday_egg_daily_table()
    egg_dailyprice_res = get_egg_quanguo_dailyprice(pig_type_id)
    print('egg_dailyprice_res',egg_dailyprice_res)
    # chanxiao_compare = get_egg_chanxiao_dailyprice()
    content = {
        'current_day': json.dumps(current_day),
        'egg_date_list': egg_dailyprice_res[0],
        'egg_quanguo_avg_daily_price': egg_dailyprice_res[1],
        # 'chanxiao_compare': json.dumps(chanxiao_compare)
    }
    return HttpResponse(json.dumps(content), content_type='application/json')


def ajax_egg_daily_price(request):

    if request.is_ajax():
        if request.method == 'GET' and 'province_list' in request.GET.dict():
            print('request.GET',request.GET)
            province_list = request.GET['province_list']
            print('@@@@@',province_list,type(province_list))
            province_id_list = province_list.replace('"','').split(',')
            print('province_id_list',province_id_list)
            ajax_date,ajax_series,province_name_list = gen_ajax_province_price_format(province_id_list)
            print('ajax_date',ajax_date)
            print('ajax_series',ajax_series)
            content = {
                'egg_province_date_list':ajax_date,
                'egg_province_daily_price':ajax_series,
                'province_name_list':province_name_list
            }
            return HttpResponse(json.dumps(content), content_type='application/json')


def weekly_egg_price(request):
    return render(request,'weekly_egg_price.html')


def monthly_egg_price(request):
    return render(request,'monthly_egg_price.html')

def weekly_egg_output(request):
    date_list = []
    data_list = []
    res = WeeklyCunchulanOutput.objects.values().filter(chanliang_type=2)
    for index in res:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        data_index = index['chanliang_value']
        date_list.append(date_index)
        data_list.append(data_index)
    content = {
        'data_list':data_list,
        'date_list':date_list
    }
    print(data_list,date_list)
    return render(request,'weekly_egg_output.html',content)


def ajax_weekly_egg_output(request):
    if 'output_type_id_yucheng' in request.GET.dict():
        output_type_id_yucheng = int(request.GET['output_type_id_yucheng'])
        output_type_id_chandan = int(request.GET['output_type_id_chandan'])
        yucheng_date_list, yucheng_data_list = get_week_cunchulan_output(output_type_id_yucheng)
        date_list, chandan_data_list = get_week_cunchulan_output(output_type_id_chandan)

        content = {
            'date_list': date_list,
            'yucheng_data_list': yucheng_data_list,
            'chandan_data_list':chandan_data_list
        }
        return HttpResponse(json.dumps(content), content_type='application/json')
    elif 'output_type_id' in request.GET.dict():
        print(request.GET.dict())
        output_type_id = int(request.GET['output_type_id'])
        date_list, data_list = get_week_cunchulan_output(output_type_id)
        content = {
            'date_list': date_list,
            'data_list': data_list,
        }
        return HttpResponse(json.dumps(content), content_type='application/json')



def monthly_egg_output(request):
    date_list = []
    data_list = []
    res = WeeklyCunchulanOutput.objects.values().filter(chanliang_type=2)
    for index in res:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        data_index = index['chanliang_value']
        date_list.append(date_index)
        data_list.append(data_index)
    content = {
        'data_list': data_list,
        'date_list': date_list
    }
    print(data_list, date_list)
    return render(request, 'monthly_egg_output.html', content)

def yearly_egg_output(request):
    return render(request,'yearly_egg_output.html')

def weekly_egg_cost(request):
    return render(request,'weekly_egg_cost.html')

def monthly_egg_cost(request):
    return render(request,'monthly_egg_cost.html')

def weekly_egg_profit(request):
    week_list,profit_data_list = get_weekly_profit_quanguo_info()
    content = {
        'week_list':week_list,
        'profit_data_list':profit_data_list
    }
    print(content)
    return render(request,'weekly_egg_profit.html',content)

def monthly_egg_profit(request):
    month_list, profit_data_list = get_monthly_profit_quanguo_info()
    content = {
        'month_list': month_list,
        'profit_data_list': profit_data_list
    }
    print(content)
    return render(request,'monthly_egg_profit.html',content)


def qihuo_zhuli(request):

    price_dict = get_daily_futures_price()

    if len(price_dict['xianhuo_price_list']) == len(price_dict['qihuo_price_list']):
        jicha_list = list(
            map(lambda x, y: x - y, price_dict['qihuo_price_list'], price_dict['xianhuo_price_list']))
    content = {
        'date_list': price_dict['date_list'],
        'futures_price_list': price_dict['qihuo_price_list'],
        'xianhuo_price_list': price_dict['xianhuo_price_list'],
        'jicha': jicha_list
    }
    print('content', content)
    return render(request,'qihuo_zhuli.html',content)

def yuce_egg_chanliang(request):
    today = datetime.date.today().strftime('%Y-%m-%d')
    res_week = WeekDateStandard.objects.values().filter(startDate__lte=today,endDate__gte=today)[0]
    year = res_week['Year']
    week = res_week['WeekNum']

    exist_date_list = []
    exist_date = WeeklyCunchulanOutput.objects.values().filter(chanliang_type=9).filter(Q(year__lt=year) | Q(year=year,weekNum__lt=week))
    for index in exist_date:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        exist_date_list.append(date_index)
    date_list = []
    data_list = []
    res = WeeklyCunchulanOutput.objects.values().filter(chanliang_type=9)
    for index in res:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        data_index = index['chanliang_value']
        date_list.append(date_index)
        data_list.append(data_index)
    content = {
        'data_list': data_list,
        'date_list': date_list,
        'exist_date_list':exist_date_list
    }
    return render(request,'yuce_egg_chanliang.html',content)

def yuce_egg_price(request):
    today = datetime.date.today().strftime('%Y-%m-%d')
    res_week = WeekDateStandard.objects.values().filter(startDate__lte=today,endDate__gte=today)[0]
    year = res_week['Year']
    week = res_week['WeekNum']
    # week = 20
    exist_date_list = []
    exist_data_list = []
    exist_date = WeeklyPriceQGAvg.objects.values().filter(pricetype_id=1,weekly_price__gt=0).filter(Q(year__lt=year) | Q(year=year,weekNum__lte=week))
    for index in exist_date:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        exist_date_list.append(date_index)
        exist_data_list.append(round(index['weekly_price'],2))

    date_list = []
    data_list = []
    res = WeeklyPriceQGAvg.objects.values().filter(pricetype_id=1,weekly_price__gt=0)
    for index in res:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        data_index = round(index['weekly_price'],2)
        date_list.append(date_index)
        data_list.append(data_index)
    yuce_price_list = []
    yuce_price = data_list[len(exist_date)-1:]

    for i in range(len(res)-len(exist_date)):
        exist_data_list.append('-')

    for i in range(len(exist_date)-1):
        yuce_price_list.append('-')

    yuce_price_list.extend(yuce_price)

    content = {
        'data_list': data_list,
        'date_list': date_list,
        'exist_date_list':exist_date_list,
        'exist_data_list':exist_data_list,
        'yuce_price_list':yuce_price_list
    }
    print(len(date_list),len(exist_date_list))
    return render(request,'yuce_egg_price.html',content)

def yuce_shangpindai_chuji_chanliang(request):
    today = datetime.date.today().strftime('%Y-%m-%d')
    res_week = WeekDateStandard.objects.values().filter(startDate__lte=today, endDate__gte=today)[0]
    year = res_week['Year']
    week = res_week['WeekNum']
    # week = 10
    exist_date_list = []
    exist_date = WeeklyCunchulanOutput.objects.values().filter(chanliang_type=5).filter(
        Q(year__lt=year) | Q(year=year, weekNum__lt=week))
    for index in exist_date:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        exist_date_list.append(date_index)
    date_list = []
    data_list = []
    res = WeeklyCunchulanOutput.objects.values().filter(chanliang_type=5)
    for index in res:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        data_index = index['chanliang_value']
        date_list.append(date_index)
        data_list.append(data_index)
    content = {
        'data_list': data_list,
        'date_list': date_list,
        'exist_date_list': exist_date_list
    }
    return render(request,'yuce_shangpindai_chuji_chanliang.html',content)

def yuce_taoji_shuliang(request):
    today = datetime.date.today().strftime('%Y-%m-%d')
    res_week = WeekDateStandard.objects.values().filter(startDate__lte=today, endDate__gte=today)[0]
    year = res_week['Year']
    week = res_week['WeekNum']
    # week = 10
    exist_date_list = []
    exist_date = WeeklyCunchulanOutput.objects.values().filter(chanliang_type=11).filter(
        Q(year__lt=year) | Q(year=year, weekNum__lt=week))
    for index in exist_date:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        exist_date_list.append(date_index)
    date_list = []
    data_list = []
    res = WeeklyCunchulanOutput.objects.values().filter(chanliang_type=11)
    for index in res:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        data_index = index['chanliang_value']
        date_list.append(date_index)
        data_list.append(data_index)
    content = {
        'data_list': data_list,
        'date_list': date_list,
        'exist_date_list': exist_date_list
    }
    return render(request, 'yuce_taoji_shuliang.html', content)

def yuce_fmd_yucheng_cunlan(request):
    today = datetime.date.today().strftime('%Y-%m-%d')
    res_week = WeekDateStandard.objects.values().filter(startDate__lte=today, endDate__gte=today)[0]
    year = res_week['Year']
    week = res_week['WeekNum']
    # week = 10
    exist_date_list = []
    exist_date = WeeklyCunchulanOutput.objects.values().filter(chanliang_type=2).filter(
        Q(year__lt=year) | Q(year=year, weekNum__lt=week))
    for index in exist_date:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        exist_date_list.append(date_index)
    date_list = []
    data_list = []
    res = WeeklyCunchulanOutput.objects.values().filter(chanliang_type=2)
    for index in res:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        data_index = index['chanliang_value']
        date_list.append(date_index)
        data_list.append(data_index)
    content = {
        'data_list': data_list,
        'date_list': date_list,
        'exist_date_list': exist_date_list
    }
    return render(request, 'yuce_fmd_yucheng_cunlan.html', content)

def yuce_fmd_chandan_cunlan(request):
    today = datetime.date.today().strftime('%Y-%m-%d')
    res_week = WeekDateStandard.objects.values().filter(startDate__lte=today, endDate__gte=today)[0]
    year = res_week['Year']
    week = res_week['WeekNum']
    # week = 10
    exist_date_list = []
    exist_date = WeeklyCunchulanOutput.objects.values().filter(chanliang_type=3).filter(
        Q(year__lt=year) | Q(year=year, weekNum__lt=week))
    for index in exist_date:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        exist_date_list.append(date_index)
    date_list = []
    data_list = []
    res = WeeklyCunchulanOutput.objects.values().filter(chanliang_type=3)
    for index in res:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        data_index = index['chanliang_value']
        date_list.append(date_index)
        data_list.append(data_index)
    content = {
        'data_list': data_list,
        'date_list': date_list,
        'exist_date_list': exist_date_list
    }
    return render(request, 'yuce_fmd_chandan_cunlan.html', content)

def yuce_spd_yucheng_cunlan(request):
    today = datetime.date.today().strftime('%Y-%m-%d')
    res_week = WeekDateStandard.objects.values().filter(startDate__lte=today, endDate__gte=today)[0]
    year = res_week['Year']
    week = res_week['WeekNum']
    # week = 10
    exist_date_list = []
    exist_date = WeeklyCunchulanOutput.objects.values().filter(chanliang_type=6).filter(
        Q(year__lt=year) | Q(year=year, weekNum__lt=week))
    for index in exist_date:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        exist_date_list.append(date_index)
    date_list = []
    data_list = []
    res = WeeklyCunchulanOutput.objects.values().filter(chanliang_type=6)
    for index in res:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        data_index = index['chanliang_value']
        date_list.append(date_index)
        data_list.append(data_index)
    content = {
        'data_list': data_list,
        'date_list': date_list,
        'exist_date_list': exist_date_list
    }
    return render(request, 'yuce_spd_yucheng_cunlan.html', content)

def yuce_spd_chandan_cunlan(request):
    today = datetime.date.today().strftime('%Y-%m-%d')
    res_week = WeekDateStandard.objects.values().filter(startDate__lte=today, endDate__gte=today)[0]
    year = res_week['Year']
    week = res_week['WeekNum']
    # week = 10
    exist_date_list = []
    exist_date = WeeklyCunchulanOutput.objects.values().filter(chanliang_type=7).filter(
        Q(year__lt=year) | Q(year=year, weekNum__lt=week))
    for index in exist_date:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        exist_date_list.append(date_index)
    date_list = []
    data_list = []
    res = WeeklyCunchulanOutput.objects.values().filter(chanliang_type=7)
    for index in res:
        date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
        data_index = index['chanliang_value']
        date_list.append(date_index)
        data_list.append(data_index)
    content = {
        'data_list': data_list,
        'date_list': date_list,
        'exist_date_list': exist_date_list
    }
    return render(request, 'yuce_spd_chandan_cunlan.html', content)


def weekly_siliao_usage(request):
    return render(request,'weekly_siliao_usage.html')

def monthly_siliao_usage(request):
    return render(request,'monthly_siliao_usage.html')

def yearly_siliao_usage(request):
    return render(request,'yearly_siliao_usage.html')

def weekly_cost_calc(request):

    result = get_cost_calc(2020,39)
    content = {
        'shengchanWeek_list':result['shengchanWeek_list'],
        'leijiProfit_list':result['leijiProfit_list']
    }
    return render(request,'weekly_cost_calc.html',content)





