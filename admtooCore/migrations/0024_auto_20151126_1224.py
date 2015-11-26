# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0023_auto_20151123_1619'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='user_state',
            field=models.IntegerField(default=0, choices=[(0, b'utilisateur actif'), (1, b'utilisateur nouvellement import\xc3\xa9'), (2, b'utilisateur supprim\xc3\xa9'), (3, b'utilisateur cr\xc3\xa9\xc3\xa9 par erreur')]),
            preserve_default=True,
        ),
    ]
