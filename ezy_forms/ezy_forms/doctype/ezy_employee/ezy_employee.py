# Copyright (c) 2024, bharath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EzyEmployee(Document):
	def after_insert(self):
		###### Employee updating in User doc
		user_doc = frappe.new_doc("User")
		user_doc.email = self.emp_mail_id
		user_doc.username = self.emp_name
		user_doc.first_name = self.emp_name.split(" ")[0]
		user_doc.insert(ignore_permissions=True)
		frappe.db.commit()
		user_doc.reload()

		if self.designation:
			if not frappe.db.exists("Role",{"role_name":self.designation}):
				adding_role_doc = frappe.new_doc("Role")
				adding_role_doc.role_name = self.designation
				adding_role_doc.insert(ignore_permissions=True)
				frappe.db.commit()
			if not frappe.db.exists("WF Roles",{"role":self.designation}):
				adding_role_doc = frappe.new_doc("WF Roles")
				adding_role_doc.role = self.designation
				adding_role_doc.insert(ignore_permissions=True)
				frappe.db.commit()
		
		###### Adding role to User after creating role in Role DocType
		user_doc = frappe.get_doc("User",self.emp_mail_id)
		user_doc.append("roles",{"role":self.designation})
		user_doc.save(ignore_permissions=True)
		frappe.db.commit()
		user_doc.reload()

		if self.reporting_designation:
			if not frappe.db.exists("Role",{"role_name":self.reporting_designation}):
				adding_role_doc = frappe.new_doc("Role")
				adding_role_doc.role_name = self.reporting_designation
				adding_role_doc.insert(ignore_permissions=True)
				frappe.db.commit()
			if not frappe.db.exists("WF Roles",{"role":self.reporting_designation}):
				adding_role_doc = frappe.new_doc("WF Roles")
				adding_role_doc.role = self.reporting_designation
				adding_role_doc.insert(ignore_permissions=True)
				frappe.db.commit()
		if self.company_field:
			if not frappe.db.exists("WF Role Matrix",{"name":self.company_field}):
				role_matrix = frappe.new_doc("WF Role Matrix")
				role_matrix.property = self.company_field
				role_matrix.append("users",{"mail":self.emp_mail_id,"role_name":self.designation})
				role_matrix.insert(ignore_permissions=True)
				frappe.db.commit()
			else:
				role_matrix = frappe.get_doc("WF Role Matrix",self.company_field)
				wf_users_data = role_matrix.as_dict().users
				if self.emp_mail_id not in [role["mail"] if "mail" == role else "" for role in wf_users_data]:
					role_matrix.append("users",{"role_name":self.designation,"mail":self.emp_mail_id})
					role_matrix.save(ignore_permissions=True)
					frappe.db.commit()

	def save(self):
		super().save(self.name) # call the base save method