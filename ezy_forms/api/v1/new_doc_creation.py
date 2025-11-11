import frappe


def get_request_form_data():
    """Extract request body as dict or form_dict"""
    raw = frappe.local.form_dict.data or frappe.safe_decode(frappe.local.request.get_data())
    try:
        return frappe.parse_json(raw)
    except ValueError:
        return frappe.local.form_dict


@frappe.whitelist(methods=["POST", "PUT", "DELETE"])
def new_doc_creation(doctype, name=None):
    """
    Generic API for creating, updating, and deleting documents.

    - POST   → Create new doc
    - PUT    → Update existing doc
    - DELETE → Delete existing doc
    """

    method = frappe.local.request.method
    data = get_request_form_data() or {}

    # --- validations ---
    if not doctype:
        return _error("Please provide doctype")

    if not frappe.db.exists("DocType", doctype):
        return _error(f"DocType '{doctype}' does not exist")

    if method in ("POST", "PUT") and not isinstance(data, dict):
        return _error("Data should be in dictionary format")

    if method in ("PUT", "DELETE") and not name:
        return _error("Please provide document name")

    # --- main logic ---
    try:
        if method == "POST":
            return _create_doc(doctype, data)

        if method == "PUT":
            return _update_doc(doctype, name, data)

        if method == "DELETE":
            return _delete_doc(doctype, name)

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "new_doc_creation error")
        return _error(str(e))


# ----------------------------
# Helpers
# ----------------------------

def _create_doc(doctype, data):
    doc = frappe.get_doc({"doctype": doctype})
    doc.update(data)
    doc.insert(ignore_permissions=True)
    frappe.db.commit()
    return {"success": True, "data": doc.as_dict()}


def _update_doc(doctype, name, data):
    doc = frappe.get_doc(doctype, name, for_update=True)
    data.pop("flags", None)  # avoid overwriting internal flags

    doc.update(data)
    doc.save()

    if frappe.get_system_settings("apply_perm_level_on_api_calls"):
        doc.apply_fieldlevel_read_permissions()

    # if updating child table, save parent too
    if doc.get("parenttype"):
        frappe.get_doc(doc.parenttype, doc.parent).save()

    frappe.db.commit()
    return {"success": True, "data": doc.as_dict()}


def _delete_doc(doctype, name):
    frappe.delete_doc(doctype, name, ignore_missing=False)
    frappe.db.commit()
    return {"success": True, "message": "Document deleted", "http_status": 202}


def _error(message):
    return {"success": False, "message": message}
