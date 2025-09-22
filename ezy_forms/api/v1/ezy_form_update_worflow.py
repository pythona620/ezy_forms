
import frappe
from frappe.utils import add_to_date
import ast
from frappe.utils.background_jobs import enqueue
from frappe.core.page.permission_manager.permission_manager import reset
import string
import operator
import random
from ezy_forms.ezy_forms.doctype.ezy_form_definitions.dynamic_form_template import download_filled_form
from ezy_forms.api.v1.mail_message_html import preview_dynamic_form
from ezy_forms.ezy_forms.doctype.email_approval.email_approval import (
    create_email_approval_records,update_token_status
)
# from frappe import STANDARD_USERS, _, msgprint, throw
from frappe.utils import (
    cint,
    escape_html,
    flt,
    format_datetime,
    get_formatted_email,
    get_system_timezone,
    has_gravatar,
    now_datetime,
    today,
)
import sys, traceback, time
from ezy_forms.api.v1.delete_files import delete_files_api

from ezy_forms.api.v1.ezy_form_rasie_request import *

@frappe.whitelist()
def updating_wf_workflow_requests(request_details,user_session=None,unwanted_files=[]):
	# doctype,request_ids:list, current_level, action, reason, url_for_approval_id, files:None, property = None, cluster_name=None
	
	for per_request_updation in request_details:
		enqueue(
			method = enqueuing_updating_wf_workflow_requests,
			queue="short",
			timeout=1000,
			is_async=False,
			now=False,
			doctype=per_request_updation["doctype"],
			request_ids =per_request_updation["request_ids"],
			current_level= per_request_updation["current_level"],
			action= per_request_updation["action"],
			reason=per_request_updation["reason"],
			url_for_approval_id=per_request_updation["url_for_approval_id"],
			files=per_request_updation["files"],
			property=per_request_updation["property"],
			cluster_name=per_request_updation["cluster_name"],
			user_session=user_session,
			unwanted_files = unwanted_files
			
		)
		if per_request_updation["action"] == "Approve":
			message = "Approved"
		if per_request_updation["action"] == "Reject":
			message = "Rejected"
		   
   
	return {"success":True,"message":message}

@frappe.whitelist()
def enqueuing_updating_wf_workflow_requests(doctype,request_ids:list, current_level, action, reason, url_for_approval_id, files:list|None, property = None, cluster_name=None,user_session=None,unwanted_files =[]):
    try:
        message = ""
        email_template_for_requested_status_response_html = None
        
        now = add_to_date(None,as_datetime=True)
        my_time = f"{now.year}/{now.month}/{now.day} {now.hour}:{now.minute}:{now.second}:{now.microsecond}"        

        # Setting the Role while creation of Request itself
        user_id = (
            frappe.session.user if frappe.session.user != "Guest" else user_session
        )

        role = frappe.get_all("Has Role",fields = ['role'], filters = {"parent":user_id},pluck = "role")
        role = list(filter(lambda x: x!= "System Manager", role))
        employee_role = frappe.db.get_value("Ezy Employee",frappe.session.user,"designation")
        role = role[0] if not employee_role else employee_role
       
        if property != None:
            roadmap_title = "_".join(property.split()).upper() +"_" + "_".join(doctype.split()).upper().replace(" ", "_")
        elif cluster_name != None:
            roadmap_title = "_".join(cluster_name.split()).upper() +"_" + "_".join(doctype.split()).upper().replace(" ", "_")
       
        # Checking whether Role is having right to update the request
        current_level_updating_if_mandatory = frappe.get_all("WF Level Setup",fields=["*"],filters = {"parent":roadmap_title,"level":current_level,"role":role})
       
        if len(current_level_updating_if_mandatory) <=0 :
            return {"success":False,"message":f"{role} is not having right to update the request in this level : {current_level}"}
               
        for request_id in request_ids :
            setting_id = frappe.get_doc("WF Workflow Requests",request_id)
            setting_id.action = action
            setting_id.current_level = current_level
            setting_id.user_session_id = user_id
            setting_id.status = "In Progress"
            setting_id.save()
            frappe.db.commit()
            setting_id.reload()
            
            requested_by = setting_id.requested_by
            requested_by_role = setting_id.role

            ########################################
            # Adding Reason by which roles are given
            ########################################
            previous_reasons = []
            # deleting record if exists
            if frappe.db.exists({"doctype": "WF Activity Log", "name": request_id}):
                first_getting_all_previous_reasons = frappe.get_all("WF Comments",fields=["level","role","user","action","reason","time","random_string"],filters={"parent":request_id})
                for reasons_ in first_getting_all_previous_reasons:
                    previous_reasons.append(reasons_)
                frappe.db.delete("WF Activity Log", {"name": request_id})
                frappe.db.commit()
                frappe.db.delete("WF Comments",{"parent":request_id})
                frappe.db.commit()

            already_used_random_string = True

            while already_used_random_string:
                random_reference_id = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=10))
                random_reference_id = ''.join(random.sample(random_reference_id,len(random_reference_id)))
                if random_reference_id not in frappe.db.get_all("WF Supporting Documents",fields=["reference_id"],pluck="reference_id"):
                    already_used_random_string = False

            if action == "Approve":
                dict_for_child_reason_table = {"level":current_level,'reason': reason,"role":role,"user":user_id,"action":action+"d","time":my_time,"random_string":random_reference_id}
                previous_reasons.append(dict_for_child_reason_table)
            elif action == "Reject":
                dict_for_child_reason_table = {"level":current_level,'reason': reason,"role":role,"user":user_id,"action":action+"ed","time":my_time,"random_string":random_reference_id}
                previous_reasons.append(dict_for_child_reason_table)

            # Sorting as per the Time so that we can append in the correct order
            previous_reasons.sort(key = operator.itemgetter('time'))

            setting_reason = frappe.get_doc({"doctype":"WF Activity Log","request_id":request_id,"reason": previous_reasons})
            setting_reason.insert(ignore_permissions=True)
            setting_reason.save()
            frappe.db.commit()
            setting_reason.reload()
                       
            list_of_ids_of_mentioned_doctype = frappe.get_all("WF IDs", filters = {"parent":request_id}, fields = ["doctype_name_wf"], pluck = "doctype_name_wf")
            if len(list_of_ids_of_mentioned_doctype)<=0:
                return {"success": False, "message":"The request you are fetching does not exist."}
           
            for mentioned_id in list_of_ids_of_mentioned_doctype:
                frappe.db.set_value(doctype, mentioned_id, {"wf_generated_request_status":"In Progress"})
                frappe.db.commit()
                
            if action == "Approve":
                message = "Approved"
                requests_with_combo_roadmap = combination_of_roadmap_and_request(document_type=doctype, request_id = request_id, property=property, cluster_name=cluster_name)
               
                approvals_reasons = requests_with_combo_roadmap["message"]["approvals_reasons"]
                
                if_current_level_not_req_action_check = [d for d in approvals_reasons if d['level'] == current_level and d["mandatory"] == 1 and d["action"] == ""]
                checking_whether_it_matches_levels = frappe.get_all("WF Roadmap", filters = {"roadmap_title":roadmap_title}, fields = ["workflow_levels"], pluck="workflow_levels")
                checking_whether_it_matches_levels = checking_whether_it_matches_levels[0]
               
                if len(if_current_level_not_req_action_check) == 0:
                   
                    # Fix: If only one level, allow completion when current_level == 1 and total levels == 1
                    if int(current_level) < checking_whether_it_matches_levels:
                    # or (
                        # int(current_level) == 1 and int(checking_whether_it_matches_levels) == 1
                    # ):
                        
                        request_id_document = frappe.get_all(doctype, filters={"wf_generated_request_id": request_id}, fields=["name"])
                        # level_1_reasons = [row for row in setting_reason.reason if row.level == current_level]
                        # count_level_1 = len(level_1_reasons)
                        
                        members_having_mails = frappe.get_doc("WF Roadmap",roadmap_title).as_dict()
                        # workflow_levels = members_having_mails['workflow_levels']
                        

                        
                        approvals_reasons_ = requests_with_combo_roadmap["message"]["approvals_reasons"]
                        
                        if_current_level_not_req_action_check_ = []
                        
                        for each in approvals_reasons_:
                            level_match = str(each.get('level')) == str(current_level)
                            action_blank = each.get("action") == ""  # handles "" and None
                            mandatory = each.get("mandatory") == 1
                            all_required = each.get("all_approvals_required") == 1
                            
                            if level_match and all_required and action_blank and mandatory:
                                if_current_level_not_req_action_check_.append(each)
                            
                        change_current_level = None
                        todo_value = None
                        
                        if len(if_current_level_not_req_action_check_) > 0:
                            todo_value = current_level
                            change_current_level = current_level
                        else:
                            todo_value = current_level
                            change_current_level = int(current_level) + 1
                        frappe.db.set_value("WF Workflow Requests", request_id, {"current_level": change_current_level,"status":"In Progress","action":action})
                        frappe.db.commit()
                        todo_tab(document_type = doctype, request_id = request_id,  property=property, cluster_name=cluster_name, current_level= change_current_level,account_ids=request_id_document[0].name,status=None)                            

                        members_having_mails = members_having_mails["wf_level_setup"]
                        
                        roles_in_next_level_level = [rolee ["role"] for rolee in members_having_mails if rolee["level"] == change_current_level and rolee["view_only_reportee"] == 1]
                        roles_in_next_level = [rolee ["role"] for rolee in members_having_mails if rolee["level"] == change_current_level]
                        
                        if len(roles_in_next_level_level) > 0:
                            roles_in_next_level = roles_in_next_level_level
                            
                        next_role_values = ast.literal_eval(frappe.get_value("WF Workflow Requests",request_id,"assigned_to_users"))
                        if property!=None:
                            fetching_all_roles_from_role_matrix = frappe.db.get_all("WF Users",filters = {"role_name":["in", next_role_values],"parent":property}, fields = ["mail"],pluck="mail")
                        elif cluster_name!=None:
                            fetching_all_roles_from_role_matrix = frappe.db.get_all("WF Users",filters = {"role_name":["in", next_role_values],"parent":property}, fields = ["mail"],pluck="mail")

                       
                        # Now adding Requestor for sending mail.
                        is_email_account_set = frappe.db.get_all("Email Account",{"enable_outgoing":["=",1],"default_outgoing":["=",1]})
                        if is_email_account_set:    
                        
                            requestor_user = frappe.db.get_value("WF Comments",{"parent" :request_id, "level":0},["user"])
                            
                            if len(roles_in_next_level_level) > 0:
                                fetching_all_roles_from_role_matrix = []
                                reporting_manager = frappe.db.get_value("Ezy Employee",frappe.get_value("WF Workflow Requests",request_id,"requested_by"),"reporting_to")
                                if reporting_manager not in fetching_all_roles_from_role_matrix and reporting_manager:
                                    fetching_all_roles_from_role_matrix.append(reporting_manager)
                                
                            # Now adding Requestor for sending mail.
                            if requestor_user not in fetching_all_roles_from_role_matrix:
                                fetching_all_roles_from_role_matrix.append(requestor_user)
                                
                            attachment_to_mail = frappe.get_value("Ezy Business Unit",property,"send_form_as_a_attach_through_mail")
                            # sending mail after level changes
                            from urllib.parse import urlparse
                            attach_down = []
                            if attachment_to_mail :
                                file_down = download_filled_form(form_short_name=doctype, name=request_id_document[0].name,business_unit=property,from_raise_request='from_raise_request')
                                parsed_url = urlparse(file_down)
                                attach_down.append({
                                    "file_url":  parsed_url.path
                                })

                            user_name_by_seccion = frappe.get_value("User",requested_by,'full_name')    
                            employee_mails = frappe.db.get_all("Ezy Employee",filters = {'emp_mail_id':['in',fetching_all_roles_from_role_matrix],'enable': 1})
                            fetching_all_roles_from_role_matrix = [emp['name'] for emp in employee_mails]
                        

                            for email in fetching_all_roles_from_role_matrix:
                                email_content = generate_email_content(
                                    request_id, doctype, user_name_by_seccion, requested_by_role, email,requested_by,
                                    reason, my_time
                                )
                                frappe.sendmail(
                                    recipients=[email],
                                    subject="ezyForms Notification",
                                    message=email_content['message'],
                                    content = email_content['email_template'],
                                    attachments=attach_down
                                )
                            update_token_status(action,request_id,request_id_document[0],change_current_level,status='In Progress')

                    elif int(current_level) == checking_whether_it_matches_levels:
                    
                        activate_log_request_id = frappe.get_all("WF Comments",{"parenttype":"WF Activity Log","parentfield": "reason","parent":request_id,"level":current_level})
                        
                        return_message = combination_of_roadmap_and_request(doctype, request_id, property=property, cluster_name=cluster_name)

                        approvals_reasons = return_message["message"]["approvals_reasons"]
                        all_approvals_required = [
                            remaining_role["role"]
                            for remaining_role in approvals_reasons
                            if int(remaining_role["level"]) == int(current_level) and not remaining_role["action"].strip() and not remaining_role["user"].strip() and remaining_role.get("all_approvals_required", 0) == 1
                        ]
                        if all_approvals_required :
                            frappe.db.set_value("WF Workflow Requests", request_id, "status", "In Progress")
                        else:
                            frappe.db.set_value("WF Workflow Requests", request_id, "status", "Completed")
                        frappe.db.commit()
        
                        list_of_ids_of_mentioned_doctype = frappe.get_all("WF IDs", filters = {"parent":request_id}, fields = ["doctype_name_wf"], pluck = "doctype_name_wf")
                       
                        for mentioned_id in list_of_ids_of_mentioned_doctype:
                            frappe.db.set_value(doctype, mentioned_id, {"wf_generated_request_status":"Completed","wf_generated_request_id":request_id})
                            frappe.db.commit()
                        request_id_document = frappe.get_all(doctype, filters={"wf_generated_request_id": request_id}, fields=["name"])
                        todo_tab(document_type = doctype, request_id = request_id,  property=property, cluster_name=cluster_name, current_level=current_level,account_ids=request_id_document[0].name,status=None)
                        
                        is_email_account_set = frappe.db.get_all("Email Account",{"enable_outgoing":["=",1],"default_outgoing":["=",1]})
                        if is_email_account_set:
                            attachment_to_mail = frappe.get_value("Ezy Business Unit",property,"send_form_as_a_attach_through_mail")
                            from urllib.parse import urlparse

                            attach_down = []
                            if attachment_to_mail:
                                file_down = download_filled_form(form_short_name=doctype, name=request_id_document[0].name,business_unit=property,from_raise_request='from_raise_request')
                                parsed_url = urlparse(file_down)
                                attach_down.append({
                                    "file_url":  parsed_url.path
                                })

                            user_name_by_seccion = frappe.get_value("User",requested_by,'full_name')
                            email_content = generate_email_content(
                                request_id, doctype, user_name_by_seccion, requested_by_role, requested_by,requested_by,
                                reason, my_time
                            )
                            frappe.sendmail(
                                recipients=[requested_by],
                                subject="ezyForms Notification",
                                message=email_content['message'],
                                content = email_content['email_template'],
                                attachments=attach_down
                            )
                            
                            update_token_status(action,request_id,request_id_document[0],current_level,status="Completed")


            elif action == "Reject":
                message = "Rejected"
                on_rejection_level = frappe.get_all("WF Level Setup", filters = {"level": current_level,"role": role, "parent":roadmap_title}, fields = 'on_rejection', pluck="on_rejection")
                level_changed = int(current_level)
                current_level = on_rejection_level[0]
                
                is_email_account_set = frappe.db.get_all("Email Account",{"enable_outgoing":["=",1],"default_outgoing":["=",1]})
            

                members_having_mails = frappe.get_doc("WF Roadmap",roadmap_title).as_dict()
                members_having_mails = members_having_mails["wf_level_setup"]

                roles_in_next_level = [rolee ["role"] for rolee in members_having_mails if rolee["level"] == current_level]

                request_id_document = frappe.get_all(doctype, filters={"wf_generated_request_id": request_id}, fields=["name"])
                todo_tab(document_type = doctype, request_id = request_id,  property=property, cluster_name=cluster_name, current_level=current_level,account_ids = request_id_document[0]["name"],status="Reject")
                frappe.db.set_value("WF Workflow Requests", request_id, {"current_level" : int(current_level)if int(current_level) != 0 else 0, "action":action,"status":"In Progress" if int(current_level) != 0 else "Request Cancelled"})
                frappe.db.commit()
               
                attachment_to_mail = frappe.get_value("Ezy Business Unit",property,"send_form_as_a_attach_through_mail")
                
                next_role_values = ast.literal_eval(frappe.get_value("WF Workflow Requests",request_id,"assigned_to_users"))
                if property!=None:
                    fetching_all_roles_from_role_matrix = frappe.db.get_all("WF Users",filters = {"role_name":["in", next_role_values],"parent":property}, fields = ["mail"],pluck="mail")
                elif cluster_name!=None:
                    fetching_all_roles_from_role_matrix = frappe.db.get_all("WF Users",filters = {"role_name":["in", next_role_values],"parent":property}, fields = ["mail"],pluck="mail")
               
                    # sending mail after level changes
                from urllib.parse import urlparse

                attach_down = []
                if request_id_document:
                    docname = request_id_document[0]["name"]
                    doc = frappe.get_doc(doctype, docname)

                    for i in range(int(current_level), int(level_changed) + 1):
                        # Dynamic field names like approver_1, approved_by_1, approved_on_1
                        field_approver = f"approver_{i}"
                        field_approved_by = f"approved_by_{i}"
                        field_approved_on = f"approved_on_{i}"

                        # Clear the dynamic fields
                        for field in [field_approver, field_approved_by, field_approved_on]:
                            if field in doc.as_dict():
                                doc.set(field, None)

                        # # Also update the normal (non-dynamic) fields at current_level
                        if int(current_level) == 0 :
                            doc.approver = None
                            doc.approved_by = None
                            doc.approved_on = None

                    doc.save(ignore_permissions=True)
                    frappe.db.commit()
                    ###################################
                    if attachment_to_mail:
                        file_down = download_filled_form(form_short_name=doctype, name=request_id_document[0].name,business_unit=property,from_raise_request='from_raise_request')
                        parsed_url = urlparse(file_down)
                        attach_down.append({
                            "file_url":  parsed_url.path
                        })


               
                    # Now adding Requestor for sending mail.
                    requestor_user = frappe.db.get_value("WF Comments",{"parent" :request_id, "level":0},["user"])
                    if requestor_user not in fetching_all_roles_from_role_matrix:
                        fetching_all_roles_from_role_matrix.append(requestor_user)

                    user_name_by_seccion = frappe.get_value("User",requested_by,'full_name')
                employee_mails = frappe.get_all("Ezy Employee",filters = {'emp_mail_id':['in',fetching_all_roles_from_role_matrix],'enable': 1},fields=['emp_mail_id'])
                fetching_all_roles_from_role_matrix = [emp['emp_mail_id'] for emp in employee_mails]
                for each_one_mail in fetching_all_roles_from_role_matrix:
                    email_content = generate_email_content(
                        request_id, doctype, user_name_by_seccion, requested_by_role, each_one_mail,requested_by,
                        reason, my_time
                    )
                    frappe.sendmail(
                        recipients=[each_one_mail],
                        subject="ezyForms Notification",
                        message=email_content['message'],
                        content = email_content['email_template'],
                        attachments=attach_down
                            )
                            
            if property !=None:
                frappe.publish_realtime("custom_socket", {'message':'Request Updated', 'type':"Request Updated","total_count":100, "count":100,"request_id":request_id, "property":property,"user":user_id})
            elif cluster_name!=None:
                frappe.publish_realtime("custom_socket", {'message':'Request Updated', 'type':"Request Updated","total_count":100, "count":100,"request_id":request_id, "cluster":cluster_name,"user":user_id})
            if len(unwanted_files)>0:
                enqueue(
                    method=delete_files_api,
                    unwanted_files=unwanted_files
                    )
        return {"success":True,"message":message}
   

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error("Error In Updating WF Workflow Requests", "line No:{}\n{}".format(
            exc_tb.tb_lineno, traceback.format_exc()))
        return {"success": False, "error": str(e)}
