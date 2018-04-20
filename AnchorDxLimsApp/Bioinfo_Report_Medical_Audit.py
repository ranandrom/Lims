# encoding: utf-8

from django.shortcuts import render
from AnchorDxLimsApp import models
from django.contrib.auth.models import User
from time import strftime,gmtime
from itertools import chain
import time,httplib,datetime
from AnchorDxLimsApp.views import sendEmail
from itertools import chain
import os
from django.http import StreamingHttpResponse
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# Create your views here.
#coding:utf-8

from django.shortcuts import render,HttpResponse

# 遗传咨询师审核报告任务列表
def Bioinfo_Report_Medical_Audit_Task_Review(request):
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
        temp_unfinished = models.BioinfoDataAnalysisInfo.objects.filter(Report_Make_Sign=1, Medical_Examine_Sign=0)
        temp_finished = models.BioinfoDataAnalysisInfo.objects.filter(Report_Make_Sign=1, Medical_Examine_Sign=1)

        return render(request, "modelspage/Bioinfo_Report_Medical_Audit_Task_Review.html",
                      {"userinfo": temp, "unfinished": temp_unfinished,
                       "finished": temp_finished, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 遗传咨询师审核报告信息录入页
def Bioinfo_Report_Medical_Audit_Info_Input (request):
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
        temp_userlist = User.objects.filter(first_name='市场部')
        temp_mysql = models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                   DataAnalysis_num=DataAnalysis_num)

        return render(request, "modelspage/Bioinfo_Report_Medical_Audit_Submit.html",
                      {"data": temp_mysql, "userinfo": temp, "userlist": temp_userlist, "myInfo": temp_myInfo,
                       "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

#  遗传咨询师审核报告信息录入到数据库以及报告文件下载
def Bioinfo_Report_Medical_Audit_InfoToDataBases(request):
    button_name = ''  # 按钮名字
    Report_File_Name = request.POST.get('Report_File_Name')  # 报告文件名
    # 判断哪个按钮提交的数据
    if request.POST.has_key('download'):
        button_name = 'download'
    elif request.POST.has_key('Determine'):
        button_name = 'Determine'
    elif request.POST.has_key('submitModify'):
        button_name = 'submitModify'

    # 报告制作信息录入到数据库
    # 样本信息
    sam_code_num = ''  # 样本条码号
    ExperimentNumber = ''  # 实验编号
    DataAnalysis_num = ''  # 数据分析次数
    # 遗传咨询师审核报告信息
    Medical_Examine_Result = ''  # 审核结果
    Medical_Examine_Time = ''  # 审核时间
    Medical_Examine_Remarks = ''  # 审核备注
    Operater = ''  # 运营审核人
    NoPass = '' # 不通过

    if request.method == "POST":
        print '样本信息: ============================================= '
        # 样本条码号
        sam_code_num = request.POST.get('sam_code_num')
        print '样本条码号: ', sam_code_num

        # 实验编号
        ExperimentNumber = request.POST.get('ExperimentNumber')
        print '实验编号: ', ExperimentNumber

        # 数据分析次数
        DataAnalysis_num = request.POST.get('DataAnalysis_num')
        print '数据分析次数: ', DataAnalysis_num

        print '其他信息: ============================================= '

        # 审核结果
        Medical_Examine_Result = request.POST.get('Medical_Examine_Result')
        print '审核结果: ', Medical_Examine_Result

        # 审核时间
        Medical_Examine_Time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print '审核时间: ', Medical_Examine_Time

        # 审核备注
        Medical_Examine_Remarks = request.POST.get('Medical_Examine_Remarks')
        print '审核备注: ', Medical_Examine_Remarks

        Operater = request.POST.get('Operater')  # 运营审核人

        # 不通过
        NoPass = request.POST.get('NoPass')
        print '不通过: ', NoPass

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

        # 从数据里取出所有数据
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息

        if button_name == 'download':
            print '报告文件名: ', Report_File_Name
            filename = './upload/' + Report_File_Name  # 要下载的文件路径
            response = StreamingHttpResponse(ReadFile(filename))
            response['Content-Type'] = 'application/octet-stream'
            response['Content-Disposition'] = 'attachment;filename="{0}"'.format(Report_File_Name)
            return response
        elif button_name == 'Determine':
            temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                username=username)  # 用户操作权限信息
            # print 'ClinicalSampleRegistration: ', temp_UserOperationPermissionsInfo.ClinicalSampleRegistration
            if temp_UserOperationPermissionsInfo.BioinfoReportMedicalAuditTaskReview == '1':
                # 添加数据到数据库
                models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                              DataAnalysis_num=DataAnalysis_num).update(
                    Medical_Examine_Result=Medical_Examine_Result,
                    Medical_Examine_Time=Medical_Examine_Time,
                    Medical_Examine_Remarks=Medical_Examine_Remarks,
                    Medical_Examine_Sign='1',
                    Operater=Operater,
                )

                if Medical_Examine_Result == '通过':
                    # 添加系统消息
                    Title = '通知：生信报告审核任务'  # 系统消息标题
                    Message = username + '分派给你一个生信报告审核任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                    user = Operater
                else:
                    # 添加系统消息
                    Title = '通知：生信报告重制作任务'  # 系统消息标题
                    Message = username + '分派给你一个生信报告重制作任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                    sample = models.BioinfoDataAnalysisInfo.objects.get(sam_code_num=sam_code_num,
                                                                        DataAnalysis_num=DataAnalysis_num)
                    user = sample.ReportMakeTask_Man

                models.UserSystemMessage.objects.create(
                    # 用户信息
                    Sender=username,  # 发送者
                    Receiver=user,  # 接收者
                    # 信息内容
                    Time=Medical_Examine_Time,  # 信息生成时间
                    Title=Title,  # 系统消息标题
                    Message=Message,  # 系统消息正文
                    ReadingState='未读',  # 信息阅读状态
                )
                sendEmail(user, Title, Message)  # 发送邮件通知

                temp_unfinished = models.BioinfoDataAnalysisInfo.objects.filter(Report_Make_Sign=1, Medical_Examine_Sign=0)
                temp_finished = models.BioinfoDataAnalysisInfo.objects.filter(Report_Make_Sign=1, Medical_Examine_Sign=1)

                return render(request, "modelspage/Bioinfo_Report_Medical_Audit_Task_Review.html",
                              {"userinfo": temp, "unfinished": temp_unfinished,
                               "finished": temp_finished, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})
            else:
                return render(request, "modelspage/PermissionsPrompt.html",
                              {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})

        elif button_name == 'submitModify':
            temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                username=username)  # 用户操作权限信息
            # print 'ClinicalSampleRegistration: ', temp_UserOperationPermissionsInfo.ClinicalSampleRegistration
            if temp_UserOperationPermissionsInfo.BioinfoReportMedicalAuditTaskReview == '1':
                temp_OldData = models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                             DataAnalysis_num=DataAnalysis_num)
                if Medical_Examine_Result == '通过':
                    if not temp_OldData[0].Medical_Examine_Result == Medical_Examine_Result and \
                                    temp_OldData[0].Operate_Examine_Result == '' or not \
                                    temp_OldData[0].Operater == Operater:
                        # 添加系统消息
                        Title = '通知：生信报告审核任务'  # 系统消息标题
                        Message = username + '分派给你一个生信报告审核任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                        user = Operater
                        models.UserSystemMessage.objects.create(
                            # 用户信息
                            Sender=username,  # 发送者
                            Receiver=user,  # 接收者
                            # 信息内容
                            Time=Medical_Examine_Time,  # 信息生成时间
                            Title=Title,  # 系统消息标题
                            Message=Message,  # 系统消息正文
                            ReadingState='未读',  # 信息阅读状态
                        )
                        sendEmail(user, Title, Message)  # 发送邮件通知
                elif Medical_Examine_Result == '不通过':
                    if not temp_OldData[0].Medical_Examine_Result == Medical_Examine_Result:
                        # 添加系统消息
                        Title = '通知：生信报告重制作任务'  # 系统消息标题
                        Message = username + '分派给你一个生信报告重制作任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                        sample = models.BioinfoDataAnalysisInfo.objects.get(sam_code_num=sam_code_num,
                                                                            DataAnalysis_num=DataAnalysis_num)
                        user = sample.ReportMakeTask_Man
                        models.UserSystemMessage.objects.create(
                            # 用户信息
                            Sender=username,  # 发送者
                            Receiver=user,  # 接收者
                            # 信息内容
                            Time=Medical_Examine_Time,  # 信息生成时间
                            Title=Title,  # 系统消息标题
                            Message=Message,  # 系统消息正文
                            ReadingState='未读',  # 信息阅读状态
                        )
                        sendEmail(user, Title, Message)  # 发送邮件通知

                # 添加数据到数据库
                models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                              DataAnalysis_num=DataAnalysis_num).update(
                    Medical_Examine_Result=Medical_Examine_Result,
                    Medical_Examine_Time=Medical_Examine_Time,
                    Medical_Examine_Remarks=Medical_Examine_Remarks,
                    Medical_Examine_Sign='1',
                    Operater=Operater,
                )

                temp_unfinished = models.BioinfoDataAnalysisInfo.objects.filter(Report_Make_Sign=1,
                                                                                Medical_Examine_Sign=0)
                temp_finished = models.BioinfoDataAnalysisInfo.objects.filter(Report_Make_Sign=1,
                                                                              Medical_Examine_Sign=1)

                return render(request, "modelspage/Bioinfo_Report_Medical_Audit_Task_Review.html",
                              {"userinfo": temp, "unfinished": temp_unfinished,
                               "finished": temp_finished, "myInfo": temp_myInfo,
                               "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})
            else:
                return render(request, "modelspage/PermissionsPrompt.html",
                              {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})

#  遗传咨询师审核报告信息详情页
def Bioinfo_Report_Medical_Audit_ShowData (request):
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
        temp_mysql = models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                   DataAnalysis_num=DataAnalysis_num)

        if button_name == 'seeInfo':
            return render(request, "modelspage/Bioinfo_Report_Medical_Audit_ShowData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'ModifyData':
            temp_userlist = User.objects.filter(first_name='市场部')
            return render(request, "modelspage/Bioinfo_Report_Medical_Audit_ModifyData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 报告下载
def download_file(Report_File_Name):
    # 显示在弹出对话框中的默认的下载文件名 
    # Report_File_Name =request.POST.get('Report_File_Name')  # 报告文件名
    print '报告文件名: ', Report_File_Name
    # the_file_name='11.png' #显示在弹出对话框中的默认的下载文件名  
    # filename='media/uploads/11.png' # 要下载的文件路径
    filename='./upload/'+Report_File_Name  # 要下载的文件路径
    response=StreamingHttpResponse(ReadFile(filename))
    response['Content-Type']='application/octet-stream'
    response['Content-Disposition']='attachment;filename="{0}"'.format(Report_File_Name)
    return response

def ReadFile(filename,chunk_size=512):
    with open(filename,'rb') as f:
        while True:
            c=f.read(chunk_size)
            if c:
                yield c
            else:
                break
