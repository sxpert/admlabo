# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0047_auto_20150430_1010'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailalertmessage',
            name='msgtext',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
