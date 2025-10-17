import frappe
@frappe.whitelist()
def employee_update(emp_mail):
    try:
        emp_name= frappe.db.get_value("Signup Employee", {"name": emp_mail}, ["name"])
        if not emp_mail:
            return f"No employee found with email ID: {emp_mail}"
        sign_up_doc = frappe.get_doc("Signup Employee", emp_mail)
        sign_up_doc.enable = 1
        sign_up_doc.save(ignore_permissions=True)
        frappe.db.commit()
        return f"Activation email has been sent successfully to employee {emp_name}."

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Employee Activation Error")
        return f"An error occurred: {str(e)}"
    