# encoding: utf-8

from django.shortcuts import render
from AnchorDxLimsApp import models
from django.contrib.auth.models import User
import time,httplib,datetime
from AnchorDxLimsApp.views import sendEmail
from itertools import chain
# Create your views here.
#coding:utf-8

from django.shortcuts import render,HttpResponse

# DNA提取任务列表
def DNAExtractTask_Review(request):
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

        temp_not_Pretreatment = models.clinicalSampleInfo.objects.filter(Next_TaskProgress_Sign=1, TissueSampleSign=1,
                                                                         DNAExtract_Sign=0)  # 任务已分配信息
        temp_Pretreatment = models.clinicalSamplePretreatment.objects.filter(DNAExtract_Sign=0,
                                                                             Next_TaskProgress_Sign=1)  # 任务已分配信息
        temp_DNAExtractTask = chain(temp_not_Pretreatment, temp_Pretreatment)  # 合并所有数据表数据

        Pending_audit = models.DNAExtractInfo.objects.all()  # 所有已完成DNA提取数据信息

        return render(request, "modelspage/DNAExtractTaskReview.html",
                      {"userinfo": temp, "data": temp_DNAExtractTask, "Pending_audit": Pending_audit,
                       "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# DNA提取数据录入页
def DNAExtractTask_To_Examine (request):
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
        temp_mysql = models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num)

        return render(request, "modelspage/DNAExtractTask_submit.html",
                      {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# DNA提取数据录入到数据库
def DNAExtractInfoToDataBases(request):
    # 样本信息
    sam_code_num = ''  # 样本条码号
    ExperimentNumber = ''  # 实验编号
    # DNA提取信息
    DNA_Concentration = ''  # DNA浓度(ng/µL)
    DNA_volume = ''  # DNA体积(µL)
    DNA_Total = ''  # DNA总量(ng)
    Quality_inspection_method = ''   # 质检方法
    Quality_inspection_result = ''    # 质检结果
    Quality_inspection_volume = ''  # 质检使用体积(µL)
    Residual_volume = ''  # 剩余体积(µL)
    Extraction_kit_type = ''   # 提取试剂盒类型
    DNA_extraction_people = ''   # DNA提取人
    DNA_extraction_time = ''  # 提取时间
    DNA_extraction_remarks = ''   # 其它（备注）
    button_name = ''  # 按钮名字
    if request.method == "POST":
        print '样本信息: ============================================= '
        # 样本条码号
        sam_code_num = request.POST.get('sam_code_num')
        print '样本条码号: ', sam_code_num

        # 实验编号
        ExperimentNumber = request.POST.get('ExperimentNumber')
        print '实验编号: ', ExperimentNumber

        print 'DNA提取信息: ============================================= '

        # DNA浓度
        DNA_Concentration = request.POST.get('DNA_Concentration')
        print 'DNA浓度: ', DNA_Concentration

        # DNA体积
        DNA_volume = request.POST.get('DNA_volume')
        print 'DNA体积: ', DNA_volume

        # DNA总量
        DNA_Total = request.POST.get('DNA_Total')
        print 'DNA总量: ', DNA_Total

        # 质检方法
        Quality_inspection_method = request.POST.get('Quality_inspection_method')
        print '质检方法: ', Quality_inspection_method

        # 质检结果
        Quality_inspection_result = request.POST.get('Quality_inspection_result')
        print '质检结果: ', Quality_inspection_result

        # 质检使用体积
        Quality_inspection_volume = request.POST.get('Quality_inspection_volume')
        print '质检使用体积: ', Quality_inspection_volume

        # 剩余体积
        Residual_volume = request.POST.get('Residual_volume')
        print '剩余体积: ', Residual_volume

        # 提取试剂盒类型
        Extraction_kit_type = request.POST.get('Extraction_kit_type')
        print '提取试剂盒类型: ', Extraction_kit_type

        # DNA提取人
        DNA_extraction_people = request.POST.get('DNA_extraction_people')
        print 'DNA提取人: ', DNA_extraction_people

        # 提取时间
        DNA_extraction_time = request.POST.get('DNA_extraction_time')
        print '提取时间: ', DNA_extraction_time

        # 其它（备注）
        DNA_extraction_remarks = request.POST.get('DNA_extraction_remarks')
        print '其它（备注）: ', DNA_extraction_remarks

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
        if temp_UserOperationPermissionsInfo.DNAExtractTaskReview == '1':
            if button_name == 'Determine':
                temp_DNAExtractTask = models.DNAExtractInfo.objects.filter(sam_code_num=sam_code_num)  # DNA提取样本信息
                num = len(temp_DNAExtractTask)

                # 添加数据到数据库
                models.DNAExtractInfo.objects.create(
                    # 用户信息
                    username=username,  # 用户名
                    department=department,  # 部门
                    # 样本信息
                    sam_code_num=sam_code_num,  # 样本条码号
                    ExperimentNumber=ExperimentNumber,  # 实验编号
                    # DNA提取信息
                    DNA_Concentration=DNA_Concentration,  # DNA浓度(ng/µL)
                    DNA_volume=DNA_volume,  # DNA体积(µL)
                    DNA_Total=DNA_Total,  # DNA总量(ng)
                    Quality_inspection_method=Quality_inspection_method,  # 质检方法
                    Quality_inspection_result=Quality_inspection_result,  # 质检结果
                    Quality_inspection_volume=Quality_inspection_volume,  # 质检使用体积(µL)
                    Residual_volume=Residual_volume,  # 剩余体积(µL)
                    Extraction_kit_type=Extraction_kit_type,  # 提取试剂盒类型
                    DNA_extraction_people=DNA_extraction_people,  # DNA提取人
                    DNA_extraction_time=DNA_extraction_time,  # 提取时间
                    DNA_extraction_remarks=DNA_extraction_remarks,  # 其它（备注）
                    # 其他信息
                    ExperimentTimes=num+1,  # DNA提取实验次数
                    Next_TaskProgress_Sign=0,  # 审核标志
                    Next_TaskProgress='DNA提取',  # 任务进度
                    PreLibCon_Sign=0  # 预文库构建任务标记
                )
                models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num).update(DNAExtract_Sign='1')
                models.clinicalSamplePretreatment.objects.filter(sam_code_num=sam_code_num).update(DNAExtract_Sign='1')

                # 添加系统消息
                taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                Title = '通知：临检样本预文库构建实验分派任务'  # 系统消息标题
                Message = username + '分派给你一个临检样本预文库构建实验分派任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                sample = models.clinicalSampleInfo.objects.get(sam_code_num=sam_code_num)
                TaskReceiver = sample.TaskAssignment
                models.UserSystemMessage.objects.create(
                    # 用户信息
                    Sender=username,  # 发送者
                    Receiver=TaskReceiver,  # 接收者
                    # 信息内容
                    Time=taskTime,  # 信息生成时间
                    Title=Title,  # 系统消息标题
                    Message=Message,  # 系统消息正文
                    ReadingState='未读',  # 信息阅读状态
                )
                sendEmail(TaskReceiver, Title, Message)  # 发送邮件通知
            elif button_name == 'submitModify':
                # DNA提取实验次数
                DNA_extraction_num = request.POST.get('DNA_extraction_num')
                models.DNAExtractInfo.objects.filter(sam_code_num=sam_code_num,
                                                     ExperimentTimes=DNA_extraction_num).update(
                    # DNA提取信息
                    DNA_Concentration=DNA_Concentration,  # DNA浓度(ng/µL)
                    DNA_volume=DNA_volume,  # DNA体积(µL)
                    DNA_Total=DNA_Total,  # DNA总量(ng)
                    Quality_inspection_method=Quality_inspection_method,  # 质检方法
                    Quality_inspection_result=Quality_inspection_result,  # 质检结果
                    Quality_inspection_volume=Quality_inspection_volume,  # 质检使用体积(µL)
                    Residual_volume=Residual_volume,  # 剩余体积(µL)
                    Extraction_kit_type=Extraction_kit_type,  # 提取试剂盒类型
                    DNA_extraction_people=DNA_extraction_people,  # DNA提取人
                    DNA_extraction_time=DNA_extraction_time,  # 提取时间
                    DNA_extraction_remarks=DNA_extraction_remarks,  # 其它（备注）
                )

            # 从数据里取出所有数据
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            temp_not_Pretreatment = models.clinicalSampleInfo.objects.filter(Next_TaskProgress_Sign=1,
                                                                             TissueSampleSign=1,
                                                                             DNAExtract_Sign=0)  # 任务已分配信息
            temp_Pretreatment = models.clinicalSamplePretreatment.objects.filter(DNAExtract_Sign=0,
                                                                                 Next_TaskProgress_Sign=1)  # 任务已分配信息
            temp_DNAExtractTask = chain(temp_not_Pretreatment, temp_Pretreatment)  # 合并所有数据表数据
            Pending_audit = models.DNAExtractInfo.objects.all()  # 所有已完成DNA提取数据信息

            return render(request, "modelspage/DNAExtractTaskReview.html",
                          {"userinfo": temp, "data": temp_DNAExtractTask, "Pending_audit": Pending_audit,
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

# DNA提取数据待审核详情页
def DNAExtractTask_ShowData (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        sam_code_num = ''
        DNA_extraction_num = ''
        button_name = ''
        if request.method == "POST":
            print '患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号: ', sam_code_num
            # DNA提取实验次数
            DNA_extraction_num = request.POST.get('DNA_extraction_num')
            print 'DNA提取实验次数: ', DNA_extraction_num

            # 判断哪个按钮提交的数据
            if request.POST.has_key('seeInfo'):
                button_name = 'seeInfo'
            elif request.POST.has_key('ModifyData'):
                button_name = 'ModifyData'
            elif request.POST.has_key('delete'):
                temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                    username=username)  # 用户操作权限信息
                # print 'ClinicalSampleRegistration: ', temp_UserOperationPermissionsInfo.ClinicalSampleRegistration
                if temp_UserOperationPermissionsInfo.DNAExtractTaskReview == '1':
                    models.DNAExtractInfo.objects.filter(sam_code_num=sam_code_num,
                                                         ExperimentTimes=DNA_extraction_num).delete()
                    # 从数据里取出所有数据
                    # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
                    temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                        ReadingState='未读')  # 用户信息
                    num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
                    temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息

                    temp_not_Pretreatment = models.clinicalSampleInfo.objects.filter(Next_TaskProgress_Sign=1,
                                                                                     TissueSampleSign=1,
                                                                                     DNAExtract_Sign=0)  # 任务已分配信息
                    temp_Pretreatment = models.clinicalSamplePretreatment.objects.filter(DNAExtract_Sign=0,
                                                                                         Next_TaskProgress_Sign=1)  # 任务已分配信息
                    temp_DNAExtractTask = chain(temp_not_Pretreatment, temp_Pretreatment)  # 合并所有数据表数据

                    Pending_audit = models.DNAExtractInfo.objects.all()  # 所有已完成DNA提取数据信息

                    return render(request, "modelspage/DNAExtractTaskReview.html",
                                  {"userinfo": temp, "data": temp_DNAExtractTask, "Pending_audit": Pending_audit,
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

        # 从数据里取出某条记录
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_mysql = models.DNAExtractInfo.objects.filter(sam_code_num=sam_code_num, ExperimentTimes=DNA_extraction_num)  # DNA提取样本信息

        if button_name == 'seeInfo':
            return render(request, "modelspage/DNAExtractTask_ShowData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'ModifyData':
            return render(request, "modelspage/DNAExtractTask_ModifyData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
