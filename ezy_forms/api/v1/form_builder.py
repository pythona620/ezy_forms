"""
Form Builder API
Provides endpoints for dynamic form field creation and management
"""

import frappe
import json
import re
from frappe import _


@frappe.whitelist()
def get_field_types():
    """
    Get all available field types from Frappe

    Returns:
        dict: Success status and list of field types
    """
    # Authentication check
    if frappe.session.user == "Guest":
        frappe.throw(_("Authentication required"), frappe.AuthenticationError)

    try:
        # Query distinct field types from DocField
        query = """
            SELECT DISTINCT fieldtype
            FROM `tabDocField`
            WHERE fieldtype IS NOT NULL
            ORDER BY fieldtype
        """
        field_types = frappe.db.sql(query, as_dict=True)

        return {
            "success": True,
            "field_types": [f['fieldtype'] for f in field_types]
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Field Types Error")
        return {
            "success": False,
            "message": "Failed to fetch field types",
            "error": str(e)
        }


@frappe.whitelist()
def save_form_definition(form_name, fields, metadata=None):
    """
    Save form definition with field schema

    Args:
        form_name: Name of the form
        fields: JSON string or list of field definitions
        metadata: Additional form metadata (optional)

    Returns:
        dict: Success status and form ID
    """
    # Authentication check
    if frappe.session.user == "Guest":
        frappe.throw(_("Authentication required"), frappe.AuthenticationError)

    try:
        # Parse fields if JSON string
        if isinstance(fields, str):
            fields = json.loads(fields)

        # Validate all fields
        for idx, field in enumerate(fields):
            validate_field(field, idx)

        # Check if form already exists
        existing_form = frappe.db.exists("Ezy Form Definitions", {"form_name": form_name})

        if existing_form:
            # Update existing form
            form_doc = frappe.get_doc("Ezy Form Definitions", existing_form)
            form_doc.form_json = json.dumps(fields)
            if metadata:
                # Add metadata fields if they exist in the doctype
                for key, value in metadata.items():
                    if hasattr(form_doc, key):
                        setattr(form_doc, key, value)
            form_doc.save()
            frappe.db.commit()

            return {
                "success": True,
                "form_id": form_doc.name,
                "message": "Form updated successfully"
            }
        else:
            # Create new form
            form_doc = frappe.get_doc({
                "doctype": "Ezy Form Definitions",
                "form_name": form_name,
                "form_json": json.dumps(fields)
            })

            # Add metadata if provided
            if metadata:
                for key, value in metadata.items():
                    if hasattr(form_doc, key):
                        setattr(form_doc, key, value)

            form_doc.insert()
            frappe.db.commit()

            return {
                "success": True,
                "form_id": form_doc.name,
                "message": "Form created successfully"
            }

    except frappe.ValidationError as e:
        return {
            "success": False,
            "message": str(e)
        }
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Save Form Definition Error")
        return {
            "success": False,
            "message": "Failed to save form definition",
            "error": str(e)
        }


@frappe.whitelist()
def get_form_definition(form_name):
    """
    Get form definition with all fields

    Args:
        form_name: Name of the form to retrieve

    Returns:
        dict: Success status and form data
    """
    # Authentication check
    if frappe.session.user == "Guest":
        frappe.throw(_("Authentication required"), frappe.AuthenticationError)

    try:
        # Check if form exists
        if not frappe.db.exists("Ezy Form Definitions", {"form_name": form_name}):
            return {
                "success": False,
                "message": f"Form '{form_name}' not found"
            }

        # Get form document
        query = """
            SELECT name, form_name, form_json, creation, modified, owner
            FROM `tabEzy Form Definitions`
            WHERE form_name = %s
            LIMIT 1
        """
        form_data = frappe.db.sql(query, (form_name,), as_dict=True)

        if not form_data:
            return {
                "success": False,
                "message": f"Form '{form_name}' not found"
            }

        form = form_data[0]
        fields = json.loads(form.form_json) if form.form_json else []

        return {
            "success": True,
            "form_name": form.form_name,
            "fields": fields,
            "form_id": form.name,
            "created": form.creation,
            "modified": form.modified,
            "owner": form.owner
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Form Definition Error")
        return {
            "success": False,
            "message": "Failed to retrieve form definition",
            "error": str(e)
        }


@frappe.whitelist()
def get_docfield_meta(doctype=None):
    """
    Get DocField structure for reference
    Returns the meta structure of DocField doctype

    Args:
        doctype: Optional specific doctype to get fields for

    Returns:
        dict: Success status and field structure
    """
    # Authentication check
    if frappe.session.user == "Guest":
        frappe.throw(_("Authentication required"), frappe.AuthenticationError)

    try:
        meta = frappe.get_meta("DocField")

        field_structure = {}
        for field in meta.fields:
            field_structure[field.fieldname] = {
                "fieldtype": field.fieldtype,
                "label": field.label,
                "options": field.options,
                "default": field.default,
                "reqd": field.reqd,
                "description": field.description
            }

        return {
            "success": True,
            "structure": field_structure
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get DocField Meta Error")
        return {
            "success": False,
            "message": "Failed to retrieve DocField meta",
            "error": str(e)
        }


@frappe.whitelist()
def validate_fieldname(fieldname):
    """
    Validate if a fieldname is in correct format

    Args:
        fieldname: The fieldname to validate

    Returns:
        dict: Success status and validation result
    """
    # Authentication check
    if frappe.session.user == "Guest":
        frappe.throw(_("Authentication required"), frappe.AuthenticationError)

    try:
        # Check fieldname format
        if not re.match(r'^[a-z_][a-z0-9_]*$', fieldname):
            return {
                "success": False,
                "valid": False,
                "message": "Fieldname must start with a letter or underscore and contain only lowercase letters, numbers, and underscores"
            }

        # Check if fieldname is a reserved keyword
        reserved_keywords = [
            'name', 'owner', 'creation', 'modified', 'modified_by',
            'docstatus', 'idx', 'doctype'
        ]

        if fieldname in reserved_keywords:
            return {
                "success": True,
                "valid": False,
                "message": f"'{fieldname}' is a reserved keyword"
            }

        return {
            "success": True,
            "valid": True,
            "message": "Fieldname is valid"
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Validate Fieldname Error")
        return {
            "success": False,
            "message": "Failed to validate fieldname",
            "error": str(e)
        }


def validate_field(field, idx=None):
    """
    Validate field definition

    Args:
        field: Field dictionary to validate
        idx: Optional index for error messages

    Raises:
        frappe.ValidationError: If validation fails
    """
    field_ref = f" at index {idx}" if idx is not None else ""

    # Check required fields
    required_fields = ['fieldname', 'fieldtype', 'label']
    for req_field in required_fields:
        if not field.get(req_field):
            frappe.throw(
                f"Field '{req_field}' is required{field_ref}",
                frappe.ValidationError
            )

    # Validate fieldname format
    if not re.match(r'^[a-z_][a-z0-9_]*$', field['fieldname']):
        frappe.throw(
            f"Invalid fieldname '{field['fieldname']}'{field_ref}. "
            f"Must start with letter/underscore and contain only lowercase letters, numbers, and underscores",
            frappe.ValidationError
        )

    # Check for reserved keywords
    reserved_keywords = [
        'name', 'owner', 'creation', 'modified', 'modified_by',
        'docstatus', 'idx', 'doctype', 'parent', 'parenttype', 'parentfield'
    ]

    if field['fieldname'] in reserved_keywords:
        frappe.throw(
            f"'{field['fieldname']}' is a reserved keyword{field_ref}",
            frappe.ValidationError
        )

    # Validate options for specific field types
    fields_requiring_options = ['Select', 'Link', 'Table', 'Table MultiSelect', 'Dynamic Link']
    if field['fieldtype'] in fields_requiring_options and not field.get('options'):
        frappe.throw(
            f"Options required for {field['fieldtype']} field '{field['fieldname']}'{field_ref}",
            frappe.ValidationError
        )

    # Validate numeric fields
    if field.get('precision') and field['fieldtype'] not in ['Float', 'Currency', 'Percent']:
        frappe.throw(
            f"Precision is only applicable for Float, Currency, or Percent fields{field_ref}",
            frappe.ValidationError
        )

    # Validate length for applicable fields
    if field.get('length'):
        valid_length_fields = ['Data', 'Small Text', 'Password', 'Barcode']
        if field['fieldtype'] not in valid_length_fields:
            frappe.throw(
                f"Length is only applicable for {', '.join(valid_length_fields)} fields{field_ref}",
                frappe.ValidationError
            )


@frappe.whitelist()
def get_link_options(doctype_filter=None):
    """
    Get list of available doctypes for Link field options

    Args:
        doctype_filter: Optional filter for doctype names

    Returns:
        dict: Success status and list of doctypes
    """
    # Authentication check
    if frappe.session.user == "Guest":
        frappe.throw(_("Authentication required"), frappe.AuthenticationError)

    try:
        query = """
            SELECT name, module, issingle, istable
            FROM `tabDocType`
            WHERE istable = 0
            AND name NOT LIKE 'tmp%'
            ORDER BY name
        """

        doctypes = frappe.db.sql(query, as_dict=True)

        # Apply filter if provided
        if doctype_filter:
            doctypes = [
                dt for dt in doctypes
                if doctype_filter.lower() in dt['name'].lower()
            ]

        return {
            "success": True,
            "doctypes": [dt['name'] for dt in doctypes]
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Link Options Error")
        return {
            "success": False,
            "message": "Failed to retrieve link options",
            "error": str(e)
        }


@frappe.whitelist()
def get_child_table_options():
    """
    Get list of available child doctypes for Table field options

    Returns:
        dict: Success status and list of child doctypes
    """
    # Authentication check
    if frappe.session.user == "Guest":
        frappe.throw(_("Authentication required"), frappe.AuthenticationError)

    try:
        query = """
            SELECT name, module
            FROM `tabDocType`
            WHERE istable = 1
            ORDER BY name
        """

        child_doctypes = frappe.db.sql(query, as_dict=True)

        return {
            "success": True,
            "child_doctypes": [dt['name'] for dt in child_doctypes]
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Get Child Table Options Error")
        return {
            "success": False,
            "message": "Failed to retrieve child table options",
            "error": str(e)
        }
