# Generated by Django 2.0.3 on 2020-09-04 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vitamin', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vitaminweeklyprice',
            name='vitamintype',
        ),
        migrations.DeleteModel(
            name='VitaminWeeklyPrice',
        ),
    ]
