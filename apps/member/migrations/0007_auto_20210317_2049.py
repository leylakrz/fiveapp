# Generated by Django 3.1.7 on 2021-03-17 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0006_auto_20210317_2049'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='token',
            field=models.CharField(max_length=4, verbose_name='Sms Token'),
        ),
    ]