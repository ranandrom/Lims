# encoding: utf-8

from django.shortcuts import render
from AnchorDxLimsApp import models
from itertools import chain
# Create your views here.
#coding:utf-8

from django.shortcuts import render,HttpResponse

# 临床样本审核首页
def sample_Review(request):
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

        if department == '管理员':
            temp_not_audited = models.clinicalSampleInfo.objects.filter(sample_review=0)  # 临床样本未审核信息
        else:
            temp_not_audited = models.clinicalSampleInfo.objects.filter(SampleAuditor=username, sample_review=0)  # 临床样本未审核信息
        temp_pass = models.clinicalSampleInfo.objects.filter(sample_review=1)  # 临床样本已通过审核信息
        temp_return = models.clinicalSampleInfo.objects.filter(sample_review=4)  # 临床样本已退回信息
        temp_Suspend = models.clinicalSampleInfo.objects.filter(sample_review=2)  # 临床样本暂停任务信息
        temp_not_pass = models.clinicalSampleInfo.objects.filter(sample_review=3)  # 临床样本终止任务信息

        return render(request, "modelspage/sample_review.html",
                      {"userinfo": temp, "data": temp_not_audited, "pass": temp_pass, "return": temp_return,
                       "Suspend": temp_Suspend, "Not_pass": temp_not_pass, "myInfo": temp_myInfo,
                       "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 临床样本实验任务分配页
def clinical_Experimental_Task_Assignment(request):
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

        # 预处理任务列表
        # Pretreatment_not_audited = models.clinicalSampleInfo.objects.filter(Next_TaskProgress_Sign=0)  # 任务未分配信息
        # Pretreatment_audited = models.clinicalSampleInfo.objects.filter(Next_TaskProgress_Sign=1)  # 任务已分配信息
        Pretreatment_not_audited = models.clinicalSampleInfo.objects.filter(Next_TaskProgress_Sign=0,
                                                                            sample_review=1,
                                                                            TissueSampleSign=0)  # 任务未分配信息
        Pretreatment_audited = models.clinicalSampleInfo.objects.filter(Next_TaskProgress_Sign=1, sample_review=1,
                                                                        TissueSampleSign=0)  # 任务已分配信息

        # DNA提取任务列表
        # DNA_not_audited = models.clinicalSamplePretreatment.objects.filter(Next_TaskProgress_Sign=0)  # 任务未分配信息
        # DNA_audited = models.clinicalSamplePretreatment.objects.filter(Next_TaskProgress_Sign=1)  # 任务已分配信息
        temp_not_Pretreatment = models.clinicalSampleInfo.objects.filter(Next_TaskProgress_Sign=0, sample_review=1,
                                                                         TissueSampleSign=1)  # 任务未分配信息
        temp_Pretreatment = models.clinicalSamplePretreatment.objects.filter(Next_TaskProgress_Sign=0)  # 任务未分配信息
        DNA_not_audited = chain(temp_not_Pretreatment, temp_Pretreatment)  # 合并所有数据表数据

        temp_not_Pretreatment_audited = models.clinicalSampleInfo.objects.filter(Next_TaskProgress_Sign=1,
                                                                                 sample_review=1,
                                                                                 TissueSampleSign=1)  # 任务已分配信息
        temp_Pretreatment_audited = models.clinicalSamplePretreatment.objects.filter(
            Next_TaskProgress_Sign=1)  # 任务已分配信息
        DNA_audited = chain(temp_not_Pretreatment_audited, temp_Pretreatment_audited)  # 合并所有数据表数据

        # 预文库构建任务列表
        temp_Fin_unaud = models.clinicalSampleInfo.objects.filter(contract_review=0, sample_review=1, )  # 财务未审核信息
        temp_Fin_NoPass = models.clinicalSampleInfo.objects.filter(contract_review=2, sample_review=1)  # 财务审核不通过信息
        PreLibCon_not_audited = models.DNAExtractInfo.objects.filter(Next_TaskProgress_Sign=0)  # 任务未分配信息
        PreLibCon_audited = models.DNAExtractInfo.objects.filter(Next_TaskProgress_Sign=1)  # 任务已分配信息

        # 终文库构建任务列表
        FinLibCon_not_audited = models.PreLibConInfo.objects.filter(Next_TaskProgress_Sign=0)  # 任务未分配信息
        FinLibCon_audited = models.PreLibConInfo.objects.filter(Next_TaskProgress_Sign=1)  # 任务已分配信息

        # 上机测序任务列表
        ComputerSeq_not_audited = models.FinLibConInfo.objects.filter(Next_TaskProgress_Sign=0)  # 任务未分配信息
        ComputerSeq_audited = models.FinLibConInfo.objects.filter(Next_TaskProgress_Sign=1)  # 任务已分配信息

        # 其他信息列表
        # 任务暂停信息
        temp_Pretreatment = models.clinicalSampleInfo.objects.filter(Next_TaskProgress_Sign=2,
                                                                     sample_review=1)  # 预处理任务暂停信息
        temp_DNAExtract = models.clinicalSamplePretreatment.objects.filter(Next_TaskProgress_Sign=2)  # DNA提取任务暂停信息
        temp_PreLibCon = models.DNAExtractInfo.objects.filter(Next_TaskProgress_Sign=2)  # 预文库构建任务暂停信息
        temp_FinLibCon = models.PreLibConInfo.objects.filter(Next_TaskProgress_Sign=2)  # 终文库构建任务暂停信息
        temp_SeqCom = models.FinLibConInfo.objects.filter(Next_TaskProgress_Sign=2)  # 上机测序任务暂停信息
        temp_suspend = chain(temp_Pretreatment, temp_DNAExtract, temp_PreLibCon, temp_FinLibCon,
                             temp_SeqCom)  # 合并所有数据表数据
        # 任务终止信息
        # temp_stop = models.clinicalSampleInfo.objects.filter(Next_TaskProgress_Sign=3)  # 任务终止信息
        temp_Pretreatment_stop = models.clinicalSampleInfo.objects.filter(Next_TaskProgress_Sign=3,
                                                                          sample_review=1)  # 预处理任务终止信息
        temp_DNAExtract_stop = models.clinicalSamplePretreatment.objects.filter(Next_TaskProgress_Sign=3)  # DNA提取任务终止信息
        temp_PreLibCon_stop = models.DNAExtractInfo.objects.filter(Next_TaskProgress_Sign=3)  # 预文库构建任务终止信息
        temp_FinLibCon_stop = models.PreLibConInfo.objects.filter(Next_TaskProgress_Sign=3)  # 终文库构建任务终止信息
        temp_SeqCom_stop = models.FinLibConInfo.objects.filter(Next_TaskProgress_Sign=3)  # 上机测序任务终止信息
        temp_stop = chain(temp_Pretreatment_stop, temp_DNAExtract_stop, temp_PreLibCon_stop, temp_FinLibCon_stop,
                          temp_SeqCom_stop)  # 合并所有数据表数据

        return render(request, "modelspage/clinicalExperimentalTaskAssignment.html", {"userinfo": temp,
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