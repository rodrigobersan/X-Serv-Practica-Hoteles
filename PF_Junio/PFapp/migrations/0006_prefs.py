# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-23 12:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PFapp', '0005_auto_20160623_1204'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prefs',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=32)),
                ('size', models.IntegerField()),
                ('face', models.CharField(max_length=32)),
            ],
        ),
    ]