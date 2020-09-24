from django.test import TestCase

# Create your tests here.
#-*- coding: utf-8 -*-
import xlrd
from basic.models import Province
import xlwt
from datetime import datetime
from xlrd import xldate_as_tuple
from futures.models import *
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


def get_province_id(province_name):
    province_id = 0
    try:
        province_id = Province.objects.values('province_id').filter(provinceName=province_name)[0]['province_id']
    except Exception as e:
        print('Error')
    return province_id

def get_company_id(company_name):
    company_id = 0
    try:
        company_id = FuturesCompany.objects.values('futurescompany_id').filter(companyName__contains=company_name)[0]['futurescompany_id']
    except Exception as e:
        print('Error')
    return company_id


def read_daily_futures_price(file):

    handle = open_excel(file)
    table = handle.sheet_by_index(0)
    item_list = []
    for index in range(1, 1639):
        cell = table.cell(index, 2).value
        temp = table.cell(index, 4).value
        xianhuo = table.cell(index, 3).value
        print(cell, temp,table.cell(index, 4).ctype)
        if 3 == table.cell(index, 2).ctype:
            date = datetime(*xldate_as_tuple(cell, 0)).strftime('%Y-%m-%d')

        if temp == 'X':
            eggFuturePrice = 0
        else:
            eggFuturePrice = temp

        if xianhuo == 'X':
            xianhuoPrice = 0
        else:
            xianhuoPrice = xianhuo

        item = EggMainPrice(
            date = date,
            eggFuturePrice= eggFuturePrice,
            xianhuoPrice = xianhuoPrice,
            comments=''
        )
        item_list.append(item)
    EggMainPrice.objects.bulk_create(item_list)


def read_qihuo_company(file):

    handle = open_excel(file)
    table = handle.sheet_by_index(0)
    item_list = []
    for index in range(1, 150):
        conmanyName = table.cell(index, 3).value
        conmanyFullName = table.cell(index, 2).value
        provinceName = table.cell(index, 1).value
        print('provinceName',provinceName)
        province_id = get_province_id(provinceName)

        item = FuturesCompany(
            companyName= conmanyName,
            companyFullName = conmanyFullName,
            province_id = province_id,
            comments=''
        )
        item_list.append(item)
    FuturesCompany.objects.bulk_create(item_list)


def read_chicang_info(file):

    handle = open_excel(file)
    table = handle.sheet_by_index(0)
    item_list = []
    for index in range(4, 24):
        companyName = table.cell(index, 9).value
        chicang_value = int(table.cell(index, 10).value.replace(',',''))
        fluctuate = int(table.cell(index, 11).value.replace(',',''))

        futurescompany_id = get_company_id(companyName)

        item = ChicangInfo(
            date = '2020-09-09',
            duo_kong_flag = 2,
            futurescompany_id = futurescompany_id,
            chicang_value = chicang_value,
            fluctuate = fluctuate,
            comments=''
        )
        item_list.append(item)
    ChicangInfo.objects.bulk_create(item_list)


if __name__ == '__main__':
    file = 'C:\\Users\\sujie\\Desktop\\数据库项目\\蛋鸡\\鸡蛋期货连续合约图.xlsx'
    file = 'C:\\Users\\sujie\\Desktop\\数据库项目\\蛋鸡\\20200909_jd2010.xls'
    file = 'C:\\Users\\sujie\\Desktop\\数据库项目\\蛋鸡\\期货公司.xls'

    read_daily_futures_price(file)

