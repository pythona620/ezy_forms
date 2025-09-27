import frappe
from ezy_forms.api.v1.send_an_email import sending_mail_api
import ast

@frappe.whitelist(methods=["GET"])
@frappe.read_only()
def send_daily_alerts():
    business_units = frappe.db.get_all(
        "Ezy Business Unit",
        filters={"send_daily_alerts": 1},
        fields=["name"]
    )

    sender = frappe.get_value("Email Account", {"enable_outgoing": 1, "default_outgoing": 1}, "email_id")
    if not business_units:
        return "No business units configured to send daily alerts."
    if sender is None:
        return "No outgoing email account configured."

    for bu in business_units:
        property_name = bu.name
        raise_request_data = frappe.db.get_all(
            "WF Workflow Requests",
            filters={
                "status": ["in", ["In Progress", "Raise Request"]],
                "property": property_name
            },
            fields=["name",  "assigned_to_users","doctype_name","status","role","requested_by","requested_on"]
        )

        if not raise_request_data:
            continue

        for request in raise_request_data:
            assigned_to_designation = request.assigned_to_users
            doctype = request.doctype_name
            request_id = request.name
            status = request.status
            role = request.role
            user_name_by_seccion = frappe.get_value("Ezy Employee",request.requested_by,'emp_name')
            requested_on = request.requested_on
            
            if not assigned_to_designation:
                continue
            # Fetch employee emails based on the assigned designation
            if isinstance(assigned_to_designation, str):
                assigned_to_designation = ast.literal_eval(assigned_to_designation)
            
            employee_emails = frappe.get_all(
                "Ezy Employee",
                filters={"designation": ["in", assigned_to_designation], "enable": 1},
                fields=["emp_mail_id"]
            )
            for emp in employee_emails:
                to_email = emp.emp_mail_id
                if not to_email:
                    continue

                email_template = frappe.get_doc("Email Template", {"name": "Approval Remainder"})
                subject = f"Approval Reminder for {doctype}. "
                if not email_template:
                    continue
                # Prepare the email content
                context = {
                    "doctypename": doctype,
                    "generated_request_id": request_id,
                    "action_by": f"{user_name_by_seccion if user_name_by_seccion else frappe.session.user}  ({role})",
                    "current_date_and_time": requested_on,
                    "current_status": status,
                }

                message = frappe.render_template(email_template.response_html, context)
                # Assuming this is your internal email sending method
                frappe.enqueue(
                    method=frappe.sendmail,
                    queue="default",
                    timeout=300,   # optional, in seconds
                    recipients=[to_email],
                    subject=subject,
                    message=message
                )

    return "Emails sent successfully."