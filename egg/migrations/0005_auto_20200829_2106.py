# Generated by Django 2.0.3 on 2020-08-29 13:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('egg', '0004_weeklycunchulanoutput'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dailypriceprovince',
            name='pricetype',
        ),
        migrations.RemoveField(
            model_name='dailypriceprovince',
            name='province',
        ),
        migrations.DeleteModel(
            name='DailyPriceProvince',
        ),
    ]
