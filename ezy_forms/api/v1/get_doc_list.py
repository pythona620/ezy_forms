import frappe
import json
from frappe.model.db_query import DatabaseQuery

@frappe.whitelist(methods=["GET"])
def get_doctype_list(doctype, fields:str, filters=None, limit_start:int=None, limit_page_length=None, doc_id=None,order_by=None):
    # Prevent using '*' in fields
    
    # if not limit_page_length:
    #     limit_page_length = 20
    # Parse fields into a list
    fields = json.loads(fields)

    meta = frappe.get_meta(doctype)
    # Handle Single DocTypes
    if meta.issingle:
        doc = frappe.get_doc(doctype)
        if fields:
            data = [{field: doc.get(field) for field in fields}]
        else:
            data = [doc.as_dict()]
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
        limit_start = int(limit_start or 0)
    except Exception:
        limit_start = 0

    # Parse filters
    filters = frappe.parse_json(filters) if filters else None

    # Separate parent fields vs child table fields
    parent_fields = []
    child_fields = []
    for f in fields:
        df = meta.get_field(f)
        if df and df.fieldtype in ["Table", "Table MultiSelect"]:
            child_fields.append(df)
        else:
            parent_fields.append(f)

    # Always include name for linking child tables
    if "name" not in parent_fields:
        parent_fields.append("name")

    # Query parent records
    data = DatabaseQuery(doctype).execute(
        fields=parent_fields,
        filters=filters,
        limit_start=limit_start,
        limit_page_length=limit_page_length,
        order_by="modified desc" if not order_by else order_by,
    )

    # Attach child tables
    if child_fields and data:
        for row in data:
            for df in child_fields:
                row[df.fieldname] = frappe.get_all(
                    df.options,  # child doctype
                    filters={"parent": row["name"], "parentfield": df.fieldname, "parenttype": doctype},
                    fields="*"
                )

    # Count total records
    total_count = frappe.db.count(doctype, filters)

    return {
        "data": data,
        "total_count": total_count,
        "limit_start": limit_start,
        "limit_page_length": limit_page_length
    }