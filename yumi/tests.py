from django.test import TestCase
#-*- coding: utf-8 -*-
import xlrd
import xlwt
from datetime import datetime
from xlrd import xldate_as_tuple
from yumi.models import *
from basic.models import Province
from django.db.models import Avg

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
# Create your tests here.


def read_daily_quanguo_yumi(file):
    handle = open_excel(file)
    table = handle.sheet_by_index(1)
    # yumipricetype_id = 1
    # col_param = 3
    # yumipricetype_id = 2
    # col_param = 10
    # yumipricetype_id = 3
    # col_param = 20
    # yumipricetype_id = 4
    # col_param = 35
    yumipricetype_id = 5
    col_param = 44
    item_list = []
    for index in range(1495, 1586):
        cell = table.cell(index, 0).value
        temp = table.cell(index, col_param).value
        if 3 == table.cell(index, 0).ctype:
            date = datetime(*xldate_as_tuple(cell, 0)).strftime('%Y-%m-%d')
        if temp == 'X':
            daily_price = 0
        else:
            daily_price = temp
        print(date,daily_price)
        item = YumiDailyPriceQuanguoAvg(
            date = date,
            yumipricetype_id = yumipricetype_id,
            daily_price = daily_price,
            comments=''
        )
        item_list.append(item)
    YumiDailyPriceQuanguoAvg.objects.bulk_create(item_list)

def read_daily_yumi_province(file):
    '''
    read the infomation of enterprise name
    :return a list

    '''
    # province_list = [2,5,6,7,8]
    # province_list = [2, 5, 6, 7, 8,12,14,15]
    # province_list = [1,3,2,4,5,6,7,8,10,12,14,15,24]
    # province_list = [2, 5, 6, 7, 8, 14, 15]
    province_list = [9,11,19,13,16,17,18,20,28,21,22]
    # yumipricetype_id = 5
    # yumipricetype_id = 1
    # col_param = 4
    # yumipricetype_id = 2
    # col_param = 11
    # yumipricetype_id = 3
    # col_param = 21
    # yumipricetype_id = 4
    # col_param = 36
    yumipricetype_id = 5
    col_param = 45

    handle = open_excel(file)
    table = handle.sheet_by_index(1)
    item_list = []
    for key,val in enumerate(province_list):
        for index in range(1495, 1586):
            cell = table.cell(index, 0).value
            temp = table.cell(index, key + col_param).value
            if 3 == table.cell(index, 0).ctype:
                date = datetime(*xldate_as_tuple(cell, 0)).strftime('%Y-%m-%d')
            if temp == 'X':
                daily_price = 0
            else:
                daily_price = temp
            province_id = province_list[key]
            print(date, daily_price,province_id)

            item = YumiDailyPriceProvince(
                date = date,
                province_id = province_id,
                yumipricetype_id = yumipricetype_id,
                daily_price = daily_price,
                comments = ''
            )
            item_list.append(item)
    YumiDailyPriceProvince.objects.bulk_create(item_list)

def read_weekly_quanguo_yumi(file):
    handle = open_excel(file)
    table = handle.sheet_by_index(2)
    item_list = []
    # yumipricetype_id = 1
    # col_param = 3
    # yumipricetype_id = 2
    # col_param = 10
    # yumipricetype_id = 3
    # col_param = 20
    # yumipricetype_id = 4
    # col_param = 35
    yumipricetype_id = 5
    col_param = 44
    for index in range(216,230):
        # year = table.cell(index, 3).value
        # week = table.cell(index, 4).value
        cell_time = table.cell(index, 1).value
        year = int(cell_time.split('WK')[0])
        week = int(cell_time.split('WK')[1])
        temp = table.cell(index, col_param).value
        if temp == 'X':
            weekly_price = 0
        else:
            weekly_price = temp
        print(year,week,weekly_price)
        item = YumiWeeklyPriceQuanguoAvg(
            year = year,
            weekNum = week,
            yumipricetype_id = yumipricetype_id,
            weekly_price=weekly_price,
            comments=''
        )
        item_list.append(item)
    YumiWeeklyPriceQuanguoAvg.objects.bulk_create(item_list)

def read_weekly_yumi_province(file):
    '''
    read the infomation of enterprise name
    :return a list

    '''

    # yumipricetype_id = 1
    # col_param = 4
    # yumipricetype_id = 2
    # col_param = 11
    # yumipricetype_id = 3
    # col_param = 21
    # yumipricetype_id = 4
    # col_param = 36
    yumipricetype_id = 5
    col_param = 45

    # province_list = [2,5,6,7,8]
    # province_list = [2, 5, 6, 7, 8,12,14,15]
    # province_list = [1,3,2,4,5,6,7,8,10,12,14,15,24]
    # province_list = [2, 5, 6, 7, 8, 14, 15]
    province_list = [9,11,19,13,16,17,18,20,28,21,22]


    handle = open_excel(file)
    table = handle.sheet_by_index(2)
    item_list = []
    for key,val in enumerate(province_list):
        for index in range(216,230):
            # year = table.cell(index, 3).value
            # week = table.cell(index, 4).value
            cell_time = table.cell(index, 1).value
            year = int(cell_time.split('WK')[0])
            week = int(cell_time.split('WK')[1])
            temp = table.cell(index, key + col_param).value
            if temp == 'X':
                weekly_price = 0
            else:
                weekly_price = temp
            province_id = province_list[key]
            print(year,week, weekly_price,province_id)

            item = YumiWeeklyPriceProvince(
                year = year,
                weekNum = week,
                province_id = province_id,
                yumipricetype_id = yumipricetype_id,
                weekly_price = weekly_price,
                comments = ''
            )
            item_list.append(item)
    YumiWeeklyPriceProvince.objects.bulk_create(item_list)

def read_monthly_quanguo_yumi(file):
    handle = open_excel(file)
    table = handle.sheet_by_index(3)
    item_list = []
    # yumipricetype_id = 1
    # col_param = 3
    # yumipricetype_id = 2
    # col_param = 10
    # yumipricetype_id = 3
    # col_param = 20
    # yumipricetype_id = 4
    # col_param = 35
    yumipricetype_id = 5
    col_param = 44
    for index in range(52,55):
        # year = table.cell(index, 3).value
        # month = table.cell(index, 4).value
        cell_time1 = table.cell(index, 0).value
        cell_time2 = table.cell(index, 1).value
        print(cell_time1, cell_time2, table.cell(index, 0).ctype)
        if 2 == table.cell(index, 0).ctype:
            dete = datetime(*xldate_as_tuple(cell_time1, 0)).strftime('%Y-%m-%d')
            year = dete.split('-')[0]
        month = int(cell_time2.split('月')[0])

        temp = table.cell(index, col_param).value
        if temp == 'X':
            monthly_price = 0
        else:
            monthly_price = temp
        print(year,month,monthly_price)
        item = YumiMonthlyPriceQuanguoAvg(
            year = year,
            month = month,
            yumipricetype_id = yumipricetype_id,
            monthly_price=monthly_price,
            comments=''
        )
        item_list.append(item)
    YumiMonthlyPriceQuanguoAvg.objects.bulk_create(item_list)

def read_monthly_yumi_province(file):
    '''
    read the infomation of enterprise name
    :return a list

    '''

    # province_list = [2,5,6,7,8]
    # province_list = [2, 5, 6, 7, 8,12,14,15]
    # province_list = [1,3,2,4,5,6,7,8,10,12,14,15,24]
    # province_list = [2, 5, 6, 7, 8, 14, 15]
    province_list = [9,11,19,13,16,17,18,20,28,21,22]
    # yumipricetype_id = 1
    # col_param = 4
    # yumipricetype_id = 2
    # col_param = 11
    # yumipricetype_id = 3
    # col_param = 21
    # yumipricetype_id = 4
    # col_param = 36
    yumipricetype_id = 5
    col_param = 45
    handle = open_excel(file)
    table = handle.sheet_by_index(3)
    item_list = []


    for key,val in enumerate(province_list):
        for index in range(52,55):
            # year = table.cell(index, 3).value
            # month = table.cell(index, 4).value
            cell_time1 = table.cell(index, 0).value
            cell_time2 = table.cell(index, 1).value
            print(cell_time1, cell_time2, table.cell(index, 0).ctype)
            if 2 == table.cell(index, 0).ctype:
                dete = datetime(*xldate_as_tuple(cell_time1, 0)).strftime('%Y-%m-%d')
                year = dete.split('-')[0]
            month = int(cell_time2.split('月')[0])

            temp = table.cell(index, key + col_param).value
            if temp == 'X':
                monthly_price = 0
            else:
                monthly_price = temp
            province_id = province_list[key]
            print(year,month, monthly_price,province_id)

            item = YumiMonthlyPriceProvince(
                year = year,
                month = month,
                province_id = province_id,
                yumipricetype_id = yumipricetype_id,
                monthly_price = monthly_price,
                comments = ''
            )
            item_list.append(item)
    YumiMonthlyPriceProvince.objects.bulk_create(item_list)




