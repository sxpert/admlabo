# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AdminToolCore', '0029_auto_20150327_1249'),
    ]

    operations = [
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ref', models.CharField(max_length=16)),
            ],
            options={
                'ordering': ['ref'],
            },
            bases=(models.Model,),
        ),
    ]
