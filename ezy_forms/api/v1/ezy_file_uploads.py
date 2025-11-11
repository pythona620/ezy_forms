import frappe
from frappe import _
from frappe.utils import cint
from typing import TYPE_CHECKING
from mimetypes import guess_type
from frappe import is_whitelisted
from frappe.utils.image import optimize_image
from frappe.handler import check_write_permission


if TYPE_CHECKING:
    from frappe.core.doctype.user.user import User


# Safe MIME types - removed dangerous types like SQL, ZIP, and PKCS12
ALLOWED_MIMETYPES = (
    "image/png",
    "image/jpeg",
    "image/gif",
    "application/pdf",
    "application/msword",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "application/vnd.ms-excel",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "application/vnd.oasis.opendocument.text",
    "application/vnd.oasis.opendocument.spreadsheet",
    "text/plain",
    "text/csv",
    "video/quicktime",
    "video/mp4"
)

# Maximum file size: 10MB
MAX_FILE_SIZE = 10 * 1024 * 1024

# Hardcoded safe extensions - do not allow dangerous extensions
# Removed: .sql, .zip, .exe, .sh, .bat, .pgp, .p12
SAFE_EXTENSIONS = {
    'jpg', 'jpeg', 'png', 'gif',  # Images
    'pdf',  # PDF documents
    'doc', 'docx',  # Word documents
    'xls', 'xlsx', 'csv',  # Spreadsheets
    'txt',  # Text files
    'odt', 'ods',  # OpenDocument
    'mp4', 'mov'  # Videos
}

# Fetch allowed extensions from database but filter against safe list
extensions_str = frappe.db.get_value("Ezy File Extensions", "Ezy File Extensions", "allowed_extensions") or ""
db_extensions = {ext.replace(" ", "").lower() for ext in extensions_str.split(",") if ext.strip()}

# Only allow extensions that are in both the database config AND the safe list
ALLOWED_EXTENSIONS = SAFE_EXTENSIONS if not db_extensions else (SAFE_EXTENSIONS & db_extensions)


def is_allowed_file(filename):
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )

@frappe.whitelist()
def custom_upload_file():
    """
    Custom file upload with security validations.
    Requires authentication - guest uploads are disabled for security.
    """
    # Require authentication
    if frappe.session.user == "Guest":
        frappe.throw("Authentication required for file uploads", frappe.AuthenticationError)

    user: "User" = frappe.get_doc("User", frappe.session.user)

    files = frappe.request.files
    is_private = frappe.form_dict.is_private
    doctype = frappe.form_dict.doctype
    docname = frappe.form_dict.docname
    fieldname = frappe.form_dict.fieldname
    file_url = frappe.form_dict.file_url
    folder = frappe.form_dict.folder or "Home"
    method = frappe.form_dict.method
    filename = frappe.form_dict.file_name
    optimize = frappe.form_dict.optimize
    content = None

    # Always check write permissions
    check_write_permission(doctype, docname)

    if library_file := frappe.form_dict.get("library_file_name"):
        frappe.has_permission("File", doc=library_file, throw=True)
        doc = frappe.get_value(
            "File",
            frappe.form_dict.library_file_name,
            ["is_private", "file_url", "file_name"],
            as_dict=True,
        )
        is_private = doc.is_private
        file_url = doc.file_url
        filename = doc.file_name

    if "file" in files:
        file = files["file"]
        content = file.stream.read()
        filename = file.filename

        # Validate file size
        if len(content) > MAX_FILE_SIZE:
            frappe.throw(f"File size exceeds maximum allowed size of {MAX_FILE_SIZE / (1024 * 1024):.1f}MB", frappe.ValidationError)

        # Validate file extension
        if not is_allowed_file(filename):
            frappe.throw(f"File type not allowed. Allowed types: {', '.join(sorted(ALLOWED_EXTENSIONS))}", frappe.ValidationError)

        content_type = guess_type(filename)[0]

        # Validate MIME type
        if content_type and content_type not in ALLOWED_MIMETYPES:
            frappe.throw(f"File MIME type '{content_type}' is not allowed", frappe.ValidationError)
        
        if optimize and content_type and content_type.startswith("image/"):
            args = {"content": content, "content_type": content_type}
            if frappe.form_dict.max_width:
                args["max_width"] = int(frappe.form_dict.max_width)
            if frappe.form_dict.max_height:
                args["max_height"] = int(frappe.form_dict.max_height)
            content = optimize_image(**args)

    frappe.local.uploaded_file = content
    frappe.local.uploaded_filename = filename

    # Check allowed extensions
    if not is_allowed_file(filename):
        frappe.log_error(message=f"Extension not allowed: {filename} | Allowed: {ALLOWED_EXTENSIONS}",title="File Upload Error"   )
        frappe.throw("File type not allowed.")

    if content is not None and (frappe.session.user == "Guest" or (user and not user.has_desk_access())):
        filetype = guess_type(filename)[0]
        
        if filetype not in ALLOWED_MIMETYPES:
            frappe.throw(_("You can only upload JPG, PNG, PDF, TXT or Microsoft documents."))

    if method:
        method = frappe.get_attr(method)
        is_whitelisted(method)
        return method()
    else:
        return frappe.get_doc(
            {
                "doctype": "File",
                "attached_to_doctype": doctype,
                "attached_to_name": docname,
                "attached_to_field": fieldname,
                "folder": folder,
                "file_name": filename,
                "file_url": file_url,
                "is_private": cint(is_private),
                "content": content,
            }
        ).save(ignore_permissions=ignore_permissions)
