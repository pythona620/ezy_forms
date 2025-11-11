import frappe
import sys, traceback
from ezy_forms.ezy_forms.utils import pick_view_only_reportee
from frappe.model.db_query import DatabaseQuery


# Api for all forms count dashboards    
@frappe.whitelist()
def dashboard_counts():
    try:
        session_user = frappe.session.user
        # Requests initiated by session user
        forms_requested = frappe.db.get_all("WF Workflow Requests", fields=["status"], filters={'requested_by': session_user})
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
                        
        forms_received = pick_view_only_reportee()
        # forms_received = frappe.db.get_all(
        #     "WF Workflow Requests", 
        #     fields=["status"], 
        #     filters={'name': ["in", wf_workflow_requests]}
        # )
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
        return {
            "data": {
                "requested_by_user": requested_counts,
                "received_by_user": received_counts
            }
        }
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error("Error In dashboard.", "line No:{}\n{}".format(
            exc_tb.tb_lineno, traceback.format_exc()))
        return {"success": False, "error": str(e)}