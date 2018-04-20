# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-01-09 08:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AnchorDxLimsApp', '0063_computerseqinfo_biotaskassignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='randdsampleinfo',
            name='ContractAuditor',
            field=models.CharField(default=0, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='randdsampleinfo',
            name='SampleAuditor',
            field=models.CharField(default=0, max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='randdsampleinfo',
            name='TaskAssignment',
            field=models.CharField(default=0, max_length=64),
            preserve_default=False,
        ),
    ]