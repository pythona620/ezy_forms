# Copyright (c) 2025, bharath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
import json


class LoginCheck(Document):
	pass

@frappe.whitelist(allow_guest=True)
def after_insert_user(self, method=None):
    try:
        existing_user = frappe.db.get_value("Login Check",{"user_id": self.emp_mail_id},["user_id"])
        
        if not existing_user:
            new_doc = frappe.new_doc("Login Check")
            new_doc.user_id = self.emp_mail_id
            new_doc.insert(ignore_permissions=True)
            frappe.db.commit()
            
 
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
def check_is_first_time_or_not(user_id,company=None):
    try:
        login_doc = frappe.get_doc("Login Check", {"user_id": user_id}, ['*'])
        login_dict = login_doc.as_dict()
        
        enable_two_factor_auth = frappe.db.get_value("System Settings", "System Settings", "enable_two_factor_auth")
        enable_check = frappe.get_value('User',{"email":user_id},'enabled')
        login_dict["enable_check"] = 1 if enable_check else 0
        login_dict["enable_two_factor_auth"] = enable_two_factor_auth
        
        
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
        
        

 
@frappe.whitelist(allow_guest=True)
def employee_update_notification(emp_mail):

    emp_mail,emp_name = frappe.db.get_value("Ezy Employee",{"name":emp_mail},["name","emp_name"])
    
    frappe.sendmail(
            recipients=emp_mail,
            subject="Employee Profile Status",
            message=f"""Dear {emp_name},<br><br>
            Your employee profile has been enabled. Please check your details.<br><br>
            Regards,<br>IT Team""",
            now = True
        )
    return "Notification sent successfully"
