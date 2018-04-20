# encoding: utf-8

from django.shortcuts import render
from AnchorDxLimsApp import models
from time import strftime,gmtime
from itertools import chain
import time,httplib,datetime
# Create your views here.
#coding:utf-8

from django.shortcuts import render,HttpResponse


# 研发样本任务待财务审核信息详情页
def task_Fin_unaud (request):
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
            print 'Pass患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('Fin_unaud_sam_code_num')
            print 'Pass样本条码号: ', sam_code_num

        # 从数据里取出某条记录
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_mysql = models.clinicalSampleInfo.objects.filter(sam_code_num=sam_code_num)

        return render(request, "modelspage/clinicalSampleInfoPassInfo.html",
                      {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                       "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 合同信息不通过审核信息详情页
def contract_To_Examine_Not_Pass(request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        if request.method == "POST":
            print 'Pass患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print 'Pass样本条码号: ', sam_code_num

            # 实验次数
            contract_Times = request.POST.get('contract_Times')
            print '实验次数: ', contract_Times

            # 从数据里取出某条记录
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            temp_mysql = models.clinicalSampleInfo.objects.get(sam_code_num=sam_code_num)
            temp_contractReviewInfo = models.contractReviewInfo.objects.filter(sam_code_num=sam_code_num,
                                                                               ExperimentTimes=contract_Times)  # 临床样本未审核信息

            return render(request, "modelspage/contract_Review_NoPassInfo.html",
                          {"data": temp_mysql, "temp_contractReviewInfo": temp_contractReviewInfo, "userinfo": temp,
                           "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 研发样本已暂停任务信息详情页
def RandDSampleTaskSuspendInfo (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息

        sam_code_num = ''
        Next_TaskProgress = ''  # 下一步任务进度
        ExperimentTimes = '' # 实验次数
        if request.method == "POST":
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号: ', sam_code_num

            # 下一步任务进度
            Next_TaskProgress = request.POST.get('Next_TaskProgress')
            print '下一步任务进度: ', Next_TaskProgress

            # 实验次数
            ExperimentTimes = request.POST.get('ExperimentTimes')
            print '实验次数: ', ExperimentTimes

        if Next_TaskProgress == request.POST.get('Pretreatment'):
            print '下一步进行样本预处理'
            # 从数据里取出某条记录
            temp_mysql = models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num)  # 样本信息
            return render(request, "modelspage/RandDSamplePretreatmentTaskSuspend.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif Next_TaskProgress == request.POST.get('DNA_extraction'):
            print '下一步进行DNA提取'
            # 从数据里取出某条记录
            temp_RandDSampleInfo = models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num)
            temp_RandDSamplePretreatmentInfo = models.RandDSamplePretreatmentInfo.objects.filter(
                sam_code_num=sam_code_num)
            if len(temp_RandDSamplePretreatmentInfo) == 0:
                TaskProgress = '样本登记'
                TaskDetails = models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num)
            else:
                TaskProgress = '样本预处理'
                TaskDetails = models.RandDSamplePretreatmentInfo.objects.filter(sam_code_num=sam_code_num)
            return render(request, "modelspage/RandDSampleDNAExtractTaskSuspend.html",
                          {"data": temp_RandDSampleInfo, "userinfo": temp, "myInfo": temp_myInfo,
                           "TaskProgress": TaskProgress,
                           "RandDSamplePretreatmentInfo": temp_RandDSamplePretreatmentInfo,
                           "TaskDetails": TaskDetails, "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif Next_TaskProgress == request.POST.get('PreLibCon'):
            print '下一步进行预文库构建'
            # 从数据里取出某条记录
            temp_mysql = models.RandDSampleDNAExtractInfo.objects.filter(sam_code_num=sam_code_num,
                                                              ExperimentTimes=ExperimentTimes)   # DNA提取信息
            return render(request, "modelspage/RandDSamplePreLibConTaskSuspend.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif Next_TaskProgress == request.POST.get('FinLibCon'):
            print '下一步进行终文库构建'
            # 从数据里取出某条记录
            temp_mysql = models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                              ExperimentTimes=ExperimentTimes)  # 预文库构建
            return render(request, "modelspage/RandDSampleFinLibConTaskSuspend.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif Next_TaskProgress == request.POST.get('ComSeq'):
            print '下一步进行上机测序'
            # 从数据里取出某条记录
            temp_mysql = models.RandDSampleFinLibConInfo.objects.filter(sam_code_num=sam_code_num,
                                                              ExperimentTimes=ExperimentTimes)  # 终文库构建信息
            return render(request, "modelspage/RandDSampleComSeqTaskSuspend.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 已暂停的样本恢复操作
def RandD_Recovery_Task_Operation (request):
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
            taskTime = ''  # 任务分配时间
            TaskProgress = '' # 任务进度
            Next_TaskProgress = ''  # 下一步任务'
            if request.method == "POST":
                # 样本条码号
                sam_code_num = request.POST.get('sam_code_num')
                print '样本编号: ', sam_code_num

                # 判断哪个按钮提交的数据
                # 判断哪个按钮提交的数据
                if request.POST.has_key('recoveryTask'):
                    button_name = 'recoveryTask'
                    # 下一步任务
                    Next_TaskProgress = request.POST.get('Next_TaskProgress')
                    print '下一步任务: ', Next_TaskProgress
                elif request.POST.has_key('Stop_recoveryTask'):
                    button_name = 'recoveryTask'
                    # 下一步任务
                    Next_TaskProgress = request.POST.get('Stop_Next_TaskProgress')
                    print '下一步任务: ', Next_TaskProgress

            # 修改数据库合同信息状态
            if button_name == 'recoveryTask':
                # 任务恢复
                if Next_TaskProgress == request.POST.get('Pretreatment'):
                    print '下一步进行样本预处理'
                    models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(
                        Next_TaskProgress_Sign='0',
                        Next_TaskProgress_Man=TaskReceiver,
                        Next_TaskProgress_Remarks=taskRemarks,
                        Next_TaskProgress_Time=taskTime,
                    )
                elif Next_TaskProgress == request.POST.get('DNA_extraction'):
                    print '下一步进行DNA提取'
                    temp_RandDSamplePretreatmentInfo = models.RandDSamplePretreatmentInfo.objects.filter(
                        sam_code_num=sam_code_num)
                    if len(temp_RandDSamplePretreatmentInfo) == 0:
                        models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(
                            Next_TaskProgress_Sign='0',
                            Next_TaskProgress_Man=TaskReceiver,
                            Next_TaskProgress_Remarks=taskRemarks,
                            Next_TaskProgress_Time=taskTime,
                        )
                    else:
                        models.RandDSamplePretreatmentInfo.objects.filter(sam_code_num=sam_code_num).update(
                            Next_TaskProgress_Sign='0',
                            Next_TaskProgress_Man=TaskReceiver,
                            Next_TaskProgress_Remarks=taskRemarks,
                            Next_TaskProgress_Time=taskTime,
                        )
                elif Next_TaskProgress == request.POST.get('PreLibCon'):
                    print '下一步进行预文库构建'
                    DNA_extraction_num = request.POST.get('DNA_extraction_num')
                    models.RandDSampleDNAExtractInfo.objects.filter(sam_code_num=sam_code_num, ExperimentTimes=DNA_extraction_num).update(
                        Next_TaskProgress_Sign='0',
                        Next_TaskProgress_Man=TaskReceiver,
                        Next_TaskProgress_Remarks=taskRemarks,
                        Next_TaskProgress_Time=taskTime,
                        Next_TaskProgress=TaskProgress,
                    )

                elif Next_TaskProgress == request.POST.get('FinLibCon'):
                    print '下一步进行终文库构建'
                    task_num = request.POST.get('Build_lib_num')
                    models.RandDSamplePreLibConInfo.objects.filter(sam_code_num=sam_code_num, ExperimentTimes=task_num).update(
                        Next_TaskProgress_Sign='0',
                        Next_TaskProgress_Man=TaskReceiver,
                        Next_TaskProgress_Remarks=taskRemarks,
                        Next_TaskProgress_Time=taskTime,
                        Next_TaskProgress=TaskProgress,
                    )

                elif Next_TaskProgress == request.POST.get('ComSeq'):
                    print '下一步进行上机测序'
                    Build_finlib_num = request.POST.get('Build_finlib_num')
                    models.RandDSampleFinLibConInfo.objects.filter(sam_code_num=sam_code_num, ExperimentTimes=Build_finlib_num).update(
                        Next_TaskProgress_Sign='0',
                        Next_TaskProgress_Man=TaskReceiver,
                        Next_TaskProgress_Remarks=taskRemarks,
                        Next_TaskProgress_Time=taskTime,
                        Next_TaskProgress=TaskProgress,
                    )

            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
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
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            return render(request, "modelspage/PermissionsPrompt.html",
                          {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 研发样本已终止任务信息详情页
def RandDTaskStop (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        sam_code_num = ''
        Next_TaskProgress = ''  # 下一步任务
        DNA_extraction_num = 0  # DNA提取实验次数
        Build_Prelib_num = 0  # 预文库构建实验次数
        Build_finlib_num = 0  # 终文库构建实验次数
        # ComSeq_num = 0  # 上机测序实验次数
        Pretreatment_Sing = 0 # 预处理标志
        if request.method == "POST":
            print '患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号: ', sam_code_num
            # 下一步任务
            Next_TaskProgress = request.POST.get('Next_TaskProgress')
            print '下一步任务: ', Next_TaskProgress
            # DNA提取实验次数
            DNA_extraction_num = request.POST.get('DNA_extraction_num')
            print 'DNA提取实验次数: ', DNA_extraction_num
            # 预文库构建实验次数
            Build_Prelib_num = request.POST.get('Build_Prelib_num')
            print '预文库构建实验次数: ', Build_Prelib_num
            # 终文库构建实验次数
            Build_finlib_num = request.POST.get('Build_finlib_num')
            print '终文库构建实验次数: ', Build_finlib_num
            # 上机测序实验次数
            # ComSeq_num = request.POST.get('ComSeq_num')
            # print '上机测序实验次数: ', ComSeq_num
        if Next_TaskProgress == request.POST.get('PreLibCon'):
            DNA_extraction_num = request.POST.get('ExperimentTimes')
        elif Next_TaskProgress == request.POST.get('FinLibCon'):
            Build_Prelib_num = request.POST.get('ExperimentTimes')
        elif Next_TaskProgress == request.POST.get('ComSeq'):
            Build_finlib_num = request.POST.get('ExperimentTimes')

        temp_RandDSamplePretreatmentInfo = models.RandDSamplePretreatmentInfo.objects.filter(
            sam_code_num=sam_code_num)
        if len(temp_RandDSamplePretreatmentInfo) == 0:
            Pretreatment_Sing = 0
        else:
            Pretreatment_Sing = 1

        # 从数据里取出某条记录
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_RandDSampleInfo_stop = models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num)  # 收样信息
        temp_RandDPretreatment_stop = models.RandDSamplePretreatmentInfo.objects.filter(
            sam_code_num=sam_code_num)  # 样本预处理信息
        temp_RandDDNAExtractInfo_stop = models.RandDSampleDNAExtractInfo.objects.filter(
            sam_code_num=sam_code_num,
            ExperimentTimes=DNA_extraction_num)  # DNA提取信息
        temp_RandDPreLibConInfo_stop = models.RandDSamplePreLibConInfo.objects.filter(
            sam_code_num=sam_code_num,
            ExperimentTimes=Build_Prelib_num)  # 预文库构建信息
        temp_RandDFinLibConInfo_stop = models.RandDSampleFinLibConInfo.objects.filter(
            sam_code_num=sam_code_num,
            ExperimentTimes=Build_finlib_num)  # 终文库构建信息

        return render(request, "modelspage/RandDTaskStopInfo.html",
                      {"userinfo": temp, "Next_TaskProgress": Next_TaskProgress,
                       "temp_RandDSampleInfo_stop": temp_RandDSampleInfo_stop,
                       "temp_RandDPretreatment_stop": temp_RandDPretreatment_stop,
                       "temp_RandDDNAExtractInfo_stop": temp_RandDDNAExtractInfo_stop,
                       "temp_RandDPreLibConInfo_stop": temp_RandDPreLibConInfo_stop,
                       "temp_RandDFinLibConInfo_stop": temp_RandDFinLibConInfo_stop,
                       "myInfo": temp_myInfo,
                       "Pretreatment_Sing": Pretreatment_Sing,
                       "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})
