"""
Insights Forms API
Provides form listing, field metadata, and record retrieval for insights
"""

import frappe
from frappe import _
from frappe.model import get_meta
import json


@frappe.whitelist()
def get_forms_list():
    """
    Get list of all forms with metadata and record counts

    Returns:
        dict: List of forms with counts and metadata
    """
    try:
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        # Get all forms from workflow requests
        query = """
            SELECT
                wfr.doctype_name as form_name,
                COUNT(DISTINCT wfr.name) as total_records,
                MIN(wfr.requested_on) as first_submission,
                MAX(wfr.requested_on) as last_submission,
                COUNT(DISTINCT CASE WHEN wfr.status = 'Completed' THEN wfr.name END) as completed_count,
                COUNT(DISTINCT CASE WHEN wfr.status IN ('Request Raised', 'Request Raised Via QR Code') THEN wfr.name END) as pending_count
            FROM `tabWF Workflow Requests` wfr
            WHERE wfr.docstatus != 2
            GROUP BY wfr.doctype_name
            ORDER BY total_records DESC
        """

        forms = frappe.db.sql(query, as_dict=True)

        # Enrich with DocType metadata
        enriched_forms = []
        for form in forms:
            try:
                meta = get_meta(form.form_name)
                enriched_forms.append({
                    "form_name": form.form_name,
                    "total_records": form.total_records,
                    "completed_count": form.completed_count,
                    "pending_count": form.pending_count,
                    "first_submission": form.first_submission,
                    "last_submission": form.last_submission,
                    "module": meta.module if hasattr(meta, 'module') else None,
                    "is_submittable": meta.is_submittable if hasattr(meta, 'is_submittable') else 0
                })
            except Exception as e:
                # Skip forms that don't exist or have errors
                frappe.log_error(f"Error getting metadata for {form.form_name}: {str(e)}")
                continue

        return {
            "success": True,
            "data": enriched_forms
        }

    except Exception as e:
        frappe.log_error(f"Error in get_forms_list: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_form_fields(form_name):
    """
    Get all fields for a specific form with their metadata

    Args:
        form_name: Name of the DocType/Form

    Returns:
        dict: List of fields with types and options
    """
    try:
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        meta = get_meta(form_name)

        fields = []
        for field in meta.fields:
            # Skip internal/system fields
            if field.fieldtype in ['Section Break', 'Column Break', 'Tab Break', 'HTML', 'Button']:
                continue

            field_info = {
                "fieldname": field.fieldname,
                "label": field.label or field.fieldname,
                "fieldtype": field.fieldtype,
                "options": field.options if hasattr(field, 'options') else None,
                "reqd": field.reqd if hasattr(field, 'reqd') else 0,
                "in_list_view": field.in_list_view if hasattr(field, 'in_list_view') else 0,
                "in_filter": field.in_filter if hasattr(field, 'in_filter') else 0,
                "is_numeric": field.fieldtype in ['Int', 'Float', 'Currency', 'Percent'],
                "is_date": field.fieldtype in ['Date', 'Datetime', 'Time'],
                "is_select": field.fieldtype in ['Select', 'Link'],
                "is_aggregatable": field.fieldtype in ['Int', 'Float', 'Currency', 'Percent', 'Check']
            }

            fields.append(field_info)

        # Add standard fields
        standard_fields = [
            {"fieldname": "name", "label": "ID", "fieldtype": "Data", "is_numeric": False, "is_aggregatable": False},
            {"fieldname": "owner", "label": "Created By", "fieldtype": "Link", "options": "User", "is_select": True},
            {"fieldname": "creation", "label": "Created On", "fieldtype": "Datetime", "is_date": True},
            {"fieldname": "modified", "label": "Modified On", "fieldtype": "Datetime", "is_date": True},
            {"fieldname": "modified_by", "label": "Modified By", "fieldtype": "Link", "options": "User", "is_select": True}
        ]

        fields.extend(standard_fields)

        return {
            "success": True,
            "data": {
                "form_name": form_name,
                "fields": fields
            }
        }

    except Exception as e:
        frappe.log_error(f"Error in get_form_fields: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_form_records(form_name, page=1, page_size=20, filters=None, search=None, sort_by=None, sort_order="desc"):
    """
    Get paginated records for a form with filtering and search

    Args:
        form_name: Name of the DocType/Form
        page: Page number (1-indexed)
        page_size: Records per page
        filters: JSON string of filters
        search: Search query
        sort_by: Field to sort by
        sort_order: asc or desc

    Returns:
        dict: Paginated records with metadata
    """
    try:
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        # Parse filters
        filter_dict = {}
        if filters:
            try:
                filter_dict = json.loads(filters) if isinstance(filters, str) else filters
            except json.JSONDecodeError:
                pass

        # Get records from workflow requests
        page = int(page)
        page_size = int(page_size)
        offset = (page - 1) * page_size

        # Build query conditions
        conditions = ["wfr.docstatus != 2"]
        values = {"form_name": form_name}

        # Add form name filter
        conditions.append("wfr.doctype_name = %(form_name)s")

        # Add custom filters
        if filter_dict:
            for field, value in filter_dict.items():
                if value:
                    conditions.append(f"wfr.{field} = %({field})s")
                    values[field] = value

        # Add search
        if search:
            conditions.append("(wfr.name LIKE %(search)s OR wfr.requested_by LIKE %(search)s)")
            values["search"] = f"%{search}%"

        where_clause = " AND ".join(conditions)

        # Determine sort
        if not sort_by:
            sort_by = "requested_on"
        order_clause = f"wfr.{sort_by} {sort_order.upper()}"

        # Get total count
        count_query = f"""
            SELECT COUNT(*) as total
            FROM `tabWF Workflow Requests` wfr
            LEFT JOIN `tabEzy Employee` emp ON wfr.requested_by = emp.emp_mail_id
            WHERE {where_clause}
        """

        total_result = frappe.db.sql(count_query, values=values, as_dict=True)
        total_records = total_result[0].total if total_result else 0

        # Get paginated records
        query = f"""
            SELECT
                wfr.name,
                wfr.doctype_name,
                wfr.requested_by,
                wfr.requested_on,
                wfr.status,
                wfr.property,
                wfr.modified,
                wfr.modified_by,
                emp.emp_name as requestor_name,
                dept.department_name as department
            FROM `tabWF Workflow Requests` wfr
            LEFT JOIN `tabEzy Employee` emp ON wfr.requested_by = emp.emp_mail_id
            LEFT JOIN `tabEzy Departments` dept ON emp.department = dept.name
            WHERE {where_clause}
            ORDER BY {order_clause}
            LIMIT {page_size} OFFSET {offset}
        """

        records = frappe.db.sql(query, values=values, as_dict=True)

        total_pages = (total_records + page_size - 1) // page_size

        return {
            "success": True,
            "data": {
                "records": records,
                "pagination": {
                    "page": page,
                    "page_size": page_size,
                    "total_records": total_records,
                    "total_pages": total_pages,
                    "has_next": page < total_pages,
                    "has_prev": page > 1
                }
            }
        }

    except Exception as e:
        frappe.log_error(f"Error in get_form_records: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_field_values(form_name, field_name, search=None, limit=50):
    """
    Get unique values for a field (for filter dropdowns)

    Args:
        form_name: Name of the DocType/Form
        field_name: Field to get values for
        search: Optional search filter
        limit: Maximum values to return

    Returns:
        dict: List of unique values
    """
    try:
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        # Validate field exists
        meta = get_meta(form_name)
        field = meta.get_field(field_name)

        if not field:
            # Check if it's a standard field
            if field_name not in ['name', 'owner', 'creation', 'modified', 'modified_by']:
                frappe.throw(f"Field {field_name} not found in {form_name}")

        # Build query based on field type
        if field and field.fieldtype == 'Link' and field.options:
            # Get values from linked doctype
            search_condition = ""
            if search:
                search_condition = f"WHERE name LIKE %(search)s"

            query = f"""
                SELECT DISTINCT name as value, name as label
                FROM `tab{field.options}`
                {search_condition}
                ORDER BY name
                LIMIT {int(limit)}
            """
            values = {"search": f"%{search}%"} if search else {}
        else:
            # Get values from workflow requests
            search_condition = ""
            if search:
                search_condition = f"AND wfr.{field_name} LIKE %(search)s"

            query = f"""
                SELECT DISTINCT wfr.{field_name} as value, wfr.{field_name} as label
                FROM `tabWF Workflow Requests` wfr
                WHERE wfr.doctype_name = %(form_name)s
                  AND wfr.{field_name} IS NOT NULL
                  {search_condition}
                ORDER BY wfr.{field_name}
                LIMIT {int(limit)}
            """
            values = {"form_name": form_name}
            if search:
                values["search"] = f"%{search}%"

        results = frappe.db.sql(query, values=values, as_dict=True)

        return {
            "success": True,
            "data": results
        }

    except Exception as e:
        frappe.log_error(f"Error in get_field_values: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }
