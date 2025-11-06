import frappe
import json
from frappe.model.db_query import DatabaseQuery

@frappe.whitelist(methods=["GET"])
@frappe.read_only()
def get_doctype_list(doctype, fields: str, filters=None, limit_start: int = None, limit_page_length=None, doc_id=None, order_by=None, group_by=None,doctype_name= None):
    # Prevent using '*' in fields
    if not doc_id and fields == '["*"]':
        frappe.throw("Wildcard '*' is not allowed in fields. Please pass required fields explicitly.")

    # Parse fields into a list
    fields = json.loads(fields)

    meta = frappe.get_meta(doctype)

    # Handle Single DocTypes
    if meta.issingle:
        doc = frappe.get_doc(doctype)
        data = [{field: doc.get(field) for field in fields}] if fields else [doc.as_dict()]
        return {
            "data": data,
            "total_count": 1,
            "limit_start": 0,
            "limit_page_length": 1
        }

    # Fetch by doc_id
    if doc_id:
        doc = frappe.get_doc(doctype, doc_id).as_dict()
        return {
            "data": doc,
            "total_count": 1,
            "limit_start": 0,
            "limit_page_length": 1
        }

    # Parse filters safely
    filters = frappe.parse_json(filters) if filters else None

    # Handle pagination
    try:
        limit_start = int(limit_start or 0)
    except Exception:
        limit_start = 0

    # Separate parent vs child fields
    parent_fields = []
    child_fields = []
    for f in fields:
        df = meta.get_field(f)
        if df and df.fieldtype in ["Table", "Table MultiSelect"]:
            child_fields.append(df)
        else:
            parent_fields.append(f)

    # Always include name
    if "name" not in parent_fields:
        parent_fields.append("name")

    # Handle GROUP BY
    group_by_data = None
    if group_by:
        try:
            group_by = group_by.strip()
            query = f"""                
                SELECT {group_by}, COUNT(*) AS count
                FROM `tab{doctype}`
                WHERE doctype_name = '{doctype_name}'
                GROUP BY {group_by}
                ORDER BY count DESC;
            """
            group_by_data = frappe.db.sql(query, as_dict=True)
            return group_by_data
        except Exception as e:
            frappe.log_error(f"Group By Error in {doctype}", str(e))
            group_by_data = []

    # Main data query
    data = DatabaseQuery(doctype).execute(
        fields=parent_fields,
        filters=filters,
        limit_start=limit_start,
        limit_page_length=limit_page_length,
        order_by=order_by or "modified desc"
    )

    # Attach child tables
    if child_fields and data:
        for row in data:
            for df in child_fields:
                row[df.fieldname] = frappe.get_all(
                    df.options,
                    filters={"parent": row["name"], "parentfield": df.fieldname, "parenttype": doctype},
                    fields="*"
                )

    # Count total
    total_count = frappe.db.count(doctype, filters)

    return {
        "data": data,
        "total_count": total_count,
        "limit_start": limit_start,
        "limit_page_length": limit_page_length,
        "group_by_count": group_by_data or []
    }

# import frappe
# import json
# from frappe.model.db_query import DatabaseQuery

# @frappe.whitelist(methods=["GET"])
# def get_doctype_list(doctype, fields: str, filters=None, limit_start: int=None, limit_page_length=None, doc_id=None, order_by=None, group_by=None):
#     """
#     Generic Doctype Data Fetch API with optional GROUP BY and COUNT support
#     """

#     # Parse fields
#     fields = json.loads(fields)
#     if doctype and fields == ['*']:
#         frappe.throw("Wildcard '*' is not allowed. Please specify fields explicitly.")

#     meta = frappe.get_meta(doctype)

#     # Handle Single DocTypes
#     if meta.issingle:
#         doc = frappe.get_doc(doctype)
#         data = [{field: doc.get(field) for field in fields}] if fields else [doc.as_dict()]
#         return {
#             "data": data,
#             "total_count": 1,
#             "limit_start": 0,
#             "limit_page_length": 1
#         }

#     # Fetch specific document by name
#     if doc_id:
#         doc = frappe.get_doc(doctype, doc_id).as_dict()
#         return {
#             "data": doc,
#             "total_count": 1,
#             "limit_start": 0,
#             "limit_page_length": 1
#         }

#     # Parse filters
#     filters = frappe.parse_json(filters) if filters else None
#     try:
#         limit_start = int(limit_start or 0)
#     except Exception:
#         limit_start = 0

#     # Separate parent vs child fields
#     parent_fields, child_fields = [], []
#     for f in fields:
#         df = meta.get_field(f)
#         if df and df.fieldtype in ["Table", "Table MultiSelect"]:
#             child_fields.append(df)
#         else:
#             parent_fields.append(f)

#     # Always include name
#     if "name" not in parent_fields:
#         parent_fields.append("name")

#     # Build the base query
#     query = frappe.qb.from_(f"`tab{doctype}`")

#     # Select fields
#     select_fields = []
#     for field in parent_fields:
#         if field.lower().startswith(("count(", "sum(", "avg(")):
#             # Allow SQL functions like COUNT(field) or SUM(amount)
#             select_fields.append(frappe.qb.Field(field))
#         else:
#             select_fields.append(query.field(field))

#     # Apply filters
#     if filters:
#         for key, value in filters.items():
#             query = query.where(query.field(key) == value)

#     # Apply GROUP BY
#     if group_by:
#         query = query.group_by(query.field(group_by))

#     # Apply ORDER BY
#     if order_by:
#         query = query.orderby(order_by)
#     else:
#         query = query.orderby("modified", order=frappe.qb.desc)

#     # Apply pagination
#     if limit_page_length:
#         query = query.limit(limit_page_length).offset(limit_start)

#     # Execute
#     data = query.select(*select_fields).run(as_dict=True)

#     # Count (if grouped)
#     if group_by:
#         total_count = len(data)
#     else:
#         total_count = frappe.db.count(doctype, filters)

#     # Fetch child tables if applicable
#     if child_fields and data:
#         for row in data:
#             for df in child_fields:
#                 row[df.fieldname] = frappe.get_all(
#                     df.options,
#                     filters={"parent": row["name"], "parentfield": df.fieldname, "parenttype": doctype},
#                     fields="*"
#                 )

#     return {
#         "data": data,
#         "total_count": total_count,
#         "limit_start": limit_start,
#         "limit_page_length": limit_page_length
#     }
