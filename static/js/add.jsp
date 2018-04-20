<%@ page language="java"
	import="java.util.*,cn.eio.MisSys.SysBasic.SysBasic"
	pageEncoding="UTF-8"%>
<%@ page import="cn.eio.MisSys.SysInfo.*"%>
<%
	String path = request.getContextPath();
	String basePath = request.getScheme() + "://"
			+ request.getServerName() + ":" + request.getServerPort()
			+ path + "/";
	SysBasic sb = new SysBasic();
	SysInfo info = new SysInfo(request);
%>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
	<head>
		<base href="<%=basePath%>" />
		<!--框架必须start-->
		<script>
		var paths = "<%=path%>";
	</script>
		<!-- jquery核心 -->
		<script src="<%=path%>/action/js/jquery-1.3.2.min.js"
			type="text/javascript"></script>

		<!-- flexigrid组件核心 -->
		<script src="<%=path%>/action/js/jquery.flexigrid.js"
			type="text/javascript"></script>
		<link href="<%=path%>/action/css/flexigrid.css" type="text/css"
			rel="stylesheet" />

		<!-- qui组件核心 -->
		<script type="text/javascript" src="<%=path%>/bin/js/framework.js"></script>
		<script type="text/javascript" src="<%=path%>/bin/js/form/loadmask.js"></script>
		<link href="<%=path%>/bin/css/import_basic.css" rel="stylesheet"
			type="text/css" />
		<link rel="stylesheet" type="text/css" id="skin"
			prePath="<%=request.getContextPath()%>/bin/" />
		<!--框架必须end  -->

		<!--多选下拉框start-->
		<script type="text/javascript"
			src="<%=path%>/bin/js/form/multiselect.js"></script>
		<!--多选下拉框end-->
		<!--表单验证start-->
		<script src="<%=path%>/bin/js/form/validationEngine-cn.js"
			type="text/javascript"></script>
		<script src="<%=path%>/bin/js/form/validationEngine.js"
			type="text/javascript"></script>
		<!--表单验证end-->


		<!--表单回填start-->
		<script src="<%=path%>/action/js/klims/setFormOfJson.js"
			type="text/javascript"></script>
		<!--表单回填end-->
		<!-- 选择输入 -->
		<script type="text/javascript"
			src="<%=path%>/workflow/subs/klims/function/CheckSite.js"></script>
		<!--自动完成输入start-->
		<script type="text/javascript" src="<%=path%>/bin/js/form/hintbox.js"></script>
		<!--自动完成输入end-->


		<script type="text/javascript"
			src="<%=path%>/workflow/subs/klims/fp_info/js/add.js"></script>

		<script>
		function loadCheck(){
			getRecordInfo();
		}
		
		var i=0;
		function xz(x){
				i=x;				
		}
		
		function setRYXZ(str){
			if(str==""||str=="-1"){
				return;
			}else{
				var a=str.split("§");
				var formid = document.getElementById("add_updata_form");
				if(i==0){
					$(formid).find("#FP_USER").val(a[2]);
				}else if(i==1){
					$(formid).find("#FP_ATTN_NAME").val(a[2]);
				}
			}
		}
		function setHTXZ(str){
			if(str==""||str=="-1"){
				return;
			}else{
				var a=str.split("§");
				var formid = document.getElementById("add_updata_form");
				$(formid).find("#CONTRACT_INFO_ID").val(a[0]);
				$(formid).find("#CONTRACT_NAME").val(a[2]);
				$(formid).find("#CONTRACT_NUMBER").val(a[1]);
			}
		}
		
	function onmoney(){
	
				var tempid;
				tempid=$("#FP_SUM").val();
			
				if(tempid==null||tempid=="null"||tempid=="") {
					return;
				}
				$.ajax({
					type: "POST",
					url: "sqlservlet.C?cmd=fp_info_object&docmd=money",
					data: "FP_SUM="+tempid,
					dataType:"txt",
					success: function(data){
					
						$("#FP_SUM_STRING").val(data);
						
					},
					error: function(data){
						alert("提示:操作失败!");
					}
				});
				
		}
	</script>
	</head>

	<body id="add_ear" onLoad="loadCheck()">

		<table id="_MessageTable_0" width="100%" cellspacing="0"
			cellpadding="0" border="0"
			style="background: #eaece9 url(<%=path%>/bin/js/attention/zDialog/skins/blue/dialog_bg.jpg) no-repeat scroll right top;">
			<tbody>
				<tr>
					<td width="50" height="50" align="center">
						<img id="_MessageIcon_0" width="32" height="32"
							src="<%=path%>/bin/js/attention/zDialog/skins/blue/window.gif" />
					</td>
					<td style="line-height: 16px;">
						<div id="_MessageTitle_0" style="font-weight: bold">
							发票申请单信息登记
						</div>
						<div id="_Message_0">
							填写或编辑修改“发票申请单”相应主要信息!
						</div>
					</td>
				</tr>
				<tr>
					<td colspan="3" align="right" style="line-height: 20px;">
						<button onClick="doAdd_updata('save');return false;" disabled="">
							<span class="icon_item">保存</span>
						</button>
						
						<button onClick="top.Dialog.close();return false;">
							<span class="icon_close">关闭</span>
						</button>
						&nbsp;&nbsp;&nbsp;
					</td>
				</tr>
			</tbody>
		</table>

		<div class="box1 padding_left4" panelWidth="99%" panelHeight="490">

			<form name="add_updata_form" id="add_updata_form" method="post">
				<!-- 信息填写 -->
				<input type="hidden" id="ID" name="ID"
					value="<%=request.getParameter("ID")%>" />
				<fieldset style="background: #efefef">

					<legend>
						填写项
					</legend>

					<table>
						<tr>
							<td>
								申请单编号:
							</td>
							<td>
								<input id="FP_NUMBER" name="FP_NUMBER" type="text"
									style="width: 310px;"
									class="validate[required,custom[illegalLetter]]" />
								<span style="color: red">*</span>
							</td>
							<td>
								发票号:
							</td>
							<td>
								<input id="FP_NO" name="FP_NO" type="text" style="width: 310px;"
									class="validate[required,custom[illegalLetter]]" />
								<span style="color: red">*</span>
							</td>
						</tr>
						<tr>
							<td>
								合同编号
							</td>
							<td>
								<span onclick="setc('合同选择');" class="icon_item hand blue">选择...</span>
								<input id="CONTRACT_NUMBER" name="CONTRACT_NUMBER" type="text"
									style="width: 246px;"/>
								<span style="color: red">*</span>
								<input id="CONTRACT_INFO_ID" name="CONTRACT_INFO_ID"
									type="hidden" />
							</td>
							<td>
								发票性质:
							</td>
							<td>
								<select id="FP_NATURE" name="FP_NATURE" autoWidth="true"
									style="width: 307px;">
									<option value="预开开票">
										预开开票
									</option>
									<option value="到款开票">
										到款开票
									</option>
									<option value="退票申请">
										退票申请
									</option>
								</select>
							</td>
						</tr>
						<tr>
							<td>
								合同名称
							</td>
							<td>
								<input id="CONTRACT_NAME" name="CONTRACT_NAME" type="text"
									style="width: 310px;" readonly="readonly" />
							</td>
							<td>
								开票单位
							</td>
							<td>
								<input id="FP_COMPANY" name="FP_COMPANY" type="text"
									style="width: 310px;"  watermark="北京诺禾致源生物信息科技有限公司" readonly="readonly" />
							</td>
						</tr>
						<tr>
							<td>
								发票抬头
							</td>
							<td>
								<input id="FP_TT" name="FP_TT" type="text" style="width: 310px;"/>
							</td>
						</tr>
						<tr>
							<td>
								项目类型
							</td>
							<td>
								<input id="FP_PROJECT_TYPE" name="FP_PROJECT_TYPE" type="text"
									style="width: 310px;" />
							</td>
							<td>
								发票币种
							</td>
							<td>
								<select id="FP_COST" name="FP_COST" autoWidth="true"
									style="width: 307px;"
									class="validate[required,custom[illegalLetter]]">
									<option value="￥">
										人民币
									</option>
									<option value="HK$">
										港币
									</option>
									<option value="$">
										美元
									</option>
									<option value="€">
										欧元
									</option>
									<option value="£">
										英镑
									</option>
									<option value="¥">
										日元
									</option>
									<option value="฿">
										泰铢
									</option>
								</select>
							</td>
						</tr>
						<tr>
							<td>
								发票金额(小写)：
							</td>
							<td>
								<input id="FP_SUM" name="FP_SUM" type="text" onkeyup="onmoney()"
									class="validate[custom[onlyNumberWide]]" style="width: 310px;" />
							</td>
							<td>
								发票金额(大写)：
							</td>
							<td>
								<input id="FP_SUM_STRING" name="FP_SUM_STRING" type="text"
									style="width: 310px;" readonly="readonly" />
							</td>
						</tr>
						<tr>
							<td>
								开票内容：
							</td>
							<td colspan="3">
							<textarea id="FP_NR" name="FP_NR"
									style="width: 740px; height: 60px;"></textarea>
							</td>
						</tr>
						<tr>
							<td>
								预回款时间：
							</td>
							<td>
								<select id="FP_EXPECTED_DATE" name="FP_EXPECTED_DATE"
									autoWidth="true" style="width: 307px;"
									class="validate[required,custom[illegalLetter]]">
									<option value="1个月内">
										1个月内
									</option>
									<option value="2个月内">
										2个月内
									</option>
									<option value="3个月内">
										3个月内
									</option>
								</select>
							</td>
						</tr>
						<tr>
							<td>
								申请人:
							</td>
							<td>
								<span class="icon_item hand blue" onclick="setc('人员选择'),xz('0')">选择...</span>
								<input id="FP_USER" name="FP_USER" type="text"
									style="width: 246px;" readonly="readonly"
									class="validate[required,custom[illegalLetter]]" />
								<span style="color: red">*</span>
								<input type="hidden" id="G_STID" name="G_STID" />
							</td>
							<td>
								申请日期
							</td>
							<td>
								<input class="date" type="text" id="FP_DATE"
									readonly="readonly" name="FP_DATE" style="width: 310px;" />
							</td>
						</tr>
						<tr>
							<td>
								经办人:
							</td>
							<td>
								<span class="icon_item hand blue" onclick="setc('人员选择'),xz('1')">选择...</span>
								<input id="FP_ATTN_NAME" name="FP_ATTN_NAME" type="text"
									style="width: 246px;"
									class="validate[required,custom[illegalLetter]]" />
								<span style="color: red">*</span>
							</td>
							<td>
								办理时间
							</td>
							<td>
								<input class="date" type="text" id="FP_ATTN_DATE"
									readonly="readonly" name="FP_ATTN_DATE" style="width: 310px;" />
							</td>
						</tr>
						<tr>
							<td>
								备注：
							</td>
							<td colspan="3">
							<textarea id="FP_REMARK" name="FP_REMARK"
									style="width: 740px; height: 60px;"></textarea>
							</td>
						</tr>
					</table>
				</fieldset>
			</form>
		</div>

	</body>
</html>
