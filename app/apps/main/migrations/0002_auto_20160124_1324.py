# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='physiciantimelogperiod',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='physiciantimelogperiod',
            name='edited_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
    ]
