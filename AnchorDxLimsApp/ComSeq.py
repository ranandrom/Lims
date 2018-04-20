# encoding: utf-8

from django.shortcuts import render
from AnchorDxLimsApp import models
import time,httplib,datetime
from django.contrib.auth.models import User
from AnchorDxLimsApp.views import sendEmail
# Create your views here.
#coding:utf-8

from django.shortcuts import render,HttpResponse

# 上机测序任务列表
def ComSeqTask_Review(request):
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
        temp_Task = models.FinLibConInfo.objects.filter(Next_TaskProgress="上机测序", Next_TaskProgress_Sign='1',
                                                        ComputerSeq_Sign='0')  # 上机测序任务信息
        temp_pass = models.ComputerSeqInfo.objects.all()  # 上机测序任务已完成

        return render(request, "modelspage/ComSeqTaskReview.html",
                      {"userinfo": temp, "data": temp_Task, "pass": temp_pass, "myInfo": temp_myInfo,
                       "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 上机测序数据录入页
def ComSeqTask_To_Examine (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        sam_code_num = ''
        Build_finlib_num = ''
        if request.method == "POST":
            print '患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号: ', sam_code_num
            # 终文库构建次数
            Build_finlib_num = request.POST.get('Build_finlib_num')
            print '终文库构建次数: ', Build_finlib_num

        # 从数据里取出某条记录
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_userlist = User.objects.filter(first_name='生信部')
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_mysql = models.FinLibConInfo.objects.filter(sam_code_num=sam_code_num, ExperimentTimes=Build_finlib_num)

        return render(request, "modelspage/ComSeqTask_submit.html",
                      {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                       "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 上机测序数据录入到数据库
def ComSeqInfoToDataBases(request):
    # 样本信息
    sam_code_num = ''  # 样本条码号
    ExperimentNumber = ''  # 实验编号
    DNA_extraction_num = '' # DNA提取实验次数
    Build_Prelib_num = ''  # 预文库构建实验次数
    Build_finlib_num = '' # 终文库构建次数
    # 上机测序信息
    DilutionMultiple = ''  # 稀释倍数
    qPCR = ''  # qPCR测量值(pM)
    AverageLengthLibrary = ''  # 文库平均长度(bp)
    LibEffConcentration = ''  # 文库有效浓度(nM)
    QuantitativeHuman = ''   # 定量人
    OperatingTime = ''  # 操作时间（系统默认）
    SeqRemarks = ''   # 其它（备注）
    BioTaskAssignment = ''  # 生信分析任务分派人
    button_name = ''  # 按钮名字
    if request.method == "POST":
        print '样本信息: ============================================= '
        # 样本条码号
        sam_code_num = request.POST.get('sam_code_num')
        print '样本条码号: ', sam_code_num

        # 实验编号
        ExperimentNumber = request.POST.get('ExperimentNumber')
        print '实验编号: ', ExperimentNumber

        # DNA提取实验次数
        DNA_extraction_num = request.POST.get('DNA_extraction_num')
        print 'DNA提取实验次数: ', DNA_extraction_num

        # 预文库构建实验次数
        Build_Prelib_num = request.POST.get('Build_Prelib_num')
        print '预文库构建实验次数: ', Build_Prelib_num

        # 终文库构建次数
        Build_finlib_num = request.POST.get('Build_finlib_num')
        print '终文库构建次数: ', Build_finlib_num

        print '上机测序信息: ============================================= '

        # 稀释倍数
        DilutionMultiple = request.POST.get('DilutionMultiple')
        print '稀释倍数: ', DilutionMultiple

        # qPCR测量值(pM)
        qPCR = request.POST.get('qPCR')
        print 'qPCR测量值(pM): ', qPCR

        # 文库平均长度(bp)
        AverageLengthLibrary = request.POST.get('AverageLengthLibrary')
        print '文库平均长度(bp): ', AverageLengthLibrary

        # 文库有效浓度(nM)
        LibEffConcentration = request.POST.get('LibEffConcentration')
        print '文库有效浓度(nM): ', LibEffConcentration

        # 定量人
        QuantitativeHuman = request.POST.get('QuantitativeHuman')
        print '定量人: ', QuantitativeHuman

        # 操作时间
        OperatingTime = request.POST.get('OperatingTime')
        print '操作时间: ', OperatingTime

        # 其它（备注）
        SeqRemarks = request.POST.get('SeqRemarks')
        print '其它（备注）: ', SeqRemarks

        # 生信分析任务分派人
        BioTaskAssignment = request.POST.get('BioTaskAssignment')

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
        if temp_UserOperationPermissionsInfo.ComSeqTaskReview == '1':
            if button_name == 'Determine':
                temp_ComSeqTask = models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num)
                num = len(temp_ComSeqTask)

                # 添加数据到数据库
                models.ComputerSeqInfo.objects.create(
                    # 用户信息
                    username=username,  # 用户名
                    department=department,  # 部门
                    # 样本信息
                    sam_code_num=sam_code_num,  # 样本条码号
                    ExperimentNumber=ExperimentNumber,  # 实验编号
                    # 上机测序信息
                    DilutionMultiple=DilutionMultiple,  # 稀释倍数
                    qPCR=qPCR,  # qPCR测量值(pM)
                    AverageLengthLibrary=AverageLengthLibrary,  # 文库平均长度(bp)
                    LibEffConcentration=LibEffConcentration,  # 文库有效浓度(nM)
                    QuantitativeHuman=QuantitativeHuman,  # 定量人
                    OperatingTime=OperatingTime,  # 操作时间（系统默认）
                    SeqRemarks=SeqRemarks,  # 其它（备注）
                    BioTaskAssignment=BioTaskAssignment,  # 生信分析任务分派人
                    # 其他信息
                    DNA_extraction_num=DNA_extraction_num,  # DNA提取实验次数
                    Build_Prelib_num=Build_Prelib_num,  # 预文库构建实验次数
                    Build_finlib_num=Build_finlib_num,  # 终文库构建实验次数
                    ExperimentTimes=num + 1,  # 上机测序实验次数
                    Bioinfo_Sign=0,  # 生信任务标记
                    Next_TaskProgress_Sign=0,  # 下一步任务分配标记
                )
                models.FinLibConInfo.objects.filter(sam_code_num=sam_code_num, Next_TaskProgress="上机测序",
                                                    ExperimentTimes=Build_finlib_num).update(ComputerSeq_Sign='1')

                # 添加系统消息
                taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                Title = '通知：临检样本生信分析分派任务'  # 系统消息标题
                Message = username + '分派给你一个临检样本生信分析分派任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                models.UserSystemMessage.objects.create(
                    # 用户信息
                    Sender=username,  # 发送者
                    Receiver=BioTaskAssignment,  # 接收者
                    # 信息内容
                    Time=taskTime,  # 信息生成时间
                    Title=Title,  # 系统消息标题
                    Message=Message,  # 系统消息正文
                    ReadingState='未读',  # 信息阅读状态
                )
                sendEmail(BioTaskAssignment, Title, Message)  # 发送邮件通知
            elif button_name == 'submitModify':
                # 上机测序实验次数
                Computer_Seq_num = request.POST.get('Computer_Seq_num')
                temp_data = models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                  ExperimentTimes=Computer_Seq_num)
                if not temp_data[0].BioTaskAssignment == BioTaskAssignment and temp_data[0].Next_TaskProgress_Sign == '0':
                    # 添加系统消息
                    taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    Title = '通知：临检样本生信分析分派任务'  # 系统消息标题
                    Message = username + '分派给你一个临检样本生信分析分派任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                    models.UserSystemMessage.objects.create(
                        # 用户信息
                        Sender=username,  # 发送者
                        Receiver=BioTaskAssignment,  # 接收者
                        # 信息内容
                        Time=taskTime,  # 信息生成时间
                        Title=Title,  # 系统消息标题
                        Message=Message,  # 系统消息正文
                        ReadingState='未读',  # 信息阅读状态
                    )
                    sendEmail(BioTaskAssignment, Title, Message)  # 发送邮件通知

                models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num, ExperimentTimes=Computer_Seq_num).update(
                    # 上机测序信息
                    DilutionMultiple=DilutionMultiple,  # 稀释倍数
                    qPCR=qPCR,  # qPCR测量值(pM)
                    AverageLengthLibrary=AverageLengthLibrary,  # 文库平均长度(bp)
                    LibEffConcentration=LibEffConcentration,  # 文库有效浓度(nM)
                    QuantitativeHuman=QuantitativeHuman,  # 定量人
                    OperatingTime=OperatingTime,  # 操作时间（系统默认）
                    SeqRemarks=SeqRemarks,  # 其它（备注）
                    BioTaskAssignment=BioTaskAssignment,  # 生信分析任务分派人
                )

            # 从数据里取出所有数据
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            temp_ComSeqTask = models.FinLibConInfo.objects.filter(Next_TaskProgress="上机测序", Next_TaskProgress_Sign='1',ComputerSeq_Sign='0')  # 上机测序任务未完成
            temp_pass = models.ComputerSeqInfo.objects.all()  # 上机测序任务已完成

            return render(request, "modelspage/ComSeqTaskReview.html",
                          {"userinfo": temp, "data": temp_ComSeqTask, "pass": temp_pass, "myInfo": temp_myInfo,
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


# 上机测序信息详情页
def ComSeqTask_ShowData (request):
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

            # 判断哪个按钮提交的数据
            if request.POST.has_key('seeInfo'):
                button_name = 'seeInfo'
            elif request.POST.has_key('ModifyData'):
                button_name = 'ModifyData'
            elif request.POST.has_key('delete'):
                temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                    username=username)  # 用户操作权限信息
                # print 'ClinicalSampleRegistration: ', temp_UserOperationPermissionsInfo.ClinicalSampleRegistration
                if temp_UserOperationPermissionsInfo.ComSeqTaskReview == '1':
                    models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                          ExperimentTimes=Computer_Seq_num).delete()
                    # 从数据里取出所有数据
                    # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
                    temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                        ReadingState='未读')  # 用户信息
                    num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
                    temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
                    temp_Task = models.FinLibConInfo.objects.filter(Next_TaskProgress="上机测序",
                                                                    Next_TaskProgress_Sign='1',
                                                                    ComputerSeq_Sign='0')  # 上机测序任务信息
                    temp_pass = models.ComputerSeqInfo.objects.all()  # 上机测序任务已完成

                    return render(request, "modelspage/ComSeqTaskReview.html",
                                  {"userinfo": temp, "data": temp_Task, "pass": temp_pass, "myInfo": temp_myInfo,
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

        # 从数据里取出某条记录
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_mysql = models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num, ExperimentTimes=Computer_Seq_num)  # 终文库构建信息

        if button_name == 'seeInfo':
            return render(request, "modelspage/ComSeqTask_ShowData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'ModifyData':
            temp_userlist = User.objects.filter(first_name='生信部')
            return render(request, "modelspage/ComSeqTask_ModifyData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
