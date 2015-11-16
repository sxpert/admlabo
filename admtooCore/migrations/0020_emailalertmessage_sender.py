# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0019_auto_20151110_1317'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailalertmessage',
            name='sender',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
