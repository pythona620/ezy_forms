import frappe
import json

@frappe.whitelist()
def get_doctype_list(doctype, fields, filters=None, length=20):
    # Parse fields into a Python list
    if isinstance(fields, str):
        try:
            fields = json.loads(fields)
        except Exception:
            fields = [f.strip() for f in fields.split(',')]

    # Convert filters to Python list
    parsed_filters = {}
    if filters:
        try:
            parsed_filters = json.loads(filters)
        except Exception as e:
            frappe.throw(f"Invalid filters format: {str(e)}")

    try:
        length = int(length)
    except:
        length = 20

    # Correct usage: fields must be a list
    data = frappe.get_all(
        doctype,
        fields=fields,
        filters=parsed_filters,
        limit_page_length=length
    )

    total_count = frappe.db.count(doctype, parsed_filters)

    return {
        "data": data,
        "total_count": total_count
    }
