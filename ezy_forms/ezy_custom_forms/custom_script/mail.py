
import frappe
from frappe.model.document import Document
from frappe.www.printview import get_html_and_style
from random import randint
import os, sys
import traceback
from frappe.utils import get_bench_path, cstr
from frappe.utils import get_bench_path, cstr, get_url
# from frappe.frappe import get_print
import pdfkit

def email_pdf_send(doc,method=None):
	try:
		pdf_file = frappe.attach_print(
		doctype= doc.doctype,
		name= doc.name,
		)
		
		sender = frappe.db.get_list("Email Account",{"enable_outgoing":1,"default_outgoing":1},["email_id"],ignore_permissions=True)
		mail = frappe.db.get_single_value("Notifications Mail", "mail_id")
		frappe.sendmail(
		recipients= mail,
		sender=sender[0]['email_id'],
		message=f"Dear Team, {doc.doctype} has been submitted.",
    	subject=f"{doc.doctype} Form",
		# reply_to = frappe.session.user,
		now=True,
		attachments=[pdf_file],
		)
		
	except Exception as e:
		frappe.log_error("email_pdf_send",e)
  
  


import shutil
 
def make_file_public_after_insert(doc, method=None):
    if doc.is_private:
        # Extract the filename
        filename = os.path.basename(doc.file_url)
 
        # Construct full source and target paths
        private_path = frappe.get_site_path("private", "files", filename)
        public_path = frappe.get_site_path("public", "files", filename)
 
        # Ensure the private file exists before moving
        if os.path.exists(private_path):
            shutil.move(private_path, public_path)
 
            # Update file doc
            doc.db_set("is_private", 0)
            doc.db_set("file_url", f"/files/{filename}")
        else:
            frappe.log_error(f"File not found at {private_path}", "make_file_public_after_insert Error")
            frappe.throw(f"Private file {filename} does not exist.")