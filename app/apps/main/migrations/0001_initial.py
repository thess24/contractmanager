# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('level', models.IntegerField(default=2)),
            ],
        ),
        migrations.CreateModel(
            name='ContactRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254)),
                ('phone_number', models.CharField(max_length=10, null=True, blank=True)),
                ('organization', models.CharField(max_length=255, null=True, blank=True)),
                ('city', models.CharField(max_length=255, null=True, blank=True)),
                ('state', models.CharField(max_length=100, null=True, blank=True)),
                ('zipcode', models.CharField(max_length=5, null=True, blank=True)),
                ('job_title', models.CharField(max_length=255, null=True, blank=True)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('responded', models.BooleanField(default=False)),
                ('notes', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('contract_file', models.FileField(null=True, upload_to=b'contracts', blank=True)),
                ('status', models.CharField(default=b'In Progress', max_length=50)),
                ('signed', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ContractApproval',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('contract', models.ForeignKey(to='main.Contract')),
            ],
        ),
        migrations.CreateModel(
            name='ContractAttachment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, null=True, blank=True)),
                ('attachment', models.FileField(upload_to=b'attachments')),
                ('contract', models.ForeignKey(to='main.Contract')),
            ],
        ),
        migrations.CreateModel(
            name='ContractInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('version', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('html', models.TextField(null=True, blank=True)),
                ('html_output', models.TextField(null=True, blank=True)),
                ('change_made', models.CharField(max_length=255)),
                ('grabbed_at', models.DateTimeField(null=True, blank=True)),
                ('sent_at', models.DateTimeField(null=True, blank=True)),
                ('region', models.CharField(max_length=100, null=True, blank=True)),
                ('specialty', models.CharField(max_length=100, null=True, blank=True)),
                ('contracting_entity', models.CharField(max_length=100, null=True, blank=True)),
                ('start_date', models.DateTimeField(null=True, blank=True)),
                ('end_date', models.DateTimeField(null=True, blank=True)),
                ('type_of_services', models.CharField(max_length=255, null=True, blank=True)),
                ('type_of_admin_services', models.TextField(null=True, blank=True)),
                ('admin_services_title', models.CharField(max_length=255, null=True, blank=True)),
                ('num_physicians', models.IntegerField(null=True, blank=True)),
                ('max_monthly_hours', models.DecimalField(null=True, max_digits=5, decimal_places=2, blank=True)),
                ('amount', models.IntegerField(null=True, blank=True)),
                ('performance_linked', models.NullBooleanField(default=None)),
                ('performance_criteria', models.TextField(null=True, blank=True)),
                ('responsible_party', models.CharField(max_length=100, null=True, blank=True)),
                ('responsible_party_secondary', models.CharField(max_length=100, null=True, blank=True)),
                ('termination_days_notice', models.IntegerField(null=True, blank=True)),
                ('malpractice_coverage_party', models.CharField(max_length=100, null=True, blank=True)),
                ('malpractice_limits', models.IntegerField(null=True, blank=True)),
                ('type_of_malpractice_coverage', models.CharField(max_length=100, null=True, blank=True)),
                ('physician_tail_responsibility', models.NullBooleanField(default=None)),
                ('right_to_bill', models.CharField(max_length=100, null=True, blank=True)),
                ('non_compete', models.NullBooleanField(default=None)),
                ('non_solicitation', models.NullBooleanField(default=None)),
                ('auto_renew', models.NullBooleanField(default=None)),
                ('renewal_date', models.DateTimeField(null=True, blank=True)),
                ('contract', models.ForeignKey(to='main.Contract')),
            ],
        ),
        migrations.CreateModel(
            name='ContractSubType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ContractType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='HealthSite',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100, null=True, blank=True)),
                ('city', models.CharField(max_length=100, null=True, blank=True)),
                ('state', models.CharField(max_length=30, null=True, blank=True)),
                ('zipcode', models.CharField(max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='HealthSystem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('street', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=30)),
                ('zipcode', models.CharField(max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('logo', models.ImageField(null=True, upload_to=b'logos', blank=True)),
                ('shorthand', models.CharField(max_length=6)),
            ],
        ),
        migrations.CreateModel(
            name='Physician',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('npi', models.CharField(max_length=100)),
                ('payroll_num', models.CharField(max_length=100, null=True, blank=True)),
                ('med_license_num', models.CharField(max_length=100)),
                ('med_license_state', models.CharField(max_length=100)),
                ('med_degree', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhysicianGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('system', models.ForeignKey(to='main.HealthSystem')),
            ],
        ),
        migrations.CreateModel(
            name='PhysicianTimeLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField(null=True, blank=True)),
                ('start_time', models.DateTimeField(null=True, blank=True)),
                ('end_time', models.DateTimeField(null=True, blank=True)),
                ('mins_worked', models.IntegerField(null=True, blank=True)),
                ('category', models.CharField(max_length=100)),
                ('notes', models.TextField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('physician', models.ForeignKey(to='main.Physician')),
            ],
        ),
        migrations.CreateModel(
            name='PhysicianTimeLogPeriod',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('period', models.DateField()),
                ('mins_worked', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approved_at', models.DateTimeField(null=True, blank=True)),
                ('category', models.ForeignKey(to='main.ContractType')),
                ('physician', models.ForeignKey(to='main.Physician')),
            ],
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('admin', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('system', models.ForeignKey(to='main.HealthSystem')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('short_desc', models.CharField(max_length=100, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('add_on', models.BooleanField(default=False)),
                ('html', models.TextField()),
                ('system', models.ForeignKey(to='main.HealthSystem')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('system', models.ForeignKey(to='main.HealthSystem')),
                ('team', models.ForeignKey(to='main.Team')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('system', models.ForeignKey(to='main.HealthSystem')),
            ],
        ),
        migrations.CreateModel(
            name='WorkflowItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField()),
                ('team', models.ForeignKey(blank=True, to='main.Team', null=True)),
                ('user', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('workflow', models.ForeignKey(to='main.Workflow')),
            ],
        ),
        migrations.AddField(
            model_name='physician',
            name='physiciangroup',
            field=models.ForeignKey(blank=True, to='main.PhysicianGroup', null=True),
        ),
        migrations.AddField(
            model_name='physician',
            name='system',
            field=models.ForeignKey(to='main.HealthSystem'),
        ),
        migrations.AddField(
            model_name='physician',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='healthsite',
            name='system',
            field=models.ForeignKey(to='main.HealthSystem'),
        ),
        migrations.AddField(
            model_name='contracttype',
            name='system',
            field=models.ForeignKey(to='main.HealthSystem'),
        ),
        migrations.AddField(
            model_name='contractsubtype',
            name='contract_type',
            field=models.ForeignKey(to='main.ContractType'),
        ),
        migrations.AddField(
            model_name='contractinfo',
            name='current_team',
            field=models.ForeignKey(related_name='contract_current_team', blank=True, to='main.Team', null=True),
        ),
        migrations.AddField(
            model_name='contractinfo',
            name='current_user',
            field=models.ForeignKey(related_name='contract_current_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='contractinfo',
            name='next_team',
            field=models.ForeignKey(related_name='contract_next_team', blank=True, to='main.Team', null=True),
        ),
        migrations.AddField(
            model_name='contractinfo',
            name='next_user',
            field=models.ForeignKey(related_name='contract_next_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='contractinfo',
            name='prev_team',
            field=models.ForeignKey(related_name='contract_past_team', blank=True, to='main.Team', null=True),
        ),
        migrations.AddField(
            model_name='contractinfo',
            name='prev_user',
            field=models.ForeignKey(related_name='contract_past_user', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='contractinfo',
            name='site',
            field=models.ForeignKey(blank=True, to='main.HealthSite', null=True),
        ),
        migrations.AddField(
            model_name='contractapproval',
            name='team',
            field=models.ForeignKey(to='main.Team'),
        ),
        migrations.AddField(
            model_name='contractapproval',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='contract_subtype',
            field=models.ForeignKey(blank=True, to='main.ContractSubType', null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='contract_type',
            field=models.ForeignKey(blank=True, to='main.ContractType', null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='contract',
            name='physician',
            field=models.ForeignKey(blank=True, to='main.Physician', null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='physician_group',
            field=models.ForeignKey(blank=True, to='main.PhysicianGroup', null=True),
        ),
        migrations.AddField(
            model_name='contract',
            name='system',
            field=models.ForeignKey(to='main.HealthSystem'),
        ),
        migrations.AddField(
            model_name='contract',
            name='workflow',
            field=models.ForeignKey(blank=True, to='main.Workflow', null=True),
        ),
        migrations.AddField(
            model_name='alert',
            name='contract',
            field=models.ForeignKey(to='main.Contract'),
        ),
        migrations.AddField(
            model_name='alert',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
