# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminToolCore', '0006_auto_20141212_1323'),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('gidnumber', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('parent', models.ForeignKey(blank=True, to='AdminToolCore.Group', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
