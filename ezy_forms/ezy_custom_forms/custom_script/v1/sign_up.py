import frappe
from frappe.website.utils import get_home_page, is_signup_disabled
from frappe.utils import escape_html
from frappe import _
 
@frappe.whitelist(allow_guest=True)
def sign_up(email: str, full_name: str, redirect_to: str|None) -> tuple[int, str]:
    if is_signup_disabled():
        frappe.throw(_("Sign Up is disabled"), title=_("Not Allowed"))
 
    user = frappe.db.get("User", {"email": email})
    if user:
        if user.enabled:
            return  _("Already Registered")
        else:
            return  _("Registered but disabled")
    else:
        if frappe.db.get_creation_count("User", 60) > 300:
            frappe.respond_as_web_page(
                _("Temporarily Disabled"),
                _(
                    "Too many users signed up recently, so the registration is disabled. Please try back in an hour"
                ),
                http_status_code=429,
            )
 
        from frappe.utils import random_string
 
        user = frappe.get_doc(
            {
                "doctype": "User",
                "email": email,
                "first_name": escape_html(full_name),
                "enabled": 0,
                'send_welcome_email': 0,
                "new_password": random_string(10),
                "user_type": "Website User",
            }
        )
        user.flags.ignore_permissions = True
        user.flags.ignore_password_policy = True
        user.insert()
 
        # set default signup role as per Portal Settings
        default_role = frappe.db.get_single_value("Portal Settings", "default_role")
        if default_role:
            user.add_roles(default_role)
 
        if redirect_to:
            frappe.cache.hset("redirect_after_login", user.name, redirect_to)
    return 2, _("Please contact your IT Manager to verify your sign-up")
 
 
 
 
 
@frappe.whitelist()
def employee_creation(self, method):
    company_field = frappe.get_all("Ezy Business Unit",fields = ['name'])
    company = company_field[0].name
    if self and hasattr(self, "email"):
        if not frappe.db.exists("Ezy Employee", {"emp_mail_id": self.email}):
            doc = frappe.new_doc("Ezy Employee")
            doc.update({
                "emp_name": self.username.replace('_'," ") if self.username else self.first_name,
                "emp_mail_id": self.email,
                "company_field":company,
                "enable":0,
            })
            doc.insert(ignore_permissions=True)
            frappe.db.commit()
 