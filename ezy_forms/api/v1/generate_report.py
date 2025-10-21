import frappe
from frappe.desk.query_report import run
import re

@frappe.whitelist(methods=["GET"])
def generate_custom_report(doctype_name, source, filters=None):
    """
    Generates a dynamic report based on Ezy Form Definitions configuration.
    Supports multiple filters, AND/OR groups:
    
    Example for OR groups:
    filters = [
        {"creation": ["2025-10-10", "2025-10-17"], "status": "Active"},  # Group 1
        {"employee_name": ["LIKE", "%John%"]}  # Group 2
    ]
    This translates to: (creation BETWEEN ... AND status='Active') OR (employee_name LIKE '%John%')
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
        match = re.match(r"([\w\.]+)\s+as\s+['\"]?(.+?)['\"]?$", field_expr, re.IGNORECASE)
        if match:
            fieldname, label = match.groups()
            parsed_fields.append(f"{fieldname} as `{fieldname}`")
            field_mappings.append({"fieldname": fieldname, "label": label})
        else:
            fieldname = field_expr
            parsed_fields.append(fieldname)
            field_mappings.append({
                "fieldname": fieldname,
                "label": frappe.unscrub(fieldname).title()
            })

    # Build base query
    query = f"SELECT {', '.join(parsed_fields)} FROM `tab{doctype_name}`"

    # --- 🔹 Filter Handling (OR groups) ---
    or_conditions = []
    values = {}

    if filters:
        if isinstance(filters, str):
            try:
                filters = frappe.parse_json(filters)
            except Exception:
                frappe.throw("Invalid filters format. Must be a JSON object or list of objects.")

        if isinstance(filters, dict):
            filters = [filters]  # Convert single dict to list for uniform processing

        if not isinstance(filters, list):
            frappe.throw("Filters must be a dictionary or a list of dictionaries.")

        for group_index, f_group in enumerate(filters):
            if not isinstance(f_group, dict):
                frappe.throw("Each filter group must be a dictionary.")

            group_conditions = []

            for key, val in f_group.items():
                if val is None or val == "":
                    continue

                param_key = f"{key.replace('.', '_')}_{group_index}"

                # Date range / BETWEEN
                if isinstance(val, (list, tuple)) and len(val) == 2 and all(isinstance(v, str) for v in val):
                    group_conditions.append(f"`{key}` BETWEEN %({param_key}_from)s AND %({param_key}_to)s")
                    values[f"{param_key}_from"] = val[0]
                    values[f"{param_key}_to"] = val[1]

                # Operator-based filter ["<", value] or [">=", value]
                elif isinstance(val, (list, tuple)) and len(val) == 2 and val[0] in [">", "<", ">=", "<="]:
                    operator = val[0]
                    group_conditions.append(f"`{key}` {operator} %({param_key})s")
                    values[param_key] = val[1]

                # LIKE operator
                elif isinstance(val, (list, tuple)) and len(val) == 2 and val[0].upper() == "LIKE":
                    group_conditions.append(f"`{key}` LIKE %({param_key})s")
                    values[param_key] = val[1]

                # IN / NOT IN operator
                elif isinstance(val, (list, tuple)) and len(val) == 2 and val[0].upper() in ["IN", "NOT IN"]:
                    operator = val[0].upper()
                    in_values = val[1]
                    if not isinstance(in_values, (list, tuple)):
                        frappe.throw(f"Values for {operator} filter on {key} must be a list or tuple.")
                    placeholders = ", ".join([f"%({param_key}_{i})s" for i in range(len(in_values))])
                    group_conditions.append(f"`{key}` {operator} ({placeholders})")
                    for i, v in enumerate(in_values):
                        values[f"{param_key}_{i}"] = v

                # Simple equality
                elif not isinstance(val, (list, tuple)):
                    group_conditions.append(f"`{key}` = %({param_key})s")
                    values[param_key] = val

            if group_conditions:
                or_conditions.append("(" + " AND ".join(group_conditions) + ")")

    # Add WHERE clause if OR conditions exist
    if or_conditions:
        query += " WHERE " + " OR ".join(or_conditions)

    # Execute query safely
    result = frappe.db.sql(query, values, as_dict=True)

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
        "result": result,
        "message": None,
        "chart": None,
        "report_summary": None
    }