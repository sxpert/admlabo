# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0008_auto_20151021_1101'),
    ]

    operations = [
        migrations.AddField(
            model_name='newuser',
            name='os_lang',
            field=models.IntegerField(default=0, choices=[(0, b'Fran\xc3\xa7ais'), (1, b'Anglais')]),
            preserve_default=True,
        ),
    ]
