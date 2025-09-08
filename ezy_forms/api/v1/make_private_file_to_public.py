import shutil
import frappe
import os


def make_file_public_after_insert(doc, method=None):
    if doc.is_private:
        # Extract the filename
        filename = os.path.basename(doc.file_url)
 
        # Construct full source and target paths
        private_path = frappe.get_site_path("private", "files", filename)
        public_path = frappe.get_site_path("public", "files", filename)
 
        # Ensure the private file exists before moving
        if os.path.exists(private_path):
            shutil.move(private_path, public_path)
 
            # Update file doc
            doc.db_set("is_private", 0)
            doc.db_set("file_url", f"/files/{filename}")
        else:
            frappe.log_error(f"File not found at {private_path}", "make_file_public_after_insert Error")
            frappe.throw(f"Private file {filename} does not exist.")
