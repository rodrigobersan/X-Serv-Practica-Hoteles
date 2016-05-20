# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-20 13:36
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Alojamientos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('url', models.URLField()),
                ('address', models.CharField(max_length=256)),
                ('zipcode', models.IntegerField()),
                ('country', models.CharField(max_length=256)),
                ('city', models.CharField(max_length=256)),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('date', models.DateTimeField()),
                ('alojamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PFapp.Alojamientos')),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('alojamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PFapp.Alojamientos')),
            ],
        ),
        migrations.CreateModel(
            name='UserSels',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.CharField(max_length=32)),
                ('date', models.DateTimeField()),
                ('alojamiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='PFapp.Alojamientos')),
            ],
        ),
    ]
