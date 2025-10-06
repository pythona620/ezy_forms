import frappe

@frappe.whitelist(allow_guest=True)
def get_reports_list():
    """
    Fetches all reports from 'Report' and 'Ezy Form Definitions' doctypes.
    Each entry will include a 'source' field indicating its origin.
    """
    # Get all reports in the module
    reports = frappe.get_all(
        "Report",
        filters={"module": "ezy_custom_forms"},
        fields=["name"]
    )

    # Add a 'source' key for identification
    reports = [{"name": r["name"], "source": "report"} for r in reports]

    # Get all Ezy Form Definitions where report_fields is not empty
    ezy_form_reports = frappe.get_all(
        "Ezy Form Definitions",
        filters={"report_fields": ["!=", ""]},
        fields=["name"]
    )

    # Add a 'source' key for identification
    ezy_form_reports = [{"name": r["name"], "source": "ezy_form_definition"} for r in ezy_form_reports]

    # Combine both lists
    reports.extend(ezy_form_reports)

    return reports
