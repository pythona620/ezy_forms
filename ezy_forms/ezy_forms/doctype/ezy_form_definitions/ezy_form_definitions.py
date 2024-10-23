# Copyright (c) 2024, bharath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now as frappe_now
import sys
import subprocess
import os
from ast import literal_eval
import pandas as pd
from frappe.utils.background_jobs import enqueue

class EzyFormDefinitions(Document):
	pass

@frappe.whitelist()
def add_dynamic_doctype(owner_of_the_form:str,business_unit:str,form_category:str,form_name:str,accessible_departments:str,form_short_name:str,fields:list[dict]):
	enqueue(
		enqueued_add_dynamic_doctype,
		owner_of_the_form=owner_of_the_form,
		business_unit=business_unit,
		form_category=form_category,
		form_name=form_name,
		accessible_departments=accessible_departments,
		form_short_name=form_short_name,
		fields=fields,
		now=True,
		is_async=True, 
		queue="short")

@frappe.whitelist()
def add_customized_fields_for_dynamic_doc(fields:list[dict],doctype:str):
	enqueue(
		enqueued_add_customized_fields_for_dynamic_doc,
		fields=fields,
		doctype=doctype,
		now=True,
		is_async=True, 
		queue="short")

@frappe.whitelist()
def deleting_customized_field_from_custom_dynamic_doc(doctype,field):
	enqueue(
		enqueued_deleting_customized_field_from_custom_dynamic_doc,
		doctype=doctype,
		field=field,
		now=True,
		is_async=True, 
		queue="short")

@frappe.whitelist()
def enqueued_add_dynamic_doctype(owner_of_the_form:str,business_unit:str,form_category:str,form_name:str,accessible_departments:str,form_short_name:str,fields:list[dict]):
	""" Owner_of_the_form should come from Departments Doctype in Select Field."""
	"""Adding DocTypes dynamically, giving Perms for the doctype and creating a default section-break field for DocType"""
	try:
		if business_unit == None or business_unit == "":return {"success":False,"message":"Pass Business Unit because it is considered as prefix"}
		doctype = business_unit + "-" + form_short_name		
		if isinstance(fields,str):
			fields = literal_eval(fields)
		if frappe.db.exists("Ezy Form Definitions",doctype):return {"success":False,"message":f"Already '{doctype}' exists. Please rename the form."}
		doc = frappe.new_doc("DocType")
		doc.name = doctype
		doc.creation = frappe_now()
		doc.modified = frappe_now()
		doc.modified_by = frappe.session.user
		doc.module = "User Forms"
		doc.app = "ezy_forms"
		doc.custom = 1
		doc.insert(ignore_permissions=True)
		frappe.db.commit()
		doc.reload()
		custom_docperm = frappe.new_doc("Custom DocPerm")
		custom_docperm.parent = doctype
		custom_docperm.read = 1
		custom_docperm.create = 1
		custom_docperm.delete = 1
		custom_docperm.select = 1
		custom_docperm.write = 1
		custom_docperm.role = "System Manager"
		custom_docperm.insert(ignore_permissions=True)
		frappe.db.commit()
		custom_docperm.reload()
		form_defs = frappe.new_doc("Ezy Form Definitions")
		form_defs.form_category = form_category
		form_defs.accessible_departments = accessible_departments
		form_defs.form_name = form_name
		form_defs.form_short_name = form_short_name
		form_defs.owner_of_the_form = owner_of_the_form
		form_defs.active = 1
		form_defs.business_unit = business_unit
		form_defs.count = 0
		form_defs.insert(ignore_permissions=True).save()
		form_defs.reload()
		frappe.db.commit()
		"""need to migrate in this step itself as DocType is created need to update in DB."""
		bench_migrating_from_code()

		"""need to add perms in this step itself for system manager to access the DocType"""
		activating_perms(doctype=doctype)
		document_to_reload = frappe.get_doc("DocType",doctype)
		document_to_reload.reload()

		"""need to migrate in this step itself because of adding permissions in the below level"""
		bench_migrating_from_code()
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		if "list index out of range" in str(e):
			return {"success":False,"message":"Please try again after some time else change the short name to add new form. Reason :- Already this name has been used. Deleting this form in database (works in background)."}
		frappe.log_error("Error in Creating New Doc",
						 "line No:{}\n{}".format(exc_tb.tb_lineno, str(e)))
		frappe.db.rollback()
		frappe.throw(str(e))
		return {"success": False, "message": str(e)}

@frappe.whitelist()
def enqueued_add_customized_fields_for_dynamic_doc(fields:list[dict],doctype:str):
	try:
		if isinstance(fields,str):fields = literal_eval(fields)
		if not len(fields)>0:return {"success":False,"message":"Pass Fields for storing."}
		# if not frappe.db.exists("Ezy Form Definitions",{"name":doctype}):
		# 	return {"success":False,"message":f"pass a valide Form's Short Name - {doctype} which exists."}
		fields_in_mentioned_doctype = [_[0] for _ in frappe.db.sql(f"DESCRIBE `tab{doctype}`;")]
		for dicts_of_docs_entries in fields:
			if dicts_of_docs_entries["fieldname"] in fields_in_mentioned_doctype:
				doc_exists_name_or_not = frappe.db.exists(dicts_of_docs_entries)
				if dicts_of_docs_entries["fieldtype"] not in ["Section Break","Column Break","Tab Break"]: dicts_of_docs_entries = dicts_of_docs_entries | {"in_list_view":1}
				if not doc_exists_name_or_not:
					name_of_existing_doc = frappe.db.get_all("DocField",filters={"fieldname":dicts_of_docs_entries["fieldname"],"parent":dicts_of_docs_entries["parent"]},pluck="name")[0]
					doc_for_existing_custom_field = frappe.get_doc("DocField",name_of_existing_doc)
					if "reqd" in dicts_of_docs_entries:doc_for_existing_custom_field.reqd = dicts_of_docs_entries["reqd"]
					if "options" in dicts_of_docs_entries:
						if isinstance(dicts_of_docs_entries["options"],str):
							dicts_of_docs_entries["options"] = literal_eval(dicts_of_docs_entries["options"])
						doc_for_existing_custom_field.options = "\n".join(dicts_of_docs_entries["options"])
					if "default" in dicts_of_docs_entries:
						doc_for_existing_custom_field.default = dicts_of_docs_entries["default"]
					if "description" in dicts_of_docs_entries:
						doc_for_existing_custom_field.description = dicts_of_docs_entries["description"]
					doc_for_existing_custom_field.idx = dicts_of_docs_entries["idx"]
					doc_for_existing_custom_field.label = dicts_of_docs_entries["label"]
					doc_for_existing_custom_field.fieldtype = dicts_of_docs_entries["fieldtype"]
					doc_for_existing_custom_field.save(ignore_permissions=True)
					frappe.db.commit()
					doc_for_existing_custom_field.db_update()
					doc_for_existing_custom_field.reload()
			else:
				# Create a new field
				if dicts_of_docs_entries["fieldtype"] not in ["Section Break","Column Break","Tab Break"]: dicts_of_docs_entries = dicts_of_docs_entries | {"in_list_view":1}
				doc_for_new_custom_field = frappe.get_doc(dicts_of_docs_entries).insert(ignore_permissions=True)
				doc_for_new_custom_field.save()
				frappe.db.commit()
				doc_for_new_custom_field.db_update()
				doc_for_new_custom_field.reload()
		bench_migrating_from_code()
		keys = ["idx","label","fieldname","fieldtype","reqd","options","default","description"]
		field_attributes = frappe.db.get_all("DocField",{"parent":doctype},keys)
		custom_fields_df = pd.DataFrame.from_records(field_attributes)
		field_attributes = custom_fields_df.sort_values(by=['idx']).to_dict("records")
		frappe.db.set_value("Ezy Form Definitions",doctype,{"form_json":str(field_attributes).replace("'",'"').replace("None","null")})
		frappe.db.commit()
		return field_attributes
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		frappe.log_error("Error in add_customized_fields_for_dynamic_doc",
						 "line No:{}\n{}".format(exc_tb.tb_lineno, str(e)))
		frappe.db.rollback()
		frappe.throw(str(e))
		return {"success": False, "message": str(e)}

@frappe.whitelist()
def enqueued_deleting_customized_field_from_custom_dynamic_doc(doctype,field):
	try:
		if not frappe.db.exists("DocType",doctype): return {"success":False,"message":f"The Form mentioned doesnot exists - '{doctype}'"}
		frappe.db.delete("DocField",{"parent":doctype,"fieldname":field})
		frappe.db.commit()
		bench_migrating_from_code()
		keys = ["idx","label","fieldname","fieldtype","reqd","options","default","description"]
		field_attributes = frappe.db.get_all("DocField",{"parent":doctype},keys)
		custom_fields_df = pd.DataFrame.from_records(field_attributes)
		field_attributes = custom_fields_df.sort_values(by=['idx']).to_dict("records")
		frappe.db.set_value("Ezy Form Definitions",doctype,{"form_json":str(field_attributes).replace("'",'"').replace("None","null")})
		frappe.db.commit()
		reloading = frappe.get_doc("DocType",doctype)
		reloading.reload()
		return field_attributes
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		frappe.log_error("Error in Deleting Field",
						 "line No:{}\n{}".format(exc_tb.tb_lineno, str(e)))
		frappe.db.rollback()
		frappe.throw(str(e))
		return {"success": False, "message": str(e)}

def bench_migrating_from_code():
	os.chdir(frappe.utils.get_bench_path()+"/sites")
	subprocess.run(["bench","migrate"])

def activating_perms(doctype):
	perm_doc = frappe.new_doc("DocPerm")
	perm_doc.parent = doctype
	perm_doc.parentfield="permissions"
	perm_doc.parenttype="DocType"
	perm_doc.role="System Manager"
	perm_doc.insert(ignore_permissions=True)
	frappe.db.commit()
