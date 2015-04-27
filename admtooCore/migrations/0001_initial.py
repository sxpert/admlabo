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
				('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uidnumber', models.IntegerField(unique=True)),
                ('login', models.CharField(unique=True, max_length=64)),
                ('manager', models.ForeignKey(to='admtooCore.User')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
