# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-26 03:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tag',
            name='code',
            field=models.IntegerField(null=True, verbose_name='\u7f16\u7801'),
        ),
    ]
