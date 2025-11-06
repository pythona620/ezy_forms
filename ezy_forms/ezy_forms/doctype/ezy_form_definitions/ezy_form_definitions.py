# Copyright (c) 2024, bharath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import now as frappe_now
from frappe.utils.background_jobs import enqueue
from frappe.modules.import_file import import_file_by_path,get_module_path
from frappe.modules import get_module_path
import sys
import subprocess
import os
import re
import json
import shutil
from ast import literal_eval
from itertools import chain
from typing import List, Dict, Any, Optional, Union
from contextlib import contextmanager

# Import custom modules
from ezy_forms.ezy_forms.doctype.ezy_form_definitions.linking_flow_and_forms import enqueing_creation_of_roadmap
from ezy_forms.api.v1.ezy_web_forms import create_qr_for_web_view


class EzyFormDefinitions(Document):
    pass


@contextmanager
def db_transaction():
    """Context manager for database transactions with automatic rollback on error."""
    try:
        yield
        frappe.db.commit()
    except Exception:
        frappe.db.rollback()
        raise


def validate_and_clean_fields(fields: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Validate and clean field data, handling edge cases."""
    cleaned_fields = []
    
    for i, field in enumerate(fields):
        # Skip layout fields that don't need fieldnames
        layout_fields = ['Column Break', 'Section Break', 'Row Break', 'Block Break']
        if field.get('fieldtype') in layout_fields:
            # Generate fieldname for layout fields if missing
            if not field.get('fieldname'):
                field['fieldname'] = f"_{field.get('fieldtype', 'field').lower().replace(' ', '_')}_{i}"
            cleaned_fields.append(field)
            continue
        
        # Validate regular fields
        fieldname = field.get('fieldname')
        if not fieldname:
            # Generate fieldname from label if missing
            label = field.get('label', f'field_{i}')
            fieldname = sanitize_fieldname(label.lower().replace(' ', '_'))
            field['fieldname'] = fieldname
        
        # Ensure required field properties exist
        field.setdefault('label', field.get('fieldname', '').replace('_', ' ').title())
        field.setdefault('fieldtype', 'Data')
        field.setdefault('reqd', 0)
        field.setdefault('idx', i)
        
        cleaned_fields.append(field)
    
    return cleaned_fields
   
def validate_required_params(**kwargs):
    """Validate required parameters and return cleaned data."""
    required_fields = ['owner_of_the_form', 'business_unit', 'form_name', 'form_short_name']
    missing_fields = [field for field in required_fields if not kwargs.get(field)]
    
    if missing_fields:
        frappe.throw(f"Missing required fields: {', '.join(missing_fields)}")
    
    # Clean and validate business unit
    business_unit = kwargs['business_unit']
    if not business_unit:
        frappe.throw("Business Unit is required as a prefix")
    
    return kwargs


@frappe.whitelist()
def process_form_creation_payload(**kwargs):
    """
    Process complete form creation payload from frontend.
    Handles all parameters including workflow_check, doctype, etc.
    """
    try:
        # Extract and validate main parameters
        main_params = {
            'owner_of_the_form': kwargs.get('owner_of_the_form'),
            'business_unit': kwargs.get('business_unit'), 
            'form_category': kwargs.get('form_category'),
            'form_name': kwargs.get('form_name'),
            'accessible_departments': kwargs.get('accessible_departments'),
            'form_short_name': kwargs.get('form_short_name'),
            'fields': kwargs.get('fields', []),
            'form_status': kwargs.get('form_status', 'Created'),
            'has_workflow': kwargs.get('has_workflow', ''),
            'is_linked_form': kwargs.get('is_linked_form', ''),
            'is_linked': kwargs.get('is_linked', 0),
            'is_predefined_doctype': kwargs.get('is_predefined_doctype', 0),
            'series': kwargs.get('series'),
        }
        
        # Additional parameters for context
        additional_params = {
            'workflow_check': kwargs.get('workflow_check', ''),
            'workflow_setup': kwargs.get('workflow_setup', []),
            'doctype': kwargs.get('doctype', kwargs.get('form_short_name')),
        }
        
        # Combine parameters
        all_params = {**main_params, **additional_params}
        
        # Call the main function
        return add_dynamic_doctype(**all_params)
        
    except Exception as e:
        frappe.log_error(
            title="Form Creation Payload Error",
            message=f"Error processing payload: {str(e)}\nPayload: {kwargs}"
        )
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def add_dynamic_doctype(
    owner_of_the_form: str,
    business_unit: str,
    form_category: str,
    form_name: str,
    accessible_departments: str,
    form_short_name: str,
    fields: List[Dict[str, Any]],
    form_status: str,
    has_workflow: Optional[str] = None,
    is_linked_form: Optional[str] = None,
    is_linked: Optional[int] = None,
    is_predefined_doctype: Optional[int] = None,
    series: Optional[str] = None,
    as_web_view:Optional[int] = None,
    mail_id:Optional[str] = None,
    public_form_response:Optional[str] = None,
    **kwargs  # Accept additional parameters gracefully
):
    """Optimized version with better parameter validation and error handling."""
    
    # Handle additional parameters that might be passed
    workflow_check = kwargs.get('workflow_check', '')
    doctype = kwargs.get('doctype', form_short_name)
    workflow_setup = kwargs.get('workflow_setup', [])
    
    # Validate parameters early
    validate_required_params(
        owner_of_the_form=owner_of_the_form,
        business_unit=business_unit,
        form_name=form_name,
        form_short_name=form_short_name
    )
    
    return enqueue(
        enqueued_add_dynamic_doctype,
        owner_of_the_form=owner_of_the_form,
        business_unit=business_unit,
        form_category=form_category,
        form_name=form_name,
        accessible_departments=accessible_departments,
        form_short_name=form_short_name,
        fields=fields,
        form_status=form_status,
        series=series,
        has_workflow=has_workflow,
        is_linked_form=is_linked_form,
        is_linked=is_linked,
        is_predefined_doctype=is_predefined_doctype,
        workflow_check=workflow_check,
        workflow_setup=workflow_setup,
        as_web_view=as_web_view,
        mail_id=mail_id,
        public_form_response=public_form_response,
        now=True,
        is_async=True,
        queue="short"
    )


@frappe.whitelist()
def add_customized_fields_for_dynamic_doc(fields: List[Dict[str, Any]], doctype: str):
    """Optimized field addition with better validation."""
    if not fields:
        frappe.throw("Fields parameter is required")
    
    if not doctype:
        frappe.throw("DocType parameter is required")
    
    return enqueue(
        enqueued_add_customized_fields_for_dynamic_doc,
        fields=fields,
        doctype=doctype,
        now=True,
        is_async=True,
        queue="short"
    )


def deleting_customized_field_from_custom_dynamic_doc(doctype: str, deleted_fields: List[str]):
    """Optimized field deletion with validation."""
    if not doctype or not deleted_fields:
        frappe.throw("Both doctype and deleted_fields are required")
    
    return enqueue(
        enqueued_deleting_customized_field_from_custom_dynamic_doc,
        doctype=doctype,
        deleted_fields=deleted_fields,
        now=True,
        is_async=True,
        queue="short"
    )


@frappe.whitelist()
def enqueued_add_dynamic_doctype(
    owner_of_the_form: str,
    business_unit: str,
    form_category: str,
    form_name: str,
    accessible_departments: str,
    form_short_name: str,
    fields: List[Dict[str, Any]],
    form_status: str,
    has_workflow: Optional[str] = None,
    is_linked: Optional[int] = None,
    is_predefined_doctype: Optional[int] = None,
    is_linked_form: Optional[str] = None,
    series: Optional[str] = None,
    workflow_check: Optional[str] = None,
    workflow_setup: Optional[List] = None,
    as_web_view:Optional[int] = None,
    mail_id:Optional[str] = None,
    public_form_response:Optional[str] = None,
    **kwargs  # Accept any additional parameters
):
    """Optimized DocType creation with better error handling and performance."""
    
    try:
        # Parse fields if string and clean them
        if isinstance(fields, str):
            fields = literal_eval(fields)
        
        # Clean and validate fields
        fields = validate_and_clean_fields(fields or [])

        doctype = form_short_name
        frappe.db.set_value("DocType",doctype,"owner", "Administrator")
        frappe.db.commit()
        # Batch database checks for better performance
        existing_checks = frappe.db.sql("""
            SELECT 
                EXISTS(SELECT 1 FROM `tabEzy Form Definitions` WHERE name = %(form_name)s) as form_exists,
                EXISTS(SELECT 1 FROM `tabDocType` WHERE name = %(doctype)s) as doctype_exists
        """, {"form_name": form_short_name, "doctype": doctype}, as_dict=True)[0]

        form_def_exists = existing_checks['form_exists']
        doctype_exists = existing_checks['doctype_exists']

        with db_transaction():
            # Update existing form definition efficiently
            if form_def_exists:
                frappe.db.set_value("Ezy Form Definitions", form_short_name, {
                    "form_status": form_status,
                    "accessible_departments": accessible_departments,
                    "owner_of_the_form": owner_of_the_form,
                    "is_linked_form": is_linked_form,
                    "is_linked": is_linked,
                    "is_predefined_doctype": is_predefined_doctype,
                    "has_workflow": has_workflow,
                    "as_web_view":as_web_view,
                    "mail_id":mail_id,
                    "public_form_response":public_form_response
                })
                if as_web_view == 1:
                    enqueue(create_qr_for_web_view,form_name=form_short_name,queue="short")

            # Create DocType if it doesn't exist
            if not doctype_exists:
                if form_def_exists:
                    return {
                        "success": True,
                        "message": f"Form '{form_short_name}' already created but not removed from 'Ezy Form Definitions'"
                    }

                # Generate naming series more efficiently
                naming_series = _generate_naming_series(series, business_unit, doctype)

                # Create DocType with optimized structure
                doc = _create_doctype(doctype, naming_series)
                doc.insert(ignore_permissions=True)

                # Set permissions immediately
                _set_system_manager_permissions(doctype)

                # Run migration
                bench_migrating_from_code()

                # Create form definitions
                _create_form_definitions(
                    form_category, accessible_departments, form_name, form_short_name,
                    form_status, owner_of_the_form, naming_series, business_unit,
                    has_workflow, is_linked_form, is_linked, is_predefined_doctype,public_form_response,as_web_view,mail_id
                )

                # Add default static fields
                _add_default_static_fields(doctype)

                # Create roadmap
                enqueing_creation_of_roadmap(
                    doctype=doctype, 
                    property_name=business_unit, 
                    bulk_request=False
                )

            # Add custom fields if provided
            if fields:
                add_customized_fields_for_dynamic_doc(fields=fields, doctype=doctype)

        return {"success": True, "message": doctype}

    except Exception as e:
        frappe.log_error(
            title="Dynamic DocType Creation Error",
            message=f"Error at line {sys.exc_info()[2].tb_lineno}: {str(e)}"
        )
        
        if "list index out of range" in str(e):
            return {"success": False, "message": "Short name already used. Please change and try again."}
        
        frappe.throw(str(e))


def _generate_naming_series(series: Optional[str], business_unit: str, doctype: str) -> str:
    """Generate naming series with proper validation."""
    if not series:
        return f"{business_unit}_{doctype}"
    
    cleaned_series = re.sub(r'[^a-zA-Z0-9#\-/\.]', '', series)
    if not cleaned_series:
        return f"{business_unit}_{doctype}"
    
    final_series = (
        f"{cleaned_series.upper()}-.####"
        if not re.search(r'[-/]\.#+$', cleaned_series.upper())
        else cleaned_series.upper()
    )
    
    return final_series


def _create_doctype(doctype: str, naming_series: str) -> Document:
    """Create DocType with standard configuration."""
    return frappe.get_doc({
        "doctype": "DocType",
        "name": doctype,
        "module": "User Forms",
        "app": "ezy_forms",
        "custom": 1,
        "owner": "Administrator",
        "track_changes": 1,
        "autoname": "naming_series:",
        "naming_rule": 'By "Naming Series" field',
        "naming_series": naming_series,
        "fields": [{
            "doctype": "DocField",
            "label": "Naming Series",
            "fieldname": "naming_series",
            "fieldtype": "Select",
            "options": naming_series,
            "reqd": 1,
            "insert_after": "title"
        }]
    })


def _set_system_manager_permissions(doctype: str):
    """Set System Manager permissions efficiently."""
    if not frappe.db.exists("DocPerm", {
        "parent": doctype,
        "parentfield": "permissions",
        "parenttype": "DocType",
        "role": "System Manager"
    }):
        perm_doc = frappe.new_doc("DocPerm")
        perm_doc.update({
            "parent": doctype,
            "parentfield": "permissions",
            "parenttype": "DocType",
            "role": "System Manager"
        })
        perm_doc.insert(ignore_permissions=True)


def _create_form_definitions(
    form_category: str, accessible_departments: str, form_name: str,
    form_short_name: str, form_status: str, owner_of_the_form: str,
    naming_series: str, business_unit: str, has_workflow: Optional[str],
    is_linked_form: Optional[str], is_linked: Optional[int],
    is_predefined_doctype: Optional[int],public_form_response:Optional[str],as_web_view:Optional[int],mail_id:Optional[str],
):
    """Create form definitions efficiently."""
    form_defs = frappe.get_doc({
        "doctype": "Ezy Form Definitions",
        "form_category": form_category,
        "owner": "Administrator",
        "accessible_departments": accessible_departments,
        "form_name": form_name,
        "form_short_name": form_short_name,
        "form_status": form_status,
        "owner_of_the_form": owner_of_the_form,
        "active": 1,
        "series": naming_series.upper(),
        "business_unit": business_unit,
        "count": 0,
        "has_workflow": has_workflow or '',
        "is_linked_form": is_linked_form or '',
        "is_linked": is_linked,
        "is_predefined_doctype": is_predefined_doctype,
        "as_web_view": as_web_view,
        "mail_id":mail_id,
        "public_form_response":public_form_response
    })
    form_defs.insert(ignore_permissions=True)

    
    # creating Qr For Web View forms
    if as_web_view == 1:
        enqueue(create_qr_for_web_view,form_name=form_short_name,queue="short")

def _add_default_static_fields(doctype: str):
    """Add default static fields to DocType."""
    default_fields = [
        {
            "label": "Company Field",
            "fieldname": "company_field",
            "fieldtype": "Link",
            "description": "static",
            "idx": 0,
            "options": "Ezy Business Unit"
        },
        {
            "label": "WF Generated Request Id",
            "fieldname": "wf_generated_request_id",
            "fieldtype": "Data",
            "description": "static",
            "idx": 1
        },
        {
            "label": "WF Generated Request Status",
            "fieldname": "wf_generated_request_status",
            "fieldtype": "Data",
            "description": "static",
            "idx": 2
        }
    ]
    add_customized_fields_for_dynamic_doc(fields=default_fields, doctype=doctype)


def enqueued_add_customized_fields_for_dynamic_doc(fields: List[Dict[str, Any]], doctype: str):
    """Optimized field addition with better performance and error handling."""
    try:
        if isinstance(fields, str):
            fields = literal_eval(fields)
        
        if not fields:
            return {"success": False, "message": "Pass Fields for storing."}

        with db_transaction():
            # Get existing fieldnames in single query
            existing_fieldnames = {
                r[0] for r in frappe.db.sql(
                    "SELECT fieldname FROM `tabDocField` WHERE parent = %s",
                    (doctype,)
                )
            }

            # Collect child table fieldnames
            table_fieldnames = [f["options"] for f in fields if f.get("fieldtype") == "Table"]
            child_table_fields ={}
            if table_fieldnames:
                child_table_fields = _get_child_table_fields(table_fieldnames)

            # Process fields efficiently
            doc = frappe.get_doc("DocType", doctype)
            
            for field in fields:
                fieldname = field["fieldname"]
                # try to find existing field
                existing_df = next((df for df in doc.fields if df.fieldname == fieldname), None)
                options_value = (
                    field.get("options") if isinstance(field.get("options"), str)
                    else "\n".join(field.get("options", []))
                )

                if existing_df:
                    # update existing
                    existing_df.options = options_value
                    existing_df.description = field.get("description")
                    existing_df.fieldtype = field.get("fieldtype")
                    existing_df.idx = field.get("idx")
                    existing_df.label = field.get("label")
                    existing_df.default = field.get("value")  # 'value' maps to 'default'
                else:
                    # append new
                    doc.append("fields", {
                        "description": field.get("description"),
                        "fieldname": fieldname,
                        "fieldtype": field.get("fieldtype"),
                        "idx": field.get("idx"),
                        "options": options_value,
                        "label": field.get("label"),
                        "default": field.get("value")
                    })

            doc.save(ignore_permissions=True)
            bench_migrating_from_code()

            # Update form JSON efficiently
            _update_form_json(doctype, fields, child_table_fields)

        return {"success": True, "message": fields}

    except Exception as e:
        frappe.log_error(
            title="Error in add_customized_fields_for_dynamic_doc",
            message=f"Line: {sys.exc_info()[2].tb_lineno}\n{str(e)}"
        )
        frappe.throw(str(e))


def _get_child_table_fields(table_fieldnames: List[str]) -> Dict[str, Any]:
    """Get child table fields efficiently."""
    if not table_fieldnames:
        return {"child_table_fields": {}}

    # Use single query for all child tables
    placeholders = ", ".join(["%s"] * len(table_fieldnames))
    child_fields_data = frappe.db.sql(f"""
        SELECT 
            parent,
            IFNULL(options,'') AS options,
            IFNULL(description,'') AS description,
            fieldname, fieldtype, idx, label
        FROM `tabDocField` 
        WHERE parent IN ({placeholders})
        ORDER BY parent, idx
    """, table_fieldnames, as_dict=True)

    # Group by parent table
    child_table_fields = {}
    for field in child_fields_data:
        parent = field.pop('parent')
        field['value'] = ""
        
        if parent not in child_table_fields:
            child_table_fields[parent] = []
        child_table_fields[parent].append(field)

    return {"child_table_fields": dict(sorted(child_table_fields.items()))}


def _update_existing_field(fieldname: str, doctype: str, field_data: Dict[str, Any]):
    """Update existing field efficiently."""
    name = frappe.db.get_value(
        "DocField", 
        {"fieldname": fieldname, "parent": doctype}, 
        "name"
    )
    
    if name:
        # Use direct SQL update for better performance
        options_value = (
            field_data.get("options") if isinstance(field_data.get("options"), str)
            else "\n".join(field_data.get("options", []))
        )
        
        frappe.db.sql("""
            UPDATE `tabDocField` 
            SET options = %s, `default` = %s, description = %s, 
                idx = %s, label = %s, fieldtype = %s, modified = %s
            WHERE name = %s
        """, (
            options_value,
            field_data.get("default"),
            field_data.get("description"),
            field_data.get("idx"),
            field_data.get("label"),
            field_data.get("fieldtype"),
            frappe_now(),
            name
        ))
        frappe.db.commit()


def _update_form_json(doctype: str, fields: List[Dict[str, Any]], child_table_fields: Dict[str, Any]):
    """Update form JSON efficiently."""
    existing_workflow = frappe.db.get_value("Ezy Form Definitions", doctype, "form_json")
    workflow = {"workflow": []}
    
    if existing_workflow:
        try:
            parsed_workflow = literal_eval(existing_workflow)
            workflow = {"workflow": parsed_workflow.get("workflow", [])}
        except (ValueError, SyntaxError):
            pass  # Keep default empty workflow

    field_with_workflow = {"fields": fields, **workflow, **child_table_fields}
    
    frappe.db.set_value(
        "Ezy Form Definitions",
        doctype,
        "form_json",
        json.dumps(field_with_workflow)
    )


def enqueued_deleting_customized_field_from_custom_dynamic_doc(doctype: str, deleted_fields: List[str]):
    """Optimized field deletion."""
    try:
        with db_transaction():
            # Use efficient batch delete
            frappe.db.delete("DocField", {
                "parent": doctype,
                "fieldname": ["in", deleted_fields]
            })
            
            # Reload DocType
            doc = frappe.get_doc("DocType", doctype)
            doc.reload()
            
        return {"success": True, "message": deleted_fields}
        
    except Exception as e:
        frappe.log_error(
            title="Error in Deleting Field",
            message=f"Line: {sys.exc_info()[2].tb_lineno}\n{str(e)}"
        )
        frappe.throw(str(e))


@frappe.whitelist()
def bench_migrating_from_code():
    """Optimized module sync with better error handling."""
    try:
        module = "User Forms"
        module_path = get_module_path(module)
        
        if not os.path.exists(module_path):
            return f"Module path {module_path} does not exist."

        # Use os.walk more efficiently
        json_files = [
            os.path.join(root, fname)
            for root, _, files in os.walk(module_path)
            for fname in files
            if fname.endswith(".json")
        ]

        # Import files with better error handling
        for file_path in json_files:
            try:
                import_file_by_path(file_path, force=True, ignore_version=True)
            except Exception as e:
                frappe.log_error(f"Failed to import {file_path}: {str(e)}")

        frappe.clear_cache()
        return f"Module {module} synced successfully."

    except Exception as e:
        frappe.log_error(f"Error syncing module: {str(e)}")
        return f"Error syncing {module}: {str(e)}"


def activating_perms(doctype: str, role: str):
    """Optimized permission activation."""
    if not frappe.db.exists("DocPerm", {
        "parent": doctype,
        "parentfield": "permissions",
        "parenttype": "DocType",
        "role": role
    }):
        perm_doc = frappe.new_doc("DocPerm")
        perm_doc.update({
            "parent": doctype,
            "parentfield": "permissions",
            "parenttype": "DocType",
            "role": role
        })
        perm_doc.insert(ignore_permissions=True)
        frappe.db.commit()


def activating_perms_for_all_roles_in_wf_roadmap():
    """Optimized bulk permission activation."""
    try:
        # Get all unique roles and doctypes in single queries
        unique_roles = frappe.db.get_list("WF Roles", pluck="name")
        
        document_types = frappe.get_all(
            "Doctype Permissions",
            filters={
                "parent": "Ezy Doctype Permissions",
                "parenttype": "Ezy Doctype Permissions",
                "parentfield": "document_type",
            },
            pluck="doctype_names"
        )

        # Batch check existing permissions
        existing_perms = set()
        if document_types and unique_roles:
            existing_perms_data = frappe.db.sql("""
                SELECT CONCAT(parent, '|', role) as perm_key
                FROM `tabCustom DocPerm`
                WHERE parent IN ({}) AND role IN ({})
            """.format(
                ', '.join(['%s'] * len(document_types)),
                ', '.join(['%s'] * len(unique_roles))
            ), document_types + unique_roles)
            
            existing_perms = {row[0] for row in existing_perms_data}

        # Bulk create missing permissions
        missing_perms = []
        for doctype in document_types:
            for role in unique_roles:
                perm_key = f"{doctype}|{role}"
                if perm_key not in existing_perms:
                    missing_perms.append({
                        "doctype": "Custom DocPerm",
                        "parent": doctype,
                        "role": role,
                        "delete": 1,
                        "select": 1,
                        "read": 1,
                        "write": 1,
                        "create": 1
                    })

        # Bulk insert missing permissions
        if missing_perms:
            for perm_data in missing_perms:
                doc = frappe.get_doc(perm_data)
                doc.insert(ignore_permissions=True)
            
            frappe.db.commit()

    except Exception as e:
        frappe.log_error(f"Error in activating_perms_for_all_roles_in_wf_roadmap: {str(e)}")
        frappe.db.rollback()


def sanitize_fieldname(name: str) -> str:
    """Optimized fieldname sanitization."""
    if not name:
        return ""
    
    # Remove special characters and handle digits at start
    cleaned = re.sub(r'[^a-zA-Z0-9_]', '', str(name))
    return f"_{cleaned}" if cleaned and cleaned[0].isdigit() else cleaned


@frappe.whitelist()
def add_child_doctype(form_short_name: str, as_a_block: str, fields: List[Dict[str, Any]], idx: Optional[int] = None):
    """Optimized child doctype creation."""
    try:
        if not idx:
            idx = 0

        # Sanitize and validate fields
        for i, field in enumerate(fields, start=1):
            field['idx'] = i
            raw_fieldname = field.get("fieldname") or field.get("label")
            clean_fieldname = sanitize_fieldname(raw_fieldname)
            
            if not clean_fieldname:
                frappe.throw(f"Invalid fieldname after sanitization: '{raw_fieldname}' became empty.")
            
            field["fieldname"] = clean_fieldname

        with db_transaction():
            if frappe.db.exists("DocType", form_short_name):
                result = _update_existing_child_doctype(form_short_name, fields)
                return result
            else:
                result = _create_new_child_doctype(form_short_name, as_a_block, fields, idx)
                return result

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in add_child_doctype")
        return {"error": str(e)}


def _update_existing_child_doctype(form_short_name: str, fields: List[Dict[str, Any]]) -> str:
    """Update existing child doctype efficiently."""
    doc = frappe.get_doc("DocType", form_short_name)
    existing_fields_dict = {field.fieldname: field for field in doc.fields}
    incoming_fieldnames = {field["fieldname"] for field in fields}
    fields_updated = False

    for field in fields:
        options_value = (
            field.get("options") if isinstance(field.get("options"), str)
            else "\n".join(field.get("options", []))
        )
        fieldname = field["fieldname"]
        new_field_data = {
            "label": field.get("label"),
            "fieldtype": field.get("fieldtype"),
            "options":options_value,
            "reqd":0,
            "description":field.get("description", ""),
        }

        if fieldname in existing_fields_dict:
            # Update existing field
            existing_field = existing_fields_dict[fieldname]
            for key, val in new_field_data.items():
                if val is not None and getattr(existing_field, key) != val:
                    setattr(existing_field, key, val)
                    fields_updated = True
        else:
            # Add new field
            doc.append("fields", {
                "fieldname": fieldname,
                **new_field_data,
                "parentfield": "fields",
                "parenttype": "DocType",
            })
            fields_updated = True

    # Remove obsolete fields
    doc.fields = [f for f in doc.fields if f.fieldname in incoming_fieldnames]
    
    if fields_updated:
        doc.flags.ignore_validate = True
        doc.save(ignore_permissions=True)
        frappe.clear_cache(doctype=form_short_name)
        
    return f"Fields updated successfully in DocType '{form_short_name}'."


def _create_new_child_doctype(form_short_name: str, as_a_block: str, fields: List[Dict[str, Any]], idx: int):
    """Create new child doctype efficiently."""
    # Create DocType
    doc = frappe.get_doc({
        "doctype": "DocType",
        "name": form_short_name,
        "description": as_a_block,
        "module": "User Forms",
        "app": "ezy_forms",
        "custom": 1,
        "istable": 1
    })
    doc.insert(ignore_permissions=True)
    doc.reload()

    # Add fields
    for field in fields:
        # Handle Select field options
        if field.get("fieldtype") == "Select":
            options = field.get("options", "")
            if options and not options.startswith("\n"):
                field["options"] = f"\n{options}"

        doc.append("fields", {
            "fieldname": field.get("fieldname"),
            "label": field.get("label"),
            "fieldtype": field.get("fieldtype"),
            "parentfield": "fields",
            "parenttype": "DocType",
            "options": field.get("options"),
            "idx": field.get('idx')
        })

    doc.save(ignore_permissions=True)

    # Add customized fields
    if fields:
        add_customized_fields_for_dynamic_doc(fields=fields, doctype=form_short_name)

    return [
        {
            "child_doc": {
                "description": as_a_block,
                "fieldname": form_short_name.replace(" ", "_").lower(),
                "fieldtype": "Table",
                "idx": idx,
                "label": form_short_name,
                "reqd": 0,
                "value": "",
                "options": form_short_name
            }
        }
    ], "Table Added Successfully"


@frappe.whitelist()
def delete_roles_for_approver_roles(
    role: Optional[List[str]], 
    level: Optional[int], 
    short_name: Optional[str], 
    document_type: Optional[str], 
    property: Optional[str]
):
    """Optimized role deletion with better error handling."""
    try:
        if not all([role, level is not None, short_name, document_type, property]):
            frappe.throw("All parameters are required")

        level = int(level)
        
        with db_transaction():
            # Get form JSON efficiently
            form_json, doc_name = frappe.get_value(
                "Ezy Form Definitions", 
                {'form_name': document_type, 'business_unit': property}, 
                ["form_json", "name"]
            )
            
            if not form_json:
                frappe.throw("Form definition not found")

            form_data = json.loads(form_json)
            workflow = form_data.get("workflow", [])
            
            # Filter and reindex workflow
            filtered_workflow = []
            for i, step in enumerate(workflow):
                if (step.get("type") == "approver" and 
                    step.get("idx") == level and 
                    any(r in role for r in step.get("roles", []))):
                    continue
                step["idx"] = len(filtered_workflow)
                filtered_workflow.append(step)

            form_data["workflow"] = filtered_workflow
            
            # Update form definition
            frappe.db.set_value("Ezy Form Definitions", doc_name, "form_json", json.dumps(form_data))

            # Update roadmap
            updated_roadmaps = _update_roadmap(short_name, property, role, level)

        return {
            "status": "success",
            "updated_workflow": filtered_workflow,
            "updated_roadmaps": updated_roadmaps
        }

    except Exception as e:
        frappe.log_error(f"Error in delete_roles_for_approver_roles: {str(e)}")
        frappe.throw(str(e))


def _update_roadmap(short_name: str, property: str, role: List[str], level: int) -> List[str]:
    """Update roadmap efficiently and safely."""
    doc = frappe.get_doc("WF Roadmap", {"document_type": short_name, "property": property})
    
    # Filter and reindex levels
    new_setup = []
    seen = set()

    for entry in doc.wf_level_setup:
        key = (entry.role, entry.level)
        # Skip duplicates or entries to delete
        if (entry.role in role and entry.level == level) or key in seen:
            continue

        # Reindex levels higher than deleted one
        if entry.level > level:
            entry.level -= 1

        seen.add((entry.role, entry.level))
        new_setup.append(entry)

    # Sort and reindex by level
    new_setup.sort(key=lambda x: x.level or 0)
    for idx, entry in enumerate(new_setup, start=1):
        entry.idx = idx

    # Replace the child table
    doc.set("wf_level_setup", new_setup)

    # Validate level count
    level_counts = [entry.level for entry in new_setup]
    doc.workflow_levels = max(level_counts) if level_counts else 0


    doc.save(ignore_permissions=True)
    return [doc.name]



@frappe.whitelist()
def ezy_doctype_permission():
    """
    Optimized function to update Ezy Doctype Permissions.
    API: api/method/ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions.ezy_doctype_permission
    """
    try:
        # Default configurations
        default_employee_doctypes = [
            'DocType', 'User', 'Role', 'Data Import', 'Data Export',
            'System Settings', 'Website Settings', 'Email Account',
            'Version', 'Activity Log', 'Notification Settings'
        ]
        
        default_modules = [
            "User Forms", "ezy_custom_forms", "Form Templates",
            "Ezy Forms", "Ezy Flow", "ezy_forms"
        ]

        with db_transaction():
            # Get or create main permissions document
            ezy_permissions = frappe.get_doc("Ezy Doctype Permissions", "Ezy Doctype Permissions")
            
            # Get existing configurations efficiently
            existing_employee_perms = {d.doctype_names for d in ezy_permissions.document_type}
            existing_modules = {d.custom_modules for d in ezy_permissions.custom_modules or []}
            
            # Add missing default employee doctypes
            added_perms = False
            for doctype in default_employee_doctypes:
                if doctype not in existing_employee_perms:
                    ezy_permissions.append("document_type", {"doctype_names": doctype})
                    added_perms = True
            
            # Add missing default modules
            added_modules = False
            for module in default_modules:
                if module not in existing_modules:
                    ezy_permissions.append("custom_modules", {"custom_modules": module})
                    added_modules = True
            
            # Save if changes were made
            if added_perms or added_modules:
                ezy_permissions.save(ignore_permissions=True)
            
            # Get final module list and fetch custom doctypes
            final_modules = [d.custom_modules for d in ezy_permissions.custom_modules]
            custom_doctypes = frappe.get_list(
                "DocType", 
                filters={'module': ["in", final_modules]}, 
                pluck="name"
            ) if final_modules else []
            
            # Combine all doctypes and remove duplicates
            all_doctypes = list(set(default_employee_doctypes + custom_doctypes))
            
        return all_doctypes

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in ezy_doctype_permissions")
        return {"error": str(e)}


# Additional utility functions for better performance

def bulk_field_operations(doctype: str, operations: List[Dict[str, Any]]):
    """
    Perform bulk field operations (add/update/delete) in a single transaction.
    
    Args:
        doctype: Target DocType name
        operations: List of operations with 'action' and 'field_data'
    """
    try:
        with db_transaction():
            doc = frappe.get_doc("DocType", doctype)
            existing_fields = {f.fieldname: f for f in doc.fields}
            
            for operation in operations:
                action = operation.get('action')
                field_data = operation.get('field_data', {})
                
                if action == 'add':
                    if field_data.get('fieldname') not in existing_fields:
                        doc.append("fields", field_data)
                
                elif action == 'update':
                    fieldname = field_data.get('fieldname')
                    if fieldname in existing_fields:
                        field_obj = existing_fields[fieldname]
                        for key, value in field_data.items():
                            if hasattr(field_obj, key):
                                setattr(field_obj, key, value)
                
                elif action == 'delete':
                    fieldname = field_data.get('fieldname')
                    doc.fields = [f for f in doc.fields if f.fieldname != fieldname]
            
            doc.save(ignore_permissions=True)
            bench_migrating_from_code()
            
        return {"success": True, "message": "Bulk operations completed successfully"}
        
    except Exception as e:
        frappe.log_error(f"Error in bulk_field_operations: {str(e)}")
        return {"success": False, "error": str(e)}


def get_form_statistics():
    """Get comprehensive form statistics for dashboard/reporting."""
    try:
        stats = frappe.db.sql("""
            SELECT 
                business_unit,
                form_category,
                COUNT(*) as total_forms,
                SUM(CASE WHEN form_status = 'Active' THEN 1 ELSE 0 END) as active_forms,
                SUM(CASE WHEN has_workflow != '' THEN 1 ELSE 0 END) as workflow_forms,
                AVG(count) as avg_submissions
            FROM `tabEzy Form Definitions`
            GROUP BY business_unit, form_category
            ORDER BY business_unit, form_category
        """, as_dict=True)
        
        return {
            "success": True,
            "statistics": stats,
            "summary": {
                "total_forms": sum(s['total_forms'] for s in stats),
                "total_active": sum(s['active_forms'] for s in stats),
                "total_with_workflow": sum(s['workflow_forms'] for s in stats)
            }
        }
        
    except Exception as e:
        frappe.log_error(f"Error in get_form_statistics: {str(e)}")
        return {"success": False, "error": str(e)}


def cleanup_orphaned_fields():
    """Clean up orphaned fields and optimize database."""
    try:
        with db_transaction():
            # Find orphaned DocFields
            orphaned_fields = frappe.db.sql("""
                SELECT df.name
                FROM `tabDocField` df
                LEFT JOIN `tabDocType` dt ON df.parent = dt.name
                WHERE dt.name IS NULL
            """)
            
            if orphaned_fields:
                orphaned_names = [f[0] for f in orphaned_fields]
                frappe.db.sql("""
                    DELETE FROM `tabDocField` 
                    WHERE name IN ({})
                """.format(', '.join(['%s'] * len(orphaned_names))), orphaned_names)
            
            # Find orphaned DocPerms
            orphaned_perms = frappe.db.sql("""
                SELECT dp.name
                FROM `tabDocPerm` dp
                LEFT JOIN `tabDocType` dt ON dp.parent = dt.name
                WHERE dt.name IS NULL
            """)
            
            if orphaned_perms:
                orphaned_perm_names = [p[0] for p in orphaned_perms]
                frappe.db.sql("""
                    DELETE FROM `tabDocPerm` 
                    WHERE name IN ({})
                """.format(', '.join(['%s'] * len(orphaned_perm_names))), orphaned_perm_names)
        
        return {
            "success": True,
            "cleaned_fields": len(orphaned_fields) if orphaned_fields else 0,
            "cleaned_permissions": len(orphaned_perms) if orphaned_perms else 0
        }
        
    except Exception as e:
        frappe.log_error(f"Error in cleanup_orphaned_fields: {str(e)}")
        return {"success": False, "error": str(e)}


class FormDefinitionManager:
    """
    Enhanced manager class for handling form definitions with caching and batch operations.
    """
    
    def __init__(self):
        self._cache = {}
        self._cache_expiry = {}
    
    def get_cached_form_definition(self, form_name: str, business_unit: str, cache_timeout: int = 300):
        """Get form definition with caching."""
        cache_key = f"{business_unit}_{form_name}"
        now = frappe.utils.now_datetime()
        
        # Check cache validity
        if (cache_key in self._cache and 
            cache_key in self._cache_expiry and 
            now < self._cache_expiry[cache_key]):
            return self._cache[cache_key]
        
        # Fetch from database
        form_def = frappe.get_value(
            "Ezy Form Definitions",
            {"form_name": form_name, "business_unit": business_unit},
            ["form_json", "form_status", "accessible_departments"],
            as_dict=True
        )
        
        if form_def:
            # Cache the result
            self._cache[cache_key] = form_def
            self._cache_expiry[cache_key] = now + frappe.utils.datetime.timedelta(seconds=cache_timeout)
            
        return form_def
    
    def invalidate_cache(self, form_name: str = None, business_unit: str = None):
        """Invalidate cache for specific form or all forms."""
        if form_name and business_unit:
            cache_key = f"{business_unit}_{form_name}"
            self._cache.pop(cache_key, None)
            self._cache_expiry.pop(cache_key, None)
        else:
            self._cache.clear()
            self._cache_expiry.clear()
    
    def batch_update_forms(self, updates: List[Dict[str, Any]]):
        """Perform batch updates on multiple forms."""
        try:
            with db_transaction():
                for update in updates:
                    form_name = update.get('form_name')
                    business_unit = update.get('business_unit')
                    update_data = update.get('data', {})
                    
                    if form_name and business_unit:
                        frappe.db.set_value(
                            "Ezy Form Definitions",
                            {"form_name": form_name, "business_unit": business_unit},
                            update_data
                        )
                        
                        # Invalidate cache
                        self.invalidate_cache(form_name, business_unit)
            
            return {"success": True, "updated_count": len(updates)}
            
        except Exception as e:
            frappe.log_error(f"Error in batch_update_forms: {str(e)}")
            return {"success": False, "error": str(e)}


# Global instance
form_manager = FormDefinitionManager()


# Performance monitoring decorator
def monitor_performance(func):
    """Decorator to monitor function performance."""
    @frappe.whitelist()
    def wrapper(*args, **kwargs):
        import time
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            execution_time = time.time() - start_time
            
            # Log slow operations (>5 seconds)
            if execution_time > 5:
                frappe.log_error(
                    f"Slow operation detected: {func.__name__} took {execution_time:.2f} seconds",
                    "Performance Warning"
                )
            
            return result
            
        except Exception as e:
            execution_time = time.time() - start_time
            frappe.log_error(
                f"Error in {func.__name__} after {execution_time:.2f} seconds: {str(e)}",
                "Function Error"
            )
            raise
    
    return wrapper

# Apply performance monitoring to critical functions
add_dynamic_doctype = monitor_performance(add_dynamic_doctype)
enqueued_add_dynamic_doctype = monitor_performance(enqueued_add_dynamic_doctype)
enqueued_add_customized_fields_for_dynamic_doc = monitor_performance(enqueued_add_customized_fields_for_dynamic_doc)