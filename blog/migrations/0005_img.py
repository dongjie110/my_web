# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-29 07:57
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_myuser'),
    ]

    operations = [
        migrations.CreateModel(
            name='Img',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('img', models.ImageField(upload_to='image/%Y/%m/%d/')),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Book')),
            ],
        ),
    ]