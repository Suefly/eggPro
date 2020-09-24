#-*- coding: utf-8 -*-
import xlrd
import xlwt
from datetime import datetime
from xlrd import xldate_as_tuple
from egg.models import *

def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))

def get_province_name(province_id):
    try:
        province_name = Province.objects.values('provinceName').filter(province_id=province_id)[0]['provinceName']
    except Exception as e:
        print('Error')
    return province_name

def get_province_id(province_name):
    try:
        province_id = Province.objects.values('province_id').filter(provinceName=province_name)[0]['province_id']
    except Exception as e:
        print('Error')
    return province_id

def read_province_info_daily_egg(file):
    '''
    read the infomation of enterprise name
    :return a list

    '''
    # x = 6   35   type_id = 1  2
    province_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,12, 13, 14, 15, 16, 17, 18, 19,22,23,24,25, 27, 28]
    handle = open_excel(file)
    table = handle.sheet_by_index(1)
    # province_id_list = []
    # for index in range(4,table.ncols):
    #     province_name = table.cell(1, index).value
    #     print(province_name)
    #     province_id = get_province_id(province_name)
    #     province_id_list.append(province_id)
    # item_list = []
    for key,val in enumerate(province_list):
        item_list = []
        for index in range(3, 2799):
            cell = table.cell(index, 0).value
            if 3 == table.cell(index, 0).ctype:
                date = datetime(*xldate_as_tuple(cell, 0)).strftime('%Y-%m-%d')
                temp = table.cell(index,key+4).value
                if temp == 'X':
                    p_daily_price = 0
                else:
                    p_daily_price = temp
                province_id = province_list[key]
                print(date,get_province_name(province_id),p_daily_price)
                item = DailyPriceProvince(
                    date= date,
                    pricetype_id = 1,
                    province_id = province_id,
                    p_daily_price = p_daily_price,
                    comments = ''
                )
                item_list.append(item)
                # print(item_list)
        DailyPriceProvince.objects.bulk_create(item_list)

def read_quanguo_daily_price(file):
    handle = open_excel(file)
    table = handle.sheet_by_index(4)
    item_list = []
    for index in range(3, 2799):
        cell = table.cell(index, 0).value
        if 3 == table.cell(index, 0).ctype:
            date = datetime(*xldate_as_tuple(cell, 0)).strftime('%Y-%m-%d')
            temp1 = table.cell(index, 5).value
            temp2 = table.cell(index, 4).value
            temp3 = table.cell(index, 3).value
            if temp1 == 'X':
                daily_price = 0
            else:
                daily_price = temp1

            if temp2 == 'X':
                chan_dailyprice = 0
            else:
                chan_dailyprice = temp2

            if temp3 == 'X':
                xiao_dailyprice = 0
            else:
                xiao_dailyprice = temp3

            item = DailyPriceQGAvg(
                date=date,
                pricetype_id = 1,
                daily_price=daily_price,
                chan_dailyprice = chan_dailyprice,
                xiao_dailyprice = xiao_dailyprice,
                comments=''
            )
            item_list.append(item)
            print(date,xiao_dailyprice,chan_dailyprice,daily_price)
    DailyPriceQGAvg.objects.bulk_create(item_list)

def read_quanguo_weekly_price(file):
    handle = open_excel(file)
    table = handle.sheet_by_index(4)
    item_list = []
    for index in range(3, 403):
        cell_time = table.cell(index, 8).value
        year = int(cell_time.split('WK')[0])
        week = int(cell_time.split('WK')[1])

        temp1 = table.cell(index, 12).value
        temp2 = table.cell(index, 11).value
        temp3 = table.cell(index, 10).value
        if temp1 == 'X':
            weekly_price = 0
        else:
            weekly_price = temp1

        if temp2 == 'X':
            chan_weeklyprice = 0
        else:
            chan_weeklyprice = temp2

        if temp3 == 'X':
            xiao_weeklyprice = 0
        else:
            xiao_weeklyprice = temp3

        item = WeeklyPriceQGAvg(
            year = year,
            weekNum = week,
            pricetype_id= 1,
            weekly_price = weekly_price,
            chan_weeklyprice = chan_weeklyprice,
            xiao_weeklyprice = xiao_weeklyprice,
            comments=''
        )
        item_list.append(item)
        print(year,week,xiao_weeklyprice,chan_weeklyprice,weekly_price)
    WeeklyPriceQGAvg.objects.bulk_create(item_list)

def read_province_weekly_price(file):
    province_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 25, 27, 28]
    handle = open_excel(file)
    table = handle.sheet_by_index(2)
    # item_list = []

    for key,val in enumerate(province_list):
        item_list = []
        for index in range(3, 377):
            cell_time = table.cell(index, 1).value
            year = int(cell_time.split('WK')[0])
            week = int(cell_time.split('WK')[1])

            temp = table.cell(index,key+4).value
            if temp == 'X':
                p_weekly_price = 0
            else:
                p_weekly_price = temp
            province_id = province_list[key]
            print(year,week,get_province_name(province_id),p_weekly_price)

            item = WeeklyPriceProvince(
                year = year,
                weekNum = week,
                province_id = province_id,
                p_weekly_price = p_weekly_price,
                comments = ''
            )
            item_list.append(item)
        WeeklyPriceProvince.objects.bulk_create(item_list)

def read_quanguo_monthly_price(file):
    handle = open_excel(file)
    table = handle.sheet_by_index(4)
    item_list = []
    for index in range(3, 89):
        cell_time1 = table.cell(index, 14).value
        cell_time2 = table.cell(index, 15).value
        print(cell_time1, cell_time2)
        if 3 == table.cell(index, 0).ctype:
            dete = datetime(*xldate_as_tuple(cell_time1, 0)).strftime('%Y-%m-%d')
            year = dete.split('-')[0]
        month = int(cell_time2.split('月')[0])
        temp1 = table.cell(index, 19).value
        temp2 = table.cell(index, 18).value
        temp3 = table.cell(index, 17).value
        if temp1 == 'X':
            monthly_price = 0
        else:
            monthly_price = temp1

        if temp2 == 'X':
            chan_monthlyprice = 0
        else:
            chan_monthlyprice = temp2

        if temp3 == 'X':
            xiao_monthlyprice = 0
        else:
            xiao_monthlyprice = temp3

        item = DanMonthlyPriceQGAvg(
            year=year,
            month=month,
            month_price=monthly_price,
            chan_monthlyprice=chan_monthlyprice,
            xiao_monthlyprice=xiao_monthlyprice,
            comments=''
        )
        item_list.append(item)
        print(year,month,xiao_monthlyprice,chan_monthlyprice,monthly_price)
    DanMonthlyPriceQGAvg.objects.bulk_create(item_list)

def read_province_monthly_price(file):
    province_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 13, 14, 15, 16, 17, 18, 19, 25, 27, 28]
    handle = open_excel(file)
    table = handle.sheet_by_index(3)
    # item_list = []

    for key,val in enumerate(province_list):
        item_list = []
        for index in range(3, 89):
            cell_time1 = table.cell(index, 0).value
            cell_time2 = table.cell(index, 1).value
            # print(cell_time1,cell_time2,table.cell(index, 0).ctype)
            if 2 == table.cell(index, 0).ctype:
                dete = datetime(*xldate_as_tuple(cell_time1, 0)).strftime('%Y-%m-%d')
                year = dete.split('-')[0]
            month = int(cell_time2.split('月')[0])

            temp = table.cell(index,key+4).value
            if temp == 'X':
                p_monthly_price = 0
            else:
                p_monthly_price = temp
            province_id = province_list[key]
            print(year,month,get_province_name(province_id),p_monthly_price)

            item = DanMonthlyPriceProvince(
                year = year,
                month = month,
                province_id = province_id,
                p_monthly_price = p_monthly_price,
                comments = ''
            )
            item_list.append(item)
        DanMonthlyPriceProvince.objects.bulk_create(item_list)

def read_info_daily_taotaiji_province(file):
    '''
    read the infomation of enterprise name
    :return a list

    '''
    # x = 6   35   type_id = 1  2
    province_list = [3, 4, 5, 6, 7, 8, 10, 11, 12, 15, 16, 17, 18, 27, 28, 31]
    handle = open_excel(file)
    table = handle.sheet_by_index(7)
    # province_id_list = []
    # for index in range(4,table.ncols):
    #     province_name = table.cell(1, index).value
    #     print(province_name)
    #     province_id = get_province_id(province_name)
    #     province_id_list.append(province_id)
    # item_list = []
    for key,val in enumerate(province_list):
        item_list = []
        for index in range(3, 2531):
            cell = table.cell(index, 0).value
            if 3 == table.cell(index, 0).ctype:
                date = datetime(*xldate_as_tuple(cell, 0)).strftime('%Y-%m-%d')
                temp = table.cell(index,key+4).value
                if temp == 'X':
                    p_daily_price = 0
                else:
                    p_daily_price = temp
                province_id = province_list[key]
                print(date,get_province_name(province_id),p_daily_price)
                item = TaojiDailyPriceProvince(
                    date= date,
                    province_id = province_id,
                    p_daily_price = p_daily_price,
                    comments = ''
                )
                item_list.append(item)
                # print(item_list)
        TaojiDailyPriceProvince.objects.bulk_create(item_list)

def read_taotaiji_quanguo_daily_price(file):
    handle = open_excel(file)
    table = handle.sheet_by_index(8)
    item_list = []
    for index in range(3, 2750):
        cell = table.cell(index, 0).value
        if 3 == table.cell(index, 0).ctype:
            date = datetime(*xldate_as_tuple(cell, 0)).strftime('%Y-%m-%d')
            temp1 = table.cell(index, 3).value


            if temp1 == 'X':
                daily_price = 0
            else:
                daily_price = temp1

            item = DailyPriceQGAvg(
                date=date,
                pricetype_id=2,
                daily_price=daily_price,
                chan_dailyprice=0,
                xiao_dailyprice=0,
                comments=''
            )
            item_list.append(item)

    DailyPriceQGAvg.objects.bulk_create(item_list)

def read_taotaiji_province_weekly_price(file):
    province_list = [3, 4, 5, 6, 7, 8, 10, 11, 12, 15, 16, 17, 18, 27, 28, 31]
    handle = open_excel(file)
    table = handle.sheet_by_index(2)
    # item_list = []

    for key,val in enumerate(province_list):
        item_list = []
        for index in range(3, 365):
            cell_time = table.cell(index, 1).value
            year = int(cell_time.split('WK')[0])
            week = int(cell_time.split('WK')[1])

            temp = table.cell(index,key+4).value
            if temp == 'X':
                p_weekly_price = 0
            else:
                p_weekly_price = temp

            province_id = province_list[key]
            print(year,week,get_province_name(province_id),p_weekly_price)

            item = TaojiWeeklyPriceProvince(
                year = year,
                weekNum = week,
                province_id = province_id,
                p_weekly_price = p_weekly_price,
                comments = ''
            )
            item_list.append(item)
        TaojiWeeklyPriceProvince.objects.bulk_create(item_list)


def read_taotaiji_province_monthly_price(file):
    province_list = [3, 4, 5, 6, 7, 8, 10, 11, 12, 15, 16, 17, 18, 27, 28, 31]
    handle = open_excel(file)
    table = handle.sheet_by_index(3)
    # item_list = []

    for key,val in enumerate(province_list):
        item_list = []
        for index in range(3, 88):
            cell_time1 = table.cell(index, 0).value
            cell_time2 = table.cell(index, 1).value
            # print(cell_time1,cell_time2,table.cell(index, 0).ctype)
            if 2 == table.cell(index, 0).ctype:
                dete = datetime(*xldate_as_tuple(cell_time1, 0)).strftime('%Y-%m-%d')
                year = dete.split('-')[0]
            month = int(cell_time2.split('月')[0])

            temp = table.cell(index,key+4).value
            if temp == 'X':
                p_monthly_price = 0
            else:
                p_monthly_price = temp
            province_id = province_list[key]
            print(year,month,get_province_name(province_id),p_monthly_price)

            item = TaojiMonthlyPriceProvince(
                year = year,
                month = month,
                province_id = province_id,
                p_monthly_price = p_monthly_price,
                comments = ''
            )
            item_list.append(item)
        TaojiMonthlyPriceProvince.objects.bulk_create(item_list)

def read_taotaiji_quanguo_weekly_price(file):
    handle = open_excel(file)
    table = handle.sheet_by_index(4)
    item_list = []
    for index in range(3, 365):
        cell_time = table.cell(index, 30).value
        year = int(cell_time.split('WK')[0])
        week = int(cell_time.split('WK')[1])

        temp1 = table.cell(index, 32).value
        temp2 = table.cell(index, 33).value

        if temp1 == 'X':
            weekly_price = 0
        else:
            weekly_price = temp1

        if temp2 == 'X':
            chan_weeklyprice = 0
        else:
            chan_weeklyprice = temp2

        item = TaojiWeeklyPriceQGAvg(
            year = year,
            weekNum = week,
            weekly_price = weekly_price,
            chan_weeklyprice = chan_weeklyprice,
            comments=''
        )
        item_list.append(item)
        print(year,week,weekly_price,chan_weeklyprice)
    TaojiWeeklyPriceQGAvg.objects.bulk_create(item_list)


def read_taotaiji_quanguo_monthly_price(file):
    handle = open_excel(file)
    table = handle.sheet_by_index(4)
    item_list = []
    for index in range(3, 87):
        cell_time1 = table.cell(index, 40).value
        cell_time2 = table.cell(index, 41).value
        # print(cell_time1,cell_time2,table.cell(index, 0).ctype)
        if 2 == table.cell(index, 40).ctype:
            dete = datetime(*xldate_as_tuple(cell_time1, 0)).strftime('%Y-%m-%d')
            year = dete.split('-')[0]
        month = int(cell_time2.split('月')[0])

        temp1 = table.cell(index, 43).value
        temp2 = table.cell(index, 44).value

        if temp1 == 'X':
            monthly_price = 0
        else:
            monthly_price = temp1

        if temp2 == 'X':
            chan_monthlyprice = 0
        else:
            chan_monthlyprice = temp2

        item = TaojiMonthlyPriceQGAvg(
            year = year,
            month = month,
            month_price = monthly_price,
            chan_monthlyprice = chan_monthlyprice,
            comments=''
        )
        item_list.append(item)
        print(year,month,monthly_price,chan_monthlyprice)
    TaojiMonthlyPriceQGAvg.objects.bulk_create(item_list)


#################################################################
#####  成本   收益
#################################################################
def read_layer_quanguo_weekly_cost(file):
    handle = open_excel(file)
    table = handle.sheet_by_index(0)
    item_list = []
    for index in range(3, 639):
        cell_time = table.cell(index, 1).value
        year = int(cell_time.split('WK')[0])
        week = int(cell_time.split('WK')[1])

        temp = table.cell(index, 3).value

        if temp == 'X':
            cost_value = 0
        else:
            cost_value = temp

        item = WeeklyCostQGAvg(
            year = year,
            weekNum = week,
            cost_value = cost_value,
            comments=''
        )
        item_list.append(item)
        print(year,week,cost_value)
    WeeklyCostQGAvg.objects.bulk_create(item_list)

def read_layer_province_weekly_cost(file):
    province_list = [6,3,15,16]
    handle = open_excel(file)
    table = handle.sheet_by_index(0)

    for key,val in enumerate(province_list):
        item_list = []
        for index in range(3, 639):
            cell_time = table.cell(index, 1).value
            year = int(cell_time.split('WK')[0])
            week = int(cell_time.split('WK')[1])

            temp = table.cell(index,key+4).value
            if temp == 'X':
                cost_value = 0
            else:
                cost_value = temp
            province_id = province_list[key]
            print(year,week,get_province_name(province_id),cost_value)

            item = WeeklyCostProvince(
                year = year,
                weekNum = week,
                province_id = province_id,
                cost_value = cost_value,
                comments = ''
            )
            item_list.append(item)
        WeeklyCostProvince.objects.bulk_create(item_list)


def read_layer_quanguo_weekly_profit(file):
    handle = open_excel(file)
    table = handle.sheet_by_index(0)
    item_list = []
    for index in range(3, 639):
        cell_time = table.cell(index, 1).value
        year = int(cell_time.split('WK')[0])
        week = int(cell_time.split('WK')[1])

        temp = table.cell(index, 8).value

        if temp == 'X':
            profit_value = 0
        else:
            profit_value = temp

        item = WeeklyProfitQGAvg(
            year = year,
            weekNum = week,
            profit_value = profit_value,
            comments=''
        )
        item_list.append(item)
        print(year,week,profit_value)
    WeeklyProfitQGAvg.objects.bulk_create(item_list)


def read_layer_province_weekly_profit(file):
    province_list = [6,3,15,16]
    handle = open_excel(file)
    table = handle.sheet_by_index(0)

    for key,val in enumerate(province_list):
        item_list = []
        for index in range(3, 639):
            cell_time = table.cell(index, 1).value
            year = int(cell_time.split('WK')[0])
            week = int(cell_time.split('WK')[1])

            temp = table.cell(index,key+9).value
            if temp == 'X':
                profit_value = 0
            else:
                profit_value = temp
            province_id = province_list[key]
            print(year,week,get_province_name(province_id),profit_value)

            item = WeeklyProfitProvince(
                year = year,
                weekNum = week,
                province_id = province_id,
                profit_value = profit_value,
                comments = ''
            )
            item_list.append(item)
        WeeklyProfitProvince.objects.bulk_create(item_list)


def read_layer_quanguo_monthly_cost(file):
    handle = open_excel(file)
    table = handle.sheet_by_index(1)
    item_list = []
    for index in range(3, 150):
        cell_time1 = table.cell(index, 0).value
        cell_time2 = table.cell(index, 1).value
        # print(cell_time1,cell_time2,table.cell(index, 0).ctype)
        if 2 == table.cell(index, 0).ctype:
            dete = datetime(*xldate_as_tuple(cell_time1, 0)).strftime('%Y-%m-%d')
            year = dete.split('-')[0]
        month = int(cell_time2.split('月')[0])

        temp = table.cell(index, 3).value

        if temp == 'X':
            cost_value = 0
        else:
            cost_value = temp

        item = MonthlyCostQGAvg(
            year = year,
            month = month,
            cost_value = cost_value,
            comments=''
        )
        item_list.append(item)
        print(year,month,cost_value)
    MonthlyCostQGAvg.objects.bulk_create(item_list)


def read_layer_province_monthly_cost(file):
    province_list = [6,3,15,16]
    handle = open_excel(file)
    table = handle.sheet_by_index(1)

    for key,val in enumerate(province_list):
        item_list = []
        for index in range(3, 150):
            cell_time1 = table.cell(index, 0).value
            cell_time2 = table.cell(index, 1).value
            # print(cell_time1,cell_time2,table.cell(index, 0).ctype)
            if 2 == table.cell(index, 0).ctype:
                dete = datetime(*xldate_as_tuple(cell_time1, 0)).strftime('%Y-%m-%d')
                year = dete.split('-')[0]
            month = int(cell_time2.split('月')[0])

            temp = table.cell(index,key+4).value
            if temp == 'X':
                cost_value = 0
            else:
                cost_value = temp
            province_id = province_list[key]
            print(year,month,get_province_name(province_id),cost_value)

            item = MonthlyCostProvince(
                year = year,
                month = month,
                province_id = province_id,
                cost_value = cost_value,
                comments = ''
            )
            item_list.append(item)
        MonthlyCostProvince.objects.bulk_create(item_list)


def read_layer_quanguo_monthly_profit(file):
    handle = open_excel(file)
    table = handle.sheet_by_index(1)
    item_list = []
    for index in range(3, 150):
        cell_time1 = table.cell(index, 0).value
        cell_time2 = table.cell(index, 1).value

        if 2 == table.cell(index, 0).ctype:
            dete = datetime(*xldate_as_tuple(cell_time1, 0)).strftime('%Y-%m-%d')
            year = dete.split('-')[0]
        month = int(cell_time2.split('月')[0])

        temp = table.cell(index, 8).value

        if temp == 'X':
            profit_value = 0
        else:
            profit_value = temp

        item = MonthlyProfitQGAvg(
            year = year,
            month = month,
            profit_value = profit_value,
            comments=''
        )
        item_list.append(item)
        print(year,month,profit_value)
    MonthlyProfitQGAvg.objects.bulk_create(item_list)


def read_layer_province_monthly_profit(file):
    province_list = [6,3,15,16]
    handle = open_excel(file)
    table = handle.sheet_by_index(1)

    for key,val in enumerate(province_list):
        item_list = []
        for index in range(3, 150):
            cell_time1 = table.cell(index, 0).value
            cell_time2 = table.cell(index, 1).value
            # print(cell_time1,cell_time2,table.cell(index, 0).ctype)
            if 2 == table.cell(index, 0).ctype:
                dete = datetime(*xldate_as_tuple(cell_time1, 0)).strftime('%Y-%m-%d')
                year = dete.split('-')[0]
            month = int(cell_time2.split('月')[0])

            temp = table.cell(index,key+9).value
            if temp == 'X':
                profit_value = 0
            else:
                profit_value = temp
            province_id = province_list[key]
            print(year,month,get_province_name(province_id),profit_value)

            item = MonthlyProfitProvince(
                year = year,
                month = month,
                province_id = province_id,
                profit_value = profit_value,
                comments = ''
            )
            item_list.append(item)
        MonthlyProfitProvince.objects.bulk_create(item_list)

def read_cunlan_fumudai_yucheng(file):
    handle = open_excel(file)
    table = handle.sheet_by_index(0)
    item_list = []
    for index in range(663, 676):
        cell = table.cell(index,1).value
        year = cell.split('WK')[0]
        weekNum = cell.split('WK')[1]

        temp = table.cell(index, 6).value
        if temp == 'X':
            chanliang_value = 0
        else:
            chanliang_value = temp


        item = WeeklyCunchulanOutput(
            year=year,
            weekNum = weekNum,
            chanliang_type = 5,
            chanliang_value=chanliang_value,
            comments=''
        )
        item_list.append(item)
    WeeklyCunchulanOutput.objects.bulk_create(item_list)


def read_quanguo_weekly_price(file):
    handle = open_excel(file)
    table = handle.sheet_by_index(1)
    item_list = []
    for index in range(36, 53):
        cell_time = table.cell(index, 0).value
        year = 2020
        week = int(cell_time.split('wk')[1])

        temp1 = table.cell(index, 2).value

        if temp1 == 'X':
            weekly_price = 0
        else:
            weekly_price = temp1

        item = WeeklyPriceQGAvg(
            year = year,
            weekNum = week,
            pricetype_id= 1,
            weekly_price = weekly_price,
            chan_weeklyprice = 0,
            xiao_weeklyprice = 0,
            comments=''
        )
        item_list.append(item)
    WeeklyPriceQGAvg.objects.bulk_create(item_list)


def read_cunlan_fumudai_yucheng(file):
    handle = open_excel(file)
    table = handle.sheet_by_index(0)
    item_list = []
    for index in range(91, 790):
        year = table.cell(index,0).value
        weekNum = table.cell(index,1).value

        temp = table.cell(index, 7).value
        if temp == 'X':
            chanliang_value = 0
        else:
            chanliang_value = temp


        item = WeeklyCunchulanOutput(
            year=year,
            weekNum = weekNum,
            chanliang_type = 11,
            chanliang_value=chanliang_value,
            comments=''
        )
        item_list.append(item)
    WeeklyCunchulanOutput.objects.bulk_create(item_list)


def ReadWeeklyDanjiLeijiProfit(file):
    handle = open_excel(file)
    table = handle.sheet_by_index(0)

    week_list = []
    for index in range(1,111):
        week_tmp = table.cell(index, 4).value
        year = week_tmp.split('WK')[0]
        weekNum = week_tmp.split('WK')[1]
        week_list.append((year,weekNum))

    shengchanweek_list = []
    for index in range(1,111):
        shengchanweek_tmp = int(table.cell(index, 5).value)
        shengchanweek_list.append(shengchanweek_tmp)


    item_list = []

    t = 1

    while t < 111:
        originYear = int(week_list[t - 1][0])
        originWeek = int(week_list[t - 1][1])
        k = 0
        for index in range(t, 111):
            week_tmp = table.cell(index, 4).value
            date_tmp = table.cell(index, 3).value
            if 3 == table.cell(index, 3).ctype:
                date_value = datetime(*xldate_as_tuple(date_tmp, 0)).strftime('%Y-%m-%d')
            year = week_tmp.split('WK')[0]
            weekNum = week_tmp.split('WK')[1]
            shengchanWeek = shengchanweek_list[k]
            leijiProfit = table.cell(index,t+5).value

            item = WeeklyDanjiLeijiProfit(
                date = date_value,
                originYear=originYear,
                originWeek=originWeek,
                year = year,
                weekNum = weekNum,
                shengchanWeek = shengchanWeek,
                leijiProfit=leijiProfit,
                Remark=''
            )
            item_list.append(item)
            k = k +1
        t = t+1
    WeeklyDanjiLeijiProfit.objects.bulk_create(item_list)


if __name__ == '__main__':
    file = 'C:\\Users\\sujie\\Desktop\\数据库项目\\蛋鸡\\鸡蛋和淘汰蛋鸡价格汇总-1-20200827.xlsx'
    file = 'C:\\Users\\sujie\\Desktop\\数据库项目\\蛋鸡\\蛋鸡应用数据-20200826.xlsx'
    file = 'C:\\Users\\sujie\\Desktop\\数据库项目\\蛋鸡\\补数据.xlsx'
    file = 'C:\\Users\\sujie\\Desktop\\数据库项目\\蛋鸡\\分批次成本效益核算-1.xlsx'
    # read_quanguo_daily_price(file)



