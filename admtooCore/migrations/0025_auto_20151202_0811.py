# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0024_auto_20151126_1224'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailalert',
            name='email',
            field=models.CharField(default=b'user@example.com', max_length=254),
            preserve_default=True,
        ),
    ]
