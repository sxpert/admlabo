# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0018_userclass_annuaire'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userclass',
            old_name='annuaire',
            new_name='directory',
        ),
    ]
