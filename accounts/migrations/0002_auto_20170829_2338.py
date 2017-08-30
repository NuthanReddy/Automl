# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-08-29 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='userprofile',
            managers=[
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='description',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='website',
            field=models.URLField(default='', max_length=100),
        ),
    ]