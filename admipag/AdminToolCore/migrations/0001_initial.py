# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('uidnumber', models.IntegerField(serialize=False, primary_key=True)),
                ('login', models.CharField(unique=True, max_length=64)),
                ('manager', models.ForeignKey(to='AdminToolCore.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
