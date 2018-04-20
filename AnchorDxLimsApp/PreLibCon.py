# encoding: utf-8

from django.shortcuts import render
from AnchorDxLimsApp import models
import time,httplib,datetime
from AnchorDxLimsApp.views import sendEmail
# Create your views here.
#coding:utf-8

from django.shortcuts import render,HttpResponse

# 预文库构建任务列表
def PreLibConTask_Review(request):
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
        temp_PreLibConTask = models.DNAExtractInfo.objects.filter(Next_TaskProgress="预文库构建", Next_TaskProgress_Sign='1',PreLibCon_Sign='0')  # 预文库构建任务信息
        temp_pass = models.PreLibConInfo.objects.all()  # 预文库构建任务已完成

        return render(request, "modelspage/PreLibConTaskReview.html",
                      {"userinfo": temp, "data": temp_PreLibConTask, "pass": temp_pass, "myInfo": temp_myInfo,
                       "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# DNA提取数据录入页
def PreLibConTask_To_Examine (request):
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
        if request.method == "POST":
            print '患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号: ', sam_code_num
            # DNA提取实验次数
            DNA_extraction_num = request.POST.get('DNA_extraction_num')
            print 'DNA提取实验次数: ', DNA_extraction_num

        # 从数据里取出某条记录
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_mysql = models.DNAExtractInfo.objects.filter(sam_code_num=sam_code_num,
                                                          ExperimentTimes=DNA_extraction_num)  # DNA提取样本信息

        return render(request, "modelspage/PreLibConTask_submit.html",
                      {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# DNA提取数据录入到数据库
def PreLibConInfoToDataBases(request):
    # 样本信息
    sam_code_num = ''  # 样本条码号
    ExperimentNumber = ''  # 实验编号
    DNA_extraction_num = '' # DNA提取实验次数
    # 预文库构建信息
    DNA_Concentration = ''  # 预文库浓度(ng/µL)
    DNA_volume = ''  # DNA体积(µL)
    DNA_Total = ''  # DNA总量(ng)
    Indexi5i7 = ''  # Indexi5i7
    Quality_inspection_method = ''   # 质检方法
    Quality_inspection_result = ''    # 质检结果
    Quality_inspection_volume = ''  # 质检使用体积(µL)
    Quality_inspection_mass = ''  # 质检使用质量(ng)
    Residual_volume = ''  # 剩余体积(µL)
    Residual_mass = ''  # 剩余质量(ng)
    Build_lib_method = ''   # 建库方法（可选Batman、Ironman）
    Build_lib_man = ''   # 建库人
    Build_lib_time = ''  # 建库时间（系统默认时间）
    Build_lib_remarks = ''   # 其它（备注）
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

        print 'DNA提取信息: ============================================= '

        # 预文库浓度
        DNA_Concentration = request.POST.get('DNA_Concentration')
        print '预文库浓度: ', DNA_Concentration

        # DNA体积
        DNA_volume = request.POST.get('DNA_volume')
        print 'DNA体积: ', DNA_volume

        # DNA总量
        DNA_Total = request.POST.get('DNA_Total')
        print 'DNA总量: ', DNA_Total

        # Indexi5i7
        Indexi5i7 = request.POST.get('Indexi5i7')
        print 'Indexi5i7: ', Indexi5i7

        # 质检方法
        Quality_inspection_method = request.POST.get('Quality_inspection_method')
        print '质检方法: ', Quality_inspection_method

        # 质检结果
        Quality_inspection_result = request.POST.get('Quality_inspection_result')
        print '质检结果: ', Quality_inspection_result

        # 质检使用体积
        Quality_inspection_volume = request.POST.get('Quality_inspection_volume')
        print '质检使用体积: ', Quality_inspection_volume

        # 质检使用质量
        Quality_inspection_mass = request.POST.get('Quality_inspection_mass')
        print '质检使用质量: ', Quality_inspection_mass

        # 剩余体积
        Residual_volume = request.POST.get('Residual_volume')
        print '剩余体积: ', Residual_volume

        # 剩余质量
        Residual_mass = request.POST.get('Residual_mass')
        print '剩余质量: ', Residual_mass

        # 建库方法
        Build_lib_method = request.POST.get('Build_lib_method')
        print '建库方法: ', Build_lib_method

        # 建库人
        Build_lib_man = request.POST.get('Build_lib_man')
        print '建库人: ', Build_lib_man

        # 建库时间
        Build_lib_time = request.POST.get('Build_lib_time')
        print '建库时间: ', Build_lib_time

        # 其它（备注）
        Build_lib_remarks = request.POST.get('Build_lib_remarks')
        print '其它（备注）: ', Build_lib_remarks

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
        print '首页，username: ', username, department
        temp = {"username": username, "department": department}

        temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
            username=username)  # 用户操作权限信息
        # print 'ClinicalSampleRegistration: ', temp_UserOperationPermissionsInfo.ClinicalSampleRegistration
        if temp_UserOperationPermissionsInfo.PreLibConTaskReview == '1':
            if button_name == 'Determine':
                temp_PreLibConTask = models.PreLibConInfo.objects.filter(sam_code_num=sam_code_num)  # DNA提取样本信息
                num = len(temp_PreLibConTask)

                # 添加数据到数据库
                models.PreLibConInfo.objects.create(
                    # 用户信息
                    username=username,  # 用户名
                    department=department,  # 部门
                    # 样本信息
                    sam_code_num=sam_code_num,  # 样本条码号
                    ExperimentNumber=ExperimentNumber,  # 实验编号
                    # 预文库构建信息
                    DNA_Concentration=DNA_Concentration,  # 预文库浓度(ng/µL)
                    DNA_volume=DNA_volume,  # DNA体积(µL)
                    DNA_Total=DNA_Total,  # DNA总量(ng)
                    Indexi5i7=Indexi5i7,  # Indexi5i7
                    Quality_inspection_method=Quality_inspection_method,  # 质检方法
                    Quality_inspection_result=Quality_inspection_result,  # 质检结果
                    Quality_inspection_volume=Quality_inspection_volume,  # 质检使用体积(µL)
                    Quality_inspection_mass=Quality_inspection_mass,  # 质检使用质量(ng)
                    Residual_volume=Residual_volume,  # 剩余体积(µL)
                    Residual_mass=Residual_mass,  # 剩余质量(ng)
                    Build_lib_method=Build_lib_method,  # 建库方法（可选Batman、Ironman）
                    Build_lib_man=Build_lib_man,  # 建库人
                    Build_lib_time=Build_lib_time,  # 建库时间（系统默认时间）
                    Build_lib_remarks=Build_lib_remarks,  # 其它（备注）
                    # 其他信息
                    DNA_extraction_num=DNA_extraction_num,  # DNA提取实验次数
                    ExperimentTimes=num+1,  # 预文库构建实验次数
                    FinalLibCon_Sign=0,  # 终文库构建任务标记
                    Next_TaskProgress_Sign=0  # 下一步任务分配标记
                )
                models.DNAExtractInfo.objects.filter(sam_code_num=sam_code_num, Next_TaskProgress='预文库构建',
                                                     ExperimentTimes=DNA_extraction_num).update(PreLibCon_Sign='1')

                # 添加系统消息
                taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                Title = '通知：临检样本终文库构建实验分派任务'  # 系统消息标题
                Message = username + '分派给你一个临检样本终文库构建实验分派任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
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
                # 预文库构建次数
                Build_lib_num = request.POST.get('Build_lib_num')
                models.PreLibConInfo.objects.filter(sam_code_num=sam_code_num, ExperimentTimes=Build_lib_num).update(
                    # 预文库构建信息
                    DNA_Concentration=DNA_Concentration,  # 预文库浓度(ng/µL)
                    DNA_volume=DNA_volume,  # DNA体积(µL)
                    DNA_Total=DNA_Total,  # DNA总量(ng)
                    Indexi5i7=Indexi5i7,  # Indexi5i7
                    Quality_inspection_method=Quality_inspection_method,  # 质检方法
                    Quality_inspection_result=Quality_inspection_result,  # 质检结果
                    Quality_inspection_volume=Quality_inspection_volume,  # 质检使用体积(µL)
                    Quality_inspection_mass=Quality_inspection_mass,  # 质检使用质量(ng)
                    Residual_volume=Residual_volume,  # 剩余体积(µL)
                    Residual_mass=Residual_mass,  # 剩余质量(ng)
                    Build_lib_method=Build_lib_method,  # 建库方法（可选Batman、Ironman）
                    Build_lib_man=Build_lib_man,  # 建库人
                    Build_lib_time=Build_lib_time,  # 建库时间（系统默认时间）
                    Build_lib_remarks=Build_lib_remarks,  # 其它（备注）
                )

            # 从数据里取出所有数据
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            temp_PreLibConTask = models.DNAExtractInfo.objects.filter(Next_TaskProgress="预文库构建", Next_TaskProgress_Sign='1',PreLibCon_Sign='0')  # 预文库构建任务信息
            temp_pass = models.PreLibConInfo.objects.all()  # 预文库构建任务已完成

            return render(request, "modelspage/PreLibConTaskReview.html",
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


# DNA提取数据待审核详情页
def PreLibConTask_ShowData (request):
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
        button_name = ''
        if request.method == "POST":
            print '患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号: ', sam_code_num
            # 预文库构建次数
            Build_lib_num = request.POST.get('Build_lib_num')
            print '预文库构建次数: ', Build_lib_num

            # 判断哪个按钮提交的数据
            if request.POST.has_key('seeInfo'):
                button_name = 'seeInfo'
            elif request.POST.has_key('ModifyData'):
                button_name = 'ModifyData'
            elif request.POST.has_key('delete'):
                temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                    username=username)  # 用户操作权限信息
                # print 'ClinicalSampleRegistration: ', temp_UserOperationPermissionsInfo.ClinicalSampleRegistration
                if temp_UserOperationPermissionsInfo.PreLibConTaskReview == '1':
                    models.PreLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                        ExperimentTimes=Build_lib_num).delete()
                    # 从数据里取出所有数据
                    # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
                    temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                        ReadingState='未读')  # 用户信息
                    num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
                    temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
                    temp_PreLibConTask = models.DNAExtractInfo.objects.filter(Next_TaskProgress="预文库构建",
                                                                              Next_TaskProgress_Sign='1',
                                                                              PreLibCon_Sign='0')  # 预文库构建任务信息
                    temp_pass = models.PreLibConInfo.objects.all()  # 预文库构建任务已完成

                    return render(request, "modelspage/PreLibConTaskReview.html",
                                  {"userinfo": temp, "data": temp_PreLibConTask, "pass": temp_pass,
                                   "myInfo": temp_myInfo,
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
        temp_mysql = models.PreLibConInfo.objects.filter(sam_code_num=sam_code_num, ExperimentTimes=Build_lib_num)  # DNA提取样本信息

        if button_name == 'seeInfo':
            return render(request, "modelspage/PreLibConTask_ShowData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'ModifyData':
            return render(request, "modelspage/PreLibConTask_ModifyData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
