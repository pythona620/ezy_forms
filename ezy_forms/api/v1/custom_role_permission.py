import frappe
from frappe.permissions import add_permission
from frappe.core.page.permission_manager.permission_manager import get_standard_permissions, reset, get_permissions
@frappe.whitelist()
def assign_custom_permissions(doc, method):
    """
    Enqueue the assignment of custom permissions when a Role is created.
    """
    frappe.enqueue(
        "ezy_forms.api.v1.custom_role_permission.assign_custom_permissions_job",
        role_name=doc.name,
        queue="default"
    )
    return f"Permission assignment enqueued for role: {doc.name}"

@frappe.whitelist()
def assign_custom_permissions_job(role_name):
    if not frappe.db.exists("WF Roles", role_name):
        frappe.get_doc({"doctype": "WF Roles", "role": role_name}).insert(ignore_permissions=True)
        frappe.db.commit()

    custom_modules = ["Ezy Flow", "Ezy Forms", "Form Templates"]

    for module in custom_modules:
        if not frappe.db.exists("Module Def", module):
            continue

        doctypes = frappe.get_all("DocType", filters={"module": module}, pluck="name")

        for doc_name in doctypes:
            existing = frappe.get_all("DocPerm",
                filters={"parent": doc_name, "role": role_name},
                fields=["name"]
            )
            if not existing:
                form_perms = frappe.new_doc("DocPerm")
                form_perms.parent = doc_name
                form_perms.parenttype = "DocType"
                form_perms.parentfield = "permissions"
                form_perms.role = role_name
                form_perms.select = 1
                form_perms.read = 1
                form_perms.write = 1
                form_perms.create = 1
                form_perms.delete = 1
                form_perms.owner = "Administrator"
                form_perms.insert(ignore_permissions=True)
                frappe.db.commit()

            frappe.set_user("Administrator")
            try:
                try:
                    get_standard_permissions(doc_name)
                except OSError as e:
                    if "missing" in str(e):
                        frappe.log_error(message=f"Skipped missing JSON for {doc_name}", title="permission skip")
                    else:
                        raise
                reset(doc_name)
                get_permissions(role=role_name, doctype=doc_name)
            except Exception as ex:
                frappe.log_error(message=f"{str(ex)}", title="permission creation error")


    return f"Custom permissions assigned to role: {role_name}"
