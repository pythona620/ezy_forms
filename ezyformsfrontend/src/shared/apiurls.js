export const domain =
  import.meta.env.VITE_API_BASE_URL === "production" ? "" : "/api";

//=  "/api";   process.env.NODE_ENV === 'production' ? '/' : '/api'

export const fileDomain = "";

export const doctypes = {
  // poschecks: "User",
  users: "User",
  departments: "Ezy Departments",
  wfSettingEzyForms: "Ezy Business Unit",
  EzyFormDefinitions: "Ezy Form Definitions",
  EzyCategories: "Ezy Category",
  designations: "WF Roles",
  EzyEmployeeList: "Ezy Employee",
  SignUpEmployee: "Signup Employee",
  roles: 'Role',
  WFRoleMatrix: "WF Role Matrix",
  WFWorkflowRequests: 'WF Workflow Requests',
  WFActivityLog: 'WF Activity Log',
  CheckUser: 'Login Check',
  SystemSettings:"System Settings",
  Email_Account: 'Email Account',
  doctypesList: 'DocType',
  reportsApi: 'Report',
  preDefinedForm: 'Predefined Doctype',
  ActivityLog:'Activity Log',
  version:'Version',
  websiteSettings:'Website Settings',
  acknowledgement:'Acknowledgement',
  emailTemplate:'Email Template',
  emailQueue:'Email Queue',


  ezyItems: "Ezy Items",
  ezyVendors :'Ezy Vendor Details',
  // ezyContracts: 'Contract',
  ezyContracts: 'CTO',
  EzyInsights:"Ezy Insights",
  wfRoadmap: 'WF Roadmap',
  ExpenseCodes: 'Expense Code',
  CostCenter: 'Cost Center',

  EzyActivityLog:"Ezy Dynamic Activate Log"
  

};

export const apis = {
  resource: domain + `/resource/`,
  uploadfile: domain + `/method/upload_file`,
  login: domain + `/method/login`,
  logout: domain + `/method/logout`,
  


  savedata:
    domain +
    `/method/ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions.add_dynamic_doctype`,

  childtable:domain +
    `/method/ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions.add_child_doctype`,

  update_child_doctype:domain +
  `/method/ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions.add_child_doctype`,

    
  savedocs: domain + '/method/frappe.desk.form.save.savedocs',
  delete_form_items: domain + '/method/ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions.deleting_customized_field_from_custom_dynamic_doc',
  checkRecord: domain + '/method/frappe.client.get_list',
  add_roles_WF: domain + '/method/ezy_forms.ezy_forms.doctype.ezy_form_definitions.linking_flow_and_forms.add_roles_to_wf_requestors',
  raiseFormdata: domain + '/method/ezy_forms.ezy_forms.doctype.ezy_employee.ezy_employee.role_based_accessible_requests',
  raising_request: domain + `/method/ezy_forms.api.v1.ezy_form_rasie_request.raising_requests_to_enqueue`,
  requestApproval: domain + `/method/ezy_forms.api.v1.ezy_form_update_worflow.updating_wf_workflow_requests`,
  wf_cancelling_request: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.wf_cancelling_request`,
  preview_dynamic_form: domain + `/method/ezy_forms.ezy_forms.doctype.ezy_form_definitions.dynamic_form_template.preview_dynamic_form`,
  download_pdf_form: domain + `/method/ezy_forms.ezy_forms.doctype.ezy_form_definitions.dynamic_form_template.download_filled_form`,
  loginCheckmethod: domain + `/method/ezy_forms.ezy_forms.doctype.login_check.login_check.check_is_first_time_or_not`,
  loginUpdatePassword: domain + `/method/ezy_forms.ezy_forms.doctype.login_check.login_check.update_password`,
  loginCheckuseermethod: domain + `/method/ezy_forms.ezy_forms.doctype.login_check.login_check.update_is_first_value`,
  dashboard: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.dashboard_counts`,
  Update_raising_request: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.rejected_form_updating`,
  edit_form_before_approve: domain + `/method/ezy_forms.api.v1.ezy_form_update.edit_the_form_before_approve`,
  uploadbulkEmployeefile: domain + `/method/ezy_forms.api.v1.bulk_import_data.import_bulk_data`,
  childFieldsUpdation: domain + `/method/ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions.update_field_properties`,
 view_only_reportee : domain + `/method/ezy_forms.api.v1.assign_to_me.pick_view_only_reportee`,
 toMailApproval: domain + `/method/ezy_forms.ezy_forms.doctype.email_approval.custom_email_approval.email_approval`,
 deleteAssigneRoles:domain+`/method/ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions.delete_roles_for_approver_roles`,
 
  ExportReport: domain + `/method/ezy_forms.api.v1.export_report.export_report_data`,
  approvedByMe:domain+`/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.approval_by_me`,
  ActivitySaveComment: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.save_button_commite_update`,
  activityLogWithChild: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.get_doc_changes`,
  gettingDataTo: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.form_redict_gate_pass`,
  dynmic_calculations: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.dynamic_calutae`,
  getReportData:  `/printview`,
  signUp:domain+`/method/ezy_forms.api.v1.sign_up.sign_up`,
  GetsignUp:domain+`/method/ezy_forms.api.v1.sign_up.get_signup_value`,
  deleteEmployee:domain+`/method/ezy_forms.ezy_forms.doctype.ezy_employee.ezy_employee.employee_rejection`,
  unablUpdateEmail:domain+`/method/ezy_forms.api.v1.sign_up.employee_update_notification`,
  DepartmentNames: domain + `/method/ezy_forms.ezy_forms.doctype.ezy_departments.ezy_departments.side_nav_department_and_forms`,
  linked_doc_list: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.linked_form_list`,
  linked_form_id_update: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.linked_form_id_update`,
  forgotPassword:domain +`/method/frappe.core.doctype.user.user.reset_password`,
  resetPassword:domain + `/method/ezy_forms.api.v1.reset_password.reset_password`,
  reportMailSend:domain+`/method/ezy_forms.api.v1.send_doctype_as_mail.email_reports_send`,
  employeedisable:domain+`/method/ezy_forms.api.v1.enable_employee.employee_update`,
  get_approved_by_me: domain + `/method/ezy_forms.api.v1.approved_by_me.get_approved_by_me`,
  get_wf_activate_log: domain + `/method/ezy_flow.ezy_flow.doctype.wf_activity_log.wf_activity_log.get_wf_activate_log`,
  download_workorder: domain + `/method/forms_templates.api.v1.vendor_comparision.vendor_comparision_api`,
  generate_qr_code:domain + `/method/ezy_forms.api.v1.generate_qr.generate_qr_for_new_doc`,
  getQrCodeData:domain+`/method/ezy_forms.api.v1.ezy_web_forms.qr_code_to_new_form`,
  addDesignationroles: domain + `/method/ezy_forms.api.v1.get_roles.get_role_list`,
  GetEmployeeForms:domain + `/method/ezy_forms.api.v1.get_employee_form.get_employee_forms`,
  GetAccessibleDeptForms:domain + `/method/ezy_forms.api.v1.get_employee_accessible_forms.get_employee_accessible_forms`,
  GetDoctypeData:domain + `/method/ezy_forms.api.v1.get_doc_list.get_doctype_list`,
  DataUpdate:domain + `/method/ezy_forms.api.v1.doc_operations.doc_operation`,
  // repostListData: domain + `/method/frappe.desk.query_report.run`,
  repostListData: domain + `/method/ezy_forms.api.v1.generate_report.generate_custom_report`,
  getReportList: domain + `/method/ezy_forms.api.v1.get_report_list.get_reports_list`
};

// export const tokens = {
//   Apikey: "1812146a6f090f1",
//   secretkey: "7a5e80cad93659f",

// }
