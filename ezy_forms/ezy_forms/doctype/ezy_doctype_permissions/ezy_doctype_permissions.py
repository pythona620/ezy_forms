# Copyright (c) 2025, bharath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EzyDoctypePermissions(Document):
	pass


@frappe.whitelist()
def activating_perms_for_new_role(doc, method):
	child_entries = frappe.get_all(
			"Doctype Permissions",
			filters={"parent": "Ezy Doctype Permissions", "parenttype": "Ezy Doctype Permissions", "parentfield": "document_type"},
			fields=["doctype_names"]
		)
	document_type_list = [entry["doctype_names"] for entry in child_entries]
	custom_feilds = frappe.get_all("DocType",filters={'module':["in",["User Forms","ezy_custom_forms", "ezy_custom_forms","Ezy Flow"]]})
	custom_feilds_list = [doc.name for doc in custom_feilds]
	document_type_list.extend(custom_feilds_list)
	for doc_name in document_type_list:
		if not frappe.db.exists("Custom DocPerm",{"parent":doc_name,"role":doc.name}):
			form_perms = frappe.new_doc("Custom DocPerm")
			form_perms.parent = doc_name
			form_perms.role = doc.name
			form_perms.delete = 1
			form_perms.select = 1
			form_perms.read = 1
			form_perms.write = 1
			form_perms.create = 1
			form_perms.delete = 1
			form_perms.insert(ignore_permissions=True)
	frappe.db.commit()