# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admtooCore', '0026_country'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64)),
            ],
            options={
                'ordering': ['name'],
                'verbose_name_plural': 'UserClasses',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ['name'], 'verbose_name_plural': 'Countries'},
        ),
    ]
