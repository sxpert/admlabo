# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0036_user_user_state'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='new',
        ),
    ]
