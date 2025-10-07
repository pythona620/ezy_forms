import frappe
import json

@frappe.whitelist(methods=["GET"])
def get_doctype_list(doctype, fields:str, filters=None, limit_start:int=None, limit_page_length=None, doc_id=None,order_by=None):
    # Prevent using '*' in fields
    
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

    # Fetch by doc_id
    if doc_id:
        doc = frappe.get_doc(doctype, doc_id).as_dict()
        frappe.log_error("doc",doc)
        # data = [doc.as_dict()] if fields == ["*"] else [{field: doc.get(field) for field in fields}]
        # frappe.log_error("data",data)
        return {
            "data": doc,
            "total_count": 1,
            "limit_start": 0,
            "limit_page_length": 1
        }
    if doctype and fields == '["*"]':
        frappe.throw("Wildcard '*' is not allowed in fields. Please pass required fields explicitly.")
    # Normal DocTypes
    try:
        limit_start = int(limit_start)
    except:
        limit_start = 0

    data = frappe.get_all(
        doctype,
        fields=fields,
        filters=filters,
        limit_start=limit_start,
        limit_page_length=limit_page_length,
        order_by="modified desc" if not order_by else order_by,
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