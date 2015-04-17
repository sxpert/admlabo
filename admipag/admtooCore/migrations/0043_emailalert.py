# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0042_userdir_files'),
    ]

    operations = [
        migrations.CreateModel(
            name='EmailAlert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cause', models.CharField(default=b'Unknown', max_length=32)),
                ('email', models.EmailField(default=b'user@example.com', max_length=254)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
