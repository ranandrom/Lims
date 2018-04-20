# encoding: utf-8

from django.shortcuts import render
from AnchorDxLimsApp import models
from django.contrib.auth.models import User
import time,httplib,datetime
from AnchorDxLimsApp.views import sendEmail
# Create your views here.
#coding:utf-8

from django.shortcuts import render,HttpResponse

# 预处理任务列表
def RandDPretreatmentInfoInputHomePage(request):
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
        temp_PretreatmentTask = models.RandDSampleInfo.objects.filter(Pretreatment_Sign=0, Next_TaskProgress_Sign='1',
                                                                      TissueSampleSign=0)  # 预处理样本信息
        Pending_audit = models.RandDSamplePretreatmentInfo.objects.all()  # 所有已完成预处理数据信息

        return render(request, "modelspage/RandDPretreatmentInfoInputHomePage.html",
                      {"userinfo": temp, "data": temp_PretreatmentTask, "Pending_audit": Pending_audit,
                       "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 预处理数据录入页
def RandDPretreatmentInfoInput (request):
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
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号: ', sam_code_num

        # 从数据里取出某条记录
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_mysql = models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num)

        return render(request, "modelspage/RandDPretreatmentInfoInput.html",
                      {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 预处理数据录入到数据库
def RandDPretreatmentInfoToDataBases(request):
    # 样本信息
    sam_code_num = ''  # 样本条码号
    # 样本预处理信息
    Plasma_volume = ''  # 血浆总体积(mL)
    Division_Tube_Number = ''  # 分装管数
    number_of_white_blood_cells = ''  # 白细胞分离管数
    isHemolysis = ''  # 是否溶血
    isFatBlood = ''  # 是否脂血
    Type_of_blood_vessel = ''  # 采血管类型
    Blood_sharing_time = ''  # 分血时间
    Pretreatment_remarks = ''  # 其它（备注）
    button_name = ''  # 按钮名字
    if request.method == "POST":
        print '样本信息: ============================================= '
        # 样本条码号
        sam_code_num = request.POST.get('sam_code_num')

        print '样本预处理信息: ============================================= '
        Plasma_volume = request.POST.get('Plasma_volume')  # 血浆总体积(mL)
        Division_Tube_Number = request.POST.get('Division_Tube_Number')  # 分装管数
        number_of_white_blood_cells = request.POST.get('number_of_white_blood_cells')  # 白细胞分离管数
        isHemolysis = request.POST.get('isHemolysis')  # 是否溶血
        isFatBlood = request.POST.get('isFatBlood')   # 是否脂血
        Type_of_blood_vessel = request.POST.get('Type_of_blood_vessel')   # 采血管类型
        Blood_sharing_time = request.POST.get('Blood_sharing_time')  # 分血时间
        Pretreatment_remarks = request.POST.get('Pretreatment_remarks')  # 其它（备注）

        # 判断哪个按钮提交的数据
        if request.POST.has_key('Determine'):
            button_name = 'Determine'
        elif request.POST.has_key('submitModify'):
            button_name = 'submitModify'

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
        if temp_UserOperationPermissionsInfo.RandDPretreatmentInfoInputHomePage == '1':
            if button_name == 'Determine':
                # 添加数据到数据库
                models.RandDSamplePretreatmentInfo.objects.create(
                    # 用户信息
                    username=username,  # 用户名
                    department=department,  # 部门
                    # 样本信息
                    sam_code_num=sam_code_num,  # 样本条码号
                    # 样本预处理信息
                    Plasma_volume=Plasma_volume,  # 血浆总体积(mL)
                    Division_Tube_Number=Division_Tube_Number,  # 分装管数
                    number_of_white_blood_cells=number_of_white_blood_cells,  # 白细胞分离管数
                    isHemolysis=isHemolysis,  # 是否溶血
                    isFatBlood=isFatBlood,  # 是否脂血
                    Type_of_blood_vessel=Type_of_blood_vessel,  # 采血管类型
                    Blood_sharing_time=Blood_sharing_time,  # 分血时间
                    Pretreatment_remarks=Pretreatment_remarks,  # 其它（备注）
                    # 其他信息
                    Next_TaskProgress_Sign=0,  # 审核标志
                    Next_TaskProgress="样本预处理",  # 任务进度
                    DNAExtract_Sign=0,  # DNA提取任务标记
                )
                models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(Pretreatment_Sign=1)

                # 添加系统消息
                taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                Title = '通知：研发样本DNA提取实验分派任务'  # 系统消息标题
                Message = username + '分派给你一个研发样本DNA提取实验分派任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
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
                # 添加数据到数据库
                models.RandDSamplePretreatmentInfo.objects.filter(sam_code_num=sam_code_num).update(
                    # 样本预处理信息
                    Plasma_volume=Plasma_volume,  # 血浆总体积(mL)
                    Division_Tube_Number=Division_Tube_Number,  # 分装管数
                    number_of_white_blood_cells=number_of_white_blood_cells,  # 白细胞分离管数
                    isHemolysis=isHemolysis,  # 是否溶血
                    isFatBlood=isFatBlood,  # 是否脂血
                    Type_of_blood_vessel=Type_of_blood_vessel,  # 采血管类型
                    Blood_sharing_time=Blood_sharing_time,  # 分血时间
                    Pretreatment_remarks=Pretreatment_remarks,  # 其它（备注）
                )

            # 从数据里取出所有数据
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            temp_PretreatmentTask = models.RandDSampleInfo.objects.filter(Pretreatment_Sign=0,
                                                                          Next_TaskProgress_Sign='1',
                                                                          TissueSampleSign=0)  # 样本预处理信息
            Pending_audit = models.RandDSamplePretreatmentInfo.objects.all()  # 所有已完预处理数据信息

            return render(request, "modelspage/RandDPretreatmentInfoInputHomePage.html",
                          {"userinfo": temp, "data": temp_PretreatmentTask, "Pending_audit": Pending_audit,
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
def RandDPretreatmentInfoShowData (request):
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
        button_name = ''
        if request.method == "POST":
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')

            # 判断哪个按钮提交的数据
            if request.POST.has_key('Pretreatment_audited'):
                button_name = 'Pretreatment_audited'
            elif request.POST.has_key('ModifyData'):
                button_name = 'ModifyData'
            elif request.POST.has_key('delete'):
                temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                    username=username)  # 用户操作权限信息
                # print 'ClinicalSampleRegistration: ', temp_UserOperationPermissionsInfo.ClinicalSampleRegistration
                if temp_UserOperationPermissionsInfo.RandDPretreatmentInfoInputHomePage == '1':
                    models.RandDSamplePretreatmentInfo.objects.filter(sam_code_num=sam_code_num).delete()
                    temp_PretreatmentTask = models.RandDSampleInfo.objects.filter(
                        Pretreatment_Sign=0,
                        Next_TaskProgress_Sign='1',
                        TissueSampleSign=0)  # 预处理样本信息
                    Pending_audit = models.RandDSamplePretreatmentInfo.objects.all()  # 所有已完成预处理数据信息
                    return render(request, "modelspage/RandDPretreatmentInfoInputHomePage.html",
                                  {"userinfo": temp, "data": temp_PretreatmentTask, "Pending_audit": Pending_audit,
                                   "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                                   "num_SystemMessage_Unread": num_SystemMessage_Unread})
                else:
                    return render(request, "modelspage/PermissionsPrompt.html",
                                  {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                                   "num_SystemMessage_Unread": num_SystemMessage_Unread})

        temp_mysql = models.RandDSamplePretreatmentInfo.objects.filter(sam_code_num=sam_code_num)  # 样本预处理信息

        if button_name == 'Pretreatment_audited':
            return render(request, "modelspage/RandDSamplePretreatmentInfoShowData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'ModifyData':
            return render(request, "modelspage/RandDPretreatmentInfoModifyData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
