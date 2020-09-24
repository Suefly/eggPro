from django.db import models
import basic
# Create your models here.

class EggFuturesPrice(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    date = models.DateField(verbose_name='日期')
    futureCode = models.IntegerField(verbose_name='期货')
    eggFuturePrice = models.IntegerField(blank=True, null=True,verbose_name='期货价格')
    isMainFlag = models.IntegerField(blank=True, null=True,verbose_name='是否是主力合约')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'futures_eggfuturesprice'
        verbose_name = '期货价格'
        verbose_name_plural = '期货价格'


class EggMainPrice(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    date = models.DateField(verbose_name='日期')
    eggFuturePrice = models.IntegerField(blank=True, null=True, verbose_name='期货价格')
    xianhuoPrice = models.IntegerField(blank=True, null=True, verbose_name='现货价格')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')


class FuturesCompany(models.Model):
    futurescompany_id = models.AutoField(primary_key=True, verbose_name='序号')
    companyName = models.CharField(max_length=64, null=True, blank=True, verbose_name='期货公司名称')
    province = models.ForeignKey('basic.Province', on_delete=models.CASCADE, verbose_name='省份')
    companyFullName = models.CharField(max_length=64, null=True, blank=True, verbose_name='期货公司全名')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')


class ChicangInfo(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    date = models.DateField(verbose_name='日期')
    futurescompany = models.ForeignKey('FuturesCompany', on_delete=models.CASCADE, verbose_name='期货公司')
    duo_kong_choice = (
        (1, "多：买进"),
        (2, "空：卖出"),
    )
    duo_kong_flag = models.IntegerField(choices=duo_kong_choice, verbose_name='多空选择')
    chicang_value = models.BigIntegerField(verbose_name='持仓量')
    fluctuate = models.BigIntegerField(verbose_name='增减')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')




