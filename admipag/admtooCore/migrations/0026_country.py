# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0025_auto_20150325_1615'),
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('iso2', models.CharField(max_length=2, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('citizenship', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
            bases=(models.Model,),
        ),
    ]
