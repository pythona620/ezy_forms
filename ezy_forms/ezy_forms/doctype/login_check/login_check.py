# Copyright (c) 2025, bharath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class LoginCheck(Document):
	pass

@frappe.whitelist(allow_guest=True)
def after_insert_user(self, method=None):
    try:
        existing_user = frappe.db.get_value("Login Check",{"user_id": self.email},["user_id"])
        
        if not existing_user:
            new_doc = frappe.new_doc("Login Check")
            new_doc.user = self.email
            new_doc.insert(ignore_permissions=True)
            frappe.db.commit()
 
    except Exception as e:
        frappe.log_error(f"Error in after_insert_user for {self.email}: {str(e)}")