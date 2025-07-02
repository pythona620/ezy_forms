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
  raising_request: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.raising_requests`,
  requestApproval: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.updating_wf_workflow_requests`,
  wf_cancelling_request: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.wf_cancelling_request`,
  preview_dynamic_form: domain + `/method/ezy_forms.ezy_forms.doctype.ezy_form_definitions.dynamic_form_template.preview_dynamic_form`,
  download_pdf_form: domain + `/method/ezy_forms.ezy_forms.doctype.ezy_form_definitions.dynamic_form_template.download_filled_form`,
  loginCheckmethod: domain + `/method/ezy_forms.ezy_forms.doctype.login_check.login_check.check_is_first_time_or_not`,
  loginUpdatePassword: domain + `/method/ezy_forms.ezy_forms.doctype.login_check.login_check.update_password`,
  loginCheckuseermethod: domain + `/method/ezy_forms.ezy_forms.doctype.login_check.login_check.update_is_first_value`,
  dashboard: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.dashboard_counts`,
  Update_raising_request: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.rejected_form_updating`,
  edit_form_before_approve: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.edit_the_form_before_approve`,
  uploadbulkEmployeefile: domain + `/method/ezy_forms.ezy_custom_forms.custom_script.v1.bulk_import_data.import_bulk_data`,
  childFieldsUpdation: domain + `/method/ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions.update_field_properties`,
 view_only_reportee : domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.pick_view_only_reportee`,
 toMailApproval: domain + `/method/ezy_forms.ezy_forms.doctype.email_approval.custom_email_approval.email_approval`,
 deleteAssigneRoles:domain+`/method/ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions.delete_roles_for_approver_roles`,
 repostListData: domain + `/method/frappe.desk.query_report.run`,
  ExportReport: domain + `/method/ezy_forms.ezy_custom_forms.custom_script.v1.export_report_api.export_report_data`,
  approvedByMe:domain+`/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.approval_by_me`,
  ActivitySaveComment: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.save_button_commite_update`,
  activityLogWithChild: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.get_doc_changes`,
  gettingDataTo: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.form_redict_gate_pass`,
  dynmic_calculations: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.dynamic_calutae`,
  getReportData:  `/printview`,
  signUp:domain+`/method/ezy_forms.ezy_custom_forms.custom_script.v1.sign_up.sign_up`,
  deleteEmployee:domain+`/method/ezy_forms.ezy_forms.doctype.ezy_employee.ezy_employee.employee_rejection`,
  unablUpdateEmail:domain+`/method/ezy_forms.ezy_forms.doctype.login_check.login_check.employee_update_notification`,
  DepartmentNames: domain + `/method/ezy_forms.ezy_forms.doctype.ezy_departments.ezy_departments.side_nav_department_and_forms`,
  linked_doc_list: domain + `/method/ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.linked_form_list`,
  // getReportData: domain + `/api/method/frappe.utils.print_format.download_pdf`
};

// export const tokens = {
//   Apikey: "1812146a6f090f1",
//   secretkey: "7a5e80cad93659f",

// }
