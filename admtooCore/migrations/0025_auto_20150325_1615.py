# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0024_auto_20150317_1202'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='command',
            options={'ordering': ['-created'], 'get_latest_by': 'created'},
        ),
    ]
