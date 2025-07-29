# Copyright (c) 2025, bharath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json
from frappe.utils import now_datetime
from ezy_forms.api.v1.sign_up import employee_update_notification
class LoginCheck(Document):
	pass

@frappe.whitelist()
def after_insert_user(self, method=None):
    try:
        if not frappe.db.exists("Login Check", {"user_id": self.emp_mail_id}):
            existing_user = frappe.db.get_value("Login Check",{"user_id": self.emp_mail_id},["user_id"])
            
            if not existing_user:
                new_doc = frappe.new_doc("Login Check")
                new_doc.user_id = self.emp_mail_id
                new_doc.insert(ignore_permissions=True)
                frappe.db.commit()
                employee_update_notification(emp_mail=self.emp_mail_id)
                
 
    except Exception as e:
        frappe.log_error(f"Error in after_insert_user for {self.emp_mail_id}: {str(e)}")
        
@frappe.whitelist(allow_guest=True)
def update_is_first_value(user_id_name,company=None):
    try:
 
        get_doc = frappe.get_doc("Login Check",{"name":user_id_name})
        get_doc.is_first_login  = 1
        get_doc.save(ignore_permissions=True)
        frappe.db.commit()
 
        return get_doc
    
    except Exception as e:
        frappe.log_error(f"Error In User Not exit for :", {str(e)})  
        
             
        
@frappe.whitelist(allow_guest=True)
def check_is_first_time_or_not(user_id,acknowledgement=None):
    if not frappe.db.exists("Ezy Employee", {"emp_mail_id": user_id}):
        return  "User does not exist"
    try:
        if acknowledgement and user_id:
            frappe.db.set_value('Ezy Employee',user_id,'acknowledgement',acknowledgement)
            frappe.db.set_value('Ezy Employee',user_id,'acknowledge_on',now_datetime())
            frappe.db.commit()
            return "Acknowledgement Updated"
        else:
            login_doc = frappe.get_doc("Login Check", {"user_id": user_id}, ['*']).as_dict()
            login_dict = login_doc
            login_dict["is_signature"] = 1 if frappe.get_value('Ezy Employee', user_id, 'signature') else 0
            enable_two_factor_auth = frappe.db.get_value("System Settings", "System Settings", "enable_two_factor_auth")
            enable_check = frappe.get_value('User',{"email":user_id},'enabled')
            login_dict["enable_check"] = 1 if enable_check else 0
            login_dict["enable_two_factor_auth"] = enable_two_factor_auth
            is_acknowledge = frappe.get_value('Ezy Employee',user_id,'acknowledgement')
            login_dict["is_acknowledge"] = 1 if is_acknowledge else 0
            
        
        return login_dict
     
    except Exception as e:
        frappe.log_error(f"Error In User Not exit for:", {str(e)})
         
         
@frappe.whitelist(allow_guest=True)
def update_password(user_id,new_password,company=None):
    try:
 
        get_doc = frappe.get_doc("User",{"name":user_id})
        get_doc.new_password  = new_password
        get_doc.save(ignore_permissions=True)
        frappe.db.commit()
 
        return get_doc
    
    except Exception as e:
        frappe.log_error(f"Error In User Not exit for :", {str(e)})  
        
        

