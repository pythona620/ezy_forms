import frappe
import sys
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
def add_roles_to_wf_requestors(business_unit: str, doctype: str, workflow_setup: list[dict]):
    try:
        from ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions import activating_perms
        if not len(workflow_setup) > 0 or not business_unit or not doctype:
            return {"success": False, "message": "Please pass levels or requestors for adding Workflow Level Setup."}
        
        doc_rec = "_".join(business_unit.split()).upper() + "_" + "_".join(doctype.split()).upper().replace(" ", "_")
        
        # Replace Polars DataFrame operations with native Python
        exploded_data = sum( map(lambda row: list( map(lambda role: {**row, "roles": role}, row.get("roles") if isinstance(row.get("roles"), list)  else ([row.get("roles")] if isinstance(row.get("roles"), str) else [])  )  ), workflow_setup),   []  )

        
        # Process fields column - convert list to dict with ones
        exploded_data = list(map(lambda row: 
            {**row, "fields": list_to_dict_with_ones(" ,".join(map(str, row.get("fields", []))))} 
            if isinstance(row.get("fields", []), list) else row, exploded_data))

        
        # Filter requestors section
        requestors_section = list(map(
            lambda row: {
                "requestor": row.get("roles"),
                "columns_allowed": row.get("fields")
            },
            filter(lambda row: "requestor" in row.get("type", ""), exploded_data)
        ))
        
        # Filter approvers section
        approvers_data = list(filter(lambda row: "approver" in row.get('type', ''), exploded_data))

        approvers_section = list(map(lambda row: {
            "role": row.get("roles"),
            "columns_allowed": row.get("fields"),
            "level": row.get("idx"),
            "cancel_request": 1,
            "mandatory": 1,
            "action": "Approve/Reject",
            "view_only_reportee": row.get("view_only_reportee"),
            "requester_as_a_approver": row.get("requester_as_a_approver"),
            "all_approvals_required": row.get("all_approvals_required"),
            "on_rejection": row.get("on_rejection")
        }, approvers_data))

        
        try:
            frappe.db.sql(f"""delete from `tabWF Requestors` where parent = '{doc_rec}' and parentfield = 'wf_requestors' and parenttype = 'WF Roadmap';""")
            frappe.db.commit()
            frappe.db.sql(f"""delete from `tabWF Level Setup` where parent ='{doc_rec}' and parentfield = 'wf_level_setup' and parenttype='WF Roadmap';""")
            frappe.db.commit()
        except Exception as e:
            frappe.log_error("add role to wf requestors", str(e))
   
        roadmap_doc = frappe.get_doc("WF Roadmap", doc_rec)

        # Set workflow_levels if approvers_section is not empty
        if approvers_section:
            roadmap_doc.workflow_levels = max(map(lambda max_level: max_level['level'], approvers_section))

        # Process requestors_section using map and lambda
        list(map(lambda single_requestor: (
            activating_perms(doctype=doctype, role=single_requestor["requestor"]),
            roadmap_doc.append("wf_requestors", single_requestor)
        ) if single_requestor["requestor"] else None, requestors_section))

        # Process approvers_section using map and lambda
        list(map(lambda single_approver: (
            activating_perms(doctype=doctype, role=single_approver["role"]),
            roadmap_doc.append("wf_level_setup", single_approver)
        ) if single_approver["role"] else None, approvers_section))

        # Save and commit
        roadmap_doc.save(ignore_permissions=True)
        frappe.db.commit()

        
        workflow_from_defs = frappe.db.get_value("Ezy Form Definitions", doctype, "form_json")
        fields_from_defs = literal_eval(workflow_from_defs)["fields"]
        fields_from_defs = {"fields": fields_from_defs}
        child_table_fields = literal_eval(workflow_from_defs)["child_table_fields"]
        field_with_workflow = fields_from_defs | {"workflow": workflow_setup} | {"child_table_fields": child_table_fields}
        frappe.db.set_value("Ezy Form Definitions", doctype, {"form_json": str(field_with_workflow).replace("'", '"').replace("None", "null")})
        frappe.db.commit()
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error("Error in Updating Roadmap's requestors and approvers in Workflow.",
                         "line No:{}\n{}".format(exc_tb.tb_lineno, str(e)))
        frappe.db.rollback()
        frappe.throw(str(e))
        return {"success": False, "message": str(e)}