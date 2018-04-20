# encoding: utf-8
from django.contrib import admin
from AnchorDxLimsApp import models

# Register your models here.

admin.site.register(models.UserSystemMessage)  # 用户系统消息表
admin.site.register(models.UserInfo)  # 用户信息表
admin.site.register(models.UserOperationPermissionsInfo)  # 用户操作权限信息表
admin.site.register(models.clinicalSampleInfo)  # 临检收样信息表
admin.site.register(models.RandDSampleInfo)  # 研发收样信息表
admin.site.register(models.contractReviewInfo)  # 临检样本财务审核信息表
admin.site.register(models.clinicalSamplePretreatment)  # 临检样本预处理信息表
admin.site.register(models.RandDSamplePretreatmentInfo)  # 研发样本预处理信息表
admin.site.register(models.DNAExtractInfo)  # 临检DNA提取信息表
admin.site.register(models.RandDSampleDNAExtractInfo)  # 研发DNA提取信息表
admin.site.register(models.PreLibConInfo)  # 临检预文库构建信息表
admin.site.register(models.RandDSamplePreLibConInfo)  # 研发预文库构建信息表
admin.site.register(models.FinLibConInfo)  # 临检终文库构建信息表
admin.site.register(models.RandDSampleFinLibConInfo)  # 研发终文库构建信息表
admin.site.register(models.ComputerSeqInfo)  # 临检上机测序信息表
admin.site.register(models.RandDSampleComputerSeqInfo)  # 研发上机测序信息表
admin.site.register(models.BioinfoDataAnalysisInfo)  # 生信数据分析信息表