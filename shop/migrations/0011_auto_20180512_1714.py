# Generated by Django 2.0.4 on 2018-05-12 17:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0010_auto_20180512_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='cutter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='orders', to=settings.AUTH_USER_MODEL),
        ),
    ]
