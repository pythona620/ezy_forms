from ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests import (
    updating_wf_workflow_requests,wf_cancelling_request
)
import frappe
from frappe.utils import add_to_date,now_datetime


@frappe.whitelist(allow_guest=True)
def email_approval(token, action=None, reason=None):
    try:
        email_doc = frappe.get_doc("Email Approval", {"action_token": token})

        if email_doc.token_status == "Inactive":
            return {"success":False,"message":"Invalid or expired token"}

        # Get document detail
        if not action:
            get_doc = frappe.get_doc(email_doc.doctype_name, {"name": email_doc.document_id})    
            data = get_doc.as_dict()
            
            get_wf_request = frappe.get_doc("WF Workflow Requests",{"name":email_doc.wf_request_id})
            wf_data = get_wf_request.as_dict()
           
            return {"success":True,"message":{"doc_data":data,"wf_data":wf_data}}

        # Update Workflow Request.
        request_details = [
            {
                "doctype": email_doc.doctype_name,
                "request_ids": [email_doc.wf_request_id],
                "current_level": email_doc.current_level,
                "action": action,
                "reason": reason,
                "url_for_approval_id": None,
                "files": [],
                "property": email_doc.property,
                "cluster_name": None,
            }
        ]
        if action == "Approve":
            get_return = updating_wf_workflow_requests(request_details, email_doc.user_id)
            update_value(email_doc)
            
        if action == "Request Cancelled":
            get_return = wf_cancelling_request(email_doc.doctype_name,email_doc.wf_request_id,email_doc.current_level,reason,files=[],property=email_doc.property,cluster_name=None,action=action,url_for_cancelling_id=None,user_session=email_doc.user_id)
            update_value(email_doc)
            
        frappe.db.set_value(
            "Email Approval",
            {"current_level":  email_doc.current_level, "token_status": "Active","wf_request_id":email_doc.wf_request_id,"document_id":email_doc.document_id},
            {"token_status": "Inactive"},
        )
        frappe.db.commit()

        return {"success":True,"message":f"Form {get_return.get('message')} successfully"}

    except Exception as e:
        frappe.log_error(f"Email Approval Action Error: {str(e)}")

def update_value(email_doc):
    get_doc = frappe.get_doc(
        email_doc.doctype_name, {"name": email_doc.document_id}
    )
    approval_detail = frappe.get_doc("Ezy Employee",{"name":email_doc.user_id},["emp_name","signature"])
    frappe.log_error(f"{get_doc}")
    if int(email_doc.current_level) == 1:
        frappe.log_error(email_doc.current_level)
        get_doc.approver = approval_detail.emp_name
        get_doc.approved_by = approval_detail.signature
        get_doc.approved_on = now_datetime().replace(second=0, microsecond=0)
        get_doc.save(ignore_permissions=True)
        frappe.db.commit()
        get_doc.reload()
    else:
        setattr(get_doc, f"approver_{int(email_doc.current_level)-1}", approval_detail.emp_name)
        setattr(get_doc, f"approved_by_{int(email_doc.current_level)-1}", approval_detail.signature)
        setattr(get_doc, f"approved_on_{int(email_doc.current_level)-1}",now_datetime().replace(second=0, microsecond=0))
        get_doc.save(ignore_permissions=True)
        frappe.db.commit()
        get_doc.reload()
     

