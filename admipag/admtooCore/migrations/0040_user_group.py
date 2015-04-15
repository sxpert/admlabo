# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0039_userdir'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.ForeignKey(blank=True, to='admtooCore.Group', null=True),
            preserve_default=True,
        ),
    ]
