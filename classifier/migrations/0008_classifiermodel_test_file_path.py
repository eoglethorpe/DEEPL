# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-14 10:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classifier', '0007_classifiermodel_metadata'),
    ]

    operations = [
        migrations.AddField(
            model_name='classifiermodel',
            name='test_file_path',
            field=models.CharField(max_length=250, null=True),
        ),
    ]