# encoding: utf-8
# coding:utf-8
"""AnchorDx_Lims URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib import admin
from AnchorDxLimsApp import views
from AnchorDxLimsApp import clinicalSampleInformation
from AnchorDxLimsApp import RandD_SampleInfo_Input
from AnchorDxLimsApp import sampleReview
from AnchorDxLimsApp import RandDSampleReview
from AnchorDxLimsApp import RandDTaskAssignment
from AnchorDxLimsApp import sampleToExamine
from AnchorDxLimsApp import contractToExamine
from AnchorDxLimsApp import Pretreatment_TaskToExamine
from AnchorDxLimsApp import RandDPretreatmentTaskAssignment
from AnchorDxLimsApp import DNAExtract_TaskToExamine
from AnchorDxLimsApp import RandDDNAExtractTaskAssignment
from AnchorDxLimsApp import PreLibCon_TaskToExamine
from AnchorDxLimsApp import RandDPreLibConTaskAssignment
from AnchorDxLimsApp import FinLibCon_TaskToExamine
from AnchorDxLimsApp import RandDFinLibConTaskAssignment
from AnchorDxLimsApp import ComputerSeq_TaskToExamine
from AnchorDxLimsApp import RandDComSeqTaskAssignment
from AnchorDxLimsApp import OtherInformation_ToExamine
from AnchorDxLimsApp import RandDOtherInformation
from AnchorDxLimsApp import Pretreatment
from AnchorDxLimsApp import RandDSamplePretreatment
from AnchorDxLimsApp import DNAExtract
from AnchorDxLimsApp import RandDSampleDNAExtract
from AnchorDxLimsApp import PreLibCon
from AnchorDxLimsApp import RandDSamplePreLibCon
from AnchorDxLimsApp import FinLibCon
from AnchorDxLimsApp import RandDSampleFinLibCon
from AnchorDxLimsApp import ComSeq
from AnchorDxLimsApp import RandDSampleComSeq
from AnchorDxLimsApp import Bioinfo_TaskToExamine
from AnchorDxLimsApp import Bioinfo_DataAnalysis
from AnchorDxLimsApp import Bioinfo_DataAnalysis_ResultAudit
from AnchorDxLimsApp import Bioinfo_Report_Make
from AnchorDxLimsApp import Bioinfo_Report_Medical_Audit
from AnchorDxLimsApp import Bioinfo_Report_Operate_Audit
from AnchorDxLimsApp import Bioinfo_Report_Send_Info
from AnchorDxLimsApp import tests


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.index),
    # url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^homepage/$', views.homepage),
    url(r'^UserAccessRightsSetting/$', views.UserAccessRightsSetting),
    url(r'^UserAccessRightsSettingUsernameInput/$', views.UserAccessRightsSetting_usernameInput),
    url(r'^UserAccessRightsSettingToDataBases/$', views.UserAccessRightsSettingToDataBases),
    url(r'^UserOperationPermissionsSetting/$', views.UserOperationPermissionsSetting),
    url(r'^UserOperationPermissionsSettingUsernameInput/$', views.UserOperationPermissionsSetting_usernameInput),
    url(r'^UserOperationPermissionsSettingToDataBases/$', views.UserOperationPermissionsSettingToDataBases),
    url(r'^UserSystemMessageHomePage/$', views.UserSystemMessageHomePage),  # 用户系统信息列表首页
    url(r'^UserSystemMessagedetailedInfo/$', views.UserSystemMessagedetailedInfo),  # 用户系统信息详细信息展示页
    url(r'^UserSystemMessageProcessing/$', views.UserSystemMessageProcessing),  # 用户系统信息处理
    # 临床样本登记
    url(r'^ClinicalSampleRegistration/$', views.ClinicalSampleRegistration),    # 临床样本登记首页
    url(r'^ClinicalSampleRegistrationInputdata/$', views.ClinicalSampleRegistrationInputdata),    # 临床样本登记数据录入页
    url(r'^ClinicalSampleShowData/$', views.ClinicalSampleShowData),    # 临床样本登记数据展示页
    url(r'^CSRDataToBackstage/$', clinicalSampleInformation.CSRDataToBackstage),    # 临床样本登记数据传到后台
    # 研发样本登记
    url(r'^RandDSampleInfoInputHomePage/$', RandD_SampleInfo_Input.RandDSampleInfoInputHomePage),  # 研发样本登记首页
    url(r'^RandDSampleInfoInputData/$', RandD_SampleInfo_Input.RandDSampleInfoInputData),    # 研发样本登记数据录入页
    url(r'^RandDSampleInfoInputToDataBase/$', RandD_SampleInfo_Input.RandDSampleInfoInputToDataBase),    # 研发样本登记数据录入到数据库
    url(r'^RandDSampleInfoShowData/$', RandD_SampleInfo_Input.RandDSampleInfoShowData),    # 研发样本登记数据展示页
    # 临床样本审核
    url(r'^sample_Review/$', sampleReview.sample_Review),  # 临床样本审核列表页
    url(r'^sampleToExamine/$', sampleToExamine.sample_To_Examine), # 临床样本审核详情页
    url(r'^sampleExamineOperation/$', sampleToExamine.sample_Examine_Operation),  # 临床样本审核操作页
    url(r'^sample_recovery_Task_Operation/$', sampleToExamine.recovery_Task_Operation), # 临床样本暂停任务信息详情页
    url(r'^sample_To_Examine_Suspend/$', sampleToExamine.sample_To_Examine_Suspend), # 已暂停的样本恢复操作
    url(r'^sampleToExamine_Pass/$', sampleToExamine.sample_To_Examine_Pass), # 临床样本已通过审核信息详情页
    url(r'^sampleToExamine_Not_Pass/$', sampleToExamine.sample_To_Examine_Not_Pass), # 临床样本终止任务信息详情页
    # 研发样本审核
    url(r'^RandDSampleReviewHomePage/$', RandDSampleReview.RandDSampleReviewHomePage),  # 研发样本审核首页
    url(r'^RandDSampleReview/$', RandDSampleReview.RandDSampleReview),  # 研发样本审核详情页
    url(r'^RandDSampleReviewOperation/$', RandDSampleReview.RandDSampleReviewOperation),  # 研发样本审核操作
    url(r'^RandDSampleReviewPassInfo/$', RandDSampleReview.RandDSampleReviewPassInfo),  # 研发样本审核通过详情页
    url(r'^RandDSampleReviewSuspendInfo/$', RandDSampleReview.RandDSampleReviewSuspendInfo),  # 研发样本审暂停任务信息详情页
    url(r'^RandDSampleRecoveryTaskOperation/$', RandDSampleReview.RandDSampleRecoveryTaskOperation),  # 研发样本恢复操作
    url(r'^RandDSampleReviewNotPassInfo/$', RandDSampleReview.RandDSampleReviewNotPassInfo),  # 研发样本终止任务信息详情页
    # 合同管理
    url(r'^contract_Review/$', contractToExamine.contract_Review),  # 合同信息审核列表页
    url(r'^contractToExamine/$', contractToExamine.contract_To_Examine),  # 合同信息审核详情页
    url(r'^contractToExamineOperation/$', contractToExamine.contract_Examine_Operation),  # 合同信息审核操作页
    url(r'^contractToExamine_Pass/$', contractToExamine.contract_To_Examine_Pass), # 合同已通过审核信息详情页
    url(r'^contractToExamine_Not_Pass/$', contractToExamine.contract_To_Examine_Not_Pass), # 合同不通过审核信息详情页
    url(r'^contract_reviewing_Operation/$', contractToExamine.contract_reviewing_Operation), # 合同不通过审核信息详情页
    # 临床样本实验任务分配
    url(r'^clinicalExperimentalTaskAssignment/$', sampleReview.clinical_Experimental_Task_Assignment),  # 临床样本实验任务分配列表页
    url(r'^Pretreatment_taskToExamine/$', Pretreatment_TaskToExamine.task_To_Examine), # 临床样本预处理任务未分配详情页
    url(r'^Pretreatment_taskToExamineOperation/$', Pretreatment_TaskToExamine.task_Examine_Operation), # 临床样本预处理任务分配操作
    url(r'^Pretreatment_taskToExamineDetermine/$', Pretreatment_TaskToExamine.task_To_Examine_Determine),  # 临床样本预处理任务已分配详情页
    url(r'^DNAExtract_taskToExamine/$', DNAExtract_TaskToExamine.task_To_Examine), # 临床样本DNA提取任务未分配详情页
    url(r'^DNAExtract_taskToExamineOperation/$', DNAExtract_TaskToExamine.task_Examine_Operation), # 临床样本DNA提取任务分配操作
    url(r'^DNAExtract_taskToExamineDetermine/$', DNAExtract_TaskToExamine.task_To_Examine_Determine),  # 临床样本DNA提取任务已分配详情页
    url(r'^PreLibCon_taskToExamine/$', PreLibCon_TaskToExamine.task_To_Examine),  # 临床样本预文库构建任务未分配详情页
    url(r'^PreLibCon_taskToExamineOperation/$', PreLibCon_TaskToExamine.task_Examine_Operation),  # 临床样本预文库构建任务分配操作
    url(r'^PreLibCon_taskToExamineDetermine/$', PreLibCon_TaskToExamine.task_To_Examine_Determine), # 临床样本预文库构建任务已分配详情页
    url(r'^FinLibCon_taskToExamine/$', FinLibCon_TaskToExamine.task_To_Examine),  # 临床样本终文库构建任务未分配详情页
    url(r'^FinLibCon_taskToExamineOperation/$', FinLibCon_TaskToExamine.task_Examine_Operation),  # 临床样本终文库构建任务分配操作
    url(r'^FinLibCon_taskToExamineDetermine/$', FinLibCon_TaskToExamine.task_To_Examine_Determine), # 临床样本终文库构建任务已分配详情页
    url(r'^ComputerSeq_taskToExamine/$', ComputerSeq_TaskToExamine.task_To_Examine),  # 临床样本上机测序任务未分配详情页
    url(r'^ComputerSeq_taskToExamineOperation/$', ComputerSeq_TaskToExamine.task_Examine_Operation),  # 临床样本上机测序任务分配操作
    url(r'^ComputerSeq_taskToExamineDetermine/$', ComputerSeq_TaskToExamine.task_To_Examine_Determine), # 临床样本上机测序任务已分配详情页
    url(r'^taskToExamineSuspend/$', OtherInformation_ToExamine.task_To_Examine_Suspend), # 临床样本任务已暂停详情页
    url(r'^taskToExamineStop/$', OtherInformation_ToExamine.task_To_Examine_Stop), # 临床样本任务终止详情页
    url(r'^recoveryTaskOperation/$', OtherInformation_ToExamine.recovery_Task_Operation), # 临床样本样本已暂停任务恢复操作
    url(r'^taskFinUnaud/$', OtherInformation_ToExamine.task_Fin_unaud), # 临床样本样本任务待财务审核详情页
    url(r'^contract_To_Examine_Not_Pass/$', OtherInformation_ToExamine.contract_To_Examine_Not_Pass), # 临床样本样本任务财务审核不通过详情页
    # 研发样本实验任务分配
    url(r'^RandDExperimentalTaskAssignmentHomePage/$', RandDTaskAssignment.RandDExperimentalTaskAssignmentHomePage),  # 研发样本实验任务分配首页
    url(r'^RandDSamplePretreatmentTaskInfo/$', RandDPretreatmentTaskAssignment.RandDSamplePretreatmentTaskInfo),  # 研发样本预处理任务未分配详情页
    url(r'^RandDSamplePretreatmentTaskAssignmentOperation/$', RandDPretreatmentTaskAssignment.RandDSamplePretreatmentTaskAssignmentOperation),  # 研发样本预处理任务分配操作
    url(r'^RandDSamplePretreatmentTaskDetails/$',RandDPretreatmentTaskAssignment.RandDSamplePretreatmentTaskDetails),  # 研发样本预处理任务已分配详情页
    url(r'^RandDSampleDNAExtractTaskInfo/$', RandDDNAExtractTaskAssignment.RandDSampleDNAExtractTaskInfo),  # 研发样本DNA提取任务未分配详情页
    url(r'^RandDSampleDNAExtractTaskAssignmentOperation/$',RandDDNAExtractTaskAssignment.RandDSampleDNAExtractTaskAssignmentOperation),  # 研发样本DNA提取任务分配操作
    url(r'^RandDSampleDNAExtractTaskDetails/$', RandDDNAExtractTaskAssignment.RandDSampleDNAExtractTaskDetails), # 研发样本DNA提取任务已分配详情页
    url(r'^RandDSamplePreLibTaskInfo/$', RandDPreLibConTaskAssignment.RandDSamplePreLibTaskInfo), # 研发样本预文库构建任务未分配详情页
    url(r'^RandDSamplePreLibTaskAssignmentOperation/$', RandDPreLibConTaskAssignment.RandDSamplePreLibTaskAssignmentOperation),  # 研发样本预文库构建任务分配操作
    url(r'^RandDSamplePreLibTaskDetails/$', RandDPreLibConTaskAssignment.RandDSamplePreLibTaskDetails), # 研发样本预文库构建任务已分配详情页
    url(r'^RandDSampleDFinLibTaskInfo/$', RandDFinLibConTaskAssignment.RandDSampleDFinLibTaskInfo),  # 研发样本终文库构建任务未分配详情页
    url(r'^RandDSampleFinLibTaskAssignmentOperation/$',RandDFinLibConTaskAssignment.RandDSampleFinLibTaskAssignmentOperation),  # 研发样本终文库构建任务分配操作
    url(r'^RandDSampleFinLibTaskDetails/$', RandDFinLibConTaskAssignment.RandDSampleFinLibTaskDetails),  # 研发样本终文库构建任务已分配详情页
    url(r'^RandDSampleComSeqTaskInfo/$', RandDComSeqTaskAssignment.RandDSampleComSeqTaskInfo),  # 研发样本上机测序任务未分配详情页
    url(r'^RandDSampleComSeqTaskAssignmentOperation/$', RandDComSeqTaskAssignment.RandDSampleComSeqTaskAssignmentOperation),  # 研发样本上机测序任务分配操作
    url(r'^RandDSampleComSeqTaskDetails/$', RandDComSeqTaskAssignment.RandDSampleComSeqTaskDetails),  # 研发样本上机测序任务已分配详情页
    url(r'^RandDSampleTaskSuspendInfo/$', RandDOtherInformation.RandDSampleTaskSuspendInfo),  # 研发样本任务已暂停详情页
    url(r'^RandDTaskStop/$', RandDOtherInformation.RandDTaskStop),  # 临床样本任务终止详情页
    url(r'^RandD_Recovery_Task_Operation/$', RandDOtherInformation.RandD_Recovery_Task_Operation),  # 临床样本样本已暂停任务恢复操作
    url(r'^taskFinUnaud/$', RandDOtherInformation.task_Fin_unaud),  # 临床样本样本任务待财务审核详情页
    url(r'^contract_To_Examine_Not_Pass/$', RandDOtherInformation.contract_To_Examine_Not_Pass),  # 临床样本样本任务财务审核不通过详情页
    # 临床样本预处理任务
    url(r'^PretreatmentTaskReview/$', Pretreatment.PretreatmentTask_Review),  # 预处理任务列表页
    url(r'^PretreatmentTaskToExamine/$', Pretreatment.PretreatmentTask_To_Examine),  # 预处理数据录入页
    url(r'^PretreatmentInfoToDataBases/$', Pretreatment.PretreatmentInfoToDataBases),  # 预处理任务操作页
    url(r'^PretreatmentTask_ShowData/$', Pretreatment.PretreatmentTask_ShowData),  # 预处理数据详情页
    # 研发样本预处理任务
    url(r'^RandDPretreatmentInfoInputHomePage/$', RandDSamplePretreatment.RandDPretreatmentInfoInputHomePage),  # 预处理任务列表页
    url(r'^RandDPretreatmentInfoInput/$', RandDSamplePretreatment.RandDPretreatmentInfoInput),  # 预处理数据录入页
    url(r'^RandDPretreatmentInfoToDataBases/$', RandDSamplePretreatment.RandDPretreatmentInfoToDataBases),  # 预处理任务操作页
    url(r'^RandDPretreatmentInfoShowData/$', RandDSamplePretreatment.RandDPretreatmentInfoShowData),  # 预处理数据详情页
    # 临床样本DNA提取任务
    url(r'^DNAExtractTaskReview/$', DNAExtract.DNAExtractTask_Review),  # DNA提取任务列表页
    url(r'^DNAExtractTaskToExamine/$', DNAExtract.DNAExtractTask_To_Examine),  # DNA提取数据录入页
    url(r'^DNAExtractInfoToDataBases/$', DNAExtract.DNAExtractInfoToDataBases),  # DNA提取任务操作页
    url(r'^DNAExtractTask_ShowData/$', DNAExtract.DNAExtractTask_ShowData),  # DNA提取数据详情页 RandDSampleDNAExtract
    # 研发样本DNA提取任务
    url(r'^RandDDNAExtractInfoInputHomePage/$', RandDSampleDNAExtract.RandDDNAExtractInfoInputHomePage),  # DNA提取任务列表页
    url(r'^RandDDNAExtractInfoInput/$', RandDSampleDNAExtract.RandDDNAExtractInfoInput),  # DNA提取数据录入页
    url(r'^RandDDNAExtractInfoToDataBases/$', RandDSampleDNAExtract.RandDDNAExtractInfoToDataBases),  # DNA提取任务操作页
    url(r'^RandDDNAExtractInfoShowData/$', RandDSampleDNAExtract.RandDDNAExtractInfoShowData),  # DNA提取数据详情页
    # 临床样本预文库构建任务
    url(r'^PreLibConTaskReview/$', PreLibCon.PreLibConTask_Review),  # 预文库构建任务列表页
    url(r'^PreLibContTaskToExamine/$', PreLibCon.PreLibConTask_To_Examine),  # 预文库构建任务详情页
    url(r'^PreLibConInfoToDataBases/$', PreLibCon.PreLibConInfoToDataBases),  # 预文库构建任务操作页
    url(r'^PreLibConTask_ShowData/$', PreLibCon.PreLibConTask_ShowData),  # 预文库构建数据详情页
    # 研发样本预文库构建任务
    url(r'^RandDPreLibConInfoInputHomePage/$', RandDSamplePreLibCon.RandDPreLibConInfoInputHomePage),  # 预文库构建任务列表页
    url(r'^RandDPreLibConInfoInput/$', RandDSamplePreLibCon.RandDPreLibConInfoInput),  # 预文库构建任务详情页
    url(r'^RandDPreLibConInfoToDataBases/$', RandDSamplePreLibCon.RandDPreLibConInfoToDataBases),  # 预文库构建任务操作页
    url(r'^RandDPreLibConInfoShowData/$', RandDSamplePreLibCon.RandDPreLibConInfoShowData),  # 预文库构建数据详情页
    # 临床样本终文库构建任务
    url(r'^FinLibConTaskReview/$', FinLibCon.FinLibConTask_Review),  # 终文库构建任务列表页
    url(r'^FinLibContTaskToExamine/$', FinLibCon.FinLibConTask_To_Examine),  # 终文库构建任务详情页
    url(r'^FinLibConInfoToDataBases/$', FinLibCon.FinLibConInfoToDataBases),  # 终文库构建任务操作页
    url(r'^FinLibConTask_ShowData/$', FinLibCon.FinLibConTask_ShowData),  # 终文库构建数据详情页
    # 研发样本终文库构建任务
    url(r'^RandDFinLibConInfoInputHomePage/$', RandDSampleFinLibCon.RandDFinLibConInfoInputHomePage),  # 研发终文库构建任务列表页
    url(r'^RandDFinLibConInfoInput/$', RandDSampleFinLibCon.RandDFinLibConInfoInput),  # 研发终文库构建任务详情页
    url(r'^RandDFinLibConInfoToDataBases/$', RandDSampleFinLibCon.RandDFinLibConInfoToDataBases),  # 研发终文库构建任务操作页
    url(r'^RandDFinLibConInfoShowData/$', RandDSampleFinLibCon.RandDFinLibConInfoShowData),  # 研发终文库构建数据详情页
    # 临床样本上机测序任务
    url(r'^ComSeqTaskReview/$', ComSeq.ComSeqTask_Review),  # 上机测序列任务列表页
    url(r'^ComSeqTaskToExamine/$', ComSeq.ComSeqTask_To_Examine),  # 上机测序列任务详情页
    url(r'^ComSeqInfoToDataBases/$', ComSeq.ComSeqInfoToDataBases),  # 上机测序任务操作页
    url(r'^ComSeqTask_ShowData/$', ComSeq.ComSeqTask_ShowData),  # 上机测序数据详情页
    # 临床样本上机测序任务
    url(r'^RandDComSeqInfoInputHomePage/$', RandDSampleComSeq.RandDComSeqInfoInputHomePage),  # 上机测序列任务列表页
    url(r'^RandDComSeqInfoInput/$', RandDSampleComSeq.RandDComSeqInfoInput),  # 上机测序列任务详情页
    url(r'^RandDComSeqInfoToDataBases/$', RandDSampleComSeq.RandDComSeqInfoToDataBases),  # 上机测序任务操作页
    url(r'^RandDComSeqInfoShowData/$', RandDSampleComSeq.RandDComSeqInfoShowData),  # 上机测序数据详情页
    # 生信分析任务分配
    url(r'^BioinfoTaskAssignment/$', Bioinfo_TaskToExamine.Bioinfo_Task_Assignment),  # 临床样本生信分析任务分配列表页
    url(r'^Bioinfo_taskToExamine/$', Bioinfo_TaskToExamine.task_To_Examine),  # 临床样本生信分析任务未分配详情页
    url(r'^Bioinfo_taskToExamineOperation/$', Bioinfo_TaskToExamine.task_Examine_Operation),  # 临床样本生信分析任务务分配操作
    url(r'^Bioinfo_taskToExamineDetermine/$', Bioinfo_TaskToExamine.task_To_Examine_Determine),  # 临床样本生信分析任务已分配详情页
    url(r'^Bioinfo_recoveryTaskOperation/$', Bioinfo_TaskToExamine.recovery_Task_Operation),  # 临床样本生信分析任务已分配详情页
    # 数据分析任务
    url(r'^Bioinfo_DataAnalysisTask_Review/$', Bioinfo_DataAnalysis.DataAnalysisTask_Review),  # 临床样本生信分析任务列表页
    url(r'^Bioinfo_DataAnalysisTask_To_Examine/$', Bioinfo_DataAnalysis.DataAnalysisTask_To_Examine),  # 临床样本生信分析任务未完成详情页
    url(r'^Bioinfo_DataAnalysisInfoToDataBases/$', Bioinfo_DataAnalysis.DataAnalysisInfoToDataBases),  # 临床样本生信分析任务数据录入
    url(r'^Bioinfo_DataAnalysisTask_ShowData/$', Bioinfo_DataAnalysis.DataAnalysisTask_ShowData),  # 临床样本生信分析任务已完成详情页
    # 数据分析结果审核
    url(r'^Bioinfo_DataAnalysisResult_Review/$', Bioinfo_DataAnalysis_ResultAudit.DataAnalysisResult_Review),  # 临床样本生信数据分析结果审核列表页
    url(r'^Bioinfo_DataAnalysisResult_To_Examine/$', Bioinfo_DataAnalysis_ResultAudit.DataAnalysisResult_To_Examine),  # 临床样本数据分析结果审核未完成详情页
    url(r'^Bioinfo_DataAnalysisResult_Examine_ToDataBases/$', Bioinfo_DataAnalysis_ResultAudit.DataAnalysisResult_Examine_ToDataBases),  # 临床样本数据分析结果审核录入
    url(r'^Bioinfo_DataAnalysis_Result_Examine_ShowData/$', Bioinfo_DataAnalysis_ResultAudit.DataAnalysis_Result_Examine_ShowData),  # 临床样本数据分析结果审核已完成详情页
    # 报告制作任务
    url(r'^Bioinfo_Report_Task_Review/$', Bioinfo_Report_Make.Bioinfo_Report_Task_Review),  # 临床样本生信报告制作任务列表页
    url(r'^Bioinfo_Report_Info_Input/$', Bioinfo_Report_Make.Bioinfo_Report_Info_Input), # 临床样本生信报告制作任务未完成详情页
    url(r'^Bioinfo_Report_Info_Again_Input/$', Bioinfo_Report_Make.Bioinfo_Report_Info_Again_Input), # 临床样本生信报告制作任务重新上传详情页
    url(r'^Bioinfo_Report_InfoToDataBases/$', Bioinfo_Report_Make.Bioinfo_Report_InfoToDataBases),  # 临床样本生信报告制作任务数据录入
    url(r'^Bioinfo_Report_ShowData/$', Bioinfo_Report_Make.Bioinfo_Report_ShowData),  # 临床样本生信报告制作任务已完成详情页
    url(r'^download_file/$', Bioinfo_Report_Make.download_file),  # 临床样本生信报告报告下载
    # 遗传咨询师审核报告
    url(r'^Bioinfo_Report_Medical_Audit_Task_Review/$', Bioinfo_Report_Medical_Audit.Bioinfo_Report_Medical_Audit_Task_Review),  # 遗传咨询师审核报告任务列表页
    url(r'^Bioinfo_Report_Medical_Audit_Info_Input/$', Bioinfo_Report_Medical_Audit.Bioinfo_Report_Medical_Audit_Info_Input),  # 遗传咨询师审核报告任务未完成详情页
    url(r'^Bioinfo_Report_Medical_Audit_InfoToDataBases/$', Bioinfo_Report_Medical_Audit.Bioinfo_Report_Medical_Audit_InfoToDataBases),  # 遗传咨询师审核报告任务数据录入
    url(r'^Bioinfo_Report_Medical_Audit_ShowData/$', Bioinfo_Report_Medical_Audit.Bioinfo_Report_Medical_Audit_ShowData),  # 遗传咨询师审核报告任务已完成详情页
    # 运营审核报告
    url(r'^Bioinfo_Report_Operate_Audit_Task_Review/$', Bioinfo_Report_Operate_Audit.Bioinfo_Report_Operate_Audit_Task_Review),  # 运营审核报告任务列表页
    url(r'^Bioinfo_Report_Operate_Audit_Info_Input/$', Bioinfo_Report_Operate_Audit.Bioinfo_Report_Operate_Audit_Info_Input),  # 运营审核报告任务未完成详情页
    url(r'^Bioinfo_Report_Operate_Audit_InfoToDataBases/$', Bioinfo_Report_Operate_Audit.Bioinfo_Report_Operate_Audit_InfoToDataBases),  # 运营审核报告任务数据录入
    url(r'^Bioinfo_Report_Operate_Audit_ShowData/$', Bioinfo_Report_Operate_Audit.Bioinfo_Report_Operate_Audit_ShowData),  # 运营审核报告任务已完成详情页
    # 报告发送
    url(r'^Bioinfo_Report_Send_Info_Task_Review/$', Bioinfo_Report_Send_Info.Bioinfo_Report_Send_Info_Task_Review),  # 报告发送任务列表页
    url(r'^Bioinfo_Report_Send_Info_Input/$', Bioinfo_Report_Send_Info.Bioinfo_Report_Send_Info_Input),  # 报告发送任务未完成详情页
    url(r'^Bioinfo_Report_Send_InfoToDataBases/$', Bioinfo_Report_Send_Info.Bioinfo_Report_Send_InfoToDataBases),  # 报告发送任务数据录入
    url(r'^Bioinfo_Report_Send_ShowData/$', Bioinfo_Report_Send_Info.Bioinfo_Report_Send_ShowData),  # 报告发送任务已完成详情页
    # 测试
    url(r'^test01/$', tests.test01),
]
