import frappe
from frappe.model.document import Document
from frappe.utils import get_url
from frappe.utils.file_manager import save_file
from io import BytesIO
import json
import uuid
import random
import string
from frappe.utils import add_to_date,get_datetime, now_datetime
from ezy_forms.api.v1.send_an_email import sending_mail_api  


def create_qr_for_web_view(form_name):
    action_token = str(uuid.uuid4())

    existing_qr = frappe.db.exists("EzyForm QR Code", {"form_name": form_name})
    if not existing_qr:
        # Create a new QR code entry
        qr_form_doctype = frappe.get_doc({
            "doctype": "EzyForm QR Code",
            "form_name": form_name,
            "token": action_token
        })
        qr_form_doctype.insert(ignore_permissions=True)
        frappe.db.commit()

    # get the site url
    base_url = get_url()
    #form_name in link should be in lowercase and spaces replaced with hyphens
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

    # now = now_datetime()  # Current date + time (as datetime)
    # form_from = get_datetime(form_valid_from) if form_valid_from else now
    # form_to = get_datetime(form_valid_to) if form_valid_to else None

    # # Check not yet active
    # if form_from and form_from > now:
    #     diff = form_from - now
    #     hours, remainder = divmod(diff.total_seconds(), 3600)
    #     minutes, seconds = divmod(remainder, 60)
    #     frappe.throw(
    #         f"This form will start in {int(hours)} hour(s) and {int(minutes)} minute(s) at {form_from}."
    #     )

    # # Check expired
    # if form_to and form_to < now:
    #     frappe.throw("This form is expired.")
    
 
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
    
    sending_mail_api(request_id=new_wf_work_flow_requests.name, doctype_name=doctype_name,Qr_form_mali_id=data.get("mail_id"),property= data.get("business_unit"),cluster=None,timestamp=None,reason= reason,skip_user_role= None,user=None,field_changes=None,current_level=None,current_status = "Request Raised Via QR Code" )

    
    
    
    if data.get("public_form_response"):
        message_response = data.get("public_form_response")
    else:
        message_response = "Thank you! Your form has been submitted successfully."

    return {
        "message": message_response,
        "docname": new_doc
    }
    
    
@frappe.whitelist()
def get_dynamic_Qr_data(form_name, form_valid_from=None, form_valid_to=None):
    from frappe.utils import now_datetime, get_datetime

    # Get existing active dynamic QR for the form
    existing_data_for_qr = frappe.db.get_list(
        "EzyForm QR Code",
        filters={
            "form_name": form_name,
            "is_dynamic_qr": 1,
            "token_status": "Active"
        },
        fields=["name","form_valid_from", "form_valid_to", "dynamic_link", "token_status"]
    )

    now = now_datetime()

    # If no existing QR found
    if not existing_data_for_qr:
        return {"message": "No active dynamic QR link found. Please create a new one."}

    qr_data = existing_data_for_qr[0]

    # Convert to datetime for comparison
    form_from = get_datetime(qr_data["form_valid_from"]) if qr_data["form_valid_from"] else None
    form_to = get_datetime(qr_data["form_valid_to"]) if qr_data["form_valid_to"] else None

    # Check validity period
    if form_from and form_from > now:
        return {
            "message": "QR link is not yet active.",
            "dynamic_link": qr_data["dynamic_link"],
            "token_status": qr_data["token_status"],
            "form_valid_from": qr_data["form_valid_from"],
            "form_valid_to": qr_data["form_valid_to"]
        }

    if form_to and form_to < now:
        frappe.db.set_value(
            "EzyForm QR Code",
            qr_data["name"],
            {
                "is_dynamic_qr": 0,
                "token_status": "Inactive"
            }
        )
        frappe.db.commit()
        return {"message": "QR link has expired. Please create a new one."}

    # If valid (active)
    return {
        "message": "Active QR link found.",
        "dynamic_link": qr_data["dynamic_link"],
        "token_status": qr_data["token_status"],
        "form_valid_from": qr_data["form_valid_from"],
        "form_valid_to": qr_data["form_valid_to"]
    }


@frappe.whitelist()
def create_dynamic_qr_link(form_name, form_valid_from=None, form_valid_to=None, status=None):
    import uuid
    from frappe.utils import get_url

    existing_data_for_qr = frappe.db.get_list(
        "EzyForm QR Code",
        filters={
            "form_name": form_name,
            "is_dynamic_qr": 1,
            "token_status": "Active"
        },
        fields=["name", "form_valid_from", "form_valid_to", "dynamic_link", "is_dynamic_qr", "token_status"]
    )

    if existing_data_for_qr:
        # Update existing QR
        frappe.db.set_value(
            "EzyForm QR Code",
            existing_data_for_qr[0]["name"],
            {
                "form_valid_from": form_valid_from,
                "form_valid_to": form_valid_to
            }
        )
        frappe.db.commit()

        return {
            "message": "Dynamic QR Code updated successfully.",
            "dynamic_link": existing_data_for_qr[0]["dynamic_link"],
            "form_valid_from": form_valid_from,
            "form_valid_to": form_valid_to
        }

    else:
        # Create new QR
        action_token = str(uuid.uuid4())
        base_url = get_url()
        qr_link = f"{base_url}/ezyformsfrontend#/qrRaiseRequest?{form_name.lower().replace(' ', '-')}?&ftid={action_token}"

        qr_doc = frappe.get_doc({
            "doctype": "EzyForm QR Code",
            "form_name": form_name,
            "token": action_token,
            "form_valid_from": form_valid_from,
            "form_valid_to": form_valid_to,
            "is_dynamic_qr": 1,
            "token_status": "Active",
            "dynamic_link": qr_link
        })
        qr_doc.insert(ignore_permissions=True)

        return {
            "message": "Dynamic QR Code created successfully.",
            "dynamic_link": qr_link,
            "token_status": "Active",
            "form_valid_from": form_valid_from,
            "form_valid_to": form_valid_to
        }