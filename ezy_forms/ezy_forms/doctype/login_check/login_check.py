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
def check_is_first_time_or_not(user_id, acknowledgement=None, is_signature=None):
    if not frappe.db.exists("Ezy Employee", {"emp_mail_id": user_id}):
        return "User does not exist"

    try:
        response = {}

        if is_signature:
            frappe.set_value("Ezy Employee", user_id, "signature", is_signature)
            response["signature_updated"] = True

        if acknowledgement:
            frappe.db.set_value("Ezy Employee", user_id, "acknowledgement", acknowledgement)
            frappe.db.set_value("Ezy Employee", user_id, "acknowledge_on", now_datetime())
            response["acknowledgement_updated"] = True

        # Commit only if any update has happened
        if "signature_updated" in response or "acknowledgement_updated" in response:
            frappe.db.commit()
            response["success"] = True
            return response

        # If no updates, return user data
        login_doc = frappe.get_doc("Login Check", {"user_id": user_id}).as_dict()
        login_doc["is_signature"] = 1 if frappe.get_value("Ezy Employee", user_id, "signature") else 0
        login_doc["login_acknowledge"] = frappe.get_value("Ezy Business Unit",frappe.get_value("Ezy Employee", user_id, "company_field"),"is_acknowledge")
        login_doc["is_acknowledge"] = 1 if frappe.get_value("Ezy Employee", user_id, "acknowledgement") else 0
        login_doc["subscription_end_date"] = frappe.get_value("Ezy Business Unit",frappe.get_value("Ezy Employee", user_id, "company_field"),"subscription_end_date")
        login_doc["enable_check"] = 1 if frappe.get_value("User", {"email": user_id}, "enabled") else 0
        login_doc["enable_two_factor_auth"] = frappe.db.get_value("System Settings", "System Settings", "enable_two_factor_auth")
        login_doc['minimum_password_score'] = frappe.db.get_value("System Settings", "System Settings", "minimum_password_score")
        return login_doc

    except Exception as e:
        frappe.log_error(f"Error in check_is_first_time_or_not: {str(e)}")
        return {"success": False, "error": str(e)}

         
         
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
        
        

