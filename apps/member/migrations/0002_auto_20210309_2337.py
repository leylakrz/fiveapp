# Generated by Django 3.1.7 on 2021-03-09 20:07

import apps.member.managers
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='member',
            managers=[
                ('objects', apps.member.managers.MemberManager()),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='active'),
        ),
        migrations.AddField(
            model_name='member',
            name='is_staff',
            field=models.BooleanField(default=False, verbose_name='staff'),
        ),
        migrations.AlterField(
            model_name='member',
            name='is_superuser',
            field=models.BooleanField(default=False, verbose_name='superuser'),
        ),
    ]
