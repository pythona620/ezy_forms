import frappe
from datetime import datetime
from frappe.model.db_query import DatabaseQuery
def parse_time(t):
    try:
        # Handle format with microseconds
        return datetime.strptime(t, "%Y/%m/%d %H:%M:%S:%f")
    except ValueError:
        # Handle format without full microseconds (e.g., single-digit seconds)
        return datetime.strptime(t, "%Y/%m/%d %H:%M:%S:%f".replace("%S", "%-S"))

@frappe.whitelist()
def pick_view_only_reportee():
    present_user = frappe.session.user

    designation = frappe.db.get_value("Ezy Employee", present_user, "designation")
 
    if not designation:
        return f"No Designation For the Employee:- {present_user}"
 

    def fetch_requests(view_only_flag):
        matched_requests = []
 
        parent_names = frappe.db.get_all(
            "WF Level Setup",
            filters={
                "role": designation,
                "view_only_reportee": view_only_flag  # <-- using view_only_flag here
            },
            fields=["parent", "requester_as_a_approver", "view_only_reportee", "all_approvals_required","level"]
        )
        for parent in parent_names:
            parent_series = frappe.db.get_value("WF Roadmap", parent["parent"], "series")
            series_prefix = parent_series.replace(" ","_") if parent_series else parent["parent"]
 
            dynamic_filter = {
                "name": ["like", f"%{series_prefix}%"],
            }
 
            if parent["requester_as_a_approver"] == 1:
                dynamic_filter.update({
                    "requested_by": ["like", f"%{present_user}%"],
                    "current_level":parent['level'],
                    "status": "In Progress",
                    
                })
                
            else:
                dynamic_filter.update({
                    "assigned_to_users": ["like", f"%'{designation}'%"],
                    "current_level":parent['level']
                })
            requests = DatabaseQuery("WF Workflow Requests").execute( filters=dynamic_filter, pluck="name")
            matched_requests.extend(requests)
            
        return matched_requests
 
    # Step 1: Get requests where view_only_reportee = 1
    view_only_requests_all = fetch_requests(view_only_flag=1)
    # Step 2: Filter requests where top comment user reports to current user
    filtered_view_only_requests = []
    for req in view_only_requests_all:
        
        comments = frappe.db.get_all(
            "WF Comments",
            filters={"parent": req},
            fields=["user", "level","time"],
            order_by="level DESC"
        )   
        comments = sorted( [{"level": c["level"], "user": c["user"], "time": c["time"]} for c in comments],  key=lambda x: (  x["level"],   parse_time(x["time"]) if x.get("time") else datetime.min ),reverse=True)
        
        if comments:
            comment_user = comments[-1]["user"]
            # Get the reporting manager of the comment user 
            reporting_to = frappe.db.get_value("Ezy Employee", comment_user, "reporting_to")
            check_behalf_of = frappe.db.get_value("WF Workflow Requests", req, "be_half_of")
            if check_behalf_of:
                reporting_to = frappe.db.get_value("Ezy Employee", check_behalf_of, "reporting_to")
                # reporting_to = frappe.db.get_value("Ezy Employee", comment_user, "reporting_to")
            if reporting_to and reporting_to.lower() == present_user.lower():
                filtered_view_only_requests.append(req)

    # Step 3: Get requests where view_only_reportee = 0
    non_reportee_requests = fetch_requests(view_only_flag=0)
 
    # Step 4: Combine and deduplicate
    final_requests = list(set(filtered_view_only_requests + non_reportee_requests))
    final_requests  = DatabaseQuery("WF Workflow Requests").execute(
        filters={"name": ["in", final_requests]},
        fields=["name", "requested_by", "role", "current_level", "total_levels","requested_on","action","department","is_linked_form","linked_form_id","is_linked","user_session_id","property",
                "status", "assigned_to_users", "is_linked", "is_linked_form", "linked_form_id","doctype_name","role","be_half_of","department_name","requester_name"],
        order_by="creation desc",
    )
    return final_requests
