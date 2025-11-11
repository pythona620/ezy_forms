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
            new_doc = frappe.new_doc("Login Check")
            new_doc.user_id = self.emp_mail_id
            new_doc.insert(ignore_permissions=True)
            frappe.db.commit()
            employee_update_notification(emp_mail=self.emp_mail_id)
            
    except Exception as e:
        frappe.log_error(f"Error in after_insert_user for {self.emp_mail_id}: {str(e)}")
        
@frappe.whitelist()
def update_is_first_value(user_id_name, company=None):
    """Update first login flag - requires authentication"""
    try:
        # Ensure user is authenticated
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        # Check if user exists
        login_doc = frappe.db.get_value("Login Check", {"name":user_id_name}, ["name", "is_first_login"], as_dict=True)
        if not login_doc:
            frappe.throw("User does not exist", frappe.DoesNotExistError)

        # Users can only update their own login status
        if frappe.session.user != user_id_name and frappe.session.user != "Administrator":
            frappe.throw("You can only update your own login status", frappe.PermissionError)

        # Update only if not already set
        if login_doc.is_first_login == 0:
            frappe.db.set_value("Login Check", login_doc.name, "is_first_login", 1)
        return {"success": True, "message": "User updated successfully"}

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "update_is_first_value error")
        frappe.throw("Failed to update user status")  
        
        
@frappe.whitelist(methods=["GET","POST"])
def check_is_first_time_or_not(user_id, acknowledgement=None, is_signature=None):
    """Check first-time login status and update user preferences - requires authentication"""
    # Ensure user is authenticated
    if frappe.session.user == "Guest":
        frappe.throw("Authentication required", frappe.AuthenticationError)

    # Users can only check their own status
    if frappe.session.user != user_id and frappe.session.user != "Administrator":
        frappe.throw("You can only check your own status", frappe.PermissionError)

    if not frappe.db.exists("Ezy Employee", {"emp_mail_id": user_id}):
        frappe.throw("User does not exist", frappe.DoesNotExistError)

    try:
        response = {}

        if is_signature:
            frappe.set_value("Ezy Employee", user_id, "signature", is_signature)
            response["signature_updated"] = True

        if acknowledgement:
            frappe.db.set_value("Ezy Employee", user_id, {
                "acknowledgement": acknowledgement,
                "acknowledge_on": now_datetime()
            })
            response["acknowledgement_updated"] = True

        # Commit only if any update has happened
        if "signature_updated" in response or "acknowledgement_updated" in response:
            frappe.db.commit()
            response["success"] = True
            return response
        
        emp_fields = ["signature", "acknowledgement", "company_field"]
        emp_data = frappe.db.get_value("Ezy Employee", {"emp_mail_id": user_id}, emp_fields, as_dict=True)

        bu_fields = ["is_acknowledge"]
        bu_data = frappe.db.get_value("Ezy Business Unit", emp_data.company_field, bu_fields, as_dict=True)
        
        sys_fields = ["enable_two_factor_auth", "minimum_password_score"]
        sys_data = frappe.db.get_value("System Settings", "System Settings", sys_fields, as_dict=True)
        subscription_end_date=frappe.get_value("Global Site Settings","Global Site Settings","subscription_end_date")
        # If no updates, return user data
        login_doc = frappe.get_doc("Login Check", {"user_id": user_id}).as_dict()
        login_doc["is_signature"] = 1 if emp_data.signature else 0
        login_doc["login_acknowledge"] = bu_data.is_acknowledge if bu_data else 0
        login_doc["is_acknowledge"] = 1 if emp_data.acknowledgement else 0
        login_doc["subscription_end_date"] = subscription_end_date if subscription_end_date else None
        login_doc["enable_check"] = 1 if frappe.get_value("User", {"email": user_id}, "enabled") else 0
        login_doc["enable_two_factor_auth"] = sys_data.enable_two_factor_auth
        login_doc['minimum_password_score'] =  sys_data.minimum_password_score
        return login_doc

    except Exception as e:
        frappe.log_error(f"Error in check_is_first_time_or_not: {str(e)}")
        return {"success": False, "error": str(e)}

         
         
@frappe.whitelist(methods=["PUT"])
def update_password(user_id, new_password, old_password, company=None):
    """
    Update user password with proper authentication and validation.
    Requires:
    - User must be logged in
    - User can only change their own password
    - Old password must be verified
    """
    try:
        # Ensure user is authenticated
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        # Users can only change their own password (unless they're Administrator)
        if frappe.session.user != user_id and frappe.session.user != "Administrator":
            frappe.throw("You can only change your own password", frappe.PermissionError)

        # Verify old password (except for Administrator changing other users' passwords)
        if frappe.session.user == user_id:
            from frappe.utils.password import check_password
            if not old_password:
                frappe.throw("Current password is required")
            check_password(user_id, old_password)

        # Validate new password strength
        if not new_password or len(new_password) < 8:
            frappe.throw("New password must be at least 8 characters long")

        # Update password
        get_doc = frappe.get_doc("User", user_id)
        get_doc.new_password = new_password
        get_doc.save()
        frappe.db.commit()

        # Log the password change for audit
        frappe.logger().info(f"Password changed for user: {user_id}")

        return {"success": True, "message": "Password updated successfully"}

    except frappe.AuthenticationError:
        frappe.log_error("Unauthenticated password reset attempt", "Security Alert")
        raise
    except frappe.PermissionError:
        frappe.log_error(f"Unauthorized password change attempt by {frappe.session.user} for {user_id}", "Security Alert")
        raise
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Password Update Error")
        frappe.throw("Failed to update password")  


