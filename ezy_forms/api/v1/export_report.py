import frappe
from frappe.desk.query_report import run, format_duration_fields, build_xlsx_data
from frappe.desk.utils import get_csv_bytes, pop_csv_params, provide_binary_file
from frappe import _

@frappe.whitelist()
def export_report_data(report_name=None, file_format_type=None, form_params=None, filters=None):
	# Optional: override for testing
	if not report_name or not file_format_type:
		return "required file name and file formate (xlsx or csv)"
	

	# Ensure form_params is a dictionary
	if isinstance(form_params, str):
		import json
		form_params = json.loads(form_params)
	if form_params is None:
		form_params = {}

	data = run(report_name, form_params, custom_columns=[], are_default_filters=False)
	data = frappe._dict(data)
	data.filters = form_params.get("applied_filters")

	if not data.get("columns"):
		frappe.respond_as_web_page(
			_("No data to export"),
			_("You can try changing the filters of your report."),
		)
		return

	format_duration_fields(data)

	# Safe defaults
	visible_idx = []  # Fix: must be a list, not None
	include_indentation = False
	

	xlsx_data, column_widths = build_xlsx_data(
		data, visible_idx, include_indentation
	)

	if file_format_type == "Csv":
		csv_params = pop_csv_params(form_params)
		content = get_csv_bytes(xlsx_data, csv_params)
		file_extension = "csv"
	elif file_format_type == "Excel":
		from frappe.utils.xlsxutils import make_xlsx
		file_extension = "xlsx"
		content = make_xlsx(xlsx_data, "Query Report", column_widths=column_widths).getvalue()
	else:
		frappe.throw(_("Invalid file format type"))

	provide_binary_file(report_name, file_extension, content)
