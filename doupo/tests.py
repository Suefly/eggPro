from django.test import TestCase

# Create your tests here.
#-*- coding: utf-8 -*-
import xlrd
from basic.models import Province
import xlwt
from datetime import datetime
from xlrd import xldate_as_tuple
from doupo.models import *
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


def read_daily_quanguo_doupo(file):
    # doupolevel_id = 1
    # col_param = 3

    doupolevel_id = 2
    col_param = 23
    handle = open_excel(file)
    table = handle.sheet_by_index(1)
    item_list = []
    for index in range(1496, 1587):
        cell = table.cell(index, 0).value
        temp = table.cell(index, col_param).value
        if 3 == table.cell(index, 0).ctype:
            date = datetime(*xldate_as_tuple(cell, 0)).strftime('%Y-%m-%d')
        if temp == 'X':
            daily_price = 0
        else:
            daily_price = temp
        print(date,daily_price)
        item = DoupoDailyPriceQuanguoAvg(
            date = date,
            doupolevel_id= doupolevel_id,
            daily_price=daily_price,
            comments=''
        )
        item_list.append(item)
    DoupoDailyPriceQuanguoAvg.objects.bulk_create(item_list)

if __name__ == '__main__':
    file = 'C:\\Users\\sujie\\Desktop\\数据库项目\\各栏目数据\\维生素-柳晓峰.xlsx'
    read_daily_quanguo_doupo(file)