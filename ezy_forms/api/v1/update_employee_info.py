import socket as so
import frappe
@frappe.whitelist()
def employee_last_login_activate(login_manager):
    # Ignore permissions for this DB update
    frappe.flags.ignore_permissions = True  

    frappe.db.set_value(
        "Ezy Employee",
        {"emp_mail_id": frappe.session.user},
        {
            "last_login": frappe.utils.now(),
            "last_ip": so.gethostbyname(so.gethostname())
        },
        update_modified=False
    )
    employee_doc = frappe.db.get_values(
        "Ezy Employee", 
        frappe.session.user,
        ["name","company_field","emp_name","emp_mail_id","designation","department","emp_code","is_admin"]
    )
    frappe.local.response["employee_doc"] = employee_doc