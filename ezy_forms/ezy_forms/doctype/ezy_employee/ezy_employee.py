# Copyright (c) 2024, bharath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document

class EzyEmployee(Document):
	def after_insert(self):
		if self.designation:
			if not frappe.db.exists("Role",{"role_name":self.designation}):
				adding_role_doc = frappe.new_doc("Role")
				adding_role_doc.role_name = self.designation
				adding_role_doc.insert(ignore_permissions=True)
				frappe.db.commit()
			if not frappe.db.exists("WF Roles",{"role":self.designation}):
				adding_role_doc = frappe.new_doc("WF Roles")
				adding_role_doc.role_name = self.designation
				adding_role_doc.insert(ignore_permissions=True)
				frappe.db.commit()
		if self.reporting_designation:
			if not frappe.db.exists("Role",{"role_name":self.reporting_designation}):
				adding_role_doc = frappe.new_doc("Role")
				adding_role_doc.role_name = self.reporting_designation
				adding_role_doc.insert(ignore_permissions=True)
				frappe.db.commit()
			if not frappe.db.exists("WF Roles",{"role":self.reporting_designation}):
				adding_role_doc = frappe.new_doc("WF Roles")
				adding_role_doc.role_name = self.reporting_designation
				adding_role_doc.insert(ignore_permissions=True)
				frappe.db.commit()