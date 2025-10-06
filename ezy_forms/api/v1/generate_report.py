import frappe
from frappe.desk.query_report import run
import re

@frappe.whitelist(allow_guest=True)
def generate_custom_report(doctype_name, source):
    """
    Generates a report dynamically based on report_fields in a given custom config DocType.
    Returns response in same format as frappe's query report output,
    keeping result keys as fieldnames (not aliases).
    """

    # Case 1: Run normal frappe report
    if source != "ezy_form_definition":
        return run(doctype_name)

    # Case 2: Custom config-based dynamic report
    config = frappe.get_doc("Ezy Form Definitions", doctype_name)
    report_fields = config.report_fields

    if not doctype_name or not report_fields:
        frappe.throw("Please specify both Doctype and Report Fields in the configuration")

    # Parse fields to map aliases
    field_mappings = []
    parsed_fields = []
    for field_expr in report_fields.split(","):
        field_expr = field_expr.strip()

        # Match: fieldname AS 'Label'
        match = re.match(r"([\w\.]+)\s+as\s+['\"]?(.+?)['\"]?$", field_expr, re.IGNORECASE)
        if match:
            fieldname, label = match.groups()
            parsed_fields.append(f"{fieldname} as `{fieldname}`")  # keep key consistent
            field_mappings.append({"fieldname": fieldname, "label": label})
        else:
            fieldname = field_expr
            parsed_fields.append(fieldname)
            field_mappings.append({"fieldname": fieldname, "label": frappe.unscrub(fieldname).title()})

    # Build query with corrected aliases
    query = f"SELECT {', '.join(parsed_fields)} FROM `tab{doctype_name}`"

    # Execute query
    result = frappe.db.sql(query, as_dict=True)

    # Prepare columns
    columns = []
    for f in field_mappings:
        columns.append({
            "label": f["label"],
            "fieldname": f["fieldname"],
            "fieldtype": "Data",
            "width": 150
        })

    return {
        "columns": columns,
        "result": result,  # keys will now be fieldnames
        "message": None,
        "chart": None,
        "report_summary": None
    }
