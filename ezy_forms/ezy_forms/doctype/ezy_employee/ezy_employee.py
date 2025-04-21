# Copyright (c) 2024, bharath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import sys
from ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions import activating_perms, bench_migrating_from_code

class EzyEmployee(Document):
	def after_insert(self):
		is_email_account_set = frappe.db.get_all("Email Account",{"enable_outgoing":["=",1],"default_outgoing":["=",1]})
		###### Employee updating in User doc
		user_doc = frappe.new_doc("User")
		user_doc.email = self.emp_mail_id
		user_doc.username = self.emp_name
		user_doc.send_welcome_email = 0
		user_doc.first_name = self.emp_name.split(" ")[0]
		user_doc.send_welcome_email = 1 if len(is_email_account_set) > 0 else 0
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
			for doc_name in ["Ezy Employee","WF Workflow Requests","WF Roadmap","Ezy Business Unit","WF Roles","Ezy Form Definitions","Ezy Departments"]:
				if not frappe.db.exists("DocPerm",{"parent":doc_name,"parenttype":"DocType","role":self.designation,"parentfield":"permissions"}):
					activating_perms(doc_name,self.designation)
			bench_migrating_from_code()
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
