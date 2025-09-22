import frappe
from frappe.core.page.permission_manager.permission_manager import (
    get_standard_permissions, reset, get_permissions
)

@frappe.whitelist()
def assign_custom_permissions(doc, method):
    """Enqueue the assignment of custom permissions when a Role is created."""
    frappe.enqueue(
        "ezy_forms.api.v1.custom_role_permission.assign_custom_permissions_job",
        role_name=doc.name,
        queue="long"
    )
    return f"Permission assignment enqueued for role: {doc.name}"

@frappe.whitelist()
def assign_custom_permissions_job(role_name: str):
    """Assign custom permissions to the given role across selected modules."""

    # Ensure WF Role exists
    if not frappe.db.exists("WF Roles", role_name):
        frappe.get_doc({
            "doctype": "WF Roles",
            "role": role_name
        }).insert(ignore_permissions=True)

    custom_modules = ["Ezy Flow", "Ezy Forms", "Form Templates"]

    frappe.set_user("Administrator")  # ensure admin context

    for module in custom_modules:
        if not frappe.db.exists("Module Def", module):
            continue

        # Get all doctypes in the module
        doctypes = frappe.get_all("DocType", filters={"module": module}, pluck="name")

        for doc_name in doctypes:
            # Skip if permission already exists
            if frappe.db.exists("DocPerm", {"parent": doc_name, "role": role_name}):
                continue

            # Create default permissions
            frappe.get_doc({
                "doctype": "DocPerm",
                "parent": doc_name,
                "parenttype": "DocType",
                "parentfield": "permissions",
                "role": role_name,
                "select": 1,
                "read": 1,
                "write": 1,
                "create": 1,
                "delete": 1,
            }).insert(ignore_permissions=True)

            # Handle permission reset
            try:
                try:
                    get_standard_permissions(doc_name)
                except OSError as e:
                    if "missing" in str(e):
                        frappe.log_error(
                            message=f"Skipped missing JSON for {doc_name}",
                            title="Permission Skip"
                        )
                        continue
                    raise

                reset(doc_name)
                get_permissions(role=role_name, doctype=doc_name)

            except Exception as ex:
                frappe.log_error(
                    message=f"{str(ex)}",
                    title="Permission Creation Error"
                )

    frappe.db.commit()
    return f"Custom permissions assigned to role: {role_name}"
