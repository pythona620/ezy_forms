# Copyright (c) 2025, bharath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EzyDynamicActivateLog(Document):
	pass



@frappe.whitelist()
def create_default_activation_log():
    # create a default record for Ezy Dynamic Activate Log
    ezy_dynamic_activate_log = frappe.get_doc(
        {
        "doctype": "Ezy Dynamic Activate Log",
        "activate_log": "Ezy Employee, User, Ezy Departments, WF Roles, Roles, Ezy Form Definitions, WF Workflow Requests"
    	}
	)
    ezy_dynamic_activate_log.insert(ignore_permissions=True)

    # Commit only if this is part of after_install or patch
    frappe.db.commit()
