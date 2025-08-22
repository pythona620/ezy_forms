# Copyright (c) 2025, bharath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import uuid


class EmailApproval(Document):
	pass



def create_email_approval_records(
    wf_request_id,
    doctype_name,
    document_id,
    user_id,
    wf_statsu,
    current_level,
    propert_id,
    department=None,
):
    action_token = str(uuid.uuid4())

    get_role_uses = frappe.db.get_list(
        "WF Users",
        {"parent": propert_id, "mail": user_id},
        ["role_name", "mail"],
        ignore_permissions=True,
    )

    # for each in get_role_uses:
    new_doc = frappe.get_doc(
        {
            "doctype": "Email Approval",
            "property": propert_id,
            "wf_request_id": wf_request_id,
            "doctype_name": doctype_name,
            "document_id": document_id[0].name,
            "role": (
                get_role_uses[0].get("role_name") if len(get_role_uses) > 0 else None
            ),
            "user_id": user_id,
            "action_token": action_token,
            "status": wf_statsu,
            "department": department,
            "current_level": current_level,
        }
    )

    new_doc.insert(ignore_permissions=True)
    frappe.db.commit()

    return new_doc.action_token



# Update token status if any one approve through web version.    
def update_token_status(action,wf_request_id,document_id,current_level,status=None):
    
    if action == "Approve" or action == "Request Cancelled":
        
        if status == "In Progress":
            previous_level = int(current_level) - 1
        else:
            previous_level = int(current_level)
            
        frappe.db.set_value(
                "Email Approval",
                {"current_level":  str(previous_level), "token_status": "Active","wf_request_id":wf_request_id,"document_id":document_id.get("name")},
                {"token_status": "Inactive"},
            )
        frappe.db.commit()