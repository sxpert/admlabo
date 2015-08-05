# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0059_mailalias'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailalias',
            name='user',
            field=models.ForeignKey(related_name='UserAliases', blank=True, to='admtooCore.User', null=True),
            preserve_default=True,
        ),
    ]
