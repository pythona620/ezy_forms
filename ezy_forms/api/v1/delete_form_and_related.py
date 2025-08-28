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
    
    
    try:
        parent_docs = frappe.get_all("WF Setting", fields=["name"])
        for doc_info in parent_docs:
            doc = frappe.get_doc("WF Setting", doc_info.name)
            removed = False
            for row in doc.wf_doctype_and_field:
                if row.workflow_doctype == form_short_name:
                    doc.remove(row)
                    removed = True
            if removed:
                doc.save()
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
        records_in_doctye = frappe.get_all(form_short_name)
        for record in records_in_doctye:
            frappe.delete_doc(form_short_name, record.name)
        frappe.delete_doc("DocType", form_short_name, )
    except frappe.DoesNotExistError:
        pass
    frappe.db.commit()
    return f"Deleted all records and DocType related to: {form_short_name}"
    
    
    
@frappe.whitelist()
def delete_workflow_request(from_date, to_date, form_short_name):
    """
    Delete Workflow Requests, related Activity Logs, 
    and the corresponding document records created between given dates.
    
    """
    
    # Fetch Workflow Request names for the given DocType and date range
    list_workflow_requests = frappe.db.get_all(
        "WF Workflow Requests",
        filters={"doctype_name": form_short_name, "creation": ["Between", from_date, to_date]},
        pluck="name"
    )
    
    # Fetch related Activity Log entries linked to the above Workflow Requests
    list_activity_logs = frappe.db.get_all(
        "WF Activity Log",
        filters={"name": ["in", list_workflow_requests]},
        pluck="name"
    )
    
    # Fetch actual DocType records created in the same date range
    list_docrecords = frappe.db.get_all(
        form_short_name,
        filters={"creation": ["Between", from_date, to_date]},
        pluck="name"
    )

    '''
    
    delete all in one-liners using map + lambda
    
    '''
    # Delete corresponding Activity Logs
    list(map(lambda name: frappe.delete_doc("WF Activity Log", name, force=1), list_activity_logs))
    
    # Delete Workflow Requests
    list(map(lambda name: frappe.delete_doc("WF Workflow Requests", name, force=1), list_workflow_requests))
    
    # Delete actual DocType records
    list(map(lambda name: frappe.delete_doc(form_short_name, name, force=1), list_docrecords))
    
    frappe.db.commit()
    return {"deleted_requests": list_workflow_requests, "deleted_logs": list_activity_logs, "deleted_docs": list_docrecords}