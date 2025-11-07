import frappe
import os
import ast
from urllib.parse import urlparse
from ezy_forms.ezy_forms.doctype.ezy_form_definitions.dynamic_form_template import download_filled_form
from ezy_forms.api.v1.mail_message_html import preview_dynamic_form
from frappe.utils import add_to_date,get_url

def sending_mail_api(request_id, doctype_name, property, cluster, reason, timestamp,Qr_form_mali_id=None,skip_user_role=None,user=None,field_changes=None,current_level=None,current_status=None):
	frappe.enqueue('ezy_forms.api.v1.send_an_email.send_notifications',
		queue='default',
		timeout=300,
		request_id=request_id,
		doctype_name=doctype_name,
		property=property,
		cluster=cluster,
		reason=reason,
		current_level=current_level,
		field_changes=field_changes,
		timestamp= timestamp,
		current_status =current_status,
		skip_user_role = skip_user_role,
		Qr_form_mali_id=Qr_form_mali_id,
		user=user
	)
def send_notifications(request_id, doctype_name, property, cluster, reason, timestamp,Qr_form_mali_id,skip_user_role=None,user=None,field_changes=None,current_level=None,current_status=None):
	"""Send email notifications to relevant users"""
	email_accounts = frappe.get_all(
		"Email Account",
		filters={"enable_outgoing": 1, "default_outgoing": 1}
	)
	user_list = []
	if field_changes:
		user_list= frappe.get_doc("WF Activity Log",request_id)
		user_list = [role.user for role in user_list.reason if int(role.level) != 0 and int(role.level) !=int(current_level)]

	if not email_accounts:
		return
	request_id_document = frappe.get_all(doctype_name, filters={"wf_generated_request_id": request_id}, fields=["name"])
	attach_down = []
	file_down = None
	attachment_to_mail = frappe.get_value("Ezy Business Unit",property,"send_form_as_a_attach_through_mail")
	if request_id_document and attachment_to_mail:

		file_down = download_filled_form(form_short_name=doctype_name, name=request_id_document[0].name,business_unit=property,from_raise_request='from_raise_request')
		parsed_url = urlparse(file_down["full_download_url"])
		file_path = frappe.get_site_path("public", parsed_url.path.lstrip("/"))
		if os.path.exists(file_path):
			with open(file_path, "rb") as f:
				attach_down.append({
					"fname": os.path.basename(file_path),
					"fcontent": f.read()
				})
	try:
		assigned_users = frappe.get_value("WF Workflow Requests", request_id, "assigned_to_users") if not skip_user_role else [skip_user_role]
		requested_by = frappe.get_value("WF Workflow Requests", request_id, "requested_by")
		if assigned_users and isinstance(assigned_users, str):
			assigned_users = ast.literal_eval(assigned_users)
   
		else:
			assigned_users = assigned_users
		# Fetch roadmap and current level
		roadmap = frappe.get_doc("WF Roadmap", {"property": property, "document_type": doctype_name}).as_dict()
		if not roadmap:
			return "No Roadmap Founded"	
		current_level = int(frappe.get_value("WF Workflow Requests", request_id, "current_level"))
		# Precompute level setup for current level
		level_setup = [i for i in roadmap.wf_level_setup if int(i.level) == current_level]

		# Identify approver and requester roles
		approver_level = [i.role for i in level_setup if int(i.view_only_reportee) == 1]
		requester_to_level = [i.role for i in level_setup if int(i.requester_as_a_approver) == 1]
		# Get user emails based on property/cluster
		if  requester_to_level:
			user_emails = [requested_by]
		elif approver_level:
			user_emails = [frappe.db.get_value("Ezy Employee", requested_by, "reporting_to")]
   
		else:
			if Qr_form_mali_id:
				user_emails = [email.strip() for email in Qr_form_mali_id.split(",")]
			else:
				user_emails = frappe.get_all("Ezy Employee",filters={"designation": ["in", assigned_users], "company_field": property, "enable": 1},fields=["name"],pluck="name") if not user else [user]
		if requested_by !="Guest":
			user_emails.append(requested_by)
		if user_list:
			user_emails = list(set(user_emails + user_list ))
		else:
			user_emails = list(set(user_emails))
		# Get user details
		user_name = frappe.get_value("User", frappe.get_value("WF Workflow Requests", request_id, "requested_by"), "full_name")
		if current_status in ["Approved","Rejected"]:
			current_status = f"Pending With {', '.join(assigned_users)}"
		elif current_status == "Completed":
			current_status = "Completed"

		else:
			current_status = "Request Raised"
		user_role = frappe.get_value("Ezy Employee",frappe.get_value("WF Workflow Requests", request_id, "requested_by"),"designation")
		file_attachment_limit_for_form=int(frappe.get_value("Ezy Business Unit",property,"file_attachment_limit_for_form"))
		# Send emails
		if email_accounts:
			for email in user_emails:
				if email in user_list and user_list:

					reason =  "Form Has been Updated"
				elif field_changes and user_emails:
					reason = reason + ("<br><b>Form Has been Updated <b> ")
				try:
					email_content = generate_email_content(
						request_id, doctype_name, user_name, user_role, email,requested_by,
						reason, timestamp,current_status,property
					)
					
					frappe.sendmail(
						recipients=[email],
						subject="ezyForms Notification",
						message=email_content['message'] if email_content['email_template'] else("<br><b>Note: </b>Since the file size is more than 30MB, please refer to the attachments in the form.<br>" if  file_down and file_down['file_size'] else '')+ email_content['message'] ,
						content = email_content['email_template'] + (f"<b>Note: </b>Since the file size is more than {file_attachment_limit_for_form}MB, please refer to the attachments in the form." if  file_down and file_down['file_size'] else '') if email_content['email_template'] else '',
						attachments=attach_down
					)
				except Exception as e:
					frappe.log_error(message=f"{str(e)}", title="Email Error")
					
	except Exception as e:
		frappe.log_error(f"Notification sending failed: {str(e)}", "Notification Error")


def generate_email_content(request_id, doctype_name, user_name, user_role, email,requested_by,reason, timestamp,current_status,property):
	email_template = frappe.get_doc('Email Template',"ezyForms Notification")
	if requested_by != email:
		# token = get_ezy_forms_token(request_id,doctype_name,request_id_document,each_one_mail,reason if reason else 'Request Raised',next_level_after_raising_request,property)
		url_for_request_id = get_url(
			f"/ezyformsfrontend#/"
		)
		# url_for_request_id = get_url(
		#     f"/ezyformsfrontend#/emailapprove?&key={token}&readOnly=true"
		# )
	else:
		url_for_request_id = ''
	now = add_to_date(None,as_datetime=True)
	my_time = f"{now.year}/{now.month}/{now.day} {now.hour}:{now.minute}"
	response_data = email_template.response_html
	if response_data:
		rep = response_data.replace("doctypename", doctype_name)
		rep = rep.replace("property",property)
		rep = rep.replace("generated_request_id", request_id)
		rep = rep.replace("--action_by--", f"{user_name if user_name else frappe.session.user}  ({user_role})")
		rep = rep.replace("current_date_and_time", my_time)
		if url_for_request_id and url_for_request_id != '---url---':
			rep = rep.replace("---url---", url_for_request_id)
		else:
			rep = rep.replace(
				'href="---url---"',
				'href="/ezyformsfrontend#" style="pointer-events: none; background-color: #eee; color: #999; border: 1px solid #ccc; cursor: not-allowed;"'
			)
		rep = rep.replace("reason_after_action", reason)
		rep = rep.replace("--current_status--", current_status if current_status else 'Request Raised')
		rep = rep.replace("--next-level--", f"{1}")
		email_template.response_html = rep
		
		if int(frappe.get_value("Ezy Business Unit",property,"send_form_in_email")) == 1:
			email_template_response_html = None
			message =preview_dynamic_form(form_short_name=doctype_name, business_unit=property, name=request_id)
			message =message+f"""<a href="{url_for_request_id}" style=" color: blue; text-decoration: none;padding:5px 10px; border:1px solid blue; border-radius: 4px; ">   Approve Email    </a>"""
		else:
			message = email_template.response_html
			email_template_response_html = email_template.response_html
	return {"email_template":email_template_response_html,"message":message}