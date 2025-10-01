import frappe
import json
from frappe.model.db_query import DatabaseQuery

@frappe.whitelist(methods=["GET"])
def get_doctype_list(doctype, fields:str, filters=None, limit_start:int=None, limit_page_length=None):
    # Prevent using '*' in fields
    if doctype and fields == '["*"]':
        frappe.throw("Wildcard '*' is not allowed in fields. Please pass required fields explicitly.")
    # if not limit_page_length:
    #     limit_page_length = 20
    # Parse fields into a list
    meta = frappe.get_meta(doctype)

    # Handle Single DocTypes
    if meta.issingle:
        doc = frappe.get_doc(doctype)
        if fields == fields:
            data = [doc.as_dict()]
        else:
            data = [{field: doc.get(field) for field in fields}]
        return {
            "data": data,
            "total_count": 1,
            "limit_start": 0,
            "limit_page_length": 1
        }
    # Normal DocTypes
    try:
        limit_start = int(limit_start)
    except:
        limit_start = 0

    data = DatabaseQuery(
        doctype).execute(
        fields=fields,
        filters=filters,
        limit_start=limit_start,
        limit_page_length=limit_page_length
    )

    # Get total count of matching records
    total_count = 0
    filters = frappe.parse_json(filters)
    if not filters:
        total_count = frappe.db.count(doctype)
    else:
        total_count = frappe.db.count(doctype,filters)
        
    return {
        "data": data,
        "total_count": total_count,
        "limit_start": limit_start,
        "limit_page_length": limit_page_length
    }