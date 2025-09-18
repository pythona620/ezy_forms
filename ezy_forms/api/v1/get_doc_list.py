import frappe
import json

@frappe.whitelist()
def get_doctype_list(doctype, fields:list, filters:dict=None, limit_start:int=None, limit_page_length:int=None):
    # Prevent using '*' in fields
    if fields == ["*"]:
        frappe.throw("Wildcard '*' is not allowed in fields. Please pass required fields explicitly.")
    if not limit_page_length:
        limit_page_length = 20
    # Parse fields into a list
    if isinstance(fields, str):
        try:
            fields = json.loads(fields)
        except Exception:
            fields = [f.strip() for f in fields.split(',')]

    if not fields or not isinstance(fields, list):
        frappe.throw("Fields parameter must be a non-empty list of field names.")

    # Parse filters into Python object
    parsed_filters = {}
    if filters:
        try:
            parsed_filters = json.loads(filters)
        except Exception as e:
            frappe.throw(f"Invalid filters format: {str(e)}")

    # Ensure pagination parameters are integers
    try:
        limit_start = int(limit_start)
    except:
        limit_start = 0

    try:
        limit_page_length = int(limit_page_length)
    except:
        limit_page_length = 20

    # Fetch data with pagination
    data = frappe.get_all(
        doctype,
        fields=fields,
        filters=parsed_filters,
        limit_start=limit_start,
        limit_page_length=limit_page_length 
    )

    # Get total count of matching records
    total_count = frappe.db.count(doctype, parsed_filters)

    return {
        "data": data,
        "total_count": total_count,
        "limit_start": limit_start,
        "limit_page_length": limit_page_length
    }