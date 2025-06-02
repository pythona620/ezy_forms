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
	pass