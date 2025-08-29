import frappe
from frappe.utils import get_url
from frappe import _
from ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions import ezy_doctype_permission
from ezy_forms.ezy_forms.doctype.ezy_dynamic_activate_log.ezy_dynamic_activate_log import create_default_activation_log

def email_template_create():
    
	def create_template(name, subject, message):
		if not frappe.db.exists("Email Template", name):
			template = frappe.new_doc("Email Template")
			template.update({
				"name": name,
				"subject": subject,
				"use_html": 1,
				"response_html": message
			})
			template.insert(ignore_permissions=True)
			frappe.db.commit()

	# Template 1: Account Activation
	activation_message = '''
		Hi {{emp_name}},<br>
		Your user account in ezyForms has been successfully activated by the IT team.<br>
		You can now log in and start using the system. If you haven’t received your login details or need help accessing your account, please contact IT support.<br> 
		Login Link: <a href="{{site_url}}">View Page</a><br>
		Let us know if you have any questions.
	'''
	create_template(
		name="Account Activation",
		subject="Your ezyForms Profile is Now Active",
		message=activation_message
	)

	# Template 2: Employee Sign-Up Notification
	signup_message = '''
		Dear IT Team,<br><br>
		An employee has submitted a sign-up request for the site. Please find the details below:<br><br>
		<ul>
			<li><strong>Email ID:</strong> {{emp_mail_id}}</li>
			<li><strong>Employee Name:</strong> {{emp_name}}</li>
			<li><strong>Employee Designation:</strong> {{designation}}</li>
			<li><strong>Employee Department:</strong> {{department}}</li>
		</ul>
		<br>
		Kindly initiate the necessary steps to enable their access.<br><br>
		Thank you for your support.<br>
		Best regards,<br>
		IT Team
	'''
	create_template(
		name="Employee sign-up",
		subject="Employee sign-up Attempt – Access Enablement Required",
		message=signup_message
	)
 
	ezy_flow_notification = '''
 <p>Dear Sir/Madam,</p>

<p>A new request has been generated in the system with the following details:</p>

<table border="1" cellpadding="10" cellspacing="0">
	<tr>
		<th>Form</th>
		<th>Form Details</th>
	</tr>
	<tr>
		<td><strong>Form Name</strong></td>
		<td>doctypename</td>
	</tr>
	<tr>
		<td><strong>Requested Form ID</strong></td>
		<td>generated_request_id</td>
	</tr>
	<tr>
		<td><strong>Form Requested By</strong></td>
		<td>--action_by--</td>
	</tr>
	<tr>
		<td><strong>Form Requested On</strong></td>
		<td>current_date_and_time</td>
	</tr>
	<tr>
		<td><strong>Form Current Status</strong></td>
		<td>--current_status--</td>
	</tr>
</table>


<p>The reason provided after this action is:</p>
<blockquote style="background-color: #f9f9f9; padding: 10px; border-left: 4px solid #ccc;">
	<em>reason_after_action</em>
</blockquote>

<p>For more details, you can access the request using the following link:</p>


	  <p>
	<a href="---url---" style="
		background-color: #fff;
		color: Blue;
		border:1px solid Blue;
		padding: 10px 20px;
		text-align: center;
		text-decoration: none;
		display: inline-block;
		border-radius: 5px;
		font-weight: bold;">
		Actions
	</a>
</p>

<p>Best Regards,<br>ezyForms</p>
'''
	create_template(
		name="ezyForms Notification",
		subject="ezyForms Notification",
		message=ezy_flow_notification
	)
	approval_remainder = '''
 
<p>Dear Sir/Madam,</p>
 
<p>The following form approval is pending:</p>
 
<table border="1" cellpadding="10" cellspacing="0">
	<tr>
		<th>Form</th>
		<th>Form Details</th>
	</tr>
	<tr>
		<td><strong>Form Name</strong></td>
		<td>{{doctypename}}</td>
	</tr>
	<tr>
		<td><strong>Requested Form ID</strong></td>
		<td>{{generated_request_id}}</td>
	</tr>
	<tr>
		<td><strong>Form Requested By</strong></td>
		<td>{{action_by}}</td>
	</tr>
	<tr>
		<td><strong>Form Requested On</strong></td>
		<td>{{current_date_and_time}}</td>
	</tr>
	<tr>
		<td><strong>Form Current Status</strong></td>
		<td>{{current_status}}</td>
	</tr>
</table>
 
 
<p>Kindly take the necessary action at your earliest convenience.</p>
<p>Best Regards,<br>ezyForms</p>
'''
	create_template(
		name="Approval Remainder",
		subject="ezyForms Approval Remainder",
		message=approval_remainder
	)
 
	frappe.db.commit()
	
	ezy_doctype_permission()
	create_default_activation_log()