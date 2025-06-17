import frappe
import pandas as pd
from frappe import _
from frappe.core.doctype.data_import.data_import import start_import, get_import_logs, get_preview_from_template
from frappe.utils.file_manager import get_file

@frappe.whitelist(allow_guest=True)
def import_bulk_data(file: str | None, doctype: str | None):
    try:
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

        # Get the uploaded file
        file_doc = frappe.get_doc("File", {"file_url": file})
        if not file_doc:
            frappe.response["data"] = {"message": _("Invalid file URL"), "success": False}
            return

        # Create Data Import Doc
        data_import_doc = frappe.get_doc({
            "doctype": "Data Import",
            "reference_doctype": doctype,
            "import_type": "Insert New Records",
            "status": "Pending"
        })
        data_import_doc.insert(ignore_permissions=True)
        frappe.db.set_value("Data Import", data_import_doc.name, "import_file", file)
        frappe.db.commit()

        # Get template preview and logs
        try:
            templet = get_preview_from_template(data_import=data_import_doc.name, import_file=file)
            get_logs = get_import_logs(data_import=data_import_doc.name)
        except Exception as e:
            frappe.log_error(f"Preview/Logs error: {str(e)}")
            frappe.response["data"] = {"message": _("Preview/Logs error: ") + str(e), "success": False}
            return

        template_warnings = [warning["message"] for warning in templet.get("warnings", [])]
        log_warnings = get_logs.get("messages", []) if isinstance(get_logs, dict) else []

        # Handle missing Ezy Departments
        missing_departments = []
        created_departments = []

        for warning in template_warnings:
            if "do not exist for Ezy Departments" in warning:
                dept_list = warning.split(":")[1].strip().split(", ")
                missing_departments.extend(dept_list)

        if missing_departments:
            ignored, content = get_file(file_doc.file_url)
            df = pd.read_excel(content, engine="openpyxl")

            for dept_code_raw in missing_departments:
                parts = dept_code_raw.split("-")
                dept_code = f"{parts[0]}-{parts[-1]}" if len(parts) >= 3 else dept_code_raw

                try:
                    row = df[df["Department"] == dept_code_raw].iloc[0]
                    business_unit = row.get("Company Field", "")
                except Exception as e:
                    frappe.log_error(f"Error extracting department from Excel: {e}")
                    continue

                if not frappe.db.exists("Ezy Departments", {"department_code": dept_code}):
                    frappe.get_doc({
                        "doctype": "Ezy Departments",
                        "department_code": dept_code,
                        "department_name": dept_code,
                        "business_unit": business_unit
                    }).insert(ignore_permissions=True)
                    created_departments.append(dept_code_raw)

        # Remove warnings for departments that were created
        cleaned_template_warnings = []
        for warning in template_warnings:
            if "do not exist for Ezy Departments" in warning:
                # Extract dept list and filter out created ones
                dept_part = warning.split(":")[1].strip()
                remaining_depts = [d for d in dept_part.split(", ") if d not in created_departments]
                if remaining_depts:
                    cleaned_template_warnings.append(
                        f"The following values do not exist for Ezy Departments: {', '.join(remaining_depts)}"
                    )
            else:
                cleaned_template_warnings.append(warning)

        # Start import
        try:
            start_import(data_import_doc.name)
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"Import failed: {str(e)}")
            frappe.response["data"] = {
                "message": _("Import failed: ") + str(e),
                "success": False,
                "template_warnings": cleaned_template_warnings,
                "log_warnings": log_warnings,
            }
            return

        # Get import results
        import_status = frappe.db.get_value("Data Import", data_import_doc.name, "status")
        logs = frappe.get_all("Data Import Log",
                              filters={"data_import": data_import_doc.name},
                              fields=["success", "exception", "log_index", "messages", "docname"])

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
            "template_warnings": cleaned_template_warnings,
            "log_warnings": log_warnings,
        }
        frappe.db.commit()

    except Exception as e:
        frappe.log_error(f"Unexpected error: {str(e)}")
        frappe.response["data"] = {"message": _("Unexpected error: ") + str(e), "success": False}
