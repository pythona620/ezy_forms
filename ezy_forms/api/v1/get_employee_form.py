import frappe

@frappe.whitelist(methods=["GET"])
def get_employee_forms(property_field,employee=None, requested_by_me=False, approved_by_me=False, department=None,):
    
    filters = {"department": department,"property":property_field} if department else {"property":property_field}
    all_employees = []

    reporting_to = frappe.get_value("Ezy Employee", frappe.session.user, "reporting_to")

    # Get employees reporting to me + myself
    all_employees = frappe.get_all(
        "Ezy Employee",
        filters={"reporting_to": ["in", [frappe.session.user, reporting_to]]},
        pluck="name"
    )

    if all_employees:
        filters.update({"requested_by": ["in", all_employees]})
    if approved_by_me:
        approved_comments = frappe.db.get_all(
            "WF Comments",
            filters={
                "user": employee,
                "action": ["in", ["Approved", "Request Cancelled"]]
            },
            pluck="parent"
        )
        approved_requests = list(set(approved_comments)) if approved_comments else []
        
        if not approved_requests:
            return []
        
        filters={"name": ["in", approved_requests]}

    if requested_by_me:
        filters={"requested_by": employee}

    if not filters:
        return []

    print(filters,"-"*100)
    workflow_requests = frappe.db.get_all(
        "WF Workflow Requests",
        filters=filters,
        fields=[
            "name", "requested_by", "role", "current_level", "total_levels", "employee_id",
            "json_columns", "requested_on", "action", "status", "assigned_to_users",
            "is_linked", "is_linked_form", "linked_form_id", "department_name",
            "requester_name", "doctype_name"
        ],
        
        order_by="creation desc"
    )
    return workflow_requests
