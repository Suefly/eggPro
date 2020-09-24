from django.db import models

# Create your models here.
class DoupoDailyPriceQuanguoAvg(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    date = models.DateField(verbose_name='日期')
    doupolevel = models.ForeignKey('ProductLevel', on_delete=models.CASCADE, verbose_name='豆粕等级',default=1)
    daily_price = models.FloatField(blank=True, null=True, verbose_name='全国均价')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'doupo_dailypricequanguoavg'
        verbose_name = '豆粕全国日均价'
        verbose_name_plural = verbose_name

class DoupoDailyPriceProvince(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    date = models.DateField(verbose_name='日期')
    province = models.ForeignKey('basic.Province', on_delete=models.CASCADE, verbose_name='省份')
    doupolevel = models.ForeignKey('ProductLevel', on_delete=models.CASCADE, verbose_name='豆粕等级', default=1)
    daily_price = models.FloatField(blank=True, null=True, verbose_name='各省价格')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'doupo_dailypriceprovince'
        verbose_name = '豆粕各省份日均价'
        verbose_name_plural = '豆粕各省份日均价'

class DoupoWeeklyPriceQuanguoAvg(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    weekNum = models.IntegerField(verbose_name='第几周')
    doupolevel = models.ForeignKey('ProductLevel', on_delete=models.CASCADE, verbose_name='豆粕等级',default=1)
    weekly_price = models.FloatField(blank=True, null=True, verbose_name='全国均价')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'doupo_weeklypricequanguoavg'
        verbose_name = '豆粕全国周均价'
        verbose_name_plural = verbose_name

class DoupoWeeklyPriceProvince(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    weekNum = models.IntegerField(verbose_name='第几周')
    province = models.ForeignKey('basic.Province', on_delete=models.CASCADE, verbose_name='省份')
    doupolevel = models.ForeignKey('ProductLevel', on_delete=models.CASCADE, verbose_name='豆粕等级',default=1)
    weekly_price = models.FloatField(blank=True, null=True, verbose_name='全国均价')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'doupo_weeklypriceprovince'
        verbose_name = '豆粕各省份周均价'
        verbose_name_plural = verbose_name

class DoupoMonthlyPriceQuanguoAvg(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    month = models.IntegerField(verbose_name='几月')
    doupolevel = models.ForeignKey('ProductLevel', on_delete=models.CASCADE, verbose_name='豆粕等级',default=1)
    monthly_price = models.FloatField(blank=True, null=True, verbose_name='全国均价')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'doupo_monthlypricequanguoavg'
        verbose_name = '豆粕全国月均价'
        verbose_name_plural = verbose_name

class DoupoMonthlyPriceProvince(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    month = models.IntegerField(verbose_name='几月')
    province = models.ForeignKey('basic.Province', on_delete=models.CASCADE, verbose_name='省份')
    doupolevel = models.ForeignKey('ProductLevel', on_delete=models.CASCADE, verbose_name='豆粕等级',default=1)
    monthly_price = models.FloatField(blank=True, null=True, verbose_name='全国均价')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'doupo_monthlypriceprovince'
        verbose_name = '豆粕各省份月均价'
        verbose_name_plural = verbose_name

class DoupoDailyPriceDetail(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='序号')
    date = models.DateField(verbose_name='日期')
    doupocity = models.ForeignKey('basic.City',on_delete=models.CASCADE,verbose_name='城市/港口')
    doupolevel = models.ForeignKey('ProductLevel', on_delete=models.CASCADE, verbose_name='豆粕等级')
    dailyprice = models.FloatField(blank=True, null=True,verbose_name='日度价格')
    comments = models.CharField(max_length=256, blank=True, null=True,verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'doupo_dailypricedetail'
        verbose_name = '豆粕各地区日度价格'
        verbose_name_plural = verbose_name


class ProductLevel(models.Model):
    doupolevel_id = models.AutoField(primary_key=True, verbose_name='序号')
    levelName = models.CharField(max_length=16,verbose_name='等级')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.levelName
    class Meta:
        # managed = False
        db_table = 'doupo_productlevel'
        verbose_name = '豆粕等级表'
        verbose_name_plural = verbose_name