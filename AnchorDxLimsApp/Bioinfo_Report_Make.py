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

# 报告制作任务列表
def Bioinfo_Report_Task_Review(request):
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
        temp_unfinished = models.BioinfoDataAnalysisInfo.objects.filter(Report_Make_Sign=0, BioinfoResult_Sign=1,
                                                                        Examine_Result='通过')
        temp_Make = models.BioinfoDataAnalysisInfo.objects.filter(Report_Make_Sign=1, BioinfoResult_Sign=1,
                                                                  Medical_Examine_Result='不通过')
        temp_Operate = models.BioinfoDataAnalysisInfo.objects.filter(Report_Make_Sign=1, BioinfoResult_Sign=1,
                                                                     Operate_Examine_Result='不通过')
        temp_AllNoPass = chain(temp_Make, temp_Operate)  # 合并所有数据表数据
        temp_NoPass = list(set(temp_AllNoPass))
        temp_finished = models.BioinfoDataAnalysisInfo.objects.filter(Report_Make_Sign=1, BioinfoResult_Sign=1)

        return render(request, "modelspage/Bioinfo_Report_Task_Review.html",
                      {"userinfo": temp, "unfinished": temp_unfinished,
                       "NoPass": temp_NoPass,
                       "finished": temp_finished, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 报告制作信息录入页
def Bioinfo_Report_Info_Input (request):
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
        temp_userlist = User.objects.filter(first_name='市场部')
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_mysql = models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                   DataAnalysis_num=DataAnalysis_num)

        return render(request, "modelspage/Bioinfo_Report_Info_Submit.html",
                      {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                       "SystemMessage": temp_SystemMessage_Unread, "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 报告制作信息重新录入页
def Bioinfo_Report_Info_Again_Input (request):
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
        temp_userlist = User.objects.filter(first_name='市场部')
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_mysql = models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                   DataAnalysis_num=DataAnalysis_num)

        return render(request, "modelspage/Bioinfo_Report_Info_Again_Submit.html",
                      {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                       "SystemMessage": temp_SystemMessage_Unread, "num_SystemMessage_Unread": num_SystemMessage_Unread})


# 报告制作信息录入到数据库以及报告文件上传
def Bioinfo_Report_InfoToDataBases(request):
    Report_File_Name = ''  # 报告文件名
    # 报告制作信息录入到数据库
    # 样本信息
    sam_code_num = ''  # 样本条码号
    ExperimentNumber = ''  # 实验编号
    DataAnalysis_num = ''  # 数据分析次数
    # 报告制作信息
    Report_Maker = ''  # 报告制作人
    Report_Make_Time = ''  # 报告制作时间
    Report_Remarks = ''  # 报告备注
    GeneticCounselor = ''  # 遗传咨询师
    button_name = ''
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

        # 报告制作人
        Report_Maker = request.POST.get('Report_Maker')
        print '报告制作人: ', Report_Maker

        # 报告制作时间
        Report_Make_Time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print '报告制作时间: ', Report_Make_Time

        # 报告备注
        Report_Remarks = request.POST.get('Report_Remarks')
        print '报告备注: ', Report_Remarks

        GeneticCounselor = request.POST.get('GeneticCounselor')  # 遗传咨询师

        # 判断哪个按钮提交的数据
        if request.POST.has_key('Determine'):
            button_name = 'Determine'
        elif request.POST.has_key('submitModify'):
            button_name = 'submitModify'
        elif request.POST.has_key('DownloadReport'):
            button_name = 'DownloadReport'

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
        if temp_UserOperationPermissionsInfo.BioinfoReportTaskReview == '1':
            if button_name == 'Determine':
                # 上传文件
                if request.method == "POST":  # 请求方法为POST时，进行处理  
                    myFile = request.FILES.get("myfile", None)  #  获取上传的文件，如果没有文件，则默认为None
                    if not myFile:
                        return HttpResponse("no files for upload!")
                    if not os.path.exists('./upload'):
                        os.makedirs('./upload')
                    Report_File_Name = myFile.name
                    destination = open(os.path.join("./upload", myFile.name), 'wb+')  #  打开特定的文件进行二进制的写操作
                    if myFile.multiple_chunks() == False:
                        # 使用myFile.read()
                        for read in myFile.read():  # 整个上传  
                            destination.write(read)
                    else:
                        # 使用myFile.chunks()
                        for chunk in myFile.chunks():  # 分块写入文件
                            destination.write(chunk)
                    destination.close()
                    # return HttpResponse("upload over!")

                # 添加数据到数据库
                models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                              DataAnalysis_num=DataAnalysis_num).update(
                    Report_Maker=Report_Maker,
                    Report_Make_Time=Report_Make_Time,
                    Report_Remarks=Report_Remarks,
                    Report_Make_Sign='1',
                    Report_File_Name=Report_File_Name,
                    GeneticCounselor=GeneticCounselor,
                    Medical_Examine_Sign=0,
                    Operate_Examine_Sign=0,
                    Medical_Examine_Result='',
                    Operate_Examine_Result='',
                )

                # 添加系统消息
                Title = '通知：样本报告审核任务'  # 系统消息标题
                Message = username + '分派给你一个样本报告审核任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                models.UserSystemMessage.objects.create(
                    # 用户信息
                    Sender=username,  # 发送者
                    Receiver=GeneticCounselor,  # 接收者
                    # 信息内容
                    Time=Report_Make_Time,  # 信息生成时间
                    Title=Title,  # 系统消息标题
                    Message=Message,  # 系统消息正文
                    ReadingState='未读',  # 信息阅读状态
                )
                sendEmail(GeneticCounselor, Title, Message)  # 发送邮件通知

            elif button_name == 'submitModify':
                temp_oldData = models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                             DataAnalysis_num=DataAnalysis_num)
                if not temp_oldData[0].GeneticCounselor == GeneticCounselor and temp_oldData[0].Medical_Examine_Sign == '0':
                    # 添加系统消息
                    Title = '通知：样本报告审核任务'  # 系统消息标题
                    Message = username + '分派给你一个样本报告审核任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                    models.UserSystemMessage.objects.create(
                        # 用户信息
                        Sender=username,  # 发送者
                        Receiver=GeneticCounselor,  # 接收者
                        # 信息内容
                        Time=Report_Make_Time,  # 信息生成时间
                        Title=Title,  # 系统消息标题
                        Message=Message,  # 系统消息正文
                        ReadingState='未读',  # 信息阅读状态
                    )
                    sendEmail(GeneticCounselor, Title, Message)  # 发送邮件通知

                # 添加数据到数据库
                models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                              DataAnalysis_num=DataAnalysis_num).update(
                    Report_Maker=Report_Maker,
                    Report_Make_Time=Report_Make_Time,
                    Report_Remarks=Report_Remarks,
                    GeneticCounselor=GeneticCounselor,
                )
            elif button_name == 'DownloadReport':
                # 显示在弹出对话框中的默认的下载文件名 
                Report_File_Name = request.POST.get('Report_File_Name')  # 报告文件名
                print '报告文件名: ', Report_File_Name
                # the_file_name='11.png' #显示在弹出对话框中的默认的下载文件名  
                # filename='media/uploads/11.png' # 要下载的文件路径
                filename = './upload/' + Report_File_Name  # 要下载的文件路径
                response = StreamingHttpResponse(ReadFile(filename))
                response['Content-Type'] = 'application/octet-stream'
                response['Content-Disposition'] = 'attachment;filename="{0}"'.format(Report_File_Name)
                return response

            # 从数据里取出所有数据
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            temp_unfinished = models.BioinfoDataAnalysisInfo.objects.filter(Report_Make_Sign=0, BioinfoResult_Sign=1,
                                                                            Examine_Result='通过')
            temp_Make = models.BioinfoDataAnalysisInfo.objects.filter(Report_Make_Sign=1, BioinfoResult_Sign=1,
                                                                      Medical_Examine_Result='不通过')
            temp_Operate = models.BioinfoDataAnalysisInfo.objects.filter(Report_Make_Sign=1, BioinfoResult_Sign=1,
                                                                         Operate_Examine_Result='不通过')
            temp_NoPass = chain(temp_Make, temp_Operate)  # 合并所有数据表数据
            temp_finished = models.BioinfoDataAnalysisInfo.objects.filter(Report_Make_Sign=1, BioinfoResult_Sign=1)

            return render(request, "modelspage/Bioinfo_Report_Task_Review.html",
                          {"userinfo": temp, "unfinished": temp_unfinished,
                           "NoPass": temp_NoPass,
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

# 数据分析报告制作信息详情页
def Bioinfo_Report_ShowData (request):
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
            return render(request, "modelspage/Bioinfo_Report_ShowData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'ModifyData':
            temp_userlist = User.objects.filter(first_name='市场部')
            return render(request, "modelspage/Bioinfo_Report_ModifyData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 报告下载
def download_file(request):
    # 显示在弹出对话框中的默认的下载文件名 
    Report_File_Name =request.POST.get('Report_File_Name')  # 报告文件名
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
