# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('silabo', '0002_auto_20141210_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='manager',
            field=models.ForeignKey(blank=True, to='silabo.User', null=True),
            preserve_default=True,
        ),
    ]
