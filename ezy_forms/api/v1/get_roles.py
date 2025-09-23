import frappe

@frappe.whitelist()
def get_role_list(index:int=None, departments:list=None, property:str=None):
    """
    Returns a list of roles with a flag indicating if they belong 
    to an admin (HOD) or employee.

    api = "ezy_forls.api.v1.get_roles.get_role_list"
    """

    # Ensure index is an integer
    index = int(index) if index is not None else -1
    requester = None
    approver =None
    # Determine flags
    if int(index) ==0:
        requester = 0
    else:
        approver = 1

    # Base filters
    filters = {"enable": 1,"department": ["in", departments],"company_field": property}

    # Apply additional filters based on index
    if approver:
        filters.update({"is_hod": 1})

    # Fetch employee designations
    admin_designations = frappe.get_all(
        "Ezy Employee",
        filters=filters,
        pluck="designation"
    )

    # Fetch workflow roles
    wf_roles = frappe.get_all("WF Roles", pluck="role")

    # Build role list
    if requester:
        roles_list = [
            {
                "role": role,
                "employee": 1 if role in admin_designations else 0
            }
            for role in wf_roles
        ]
    elif approver:
        roles_list = [
            {
                "role": role,
                "is_hod": 1 if role in admin_designations else 0
            }
            for role in wf_roles
        ]
    else:
        # Default case
        roles_list = [{"role": role} for role in wf_roles]

    return roles_list
