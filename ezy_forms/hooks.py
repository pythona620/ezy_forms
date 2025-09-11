app_name = "ezy_forms"
app_title = "ezy_forms"
app_publisher = "bharath"
app_description = "ezy_forms"
app_email = "bharath@gmail.com"
app_license = "mit"

# Apps
# ------------------

# required_apps = []

# Each item in the list will be shown as an app in the apps page
# add_to_apps_screen = [
# 	{
# 		"name": "ezy_forms",
# 		"logo": "/assets/ezy_forms/logo.png",
# 		"title": "ezy_forms",
# 		"route": "/ezy_forms",
# 		"has_permission": "ezy_forms.api.permission.has_app_permission"
# 	}
# ]
after_install = "ezy_forms.api.v1.default_mail_templates.email_template_create"
after_migrate = ["ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions.activating_perms_for_all_roles_in_wf_roadmap"]
# Includes in <head>
# ------------------
on_session_creation = "ezy_forms.ezy_forms.doctype.ezy_employee.ezy_employee.employee_last_login_activate"
# include js, css files in header of desk.html
# app_include_css = "/assets/ezy_forms/css/ezy_forms.css"
# app_include_js = "/assets/ezy_forms/js/ezy_forms.js"

# include js, css files in header of web template
# web_include_css = "/assets/ezy_forms/css/ezy_forms.css"
# web_include_js = "/assets/ezy_forms/js/ezy_forms.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ezy_forms/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
webform_include_js = {
    "emc-articles-creation-approval-form":"ezy_forms.ezy_forms.public.web_form_list.js"
    }
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "ezy_forms/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "ezy_forms.utils.jinja_methods",
# 	"filters": "ezy_forms.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "ezy_forms.install.before_install"
# after_install = "ezy_forms.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "ezy_forms.uninstall.before_uninstall"
# after_uninstall = "ezy_forms.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "ezy_forms.utils.before_app_install"
# after_app_install = "ezy_forms.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "ezy_forms.utils.before_app_uninstall"
# after_app_uninstall = "ezy_forms.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ezy_forms.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
"Ezy Employee":{
        "after_insert":"ezy_forms.ezy_forms.doctype.ezy_employee.ezy_employee.set_reporting_to_and_designation"
    },
# "NICO MOD REPORT":{
#     "after_insert":"ezy_forms.ezy_custom_forms.custom_script.mail.email_pdf_send"
#     },
# "NICO ROOM CHECK LIST":{
#     "after_insert":"ezy_forms.ezy_custom_forms.custom_script.mail.email_pdf_send"
#     },
"File":{
    "after_insert":"ezy_forms.api.v1.make_private_file_to_public.make_file_public_after_insert"
},
"Role": {
        "after_insert": "ezy_forms.api.v1.custom_role_permission.assign_custom_permissions"    
}
}

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ezy_forms.tasks.all"
# 	],
# 	"daily": [
# 		"ezy_forms.tasks.daily"
# 	],
# 	"hourly": [
# 		"ezy_forms.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ezy_forms.tasks.weekly"
# 	],
# 	"monthly": [
# 		"ezy_forms.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "ezy_forms.install.before_tests"

# Overriding Methods
# ------------------------------
#
override_whitelisted_methods = {
    # "frappe.desk.doctype.event.event.get_events": "ezy_forms.event.get_events"
"frappe.core.doctype.user.user.sign_up":"ezy_forms.api.v1.sign_up.sign_up",
"upload_file": "ezy_forms.api.v1.ezy_file_uploads.custom_upload_file",
}
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ezy_forms.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["ezy_forms.utils.before_request"]
# after_request = ["ezy_forms.utils.after_request"]

# Job Events
# ----------
# before_job = ["ezy_forms.utils.before_job"]
# after_job = ["ezy_forms.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ezy_forms.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }


# website_route_rules = [{'from_route': '/UserManagement/<path:app_path>', 'to_route': 'UserManagement'},]

website_redirects = [
    {"source": "/fr", "target": "/ezyformsfrontend"},
    {"source": "/user", "target": "/UserManagement"}
]