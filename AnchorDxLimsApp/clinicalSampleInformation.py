# encoding: utf-8

from django.shortcuts import render
from AnchorDxLimsApp import models
import time,httplib,datetime
from django.contrib.auth.models import User
from django.core.mail import send_mail
from smtplib import SMTPException
from AnchorDxLimsApp.views import sendEmail
# Create your views here.
#coding:utf-8

from django.shortcuts import render

# 临床样本登记数据录入
def CSRDataToBackstage(request):
    # 患者信息
    sam_code_num = '' # 样本条码号
    PatientName = ''  # 患者姓名
    PatientAge = ''  # 患者年龄（岁）
    PatientSex = ''  # 患者性别
    PatientBirthday = ''  # 患者身份证号码
    PatientPhoneNumber = ''  # 患者联系电话
    PatientEmail = ''  # 患者电子邮箱
    PatientAddress = ''  # 报告接收地址
    treatment_hospital = ''  # 就诊医院
    treatment_department = ''  # 就诊科室
    AttendingDoctor = ''  # 主治医生
    DoctorEmail = ''  # 医生邮箱
    # 样本信息
    Pathological_diagnosis = ''  # 病理诊断
    clinical_diagnosis = ''  # 临床诊断
    Clinical_stage = ''  # 临床分期
    is_tubercle_history = ''  # 结核病史
    tubercle_distribution = ''  # 结节大小和分布
    sample_source = ''  # 样本来源
    acquisition_time = ''  # 采集时间
    family_history = ''  # 家族史
    receiving_time = ''  # 收样时间
    sample_count = ''  # 样本数量
    sample_type = ''  # 样本类型
    sample_type_text = ''  # 样本类型描述
    infection_history = ''  # 传染病史
    # 基因检测史
    detected_gene_time = ''  # 检测时间
    detected_gene_name = ''  # 检测基因
    detected_gene_result = ''  # 检测结果
    # 曾有治疗史
    treatment_history_surgery = ''  # 手术
    treatment_history_chem = ''  # 化疗
    treatment_history_therapy = ''  # 靶向治疗
    # 合同信息
    contract_name = ''  # 项目编号
    contract_pay = ''  # 合同金额（人民币）
    pay_way = ''  # 支付方式
    pos_code = ''  # pos单号(交易参考号)
    Client = ''  # 委托人
    remarks = ''  # 其它（备注）
    # 检测方案
    cancer_type = ''  # 癌种
    # detection_type = ''  # 类型
    product_name = ''  # 产品名称
    is_return = ''  # 剩余样本是否退回
    is_invoice = ''     # 是否需要发票
    SampleAuditor = ''  # 样本审核人
    TissueSampleSign = ''  # 组织样本标记
    # 按钮名字
    button_name = ''  # 按钮名字
    sample_review = ''  # 审核标记
    review_submitModify = 0
    NO = ''
    old_sam_code_num = ''  # 旧样本编号
    if request.method == "POST":
        # 样本条码号
        sam_code_num = request.POST.get('sam_code_num')
        # 患者姓名
        PatientName = request.POST.get('PatientName')
        # 患者年龄（岁）
        PatientAge = request.POST.get('PatientAge')
        # 患者性别
        PatientSex = request.POST.get('PatientSex')
        # 患者身份证号码
        PatientBirthday = request.POST.get('PatientBirthday')
        # 患者联系电话
        PatientPhoneNumber = request.POST.get('PatientPhoneNumber')
        # 患者电子邮箱
        PatientEmail = request.POST.get('PatientEmail')
        # 报告接收地址
        PatientAddress = request.POST.get('PatientAddress')
        # 就诊医院
        treatment_hospital = request.POST.get('treatment_hospital')
        # if treatment_hospital == "其他".decode('utf-8'):
        #     treatment_hospital = request.POST.get('other_treatment_hospital')
        # 就诊科室
        treatment_department = request.POST.get('treatment_department')
        if treatment_department == "其他".decode('utf-8'):
            treatment_department = request.POST.get('othertreatment')
        # 主治医生
        AttendingDoctor = request.POST.get('AttendingDoctor')
        # 医生邮箱
        DoctorEmail = request.POST.get('DoctorEmail')
        # 病理诊断
        Pathological_diagnosis = request.POST.get('Pathological_diagnosis')
        # 临床诊断
        clinical_diagnosis = request.POST.get('clinical_diagnosis')
        # 临床分期
        Clinical_stage = request.POST.get('Clinical_stage')
        # 结核病史
        is_tubercle_history = request.POST.get('is_tubercle_history')
        # 结节大小和分布
        tubercle_distribution = request.POST.get('tubercle_distribution')
        # 样本来源
        sample_source = request.POST.get('sample_source')
        # 采集时间
        acquisition_time = request.POST.get('acquisition_time')
        # 家族史
        family_history = request.POST.get('family_history')
        # 收样时间
        receiving_time = request.POST.get('receiving_time')
        # 样本数量
        sample_count = request.POST.get('sample_count')
        # 样本类型
        sample_type = request.POST.get('sample_type')
        sample_type_text = request.POST.get('sample_type_text')
        # 传染病史
        infection_history = request.POST.get('infection_history')
        # 基因检测史
        detected_gene_time_list = request.POST.getlist('detected_gene_time')
        detected_gene_name_list = request.POST.getlist('detected_gene_name')
        detected_gene_result_list = request.POST.getlist('detected_gene_result')
        for i in range(0, len(detected_gene_time_list)):
            if i == 0:
                detected_gene_time = detected_gene_time_list[i]
                detected_gene_name = detected_gene_name_list[i]
                detected_gene_result = detected_gene_result_list[i]
            else:
                detected_gene_time += ';' + detected_gene_time_list[i]
                detected_gene_name += ';' + detected_gene_name_list[i]
                detected_gene_result += ';' + detected_gene_result_list[i]

        # 曾有治疗史
        treatment_history_surgery = request.POST.get('treatment_history_surgery')
        treatment_history_chem = request.POST.get('treatment_history_chem')
        treatment_history_therapy = request.POST.get('treatment_history_therapy')
        # 合同名称
        contract_name = request.POST.get('contract_name')
        # 合同金额（人民币）
        contract_pay = request.POST.get('contract_pay')
        # 支付方式
        pay_way = request.POST.get('pay_way')
        if pay_way == "pos机支付".decode('utf-8'):
            pos_code = request.POST.get('pos_code')

        # 业务员
        # Client = request.POST.get('Client')
        username = request.session['username']
        user = User.objects.get(username=username)
        Client = user.last_name
        # 其它（备注）
        remarks = request.POST.get('remarks')
        # 癌种
        cancer_type = request.POST.get('cancer_type')
        if cancer_type == "其他癌种".decode('utf-8'):
            cancer_type = request.POST.get('other_cancer_type')
        # 类型
        # detection_type_list = request.POST.getlist('detection_type')
        # detection_type = ''
        # for i in range(0, len(detection_type_list)):
        #     if i == 0:
        #         detection_type = detection_type_list[i]
        #     else:
        #         detection_type += ';' + detection_type_list[i]
        # 产品名称
        product_name_list = request.POST.getlist('product_name')
        product_name = ''
        for i in range(0, len(product_name_list)):
            if i == 0:
                product_name = product_name_list[i]
            else:
                product_name += ';' + product_name_list[i]

        # 剩余样本是否退回
        is_return = request.POST.get('is_return')

        # 是否需要发票
        is_invoice = request.POST.get('is_invoice')

        SampleAuditor = request.POST.get('SampleAuditor')  # 样本审核人
        # TissueSampleSign = request.POST.get('TissueSampleSign')  # 组织样本标记
        if '血' in sample_type:
            TissueSampleSign = '0'
        else:
            TissueSampleSign = '1'

        IS = request.POST.get('is')
        NO = request.POST.get('no')
        old_sam_code_num = request.POST.get('old_sam_code_num')  # 旧样本编号

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
        elif request.POST.has_key('review_submitModify'):
            button_name = 'submitModify'
            review_submitModify = 1

    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print '首页，username: ', username, department
        temp = {"username": username, "department": department}

        temp_mySample = models.clinicalSampleInfo.objects.all()  # 临床样本信息
        AlreadyExistedList = ''  # 重复样本编号列表
        Sample_list = []  # 空列表
        for i in range(0, len(temp_mySample)):
            Sample_list.append(temp_mySample[i].sam_code_num)

        temp_UserOperationPermissionsInfo = models.UserOperationPermissionsInfo.objects.get(username=username)  # 用户操作权限信息

        if temp_UserOperationPermissionsInfo.ClinicalSampleRegistration == '1':
            if button_name == 'singleAddSample':
                if sam_code_num not in Sample_list:
                    # 添加数据到数据库
                    models.clinicalSampleInfo.objects.create(
                        # 用户信息
                        username=username,  # 用户名
                        department=department,  # 部门
                        # 患者信息
                        sam_code_num=sam_code_num,  # 样本条码号
                        PatientName=PatientName,  # 患者姓名
                        PatientAge=PatientAge,  # 患者年龄（岁）
                        PatientSex=PatientSex,  # 患者性别
                        PatientBirthday=PatientBirthday,  # 患者身份证号码
                        PatientPhoneNumber=PatientPhoneNumber,  # 患者联系电话
                        PatientEmail=PatientEmail,  # 患者电子邮箱
                        PatientAddress=PatientAddress,  # 报告接收地址
                        treatment_hospital=treatment_hospital,  # 就诊医院
                        treatment_department=treatment_department,  # 就诊科室
                        AttendingDoctor=AttendingDoctor,  # 主治医生
                        DoctorEmail=DoctorEmail,  # 医生邮箱
                        # 样本信息
                        Pathological_diagnosis=Pathological_diagnosis,  # 病理诊断
                        clinical_diagnosis=clinical_diagnosis,  # 临床诊断
                        Clinical_stage=Clinical_stage,  # 临床分期
                        is_tubercle_history=is_tubercle_history,  # 结核病史
                        tubercle_distribution=tubercle_distribution,  # 结节大小和分布
                        sample_source=sample_source,  # 样本来源
                        acquisition_time=acquisition_time,  # 采集时间
                        family_history=family_history,  # 家族史
                        receiving_time=receiving_time,  # 收样时间
                        sample_count=sample_count,  # 样本数量
                        sample_type=sample_type,  # 样本类型
                        sample_type_text=sample_type_text,  # 样本类型描述
                        infection_history=infection_history,  # 传染病史
                        # 基因检测史
                        detected_gene_time=detected_gene_time,  # 检测时间
                        detected_gene_name=detected_gene_name,  # 检测基因
                        detected_gene_result=detected_gene_result,  # 检测结果
                        # 曾有治疗史
                        treatment_history_surgery=treatment_history_surgery,  # 手术
                        treatment_history_chem=treatment_history_chem,  # 化疗
                        treatment_history_therapy=treatment_history_therapy,  # 靶向治疗
                        # 合同信息
                        contract_name=contract_name,  # 合同名称
                        contract_pay=contract_pay,  # 合同金额（人民币）
                        pay_way=pay_way,  # 支付方式
                        pos_code=pos_code,  # pos单号(交易参考号)
                        Client=Client,  # 委托人
                        remarks=remarks,  # 其它（备注）
                        # 检测方案
                        cancer_type=cancer_type,  # 癌种
                        # detection_type=detection_type,  # 类型
                        product_name=product_name,  # 产品名称
                        is_return=is_return,  # 剩余样本是否退回
                        is_invoice=is_invoice,  # 是否需要发票
                        # 审核标记
                        # contract_review=0,  # 合同审核标记
                        sample_review=sample_review,    # 样本审核标记
                        Pretreatment_Sign=0,  # 样本预处理标记
                        DNAExtract_Sign=0,  # DNA提取任务标记
                        # 样本审核信息
                        SampleAuditor=SampleAuditor,  # 样本审核人
                        # 组织样本标记
                        TissueSampleSign=TissueSampleSign,  # 组织样本标记
                    )

                    if not sample_review == '':
                        # 添加系统消息
                        taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        Title = '通知：临检样本审核任务'  # 系统消息标题
                        Message = username + '分派给你一个临检样本审核任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
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
                    print sam_code_num + '已存在！'
            elif button_name == 'updata':
                isupdata = 0
                if not sam_code_num == old_sam_code_num:
                    if sam_code_num in Sample_list:
                        isupdata = 1

                if isupdata == 0:
                    # 添加数据到数据库
                    models.clinicalSampleInfo.objects.filter(sam_code_num=old_sam_code_num).update(
                        # 用户信息
                        username=username,  # 用户名
                        department=department,  # 部门
                        # 患者信息
                        sam_code_num=sam_code_num,  # 样本条码号
                        PatientName=PatientName,  # 患者姓名
                        PatientAge=PatientAge,  # 患者年龄（岁）
                        PatientSex=PatientSex,  # 患者性别
                        PatientBirthday=PatientBirthday,  # 患者身份证号码
                        PatientPhoneNumber=PatientPhoneNumber,  # 患者联系电话
                        PatientEmail=PatientEmail,  # 患者电子邮箱
                        PatientAddress=PatientAddress,  # 报告接收地址
                        treatment_hospital=treatment_hospital,  # 就诊医院
                        treatment_department=treatment_department,  # 就诊科室
                        AttendingDoctor=AttendingDoctor,  # 主治医生
                        DoctorEmail=DoctorEmail,  # 医生邮箱
                        # 样本信息
                        Pathological_diagnosis=Pathological_diagnosis,  # 病理诊断
                        clinical_diagnosis=clinical_diagnosis,  # 临床诊断
                        Clinical_stage=Clinical_stage,  # 临床分期
                        is_tubercle_history=is_tubercle_history,  # 结核病史
                        tubercle_distribution=tubercle_distribution,  # 结节大小和分布
                        sample_source=sample_source,  # 样本来源
                        acquisition_time=acquisition_time,  # 采集时间
                        family_history=family_history,  # 家族史
                        receiving_time=receiving_time,  # 收样时间
                        sample_count=sample_count,  # 样本数量
                        sample_type=sample_type,  # 样本类型
                        sample_type_text=sample_type_text,  # 样本类型描述
                        infection_history=infection_history,  # 传染病史
                        # 基因检测史
                        detected_gene_time=detected_gene_time,  # 检测时间
                        detected_gene_name=detected_gene_name,  # 检测基因
                        detected_gene_result=detected_gene_result,  # 检测结果
                        # 曾有治疗史
                        treatment_history_surgery=treatment_history_surgery,  # 手术
                        treatment_history_chem=treatment_history_chem,  # 化疗
                        treatment_history_therapy=treatment_history_therapy,  # 靶向治疗
                        # 合同信息
                        contract_name=contract_name,  # 合同名称
                        contract_pay=contract_pay,  # 合同金额（人民币）
                        pay_way=pay_way,  # 支付方式
                        pos_code=pos_code,  # pos单号(交易参考号)
                        Client=Client,  # 委托人
                        remarks=remarks,  # 其它（备注）
                        # 检测方案
                        cancer_type=cancer_type,  # 癌种
                        # detection_type=detection_type,  # 类型
                        product_name=product_name,  # 产品名称
                        is_return=is_return,  # 剩余样本是否退回
                        is_invoice=is_invoice,  # 是否需要发票
                        # 审核标记
                        # contract_review=0,  # 合同审核标记
                        sample_review=sample_review,  # 样本审核标记
                        Pretreatment_Sign=0,  # 样本预处理标记
                        DNAExtract_Sign=0,  # DNA提取任务标记
                        # 样本审核信息
                        SampleAuditor=SampleAuditor,  # 样本审核人
                        # 组织样本标记
                        TissueSampleSign=TissueSampleSign,  # 组织样本标记
                    )

                    if not sample_review == '':
                        # 添加系统消息
                        taskTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        Title = '通知：临检样本审核任务'  # 系统消息标题
                        Message = username + '分派给你一个临检样本审核任务！样本编号为：' + sam_code_num + '。请尽快完成任务！'  # 系统邮件正文
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
                    # 添加数据到数据库
                    models.clinicalSampleInfo.objects.filter(sam_code_num=old_sam_code_num).update(
                        # 用户信息
                        username=username,  # 用户名
                        department=department,  # 部门
                        # 患者信息
                        sam_code_num=sam_code_num,  # 样本条码号
                        PatientName=PatientName,  # 患者姓名
                        PatientAge=PatientAge,  # 患者年龄（岁）
                        PatientSex=PatientSex,  # 患者性别
                        PatientBirthday=PatientBirthday,  # 患者身份证号码
                        PatientPhoneNumber=PatientPhoneNumber,  # 患者联系电话
                        PatientEmail=PatientEmail,  # 患者电子邮箱
                        PatientAddress=PatientAddress,  # 报告接收地址
                        treatment_hospital=treatment_hospital,  # 就诊医院
                        treatment_department=treatment_department,  # 就诊科室
                        AttendingDoctor=AttendingDoctor,  # 主治医生
                        DoctorEmail=DoctorEmail,  # 医生邮箱
                        # 样本信息
                        Pathological_diagnosis=Pathological_diagnosis,  # 病理诊断
                        clinical_diagnosis=clinical_diagnosis,  # 临床诊断
                        Clinical_stage=Clinical_stage,  # 临床分期
                        is_tubercle_history=is_tubercle_history,  # 结核病史
                        tubercle_distribution=tubercle_distribution,  # 结节大小和分布
                        sample_source=sample_source,  # 样本来源
                        acquisition_time=acquisition_time,  # 采集时间
                        family_history=family_history,  # 家族史
                        receiving_time=receiving_time,  # 收样时间
                        sample_count=sample_count,  # 样本数量
                        sample_type=sample_type,  # 样本类型
                        sample_type_text=sample_type_text,  # 样本类型描述
                        infection_history=infection_history,  # 传染病史
                        # 基因检测史
                        detected_gene_time=detected_gene_time,  # 检测时间
                        detected_gene_name=detected_gene_name,  # 检测基因
                        detected_gene_result=detected_gene_result,  # 检测结果
                        # 曾有治疗史
                        treatment_history_surgery=treatment_history_surgery,  # 手术
                        treatment_history_chem=treatment_history_chem,  # 化疗
                        treatment_history_therapy=treatment_history_therapy,  # 靶向治疗
                        # 合同信息
                        contract_name=contract_name,  # 合同名称
                        contract_pay=contract_pay,  # 合同金额（人民币）
                        pay_way=pay_way,  # 支付方式
                        pos_code=pos_code,  # pos单号(交易参考号)
                        Client=Client,  # 委托人
                        remarks=remarks,  # 其它（备注）
                        # 检测方案
                        cancer_type=cancer_type,  # 癌种
                        # detection_type=detection_type,  # 类型
                        product_name=product_name,  # 产品名称
                        is_return=is_return,  # 剩余样本是否退回
                        is_invoice=is_invoice,  # 是否需要发票
                        # 组织样本标记
                        TissueSampleSign=TissueSampleSign,  # 组织样本标记
                    )
                else:
                    AlreadyExistedList = sam_code_num
                    # print sam_code_num + '已存在！'
                if review_submitModify == 1:
                    # 从数据里取出所有数据
                    # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
                    temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                        ReadingState='未读')  # 用户信息
                    num_SystemMessage_Unread = len(temp_SystemMessage_Unread)

                    temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
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
            elif button_name == 'batchAddSample':
                # print 'batchAddSample'
                isAlreadyExisted = 0  # 是否存在重复样本编号标志
                sam_code_num_list = ''  # 样本编号列表
                num_sam = 0  # 样本编号个数
                # 患者信息
                sam_code_num = sam_code_num.split('\n')  # 样本条码号

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

                PatientBirthday = PatientBirthday.split('\n')  # 患者身份证号码
                if len(sam_code_num) > len(PatientBirthday):
                    li = [''] * (len(sam_code_num) - len(PatientBirthday))
                    tuple(li)
                    PatientBirthday = PatientBirthday + li

                PatientPhoneNumber = PatientPhoneNumber.split('\n')  # 患者联系电话
                if len(sam_code_num) > len(PatientPhoneNumber):
                    li = [''] * (len(sam_code_num) - len(PatientPhoneNumber))
                    tuple(li)
                    PatientPhoneNumber = PatientPhoneNumber + li

                PatientEmail = PatientEmail.split('\n')  # 患者电子邮箱
                if len(sam_code_num) > len(PatientEmail):
                    li = [''] * (len(sam_code_num) - len(PatientEmail))
                    tuple(li)
                    PatientEmail = PatientEmail + li

                PatientAddress = PatientAddress.split('\n')  # 报告接收地址
                if len(sam_code_num) > len(PatientAddress):
                    li = [''] * (len(sam_code_num) - len(PatientAddress))
                    tuple(li)
                    PatientAddress = PatientAddress + li

                treatment_hospital = treatment_hospital.split('\n')  # 就诊医院
                if len(sam_code_num) > len(treatment_hospital):
                    li = [''] * (len(sam_code_num) - len(treatment_hospital))
                    tuple(li)
                    treatment_hospital = treatment_hospital + li

                treatment_department = treatment_department.split('\n')  # 就诊科室
                if len(sam_code_num) > len(treatment_department):
                    li = [''] * (len(sam_code_num) - len(treatment_department))
                    tuple(li)
                    treatment_department = treatment_department + li

                AttendingDoctor = AttendingDoctor.split('\n')  # 主治医生
                if len(sam_code_num) > len(AttendingDoctor):
                    li = [''] * (len(sam_code_num) - len(AttendingDoctor))
                    tuple(li)
                    AttendingDoctor = AttendingDoctor + li

                DoctorEmail = DoctorEmail.split('\n')  # 医生邮箱
                if len(sam_code_num) > len(DoctorEmail):
                    li = [''] * (len(sam_code_num) - len(DoctorEmail))
                    tuple(li)
                    DoctorEmail = DoctorEmail + li

                # 样本信息
                Pathological_diagnosis = Pathological_diagnosis.split('\n')  # 病理诊断
                if len(sam_code_num) > len(Pathological_diagnosis):
                    li = [''] * (len(sam_code_num) - len(Pathological_diagnosis))
                    tuple(li)
                    Pathological_diagnosis = Pathological_diagnosis + li

                clinical_diagnosis = clinical_diagnosis.split('\n')  # 临床诊断
                if len(sam_code_num) > len(clinical_diagnosis):
                    li = [''] * (len(sam_code_num) - len(clinical_diagnosis))
                    tuple(li)
                    clinical_diagnosis = clinical_diagnosis + li

                Clinical_stage = Clinical_stage.split('\n')  # 临床分期
                if len(sam_code_num) > len(Clinical_stage):
                    li = [''] * (len(sam_code_num) - len(Clinical_stage))
                    tuple(li)
                    Clinical_stage = Clinical_stage + li

                is_tubercle_history = is_tubercle_history.split('\n')  # 结核病史
                if len(sam_code_num) > len(is_tubercle_history):
                    li = [''] * (len(sam_code_num) - len(is_tubercle_history))
                    tuple(li)
                    is_tubercle_history = is_tubercle_history + li

                tubercle_distribution = tubercle_distribution.split('\n')  # 结节大小和分布
                if len(sam_code_num) > len(tubercle_distribution):
                    li = [''] * (len(sam_code_num) - len(tubercle_distribution))
                    tuple(li)
                    tubercle_distribution = tubercle_distribution + li

                sample_source = sample_source.split('\n')  # 样本来源
                if len(sam_code_num) > len(sample_source):
                    li = [''] * (len(sam_code_num) - len(sample_source))
                    tuple(li)
                    sample_source = sample_source + li

                acquisition_time = acquisition_time.split('\n')  # 采集时间
                if len(sam_code_num) > len(acquisition_time):
                    li = [''] * (len(sam_code_num) - len(acquisition_time))
                    tuple(li)
                    acquisition_time = acquisition_time + li

                family_history = family_history.split('\n')  # 家族史
                if len(sam_code_num) > len(family_history):
                    li = [''] * (len(sam_code_num) - len(family_history))
                    tuple(li)
                    family_history = family_history + li

                receiving_time = receiving_time.split('\n')  # 收样时间
                if len(sam_code_num) > len(receiving_time):
                    li = [''] * (len(sam_code_num) - len(receiving_time))
                    tuple(li)
                    receiving_time = receiving_time + li

                sample_count = sample_count.split('\n')  # 样本数量
                if len(sam_code_num) > len(sample_count):
                    li = [''] * (len(sam_code_num) - len(sample_count))
                    tuple(li)
                    sample_count = sample_count + li

                sample_type = sample_type.split('\n')  # 样本类型
                if len(sam_code_num) > len(sample_type):
                    li = [''] * (len(sam_code_num) - len(sample_type))
                    tuple(li)
                    sample_type = sample_type + li

                sample_type_text = sample_type_text.split('\n')  # 样本类型描述
                if len(sam_code_num) > len(sample_type_text):
                    li = [''] * (len(sam_code_num) - len(sample_type_text))
                    tuple(li)
                    sample_type_text = sample_type_text + li

                infection_history = infection_history.split('\n')  # 传染病史
                if len(sam_code_num) > len(infection_history):
                    li = [''] * (len(sam_code_num) - len(infection_history))
                    tuple(li)
                    infection_history = infection_history + li

                # 基因检测史
                detected_gene_time = detected_gene_time.split('\n')  # 检测时间
                if len(sam_code_num) > len(detected_gene_time):
                    li = [''] * (len(sam_code_num) - len(detected_gene_time))
                    tuple(li)
                    detected_gene_time = detected_gene_time + li

                detected_gene_name = detected_gene_name.split('\n')  # 检测基因
                if len(sam_code_num) > len(detected_gene_name):
                    li = [''] * (len(sam_code_num) - len(detected_gene_name))
                    tuple(li)
                    detected_gene_name = detected_gene_name + li

                detected_gene_result = detected_gene_result.split('\n')  # 检测结果
                if len(sam_code_num) > len(detected_gene_result):
                    li = [''] * (len(sam_code_num) - len(detected_gene_result))
                    tuple(li)
                    detected_gene_result = detected_gene_result + li

                # 曾有治疗史
                treatment_history_surgery = treatment_history_surgery.split('\n')  # 手术
                if len(sam_code_num) > len(treatment_history_surgery):
                    li = [''] * (len(sam_code_num) - len(treatment_history_surgery))
                    tuple(li)
                    treatment_history_surgery = treatment_history_surgery + li

                treatment_history_chem = treatment_history_chem.split('\n')  # 化疗
                if len(sam_code_num) > len(treatment_history_chem):
                    li = [''] * (len(sam_code_num) - len(treatment_history_chem))
                    tuple(li)
                    treatment_history_chem = treatment_history_chem + li

                treatment_history_therapy = treatment_history_therapy.split('\n')  # 靶向治疗
                if len(sam_code_num) > len(treatment_history_therapy):
                    li = [''] * (len(sam_code_num) - len(treatment_history_therapy))
                    tuple(li)
                    treatment_history_therapy = treatment_history_therapy + li

                # 合同信息
                contract_name = contract_name.split('\n')  # 项目编号
                if len(sam_code_num) > len(contract_name):
                    li = [''] * (len(sam_code_num) - len(contract_name))
                    tuple(li)
                    contract_name = contract_name + li

                contract_pay = contract_pay.split('\n')  # 合同金额（人民币）
                if len(sam_code_num) > len(contract_pay):
                    li = [''] * (len(sam_code_num) - len(contract_pay))
                    tuple(li)
                    contract_pay = contract_pay + li

                pay_way = pay_way.split('\n')  # 支付方式
                if len(sam_code_num) > len(pay_way):
                    li = [''] * (len(sam_code_num) - len(pay_way))
                    tuple(li)
                    pay_way = pay_way + li

                pos_code = pos_code.split('\n')  # pos单号(交易参考号)
                if len(sam_code_num) > len(pos_code):
                    li = [''] * (len(sam_code_num) - len(pos_code))
                    tuple(li)
                    pos_code = pos_code + li

                # 业务员
                # Client = Client.split('\n')  # 委托人
                # if len(sam_code_num) > len(Client):
                #     li = [''] * (len(sam_code_num) - len(Client))
                #     tuple(li)
                #     Client = Client + li
                # username = request.session['username']
                # user = User.objects.get(username=username)
                # Client = user.last_name

                remarks = remarks.split('\n')  # 其它（备注）
                if len(sam_code_num) > len(remarks):
                    li = [''] * (len(sam_code_num) - len(remarks))
                    tuple(li)
                    remarks = remarks + li

                # 检测方案
                cancer_type = cancer_type.split('\n')  # 癌种
                if len(sam_code_num) > len(cancer_type):
                    li = [''] * (len(sam_code_num) - len(cancer_type))
                    tuple(li)
                    cancer_type = cancer_type + li

                # detection_type = detection_type.split('\n')  # 类型
                # if len(sam_code_num) > len(detection_type):
                #     li = [''] * (len(sam_code_num) - len(detection_type))
                #     tuple(li)
                #     detection_type = detection_type + li

                product_name = product_name.split('\n')  # 产品名称
                if len(sam_code_num) > len(product_name):
                    li = [''] * (len(sam_code_num) - len(product_name))
                    tuple(li)
                    product_name = product_name + li

                is_return = is_return.split('\n')  # 剩余样本是否退回
                if len(sam_code_num) > len(is_return):
                    li = [''] * (len(sam_code_num) - len(is_return))
                    tuple(li)
                    is_return = is_return + li

                is_invoice = is_invoice.split('\n')  # 是否需要发票
                if len(sam_code_num) > len(is_invoice):
                    li = [''] * (len(sam_code_num) - len(is_invoice))
                    tuple(li)
                    is_invoice = is_invoice + li

                # TissueSampleSign = TissueSampleSign.split('\n')  # 组织样本标记
                # if len(sam_code_num) > len(TissueSampleSign):
                #     li = [''] * (len(sam_code_num) - len(TissueSampleSign))
                #     tuple(li)
                #     TissueSampleSign = TissueSampleSign + li

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

                            # print 'IS:', request.POST.get('is')
                            if '血' in sample_type[i].strip('\r'):
                                isTissueSample = '0'
                            else:
                                isTissueSample = '1'
                            # if TissueSampleSign[i].strip('\r') == IS:
                            #     isTissueSample = 1  # 组织样本标记
                            #     # print '组织样本标记是是是: ', TissueSampleSign[i]
                            # else:
                            #     isTissueSample = 0  # 组织样本标记
                            #     # print '组织样本标记: ', TissueSampleSign[i]

                            # 添加数据到数据库
                            models.clinicalSampleInfo.objects.create(
                                # 用户信息
                                username=username,  # 用户名
                                department=department,  # 部门
                                # 患者信息
                                sam_code_num=sam_code_num[i].strip('\r'),  # 样本条码号
                                PatientName=PatientName[i].strip('\r'),  # 患者姓名
                                PatientAge=PatientAge[i].strip('\r'),  # 患者年龄（岁）
                                PatientSex=PatientSex[i].strip('\r'),  # 患者性别
                                PatientBirthday=PatientBirthday[i].strip('\r'),  # 患者身份证号码
                                PatientPhoneNumber=PatientPhoneNumber[i].strip('\r'),  # 患者联系电话
                                PatientEmail=PatientEmail[i].strip('\r'),  # 患者电子邮箱
                                PatientAddress=PatientAddress[i].strip('\r'),  # 报告接收地址
                                treatment_hospital=treatment_hospital[i].strip('\r'),  # 就诊医院
                                treatment_department=treatment_department[i].strip('\r'),  # 就诊科室
                                AttendingDoctor=AttendingDoctor[i].strip('\r'),  # 主治医生
                                DoctorEmail=DoctorEmail[i].strip('\r'),  # 医生邮箱
                                # 样本信息
                                Pathological_diagnosis=Pathological_diagnosis[i].strip('\r'),  # 病理诊断
                                clinical_diagnosis=clinical_diagnosis[i].strip('\r'),  # 临床诊断
                                Clinical_stage=Clinical_stage[i].strip('\r'),  # 临床分期
                                is_tubercle_history=is_tubercle_history[i].strip('\r'),  # 结核病史
                                tubercle_distribution=tubercle_distribution[i].strip('\r'),  # 结节大小和分布
                                sample_source=sample_source[i].strip('\r'),  # 样本来源
                                acquisition_time=acquisition_time[i].strip('\r'),  # 采集时间
                                family_history=family_history[i].strip('\r'),  # 家族史
                                receiving_time=receiving_time[i].strip('\r'),  # 收样时间
                                sample_count=sample_count[i].strip('\r'),  # 样本数量
                                sample_type=sample_type[i].strip('\r'),  # 样本类型
                                sample_type_text=sample_type_text[i].strip('\r'),  # 样本类型描述
                                infection_history=infection_history[i].strip('\r'),  # 传染病史
                                # 基因检测史
                                detected_gene_time=detected_gene_time[i].strip('\r'),  # 检测时间
                                detected_gene_name=detected_gene_name[i].strip('\r'),  # 检测基因
                                detected_gene_result=detected_gene_result[i].strip('\r'),  # 检测结果
                                # 曾有治疗史
                                treatment_history_surgery=treatment_history_surgery[i].strip('\r'),  # 手术
                                treatment_history_chem=treatment_history_chem[i].strip('\r'),  # 化疗
                                treatment_history_therapy=treatment_history_therapy[i].strip('\r'),  # 靶向治疗
                                # 合同信息
                                contract_name=contract_name[i].strip('\r'),  # 合同名称
                                contract_pay=contract_pay[i].strip('\r'),  # 合同金额（人民币）
                                pay_way=pay_way[i].strip('\r'),  # 支付方式
                                pos_code=pos_code[i].strip('\r'),  # pos单号(交易参考号)
                                Client=Client,  # 委托人
                                remarks=remarks[i].strip('\r'),  # 其它（备注）
                                # 检测方案
                                cancer_type=cancer_type[i].strip('\r'),  # 癌种
                                # detection_type=detection_type[i].strip('\r'),  # 类型
                                product_name=product_name[i].strip('\r'),  # 产品名称
                                is_return=is_return[i].strip('\r'),  # 剩余样本是否退回
                                is_invoice=is_invoice[i].strip('\r'),  # 是否需要发票
                                # 审核标记
                                # contract_review=0,  # 合同审核标记
                                sample_review=sample_review,  # 样本审核标记
                                Pretreatment_Sign=0,  # 样本预处理标记
                                DNAExtract_Sign=0,  # DNA提取任务标记
                                # 样本审核信息
                                SampleAuditor=SampleAuditor,  # 样本审核人
                                # 组织样本标记
                                TissueSampleSign=isTissueSample,  # 组织样本标记
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
                        Title = '通知：临检样本审核任务'  # 系统消息标题
                        Message = username + '录入一批(共' + str(num_sam) + '个)临检样本！样本编号分别为：' + sam_code_num_list + '。请尽快完成审核！'  # 系统邮件正文
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
            # temp_mySample = models.clinicalSampleInfo.objects.filter(username=username)  # 临床样本信息
            if department == '管理员':
                temp_not_audited = models.clinicalSampleInfo.objects.filter(sample_review=0)  # 研发样本未审核信息
                temp_draft = models.clinicalSampleInfo.objects.filter(sample_review='')  # 研发样本草稿信息
                temp_return = models.clinicalSampleInfo.objects.filter(sample_review=4)  # 研发审核退回样本信息
                temp_audited = models.clinicalSampleInfo.objects.filter(
                    sample_review__in=[1, 2, 3])  # 研发样本已审核信息
            else:
                temp_not_audited = models.clinicalSampleInfo.objects.filter(username=username,
                                                                            sample_review=0)  # 研发样本未审核信息
                temp_draft = models.clinicalSampleInfo.objects.filter(username=username,
                                                                      sample_review='')  # 研发样本草稿信息
                temp_return = models.clinicalSampleInfo.objects.filter(username=username,
                                                                       sample_review=4)  # 研发审核退回样本信息
                temp_audited = models.clinicalSampleInfo.objects.filter(username=username,
                                                                        sample_review__in=[1, 2, 3])  # 研发样本已审核信息
            return render(request, "modelspage/sample_entry.html",
                          {"userinfo": temp, "not_audited": temp_not_audited, "audited": temp_audited,
                           "draft": temp_draft, "AlreadyExistedList": AlreadyExistedList,
                           "return": temp_return, "myInfo": temp_myInfo,
                           "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})
        else:
            temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
            # temp_SystemMessage = models.UserSystemMessage.objects.filter(Receiver=username)  # 用户信息
            temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                                ReadingState='未读')  # 用户信息
            num_SystemMessage_Unread = len(temp_SystemMessage_Unread)
            return render(request, "modelspage/PermissionsPrompt.html",
                          {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                           "num_SystemMessage_Unread": num_SystemMessage_Unread})


