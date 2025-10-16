import frappe
from frappe.model.document import Document
from frappe.utils import get_url
from frappe.utils.file_manager import save_file
from io import BytesIO
import json
import uuid
import random
import string
from frappe.utils import add_to_date

def create_qr_for_web_view(form_name):
    # Generate a unique token
    action_token = str(uuid.uuid4())

    # Create and insert QR record
    frappe.get_doc({
        "doctype": "EzyForm QR Code",
        "form_name": form_name,
        "token": action_token
    }).insert(ignore_permissions=True)

    # Build the QR link
    # base_url = frappe.get_value("Global Site Settings","Global Site Settings","site")
    # base_url = frappe.utils.get_url()
    base_url = get_url()
    qr_link = f"{base_url}/ezyformsfrontend#/qrRaiseRequest?{form_name.lower().replace(' ', '-')}?&ftid={action_token}"

    # Update the Ezy Form Definitions record
    frappe.db.set_value("Ezy Form Definitions", {"name": form_name}, "qr_url", qr_link)
    frappe.db.commit()

@frappe.whitelist(allow_guest=True)
def qr_code_to_new_form(token, save_doc=None):
    # Get form_name from QR token
    form_name = frappe.db.get_value("EzyForm QR Code", {"token": token}, "form_name")
    if not form_name:
        frappe.throw("Invalid token")
 
    # Get form definition details
    data = frappe.get_doc("Ezy Form Definitions", {"name": form_name}).as_dict()
    if data.get("enable") == 0:
        frappe.throw("This form is disabled. Please contact administrator.")
    # Case 1: If save_doc is NOT provided → return form definition only
    if not save_doc:
        return {
            "message": "Form definition fetched successfully",
            "data": data
        }
 
    # Case 2: If save_doc is provided → create document
    if isinstance(save_doc, str):
        import json
        field_data = json.loads(save_doc)
    else:
        field_data = save_doc  # already dict
 
    # Prepare new document
    new_doc = frappe.get_doc({
        "doctype": data.get("name"),
        **field_data
    })
 
    # Insert document
    new_doc.insert(ignore_permissions=True)
    frappe.db.commit()
    document_id = new_doc.name
    
    # return {
    #     "message": "Save Doc successfully Done",
    #     "docname": document_id,
    #     "doctype_name":data.get("form_name")
    # }
    
    doctype_name = data.get("name")
    reason = "Request Raised via QR Code"  
    parent_for_wf_level_setup = "_".join(data.get("business_unit").split()).upper() + "_" + "_".join(data.get("name").split()).upper().replace(" ", "_")
    
    assign_to_users = frappe.db.get_list("WF Level Setup",{"parent":parent_for_wf_level_setup,"level":1,"parenttype":"WF Roadmap"},pluck="role",ignore_permissions=True)
    
    # working flow
    new_wf_work_flow_requests = frappe.get_doc({
        "doctype": "WF Workflow Requests",
        "doctype_name": doctype_name,
        "status": "Request Raised Via QR Code",
        "property": data.get("business_unit"),
        "action": reason,
        "reference_id": [{
            'doctype':"WF IDs",
            "parenttype":"WF Workflow Requests",
            "doctype_name_wf":document_id,
            "parentfield":"reference_id",
        }],
        'requester_name':new_doc.requested_by,
        'requested_on':new_doc.requested_on,
        "assigned_to_users": str(assign_to_users)
    })
    new_wf_work_flow_requests.insert(ignore_permissions=True)
    frappe.db.commit()
    new_wf_work_flow_requests.reload()
    
    new_doc.wf_generated_request_id = new_wf_work_flow_requests.name
    new_doc.wf_generated_request_status = reason
    new_doc.save(ignore_permissions=True)
    frappe.db.commit()
    random_reference_id = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=10))
    random_reference_id = ''.join(random.sample(random_reference_id,len(random_reference_id)))
    
    # activate log
    now = add_to_date(None,as_datetime=True)
    my_time = f"{now.year}/{now.month}/{now.day} {now.hour}:{now.minute}:{now.second}:{now.microsecond}"
    new_activate_log = frappe.get_doc({
        "doctype": "WF Activity Log",
        "request_id":new_wf_work_flow_requests.name,
        'reason':[{
            "doctype":"WF Comments",
            "level":0,
            "reason":"Request Raised via QR Code",
            "user":"Guest",
            "user_name":"Guest",
            "action":"Request Raised",
            "random_string":random_reference_id,
            "time":my_time,
            
        }]
    })
    new_activate_log.insert(ignore_permissions=True)
    frappe.db.commit()
    new_activate_log.reload()
    
    
    
    if data.get("public_form_response"):
        message_response = data.get("public_form_response")
    else:
        message_response = "Thank you! Your form has been submitted successfully."

    return {
        "message": message_response,
        "docname": new_doc
    }