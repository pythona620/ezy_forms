 
import frappe
from frappe import _
from frappe.core.doctype.data_import.data_import import start_import, get_import_logs, get_preview_from_template

@frappe.whitelist(allow_guest=True)
def import_bulk_data(file: str | None, doctype: str | None):
    try:
        # Check if the user has permission to create the specified doctype
        if not any(frappe.has_permission(doctype, ptype=pt, user=frappe.session.user) for pt in ["create", "import", "write"]):

            frappe.response["data"] = {
                "message": _("Employee Has No Permission To Perform This Action"),

                "success":False
            }
            return
        
        # Validate file and doctype inputs
        if not file:
            frappe.response["data"] = {
                "message": _("Please select a file to import"),

                "success":False
            }
            return
        if not doctype:
            frappe.response["data"] = {
                "message": _("Please select a doctype to import"),

                "success":False
            }
            return	

        # Check if data import is allowed for the specified doctype
        allow_data_import = frappe.get_value("DocType", doctype, "allow_import")
        if not allow_data_import or allow_data_import ==  0 :
            frappe.response["data"] = {
                "message": _("Importing data for this doctype is not allowed"),

                "success":False
            }
            return

        # Get the file document from the database
        file_doc = frappe.get_doc("File", {"file_url": file})
        if not file_doc:
            frappe.response["data"] = {
                "message": _("Invalid file URL"),

                "success":False
            }
            return

        # Create a new data import document
        data_import_doc = frappe.get_doc({
            "doctype": "Data Import",
            "reference_doctype": doctype,
            "import_type": "Insert New Records",
            "status": "Pending"
        })
        data_import_doc.insert(ignore_permissions=True)

        # Set the import file for the data import document
        frappe.db.set_value("Data Import", data_import_doc.name, "import_file", file)
        frappe.db.commit()

        try:
            # Get the preview and logs for the data import
            templet = get_preview_from_template(data_import=data_import_doc.name, import_file=file)
            get_logs = get_import_logs(data_import=data_import_doc.name)
        except Exception as e:
            frappe.log_error(f"Preview/Logs error: {str(e)}")
            frappe.response["data"] = {
                "message": _("Preview/Logs error: ") + str(e),

                "success":False
            }
            return

        # Extract warnings from the preview and logs
        template_warnings = [warning["message"] for warning in templet.get("warnings", [])]
        log_warnings = get_logs.get("messages", []) if isinstance(get_logs, dict) else []

        if template_warnings or log_warnings:
            frappe.response["data"] = {
                "message": "Warnings detected in import template and logs.",

                "success":False,
                "template_warnings": template_warnings,
                "log_warnings": log_warnings,
                "template_status": "failed"
            }
            return

        # Start the data import process
        try:
            start_import(data_import_doc.name)
            frappe.db.commit()
        except Exception as e:
            frappe.log_error(f"Import failed: {str(e)}")
            frappe.response["data"] = {
                "message": _("Import failed: ") + str(e),

                "success":False
            }
            return

        # Fetch import status
        import_status = frappe.db.get_value("Data Import", data_import_doc.name, "status")

        # Fetch logs again to check success/failure
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
            "success":True,
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
            "success":False
        }