#-*- coding: utf-8 -*-
import xlrd
import xlwt
from datetime import datetime
from xlrd import xldate_as_tuple
from vitamin.models import *

def open_excel(file):
    try:
        data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(str(e))


def read_vitzmin_weekly_price(file):
    vitamin_type_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10,11, 12, 13, 14, 15, 16, 17, 18]
    handle = open_excel(file)
    table = handle.sheet_by_index(1)
    # item_list = []

    for key,val in enumerate(vitamin_type_list):
        item_list = []
        for index in range(3, 639):
            year = int(table.cell(index, 0).value.split('年')[0])
            week = int(table.cell(index, 1).value.split('周')[0])
            temp = table.cell(index,key+3).value
            if temp == 'X':
                weekly_price = 0
            else:
                weekly_price = temp
            vtpye_id = vitamin_type_list[key]

            item = VitaminWeeklyPrice(
                year = year,
                weekNum = week,
                vitamintype_id = vtpye_id,
                weeklyprice = weekly_price,
                comments = ''
            )
            item_list.append(item)
        VitaminWeeklyPrice.objects.bulk_create(item_list)


if __name__ == '__main__':
    file = 'C:\\Users\\sujie\\Desktop\\数据库项目\\各栏目数据\\维生素-柳晓峰.xlsx'
    read_vitzmin_weekly_price(file)
