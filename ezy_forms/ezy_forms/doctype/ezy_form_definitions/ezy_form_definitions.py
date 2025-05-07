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
from frappe.utils import cstr
from frappe.utils import now as frappe_now
 
class EzyFormDefinitions(Document):
    pass
 
@frappe.whitelist()
def add_dynamic_doctype(owner_of_the_form:str,business_unit:str,form_category:str,form_name:str,accessible_departments:str,form_short_name:str,fields:list[dict],form_status:str,series=None):
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
 
def enqueued_add_dynamic_doctype(owner_of_the_form:str,business_unit:str,form_category:str,form_name:str,accessible_departments:str,form_short_name:str,fields:list[dict],form_status:str,series=None):
    """ Owner_of_the_form should come from Departments Doctype in Select Field."""
    """Adding DocTypes dynamically, giving Perms for the doctype and creating a default section-break field for DocType"""
    try:
        if business_unit == None or business_unit == "":return {"success":False,"message":"Pass Business Unit because it is considered as prefix"}
        doctype = form_short_name
        if isinstance(fields,str):
            fields = literal_eval(fields)
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
            doc.description = business_unit
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
            form_defs.series = series + "-.####" if series else None
            form_defs.business_unit = business_unit
            form_defs.count = 0
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

        table_fieldnames = [item["fieldname"] for item in fields if item.get("fieldtype") == "Table"]
        
        # Initialize as an empty dictionary
        child_table_fields = {"child_table_fields": {}}

        for table_name in table_fieldnames:
            fields_in_child_doctype = frappe.db.sql(
                f"SELECT fieldname, fieldtype, idx, label FROM `tabDocField` WHERE parent ='{table_name}';",
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
 
def activating_perms_for_all_roles_in_wf_roadmap():

    unique_roles_from_all_roles = frappe.db.get_list("WF Roles",pluck="name")
    
    child_entries = frappe.get_all(
            "Doctype Permissions",
            filters={"parent": "Ezy Doctype Permissions", "parenttype": "Ezy Doctype Permissions", "parentfield": "document_type"},
            fields=["doctype_names"]
        )
    document_type_list = [entry["doctype_names"] for entry in child_entries]
 
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
    
 
 
 
@frappe.whitelist()
def add_child_doctype(form_short_name: str, as_a_block:str, fields: list[dict],idx=None) :

    try:
        doc = None  # Ensure 'doc' is always defined
        exist_child_table = None
        if not idx :
            idx = 0
        # Check if the DocType exists
        if frappe.db.exists("DocType", form_short_name):
 
            exist_child_table = frappe.get_doc("DocType", form_short_name)
            existing_fields = {field.fieldname: field for field in exist_child_table.fields}
            incoming_fieldnames = {field["fieldname"] for field in fields}
            fields_updated = False
 
            # Update existing fields or add new ones
            for field in fields:
                fieldname = field.get("fieldname")
                new_label = field.get("label")
                new_fieldtype = field.get("fieldtype")
                
                if fieldname in existing_fields:
                    existing_field = existing_fields[fieldname]
                    if new_label:
                        existing_field.label = new_label
                    if new_fieldtype:
                        existing_field.fieldtype = new_fieldtype
                    fields_updated = True
                else:
                    new_field = exist_child_table.append("fields", {
                        "fieldname": fieldname,
                        "label": new_label,
                        "fieldtype": new_fieldtype,
                        "parentfield": "fields",
                        "parenttype": "DocType",
                        # "options":field.get("options")
                    })
                    fields_updated = True
 
            # Remove fields not in the incoming data
            exist_child_table.fields = [field for field in exist_child_table.fields if field.fieldname in incoming_fieldnames]
            
            if fields_updated:
                exist_child_table.save(ignore_permissions=True)
                frappe.db.commit()
                exist_child_table.db_update()
                
                return f"Fields updated successfully in Doctype '{form_short_name}'."
            else:
                return f"No changes made to Doctype '{form_short_name}'."
 
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
                doc.append("fields", {
                    "fieldname": field.get("fieldname"),
                    "label": field.get("label"),
                    "fieldtype": field.get("fieldtype"),
                    "parentfield": "fields",
                    "parenttype": "DocType",
                    "options":field.get("options")
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
                    "idx": idx ,
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
 
