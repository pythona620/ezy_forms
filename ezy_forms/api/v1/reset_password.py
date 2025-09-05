
import frappe
from frappe.utils import now_datetime, get_url
import hashlib
from frappe import _

def sha256_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()

@frappe.whitelist()
def reset_password(user_email, password_expired=False):
    # Fetch user document
    user = frappe.get_doc("User", user_email)

    # Generate password reset key
    key = frappe.generate_hash()
    hashed_key = sha256_hash(key)

    # Save key and timestamp to user record
    user.db_set("reset_password_key", hashed_key)
    user.db_set("last_reset_password_key_generated_on", now_datetime())

    # Build reset URL
    url = "/update-password?key=" + key
    if password_expired:
        url += "&password_expired=true"

    link = get_url(url)  # 👈 Removed `allow_header_override`

    # Get email sender
    sender = frappe.get_value(
        "Email Account",
        {"enable_outgoing": 1, "default_outgoing": 1},
        "email_id"
    )

    # Get system email template if any
    reset_password_template = frappe.db.get_system_setting("reset_password_template")

    # Send email
    frappe.sendmail(
        recipients=user_email,
        subject=_("Password Reset"),
        template="password_reset",
        args={"link": link},
        now=True,
        sender=sender
    )

    return {"message": "Password reset email sent", "link": link}

