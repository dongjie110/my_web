# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-29 01:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_tag_code'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('price', models.FloatField()),
                ('author', models.CharField(max_length=128)),
                ('publish_date', models.DateField()),
                ('category', models.CharField(max_length=128)),
            ],
        ),
    ]