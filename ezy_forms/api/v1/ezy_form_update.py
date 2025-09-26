import frappe
from ezy_forms.api.v1.ezy_form_rasie_request import todo_tab
import random
import string
from frappe.utils import add_to_date
import sys,os
from ezy_forms.ezy_forms.doctype.ezy_form_definitions.dynamic_form_template import download_filled_form
import traceback
from urllib.parse import urlparse
import ast
from ezy_forms.api.v1.send_an_email import sending_mail_api

@frappe.whitelist()
def edit_the_form_before_approve(document_type,property,form_id,updated_fields,status=None):
    try:
        status = 'Request Raised'
        current_level_for_form =  0
        current_level_for_wf_workflow = 1
        if not frappe.db.exists("DocType",document_type):
            return {"success":True, "message":"Form Not Found"}
        record_data = frappe.get_doc(document_type,{"wf_generated_request_id":form_id,"company_field":property})
        frappe.db.set_value('WF Workflow Requests', form_id, {"status":'Request Raised','current_level':1,"action":"Request Raised","user_session_id":""})
        todo_tab(document_type=document_type, request_id=form_id, property=property, cluster_name=None, current_level=current_level_for_wf_workflow,account_ids=record_data,status="None")
            
        now = add_to_date(None,as_datetime=True)
        my_time = f"{now.year}/{now.month}/{now.day} {now.hour}:{now.minute}:{now.second}:{now.microsecond}" 
        random_reference_id = ''.join(random.choices(string.ascii_lowercase + string.ascii_uppercase + string.digits, k=10))
        setting_reason = frappe.get_doc('WF Activity Log', form_id)
        # Append to the child table "reason"
        setting_reason.append("reason", {
            "level": current_level_for_form,
            "reason": 'Request Updated',
            "role": frappe.get_value('WF Workflow Requests', form_id, 'role'),
            "user": frappe.session.user,
            "action": 'Request Raised',
            "time": my_time,
            "random_string":  ''.join(random.sample(random_reference_id,len(random_reference_id)))
        })
        # Save the parent document
        setting_reason.save(ignore_permissions=True)
        frappe.db.commit()
        setting_reason.reload() 
          
        name,doctype_name,status,property = frappe.db.get_value("WF Workflow Requests",form_id,["name","doctype_name",",status","property"])
        form_doctype_query = """
            SELECT doctype_name_wf
            FROM `tabWF IDs`
            WHERE parent = %s AND parentfield = 'reference_id' AND parenttype = 'WF Workflow Requests'
        """
        form_documents = frappe.db.sql(form_doctype_query,(form_id,), as_dict=True)
        document_name = form_documents[0]["doctype_name_wf"]
 
        doc = frappe.get_doc(doctype_name, document_name)
 
        # Update normal fields (filter out child tables)
        for key, value in updated_fields.items():
            if isinstance(value, list):
                # assume child table, update below
                continue
            setattr(doc, key, value)
 
        # Update child tables properly
        for key, value in updated_fields.items():
            if isinstance(value, list):
                # clear existing child rows
                doc.set(key, [])
                for row in value:
                    doc.append(key, row)
 
        doc.save()
        doc.reload()
        frappe.db.commit()
        sending_mail_api(request_id=form_id, doctype_name=doctype_name, property=property, cluster=None, reason="Request Updated", timestamp=my_time,skip_user_role= None)
        return {"success":True, "message":"edit form Succesfully Updated"}
       
    except Exception as e:
        exc_type,exc_obj, exc_tb = sys.exc_info()
        frappe.log_error("error in edit the form.","line No:{}\n{}".format(
            exc_tb.tb_lineno,traceback.format_exc()))
        return {"success":False, "error":str(e)}  