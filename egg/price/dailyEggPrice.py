from egg.common import *

def get_egg_quanguo_dailyprice(type_id):
    '''

    :param typeId: pig type
    :return: date_list,daily_price_list
    '''
    date_list = []
    daily_price_list = []
    try:
        res_list = DailyPriceQGAvg.objects.values('date','daily_price').filter(pricetype_id=type_id, daily_price__gt=0).order_by('date',)
        for index in res_list:
            date_list.append(index['date'].strftime('%Y-%m-%d'))
            daily_price_list.append(round(index['daily_price'],2))
    except Exception as e:
        print(str(e))
    return date_list,daily_price_list


def get_egg_dailypice_for_province(province_id):
    daily_price_list = []
    date_list = []
    try:
        res = DailyPriceProvince.objects.values('date', 'p_daily_price').filter(province_id=province_id,p_daily_price__gt=0)
        for index in res:
            date_list.append(index['date'].strftime('%Y-%m-%d'))
            daily_price_list.append(round(index['p_daily_price'],2))
    except Exception as e:
        print(str(e))
    return date_list,daily_price_list


def gen_egg_province_dprice_map(date):
    data_list = []
    try:
        res_list = DailyPriceProvince.objects.filter(
            date=date).annotate(
            name=F('province__provinceName'),
            value=F('p_daily_price')).values('name','value')
        for index in res_list:
            index['value'] = round(index['value'],2)
            data_list.append(index)
    except Exception as e:
        print(str(e))
    return data_list


def get_lastday_egg_daily_table():
    try:
        res = DailyPriceProvince.objects.values('date').distinct().order_by('-date')[0]
        last_date = res['date'].strftime('%Y-%m-%d')
    except Exception as e:
        last_date = ''
        print(str(e))
    return last_date


def get_egg_chanxiao_dailyprice():
    result_dict = {}
    quanguo_price = []
    chan_price = []
    xiao_price = []
    date_list = []
    try:
        res = DailyPriceQGAvg.objects.values('date','daily_price','chan_dailyprice','xiao_dailyprice').filter(daily_price__gt=0,date__gt='2013-01-04').order_by('date')
        for index in res:
            date_list.append(index['date'].strftime('%Y-%m-%d'))
            quanguo_price.append(round(index['daily_price'],2))
            chan_price.append(round(index['chan_dailyprice'],2))
            xiao_price.append(round(index['xiao_dailyprice'],2))
        result_dict['date_list'] = date_list
        result_dict['quanguo_price'] = quanguo_price
        result_dict['chan_price'] = chan_price
        result_dict['xiao_price'] = xiao_price

    except Exception as e:
        print(str(e))
    return result_dict


def gen_date_format(province_id_list):
    final_date = []
    for province_id in range(1, len(get_province_list())):
        pro_dict = {}
        pro_dict['name'] = get_provinceName_by_id(province_id)
        pro_dict['type'] = 'line'
        pro_date = get_egg_dailypice_for_province(province_id)[1]
        pro_dict['data'] = pro_date
        final_date.append(pro_dict)
        del pro_dict
    return final_date

def gen_ajax_province_price_format(province_id_list):
    final_data = []
    province_name_list = []
    date_index = get_egg_dailypice_for_province(province_id_list[0])[0]
    for province_id in province_id_list:
        pro_dict = {}
        pro_dict['name'] = get_provinceName_by_id(province_id)
        province_name_list.append(pro_dict['name'])
        pro_dict['type'] = 'line'
        pro_date = get_egg_dailypice_for_province(province_id)[1]
        pro_dict['data'] = pro_date
        final_data.append(pro_dict)
        del pro_dict
    return date_index,final_data,province_name_list


####  存出栏和产量
def get_lastweek_egg_output_table(output_type_id):
    try:
        res = WeeklyCunchulanOutput.objects.values('year','weekNum').filter(chanliang_type=output_type_id).distinct().order_by('-year','-weekNum')[0]
        year = res['year']
        week = res['weekNum']
    except Exception as e:
        last_date = ''
        print(str(e))
    return year,week


def get_week_cunchulan_output(output_type_id):
    date_list = []
    data_list = []
    try:
        res = WeeklyCunchulanOutput.objects.filter(chanliang_type=output_type_id).values()
        for index in res:
            date_index = str(index['year']) + '年第' + str(index['weekNum']) + '周'
            data_index = index['chanliang_value']
            date_list.append(date_index)
            data_list.append(data_index)
    except Exception as e:
        print('get_week_cunchulan_output',str(e))

    return date_list,data_list



