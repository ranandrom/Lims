# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-01-12 05:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AnchorDxLimsApp', '0070_randdsamplecomputerseqinfo_biotaskassignment'),
    ]

    operations = [
        migrations.AddField(
            model_name='bioinfodataanalysisinfo',
            name='SampleSource',
            field=models.CharField(default=0, max_length=16),
            preserve_default=False,
        ),
    ]
