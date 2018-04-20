# encoding: utf-8

from django.shortcuts import render
from AnchorDxLimsApp import models
import time,httplib,datetime
from AnchorDxLimsApp.views import sendEmail
import copy
import string
# Create your views here.
#coding:utf-8

from django.shortcuts import render,HttpResponse

# 临床样本合同审核首页
def contract_Review(request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        # 从数据里取出所有数据
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_not_audited = models.clinicalSampleInfo.objects.filter(contract_review=0)  # 临床样本未审核信息
        temp_pass = models.clinicalSampleInfo.objects.filter(contract_review=1)  # 临床样本已通过审核信息
        temp_not_pass = models.clinicalSampleInfo.objects.filter(contract_review=2)  # 临床样本不通过审核信息
        return render(request, "modelspage/contract_review.html",
                      {"userinfo": temp, "data": temp_not_audited, "pass": temp_pass, "Not_pass": temp_not_pass,
                       "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 合同信息审核页
def contract_To_Examine (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        sam_code_num = ''
        if request.method == "POST":
            print '患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号: ', sam_code_num

        # 从数据里取出某条记录
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_mysql = models.clinicalSampleInfo.objects.get(sam_code_num=sam_code_num)

        return render(request, "modelspage/contract_reg_review_submit.html",
                      {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 合同信息审核操作
def contract_Examine_Operation (request):
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
        if temp_UserOperationPermissionsInfo.contractReview == '1':
            button_name = ''  # 按钮名字
            sam_code_num = ''
            ExperimentNumber = ''  # 实验编号
            # 合同审核信息
            Receivables = ''  # 收款金额
            ReceivablesDate = ''  # 收款时间
            contract_Time = ''  # 财务审核时间
            ExperimentTimes = ''  # 实验次数
            contractReviewReason = ''  # 财务审核备注
            if request.method == "POST":
                print '患者信息: ============================================= '
                # 样本条码号
                sam_code_num = request.POST.get('sam_code_num').strip('HT')
                print '样本条码号: ', sam_code_num

                # 实验编号
                ExperimentNumber = request.POST.get('ExperimentNumber')
                print '实验编号: ', ExperimentNumber

                # 收款金额
                Receivables = request.POST.get('Receivables')
                print '收款金额: ', Receivables

                # 收款时间
                ReceivablesDate = request.POST.get('ReceivablesDate')
                print '收款时间: ', ReceivablesDate

                # 财务审核时间
                contract_Time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print '财务审核时间: ', contract_Time

                # 财务审核备注
                contractReviewReason = request.POST.get('contractReviewReason')
                print '财务审核备注: ', contractReviewReason

                # 判断哪个按钮提交的数据
                if request.POST.has_key('pass'):
                    button_name = 'pass'
                elif request.POST.has_key('Not_pass'):
                    button_name = 'Not_pass'
                elif request.POST.has_key('submitModify'):
                    button_name = 'submitModify'

            if button_name == 'pass':
                # 通过审核
                models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num).update(contract_review='1')
                # 修改数据库合同信息状态
                temp_contractReview = models.contractReviewInfo.objects.filter(sam_code_num=sam_code_num)  # DNA提取样本信息
                num = len(temp_contractReview)
                # 添加数据到数据库
                models.contractReviewInfo.objects.create(
                    # 用户信息
                    username=username,  # 用户名
                    department=department,  # 部门
                    # 样本信息
                    sam_code_num=sam_code_num,  # 样本条码号
                    ExperimentNumber=ExperimentNumber,  # 实验编号
                    # 合同审核信息
                    Receivables=Receivables,  # 收款金额
                    ReceivablesDate=ReceivablesDate,  # 收款时间
                    contract_Time=contract_Time,  # 财务审核时间
                    contractReviewReason=contractReviewReason,  # 财务审核备注
                    # 其他信息
                    ExperimentTimes=num + 1  # 财务审核次数
                )
                models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num).update(contract_Times=num + 1)
            elif button_name == 'Not_pass':
                # 修改数据库合同信息状态
                temp_contractReview = models.contractReviewInfo.objects.filter(sam_code_num=sam_code_num)  # DNA提取样本信息
                num = len(temp_contractReview)
                # 添加数据到数据库
                models.contractReviewInfo.objects.create(
                    # 用户信息
                    username=username,  # 用户名
                    department=department,  # 部门
                    # 样本信息
                    sam_code_num=sam_code_num,  # 样本条码号
                    ExperimentNumber=ExperimentNumber,  # 实验编号
                    # 合同审核信息
                    Receivables=Receivables,  # 收款金额
                    ReceivablesDate=ReceivablesDate,  # 收款时间
                    contract_Time=contract_Time,  # 财务审核时间
                    contractReviewReason=contractReviewReason,  # 财务审核备注
                    # 其他信息
                    ExperimentTimes=num + 1  # 财务审核次数
                )
                models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num).update(contract_Times=num + 1)
                # 不通过审核
                models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num).update(contract_review='2')
                sample = models.clinicalSampleInfo.objects.get(sam_code_num=sam_code_num)
                user = sample.SampleAuditor
                # 添加系统消息
                Title = '通知：临检样本合同审核不通过'  # 系统消息标题
                Message = username + '已经对样本编号为：‘' + sam_code_num + '’的样本合同审核完成，审核结果为不通过！'  # 系统邮件正文
                models.UserSystemMessage.objects.create(
                    # 用户信息
                    Sender=username,  # 发送者
                    Receiver=user,  # 接收者
                    # 信息内容
                    Time=contract_Time,  # 信息生成时间
                    Title=Title,  # 系统消息标题
                    Message=Message,  # 系统消息正文
                    ReadingState='未读',  # 信息阅读状态
                )
                sendEmail(user, Title, Message)  # 发送邮件通知
            elif button_name == 'submitModify':
                # 实验次数
                contract_Times = request.POST.get('contract_Times')
                print '实验次数111submitModify: ', contract_Times
                # 添加数据到数据库
                models.contractReviewInfo.objects.filter(sam_code_num=sam_code_num,
                                                         ExperimentTimes=contract_Times,).update(
                    # 合同审核信息
                    Receivables=Receivables,  # 收款金额
                    ReceivablesDate=ReceivablesDate,  # 收款时间
                    contract_Time=contract_Time,  # 财务审核时间
                    contractReviewReason=contractReviewReason,  # 财务审核备注
                )

            # 从数据里取出所有数据
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            temp_not_audited = models.clinicalSampleInfo.objects.filter(contract_review=0)  # 临床样本未审核信息
            temp_pass = models.clinicalSampleInfo.objects.filter(contract_review=1)  # 临床样本已通过审核信息
            temp_not_pass = models.clinicalSampleInfo.objects.filter(contract_review=2)  # 临床样本不通过审核信息

            return render(request, "modelspage/contract_review.html",
                          {"userinfo": temp, "data": temp_not_audited, "pass": temp_pass, "Not_pass": temp_not_pass,
                           "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
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

# 合同信息已通过审核信息详情页
def contract_To_Examine_Pass (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        sam_code_num = ''
        contract_Times = ''  # 实验次数
        button_name = ''
        if request.method == "POST":
            print 'Pass患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num').strip('HT')
            print 'Pass样本条码号: ', sam_code_num

            # 实验次数
            contract_Times = request.POST.get('contract_Times')
            print '实验次数: ', contract_Times

            # 判断哪个按钮提交的数据
            if request.POST.has_key('seeInfo'):
                button_name = 'seeInfo'
            elif request.POST.has_key('ModifyData'):
                button_name = 'ModifyData'

        # 从数据里取出某条记录
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_mysql = models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num)
        temp_contractReviewInfo = models.contractReviewInfo.objects.filter(sam_code_num=sam_code_num,
                                                                           ExperimentTimes=contract_Times)  # 临床样本未审核信息

        if button_name == 'seeInfo':
            return render(request, "modelspage/contract_Review_Result.html",
                          {"data": temp_mysql, "temp_contractReviewInfo": temp_contractReviewInfo, "userinfo": temp,
                           "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'ModifyData':
            return render(request, "modelspage/contract_reg_review_ModifyData.html",
                          {"data": temp_mysql, "temp_contractReviewInfo": temp_contractReviewInfo, "userinfo": temp,
                           "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 合同信息不通过审核信息详情页
def contract_To_Examine_Not_Pass (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        sam_code_num = ''
        contract_Times = ''  # 实验次数
        if request.method == "POST":
            print 'Pass患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num').strip('HT')
            print 'Pass样本条码号: ', sam_code_num

            # 实验次数
            contract_Times = request.POST.get('contract_Times')
            print '实验次数: ', contract_Times

        # 从数据里取出某条记录
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_mysql = models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num)
        temp_contractReviewInfo = models.contractReviewInfo.objects.filter(sam_code_num=sam_code_num,
                                                                           ExperimentTimes=contract_Times)  # 临床样本未审核信息
        return render(request, "modelspage/contract_Review_ResultInfo.html",
                      {"data": temp_mysql, "temp_contractReviewInfo": temp_contractReviewInfo, "userinfo": temp,
                       "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 合同信息再次审核操作
def contract_reviewing_Operation (request):
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
        if temp_UserOperationPermissionsInfo.contractReview == '1':
            sam_code_num = ''
            if request.method == "POST":
                print '患者信息: ============================================= '
                # 样本条码号
                sam_code_num = request.POST.get('sam_code_num').strip('HT')
                print '样本条码号: ', sam_code_num

            # 修改数据库合同信息状态
            models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num).update(contract_review='0')

            # 从数据里取出所有数据
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            temp_not_audited = models.clinicalSampleInfo.objects.filter(contract_review=0)  # 临床样本未审核信息
            temp_pass = models.clinicalSampleInfo.objects.filter(contract_review=1)  # 临床样本已通过审核信息
            temp_not_pass = models.clinicalSampleInfo.objects.filter(contract_review=2)  # 临床样本不通过审核信息

            return render(request, "modelspage/contract_review.html",
                          {"userinfo": temp, "data": temp_not_audited, "pass": temp_pass, "Not_pass": temp_not_pass,
                           "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
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

