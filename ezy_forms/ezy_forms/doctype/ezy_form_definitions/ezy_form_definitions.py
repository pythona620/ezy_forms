# Copyright (c) 2024, bharath and contributors
# For license information, please see license.txt
 
import frappe
from frappe.model.document import Document
from frappe.utils import now as frappe_now
import sys
import subprocess
import os
from ast import literal_eval
from frappe.utils.background_jobs import enqueue
from ezy_forms.ezy_forms.doctype.ezy_form_definitions.linking_flow_and_forms import enqueing_creation_of_roadmap
from itertools import chain
from frappe.utils import cstr,get_site_path
from frappe.utils import now as frappe_now
import re
import json
import shutil


 
class EzyFormDefinitions(Document):
    pass
 
@frappe.whitelist()
def add_dynamic_doctype(owner_of_the_form:str,business_unit:str,form_category:str,form_name:str,accessible_departments:str,has_workflow:str|None,is_linked_form:str| None, is_linked:int | None, is_predefined_doctype:int |None, form_short_name:str,fields:list[dict],form_status:str,series=None):
    return_response_for_doc_add = enqueue(
        enqueued_add_dynamic_doctype,
        owner_of_the_form=owner_of_the_form,
        business_unit=business_unit,
        form_category=form_category,
        form_name=form_name,
        accessible_departments=accessible_departments,
        form_short_name=form_short_name,
        fields=fields,
        form_status=form_status,
        now=True,
        series =series,
        has_workflow=has_workflow,
        is_linked_form = is_linked_form,
        is_linked=is_linked,
        is_predefined_doctype=is_predefined_doctype,
        is_async=True,
        queue="short")
    return return_response_for_doc_add
 
@frappe.whitelist()
def add_customized_fields_for_dynamic_doc(fields:list[dict],doctype:str):
# def add_customized_fields_for_dynamic_doc(fields:list[dict],doctype:str,accessible_departments:str):
    return_response_for_add_or_edit_fields = enqueue(
        enqueued_add_customized_fields_for_dynamic_doc,
        fields=fields,
        doctype=doctype,
        # accessible_departments=accessible_departments,
        now=True,
        is_async=True,
        queue="short")
    return return_response_for_add_or_edit_fields
 
def deleting_customized_field_from_custom_dynamic_doc(doctype:str,deleted_fields:list):
    deleted_fields_qresponse = enqueue(
        enqueued_deleting_customized_field_from_custom_dynamic_doc,
        doctype=doctype,
        deleted_fields=deleted_fields,
        now=True,
        is_async=True,
        queue="short")
    return deleted_fields_qresponse
 
def enqueued_add_dynamic_doctype(owner_of_the_form:str,business_unit:str,form_category:str,form_name:str,accessible_departments:str,form_short_name:str,fields:list[dict],form_status:str,has_workflow:str,is_linked:int | None,is_predefined_doctype: int|None,is_linked_form:str| None,series=None):
    """ Owner_of_the_form should come from Departments Doctype in Select Field."""
    """Adding DocTypes dynamically, giving Perms for the doctype and creating a default section-break field for DocType"""
    try:
        if business_unit == None or business_unit == "":return {"success":False,"message":"Pass Business Unit because it is considered as prefix"}
        doctype = form_short_name
        if isinstance(fields,str):
            fields = literal_eval(fields)
        if frappe.db.exists("Ezy Form Definitions",{"name":form_short_name}):
            
            frappe.set_value("Ezy Form Definitions",form_short_name,"has_workflow",has_workflow)
            # frappe.set_value("Ezy Form Definitions",form_short_name,"is_linked_form", is_linked_form)
            
            frappe.set_value("Ezy Form Definitions",{"name":form_short_name},{"form_status":form_status,"accessible_departments":accessible_departments,"owner_of_the_form":owner_of_the_form,"is_linked_form":is_linked_form,"is_linked":is_linked,"is_predefined_doctype":is_predefined_doctype})
        if not frappe.db.exists("DocType",doctype):
            frappe.db.sql(f"DROP TABLE IF EXISTS `tab{doctype}`;")
            frappe.db.commit()
            if frappe.db.exists("Ezy Form Definitions",{"name":form_short_name}):return {"success":True,"message":f"Already Created Form with the same name - '{form_short_name}' but haven't removed in 'Ezy Form Definitions'."}
            doc = frappe.new_doc("DocType")
            doc.name = doctype
            doc.creation = frappe_now()
            doc.modified = frappe_now()
            doc.modified_by = frappe.session.user
            doc.module = "User Forms"
            doc.app = "ezy_forms"
            doc.custom = 1
            doc.track_changes = 1
            doc.autoname = "naming_series:"
            doc.naming_rule ='By "Naming Series" field '
            cleaned_series = re.sub(r'[^a-zA-Z0-9#\-/\.]', '', series or '') if series else None
            series = None if not cleaned_series else (
                    cleaned_series.upper() + "-.####" if not re.search(r'[-/]\.#+$', cleaned_series.upper()) else cleaned_series.upper()
                )
            doc.naming_series = series if series else f"{business_unit}_{doctype}"  # optional if you want to set a default value
            doc.append("fields", frappe.get_doc({
            "doctype": "DocField",
            "label": "Naming Series",
            "fieldname": "naming_series",
            "fieldtype": "Select",
            "options": series if series else f"{business_unit}_{doctype.replace(' ', '_').upper() or doctype.upper()}-",
            "reqd": 1,
            "insert_after": "title"
        }))
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            doc.reload()
            """need to add perms in this step itself for system manager to access the DocType"""
            activating_perms(doctype=doctype,role="System Manager")
            """need to migrate in this step itself as DocType is created need to update in DB."""
            bench_migrating_from_code()
            form_defs = frappe.new_doc("Ezy Form Definitions")
            form_defs.form_category = form_category
            form_defs.accessible_departments = accessible_departments
            form_defs.form_name = form_name
            form_defs.form_short_name = form_short_name
            form_defs.form_status = form_status
            form_defs.owner_of_the_form = owner_of_the_form
            form_defs.active = 1
            cleaned_series = re.sub(r'[^a-zA-Z0-9#\-/\.]', '', series or '') if series else None

            # Apply logic
            form_defs.series = None if not cleaned_series else (
            cleaned_series.upper() + "-.####" if not re.search(r'[-/]\.#+$', cleaned_series.upper()) else cleaned_series.upper()
        )
            form_defs.business_unit = business_unit
            form_defs.count = 0
            form_defs.has_workflow = has_workflow or ''
            form_defs.is_linked_form = is_linked_form or ''
            form_defs.is_linked = is_linked
            form_defs.is_predefined_doctype = is_predefined_doctype
            form_defs.insert(ignore_permissions=True).save()
            form_defs.reload()
            frappe.db.commit()
 
            document_to_reload = frappe.get_doc("DocType",doctype)
            document_to_reload.reload()
            add_customized_fields_for_dynamic_doc(fields=[
                {"label": "Company Field","fieldname": "company_field","fieldtype": "Link","description": "static","idx": 0,"options":"Ezy Business Unit"},
                {"label": "WF Generated Request Id","fieldname": "wf_generated_request_id","fieldtype": "Data","description": "static","idx": 1},
                {"label": "WF Generated Request Status","fieldname": "wf_generated_request_status","fieldtype": "Data","description": "static","idx": 2}]
                ,doctype=doctype)
 
            ##### calling enqueing_creation_of_roadmap for creating roadmap for this particular mentioned form
            enqueing_creation_of_roadmap(doctype=doctype,property_name=business_unit,bulk_request=False)
        if len(fields)>0:
            # add_customized_fields_for_dynamic_doc(fields=fields,doctype=doctype,accessible_departments=accessible_departments)
            add_customized_fields_for_dynamic_doc(fields=fields,doctype=doctype)
        return {"success":True,"message":doctype}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        if "list index out of range" in str(e):
            return {"success":False,"message":"Please try again after some time else change the short name to add new form. Reason :- Already this name has been used. Deleting this form in database (works in background)."}
        frappe.log_error("Error in Creating New Doc",
                         "line No:{}\n{}".format(exc_tb.tb_lineno, str(e)))
        frappe.db.rollback()
        frappe.throw(str(e))
        return {"success": False, "message": str(e)}
def enqueued_add_customized_fields_for_dynamic_doc(fields: list[dict], doctype: str):
    try:
        if isinstance(fields, str):
            fields = literal_eval(fields)
        if not len(fields) > 0:
            return {"success": False, "message": "Pass Fields for storing."}

        fields_in_mentioned_doctype = [
            _[0] for _ in frappe.db.sql(f"SELECT fieldname FROM `tabDocField` WHERE parent ='{doctype}';")
        ]

        table_fieldnames = [item["options"] for item in fields if item.get("fieldtype") == "Table"]
        
        # Initialize as an empty dictionary
        child_table_fields = {"child_table_fields": {}}

        for table_name in table_fieldnames:
            fields_in_child_doctype = frappe.db.sql(
                f"SELECT IFNULL(options, '') AS options,IFNULL(description, '') AS description, fieldname, fieldtype, idx, label FROM `tabDocField` WHERE parent ='{table_name}';",
                as_dict=True
            )
           
            for each_child in fields_in_child_doctype:
                each_child['value'] = ''
            # Sort the fields by 'idx' within each child table
            sorted_fields = sorted(fields_in_child_doctype, key=lambda x: x["idx"])
 
            # Store the sorted results in the dictionary
            child_table_fields["child_table_fields"][table_name] = sorted_fields
            
        # Sort the dictionary keys before returning
        child_table_fields["child_table_fields"] = dict(sorted(child_table_fields["child_table_fields"].items()))
      
        for dicts_of_docs_entries in fields:
            if dicts_of_docs_entries["fieldname"] in fields_in_mentioned_doctype:
                doc_exists_name_or_not = frappe.db.exists("DocField", dicts_of_docs_entries)             
                if not doc_exists_name_or_not:
                    name_of_existing_doc = frappe.db.get_all(
                        "DocField",
                        filters={"fieldname": dicts_of_docs_entries["fieldname"], "parent": doctype},
                        pluck="name"
                    )[0]
                    doc_for_existing_custom_field = frappe.get_doc("DocField", name_of_existing_doc)
                    
                    if "options" in dicts_of_docs_entries:
                        if isinstance(dicts_of_docs_entries["options"], str):
                            doc_for_existing_custom_field.options = dicts_of_docs_entries["options"]
                        else:
                            doc_for_existing_custom_field.options = "\n".join(dicts_of_docs_entries["options"])
      
                    if "default" in dicts_of_docs_entries:
                        doc_for_existing_custom_field.default = dicts_of_docs_entries["default"]
                    if "description" in dicts_of_docs_entries:
                        doc_for_existing_custom_field.description = dicts_of_docs_entries["description"]
                    doc_for_existing_custom_field.idx = dicts_of_docs_entries["idx"]
                    doc_for_existing_custom_field.label = dicts_of_docs_entries["label"]
                    doc_for_existing_custom_field.fieldtype = dicts_of_docs_entries["fieldtype"]
                    # doc_for_existing_custom_field.reqd = dicts_of_docs_entries["reqd"]
                    doc_for_existing_custom_field.save(ignore_permissions=True)
                    frappe.db.commit()
                    doc_for_existing_custom_field.db_update()
                    doc_for_existing_custom_field.reload()
            else:
                # Create a new field
                doc_for_new_custom_field = frappe.get_doc('DocType', doctype)
                # appending records in child with get_doc
                doc_for_new_custom_field.append('fields', dicts_of_docs_entries)
                doc_for_new_custom_field.save(ignore_permissions=True)
                frappe.db.commit()
                doc_for_new_custom_field.db_update()
                doc_for_new_custom_field.reload()
        bench_migrating_from_code()
        workflow_from_defs = frappe.db.get_value("Ezy Form Definitions",doctype,"form_json")
        if not workflow_from_defs:
            workflow_from_defs = {"workflow":[]}
        else:
            workflow_from_defs = literal_eval(workflow_from_defs)["workflow"]
            workflow_from_defs = {"workflow":workflow_from_defs}
        field_with_workflow = {"fields":fields} | workflow_from_defs | child_table_fields
        frappe.db.set_value("Ezy Form Definitions",doctype,{"form_json":str(field_with_workflow).replace("'",'"').replace("None","null")})
        # frappe.db.set_value("Ezy Form Definitions",doctype,{"form_json":str(field_with_workflow).replace("'",'"').replace("None","null"),'accessible_departments':accessible_departments})
        frappe.db.commit()
        return {"success":True,"message":fields}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error("Error in add_customized_fields_for_dynamic_doc",
                         "line No:{}\n{}".format(exc_tb.tb_lineno, str(e)))
        frappe.db.rollback()
        frappe.throw(str(e))
        return {"success": False, "message": str(e)}
 
def enqueued_deleting_customized_field_from_custom_dynamic_doc(doctype:str,deleted_fields:list):
    try:
        frappe.db.delete("DocField",{"parent":doctype,"fieldname":["in",deleted_fields]})
        frappe.db.commit()
        reloading_doc = frappe.get_doc("DocType",doctype)
        reloading_doc.reload()
        return {"success":True,"message":deleted_fields}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error("Error in Deleting Field",
                         "line No:{}\n{}".format(exc_tb.tb_lineno, str(e)))
        frappe.db.rollback()
        frappe.throw(str(e))
        return {"success": False, "message": str(e)}

@frappe.whitelist()    
def bench_migrating_from_code():
    try:
        site_name = cstr(frappe.local.site)
        os.chdir(frappe.utils.get_bench_path() + "/sites")
        subprocess.run(["bench","--site", site_name,"migrate"])
    except Exception as e:
        frappe.log_error(str(e))
 
def activating_perms(doctype,role):
    if not frappe.db.exists("DocPerm",{"parent":doctype,"parentfield":"permissions","parenttype":"DocType","role":role}):
        perm_doc = frappe.new_doc("DocPerm")
        perm_doc.parent = doctype
        perm_doc.parentfield="permissions"
        perm_doc.parenttype="DocType"
        perm_doc.role=role
        perm_doc.insert(ignore_permissions=True)
        frappe.db.commit()
from ezy_forms.ezy_custom_forms.custom_script.v1.sign_up import email_template_create
def activating_perms_for_all_roles_in_wf_roadmap():

    unique_roles_from_all_roles = frappe.db.get_list("WF Roles",pluck="name")
    
    child_entries = frappe.get_all(
            "Doctype Permissions",
            filters={"parent": "Ezy Doctype Permissions", "parenttype": "Ezy Doctype Permissions", "parentfield": "document_type"},
            fields=["doctype_names"]
        )
    document_type_list = [entry["doctype_names"] for entry in child_entries]
    custom_feilds = frappe.get_all("DocType",filters={'module':["in",["User Forms","ezy_custom_forms"]]})
    custom_feilds_list = [doc.name for doc in custom_feilds]
    document_type_list.extend(custom_feilds_list)
    for doc in document_type_list:
        for role in unique_roles_from_all_roles:
            if not frappe.db.exists("Custom DocPerm",{"parent":doc,"role":role}):
                form_perms = frappe.new_doc("Custom DocPerm")
                form_perms.parent = doc
                form_perms.role = role
                form_perms.delete = 1
                form_perms.select = 1
                form_perms.read = 1
                form_perms.write = 1
                form_perms.create = 1
                form_perms.delete = 1
                form_perms.insert(ignore_permissions=True)
    frappe.db.commit()
    # Check if the path exists
    folder_path = get_site_path("public", "files", "Attachment folder")
    email_template_create()

    delete = lambda path: os.unlink(path) if os.path.isfile(path) or os.path.islink(path) else shutil.rmtree(path)

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        [delete(os.path.join(folder_path, f)) for f in os.listdir(folder_path)]
        

def sanitize_fieldname(name):
    # Remove all special characters; keep only alphanumeric and underscores
    name = re.sub(r'[^a-zA-Z0-9_]', '', name)
    # Prefix with '_' if starts with digit
    if name and name[0].isdigit():
        name = '_' + name
    return name

 
@frappe.whitelist()
def add_child_doctype(form_short_name: str, as_a_block: str, fields: list[dict], idx=None):

    try:
        if not idx:
            idx = 0

        # Ensure all fields have a valid idx (1-based)
        for i, field in enumerate(fields, start=1):
            field['idx'] = i

        # Check if the DocType exists
        if frappe.db.exists("DocType", form_short_name):
            # Load existing DocType
            exist_child_table = frappe.get_doc("DocType", form_short_name)
            existing_fields_dict = {field.fieldname: field for field in exist_child_table.fields}
            incoming_fieldnames = set()
            fields_updated = False

            for field in fields:
                raw_fieldname = field.get("fieldname") or field.get("label")
                clean_fieldname = sanitize_fieldname(raw_fieldname)

                if not clean_fieldname:
                    frappe.throw(f"Invalid fieldname after sanitization: '{raw_fieldname}' became empty.")

                if raw_fieldname != clean_fieldname:
                    print(f"Sanitized fieldname from '{raw_fieldname}' to '{clean_fieldname}'")

                field["fieldname"] = clean_fieldname
                incoming_fieldnames.add(clean_fieldname)

                new_field_data = {
                            "label": field.get("label"),
                            "fieldtype": field.get("fieldtype"),
                            "options": (
                                ("\n" if not field["options"].startswith("\n") else "") +
                                "\n".join([opt.strip() for opt in field["options"].split("\n") if opt.strip()])
                            ) if field.get("fieldtype") == "Select" and field.get("options") else field.get("options"),
                            "description": field.get("description"),
                            "idx": field.get("idx"),
                        }
                if clean_fieldname in existing_fields_dict:
                    # Update existing field
                    existing_field = existing_fields_dict[clean_fieldname]
                    for key, val in new_field_data.items():
                        if val is not None and getattr(existing_field, key) != val:
                            setattr(existing_field, key, val)
                            fields_updated = True
                else:
                    # Add new field
                    exist_child_table.append("fields", {
                        "fieldname": clean_fieldname,
                        **new_field_data,
                        "parentfield": "fields",
                        "parenttype": "DocType",
                    })
                    fields_updated = True

            # Remove fields that are no longer present in the input
            filtered_fields = [
                f for f in exist_child_table.fields if f.fieldname in incoming_fieldnames
            ]

            if len(filtered_fields) != len(exist_child_table.fields):
                fields_updated = True
            exist_child_table.fields = filtered_fields

            if fields_updated:
                exist_child_table.flags.ignore_validate = True  # In case of schema issues
                exist_child_table.save(ignore_permissions=True)
                frappe.db.commit()
                frappe.clear_cache(doctype=form_short_name)
                return f"Fields updated successfully in Doctype '{form_short_name}'."

        else:
            # Create new DocType
            doc = frappe.new_doc("DocType")
            doc.name = form_short_name
            doc.description = f"{as_a_block}"
            doc.creation = frappe_now()
            doc.modified = frappe_now()
            doc.modified_by = frappe.session.user
            doc.module = "User Forms"
            doc.app = "ezy_forms"
            doc.custom = 1
            doc.istable = 1
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
            doc.reload()
    
            for field in fields:
                # Ensure Select field has '\n' at the start of options
                if field.get("fieldtype") == "Select":
                    opt = field.get("options") or ""
                    if not opt.startswith("\n"):
                        field["options"] = "\n" + opt

                doc.append("fields", {
                    "fieldname": field.get("fieldname"),
                    "label": field.get("label"),
                    "fieldtype": field.get("fieldtype"),
                    "parentfield": "fields",
                    "parenttype": "DocType",
                    "options": field.get("options"),
                    "idx":field.get('idx')
                })

            doc.save(ignore_permissions=True)
            frappe.db.commit()

        if len(fields) > 0:
            add_customized_fields_for_dynamic_doc(fields=fields, doctype=form_short_name)
        child_doc_name = doc.name if doc else exist_child_table.name

        return [
            {
                "child_doc": {
                    "description": as_a_block,
                    "fieldname": child_doc_name,
                    "fieldtype": "Table",
                    "idx": idx or 0,
                    "label": child_doc_name,
                    "reqd": 0,
                    "value": "",
                    "options": child_doc_name
                }
            }
        ], "Table Added Successfully"

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in manage_child_doctype")
        return {"error": str(e)}




@frappe.whitelist()
def delete_roles_for_approver_roles(role:list|None,level:int|None,short_name:str|None, document_type:str|None, property:str|None):
	level = int(level)
	form_json, doc_name = frappe.get_value("Ezy Form Definitions", {'form_name': document_type, 'business_unit': property}, ["form_json", "name"])
	form_def_json_str =form_json
	form_json = json.loads(form_def_json_str)
	# Remove the targeted approver step
	workflow = form_json.get("workflow", [])
	filtered_workflow = []
	for step in workflow:
		if (
			step.get("type") == "approver"
			and step.get("idx") == level
			and any(r in role for r in step.get("roles", []))
		):
			continue  # Remove this step
		filtered_workflow.append(step)
	# Reindex the workflow steps
	for i, step in enumerate(filtered_workflow):
		step["idx"] = i
	form_json["workflow"] = filtered_workflow
	# Save it back
	frappe.db.set_value("Ezy Form Definitions", doc_name, "form_json", json.dumps(form_json))
	frappe.db.commit()
 
	updated_roadmaps = []
	doc = frappe.get_doc("WF Roadmap",{"document_type": short_name, "property": property},['wf_level_setup'])
	original_level_count = len(doc.wf_level_setup)
	# Prepare new child table list excluding the entry to delete
	new_level_setup = []
	for entry in doc.wf_level_setup:
		if entry.role in role and entry.level == int(level):
			continue  # Skip this entry (deleting it)
		elif entry.level > int(level):
			entry.level -= 1  # Shift down levels above the deleted one
		new_level_setup.append(entry)
	# Sort by level to maintain logical order
	new_level_setup.sort(key=lambda x: x.level or 0)
	# Update idx (serial number) in order
	for idx, entry in enumerate(new_level_setup, start=1):
		entry.idx = idx
	doc.wf_level_setup = new_level_setup
	level_changed = len(doc.wf_level_setup) != original_level_count
	if level_changed:
		doc.workflow_levels = len(doc.wf_level_setup)
		doc.save(ignore_permissions=True)
		frappe.db.commit()
		updated_roadmaps.append(doc.name)	
	frappe.db.commit()
	return {
		"status": "success",
		"updated_workflow": filtered_workflow,
		"updated_roadmaps": updated_roadmaps
	}