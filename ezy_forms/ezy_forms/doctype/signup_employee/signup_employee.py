# Copyright (c) 2025, bharath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from ezy_forms.api.v1.sign_up import employee_update_notification

class SignupEmployee(Document):
	def on_update(self):
		if self.enable == 1:
			if frappe.db.exists("Ezy Employee", {"emp_mail_id": self.emp_mail_id}):
				frappe.throw(f"Ezy Employee with email {self.emp_mail_id} already exists.")
			create_employee_record(self.emp_mail_id)
			employee_update_notification(self.emp_mail_id)
	def after_insert(doc):
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

@frappe.whitelist()
def create_employee_record(emp_mail_id):
	if not emp_mail_id:
		frappe.throw("Employee email ID is required.")
	
	signup_record = frappe.db.get_value(
		"Signup Employee",
		{"emp_mail_id": emp_mail_id},
		[
			"emp_name", "emp_mail_id", "company_field", "designation",
			"signature", "acknowledgement", "emp_phone", "department",
			"acknowledge_on", "emp_code"
		],
		as_dict=True
	)
	
	doc = frappe.new_doc("Ezy Employee")
	doc.update(signup_record)
	doc.enable = 1
	doc.is_web_form = 0
	# Insert the new record into the database
	doc.insert(ignore_permissions=True)
	# Delete the original signup record
	frappe.db.delete("Signup Employee", {"emp_mail_id": emp_mail_id})
	# Commit the changes
	frappe.db.commit()
	return {"status": "success", "employee": doc.name}
 
@frappe.whitelist(methods=["POST"])
def employee_rejection(empl_mail_id):
	if frappe.db.exists("Signup Employee", empl_mail_id):
		frappe.delete_doc("Signup Employee", empl_mail_id, force=1)
	frappe.db.commit()
	return "Employee Deleted Sucessfully"
