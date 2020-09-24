from django.db import models

# Create your models here.
class WeekDateStandard(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    Year = models.IntegerField(verbose_name='年份')
    WeekNum = models.IntegerField(verbose_name='周度')
    startDate = models.DateField(verbose_name='开始日期')
    endDate = models.DateField(verbose_name='结束日期')
    Remark = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

class MonthDateStandard(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    month = models.IntegerField(verbose_name='月份')
    startDate = models.DateField(verbose_name='开始日期')
    endDate = models.DateField(verbose_name='结束日期')
    Remark = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')


class Province(models.Model):
    province_id = models.AutoField(primary_key=True,verbose_name='序号')
    provinceName = models.CharField(max_length=16, blank=True, null=True,verbose_name='省份')
    cityContain = models.CharField(max_length=16, blank=True, null=True,verbose_name='包含城市')
    # area = models.ForeignKey('Area', on_delete=models.CASCADE, verbose_name='所属大区', null=True, blank=True)
    danSalesAreaFlag = models.IntegerField(verbose_name="鸡蛋产区",default=0) #1表示主产区，2表示主销区，3表示即是主产区，又是主销区
    tSalesAreaFlag = models.IntegerField(verbose_name="淘汰鸡产区",default=0)
    order = models.IntegerField(verbose_name='排序')
    EnglishName = models.CharField(max_length=32, null=True, blank=True, verbose_name='英文名字')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.provinceName

class City(models.Model):
    city_id = models.AutoField(primary_key=True,verbose_name='序号')
    cityName = models.CharField(max_length=16,verbose_name='城市')
    province = models.ForeignKey('Province',on_delete=models.CASCADE,verbose_name='所属省份')
    danSalesAreaFlag = models.IntegerField(verbose_name="鸡蛋产区", default=0)  # 1表示主产区，2表示主销区，3表示即是主产区，又是主销区
    tSalesAreaFlag = models.IntegerField(verbose_name="淘汰鸡产区", default=0)
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.cityName