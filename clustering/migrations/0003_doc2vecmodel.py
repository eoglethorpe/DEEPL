# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-15 11:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('classifier', '0001_initial'),
        ('clustering', '0002_auto_20180330_1030'),
    ]

    operations = [
        migrations.CreateModel(
            name='Doc2VecModel',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='classifier.BaseModel')),
                ('name', models.CharField(max_length=100)),
                ('version', models.CharField(editable=False, max_length=20, unique=True)),
                ('modelpath', models.CharField(max_length=500)),
                ('pathtype', models.CharField(choices=[('FILE', 'File'), ('URL', 'Url')], default='FILE', max_length=50)),
            ],
            bases=('classifier.basemodel',),
        ),
    ]
