# Generated by Django 2.0.4 on 2018-05-09 18:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_auto_20180509_1015'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='date_of_completion',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2018, 5, 9, 18, 42, 0, 709979)),
            preserve_default=False,
        ),
    ]
