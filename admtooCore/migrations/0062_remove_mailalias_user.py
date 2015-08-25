# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0061_auto_20150825_1029'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mailalias',
            name='user',
        ),
    ]
