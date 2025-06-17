import frappe
import sys
import polars as pl
from ast import literal_eval

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
	
def list_to_dict_with_ones(x):
	x = str(x).split(" ,")
	x = f"""{dict(zip(x,[1] * len(x)))}"""
	return x
@frappe.whitelist()
def add_roles_to_wf_requestors(business_unit:str,doctype:str,workflow_setup:list[dict]):
	try:
		from ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions import activating_perms
		if not len(workflow_setup)>0 or not business_unit or not doctype:return {"success":False,"message":"Please pass levels or requestors for adding Workflow Level Setup."}
		doc_rec = "_".join(business_unit.split()).upper() + "_" + "_".join(doctype.split()).upper().replace(" ", "_")
		requestors_df = pl.DataFrame(workflow_setup)
		requestors_df = requestors_df.explode("roles")
		requestors_df = requestors_df.with_columns(pl.col("fields").list.join(" ,").map_elements(list_to_dict_with_ones).alias("fields"))
		requestors_section = requestors_df.filter(pl.col('type').str.contains("requestor")).select("roles","fields").rename({"roles":"requestor","fields":"columns_allowed"}).to_dicts()
		approvers_section = requestors_df.filter(pl.col('type').str.contains("approver")).with_columns(pl.lit(1).alias('cancel_request')).with_columns(pl.lit(1).alias('mandatory')).with_columns(pl.lit("Approve/Reject").alias('action'))
		if approvers_section.shape[0]>0:
			approvers_section = approvers_section.select("roles","fields","idx","cancel_request","mandatory","action",'view_only_reportee','on_rejection').rename({"roles":"role","fields":"columns_allowed","idx":"level"}).to_dicts()
		else:approvers_section=[]
  
		try:
			frappe.db.sql(f"""delete from `tabWF Requestors` where parent = '{doc_rec}' and parentfield = 'wf_requestors' and parenttype = 'WF Roadmap';""")
			frappe.db.commit()
			frappe.db.sql(f"""delete from `tabWF Level Setup` where parent ='{doc_rec}' and parentfield = 'wf_level_setup' and parenttype='WF Roadmap';""")
			frappe.db.commit()
		except Exception as e:
			frappe.log_error("add role to wf requestors",str(e))
   
		roadmap_doc = frappe.get_doc("WF Roadmap",doc_rec)
		if len(approvers_section)>0:
			roadmap_doc.workflow_levels = max([max_level['level'] for max_level in approvers_section])
		for single_requestor in requestors_section:
			if single_requestor["requestor"]:
				activating_perms(doctype=doctype,role=single_requestor["requestor"])
				roadmap_doc.append("wf_requestors", single_requestor)
		for single_approver in approvers_section:
			if single_approver["role"]:
				activating_perms(doctype=doctype,role=single_approver["role"])
				roadmap_doc.append("wf_level_setup", single_approver)
		roadmap_doc.save(ignore_permissions=True)
		frappe.db.commit()
		workflow_from_defs = frappe.db.get_value("Ezy Form Definitions",doctype,"form_json")
		fields_from_defs = literal_eval(workflow_from_defs)["fields"]
		fields_from_defs = {"fields":fields_from_defs}
		child_table_fields = literal_eval(workflow_from_defs)["child_table_fields"]
		field_with_workflow = fields_from_defs | {"workflow":workflow_setup} | {"child_table_fields":child_table_fields}
		frappe.db.set_value("Ezy Form Definitions",doctype,{"form_json":str(field_with_workflow).replace("'",'"').replace("None","null")})
		frappe.db.commit()
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		frappe.log_error("Error in Updating Roadmap's requestors and approvers in Workflow.",
						 "line No:{}\n{}".format(exc_tb.tb_lineno, str(e)))
		frappe.db.rollback()
		frappe.throw(str(e))
		return {"success": False, "message": str(e)}
