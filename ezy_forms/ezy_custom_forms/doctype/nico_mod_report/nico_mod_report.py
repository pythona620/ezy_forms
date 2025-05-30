# Copyright (c) 2025, bharath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.www.printview import get_html_and_style
from random import randint
import os, sys
import traceback
from frappe.utils import get_bench_path, cstr
from frappe.utils import get_bench_path, cstr, get_url
import pdfkit




class NICOMODREPORT(Document):
	
	def after_insert(self):
		pdf_file = frappe.get_print(
        doctype= self.doctype,
        name= self.name,
        as_pdf=True
    	)
		
		sender = frappe.get_value("Email Account",{"enable_outgoing":1,"default_outgoing":1},"email_id")
		frappe.sendmail(
		recipients= "h6714.hod@accor.com", 
		sender=sender,
		message="Dear Team NICO MOD REPORT Form Has Submitted",
		subject="NICO MOD REPORT Form",
		# reply_to = frappe.session.user,
		now=True,
		attachments=[{
            "fname": f"{self.name}.pdf",
            "fcontent": pdf_file
        }],
	)

