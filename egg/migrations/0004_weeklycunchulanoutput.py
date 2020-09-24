# Generated by Django 2.0.3 on 2020-08-26 03:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('egg', '0003_auto_20200826_1020'),
    ]

    operations = [
        migrations.CreateModel(
            name='WeeklyCunchulanOutput',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('year', models.IntegerField(verbose_name='年份')),
                ('weekNum', models.IntegerField(verbose_name='第几周')),
                ('chanliang_type', models.IntegerField(choices=[(1, '祖代蛋鸡存栏量（育成期、产蛋期）'), (2, '父母代蛋鸡存栏量（育成期、产蛋期）'), (3, '商品代蛋鸡存栏量（育成期、产蛋期）'), (4, '商品代蛋雏鸡一日龄销售量'), (5, '鸡蛋产量（高产配套系鸡蛋产量）')])),
                ('chanliang_value', models.BigIntegerField(verbose_name='产量值')),
                ('comments', models.CharField(blank=True, max_length=64, null=True, verbose_name='备注')),
            ],
        ),
    ]
