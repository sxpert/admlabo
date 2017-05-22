# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0028_newuser_handled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='modified',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='newuser',
            name='created',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
