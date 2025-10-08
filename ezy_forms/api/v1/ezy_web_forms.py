import uuid
import frappe
from frappe.model.document import Document
from frappe.utils import get_url

# creating Qr For Web View forms
def create_qr_for_web_view(form_name):

    action_token = str(uuid.uuid4())

    # creating the document in Ezy Form QR Code doctype
    qr_form_doctype = frappe.get_doc({
        "doctype":"EzyForm QR Code",
        "form_name": form_name,
        "token": action_token
        })
    qr_form_doctype.insert(ignore_permissions=True)
    frappe.db.commit()

    doctype = qr_form_doctype.form_name  # Change this to your target Doctype

    # Get the base URL of your site
    base_url = frappe.get_single("Global Site Settings").site
    
    # Link to open a new document form in Frappe
    qr_link = (
        f"{base_url}/ezyformsfrontend#/qrRaiseRequest?{doctype.lower().replace(' ', '-')}?&ftid={action_token}"
    )
    
    frappe.db.set_value("Ezy Form Definitions", {"name":doctype},{"qr_url":qr_link})
    frappe.db.commit()