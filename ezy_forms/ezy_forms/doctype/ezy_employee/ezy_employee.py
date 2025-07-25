# Copyright (c) 2024, bharath and contributors
# For license information, please see license.txt
 
import frappe
from frappe.model.document import Document
import sys
from ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions import activating_perms, bench_migrating_from_code
import socket as so
from ezy_forms.ezy_forms.doctype.login_check.login_check import after_insert_user
import time
class EzyEmployee(Document):
	def on_update(self):
		prev_doc = self.get_doc_before_save()
		if (
			not frappe.db.exists("Login Check", {"user_id": self.emp_mail_id}) 
			and self.enable 
			and prev_doc 
			and getattr(prev_doc, "enable", 0) != 1
		):

			after_insert_user(self)

 
	def after_insert(self):
		self.ensure_reporting_designation_role()
		self.create_user_if_not_exists()
		self.update_wf_role_matrix()
		if self.enable:
			after_insert_user(self)
 
	def create_user_if_not_exists(self):
		if frappe.db.exists("User", self.emp_mail_id):
			return "User already exists"

		# Create Role and WF Role if designation is provided
		if self.designation:
			self.create_role_and_wf_role(self.designation)
			# bench_migrating_from_code()
	
		# Check for outgoing email account
		is_email_account_set = frappe.db.exists("Email Account", {
			"enable_outgoing": 1,
			"default_outgoing": 1
		})
	
		# Create User document
		user_doc = frappe.new_doc("User")
		user_doc.update({
			"username": self.emp_name,
			"email": self.emp_mail_id,
			"first_name": self.emp_name.split(" ")[0],
			"send_welcome_email":  0
		})
		if self.designation:
			user_doc.append("roles", {"role": self.designation})
		time.sleep(2) 
		frappe.flags.in_import=True 
		user_doc.insert(ignore_permissions=True)
 
	   
 
	def create_role_and_wf_role(self, role_name):
		if not frappe.db.exists("Role", {"role_name": role_name}):
			frappe.get_doc({"doctype": "Role", "role_name": role_name}).insert(ignore_permissions=True)
 
		if not frappe.db.exists("WF Roles", {"role": role_name}):
			frappe.get_doc({"doctype": "WF Roles", "role": role_name}).insert(ignore_permissions=True)
 
	def ensure_reporting_designation_role(self):
		if self.reporting_designation and not frappe.db.exists("Role", {"role_name": self.reporting_designation}):
			frappe.get_doc({"doctype": "Role", "role_name": self.reporting_designation}).insert(ignore_permissions=True)
 
	def update_wf_role_matrix(self):
		if not self.company_field:
			return "Provid valid Company"
 
		role_matrix = frappe.get_doc("WF Role Matrix", self.company_field) if frappe.db.exists("WF Role Matrix", self.company_field) else None
 
		if not role_matrix:
			role_matrix = frappe.new_doc("WF Role Matrix")
			role_matrix.update({
				"name": self.company_field,
				"property": self.company_field,
				"users": [{
					"mail": self.emp_mail_id,
					"role_name": self.designation
				}]
			})
			role_matrix.insert(ignore_permissions=True)
		else:
			if self.emp_mail_id not in [u.mail for u in role_matrix.users]:
				role_matrix.append("users", {
					"mail": self.emp_mail_id,
					"role_name": self.designation
				})
				role_matrix.save(ignore_permissions=True)
 
	def save(self):
		super().save(self.name)
		wf_role_matrix_update(self)
 
 
@frappe.whitelist()
def employee_last_login_activate(login_manager):
	import socket as so
	frappe.db.set_value("Ezy Employee", {"emp_mail_id": frappe.session.user}, {
		"last_login": frappe.utils.now(),
		"last_ip": so.gethostbyname(so.gethostname())
	})
 
 
@frappe.whitelist()
def employee_rejection(empl_mail_id):
	employee_name, company_field = frappe.db.get_value("Ezy Employee", {"emp_mail_id": empl_mail_id}, ["name", "company_field"])
	if employee_name:
		frappe.delete_doc("Ezy Employee", employee_name, force=1)
 
	if frappe.db.exists("User", empl_mail_id):
		frappe.delete_doc("User", empl_mail_id, force=1)
 
	login_check_name = frappe.db.get_value("Login Check", {"user_id": empl_mail_id})
	if login_check_name:
		frappe.delete_doc("Login Check", login_check_name, force=1)
 
	if company_field and frappe.db.exists("WF Role Matrix", {"property": company_field}):
		doc = frappe.get_doc("WF Role Matrix", company_field)
		doc.set("users", [u for u in doc.users if u.mail != empl_mail_id])
		doc.save(ignore_permissions=True)
 
	return "Employee Deleted"

# when employee desgnation are updated wf role matrix and user also updated
def wf_role_matrix_update(self):
	previous_role = frappe.db.get_value("WF Users",{"mail":self.emp_mail_id},['role_name'])
	if self.designation != previous_role:
		frappe.db.set_value("WF Users",{"mail":self.emp_mail_id},{"role_name":self.designation})
		user = frappe.get_doc("User",self.emp_mail_id)
		
		user.roles = []
		
		user.append("roles", {"role": self.designation})
		user.save(ignore_permissions=True)
		frappe.db.commit()
		
  
@frappe.whitelist(allow_guest=True)
def set_reporting_to_and_designation(doc, method):
    if not doc.reporting_to and doc.department:
        hod = frappe.get_value("Ezy Employee", {
            "department": doc.department,
            "is_hod": 1
        }, ["name", "designation"], as_dict=True)

        if hod:
            doc.reporting_to = hod.name
            doc.reporting_designation = hod.designation

            doc.flags.ignore_permissions = True
            doc.save()
            frappe.db.commit()
