# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0038_auto_20150407_1551'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDir',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=32, null=True, blank=True)),
                ('basedir', models.CharField(max_length=128, null=True, blank=True)),
                ('modes', models.CharField(max_length=4, null=True, blank=True)),
                ('machine', models.ForeignKey(blank=True, to='admtooCore.Machine', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
