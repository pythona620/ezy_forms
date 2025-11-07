import frappe
from ezy_forms.api.v1.assign_to_me import pick_view_only_reportee
from frappe.model.db_query import DatabaseQuery
import sys, traceback
from frappe import db
@frappe.whitelist()
def dashboard_counts(property=None):
    try:
        session_user = frappe.session.user
        # Fetch only status of forms requested by user
        forms_requested = DatabaseQuery("WF Workflow Requests").execute(
            fields=["status"],
            filters={"requested_by": session_user,"property":property}
        )
 
        requested_counts = {
            "Approved": 0,
            "Pending": 0,
            "Request_cancelled": 0,
            "request_raised": 0
        }
        for doc in forms_requested:
            status = doc["status"]
            if status == "Completed":
                requested_counts["Approved"] += 1
            elif status == "In Progress":
                requested_counts["Pending"] += 1
            elif status == "Request Cancelled":
                requested_counts["Request_cancelled"] += 1
            elif status == "Request Raised":
                requested_counts["request_raised"] += 1
 
        # Fetch forms received by user
        forms_received = pick_view_only_reportee()
        received_counts = {
            "Approved": 0,
            "Pending": 0,
            "Request_cancelled": 0,
            "request_raised": 0
        }
 
        for doc in forms_received:
            status = doc["status"]
            if status == "Completed":
                received_counts["Approved"] += 1
            elif status == "In Progress":
                received_counts["Pending"] += 1
            elif status == "Request Cancelled":
                received_counts["Request_cancelled"] += 1
            elif status == "Request Raised":
                received_counts["request_raised"] += 1
        results = frappe.db.get_all("Ezy Employee",filters={"company_field": property}, fields=["enable", "count(name) as total"], group_by="enable")
        counts = {r.enable: r.total for r in results}
        activate_employee = counts.get(1, 0)
        inactivate_employee = counts.get(0, 0)
        pending_at_approval = frappe.db.count("Signup Employee",filters={"company_field": property,"enable": 0})
        return {
            "data": {
                "requested_by_user": requested_counts,
                "received_by_user": received_counts,
                "employee_details":{
                "activate_employee":activate_employee,
                "inactivate_employee":inactivate_employee,
                "pending_at_approval":pending_at_approval,
                },
                "pick_view_only_reportee":forms_received
            }
        }
 
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error(
            "Error In dashboard.",
            "line No:{}\n{}".format(exc_tb.tb_lineno, traceback.format_exc())
        )
        return {"success": False, "error": str(e)}