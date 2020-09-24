from django.db import models

# Create your models here.

from django.db import models

# Create your models here.
class VitaminType(models.Model):
    vitamintype_id = models.AutoField(primary_key=True,verbose_name='序号')
    vitaminName = models.CharField(max_length=64,verbose_name='维生素类别')
    danwei = models.CharField(max_length=64, blank=True, null=True,verbose_name='单位')
    dataFrom = models.CharField(max_length=64, blank=True, null=True,verbose_name='数据来源')
    comments = models.CharField(max_length=64, blank=True, null=True, verbose_name='备注')
    class Meta:
        db_table = 'vitamin_producttype'
        app_label = 'vitamin'
        verbose_name = '维生素类别'
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.vitaminName

class VitaminDailyPrice(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    date = models.DateField(verbose_name='日期')
    vitamintype = models.ForeignKey('VitaminType',on_delete=models.CASCADE,verbose_name='维生素类型')
    dailyprice = models.FloatField(blank=True, null=True,verbose_name='日度价格')
    comments = models.CharField(max_length=64, blank=True, null=True,verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'vitamin_dailyprice'

class VitaminWeeklyPrice(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    weekNum = models.IntegerField(verbose_name='周度')
    vitamintype = models.ForeignKey('VitaminType',on_delete=models.CASCADE,verbose_name='维生素类型')
    weeklyprice = models.FloatField(verbose_name='周度价格',blank=True, null=True)
    comments = models.CharField(verbose_name='备注',max_length=64, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'vitamin_weeklyprice'
        app_label = 'vitamin'
        verbose_name = '维生素周度价格'
        verbose_name_plural = verbose_name


class VitaminMonthlyPrice(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    month = models.IntegerField(verbose_name='月份')
    vitamintype = models.ForeignKey('VitaminType', on_delete=models.CASCADE, verbose_name='维生素类型')
    monthlyprice = models.FloatField(blank=True, null=True,verbose_name='月度价格')
    comments = models.CharField(max_length=64, blank=True, null=True,verbose_name='备注')

    class Meta:
        managed = False
        db_table = 'vitamin_monthlyprice'




