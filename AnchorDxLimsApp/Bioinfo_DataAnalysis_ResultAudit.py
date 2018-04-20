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

# 数据分析结果列表
def DataAnalysisResult_Review(request):
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
        temp_unfinished = models.BioinfoDataAnalysisInfo.objects.filter(BioinfoResult_Sign=0)
        temp_finished = models.BioinfoDataAnalysisInfo.objects.filter(BioinfoResult_Sign=1)

        return render(request, "modelspage/BioinfoResultAudit_TaskReview.html",
                      {"userinfo": temp, "unfinished": temp_unfinished,
                       "finished": temp_finished, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 数据分析结果详情页
def DataAnalysisResult_To_Examine (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        sam_code_num = ''
        DataAnalysis_num = ''
        if request.method == "POST":
            print '患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号: ', sam_code_num
            # 数据分析次数
            DataAnalysis_num = request.POST.get('DataAnalysis_num')
            print '数据分析次数: ', DataAnalysis_num

        # 从数据里取出某条记录
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_userlist = User.objects.filter(first_name='生信部')
        temp_mysql = models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                   DataAnalysis_num=DataAnalysis_num)

        return render(request, "modelspage/BioinfoTask_Result.html",
                      {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                       "SystemMessage": temp_SystemMessage_Unread, "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 数据分析结果审核录入到数据库
def DataAnalysisResult_Examine_ToDataBases(request):
    # 样本信息
    sam_code_num = ''  # 样本条码号
    ExperimentNumber = ''  # 实验编号
    DataAnalysis_num = ''  # 数据分析次数
    # 审核信息
    Examine_Result = ''  # 审核结果
    Examine_Time = ''  # 审核时间
    Examine_Remarks = ''  # 审核备注
    ReportMakeTask_Man = ''  # 报告制作任务接收人
    Computer_Seq_num = ''  # 上机测序实验次数
    button_name = ''

    if request.method == "POST":
        print '样本信息: ============================================= '
        # 样本条码号
        sam_code_num = request.POST.get('sam_code_num')
        print '样本条码号: ', sam_code_num

        # 实验编号
        ExperimentNumber = request.POST.get('ExperimentNumber')
        print '实验编号: ', ExperimentNumber

        print '其他信息: ============================================= '
        # 数据分析次数
        DataAnalysis_num = request.POST.get('DataAnalysis_num')
        print '数据分析次数: ', DataAnalysis_num

        print '审核信息: ============================================= '
        # 审核结果
        Examine_Result = request.POST.get('Examine_Result')
        print '审核结果: ', Examine_Result

        # 审核时间
        Examine_Time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print '审核时间: ', Examine_Time

        # 审核备注
        Examine_Remarks = request.POST.get('Examine_Remarks')
        print '审核备注: ', Examine_Remarks

        ReportMakeTask_Man = request.POST.get('ReportMakeTask_Man')  # 报告制作任务接收人
        Computer_Seq_num = request.POST.get('Computer_Seq_num')  # 上机测序实验次数

        # 判断哪个按钮提交的数据
        if request.POST.has_key('Determine'):
            button_name = 'Determine'
        elif request.POST.has_key('submitModify'):
            button_name = 'submitModify'

    print '结束: ============================================= '

    # 用户信息
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print '首页，username: '.decode('utf-8'), username, department
        temp = {"username": username, "department": department}

        temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
            username=username)  # 用户操作权限信息
        # print 'ClinicalSampleRegistration: ', temp_UserOperationPermissionsInfo.ClinicalSampleRegistration
        if temp_UserOperationPermissionsInfo.BioinfoDataAnalysisResultReview == '1':

            if Examine_Result == '通过':
                if button_name == 'Determine':
                    # 添加数据到数据库
                    models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                  DataAnalysis_num=DataAnalysis_num).update(
                        Examine_Result=Examine_Result,
                        Examine_Time=Examine_Time,
                        Examine_Remarks=Examine_Remarks,
                        BioinfoResult_Sign='1',
                        ReportMakeTask_Man=ReportMakeTask_Man,
                    )
                    # 添加系统消息
                    Title = '通知：生信报告制作任务'  # 系统消息标题
                    Message = username + '分派给你一个生信报告制作任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                    models.UserSystemMessage.objects.create(
                        # 用户信息
                        Sender=username,  # 发送者
                        Receiver=ReportMakeTask_Man,  # 接收者
                        # 信息内容
                        Time=Examine_Time,  # 信息生成时间
                        Title=Title,  # 系统消息标题
                        Message=Message,  # 系统消息正文
                        ReadingState='未读',  # 信息阅读状态
                    )
                    sendEmail(ReportMakeTask_Man, Title, Message)  # 发送邮件通知
                elif button_name == 'submitModify':
                    temp_oldData = models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                                 DataAnalysis_num=DataAnalysis_num)
                    if not temp_oldData[0].Examine_Result == Examine_Result or not \
                                    temp_oldData[0].ReportMakeTask_Man == ReportMakeTask_Man and \
                                    temp_oldData[0].Report_Make_Sign == 0:
                        # 添加系统消息
                        Title = '通知：生信报告制作任务'  # 系统消息标题
                        Message = username + '分派给你一个生信报告制作任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                        models.UserSystemMessage.objects.create(
                            # 用户信息
                            Sender=username,  # 发送者
                            Receiver=ReportMakeTask_Man,  # 接收者
                            # 信息内容
                            Time=Examine_Time,  # 信息生成时间
                            Title=Title,  # 系统消息标题
                            Message=Message,  # 系统消息正文
                            ReadingState='未读',  # 信息阅读状态
                        )
                        sendEmail(ReportMakeTask_Man, Title, Message)  # 发送邮件通知

                    if not temp_oldData[0].Examine_Result == Examine_Result:
                        Data = models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                             DataAnalysis_num=DataAnalysis_num)
                        if Data[0].SampleSource == '临检样本':
                            models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                          DataAnalysis_num=DataAnalysis_num).update(
                                BioinfoResult_Sign='1',
                            )
                            models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                  ExperimentTimes=Computer_Seq_num).update(
                                Next_TaskProgress_Time=Examine_Time,
                                Next_TaskProgress_Remarks=Examine_Remarks,
                                Bioinfo_Sign='1',
                            )
                        else:
                            models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                          DataAnalysis_num=DataAnalysis_num).update(
                                BioinfoResult_Sign='1',
                            )
                            models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                             ExperimentTimes=Computer_Seq_num).update(
                                Next_TaskProgress_Time=Examine_Time,
                                Next_TaskProgress_Remarks=Examine_Remarks,
                                Bioinfo_Sign='1',
                            )

                    # 添加数据到数据库
                    models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                  DataAnalysis_num=DataAnalysis_num).update(
                        Examine_Result=Examine_Result,
                        Examine_Time=Examine_Time,
                        Examine_Remarks=Examine_Remarks,
                        BioinfoResult_Sign='1',
                        ReportMakeTask_Man=ReportMakeTask_Man,
                    )
            else:
                # 添加系统消息
                Title = '通知：样本重新分析任务'  # 系统消息标题
                Message = username + '分派给你一个样本重新分析任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                Data = models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                     DataAnalysis_num=DataAnalysis_num)
                if button_name == 'Determine':
                    if Data[0].SampleSource == '临检样本':
                        models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                      DataAnalysis_num=DataAnalysis_num).update(
                            BioinfoResult_Sign='1',
                            Examine_Result=Examine_Result,
                            Examine_Time=Examine_Time,
                            Examine_Remarks=Examine_Remarks,
                        )
                        models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                              ExperimentTimes=Computer_Seq_num).update(
                            Next_TaskProgress_Time=Examine_Time,
                            Next_TaskProgress_Remarks=Examine_Remarks,
                            Bioinfo_Sign='0',
                        )
                        sample = models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                       ExperimentTimes=Computer_Seq_num)
                        TaskReceiver = sample[0].Next_TaskProgress_Man
                    else:
                        models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                      DataAnalysis_num=DataAnalysis_num).update(
                            BioinfoResult_Sign='1',
                            Examine_Result=Examine_Result,
                            Examine_Time=Examine_Time,
                            Examine_Remarks=Examine_Remarks,
                        )
                        models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                         ExperimentTimes=Computer_Seq_num).update(
                            Next_TaskProgress_Time=Examine_Time,
                            Next_TaskProgress_Remarks=Examine_Remarks,
                            Bioinfo_Sign='0',
                        )
                        sample = models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                                  ExperimentTimes=Computer_Seq_num)
                        TaskReceiver = sample[0].Next_TaskProgress_Man

                    models.UserSystemMessage.objects.create(
                        # 用户信息
                        Sender=username,  # 发送者
                        Receiver=TaskReceiver,  # 接收者
                        # 信息内容
                        Time=Examine_Time,  # 信息生成时间
                        Title=Title,  # 系统消息标题
                        Message=Message,  # 系统消息正文
                        ReadingState='未读',  # 信息阅读状态
                    )
                    sendEmail(TaskReceiver, Title, Message)  # 发送邮件通知
                elif button_name == 'submitModify':
                    tag = 0
                    if not Data[0].Examine_Result == Examine_Result or not \
                                    Data[0].ReportMakeTask_Man == ReportMakeTask_Man and \
                                    Data[0].Report_Make_Sign == 0:
                        tag = 1
                    if Data[0].SampleSource == '临检样本':
                        models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                      DataAnalysis_num=DataAnalysis_num).update(
                            BioinfoResult_Sign='1',
                            Examine_Result=Examine_Result,
                            Examine_Time=Examine_Time,
                            Examine_Remarks=Examine_Remarks,
                        )
                        models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                              ExperimentTimes=Computer_Seq_num).update(
                            Next_TaskProgress_Time=Examine_Time,
                            Next_TaskProgress_Remarks=Examine_Remarks,
                            Bioinfo_Sign='0',
                        )
                        sample = models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                       ExperimentTimes=Computer_Seq_num)
                        TaskReceiver = sample[0].Next_TaskProgress_Man
                    else:
                        models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                      DataAnalysis_num=DataAnalysis_num).update(
                            BioinfoResult_Sign='1',
                            Examine_Result=Examine_Result,
                            Examine_Time=Examine_Time,
                            Examine_Remarks=Examine_Remarks,
                        )
                        models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                         ExperimentTimes=Computer_Seq_num).update(
                            Next_TaskProgress_Time=Examine_Time,
                            Next_TaskProgress_Remarks=Examine_Remarks,
                            Bioinfo_Sign='0',
                        )
                        sample = models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                                  ExperimentTimes=Computer_Seq_num)
                        TaskReceiver = sample[0].Next_TaskProgress_Man

                    if tag == 1:
                        models.UserSystemMessage.objects.create(
                            # 用户信息
                            Sender=username,  # 发送者
                            Receiver=TaskReceiver,  # 接收者
                            # 信息内容
                            Time=Examine_Time,  # 信息生成时间
                            Title=Title,  # 系统消息标题
                            Message=Message,  # 系统消息正文
                            ReadingState='未读',  # 信息阅读状态
                        )
                        sendEmail(TaskReceiver, Title, Message)  # 发送邮件通知

            # 从数据里取出所有数据
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            temp_unfinished = models.BioinfoDataAnalysisInfo.objects.filter(BioinfoResult_Sign=0)
            temp_finished = models.BioinfoDataAnalysisInfo.objects.filter(BioinfoResult_Sign=1)

            return render(request, "modelspage/BioinfoResultAudit_TaskReview.html",
                          {"userinfo": temp, "unfinished": temp_unfinished,
                           "finished": temp_finished, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
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

# 数据分析结果信息详情页
def DataAnalysis_Result_Examine_ShowData (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        sam_code_num = ''
        DataAnalysis_num = ''
        button_name = ''
        if request.method == "POST":
            print '患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号: ', sam_code_num
            # 数据分析次数
            DataAnalysis_num = request.POST.get('DataAnalysis_num')
            print '数据分析次数: ', DataAnalysis_num

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
        temp_mysql = models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num, DataAnalysis_num=DataAnalysis_num)

        if button_name == 'seeInfo':
            return render(request, "modelspage/Bioinfo_Result_Examine_ShowData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'ModifyData':
            temp_userlist = User.objects.filter(first_name='生信部')
            return render(request, "modelspage/BioinfoTask_ResultAudit_ModifyData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
