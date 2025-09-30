import frappe
from frappe.model.db_query import DatabaseQuery
@frappe.whitelist(methods=["GET"])
def get_employee_accessible_forms(designation: str = None, fields = None, property: str = None, department: str = None):
    # Fetch roadmaps directly
    if not property:
        return "Property value missing"
    roadmaps = DatabaseQuery(
        "WF Roadmap").execute(
        filters={"property": property},
        fields=["name", "document_type"]
    )
    if not roadmaps:
        return "NO Roadmap Recorded"

    roadmap_map = {r["name"]: r["document_type"] for r in roadmaps}

    # Fetch requestors in one go
    req_filters = {"parent": ["in", list(roadmap_map.keys())]}
    if designation:
        req_filters["requestor"] = designation

    requestors = frappe.get_all("WF Requestors", filters=req_filters, fields=["parent"])
    valid_roadmap_names = {r["parent"] for r in requestors}

    # Get document types for valid roadmaps
    document_types = [roadmap_map[name] for name in valid_roadmap_names if name in roadmap_map]
    if not document_types:
        return []

    # Prepare filters for Ezy Form Definitions
    filters = {
        "form_short_name": ["in", document_types],
        "enable":1,
        "business_unit": property
    }
    if department:
        filters["owner_of_the_form"] = department

    # Fetch and return forms
    return  DatabaseQuery("Ezy Form Definitions").execute( filters=filters, fields=fields)
