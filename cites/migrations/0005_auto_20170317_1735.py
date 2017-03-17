# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-17 16:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cites', '0004_auto_20170317_1734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='citation',
            name='cited_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date of citation'),
        ),
        migrations.AlterField(
            model_name='citation',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='citing',
            name='cited_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date of citation'),
        ),
        migrations.AlterField(
            model_name='citing',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='created_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='last_modified_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date last modified'),
        ),
        migrations.AlterField(
            model_name='publication',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='date published'),
        ),
    ]