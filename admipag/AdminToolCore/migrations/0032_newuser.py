# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminToolCore', '0031_office_desc'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_name', models.CharField(max_length=128, null=True, blank=True)),
                ('os_type', models.IntegerField(default=1, choices=[(0, b'Autre'), (1, b'Linux'), (2, b'Mac OS'), (3, b'Windows (7)')])),
            ],
            options={
                'ordering': ['last_name'],
            },
            bases=(models.Model,),
        ),
    ]
