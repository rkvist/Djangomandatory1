# Generated by Django 3.0.5 on 2020-04-15 11:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('check_in_out', '0004_auto_20200415_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='check_in_out',
            name='loan_datetime',
            field=models.DateTimeField(default=datetime.datetime(2020, 4, 15, 11, 16, 16, 282242)),
        ),
    ]
