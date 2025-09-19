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

        if not workflow_setup or not business_unit or not doctype:
            return {"success": False, "message": "Please pass levels or requestors for adding Workflow Level Setup."}

        # Generate Roadmap doc name
        doc_rec = "_".join(business_unit.split()).upper() + "_" + "_".join(doctype.split()).upper()

        # Explode rows by role (flatten roles list/string into multiple rows)
        exploded_data = [
            {**row, "roles": role}
            for row in workflow_setup
            for role in (
                row["roles"] if isinstance(row.get("roles"), list)
                else [row["roles"]] if isinstance(row.get("roles"), str)
                else []
            )
        ]

        # Convert fields list into dict with ones
        for row in exploded_data:
            if isinstance(row.get("fields"), list):
                row["fields"] = {str(f): 1 for f in row["fields"]}

        # Separate requestors and approvers
        requestors_section = [
            {"requestor": row["roles"], "columns_allowed": row.get("fields")}
            for row in exploded_data if "requestor" in str(row.get("type", "")).lower()
        ]

        approvers_section = [
            {
                "role": row["roles"],
                "columns_allowed": row.get("fields"),
                "level": row.get("idx"),
                "cancel_request": 1,
                "mandatory": 1,
                "action": "Approve/Reject",
                "view_only_reportee": row.get("view_only_reportee"),
                "requester_as_a_approver": row.get("requester_as_a_approver"),
                "all_approvals_required": row.get("all_approvals_required"),
                "on_rejection": row.get("on_rejection"),
            }
            for row in exploded_data if "approver" in str(row.get("type", "")).lower()
        ]

        # Delete existing requestors/levels if any
        try:
            frappe.db.sql(
                """DELETE FROM `tabWF Requestors`
                   WHERE parent=%s AND parentfield='wf_requestors' AND parenttype='WF Roadmap'""",
                (doc_rec,),
            )
            frappe.db.sql(
                """DELETE FROM `tabWF Level Setup`
                   WHERE parent=%s AND parentfield='wf_level_setup' AND parenttype='WF Roadmap'""",
                (doc_rec,),
            )
            frappe.db.commit()
        except Exception as e:
            frappe.log_error("add role to wf requestors - deletion error", str(e))

        roadmap_doc = frappe.get_doc("WF Roadmap", doc_rec)

        # Set workflow levels
        if approvers_section:
            roadmap_doc.workflow_levels = max(a["level"] for a in approvers_section if a.get("level"))

        # Append requestors & approvers
        roles_to_activate = set()
        for r in requestors_section:
            if r["requestor"]:
                roles_to_activate.add(r["requestor"])
                roadmap_doc.append("wf_requestors", r)

        for a in approvers_section:
            if a["role"]:
                roles_to_activate.add(a["role"])
                roadmap_doc.append("wf_level_setup", a)

        # Activate permissions once per unique role
        for role in roles_to_activate:
            activating_perms(doctype=doctype, role=role)

        roadmap_doc.save(ignore_permissions=True)

        # Update form definition
        workflow_from_defs = frappe.db.get_value("Ezy Form Definitions", doctype, "form_json")
        parsed_defs = literal_eval(workflow_from_defs)
        field_with_workflow = {
            "fields": parsed_defs.get("fields", []),
            "workflow": workflow_setup,
            "child_table_fields": parsed_defs.get("child_table_fields", []),
        }
        frappe.db.set_value("Ezy Form Definitions", doctype, {
            "form_json": str(field_with_workflow).replace("'", '"').replace("None", "null")
        })

        frappe.db.commit()
        return {"success": True, "message": "Workflow setup completed successfully"}

    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error(
            "Error in Updating Roadmap's requestors and approvers in Workflow.",
            f"line No:{exc_tb.tb_lineno}\n{str(e)}"
        )
        frappe.db.rollback()
        frappe.throw(str(e))
        return {"success": False, "message": str(e)}
