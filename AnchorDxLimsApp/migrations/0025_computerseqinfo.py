# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-10-26 10:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AnchorDxLimsApp', '0024_finlibconinfo_computerseq_sign'),
    ]

    operations = [
        migrations.CreateModel(
            name='ComputerSeqInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=64)),
                ('department', models.CharField(max_length=64)),
                ('sam_code_num', models.CharField(max_length=64)),
                ('ExperimentNumber', models.CharField(max_length=64)),
                ('DilutionMultiple', models.CharField(max_length=16)),
                ('qPCR', models.CharField(max_length=16)),
                ('AverageLengthLibrary', models.CharField(max_length=32)),
                ('LibEffConcentration', models.CharField(max_length=32)),
                ('QuantitativeHuman', models.CharField(max_length=32)),
                ('OperatingTime', models.CharField(max_length=32)),
                ('SeqRemarks', models.CharField(max_length=512)),
                ('Next_TaskProgress', models.CharField(max_length=64)),
                ('Next_TaskProgress_Man', models.CharField(max_length=64)),
                ('Next_TaskProgress_Time', models.CharField(max_length=32)),
                ('Next_TaskProgress_Remarks', models.CharField(max_length=512)),
                ('Next_TaskProgress_Sign', models.CharField(max_length=16)),
                ('DNA_extraction_num', models.CharField(max_length=16)),
                ('Build_Prelib_num', models.CharField(max_length=16)),
                ('Build_Finlib_num', models.CharField(max_length=16)),
                ('Computer_Seq_num', models.CharField(max_length=16)),
                ('Bioinfo_Sign', models.CharField(max_length=16)),
            ],
        ),
    ]