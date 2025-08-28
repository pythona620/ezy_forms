import frappe
import sys
import traceback
from frappe.website.doctype.website_settings.website_settings import get_website_settings
from frappe.website.context import get_context



@frappe.whitelist(allow_guest=True)
def getting_auth_url():
    try:
        context = get_website_settings()
        for_getting_context_from_auth_url = get_context(context)
        auth_url = for_getting_context_from_auth_url.get("provider_logins")
        return {"success": True, "message": auth_url}
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        frappe.log_error(
            "Error In Getting Auth URL.",
            "line No:{}\n{}".format(exc_tb.tb_lineno, traceback.format_exc())
        )
        return {"success": False, "error": str(e)}
	