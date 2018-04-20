# encoding: utf-8

from django.shortcuts import render
from AnchorDxLimsApp import models
from django.contrib.auth.models import User
from AnchorDxLimsApp.views import sendEmail
from time import strftime,gmtime
from itertools import chain
import time,httplib,datetime
# Create your views here.
#coding:utf-8

from django.shortcuts import render,HttpResponse

# 研发样本上机测序任务未分配详情页
def RandDSampleComSeqTaskInfo (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        sam_code_num = ''
        Build_finlib_num = ''  # 终文库构建实验次数
        if request.method == "POST":
            print '患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号: ', sam_code_num
            # 终文库构建实验次数
            Build_finlib_num = request.POST.get('Build_finlib_num')
            print '终文库构建实验次数: ', Build_finlib_num

        # 从数据里取出某条记录
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_userlist = User.objects.filter(first_name='研发部')
        temp_mysql = models.RandDSampleFinLibConInfo.objects.filter(sam_code_num=sam_code_num, ExperimentTimes=Build_finlib_num)  # 终文库构建信息

        return render(request, "modelspage/RandDComSeqTaskAssignment.html",
                      {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                       "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 研发样本预文库构建任务分配操作
def RandDSampleComSeqTaskAssignmentOperation (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}
        # temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息

        temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
            username=username)  # 用户操作权限信息
        # print 'ClinicalSampleRegistration: ', temp_UserOperationPermissionsInfo.ClinicalSampleRegistration
        if temp_UserOperationPermissionsInfo.RandDExperimentalTaskAssignmentHomePage == '1':
            button_name = ''  # 按钮名字
            sam_code_num = ''
            # 样本任务分配信息
            Next_TaskProgress_Man = ''  # 任务接收者
            Next_TaskProgress_Remarks = ''  # 任务备注
            Next_TaskProgress = ''  # 任务进度
            Next_TaskProgress_Time = ''  # 任务分配时间
            Build_finlib_num = ''  # 实验次数
            DNA_extraction_num = ''  # DNA提取实验次数
            Build_lib_num = ''  # 预文库构建实验次数
            if request.method == "POST":
                print '患者信息: ============================================= '
                # 样本条码号
                sam_code_num = request.POST.get('sam_code_num').strip('HT')
                print '样本条码号: ', sam_code_num

                # 样本任务分配信息
                Next_TaskProgress_Man = request.POST.get('Next_TaskProgress_Man')  # 任务接收者
                Next_TaskProgress_Remarks = request.POST.get('Next_TaskProgress_Remarks')  # 任务备注
                Next_TaskProgress = request.POST.get('Next_TaskProgress')  # 任务进度
                Next_TaskProgress_Time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # 任务分配时间
                Build_finlib_num = request.POST.get('Build_finlib_num')  # 实验次数
                DNA_extraction_num = request.POST.get('DNA_extraction_num')  # DNA提取实验次数
                Build_lib_num = request.POST.get('Build_lib_num')  # 预文库构建实验次数

                # 判断哪个按钮提交的数据
                if request.POST.has_key('Determine'):
                    button_name = 'Determine'
                elif request.POST.has_key('Suspend'):
                    button_name = 'Suspend'
                elif request.POST.has_key('Stop'):
                    button_name = 'Stop'
                elif request.POST.has_key('submitModify'):
                    button_name = 'submitModify'

            # 修改数据库合同信息状态
            if button_name == 'Determine':

                if Next_TaskProgress == request.POST.get('DNA_extraction'):
                    temp_RandDSamplePretreatmentInfo = models.RandDSamplePretreatmentInfo.objects.filter(
                        sam_code_num=sam_code_num)
                    if len(temp_RandDSamplePretreatmentInfo) == 0:
                        models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(
                            DNAExtract_Sign=0,
                            Next_TaskProgress_Sign='1',
                            Next_TaskProgress_Man=Next_TaskProgress_Man,
                            Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                            Next_TaskProgress_Time=Next_TaskProgress_Time,
                            Next_TaskProgress=Next_TaskProgress,
                        )
                    else:
                        models.RandDSamplePretreatmentInfo.objects.filter(sam_code_num=sam_code_num).update(
                            DNAExtract_Sign=0,
                            Next_TaskProgress_Sign='1',
                            Next_TaskProgress_Man=Next_TaskProgress_Man,
                            Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                            Next_TaskProgress_Time=Next_TaskProgress_Time,
                            Next_TaskProgress=Next_TaskProgress,
                        )
                    # 添加系统消息
                    Title = '通知：研发样本DNA提取任务'  # 系统消息标题
                    Message = username + '分派给你一个研发样本DNA提取任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                    print '再次进行DNA提取'
                elif Next_TaskProgress == request.POST.get('PreLibCon'):
                    models.RandDSampleDNAExtractInfo.objects.filter(sam_code_num=sam_code_num,
                                                                    ExperimentTimes=DNA_extraction_num).update(
                        PreLibCon_Sign='0',
                        Next_TaskProgress_Sign='1',
                        Next_TaskProgress_Man=Next_TaskProgress_Man,
                        Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                        Next_TaskProgress_Time=Next_TaskProgress_Time,
                        Next_TaskProgress=Next_TaskProgress,
                    )

                    # 添加系统消息
                    Title = '通知：研发样本预文库构建任务'  # 系统消息标题
                    Message = username + '分派给你一个研发样本预文库构建任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                    print '再次进行预文库构建'
                elif Next_TaskProgress == request.POST.get('FinLibCon'):
                    models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                    ExperimentTimes=Build_lib_num).update(
                        FinalLibCon_Sign='0',
                        Next_TaskProgress_Sign='1',
                        Next_TaskProgress_Man=Next_TaskProgress_Man,
                        Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                        Next_TaskProgress_Time=Next_TaskProgress_Time,
                        Next_TaskProgress=Next_TaskProgress,
                    )
                    # 添加系统消息
                    Title = '通知：研发样本终文库构建任务'  # 系统消息标题
                    Message = username + '分派给你一个研发样本终文库构建任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                    print '再次进行终文库构建'
                else:
                    # 添加系统消息
                    Title = '通知：研发样本上机测序任务'  # 系统消息标题
                    Message = username + '分派给你一个研发样本上机测序任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文

                # 添加系统消息
                models.UserSystemMessage.objects.create(
                    # 用户信息
                    Sender=username,  # 发送者
                    Receiver=Next_TaskProgress_Man,  # 接收者
                    # 信息内容
                    Time=Next_TaskProgress_Time,  # 信息生成时间
                    Title=Title,  # 系统消息标题
                    Message=Message,  # 系统消息正文
                    ReadingState='未读',  # 信息阅读状态
                )
                sendEmail(Next_TaskProgress_Man, Title, Message)  # 发送邮件通知

                models.RandDSampleFinLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                ExperimentTimes=Build_finlib_num).update(
                    Next_TaskProgress_Sign='1',
                    Next_TaskProgress_Man=Next_TaskProgress_Man,
                    Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                    Next_TaskProgress_Time=Next_TaskProgress_Time,
                    Next_TaskProgress=Next_TaskProgress,
                )

            elif button_name == 'submitModify':
                # 上次分派任务进度
                OldTaskProgress = request.POST.get('OldTaskProgress')
                if not Next_TaskProgress == OldTaskProgress:
                    if OldTaskProgress == request.POST.get('DNA_extraction'):
                        temp_RandDSamplePretreatmentInfo = models.RandDSamplePretreatmentInfo.objects.filter(
                            sam_code_num=sam_code_num)
                        if len(temp_RandDSamplePretreatmentInfo) == 0:
                            models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(DNAExtract_Sign=1)
                        else:
                            models.RandDSamplePretreatmentInfo.objects.filter(sam_code_num=sam_code_num).update(DNAExtract_Sign=1)
                    elif OldTaskProgress == request.POST.get('PreLibCon'):
                        models.RandDSampleDNAExtractInfo.objects.filter(sam_code_num=sam_code_num,
                                                                        ExperimentTimes=DNA_extraction_num).update(
                            Next_TaskProgress_Man=Next_TaskProgress_Man,
                            Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                            Next_TaskProgress=Next_TaskProgress,
                        )
                    elif OldTaskProgress == request.POST.get('FinLibCon'):
                        models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                       ExperimentTimes=Build_lib_num).update(
                            Next_TaskProgress_Man=Next_TaskProgress_Man,
                            Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                            Next_TaskProgress=Next_TaskProgress,
                        )
                    else:
                        models.RandDSampleFinLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                       ExperimentTimes=Build_finlib_num).update(
                            Next_TaskProgress_Man=Next_TaskProgress_Man,
                            Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                            Next_TaskProgress=Next_TaskProgress,
                        )

                    if Next_TaskProgress == request.POST.get('DNA_extraction'):
                        temp_RandDSamplePretreatmentInfo = models.RandDSamplePretreatmentInfo.objects.filter(
                            sam_code_num=sam_code_num)
                        if len(temp_RandDSamplePretreatmentInfo) == 0:
                            models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(
                                DNAExtract_Sign=0,
                                Next_TaskProgress_Sign='1',
                                Next_TaskProgress_Man=Next_TaskProgress_Man,
                                Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                                Next_TaskProgress_Time=Next_TaskProgress_Time,
                                Next_TaskProgress=Next_TaskProgress,
                            )
                        else:
                            models.RandDSamplePretreatmentInfo.objects.filter(sam_code_num=sam_code_num).update(
                                DNAExtract_Sign=0,
                                Next_TaskProgress_Sign='1',
                                Next_TaskProgress_Man=Next_TaskProgress_Man,
                                Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                                Next_TaskProgress_Time=Next_TaskProgress_Time,
                                Next_TaskProgress=Next_TaskProgress,
                            )

                        # 添加系统消息
                        Title = '通知：研发样本DNA提取任务'  # 系统消息标题
                        Message = username + '分派给你一个研发样本DNA提取任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                        # 添加系统消息
                        models.UserSystemMessage.objects.create(
                            # 用户信息
                            Sender=username,  # 发送者
                            Receiver=Next_TaskProgress_Man,  # 接收者
                            # 信息内容
                            Time=Next_TaskProgress_Time,  # 信息生成时间
                            Title=Title,  # 系统消息标题
                            Message=Message,  # 系统消息正文
                            ReadingState='未读',  # 信息阅读状态
                        )
                        sendEmail(Next_TaskProgress_Man, Title, Message)  # 发送邮件通知
                        print '再次进行DNA提取'
                    elif Next_TaskProgress == request.POST.get('PreLibCon'):
                        models.RandDSampleDNAExtractInfo.objects.filter(sam_code_num=sam_code_num,
                                                                        ExperimentTimes=DNA_extraction_num).update(
                            PreLibCon_Sign='0',
                            Next_TaskProgress_Sign='1',
                            Next_TaskProgress_Man=Next_TaskProgress_Man,
                            Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                            Next_TaskProgress_Time=Next_TaskProgress_Time,
                            Next_TaskProgress=Next_TaskProgress,
                        )
                        Title = '通知：研发样本预文库构建任务'  # 系统消息标题
                        Message = username + '分派给你一个研发样本预文库构建任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                        # 添加系统消息
                        models.UserSystemMessage.objects.create(
                            # 用户信息
                            Sender=username,  # 发送者
                            Receiver=Next_TaskProgress_Man,  # 接收者
                            # 信息内容
                            Time=Next_TaskProgress_Time,  # 信息生成时间
                            Title=Title,  # 系统消息标题
                            Message=Message,  # 系统消息正文
                            ReadingState='未读',  # 信息阅读状态
                        )
                        sendEmail(Next_TaskProgress_Man, Title, Message)  # 发送邮件通知
                        print '再次进行预文库构建'
                    elif Next_TaskProgress == request.POST.get('FinLibCon'):
                        models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                       ExperimentTimes=Build_lib_num).update(
                            FinalLibCon_Sign='0',
                            Next_TaskProgress_Sign='1',
                            Next_TaskProgress_Man=Next_TaskProgress_Man,
                            Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                            Next_TaskProgress_Time=Next_TaskProgress_Time,
                            Next_TaskProgress=Next_TaskProgress,
                        )

                        # 添加系统消息
                        Title = '通知：研发样本终文库构建任务'  # 系统消息标题
                        Message = username + '分派给你一个研发样本终文库构建任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                        models.UserSystemMessage.objects.create(
                            # 用户信息
                            Sender=username,  # 发送者
                            Receiver=Next_TaskProgress_Man,  # 接收者
                            # 信息内容
                            Time=Next_TaskProgress_Time,  # 信息生成时间
                            Title=Title,  # 系统消息标题
                            Message=Message,  # 系统消息正文
                            ReadingState='未读',  # 信息阅读状态
                        )
                        sendEmail(Next_TaskProgress_Man, Title, Message)  # 发送邮件通知
                        print '再次进行终文库构建'
                    else:
                        models.RandDSampleFinLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                       ExperimentTimes=Build_finlib_num).update(
                            ComputerSeq_Sign='0',
                            Next_TaskProgress_Sign='1',
                            Next_TaskProgress_Man=Next_TaskProgress_Man,
                            Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                            Next_TaskProgress_Time=Next_TaskProgress_Time,
                            Next_TaskProgress=Next_TaskProgress,
                        )

                        # 添加系统消息
                        Title = '通知：研发样本上机测序任务'  # 系统消息标题
                        Message = username + '分派给你一个研发样本上机测序任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                        models.UserSystemMessage.objects.create(
                            # 用户信息
                            Sender=username,  # 发送者
                            Receiver=Next_TaskProgress_Man,  # 接收者
                            # 信息内容
                            Time=Next_TaskProgress_Time,  # 信息生成时间
                            Title=Title,  # 系统消息标题
                            Message=Message,  # 系统消息正文
                            ReadingState='未读',  # 信息阅读状态
                        )
                        sendEmail(Next_TaskProgress_Man, Title, Message)  # 发送邮件通知

                else:
                    # 预文库构建任务列表
                    if Next_TaskProgress == request.POST.get('DNA_extraction'):
                        temp_RandDSamplePretreatmentInfo = models.RandDSamplePretreatmentInfo.objects.filter(
                            sam_code_num=sam_code_num)
                        if len(temp_RandDSamplePretreatmentInfo) == 0:
                            temp_data = models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num)
                            if not temp_data[0].Next_TaskProgress_Man == Next_TaskProgress_Man and temp_data[0].DNAExtract_Sign == '0':
                                # 添加系统消息
                                Title = '通知：研发样本DNA提取任务'  # 系统消息标题
                                Message = username + '分派给你一个研发样本DNA提取任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                                # 添加系统消息
                                models.UserSystemMessage.objects.create(
                                    # 用户信息
                                    Sender=username,  # 发送者
                                    Receiver=Next_TaskProgress_Man,  # 接收者
                                    # 信息内容
                                    Time=Next_TaskProgress_Time,  # 信息生成时间
                                    Title=Title,  # 系统消息标题
                                    Message=Message,  # 系统消息正文
                                    ReadingState='未读',  # 信息阅读状态
                                )
                                sendEmail(Next_TaskProgress_Man, Title, Message)  # 发送邮件通知
                            models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(
                                Next_TaskProgress=Next_TaskProgress,
                                Next_TaskProgress_Man=Next_TaskProgress_Man,
                                Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                            )
                        else:
                            temp_data = models.RandDSamplePretreatmentInfo.objects.filter(sam_code_num=sam_code_num)
                            if not temp_data[0].Next_TaskProgress_Man == Next_TaskProgress_Man and temp_data[0].DNAExtract_Sign == '0':
                                # 添加系统消息
                                Title = '通知：研发样本DNA提取任务'  # 系统消息标题
                                Message = username + '分派给你一个研发样本DNA提取任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                                # 添加系统消息
                                models.UserSystemMessage.objects.create(
                                    # 用户信息
                                    Sender=username,  # 发送者
                                    Receiver=Next_TaskProgress_Man,  # 接收者
                                    # 信息内容
                                    Time=Next_TaskProgress_Time,  # 信息生成时间
                                    Title=Title,  # 系统消息标题
                                    Message=Message,  # 系统消息正文
                                    ReadingState='未读',  # 信息阅读状态
                                )
                                sendEmail(Next_TaskProgress_Man, Title, Message)  # 发送邮件通知
                            models.RandDSamplePretreatmentInfo.objects.filter(sam_code_num=sam_code_num).update(
                                Next_TaskProgress=Next_TaskProgress,
                                Next_TaskProgress_Man=Next_TaskProgress_Man,
                                Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                            )
                        print '再次进行DNA提取'
                    elif Next_TaskProgress == request.POST.get('PreLibCon'):
                        temp_data = models.RandDSampleDNAExtractInfo.objects.filter(sam_code_num=sam_code_num,
                                                                                    ExperimentTimes=DNA_extraction_num)
                        if not temp_data[0].Next_TaskProgress_Man == Next_TaskProgress_Man and temp_data[0].PreLibCon_Sign == '0':
                            Title = '通知：研发样本预文库构建任务'  # 系统消息标题
                            Message = username + '分派给你一个研发样本预文库构建任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                            # 添加系统消息
                            models.UserSystemMessage.objects.create(
                                # 用户信息
                                Sender=username,  # 发送者
                                Receiver=Next_TaskProgress_Man,  # 接收者
                                # 信息内容
                                Time=Next_TaskProgress_Time,  # 信息生成时间
                                Title=Title,  # 系统消息标题
                                Message=Message,  # 系统消息正文
                                ReadingState='未读',  # 信息阅读状态
                            )
                            sendEmail(Next_TaskProgress_Man, Title, Message)  # 发送邮件通知
                        models.RandDSampleDNAExtractInfo.objects.filter(sam_code_num=sam_code_num,
                                                                        ExperimentTimes=DNA_extraction_num).update(
                            Next_TaskProgress_Man=Next_TaskProgress_Man,
                            Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                            Next_TaskProgress=Next_TaskProgress,
                        )
                        print '再次进行预文库构建'
                    elif Next_TaskProgress == request.POST.get('FinLibCon'):
                        temp_data = models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                                   ExperimentTimes=Build_lib_num)
                        if not temp_data[0].Next_TaskProgress_Man == Next_TaskProgress_Man and temp_data[0].FinalLibCon_Sign == '0':
                            Title = '通知：临检样本终文库构建任务'  # 系统消息标题
                            Message = username + '分派给你一个临检样本终文库构建任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                            # 添加系统消息
                            models.UserSystemMessage.objects.create(
                                # 用户信息
                                Sender=username,  # 发送者
                                Receiver=Next_TaskProgress_Man,  # 接收者
                                # 信息内容
                                Time=Next_TaskProgress_Time,  # 信息生成时间
                                Title=Title,  # 系统消息标题
                                Message=Message,  # 系统消息正文
                                ReadingState='未读',  # 信息阅读状态
                            )
                            sendEmail(Next_TaskProgress_Man, Title, Message)  # 发送邮件通知
                        models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                       ExperimentTimes=Build_lib_num).update(
                            Next_TaskProgress_Man=Next_TaskProgress_Man,
                            Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                            Next_TaskProgress=Next_TaskProgress,
                        )
                        print '再次进行终文库构建'
                    else:
                        temp_data = models.RandDSampleFinLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                                   ExperimentTimes=Build_finlib_num)
                        if not temp_data[0].Next_TaskProgress_Man == Next_TaskProgress_Man and temp_data[0].FinalLibCon_Sign == '0':
                            Title = '通知：临检样本终文库构建任务'  # 系统消息标题
                            Message = username + '分派给你一个临检样本终文库构建任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
                            # 添加系统消息
                            models.UserSystemMessage.objects.create(
                                # 用户信息
                                Sender=username,  # 发送者
                                Receiver=Next_TaskProgress_Man,  # 接收者
                                # 信息内容
                                Time=Next_TaskProgress_Time,  # 信息生成时间
                                Title=Title,  # 系统消息标题
                                Message=Message,  # 系统消息正文
                                ReadingState='未读',  # 信息阅读状态
                            )
                            sendEmail(Next_TaskProgress_Man, Title, Message)  # 发送邮件通知
                        models.RandDSampleFinLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                       ExperimentTimes=Build_finlib_num).update(
                            Next_TaskProgress_Man=Next_TaskProgress_Man,
                            Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                            Next_TaskProgress=Next_TaskProgress,
                        )

                models.RandDSampleFinLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                               ExperimentTimes=Build_finlib_num).update(
                    Next_TaskProgress_Man=Next_TaskProgress_Man,
                    Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                    Next_TaskProgress=Next_TaskProgress,
                )
            elif button_name == 'Suspend':
                print '任务暂停'
                # 任务暂停
                models.RandDSampleFinLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                ExperimentTimes=Build_finlib_num).update(
                    Next_TaskProgress_Sign='2',
                    Next_TaskProgress_Man=Next_TaskProgress_Man,
                    Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                    Next_TaskProgress_Time=Next_TaskProgress_Time,
                    Next_TaskProgress=Next_TaskProgress,
                )
            elif button_name == 'Stop':
                print '任务终止'
                # 任务终止
                models.RandDSampleFinLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                ExperimentTimes=Build_finlib_num).update(
                    Next_TaskProgress_Sign='3',
                    Next_TaskProgress_Man=Next_TaskProgress_Man,
                    Next_TaskProgress_Remarks=Next_TaskProgress_Remarks,
                    Next_TaskProgress_Time=Next_TaskProgress_Time,
                    Next_TaskProgress=Next_TaskProgress,
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

# 研发样本预文库构建任务已分配信息详情页
def RandDSampleComSeqTaskDetails (request):
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
        button_name = ''
        if request.method == "POST":
            print '患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号: ', sam_code_num
            # 终文库构建实验次数
            Build_finlib_num = request.POST.get('Build_finlib_num')
            print '终文库构建实验次数: ', Build_finlib_num

            # 判断哪个按钮提交的数据
            if request.POST.has_key('ComputerSeq_audited'):
                button_name = 'ComputerSeq_audited'
            elif request.POST.has_key('ModifyData'):
                button_name = 'ModifyData'

        # 从数据里取出某条记录
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_mysql = models.RandDSampleFinLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                                     ExperimentTimes=Build_finlib_num)  # DNA提取样本信息

        if button_name == 'ComputerSeq_audited':
            return render(request, "modelspage/RandDComSeqTaskDetails.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'ModifyData':
            temp_userlist = User.objects.filter(first_name='研发部')
            return render(request, "modelspage/RandDComSeqTaskAssModifyData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
