 
import frappe
from frappe import _
from frappe.core.doctype.data_import.data_import import start_import, get_import_logs, get_preview_from_template

@frappe.whitelist(allow_guest=True)
def import_bulk_data(file:str|None, doctype:str|None):
    if not file:
        return {"success": False, "message": _("Please select a file to import")}
    if not doctype:
        return {"success": False, "message": _("Please select a doctype to import")}
 
    allow_data_import = frappe.get_value("DocType", doctype, "allow_import")
    if not allow_data_import or allow_data_import == "0":
        return {"success": False, "message": _("Importing data for this doctype is not allowed")}
 
 
    try:
        file_doc = frappe.get_doc("File", {"file_url": file})
        if not file_doc:
            return {"success": False, "message": _("Invalid file URL")}
 
        file_path = file_doc.get_full_path()
 
        data_import_doc = frappe.get_doc({
            "doctype": "Data Import",
            "reference_doctype": doctype,
            "import_type": "Insert New Records",
            "status": "Pending"
        })
        data_import_doc.insert(ignore_permissions=True)
 
        frappe.db.set_value("Data Import", data_import_doc.name, "import_file", file)
        frappe.db.commit()
 
        try:
            templet = get_preview_from_template(data_import=data_import_doc.name, import_file=file)
            get_logs = get_import_logs(data_import=data_import_doc.name)
        except Exception as e:
            error_message = f"Preview/Logs error: {str(e)}"
            frappe.log_error(error_message)
            return {"success": False, "message": _(error_message)}
 
        # Extract warnings from `templet`
        template_warnings = [warning["message"] for warning in templet.get("warnings", [])]
 
        # Extract warnings from `get_logs`
        log_warnings = []
        if isinstance(get_logs, dict) and "messages" in get_logs:
            log_warnings = get_logs["messages"]
 
        # If warnings exist, return them without proceeding to import
        if template_warnings or log_warnings:
            return {
                "success": False,
                "message": "Warnings detected in import template and logs.",
                "template_warnings": template_warnings,
                "log_warnings": log_warnings,
                "template_status":"failed"
            }
 
        try:
            
            start_import(data_import_doc.name)
            frappe.db.commit()  # Ensure database updates before checking logs
        except Exception as e:
            error_message = f"Import failed: {str(e)}"
            frappe.log_error(error_message)
            return {"success": False, "message": _(error_message)}
 
        # Commit changes and fetch the updated status
        frappe.db.commit()
        import_status = frappe.db.get_value("Data Import", data_import_doc.name, "status")
 
        # Fetch logs again to check success/failure
        logs = frappe.get_all("Data Import Log",
                              filters={"data_import": data_import_doc.name},
                              fields=["success", "exception", "log_index", "messages", "docname"])
 
        records = [
            {"row": log["log_index"] + 1, "status": "Success", "message": f"Successfully imported {log['docname']}"}
            if log["success"] else
            {"row": log["log_index"] + 1, "status": "Failed", "message": log["messages"]}
            for log in logs
        ]
 
        return {
            "success": any(log["success"] for log in logs),
            "status": import_status,
            "records": records,
            "No of Imported Records": sum(1 for log in logs if log["success"]),
            "No of Failed Records": sum(1 for log in logs if not log["success"]),
            "template_status":"success"
        }
 
    except Exception as e:
        error_message = f"Unexpected error: {str(e)}"
        frappe.log_error(error_message)
        return {"success": False, "message": _(error_message)}
 
 