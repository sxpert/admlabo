# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0012_auto_20151022_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='data',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
