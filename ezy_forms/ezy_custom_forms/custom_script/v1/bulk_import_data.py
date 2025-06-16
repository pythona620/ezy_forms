import frappe
from frappe import _
from frappe.core.doctype.data_import.data_import import start_import, get_import_logs, get_preview_from_template

@frappe.whitelist(allow_guest=True)
def import_bulk_data(file: str | None, doctype: str | None):
    try:
        # Check permissions
        if not any(frappe.has_permission(doctype, ptype=pt, user=frappe.session.user) for pt in ["create", "import", "write"]):
            frappe.response["data"] = {
                "message": _("Employee Has No Permission To Perform This Action"),
                "success": False
            }
            return

        # Validate inputs
        if not file:
            frappe.response["data"] = {
                "message": _("Please select a file to import"),
                "success": False
            }
            return

        if not doctype:
            frappe.response["data"] = {
                "message": _("Please select a doctype to import"),
                "success": False
            }
            return

        # Check if import allowed
        allow_data_import = frappe.get_value("DocType", doctype, "allow_import")
        if not allow_data_import:
            frappe.response["data"] = {
                "message": _("Importing data for this doctype is not allowed"),
                "success": False
            }
            return

        # Get file
        file_doc = frappe.get_doc("File", {"file_url": file})
        if not file_doc:
            frappe.response["data"] = {
                "message": _("Invalid file URL"),
                "success": False
            }
            return

        # Create Data Import doc
        data_import_doc = frappe.get_doc({
            "doctype": "Data Import",
            "reference_doctype": doctype,
            "import_type": "Insert New Records",
            "status": "Pending"
        })
        data_import_doc.insert(ignore_permissions=True)

        # Set import file
        frappe.db.set_value("Data Import", data_import_doc.name, "import_file", file)
        frappe.db.commit()

        # Preview & logs
        try:
            templet = get_preview_from_template(data_import=data_import_doc.name, import_file=file)
            get_logs = get_import_logs(data_import=data_import_doc.name)
        except Exception as e:
            frappe.log_error(f"Preview/Logs error: {str(e)}")
            frappe.response["data"] = {
                "message": _("Preview/Logs error: ") + str(e),
                "success": False
            }
            return

        # Extract warnings
        template_warnings = [warning["message"] for warning in templet.get("warnings", [])]
        log_warnings = get_logs.get("messages", []) if isinstance(get_logs, dict) else []

        # Handle missing WF Roles
        if template_warnings or log_warnings:
            created_roles = []
            for warning in template_warnings:
                if "do not exist for WF Roles" in warning:
                    missing_roles = warning.split(":")[1].strip().split(", ")
                    for role in missing_roles:
                        # Create Role
                        if not frappe.db.exists("Role", role):
                            frappe.get_doc({"doctype": "Role", "role_name": role}).insert(ignore_permissions=True)
                            created_roles.append(f"Role: {role}")

                        # Create WF Role
                        if not frappe.db.exists("WF Roles", {"role": role}):
                            frappe.get_doc({"doctype": "WF Roles", "role": role}).insert(ignore_permissions=True)
                            created_roles.append(f"WF Role: {role}")

            frappe.response["data"] = {
                "message": _("Missing WF Roles were created. Please retry the import."),
                "success": False,
                "template_status": "fixed",
                "template_warnings": template_warnings,
                "log_warnings": log_warnings,
                "created_records": created_roles
            }
            return

        # Start import
        try:
            start_import(data_import_doc.name)
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"Import failed: {str(e)}")
            frappe.response["data"] = {
                "message": _("Import failed: ") + str(e),
                "success": False
            }
            return

        # Import status & logs
        import_status = frappe.db.get_value("Data Import", data_import_doc.name, "status")
        logs = frappe.get_all("Data Import Log",
                              filters={"data_import": data_import_doc.name},
                              fields=["success", "exception", "log_index", "messages", "docname"])

        records = [
            {"row": log["log_index"] + 1, "status": "success", "message": f"successfully imported {log['docname']}"}
            if log["success"] else
            {"row": log["log_index"] + 1, "status": "Failed", "message": log["messages"]}
            for log in logs
        ]

        frappe.response["data"] = {
            "message": _("Import Completed successfully"),
            "success": True,
            "status": import_status.lower(),
            "records": records,
            "No of Imported Records": sum(1 for log in logs if log["success"]),
            "No of Failed Records": sum(1 for log in logs if not log["success"]),
            "template_status": "success"
        }

    except Exception as e:
        frappe.log_error(f"Unexpected error: {str(e)}")
        frappe.response["data"] = {
            "message": _("Unexpected error: ") + str(e),
            "success": False
        }
