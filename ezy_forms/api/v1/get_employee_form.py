import frappe
from frappe.model.db_query import DatabaseQuery
import json
from frappe import _


@frappe.whitelist(methods=["GET"])
def my_team():
    try:
        user = frappe.session.user

        # If Administrator → return all employee names
        if user == "Administrator":
            return frappe.DatabaseQuery("Ezy Employee").execute(pluck="name")

        # Get current employee record
        employee_id = frappe.db.get_value(
            "Ezy Employee", {"emp_mail_id": user}, "name"
        )
        if not employee_id:
            return []

        # Fetch all employees (only once)
        all_employees = frappe.DatabaseQuery("Ezy Employee").execute(
            fields=["name", "reporting_to"]
        )

        # Build mapping: manager → list of reports
        reports_map = {}
        for emp in all_employees:
            manager = emp.get("reporting_to")
            reports_map.setdefault(manager, []).append(emp.get("name"))

        # Recursive fetch from in-memory dict
        def get_reports(emp_id):
            direct_reports = reports_map.get(emp_id, [])
            all_reports = list(direct_reports)
            for r in direct_reports:
                all_reports.extend(get_reports(r))
            return all_reports

        # Start with self + reports
        team_list = [employee_id]
        team_list.extend(get_reports(employee_id))

        # Deduplicate
        return list(set(team_list))

    except Exception:
        frappe.log_error(frappe.get_traceback(), "Error in fetching team")
        return []


@frappe.whitelist(methods=["GET"])
@frappe.read_only()
def get_employee_forms(property_field, employee=None, requested_by_me=False, approved_by_me=False, department=None):
    filters = {"property": property_field}
    if department:
        filters["department"] = department

    is_admin = frappe.db.get_value("Ezy Employee", frappe.session.user, "is_admin")
    all_employees = my_team()

    if not is_admin and all_employees:
        filters["requested_by"] = ["in", all_employees]

    # Filter by approvals
    if approved_by_me and employee:
        # Fetch parents of comments that match the criteria
        approved_parents = frappe.get_all(
            "WF Comments",
            filters={
                "user": employee,
                "action": ["in", ["Approved", "Request Cancelled"]]
            },
            fields=["parent"]
        )
        approved_parent_names = list(set([c["parent"] for c in approved_parents]))
        if not approved_parent_names:
            return []
        filters = {"name": ["in", approved_parent_names]}

    # Filter by requests made by the user
    if requested_by_me and employee:
        filters = {"requested_by": employee}

    if not filters:
        return []

    # Fetch workflow requests using DatabaseQuery (parent table)
    workflow_requests = DatabaseQuery("WF Workflow Requests").execute(
        filters=filters,
        fields=[
            "name", "requested_by", "role", "current_level", "total_levels", "employee_id",
            "json_columns", "requested_on", "action", "status", "assigned_to_users",
            "is_linked", "is_linked_form", "linked_form_id", "department_name",
            "requester_name", "doctype_name",
        ],
        order_by="creation desc"
    )

    return workflow_requests