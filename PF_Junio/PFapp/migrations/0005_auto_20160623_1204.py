# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-23 12:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PFapp', '0004_auto_20160623_1106'),
    ]

    operations = [
        migrations.CreateModel(
            name='Titles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=32)),
                ('title', models.CharField(max_length=256)),
            ],
        ),
        migrations.DeleteModel(
            name='UserPrefs',
        ),
    ]
