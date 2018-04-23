# encoding: utf-8

from django.shortcuts import render
from AnchorDxLimsApp import models
from django.contrib.auth.models import User
from django.core.mail import send_mail
import time,httplib,datetime
import os,xlrd
import json
from AnchorDxLimsApp.views import sendEmail
from itertools import chain
from django.http import StreamingHttpResponse
import sys
reload(sys)
sys.setdefaultencoding('utf8')
# Create your views here.
#coding:utf-8

from django.shortcuts import render,HttpResponse

# 研发样本登记首页
def RandDSampleInfoInputHomePage(request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户系统信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        if department == '管理员':
            temp_not_audited = models.RandDSampleInfo.objects.filter(sample_review=0)  # 研发样本未审核信息
            # print temp_not_audited
            temp_draft = models.RandDSampleInfo.objects.filter(sample_review='')  # 研发样本草稿信息
            temp_return = models.RandDSampleInfo.objects.filter(sample_review=4)  # 研发审核退回样本信息
            temp_audited = models.RandDSampleInfo.objects.filter(sample_review__in=[1, 2, 3])  # 研发样本已审核信息
        else:
            temp_not_audited = models.RandDSampleInfo.objects.filter(username=username, sample_review=0)  # 研发样本未审核信息
            temp_draft = models.RandDSampleInfo.objects.filter(username=username, sample_review='')  # 研发样本草稿信息
            temp_return = models.RandDSampleInfo.objects.filter(username=username, sample_review=4)  # 研发审核退回样本信息
            temp_audited = models.RandDSampleInfo.objects.filter(username=username, sample_review__in=[1, 2, 3])  # 研发样本已审核信息
        return render(request, "modelspage/RandDSampleRegisterHomePage.html",
                      {"userinfo": temp, "not_audited": temp_not_audited, "audited": temp_audited, "draft": temp_draft,
                       "return": temp_return, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 研发样本登记数据录入页
def RandDSampleInfoInputData(request):
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

        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户系统信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        if temp_UserOperationPermissionsInfo.RandDSampleInfoInputHomePage == '1':
            button_name = ''  # 按钮名字
            if request.method == "POST":
                # 判断哪个按钮提交的数据
                if request.POST.has_key('singleAddSample'):
                    button_name = 'singleAddSample'
                elif request.POST.has_key('batchAddSample'):
                    button_name = 'batchAddSample'
                elif request.POST.has_key('batchAddImport'):
                    button_name = 'batchAddImport'
                elif request.POST.has_key('upload'):
                    button_name = 'upload'

            temp_userlist = User.objects.filter(first_name='研发部')
            if button_name == 'singleAddSample':
                return render(request, "modelspage/RandDSampleRegisterSingleInput.html",
                              {"userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                               "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})
            elif button_name == 'batchAddImport':
                # print 'batchAddSample'
                return render(request, "modelspage/RandDSampleRegisterBatchImport.html",
                              {"userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                               "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})
            elif button_name == 'batchAddSample':
                # print 'batchAddSample'
                return render(request, "modelspage/RandDSampleRegisterBatchInput.html",
                              {"userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                               "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})
            elif button_name == 'upload':
                File_Name = ''
                dictData = {}
                dictClos = {}
                if request.method == "POST":  # 请求方法为POST时，进行处理  
                    myFile = request.FILES.get("myfile", None)  #  获取上传的文件，如果没有文件，则默认为None
                    # print myFile
                    if not myFile:
                        return HttpResponse("no files for upload!")
                    if not os.path.exists('./temporary'):
                        os.makedirs('./temporary')
                    File_Name = myFile.name
                    destination = open(os.path.join("./temporary", myFile.name), 'wb+')  #  打开特定的文件进行二进制的写操作
                    if myFile.multiple_chunks() == False:
                        # 使用myFile.read()
                        for read in myFile.read():  # 整个上传  
                            destination.write(read)
                    else:
                        # 使用myFile.chunks()
                        for chunk in myFile.chunks():  # 分块写入文件
                            destination.write(chunk)
                    destination.close()
                    # return HttpResponse("upload over!")
                # print Report_File_Name

                # 打开文件
                filename = './temporary/' + File_Name  # 要下载的文件路径
                workbook = xlrd.open_workbook(filename)
                # 获取所有sheet
                # print workbook.sheet_names()  # [u'sheet1', u'sheet2']
                # sheet2_name = workbook.sheet_names()[0]
                sheet_name = workbook.sheet_names()

                # 根据sheet索引或者名称获取sheet内容
                # sheet2 = workbook.sheet_by_index(0)  # sheet索引从0开始
                # sheet2 = workbook.sheet_by_name('sheet1')

                # sheet的名称，行数，列数
                # print sheet2.name, sheet2.nrows, sheet2.ncols

                # print sheet2.merged_cells
                # print sheet2.merged_cells[0][2]
                # print sheet2.cell_value(9,27)  #(9, 12, 27, 30)

                # for n in range(0, sheet2.nrows):
                #     rows = sheet2.row_values(n)  # 获取第n行内容
                #     for merged_cells in sheet2.merged_cells:
                #         if merged_cells[0] <= n and n < merged_cells[1]:
                #             # print '第', n, '行', merged_cells[2], '列到', merged_cells[3],'列为合并格！'
                #             for m in range(merged_cells[2], merged_cells[3]):
                #                 rows[m] = sheet2.cell_value(merged_cells[0], merged_cells[2])
                #             # print rows[m]
                #     print rows
                for name in sheet_name:
                    sheet2 = workbook.sheet_by_name(name)
                    dataList = []
                    num_cols = []
                    for n in range(0, sheet2.ncols):
                        # 获取单元格内容的数据类型
                        # ctype : 0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
                        # print sheet2.cell(1,0).ctype
                        cols = sheet2.col_values(n)  # 获取第n列内容
                        for merged_cells in sheet2.merged_cells:
                            if merged_cells[2] <= n and n < merged_cells[3]:
                                # print '第', n, '行', merged_cells[2], '列到', merged_cells[3],'列为合并格！'
                                for m in range(merged_cells[0], merged_cells[1]):
                                    cols[m] = sheet2.cell_value(merged_cells[0], merged_cells[2])
                                # print rows[m]
                        # print cols
                        strr = ''
                        for i in range(0, len(cols)):
                            strr += str(cols[i]) + '\n'

                        dataList.append(strr)
                        num_cols.append(n+1)

                    dictData[name] = dataList
                    dictClos[name] = num_cols

                # print dataList[0], dataList
                # for i in range(0, len(dataList)):
                #     print i, dataList[i][0]

                return render(request, "modelspage/RandDSampleRegisterBatchImport.html",
                              {"userinfo": temp, "myInfo": temp_myInfo, "userlist": temp_userlist,
                               "fileName": File_Name, "sheet_name": sheet_name,
                               "dictData": json.dumps(dictData), "dictClos": json.dumps(dictClos),
                               "SystemMessage": temp_SystemMessage_Unread,
                               "num_SystemMessage_Unread": num_SystemMessage_Unread})
        else:
            # temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            return render(request, "modelspage/PermissionsPrompt.html",
                          {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})

# 研发样本登记数据录入页
def RandDSampleInfoInputToDataBase(request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        # 样本编号
        sam_code_num = ''  # 样本编号
        old_sam_code_num = ''  # 旧样本编号
        # 医院信息
        HospitalForInspection = ''  # 送检医院
        Contacts = ''  # 联系人
        # 收样信息
        SamplingTime_Blood = ''  # 收样时间（血样）
        SamplingTime_Tissue = ''  # 收样时间（组织）
        Collector = ''  # 收样人
        # 项目信息
        InpatientNumber = ''  # 住院号
        PathologicalNumber = ''  # 病理号
        CorrelationNumber = ''  # 相关编号
        # 样本信息
        PatientName = ''  # 患者姓名
        PatientAge = ''  # 患者年龄（岁）
        PatientSex = ''  # 患者性别
        BloodSampleType = ''  # 血样类型
        BloodSamplingTime = ''  # 采血时间
        TissueSampleSources = ''  # 组织样本来源
        TissueQuantity = ''  # 组织数量
        TissueType = ''  # 组织类型
        TissueSampleProcessing = ''  # 组织样本处理方式
        # 临床信息
        OperationDate = ''  # 手术日期
        PathologicalInfo = ''  # 病理信息
        TNMStaging = ''  # TNM分期
        Stage = ''  # Stage
        MolecularDiagnosticInfo = ''  # 分子诊断信息
        Classification = ''  # 分类
        # 存放信息
        PlasmaUse = ''  # 血浆用途
        TissueUse = ''  # 组织用途
        PlasmaStoragePosition = ''  # 血浆存放位置
        TissueStoragePosition = ''  # 组织存放位置
        # 组织样本标记
        TissueSampleSign = ''  # 组织样本标记
        SampleAuditor = ''  # 样本审核人
        # 按钮名字
        button_name = ''  # 按钮名字
        sample_review = '' # 审核标记
        if request.method == "POST":
            # 样本编号
            sam_code_num = request.POST.get('sam_code_num')  # 样本编号
            old_sam_code_num = request.POST.get('old_sam_code_num')  # 旧样本编号
            # print '样本条码号: ', sam_code_num
            # 医院信息
            HospitalForInspection = request.POST.get('HospitalForInspection')  # 送检医院
            Contacts = request.POST.get('Contacts')  # 联系人
            # 收样信息
            SamplingTime_Blood = request.POST.get('SamplingTime_Blood')  # 收样时间（血样）
            SamplingTime_Tissue = request.POST.get('SamplingTime_Tissue')  # 收样时间（组织）
            # print '收样时间（组织）: ', SamplingTime_Tissue
            Collector = request.POST.get('Collector')  # 收样人
            # 项目信息
            InpatientNumber = request.POST.get('InpatientNumber')  # 住院号
            PathologicalNumber = request.POST.get('PathologicalNumber')  # 病理号
            CorrelationNumber = request.POST.get('CorrelationNumber')  # 相关编号
            # 样本信息
            PatientName = request.POST.get('PatientName')  # 患者姓名
            PatientAge = request.POST.get('PatientAge')  # 患者年龄（岁）
            PatientSex = request.POST.get('PatientSex')  # 患者性别
            BloodSampleType = request.POST.get('BloodSampleType')  # 血样类型
            BloodSamplingTime = request.POST.get('BloodSamplingTime')  # 采血时间
            TissueSampleSources = request.POST.get('TissueSampleSources')  # 组织样本来源
            TissueQuantity = request.POST.get('TissueQuantity')  # 组织数量
            TissueType = request.POST.get('TissueType')  # 组织类型
            TissueSampleProcessing = request.POST.get('TissueSampleProcessing')  # 组织样本处理方式
            # 临床信息
            OperationDate = request.POST.get('OperationDate')  # 手术日期
            PathologicalInfo = request.POST.get('PathologicalInfo')  # 病理信息
            TNMStaging = request.POST.get('TNMStaging')  # TNM分期
            Stage = request.POST.get('Stage')  # Stage
            MolecularDiagnosticInfo = request.POST.get('MolecularDiagnosticInfo')  # 分子诊断信息
            Classification = request.POST.get('Classification')  # 分类
            # 存放信息
            PlasmaUse = request.POST.get('PlasmaUse')  # 血浆用途
            TissueUse = request.POST.get('TissueUse')  # 组织用途
            PlasmaStoragePosition = request.POST.get('PlasmaStoragePosition')  # 血浆存放位置
            TissueStoragePosition = request.POST.get('TissueStoragePosition')  # 组织存放位置
            # 样本审核人
            SampleAuditor = request.POST.get('SampleAuditor')  # 样本审核人
            # 判断哪个按钮提交的数据
            if request.POST.has_key('singleAddSampleDraft'):
                button_name = 'singleAddSample'
                sample_review = ''
            elif request.POST.has_key('singleAddSample'):
                button_name = 'singleAddSample'
                sample_review = 0
            elif request.POST.has_key('batchAddSampleDraft'):
                button_name = 'batchAddSample'
                sample_review = ''
            elif request.POST.has_key('batchAddSample'):
                button_name = 'batchAddSample'
                sample_review = 0
            elif request.POST.has_key('saveDraft'):
                button_name = 'updata'
                sample_review = ''
            elif request.POST.has_key('submitReview'):
                button_name = 'updata'
                sample_review = 0
            elif request.POST.has_key('submitModify'):
                button_name = 'submitModify'

        temp_mySample = models.RandDSampleInfo.objects.all()  # 研发样本信息
        AlreadyExistedList = ''  # 重复样本编号列表
        Sample_list = []  ## 空列表
        for i in range(0, len(temp_mySample)):
            Sample_list.append(temp_mySample[i].sam_code_num)

        temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
            username=username)  # 用户操作权限信息
        if temp_UserOperationPermissionsInfo.RandDSampleInfoInputHomePage == '1':
            if button_name == 'singleAddSample':
                if sam_code_num not in Sample_list:
                    if SamplingTime_Tissue == '':
                        TissueSampleSign = 0  # 组织样本标记
                        # print '组织样本标记: ', TissueSampleSign
                    else:
                        TissueSampleSign = 1  # 组织样本标记
                        # print '组织样本标记: ', TissueSampleSign
                    # 添加数据到数据库
                    models.RandDSampleInfo.objects.create(
                        # 用户信息
                        username=username,  # 用户名
                        department=department,  # 部门
                        # 样本编号
                        sam_code_num=sam_code_num,  # 样本编号
                        # 医院信息
                        HospitalForInspection=HospitalForInspection,  # 送检医院
                        Contacts=Contacts,  # 联系人
                        # 收样信息
                        SamplingTime_Blood=SamplingTime_Blood,  # 收样时间（血样）
                        SamplingTime_Tissue=SamplingTime_Tissue,  # 收样时间（组织）
                        Collector=Collector,  # 收样人
                        # 项目信息
                        InpatientNumber=InpatientNumber, # 住院号
                        PathologicalNumber=PathologicalNumber,  # 病理号
                        CorrelationNumber=CorrelationNumber,  # 相关编号
                        # 样本信息
                        PatientName=PatientName,  # 患者姓名
                        PatientAge=PatientAge,  # 患者年龄（岁）
                        PatientSex=PatientSex,  # 患者性别
                        BloodSampleType=BloodSampleType,  # 血样类型
                        BloodSamplingTime=BloodSamplingTime,  # 采血时间
                        TissueSampleSources=TissueSampleSources,  # 组织样本来源
                        TissueQuantity=TissueQuantity,  # 组织数量
                        TissueType=TissueType,  # 组织类型
                        TissueSampleProcessing=TissueSampleProcessing,  # 组织样本处理方式
                        # 临床信息
                        OperationDate=OperationDate,  # 手术日期
                        PathologicalInfo=PathologicalInfo,  # 病理信息
                        TNMStaging=TNMStaging,  # TNM分期
                        Stage=Stage,  # Stage
                        MolecularDiagnosticInfo=MolecularDiagnosticInfo,  # 分子诊断信息
                        Classification=Classification,  # 分类
                        # 存放信息
                        PlasmaUse=PlasmaUse,  # 血浆用途
                        TissueUse=TissueUse,  # 组织用途
                        PlasmaStoragePosition=PlasmaStoragePosition,  # 血浆存放位置
                        TissueStoragePosition=TissueStoragePosition,  # 组织存放位置
                        # 审核标记
                        sample_review=sample_review,  # 样本审核标记
                        Pretreatment_Sign=0,  # 样本预处理标记
                        DNAExtract_Sign=0,  # DNA提取任务标记
                        # task_assignment=0,  # 样本任务分派标记
                        # 组织样本标记
                        TissueSampleSign=TissueSampleSign,  # 组织样本标记
                        SampleAuditor=SampleAuditor,  # 样本审核人
                    )

                    if not sample_review == '':
                        # 添加系统消息
                        taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        Title = '通知：研发样本审核任务'  # 系统消息标题
                        Message = username + '录入一个研发样本！样本编号为：' + sam_code_num + '。请尽快完成审核！'  # 系统邮件正文
                        models.UserSystemMessage.objects.create(
                            # 用户信息
                            Sender=username,  # 发送者
                            Receiver=SampleAuditor,  # 接收者
                            # 信息内容
                            Time=taskTime,  # 信息生成时间
                            Title=Title,  # 系统消息标题
                            Message=Message,  # 系统消息正文
                            ReadingState='未读',  # 信息阅读状态
                        )
                        sendEmail(SampleAuditor, Title, Message)  # 发送邮件通知
                else:
                    AlreadyExistedList = sam_code_num
                    # print sam_code_num + '已存在！'
            elif button_name == 'updata':
                isupdata = 0
                if not sam_code_num == old_sam_code_num:
                    if sam_code_num in Sample_list:
                        isupdata = 1

                if isupdata == 0:
                    if SamplingTime_Tissue == '':
                        TissueSampleSign = 0  # 组织样本标记
                        # print '组织样本标记: ', TissueSampleSign
                    else:
                        TissueSampleSign = 1  # 组织样本标记
                        # print '组织样本标记: ', TissueSampleSign
                    # 添加数据到数据库
                    models.RandDSampleInfo.objects.filter(sam_code_num=old_sam_code_num).update(
                        # 用户信息
                        username=username,  # 用户名
                        department=department,  # 部门
                        # 样本编号
                        sam_code_num=sam_code_num,  # 样本编号
                        # 医院信息
                        HospitalForInspection=HospitalForInspection,  # 送检医院
                        Contacts=Contacts,  # 联系人
                        # 收样信息
                        SamplingTime_Blood=SamplingTime_Blood,  # 收样时间（血样）
                        SamplingTime_Tissue=SamplingTime_Tissue,  # 收样时间（组织）
                        Collector=Collector,  # 收样人
                        # 项目信息
                        InpatientNumber=InpatientNumber, # 住院号
                        PathologicalNumber=PathologicalNumber,  # 病理号
                        CorrelationNumber=CorrelationNumber,  # 相关编号
                        # 样本信息
                        PatientName=PatientName,  # 患者姓名
                        PatientAge=PatientAge,  # 患者年龄（岁）
                        PatientSex=PatientSex,  # 患者性别
                        BloodSampleType=BloodSampleType,  # 血样类型
                        BloodSamplingTime=BloodSamplingTime,  # 采血时间
                        TissueSampleSources=TissueSampleSources,  # 组织样本来源
                        TissueQuantity=TissueQuantity,  # 组织数量
                        TissueType=TissueType,  # 组织类型
                        TissueSampleProcessing=TissueSampleProcessing,  # 组织样本处理方式
                        # 临床信息
                        OperationDate=OperationDate,  # 手术日期
                        PathologicalInfo=PathologicalInfo,  # 病理信息
                        TNMStaging=TNMStaging,  # TNM分期
                        Stage=Stage,  # Stage
                        MolecularDiagnosticInfo=MolecularDiagnosticInfo,  # 分子诊断信息
                        Classification=Classification,  # 分类
                        # 存放信息
                        PlasmaUse=PlasmaUse,  # 血浆用途
                        TissueUse=TissueUse,  # 组织用途
                        PlasmaStoragePosition=PlasmaStoragePosition,  # 血浆存放位置
                        TissueStoragePosition=TissueStoragePosition,  # 组织存放位置
                        # 审核标记
                        sample_review=sample_review,  # 样本审核标记
                        Pretreatment_Sign=0,  # 样本预处理标记
                        DNAExtract_Sign=0,  # DNA提取任务标记
                        # task_assignment=0,  # 样本任务分派标记
                        # 组织样本标记
                        TissueSampleSign=TissueSampleSign,  # 组织样本标记
                        SampleAuditor=SampleAuditor,  # 样本审核人
                    )

                    if not sample_review == '':
                        # 添加系统消息
                        taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        Title = '通知：研发样本审核任务'  # 系统消息标题
                        Message = username + '录入一个研发样本！样本编号为：' + sam_code_num + '。请尽快完成审核！'  # 系统邮件正文
                        models.UserSystemMessage.objects.create(
                            # 用户信息
                            Sender=username,  # 发送者
                            Receiver=SampleAuditor,  # 接收者
                            # 信息内容
                            Time=taskTime,  # 信息生成时间
                            Title=Title,  # 系统消息标题
                            Message=Message,  # 系统消息正文
                            ReadingState='未读',  # 信息阅读状态
                        )
                        sendEmail(SampleAuditor, Title, Message)  # 发送邮件通知
                else:
                    AlreadyExistedList = sam_code_num
                    # print sam_code_num + '已存在！'
            elif button_name == 'submitModify':
                isupdata = 0
                if not sam_code_num == old_sam_code_num:
                    if sam_code_num in Sample_list:
                        isupdata = 1

                if isupdata == 0:
                    if SamplingTime_Tissue == '':
                        TissueSampleSign = 0  # 组织样本标记
                        # print '组织样本标记: ', TissueSampleSign
                    else:
                        TissueSampleSign = 1  # 组织样本标记
                        # print '组织样本标记: ', TissueSampleSign
                    # 添加数据到数据库
                    models.RandDSampleInfo.objects.filter(sam_code_num=old_sam_code_num).update(
                        # 样本编号
                        sam_code_num=sam_code_num,  # 样本编号
                        # 医院信息
                        HospitalForInspection=HospitalForInspection,  # 送检医院
                        Contacts=Contacts,  # 联系人
                        # 收样信息
                        SamplingTime_Blood=SamplingTime_Blood,  # 收样时间（血样）
                        SamplingTime_Tissue=SamplingTime_Tissue,  # 收样时间（组织）
                        Collector=Collector,  # 收样人
                        # 项目信息
                        InpatientNumber=InpatientNumber,  # 住院号
                        PathologicalNumber=PathologicalNumber,  # 病理号
                        CorrelationNumber=CorrelationNumber,  # 相关编号
                        # 样本信息
                        PatientName=PatientName,  # 患者姓名
                        PatientAge=PatientAge,  # 患者年龄（岁）
                        PatientSex=PatientSex,  # 患者性别
                        BloodSampleType=BloodSampleType,  # 血样类型
                        BloodSamplingTime=BloodSamplingTime,  # 采血时间
                        TissueSampleSources=TissueSampleSources,  # 组织样本来源
                        TissueQuantity=TissueQuantity,  # 组织数量
                        TissueType=TissueType,  # 组织类型
                        TissueSampleProcessing=TissueSampleProcessing,  # 组织样本处理方式
                        # 临床信息
                        OperationDate=OperationDate,  # 手术日期
                        PathologicalInfo=PathologicalInfo,  # 病理信息
                        TNMStaging=TNMStaging,  # TNM分期
                        Stage=Stage,  # Stage
                        MolecularDiagnosticInfo=MolecularDiagnosticInfo,  # 分子诊断信息
                        Classification=Classification,  # 分类
                        # 存放信息
                        PlasmaUse=PlasmaUse,  # 血浆用途
                        TissueUse=TissueUse,  # 组织用途
                        PlasmaStoragePosition=PlasmaStoragePosition,  # 血浆存放位置
                        TissueStoragePosition=TissueStoragePosition,  # 组织存放位置
                        # 组织样本标记
                        TissueSampleSign=TissueSampleSign,  # 组织样本标记
                    )
                else:
                    AlreadyExistedList = sam_code_num
                    # print sam_code_num + '已存在！'
            elif button_name == 'batchAddSample':
                # print 'batchAddSample'
                isAlreadyExisted = 0  # 是否存在重复样本编号标志
                sam_code_num_list = ''  # 样本编号列表
                num_sam = 0  # 样本编号个数
                # 样本编号
                sam_code_num = sam_code_num.split('\n')  # 样本编号

                # 医院信息
                HospitalForInspection = HospitalForInspection.split('\n')  # 送检医院
                if len(sam_code_num) > len(HospitalForInspection):
                    li = [''] * (len(sam_code_num) - len(HospitalForInspection))
                    tuple(li)
                    HospitalForInspection = HospitalForInspection + li

                Contacts = Contacts.split('\n')  # 联系人
                if len(sam_code_num) > len(Contacts):
                    li = [''] * (len(sam_code_num) - len(Contacts))
                    tuple(li)
                    Contacts = Contacts + li

                # 收样信息
                SamplingTime_Blood = SamplingTime_Blood.split('\n')  # 收样时间（血样）
                if len(sam_code_num) > len(SamplingTime_Blood):
                    li = [''] * (len(sam_code_num) - len(SamplingTime_Blood))
                    tuple(li)
                    SamplingTime_Blood = SamplingTime_Blood + li

                SamplingTime_Tissue = SamplingTime_Tissue.split('\n')  # 收样时间（组织）
                if len(sam_code_num) > len(SamplingTime_Tissue):
                    li = [''] * (len(sam_code_num) - len(SamplingTime_Tissue))
                    tuple(li)
                    SamplingTime_Tissue = SamplingTime_Tissue + li

                Collector = Collector.split('\n')  # 收样人
                if len(sam_code_num) > len(Collector):
                    li = [''] * (len(sam_code_num) - len(Collector))
                    tuple(li)
                    Collector = Collector + li

                # 项目信息
                InpatientNumber = InpatientNumber.split('\n')  # 住院号
                if len(sam_code_num) > len(InpatientNumber):
                    li = [''] * (len(sam_code_num) - len(InpatientNumber))
                    tuple(li)
                    InpatientNumber = InpatientNumber + li

                PathologicalNumber = PathologicalNumber.split('\n')  # 病理号
                if len(sam_code_num) > len(PathologicalNumber):
                    li = [''] * (len(sam_code_num) - len(PathologicalNumber))
                    tuple(li)
                    PathologicalNumber = PathologicalNumber + li

                CorrelationNumber = CorrelationNumber.split('\n')  # 相关编号
                if len(sam_code_num) > len(CorrelationNumber):
                    li = [''] * (len(sam_code_num) - len(CorrelationNumber))
                    tuple(li)
                    CorrelationNumber = CorrelationNumber + li

                # 样本信息
                PatientName = PatientName.split('\n')  # 患者姓名
                if len(sam_code_num) > len(PatientName):
                    li = [''] * (len(sam_code_num) - len(PatientName))
                    tuple(li)
                    PatientName = PatientName + li

                PatientAge = PatientAge.split('\n')  # 患者年龄（岁）
                if len(sam_code_num) > len(PatientAge):
                    li = [''] * (len(sam_code_num) - len(PatientAge))
                    tuple(li)
                    PatientAge = PatientAge + li

                PatientSex = PatientSex.split('\n')  # 患者性别
                if len(sam_code_num) > len(PatientSex):
                    li = [''] * (len(sam_code_num) - len(PatientSex))
                    tuple(li)
                    PatientSex = PatientSex + li

                BloodSampleType = BloodSampleType.split('\n')  # 血样类型
                if len(sam_code_num) > len(BloodSampleType):
                    li = [''] * (len(sam_code_num) - len(BloodSampleType))
                    tuple(li)
                    BloodSampleType = BloodSampleType + li

                BloodSamplingTime = BloodSamplingTime.split('\n')  # 采血时间
                if len(sam_code_num) > len(BloodSamplingTime):
                    li = [''] * (len(sam_code_num) - len(BloodSamplingTime))
                    tuple(li)
                    BloodSamplingTime = BloodSamplingTime + li

                TissueSampleSources = TissueSampleSources.split('\n')  # 组织样本来源
                if len(sam_code_num) > len(TissueSampleSources):
                    li = [''] * (len(sam_code_num) - len(TissueSampleSources))
                    tuple(li)
                    TissueSampleSources = TissueSampleSources + li

                TissueQuantity = TissueQuantity.split('\n')  # 组织数量
                if len(sam_code_num) > len(TissueQuantity):
                    li = [''] * (len(sam_code_num) - len(TissueQuantity))
                    tuple(li)
                    TissueQuantity = TissueQuantity + li

                TissueType = TissueType.split('\n')  # 组织类型
                if len(sam_code_num) > len(TissueType):
                    li = [''] * (len(sam_code_num) - len(TissueType))
                    tuple(li)
                    TissueType = TissueType + li

                TissueSampleProcessing = TissueSampleProcessing.split('\n')  # 组织样本处理方式
                if len(sam_code_num) > len(TissueSampleProcessing):
                    li = [''] * (len(sam_code_num) - len(TissueSampleProcessing))
                    tuple(li)
                    TissueSampleProcessing = TissueSampleProcessing + li

                # 临床信息
                OperationDate = OperationDate.split('\n')  # 手术日期
                if len(sam_code_num) > len(OperationDate):
                    li = [''] * (len(sam_code_num) - len(OperationDate))
                    tuple(li)
                    OperationDate = OperationDate + li

                PathologicalInfo = PathologicalInfo.split('\n')  # 病理信息
                if len(sam_code_num) > len(PathologicalInfo):
                    li = [''] * (len(sam_code_num) - len(PathologicalInfo))
                    tuple(li)
                    PathologicalInfo = PathologicalInfo + li

                TNMStaging = TNMStaging.split('\n')  # TNM分期
                if len(sam_code_num) > len(TNMStaging):
                    li = [''] * (len(sam_code_num) - len(TNMStaging))
                    tuple(li)
                    TNMStaging = TNMStaging + li

                Stage = Stage.split('\n')  # Stage
                if len(sam_code_num) > len(Stage):
                    li = [''] * (len(sam_code_num) - len(Stage))
                    tuple(li)
                    Stage = Stage + li

                MolecularDiagnosticInfo = MolecularDiagnosticInfo.split('\n')  # 分子诊断信息
                if len(sam_code_num) > len(MolecularDiagnosticInfo):
                    li = [''] * (len(sam_code_num) - len(MolecularDiagnosticInfo))
                    tuple(li)
                    MolecularDiagnosticInfo = MolecularDiagnosticInfo + li

                Classification = Classification.split('\n')  # 分类
                if len(sam_code_num) > len(Classification):
                    li = [''] * (len(sam_code_num) - len(Classification))
                    tuple(li)
                    Classification = Classification + li

                # 存放信息
                PlasmaUse = PlasmaUse.split('\n')  # 血浆用途
                if len(sam_code_num) > len(PlasmaUse):
                    li = [''] * (len(sam_code_num) - len(PlasmaUse))
                    tuple(li)
                    PlasmaUse = PlasmaUse + li

                TissueUse = TissueUse.split('\n')  # 组织用途
                if len(sam_code_num) > len(TissueUse):
                    li = [''] * (len(sam_code_num) - len(TissueUse))
                    tuple(li)
                    TissueUse = TissueUse + li

                PlasmaStoragePosition = PlasmaStoragePosition.split('\n')  # 血浆存放位置
                if len(sam_code_num) > len(PlasmaStoragePosition):
                    li = [''] * (len(sam_code_num) - len(PlasmaStoragePosition))
                    tuple(li)
                    PlasmaStoragePosition = PlasmaStoragePosition + li

                TissueStoragePosition = TissueStoragePosition.split('\n')  # 组织存放位置
                if len(sam_code_num) > len(TissueStoragePosition):
                    li = [''] * (len(sam_code_num) - len(TissueStoragePosition))
                    tuple(li)
                    TissueStoragePosition = TissueStoragePosition + li

                for i in range(0, len(sam_code_num)):
                    if sam_code_num[i].strip('\r') not in Sample_list:
                        Sample_list.append(sam_code_num[i].strip('\r'))
                        if not sam_code_num[i].strip('\r') == '':
                            isAlreadyExisted = 1  # 是否存在重复样本编号标志
                            num_sam += 1
                            if not i == 0:
                                sam_code_num_list += '，'+sam_code_num[i].strip('\r')
                            else:
                                sam_code_num_list = sam_code_num[i].strip('\r')

                            if SamplingTime_Tissue[i] == '':
                                TissueSampleSign = 0  # 组织样本标记
                                # print '组织样本标记: ', TissueSampleSign
                            else:
                                TissueSampleSign = 1  # 组织样本标记
                                # print '组织样本标记: ', TissueSampleSign
                            # 添加数据到数据库
                            models.RandDSampleInfo.objects.create(
                                # 用户信息
                                username=username,  # 用户名
                                department=department,  # 部门
                                # 样本编号
                                sam_code_num=sam_code_num[i].strip('\r'),  # 样本编号
                                # 医院信息
                                HospitalForInspection=HospitalForInspection[i].strip('\r'),  # 送检医院
                                Contacts=Contacts[i].strip('\r'),  # 联系人
                                # 收样信息
                                SamplingTime_Blood=SamplingTime_Blood[i].strip('\r'),  # 收样时间（血样）
                                SamplingTime_Tissue=SamplingTime_Tissue[i].strip('\r'),  # 收样时间（组织）
                                Collector=Collector[i].strip('\r'),  # 收样人
                                # 项目信息
                                InpatientNumber=InpatientNumber[i].strip('\r'),  # 住院号
                                PathologicalNumber=PathologicalNumber[i].strip('\r'),  # 病理号
                                CorrelationNumber=CorrelationNumber[i].strip('\r'),  # 相关编号
                                # 样本信息
                                PatientName=PatientName[i].strip('\r'),  # 患者姓名
                                PatientAge=PatientAge[i].strip('\r'),  # 患者年龄（岁）
                                PatientSex=PatientSex[i].strip('\r'),  # 患者性别
                                BloodSampleType=BloodSampleType[i].strip('\r'),  # 血样类型
                                BloodSamplingTime=BloodSamplingTime[i].strip('\r'),  # 采血时间
                                TissueSampleSources=TissueSampleSources[i].strip('\r'),  # 组织样本来源
                                TissueQuantity=TissueQuantity[i].strip('\r'),  # 组织数量
                                TissueType=TissueType[i].strip('\r'),  # 组织类型
                                TissueSampleProcessing=TissueSampleProcessing[i].strip('\r'),  # 组织样本处理方式
                                # 临床信息
                                OperationDate=OperationDate[i].strip('\r'),  # 手术日期
                                PathologicalInfo=PathologicalInfo[i].strip('\r'),  # 病理信息
                                TNMStaging=TNMStaging[i].strip('\r'),  # TNM分期
                                Stage=Stage[i].strip('\r'),  # Stage
                                MolecularDiagnosticInfo=MolecularDiagnosticInfo[i].strip('\r'),  # 分子诊断信息
                                Classification=Classification[i].strip('\r'),  # 分类
                                # 存放信息
                                PlasmaUse=PlasmaUse[i].strip('\r'),  # 血浆用途
                                TissueUse=TissueUse[i].strip('\r'),  # 组织用途
                                PlasmaStoragePosition=PlasmaStoragePosition[i].strip('\r'),  # 血浆存放位置
                                TissueStoragePosition=TissueStoragePosition[i].strip('\r'),  # 组织存放位置
                                # 审核标记
                                sample_review=sample_review,  # 样本审核标记
                                Pretreatment_Sign=0,  # 样本预处理标记
                                DNAExtract_Sign=0,  # DNA提取任务标记
                                # task_assignment=0,  # 样本任务分派标记
                                # 组织样本标记
                                TissueSampleSign=TissueSampleSign,  # 组织样本标记
                                SampleAuditor=SampleAuditor,  # 样本审核人
                            )
                    else:
                        # print sam_code_num[i].strip('\r') + '已存在！'
                        if not i == 0:
                            AlreadyExistedList += '，' + sam_code_num[i].strip('\r')
                        else:
                            AlreadyExistedList = sam_code_num[i].strip('\r')

                if not isAlreadyExisted == 0:
                    if not sample_review == '':
                        # 添加系统消息
                        taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        Title = '通知：研发样本审核任务'  # 系统消息标题
                        Message = username + '录入一批(共' + str(num_sam) + '个)研发样本！样本编号分别为：' + sam_code_num_list + '。请尽快完成审核！'  # 系统邮件正文
                        models.UserSystemMessage.objects.create(
                            # 用户信息
                            Sender=username,  # 发送者
                            Receiver=SampleAuditor,  # 接收者
                            # 信息内容
                            Time=taskTime,  # 信息生成时间
                            Title=Title,  # 系统消息标题
                            Message=Message,  # 系统消息正文
                            ReadingState='未读',  # 信息阅读状态
                        )
                        sendEmail(SampleAuditor, Title, Message)  # 发送邮件通知


            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)

            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            if department == '管理员':
                temp_not_audited = models.RandDSampleInfo.objects.filter(sample_review=0)  # 研发样本未审核信息
                temp_draft = models.RandDSampleInfo.objects.filter(sample_review='')  # 研发样本草稿信息
                temp_return = models.RandDSampleInfo.objects.filter(sample_review=4)  # 研发审核退回样本信息
                temp_audited = models.RandDSampleInfo.objects.filter(sample_review__in=[1, 2, 3])  # 研发样本已审核信息
            else:
                temp_not_audited = models.RandDSampleInfo.objects.filter(username=username,
                                                                         sample_review=0)  # 研发样本未审核信息
                temp_draft = models.RandDSampleInfo.objects.filter(username=username, sample_review='')  # 研发样本草稿信息
                temp_return = models.RandDSampleInfo.objects.filter(username=username, sample_review=4)  # 研发审核退回样本信息
                temp_audited = models.RandDSampleInfo.objects.filter(username=username,
                                                                     sample_review__in=[1, 2, 3])  # 研发样本已审核信息
            return render(request, "modelspage/RandDSampleRegisterHomePage.html",
                          {"userinfo": temp, "not_audited": temp_not_audited, "audited": temp_audited,
                           "draft": temp_draft, "AlreadyExistedList": AlreadyExistedList,
                           "return": temp_return, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
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

# 研发样本登记数据展示页
def RandDSampleInfoShowData(request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}
        sam_code_num = ''
        SampleAuditor = ''
        button_name = ''
        if request.method == "POST":
            # 样本条码号
            sam_code_num = request.POST.get('sam_code_num')
            print '样本条码号:', sam_code_num

            SampleAuditor = request.POST.get('SampleAuditor')

            # 判断哪个按钮提交的数据
            if request.POST.has_key('UnauditedShowData'):
                button_name = 'UnauditedShowData'
            elif request.POST.has_key('AuditedShowData'):
                button_name = 'AuditedShowData'
            elif request.POST.has_key('DraftData'):
                button_name = 'DraftData'
            elif request.POST.has_key('submitReview'):
                button_name = 'submitReview'
            elif request.POST.has_key('returnData'):
                button_name = 'returnData'
            elif request.POST.has_key('ModifyData'):
                button_name = 'ModifyData'
            elif request.POST.has_key('delete'):
                temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                    username=username)  # 用户操作权限信息
                if temp_UserOperationPermissionsInfo.RandDSampleInfoInputHomePage == '1':
                    temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                        ReadingState='未读')
                    num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
                    temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
                    models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).delete()  # 删除信息
                    if department == '管理员':
                        temp_not_audited = models.RandDSampleInfo.objects.filter(sample_review=0)  # 研发样本未审核信息
                        temp_draft = models.RandDSampleInfo.objects.filter(sample_review='')  # 研发样本草稿信息
                        temp_return = models.RandDSampleInfo.objects.filter(sample_review=4)  # 研发审核退回样本信息
                        temp_audited = models.RandDSampleInfo.objects.filter(sample_review__in=[1, 2, 3])  # 研发样本已审核信息
                    else:
                        temp_not_audited = models.RandDSampleInfo.objects.filter(username=username,
                                                                                 sample_review=0)  # 研发样本未审核信息
                        temp_draft = models.RandDSampleInfo.objects.filter(username=username,
                                                                           sample_review='')  # 研发样本草稿信息
                        temp_return = models.RandDSampleInfo.objects.filter(username=username,
                                                                            sample_review=4)  # 研发审核退回样本信息
                        temp_audited = models.RandDSampleInfo.objects.filter(username=username,
                                                                             sample_review__in=[1, 2, 3])  # 研发样本已审核信息
                    return render(request, "modelspage/RandDSampleRegisterHomePage.html",
                                  {"userinfo": temp, "not_audited": temp_not_audited, "audited": temp_audited,
                                   "draft": temp_draft,
                                   "return": temp_return, "myInfo": temp_myInfo,
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

        # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')  # 用户信息
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_data = models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num)  # 临床样本信息

        if button_name == 'UnauditedShowData':
            return render(request, "modelspage/RandDSampleUnauditedShowData.html",
                          {"userinfo": temp, "data": temp_data, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        if button_name == 'AuditedShowData':
            return render(request, "modelspage/RandDSampleAuditedShowData.html",
                          {"userinfo": temp, "data": temp_data, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        if button_name == 'ModifyData':
            return render(request, "modelspage/RandDSampleModifyData.html",
                          {"userinfo": temp, "data": temp_data, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        elif button_name == 'DraftData':
            temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                username=username)  # 用户操作权限信息
            if temp_UserOperationPermissionsInfo.RandDSampleInfoInputHomePage == '1':
                temp_userlist = User.objects.filter(first_name='研发部')
                return render(request, "modelspage/RandDSampleDraftData.html",
                              {"userinfo": temp, "data": temp_data, "myInfo": temp_myInfo, "userlist": temp_userlist,
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
        elif button_name == 'submitReview':
            temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                username=username)  # 用户操作权限信息
            if temp_UserOperationPermissionsInfo.RandDSampleInfoInputHomePage == '1':
                models.RandDSampleInfo.objects.filter(sam_code_num=sam_code_num).update(sample_review=0)  # 临床样本信息
                # 添加系统消息
                taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                Title = '通知：研发样本审核任务'  # 系统消息标题
                Message = username + '录入一个研发样本！样本编号为：' + sam_code_num + '。请尽快完成审核！'  # 系统邮件正文
                models.UserSystemMessage.objects.create(
                    # 用户信息
                    Sender=username,  # 发送者
                    Receiver=SampleAuditor,  # 接收者
                    # 信息内容
                    Time=taskTime,  # 信息生成时间
                    Title=Title,  # 系统消息标题
                    Message=Message,  # 系统消息正文
                    ReadingState='未读',  # 信息阅读状态
                )
                sendEmail(SampleAuditor, Title, Message)  # 发送邮件通知

                if department == '管理员':
                    temp_not_audited = models.RandDSampleInfo.objects.filter(sample_review=0)  # 研发样本未审核信息
                    temp_draft = models.RandDSampleInfo.objects.filter(sample_review='')  # 研发样本草稿信息
                    temp_return = models.RandDSampleInfo.objects.filter(sample_review=4)  # 研发审核退回样本信息
                    temp_audited = models.RandDSampleInfo.objects.filter(sample_review__in=[1, 2, 3])  # 研发样本已审核信息
                else:
                    temp_not_audited = models.RandDSampleInfo.objects.filter(username=username,
                                                                             sample_review=0)  # 研发样本未审核信息
                    temp_draft = models.RandDSampleInfo.objects.filter(username=username, sample_review='')  # 研发样本草稿信息
                    temp_return = models.RandDSampleInfo.objects.filter(username=username,
                                                                        sample_review=4)  # 研发审核退回样本信息
                    temp_audited = models.RandDSampleInfo.objects.filter(username=username,
                                                                         sample_review__in=[1, 2, 3])  # 研发样本已审核信息
                return render(request, "modelspage/RandDSampleRegisterHomePage.html",
                              {"userinfo": temp, "not_audited": temp_not_audited, "audited": temp_audited,
                               "draft": temp_draft,
                               "return": temp_return, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
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

        elif button_name == 'returnData':
            temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(
                username=username)  # 用户操作权限信息
            if temp_UserOperationPermissionsInfo.RandDSampleInfoInputHomePage == '1':
                temp_userlist = User.objects.filter(first_name='研发部')
                return render(request, "modelspage/RandDSampleReturnData.html",
                              {"userinfo": temp, "data": temp_data, "myInfo": temp_myInfo, "userlist": temp_userlist,
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
