# encoding: utf-8

from django.shortcuts import render
from AnchorDxLimsApp import models
from itertools import chain
# Create your views here.
#coding:utf-8

from django.shortcuts import render,HttpResponse

# 研发样本实验任务分配首页
def RandDExperimentalTaskAssignmentHomePage(request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)

        # 预处理任务列表
        Pretreatment_not_audited = models.RandDSampleInfo.objects.filter(Next_TaskProgress_Sign=0, sample_review='1',
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
        ComputerSeq_not_audited = models.RandDSampleFinLibConInfo.objects.filter(Next_TaskProgress_Sign=0)  # 任务未分配信息
        ComputerSeq_audited = models.RandDSampleFinLibConInfo.objects.filter(Next_TaskProgress_Sign=1)  # 任务已分配信息

        # 其他信息列表
        # 任务暂停信息
        temp_Pretreatment = models.RandDSampleInfo.objects.filter(Next_TaskProgress_Sign=2, sample_review='1')  # 预处理任务暂停信息
        temp_DNAExtract = models.RandDSamplePretreatmentInfo.objects.filter(Next_TaskProgress_Sign=2)  # DNA提取任务暂停信息
        temp_PreLibCon = models.RandDSampleDNAExtractInfo.objects.filter(Next_TaskProgress_Sign=2)  # 预文库构建任务暂停信息
        temp_FinLibCon = models.RandDSamplePreLibConInfo.objects.filter(Next_TaskProgress_Sign=2)  # 终文库构建任务暂停信息
        temp_SeqCom = models.RandDSampleFinLibConInfo.objects.filter(Next_TaskProgress_Sign=2)  # 上机测序任务暂停信息
        temp_suspend = chain(temp_Pretreatment, temp_DNAExtract, temp_PreLibCon, temp_FinLibCon, temp_SeqCom)  # 合并所有数据表数据
        # 任务终止信息
        # temp_stop = models.clinicalSampleInfo.objects.filter(Next_TaskProgress_Sign=3)  # 任务终止信息
        temp_Pretreatment_stop = models.RandDSampleInfo.objects.filter(Next_TaskProgress_Sign=3 , sample_review='1')  # 预处理任务终止信息
        temp_DNAExtract_stop = models.RandDSamplePretreatmentInfo.objects.filter(Next_TaskProgress_Sign=3)  # DNA提取任务终止信息
        temp_PreLibCon_stop = models.RandDSampleDNAExtractInfo.objects.filter(Next_TaskProgress_Sign=3)  # 预文库构建任务终止信息
        temp_FinLibCon_stop = models.RandDSamplePreLibConInfo.objects.filter(Next_TaskProgress_Sign=3)  # 终文库构建任务终止信息
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
