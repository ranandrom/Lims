# encoding: utf-8

from __future__ import unicode_literals
from django.db import models

# Create your models here.

# 用户系统消息表
class UserSystemMessage(models.Model):
    # 用户信息
    Sender = models.CharField(max_length=64)  # 发送者
    Receiver = models.CharField(max_length=64)  # 接收者
    # 信息内容
    Time = models.CharField(max_length=32)  # 信息生成时间
    Title = models.CharField(max_length=128)  # 系统消息标题
    Message = models.CharField(max_length=512)  # 系统消息正文
    ReadingState = models.CharField(max_length=16)  # 信息阅读状态

# 用户访问权限信息表
class UserInfo(models.Model):
    # 用户信息
    username = models.CharField(max_length=64)  # 用户名
    department = models.CharField(max_length=64)  # 部门
    DefaultMark = models.CharField(max_length=16)  # 默认标记
    # 样本管理模块
    SampleManagement = models.CharField(max_length=16)  # 样本管理
    ClinicalSampleRegistration = models.CharField(max_length=16)   # 样本登记（临检）
    sampleReview = models.CharField(max_length=16)  # 收样审核（临检）
    clinicalExperimentalTaskAssignment = models.CharField(max_length=16)  # 任务分派（临检）
    PretreatmentTaskReview = models.CharField(max_length=16)  # 样本预处理（临检）
    DNAExtractTaskReview = models.CharField(max_length=16)  # DNA提取（临检）
    PreLibConTaskReview = models.CharField(max_length=16)  # 预文库构建（临检）
    FinLibConTaskReview = models.CharField(max_length=16)  # 终文库构建（临检）
    ComSeqTaskReview = models.CharField(max_length=16)  # 上机测序（临检）
    # 项目管理模块
    projectManagement = models.CharField(max_length=16)  # 项目管理
    RandDSampleInfoInputHomePage = models.CharField(max_length=16)   # 收样登记（研发）
    RandDSampleReviewHomePage = models.CharField(max_length=16)  # 收样审核（研发）
    RandDExperimentalTaskAssignmentHomePage = models.CharField(max_length=16)  # 任务分派（研发）
    RandDPretreatmentInfoInputHomePage = models.CharField(max_length=16)  # 样本预处理（研发）
    RandDDNAExtractInfoInputHomePage = models.CharField(max_length=16)  # DNA提取（研发）
    RandDPreLibConInfoInputHomePage = models.CharField(max_length=16)  # 预文库构建（研发）
    RandDFinLibConInfoInputHomePage = models.CharField(max_length=16)  # 终文库构建（研发）
    RandDComSeqInfoInputHomePage = models.CharField(max_length=16)  # 上机测序（研发）
    # 合同管理模块
    contractManagement = models.CharField(max_length=16)  # 合同管理
    contractReview = models.CharField(max_length=16)   # 合同审核
    # 生信分析模块
    BioinfoAnalysis = models.CharField(max_length=16)  # 生信分析
    BioinfoTaskAssignment = models.CharField(max_length=16)  # 分析任务分派
    BioinfoDataAnalysisTaskReview = models.CharField(max_length=16)  # 数据分析结果
    BioinfoDataAnalysisResultReview = models.CharField(max_length=16)  # 分析结果审核
    BioinfoReportTaskReview = models.CharField(max_length=16)  # 报告生成
    # 报告管理模块
    ReportManagement = models.CharField(max_length=16)  # 报告管理
    BioinfoReportMedicalAuditTaskReview = models.CharField(max_length=16)  # 遗传咨询师审核报告
    BioinfoReportOperateAuditTaskReview = models.CharField(max_length=16)  # 运营审核报告
    # 商务管理模块
    BusinessAffairsManagement = models.CharField(max_length=16)  # 商务管理
    BioinfoReportSendInfoTaskReview = models.CharField(max_length=16)  # 报告发送

# 用户操作权限信息表
class UserOperationPermissionsInfo(models.Model):
    # 用户信息
    username = models.CharField(max_length=64)  # 用户名
    department = models.CharField(max_length=64)  # 部门
    DefaultMark = models.CharField(max_length=16)  # 默认标记
    # 样本管理模块
    ClinicalSampleRegistration = models.CharField(max_length=16)   # 样本登记（临检）
    sampleReview = models.CharField(max_length=16)  # 收样审核（临检）
    clinicalExperimentalTaskAssignment = models.CharField(max_length=16)  # 任务分派（临检）
    PretreatmentTaskReview = models.CharField(max_length=16)  # 样本预处理（临检）
    DNAExtractTaskReview = models.CharField(max_length=16)  # DNA提取（临检）
    PreLibConTaskReview = models.CharField(max_length=16)  # 预文库构建（临检）
    FinLibConTaskReview = models.CharField(max_length=16)  # 终文库构建（临检）
    ComSeqTaskReview = models.CharField(max_length=16)  # 上机测序（临检）
    # 项目管理模块
    RandDSampleInfoInputHomePage = models.CharField(max_length=16)   # 收样登记（研发）
    RandDSampleReviewHomePage = models.CharField(max_length=16)  # 收样审核（研发）
    RandDExperimentalTaskAssignmentHomePage = models.CharField(max_length=16)  # 任务分派（研发）
    RandDPretreatmentInfoInputHomePage = models.CharField(max_length=16)  # 样本预处理（研发）
    RandDDNAExtractInfoInputHomePage = models.CharField(max_length=16)  # DNA提取（研发）
    RandDPreLibConInfoInputHomePage = models.CharField(max_length=16)  # 预文库构建（研发）
    RandDFinLibConInfoInputHomePage = models.CharField(max_length=16)  # 终文库构建（研发）
    RandDComSeqInfoInputHomePage = models.CharField(max_length=16)  # 上机测序（研发）
    # 合同管理模块
    contractReview = models.CharField(max_length=16)   # 合同审核
    # 生信分析模块
    BioinfoTaskAssignment = models.CharField(max_length=16)  # 分析任务分派
    BioinfoDataAnalysisTaskReview = models.CharField(max_length=16)  # 数据分析结果
    BioinfoDataAnalysisResultReview = models.CharField(max_length=16)  # 分析结果审核
    BioinfoReportTaskReview = models.CharField(max_length=16)  # 报告生成
    # 报告管理模块
    BioinfoReportMedicalAuditTaskReview = models.CharField(max_length=16)  # 遗传咨询师审核报告
    BioinfoReportOperateAuditTaskReview = models.CharField(max_length=16)  # 运营审核报告
    # 商务管理模块
    BioinfoReportSendInfoTaskReview = models.CharField(max_length=16)  # 报告发送

# 临检收样信息表
class clinicalSampleInfo(models.Model):
    # 用户信息
    username = models.CharField(max_length=64)  # 用户名
    department = models.CharField(max_length=64)  # 部门
    # 患者信息
    sam_code_num = models.CharField(max_length=64)  # 样本条码号
    PatientName = models.CharField(max_length=64)  # 患者姓名
    PatientAge = models.CharField(max_length=16)  # 患者年龄（岁）
    PatientSex = models.CharField(max_length=16)   # 患者性别
    PatientBirthday = models.CharField(max_length=64)    # 患者身份证号码
    PatientPhoneNumber = models.CharField(max_length=64)  # 患者联系电话
    PatientEmail = models.CharField(max_length=64)  # 患者电子邮箱
    PatientAddress = models.CharField(max_length=64)   # 报告接收地址
    treatment_hospital = models.CharField(max_length=64)   # 就诊医院
    treatment_department = models.CharField(max_length=64)  # 就诊科室
    AttendingDoctor = models.CharField(max_length=64)   # 主治医生
    DoctorEmail = models.CharField(max_length=64)   # 医生邮箱
    # 样本信息
    Pathological_diagnosis = models.CharField(max_length=64)  # 病理诊断
    clinical_diagnosis = models.CharField(max_length=64)  # 临床诊断
    Clinical_stage = models.CharField(max_length=32)  # 临床分期
    is_tubercle_history = models.CharField(max_length=32)   # 结核病史
    tubercle_distribution = models.CharField(max_length=64)    # 结节大小和分布
    sample_source = models.CharField(max_length=64)  # 样本来源
    acquisition_time = models.CharField(max_length=32)  # 采集时间
    family_history = models.CharField(max_length=64)   # 家族史
    receiving_time = models.CharField(max_length=32)   # 送检时间
    sample_count = models.CharField(max_length=32)  # 样本数量
    sample_type = models.CharField(max_length=64)   # 样本类型
    sample_type_text = models.CharField(max_length=64)   # 样本类型描述
    infection_history = models.CharField(max_length=64)   # 传染病史
    # 基因检测史
    detected_gene_time = models.CharField(max_length=512)   # 检测时间
    detected_gene_name = models.CharField(max_length=512)   # 检测基因
    detected_gene_result = models.CharField(max_length=512)   # 检测结果
    # 曾有治疗史
    treatment_history_surgery = models.CharField(max_length=64)   # 手术
    treatment_history_chem = models.CharField(max_length=64)   # 化疗
    treatment_history_therapy = models.CharField(max_length=64)   # 靶向治疗
    # 合同信息
    contract_name = models.CharField(max_length=64)  # 合同名称
    contract_pay = models.CharField(max_length=64)  # 合同金额（人民币）
    pay_way = models.CharField(max_length=64)  # 支付方式
    pos_code = models.CharField(max_length=64)   # pos单号(交易参考号)
    Client = models.CharField(max_length=32)    # 业务员
    remarks = models.CharField(max_length=512)  # 其它（备注）
    ContractAuditor = models.CharField(max_length=64)  # 合同审核人
    # 检测方案
    cancer_type = models.CharField(max_length=64)  # 癌种
    detection_type = models.CharField(max_length=32)   # 类型
    product_name = models.CharField(max_length=64)   # 产品名称
    is_return = models.CharField(max_length=32)  # 剩余样本是否退回
    is_invoice = models.CharField(max_length=32)   # 是否需要发票
    # 审核标记
    contract_review = models.CharField(max_length=16)    # 合同审核标记
    sample_review = models.CharField(max_length=16)    # 样本审核标记
    task_assignment = models.CharField(max_length=16)  # 样本任务分派标记
    Pretreatment_Sign = models.CharField(max_length=16)  # 样本预处理标记
    DNAExtract_Sign = models.CharField(max_length=16)  # DNA提取任务标记
    # 样本审核信息
    ExperimentNumber = models.CharField(max_length=64)  # 实验编号
    CollectSamplesDate = models.CharField(max_length=32)  # 收样时间
    Review_Time = models.CharField(max_length=32)  # 样本审核时间
    ReviewResult = models.CharField(max_length=16)  # 样本审核结果
    Reason = models.CharField(max_length=512)  # 样本审核备注
    SampleAuditor = models.CharField(max_length=64)  # 样本审核人
    # 任务分配信息
    Next_TaskProgress = models.CharField(max_length=64)  # 下一步任务进度
    Next_TaskProgress_Man = models.CharField(max_length=64)  # 下一步任务接收者
    Next_TaskProgress_Time = models.CharField(max_length=32)  # 下一步任务分配时间
    Next_TaskProgress_Remarks = models.CharField(max_length=512)  # 下一步任务备注
    Next_TaskProgress_Sign = models.CharField(max_length=16)  # 下一步任务分配标记
    #其他信息
    ExperimentTimes = models.CharField(max_length=16)  # 实验次数
    contract_Times = models.CharField(max_length=16)  # 财务审核次数
    TaskAssignment = models.CharField(max_length=64)  # 实验任务分派人
    # 组织样本标记
    TissueSampleSign = models.CharField(max_length=16)  # 组织样本标记

# 研发收样信息表
class RandDSampleInfo(models.Model):
    # 用户信息
    username = models.CharField(max_length=64)  # 用户名
    department = models.CharField(max_length=64)  # 部门
    # 样本编号
    sam_code_num = models.CharField(max_length=64)  # 样本编号
    # 医院信息
    HospitalForInspection = models.CharField(max_length=64)  # 送检医院
    Contacts = models.CharField(max_length=32)  # 联系人
    # 收样信息
    SamplingTime_Blood = models.CharField(max_length=32)  # 收样时间（血样）
    SamplingTime_Tissue = models.CharField(max_length=32)  # 收样时间（组织）
    Collector = models.CharField(max_length=32)  # 收样人
    # 项目信息
    InpatientNumber = models.CharField(max_length=32)   # 住院号
    PathologicalNumber = models.CharField(max_length=32)   # 病理号
    CorrelationNumber = models.CharField(max_length=64)   # 相关编号
    # 样本信息
    PatientName = models.CharField(max_length=32)   # 患者姓名
    PatientAge = models.CharField(max_length=16)  # 患者年龄（岁）
    PatientSex = models.CharField(max_length=16)  # 患者性别
    BloodSampleType = models.CharField(max_length=16)  # 血样类型
    BloodSamplingTime = models.CharField(max_length=32)  # 采血时间
    TissueSampleSources = models.CharField(max_length=32)  # 组织样本来源
    TissueQuantity = models.CharField(max_length=16)  # 组织数量
    TissueType = models.CharField(max_length=16)  # 组织类型
    TissueSampleProcessing = models.CharField(max_length=32)  # 组织样本处理方式
    # 临床信息
    OperationDate = models.CharField(max_length=16)  # 手术日期
    PathologicalInfo = models.CharField(max_length=32)  # 病理信息
    TNMStaging = models.CharField(max_length=32)  # TNM分期
    Stage = models.CharField(max_length=32)   # Stage
    MolecularDiagnosticInfo = models.CharField(max_length=32)    # 分子诊断信息
    Classification = models.CharField(max_length=32)  # 分类
    # 存放信息
    PlasmaUse = models.CharField(max_length=16)  # 血浆用途
    TissueUse = models.CharField(max_length=16)   # 组织用途
    PlasmaStoragePosition = models.CharField(max_length=32)   # 血浆存放位置
    TissueStoragePosition = models.CharField(max_length=32)  # 组织存放位置
    # 样本审核信息
    ContractAuditor = models.CharField(max_length=64)  # 合同审核人
    SampleAuditor = models.CharField(max_length=64)  # 样本审核人
    TaskAssignment = models.CharField(max_length=64)  # 实验任务分派人
    ReviewTime = models.CharField(max_length=32)  # 样本审核时间
    ReviewResult = models.CharField(max_length=16)    # 样本审核结果
    ReviewRemarks = models.CharField(max_length=512)  # 样本审核备注
    # 审核标记
    sample_review = models.CharField(max_length=16)    # 样本审核标记
    Pretreatment_Sign = models.CharField(max_length=16)  # 样本预处理标记
    DNAExtract_Sign = models.CharField(max_length=16)  # DNA提取任务标记
    # task_assignment = models.CharField(max_length=16)  # 样本任务分派标记
    # 任务分配信息
    Next_TaskProgress = models.CharField(max_length=64)  # 下一步任务进度
    Next_TaskProgress_Man = models.CharField(max_length=64)  # 下一步任务接收者
    Next_TaskProgress_Time = models.CharField(max_length=32)  # 下一步任务分配时间
    Next_TaskProgress_Remarks = models.CharField(max_length=512)  # 下一步任务备注
    Next_TaskProgress_Sign = models.CharField(max_length=16)  # 下一步任务分配标记
    # 组织样本标记
    TissueSampleSign = models.CharField(max_length=16)  # 组织样本标记

# 临检样本财务审核信息表
class contractReviewInfo(models.Model):
    # 用户信息
    username = models.CharField(max_length=64)  # 用户名
    department = models.CharField(max_length=64)  # 部门
    # 样本信息
    sam_code_num = models.CharField(max_length=64)  # 样本条码号
    ExperimentNumber = models.CharField(max_length=64)  # 实验编号
    # 合同审核信息
    Receivables = models.CharField(max_length=128)  # 收款金额
    ReceivablesDate = models.CharField(max_length=256)  # 收款时间
    contract_Time = models.CharField(max_length=32)  # 财务审核时间
    contractReviewReason = models.CharField(max_length=512)  # 财务审核备注
    #其他信息
    ExperimentTimes = models.CharField(max_length=16)  # 财务审核次数

# 临检样本预处理信息表
class clinicalSamplePretreatment(models.Model):
    # 用户信息
    username = models.CharField(max_length=64)  # 用户名
    department = models.CharField(max_length=64)  # 部门
    # 样本信息
    sam_code_num = models.CharField(max_length=64)  # 样本条码号
    ExperimentNumber = models.CharField(max_length=64)  # 实验编号
    # 样本预处理信息
    Types_of_blood_vessel = models.CharField(max_length=16)  # 采血管类型（选择streck、EDTA抗凝）
    number_of_plasma = models.CharField(max_length=32)  # 分离后血浆管数（自填、也可不填）
    Plasma_volume = models.CharField(max_length=32)  # 血浆体积(mL)、可不填
    number_of_white_blood_cells = models.CharField(max_length=32)   # 白细胞管数（可不填）
    Leukocyte_volume = models.CharField(max_length=64)    # 白细胞体积(mL)、可不填
    Operator = models.CharField(max_length=32)  # 操作人（必填项）
    Operating_time = models.CharField(max_length=32)  # 操作时间（系统自动生成）
    Pretreatment_remarks = models.CharField(max_length=512)   # 其它（备注）
    # 审核信息
    Next_TaskProgress = models.CharField(max_length=64)  # 下一步任务进度
    Next_TaskProgress_Man = models.CharField(max_length=64)  # 下一步任务接收者
    Next_TaskProgress_Time = models.CharField(max_length=32)  # 下一步任务分配时间
    Next_TaskProgress_Remarks = models.CharField(max_length=512)  # 下一步任务备注
    Next_TaskProgress_Sign = models.CharField(max_length=16)  # 下一步任务分配标记
    # 其他信息
    DNAExtract_Sign = models.CharField(max_length=16)  # DNA提取任务标记

# 研发样本预处理信息表
class RandDSamplePretreatmentInfo(models.Model):
    # 用户信息
    username = models.CharField(max_length=64)  # 用户名
    department = models.CharField(max_length=64)  # 部门
    # 样本信息
    sam_code_num = models.CharField(max_length=64)  # 样本编号
    # 样本预处理信息
    Plasma_volume = models.CharField(max_length=32)  # 血浆总体积(mL)
    Division_Tube_Number = models.CharField(max_length=32)  # 分装管数
    number_of_white_blood_cells = models.CharField(max_length=32)  # 白细胞分离管数
    isHemolysis = models.CharField(max_length=16)   # 是否溶血
    isFatBlood = models.CharField(max_length=16)    # 是否脂血
    Type_of_blood_vessel = models.CharField(max_length=32)  # 采血管类型
    Blood_sharing_time = models.CharField(max_length=32)  # 分血时间
    # Operator = models.CharField(max_length=32)  # 操作人（必填项）
    # Operating_time = models.CharField(max_length=32)  # 操作时间（系统自动生成）
    Pretreatment_remarks = models.CharField(max_length=512)   # 其它（备注）
    # 审核信息
    Next_TaskProgress = models.CharField(max_length=16)  # 下一步任务进度
    Next_TaskProgress_Man = models.CharField(max_length=32)  # 下一步任务接收者
    Next_TaskProgress_Time = models.CharField(max_length=32)  # 下一步任务分配时间
    Next_TaskProgress_Remarks = models.CharField(max_length=512)  # 下一步任务备注
    Next_TaskProgress_Sign = models.CharField(max_length=16)  # 下一步任务分配标记
    # 其他信息
    DNAExtract_Sign = models.CharField(max_length=16)  # DNA提取任务标记

# 临检DNA提取信息表
class DNAExtractInfo(models.Model):
    # 用户信息
    username = models.CharField(max_length=64)  # 用户名
    department = models.CharField(max_length=64)  # 部门
    # 样本信息
    sam_code_num = models.CharField(max_length=64)  # 样本条码号
    ExperimentNumber = models.CharField(max_length=64)  # 实验编号
    # DNA提取信息
    DNA_Concentration = models.CharField(max_length=32)  # DNA浓度(ng/µL)
    DNA_volume = models.CharField(max_length=32)  # DNA体积(µL)
    DNA_Total = models.CharField(max_length=32)  # DNA总量(ng)
    Quality_inspection_method = models.CharField(max_length=32)   # 质检方法
    Quality_inspection_result = models.CharField(max_length=64)    # 质检结果
    Quality_inspection_volume = models.CharField(max_length=32)  # 质检使用体积(µL)
    Residual_volume = models.CharField(max_length=32)  # 剩余体积(µL)
    Extraction_kit_type = models.CharField(max_length=128)   # 提取试剂盒类型
    DNA_extraction_people = models.CharField(max_length=32)   # DNA提取人
    DNA_extraction_time = models.CharField(max_length=32)  # 提取时间
    DNA_extraction_remarks = models.CharField(max_length=512)   # 其它（备注）
    # 审核信息
    Next_TaskProgress = models.CharField(max_length=64)  # 下一步任务进度
    Next_TaskProgress_Man = models.CharField(max_length=64)  # 下一步任务接收者
    Next_TaskProgress_Time = models.CharField(max_length=32)  # 下一步任务分配时间
    Next_TaskProgress_Remarks = models.CharField(max_length=512)  # 下一步任务备注
    Next_TaskProgress_Sign = models.CharField(max_length=16)  # 下一步任务分配标记
    # 其他信息
    ExperimentTimes = models.CharField(max_length=16)  # DNA提取实验次数
    PreLibCon_Sign = models.CharField(max_length=16)  # 预文库构建任务标记

# 研发DNA提取信息表
class RandDSampleDNAExtractInfo(models.Model):
    # 用户信息
    username = models.CharField(max_length=64)  # 用户名
    department = models.CharField(max_length=64)  # 部门
    # 样本信息
    sam_code_num = models.CharField(max_length=64)  # 样本编号
    # DNA提取信息
    DNASampleName = models.CharField(max_length=32)  # DNA样品名称
    PlasmaVolume = models.CharField(max_length=32)  # 血浆体积(mL)
    QuantitativeMethod = models.CharField(max_length=32)  # 定量方式
    DNA_Concentration = models.CharField(max_length=32)  # DNA浓度(ng/µL)
    DNA_volume = models.CharField(max_length=32)  # DNA体积(µL)
    DNA_Total = models.CharField(max_length=32)  # DNA总量(ng)
    A260_A280 = models.CharField(max_length=32)  # A260/A280
    A260_A230 = models.CharField(max_length=32)  # A260/A230
    Extraction_kit_type = models.CharField(max_length=128)  # 提取试剂盒类型
    DNA_extraction_time = models.CharField(max_length=32)  # 提取时间
    Quality_inspection_method = models.CharField(max_length=32)   # 质检方式
    Quality_inspection_result = models.CharField(max_length=32)    # 质检结果
    Glue_map_link = models.CharField(max_length=64)  # 胶图链接
    DNA_storage_location = models.CharField(max_length=32)  # DNA存储位置
    DNA_extraction_Operator = models.CharField(max_length=32)   # DNA提取人
    DNA_extraction_remarks = models.CharField(max_length=512)   # 其它（备注）
    # 审核信息
    Next_TaskProgress = models.CharField(max_length=32)  # 下一步任务进度
    Next_TaskProgress_Man = models.CharField(max_length=32)  # 下一步任务接收者
    Next_TaskProgress_Time = models.CharField(max_length=32)  # 下一步任务分配时间
    Next_TaskProgress_Remarks = models.CharField(max_length=512)  # 下一步任务备注
    Next_TaskProgress_Sign = models.CharField(max_length=16)  # 下一步任务分配标记
    # 其他信息
    ExperimentTimes = models.CharField(max_length=16)  # DNA提取实验次数
    PreLibCon_Sign = models.CharField(max_length=16)  # 预文库构建任务标记

# 临检预文库构建信息表
class PreLibConInfo(models.Model):
    # 用户信息
    username = models.CharField(max_length=64)  # 用户名
    department = models.CharField(max_length=64)  # 部门
    # 样本信息
    sam_code_num = models.CharField(max_length=64)  # 样本条码号
    ExperimentNumber = models.CharField(max_length=64)  # 实验编号
    # 预文库构建信息
    DNA_Concentration = models.CharField(max_length=32)  # 预文库浓度(ng/µL)
    DNA_volume = models.CharField(max_length=32)  # DNA体积(µL)
    DNA_Total = models.CharField(max_length=32)  # DNA总量(ng)
    Indexi5i7 = models.CharField(max_length=32)  # Indexi5i7
    Quality_inspection_method = models.CharField(max_length=32)   # 质检方法
    Quality_inspection_result = models.CharField(max_length=64)    # 质检结果
    Quality_inspection_volume = models.CharField(max_length=32)  # 质检使用体积(µL)
    Quality_inspection_mass = models.CharField(max_length=32)  # 质检使用质量(ng)
    Residual_volume = models.CharField(max_length=32)  # 剩余体积(µL)
    Residual_mass = models.CharField(max_length=32)  # 剩余质量(ng)
    Build_lib_method = models.CharField(max_length=128)   # 建库方法（可选Batman、Ironman）
    Build_lib_man = models.CharField(max_length=32)   # 建库人
    Build_lib_time = models.CharField(max_length=32)  # 建库时间（系统默认时间）
    Build_lib_remarks = models.CharField(max_length=512)   # 其它（备注）
    # 审核信息
    Next_TaskProgress = models.CharField(max_length=64)  # 下一步任务进度
    Next_TaskProgress_Man = models.CharField(max_length=64)  # 下一步任务接收者
    Next_TaskProgress_Time = models.CharField(max_length=32)  # 下一步任务分配时间
    Next_TaskProgress_Remarks = models.CharField(max_length=512)  # 下一步任务备注
    Next_TaskProgress_Sign = models.CharField(max_length=16)  # 下一步任务分配标记
    # 其他信息
    DNA_extraction_num = models.CharField(max_length=16)  # DNA提取实验次数
    ExperimentTimes = models.CharField(max_length=16)  # 预文库构建实验次数
    FinalLibCon_Sign = models.CharField(max_length=16)  # 终文库构建任务标记

# 研发预文库构建信息表
class RandDSamplePreLibConInfo(models.Model):
    # 用户信息
    username = models.CharField(max_length=64)  # 用户名
    department = models.CharField(max_length=64)  # 部门
    # 样本信息
    sam_code_num = models.CharField(max_length=64)  # 样本编号
    # 预文库构建信息
    PreLibConName = models.CharField(max_length=64)  # 预文库名称
    InitialAmountOfTransformation = models.CharField(max_length=32)  # 转化起始量（ng）
    InitialQuantityOfPreLibCon = models.CharField(max_length=32)  # 建库起始量（ng）
    DNA_Concentration = models.CharField(max_length=32)  # 浓度(ng/µL)
    DNA_volume = models.CharField(max_length=32)  # 体积(µL)
    DNA_Total = models.CharField(max_length=32)  # DNA总量(ng)
    Index_i5 = models.CharField(max_length=32)  # Index-i5
    Index_i7 = models.CharField(max_length=32)  # Index-i7
    Build_lib_method = models.CharField(max_length=128)   # 建库方法（可选Batman、Ironman）
    Build_lib_time = models.CharField(max_length=32)  # 建库时间
    PreLibCon_storage_location = models.CharField(max_length=32)  # 预文库存储位置
    Build_lib_man = models.CharField(max_length=32)  # 建库人
    Quality_inspection_result = models.CharField(max_length=64)  # 质检结果
    Glue_map_link = models.CharField(max_length=64)  # 胶图链接
    ConversionKitNumber = models.CharField(max_length=32)  # 转化试剂盒编号
    NumberOfLibraryKit = models.CharField(max_length=32)  # 建库试剂盒编号
    Build_lib_remarks = models.CharField(max_length=512)   # 其它（备注）
    # 审核信息
    Next_TaskProgress = models.CharField(max_length=64)  # 下一步任务进度
    Next_TaskProgress_Man = models.CharField(max_length=64)  # 下一步任务接收者
    Next_TaskProgress_Time = models.CharField(max_length=32)  # 下一步任务分配时间
    Next_TaskProgress_Remarks = models.CharField(max_length=512)  # 下一步任务备注
    Next_TaskProgress_Sign = models.CharField(max_length=16)  # 下一步任务分配标记
    # 其他信息
    DNA_extraction_num = models.CharField(max_length=16)  # DNA提取实验次数
    ExperimentTimes = models.CharField(max_length=16)  # 预文库构建实验次数
    FinalLibCon_Sign = models.CharField(max_length=16)  # 终文库构建任务标记

# 临检终文库构建信息表
class FinLibConInfo(models.Model):
    # 用户信息
    username = models.CharField(max_length=64)  # 用户名
    department = models.CharField(max_length=64)  # 部门
    # 样本信息
    sam_code_num = models.CharField(max_length=64)  # 样本条码号
    ExperimentNumber = models.CharField(max_length=64)  # 实验编号
    # 终文库构建信息
    FinLibConName = models.CharField(max_length=32)  # 终文库名称
    DNA_Concentration = models.CharField(max_length=32)  # 浓度(ng/µL)
    DNA_volume = models.CharField(max_length=32)  # DNA体积(µL)
    DNA_Total = models.CharField(max_length=32)  # DNA总量(ng)
    Indexi5i7 = models.CharField(max_length=32)  # Indexi5i7
    Panel = models.CharField(max_length=32)  # 捕获panel
    Quality_inspection_method = models.CharField(max_length=32)   # 质检方法
    Quality_inspection_result = models.CharField(max_length=64)    # 质检结果
    Quality_inspection_volume = models.CharField(max_length=32)  # 质检使用体积(µL)
    Quality_inspection_mass = models.CharField(max_length=32)  # 质检使用质量(ng)
    Residual_volume = models.CharField(max_length=32)  # 剩余体积(µL)
    Residual_mass = models.CharField(max_length=32)  # 剩余质量(ng)
    # Build_lib_method = models.CharField(max_length=128)   # 建库方法（可选Batman、Ironman）
    Build_lib_man = models.CharField(max_length=32)   # 建库人
    Build_lib_time = models.CharField(max_length=32)  # 建库时间（系统默认时间）
    Build_lib_remarks = models.CharField(max_length=512)   # 其它（备注）
    # 审核信息
    Next_TaskProgress = models.CharField(max_length=64)  # 下一步任务进度
    Next_TaskProgress_Man = models.CharField(max_length=64)  # 下一步任务接收者
    Next_TaskProgress_Time = models.CharField(max_length=32)  # 下一步任务分配时间
    Next_TaskProgress_Remarks = models.CharField(max_length=512)  # 下一步任务备注
    Next_TaskProgress_Sign = models.CharField(max_length=16)  # 下一步任务分配标记
    # 其他信息
    DNA_extraction_num = models.CharField(max_length=16)  # DNA提取实验次数
    Build_Prelib_num = models.CharField(max_length=16)  # 预文库构建实验次数
    ExperimentTimes = models.CharField(max_length=16)  # 终文库构建实验次数
    ComputerSeq_Sign = models.CharField(max_length=16)  # 上机测序任务标记

# 研发终文库构建信息表
class RandDSampleFinLibConInfo(models.Model):
    # 用户信息
    username = models.CharField(max_length=64)  # 用户名
    department = models.CharField(max_length=64)  # 部门
    # 样本信息
    sam_code_num = models.CharField(max_length=64)  # 样本编号
    # 终文库构建信息
    PreLibConName = models.CharField(max_length=64)  # 预文库名称
    PoolInternalLibNumber = models.CharField(max_length=32)  # Pool内文库数目
    FinLibConName = models.CharField(max_length=32)  # 终文库名称
    DNA_Concentration = models.CharField(max_length=32)  # 浓度(ng/µL)
    DNA_volume = models.CharField(max_length=32)  # 体积(µL)
    DNA_Total = models.CharField(max_length=32)  # DNA总量(ng)
    Indexi5i7 = models.CharField(max_length=32)  # Indexi5i7
    Panel = models.CharField(max_length=32)  # 捕获panel
    Build_lib_time = models.CharField(max_length=32)  # 建库时间
    FinLibCon_storage_location = models.CharField(max_length=32)  # 终文库存储位置
    Build_lib_man = models.CharField(max_length=32)  # 建库人
    SequencingInfo = models.CharField(max_length=64)   # Sequencing Info
    Build_lib_remarks = models.CharField(max_length=512)   # 其它（备注）
    # 审核信息
    Next_TaskProgress = models.CharField(max_length=64)  # 下一步任务进度
    Next_TaskProgress_Man = models.CharField(max_length=64)  # 下一步任务接收者
    Next_TaskProgress_Time = models.CharField(max_length=32)  # 下一步任务分配时间
    Next_TaskProgress_Remarks = models.CharField(max_length=512)  # 下一步任务备注
    Next_TaskProgress_Sign = models.CharField(max_length=16)  # 下一步任务分配标记
    # 其他信息
    DNA_extraction_num = models.CharField(max_length=16)  # DNA提取实验次数
    Build_Prelib_num = models.CharField(max_length=16)  # 预文库构建实验次数
    ExperimentTimes = models.CharField(max_length=16)  # 终文库构建实验次数
    ComputerSeq_Sign = models.CharField(max_length=16)  # 上机测序任务标记

# 临检上机测序信息表
class ComputerSeqInfo(models.Model):
    # 用户信息
    username = models.CharField(max_length=64)  # 用户名
    department = models.CharField(max_length=64)  # 部门
    # 样本信息
    sam_code_num = models.CharField(max_length=64)  # 样本条码号
    ExperimentNumber = models.CharField(max_length=64)  # 实验编号
    # 上机测序信息
    DilutionMultiple = models.CharField(max_length=16)  # 稀释倍数
    qPCR = models.CharField(max_length=16)  # qPCR测量值(pM)
    AverageLengthLibrary = models.CharField(max_length=32)  # 文库平均长度(bp)
    LibEffConcentration = models.CharField(max_length=32)  # 文库有效浓度(nM)
    QuantitativeHuman = models.CharField(max_length=32)   # 定量人
    OperatingTime = models.CharField(max_length=32)  # 操作时间（系统默认）
    SeqRemarks = models.CharField(max_length=512)   # 其它（备注）
    # 审核信息
    ReviewResult = models.CharField(max_length=16)  # 样本审核结果
    DataPath = models.CharField(max_length=64)  # 数据下机路径
    Next_TaskProgress_Man = models.CharField(max_length=64)  # 下一步任务接收者
    Next_TaskProgress_Time = models.CharField(max_length=32)  # 下一步任务分配时间
    Next_TaskProgress_Remarks = models.CharField(max_length=512)  # 下一步任务备注
    Next_TaskProgress_Sign = models.CharField(max_length=16)  # 下一步任务分配标记
    # 其他信息
    BioTaskAssignment = models.CharField(max_length=64)  # 生信分析任务分派人
    DNA_extraction_num = models.CharField(max_length=16)  # DNA提取实验次数
    Build_Prelib_num = models.CharField(max_length=16)  # 预文库构建实验次数
    Build_finlib_num = models.CharField(max_length=16)  # 终文库构建实验次数
    ExperimentTimes = models.CharField(max_length=16)  # 上机测序实验次数
    Bioinfo_Sign = models.CharField(max_length=16)  # 生信任务标记

# 研发上机测序信息表
class RandDSampleComputerSeqInfo(models.Model):
    # 用户信息
    username = models.CharField(max_length=64)  # 用户名
    department = models.CharField(max_length=64)  # 部门
    # 样本信息
    sam_code_num = models.CharField(max_length=64)  # 样本编号
    # 上机测序信息
    PreLibConName = models.CharField(max_length=64)  # 预文库名称
    FinLibConName = models.CharField(max_length=32)  # 终文库名称
    DNA_Concentration = models.CharField(max_length=32)  # 浓度(ng/µL)
    DilutionMultiple = models.CharField(max_length=16)  # 稀释倍数
    qPCR = models.CharField(max_length=16)  # qPCR测量值(pM)
    AverageLengthLibrary = models.CharField(max_length=32)  # 文库平均长度(bp)
    LibEffConcentration = models.CharField(max_length=32)  # 文库有效浓度(nM)
    QuantitativeTime = models.CharField(max_length=32)  # 定量时间
    FinLibCon_storage_location = models.CharField(max_length=32)  # 终文库存储位置
    QuantitativeHuman = models.CharField(max_length=32)   # 定量人
    SeqRemarks = models.CharField(max_length=512)   # 其它（备注）
    # 审核信息
    ReviewResult = models.CharField(max_length=16)  # 样本审核结果
    DataPath = models.CharField(max_length=64)  # 数据下机路径
    Next_TaskProgress_Man = models.CharField(max_length=64)  # 下一步任务接收者
    Next_TaskProgress_Time = models.CharField(max_length=32)  # 下一步任务分配时间
    Next_TaskProgress_Remarks = models.CharField(max_length=512)  # 下一步任务备注
    Next_TaskProgress_Sign = models.CharField(max_length=16)  # 下一步任务分配标记
    # 其他信息
    BioTaskAssignment = models.CharField(max_length=64)  # 生信分析任务分派人
    DNA_extraction_num = models.CharField(max_length=16)  # DNA提取实验次数
    Build_Prelib_num = models.CharField(max_length=16)  # 预文库构建实验次数
    Build_finlib_num = models.CharField(max_length=16)  # 终文库构建实验次数
    ExperimentTimes = models.CharField(max_length=16)  # 上机测序实验次数
    Bioinfo_Sign = models.CharField(max_length=16)  # 生信任务标记

# 生信数据分析信息表
class BioinfoDataAnalysisInfo(models.Model):
    # 用户信息
    username = models.CharField(max_length=64)  # 用户名
    department = models.CharField(max_length=64)  # 部门
    # 样本信息
    sam_code_num = models.CharField(max_length=64)  # 样本条码号
    ExperimentNumber = models.CharField(max_length=64)  # 实验编号
    # 数据分析信息
    DataQquality = models.CharField(max_length=16)  # 数据质量
    Effective_sequencing_depth = models.CharField(max_length=16)  # 有效测序深度
    SequencingFileName = models.CharField(max_length=32)  # Sequencing file name
    QC_Result = models.CharField(max_length=32)  # QC result
    Path_To_Sorted_Deduped_Bam = models.CharField(max_length=32)  # Path to sorted.deduped.bam
    Analyser = models.CharField(max_length=32)  # 分析人
    AnalysisTime = models.CharField(max_length=32)  # 分析时间（系统默认）
    AnalysisRemarks = models.CharField(max_length=512)   # 其它（备注）
    # 分析结果审核信息
    Examine_Result = models.CharField(max_length=16)  # 审核结果
    Examine_Time = models.CharField(max_length=32)  # 审核时间
    Examine_Remarks = models.CharField(max_length=512)  # 审核备注
    ReportMakeTask_Man = models.CharField(max_length=32)  # 报告制作任务接收人
    BioinfoResult_Sign = models.CharField(max_length=16)  # 生信分析结果审核标记
    # 其他信息
    DNA_extraction_num = models.CharField(max_length=16)  # DNA提取实验次数
    Build_Prelib_num = models.CharField(max_length=16)  # 预文库构建实验次数
    Build_finlib_num = models.CharField(max_length=16)  # 终文库构建实验次数
    Computer_Seq_num = models.CharField(max_length=16)  # 上机测序实验次数
    DataAnalysis_num = models.CharField(max_length=16)  # 数据分析次数
    SampleSource = models.CharField(max_length=16)  # 样本来源
    # 报告制作信息
    Report_Make_Sign = models.CharField(max_length=16)  # 报告制作标记
    Report_Maker = models.CharField(max_length=32)  # 报告制作人
    Report_Make_Time = models.CharField(max_length=32)  # 报告制作时间
    Report_Remarks = models.CharField(max_length=512)  # 报告备注
    Report_File_Name = models.CharField(max_length=64)  # 报告文件名
    # 遗传咨询师审核报告信息
    GeneticCounselor = models.CharField(max_length=64)  # 遗传咨询师
    Medical_Examine_Result = models.CharField(max_length=16)  # 审核结果
    Medical_Examine_Time = models.CharField(max_length=32)  # 审核时间
    Medical_Examine_Remarks = models.CharField(max_length=512)  # 审核备注
    Medical_Examine_Sign = models.CharField(max_length=16)  # 审核标记
    # 运营审核报告信息
    Operater = models.CharField(max_length=64)  # 运营审核人
    Operate_Examine_Result = models.CharField(max_length=16)  # 审核结果
    Operate_Examine_Time = models.CharField(max_length=32)  # 审核时间
    Operate_Examine_Remarks = models.CharField(max_length=512)  # 审核备注
    Operate_Examine_Sign = models.CharField(max_length=16)  # 审核标记
    # 报告发送信息
    Report_Send_Man = models.CharField(max_length=64)  # 报告发送人
    Report_Send_Address = models.CharField(max_length=16)  # 报告发送地
    Report_Send_Date = models.CharField(max_length=32)  # 报告发送日期
    Invoice_Issuing_Date = models.CharField(max_length=32)  # 发票开具日期
    Report_Send_Remarks = models.CharField(max_length=512)  # 报告发送备注
    Report_Send_Sign = models.CharField(max_length=16)  # 报告发送标记