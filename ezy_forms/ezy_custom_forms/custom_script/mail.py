
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
		frappe.sendmail(
		recipients= "h6714.hod@accor.com",
		sender=sender[0]['email_id'],
		message="Dear Team NICO MOD REPORT Form Has Submitted",
		subject="NICO MOD REPORT Form",
		# reply_to = frappe.session.user,
		now=True,
		attachments=[pdf_file],
		)
		
	except Exception as e:
		frappe.log_error("email_pdf_send",e)