import frappe
from frappe.website.utils import get_home_page, is_signup_disabled
from frappe.utils import escape_html
from frappe import _

@frappe.whitelist(allow_guest=True)
def sign_up(email: str, full_name: str,designation:str|None,emp_phone:str|None,emp_code:str|None,dept:str|None, redirect_to: str|None,acknowledge_on=None,signature=None,acknowledgement=None) -> tuple[int, str]:
	
	if is_signup_disabled():
		return _("Sign Up is disabled")
 
	user = frappe.db.get("User", {"email": email})
	if user:
		if user.enabled:
			return  _("Already Registered")
		else:
			return  _("Registered but disabled")
	else:
		if frappe.db.get_creation_count("User", 60) > 300:
			frappe.respond_as_web_page(
				_("Temporarily Disabled"),
				_(
					"Too many users signed up recently, so the registration is disabled. Please try back in an hour"
				),
				http_status_code=429,
			)
 
		from frappe.utils import generate_hash
	
		user = frappe.get_doc(
				{
					"doctype": "User",
					"email": email,
					"first_name": escape_html(full_name),
					"enabled": 0,
					'send_welcome_email': 0,
					"new_password": generate_hash(length=10),
					"user_type": "Website User",
					"roles": [
						{
							"role": designation}]
				}
			)
		user.flags.ignore_permissions = True
		user.flags.ignore_password_policy = True
		user.insert(ignore_permissions = True)
		company_field = frappe.get_all("Ezy Business Unit",fields = ['name'])
		company = company_field[0].name
		if not frappe.db.exists("Ezy Employee", {"emp_mail_id": user.email}):
			doc = frappe.new_doc("Ezy Employee")
			doc.update({
				"emp_name": user.username.replace('_'," ") if user.username else user.first_name,
				"emp_mail_id": user.email,
				"company_field":company,
				"enable":0,
				"is_web_form":1,
				"designation":designation,
				"signature":signature,
				"acknowledgement":acknowledgement,
				'emp_phone':emp_phone,
				"department":dept if dept else None,
				"acknowledge_on": acknowledge_on if acknowledge_on else frappe.utils.now(),
				"emp_code":emp_code
			})
			doc.insert(ignore_permissions=True)
			frappe.db.commit()
			send_mail_when_user_signup(emp_name = full_name,emp_mail_id=email)
		# set default signup role as per Portal Set	tings
		default_role = frappe.db.get_single_value("Portal Settings", "default_role")
		if default_role:
			user.add_roles(default_role)
		if redirect_to:
			frappe.cache.hset("redirect_after_login", user.name, redirect_to)
	return  _("Please contact your IT Manager to verify your sign-up")




@frappe.whitelist()
def send_mail_when_user_signup(emp_name:str|None,emp_mail_id:str|None):
	sender = frappe.get_value("Email Account",{"enable_outgoing":1,"default_outgoing":1},"email_id")
	recipction_mail = frappe.get_value("Notifications Mail","Notifications Mail",'sign_up_approver')
	subject = "Employee sign-up Attempt – Access Enablement Required"
	message = f"""
	Dear IT Team,<br><br>
	An employee has submitted a sign-up request for the site. Please find the details below:<br><br>
	<ul>
		<li><strong>Email ID:</strong> {emp_mail_id}</li>
		<li><strong>Employee Name:</strong> {emp_name}</li>
	</ul>
	<br>
	Kindly initiate the necessary steps to enable their access.<br><br>
	Thank you for your support.<br>
	Best regards,<br>
	IT Team
	"""
	if  recipction_mail:
		email_template = frappe.get_doc("Email Template", "Employee sign-up")
		if email_template and email_template.use_html:
			subject = email_template.subject or subject
			message = frappe.render_template(email_template.response_html, {
				"emp_name": emp_name,
				"emp_mail_id": emp_mail_id,
			})
		frappe.sendmail(
			recipients=[recipction_mail],
			subject= subject,
			sender=sender,
			message=message,
			now = True
		)
from frappe.utils import get_url

@frappe.whitelist(allow_guest=True)
def employee_update_notification(emp_mail):
	if not emp_mail:
		frappe.throw("Employee email is required.")

	sender = frappe.get_value("Email Account",{"enable_outgoing":1,"default_outgoing":1},"email_id")
	# Get employee name using the email as the 'name' field in Ezy Employee
	emp_mail, emp_name = frappe.db.get_value(
		"Ezy Employee", {"name": emp_mail}, ["name", "emp_name"]
	)

	if not emp_mail or not emp_name:
		frappe.throw("Employee not found.")

	site_url = get_url()
	
	# Get the mail ID from the 'Notifications Mail' doctype
	mail_id = frappe.get_value("Notifications Mail", "Notifications Mail", "mail_id")

	# Get the email template
	email_template = frappe.get_doc("Email Template", "Account Activation")

	# Default subject and message
	subject = "Your Ezy Forms Profile is Now Active"
	message = f"""
		Hi {emp_name},<br>
		Your user account in Ezy Forms has been successfully activated by the IT team.<br>
		You can now log in and start using the system. If you haven’t received your login details or need help accessing your account, please contact IT support. - <b>Email:<b> {mail_id} <br> 
		Login Link: <a href="{site_url}/ezyformsfrontend#/">View Page</a><br>
		Let us know if you have any questions.
	"""

	# If template is available and using HTML
	if email_template and email_template.use_html:
		subject = email_template.subject or subject
		message = frappe.render_template(email_template.response_html,{
			"site_url": f'{site_url}/ezyformsfrontend#/',
			"emp_name": emp_name,
			"mail_id": mail_id,
		})

	# Send the email
	frappe.sendmail(
		recipients=[emp_mail],
		subject=subject,
		sender=sender,
		message=message,
		now=True
	)

	return "Notification sent successfully"

  
@frappe.whitelist(allow_guest=True)
def get_signup_value():
	return_value = {}
	web_signup_value =  frappe.get_value("Website Settings", "Website Settings", "disable_signup") or 0
	return_value["is_signup"] = web_signup_value
	return return_value



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
		Your user account in Ezy Forms has been successfully activated by the IT team.<br>
		You can now log in and start using the system. If you haven’t received your login details or need help accessing your account, please contact IT support.<br> 
		Login Link: <a href="{{site_url}}">View Page</a><br>
		Let us know if you have any questions.
	'''
	create_template(
		name="Account Activation",
		subject="Your Ezy Forms Profile is Now Active",
		message=activation_message
	)

	# Template 2: Employee Sign-Up Notification
	signup_message = '''
		Dear IT Team,<br><br>
		An employee has submitted a sign-up request for the site. Please find the details below:<br><br>
		<ul>
			<li><strong>Email ID:</strong> {{emp_mail_id}}</li>
			<li><strong>Employee Name:</strong> {{emp_name}}</li>
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
		<td><strong>Form Submitted By</strong></td>
		<td>--action_by--</td>
	</tr>
	<tr>
		<td><strong>Form Submitted On</strong></td>
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

<p>Best Regards,<br>EzyForms</p>
'''
	create_template(
		name="Ezy Flow Notification",
		subject="Ezy Flow Notification",
		message=ezy_flow_notification
	)

	child_entries = frappe.get_all(
			"Doctype Permissions",
			filters={"parent": "Ezy Doctype Permissions", "parenttype": "Ezy Doctype Permissions", "parentfield": "guest_permissions"},
			fields=["doctype_names"]
		)
	document_type_list = [entry["doctype_names"] for entry in child_entries]
	if document_type_list:
		for doc in document_type_list:
			form_perms = frappe.new_doc("Custom DocPerm")
			form_perms.parent = doc
			form_perms.role ="Guest"
			form_perms.read = 1
			form_perms.insert(ignore_permissions=True)
		frappe.db.commit()