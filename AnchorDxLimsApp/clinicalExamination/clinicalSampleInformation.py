# encoding: utf-8

from django.shortcuts import render
from AnchorDxLimsApp import models
# Create your views here.
#coding:utf-8

from django.shortcuts import render

#临床样本登记数据传到后台
def CSRDataToBackstage(request):
    if request.method == "POST":
        print '患者信息: ============================================= '
        # 样本条码号
        sam_code_num = request.POST.get('sam_code_num')
        print '样本条码号: '.decode('utf-8'), sam_code_num

        # 患者姓名
        PatientName = request.POST.get('PatientName')
        print '患者姓名: '.decode('utf-8'), PatientName

        # 患者年龄（岁）
        PatientAge = request.POST.get('PatientAge')
        print '患者年龄（岁）: '.decode('utf-8'), PatientAge

        # 患者性别
        PatientSex = request.POST.get('PatientSex')
        print '患者性别: '.decode('utf-8'), PatientSex

        # 患者身份证号码
        PatientBirthday = request.POST.get('PatientBirthday')
        print '患者身份证号码: '.decode('utf-8'), PatientBirthday

        # 患者联系电话
        PatientPhoneNumber = request.POST.get('PatientPhoneNumber')
        print '患者联系电话: '.decode('utf-8'), PatientPhoneNumber

        # 患者电子邮箱
        PatientEmail = request.POST.get('PatientEmail')
        print '患者电子邮箱: '.decode('utf-8'), PatientEmail

        # 报告接收地址
        PatientAddress = request.POST.get('PatientAddress')
        print '报告接收地址: '.decode('utf-8'), PatientAddress

        # 就诊医院
        treatment_hospital = request.POST.get('treatment_hospital')
        if treatment_hospital == "其他".decode('utf-8'):
            other_treatment_hospital = request.POST.get('other_treatment_hospital')
            print '就诊医院: '.decode('utf-8'), other_treatment_hospital
        else:
            print '就诊医院: '.decode('utf-8'), treatment_hospital

        # 就诊科室
        treatment_department = request.POST.get('treatment_department')
        if treatment_department == "其他".decode('utf-8'):
            othertreatment = request.POST.get('othertreatment')
            print '就诊科室: '.decode('utf-8'), othertreatment
        else:
            print '就诊科室: '.decode('utf-8'), treatment_department

        # 主治医生
        AttendingDoctor = request.POST.get('AttendingDoctor')
        print '主治医生: '.decode('utf-8'), AttendingDoctor

        # 医生邮箱
        DoctorEmail = request.POST.get('DoctorEmail')
        print '医生邮箱: '.decode('utf-8'), DoctorEmail

        print '样本信息: ============================================= '

        # 病理诊断
        Pathological_diagnosis = request.POST.get('Pathological_diagnosis')
        print '病理诊断: '.decode('utf-8'), Pathological_diagnosis

        # 临床诊断
        clinical_diagnosis = request.POST.get('clinical_diagnosis')
        print '临床诊断: '.decode('utf-8'), clinical_diagnosis

        # 临床分期
        Clinical_stage = request.POST.get('Clinical_stage')
        print '临床分期: '.decode('utf-8'), Clinical_stage

        # 结核病史
        is_tubercle_history = request.POST.get('is_tubercle_history')
        print '结核病史: '.decode('utf-8'), is_tubercle_history

        # 结节大小和分布
        tubercle_distribution = request.POST.get('tubercle_distribution')
        print '结节大小和分布: '.decode('utf-8'), tubercle_distribution

        # 样本来源
        sample_source = request.POST.get('sample_source')
        print '样本来源: '.decode('utf-8'), sample_source

        # 采集时间
        acquisition_time = request.POST.get('acquisition_time')
        print '采集时间: '.decode('utf-8'), acquisition_time

        # 家族史
        family_history = request.POST.get('family_history')
        print '家族史: '.decode('utf-8'), family_history

        # 收样时间
        receiving_time = request.POST.get('receiving_time')
        print '收样时间: '.decode('utf-8'), receiving_time

        # 样本数量
        sample_count = request.POST.get('sample_count')
        print '样本数量: '.decode('utf-8'), sample_count

        # 样本类型
        sample_type = request.POST.get('sample_type')
        sample_type_text = request.POST.get('sample_type_text')
        print '样本类型: '.decode('utf-8'), sample_type
        print '样本类型描述: '.decode('utf-8'), sample_type_text

        # 传染病史
        infection_history = request.POST.get('infection_history')
        print '传染病史: '.decode('utf-8'), infection_history

        # 基因检测史
        detected_gene_time = request.POST.getlist('detected_gene_time')
        detected_gene_name = request.POST.getlist('detected_gene_name')
        detected_gene_result = request.POST.getlist('detected_gene_result')
        for i in range(0, len(detected_gene_time)):
            print '基因检测史: '.decode('utf-8'), i+1
            print '检测时间: '.decode('utf-8'), detected_gene_time[i]
            print '检测基因: '.decode('utf-8'), detected_gene_name[i]
            print '检测结果: '.decode('utf-8'), detected_gene_result[i]

        # 曾有治疗史
        treatment_history_surgery = request.POST.get('treatment_history_surgery')
        treatment_history_chem = request.POST.get('treatment_history_chem')
        treatment_history_therapy = request.POST.get('treatment_history_therapy')
        print '曾有治疗史: '.decode('utf-8')
        print '手术: '.decode('utf-8'), treatment_history_surgery
        print '化疗: '.decode('utf-8'), treatment_history_chem
        print '靶向治疗: '.decode('utf-8'), treatment_history_therapy

        print '合同信息: ============================================= '

        # 合同名称
        contract_name = request.POST.get('contract_name')
        print '合同名称: '.decode('utf-8'), contract_name

        # 合同金额（人民币）
        contract_pay = request.POST.get('contract_pay')
        print '合同金额（人民币）: '.decode('utf-8'), contract_pay

        # 支付方式
        pay_way = request.POST.get('pay_way')
        print '支付方式: '.decode('utf-8'), pay_way
        if pay_way == "pos机支付".decode('utf-8'):
            pos_code = request.POST.get('pos_code')
            print 'pos单号(交易参考号): '.decode('utf-8'), pos_code

        # 委托人
        Client = request.POST.get('Client')
        print '委托人: '.decode('utf-8'), Client

        # 其它（备注）
        remarks = request.POST.get('remarks')
        print '其它（备注）: '.decode('utf-8'), remarks

        print '检测方案: ============================================= '

        # 癌种
        cancer_type = request.POST.get('cancer_type')
        if cancer_type == "其他癌种".decode('utf-8'):
            other_cancer_type = request.POST.get('other_cancer_type')
            print '癌种: '.decode('utf-8'), other_cancer_type
        else:
            print '癌种: '.decode('utf-8'), cancer_type

        # 类型
        detection_type = request.POST.getlist('detection_type')
        print '类型: '.decode('utf-8')
        for i in range(0, len(detection_type)):
            print detection_type[i]

        # 产品名称
        product_name = request.POST.getlist('product_name')
        print '产品名称: '.decode('utf-8')
        for i in range(0, len(product_name)):
            print product_name[i]

        # 剩余样本是否退回
        is_return = request.POST.get('is_return')
        print '剩余样本是否退回: '.decode('utf-8'), is_return

        # 是否需要发票
        is_invoice = request.POST.get('is_invoice')
        print '是否需要发票: '.decode('utf-8'), is_invoice

    print '检测方案: ============================================= '

    #return HttpResponse("AnchorDx-Lims")
    # 添加数据到数据库
    #models.UserInfo.objects.create(username=username, password=password)
    # 从数据里取出所有数据
    #temp_mysql = models.UserInfo.objects.all()
    username = request.session['username']
    department = request.session['department']
    print '首页，username: '.decode('utf-8'), username, department
    temp = {"username": username, "department": department}
    return render(request, "modelspage/sample_reg.html", {"data": temp})


