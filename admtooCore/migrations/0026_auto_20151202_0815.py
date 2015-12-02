# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0025_auto_20151202_0811'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailalertmessage',
            name='sender',
            field=models.TextField(default=b'', blank=True),
            preserve_default=True,
        ),
    ]
