# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import netfields.fields
import admtooCore.models.newuser


class Migration(migrations.Migration):

    replaces = [(b'admtooCore', '0001_initial'), (b'admtooCore', '0002_auto_20141210_0941'), (b'admtooCore', '0003_auto_20141210_0955'), (b'admtooCore', '0004_auto_20141210_1552'), (b'admtooCore', '0005_user_email'), (b'admtooCore', '0006_auto_20141212_1323'), (b'admtooCore', '0007_group'), (b'admtooCore', '0008_group_description'), (b'admtooCore', '0009_group_group_type'), (b'admtooCore', '0010_user_groups'), (b'admtooCore', '0011_auto_20150106_0955'), (b'admtooCore', '0012_auto_20150106_1535'), (b'admtooCore', '0013_domainname_machine_machineclass_vlan'), (b'admtooCore', '0014_auto_20150115_1648'), (b'admtooCore', '0015_networkif'), (b'admtooCore', '0016_machine_owner'), (b'admtooCore', '0017_auto_20150122_1100'), (b'admtooCore', '0018_mailinglist'), (b'admtooCore', '0019_auto_20150211_1113'), (b'admtooCore', '0020_user_login_shell'), (b'admtooCore', '0021_auto_20150311_1707'), (b'admtooCore', '0022_auto_20150311_1708'), (b'admtooCore', '0023_command'), (b'admtooCore', '0024_auto_20150317_1202'), (b'admtooCore', '0025_auto_20150325_1615'), (b'admtooCore', '0026_country'), (b'admtooCore', '0027_auto_20150326_1019'), (b'admtooCore', '0028_auto_20150326_1157'), (b'admtooCore', '0029_auto_20150327_1249'), (b'admtooCore', '0030_office'), (b'admtooCore', '0031_office_desc'), (b'admtooCore', '0032_newuser'), (b'admtooCore', '0033_auto_20150401_1652'), (b'admtooCore', '0034_auto_20150401_1723'), (b'admtooCore', '0035_auto_20150403_1622'), (b'admtooCore', '0036_user_user_state'), (b'admtooCore', '0037_remove_user_new'), (b'admtooCore', '0038_auto_20150407_1551'), (b'admtooCore', '0039_userdir'), (b'admtooCore', '0040_user_group'), (b'admtooCore', '0041_command_in_cron'), (b'admtooCore', '0042_userdir_files'), (b'admtooCore', '0043_emailalert'), (b'admtooCore', '0044_userclass_probie'), (b'admtooCore', '0045_emailalertmessage'), (b'admtooCore', '0046_emailalertmessage_subject'), (b'admtooCore', '0047_auto_20150430_1010'), (b'admtooCore', '0048_emailalertmessage_msgtext'), (b'admtooCore', '0049_user_birthdate'), (b'admtooCore', '0050_group_appspecname'), (b'admtooCore', '0051_mailinglist_userclass'), (b'admtooCore', '0052_user_userclass'), (b'admtooCore', '0053_auto_20150513_1043'), (b'admtooCore', '0054_auto_20150513_1053'), (b'admtooCore', '0055_userflag'), (b'admtooCore', '0056_user_flags'), (b'admtooCore', '0057_user_appspecname'), (b'admtooCore', '0058_user_main_team'), (b'admtooCore', '0059_mailalias'), (b'admtooCore', '0060_auto_20150805_1005'), (b'admtooCore', '0061_auto_20150825_1029'), (b'admtooCore', '0062_remove_mailalias_user')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uidnumber', models.IntegerField(unique=True)),
                ('login', models.CharField(unique=True, max_length=64)),
                ('manager', models.ForeignKey(blank=True, to='admtooCore.User', null=True)),
                ('first_name', models.CharField(max_length=128, null=True, blank=True)),
                ('last_name', models.CharField(max_length=128, null=True, blank=True)),
                ('mail', models.EmailField(max_length=75, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('gidnumber', models.IntegerField(serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=64)),
                ('parent', models.ForeignKey(blank=True, to='admtooCore.Group', null=True)),
                ('description', models.CharField(max_length=256, null=True, blank=True)),
                ('group_type', models.IntegerField(default=0, choices=[(0, b''), (1, b"Groupe d'\xc3\xa9quipe"), (2, b'Groupe de service')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(related_name='users', to=b'admtooCore.Group', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='arrival',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='departure',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
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
                ('default_name', models.ForeignKey(blank=True, to='admtooCore.DomainName', null=True)),
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
        migrations.CreateModel(
            name='IPAddress',
            fields=[
                ('address', netfields.fields.InetAddressField(max_length=39, serialize=False, primary_key=True)),
                ('ptr', models.ForeignKey(blank=True, to='admtooCore.DomainName', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='domainname',
            name='ips',
            field=models.ManyToManyField(related_name='domainnames', to=b'admtooCore.IPAddress', blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='NetworkIf',
            fields=[
                ('mac_addr', netfields.fields.MACAddressField(serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=32, null=True, blank=True)),
                ('ips', models.ManyToManyField(related_name='networkinterfaces', db_index=True, to=b'admtooCore.IPAddress', blank=True)),
                ('machine', models.ForeignKey(related_name='interfaces', blank=True, to='admtooCore.Machine', null=True)),
                ('addressing_type', models.IntegerField(default=2, choices=[(0, b'statique'), (1, b'dhcp statique'), (2, b'dhcp')])),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='machine',
            name='owner',
            field=models.ForeignKey(blank=True, to='admtooCore.User', null=True),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['login']},
        ),
        migrations.AddField(
            model_name='machine',
            name='comment',
            field=models.CharField(max_length=256, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('ml_id', models.CharField(max_length=64, serialize=False, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=128)),
                ('description', models.CharField(max_length=256)),
                ('group', models.ForeignKey(blank=True, to='admtooCore.Group', null=True)),
                ('parent', models.ForeignKey(blank=True, to='admtooCore.MailingList', null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='room',
            field=models.CharField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='telephone',
            field=models.CharField(max_length=32, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='login_shell',
            field=models.CharField(max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='login',
            field=models.CharField(unique=True, max_length=64, db_index=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Command',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('user', models.CharField(max_length=64)),
                ('verb', models.CharField(max_length=64)),
                ('data', models.TextField()),
                ('done', models.BooleanField(default=False)),
                ('modified', models.DateTimeField(auto_now=True, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='command',
            options={'ordering': ['-created'], 'get_latest_by': 'created'},
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('iso2', models.CharField(max_length=2, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=128)),
                ('citizenship', models.CharField(max_length=128)),
            ],
            options={
                'verbose_name_plural': 'Countries',
            },
            bases=(models.Model,),
        ),
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
        migrations.AlterModelOptions(
            name='userclass',
            options={'ordering': ['ref'], 'verbose_name_plural': 'UserClasses'},
        ),
        migrations.RenameField(
            model_name='userclass',
            old_name='name',
            new_name='ref',
        ),
        migrations.AddField(
            model_name='userclass',
            name='en',
            field=models.CharField(max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='userclass',
            name='fr',
            field=models.CharField(max_length=128, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='ipaddress',
            options={'verbose_name_plural': 'IP Addresses'},
        ),
        migrations.AlterModelOptions(
            name='mailinglist',
            options={'ordering': ['ml_id']},
        ),
        migrations.AddField(
            model_name='country',
            name='eu_member',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='Office',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ref', models.CharField(max_length=16)),
                ('desc', models.CharField(max_length=16, null=True, blank=True)),
            ],
            options={
                'ordering': ['ref'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('last_name', models.CharField(max_length=128, null=True, blank=True)),
                ('os_type', models.IntegerField(default=1, choices=[(0, b'Autre'), (1, b'Linux'), (2, b'Mac OS'), (3, b'Windows (7)')])),
                ('arrival', models.DateField(default=admtooCore.models.newuser.arrival_default)),
                ('birthdate', models.DateField(default=admtooCore.models.newuser.birthdate_default)),
                ('chem_lab', models.BooleanField(default=False)),
                ('citizenship', models.ForeignKey(default=admtooCore.models.newuser.citizenship_default, to='admtooCore.Country')),
                ('comments', models.TextField(null=True, blank=True)),
                ('comp_account', models.BooleanField(default=True)),
                ('comp_purchase', models.BooleanField(default=False)),
                ('departure', models.DateField(null=True, blank=True)),
                ('external_email', models.EmailField(max_length=254, null=True, blank=True)),
                ('first_name', models.CharField(max_length=128, null=True, blank=True)),
                ('ir_lab', models.BooleanField(default=False)),
                ('manager', models.ForeignKey(related_name='Manager', blank=True, to='admtooCore.User', null=True)),
                ('risky_activity', models.BooleanField(default=False)),
                ('specific_os', models.CharField(max_length=128, null=True, blank=True)),
                ('status', models.ForeignKey(default=admtooCore.models.newuser.status_default, to='admtooCore.UserClass')),
                ('workshop', models.BooleanField(default=False)),
                ('office', models.ForeignKey(blank=True, to='admtooCore.Office', null=True)),
                ('other_office', models.CharField(max_length=128, null=True, blank=True)),
                ('study_level', models.CharField(max_length=128, null=True, blank=True)),
                ('team', models.ForeignKey(blank=True, to='admtooCore.Group', null=True)),
                ('ujf_student', models.BooleanField(default=False)),
                ('user', models.ForeignKey(related_name='User', blank=True, to='admtooCore.User', null=True)),
            ],
            options={
                'ordering': ['last_name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='user_state',
            field=models.IntegerField(default=0, choices=[(0, b'utilisateur actif'), (1, b'utilisateur nouvellement import\xc3\xa9'), (2, b'utilisateur supprim\xc3\xa9')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='user',
            name='uidnumber',
            field=models.IntegerField(default=None, unique=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='UserDir',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('label', models.CharField(max_length=32, null=True, blank=True)),
                ('basedir', models.CharField(max_length=128, null=True, blank=True)),
                ('modes', models.CharField(max_length=4, null=True, blank=True)),
                ('machine', models.ForeignKey(blank=True, to='admtooCore.Machine', null=True)),
                ('files', models.TextField(default=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='group',
            field=models.ForeignKey(blank=True, to='admtooCore.Group', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='command',
            name='in_cron',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
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
        migrations.AddField(
            model_name='userclass',
            name='probie',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='EmailAlertMessage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cause', models.CharField(default=b'Unknown', max_length=32)),
                ('msghtml', models.TextField(default=b'')),
                ('subject', models.TextField(default=b'')),
                ('msgtext', models.TextField(default=b'')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='birthdate',
            field=models.DateField(null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='group',
            name='appspecname',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='mailinglist',
            name='userclass',
            field=models.ForeignKey(blank=True, to='admtooCore.UserClass', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='userclass',
            field=models.ForeignKey(blank=True, to='admtooCore.UserClass', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='UserFlag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=64, null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='user',
            name='flags',
            field=models.ManyToManyField(to=b'admtooCore.UserFlag', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='appspecname',
            field=models.TextField(default=b''),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='user',
            name='main_team',
            field=models.ForeignKey(related_name='team_member', blank=True, to='admtooCore.Group', null=True),
            preserve_default=True,
        ),
        migrations.CreateModel(
            name='MailAlias',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('alias', models.CharField(unique=True, max_length=254)),
                ('description', models.CharField(max_length=254, null=True, blank=True)),
                ('mail', models.EmailField(max_length=254, null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'MailAliases',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='user',
            name='mail',
            field=models.EmailField(max_length=254, null=True, blank=True),
            preserve_default=True,
        ),
    ]
