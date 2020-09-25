from django.db import models

# Create your models here.
from django.db import models
# from django.contrib.auth.models import AbstractUser

# Create your models here.

class PriceType(models.Model):
    pricetype_id = models.AutoField(primary_key=True,verbose_name='序号')
    pricetypeName = models.CharField(max_length=15, blank=True, null=True, verbose_name='生猪产品类型')
    description = models.CharField(max_length=32, blank=True, null=True, verbose_name='描述')
    comments = models.CharField(max_length=64,blank=True,null=True,verbose_name='备注')
    class Meta:
        # managed = False
        db_table = 'egg_pricetype'
        verbose_name = '价格类型'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pricetypeName

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
    # area = models.ForeignKey('Area',on_delete=models.CASCADE,verbose_name='所属大区',null=True, blank=True)
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    def __str__(self):
        return self.cityName


class DanDailyPriceImportFile(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='序号')
    file = models.FileField(upload_to='./upload/DanPrice/',verbose_name='上传文件')
    date = models.DateField(verbose_name='日期选择')
    name = models.CharField(max_length=32, verbose_name='文件名')
    comments = models.CharField(max_length=64,null=True,blank=True,verbose_name='备注')
    class Meta:
        # managed = False
        db_table = 'egg_dandailypriceimportfile'
        verbose_name = '鸡蛋日度价格(Excel导入)'
        verbose_name_plural = '鸡蛋日度价格(Excel导入)'
    def __str__(self):
        return self.name


class TaotaijiDailyPriceImportFile(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='序号')
    file = models.FileField(upload_to='./upload/TaotaijiPrice/',verbose_name='上传文件')
    date = models.DateField(verbose_name='日期选择')
    name = models.CharField(max_length=32, verbose_name='文件名')
    comments = models.CharField(max_length=64,null=True,blank=True,verbose_name='备注')
    class Meta:
        # managed = False
        db_table = 'egg_taotaijidailypriceimportfile'
        verbose_name = '淘汰鸡日度价格(Excel导入)'
        verbose_name_plural = '淘汰鸡日度价格(Excel导入)'
    def __str__(self):
        return self.name


class DailyPriceDetail(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='序号')
    date = models.DateField(verbose_name='日期')
    city = models.ForeignKey('City',on_delete=models.CASCADE,verbose_name='城市/区')
    pricetype = models.ForeignKey('PriceType',on_delete=models.CASCADE,verbose_name='价格类型')
    dailyprice = models.FloatField(blank=True, null=True,verbose_name='日度价格')
    comments = models.CharField(max_length=256, blank=True, null=True,verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'egg_dailypricedetail'
        verbose_name = '各地市区鸡蛋日度价格'
        verbose_name_plural = '各地市区鸡蛋日度价格'
    def __str__(self):
        return self.comments

class DailyPriceProvince(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='序号')
    date = models.DateField(verbose_name='日期')
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name='省份')
    pricetype = models.ForeignKey('PriceType', on_delete=models.CASCADE, verbose_name='价格类型')
    p_daily_price = models.FloatField(blank=True, null=True, verbose_name='省均价')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')
    class Meta:
        # managed = False
        db_table = 'egg_dailypriceprovince'
        verbose_name = '鸡蛋省级日均价'
        verbose_name_plural = '鸡蛋省级日均价'

class DailyPriceQGAvg(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='序号')
    date = models.DateField(verbose_name='日期')
    pricetype = models.ForeignKey('PriceType', on_delete=models.CASCADE, verbose_name='价格类型')
    daily_price = models.FloatField(blank=True, null=True, verbose_name='全国均价')
    chan_dailyprice = models.FloatField(blank=True, null=True, verbose_name='主产区均价')
    xiao_dailyprice = models.FloatField(blank=True, null=True, verbose_name='主销区均价')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')
    class Meta:
        # managed = False
        db_table = 'egg_dailypriceqgavg'
        verbose_name = '鸡蛋全国日均价'
        verbose_name_plural = '鸡蛋全国日均价'


class WeeklyPriceProvince(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    weekNum = models.IntegerField(verbose_name='周度')
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name='省份')
    pricetype = models.ForeignKey('PriceType', on_delete=models.CASCADE, verbose_name='价格类型')
    p_weekly_price = models.FloatField(blank=True, null=True, verbose_name='省均价')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')
    class Meta:
        # managed = False
        db_table = 'egg_weeklypriceprovince'
        verbose_name = '鸡蛋省级周度均价'
        verbose_name_plural = '鸡蛋省级周度均价'

class WeeklyPriceQGAvg(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    weekNum = models.IntegerField(verbose_name='周度')
    pricetype = models.ForeignKey('PriceType', on_delete=models.CASCADE, verbose_name='价格类型')
    weekly_price = models.FloatField(blank=True, null=True,verbose_name='周价')
    chan_weeklyprice = models.FloatField(blank=True, null=True, verbose_name='主产区均价')
    xiao_weeklyprice = models.FloatField(blank=True, null=True, verbose_name='主销区均价')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'egg_weeklypriceqgavg'
        verbose_name = '鸡蛋全国周度价格均价'
        verbose_name_plural = '鸡蛋全国周度价格均价'


class MonthlyPriceQGAvg(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    month = models.IntegerField(verbose_name='月份')
    pricetype = models.ForeignKey('PriceType', on_delete=models.CASCADE, verbose_name='价格类型')
    month_price = models.FloatField(blank=True, null=True,verbose_name='月价')
    chan_monthlyprice = models.FloatField(blank=True, null=True, verbose_name='主产区均价')
    xiao_monthlyprice = models.FloatField(blank=True, null=True, verbose_name='主销区均价')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'egg_monthlypriceqgavg'
        verbose_name = '鸡蛋全国月度价格均价'
        verbose_name_plural = '鸡蛋全国月度价格均价'

class MonthlyPriceProvince(models.Model):
    id = models.AutoField(primary_key=True,verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    month = models.IntegerField(verbose_name='周度')
    pricetype = models.ForeignKey('PriceType', on_delete=models.CASCADE, verbose_name='价格类型')
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name='省份')
    p_monthly_price = models.FloatField(blank=True, null=True, verbose_name='省均价')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')
    class Meta:
        # managed = False
        db_table = 'egg_monthlypriceprovince'
        verbose_name = '省级月度均价'
        verbose_name_plural = '省级月度均价'

##############################################
## cost   profit
##############################################
class WeeklyCostQGAvg(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    weekNum = models.IntegerField(verbose_name='第几周')
    cost_value = models.FloatField(verbose_name='成本')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'egg_weeklycostqgavg'
        verbose_name = '蛋鸡养殖全国周度成本'
        verbose_name_plural = '蛋鸡养殖全国周度成本'

class MonthlyCostQGAvg(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    month = models.IntegerField(verbose_name='几月')
    cost_value = models.FloatField(verbose_name='成本')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'egg_monthlycostqgavg'
        verbose_name = '蛋鸡养殖全国月度成本'
        verbose_name_plural = '蛋鸡养殖全国月度成本'


class WeeklyCostProvince(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    weekNum = models.IntegerField(verbose_name='第几周')
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name='省份')
    cost_value = models.FloatField(verbose_name='成本')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

class MonthlyCostProvince(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    month = models.IntegerField(verbose_name='几月')
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name='省份')
    cost_value = models.FloatField(verbose_name='成本')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')


class WeeklyProfitQGAvg(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    weekNum = models.IntegerField(verbose_name='第几周')
    profit_value = models.FloatField(verbose_name='盈利（利润）')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    # class Meta:
    #     # managed = False
    #     db_table = 'pig_weeklyquanguoyingli'
    #     verbose_name = '养殖全国周度盈利'
    #     verbose_name_plural = '养殖全国周度盈利'


class MonthlyProfitQGAvg(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    month = models.IntegerField(verbose_name='几月')
    profit_value = models.FloatField(verbose_name='盈利（利润）')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    # class Meta:
    #     # managed = False
    #     db_table = 'pig_monthlyquanguoyingli'
    #     verbose_name = '养殖全国月度盈利'
    #     verbose_name_plural = '养殖全国月度盈利'

class WeeklyProfitProvince(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    weekNum = models.IntegerField(verbose_name='第几周')
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name='省份')
    profit_value = models.FloatField(verbose_name='盈利（利润）')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

class MonthlyProfitProvince(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    month = models.IntegerField(verbose_name='几月')
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name='省份')
    profit_value = models.FloatField(verbose_name='盈利（利润）')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')



########################################################################
## 存出栏和产量
########################################################################
class WeeklyCunchulanOutput(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    weekNum = models.IntegerField(verbose_name='第几周')
    chanliang_type_choice = (
        (1, "祖代蛋鸡存栏量（育成期、产蛋期）"),
        (2, "父母代种鸡-育成期平均存栏量"),
        (3, "父母代种鸡-产蛋期平均存栏量"),
        (4, "父母代种鸡-总存栏量"),
        (5, "商品代蛋雏鸡销售量"),
        (6, "商品代蛋鸡育成期总存栏量"),
        (7, "商品代蛋鸡产蛋期总存栏量"),
        (8, "商品代蛋鸡总存栏量"),
        (9, "鸡蛋产量-总重量"),
        (10, "鸡蛋产量-总数量"),
        (11, "淘汰鸡总数量")
    )
    chanliang_type = models.IntegerField(choices=chanliang_type_choice)
    chanliang_value = models.BigIntegerField(verbose_name='产量值')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')



#### 豆粕价格

class DoupoDailyPriceQuanguoAvg(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    date = models.DateField(verbose_name='日期')
    doupo_level_choice = (
        (1, "普通豆粕"),
        (2, "高等豆粕"),
    )
    doupo_level = models.IntegerField(choices=doupo_level_choice,verbose_name='豆粕等级')
    daily_price = models.FloatField(blank=True, null=True, verbose_name='全国均价')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'egg_doupodailypricequanguoavg'
        verbose_name = '豆粕全国日均价'
        verbose_name_plural = '豆粕全国日均价'

class DoupoDailyPriceProvince(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    date = models.DateField(verbose_name='日期')
    doupo_level_choice = (
        (1, "普通豆粕"),
        (2, "高等豆粕"),
    )
    doupolevel = models.IntegerField(choices=doupo_level_choice,verbose_name='豆粕等级')
    province = models.ForeignKey('Province', on_delete=models.CASCADE, verbose_name='省份',default=1)
    daily_price = models.FloatField(blank=True, null=True, verbose_name='全国均价')
    comments = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'egg_doupodailypriceprovince'
        verbose_name = '豆粕各省份日均价'
        verbose_name_plural = '豆粕各省份日均价'

    def __str__(self):
        return self.province



class WeeklyDanjiLeijiProfit(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    date = models.DateField(verbose_name='日期')
    originYear = models.IntegerField(verbose_name='入舍年份')
    originWeek = models.IntegerField(verbose_name='入舍周度')
    year = models.IntegerField(verbose_name='年份')
    weekNum = models.IntegerField(verbose_name='周度')
    shengchanWeek = models.IntegerField(verbose_name='生产周编号', default=1,null=True,blank=True)
    leijiProfit = models.FloatField(blank=True, null=True, verbose_name='累计利润')
    Remark = models.CharField(max_length=64, null=True, blank=True, verbose_name='备注')



