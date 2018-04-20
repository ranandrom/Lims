# encoding: utf-8

from django.shortcuts import render
from AnchorDxLimsApp import models
from django.contrib.auth.models import User
import time,httplib,datetime
from AnchorDxLimsApp.views import sendEmail
# Create your views here.
#coding:utf-8

from django.shortcuts import render,HttpResponse

# 临床样本审核操作页
def sample_To_Examine (request):
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

        # 从数据里取出所有数据
        # temp_mysql = models.clinicalSampleInfo.objects.all()
        # for i in range(0, len(temp_mysql)):
        #     print temp_mysql[i].PatientName
            # temp['sam_code_num'+str(i)] = temp_mysql[i].sam_code_num
            # temp['PatientName'+str(i)] = temp_mysql[i].PatientName
            # temp['treatment_hospital'+str(i)] = temp_mysql[i].treatment_hospital

        # 从数据里取出所有数据
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                             ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)

        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        user = User.objects.get(username=username)
        temp_userlist = User.objects.filter(first_name='财务部', is_active=user.is_active)
        temp_cliuserlist = User.objects.filter(first_name='临检中心', is_active=user.is_active)
        temp_mysql = models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num)
        if temp_mysql[0].TissueSampleSign == '0':
            TissuampleSign = '否'
        else:
            TissuampleSign = '是'

    if request.POST.has_key('seeInfo'):
        return render(request, "modelspage/sample_review_submit.html",
                      {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                       "cliuserlist": temp_cliuserlist, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread, "TissuampleSign": TissuampleSign})
    elif request.POST.has_key('ModifyData'):
        return render(request, "modelspage/sample_review_ModifyData.html",
                      {"userinfo": temp, "data": temp_mysql, "myInfo": temp_myInfo,
                       "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread, "TissueSampleSign": TissuampleSign})
    elif request.POST.has_key('delete'):
        temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
            username=username)  # 用户操作权限信息
        if temp_UserOperationPermissionsInfo.sampleReview == '1':
            models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num).delete()  # 删除信息
            # 从数据里取出所有数据
            if department == '管理员':
                temp_not_audited = models.clinicalSampleInfo.objects.filter(sample_review=0)  # 临床样本未审核信息
            else:
                temp_not_audited = models.clinicalSampleInfo.objects.filter(SampleAuditor=username,
                                                                            sample_review=0)  # 临床样本未审核信息
            # temp_not_audited = models.clinicalSampleInfo.objects.filter(sample_review=0)  # 临床样本未审核信息
            temp_pass = models.clinicalSampleInfo.objects.filter(sample_review=1)  # 临床样本已通过审核信息
            temp_return = models.clinicalSampleInfo.objects.filter(sample_review=4)  # 临床样本已通过审核信息
            temp_Suspend = models.clinicalSampleInfo.objects.filter(sample_review=2)  # 临床样本暂停任务信息
            temp_not_pass = models.clinicalSampleInfo.objects.filter(sample_review=3)  # 临床样本终止任务信息

            return render(request, "modelspage/sample_review.html",
                          {"userinfo": temp, "data": temp_not_audited, "pass": temp_pass, "return": temp_return,
                           "Suspend": temp_Suspend, "Not_pass": temp_not_pass, "myInfo": temp_myInfo,
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

# 临床样本信息审核操作
def sample_Examine_Operation (request):
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
        # print temp_UserOperationPermissionsInfo.sampleReview
        if temp_UserOperationPermissionsInfo.sampleReview == '1':
            button_name = ''  # 按钮名字
            sam_code_num = ''
            # 临床样本审核信息
            ExperimentNumber = ''  # 实验编号
            CollectSamplesDate = ''  # 收样时间
            Review_Time = ''  # 样本审核时间
            Reason = ''  # 不通过理由
            ContractAuditor = ''  # 合同审核人
            TaskAssignment = ''  # 实验任务分派人
            if request.method == "POST":
                print '患者信息: ============================================= '
                # 样本条码号
                sam_code_num = request.POST.get('sam_code_num').strip('HT')
                print '样本条码号: ', sam_code_num

                # 实验编号
                ExperimentNumber = request.POST.get('ExperimentNumber')
                print '实验编号: ', ExperimentNumber

                # 收样时间
                CollectSamplesDate = request.POST.get('CollectSamplesDate')
                print '收样时间: ', CollectSamplesDate

                # 样本审核时间
                Review_Time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print '样本审核时间: ', Review_Time

                # 审核备注
                Reason = request.POST.get('Reason')
                print '审核备注: ', Reason

                ContractAuditor = request.POST.get('ContractAuditor')  # 合同审核人
                TaskAssignment = request.POST.get('TaskAssignment')  # 实验任务分派人
                # print '实验任务分派人: ', TaskAssignment

                # 判断哪个按钮提交的数据
                if request.POST.has_key('pass'):
                    button_name = 'pass'
                elif request.POST.has_key('return'):
                    button_name = 'return'
                elif request.POST.has_key('Suspend'):
                    button_name = 'Suspend'
                elif request.POST.has_key('Not_pass'):
                    button_name = 'Not_pass'
                elif request.POST.has_key('submitModify'):
                    button_name = 'submitModify'

            if button_name == 'pass':
                # 通过审核
                models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num).update(sample_review='1',
                                                                                           ReviewResult='通过',
                                                                                           contract_review='0',
                                                                                           Next_TaskProgress_Sign='0',
                                                                                           ExperimentNumber=ExperimentNumber,
                                                                                           CollectSamplesDate=CollectSamplesDate,
                                                                                           Review_Time=Review_Time,
                                                                                           Reason=Reason,
                                                                                           ContractAuditor=ContractAuditor,
                                                                                           TaskAssignment=TaskAssignment,
                                                                                           SampleAuditor=username,
                                                                                           )

                # 添加系统消息
                taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                Title = '通知：临检样本合同审核任务'  # 系统消息标题
                Message = username + '分派给你一个临检样本合同审核任务！合同编号为：HT' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                models.UserSystemMessage.objects.create(
                    # 用户信息
                    Sender=username,  # 发送者
                    Receiver=ContractAuditor,  # 接收者
                    # 信息内容
                    Time=taskTime,  # 信息生成时间
                    Title=Title,  # 系统消息标题
                    Message=Message,  # 系统消息正文
                    ReadingState='未读',  # 信息阅读状态
                )
                sendEmail(ContractAuditor, Title, Message)  # 发送邮件通知

                Title = '通知：临检样本实验分派任务'  # 系统消息标题
                Message = username + '分派给你一个临检实验分派任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                models.UserSystemMessage.objects.create(
                    # 用户信息
                    Sender=username,  # 发送者
                    Receiver=TaskAssignment,  # 接收者
                    # 信息内容
                    Time=taskTime,  # 信息生成时间
                    Title=Title,  # 系统消息标题
                    Message=Message,
                    ReadingState='未读',  # 信息阅读状态
                )
                sendEmail(TaskAssignment, Title, Message)  # 发送邮件通知

            elif button_name == 'return':
                temp_data = models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num)
                if not temp_data[0].Next_TaskProgress_Sign == '1':
                    # 通过审核
                    models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num).update(sample_review='4',
                                                                                               ReviewResult='退回',
                                                                                               ExperimentNumber=ExperimentNumber,
                                                                                               CollectSamplesDate=CollectSamplesDate,
                                                                                               Review_Time=Review_Time,
                                                                                               Reason=Reason,
                                                                                               SampleAuditor=username,
                                                                                               )

                    taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    Title = '通知：临检样本审核退回'  # 系统消息标题
                    Message = username + '在审核你登记的临检样本信息时给你退回一个样本修改登记信息！样本编号为：' + sam_code_num + '。请尽快完成修改！'  # 系统邮件正文
                    Receiver = temp_data[0].username
                    print 'Receiver:', Receiver
                    models.UserSystemMessage.objects.create(
                        # 用户信息
                        Sender=username,  # 发送者
                        Receiver=Receiver,  # 接收者
                        # 信息内容
                        Time=taskTime,  # 信息生成时间
                        Title=Title,  # 系统消息标题
                        Message=Message,
                        ReadingState='未读',  # 信息阅读状态
                    )
                    sendEmail(Receiver, Title, Message)  # 发送邮件通知

            elif button_name == 'submitModify':
                print '修改数据'
                temp_data = models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num)
                if not temp_data[0].ContractAuditor == ContractAuditor and temp_data[0].contract_review == '0':
                    # 添加系统消息
                    taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    Title = '通知：临检样本合同审核任务'  # 系统消息标题
                    Message = username + '分派给你一个临检样本合同审核任务！合同编号为：HT' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                    models.UserSystemMessage.objects.create(
                        # 用户信息
                        Sender=username,  # 发送者
                        Receiver=ContractAuditor,  # 接收者
                        # 信息内容
                        Time=taskTime,  # 信息生成时间
                        Title=Title,  # 系统消息标题
                        Message=Message,  # 系统消息正文
                        ReadingState='未读',  # 信息阅读状态
                    )
                    sendEmail(ContractAuditor, Title, Message)  # 发送邮件通知
                if not temp_data[0].TaskAssignment == TaskAssignment and temp_data[0].Next_TaskProgress_Sign == '0':
                    taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    Title = '通知：临检样本实验分派任务'  # 系统消息标题
                    Message = username + '分派给你一个临检实验分派任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                    models.UserSystemMessage.objects.create(
                        # 用户信息
                        Sender=username,  # 发送者
                        Receiver=TaskAssignment,  # 接收者
                        # 信息内容
                        Time=taskTime,  # 信息生成时间
                        Title=Title,  # 系统消息标题
                        Message=Message,
                        ReadingState='未读',  # 信息阅读状态
                    )
                    sendEmail(TaskAssignment, Title, Message)  # 发送邮件通知

                # 更新数据
                models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num).update(ExperimentNumber=ExperimentNumber,
                                                                                           CollectSamplesDate=CollectSamplesDate,
                                                                                           Reason=Reason,
                                                                                           ContractAuditor=ContractAuditor,
                                                                                           TaskAssignment=TaskAssignment,
                                                                                           )
            elif button_name == 'Suspend':
                print '暂停任务'
                temp_data = models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num)
                if not temp_data[0].Next_TaskProgress_Sign == '1':
                    # 暂停任务
                    models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num).update(sample_review='2',
                                                                                               ReviewResult='暂停',
                                                                                               ExperimentNumber=ExperimentNumber,
                                                                                               CollectSamplesDate=CollectSamplesDate,
                                                                                               Review_Time=Review_Time,
                                                                                               Reason=Reason,
                                                                                               SampleAuditor=username,
                                                                                               )
            elif button_name == 'Not_pass':
                print '终止任务'
                temp_data = models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num)
                if not temp_data[0].Next_TaskProgress_Sign == '1':
                    # 终止任务
                    models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num).update(sample_review='3',
                                                                                               ReviewResult='终止',
                                                                                               ExperimentNumber=ExperimentNumber,
                                                                                               CollectSamplesDate=CollectSamplesDate,
                                                                                               Review_Time=Review_Time,
                                                                                               Reason=Reason,
                                                                                               SampleAuditor=username,
                                                                                               )

            # 从数据里取出所有数据
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            if department == '管理员':
                temp_not_audited = models.clinicalSampleInfo.objects.filter(sample_review=0)  # 临床样本未审核信息
            else:
                temp_not_audited = models.clinicalSampleInfo.objects.filter(SampleAuditor=username,
                                                                            sample_review=0)  # 临床样本未审核信息
            # temp_not_audited = models.clinicalSampleInfo.objects.filter(sample_review=0)  # 临床样本未审核信息
            temp_pass = models.clinicalSampleInfo.objects.filter(sample_review=1)  # 临床样本已通过审核信息
            temp_return = models.clinicalSampleInfo.objects.filter(sample_review=4)  # 临床样本已通过审核信息
            temp_Suspend = models.clinicalSampleInfo.objects.filter(sample_review=2)  # 临床样本暂停任务信息
            temp_not_pass = models.clinicalSampleInfo.objects.filter(sample_review=3)  # 临床样本终止任务信息

            return render(request, "modelspage/sample_review.html",
                          {"userinfo": temp, "data": temp_not_audited, "pass": temp_pass, "return": temp_return,
                           "Suspend": temp_Suspend, "Not_pass": temp_not_pass, "myInfo": temp_myInfo,
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

# 临床样本已通过审核信息详情页
def sample_To_Examine_Pass (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        sam_code_num = ''
        button_name = ''
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)

        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        if request.method == "POST":
            print 'Pass患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('pass_sam_code_num')
            print 'Pass样本条码号: ', sam_code_num
            # 判断哪个按钮提交的数据
            if request.POST.has_key('pass'):
                button_name = 'pass'
            elif request.POST.has_key('return'):
                button_name = 'return'
            elif request.POST.has_key('ModifyData'):
                button_name = 'ModifyData'
            elif request.POST.has_key('delete'):
                temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                    username=username)  # 用户操作权限信息
                if temp_UserOperationPermissionsInfo.sampleReview == '1':
                    models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num).delete()  # 删除信息
                    # 从数据里取出所有数据
                    temp_not_audited = models.clinicalSampleInfo.objects.filter(sample_review=0)  # 临床样本未审核信息
                    temp_pass = models.clinicalSampleInfo.objects.filter(sample_review=1)  # 临床样本已通过审核信息
                    temp_return = models.clinicalSampleInfo.objects.filter(sample_review=4)  # 临床样本已通过审核信息
                    temp_Suspend = models.clinicalSampleInfo.objects.filter(sample_review=2)  # 临床样本暂停任务信息
                    temp_not_pass = models.clinicalSampleInfo.objects.filter(sample_review=3)  # 临床样本终止任务信息

                    return render(request, "modelspage/sample_review.html",
                                  {"userinfo": temp, "data": temp_not_audited, "pass": temp_pass, "return": temp_return,
                                   "Suspend": temp_Suspend, "Not_pass": temp_not_pass, "myInfo": temp_myInfo,
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
        temp_mysql = models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num)
        if temp_mysql[0].TissueSampleSign == '0':
            TissuampleSign = '否'
        else:
            TissuampleSign = '是'

        if button_name == 'pass':
            return render(request, "modelspage/clinicalSampleInfoPassInfo.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread, "TissuampleSign": TissuampleSign})
        elif button_name == 'return':
            return render(request, "modelspage/clinicalSampleInfoReturnInfo.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "TissuampleSign": TissuampleSign, "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'ModifyData':
            user = User.objects.get(username=username)
            temp_userlist = User.objects.filter(first_name='财务部', is_active=user.is_active)
            temp_cliuserlist = User.objects.filter(first_name='临检中心', is_active=user.is_active)
            return render(request, "modelspage/clinicalSampleInfoModifyReviewInfo.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                           "cliuserlist": temp_cliuserlist, "TissuampleSign": TissuampleSign,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 临床样本暂停任务信息详情页
def sample_To_Examine_Suspend (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        sam_code_num = ''
        button_name = ''
        # 从数据里取出某条记录
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        if request.method == "POST":
            print 'Pass患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print 'Pass样本条码号: ', sam_code_num

            # 判断哪个按钮提交的数据
            if request.POST.has_key('Stop'):
                button_name = 'Stop'
            elif request.POST.has_key('ModifyData'):
                button_name = 'ModifyData'
            elif request.POST.has_key('delete'):
                temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                    username=username)  # 用户操作权限信息
                if temp_UserOperationPermissionsInfo.sampleReview == '1':
                    models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num).delete()  # 删除信息
                    # 从数据里取出所有数据
                    if department == '管理员':
                        temp_not_audited = models.clinicalSampleInfo.objects.filter(sample_review=0)  # 临床样本未审核信息
                    else:
                        temp_not_audited = models.clinicalSampleInfo.objects.filter(SampleAuditor=username,
                                                                                    sample_review=0)  # 临床样本未审核信息
                    # temp_not_audited = models.clinicalSampleInfo.objects.filter(sample_review=0)  # 临床样本未审核信息
                    temp_pass = models.clinicalSampleInfo.objects.filter(sample_review=1)  # 临床样本已通过审核信息
                    temp_return = models.clinicalSampleInfo.objects.filter(sample_review=4)  # 临床样本已通过审核信息
                    temp_Suspend = models.clinicalSampleInfo.objects.filter(sample_review=2)  # 临床样本暂停任务信息
                    temp_not_pass = models.clinicalSampleInfo.objects.filter(sample_review=3)  # 临床样本终止任务信息

                    return render(request, "modelspage/sample_review.html",
                                  {"userinfo": temp, "data": temp_not_audited, "pass": temp_pass, "return": temp_return,
                                   "Suspend": temp_Suspend, "Not_pass": temp_not_pass, "myInfo": temp_myInfo,
                                   "SystemMessage": temp_SystemMessage_Unread,
                                   "num_SystemMessage_Unread": num_SystemMessage_Unread})

        temp_mysql = models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num)
        if temp_mysql[0].TissueSampleSign == '0':
            TissuampleSign = '否'
        else:
            TissuampleSign = '是'

        if button_name == 'Stop':
            return render(request, "modelspage/clinicalSampleInfoSuspendInfo.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread, "TissuampleSign": TissuampleSign})

        elif button_name == 'ModifyData':
            user = User.objects.get(username=username)
            temp_userlist = User.objects.filter(first_name='财务部', is_active=user.is_active)
            temp_cliuserlist = User.objects.filter(first_name='临检中心', is_active=user.is_active)
            return render(request, "modelspage/clinicalSampleInfoModifyReviewInfo.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                           "cliuserlist": temp_cliuserlist,
                           "TissuampleSign": TissuampleSign, "SystemMessage": temp_SystemMessage_Unread,
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
        # print temp_UserOperationPermissionsInfo.sampleReview
        if temp_UserOperationPermissionsInfo.sampleReview == '1':
            sam_code_num = ''
            if request.method == "POST":
                print '患者信息: ============================================= '
                # 样本条码号
                sam_code_num = request.POST.get('sam_code_num').strip('HT')
                print '样本条码号: ', sam_code_num

            models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num).update(sample_review='0')

            # 从数据里取出所有数据
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            if department == '管理员':
                temp_not_audited = models.clinicalSampleInfo.objects.filter(sample_review=0)  # 临床样本未审核信息
            else:
                temp_not_audited = models.clinicalSampleInfo.objects.filter(SampleAuditor=username,
                                                                            sample_review=0)  # 临床样本未审核信息
            # temp_not_audited = models.clinicalSampleInfo.objects.filter(sample_review=0)  # 临床样本未审核信息
            temp_pass = models.clinicalSampleInfo.objects.filter(sample_review=1)  # 临床样本已通过审核信息
            temp_return = models.clinicalSampleInfo.objects.filter(sample_review=4)  # 临床样本已通过审核信息
            temp_Suspend = models.clinicalSampleInfo.objects.filter(sample_review=2)  # 临床样本暂停任务信息
            temp_not_pass = models.clinicalSampleInfo.objects.filter(sample_review=3)  # 临床样本终止任务信息

            return render(request, "modelspage/sample_review.html",
                          {"userinfo": temp, "data": temp_not_audited, "pass": temp_pass, "return": temp_return,
                           "Suspend": temp_Suspend, "Not_pass": temp_not_pass, "myInfo": temp_myInfo,
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

# 临床样本不通过审核信息详情页
def sample_To_Examine_Not_Pass (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        sam_code_num = ''
        button_name = ''
        # 从数据里取出某条记录
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        if request.method == "POST":
            print 'Pass患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print 'Pass样本条码号: ', sam_code_num

            # 判断哪个按钮提交的数据
            if request.POST.has_key('Not_pass'):
                button_name = 'Not_pass'
            elif request.POST.has_key('ModifyData'):
                button_name = 'ModifyData'
            elif request.POST.has_key('delete'):
                temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                    username=username)  # 用户操作权限信息
                if temp_UserOperationPermissionsInfo.sampleReview == '1':
                    models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num).delete()  # 删除信息
                    # 从数据里取出所有数据
                    if department == '管理员':
                        temp_not_audited = models.clinicalSampleInfo.objects.filter(sample_review=0)  # 临床样本未审核信息
                    else:
                        temp_not_audited = models.clinicalSampleInfo.objects.filter(SampleAuditor=username,
                                                                                    sample_review=0)  # 临床样本未审核信息
                    # temp_not_audited = models.clinicalSampleInfo.objects.filter(sample_review=0)  # 临床样本未审核信息
                    temp_pass = models.clinicalSampleInfo.objects.filter(sample_review=1)  # 临床样本已通过审核信息
                    temp_return = models.clinicalSampleInfo.objects.filter(sample_review=4)  # 临床样本已通过审核信息
                    temp_Suspend = models.clinicalSampleInfo.objects.filter(sample_review=2)  # 临床样本暂停任务信息
                    temp_not_pass = models.clinicalSampleInfo.objects.filter(sample_review=3)  # 临床样本终止任务信息

                    return render(request, "modelspage/sample_review.html",
                                  {"userinfo": temp, "data": temp_not_audited, "pass": temp_pass, "return": temp_return,
                                   "Suspend": temp_Suspend, "Not_pass": temp_not_pass, "myInfo": temp_myInfo,
                                   "SystemMessage": temp_SystemMessage_Unread,
                                   "num_SystemMessage_Unread": num_SystemMessage_Unread})

        temp_mysql = models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num)
        if temp_mysql[0].TissueSampleSign == '0':
            TissuampleSign = '否'
        else:
            TissuampleSign = '是'

        if button_name == 'Not_pass':
            return render(request, "modelspage/clinicalSampleInfoNotPassInfo.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread, "TissuampleSign": TissuampleSign})

        elif button_name == 'ModifyData':
            user = User.objects.get(username=username)
            temp_userlist = User.objects.filter(first_name='财务部', is_active=user.is_active)
            temp_cliuserlist = User.objects.filter(first_name='临检中心', is_active=user.is_active)
            return render(request, "modelspage/clinicalSampleInfoModifyReviewInfo.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                           "cliuserlist": temp_cliuserlist, "TissuampleSign": TissuampleSign,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
