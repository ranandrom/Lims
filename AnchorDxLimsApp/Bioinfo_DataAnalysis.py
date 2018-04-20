# encoding: utf-8

from django.shortcuts import render
from AnchorDxLimsApp import models
from django.contrib.auth.models import User
from time import strftime,gmtime
from itertools import chain
import time,httplib,datetime
from AnchorDxLimsApp.views import sendEmail
# Create your views here.
#coding:utf-8

from django.shortcuts import render,HttpResponse

# 数据分析任务列表
def DataAnalysisTask_Review(request):
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
        temp_unfinished = models.ComputerSeqInfo.objects.filter(Bioinfo_Sign=0, ReviewResult='通过',
                                                                Next_TaskProgress_Sign='1')  # 临检样本
        temp_RandD_unfinished = models.RandDSampleComputerSeqInfo.objects.filter(Bioinfo_Sign=0, ReviewResult='通过',
                                                                                 Next_TaskProgress_Sign='1')  # 研发样本
        temp_finished = models.BioinfoDataAnalysisInfo.objects.all()

        return render(request, "modelspage/BioinfoTaskReview.html",
                      {"userinfo": temp, "unfinished": temp_unfinished,
                       "RandD_unfinished": temp_RandD_unfinished,
                       "finished": temp_finished, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 数据分析信息录入页
def DataAnalysisTask_To_Examine (request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        sam_code_num = ''
        Computer_Seq_num = ''
        button_name = ''
        if request.method == "POST":
            print '患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号: ', sam_code_num
            # 上机测序实验次数
            Computer_Seq_num = request.POST.get('Computer_Seq_num')
            print '上机测序实验次数: ', Computer_Seq_num

        # 从数据里取出某条记录
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        # 判断哪个按钮提交的数据
        if request.POST.has_key('ClinSample'):
            button_name = 'ClinSample'
        elif request.POST.has_key('RandDSample'):
            button_name = 'RandDSample'

        if button_name == 'ClinSample':
            temp_mysql = models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                               ExperimentTimes=Computer_Seq_num)

            return render(request, "modelspage/BioinfoTask_submit.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'RandDSample':
            temp_mysql = models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                          ExperimentTimes=Computer_Seq_num)

            return render(request, "modelspage/RandDSampleBioinfoTaskInfoInput.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread, "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 数据分析结果录入到数据库
def DataAnalysisInfoToDataBases(request):
    # 样本信息
    sam_code_num = ''  # 样本条码号
    ExperimentNumber = ''  # 实验编号
    # 数据分析信息
    DataQquality = ''  # 数据质量
    Effective_sequencing_depth = ''  # 有效测序深度
    SequencingFileName = '' # Sequencing file name
    QC_Result = ''  # QC result
    Path_To_Sorted_Deduped_Bam = ''  # Path to sorted.deduped.bam
    Analyser = ''  # 分析人
    AnalysisTime = ''  # 分析时间（系统默认）
    AnalysisRemarks = ''  # 其它（备注）
    # 其他信息
    DNA_extraction_num = ''  # DNA提取实验次数
    Build_Prelib_num = ''  # 预文库构建实验次数
    Build_finlib_num = ''  # 终文库构建实验次数
    Computer_Seq_num = ''  # 上机测序实验次数
    SampleSource = ''  # 样本来源
    button_name = ''
    if request.method == "POST":
        print '样本信息: ============================================= '
        # 样本条码号
        sam_code_num = request.POST.get('sam_code_num')
        print '样本条码号: ', sam_code_num

        # 判断哪个按钮提交的数据
        if request.POST.has_key('ClinSampleDetermine'):
            button_name = 'ClinSample'
            SampleSource = '临检样本'  # 样本来源
        elif request.POST.has_key('RandDSampleDetermine'):
            button_name = 'RandDSample'
            SampleSource = '研发样本'  # 样本来源
        elif request.POST.has_key('submitModify'):
            button_name = 'submitModify'

        if button_name == 'ClinSample':
            # 实验编号
            ExperimentNumber = request.POST.get('ExperimentNumber')
            print '实验编号: ', ExperimentNumber

        print '其他信息: ============================================= '
        # DNA提取实验次数
        DNA_extraction_num = request.POST.get('DNA_extraction_num')
        print 'DNA提取实验次数: ', DNA_extraction_num

        # 预文库构建实验次数
        Build_Prelib_num = request.POST.get('Build_Prelib_num')
        print '预文库构建实验次数: ', Build_Prelib_num

        # 终文库构建次数
        Build_finlib_num = request.POST.get('Build_finlib_num')
        print '终文库构建次数: ', Build_finlib_num

        # 上机测序实验次数
        Computer_Seq_num = request.POST.get('Computer_Seq_num')
        print '上机测序实验次数: ', Computer_Seq_num

        print '数据分析信息: ============================================= '
        # 数据质量
        DataQquality = request.POST.get('DataQquality')
        print '数据质量: ', DataQquality

        # 有效测序深度
        Effective_sequencing_depth = request.POST.get('Effective_sequencing_depth')
        print '有效测序深度: ', Effective_sequencing_depth

        # Sequencing file name
        SequencingFileName = request.POST.get('SequencingFileName')
        print 'Sequencing file name: ', SequencingFileName

        # QC result
        QC_Result = request.POST.get('QC_Result')
        print 'QC result: ', QC_Result

        # Path to sorted.deduped.bam
        Path_To_Sorted_Deduped_Bam = request.POST.get('Path_To_Sorted_Deduped_Bam')
        print 'Path to sorted.deduped.bam: ', Path_To_Sorted_Deduped_Bam

        # 分析人
        Analyser = request.POST.get('Next_TaskProgress_Man')
        print '分析人: ', Analyser

        # 分析时间
        AnalysisTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print '分析时间: ', AnalysisTime

        # 其它（备注）
        AnalysisRemarks = request.POST.get('AnalysisRemarks')
        print '其它（备注）: ', AnalysisRemarks

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
        if temp_UserOperationPermissionsInfo.BioinfoDataAnalysisTaskReview == '1':
            if not button_name == 'submitModify':
                temp_Task = models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num)
                num = len(temp_Task)

                # 添加数据到数据库
                models.BioinfoDataAnalysisInfo.objects.create(
                    # 用户信息
                    username=username,  # 用户名
                    department=department,  # 部门
                    # 样本信息
                    sam_code_num=sam_code_num,  # 样本条码号
                    ExperimentNumber=ExperimentNumber,  # 实验编号
                    # 数据分析信息
                    DataQquality=DataQquality,  # 数据质量
                    Effective_sequencing_depth=Effective_sequencing_depth,  # 有效测序深度
                    SequencingFileName=SequencingFileName,  # Sequencing file name
                    QC_Result=QC_Result,  # QC result
                    Path_To_Sorted_Deduped_Bam=Path_To_Sorted_Deduped_Bam,  # Path to sorted.deduped.bam
                    Analyser=Analyser,  # 分析人
                    AnalysisTime=AnalysisTime,  # 分析时间（系统默认）
                    AnalysisRemarks=AnalysisRemarks,  # 其它（备注）
                    # 其他信息
                    DNA_extraction_num=DNA_extraction_num,  # DNA提取实验次数
                    Build_Prelib_num=Build_Prelib_num,  # 预文库构建实验次数
                    Build_finlib_num=Build_finlib_num,  # 终文库构建实验次数
                    Computer_Seq_num=Computer_Seq_num,  # 上机测序实验次数
                    SampleSource=SampleSource,  # 样本来源
                    DataAnalysis_num=num+1,  # 数据分析次数
                    Report_Make_Sign=0,  # 报告制作标记
                    BioinfoResult_Sign=0,  # 生信分析结果审核标记
                    Medical_Examine_Sign=0,  # 遗传咨询师审核标记
                    Operate_Examine_Sign=0,  # 运营审核标记
                    Report_Send_Sign=0,  # 报告发送标记
                )
                TaskReceiver = ''  # 接收者
                if button_name == 'ClinSample':
                    models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                          ExperimentTimes=Computer_Seq_num).update(Bioinfo_Sign='1')
                    sample = models.ComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                   ExperimentTimes=Computer_Seq_num)
                    TaskReceiver = sample[0].BioTaskAssignment
                elif button_name == 'RandDSample':
                    models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                     ExperimentTimes=Computer_Seq_num).update(
                        Bioinfo_Sign='1')
                    sample = models.RandDSampleComputerSeqInfo.objects.filter(sam_code_num=sam_code_num,
                                                                              ExperimentTimes=Computer_Seq_num)
                    TaskReceiver = sample[0].BioTaskAssignment

                # 添加系统消息
                taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                Title = '通知：样本生信分析结果审核任务'  # 系统消息标题
                Message = username + '分派给你一个样本生信分析结果审核任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
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
            else:
                # 数据分析次数
                DataAnalysis_num = request.POST.get('DataAnalysis_num')
                print '数据分析次数: ', DataAnalysis_num
                # 添加数据到数据库
                models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                              DataAnalysis_num=DataAnalysis_num).update(
                    # 数据分析信息
                    DataQquality=DataQquality,  # 数据质量
                    Effective_sequencing_depth=Effective_sequencing_depth,  # 有效测序深度
                    SequencingFileName=SequencingFileName,  # Sequencing file name
                    QC_Result=QC_Result,  # QC result
                    Path_To_Sorted_Deduped_Bam=Path_To_Sorted_Deduped_Bam,  # Path to sorted.deduped.bam
                    AnalysisTime=AnalysisTime,  # 分析时间（系统默认）
                    AnalysisRemarks=AnalysisRemarks,  # 其它（备注）
                )

            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            temp_unfinished = models.ComputerSeqInfo.objects.filter(Bioinfo_Sign=0, ReviewResult='通过',
                                                                    Next_TaskProgress_Sign='1')  # 临检样本
            temp_RandD_unfinished = models.RandDSampleComputerSeqInfo.objects.filter(Bioinfo_Sign=0, ReviewResult='通过',
                                                                                     Next_TaskProgress_Sign='1')  # 研发样本
            temp_finished = models.BioinfoDataAnalysisInfo.objects.all()

            return render(request, "modelspage/BioinfoTaskReview.html",
                          {"userinfo": temp, "unfinished": temp_unfinished,
                           "RandD_unfinished": temp_RandD_unfinished,
                           "finished": temp_finished, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
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

# 数据分析结果信息详情页
def DataAnalysisTask_ShowData (request):
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
        DataAnalysis_num = ''
        button_name = ''
        if request.method == "POST":
            print '患者信息: ============================================= '
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号: ', sam_code_num
            # 数据分析次数
            DataAnalysis_num = request.POST.get('DataAnalysis_num')
            print '数据分析次数: ', DataAnalysis_num

            # 判断哪个按钮提交的数据
            if request.POST.has_key('seeInfo'):
                button_name = 'seeInfo'
            elif request.POST.has_key('ModifyData'):
                button_name = 'ModifyData'
            elif request.POST.has_key('delete'):
                temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                    username=username)  # 用户操作权限信息
                # print 'ClinicalSampleRegistration: ', temp_UserOperationPermissionsInfo.ClinicalSampleRegistration
                if temp_UserOperationPermissionsInfo.BioinfoDataAnalysisTaskReview == '1':
                    models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                  DataAnalysis_num=DataAnalysis_num).delete()
                    temp_unfinished = models.ComputerSeqInfo.objects.filter(Bioinfo_Sign=0, ReviewResult='通过',
                                                                            Next_TaskProgress_Sign='1')  # 临检样本
                    temp_RandD_unfinished = models.RandDSampleComputerSeqInfo.objects.filter(Bioinfo_Sign=0,
                                                                                             ReviewResult='通过',
                                                                                             Next_TaskProgress_Sign='1')  # 研发样本
                    temp_finished = models.BioinfoDataAnalysisInfo.objects.all()

                    return render(request, "modelspage/BioinfoTaskReview.html",
                                  {"userinfo": temp, "unfinished": temp_unfinished,
                                   "RandD_unfinished": temp_RandD_unfinished,
                                   "finished": temp_finished, "myInfo": temp_myInfo,
                                   "SystemMessage": temp_SystemMessage_Unread,
                                   "num_SystemMessage_Unread": num_SystemMessage_Unread})
                else:
                    return render(request, "modelspage/PermissionsPrompt.html",
                                  {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                                   "num_SystemMessage_Unread": num_SystemMessage_Unread})

        temp_mysql = models.BioinfoDataAnalysisInfo.objects.filter(sam_code_num=sam_code_num,
                                                                   DataAnalysis_num=DataAnalysis_num)

        if button_name == 'seeInfo':
            return render(request, "modelspage/BioinfoTask_ShowData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'ModifyData':
            return render(request, "modelspage/BioinfoTask_ModifyData.html",
                          {"data": temp_mysql, "userinfo": temp, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
