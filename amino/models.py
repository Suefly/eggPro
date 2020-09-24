from django.db import models

# Create your models here.
class AminoType(models.Model):
    aminotype_id = models.AutoField(primary_key=True,verbose_name='序号')
    aminoName = models.CharField(max_length=64,verbose_name='氨基酸类别')
    comments = models.CharField(max_length=64, blank=True, null=True,verbose_name='备注')

    class Meta:
        db_table = 'amino_producttype'
        app_label = 'amino'
        verbose_name = '氨基酸类别'
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.aminoName

class AminoDailyPrice(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    date = models.DateField(verbose_name='日期')
    aminotype = models.ForeignKey('AminoType',on_delete=models.CASCADE,verbose_name='氨基酸类型')
    dailyprice = models.FloatField(blank=True, null=True,verbose_name='日度价格')
    comments = models.CharField(max_length=64, blank=True, null=True,verbose_name='备注')

    class Meta:
        # managed = False
        db_table = 'amino_dailyprice'

class AminoWeeklyPrice(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(verbose_name='年份')
    weekNum = models.IntegerField(verbose_name='周度')
    aminotype = models.ForeignKey('AminoType',on_delete=models.CASCADE,verbose_name='氨基酸类型')
    weeklyprice = models.FloatField(verbose_name='周度价格',blank=True, null=True)
    comments = models.CharField(verbose_name='备注',max_length=64, blank=True, null=True)

    class Meta:
        # managed = False
        db_table = 'amino_weeklyprice'
        app_label = 'amino'
        verbose_name = '氨基酸周度价格'
        verbose_name_plural = verbose_name


class AminoMonthlyPrice(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='序号')
    year = models.IntegerField(blank=True, null=True,verbose_name='年份')
    month = models.IntegerField(blank=True, null=True,verbose_name='分月')
    aminotype = models.ForeignKey('AminoType', on_delete=models.CASCADE, verbose_name='氨基酸类型')
    monthlyprice = models.FloatField(blank=True, null=True,verbose_name='月度价格')
    comments = models.CharField(max_length=64, blank=True, null=True,verbose_name='备注')

    class Meta:
        managed = False
        db_table = 'amino_monthlyprice'




