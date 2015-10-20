# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0005_auto_20151019_1407'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserGroupHistory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('action', models.IntegerField(choices=[(0, b'ADD'), (1, b'DEL')])),
                ('data', models.TextField(default=b'', blank=True)),
                ('user', models.ForeignKey(to='admtooCore.User')),
            ],
            options={
                'ordering': ['created'],
                'get_latest_by': 'created',
            },
            bases=(models.Model,),
        ),
    ]
