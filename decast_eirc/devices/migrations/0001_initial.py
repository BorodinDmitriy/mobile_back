# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-01 01:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='EIRCDevice',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('type', models.CharField(max_length=50)),
                ('reading', models.CharField(max_length=10)),
                ('date', models.DateTimeField(auto_now=True)),
                ('personal_account', models.CharField(max_length=50)),
                ('serial_number', models.CharField(max_length=50)),
            ],
        ),
    ]