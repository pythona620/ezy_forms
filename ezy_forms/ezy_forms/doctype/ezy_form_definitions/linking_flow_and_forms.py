import frappe
import sys

@frappe.whitelist()
def enqueing_creation_of_roadmap(doctype:str,property_name:str,bulk_request:bool):
	try:
		if not frappe.db.exists("WF Settings",{"name":"Ezy Forms"}):
			wf_settings_doc = frappe.new_doc("WF Settings")
			wf_settings_doc.app_name = "Ezy Forms"
			wf_settings_doc.doctype_company = "Ezy Business Unit"
			wf_settings_doc.company_field = "business_unit"
			wf_settings_doc.insert(ignore_permissions=True)
			frappe.db.commit()
			wf_settings_doc.reload()
		
		#### Adding or appending records to child table fields with get_doc
		if not frappe.db.exists("WF Doctype And Field",{"workflow_doctype":doctype,"doctype_field":"company_field"}):
			wf_settings_doc = frappe.get_doc("WF Settings","Ezy Forms")
			wf_settings_doc.append("wf_doctype_and_field",{"workflow_doctype":doctype,"doctype_field":"company_field"})
			wf_settings_doc.save(ignore_permissions=True)
			frappe.db.commit()
		
		roadmap_creation_doc = frappe.new_doc("WF Roadmap")
		roadmap_creation_doc.app_name = "Ezy Forms"
		roadmap_creation_doc.property = property_name
		roadmap_creation_doc.document_type = doctype
		roadmap_creation_doc.bulk_request = bulk_request
		roadmap_creation_doc.insert(ignore_permissions=True)
		frappe.db.commit()
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		frappe.log_error("Error in Creating New Roadmap in Workflow.",
						 "line No:{}\n{}".format(exc_tb.tb_lineno, str(e)))
		frappe.db.rollback()
		frappe.throw(str(e))
		return {"success": False, "message": str(e)}