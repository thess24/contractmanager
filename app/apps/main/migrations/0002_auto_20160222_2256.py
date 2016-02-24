# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='physiciantimelogcategory',
            name='final_elevation_users',
            field=models.ManyToManyField(related_name='final_elevation', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='physiciantimelogcategory',
            name='first_elevation_users',
            field=models.ManyToManyField(related_name='first_elevation', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AddField(
            model_name='physiciantimelogcategory',
            name='second_elevation_users',
            field=models.ManyToManyField(related_name='second_elevation', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='healthsite',
            name='zipcode',
            field=models.CharField(max_length=5, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='physiciantimelogcategory',
            name='approving_users',
            field=models.ManyToManyField(related_name='approving', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='team',
            name='description',
            field=models.TextField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='sites',
            field=models.ManyToManyField(to='main.HealthSite'),
        ),
        migrations.AlterField(
            model_name='workflow',
            name='created_by',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
