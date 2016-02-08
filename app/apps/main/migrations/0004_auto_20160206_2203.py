# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_physiciantimelogperiod_note'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='analyst',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='master',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='sites',
            field=models.ManyToManyField(to='main.HealthSite', blank=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='superuser',
            field=models.BooleanField(default=False),
        ),
    ]
