import frappe
from frappe.core.page.permission_manager.permission_manager import (
    get_standard_permissions, reset, get_permissions
)

from frappe.query_builder import DocType

@frappe.whitelist()
def assign_custom_permissions(doc, method):
    """Enqueue the assignment of custom permissions when a Role is created."""
    # Ensure WF Role exists
    if not frappe.db.exists("WF Roles", doc.name):
        frappe.get_doc({
            "doctype": "WF Roles",
            "role": doc.name
        }).insert(ignore_permissions=True)
        frappe.db.commit()

    frappe.enqueue(
        "ezy_forms.api.v1.custom_role_permission.assign_custom_permissions_job",
        role_name=doc.name,
        queue="long"
    )
    return f"Permission assignment enqueued for role: {doc.name}"

@frappe.whitelist()
def assign_custom_permissions_job(role_name: str):
    """Assign custom permissions to the given role across selected modules."""   
    custom_modules = ["Ezy Flow", "Ezy Forms", "Form Templates"]

    frappe.set_user("Administrator")  # ensure admin context

    for module in custom_modules:
        if not frappe.db.exists("Module Def", module):
            continue
        # Get all doctypes in the module
        # doctypes = frappe.get_all("DocType", filters={"module": module}, pluck="name")
        doctype = DocType("DocType")
        query = (
            frappe.qb.from_(doctype)
            .select(doctype.name)
            .where(doctype.module == module)
        )
        doctypes = [r[0] for r in query.run()]

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


@frappe.whitelist() 
def system_role_permissions():
    docs = frappe.get_all("WF Roles")
    for doc in docs:
        doc = frappe.get_doc("WF Roles",doc)
        frappe.call("ezy_forms.api.v1.custom_role_permission.assign_custom_permissions",    doc=doc,    method=None)
        
        
@frappe.whitelist(methods=["POST"])
def restrict_spical_characters_in_role(doc, method):
    special_characters = [
        "!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "_", "+", "-",
        "=", "[", "]", "{", "}", "|", ";", ":", "'", '"', ",", ".", "<",
        ">", "/", "?", "`", "~"
    ]
    
    # Ensure doc.name is a valid string
    role_name = (doc.role_name or "").strip()

    if not role_name:
        frappe.throw("Role name cannot be empty.")

    if any(char in special_characters for char in role_name):
        frappe.throw(f"Role name cannot contain special characters: {''.join(special_characters)}")


@frappe.whitelist()
def wf_role_creation():
    # Get all core roles and existing WF Roles
    core_roles = frappe.get_list("Role", fields=["name"])
    wf_roles = frappe.get_list("WF Roles", fields=["name"])
    wf_role_names = {role["name"] for role in wf_roles}

    # Exclude these roles from being added
    excluded_roles = { 'Administrator', 'Guest', 'Desk User', 'System Manager', 'Dashboard Manager', 'Script Manager', 'Inbox User',  'Blogger',"All" } # Explicitly excluding 'WF Roles'

    for role in core_roles:
        role_name = role["name"]
        if role_name not in wf_role_names and role_name not in excluded_roles:
            wf_doc = frappe.new_doc("WF Roles")
            wf_doc.role = role_name
            wf_doc.insert(ignore_permissions=True)

    frappe.db.commit()
    return {"success": True, "message": "WF Roles created successfully for all core roles."}
