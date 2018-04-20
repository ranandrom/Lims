# encoding: utf-8

from django.shortcuts import render
from AnchorDxLimsApp import models
import time,httplib,datetime
from AnchorDxLimsApp.views import sendEmail
# Create your views here.
#coding:utf-8

from django.shortcuts import render,HttpResponse

# 终文库构建任务列表
def RandDFinLibConInfoInputHomePage(request):
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
        temp_PreLibConTask = models.RandDSamplePreLibConInfo.objects.filter(Next_TaskProgress="终文库构建",
                                                                            Next_TaskProgress_Sign='1',
                                                                            FinalLibCon_Sign='0')  # 终文库构建任务信息
        temp_pass = models.RandDSampleFinLibConInfo.objects.all()  # 终文库构建任务已完成

        return render(request, "modelspage/RandDFinLibConInfoInputHomePage.html",
                      {"userinfo": temp, "data": temp_PreLibConTask, "pass": temp_pass, "myInfo": temp_myInfo,
                       "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 终文库构建数据录入页
def RandDFinLibConInfoInput (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        sam_code_num = ''
        Build_lib_num = ''
        if request.method == "POST":
            print '患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号: ', sam_code_num
            # 预文库构建实验次数
            Build_lib_num = request.POST.get('Build_lib_num')
            print '预文库构建实验次数: ', Build_lib_num

        # 从数据里取出某条记录
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_mysql = models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                         ExperimentTimes=Build_lib_num)  # 预文库构建实验次数

        return render(request, "modelspage/RandDFinLibConInfoInput.html",
                      {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                       "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 终文库构建数据录入到数据库
def RandDFinLibConInfoToDataBases(request):
    # 样本信息
    sam_code_num = ''  # 样本条码号
    DNA_extraction_num = '' # DNA提取实验次数
    PreLibCon_Build_lib_num = '' # 预文库构建实验次数
    # 终文库构建信息
    PreLibConName = ''  # 预文库名称
    PoolInternalLibNumber = ''  # Pool内文库数目
    FinLibConName = ''  # 终文库名称
    DNA_Concentration = ''  # 浓度(ng/µL)
    DNA_volume = ''  # 体积(µL)
    DNA_Total = ''  # DNA总量(ng)
    Indexi5i7 = ''  # Indexi5i7
    Panel = ''  # 捕获panel
    Build_lib_time = ''  # 建库时间
    FinLibCon_storage_location = ''  # 终文库存储位置
    Build_lib_man = ''  # 建库人
    SequencingInfo = ''  # Sequencing Info
    Build_lib_remarks = ''  # 其它（备注）
    button_name = ''  # 按钮名字
    if request.method == "POST":
        print '样本信息: ============================================= '
        sam_code_num = request.POST.get('sam_code_num')   # 样本条码号
        print '样本条码号: ', sam_code_num
        DNA_extraction_num = request.POST.get('DNA_extraction_num')     # DNA提取实验次数
        PreLibCon_Build_lib_num = request.POST.get('PreLibCon_Build_lib_num')  # 预文库构建实验次数

        print '终文库构建信息: ============================================= '
        PreLibConName = request.POST.get('PreLibConName')  # 预文库名称
        PoolInternalLibNumber = request.POST.get('PoolInternalLibNumber')  # Pool内文库数目
        FinLibConName = request.POST.get('FinLibConName')  # 终文库名称
        DNA_Concentration = request.POST.get('DNA_Concentration')  # 浓度(ng/µL)
        DNA_volume = request.POST.get('DNA_volume')  # 体积(µL)
        DNA_Total = request.POST.get('DNA_Total')  # DNA总量(ng)
        Indexi5i7 = request.POST.get('Indexi5i7')  # Indexi5i7
        Panel = request.POST.get('Panel')  # 捕获panel
        Build_lib_time = request.POST.get('Build_lib_time')  # 建库时间
        FinLibCon_storage_location = request.POST.get('FinLibCon_storage_location')  # 终文库存储位置
        Build_lib_man = request.POST.get('Build_lib_man')  # 建库人
        SequencingInfo = request.POST.get('SequencingInfo')  # Sequencing Info
        Build_lib_remarks = request.POST.get('Build_lib_remarks')  # 其它（备注）

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
        if temp_UserOperationPermissionsInfo.RandDFinLibConInfoInputHomePage == '1':
            if button_name == 'Determine':
                temp_FinLibConTask = models.RandDSampleFinLibConInfo.objects.filter(sam_code_num=sam_code_num)
                num = len(temp_FinLibConTask)

                # 添加数据到数据库
                models.RandDSampleFinLibConInfo.objects.create(
                    # 用户信息
                    username=username,  # 用户名
                    department=department,  # 部门
                    # 样本信息
                    sam_code_num=sam_code_num,  # 样本条码号
                    # 终文库构建信息
                    PreLibConName=PreLibConName,  # 预文库名称
                    PoolInternalLibNumber=PoolInternalLibNumber,  # Pool内文库数目
                    FinLibConName=FinLibConName,  # 终文库名称
                    DNA_Concentration=DNA_Concentration,  # 浓度(ng/µL)
                    DNA_volume=DNA_volume,  # 体积(µL)
                    DNA_Total=DNA_Total,  # DNA总量(ng)
                    Indexi5i7=Indexi5i7,  # Indexi5i7
                    Panel=Panel,  # 捕获panel
                    Build_lib_time=Build_lib_time,  # 建库时间
                    FinLibCon_storage_location=FinLibCon_storage_location,  # 终文库存储位置
                    Build_lib_man=Build_lib_man,  # 建库人
                    SequencingInfo=SequencingInfo,  # Sequencing Info
                    Build_lib_remarks=Build_lib_remarks,  # 其它（备注）
                    # 其他信息
                    DNA_extraction_num=DNA_extraction_num,  # DNA提取实验次数
                    Build_Prelib_num=PreLibCon_Build_lib_num,  # 预文库构建实验次数
                    ExperimentTimes=num+1,  # 终文库构建实验次数
                    ComputerSeq_Sign=0,  # 上机测序任务标记
                    Next_TaskProgress_Sign=0  # 下一步任务分配标记
                )
                models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num, Next_TaskProgress="终文库构建",
                                                    ExperimentTimes=PreLibCon_Build_lib_num).update(FinalLibCon_Sign='1')  # 终文库构建任务信息

                # 添加系统消息
                taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                Title = '通知：研发样本上机测序实验分派任务'  # 系统消息标题
                Message = username + '分派给你一个研发样本上机测序实验分派任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                sample = models.RandDSampleInfo.objects.get(sam_code_num=sam_code_num)
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
                # 终文库构建次数
                Build_finlib_num = request.POST.get('Build_finlib_num')
                models.RandDSampleFinLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                               ExperimentTimes=Build_finlib_num).update(
                    # 终文库构建信息
                    PreLibConName=PreLibConName,  # 预文库名称
                    PoolInternalLibNumber=PoolInternalLibNumber,  # Pool内文库数目
                    FinLibConName=FinLibConName,  # 终文库名称
                    DNA_Concentration=DNA_Concentration,  # 浓度(ng/µL)
                    DNA_volume=DNA_volume,  # 体积(µL)
                    DNA_Total=DNA_Total,  # DNA总量(ng)
                    Indexi5i7=Indexi5i7,  # Indexi5i7
                    Panel=Panel,  # 捕获panel
                    Build_lib_time=Build_lib_time,  # 建库时间
                    FinLibCon_storage_location=FinLibCon_storage_location,  # 终文库存储位置
                    Build_lib_man=Build_lib_man,  # 建库人
                    SequencingInfo=SequencingInfo,  # Sequencing Info
                    Build_lib_remarks=Build_lib_remarks,  # 其它（备注）
                )

            # 从数据里取出所有数据
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            temp_PreLibConTask = models.RandDSamplePreLibConInfo.objects.filter(Next_TaskProgress="终文库构建", Next_TaskProgress_Sign='1', FinalLibCon_Sign='0')  # 终文库构建任务信息
            temp_pass = models.RandDSampleFinLibConInfo.objects.all()  # 预文库构建任务已完成

            return render(request, "modelspage/RandDFinLibConInfoInputHomePage.html",
                          {"userinfo": temp, "data": temp_PreLibConTask, "pass": temp_pass, "myInfo": temp_myInfo,
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

# 终文库构建信息详情页
def RandDFinLibConInfoShowData (request):
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

        sam_code_num = ''
        Build_finlib_num = ''
        button_name = ''
        if request.method == "POST":
            print '患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号: ', sam_code_num
            # 终文库构建次数
            Build_finlib_num = request.POST.get('Build_finlib_num')
            print '终文库构建次数: ', Build_finlib_num

            # 判断哪个按钮提交的数据
            if request.POST.has_key('seeInfo'):
                button_name = 'seeInfo'
            elif request.POST.has_key('ModifyData'):
                button_name = 'ModifyData'
            elif request.POST.has_key('delete'):
                temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                    username=username)  # 用户操作权限信息
                # print 'ClinicalSampleRegistration: ', temp_UserOperationPermissionsInfo.ClinicalSampleRegistration
                if temp_UserOperationPermissionsInfo.RandDFinLibConInfoInputHomePage == '1':
                    models.RandDSampleFinLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                   ExperimentTimes=Build_finlib_num).delete()
                    temp_PreLibConTask = models.RandDSamplePreLibConInfo.objects.filter(Next_TaskProgress="终文库构建",
                                                                                        Next_TaskProgress_Sign='1',
                                                                                        FinalLibCon_Sign='0')  # 终文库构建任务信息
                    temp_pass = models.RandDSampleFinLibConInfo.objects.all()  # 终文库构建任务已完成

                    return render(request, "modelspage/RandDFinLibConInfoInputHomePage.html",
                                  {"userinfo": temp, "data": temp_PreLibConTask, "pass": temp_pass, "myInfo": temp_myInfo,
                                   "SystemMessage": temp_SystemMessage_Unread,
                                   "num_SystemMessage_Unread": num_SystemMessage_Unread})
                else:
                    return render(request, "modelspage/PermissionsPrompt.html",
                                  {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                                   "num_SystemMessage_Unread": num_SystemMessage_Unread})

        temp_mysql = models.RandDSampleFinLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                    ExperimentTimes=Build_finlib_num)  # 终文库构建信息

        if button_name == 'seeInfo':
            return render(request, "modelspage/RandDFinLibConInfoShowData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'ModifyData':
            return render(request, "modelspage/RandDFinLibConInfoModifyData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
