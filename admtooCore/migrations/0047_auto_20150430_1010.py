# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0046_emailalertmessage_subject'),
    ]

    operations = [
        migrations.RenameField(
            model_name='emailalertmessage',
            old_name='message',
            new_name='msghtml',
        ),
    ]
