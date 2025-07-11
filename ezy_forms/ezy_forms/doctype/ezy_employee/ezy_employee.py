# Copyright (c) 2024, bharath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import sys
from ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions import activating_perms, bench_migrating_from_code
import socket as so
from ezy_forms.ezy_forms.doctype.login_check.login_check import after_insert_user

class EzyEmployee(Document):
	def on_update(self):
		after_insert_user(self)
	def after_insert(self):
		is_email_account_set = frappe.db.exists("Email Account", {
			"enable_outgoing": 1,
			"default_outgoing": 1
		})

		# Create User if not already created
		if not frappe.db.exists("User", self.emp_mail_id):
			user_doc = frappe.new_doc("User")
			user_doc.username = self.emp_name
			user_doc.email = self.emp_mail_id
			user_doc.first_name = self.emp_name.split(" ")[0]
			user_doc.send_welcome_email = 1 if is_email_account_set else 0
			user_doc.insert(ignore_permissions=True)

			# Create Role and WF Role if designation is provided
			if self.designation:
				if not frappe.db.exists("Role", {"role_name": self.designation}):
					role = frappe.new_doc("Role")
					role.role_name = self.designation
					role.insert(ignore_permissions=True)

				if not frappe.db.exists("WF Roles", {"role": self.designation}):
					wf_role = frappe.new_doc("WF Roles")
					wf_role.role = self.designation
					wf_role.insert(ignore_permissions=True)

				# Migration related function
				bench_migrating_from_code()

				# Assign role to user
				user_doc.append("roles", {"role": self.designation})
				user_doc.save(ignore_permissions=True)

		# Create reporting designation role if not exists
		if self.reporting_designation:
			if not frappe.db.exists("Role", {"role_name": self.reporting_designation}):
				role = frappe.new_doc("Role")
				role.role_name = self.reporting_designation
				role.insert(ignore_permissions=True)

		# Handle WF Role Matrix
		if self.company_field:
			if not frappe.db.exists("WF Role Matrix", {"name": self.company_field}):
				role_matrix = frappe.new_doc("WF Role Matrix")
				role_matrix.name = self.company_field
				role_matrix.property = self.company_field
				role_matrix.append("users", {
					"mail": self.emp_mail_id,
					"role_name": self.designation
				})
				role_matrix.insert(ignore_permissions=True)
			else:
				role_matrix = frappe.get_doc("WF Role Matrix", self.company_field)
				existing_emails = [u.mail for u in role_matrix.users]
				if self.emp_mail_id not in existing_emails:
					role_matrix.append("users", {
						"mail": self.emp_mail_id,
						"role_name": self.designation
					})
					role_matrix.save(ignore_permissions=True)

		frappe.db.commit()

	def save(self):
		super().save(self.name) # call the base save method
		self.wf_role_matrix_update()
  
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
			
	
@frappe.whitelist()
def role_based_accessible_requests(role:str,business_unit:str):
	try:
		list_of_roadmaps = frappe.db.get_all("WF Requestors",{"parent":["like",f"%{business_unit}%"],"requestor":role},pluck="parent")
		list_of_short_names = frappe.db.get_all("WF Roadmap",{"name":["in",list_of_roadmaps]},pluck="document_type")
		return {"success":True,"list_of_roadmaps":list_of_short_names}
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		frappe.log_error("Error in Role based Roadmaps.",
						 "line No:{}\n{}".format(exc_tb.tb_lineno, str(e)))
		frappe.db.rollback()
		frappe.throw(str(e))
		return {"success": False, "message": str(e)}





@frappe.whitelist()
def employee_last_login_activate(login_manager): 
	hostname = so.gethostname()
	ip_address = so.gethostbyname(hostname)
	frappe.db.set_value('Ezy Employee',{"emp_mail_id":frappe.session.user},"last_login",frappe.utils.now())
	frappe.db.set_value('Ezy Employee',{"emp_mail_id":frappe.session.user},"last_ip",ip_address)
	frappe.db.commit()
 
 

 
@frappe.whitelist()
def employee_rejection(empl_mail_id):
	# Delete Ezy Employee if exists
	employee_name,propertys = frappe.db.get_value("Ezy Employee", {"emp_mail_id": empl_mail_id},['name','company_field'])
	if employee_name:
		frappe.delete_doc("Ezy Employee", employee_name, force=1)

	# Delete User if exists
	if frappe.db.exists("User", empl_mail_id):
		frappe.delete_doc("User", empl_mail_id, force=1)

	# Delete Login Check if exists
	login_check_name = frappe.db.get_value("Login Check", {"user_id": empl_mail_id})
	if login_check_name:
		frappe.delete_doc("Login Check", login_check_name, force=1)

	# Remove from WF Users child table in WF Role Matrix
	role_matrix_list = frappe.db.get_value("WF Role Matrix", {"property": propertys}, "name")

	if role_matrix_list:
		doc = frappe.get_doc("WF Role Matrix", role_matrix_list)
		doc.set("users", [user for user in doc.users if user.mail != empl_mail_id])
		doc.save(ignore_permissions=True)

	frappe.db.commit()
	return "Employee Deleted "
