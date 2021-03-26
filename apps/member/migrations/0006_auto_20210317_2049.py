# Generated by Django 3.1.7 on 2021-03-17 17:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0005_member_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='member',
            name='token',
            field=models.CharField(default='', max_length=4, verbose_name='Sms Token'),
        ),
        migrations.AlterField(
            model_name='member',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='active'),
        ),
        migrations.AlterField(
            model_name='member',
            name='phone_number',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True, validators=[django.core.validators.RegexValidator(message="Phone number must be entered in the format: '09121234567'.                                  Up to 11 digits allowed.", regex='09[0-3][0-9]-?[0-9]{3}-?[0-9]{4}')]),
        ),
    ]
