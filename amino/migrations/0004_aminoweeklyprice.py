# Generated by Django 2.0.3 on 2020-09-04 16:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amino', '0003_auto_20200905_0018'),
    ]

    operations = [
        migrations.CreateModel(
            name='AminoWeeklyPrice',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='序号')),
                ('year', models.IntegerField(verbose_name='年份')),
                ('weekNum', models.IntegerField(verbose_name='周度')),
                ('weeklyprice', models.FloatField(blank=True, null=True, verbose_name='周度价格')),
                ('comments', models.CharField(blank=True, max_length=64, null=True, verbose_name='备注')),
                ('aminotype', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amino.AminoType', verbose_name='氨基酸类型')),
            ],
            options={
                'verbose_name': '氨基酸周度价格',
                'verbose_name_plural': '氨基酸周度价格',
                'db_table': 'amino_weeklyprice',
            },
        ),
    ]
