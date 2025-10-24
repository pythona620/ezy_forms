# Copyright (c) 2025, bharath and contributors
# For license information, please see license.txt


from frappe.model.document import Document
import frappe
from frappe.utils import nowdate, nowtime,get_url
from frappe.utils.file_manager import get_files_path
from calendar import month_abbr
import jwt
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
import secrets,requests,json
class DoctypesDatabaseLogs(Document):
	def before_save(self):
		# Ensure numeric fields are stored as float
		self.total_storage = float(self.total_storage or 0)
		self.free_stroage = float(self.free_stroage or 0)
		self.subscribtion_stroage = float(self.subscribtion_stroage or 0)


@frappe.whitelist()
def create_doctypes_db_log():
	try:
		site_name = f"{get_url()}/"
		today = nowdate()
		year = today.split("-")[0]
		month_num = int(today.split("-")[1])
		month = month_abbr[month_num].upper()
		creation_time = nowtime()

		# ✅ Modules to track
		target_modules = [
			"User Forms",
			"ezy_custom_forms",
			"Form Templates",
			"Ezy Forms",
			"Ezy Flow",
			"ezy_forms"
		]

		# --- Get all doctypes in target modules ---
		doctypes = frappe.get_all(
			"DocType",
			filters={"module": ["in", target_modules]},
			fields=["name", "module"]
		)

		# --- Get or create parent record ---
		parent_name = frappe.db.exists("Doctypes Database Logs", {
			"site_name": site_name,
			"year": year,
			"month": month
		})
		if parent_name:
			parent_doc = frappe.get_doc("Doctypes Database Logs", parent_name)
		else:
			parent_doc = frappe.get_doc({
				"doctype": "Doctypes Database Logs",
				"site_name": site_name,
				"year": year,
				"month": month,
				"last_modified_on": today,
				"total_storage": 0,
				"subscribtion_stroage":10240
			})
			parent_doc.insert(ignore_permissions=True)

		total_storage_sum = 0

		# --- Loop through each doctype and calculate DB + File size ---
		for dt in doctypes:
			table_name = f"tab{dt['name']}"

			# --- DB size per doctype ---
			db_result = frappe.db.sql(
				"""
				SELECT ROUND(SUM(data_length + index_length)/1024/1024, 2) AS db_size
				FROM information_schema.tables
				WHERE table_schema = %s AND table_name = %s
				""",
				(frappe.conf.db_name, table_name),
				as_dict=True
			)
			db_size = db_result[0]["db_size"] if db_result and db_result[0]["db_size"] else 0

			# --- File size per doctype (attached files only) ---
			file_result = frappe.db.sql(
				"""
				SELECT ROUND(SUM(file_size)/1024/1024,2) AS file_size
				FROM `tabFile`
				WHERE attached_to_doctype = %s
				""",
				dt['name'],
				as_dict=True
			)
			file_size = file_result[0]["file_size"] if file_result and file_result[0]["file_size"] else 0

			total_size = round(db_size + file_size, 2)
			total_storage_sum += total_size

			# --- Check if a record for this date & doctype already exists ---
			existing_row = next((row for row in parent_doc.daily_doctypes_db_logs if str(row.date) == str(today) and row.doctype_name == dt["name"]),None)

			if existing_row:
				# ✅ Update existing row
				existing_row.db_size = db_size
				existing_row.file_size = file_size
				existing_row.total_size = total_size
				existing_row.creation_time = creation_time
				existing_row.subscribtion_end = 0 if total_storage_sum - int(parent_doc.subscribtion_stroage) < 0 else 1
			else:
				# ✅ Add new row
				parent_doc.append("daily_doctypes_db_logs", {
					"date": today,
					"module": dt["module"],
					"doctype_name": dt["name"],
					"db_size": db_size,
					"file_size": file_size,
					"total_size": total_size,
					"creation_time": creation_time,
					"subscribtion_end": 0 if total_storage_sum - int(parent_doc.subscribtion_stroage) < 0 else 1
				})

		# --- Workflow summary data ---
		data = frappe.db.sql("""
			SELECT
				doctype_name AS form_name,
				property,
				COUNT(DISTINCT CASE WHEN status IN ('Request Raised', 'In Progress') THEN name END) AS in_progress,
				COUNT(DISTINCT CASE WHEN status = 'Completed' THEN name END) AS form_approved,
				COUNT(DISTINCT CASE WHEN status = 'Request Cancelled' THEN name END) AS form_rejected
			FROM `tabWF Workflow Requests`
			GROUP BY doctype_name, property
		""", as_dict=True)

		# --- Refresh the form_requests child table ---
		parent_doc.set("form_requests", [])
		for row in data:
			parent_doc.append("form_requests", {
				"form_name": row.form_name,
				"property": row.property,
				"in_progress": row.in_progress or 0,
				"form_approved": row.form_approved or 0,
				"form_rejected": row.form_rejected or 0
			})

		# --- Compute total & free storage ---
		parent_doc.total_storage = round(sum([float(d.total_size or 0) for d in parent_doc.daily_doctypes_db_logs]),2)
		parent_doc.free_stroage = round((float(parent_doc.subscribtion_stroage) - float(parent_doc.total_storage)), 2)

		# --- Mark overdue if exceeded ---
		if parent_doc.free_stroage < 0:
			parent_doc.over_due_on = today

		parent_doc.last_modified_on = today
		parent_doc.save(ignore_permissions=True)
		# generate_jwt_token(parent_doc.name)
		frappe.db.commit()

		return f" DB Logs created/updated for {site_name} — {len(doctypes)} doctypes processed"

	except Exception:
		frappe.log_error(frappe.get_traceback(), "Database Log Scheduler Error")
		return " Error while creating logs"




import json
@frappe.whitelist(allow_guest=True,methods=['GET'])
@frappe.read_only()
def jwt_token_method():
	
	try:
		data = json.loads(frappe.request.data)
		jwt_token = data.get("jwt_token")
		secret_key = data.get("secret_key") 
		decoded_payload = jwt.decode(
			jwt_token,
			secret_key,
			algorithms=["HS256"]
		)
		user_id = decoded_payload.get('user_id')
		site_name = decoded_payload.get('site_name')
		subscription_start_date = decoded_payload.get('subscription_start_date')
		subscription_storage = decoded_payload.get('subscribtion_stroage')
		subscription_end_date = decoded_payload.get('subscription_end_date')
		
		if user_id == "caratRED" and site_name.rstrip("/") == get_url().rstrip("/"):
			if not frappe.db.exists("Doctypes Database Logs",{"site_name": site_name}):
				frappe.log_error(message= "Record does not exist for the Doctypes Database Logs",title="Record does not exist")
				return {"status": "failed", "message": "Record does not exist","status_code": 404}
			frappe.db.set_value("Doctypes Database Logs",{"site_name": site_name},"subscribtion_stroage",subscription_storage)
			frappe.db.set_value("Global Site Settings",	"Global Site Settings",{"subscription_end_date": subscription_end_date,"subscription_start_date": subscription_start_date})
			frappe.db.commit()
			return {"status": "success", "message": "Subscription data updated successfully","status_code": 200}
		
		return {"status": "failed", "message": "Invalid user or site","status_code": 404}

	except ExpiredSignatureError:
		return {"status": "error", "message": "Token has expired","status_code": 404}
	except InvalidTokenError:
		return {"status": "error", "message": "Invalid token","status_code": 404}
	except Exception as e:
		frappe.log_error(frappe.get_traceback(), "JWT Token Method Error")
		return {"status": "error", "message": str(e),"status_code": 404}


@frappe.whitelist()
def generate_jwt_token(record):
    site_name = "Local IP"
    doc = frappe.get_doc("Doctypes Database Logs", record).as_dict()
    excluded_fields = {
        "owner", "creation", "modified", "modified_by",
        "docstatus", "idx", "name", "parentfield",
        "parent", "parenttype"
    }
    def clean_and_serialize(value):
        """Recursively clean unwanted fields and serialize dates/times."""
        if isinstance(value, dict):
            return {
                k: clean_and_serialize(v)
                for k, v in value.items()
                if k not in excluded_fields
            }
        elif isinstance(value, list):
            return [clean_and_serialize(v) for v in value]
        else:
            return str(value)
    serializable_doc = clean_and_serialize(doc)
    secret_key = secrets.token_hex(12)
    payload = {
        "user_id": "caratRED",
        "doc": serializable_doc
    }

    token = jwt.encode(payload, secret_key, algorithm="HS256")

    site_url = site_name.rstrip("/") + "/"
    url = f"{site_url}api/method/tax_deductions.tax_deductions.doctype.sites.sites.get_site_details"

    data = {
        "jwt_token": token,
        "secret_key": secret_key,
    }

    try:
        # Use json= to send JSON body in a GET is incorrect, so let's use POST if you expect JSON body
        response = requests.get(url, json=data)
        if response.status_code == 200:
            return {
                "status": "success",
                "message": "JWT sent successfully",
                "response": response.json(),
            }
        else:
            frappe.log_error(
                message=f"Failed to send payload to {site_name}\n{response.text}",
                title="generate_jwt_token",
            )
            return {"status": "failed", "message": "Remote site error", "status_code": response.status_code}
    except Exception as e:
        frappe.log_error(message=f"JWT Send Error: {str(e)}", title="generate_jwt_token")
        return {"status": "error", "message": str(e)}
