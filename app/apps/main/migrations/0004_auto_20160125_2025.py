# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0003_physiciantimelog_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='PhysicianTimeLogApproval',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=True)),
                ('note', models.TextField(null=True, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='PhysicianTimeLogCategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('category', models.ForeignKey(to='main.ContractType')),
                ('physician', models.ForeignKey(to='main.Physician')),
                ('workflow_default', models.ForeignKey(to='main.Workflow')),
            ],
        ),
        migrations.AddField(
            model_name='physiciantimelogperiod',
            name='approval_num',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='physiciantimelogperiod',
            name='approved_by',
            field=models.ForeignKey(related_name='approver', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='physiciantimelogperiod',
            name='current_user',
            field=models.ForeignKey(related_name='current', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AddField(
            model_name='physiciantimelogperiod',
            name='workflow',
            field=models.ForeignKey(blank=True, to='main.Workflow', null=True),
        ),
        migrations.AddField(
            model_name='physiciantimelogapproval',
            name='physiciantimelogperiod',
            field=models.ForeignKey(to='main.PhysicianTimeLogPeriod'),
        ),
        migrations.AddField(
            model_name='physiciantimelogapproval',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
