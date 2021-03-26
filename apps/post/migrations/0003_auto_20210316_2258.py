# Generated by Django 3.1.7 on 2021-03-16 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_post_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='post', verbose_name='Photo'),
        ),
    ]
