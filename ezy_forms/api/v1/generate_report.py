import frappe
from frappe.desk.query_report import run
import re

@frappe.whitelist(methods=["GET"])
def generate_custom_report(doctype_name, source, filters=None):
    """
    Dynamically generates a report based on Ezy Form Definitions configuration.
    Supports parent + child table fields and multiple filters.
    """

    # Case 1: Run normal frappe report
    if source != "ezy_form_definition":
        return run(doctype_name)

    # Case 2: Custom config-based dynamic report
    config = frappe.get_doc("Ezy Form Definitions", doctype_name)
    report_fields = config.report_fields

    if not doctype_name or not report_fields:
        frappe.throw("Please specify both Doctype and Report Fields in the configuration")

    frappe.log_error("Report Field Configuration", report_fields)
    # Parse fields 
    field_mappings = []
    parsed_fields = []
    child_tables = {}  # {alias: child_doctype}
    parent_meta = frappe.get_meta(doctype_name)

    for field_expr in report_fields.split(","):
        field_expr = field_expr.strip()
        if not field_expr:
            continue

        match = re.match(r"([\w\.]+)\s+as\s+['\"]?(.+?)['\"]?$", field_expr, re.IGNORECASE)
        if match:
            fieldname, label = match.groups()
        else:
            fieldname, label = field_expr, frappe.unscrub(field_expr).title()

        # --- Child table field handling ---
        if "." in fieldname:
            parent_field, child_field = fieldname.split(".", 1)
            parent_df = parent_meta.get_field(parent_field)

            if not parent_df:
                frappe.log_error(f"Invalid field '{parent_field}' in {doctype_name}", "Invalid Field")
                continue

            if parent_df.fieldtype != "Table":
                frappe.log_error(f"Field '{parent_field}' exists but is not a Table field (type: {parent_df.fieldtype})", "Invalid Child Table")
                continue

            if parent_field not in child_tables:
                child_tables[parent_field] = parent_df.options

            parsed_fields.append(f"`{parent_field}`.`{child_field}` AS `{fieldname}`")

        else:
            # Skip Table-type fields (cannot be directly queried)
            parent_df = parent_meta.get_field(fieldname)
            if parent_df and parent_df.fieldtype == "Table":
                frappe.log_error(f"Skipping table field '{fieldname}' in {doctype_name} (must specify a child field like '{fieldname}.some_child_field')", "Skipped Field")
                continue

            parsed_fields.append(f"`tab{doctype_name}`.`{fieldname}` AS `{fieldname}`")

        field_mappings.append({"fieldname": fieldname, "label": label})

    if not parsed_fields:
        frappe.throw("No valid fields found to build report. Check report_fields configuration.")

    # -----------------------
    # Build Query
    # -----------------------
    query = f"SELECT {', '.join(parsed_fields)} FROM `tab{doctype_name}`"

    for child_alias, child_doctype in child_tables.items():
        query += f" LEFT JOIN `tab{child_doctype}` AS `{child_alias}` ON `{child_alias}`.parent = `tab{doctype_name}`.name"

    # -----------------------
    # Apply Filters
    # -----------------------
    conditions = []
    values = {}

    if filters:
        if isinstance(filters, str):
            try:
                filters = frappe.parse_json(filters)
            except Exception:
                frappe.throw("Invalid filters format. Must be a valid JSON object.")

        for key, val in filters.items():
            if val in (None, ""):
                continue

            param_key = key.replace('.', '_')
            if "." in key:
                parent_field, child_field = key.split(".", 1)
                field_ref = f"`{parent_field}`.`{child_field}`"
            else:
                field_ref = f"`tab{doctype_name}`.`{key}`"

            if isinstance(val, (list, tuple)) and len(val) == 2:
                op = val[0].upper()
                if op in [">", "<", ">=", "<=", "LIKE"]:
                    conditions.append(f"{field_ref} {op} %({param_key})s")
                    values[param_key] = val[1]
                elif op in ["IN", "NOT IN"]:
                    placeholders = ", ".join([f"%({param_key}_{i})s" for i, _ in enumerate(val[1])])
                    conditions.append(f"{field_ref} {op} ({placeholders})")
                    for i, v in enumerate(val[1]):
                        values[f"{param_key}_{i}"] = v
                else:
                    # Range (between)
                    conditions.append(f"{field_ref} BETWEEN %({param_key}_from)s AND %({param_key}_to)s")
                    values[f"{param_key}_from"], values[f"{param_key}_to"] = val
            else:
                conditions.append(f"{field_ref} = %({param_key})s")
                values[param_key] = val

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    frappe.log_error("Final SQL Query", query)
    frappe.log_error("Query Values", str(values))

    # -----------------------
    # Execute Query
    # -----------------------
    try:
        result = frappe.db.sql(query, values, as_dict=True)
    except Exception as e:
        frappe.log_error(f"SQL Execution Failed\nQuery: {query}\nValues: {values}\nError: {str(e)}", "Custom Report Error")
        frappe.throw("There was an error executing the report. Check Error Logs for details.")

    # -----------------------
    # Build Columns
    # -----------------------
    columns = [
        {"label": f["label"], "fieldname": f["fieldname"], "fieldtype": "Data", "width": 150}
        for f in field_mappings
    ]

    return {
        "columns": columns,
        "result": result,
        "message": None,
        "chart": None,
        "report_summary": None
    }