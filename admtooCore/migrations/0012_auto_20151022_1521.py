# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0011_auto_20151022_1506'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userclass',
            old_name='default',
            new_name='defval',
        ),
    ]
