import frappe

@frappe.whitelist()
def delete_form_and_related(form_short_name=None):

    # Delete Ezy Form Definition
    try:    
        ezy_form_definition = frappe.get_doc("Ezy Form Definitions", {"form_short_name": form_short_name})
        activate_log = frappe.get_doc("WF Activity Log",ezy_form_definition.name)
        frappe.delete_doc("WF Activity Log",activate_log.name, force=1)
        ezy_form_definition.delete()
        frappe.db.commit()
    except frappe.DoesNotExistError:
        pass

    # Delete WF Roadmap
    try:
        wf_roadmap = frappe.get_doc("WF Roadmap", {"document_type": form_short_name})
        wf_roadmap.delete()
    except frappe.DoesNotExistError:
        pass

    # Delete all WF Workflow Requests
    wf_workflow_requests = frappe.get_all("WF Workflow Requests", filters={"doctype_name": form_short_name})
    for req in wf_workflow_requests:
        frappe.delete_doc("WF Workflow Requests", req.name, force=1)

    # Delete the DocType
    try:
        frappe.delete_doc("DocType", form_short_name, force=1)
    except frappe.DoesNotExistError:
        pass
    frappe.db.commit()
    return f"Deleted all records and DocType related to: {form_short_name}"
    