import frappe
from frappe.permissions import add_permission

def assign_custom_permissions(doc, method):
    """
    Enqueue the assignment of custom permissions when a Role is created
    """
    frappe.enqueue(
        "ezy_forms.api.v1.custom_role_permission.assign_custom_permissions_job",
        role_name=doc.name,
        queue="default"
    )
    return f"Permission assignment enqueued for role: {doc.name}"


@frappe.whitelist()
def assign_custom_permissions_job(role_name):
    
    """
    Actual job that assigns CRUD + select permissions for all doctypes in custom modules
    """
    if not frappe.db.exists("WF Roles",role_name):
        frappe.get_doc({ "doctype": "WF Roles",  "role": role_name}).insert(ignore_permissions=True)
        frappe.db.commit()
        
    custom_modules = ["Urser Forms", "Ezy Flow", "Ezy Forms", "Form Templates"]
    permissions = ["select", "read", "write", "create", "delete"]

    grant_perms = lambda doctype: [add_permission(doctype, role_name, 0, p) for p in permissions]

    for module in custom_modules:
        doctypes = frappe.get_all("DocType", filters={"module": module}, pluck="name")
        [grant_perms(doctype) for doctype in doctypes]

    frappe.db.commit()
    return f"Custom permissions assigned to role: {role_name}"
