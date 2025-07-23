# Copyright (c) 2025, bharath and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class EzyInsights(Document):
	pass



@frappe.whitelist()
def get_insights_dashboards():
    dashboard = frappe.get_doc("Ezy Insights","Ezy Insights")
    return dashboard