from egg.models import *
from django.db.models import F
from django.db.models import Q
from django.db.models import Avg

WEEK_DICT = {
    0:'一',
    1:'二',
    2:'三',
    3:'四',
    4:'五',
    5:'六',
    6:'日'
}


EGG_PRICE_DICT = {
        '北京':[],
        '天津':[],
        '河北':[],
        '辽宁':[],
        '吉林':[],
        '黑龙江':[],
        '山东':[],
        '河南':[],
        '安徽':[],
        '陕西':[],
        '山西':[],
        '江苏':[],
        '广东':[],
        '上海':[],
        '福建':[],
        '湖南':[],
        '湖北':[],
        '云南':[],
        '甘肃':[],
        '内蒙':[],
        '江西':[]
        # '浙江':[],
        # '四川':[],
        # '宁夏':[]
    }

TAOTAIJI_PRICE_DICT = {
    '辽宁':[],
    '河北':[],
    '陕西':[],
    '河南':[],
    '山东':[],
    '湖南':[],
    '湖北':[],
    '江苏':[],
    '安徽':[],
    '浙江':[],
    '山西':[],
    '甘肃':[],
    '吉林':[],
    '黑龙江':[],
    '新疆':[],
    '内蒙':[],
}

def get_city_id(city):
    '''
    :author sujie@boyar.cn  2019-11-18
    :param city: 根据日度价格表导入各地方猪价，根据地级市名获取该地级市的city_id
    :return:
    '''
    try:
        city_id = City.objects.values('city_id').filter(cityName__contains=city)[0]['city_id']
    except Exception as e:
        city_id = 0
        print(str(e))
    return city_id

def get_province_list():
    res = Province.objects.all().values('provinceName')
    p_list = []
    for index in res:
        p_list.append(index['provinceName'])
    return p_list

def get_provinceName_by_id(province_id):
    provinceName = ''
    try:
        provinceName = Province.objects.values('provinceName').filter(province_id=province_id)[0]['provinceName']
    except Exception as e:
        print(str(e))

    return provinceName



def get_huanbi_week(year,week):
    huanbi_year = 0
    huanbi_week = 0
    current_id = WeekDateStandard.objects.values('id').filter(Year=year, WeekNum=week)[0]['id']
    try:
        res = WeekDateStandard.objects.values('Year','WeekNum').filter(id= current_id-1)
        huanbi_year = res[0]['Year']
        huanbi_week = res[0]['WeekNum']
    except Exception as e:
        print(str(e))

    return huanbi_year,huanbi_week


def get_tongbi_week(year,week):

    week_list = []
    res = WeekDateStandard.objects.values('WeekNum').filter(Year=int(year)-1)
    for index in res:
        week_list.append(index['WeekNum'])
    if week not in week_list:
        tongbi_year = year - 1
        tongbi_week = 52
    else:
        tongbi_year = year - 1
        tongbi_week = week
    return tongbi_year,tongbi_week



def get_huanbi_month(year,month):
    huanbi_year = 0
    huanbi_month = 0
    current_id = MonthDateStandard.objects.values('id').filter(year=year, month = month)[0]['id']
    try:
        res = MonthDateStandard.objects.values('year','month').filter(id= current_id-1)
        huanbi_year = res[0]['year']
        huanbi_month = res[0]['month']
    except Exception as e:
        print(str(e))

    return huanbi_year,huanbi_month

def get_year_week_by_date(input_date):
    '''

    :param input_date: 给定一个日期，判断是哪一年的第几周
    :return:
    '''
    result_init = {}
    try:
        result_init = WeekDateStandard.objects.values('Year','WeekNum').filter(startDate__lte = input_date,endDate__gte=input_date)[0]
    except Exception as e:
        print(str(e))

    return result_init


# def loginValid(fun):
#     def inner(request,*args,**kwargs):
#         cookie = request.COOKIES.get('username')
#         session = request.session.get('username')
#         user_id = request.COOKIES.get('user_id')
#         if cookie and session and cookie == session:
#             user = Seller.objects.filter(username=cookie).first()
#             if user:
#                 return fun(request,*args,**kwargs)
#             else:
#                 return redirect('store:login')
#         else:
#             return redirect('store:login')
#     return inner


def get_lastday_in_weekly_cost_table():
    try:
        res = WeeklyCostProvince.objects.values('year','weekNum').distinct().order_by('-year','-weekNum')[0]
        cur_year = res['year']
        cur_week = res['weekNum']
    except Exception as e:
        cur_year = ''
        cur_week = ''
        print(str(e))
    return cur_year,cur_week


def get_weekly_cost_QGAvg_info():
    '''

    :return:
    '''
    time_list = []
    cost_value_list = []
    try:
        res_list = WeeklyCostQGAvg.objects.values('year','weekNum', 'cost_value').filter(cost_value__gt=0).order_by('year','weekNum' )
        for index in res_list:
            time_list.append(str(index['year'])+'年第'+str(index['weekNum'])+'周')
            cost_value_list.append(round(index['cost_value'],2))
    except Exception as e:
        print(str(e))
    return time_list, cost_value_list


def get_weekly_cost_all_province(input_year,input_week):
    result_list = []
    try:
        res = WeeklyCostProvince.objects.values('province__provinceName','cost_value').filter(year=input_year,weekNum=input_week,cost_value__gt=0)
        for index in res:
            index['cost_value'] = round(index['cost_value'],2)
            result_list.append(index)
    except Exception as e:
        print(str(e))

    return result_list


def get_weekly_cost_info_province(province_id):
    '''

    :return:
    '''
    time_list = []
    cost_value_list = []
    try:
        res_list = WeeklyCostProvince.objects.values('year','weekNum', 'cost_value').filter(province_id=province_id,cost_value__gt=0).order_by('year', 'weekNum')
        for index in res_list:
            time_list.append(str(index['year'])+'年第'+str(index['weekNum'])+'周')
            cost_value_list.append(round(index['cost_value'],2))
    except Exception as e:
        print(str(e))

    return time_list, cost_value_list


def get_quanguo_monthly_cost_info():
    '''
    :return:
    '''
    time_list = []
    cost_value_list = []
    try:
        res_list = MonthlyCostQGAvg.objects.values('year','month', 'cost_value').filter(cost_value__gt=0).order_by('year','month' )
        for index in res_list:
            time_list.append(str(index['year'])+'年'+str(index['month'])+'月')
            cost_value_list.append(round(index['cost_value'],2))
    except Exception as e:
        print(str(e))

    return time_list, cost_value_list


def get_lastday_in_monthly_cost_table():
    try:
        res = MonthlyCostProvince.objects.values('year','month').distinct().order_by('-year','-month')[0]
        cur_year = res['year']
        cur_month = res['month']
    except Exception as e:
        cur_year = ''
        cur_month = ''
        print(str(e))
    return cur_year,cur_month


def get_monthly_cost_all_province(input_year,input_month):
    result_list = []
    try:
        res = MonthlyCostProvince.objects.values('province__provinceName','cost_value').filter(year=input_year,month =input_month,cost_value__gt=0)
        for index in res:
            index['cost_value'] = round(index['cost_value'],2)
            result_list.append(index)
    except Exception as e:
        print(str(e))

    return result_list



def get_monthly_cost_info_province(province_id):
    '''
    :return:
    '''
    time_list = []
    cost_value_list = []
    try:
        res_list = MonthlyCostProvince.objects.values('year','month', 'cost_value').filter(province_id=province_id,cost_value__gt=0).order_by('year', 'month')
        for index in res_list:
            time_list.append(str(index['year'])+'年'+str(index['month'])+'月')
            cost_value_list.append(round(index['cost_value'],2))
    except Exception as e:
        print(str(e))

    return time_list, cost_value_list

def get_lastday_in_weekly_profit_table():
    try:
        res = WeeklyProfitProvince.objects.values('year','weekNum').distinct().order_by('-year','-weekNum')[0]
        cur_year = res['year']
        cur_week = res['weekNum']
    except Exception as e:
        cur_year = ''
        cur_week = ''
        print(str(e))
    return cur_year,cur_week


def get_weekly_profit_quanguo_info():
    '''
    :return:
    '''
    time_list = []
    profit_value_list = []
    try:
        res_list = WeeklyProfitQGAvg.objects.values('year','weekNum', 'profit_value').filter(Q(profit_value__gt=0) | Q(profit_value__lt=0)).order_by('year','weekNum' )
        for index in res_list:
            time_list.append(str(index['year'])+'年第'+str(index['weekNum'])+'周')
            profit_value_list.append(round(index['profit_value'],2))
    except Exception as e:
        print(str(e))

    return time_list, profit_value_list


def get_weekly_profit_all_province(input_year,input_week):
    result_list = []
    try:
        res = WeeklyProfitProvince.objects.values('province__provinceName','profit_value').filter(year=input_year,weekNum=input_week).filter(Q(profit_value__gt=0) | Q(profit_value__lt=0))
        for index in res:
            index['profit_value'] = round(index['profit_value'],2)
            result_list.append(index)
    except Exception as e:
        print(str(e))

    return result_list


def get_weekly_profit_info_province(province_id):
    '''
    :return:
    '''
    time_list = []
    profit_value_list = []
    try:
        res_list = WeeklyProfitProvince.objects.values('year','weekNum', 'profit_value').filter(province_id=province_id).filter(Q(profit_value__gt=0) | Q(profit_value__lt=0)).order_by('year', 'weekNum')
        for index in res_list:
            time_list.append(str(index['year'])+'年第'+str(index['weekNum'])+'周')
            profit_value_list.append(round(index['profit_value'],2))
    except Exception as e:
        print(str(e))

    return time_list, profit_value_list


def get_lastday_in_monthly_profit_table():
    try:
        res = MonthlyProfitProvince.objects.values('year','month').distinct().order_by('-year','-month')[0]
        cur_year = res['year']
        cur_month = res['month']
    except Exception as e:
        cur_year = ''
        cur_month = ''
        print(str(e))
    return cur_year,cur_month


def get_monthly_profit_quanguo_info():
    '''
    :return:
    '''
    time_list = []
    profit_value_list = []
    try:
        res_list = MonthlyProfitQGAvg.objects.values('year','month', 'profit_value').filter(Q(profit_value__gt=0) | Q(profit_value__lt=0)).order_by('year','month' )
        for index in res_list:
            time_list.append(str(index['year'])+'年'+str(index['month'])+'月')
            profit_value_list.append(round(index['profit_value'],2))
    except Exception as e:
        print(str(e))

    return time_list, profit_value_list


def get_monthly_profit_all_province(input_year,input_month):
    result_list = []
    try:
        res = MonthlyProfitProvince.objects.values('province__provinceName','profit_value').filter(year=input_year,month=input_month).filter(Q(profit_value__gt=0) | Q(profit_value__lt=0))
        for index in res:
            index['profit_value'] = round(index['profit_value'],2)
            result_list.append(index)
    except Exception as e:
        print(str(e))

    return result_list


def get_monthly_profit_info_province(province_id):
    '''
    :return:
    '''
    time_list = []
    profit_value_list = []
    try:
        res_list = MonthlyProfitProvince.objects.values('year','month', 'profit_value').filter(province_id=province_id).filter(Q(profit_value__gt=0) | Q(profit_value__lt=0)).order_by('year', 'month')
        for index in res_list:
            time_list.append(str(index['year'])+'年'+str(index['month'])+'月')
            profit_value_list.append(round(index['profit_value'],2))
    except Exception as e:
        print(str(e))

    return time_list, profit_value_list


def get_cost_calc(year,weekNum):
    profit_dict = {
        'leijiProfit_list':[],
        'shengchanWeek_list':[]
    }

    try:
        res = WeeklyDanjiLeijiProfit.objects.values().filter(year=year,weekNum=weekNum).order_by('shengchanWeek')
        for index in res:
            profit_dict['leijiProfit_list'].append(round(index['leijiProfit'],2))
            profit_dict['shengchanWeek_list'].append('第'+str(index['shengchanWeek'])+'周')
    except Exception as e:
        print(str(e))

    return profit_dict
