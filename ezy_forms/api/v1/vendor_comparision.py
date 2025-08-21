import frappe
from ezy_forms.api.v1.vendor_comparision_template import preview_dynamic_form
import json




@frappe.whitelist()
def vendor_comparision_api(doctype_name, form_id,business_unit=None):
    business_unit="CRR"
    fields = [
        "name", "vendor_name", "gst_number", "phone_number", "mail_id",
        "pricing_details", "transportation_charges", "delivery_time",
        "payment_terms", "biddle_rank", "remark", "total_value", "address",
        "cgst_percent", "utgst_percent", "cgst_amount", "utgst_amount", "igst_percent",
        "igst_amount", "transportation_gst_percent", "transportation_gst_amount","additional_charges", "grand_total"
    ]
    business_unit = frappe.get_doc("Ezy Business Unit", business_unit)
    # Fetch vendor comparison info
    vendor_comparison = frappe.db.get_value(
        doctype_name,
        form_id,
        ["requested_by", "requested_on", "wf_generated_request_id", "name", "company_field","approver_2","approver_1","approver","approved_by_2","approved_by_1","approved_by"],
        as_dict=True
    )

    # Fetch workorder details (only L1 rank)
    workorder_details_list = frappe.get_all(
        "Vendor Details",
        filters={
            'parent': form_id,
            "parenttype": doctype_name,
            "parentfield": "vendor_details",
            "biddle_rank": "L1"
        },
        fields=fields
    )

    workorder_details = {}
    
    if workorder_details_list:
        workorder_details = frappe.db.get_value(
            "Vendor Details",
            workorder_details_list[0].name,
            fields,
            as_dict=True
        )

    # Merge both dicts
    result = {
        "letter_head": business_unit.letter_head,
        "company_logo": business_unit.bu_logo,
        **vendor_comparison,
        **workorder_details
    }

    # Convert pricing_details JSON string → dict
    if result.get("pricing_details"):
        try:
            result["pricing_details"] = json.loads(result["pricing_details"])
        except Exception:
            # in case it's not valid JSON, just keep original string
            pass
	# return result
    return preview_dynamic_form(form_data=result,form_short_name=doctype_name)