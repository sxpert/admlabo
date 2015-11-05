# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0015_userflag_label'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserAppSpecName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ref', models.CharField(unique=True, max_length=64, db_index=True)),
                ('name', models.CharField(max_length=64, null=True, blank=True)),
                ('label', models.CharField(max_length=255, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
