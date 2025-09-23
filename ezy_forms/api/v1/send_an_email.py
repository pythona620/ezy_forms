import frappe
import os
import json




def sending_mail_api(each_one_mail, message=None, subject=None, attachments=[], email_template_for_requested_status=None):
    frappe.enqueue('ezy_flow.api.v1.send_an_email.send_email_task',
        queue='default',
        timeout=300,
        each_one_mail=each_one_mail,
        message=message,
        subject=subject,
        attachments=attachments,
        email_template_for_requested_status=email_template_for_requested_status
    )
    
def send_email_task( each_one_mail, message=None, subject=None, attachments=[],email_template_for_requested_status=None):
    # Get the sender email address
    # sender = (
        # frappe.session.user not in STANDARD_USERS and get_formatted_email(frappe.session.user) or None
    # )
    sender = frappe.get_value("Email Account",{"enable_outgoing":1,"default_outgoing":1},"email_id")
    if attachments is None:
        attachments = []
    attachment_list = []
    
    # Filter attachments that have a non-empty 'file_url' and whose file exists
    
    valid_attachments = filter(
        lambda attach: attach.get("file_url", "").strip() and
                    os.path.isfile(
                        os.path.join(
                            frappe.get_site_path("public", "files", "Attachment_folder"),
                            os.path.basename(attach.get("file_url", "").strip())
                        )
                    ),
        attachments
    )


    # Map the valid attachments to the desired output format
    attachment_list = list(map(lambda attach: {
        "fname": os.path.basename(attach.get("file_url", "").strip()),
        "fcontent": open(
            os.path.join(
                frappe.get_site_path("public", "files", "Attachment_folder"),
                os.path.basename(attach.get("file_url", "").strip())
            ), "rb"
        ).read()
    }, valid_attachments))

    frappe.sendmail(
        recipients=[each_one_mail], 
        sender=sender,
        message=message,
        subject=subject,
        reply_to=sender,
        content=email_template_for_requested_status,  # Assuming HTML content
        attachments=attachment_list,
        now=True
    )