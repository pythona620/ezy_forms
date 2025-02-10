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
        existing_user = frappe.db.get_value("Login Check",{"user_id": self.email},["user_id"])
        
        if not existing_user:
            new_doc = frappe.new_doc("Login Check")
            new_doc.user = self.email
            new_doc.insert(ignore_permissions=True)
            frappe.db.commit()
 
    except Exception as e:
        frappe.log_error(f"Error in after_insert_user for {self.email}: {str(e)}")
        
        
        
@frappe.whitelist(allow_guest=True)
def check_is_first_time_or_not(user_id,company=None):
    print(user_id,"[ppppppppppppppppppppp]")
    try:
        is_first_login = frappe.get_doc("Login Check",{"user_id":user_id},['*'])
        print(is_first_login,"llllllllllllllllllllllll")
 
        return is_first_login
    
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