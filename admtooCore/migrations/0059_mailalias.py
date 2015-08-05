# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0058_user_main_team'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailAlias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(unique=True, max_length=254)),
                ('user', models.ForeignKey(related_name='AliasUser', blank=True, to='admtooCore.User', null=True)),
            ],
            options={
                'verbose_name_plural': 'MailAliases',
            },
            bases=(models.Model,),
        ),
    ]
