# encoding: utf-8

from django.contrib import auth
from django.shortcuts import render
from django.contrib.auth.models import User
from AnchorDxLimsApp import models
import time,httplib,datetime
from itertools import chain
from django.core.mail import send_mail
from smtplib import SMTPException
import subprocess
import socket
import datetime
import os
import glob
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# Create your views here.
#coding:utf-8

from django.shortcuts import render,HttpResponse

#  登录页
def index(request):
    return render(request,"index.html")

# 登录验证
# def login(request):
#     username = request.POST.get('username', None)
#     password = request.POST.get('password', None)
#     user = auth.authenticate(username=username, password=password)
#     print(username, password)
#     if user is not None and user.is_active:
#         # Correct password, and the user is marked "active"
#         auth.login(request, user)
#         # Redirect to a success page.
#         department = user.first_name
#         temp = {"username": username, "department": department}
#         request.session['username'] = username
#         request.session['department'] = department
#
#         addUserAccessRights(username, department)  # 添加用户访问权限
#         addUserOperationPermissions(username, department)  # 添加用户操作权限
#         temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
#         # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户系统信息
#         temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
#                                                                             ReadingState='未读')
#         num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
#         # return HttpResponseRedirect("/account/loggedin/")
#         return render(request, "modelspage/homepage.html",
#                       {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
#                        "num_SystemMessage_Unread": num_SystemMessage_Unread})
#     else:
#         # Show an error page
#         # return HttpResponseRedirect("/account/invalid/")
#         error = {"error": 1}
#         return render(request, "index.html", {"error": error})

# 添加用户访问权限
def addUserAccessRights (username, department):
    temp_mysql = models.UserInfo.objects.filter(username=username)  # 用户信息
    if len(temp_mysql) == 0:
        if department == '管理员':
            print '用户是：', department
            # 添加数据到数据库
            models.UserInfo.objects.create(
                # 用户信息
                username=username,  # 用户名
                department=department,  # 部门
                DefaultMark=0,  # 默认标记
                # 样本管理模块
                SampleManagement=1,  # 样本管理
                ClinicalSampleRegistration=1,  # 样本登记（临检）
                sampleReview=1,  # 收样审核（临检）
                clinicalExperimentalTaskAssignment=1,  # 任务分派（临检）
                PretreatmentTaskReview=1,  # 样本预处理（临检）
                DNAExtractTaskReview=1,  # DNA提取（临检）
                PreLibConTaskReview=1,  # 预文库构建（临检）
                FinLibConTaskReview=1,  # 终文库构建（临检）
                ComSeqTaskReview=1,  # 上机测序（临检）
                # 项目管理模块
                projectManagement=1,  # 项目管理
                RandDSampleInfoInputHomePage=1,  # 收样登记（研发）
                RandDSampleReviewHomePage=1,  # 收样审核（研发）
                RandDExperimentalTaskAssignmentHomePage=1,  # 任务分派（研发）
                RandDPretreatmentInfoInputHomePage=1,  # 样本预处理（研发）
                RandDDNAExtractInfoInputHomePage=1,  # DNA提取（研发）
                RandDPreLibConInfoInputHomePage=1,  # 预文库构建（研发）
                RandDFinLibConInfoInputHomePage=1,  # 终文库构建（研发）
                RandDComSeqInfoInputHomePage=1,  # 上机测序（研发）
                # 合同管理模块
                contractManagement=1,  # 合同管理
                contractReview=1,  # 合同审核
                # 生信分析模块
                BioinfoAnalysis=1,  # 生信分析
                BioinfoTaskAssignment=1,  # 分析任务分派
                BioinfoDataAnalysisTaskReview=1,  # 数据分析结果
                BioinfoDataAnalysisResultReview=1,  # 分析结果审核
                BioinfoReportTaskReview=1,  # 报告生成
                # 报告管理模块
                ReportManagement=1,  # 报告管理
                BioinfoReportMedicalAuditTaskReview=1,  # 遗传咨询师审核报告
                BioinfoReportOperateAuditTaskReview=1,  # 运营审核报告
                # 商务管理模块
                BusinessAffairsManagement=1,  # 商务管理
                BioinfoReportSendInfoTaskReview=1,  # 报告发送
            )
        else:
            # 添加数据到数据库
            models.UserInfo.objects.create(
                # 用户信息
                username=username,  # 用户名
                department=department,  # 部门
                DefaultMark=0,  # 默认标记
                # 样本管理模块
                SampleManagement=0,  # 样本管理
                ClinicalSampleRegistration=0,  # 样本登记（临检）
                sampleReview=0,  # 收样审核（临检）
                clinicalExperimentalTaskAssignment=0,  # 任务分派（临检）
                PretreatmentTaskReview=0,  # 样本预处理（临检）
                DNAExtractTaskReview=0,  # DNA提取（临检）
                PreLibConTaskReview=0,  # 预文库构建（临检）
                FinLibConTaskReview=0,  # 终文库构建（临检）
                ComSeqTaskReview=0,  # 上机测序（临检）
                # 项目管理模块
                projectManagement=0,  # 项目管理
                RandDSampleInfoInputHomePage=0,  # 收样登记（研发）
                RandDSampleReviewHomePage=0,  # 收样审核（研发）
                RandDExperimentalTaskAssignmentHomePage=0,  # 任务分派（研发）
                RandDPretreatmentInfoInputHomePage=0,  # 样本预处理（研发）
                RandDDNAExtractInfoInputHomePage=0,  # DNA提取（研发）
                RandDPreLibConInfoInputHomePage=0,  # 预文库构建（研发）
                RandDFinLibConInfoInputHomePage=0,  # 终文库构建（研发）
                RandDComSeqInfoInputHomePage=0,  # 上机测序（研发）
                # 合同管理模块
                contractManagement=0,  # 合同管理
                contractReview=0,  # 合同审核
                # 生信分析模块
                BioinfoAnalysis=0,  # 生信分析
                BioinfoTaskAssignment=0,  # 分析任务分派
                BioinfoDataAnalysisTaskReview=0,  # 数据分析结果
                BioinfoDataAnalysisResultReview=0,  # 分析结果审核
                BioinfoReportTaskReview=0,  # 报告生成
                # 报告管理模块
                ReportManagement=0,  # 报告管理
                BioinfoReportMedicalAuditTaskReview=0,  # 遗传咨询师审核报告
                BioinfoReportOperateAuditTaskReview=0,  # 运营审核报告
                # 商务管理模块
                BusinessAffairsManagement=0,  # 商务管理
                BioinfoReportSendInfoTaskReview=0,  # 报告发送
            )
    else:
        return

# 添加用户操作权限
def addUserOperationPermissions(username, department):
    temp_mysql = models.UserOperationPermissionsInfo.objects.filter(username=username)  # 用户信息
    if len(temp_mysql) == 0:
        if department == '管理员':
            print '用户是：', department
            # 添加数据到数据库
            models.UserOperationPermissionsInfo.objects.create(
                # 用户信息
                username=username,  # 用户名
                department=department,  # 部门
                DefaultMark=0,  # 默认标记
                # 样本管理模块
                ClinicalSampleRegistration=1,  # 样本登记（临检）
                sampleReview=1,  # 收样审核（临检）
                clinicalExperimentalTaskAssignment=1,  # 任务分派（临检）
                PretreatmentTaskReview=1,  # 样本预处理（临检）
                DNAExtractTaskReview=1,  # DNA提取（临检）
                PreLibConTaskReview=1,  # 预文库构建（临检）
                FinLibConTaskReview=1,  # 终文库构建（临检）
                ComSeqTaskReview=1,  # 上机测序（临检）
                # 项目管理模块
                RandDSampleInfoInputHomePage=1,  # 收样登记（研发）
                RandDSampleReviewHomePage=1,  # 收样审核（研发）
                RandDExperimentalTaskAssignmentHomePage=1,  # 任务分派（研发）
                RandDPretreatmentInfoInputHomePage=1,  # 样本预处理（研发）
                RandDDNAExtractInfoInputHomePage=1,  # DNA提取（研发）
                RandDPreLibConInfoInputHomePage=1,  # 预文库构建（研发）
                RandDFinLibConInfoInputHomePage=1,  # 终文库构建（研发）
                RandDComSeqInfoInputHomePage=1,  # 上机测序（研发）
                # 合同管理模块
                contractReview=1,  # 合同审核
                # 生信分析模块
                BioinfoTaskAssignment=1,  # 分析任务分派
                BioinfoDataAnalysisTaskReview=1,  # 数据分析结果
                BioinfoDataAnalysisResultReview=1,  # 分析结果审核
                BioinfoReportTaskReview=1,  # 报告生成
                # 报告管理模块
                BioinfoReportMedicalAuditTaskReview=1,  # 遗传咨询师审核报告
                BioinfoReportOperateAuditTaskReview=1,  # 运营审核报告
                # 商务管理模块
                BioinfoReportSendInfoTaskReview=1,  # 报告发送
            )
        else:
            # 添加数据到数据库
            models.UserOperationPermissionsInfo.objects.create(
                # 用户信息
                username=username,  # 用户名
                department=department,  # 部门
                DefaultMark=0,  # 默认标记
                # 样本管理模块
                ClinicalSampleRegistration=0,  # 样本登记（临检）
                sampleReview=0,  # 收样审核（临检）
                clinicalExperimentalTaskAssignment=0,  # 任务分派（临检）
                PretreatmentTaskReview=0,  # 样本预处理（临检）
                DNAExtractTaskReview=0,  # DNA提取（临检）
                PreLibConTaskReview=0,  # 预文库构建（临检）
                FinLibConTaskReview=0,  # 终文库构建（临检）
                ComSeqTaskReview=0,  # 上机测序（临检）
                # 项目管理模块
                RandDSampleInfoInputHomePage=0,  # 收样登记（研发）
                RandDSampleReviewHomePage=0,  # 收样审核（研发）
                RandDExperimentalTaskAssignmentHomePage=0,  # 任务分派（研发）
                RandDPretreatmentInfoInputHomePage=0,  # 样本预处理（研发）
                RandDDNAExtractInfoInputHomePage=0,  # DNA提取（研发）
                RandDPreLibConInfoInputHomePage=0,  # 预文库构建（研发）
                RandDFinLibConInfoInputHomePage=0,  # 终文库构建（研发）
                RandDComSeqInfoInputHomePage=0,  # 上机测序（研发）
                # 合同管理模块
                contractReview=0,  # 合同审核
                # 生信分析模块
                BioinfoTaskAssignment=0,  # 分析任务分派
                BioinfoDataAnalysisTaskReview=0,  # 数据分析结果
                BioinfoDataAnalysisResultReview=0,  # 分析结果审核
                BioinfoReportTaskReview=0,  # 报告生成
                # 报告管理模块
                BioinfoReportMedicalAuditTaskReview=0,  # 遗传咨询师审核报告
                BioinfoReportOperateAuditTaskReview=0,  # 运营审核报告
                # 商务管理模块
                BioinfoReportSendInfoTaskReview=0,  # 报告发送
            )
    else:
        return

# 退出系统
def logout(request):
    auth.logout(request)
    # Redirect to a success page.
    return render(request, "index.html")

# 登录验证及系统首页
def homepage(request):
    button_name = ''
    # 判断哪个按钮提交的数据
    if request.POST.has_key('login'):
        button_name = 'login'
    if button_name == 'login':
        username = request.POST.get('username', None)
        password = request.POST.get('password', None)
        # print(r'首页，username: ', username, password)
        user = auth.authenticate(username=username, password=password)
        # print(username, password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            department = user.first_name
            temp = {"username": username, "department": department}
            request.session['username'] = username
            request.session['department'] = department

            addUserAccessRights(username, department)  # 添加用户访问权限
            addUserOperationPermissions(username, department)  # 添加用户操作权限
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户系统信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)

            temp_ClinicalSample = models.clinicalSampleInfo.objects.filter(sample_review__in=[0, 1, 2, 3])
            NumOfClinicalSample = len(temp_ClinicalSample)

            temp_RandDSample = models.RandDSampleInfo.objects.filter(sample_review__in=[0, 1, 2, 3])
            NumOfRandDSample = len(temp_RandDSample)

            temp_SendReport = models.BioinfoDataAnalysisInfo.objects.filter(Report_Send_Sign=1)  # 临检样本信息
            NumOfSendReport = len(temp_SendReport)

            if department == '销售部':
                temp_not_audited = models.clinicalSampleInfo.objects.filter(username=username,
                                                                            sample_review=0)  # 研发样本未审核信息
                temp_draft = models.clinicalSampleInfo.objects.filter(username=username, sample_review='')  # 研发样本草稿信息
                temp_return = models.clinicalSampleInfo.objects.filter(username=username, sample_review=4)  # 研发审核退回样本信息
                temp_audited = models.clinicalSampleInfo.objects.filter(username=username,
                                                                        sample_review__in=[1, 2, 3])  # 研发样本已审核信息
                return render(request, "modelspage/sample_entry.html",
                              {"userinfo": temp, "not_audited": temp_not_audited, "audited": temp_audited,
                               "draft": temp_draft,
                               "return": temp_return, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})
            else:
                return render(request, "modelspage/homepage.html",
                              {"userinfo": temp, "myInfo": temp_myInfo, "NumOfSendReport": NumOfSendReport,
                               "NumOfClinicalSample": NumOfClinicalSample, "NumOfRandDSample": NumOfRandDSample,
                               "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread, })
        else:
            # Show an error page
            # return HttpResponseRedirect("/account/invalid/")
            error = {"error": 1}
            return render(request, "index.html", {"error": error})
    else:
        try:
            username = request.session['username']
            department = request.session['department']
        except Exception:
            return render(request, "index.html")
        else:
            # print(r'首页，username: ', username, department)
            temp = {"username": username, "department": department}
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户系统信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)

            temp_ClinicalSample = models.clinicalSampleInfo.objects.filter(sample_review__in=[0, 1, 2, 3])
            NumOfClinicalSample = len(temp_ClinicalSample)

            temp_RandDSample = models.RandDSampleInfo.objects.filter(sample_review__in=[0, 1, 2, 3])
            NumOfRandDSample = len(temp_RandDSample)

            temp_SendReport = models.BioinfoDataAnalysisInfo.objects.filter(Report_Send_Sign=1)  # 临检样本信息
            NumOfSendReport = len(temp_SendReport)

            button_name = ''  # 按钮名字
            sam_code_num = ''  # 样本编号
            SampleSource = ''  # 样本来源
            sampleIsExist = '' # 样本是否存在

            TissueSampleSign = ''

            DNAExtract_Sign = ''
            PreLibCon_Sign  = ''
            FinalLibCon_Sign = ''
            ComputerSeq_Sign = ''
            Bioinfo_Sign = ''
            Report_Make_Sign = ''
            Medical_Examine_Sign = ''

            RandDSampleInfo_review_Sign = 0
            RandDSamplePretreatmentInfo_review_Sign = 0
            DNAExtract_review_Sign = 0
            PreLibCon_review_Sign = 0
            FinalLibCon_review_Sign = 0
            ComputerSeq_review_Sign = 0
            Bioinfo_review_Sign = 0

            RandDSampleInputState = ''
            Num_RandDSampleInfo = ''
            RandDSampleInfostate = ''
            Num_RandDSampleInfoReviewed = ''
            Num_RandDSamplePretreatmentInfo = ''
            RandDSamplePretreatmentInfoState = ''
            Num_RandDSampleDNAExtractInfo = ''
            RandDSampleDNAExtractInfoState = ''
            Num_RandDSamplePreLibConInfo = ''
            RandDSamplePreLibConInfoState = ''
            Num_RandDSampleFinLibConInfo = ''
            RandDSampleFinLibConInfoState = ''
            Num_RandDSampleComputerSeqInfo = ''
            RandDSampleComputerSeqInfoState = ''

            if request.method == "POST":
                # 样本条码号
                sam_code_num = request.POST.get('sam_code_num')
                SampleSource = request.POST.get('SampleSource')
                # 判断哪个按钮提交的数据
                if request.POST.has_key('Search'):
                    button_name = 'Search'

            if button_name == 'Search':
                if SampleSource == '临检样本':
                    RandDSampleInfo = models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num,
                                                                               sample_review__in=[0, 1, 2, 3])
                    Num_RandDSampleInfo = len(RandDSampleInfo)
                    RandDSampleInputState  = '无信息'
                    RandDSampleInfostate = '无信息'
                    if not Num_RandDSampleInfo == 0:
                        sampleIsExist = '样本存在'
                        RandDSampleInputState = '样本信息已登记'
                        if RandDSampleInfo[0].sample_review == '0':
                            RandDSampleInfostate = '未审核'
                            DNAExtract_Sign = 0
                            RandDSampleInfo_review_Sign = 1
                        elif RandDSampleInfo[0].sample_review == '1':
                            RandDSampleInfostate = '审核通过'
                            if RandDSampleInfo[0].DNAExtract_Sign == '0':
                                print 'DNAExtract_Sign==0'
                                DNAExtract_Sign = 0
                        elif RandDSampleInfo[0].sample_review == '2':
                            RandDSampleInfostate = '任务暂停'
                        elif RandDSampleInfo[0].sample_review == '3':
                            RandDSampleInfostate = '任务终止'
                        elif RandDSampleInfo[0].sample_review == '4':
                            RandDSampleInfostate = '样本登记信息被退回'
                    else:
                        sampleIsExist = '样本不存在'
                    RandDSampleInfoReviewed = models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num,
                                                                                       sample_review__in=[1, 2, 3])
                    Num_RandDSampleInfoReviewed = len(RandDSampleInfoReviewed)

                    if not Num_RandDSampleInfo == 0:
                        if RandDSampleInfo[0].TissueSampleSign == '0':
                            TissueSampleSign = 0
                        else:
                            TissueSampleSign = 1

                    RandDSamplePretreatmentInfo = models.clinicalSamplePretreatment.objects.filter(sam_code_num=sam_code_num)
                    Num_RandDSamplePretreatmentInfo = len(RandDSamplePretreatmentInfo)
                    RandDSamplePretreatmentInfoState = '无信息'
                    if not Num_RandDSamplePretreatmentInfo == 0:
                        if RandDSamplePretreatmentInfo[0].Next_TaskProgress_Sign == '0':
                            RandDSamplePretreatmentInfoState = '信息已录入，但未审核'
                            DNAExtract_Sign = 0
                            RandDSamplePretreatmentInfo_review_Sign = 1
                        elif RandDSamplePretreatmentInfo[0].Next_TaskProgress_Sign == '1':
                            RandDSamplePretreatmentInfoState = '信息已录入，且审核通过'
                            if RandDSamplePretreatmentInfo[0].DNAExtract_Sign == '0':
                                DNAExtract_Sign = 0
                        elif RandDSamplePretreatmentInfo[0].Next_TaskProgress_Sign == '2':
                            RandDSamplePretreatmentInfoState = '信息已录入，且任务暂停'
                        elif RandDSamplePretreatmentInfo[0].Next_TaskProgress_Sign == '3':
                            RandDSamplePretreatmentInfoState = '信息已录入，且任务终止'

                    RandDSampleDNAExtractInfo = models.DNAExtractInfo.objects.filter(sam_code_num=sam_code_num)
                    Num_RandDSampleDNAExtractInfo = len(RandDSampleDNAExtractInfo)
                    RandDSampleDNAExtractInfoState = '无信息'
                    if not Num_RandDSampleDNAExtractInfo == 0:
                        if RandDSampleDNAExtractInfo[Num_RandDSampleDNAExtractInfo-1].Next_TaskProgress_Sign == '0':
                            RandDSampleDNAExtractInfoState = 'DNA提取实验共进行' + str(Num_RandDSampleDNAExtractInfo) + '次，但第' + str(
                                Num_RandDSampleDNAExtractInfo) + '次的信息未审核'
                            PreLibCon_Sign = 0
                            DNAExtract_review_Sign = 1
                        elif RandDSampleDNAExtractInfo[Num_RandDSampleDNAExtractInfo-1].Next_TaskProgress_Sign == '1':
                            if RandDSampleDNAExtractInfo[Num_RandDSampleDNAExtractInfo-1].Next_TaskProgress == '预文库构建':
                                RandDSampleDNAExtractInfoState = 'DNA提取实验共进行' + str(Num_RandDSampleDNAExtractInfo) + '次，且第' + str(
                                    Num_RandDSampleDNAExtractInfo) + '次的信息已审核通过'
                                if RandDSampleDNAExtractInfo[Num_RandDSampleDNAExtractInfo-1].PreLibCon_Sign == '0':
                                    PreLibCon_Sign = 0
                            else:
                                RandDSampleDNAExtractInfoState = 'DNA提取实验共进行' + str(Num_RandDSampleDNAExtractInfo) + '次，且第' + str(
                                    Num_RandDSampleDNAExtractInfo) + '次的信息审核不通过，重新进行' + RandDSampleDNAExtractInfo[
                                                                     Num_RandDSampleDNAExtractInfo - 1].Next_TaskProgress + '任务'
                        elif RandDSampleDNAExtractInfo[Num_RandDSampleDNAExtractInfo-1].Next_TaskProgress_Sign == '2':
                            RandDSampleDNAExtractInfoState = 'DNA提取实验共进行'+str(Num_RandDSampleDNAExtractInfo)+'次，但第'+str(Num_RandDSampleDNAExtractInfo)+'次信息录入后任务暂停'
                        elif RandDSampleDNAExtractInfo[Num_RandDSampleDNAExtractInfo-1].Next_TaskProgress_Sign == '3':
                            RandDSampleDNAExtractInfoState = 'DNA提取实验共进行'+str(Num_RandDSampleDNAExtractInfo)+'次，但第'+str(Num_RandDSampleDNAExtractInfo)+'次信息录入后任务终止'

                    RandDSamplePreLibConInfo = models.PreLibConInfo.objects.filter(sam_code_num=sam_code_num)
                    Num_RandDSamplePreLibConInfo = len(RandDSamplePreLibConInfo)
                    RandDSamplePreLibConInfoState = '无信息'
                    if not Num_RandDSamplePreLibConInfo == 0:
                        if RandDSamplePreLibConInfo[Num_RandDSamplePreLibConInfo - 1].Next_TaskProgress_Sign == '0':
                            RandDSamplePreLibConInfoState = '预文库构建实验共进行' + str(Num_RandDSamplePreLibConInfo) + '次，但第' + str(
                                Num_RandDSamplePreLibConInfo) + '次的信息未审核'
                            FinalLibCon_Sign = 0
                            PreLibCon_review_Sign = 1
                        elif RandDSamplePreLibConInfo[Num_RandDSamplePreLibConInfo - 1].Next_TaskProgress_Sign == '1':
                            if RandDSamplePreLibConInfo[Num_RandDSamplePreLibConInfo-1].Next_TaskProgress == '终文库构建':
                                RandDSamplePreLibConInfoState = '预文库构建实验共进行' + str(Num_RandDSamplePreLibConInfo) + '次，且第' + str(
                                    Num_RandDSamplePreLibConInfo) + '次的信息已审核通过'
                                if RandDSamplePreLibConInfo[Num_RandDSamplePreLibConInfo-1].FinalLibCon_Sign == '0':
                                    FinalLibCon_Sign = 0
                            else:
                                RandDSamplePreLibConInfoState = '预文库构建实验共进行' + str(Num_RandDSamplePreLibConInfo) + '次，且第' + str(
                                    Num_RandDSamplePreLibConInfo) + '次的信息审核不通过，重新进行' + RandDSamplePreLibConInfo[
                                    Num_RandDSamplePreLibConInfo - 1].Next_TaskProgress + '任务'
                        elif RandDSamplePreLibConInfo[Num_RandDSamplePreLibConInfo - 1].Next_TaskProgress_Sign == '2':
                            RandDSamplePreLibConInfoState = '预文库构建实验共进行' + str(Num_RandDSamplePreLibConInfo) + '次，但第' + str(
                                Num_RandDSamplePreLibConInfo) + '次信息录入后任务暂停'
                        elif RandDSamplePreLibConInfo[Num_RandDSamplePreLibConInfo - 1].Next_TaskProgress_Sign == '3':
                            RandDSamplePreLibConInfoState = '预文库构建实验共进行' + str(Num_RandDSamplePreLibConInfo) + '次，但第' + str(
                                Num_RandDSamplePreLibConInfo) + '次信息录入后任务终止'

                    RandDSampleFinLibConInfo = models.FinLibConInfo.objects.filter(sam_code_num=sam_code_num)
                    Num_RandDSampleFinLibConInfo = len(RandDSampleFinLibConInfo)
                    RandDSampleFinLibConInfoState = '无信息'
                    if not Num_RandDSampleFinLibConInfo == 0:
                        if RandDSampleFinLibConInfo[Num_RandDSampleFinLibConInfo - 1].Next_TaskProgress_Sign == '0':
                            RandDSampleFinLibConInfoState = '终文库构建实验共进行' + str(Num_RandDSampleFinLibConInfo) + '次，但第' + str(
                                Num_RandDSampleFinLibConInfo) + '次的信息未审核'
                            ComputerSeq_Sign = 0
                            FinalLibCon_review_Sign = 1
                        elif RandDSampleFinLibConInfo[Num_RandDSampleFinLibConInfo - 1].Next_TaskProgress_Sign == '1':
                            if RandDSampleFinLibConInfo[Num_RandDSampleFinLibConInfo-1].Next_TaskProgress == '上机测序':
                                RandDSampleFinLibConInfoState = '终文库构建实验共进行' + str(Num_RandDSampleFinLibConInfo) + '次，且第' + str(
                                    Num_RandDSampleFinLibConInfo) + '次的信息已审核通过'
                                if RandDSampleFinLibConInfo[Num_RandDSampleFinLibConInfo - 1].ComputerSeq_Sign == '0':
                                    ComputerSeq_Sign = 0
                            else:
                                RandDSampleFinLibConInfoState = '终文库构建实验共进行' + str(Num_RandDSampleFinLibConInfo) + '次，且第' + str(
                                    Num_RandDSampleFinLibConInfo) + '次的信息审核不通过，重新进行' + RandDSampleFinLibConInfo[
                                    Num_RandDSampleFinLibConInfo - 1].Next_TaskProgress + '任务'
                        elif RandDSampleFinLibConInfo[Num_RandDSampleFinLibConInfo - 1].Next_TaskProgress_Sign == '2':
                            RandDSampleFinLibConInfoState = '终文库构建实验共进行' + str(Num_RandDSampleFinLibConInfo) + '次，但第' + str(
                                Num_RandDSampleFinLibConInfo) + '次信息录入后任务暂停'
                        elif RandDSampleFinLibConInfo[Num_RandDSampleFinLibConInfo - 1].Next_TaskProgress_Sign == '3':
                            RandDSampleFinLibConInfoState = '终文库构建实验共进行' + str(Num_RandDSampleFinLibConInfo) + '次，但第' + str(
                                Num_RandDSampleFinLibConInfo) + '次信息录入后任务终止'

                    RandDSampleComputerSeqInfo = models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num)
                    Num_RandDSampleComputerSeqInfo = len(RandDSampleComputerSeqInfo)
                    RandDSampleComputerSeqInfoState = '无信息'
                    if not Num_RandDSampleComputerSeqInfo == 0:
                        if RandDSampleComputerSeqInfo[Num_RandDSampleComputerSeqInfo - 1].Next_TaskProgress_Sign == '0':
                            RandDSampleComputerSeqInfoState = '上机测序实验共进行' + str(Num_RandDSampleComputerSeqInfo) + '次，但第' + str(
                                Num_RandDSampleComputerSeqInfo) + '次的信息未审核'
                            Bioinfo_Sign = 0
                            ComputerSeq_review_Sign = 1
                        elif RandDSampleComputerSeqInfo[Num_RandDSampleComputerSeqInfo - 1].Next_TaskProgress_Sign == '1':
                            if RandDSampleComputerSeqInfo[Num_RandDSampleComputerSeqInfo-1].ReviewResult == '通过':
                                RandDSampleComputerSeqInfoState = '上机测序实验共进行' + str(Num_RandDSampleComputerSeqInfo) + '次，且第' + str(
                                    Num_RandDSampleComputerSeqInfo) + '次的信息已审核通过'
                                if RandDSampleComputerSeqInfo[Num_RandDSampleComputerSeqInfo-1].Bioinfo_Sign == '0':
                                    Bioinfo_Sign = 0
                            elif RandDSampleComputerSeqInfo[Num_RandDSampleComputerSeqInfo-1].ReviewResult == '退回':
                                RandDSampleComputerSeqInfoState = '上机测序实验共进行' + str(Num_RandDSampleComputerSeqInfo) + '次，且第' + str(
                                    Num_RandDSampleComputerSeqInfo) + '次的信息审核不通过，已退回重新进行上机测序任务'
                        elif RandDSampleComputerSeqInfo[Num_RandDSampleComputerSeqInfo - 1].ReviewResult == '暂停':
                            RandDSampleComputerSeqInfoState = '上机测序实验共进行' + str(Num_RandDSampleComputerSeqInfo) + '次，但第' + str(
                                Num_RandDSampleComputerSeqInfo) + '次信息录入后任务暂停'
                        elif RandDSampleComputerSeqInfo[Num_RandDSampleComputerSeqInfo - 1].ReviewResult == '终止':
                            RandDSampleComputerSeqInfoState = '上机测序实验共进行' + str(Num_RandDSampleComputerSeqInfo) + '次，但第' + str(
                                Num_RandDSampleComputerSeqInfo) + '次信息录入后任务终止'
                if SampleSource == '研发样本':
                    RandDSampleInfo = models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num,
                                                                            sample_review__in=[0, 1, 2, 3])
                    Num_RandDSampleInfo = len(RandDSampleInfo)
                    RandDSampleInputState  = '无信息'
                    RandDSampleInfostate = '无信息'
                    if not Num_RandDSampleInfo == 0:
                        sampleIsExist = '样本存在'
                        RandDSampleInputState = '样本信息已登记'
                        if RandDSampleInfo[0].sample_review == '0':
                            RandDSampleInfostate = '未审核'
                            DNAExtract_Sign = 0
                            RandDSampleInfo_review_Sign = 1
                        elif RandDSampleInfo[0].sample_review == '1':
                            RandDSampleInfostate = '审核通过'
                            if RandDSampleInfo[0].DNAExtract_Sign == '0':
                                print 'DNAExtract_Sign==0'
                                DNAExtract_Sign = 0
                        elif RandDSampleInfo[0].sample_review == '2':
                            RandDSampleInfostate = '任务暂停'
                        elif RandDSampleInfo[0].sample_review == '3':
                            RandDSampleInfostate = '任务终止'
                        elif RandDSampleInfo[0].sample_review == '4':
                            RandDSampleInfostate = '样本登记信息被退回'
                    else:
                        sampleIsExist = '样本不存在'
                    RandDSampleInfoReviewed = models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num,
                                                                                    sample_review__in=[1, 2, 3])
                    Num_RandDSampleInfoReviewed = len(RandDSampleInfoReviewed)

                    if not Num_RandDSampleInfo == 0:
                        if RandDSampleInfo[0].TissueSampleSign == '0':
                            TissueSampleSign = 0
                        else:
                            TissueSampleSign = 1

                    RandDSamplePretreatmentInfo = models.RandDSamplePretreatmentInfo.objects.filter(sam_code_num=sam_code_num)
                    Num_RandDSamplePretreatmentInfo = len(RandDSamplePretreatmentInfo)
                    RandDSamplePretreatmentInfoState = '无信息'
                    if not Num_RandDSamplePretreatmentInfo == 0:
                        if RandDSamplePretreatmentInfo[0].Next_TaskProgress_Sign == '0':
                            RandDSamplePretreatmentInfoState = '信息已录入，但未审核'
                            DNAExtract_Sign = 0
                            RandDSamplePretreatmentInfo_review_Sign = 1
                        elif RandDSamplePretreatmentInfo[0].Next_TaskProgress_Sign == '1':
                            RandDSamplePretreatmentInfoState = '信息已录入，且审核通过'
                            if RandDSamplePretreatmentInfo[0].DNAExtract_Sign == '0':
                                DNAExtract_Sign = 0
                        elif RandDSamplePretreatmentInfo[0].Next_TaskProgress_Sign == '2':
                            RandDSamplePretreatmentInfoState = '信息已录入，且任务暂停'
                        elif RandDSamplePretreatmentInfo[0].Next_TaskProgress_Sign == '3':
                            RandDSamplePretreatmentInfoState = '信息已录入，且任务终止'

                    RandDSampleDNAExtractInfo = models.RandDSampleDNAExtractInfo.objects.filter(sam_code_num=sam_code_num)
                    Num_RandDSampleDNAExtractInfo = len(RandDSampleDNAExtractInfo)
                    RandDSampleDNAExtractInfoState = '无信息'
                    if not Num_RandDSampleDNAExtractInfo == 0:
                        if RandDSampleDNAExtractInfo[Num_RandDSampleDNAExtractInfo-1].Next_TaskProgress_Sign == '0':
                            RandDSampleDNAExtractInfoState = 'DNA提取实验共进行' + str(Num_RandDSampleDNAExtractInfo) + '次，但第' + str(
                                Num_RandDSampleDNAExtractInfo) + '次的信息未审核'
                            PreLibCon_Sign = 0
                            DNAExtract_review_Sign = 1
                        elif RandDSampleDNAExtractInfo[Num_RandDSampleDNAExtractInfo-1].Next_TaskProgress_Sign == '1':
                            if RandDSampleDNAExtractInfo[Num_RandDSampleDNAExtractInfo-1].Next_TaskProgress == '预文库构建':
                                RandDSampleDNAExtractInfoState = 'DNA提取实验共进行' + str(Num_RandDSampleDNAExtractInfo) + '次，且第' + str(
                                    Num_RandDSampleDNAExtractInfo) + '次的信息已审核通过'
                                if RandDSampleDNAExtractInfo[Num_RandDSampleDNAExtractInfo-1].PreLibCon_Sign == '0':
                                    PreLibCon_Sign = 0
                            else:
                                RandDSampleDNAExtractInfoState = 'DNA提取实验共进行' + str(Num_RandDSampleDNAExtractInfo) + '次，且第' + str(
                                    Num_RandDSampleDNAExtractInfo) + '次的信息审核不通过，重新进行' + RandDSampleDNAExtractInfo[
                                                                     Num_RandDSampleDNAExtractInfo - 1].Next_TaskProgress + '任务'
                        elif RandDSampleDNAExtractInfo[Num_RandDSampleDNAExtractInfo-1].Next_TaskProgress_Sign == '2':
                            RandDSampleDNAExtractInfoState = 'DNA提取实验共进行'+str(Num_RandDSampleDNAExtractInfo)+'次，但第'+str(Num_RandDSampleDNAExtractInfo)+'次信息录入后任务暂停'
                        elif RandDSampleDNAExtractInfo[Num_RandDSampleDNAExtractInfo-1].Next_TaskProgress_Sign == '3':
                            RandDSampleDNAExtractInfoState = 'DNA提取实验共进行'+str(Num_RandDSampleDNAExtractInfo)+'次，但第'+str(Num_RandDSampleDNAExtractInfo)+'次信息录入后任务终止'

                    RandDSamplePreLibConInfo = models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num)
                    Num_RandDSamplePreLibConInfo = len(RandDSamplePreLibConInfo)
                    RandDSamplePreLibConInfoState = '无信息'
                    if not Num_RandDSamplePreLibConInfo == 0:
                        if RandDSamplePreLibConInfo[Num_RandDSamplePreLibConInfo - 1].Next_TaskProgress_Sign == '0':
                            RandDSamplePreLibConInfoState = '预文库构建实验共进行' + str(Num_RandDSamplePreLibConInfo) + '次，但第' + str(
                                Num_RandDSamplePreLibConInfo) + '次的信息未审核'
                            FinalLibCon_Sign = 0
                            PreLibCon_review_Sign = 1
                        elif RandDSamplePreLibConInfo[Num_RandDSamplePreLibConInfo - 1].Next_TaskProgress_Sign == '1':
                            if RandDSamplePreLibConInfo[Num_RandDSamplePreLibConInfo-1].Next_TaskProgress == '终文库构建':
                                RandDSamplePreLibConInfoState = '预文库构建实验共进行' + str(Num_RandDSamplePreLibConInfo) + '次，且第' + str(
                                    Num_RandDSamplePreLibConInfo) + '次的信息已审核通过'
                                if RandDSamplePreLibConInfo[Num_RandDSamplePreLibConInfo-1].FinalLibCon_Sign == '0':
                                    FinalLibCon_Sign = 0
                            else:
                                RandDSamplePreLibConInfoState = '预文库构建实验共进行' + str(Num_RandDSamplePreLibConInfo) + '次，且第' + str(
                                    Num_RandDSamplePreLibConInfo) + '次的信息审核不通过，重新进行' + RandDSamplePreLibConInfo[
                                    Num_RandDSamplePreLibConInfo - 1].Next_TaskProgress + '任务'
                        elif RandDSamplePreLibConInfo[Num_RandDSamplePreLibConInfo - 1].Next_TaskProgress_Sign == '2':
                            RandDSamplePreLibConInfoState = '预文库构建实验共进行' + str(Num_RandDSamplePreLibConInfo) + '次，但第' + str(
                                Num_RandDSamplePreLibConInfo) + '次信息录入后任务暂停'
                        elif RandDSamplePreLibConInfo[Num_RandDSamplePreLibConInfo - 1].Next_TaskProgress_Sign == '3':
                            RandDSamplePreLibConInfoState = '预文库构建实验共进行' + str(Num_RandDSamplePreLibConInfo) + '次，但第' + str(
                                Num_RandDSamplePreLibConInfo) + '次信息录入后任务终止'

                    RandDSampleFinLibConInfo = models.RandDSampleFinLibConInfo.objects.filter(sam_code_num=sam_code_num)
                    Num_RandDSampleFinLibConInfo = len(RandDSampleFinLibConInfo)
                    RandDSampleFinLibConInfoState = '无信息'
                    if not Num_RandDSampleFinLibConInfo == 0:
                        if RandDSampleFinLibConInfo[Num_RandDSampleFinLibConInfo - 1].Next_TaskProgress_Sign == '0':
                            RandDSampleFinLibConInfoState = '终文库构建实验共进行' + str(Num_RandDSampleFinLibConInfo) + '次，但第' + str(
                                Num_RandDSampleFinLibConInfo) + '次的信息未审核'
                            ComputerSeq_Sign = 0
                            FinalLibCon_review_Sign = 1
                        elif RandDSampleFinLibConInfo[Num_RandDSampleFinLibConInfo - 1].Next_TaskProgress_Sign == '1':
                            if RandDSampleFinLibConInfo[Num_RandDSampleFinLibConInfo-1].Next_TaskProgress == '上机测序':
                                RandDSampleFinLibConInfoState = '终文库构建实验共进行' + str(Num_RandDSampleFinLibConInfo) + '次，且第' + str(
                                    Num_RandDSampleFinLibConInfo) + '次的信息已审核通过'
                                if RandDSampleFinLibConInfo[Num_RandDSampleFinLibConInfo - 1].ComputerSeq_Sign == '0':
                                    ComputerSeq_Sign = 0
                            else:
                                RandDSampleFinLibConInfoState = '终文库构建实验共进行' + str(Num_RandDSampleFinLibConInfo) + '次，且第' + str(
                                    Num_RandDSampleFinLibConInfo) + '次的信息审核不通过，重新进行' + RandDSampleFinLibConInfo[
                                    Num_RandDSampleFinLibConInfo - 1].Next_TaskProgress + '任务'
                        elif RandDSampleFinLibConInfo[Num_RandDSampleFinLibConInfo - 1].Next_TaskProgress_Sign == '2':
                            RandDSampleFinLibConInfoState = '终文库构建实验共进行' + str(Num_RandDSampleFinLibConInfo) + '次，但第' + str(
                                Num_RandDSampleFinLibConInfo) + '次信息录入后任务暂停'
                        elif RandDSampleFinLibConInfo[Num_RandDSampleFinLibConInfo - 1].Next_TaskProgress_Sign == '3':
                            RandDSampleFinLibConInfoState = '终文库构建实验共进行' + str(Num_RandDSampleFinLibConInfo) + '次，但第' + str(
                                Num_RandDSampleFinLibConInfo) + '次信息录入后任务终止'

                    RandDSampleComputerSeqInfo = models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num)
                    Num_RandDSampleComputerSeqInfo = len(RandDSampleComputerSeqInfo)
                    RandDSampleComputerSeqInfoState = '无信息'
                    if not Num_RandDSampleComputerSeqInfo == 0:
                        if RandDSampleComputerSeqInfo[Num_RandDSampleComputerSeqInfo - 1].Next_TaskProgress_Sign == '0':
                            RandDSampleComputerSeqInfoState = '上机测序实验共进行' + str(Num_RandDSampleComputerSeqInfo) + '次，但第' + str(
                                Num_RandDSampleComputerSeqInfo) + '次的信息未审核'
                            Bioinfo_Sign = 0
                            ComputerSeq_review_Sign = 1
                        elif RandDSampleComputerSeqInfo[Num_RandDSampleComputerSeqInfo - 1].Next_TaskProgress_Sign == '1':
                            if RandDSampleComputerSeqInfo[Num_RandDSampleComputerSeqInfo-1].ReviewResult == '通过':
                                RandDSampleComputerSeqInfoState = '上机测序实验共进行' + str(Num_RandDSampleComputerSeqInfo) + '次，且第' + str(
                                    Num_RandDSampleComputerSeqInfo) + '次的信息已审核通过'
                                if RandDSampleComputerSeqInfo[Num_RandDSampleComputerSeqInfo-1].Bioinfo_Sign == '0':
                                    Bioinfo_Sign = 0
                            elif RandDSampleComputerSeqInfo[Num_RandDSampleComputerSeqInfo-1].ReviewResult == '退回':
                                RandDSampleComputerSeqInfoState = '上机测序实验共进行' + str(Num_RandDSampleComputerSeqInfo) + '次，且第' + str(
                                    Num_RandDSampleComputerSeqInfo) + '次的信息审核不通过，已退回重新进行上机测序任务'
                        elif RandDSampleComputerSeqInfo[Num_RandDSampleComputerSeqInfo - 1].ReviewResult == '暂停':
                            RandDSampleComputerSeqInfoState = '上机测序实验共进行' + str(Num_RandDSampleComputerSeqInfo) + '次，但第' + str(
                                Num_RandDSampleComputerSeqInfo) + '次信息录入后任务暂停'
                        elif RandDSampleComputerSeqInfo[Num_RandDSampleComputerSeqInfo - 1].ReviewResult == '终止':
                            RandDSampleComputerSeqInfoState = '上机测序实验共进行' + str(Num_RandDSampleComputerSeqInfo) + '次，但第' + str(
                                Num_RandDSampleComputerSeqInfo) + '次信息录入后任务终止'

                BioinfoDataAnalysisInfo = models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num)
                Num_BioinfoDataAnalysisInfo = len(BioinfoDataAnalysisInfo)
                Num_Report_Make = 0
                Num_Medical_Examine = 0
                Num_Operate_Examine = 0
                Num_Report_Send = 0
                BioinfoDataAnalysisInfoState = '无信息'
                Report_Make_State = '无信息'
                Medical_Examine_State = '无信息'
                Operate_Examine_State = '无信息'
                Report_Send_State = '无信息'
                if not Num_BioinfoDataAnalysisInfo == 0:
                    if BioinfoDataAnalysisInfo[Num_BioinfoDataAnalysisInfo - 1].BioinfoResult_Sign == '0':
                        BioinfoDataAnalysisInfoState = '生信分析共进行' + str(Num_BioinfoDataAnalysisInfo) + '次，但第' + str(
                            Num_BioinfoDataAnalysisInfo) + '次的信息未审核'
                        Report_Make_Sign = 0
                        Bioinfo_review_Sign = 1
                    elif BioinfoDataAnalysisInfo[Num_BioinfoDataAnalysisInfo - 1].BioinfoResult_Sign == '1':
                        if BioinfoDataAnalysisInfo[Num_BioinfoDataAnalysisInfo - 1].Examine_Result == '通过':
                            BioinfoDataAnalysisInfoState = '生信分析共进行' + str(Num_BioinfoDataAnalysisInfo) + '次，且第' + str(
                                Num_BioinfoDataAnalysisInfo) + '次的信息已审核通过'
                            if BioinfoDataAnalysisInfo[Num_BioinfoDataAnalysisInfo - 1].Report_Make_Sign == '0':
                                Report_Make_Sign = 0
                        else:
                            BioinfoDataAnalysisInfoState = '生信分析共进行' + str(Num_BioinfoDataAnalysisInfo) + '次，且第' + str(
                                Num_BioinfoDataAnalysisInfo) + '次的信息审核不通过，重新进行数据分析任务'
                    elif BioinfoDataAnalysisInfo[Num_BioinfoDataAnalysisInfo - 1].BioinfoResult_Sign == '2':
                        BioinfoDataAnalysisInfoState = '生信分析共进行' + str(Num_BioinfoDataAnalysisInfo) + '次，但第' + str(
                            Num_BioinfoDataAnalysisInfo) + '次信息录入后任务暂停'
                    elif BioinfoDataAnalysisInfo[Num_BioinfoDataAnalysisInfo - 1].BioinfoResult_Sign == '3':
                        BioinfoDataAnalysisInfoState = '生信分析共进行' + str(Num_BioinfoDataAnalysisInfo) + '次，但第' + str(
                            Num_BioinfoDataAnalysisInfo) + '次信息录入后任务终止'

                    if BioinfoDataAnalysisInfo[Num_BioinfoDataAnalysisInfo - 1].Report_Make_Sign == '1':
                        Num_Report_Make = 1
                        if BioinfoDataAnalysisInfo[Num_BioinfoDataAnalysisInfo - 1].Medical_Examine_Result == '通过':
                            Num_Medical_Examine = 1
                            Report_Make_State = '生信分析报告已制作！'
                            Medical_Examine_State = '遗传咨询师审核已通过！'
                            if BioinfoDataAnalysisInfo[Num_BioinfoDataAnalysisInfo - 1].Operate_Examine_Result == '通过':
                                Num_Operate_Examine = 1
                                Operate_Examine_State = '运营审核已通过！'
                                if BioinfoDataAnalysisInfo[Num_BioinfoDataAnalysisInfo - 1].Report_Send_Sign == '1':
                                    Num_Report_Send = 1
                                    Report_Send_State = '报告已发送！'
                            elif BioinfoDataAnalysisInfo[Num_BioinfoDataAnalysisInfo - 1].Operate_Examine_Result == '不通过':
                                Num_Report_Make = 0
                                Num_Medical_Examine = 0
                                Report_Make_State = '运营审核不通过，已退回修改！'
                                Operate_Examine_State = '运营审核不通过，已退回修改！'
                        elif BioinfoDataAnalysisInfo[Num_BioinfoDataAnalysisInfo - 1].Medical_Examine_Result == '不通过':
                            Num_Report_Make = 0
                            Report_Make_State = '遗传咨询师审核不通过，已退回修改！'
                            Medical_Examine_State = '遗传咨询师审核不通过，已退回修改！'
                        else:
                            Report_Make_State = '生信分析报告已制作！'


                if DNAExtract_Sign == 0:
                    Num_RandDSampleDNAExtractInfo = 0
                    Num_RandDSamplePreLibConInfo = 0
                    Num_RandDSampleFinLibConInfo = 0
                    Num_RandDSampleComputerSeqInfo = 0
                elif PreLibCon_Sign == 0:
                    Num_RandDSamplePreLibConInfo = 0
                    Num_RandDSampleFinLibConInfo = 0
                    Num_RandDSampleComputerSeqInfo = 0
                elif FinalLibCon_Sign == 0:
                    Num_RandDSampleFinLibConInfo = 0
                    Num_RandDSampleComputerSeqInfo = 0
                elif ComputerSeq_Sign == 0:
                    Num_RandDSampleComputerSeqInfo = 0
                elif Bioinfo_Sign == 0:
                    Num_BioinfoDataAnalysisInfo = 0
                elif Report_Make_Sign == 0:
                    Num_Report_Make = 0

                return render(request, "modelspage/homepage.html",
                              {"userinfo": temp, "myInfo": temp_myInfo, "NumOfSendReport": NumOfSendReport,
                               "NumOfClinicalSample": NumOfClinicalSample, "NumOfRandDSample": NumOfRandDSample,
                               "sam_code_num": sam_code_num, "SampleSource": SampleSource,
                               "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread,
                               "TissueSampleSign": TissueSampleSign,
                               "sampleIsExist": sampleIsExist,
                               "RandDSampleInputState": RandDSampleInputState,
                               "Num_RandDSampleInfo": Num_RandDSampleInfo,
                               "RandDSampleInfostate": RandDSampleInfostate,
                               "Num_RandDSampleInfoReviewed": Num_RandDSampleInfoReviewed,
                               "Num_RandDSamplePretreatmentInfo": Num_RandDSamplePretreatmentInfo,
                               "RandDSamplePretreatmentInfoState": RandDSamplePretreatmentInfoState,
                               "Num_RandDSampleDNAExtractInfo": Num_RandDSampleDNAExtractInfo,
                               "RandDSampleDNAExtractInfoState": RandDSampleDNAExtractInfoState,
                               "Num_RandDSamplePreLibConInfo": Num_RandDSamplePreLibConInfo,
                               "RandDSamplePreLibConInfoState": RandDSamplePreLibConInfoState,
                               "Num_RandDSampleFinLibConInfo": Num_RandDSampleFinLibConInfo,
                               "RandDSampleFinLibConInfoState": RandDSampleFinLibConInfoState,
                               "Num_RandDSampleComputerSeqInfo": Num_RandDSampleComputerSeqInfo,
                               "RandDSampleComputerSeqInfoState": RandDSampleComputerSeqInfoState,
                               "Num_BioinfoDataAnalysisInfo": Num_BioinfoDataAnalysisInfo,
                               "BioinfoDataAnalysisInfoState": BioinfoDataAnalysisInfoState,
                               "Num_Report_Make": Num_Report_Make,
                               "Report_Make_State": Report_Make_State,
                               "Num_Medical_Examine": Num_Medical_Examine,
                               "Medical_Examine_State": Medical_Examine_State,
                               "Num_Operate_Examine": Num_Operate_Examine,
                               "Operate_Examine_State": Operate_Examine_State,
                               "Num_Report_Send": Num_Report_Send,
                               "Report_Send_State": Report_Send_State,
                               "RandDSampleInfo_review_Sign": RandDSampleInfo_review_Sign,
                               "RandDSamplePretreatmentInfo_review_Sign": RandDSamplePretreatmentInfo_review_Sign,
                               "DNAExtract_review_Sign": DNAExtract_review_Sign,
                               "PreLibCon_review_Sign": PreLibCon_review_Sign,
                               "FinalLibCon_review_Sign": FinalLibCon_review_Sign,
                               "ComputerSeq_review_Sign": ComputerSeq_review_Sign,
                               "Bioinfo_review_Sign": Bioinfo_review_Sign,
                               })
            else:
                return render(request, "modelspage/homepage.html",
                              {"userinfo": temp, "myInfo": temp_myInfo, "NumOfSendReport": NumOfSendReport,
                               "NumOfClinicalSample": NumOfClinicalSample, "NumOfRandDSample": NumOfRandDSample,
                               "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread,})

# 临床样本登记首页
def ClinicalSampleRegistration(request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户系统信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        if department == '管理员':
            # temp_mySample = models.clinicalSampleInfo.objects.all()  # 临床样本信息
            temp_not_audited = models.clinicalSampleInfo.objects.filter(sample_review=0)  # 研发样本未审核信息
            temp_draft = models.clinicalSampleInfo.objects.filter(sample_review='')  # 研发样本草稿信息
            temp_return = models.clinicalSampleInfo.objects.filter(sample_review=4)  # 研发审核退回样本信息
            temp_audited = models.clinicalSampleInfo.objects.filter(sample_review__in=[1, 2, 3])  # 研发样本已审核信息
        else:
            temp_not_audited = models.clinicalSampleInfo.objects.filter(username=username, sample_review=0)  # 研发样本未审核信息
            temp_draft = models.clinicalSampleInfo.objects.filter(username=username, sample_review='')  # 研发样本草稿信息
            temp_return = models.clinicalSampleInfo.objects.filter(username=username, sample_review=4)  # 研发审核退回样本信息
            temp_audited = models.clinicalSampleInfo.objects.filter(username=username,
                                                                    sample_review__in=[1, 2, 3])  # 研发样本已审核信息
        return render(request, "modelspage/sample_entry.html",
                      {"userinfo": temp, "not_audited": temp_not_audited, "audited": temp_audited, "draft": temp_draft,
                       "return": temp_return, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 临床样本登记数据录入页
def ClinicalSampleRegistrationInputdata(request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
            username=username)  # 用户操作权限信息
        # print 'ClinicalSampleRegistration: ', temp_UserOperationPermissionsInfo.ClinicalSampleRegistration
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户系统信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        if temp_UserOperationPermissionsInfo.ClinicalSampleRegistration == '1':
            button_name = ''  # 按钮名字
            if request.method == "POST":
                # 判断哪个按钮提交的数据
                if request.POST.has_key('singleAddSample'):
                    button_name = 'singleAddSample'
                elif request.POST.has_key('batchAddSample'):
                    button_name = 'batchAddSample'

            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            user = User.objects.get(username=username)
            temp_userlist = User.objects.filter(first_name='市场部', is_active=user.is_active)

            if button_name == 'singleAddSample':
                return render(request, "modelspage/sample_reg.html",
                              {"userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                               "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})
            else:
                # print 'batchAddSample'
                return render(request, "modelspage/CliSampleRegisterBatchInput.html",
                              {"userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                               "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})
        else:
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            return render(request, "modelspage/PermissionsPrompt.html",
                          {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 临床样本登记数据展示页
def ClinicalSampleShowData(request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}
        sam_code_num = ''
        button_name = ''
        SampleAuditor = ''
        if request.method == "POST":
            print '患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号: ', sam_code_num

            SampleAuditor = request.POST.get('SampleAuditor')

            # 判断哪个按钮提交的数据
            if request.POST.has_key('UnauditedShowData'):
                button_name = 'UnauditedShowData'
            elif request.POST.has_key('AuditedShowData'):
                button_name = 'AuditedShowData'
            elif request.POST.has_key('DraftData'):
                button_name = 'DraftData'
            elif request.POST.has_key('submitReview'):
                button_name = 'submitReview'
            elif request.POST.has_key('returnData'):
                button_name = 'returnData'
            elif request.POST.has_key('ModifyData'):
                button_name = 'ModifyData'
            elif request.POST.has_key('delete'):
                temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                    username=username)  # 用户操作权限信息
                if temp_UserOperationPermissionsInfo.ClinicalSampleRegistration == '1':
                    temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                        ReadingState='未读')
                    num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
                    temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
                    models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num).delete()  # 删除信息
                    if department == '管理员':
                        temp_not_audited = models.clinicalSampleInfo.objects.filter(sample_review=0)  # 研发样本未审核信息
                        temp_draft = models.clinicalSampleInfo.objects.filter(sample_review='')  # 研发样本草稿信息
                        temp_return = models.clinicalSampleInfo.objects.filter(sample_review=4)  # 研发审核退回样本信息
                        temp_audited = models.clinicalSampleInfo.objects.filter(
                            sample_review__in=[1, 2, 3])  # 研发样本已审核信息
                    else:
                        temp_not_audited = models.clinicalSampleInfo.objects.filter(username=username,
                                                                                    sample_review=0)  # 研发样本未审核信息
                        temp_draft = models.clinicalSampleInfo.objects.filter(username=username,
                                                                              sample_review='')  # 研发样本草稿信息
                        temp_return = models.clinicalSampleInfo.objects.filter(username=username,
                                                                               sample_review=4)  # 研发审核退回样本信息
                        temp_audited = models.clinicalSampleInfo.objects.filter(username=username,
                                                                                sample_review__in=[1, 2, 3])  # 研发样本已审核信息
                    return render(request, "modelspage/sample_entry.html",
                                  {"userinfo": temp, "not_audited": temp_not_audited, "audited": temp_audited,
                                   "draft": temp_draft,
                                   "return": temp_return, "myInfo": temp_myInfo,
                                   "SystemMessage": temp_SystemMessage_Unread,
                                   "num_SystemMessage_Unread": num_SystemMessage_Unread})
                else:
                    # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
                    temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                        ReadingState='未读')  # 用户信息
                    num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
                    temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
                    return render(request, "modelspage/PermissionsPrompt.html",
                                  {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                                   "num_SystemMessage_Unread": num_SystemMessage_Unread})

        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户系统信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_data = models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num)  # 临床样本信息
        if temp_data[0].TissueSampleSign == '0':
            TissueSampleSign = '否'
        else:
            TissueSampleSign = '是'

        if button_name == 'UnauditedShowData':
            return render(request, "modelspage/sample_showData.html",
                          {"userinfo": temp, "data": temp_data, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread, "TissueSampleSign": TissueSampleSign})
        if button_name == 'AuditedShowData':
            return render(request, "modelspage/sample_AuditedshowData.html",
                          {"userinfo": temp, "data": temp_data, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread, "TissueSampleSign": TissueSampleSign})
        if button_name == 'ModifyData':
            return render(request, "modelspage/sample_ModifyData.html",
                          {"userinfo": temp, "data": temp_data, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread, "TissueSampleSign": TissueSampleSign})
        elif button_name == 'DraftData':
            temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                username=username)  # 用户操作权限信息
            if temp_UserOperationPermissionsInfo.ClinicalSampleRegistration == '1':
                user = User.objects.get(username=username)
                temp_userlist = User.objects.filter(first_name='市场部', is_active=user.is_active)
                return render(request, "modelspage/sample_DraftData.html",
                              {"userinfo": temp, "data": temp_data, "myInfo": temp_myInfo, "userlist": temp_userlist,
                               "SystemMessage": temp_SystemMessage_Unread, "TissueSampleSign": TissueSampleSign,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})
            else:
                # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
                temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                    ReadingState='未读')  # 用户信息
                num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
                temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
                return render(request, "modelspage/PermissionsPrompt.html",
                              {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'submitReview':
            temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                username=username)  # 用户操作权限信息
            if temp_UserOperationPermissionsInfo.RandDSampleInfoInputHomePage == '1':
                models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num).update(sample_review=0)  # 临床样本信息
                # 添加系统消息
                taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                Title = '通知：临检样本审核任务'  # 系统消息标题
                Message = username + '录入一个临检样本！样本编号为：' + sam_code_num + '。请尽快完成审核！'  # 系统邮件正文
                models.UserSystemMessage.objects.create(
                    # 用户信息
                    Sender=username,  # 发送者
                    Receiver=SampleAuditor,  # 接收者
                    # 信息内容
                    Time=taskTime,  # 信息生成时间
                    Title=Title,  # 系统消息标题
                    Message=Message,  # 系统消息正文
                    ReadingState='未读',  # 信息阅读状态
                )
                sendEmail(SampleAuditor, Title, Message)  # 发送邮件通知

                if department == '管理员':
                    temp_not_audited = models.clinicalSampleInfo.objects.filter(sample_review=0)  # 研发样本未审核信息
                    temp_draft = models.clinicalSampleInfo.objects.filter(sample_review='')  # 研发样本草稿信息
                    temp_return = models.clinicalSampleInfo.objects.filter(sample_review=4)  # 研发审核退回样本信息
                    temp_audited = models.clinicalSampleInfo.objects.filter(
                        sample_review__in=[1, 2, 3])  # 研发样本已审核信息
                else:
                    temp_not_audited = models.clinicalSampleInfo.objects.filter(username=username,
                                                                                sample_review=0)  # 研发样本未审核信息
                    temp_draft = models.clinicalSampleInfo.objects.filter(username=username,
                                                                          sample_review='')  # 研发样本草稿信息
                    temp_return = models.clinicalSampleInfo.objects.filter(username=username,
                                                                           sample_review=4)  # 研发审核退回样本信息
                    temp_audited = models.clinicalSampleInfo.objects.filter(username=username,
                                                                            sample_review__in=[1, 2, 3])  # 研发样本已审核信息
                return render(request, "modelspage/sample_entry.html",
                              {"userinfo": temp, "not_audited": temp_not_audited, "audited": temp_audited,
                               "draft": temp_draft,
                               "return": temp_return, "myInfo": temp_myInfo,
                               "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})
            else:
                # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
                temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                    ReadingState='未读')  # 用户信息
                num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
                temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
                return render(request, "modelspage/PermissionsPrompt.html",
                              {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'returnData':
            user = User.objects.get(username=username)
            temp_userlist = User.objects.filter(first_name='市场部', is_active=user.is_active)
            temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                username=username)  # 用户操作权限信息
            if temp_UserOperationPermissionsInfo.ClinicalSampleRegistration == '1':
                return render(request, "modelspage/sample_ReturnData.html",
                              {"userinfo": temp, "data": temp_data, "myInfo": temp_myInfo, "userlist": temp_userlist,
                               "SystemMessage": temp_SystemMessage_Unread, "TissueSampleSign": TissueSampleSign,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})
            else:
                # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
                temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                    ReadingState='未读')  # 用户信息
                num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
                temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
                return render(request, "modelspage/PermissionsPrompt.html",
                              {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 用户访问权限设置操作首页
def UserAccessRightsSetting(request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户系统信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        return render(request, "modelspage/UserAccessRightsSetting_usernameInput.html",
                      {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 用户访问权限设置操作页
def UserAccessRightsSetting_usernameInput(request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户系统信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)

        # 用户信息
        Inputusername = request.POST.get("username")  # 用户名
        Inputdepartment = request.POST.get("department")  # 部门
        DefaultMark = request.POST.get("DefaultMark") # 模式标记

        if DefaultMark == "系统默认":
            temp_mysql = models.UserInfo.objects.filter(username=Inputusername)  # 用户信息
            if len(temp_mysql) == 0:
                addUserAccessRights(Inputusername, Inputdepartment)
            else:
                models.UserInfo.objects.filter(username=Inputusername).update(DefaultMark=0)
                return render(request, "modelspage/UserAccessRightsSetting_usernameInput.html",
                              {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})
        else:
            temp_InputInfo = {"Inputusername": Inputusername, "DefaultMark": DefaultMark, "Inputdepartment": Inputdepartment}
            temp_mysql = models.UserInfo.objects.filter(username=Inputusername)  # 用户信息
            if len(temp_mysql) == 0:
                addUserAccessRights(Inputusername, Inputdepartment)
                models.UserInfo.objects.filter(username=Inputusername).update(DefaultMark=1)
                temp_userinfo = models.UserInfo.objects.filter(username=Inputusername)  # 用户信息
                return render(request, "modelspage/UserAccessRightsSetting.html",
                              {"userinfo": temp, "myInfo": temp_myInfo, "InputInfo": temp_InputInfo,
                               "settingUserinfo": temp_userinfo, "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})
            else:
                return render(request, "modelspage/UserAccessRightsSetting.html",
                              {"userinfo": temp, "myInfo": temp_myInfo, "InputInfo": temp_InputInfo,
                               "settingUserinfo": temp_mysql, "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 用户访问权限设置结果录入
def UserAccessRightsSettingToDataBases(request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户系统信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)

        # 用户信息
        Inputusername = request.POST.get("username")  # 用户名
        # DefaultMark = int(request.POST.get("DefaultMark"))  # 模式标记
        # 样本管理模块
        ClinicalSampleRegistration = int(request.POST.get("ClinicalSampleRegistration"))  # 样本登记（临检）
        sampleReview = int(request.POST.get("sampleReview"))  # 收样审核（临检）
        clinicalExperimentalTaskAssignment = int(request.POST.get("clinicalExperimentalTaskAssignment"))  # 任务分派（临检）
        PretreatmentTaskReview = int(request.POST.get("PretreatmentTaskReview"))  # 样本预处理（临检）
        DNAExtractTaskReview = int(request.POST.get("DNAExtractTaskReview")) # DNA提取（临检）
        PreLibConTaskReview = int(request.POST.get("PreLibConTaskReview"))  # 预文库构建（临检）
        FinLibConTaskReview = int(request.POST.get("FinLibConTaskReview"))  # 终文库构建（临检）
        ComSeqTaskReview = int(request.POST.get("ComSeqTaskReview"))  # 上机测序（临检）
        # 项目管理模块
        RandDSampleInfoInputHomePage = int(request.POST.get("RandDSampleInfoInputHomePage"))  # 收样登记（研发）
        RandDSampleReviewHomePage = int(request.POST.get("RandDSampleReviewHomePage"))  # 收样审核（研发）
        RandDExperimentalTaskAssignmentHomePage = int(request.POST.get("RandDExperimentalTaskAssignmentHomePage"))  # 任务分派（研发）
        RandDPretreatmentInfoInputHomePage = int(request.POST.get("RandDPretreatmentInfoInputHomePage"))  # 样本预处理（研发）
        RandDDNAExtractInfoInputHomePage = int(request.POST.get("RandDDNAExtractInfoInputHomePage"))  # DNA提取（研发）
        RandDPreLibConInfoInputHomePage = int(request.POST.get("RandDPreLibConInfoInputHomePage"))  # 预文库构建（研发）
        RandDFinLibConInfoInputHomePage = int(request.POST.get("RandDFinLibConInfoInputHomePage"))  # 终文库构建（研发）
        RandDComSeqInfoInputHomePage = int(request.POST.get("RandDComSeqInfoInputHomePage"))  # 上机测序（研发）
        # 合同管理模块
        contractManagement = int(request.POST.get("contractReview"))  # 合同管理
        contractReview = int(request.POST.get("contractReview"))  # 合同审核
        # 生信分析模块
        BioinfoTaskAssignment = int(request.POST.get("BioinfoTaskAssignment"))  # 分析任务分派
        BioinfoDataAnalysisTaskReview = int(request.POST.get("BioinfoDataAnalysisTaskReview"))  # 数据分析结果
        BioinfoDataAnalysisResultReview = int(request.POST.get("BioinfoDataAnalysisResultReview"))  # 分析结果审核
        BioinfoReportTaskReview = int(request.POST.get("BioinfoReportTaskReview"))  # 报告生成
        # 报告管理模块
        BioinfoReportMedicalAuditTaskReview = int(request.POST.get("BioinfoReportMedicalAuditTaskReview"))  # 遗传咨询师审核报告
        BioinfoReportOperateAuditTaskReview = int(request.POST.get("BioinfoReportOperateAuditTaskReview"))  # 运营审核报告
        # 商务管理模块
        BusinessAffairsManagement = int(request.POST.get("BioinfoReportSendInfoTaskReview"))  # 商务管理
        BioinfoReportSendInfoTaskReview = int(request.POST.get("BioinfoReportSendInfoTaskReview"))  # 报告发送

        SampleManagement = 0  # 样本管理
        projectManagement = 0  # 项目管理
        BioinfoAnalysis = 0  # 生信分析
        ReportManagement = 0  # 报告管理

        ArrSampleManagement = ClinicalSampleRegistration + sampleReview + clinicalExperimentalTaskAssignment + \
                              PretreatmentTaskReview + DNAExtractTaskReview + PreLibConTaskReview + \
                              FinLibConTaskReview + ComSeqTaskReview
        if not ArrSampleManagement == 0:
            SampleManagement = 1

        ArrprojectManagement = RandDSampleInfoInputHomePage + RandDSampleReviewHomePage + RandDExperimentalTaskAssignmentHomePage + \
                               RandDPretreatmentInfoInputHomePage + RandDDNAExtractInfoInputHomePage + RandDPreLibConInfoInputHomePage + \
                               RandDFinLibConInfoInputHomePage + RandDComSeqInfoInputHomePage
        if not ArrprojectManagement == 0:
            projectManagement = 1

        ArrBioinfoAnalysis = BioinfoTaskAssignment + BioinfoDataAnalysisTaskReview + \
                             BioinfoDataAnalysisResultReview + BioinfoReportTaskReview
        if not ArrBioinfoAnalysis == 0:
            BioinfoAnalysis = 1

        ArrReportManagement = BioinfoReportMedicalAuditTaskReview + BioinfoReportOperateAuditTaskReview
        if not ArrReportManagement == 0:
            ReportManagement = 1

        models.UserInfo.objects.filter(username=Inputusername).update(DefaultMark=1,
                                                                 SampleManagement=SampleManagement,
                                                                 ClinicalSampleRegistration=ClinicalSampleRegistration,
                                                                 sampleReview=sampleReview,
                                                                 clinicalExperimentalTaskAssignment=clinicalExperimentalTaskAssignment,
                                                                 PretreatmentTaskReview=PretreatmentTaskReview,
                                                                 DNAExtractTaskReview=DNAExtractTaskReview,
                                                                 PreLibConTaskReview=PreLibConTaskReview,
                                                                 FinLibConTaskReview=FinLibConTaskReview,
                                                                 ComSeqTaskReview=ComSeqTaskReview,
                                                                 projectManagement=projectManagement,
                                                                 RandDSampleInfoInputHomePage=RandDSampleInfoInputHomePage,
                                                                 RandDSampleReviewHomePage=RandDSampleReviewHomePage,
                                                                 RandDExperimentalTaskAssignmentHomePage=RandDExperimentalTaskAssignmentHomePage,
                                                                 RandDPretreatmentInfoInputHomePage=RandDPretreatmentInfoInputHomePage,
                                                                 RandDDNAExtractInfoInputHomePage=RandDDNAExtractInfoInputHomePage,
                                                                 RandDPreLibConInfoInputHomePage=RandDPreLibConInfoInputHomePage,
                                                                 RandDFinLibConInfoInputHomePage=RandDFinLibConInfoInputHomePage,
                                                                 RandDComSeqInfoInputHomePage=RandDComSeqInfoInputHomePage,
                                                                 contractManagement=contractManagement,
                                                                 contractReview=contractReview,
                                                                 BioinfoAnalysis=BioinfoAnalysis,
                                                                 BioinfoTaskAssignment=BioinfoTaskAssignment,
                                                                 BioinfoDataAnalysisTaskReview=BioinfoDataAnalysisTaskReview,
                                                                 BioinfoDataAnalysisResultReview=BioinfoDataAnalysisResultReview,
                                                                 BioinfoReportTaskReview=BioinfoReportTaskReview,
                                                                 ReportManagement=ReportManagement,
                                                                 BioinfoReportMedicalAuditTaskReview=BioinfoReportMedicalAuditTaskReview,
                                                                 BioinfoReportOperateAuditTaskReview=BioinfoReportOperateAuditTaskReview,
                                                                 BusinessAffairsManagement=BusinessAffairsManagement,
                                                                 BioinfoReportSendInfoTaskReview=BioinfoReportSendInfoTaskReview)

        return render(request, "modelspage/UserAccessRightsSetting_usernameInput.html",
                      {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 用户操作权限设置操作首页
def UserOperationPermissionsSetting(request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户系统信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        return render(request, "modelspage/UserOperationPermissionsSetting_usernameInput.html",
                      {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 用户操作权限设置操作页
def UserOperationPermissionsSetting_usernameInput(request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户系统信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)

        # 用户信息
        Inputusername = request.POST.get("username")  # 用户名
        Inputdepartment = request.POST.get("department")  # 部门

        temp_InputInfo = {"Inputusername": Inputusername, "Inputdepartment": Inputdepartment}
        temp_mysql = models.UserOperationPermissionsInfo.objects.filter(username=Inputusername)  # 用户信息
        if len(temp_mysql) == 0:
            addUserAccessRights(Inputusername, Inputdepartment)
            models.UserOperationPermissionsInfo.objects.filter(username=Inputusername).update(DefaultMark=1)
            temp_userinfo = models.UserOperationPermissionsInfo.objects.filter(username=Inputusername)  # 用户信息
            return render(request, "modelspage/UserOperationPermissionsSetting.html",
                          {"userinfo": temp, "myInfo": temp_myInfo, "InputInfo": temp_InputInfo,
                           "settingUserinfo": temp_userinfo, "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        else:
            return render(request, "modelspage/UserOperationPermissionsSetting.html",
                          {"userinfo": temp, "myInfo": temp_myInfo, "InputInfo": temp_InputInfo,
                           "settingUserinfo": temp_mysql, "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 用户操作权限设置结果录入
def UserOperationPermissionsSettingToDataBases(request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户系统信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)

        # 用户信息
        Inputusername = request.POST.get("username")  # 用户名
        # 样本管理模块
        ClinicalSampleRegistration = int(request.POST.get("ClinicalSampleRegistration"))  # 样本登记（临检）
        sampleReview = int(request.POST.get("sampleReview"))  # 收样审核（临检）
        clinicalExperimentalTaskAssignment = int(request.POST.get("clinicalExperimentalTaskAssignment"))  # 任务分派（临检）
        PretreatmentTaskReview = int(request.POST.get("PretreatmentTaskReview"))  # 样本预处理（临检）
        DNAExtractTaskReview = int(request.POST.get("DNAExtractTaskReview")) # DNA提取（临检）
        PreLibConTaskReview = int(request.POST.get("PreLibConTaskReview"))  # 预文库构建（临检）
        FinLibConTaskReview = int(request.POST.get("FinLibConTaskReview"))  # 终文库构建（临检）
        ComSeqTaskReview = int(request.POST.get("ComSeqTaskReview"))  # 上机测序（临检）
        # 项目管理模块
        RandDSampleInfoInputHomePage = int(request.POST.get("RandDSampleInfoInputHomePage"))  # 收样登记（研发）
        RandDSampleReviewHomePage = int(request.POST.get("RandDSampleReviewHomePage"))  # 收样审核（研发）
        RandDExperimentalTaskAssignmentHomePage = int(request.POST.get("RandDExperimentalTaskAssignmentHomePage"))  # 任务分派（研发）
        RandDPretreatmentInfoInputHomePage = int(request.POST.get("RandDPretreatmentInfoInputHomePage"))  # 样本预处理（研发）
        RandDDNAExtractInfoInputHomePage = int(request.POST.get("RandDDNAExtractInfoInputHomePage"))  # DNA提取（研发）
        RandDPreLibConInfoInputHomePage = int(request.POST.get("RandDPreLibConInfoInputHomePage"))  # 预文库构建（研发）
        RandDFinLibConInfoInputHomePage = int(request.POST.get("RandDFinLibConInfoInputHomePage"))  # 终文库构建（研发）
        RandDComSeqInfoInputHomePage = int(request.POST.get("RandDComSeqInfoInputHomePage"))  # 上机测序（研发）
        # 合同管理模块
        contractReview = int(request.POST.get("contractReview"))  # 合同审核
        # 生信分析模块
        BioinfoTaskAssignment = int(request.POST.get("BioinfoTaskAssignment"))  # 分析任务分派
        BioinfoDataAnalysisTaskReview = int(request.POST.get("BioinfoDataAnalysisTaskReview"))  # 数据分析结果
        BioinfoDataAnalysisResultReview = int(request.POST.get("BioinfoDataAnalysisResultReview"))  # 分析结果审核
        BioinfoReportTaskReview = int(request.POST.get("BioinfoReportTaskReview"))  # 报告生成
        # 报告管理模块
        BioinfoReportMedicalAuditTaskReview = int(request.POST.get("BioinfoReportMedicalAuditTaskReview"))  # 遗传咨询师审核报告
        BioinfoReportOperateAuditTaskReview = int(request.POST.get("BioinfoReportOperateAuditTaskReview"))  # 运营审核报告
        # 商务管理模块
        BioinfoReportSendInfoTaskReview = int(request.POST.get("BioinfoReportSendInfoTaskReview"))  # 报告发送

        models.UserOperationPermissionsInfo.objects.filter(username=Inputusername).update(ClinicalSampleRegistration=ClinicalSampleRegistration,
                                                                 sampleReview=sampleReview,
                                                                 clinicalExperimentalTaskAssignment=clinicalExperimentalTaskAssignment,
                                                                 PretreatmentTaskReview=PretreatmentTaskReview,
                                                                 DNAExtractTaskReview=DNAExtractTaskReview,
                                                                 PreLibConTaskReview=PreLibConTaskReview,
                                                                 FinLibConTaskReview=FinLibConTaskReview,
                                                                 ComSeqTaskReview=ComSeqTaskReview,
                                                                 RandDSampleInfoInputHomePage=RandDSampleInfoInputHomePage,
                                                                 RandDSampleReviewHomePage=RandDSampleReviewHomePage,
                                                                 RandDExperimentalTaskAssignmentHomePage=RandDExperimentalTaskAssignmentHomePage,
                                                                 RandDPretreatmentInfoInputHomePage=RandDPretreatmentInfoInputHomePage,
                                                                 RandDDNAExtractInfoInputHomePage=RandDDNAExtractInfoInputHomePage,
                                                                 RandDPreLibConInfoInputHomePage=RandDPreLibConInfoInputHomePage,
                                                                 RandDFinLibConInfoInputHomePage=RandDFinLibConInfoInputHomePage,
                                                                 RandDComSeqInfoInputHomePage=RandDComSeqInfoInputHomePage,
                                                                 contractReview=contractReview,
                                                                 BioinfoTaskAssignment=BioinfoTaskAssignment,
                                                                 BioinfoDataAnalysisTaskReview=BioinfoDataAnalysisTaskReview,
                                                                 BioinfoDataAnalysisResultReview=BioinfoDataAnalysisResultReview,
                                                                 BioinfoReportTaskReview=BioinfoReportTaskReview,
                                                                 BioinfoReportMedicalAuditTaskReview=BioinfoReportMedicalAuditTaskReview,
                                                                 BioinfoReportOperateAuditTaskReview=BioinfoReportOperateAuditTaskReview,
                                                                 BioinfoReportSendInfoTaskReview=BioinfoReportSendInfoTaskReview)

        return render(request, "modelspage/UserOperationPermissionsSetting_usernameInput.html",
                      {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 发送邮件
def sendEmail(username, Title, Message):
    # 发送邮件提醒
    try:
        user = User.objects.get(username=username)
        # print '邮箱：', user.email
        send_mail(
            subject=Title, message=Message,
            from_email='anchordxlims@anchordx.com', recipient_list=[user.email],
            fail_silently=False,
        )
    except SMTPException, e:
        # 此处记录日志
        # 返回相关错误信息，例如：return HttpResponse(error)
        print '邮件发送失败: ', e

# def sendEmail(username, Title, Message):
#     # 发送邮件提醒
#     try:
#         usernameEmail = 'hpc_server@anchordx.com'
#         passwordEmail = 'AD20151212abc'
#         smtp_serverEmail = 'smtp.exmail.qq.com'
#
#         user = User.objects.get(username=username)
#
#         msg = MIMEMultipart('mixed')
#         msg['Subject'] = Title
#         text = Message
#         # content = MIMEText(text, 'plain')
#         # msg.attach(content)
#
#         # 输入收件人地址:
#         msg['From'] = usernameEmail
#         msg['To'] = user.email
#         server = smtplib.SMTP_SSL(smtp_serverEmail, 465)  # SSL
#         # server.set_debuglevel(1)
#         server.login(usernameEmail, passwordEmail)
#         server.sendmail(usernameEmail, user.email, text)
#         server.quit()
#     except SMTPException, e:
#         # 此处记录日志, 返回相关错误信息，例如：return HttpResponse(error)
#         print '邮件发送失败: ', e

# 用户系统信息列表首页
def UserSystemMessageHomePage(request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户系统信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)

        return render(request, "modelspage/UserSystemMessageHomePage.html",
                      {"userinfo": temp, "myInfo": temp_myInfo, "AllSystemMessage": temp_SystemMessage,
                       "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 用户系统信息详细信息展示页
def UserSystemMessagedetailedInfo(request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        # 用户信息
        Sender = ''  # 发送者
        # 信息内容
        Time = ''  # 信息生成时间
        Title = ''  # 系统消息标题
        button_name = ''  # 按钮名字
        if request.method == "POST":
            # 用户信息
            Sender = request.POST.get('Sender')  # 发送者r
            # 信息内容
            Time = request.POST.get('Time')  # 信息生成时间
            Title = request.POST.get('Title')  # 系统消息标题

            # 判断哪个按钮提交的数据
            if request.POST.has_key('delete'):
                button_name = 'delete'
            elif request.POST.has_key('Read'):
                button_name = 'Read'

        if button_name == 'delete':
            models.UserSystemMessage.objects.filter(Sender=Sender, Time=Time, Title=Title).delete()

            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户系统信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)

            return render(request, "modelspage/UserSystemMessageHomePage.html",
                          {"userinfo": temp, "myInfo": temp_myInfo,  "AllSystemMessage": temp_SystemMessage,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'Read':
            models.UserSystemMessage.objects.filter(Sender=Sender, Time=Time, Title=Title).update(ReadingState='已读')

            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户系统信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)

            return render(request, "modelspage/UserSystemMessageHomePage.html",
                          {"userinfo": temp, "myInfo": temp_myInfo,  "AllSystemMessage": temp_SystemMessage,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})

        detailedInfo = models.UserSystemMessage.objects.filter(Sender=Sender, Time=Time, Title=Title)  # 用户系统信息

        # 更新状态
        models.UserSystemMessage.objects.filter(Sender=Sender, Time=Time, Title=Title).update(ReadingState='已读')

        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户系统信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)

        return render(request, "modelspage/UserSystemMessagedetailedInfo.html",
                      {"userinfo": temp, "myInfo": temp_myInfo,  "detailedInfo": detailedInfo,
                       "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 用户系统信息处理
def UserSystemMessageProcessing(request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        button_name = ''  # 按钮名字
        # 判断哪个按钮提交的数据
        if request.POST.has_key('back'):
            button_name = 'back'
        elif request.POST.has_key('delete'):
            button_name = 'delete'

        if button_name == 'delete':
            # 用户信息
            Sender = ''  # 发送者
            # 信息内容
            Time = ''  # 信息生成时间
            Title = ''  # 系统消息标题
            if request.method == "POST":
                # 用户信息
                Sender = request.POST.get('Sender')  # 发送者
                # 信息内容
                Time = request.POST.get('Time')  # 信息生成时间
                Title = request.POST.get('Title')  # 系统消息标题
            models.UserSystemMessage.objects.filter(Sender=Sender, Time=Time, Title=Title).delete()

        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户系统信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)

        return render(request, "modelspage/UserSystemMessageHomePage.html",
                      {"userinfo": temp, "myInfo": temp_myInfo,  "AllSystemMessage": temp_SystemMessage,
                       "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})


