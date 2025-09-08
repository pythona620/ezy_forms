import frappe
from frappe.permissions import add_permission

def assign_custom_permissions(doc, method):
    """
    Assign CRUD + select permissions for all doctypes inside given modules
    when a new Role is created
    """
    role_name = doc.name

    # ✅ List of modules you want to give permissions for
    custom_modules = ["Urser Forms", "Ezy Flow", "Ezy Forms", "Form Templates"  ]

    # ✅ Permissions to assign
    permissions = ["select", "read", "write", "create", "delete"]

    # ✅ Lambda to apply permissions
    grant_perms = lambda doctype: [add_permission(doctype, role_name, 0, p) for p in permissions]

    for module in custom_modules:
        doctypes = frappe.get_all("DocType", filters={"module": module}, pluck="name")
        [grant_perms(doctype) for doctype in doctypes]

    return (f"Custom permissions assigned to role: {role_name}")
