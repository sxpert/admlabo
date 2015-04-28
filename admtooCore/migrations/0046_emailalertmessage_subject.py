# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0045_emailalertmessage'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailalertmessage',
            name='subject',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
    ]
