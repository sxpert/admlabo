# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0003_auto_20151014_0302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='appspecname',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
