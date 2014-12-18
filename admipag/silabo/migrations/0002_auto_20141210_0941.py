# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silabo', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='manager',
            field=models.ForeignKey(to='silabo.User', null=True),
            preserve_default=True,
        ),
    ]
