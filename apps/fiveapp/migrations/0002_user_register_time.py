# Generated by Django 3.1.7 on 2021-02-24 18:10

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('fiveapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='register_time',
            field=models.DateTimeField(default=datetime.datetime(2021, 2, 24, 18, 10, 56, 599671, tzinfo=utc), verbose_name='Registered At'),
        ),
    ]