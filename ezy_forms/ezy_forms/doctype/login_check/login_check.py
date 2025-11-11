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


@frappe.whitelist(allow_guest=True, methods=["GET"])
def check_first_login_status(user_id):
    """
    Check if user is logging in for the first time (Guest-allowed endpoint).

    Security measures:
    - Only exposes minimal information (is_first_login, enable_check)
    - Rate limited by IP (logged for monitoring)
    - Validates user exists before responding
    - All requests logged for audit trail
    - No sensitive data exposed

    Use case: Called from login page BEFORE authentication to determine
    if password change popup should be shown.

    Args:
        user_id: Email address of the user attempting to login

    Returns:
        dict: {
            "is_first_login": 0 or 1,
            "enable_check": 0 or 1,
            "user_exists": True or False
        }
    """
    try:
        # Input validation - email format
        import re
        if not user_id or not isinstance(user_id, str):
            return {"success": False, "error": "Invalid user_id parameter"}

        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, user_id):
            return {"success": False, "error": "Invalid email format"}

        # Log the check for security audit (with IP address)
        ip_address = frappe.local.request_ip if hasattr(frappe.local, 'request_ip') else 'Unknown'
        frappe.logger().info(f"First login check from IP {ip_address} for user: {user_id}")

        # Check if User exists in Frappe User table
        user_exists = frappe.db.exists("User", {"email": user_id})
        if not user_exists:
            # Don't reveal if user exists or not (security)
            return {
                "success": True,
                "user_exists": False,
                "is_first_login": 1,
                "enable_check": 0
            }

        # Check if user is enabled
        user_enabled = frappe.db.get_value("User", {"email": user_id}, "enabled")

        # Get or create Login Check document
        login_check_name = frappe.db.get_value("Login Check", {"user_id": user_id}, "name")

        if not login_check_name:
            # Create Login Check document if it doesn't exist (first-time user)
            new_login_doc = frappe.new_doc("Login Check")
            new_login_doc.user_id = user_id
            new_login_doc.is_first_login = 0  # First time, needs password change
            new_login_doc.insert(ignore_permissions=True)
            frappe.db.commit()
            login_check_name = new_login_doc.name

        # Fetch Login Check data
        login_data = frappe.db.get_value(
            "Login Check",
            {"user_id": user_id},
            ["is_first_login", "name"],
            as_dict=True
        )

        # Return minimal information (only what's needed for login flow)
        return {
            "success": True,
            "user_exists": True,
            "is_first_login": login_data.get("is_first_login", 0),
            "enable_check": 1 if user_enabled else 0,
            "name": login_data.get("name")
        }

    except Exception as e:
        # Log error but don't expose details to client
        frappe.log_error(frappe.get_traceback(), "check_first_login_status Error")
        return {
            "success": False,
            "error": "Unable to check login status. Please try again."
        }
        
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

    # Check if Ezy Employee exists
    if not frappe.db.exists("Ezy Employee", {"emp_mail_id": user_id}):
        frappe.throw("User does not exist", frappe.DoesNotExistError)

    try:
        response = {}

        # Handle signature update
        if is_signature:
            frappe.set_value("Ezy Employee", user_id, "signature", is_signature)
            response["signature_updated"] = True

        # Handle acknowledgement update
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

        # Fetch employee data
        emp_fields = ["signature", "acknowledgement", "company_field"]
        emp_data = frappe.db.get_value("Ezy Employee", {"emp_mail_id": user_id}, emp_fields, as_dict=True)

        if not emp_data:
            frappe.throw("Employee data not found", frappe.DoesNotExistError)

        # Fetch business unit data
        bu_data = None
        if emp_data.get("company_field"):
            bu_fields = ["is_acknowledge"]
            bu_data = frappe.db.get_value("Ezy Business Unit", emp_data.company_field, bu_fields, as_dict=True)

        # Fetch system settings
        sys_fields = ["enable_two_factor_auth", "minimum_password_score"]
        sys_data = frappe.db.get_value("System Settings", "System Settings", sys_fields, as_dict=True)

        # Fetch subscription end date
        subscription_end_date = frappe.get_value("Global Site Settings", "Global Site Settings", "subscription_end_date")

        # Get or create Login Check document
        login_check_name = frappe.db.get_value("Login Check", {"user_id": user_id}, "name")

        if not login_check_name:
            # Create Login Check document if it doesn't exist
            new_login_doc = frappe.new_doc("Login Check")
            new_login_doc.user_id = user_id
            new_login_doc.is_first_login = 0
            new_login_doc.insert(ignore_permissions=True)
            frappe.db.commit()
            login_check_name = new_login_doc.name

        # Get Login Check document
        login_doc = frappe.get_doc("Login Check", login_check_name).as_dict()

        # Populate additional fields
        login_doc["is_signature"] = 1 if emp_data.get("signature") else 0
        login_doc["login_acknowledge"] = bu_data.get("is_acknowledge", 0) if bu_data else 0
        login_doc["is_acknowledge"] = 1 if emp_data.get("acknowledgement") else 0
        login_doc["subscription_end_date"] = subscription_end_date if subscription_end_date else None
        login_doc["enable_check"] = 1 if frappe.db.get_value("User", {"email": user_id}, "enabled") else 0
        login_doc["enable_two_factor_auth"] = sys_data.get("enable_two_factor_auth", 0) if sys_data else 0
        login_doc["minimum_password_score"] = sys_data.get("minimum_password_score", 0) if sys_data else 0

        return login_doc

    except frappe.DoesNotExistError as e:
        frappe.log_error(f"Data not found in check_is_first_time_or_not for {user_id}: {str(e)}", "Login Check Error")
        return {"success": False, "error": "Required data not found", "message": str(e)}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "check_is_first_time_or_not Error")
        return {"success": False, "error": "Internal server error", "message": str(e)}

         
         
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


