# Generated by Django 2.0.3 on 2020-09-10 06:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('futures', '0011_auto_20200910_1419'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChicangInfo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('date', models.DateField(verbose_name='日期')),
                ('duo_kong_flag', models.IntegerField(choices=[(1, '多：买进'), (2, '空：卖出')], verbose_name='多空选择')),
                ('chicang_value', models.BigIntegerField(verbose_name='持仓量')),
                ('fluctuate', models.BigIntegerField(verbose_name='增减')),
                ('comments', models.CharField(blank=True, max_length=64, null=True, verbose_name='备注')),
                ('futurescompany', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='futures.FuturesCompany', verbose_name='期货公司')),
            ],
        ),
    ]
