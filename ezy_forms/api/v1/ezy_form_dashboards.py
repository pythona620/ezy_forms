import frappe
from ezy_forms.api.v1.assign_to_me import pick_view_only_reportee
from frappe.model.db_query import DatabaseQuery
import sys, traceback

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

        if forms_received:
            # Extract names to query only required fields
            names = [doc["name"] for doc in forms_received]
            received_docs = DatabaseQuery("WF Workflow Requests").execute(
                fields=["status"],
                filters={"name": ["in", names],
                         "property":property}
            )
            for doc in received_docs:
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
        frappe.log_error(
            "Error In dashboard.",
            "line No:{}\n{}".format(exc_tb.tb_lineno, traceback.format_exc())
        )
        return {"success": False, "error": str(e)}
