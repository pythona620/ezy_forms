import io
import frappe
import pandas as pd
from frappe import _
from frappe.core.doctype.data_import.data_import import start_import, get_import_logs, get_preview_from_template,form_start_import
from frappe.utils.file_manager import save_file

@frappe.whitelist()
def import_bulk_data(file: str | None, doctype: str | None):
    """
    Import bulk data from Excel file.
    Requires authentication and appropriate permissions.
    """
    try:
        # Ensure user is authenticated
        if frappe.session.user == "Guest":
            frappe.throw(_("Authentication required for data import"), frappe.AuthenticationError)

        # Permission checks
        if not any(frappe.has_permission(doctype, ptype=pt, user=frappe.session.user) for pt in ["create", "import", "write"]):
            frappe.response["data"] = {"message": _("You do not have permission to perform this action"), "success": False}
            return

        if not file:
            frappe.response["data"] = {"message": _("Please select a file to import"), "success": False}
            return

        if not doctype:
            frappe.response["data"] = {"message": _("Please select a doctype to import"), "success": False}
            return

        allow_data_import = frappe.get_value("DocType", doctype, "allow_import")
        if not allow_data_import:
            frappe.response["data"] = {"message": _("Importing data for this doctype is not allowed"), "success": False}
            return

        # Locate uploaded file
        file_doc = frappe.get_doc("File", {"file_url": file})
        if not file_doc:
            frappe.response["data"] = {"message": _("Invalid file URL"), "success": False}
            return

        # Create Data Import doc
        data_import_doc = frappe.get_doc({
            "doctype": "Data Import",
            "reference_doctype": doctype,
            "import_type": "Insert New Records",
            "import_file": file_doc.file_url,
            "status": "Pending"
        })
        data_import_doc.insert(ignore_permissions=True)
        frappe.db.commit()
        # Preview & logs
        try:
            templet = get_preview_from_template(data_import=data_import_doc.name, import_file=file)
            get_logs = get_import_logs(data_import=data_import_doc.name)
        except Exception as e:
            frappe.response["data"] = {"message": _("Preview/Logs error: ") + str(e), "success": False}
            return

        template_warnings = [w["message"] for w in templet.get("warnings", [])]
        log_warnings = get_logs.get("messages", []) if isinstance(get_logs, dict) else []

        # ----- Read Excel with pandas -----
        try:
            df = pd.read_excel(file_doc.get_full_path(), engine="openpyxl")
        except Exception as e:
            frappe.response["data"] = {"message": _("Error reading Excel file: ") + str(e), "success": False}
            return

        # ----- Normalize Department using Company ONLY for Ezy Employee -----
        if doctype == "Ezy Employee":
            column_map = {
                "department code": "Department",
                # You can add more mappings here if needed
            }

            # Lowercase the Excel columns for matching
            df_columns_lower = {c.lower(): c for c in df.columns}
            rename_map = {df_columns_lower[k]: v for k, v in column_map.items() if k in df_columns_lower}
            df.rename(columns=rename_map, inplace=True)
            cols_lower = {c.lower().strip(): c for c in df.columns}

            company_col, department_col = None, None

            for key in ("company", "company name", "company_field", "company field"):
                if key in cols_lower:
                    company_col = cols_lower[key]
                    break

            for key in ("department", "dept", "department name"):
                if key in cols_lower:
                    department_col = cols_lower[key]
                    break

            if company_col and department_col:
                def fix_department(row):
                    comp = str(row[company_col]).strip() if pd.notna(row[company_col]) else ""
                    dept = str(row[department_col]).strip() if pd.notna(row[department_col]) else ""
                    if not dept:
                        return dept
                    if comp and not dept.startswith(f"{comp}-"):
                        return f"{comp}-{dept}"
                    return dept

                df[department_col] = df.apply(fix_department, axis=1)

        # ----- Save modified Excel and set it on Data Import -----
        try:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
                df.to_excel(writer, index=False)
            buffer.seek(0)

            new_filename = f"normalized_{file_doc.file_name or 'import.xlsx'}"
            saved = save_file(
                new_filename,
                buffer.getvalue(),
                "Data Import",
                data_import_doc.name,
                is_private=0
            )
            frappe.db.set_value("Data Import", data_import_doc.name, "import_file", saved.file_url)
            frappe.db.set_value("Data Import", data_import_doc.name, "status", "Pending")
            start_import(data_import_doc.name)
            frappe.db.commit()
        except Exception as e:
            frappe.response["data"] = {"message": _("Failed to save normalized file: ") + str(e), "success": False}
            return
        template_warnings = [
    w["message"] for w in templet.get("warnings", [])
    if "Department Code" not in w.get("message", "")
]
        # ----- Run import -----
        try:
            start_import(data_import_doc.name)
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"Import failed: {str(e)}")
            frappe.response["data"] = {
                "message": _("Import failed: ") + str(e),
                "success": False,
                "template_warnings": template_warnings,
                "log_warnings": log_warnings,
            }
            return

        # ----- Collect results -----
        import_status = frappe.db.get_value("Data Import", data_import_doc.name, "status")
        logs = frappe.get_all(
            "Data Import Log",
            filters={"data_import": data_import_doc.name},
            fields=["success", "exception", "log_index", "messages", "docname"]
        )

        records = [
            {"row": log["log_index"] + 1, "status": "success", "message": f"Successfully imported {log['docname']}"}
            if log["success"] else
            {"row": log["log_index"] + 1, "status": "Failed", "message": log["messages"]}
            for log in logs
        ]

        frappe.response["data"] = {
            "message": _("Import completed") if import_status == "Success" else _("Import finished with issues"),
            "success": import_status == "Success",
            "status": import_status.lower(),
            "records": records,
            "No of Imported Records": sum(1 for log in logs if log["success"]),
            "No of Failed Records": sum(1 for log in logs if not log["success"]),
            "template_status": "success" if import_status == "Success" else "partial",
            "template_warnings": template_warnings,
            "log_warnings": log_warnings,
        }
        frappe.db.commit()

    except Exception as e:
        frappe.log_error(f"Unexpected error: {str(e)}")
        frappe.response["data"] = {"message": _("Unexpected error: ") + str(e), "success": False}
