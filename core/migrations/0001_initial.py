# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-11-14 03:14
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BaseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('idx', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_on', models.DateTimeField(editable=False)),
                ('modified_on', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ClassifierModel',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.BaseModel')),
                ('name', models.CharField(max_length=100)),
                ('version', models.CharField(editable=False, max_length=20, unique=True)),
                ('_data', models.TextField(db_column='data')),
                ('accuracy', models.FloatField(default=0)),
                ('description', models.TextField()),
            ],
            bases=('core.basemodel',),
        ),
    ]