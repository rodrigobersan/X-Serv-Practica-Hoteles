# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-06-22 15:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('PFapp', '0002_pagetitles'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PageTitles',
            new_name='Titles',
        ),
    ]