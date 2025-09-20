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
        
        exploded_data = []
        for row in workflow_setup:
            roles = row.get("roles", [])
            if isinstance(roles, str):
                roles = [roles]
            elif not isinstance(roles, list):
                roles = []
            
            for role in roles:
                new_row = row.copy()
                new_row["roles"] = role
                exploded_data.append(new_row)
        
        # Process fields column - convert list to dict with ones
        for row in exploded_data:
            fields = row.get("fields", [])
            if isinstance(fields, list):
                fields_str = " ,".join(str(f) for f in fields)
                row["fields"] = list_to_dict_with_ones(fields_str)
        
        # Filter requestors and approvers sections
        requestors_section = []
        approvers_section = []
        
        for row in exploded_data:
            row_type = row.get('type', '')
            if row_type.find("requestor") != -1:
                requestors_section.append({
                    "requestor": row.get("roles"),
                    "columns_allowed": row.get("fields")
                })
            elif row_type.find("approver") != -1:
                approvers_section.append({
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
                })
        
        # Check if records exist before deleting
        try:
            # Check for existing requestors
            existing_requestors = frappe.db.sql(
                f"""SELECT COUNT(*) as count FROM `tabWF Requestors` 
                    WHERE parent = '{doc_rec}' AND parentfield = 'wf_requestors' AND parenttype = 'WF Roadmap'""", 
                as_dict=True
            )
            
            # Check for existing level setup
            existing_levels = frappe.db.sql(
                f"""SELECT COUNT(*) as count FROM `tabWF Level Setup` 
                    WHERE parent = '{doc_rec}' AND parentfield = 'wf_level_setup' AND parenttype = 'WF Roadmap'""", 
                as_dict=True
            )
            
            # Only delete if records exist and combine both deletions in single transaction
            if existing_requestors[0]['count'] > 0 or existing_levels[0]['count'] > 0:
                if existing_requestors[0]['count'] > 0:
                    frappe.db.sql(f"""DELETE FROM `tabWF Requestors` 
                                     WHERE parent = '{doc_rec}' AND parentfield = 'wf_requestors' AND parenttype = 'WF Roadmap'""")
                
                if existing_levels[0]['count'] > 0:
                    frappe.db.sql(f"""DELETE FROM `tabWF Level Setup` 
                                     WHERE parent = '{doc_rec}' AND parentfield = 'wf_level_setup' AND parenttype = 'WF Roadmap'""")
                
                frappe.db.commit()  #c                
        except Exception as e:
            frappe.log_error("add role to wf requestors - deletion error", str(e))
   
        roadmap_doc = frappe.get_doc("WF Roadmap", doc_rec)
        
        # Set workflow levels if approvers exist
        if approvers_section:
            roadmap_doc.workflow_levels = max(level['level'] for level in approvers_section)
        
        # Batch process requestors with role activation
        roles_to_activate = set()  # Use set to avoid duplicate role activations
        
        for single_requestor in requestors_section:
            if single_requestor["requestor"]:
                roles_to_activate.add(single_requestor["requestor"])
                roadmap_doc.append("wf_requestors", single_requestor)
        
        for single_approver in approvers_section:
            if single_approver["role"]:
                roles_to_activate.add(single_approver["role"])
                roadmap_doc.append("wf_level_setup", single_approver)
        
        # Activate permissions for all unique roles at once
        for role in roles_to_activate:
            activating_perms(doctype=doctype, role=role)
        
        roadmap_doc.save(ignore_permissions=True)
        
        # Optimize form definition update
        workflow_from_defs = frappe.db.get_value("Ezy Form Definitions", doctype, "form_json")
        fields_from_defs = literal_eval(workflow_from_defs)["fields"]
        child_table_fields = literal_eval(workflow_from_defs)["child_table_fields"]
        
        field_with_workflow = {
            "fields": fields_from_defs,
            "workflow": workflow_setup,
            "child_table_fields": child_table_fields
        }
        
        frappe.db.set_value("Ezy Form Definitions", doctype, {
            "form_json": str(field_with_workflow).replace("'", '"').replace("None", "null")
        })
        
        frappe.db.commit()  # Final commit for all operations
        
        return {"success": True, "message": "Workflow setup completed successfully"}
        
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error("Error in Updating Roadmap's requestors and approvers in Workflow.",
                         "line No:{}\n{}".format(exc_tb.tb_lineno, str(e)))
        frappe.db.rollback()
        frappe.throw(str(e))
        return {"success": False, "message": str(e)}