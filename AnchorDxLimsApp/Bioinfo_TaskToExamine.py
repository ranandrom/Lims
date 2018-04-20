# encoding: utf-8

from django.shortcuts import render
from AnchorDxLimsApp import models
from django.contrib.auth.models import User
from time import strftime,gmtime
from itertools import chain
import time,httplib,datetime
from AnchorDxLimsApp.views import sendEmail
# Create your views here.
#coding:utf-8

from django.shortcuts import render,HttpResponse

# 临床样本生信分析任务未分配列表
def Bioinfo_Task_Assignment (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        # 从数据里取出某条记录
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        # 临检样本
        temp_Clin_not_audited = models.ComputerSeqInfo.objects.filter(Next_TaskProgress_Sign='0')  # 上机测序任务未分派
        temp_Clin_audited = models.ComputerSeqInfo.objects.filter(Next_TaskProgress_Sign='1')  # 上机测序任务已分派
        temp_Clin_Suspend = models.ComputerSeqInfo.objects.filter(Next_TaskProgress_Sign='2')  # 上机测序任务已分派
        temp_Clin_Stop = models.ComputerSeqInfo.objects.filter(Next_TaskProgress_Sign='3')  # 上机测序任务已分派
        # 研发样本
        temp_RandD_not_audited = models.RandDSampleComputerSeqInfo.objects.filter(Next_TaskProgress_Sign='0')  # 上机测序任务未分派
        temp_RandD_audited = models.RandDSampleComputerSeqInfo.objects.filter(Next_TaskProgress_Sign='1')  # 上机测序任务已分派
        temp_RandD_Suspend = models.RandDSampleComputerSeqInfo.objects.filter(Next_TaskProgress_Sign='2')  # 上机测序任务已分派
        temp_RandD_Stop = models.RandDSampleComputerSeqInfo.objects.filter(Next_TaskProgress_Sign='3')  # 上机测序任务已分派

        return render(request, "modelspage/BioinfoTaskAssignment.html",
                      {"userinfo": temp, "Clin_not_audited": temp_Clin_not_audited, "Clin_audited": temp_Clin_audited,
                       "Clin_Suspend": temp_Clin_Suspend, "Clin_Stop": temp_Clin_Stop,
                       "RandD_not_audited": temp_RandD_not_audited, "RandD_audited": temp_RandD_audited,
                       "RandD_Suspend": temp_RandD_Suspend, "RandD_Stop": temp_RandD_Stop,
                       "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 临床样本生信分析任务未分配详情页
def task_To_Examine (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        sam_code_num = ''
        Computer_Seq_num = ''
        button_name = ''
        if request.method == "POST":
            print '患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号: ', sam_code_num
            # 上机测序实验次数
            Computer_Seq_num = request.POST.get('Computer_Seq_num')
            print '上机测序实验次数: ', Computer_Seq_num

        # 从数据里取出某条记录
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_userlist = User.objects.filter(first_name='生信部')
        # 判断哪个按钮提交的数据
        if request.POST.has_key('ClinSample'):
            button_name = 'ClinSample'
        elif request.POST.has_key('RandDSample'):
            button_name = 'RandDSample'
        if button_name == 'ClinSample':
            temp_mysql = models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                               ExperimentTimes=Computer_Seq_num)

            return render(request, "modelspage/BioinfoTask_review_submit.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                           "SystemMessage": temp_SystemMessage_Unread, "num_SystemMessage_Unread": num_SystemMessage_Unread})
        else:
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_mysql = models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                               ExperimentTimes=Computer_Seq_num)

            return render(request, "modelspage/RandDSampleBioinfoTaskAssignment.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                           "SystemMessage": temp_SystemMessage_Unread, "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 临床样本生信分析任务分配操作
def task_Examine_Operation (request):
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
        if temp_UserOperationPermissionsInfo.BioinfoTaskAssignment == '1':
            button_name = ''  # 按钮名字
            sam_code_num = ''
            Computer_Seq_num = ''
            # 样本任务分配信息
            Next_TaskProgress_Man = ''  # 任务接收者
            DataPath = ''  # 数据下机路径
            Next_TaskProgress_Remarks = ''  # 任务备注
            Next_TaskProgress_Time = ''  # 任务分配时间
            log = 0  # 是否需要发送邮件通知的标记
            if request.method == "POST":
                print '患者信息: ============================================= '
                # 样本条码号
                sam_code_num = request.POST.get('sam_code_num').strip('HT')
                print '样本条码号: ', sam_code_num

                # 上机测序实验次数
                Computer_Seq_num = request.POST.get('Computer_Seq_num')
                print '上机测序实验次数: ', Computer_Seq_num

                # 任务接收者
                Next_TaskProgress_Man = request.POST.get('Next_TaskProgress_Man')
                print '任务接收者: ', Next_TaskProgress_Man

                # 任务备注
                Next_TaskProgress_Remarks = request.POST.get('Next_TaskProgress_Remarks')
                print '任务备注: ', Next_TaskProgress_Remarks

                # 数据下机路径
                DataPath = request.POST.get('DataPath')
                print '数据下机路径: ', DataPath

                # 任务分配时间
                Next_TaskProgress_Time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # taskTime = getBeijinTime()
                print '任务分配时间: ', Next_TaskProgress_Time

                # 判断哪个按钮提交的数据
                if request.POST.has_key('Determine'):
                    button_name = 'Determine'
                elif request.POST.has_key('RandDDetermine'):
                    button_name = 'RandDDetermine'
                elif request.POST.has_key('Return'):
                    button_name = 'Return'
                elif request.POST.has_key('RandDReturn'):
                    button_name = 'RandDReturn'
                elif request.POST.has_key('Suspend'):
                    button_name = 'Suspend'
                elif request.POST.has_key('RandDSuspend'):
                    button_name = 'RandDSuspend'
                elif request.POST.has_key('Stop'):
                    button_name = 'Stop'
                elif request.POST.has_key('RandDStop'):
                    button_name = 'RandDStop'
                elif request.POST.has_key('Clin_submitModify'):
                    log = 1
                    ReviewResult = request.POST.get('ReviewResult')
                    if ReviewResult == '通过':
                        button_name = 'Determine'
                    elif ReviewResult == '退回':
                        button_name = 'Return'
                    elif ReviewResult == '暂停':
                        button_name = 'Suspend'
                    elif ReviewResult == '终止':
                        button_name = 'Stop'
                elif request.POST.has_key('RandD_submitModify'):
                    log = 1
                    ReviewResult = request.POST.get('ReviewResult')
                    if ReviewResult == '通过':
                        button_name = 'RandDDetermine'
                    elif ReviewResult == '退回':
                        button_name = 'Return'
                    elif ReviewResult == '暂停':
                        button_name = 'RandDSuspend'
                    elif ReviewResult == '终止':
                        button_name = 'RandDStop'

            # 修改数据库合同信息状态
            if button_name == 'Determine':
                if log == 0:
                    # 添加系统消息
                    Title = '通知：生信分析任务'  # 系统消息标题
                    Message = username + '分派给你一个生信分析任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                    models.UserSystemMessage.objects.create(
                        # 用户信息
                        Sender=username,  # 发送者
                        Receiver=Next_TaskProgress_Man,  # 接收者
                        # 信息内容
                        Time=Next_TaskProgress_Time,  # 信息生成时间
                        Title=Title,  # 系统消息标题
                        Message=Message,  # 系统消息正文
                        ReadingState='未读',  # 信息阅读状态
                    )
                    sendEmail(Next_TaskProgress_Man, Title, Message)  # 发送邮件通知
                elif log == 1:
                    temp_data = models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                      ExperimentTimes=Computer_Seq_num)
                    if not temp_data[0].Next_TaskProgress_Man == Next_TaskProgress_Man and temp_data[0].Bioinfo_Sign == 0:
                        # 添加系统消息
                        Title = '通知：生信分析任务'  # 系统消息标题
                        Message = username + '分派给你一个生信分析任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                        models.UserSystemMessage.objects.create(
                            # 用户信息
                            Sender=username,  # 发送者
                            Receiver=Next_TaskProgress_Man,  # 接收者
                            # 信息内容
                            Time=Next_TaskProgress_Time,  # 信息生成时间
                            Title=Title,  # 系统消息标题
                            Message=Message,  # 系统消息正文
                            ReadingState='未读',  # 信息阅读状态
                        )
                        sendEmail(Next_TaskProgress_Man, Title, Message)  # 发送邮件通知

                # 任务已分配
                models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                      ExperimentTimes=Computer_Seq_num).update(
                    ReviewResult='通过',
                    Next_TaskProgress_Sign='1',
                    Next_TaskProgress_Man=Next_TaskProgress_Man,
                    DataPath=DataPath,
                    Next_TaskProgress_Time=Next_TaskProgress_Time,
                    Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                )
            elif button_name == 'RandDDetermine':
                if log == 0:
                    # 添加系统消息
                    Title = '通知：研发样本生信分析任务'  # 系统消息标题
                    Message = username + '分派给你一个研发样本生信分析任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                    models.UserSystemMessage.objects.create(
                        # 用户信息
                        Sender=username,  # 发送者
                        Receiver=Next_TaskProgress_Man,  # 接收者
                        # 信息内容
                        Time=Next_TaskProgress_Time,  # 信息生成时间
                        Title=Title,  # 系统消息标题
                        Message=Message,  # 系统消息正文
                        ReadingState='未读',  # 信息阅读状态
                    )
                    sendEmail(Next_TaskProgress_Man, Title, Message)  # 发送邮件通知
                elif log == 1:
                    temp_data = models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                                 ExperimentTimes=Computer_Seq_num)
                    if not temp_data[0].Next_TaskProgress_Man == Next_TaskProgress_Man and temp_data[0].Bioinfo_Sign == 0:
                        # 添加系统消息
                        Title = '通知：研发样本生信分析任务'  # 系统消息标题
                        Message = username + '分派给你一个研发样本生信分析任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                        models.UserSystemMessage.objects.create(
                            # 用户信息
                            Sender=username,  # 发送者
                            Receiver=Next_TaskProgress_Man,  # 接收者
                            # 信息内容
                            Time=Next_TaskProgress_Time,  # 信息生成时间
                            Title=Title,  # 系统消息标题
                            Message=Message,  # 系统消息正文
                            ReadingState='未读',  # 信息阅读状态
                        )
                        sendEmail(Next_TaskProgress_Man, Title, Message)  # 发送邮件通知

                models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                 ExperimentTimes=Computer_Seq_num).update(
                    ReviewResult='通过',
                    Next_TaskProgress_Sign='1',
                    Next_TaskProgress_Man=Next_TaskProgress_Man,
                    DataPath=DataPath,
                    Next_TaskProgress_Time=Next_TaskProgress_Time,
                    Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                )
            elif button_name == 'Return':
                temp_data = models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                  ExperimentTimes=Computer_Seq_num)
                if temp_data[0].Bioinfo_Sign == '0':
                    # 添加系统消息
                    Title = '通知：研发样本测序重测任务'  # 系统消息标题
                    Message = username + '退回给你一个研发样本测序重测任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                    models.UserSystemMessage.objects.create(
                        # 用户信息
                        Sender=username,  # 发送者
                        Receiver=temp_data[0].username,  # 接收者
                        # 信息内容
                        Time=Next_TaskProgress_Time,  # 信息生成时间
                        Title=Title,  # 系统消息标题
                        Message=Message,  # 系统消息正文
                        ReadingState='未读',  # 信息阅读状态
                    )
                    sendEmail(temp_data[0].username, Title, Message)  # 发送邮件通知
                    # 任务退回
                    models.FinLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                        ExperimentTimes=temp_data[0].Build_finlib_num).update(
                        ComputerSeq_Sign='0',
                        Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                        Next_TaskProgress_Time=Next_TaskProgress_Time,
                    )
                    # 任务已分配
                    models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                          ExperimentTimes=Computer_Seq_num).update(
                        ReviewResult='退回',
                        Next_TaskProgress_Sign='1',
                        Next_TaskProgress_Man=Next_TaskProgress_Man,
                        DataPath=DataPath,
                        Next_TaskProgress_Time=Next_TaskProgress_Time,
                        Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                    )
            elif button_name == 'RandDReturn':
                temp_data = models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                             ExperimentTimes=Computer_Seq_num)
                if temp_data[0].Bioinfo_Sign == '0':
                    # 添加系统消息
                    Title = '通知：研发样本测序重测任务'  # 系统消息标题
                    Message = username + '退回给你一个研发样本测序重测任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                    models.UserSystemMessage.objects.create(
                        # 用户信息
                        Sender=username,  # 发送者
                        Receiver=temp_data[0].username,  # 接收者
                        # 信息内容
                        Time=Next_TaskProgress_Time,  # 信息生成时间
                        Title=Title,  # 系统消息标题
                        Message=Message,  # 系统消息正文
                        ReadingState='未读',  # 信息阅读状态
                    )
                    sendEmail(temp_data[0].username, Title, Message)  # 发送邮件通知
                    # 任务退回
                    models.RandDSampleFinLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                   ExperimentTimes=temp_data[0].Build_finlib_num).update(
                        ComputerSeq_Sign='0',
                        Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                        Next_TaskProgress_Time=Next_TaskProgress_Time,
                    )
                    # 任务已分配
                    models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                     ExperimentTimes=Computer_Seq_num).update(
                        ReviewResult='退回',
                        Next_TaskProgress_Sign='1',
                        Next_TaskProgress_Man=Next_TaskProgress_Man,
                        DataPath=DataPath,
                        Next_TaskProgress_Time=Next_TaskProgress_Time,
                        Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                    )
            elif button_name == 'Suspend':
                temp_data = models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                  ExperimentTimes=Computer_Seq_num)
                if temp_data[0].Bioinfo_Sign == '0':
                    # 任务暂停
                    models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                          ExperimentTimes=Computer_Seq_num).update(
                        ReviewResult='暂停',
                        Next_TaskProgress_Sign='2',
                        Next_TaskProgress_Man=Next_TaskProgress_Man,
                        DataPath=DataPath,
                        Next_TaskProgress_Time=Next_TaskProgress_Time,
                        Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                    )
            elif button_name == 'RandDSuspend':
                temp_data = models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                             ExperimentTimes=Computer_Seq_num)
                if temp_data[0].Bioinfo_Sign == '0':
                    # 任务暂停
                    models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                     ExperimentTimes=Computer_Seq_num).update(
                        ReviewResult='暂停',
                        Next_TaskProgress_Sign='2',
                        Next_TaskProgress_Man=Next_TaskProgress_Man,
                        DataPath=DataPath,
                        Next_TaskProgress_Time=Next_TaskProgress_Time,
                        Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                    )
            elif button_name == 'Stop':
                temp_data = models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                  ExperimentTimes=Computer_Seq_num)
                if temp_data[0].Bioinfo_Sign == '0':
                    # 任务暂停
                    models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                          ExperimentTimes=Computer_Seq_num).update(
                        ReviewResult='终止',
                        Next_TaskProgress_Sign='3',
                        Next_TaskProgress_Man=Next_TaskProgress_Man,
                        DataPath=DataPath,
                        Next_TaskProgress_Time=Next_TaskProgress_Time,
                        Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                    )
            elif button_name == 'RandDStop':
                temp_data = models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                  ExperimentTimes=Computer_Seq_num)
                if temp_data[0].Bioinfo_Sign == '0':
                    # 任务终止
                    models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                     ExperimentTimes=Computer_Seq_num).update(
                        ReviewResult='终止',
                        Next_TaskProgress_Sign='3',
                        Next_TaskProgress_Man=Next_TaskProgress_Man,
                        DataPath=DataPath,
                        Next_TaskProgress_Time=Next_TaskProgress_Time,
                        Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                    )

            # 从数据里取出某条记录
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            # 临检样本
            temp_Clin_not_audited = models.ComputerSeqInfo.objects.filter(Next_TaskProgress_Sign='0')  # 上机测序任务未分派
            temp_Clin_audited = models.ComputerSeqInfo.objects.filter(Next_TaskProgress_Sign='1')  # 上机测序任务已分派
            temp_Clin_Suspend = models.ComputerSeqInfo.objects.filter(Next_TaskProgress_Sign='2')  # 上机测序任务已分派
            temp_Clin_Stop = models.ComputerSeqInfo.objects.filter(Next_TaskProgress_Sign='3')  # 上机测序任务已分派
            # 研发样本
            temp_RandD_not_audited = models.RandDSampleComputerSeqInfo.objects.filter(
                Next_TaskProgress_Sign='0')  # 上机测序任务未分派
            temp_RandD_audited = models.RandDSampleComputerSeqInfo.objects.filter(
                Next_TaskProgress_Sign='1')  # 上机测序任务已分派
            temp_RandD_Suspend = models.RandDSampleComputerSeqInfo.objects.filter(
                Next_TaskProgress_Sign='2')  # 上机测序任务已分派
            temp_RandD_Stop = models.RandDSampleComputerSeqInfo.objects.filter(Next_TaskProgress_Sign='3')  # 上机测序任务已分派

            return render(request, "modelspage/BioinfoTaskAssignment.html",
                          {"userinfo": temp, "Clin_not_audited": temp_Clin_not_audited,
                           "Clin_audited": temp_Clin_audited,
                           "Clin_Suspend": temp_Clin_Suspend, "Clin_Stop": temp_Clin_Stop,
                           "RandD_not_audited": temp_RandD_not_audited, "RandD_audited": temp_RandD_audited,
                           "RandD_Suspend": temp_RandD_Suspend, "RandD_Stop": temp_RandD_Stop,
                           "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        else:
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            return render(request, "modelspage/PermissionsPrompt.html", {"userinfo": temp, "myInfo": temp_myInfo,
                                                                         "SystemMessage": temp_SystemMessage_Unread,
                                                                         "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 样本生信分析任务已分配信息详情页
def task_To_Examine_Determine (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        sam_code_num = ''
        Computer_Seq_num = ''
        button_name = ''
        if request.method == "POST":
            print '患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号: ', sam_code_num
            # 上机测序实验次数
            Computer_Seq_num = request.POST.get('Computer_Seq_num')
            print '上机测序实验次数: ', Computer_Seq_num

        # 从数据里取出某条记录
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        # 判断哪个按钮提交的数据
        if request.POST.has_key('ClinSample'):
            button_name = 'ClinSample'
        elif request.POST.has_key('RandDSample'):
            button_name = 'RandDSample'
        elif request.POST.has_key('ClinicalSampleSuspend'):
            button_name = 'ClinicalSampleSuspend'
        elif request.POST.has_key('RandDSampleSuspend'):
            button_name = 'RandDSampleSuspend'
        elif request.POST.has_key('ClinicalSampleStop'):
            button_name = 'ClinicalSampleStop'
        elif request.POST.has_key('RandDSampleStop'):
            button_name = 'RandDSampleStop'
        elif request.POST.has_key('Clin_ModifyData'):
            button_name = 'Clin_ModifyData'
        elif request.POST.has_key('RandD_ModifyData'):
            button_name = 'RandD_ModifyData'

        if button_name == 'ClinSample':
            temp_mysql = models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                               ExperimentTimes=Computer_Seq_num)
            return render(request, "modelspage/Bioinfo_TaskToExamineDetermine.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'RandDSample':
            temp_mysql = models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                          ExperimentTimes=Computer_Seq_num)
            return render(request, "modelspage/RandDSampleBioinfoTaskDetails.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'ClinicalSampleSuspend':
            temp_mysql = models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                          ExperimentTimes=Computer_Seq_num)
            return render(request, "modelspage/Bioinfo_TaskToExamineSuspend.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'RandDSampleSuspend':
            temp_mysql = models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                          ExperimentTimes=Computer_Seq_num)
            return render(request, "modelspage/RandDSampleBioinfoTaskSuspend.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'ClinicalSampleStop':
            temp_mysql = models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                               ExperimentTimes=Computer_Seq_num)
            return render(request, "modelspage/Bioinfo_TaskToExamineStop.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'RandDSampleStop':
            temp_mysql = models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                          ExperimentTimes=Computer_Seq_num)
            return render(request, "modelspage/RandDSampleBioinfoTaskStop.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        if button_name == 'Clin_ModifyData':
            temp_mysql = models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                               ExperimentTimes=Computer_Seq_num)
            temp_userlist = User.objects.filter(first_name='生信部')
            return render(request, "modelspage/BioinfoTask_review_ModifyData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'RandD_ModifyData':
            temp_mysql = models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                          ExperimentTimes=Computer_Seq_num)
            temp_userlist = User.objects.filter(first_name='生信部')
            return render(request, "modelspage/RandDSampleBioinfoTaskAssModifyData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 已暂停的样本恢复操作
def recovery_Task_Operation (request):
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
        if temp_UserOperationPermissionsInfo.BioinfoTaskAssignment == '1':
            button_name = ''  # 按钮名字
            sam_code_num = ''
            Computer_Seq_num = ''
            if request.method == "POST":
                print '患者信息: ============================================= '
                # 样本条码号
                sam_code_num = request.POST.get('sam_code_num').strip('HT')
                print '样本条码号: ', sam_code_num

                # 上机测序实验次数
                Computer_Seq_num = request.POST.get('Computer_Seq_num')
                print '上机测序实验次数: ', Computer_Seq_num

                # 判断哪个按钮提交的数据
                if request.POST.has_key('ClinSample'):
                    button_name = 'ClinSample'
                elif request.POST.has_key('RandDSample'):
                    button_name = 'RandDSample'

            if button_name == 'ClinSample':
                # 任务已分配
                models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num, ExperimentTimes=Computer_Seq_num).update(
                    Next_TaskProgress_Sign='0')  # 任务分配标志
            elif button_name == 'RandDSample':
                # 任务暂停
                models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                 ExperimentTimes=Computer_Seq_num).update(
                    Next_TaskProgress_Sign='0')  # 任务分配标志

            # 从数据里取出某条记录
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            # 临检样本
            temp_Clin_not_audited = models.ComputerSeqInfo.objects.filter(Next_TaskProgress_Sign='0')  # 上机测序任务未分派
            temp_Clin_audited = models.ComputerSeqInfo.objects.filter(Next_TaskProgress_Sign='1')  # 上机测序任务已分派
            temp_Clin_Suspend = models.ComputerSeqInfo.objects.filter(Next_TaskProgress_Sign='2')  # 上机测序任务已分派
            temp_Clin_Stop = models.ComputerSeqInfo.objects.filter(Next_TaskProgress_Sign='3')  # 上机测序任务已分派
            # 研发样本
            temp_RandD_not_audited = models.RandDSampleComputerSeqInfo.objects.filter(
                Next_TaskProgress_Sign='0')  # 上机测序任务未分派
            temp_RandD_audited = models.RandDSampleComputerSeqInfo.objects.filter(
                Next_TaskProgress_Sign='1')  # 上机测序任务已分派
            temp_RandD_Suspend = models.RandDSampleComputerSeqInfo.objects.filter(
                Next_TaskProgress_Sign='2')  # 上机测序任务已分派
            temp_RandD_Stop = models.RandDSampleComputerSeqInfo.objects.filter(
                Next_TaskProgress_Sign='3')  # 上机测序任务已分派

            return render(request, "modelspage/BioinfoTaskAssignment.html",
                          {"userinfo": temp, "Clin_not_audited": temp_Clin_not_audited,
                           "Clin_audited": temp_Clin_audited,
                           "Clin_Suspend": temp_Clin_Suspend, "Clin_Stop": temp_Clin_Stop,
                           "RandD_not_audited": temp_RandD_not_audited, "RandD_audited": temp_RandD_audited,
                           "RandD_Suspend": temp_RandD_Suspend, "RandD_Stop": temp_RandD_Stop,
                           "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})

