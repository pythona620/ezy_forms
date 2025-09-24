import frappe



def my_team():
    try:
        user = frappe.session.user

        #  If Administrator → return all employee names
        if user == 'Administrator':
            return frappe.get_all("Ezy Employee", pluck="name")

        #  Get current employee record
        employee_id = frappe.db.get_value("Ezy Employee", {"emp_mail_id": user}, "name")
        if not employee_id:
            return []

        def get_reports(emp_id):
            reports = frappe.get_all(
                "Ezy Employee",
                filters={'reporting_to': emp_id},
                pluck="name"   #  return only name
            )
            all_reports = list(reports)

            for r in reports:
                all_reports.extend(get_reports(r))  # recurse deeper
            return all_reports

        # Start with self
        team_list = [employee_id]

        # Add all reports (direct + indirect)
        team_list.extend(get_reports(employee_id))

        # Deduplicate
        return list(set(team_list))

    except Exception:
        frappe.log_error(frappe.get_traceback(), "Error in fetching team")
        return []


@frappe.whitelist(methods=["GET"])
def get_employee_forms(property_field,employee=None, requested_by_me=False, approved_by_me=False, department=None,):
    
    filters = {"department": department,"property":property_field} if department else {"property":property_field}
    all_employees =my_team()

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
