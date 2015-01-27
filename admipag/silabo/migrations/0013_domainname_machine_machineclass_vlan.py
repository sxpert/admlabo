# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import netfields.fields


class Migration(migrations.Migration):

    dependencies = [
        ('silabo', '0012_auto_20150106_1535'),
    ]

    operations = [
        migrations.CreateModel(
            name='DomainName',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('fqdn', models.CharField(unique=True, max_length=255)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Machine',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('default_name', models.ForeignKey(blank=True, to='silabo.DomainName', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MachineClass',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('shortdesc', models.CharField(max_length=128, blank=True)),
                ('longdesc', models.CharField(max_length=128, blank=True)),
            ],
            options={
                'verbose_name_plural': 'MachineClasses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Vlan',
            fields=[
                ('vlan_id', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=64)),
                ('ip_block', netfields.fields.CidrAddressField(unique=True, max_length=43)),
                ('gateway', netfields.fields.InetAddressField(unique=True, max_length=39)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
