# Generated by Django 3.0.5 on 2020-04-16 22:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('check_in_out', '0010_auto_20200416_1950'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check_in_out',
            name='checked_out_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 16, 22, 8, 39, 94534)),
        ),
    ]
