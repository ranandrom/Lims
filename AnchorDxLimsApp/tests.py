# encoding: utf-8
from django.test import TestCase

from django.contrib import auth
from django.shortcuts import render
from django.contrib.auth.models import User
from AnchorDxLimsApp import models
# Create your views here.
#coding:utf-8

from django.shortcuts import render,HttpResponse
# Create your tests here.


# 测试
def test01(request):
    try:
        username = request.session['username']
        department = request.session['department']
    except Exception:
        return render(request, "index.html")
    else:
        print(r'首页，username: ', username, department)
        temp = {"username": username, "department": department}

        if request.method == "POST":
            # 样本编号
            sam_code_num = request.POST.get('sam_code_num')  # 样本编号
            print '样本条码号: ', sam_code_num
            sam_code_num = sam_code_num.split('\n')
            for i in range(0, len(sam_code_num)):
                print '[i]', sam_code_num[i]

            print '长度', len(sam_code_num)
            print '[0]', sam_code_num
            print '[1]', sam_code_num[1]
            print '[last]', sam_code_num[len(sam_code_num)-1]
            if sam_code_num[len(sam_code_num)-1] == '':
                print '空: '

            HospitalForInspection = request.POST.get('HospitalForInspection')  # 送检医院
            print '送检医院: ', HospitalForInspection
            HospitalForInspection = HospitalForInspection.split('\n')  # 送检医院
            if len(sam_code_num) > len(HospitalForInspection):
                li = [''] * (len(sam_code_num) - len(HospitalForInspection))
                tuple(li)
                HospitalForInspection = HospitalForInspection + li

            SampleAuditor = request.POST.get('SampleAuditor')  # 收样人
            print '收样人: ', SampleAuditor

            Collector = request.POST.get('Collector')  # 患者姓名
            print '患者姓名: ', Collector

            PatientName = request.POST.get('PatientName')  # 患者年龄
            print '患者年龄: ', PatientName

            PatientAge = request.POST.get('PatientAge')  # 手术日期
            print '手术日期: ', PatientAge

            OperationDate = request.POST.get('OperationDate')  # 分子诊断信息
            print '分子诊断信息: ', OperationDate

            MolecularDiagnosticInfo = request.POST.get('MolecularDiagnosticInfo')  # 分类
            print '分类: ', MolecularDiagnosticInfo

            Classification = request.POST.get('Classification')  # 样本审核人
            print '样本审核人: ', Classification

        temp_myInfo = models.UserInfo.objects.filter(username=username)  # 用户信息
        temp_SystemMessage_Unread = models.UserSystemMessage.objects.filter(Receiver=username,
                                                                            ReadingState='未读')
        num_SystemMessage_Unread = len(temp_SystemMessage_Unread)

        return render(request, "modelspage/RandDSampleRegisterBatchInput.html",
                      {"userinfo": temp, "myInfo": temp_myInfo, "SystemMessage": temp_SystemMessage_Unread,
                       "num_SystemMessage_Unread": num_SystemMessage_Unread})
