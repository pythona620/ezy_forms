import frappe
from frappe.utils import get_url
from ezy_forms.ezy_forms.doctype.login_check.login_check import after_insert_user
@frappe.whitelist()
def employee_update(emp_mail):
    try:
        sender = frappe.get_value("Email Account", {"enable_outgoing": 1, "default_outgoing": 1}, "email_id")
        if not sender:
            return "No outgoing email account is configured."

        employee = frappe.db.get_value("Ezy Employee", {"name": emp_mail}, ["name", "emp_name"])
        if not employee:
            return f"No employee found with email ID: {emp_mail}"

        emp_mail, emp_name = employee
        site_url = get_url()

        email_template = frappe.get_doc("Email Template", "Account Activation")
        subject = email_template.subject or "Account Activation Required"
        message = frappe.render_template(email_template.response_html, {
            "emp_name": emp_name.upper(),
            "emp_mail_id": emp_mail,
            "site_url": f"{site_url}/ezyformsfrontend#/"
        })

        frappe.sendmail(
            recipients=[emp_mail],
            subject=subject,
            sender=sender,
            message=message,
            now=True
        )

        frappe.db.set_value("Ezy Employee", emp_mail, {"enable": 1, "is_web_form": 0})
        frappe.db.set_value("User", emp_mail, "enabled", 1)
        if not frappe.db.exists("Login Check", {"user_id": emp_mail}): # Ensure user is created in Login Check
            new_doc = frappe.new_doc("Login Check")
            new_doc.user_id = emp_mail
            new_doc.insert(ignore_permissions=True)
            
        frappe.db.commit()

        return f"Activation email has been sent successfully to employee {emp_name}."

    except frappe.DoesNotExistError:
        return "No outgoing email account is configured."
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Employee Activation Error")
        return f"An error occurred: {str(e)}"

    