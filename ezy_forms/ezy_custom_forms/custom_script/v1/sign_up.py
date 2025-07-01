import frappe
from frappe.website.utils import get_home_page, is_signup_disabled
from frappe.utils import escape_html
from frappe import _

@frappe.whitelist(allow_guest=True)
def sign_up(email: str, full_name: str,designation:str|None,emp_phone:str|None,emp_code:str|None,dept:str|None, redirect_to: str|None,acknowledge_on=None,signature=None) -> tuple[int, str]:
	
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
 
		from frappe.utils import random_string
	
		user = frappe.get_doc(
				{
					"doctype": "User",
					"email": email,
					"first_name": escape_html(full_name),
					"enabled": 0,
					'send_welcome_email': 0,
					"new_password": random_string(10),
					"user_type": "Website User",
				}
			)
		user.flags.ignore_permissions = True
		user.flags.ignore_password_policy = True
		user.insert()
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
				'emp_phone':emp_phone,
				"department":dept if dept else None,
				"acknowledge_on": acknowledge_on if acknowledge_on else frappe.utils.now(),
				"emp_code":emp_code
			})
			doc.insert(ignore_permissions=True)
			frappe.db.commit()
			send_mail_when_user_signup(emp_name = full_name,emp_mail_id=email)
		# set default signup role as per Portal Settings
		default_role = frappe.db.get_single_value("Portal Settings", "default_role")
		if default_role:
			user.add_roles(default_role)

		if  user: 
			new_doc = frappe.new_doc("Login Check")
			new_doc.user_id = user
			new_doc.insert(ignore_permissions=True)
			frappe.db.commit()
		if redirect_to:
			frappe.cache.hset("redirect_after_login", user.name, redirect_to)
	return  _("Please contact your IT Manager to verify your sign-up")




@frappe.whitelist()
def send_mail_when_user_signup(emp_name:str|None,emp_mail_id:str|None):
	recipction_mail = frappe.get_value("Notifications Mail","Notifications Mail",'sign_up_approver')
	if recipction_mail:
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
		frappe.sendmail(
			recipients=[recipction_mail],
			subject=subject,
			message=message,
			now = True
		)