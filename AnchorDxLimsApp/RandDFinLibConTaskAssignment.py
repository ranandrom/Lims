# encoding: utf-8

from django.shortcuts import render
from AnchorDxLimsApp import models
from django.contrib.auth.models import User
from time import strftime,gmtime
from AnchorDxLimsApp.views import sendEmail
from itertools import chain
import time,httplib,datetime
# Create your views here.
#coding:utf-8

from django.shortcuts import render,HttpResponse

# 研发样本终文库构建任务未分配详情页
def RandDSampleDFinLibTaskInfo (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        sam_code_num = ''
        Build_lib_num = ''  # 预文库构建实验次数
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
        temp_userlist = User.objects.filter(first_name='研发部')
        temp_mysql = models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num, ExperimentTimes=Build_lib_num)  # DNA提取样本信息

        return render(request, "modelspage/RandDFinLibConTaskAssignment.html",
                      {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                       "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 研发样本终文库构建任务分配操作
def RandDSampleFinLibTaskAssignmentOperation(request):
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
        # print 'ClinicalSampleRegistration: ', temp_UserOperationPermissionsInfo.ClinicalSampleRegistration
        if temp_UserOperationPermissionsInfo.RandDExperimentalTaskAssignmentHomePage == '1':
            button_name = ''  # 按钮名字
            sam_code_num = ''
            # 样本任务分配信息
            TaskReceiver = ''  # 任务接收者
            taskRemarks = ''  # 任务备注
            TaskProgress = ''  # 任务进度
            taskTime = ''  # 任务分配时间
            task_num = ''  # 预文库构建实验次数
            DNA_extraction_num = ''  # DNA提取实验次数
            if request.method == "POST":
                print '患者信息: ============================================= '
                # 样本条码号
                sam_code_num = request.POST.get('sam_code_num')
                print '样本条码号: ', sam_code_num

                # 任务接收者
                TaskReceiver = request.POST.get('TaskReceiver')
                print '任务接收者: ', TaskReceiver

                # 任务备注
                taskRemarks = request.POST.get('taskRemarks')
                print '任务备注: ', taskRemarks

                # 任务进度
                TaskProgress = request.POST.get('TaskProgress')
                print '任务进度: ', TaskProgress

                # 任务分配时间
                taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # taskTime = getBeijinTime()
                print '任务分配时间: ', taskTime

                # 预文库构建实验次数
                task_num = request.POST.get('Build_lib_num')
                print '预文库构建实验次数: ', task_num

                # DNA提取实验次数
                DNA_extraction_num = request.POST.get('DNA_extraction_num')
                print 'DNA提取实验次数: ', DNA_extraction_num

                # 判断哪个按钮提交的数据
                if request.POST.has_key('Determine'):
                    button_name = 'Determine'
                elif request.POST.has_key('Suspend'):
                    button_name = 'Suspend'
                elif request.POST.has_key('Stop'):
                    button_name = 'Stop'
                elif request.POST.has_key('submitModify'):
                    button_name = 'submitModify'

            # 修改数据库预文库构建信息状态
            if button_name == 'Determine':
                # 任务已分配
                if TaskProgress == request.POST.get('DNA_extraction'):
                    temp_RandDSamplePretreatmentInfo = models.RandDSamplePretreatmentInfo.objects.filter(
                        sam_code_num=sam_code_num)
                    if len(temp_RandDSamplePretreatmentInfo) == 0:
                        models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(
                            DNAExtract_Sign=0,
                            Next_TaskProgress_Sign='1',
                            Next_TaskProgress_Man=TaskReceiver,
                            Next_TaskProgress_Remarks=taskRemarks,
                            Next_TaskProgress_Time=taskTime,
                            Next_TaskProgress=TaskProgress,
                        )
                    else:
                        models.RandDSamplePretreatmentInfo.objects.filter(sam_code_num=sam_code_num).update(
                            DNAExtract_Sign=0,
                            Next_TaskProgress_Sign='1',
                            Next_TaskProgress_Man=TaskReceiver,
                            Next_TaskProgress_Remarks=taskRemarks,
                            Next_TaskProgress_Time=taskTime,
                            Next_TaskProgress=TaskProgress,
                        )

                    # 添加系统消息
                    Title = '通知：研发样本DNA提取任务'  # 系统消息标题
                    Message = username + '分派给你一个研发样本DNA提取任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                    print '再次进行DNA提取'
                elif TaskProgress == request.POST.get('PreLibCon'):
                    models.RandDSampleDNAExtractInfo.objects.filter(sam_code_num=sam_code_num,
                                                                    ExperimentTimes=DNA_extraction_num).update(
                        PreLibCon_Sign='0',
                        Next_TaskProgress_Sign='1',
                        Next_TaskProgress_Man=TaskReceiver,
                        Next_TaskProgress_Remarks=taskRemarks,
                        Next_TaskProgress_Time=taskTime,
                        Next_TaskProgress=TaskProgress,
                    )

                    # 添加系统消息
                    Title = '通知：研发样本预文库构建任务'  # 系统消息标题
                    Message = username + '分派给你一个研发样本预文库构建任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                    print '再次进行预文库构建'
                else:
                    # 添加系统消息
                    Title = '通知：研发样本终文库构建任务'  # 系统消息标题
                    Message = username + '分派给你一个研发样本终文库构建任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文

                models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                               ExperimentTimes=task_num).update(
                    Next_TaskProgress_Sign='1',
                    Next_TaskProgress_Man=TaskReceiver,
                    Next_TaskProgress_Remarks=taskRemarks,
                    Next_TaskProgress_Time=taskTime,
                    Next_TaskProgress=TaskProgress,
                )

                # 添加系统消息
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
                # 上次分派任务进度
                OldTaskProgress = request.POST.get('OldTaskProgress')
                if not TaskProgress == OldTaskProgress:
                    if OldTaskProgress == request.POST.get('DNA_extraction'):
                        temp_RandDSamplePretreatmentInfo = models.RandDSamplePretreatmentInfo.objects.filter(
                            sam_code_num=sam_code_num)
                        if len(temp_RandDSamplePretreatmentInfo) == 0:
                            models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(DNAExtract_Sign=1)
                        else:
                            models.RandDSamplePretreatmentInfo.objects.filter(sam_code_num=sam_code_num).update(
                                DNAExtract_Sign=1)
                    elif OldTaskProgress == request.POST.get('PreLibCon'):
                        models.RandDSampleDNAExtractInfo.objects.filter(sam_code_num=sam_code_num,
                                                                        ExperimentTimes=DNA_extraction_num).update(
                            Next_TaskProgress_Man=TaskReceiver,
                            Next_TaskProgress_Remarks=taskRemarks,
                            Next_TaskProgress=TaskProgress,
                        )
                    else:
                        models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                       ExperimentTimes=task_num).update(
                            Next_TaskProgress_Man=TaskReceiver,
                            Next_TaskProgress_Remarks=taskRemarks,
                            Next_TaskProgress=TaskProgress,
                        )

                    if TaskProgress == request.POST.get('DNA_extraction'):
                        temp_RandDSamplePretreatmentInfo = models.RandDSamplePretreatmentInfo.objects.filter(
                            sam_code_num=sam_code_num)
                        if len(temp_RandDSamplePretreatmentInfo) == 0:
                            models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(
                                DNAExtract_Sign=0,
                                Next_TaskProgress_Sign='1',
                                Next_TaskProgress_Man=TaskReceiver,
                                Next_TaskProgress_Remarks=taskRemarks,
                                Next_TaskProgress_Time=taskTime,
                                Next_TaskProgress=TaskProgress,
                            )
                        else:
                            models.RandDSamplePretreatmentInfo.objects.filter(sam_code_num=sam_code_num).update(
                                DNAExtract_Sign=0,
                                Next_TaskProgress_Sign='1',
                                Next_TaskProgress_Man=TaskReceiver,
                                Next_TaskProgress_Remarks=taskRemarks,
                                Next_TaskProgress_Time=taskTime,
                                Next_TaskProgress=TaskProgress,
                            )

                        # 添加系统消息
                        Title = '通知：研发样本DNA提取任务'  # 系统消息标题
                        Message = username + '分派给你一个研发样本DNA提取任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                        # 添加系统消息
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
                        print '再次进行DNA提取'
                    elif TaskProgress == request.POST.get('PreLibCon'):
                        models.RandDSampleDNAExtractInfo.objects.filter(sam_code_num=sam_code_num,
                                                                        ExperimentTimes=DNA_extraction_num).update(
                            PreLibCon_Sign='0',
                            Next_TaskProgress_Sign='1',
                            Next_TaskProgress_Man=TaskReceiver,
                            Next_TaskProgress_Remarks=taskRemarks,
                            Next_TaskProgress_Time=taskTime,
                            Next_TaskProgress=TaskProgress,
                        )
                        Title = '通知：研发样本预文库构建任务'  # 系统消息标题
                        Message = username + '分派给你一个研发样本预文库构建任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                        # 添加系统消息
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
                        print '再次进行预文库构建'
                    else:
                        models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                       ExperimentTimes=task_num).update(
                            FinalLibCon_Sign='0',
                            Next_TaskProgress_Sign='1',
                            Next_TaskProgress_Man=TaskReceiver,
                            Next_TaskProgress_Remarks=taskRemarks,
                            Next_TaskProgress_Time=taskTime,
                            Next_TaskProgress=TaskProgress,
                        )

                        # 添加系统消息
                        Title = '通知：研发样本终文库构建任务'  # 系统消息标题
                        Message = username + '分派给你一个研发样本终文库构建任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
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
                        print '进行终文库构建'
                else:
                    # 预文库构建任务列表
                    if TaskProgress == request.POST.get('DNA_extraction'):
                        temp_RandDSamplePretreatmentInfo = models.RandDSamplePretreatmentInfo.objects.filter(
                            sam_code_num=sam_code_num)
                        if len(temp_RandDSamplePretreatmentInfo) == 0:
                            temp_data = models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num)
                            if not temp_data[0].Next_TaskProgress_Man == TaskReceiver and temp_data[0].DNAExtract_Sign == '0':
                                # 添加系统消息
                                Title = '通知：研发样本DNA提取任务'  # 系统消息标题
                                Message = username + '分派给你一个研发样本DNA提取任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                                # 添加系统消息
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
                            models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(
                                Next_TaskProgress=TaskProgress,
                                Next_TaskProgress_Man=TaskReceiver,
                                Next_TaskProgress_Remarks=taskRemarks,
                            )
                        else:
                            temp_data = models.RandDSamplePretreatmentInfo.objects.filter(sam_code_num=sam_code_num)
                            if not temp_data[0].Next_TaskProgress_Man == TaskReceiver and temp_data[0].DNAExtract_Sign == '0':
                                # 添加系统消息
                                Title = '通知：研发样本DNA提取任务'  # 系统消息标题
                                Message = username + '分派给你一个研发样本DNA提取任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                                # 添加系统消息
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
                            models.RandDSamplePretreatmentInfo.objects.filter(sam_code_num=sam_code_num).update(
                                Next_TaskProgress=TaskProgress,
                                Next_TaskProgress_Man=TaskReceiver,
                                Next_TaskProgress_Remarks=taskRemarks,
                            )
                        print '再次进行DNA提取'
                    elif TaskProgress == request.POST.get('PreLibCon'):
                        temp_data = models.RandDSampleDNAExtractInfo.objects.filter(sam_code_num=sam_code_num,
                                                                                    ExperimentTimes=DNA_extraction_num)
                        if not temp_data[0].Next_TaskProgress_Man == TaskReceiver and temp_data[
                            0].PreLibCon_Sign == '0':
                            Title = '通知：临检样本预文库构建任务'  # 系统消息标题
                            Message = username + '分派给你一个临检样本预文库构建任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                            # 添加系统消息
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
                        models.RandDSampleDNAExtractInfo.objects.filter(sam_code_num=sam_code_num,
                                                                        ExperimentTimes=DNA_extraction_num).update(
                            Next_TaskProgress_Man=TaskReceiver,
                            Next_TaskProgress_Remarks=taskRemarks,
                            Next_TaskProgress=TaskProgress,
                        )
                        print '再次进行预文库构建'
                    else:
                        temp_data = models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                                   ExperimentTimes=task_num)
                        if not temp_data[0].Next_TaskProgress_Man == TaskReceiver and temp_data[0].FinalLibCon_Sign == '0':
                            Title = '通知：临检样本终文库构建任务'  # 系统消息标题
                            Message = username + '分派给你一个临检样本终文库构建任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                            # 添加系统消息
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
                        models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                       ExperimentTimes=task_num).update(
                            Next_TaskProgress_Man=TaskReceiver,
                            Next_TaskProgress_Remarks=taskRemarks,
                            Next_TaskProgress=TaskProgress,
                        )

                models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                               ExperimentTimes=task_num).update(
                    Next_TaskProgress_Man=TaskReceiver,
                    Next_TaskProgress_Remarks=taskRemarks,
                    Next_TaskProgress=TaskProgress,
                )
            elif button_name == 'Suspend':
                # 任务暂停
                models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                               ExperimentTimes=task_num).update(
                    Next_TaskProgress_Sign='2',
                    Next_TaskProgress_Man=TaskReceiver,
                    Next_TaskProgress_Remarks=taskRemarks,
                    Next_TaskProgress_Time=taskTime,
                    Next_TaskProgress=TaskProgress,
                )
            elif button_name == 'Stop':
                # 任务终止
                models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                               ExperimentTimes=task_num).update(
                    Next_TaskProgress_Sign='3',
                    Next_TaskProgress_Man=TaskReceiver,
                    Next_TaskProgress_Remarks=taskRemarks,
                    Next_TaskProgress_Time=taskTime,
                    Next_TaskProgress=TaskProgress,
                )

            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)

            # 预处理任务列表
            Pretreatment_not_audited = models.RandDSampleInfo.objects.filter(Next_TaskProgress_Sign=0,
                                                                             sample_review='1',
                                                                             TissueSampleSign=0)  # 任务未分配信息
            Pretreatment_audited = models.RandDSampleInfo.objects.filter(Next_TaskProgress_Sign=1, sample_review='1',
                                                                         TissueSampleSign=0)  # 任务已分配信息

            # DNA提取任务列表
            # DNA_not_audited = models.RandDSampleInfo.objects.filter(Next_TaskProgress_Sign=0, TissueSampleSign=1)  # 任务未分配信息
            temp_not_Pretreatment = models.RandDSampleInfo.objects.filter(Next_TaskProgress_Sign=0, sample_review='1',
                                                                          TissueSampleSign=1)  # 任务未分配信息
            temp_Pretreatment = models.RandDSamplePretreatmentInfo.objects.filter(Next_TaskProgress_Sign=0)  # 任务未分配信息
            DNA_not_audited = chain(temp_not_Pretreatment, temp_Pretreatment)  # 合并所有数据表数据
            # DNA_audited = models.RandDSampleInfo.objects.filter(Next_TaskProgress_Sign=1, TissueSampleSign=1)  # 任务已分配信息
            temp_not_Pretreatment_audited = models.RandDSampleInfo.objects.filter(Next_TaskProgress_Sign=1,
                                                                                  sample_review='1',
                                                                                  TissueSampleSign=1)  # 任务已分配信息
            temp_Pretreatment_audited = models.RandDSamplePretreatmentInfo.objects.filter(
                Next_TaskProgress_Sign=1)  # 任务已分配信息
            DNA_audited = chain(temp_not_Pretreatment_audited, temp_Pretreatment_audited)  # 合并所有数据表数据

            # 预文库构建任务列表
            temp_Fin_unaud = models.clinicalSampleInfo.objects.filter(contract_review=0)  # 财务未审核信息
            temp_Fin_NoPass = models.clinicalSampleInfo.objects.filter(contract_review=2)  # 财务审核不通过信息
            PreLibCon_not_audited = models.RandDSampleDNAExtractInfo.objects.filter(Next_TaskProgress_Sign=0)  # 任务未分配信息
            PreLibCon_audited = models.RandDSampleDNAExtractInfo.objects.filter(Next_TaskProgress_Sign=1)  # 任务已分配信息

            # 终文库构建任务列表
            FinLibCon_not_audited = models.RandDSamplePreLibConInfo.objects.filter(Next_TaskProgress_Sign=0)  # 任务未分配信息
            FinLibCon_audited = models.RandDSamplePreLibConInfo.objects.filter(Next_TaskProgress_Sign=1)  # 任务已分配信息

            # 上机测序任务列表
            ComputerSeq_not_audited = models.RandDSampleFinLibConInfo.objects.filter(
                Next_TaskProgress_Sign=0)  # 任务未分配信息
            ComputerSeq_audited = models.RandDSampleFinLibConInfo.objects.filter(Next_TaskProgress_Sign=1)  # 任务已分配信息

            # 其他信息列表
            # 任务暂停信息
            temp_Pretreatment = models.RandDSampleInfo.objects.filter(Next_TaskProgress_Sign=2,
                                                                      sample_review='1')  # 预处理任务暂停信息
            temp_DNAExtract = models.RandDSamplePretreatmentInfo.objects.filter(Next_TaskProgress_Sign=2)  # DNA提取任务暂停信息
            temp_PreLibCon = models.RandDSampleDNAExtractInfo.objects.filter(Next_TaskProgress_Sign=2)  # 预文库构建任务暂停信息
            temp_FinLibCon = models.RandDSamplePreLibConInfo.objects.filter(Next_TaskProgress_Sign=2)  # 终文库构建任务暂停信息
            temp_SeqCom = models.RandDSampleFinLibConInfo.objects.filter(Next_TaskProgress_Sign=2)  # 上机测序任务暂停信息
            temp_suspend = chain(temp_Pretreatment, temp_DNAExtract, temp_PreLibCon, temp_FinLibCon,
                                 temp_SeqCom)  # 合并所有数据表数据
            # 任务终止信息
            # temp_stop = models.clinicalSampleInfo.objects.filter(Next_TaskProgress_Sign=3)  # 任务终止信息
            temp_Pretreatment_stop = models.RandDSampleInfo.objects.filter(Next_TaskProgress_Sign=3,
                                                                           sample_review='1')  # 预处理任务终止信息
            temp_DNAExtract_stop = models.RandDSamplePretreatmentInfo.objects.filter(
                Next_TaskProgress_Sign=3)  # DNA提取任务终止信息
            temp_PreLibCon_stop = models.RandDSampleDNAExtractInfo.objects.filter(
                Next_TaskProgress_Sign=3)  # 预文库构建任务终止信息
            temp_FinLibCon_stop = models.RandDSamplePreLibConInfo.objects.filter(
                Next_TaskProgress_Sign=3)  # 终文库构建任务终止信息
            temp_SeqCom_stop = models.RandDSampleFinLibConInfo.objects.filter(Next_TaskProgress_Sign=3)  # 上机测序任务终止信息
            temp_stop = chain(temp_Pretreatment_stop, temp_DNAExtract_stop, temp_PreLibCon_stop, temp_FinLibCon_stop,
                              temp_SeqCom_stop)  # 合并所有数据表数据

            return render(request, "modelspage/RandDExperimentalTaskAssignment.html", {"userinfo": temp,
                                                                                       "Pretreatment_not_audited": Pretreatment_not_audited,
                                                                                       "Pretreatment_audited": Pretreatment_audited,
                                                                                       "DNA_not_audited": DNA_not_audited,
                                                                                       "DNA_audited": DNA_audited,
                                                                                       "PreLibCon_not_audited": PreLibCon_not_audited,
                                                                                       "PreLibCon_audited": PreLibCon_audited,
                                                                                       "FinLibCon_not_audited": FinLibCon_not_audited,
                                                                                       "FinLibCon_audited": FinLibCon_audited,
                                                                                       "ComputerSeq_not_audited": ComputerSeq_not_audited,
                                                                                       "ComputerSeq_audited": ComputerSeq_audited,
                                                                                       "Fin_unaud": temp_Fin_unaud,
                                                                                       "Fin_NoPass": temp_Fin_NoPass,
                                                                                       "suspend": temp_suspend,
                                                                                       "stop": temp_stop,
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

# 研发样本终文库构建任务已分配信息详情页
def RandDSampleFinLibTaskDetails (request):
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
            # 预文库构建实验次数
            Build_lib_num = request.POST.get('Build_lib_num')
            print '预文库构建实验次数: ', Build_lib_num

            # 判断哪个按钮提交的数据
            if request.POST.has_key('FinLibCon_audited'):
                button_name = 'FinLibCon_audited'
            elif request.POST.has_key('ModifyData'):
                button_name = 'ModifyData'

        # 从数据里取出某条记录
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_mysql = models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                     ExperimentTimes=Build_lib_num)  # DNA提取样本信息

        if button_name == 'FinLibCon_audited':
            return render(request, "modelspage/RandDFinLibConTaskDetails.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'ModifyData':
            temp_userlist = User.objects.filter(first_name='研发部')
            return render(request, "modelspage/RandDFinLibConTaskAssModifyData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
