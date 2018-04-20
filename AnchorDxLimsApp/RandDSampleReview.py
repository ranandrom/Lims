# encoding: utf-8

from django.shortcuts import render
from AnchorDxLimsApp import models
import time,httplib,datetime
from django.contrib.auth.models import User
from AnchorDxLimsApp.views import sendEmail
from itertools import chain
# Create your views here.
#coding:utf-8

from django.shortcuts import render,HttpResponse

# 研发样本审核首页
def RandDSampleReviewHomePage(request):
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
        temp_not_audited = models.RandDSampleInfo.objects.filter(sample_review=0)  # 研发样本未审核信息
        temp_pass = models.RandDSampleInfo.objects.filter(sample_review=1)  # 研发样本已通过审核信息
        temp_return = models.RandDSampleInfo.objects.filter(sample_review=4)  # 研发审核退回样本信息
        temp_Suspend = models.RandDSampleInfo.objects.filter(sample_review=2)  # 研发样本暂停任务信息
        temp_not_pass = models.RandDSampleInfo.objects.filter(sample_review=3)  # 研发样本终止任务信息

        return render(request, "modelspage/RandD_Sample_ReviewHomePage.html",
                      {"userinfo": temp, "data": temp_not_audited, "pass": temp_pass, "Suspend": temp_Suspend,
                       "Not_pass": temp_not_pass, "myInfo": temp_myInfo, "return": temp_return,
                       "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 研发样本审核页
def RandDSampleReview (request):
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
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_userlist = User.objects.filter(first_name='财务部')
        temp_rnduserlist = User.objects.filter(first_name='研发部')
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_mysql = models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num)

        return render(request, "modelspage/RandDSampleReviewSubmit.html",
                      {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                       "rnduserlist": temp_rnduserlist, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 研发样本信息审核操作
def RandDSampleReviewOperation (request):
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
        if temp_UserOperationPermissionsInfo.RandDSampleReviewHomePage == '1':
            button_name = ''  # 按钮名字
            sam_code_num = ''
            # 研发样本审核信息
            ReviewTime = ''  # 样本审核时间
            ReviewRemarks = ''  # 样本审核备注
            ContractAuditor = ''  # 合同审核人
            TaskAssignment = ''  # 实验任务分派人
            if request.method == "POST":
                # 样本条码号
                sam_code_num = request.POST.get('sam_code_num').strip('HT')
                print '样本条码号: ', sam_code_num

                # 样本审核时间
                ReviewTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print '样本审核时间: ', ReviewTime

                # 审核备注
                ReviewRemarks = request.POST.get('ReviewRemarks')
                print '审核备注: ', ReviewRemarks

                ContractAuditor = request.POST.get('ContractAuditor')  # 合同审核人
                TaskAssignment = request.POST.get('TaskAssignment')  # 实验任务分派人

                # 判断哪个按钮提交的数据
                if request.POST.has_key('pass'):
                    button_name = 'pass'
                elif request.POST.has_key('Suspend'):
                    button_name = 'Suspend'
                elif request.POST.has_key('return'):
                    button_name = 'return'
                elif request.POST.has_key('Not_pass'):
                    button_name = 'Not_pass'
                elif request.POST.has_key('submitModify'):
                    button_name = 'submitModify'

            if button_name == 'pass':
                # 通过审核
                models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(
                    sample_review='1',
                    ReviewResult='通过',
                    Next_TaskProgress_Sign='0',
                    ReviewTime=ReviewTime,
                    ReviewRemarks=ReviewRemarks,
                    SampleAuditor=username,
                    ContractAuditor=ContractAuditor,
                    TaskAssignment=TaskAssignment,
                )

                # # 添加系统消息
                taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # Title = '通知：研发样本合同审核任务'  # 系统消息标题
                # Message = username + '分派给你一个研发样本合同审核任务！样本编号为：HT' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                # models.UserSystemMessage.objects.create(
                #     # 用户信息
                #     Sender=username,  # 发送者
                #     Receiver=ContractAuditor,  # 接收者
                #     # 信息内容
                #     Time=taskTime,  # 信息生成时间
                #     Title=Title,  # 系统消息标题
                #     Message=Message,  # 系统消息正文
                #     ReadingState='未读',  # 信息阅读状态
                # )
                # sendEmail(ContractAuditor, Title, Message)  # 发送邮件通知

                Title = '通知：研发样本实验分派任务'  # 系统消息标题
                Message = username + '分派给你一个研发实验分派任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
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

            elif button_name == 'submitModify':
                print '修改数据'
                temp_data = models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num)
                # if not temp_data[0].ContractAuditor == ContractAuditor and temp_data[0].contract_review == '0':
                #     # 添加系统消息
                #     taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                #     Title = '通知：研发样本合同审核任务'  # 系统消息标题
                #     Message = username + '分派给你一个研发样本合同审核任务！样本编号为：HT' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                #     models.UserSystemMessage.objects.create(
                #         # 用户信息
                #         Sender=username,  # 发送者
                #         Receiver=ContractAuditor,  # 接收者
                #         # 信息内容
                #         Time=taskTime,  # 信息生成时间
                #         Title=Title,  # 系统消息标题
                #         Message=Message,  # 系统消息正文
                #         ReadingState='未读',  # 信息阅读状态
                #     )
                #     sendEmail(ContractAuditor, Title, Message)  # 发送邮件通知
                if not temp_data[0].TaskAssignment == TaskAssignment and temp_data[0].Next_TaskProgress_Sign == '0':
                    Title = '通知：研发样本实验分派任务'  # 系统消息标题
                    taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    Message = username + '分派给你一个研发实验分派任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
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
                models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(
                    ReviewTime=ReviewTime,
                    ReviewRemarks=ReviewRemarks,
                    ContractAuditor=ContractAuditor,
                    TaskAssignment=TaskAssignment,
                    )

            elif button_name == 'Suspend':
                print '暂停任务'
                temp_data = models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num)
                if not temp_data[0].Next_TaskProgress_Sign == '1':
                    # 暂停任务
                    models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(
                        sample_review='2',
                        ReviewResult='暂停',
                        SampleAuditor=username,
                        ReviewTime=ReviewTime,
                        ReviewRemarks=ReviewRemarks,
                        ContractAuditor=ContractAuditor,
                        TaskAssignment=TaskAssignment,
                    )
            elif button_name == 'return':
                print '退回修改'
                temp_data = models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num)
                if not temp_data[0].Next_TaskProgress_Sign == '1':
                    # 暂停任务
                    models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(
                        sample_review='4',
                        SampleAuditor=username,
                        ReviewTime=ReviewTime,
                        ReviewRemarks=ReviewRemarks,
                        ContractAuditor=ContractAuditor,
                        TaskAssignment=TaskAssignment,
                    )

                    taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    Title = '通知：研发样本审核退回'  # 系统消息标题
                    Message = username + '在审核你登记的研发样本信息时给你退回一个样本修改登记信息！样本编号为：' + sam_code_num + '。请尽快完成修改！'  # 系统邮件正文
                    temp_data = models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num)
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
            elif button_name == 'Not_pass':
                print '终止任务'
                temp_data = models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num)
                if not temp_data[0].Next_TaskProgress_Sign == '1':
                    # 终止任务
                    models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(
                        sample_review='3',
                        ReviewResult='终止',
                        SampleAuditor=username,
                        ReviewTime=ReviewTime,
                        ReviewRemarks=ReviewRemarks,
                        ContractAuditor=ContractAuditor,
                        TaskAssignment=TaskAssignment,
                    )

            # 从数据里取出所有数据
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            temp_not_audited = models.RandDSampleInfo.objects.filter(sample_review=0)  # 研发样本未审核信息
            temp_pass = models.RandDSampleInfo.objects.filter(sample_review=1)  # 研发样本已通过审核信息
            temp_return = models.RandDSampleInfo.objects.filter(sample_review=4)  # 研发审核退回样本信息
            temp_Suspend = models.RandDSampleInfo.objects.filter(sample_review=2)  # 研发样本暂停任务信息
            temp_not_pass = models.RandDSampleInfo.objects.filter(sample_review=3)  # 研发样本终止任务信息

            return render(request, "modelspage/RandD_Sample_ReviewHomePage.html",
                          {"userinfo": temp, "data": temp_not_audited, "pass": temp_pass, "Suspend": temp_Suspend,
                           "Not_pass": temp_not_pass, "myInfo": temp_myInfo, "return": temp_return,
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

# 研发样本已通过审核信息详情页
def RandDSampleReviewPassInfo (request):
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
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print 'Pass样本条码号: ', sam_code_num

            # 判断哪个按钮提交的数据
            if request.POST.has_key('pass'):
                button_name = 'pass'
            elif request.POST.has_key('ModifyData'):
                button_name = 'ModifyData'
            elif request.POST.has_key('delete'):
                temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                    username=username)  # 用户操作权限信息
                # print temp_UserOperationPermissionsInfo.sampleReview
                if temp_UserOperationPermissionsInfo.RandDSampleReviewHomePage == '1':
                    models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).delete()  # 删除信息
                    # 从数据里取出所有数据
                    temp_not_audited = models.RandDSampleInfo.objects.filter(sample_review=0)  # 研发样本未审核信息
                    temp_pass = models.RandDSampleInfo.objects.filter(sample_review=1)  # 研发样本已通过审核信息
                    temp_return = models.RandDSampleInfo.objects.filter(sample_review=4)  # 研发审核退回样本信息
                    temp_Suspend = models.RandDSampleInfo.objects.filter(sample_review=2)  # 研发样本暂停任务信息
                    temp_not_pass = models.RandDSampleInfo.objects.filter(sample_review=3)  # 研发样本终止任务信息

                    return render(request, "modelspage/RandD_Sample_ReviewHomePage.html",
                                  {"userinfo": temp, "data": temp_not_audited, "pass": temp_pass,
                                   "Suspend": temp_Suspend,
                                   "Not_pass": temp_not_pass, "myInfo": temp_myInfo, "return": temp_return,
                                   "SystemMessage": temp_SystemMessage_Unread,
                                   "num_SystemMessage_Unread": num_SystemMessage_Unread})
                else:
                    return render(request, "modelspage/PermissionsPrompt.html",
                                  {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                                   "num_SystemMessage_Unread": num_SystemMessage_Unread})

        temp_mysql = models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num)
        if button_name == 'pass':
            return render(request, "modelspage/RandDSampleReviewPassInfo.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'ModifyData':
            temp_userlist = User.objects.filter(first_name='财务部')
            temp_rnduserlist = User.objects.filter(first_name='研发部')
            return render(request, "modelspage/RandDSampleReviewModifyData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                           "rnduserlist": temp_rnduserlist,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 研发样本暂停任务信息详情页
def RandDSampleReviewSuspendInfo (request):
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
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print 'Pass样本条码号: ', sam_code_num
            # 判断哪个按钮提交的数据
            if request.POST.has_key('Suspend'):
                button_name = 'Suspend'
            elif request.POST.has_key('return'):
                button_name = 'return'
            elif request.POST.has_key('ModifyData'):
                button_name = 'ModifyData'
            elif request.POST.has_key('delete'):
                temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                    username=username)  # 用户操作权限信息
                # print temp_UserOperationPermissionsInfo.sampleReview
                if temp_UserOperationPermissionsInfo.RandDSampleReviewHomePage == '1':
                    models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).delete()  # 删除信息
                    # 从数据里取出所有数据
                    temp_not_audited = models.RandDSampleInfo.objects.filter(sample_review=0)  # 研发样本未审核信息
                    temp_pass = models.RandDSampleInfo.objects.filter(sample_review=1)  # 研发样本已通过审核信息
                    temp_return = models.RandDSampleInfo.objects.filter(sample_review=4)  # 研发审核退回样本信息
                    temp_Suspend = models.RandDSampleInfo.objects.filter(sample_review=2)  # 研发样本暂停任务信息
                    temp_not_pass = models.RandDSampleInfo.objects.filter(sample_review=3)  # 研发样本终止任务信息

                    return render(request, "modelspage/RandD_Sample_ReviewHomePage.html",
                                  {"userinfo": temp, "data": temp_not_audited, "pass": temp_pass,
                                   "Suspend": temp_Suspend,
                                   "Not_pass": temp_not_pass, "myInfo": temp_myInfo, "return": temp_return,
                                   "SystemMessage": temp_SystemMessage_Unread,
                                   "num_SystemMessage_Unread": num_SystemMessage_Unread})
                else:
                    return render(request, "modelspage/PermissionsPrompt.html",
                                  {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                                   "num_SystemMessage_Unread": num_SystemMessage_Unread})

        temp_mysql = models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num)

        if button_name == 'Suspend':
            return render(request, "modelspage/RandDSampleReviewSuspendInfo.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'return':
            return render(request, "modelspage/RandDSampleReviewReturnInfo.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'ModifyData':
            temp_userlist = User.objects.filter(first_name='财务部')
            temp_rnduserlist = User.objects.filter(first_name='研发部')
            return render(request, "modelspage/RandDSampleReviewModifyData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                           "rnduserlist": temp_rnduserlist,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 研发已暂停的样本恢复操作
def RandDSampleRecoveryTaskOperation (request):
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
        if temp_UserOperationPermissionsInfo.RandDSampleReviewHomePage == '1':
            sam_code_num = ''
            # 研发样本审核信息
            ReviewTime = ''  # 样本审核时间
            ReviewRemarks = ''  # 审核备注
            if request.method == "POST":
                # 样本条码号
                sam_code_num = request.POST.get('sam_code_num').strip('HT')
                print '样本条码号: ', sam_code_num

            models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(sample_review='0')
            models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(ReviewTime=ReviewTime)
            models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(ReviewRemarks=ReviewRemarks)

            # 从数据里取出所有数据
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            temp_not_audited = models.RandDSampleInfo.objects.filter(sample_review=0)  # 研发样本未审核信息
            temp_pass = models.RandDSampleInfo.objects.filter(sample_review=1)  # 研发样本已通过审核信息
            temp_return = models.RandDSampleInfo.objects.filter(sample_review=4)  # 研发审核退回样本信息
            temp_Suspend = models.RandDSampleInfo.objects.filter(sample_review=2)  # 研发样本暂停任务信息
            temp_not_pass = models.RandDSampleInfo.objects.filter(sample_review=3)  # 研发样本终止任务信息

            return render(request, "modelspage/RandD_Sample_ReviewHomePage.html",
                          {"userinfo": temp, "data": temp_not_audited, "pass": temp_pass, "Suspend": temp_Suspend,
                           "Not_pass": temp_not_pass, "myInfo": temp_myInfo, "return": temp_return,
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

# 研发样本不通过审核信息详情页
def RandDSampleReviewNotPassInfo (request):
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
            print 'Pass样本条码号: ', sam_code_num

            # 判断哪个按钮提交的数据
            if request.POST.has_key('Stop'):
                button_name = 'Stop'
            elif request.POST.has_key('ModifyData'):
                button_name = 'ModifyData'
            elif request.POST.has_key('delete'):
                temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                    username=username)  # 用户操作权限信息
                # print temp_UserOperationPermissionsInfo.sampleReview
                if temp_UserOperationPermissionsInfo.RandDSampleReviewHomePage == '1':
                    models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).delete()  # 删除信息
                    # 从数据里取出所有数据
                    temp_not_audited = models.RandDSampleInfo.objects.filter(sample_review=0)  # 研发样本未审核信息
                    temp_pass = models.RandDSampleInfo.objects.filter(sample_review=1)  # 研发样本已通过审核信息
                    temp_return = models.RandDSampleInfo.objects.filter(sample_review=4)  # 研发审核退回样本信息
                    temp_Suspend = models.RandDSampleInfo.objects.filter(sample_review=2)  # 研发样本暂停任务信息
                    temp_not_pass = models.RandDSampleInfo.objects.filter(sample_review=3)  # 研发样本终止任务信息

                    return render(request, "modelspage/RandD_Sample_ReviewHomePage.html",
                                  {"userinfo": temp, "data": temp_not_audited, "pass": temp_pass,
                                   "Suspend": temp_Suspend,
                                   "Not_pass": temp_not_pass, "myInfo": temp_myInfo, "return": temp_return,
                                   "SystemMessage": temp_SystemMessage_Unread,
                                   "num_SystemMessage_Unread": num_SystemMessage_Unread})
                else:
                    return render(request, "modelspage/PermissionsPrompt.html",
                                  {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                                   "num_SystemMessage_Unread": num_SystemMessage_Unread})

        temp_mysql = models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num)

        if button_name == 'Stop':
            return render(request, "modelspage/RandDSampleReviewNotPassInfo.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'ModifyData':
            temp_userlist = User.objects.filter(first_name='财务部')
            temp_rnduserlist = User.objects.filter(first_name='研发部')
            return render(request, "modelspage/RandDSampleReviewModifyData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                           "rnduserlist": temp_rnduserlist,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
