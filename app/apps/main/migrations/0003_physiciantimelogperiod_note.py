# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_physiciantimelogapproval_active'),
    ]

    operations = [
        migrations.AddField(
            model_name='physiciantimelogperiod',
            name='note',
            field=models.TextField(null=True, blank=True),
        ),
    ]
