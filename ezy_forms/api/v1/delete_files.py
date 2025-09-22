import frappe
import os

@frappe.whitelist(methods=["Post"])
@frappe.read_only()
def delete_files_api(unwanted_files):
    for file_name in unwanted_files:
        try:
            # Get the File doc by name
            file_doc = frappe.get_doc("File", file_name)

            # Construct full path to the file on disk
            if file_doc.file_url:
                # Remove leading slash to avoid double-slashing in path
                relative_path = file_doc.file_url.lstrip("/")
                full_path = frappe.get_site_path("public", relative_path)

                # Delete the physical file if it exists
                if os.path.isfile(full_path):
                    os.remove(full_path)
                    frappe.logger().info(f"Deleted file from disk: {full_path}")
                else:
                    frappe.logger().warning(f"File not found: {full_path}")

            # Delete the File doc (database entry)
            frappe.delete_doc("File", file_name, force=True)

        except Exception as e:
            frappe.log_error(frappe.get_traceback(), f"Error deleting file: {file_name}")
            frappe.msgprint(f"Could not delete file {file_name}: {str(e)}")
