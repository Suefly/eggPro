from django.db import models
# from basic.models import ProvinceStandard
# Create your models here.
####玉米

class YumiPriceType(models.Model):
    yumipricetype_id = models.AutoField(primary_key=True, verbose_name='序号')
    pricetypeName = models.CharField(max_length=16,verbose_name='价格分类名字')
    description = models.CharField(max_length=64, null=True, blank=True, verbose_name='描述')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')


class YumiDailyPriceQuanguoAvg(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    date = models.DateField(verbose_name='日期')
    yumipricetype = models.ForeignKey('YumiPriceType', on_delete=models.CASCADE, verbose_name='种类')
    daily_price = models.FloatField(blank=True, null=True, verbose_name='全国均价')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'yumi_dailypricequanguoavg'
        verbose_name = '玉米全国日均价'
        verbose_name_plural = '玉米全国日均价'

class YumiDailyPriceProvince(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    date = models.DateField(verbose_name='日期')
    province = models.ForeignKey('basic.Province', on_delete=models.CASCADE, verbose_name='省份')
    yumipricetype = models.ForeignKey('YumiPriceType', on_delete=models.CASCADE, verbose_name='种类')
    daily_price = models.FloatField(blank=True, null=True, verbose_name='全国均价')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'yumi_dailypriceprovince'
        verbose_name = '玉米各省份日均价'
        verbose_name_plural = '玉米各省份日均价'


class YumiWeeklyPriceQuanguoAvg(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    weekNum = models.IntegerField(verbose_name='第几周')
    yumipricetype = models.ForeignKey('YumiPriceType', on_delete=models.CASCADE, verbose_name='种类')
    weekly_price = models.FloatField(blank=True, null=True, verbose_name='全国均价')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'yumi_weeklypricequanguoavg'
        verbose_name = '玉米全国周均价'
        verbose_name_plural = '玉米全国周均价'

class YumiWeeklyPriceProvince(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    weekNum = models.IntegerField(verbose_name='第几周')
    province = models.ForeignKey('basic.Province', on_delete=models.CASCADE, verbose_name='省份')
    yumipricetype = models.ForeignKey('YumiPriceType', on_delete=models.CASCADE, verbose_name='种类')
    weekly_price = models.FloatField(blank=True, null=True, verbose_name='全国均价')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'yumi_weeklypriceprovince'
        verbose_name = '玉米各省份周均价'
        verbose_name_plural = '玉米各省份周均价'

class YumiMonthlyPriceQuanguoAvg(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    month = models.IntegerField(verbose_name='几月')
    yumipricetype = models.ForeignKey('YumiPriceType', on_delete=models.CASCADE, verbose_name='种类',default=1)
    monthly_price = models.FloatField(blank=True, null=True, verbose_name='全国均价')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'yumi_monthlypricequanguoavg'
        verbose_name = '玉米全国月均价'
        verbose_name_plural = '玉米全国月均价'

class YumiMonthlyPriceProvince(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    month = models.IntegerField(verbose_name='几月')
    province = models.ForeignKey('basic.Province', on_delete=models.CASCADE, verbose_name='省份')
    yumipricetype = models.ForeignKey('YumiPriceType', on_delete=models.CASCADE, verbose_name='种类',default=1)
    monthly_price = models.FloatField(blank=True, null=True, verbose_name='全国均价')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'yumi_monthlypriceprovince'
        verbose_name = '玉米各省份月均价'
        verbose_name_plural = '玉米各省份月均价'

class YumiDailyPriceDetail(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='序号')
    date = models.DateField(verbose_name='日期')
    yumicity = models.ForeignKey('basic.City',on_delete=models.CASCADE,verbose_name='城市/港口')
    yumipricetype = models.ForeignKey('YumiPriceType', on_delete=models.CASCADE, verbose_name='玉米分类')
    dailyprice = models.FloatField(blank=True, null=True,verbose_name='日度价格')
    comments = models.CharField(max_length=256, blank=True, null=True,verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'yumi_dailypricedetail'
        verbose_name = '玉米各地区日度价格'
        verbose_name_plural = '玉米各地区日度价格'
