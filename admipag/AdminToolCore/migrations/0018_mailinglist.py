# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminToolCore', '0017_auto_20150122_1100'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('ml_id', models.CharField(max_length=64, serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('description', models.CharField(max_length=256)),
                ('group', models.ForeignKey(blank=True, to='AdminToolCore.Group', null=True)),
                ('parent', models.ForeignKey(blank=True, to='AdminToolCore.MailingList', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
