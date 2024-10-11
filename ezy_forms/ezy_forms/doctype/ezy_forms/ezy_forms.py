# Copyright (c) 2024, bharath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now as frappe_now
import sys
from frappe.modules.utils import export_customizations
class EzyForms(Document):
	pass

@frappe.whitelist()
def add_dynamic_doctype(doctype):
	try:
		doc = frappe.new_doc("DocType")
		doc.name = doctype
		doc.creation = frappe_now()
		doc.modified = frappe_now()
		doc.modified_by = frappe.session.user
		doc.module = "Ezy Forms"
		doc.app = "ezy_forms"
		doc.custom = 1
		doc.insert(ignore_permissions=True)
		frappe.db.commit()
		doc.reload()
		
		"""need to migrate in this step itself"""
		bench_migrating_from_code()

		"""need to add perms in this step itself"""
		activating_perms(doctype=doctype)
		document_to_reload = frappe.get_doc("DocType",doctype)
		document_to_reload.reload()

		"""need to migrate in this step itself"""
		bench_migrating_from_code()
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		frappe.log_error("Error in Creating New Doc",
						 "line No:{}\n{}".format(exc_tb.tb_lineno, str(e)))
		return {"success": False, "message": str(e)}
@frappe.whitelist()
def bench_migrating_from_code():
	import os
	import subprocess
	bench_path = frappe.utils.get_bench_path()+"/sites"
	os.chdir(bench_path)
	result = subprocess.run(["bench","migrate"])

def activating_perms(doctype):
	perm_doc = frappe.new_doc("DocPerm")
	perm_doc.parent = doctype
	perm_doc.parentfield="permissions"
	perm_doc.parenttype="DocType"
	perm_doc.role="System Manager"
	perm_doc.insert(ignore_permissions=True)
	frappe.db.commit()

@frappe.whitelist()
def customized_fields_for_dynamic_doc(doctype,label_name,field_name,field_type):
	try:
		# Now Checking whether those column are already existing or not
		checking_columns_are_already_existing_or_not_in_doctype_mentioned = frappe.db.sql(f"DESCRIBE `tab{doctype}`;")
		checking_columns_are_already_existing_or_not_in_doctype_mentioned = [i[0] for i in checking_columns_are_already_existing_or_not_in_doctype_mentioned]
				
		if any(x in checking_columns_are_already_existing_or_not_in_doctype_mentioned for x in field_name):
			return "Already field_name exists in doctype"

		for req_id , req_stat in zip(label_name,field_name):
			if not frappe.get_meta(doctype).get_field(req_stat):
				# Create a new field
				doc_for_custom_field = frappe.get_doc({
					"doctype": "Custom Field",
					"dt": doctype,
					"fieldname": req_stat,
					"fieldtype": field_type,
					"label":req_id,
					"module":"Ezy Forms",
					"in_list_view": 1,
				}).insert(ignore_permissions=True)
				frappe.db.commit()
				doc_for_custom_field.save()
				doc_for_custom_field.db_update()
		export_customizations(doctype= doctype,module= "Ezy Forms",sync_on_migrate= 1,with_permissions= 0)
	except frappe.db.OperationalError:
			frappe.log_error(req_stat,f"Already Field: {req_stat} created")