# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-09-07 18:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('comp', '0002_auto_20170905_1909'),
    ]

    operations = [
        migrations.AlterField(
            model_name='competition',
            name='bronze',
            field=models.IntegerField(default=50),
        ),
        migrations.AlterField(
            model_name='competition',
            name='gold',
            field=models.IntegerField(default=100),
        ),
        migrations.AlterField(
            model_name='competition',
            name='prize10',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='competition',
            name='prize4',
            field=models.IntegerField(default=30),
        ),
        migrations.AlterField(
            model_name='competition',
            name='prize5',
            field=models.IntegerField(default=20),
        ),
        migrations.AlterField(
            model_name='competition',
            name='prize6',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='competition',
            name='prize7',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='competition',
            name='prize8',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='competition',
            name='prize9',
            field=models.IntegerField(default=10),
        ),
        migrations.AlterField(
            model_name='competition',
            name='silver',
            field=models.IntegerField(default=70),
        ),
        migrations.AlterField(
            model_name='submission',
            name='score',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=64),
        ),
    ]
