import pandas as pd
from urllib.parse import urlparse
import frappe
from frappe.utils import add_to_date
import ast
from frappe.utils.background_jobs import enqueue
import string
import numpy as np
import random
import sys, traceback, time
from ezy_forms.api.v1.delete_files import delete_files_api
import os
from ezy_forms.api.v1.send_an_email import sending_mail_api





@frappe.whitelist()
def raising_requests_to_enqueue(
module_name,
doctype_name,
ids:list,
reason, url_for_request_id, 
files:list,
property=None,
cluster=None, 
reference_doctype=None,
ip_address=None,
employee_id=None,
is_linked=None, 
be_half_of=None, 
bulk= None,
request_for=None,
unwanted_files=[]
):
	try:
		# Input validation
		if not ids or not isinstance(ids, list):
			return {"success": False, "message": "No valid account IDs provided"}
		
		if not property and not cluster:
			return {"success": False, "message": "Either property or cluster must be provided"}
		
		# Initialize variables
		current_time =add_to_date(None, as_datetime=True)
		timestamp = f"{current_time.year}/{current_time.month}/{current_time.day} {current_time.hour}:{current_time.minute}:{current_time.second}:{current_time.microsecond}"
		
		# Get workflow configuration
		workflow_config = get_workflow_configuration(module_name, doctype_name, property, cluster)
		if not workflow_config["success"]:
			return workflow_config
		
		roadmap_title, doctype_field, members_having_mails = workflow_config["data"]
		
		# Get next level roles
		next_level_roles = get_next_level_roles(members_having_mails)
		
		# Validate and process account IDs
		validation_result = validate_account_ids(ids, doctype_name, doctype_field, property, cluster)
		if not validation_result["success"]:
			return validation_result
		if len(unwanted_files)>0:
			enqueue(
				method=delete_files_api,
				unwanted_files=unwanted_files
				)
		# Process request based on bulk flag
		if bulk is None:  # Individual requests
			return process_individual_requests(
				ids, doctype_name, doctype_field, property, cluster, reason,
				roadmap_title, url_for_request_id, ip_address, employee_id, 
				be_half_of, is_linked, timestamp
			)
		else:  # Bulk request
			return process_bulk_request(
				ids, doctype_name, doctype_field, property, cluster, reason,
				roadmap_title, url_for_request_id, ip_address, employee_id, 
				be_half_of, is_linked, timestamp
			)
			
	except Exception as e:
		frappe.log_error(
			title="Error in raising_requests_to_enqueue",
			message=f"Error: {str(e)}\n{frappe.get_traceback()}"
		)
		return {"success": False, "error": str(e)}



def get_workflow_configuration(module_name, doctype_name, property, cluster):
	"""Get workflow configuration and roadmap details"""
	try:
		# Build roadmap title
		if property:
			roadmap_title = f"{'_'.join(property.split()).upper()}_{'_'.join(doctype_name.split()).upper().replace(' ', '_')}"
		elif cluster:
			roadmap_title = f"{'_'.join(cluster.split()).upper()}_{'_'.join(doctype_name.split()).upper().replace(' ', '_')}"
		
		# Get roadmap members
		try:
			roadmap_doc = frappe.get_doc("WF Roadmap", roadmap_title)
			members_having_mails = roadmap_doc.wf_level_setup
		except frappe.DoesNotExistError:
			return {"success": False, "message": f"Roadmap '{roadmap_title}' not found"}
		
		# Get doctype field configuration
		wf_settings = frappe.get_doc("WF Settings", module_name)
		doctype_field = None
		doctype_found = False
		
		for doc in wf_settings.wf_doctype_and_field:
			if doc.workflow_doctype == doctype_name:
				doctype_field = doc.doctype_field
				doctype_found = True
				break
		
		if not doctype_found:
			return {"success": False, "message": f"Doctype '{doctype_name}' not assigned in WF Settings"}
		
		return {
			"success": True,
			"data": (roadmap_title, doctype_field, members_having_mails)
		}
		
	except Exception as e:
		return {"success": False, "message": f"Configuration error: {str(e)}"}


def get_next_level_roles(members_having_mails):
	"""Extract next level roles from roadmap configuration"""
	roles_with_reportee = [
		role.role for role in members_having_mails 
		if role.level == 1 and role.view_only_reportee == 1
	]
	
	all_roles_level_1 = [
		role.role for role in members_having_mails 
		if role.level == 1
	]
	
	return roles_with_reportee if roles_with_reportee else all_roles_level_1


def validate_account_ids(ids, doctype_name, doctype_field, property, cluster):
	"""Validate account IDs existence and check for existing requests"""
	# Check if accounts exist (batch query)
	existing_accounts = frappe.get_all(
		doctype_name,
		filters={"name": ["in", ids]},
		fields=["name"]
	)
	existing_account_names = {acc.name for acc in existing_accounts}
	
	# Find missing accounts
	missing_accounts = [acc_id for acc_id in ids if acc_id not in existing_account_names]
	if missing_accounts:
		return {
			"success": False,
			"message": f"Accounts not found: {', '.join(missing_accounts[:5])}{'...' if len(missing_accounts) > 5 else ''}"
		}
	
	# Check for existing requests (batch query)
	filter_dict = {"name": ["in", ids]}
	if property:
		filter_dict[doctype_field] = property
	elif cluster:
		filter_dict[doctype_field] = cluster
	
	existing_requests = frappe.get_all(
		doctype_name,
		filters=filter_dict,
		fields=["name", "wf_generated_request_id"]
	)
	
	accounts_with_requests = [
		req.name for req in existing_requests 
		if req.wf_generated_request_id
	]
	
	if accounts_with_requests:
		return {
			"success": False,
			"message": f"Request already exists for accounts: {', '.join(accounts_with_requests[:5])}{'...' if len(accounts_with_requests) > 5 else ''}"
		}
	
	return {"success": True}


def create_workflow_request(doctype_name, property, cluster, child_ids, reason, ip_address, employee_id, be_half_of, is_linked):
	"""Create a new workflow request document"""
	doc_data = {
		"doctype": "WF Workflow Requests",
		"doctype_name": doctype_name,
		"reference_id": child_ids,
		"action": reason or 'Request Raised',
		"status": reason or 'Request Raised',
		"ip_address": ip_address,
		"employee_id": employee_id,
		"be_half_of": be_half_of,
		"is_linked_form": is_linked,
		"requester_name": frappe.db.get_value("Ezy Employee", frappe.session.user, "emp_name"),
		"department": frappe.db.get_value("Ezy Employee", frappe.session.user, "department") or 'General'
	}
	
	if property:
		doc_data["property"] = property
	elif cluster:
		doc_data["cluster_name"] = cluster
	
	workflow_request = frappe.get_doc(doc_data)
	workflow_request.insert(ignore_permissions=True)
	frappe.db.commit()
	
	return workflow_request


def create_activity_log(request_id, reason, timestamp):
	"""Create activity log entry for the request"""
	# Get user role
	user_roles = frappe.get_all(
		"Has Role",
		filters={"parent": frappe.session.user},
		fields=["role"]
	)
	user_roles = [role.role for role in user_roles if role.role != "System Manager"]
	employee_role = frappe.db.get_value("Ezy Employee", frappe.session.user, "designation")
	role = employee_role or (user_roles[0] if user_roles else "User")
	
	# Generate unique random string
	random_reference_id = generate_unique_random_string()
	
	# Create activity log
	log_data = [{
		"level": 0,
		"reason": reason,
		"role": role,
		"user": frappe.session.user,
		"time": timestamp,
		"action": reason or 'Request Raised',
		"random_string": random_reference_id
	}]
	
	activity_log = frappe.get_doc({
		"doctype": "WF Activity Log",
		"request_id": request_id,
		"reason": log_data
	})
	activity_log.insert(ignore_permissions=True)
	frappe.db.commit()
	
	return activity_log.name, role


def generate_unique_random_string(length=10):
	"""Generate a unique random string for file references"""
  
	existing_refs = set(frappe.get_all(
		"WF Supporting Documents",
		fields=["reference_id"],
		pluck="reference_id"
	))
	
	while True:
		random_string = ''.join(
			random.choices(
				string.ascii_lowercase + string.ascii_uppercase + string.digits, 
				k=length
			)
		)
		random_string = ''.join(random.sample(random_string, len(random_string)))
		
		if random_string not in existing_refs:
			return random_string


def process_individual_requests(ids, doctype_name, doctype_field, property, cluster, 
							   reason, roadmap_title, url_for_request_id, ip_address, 
							   employee_id, be_half_of, is_linked, timestamp):
	"""Process individual workflow requests"""
	
	for account_id in ids:
		if not account_id.strip():
			continue
			
		# Create child reference
		child_ids = [{"doctype_name_wf": account_id}]
		
		# Create workflow request
		workflow_request = create_workflow_request(
			doctype_name, property, cluster, child_ids, reason,
			ip_address, employee_id, be_half_of, is_linked
		)
		
		request_id = workflow_request.name
		
		# Update source document with request ID
		frappe.db.set_value(
			doctype_name,
			account_id,
			{
				"wf_generated_request_id": request_id,
				"wf_generated_request_status": reason or 'Request Raised'
			}
		)
		
		# Create activity log
		activity_log_id, user_role = create_activity_log(request_id, reason, timestamp)
		
		# Handle auto-approval
		handle_auto_approval(roadmap_title, user_role, doctype_name, request_id, 
						   property, cluster, url_for_request_id)
		
		# Create todos for next level
		create_next_level_todos(doctype_name, request_id, property, cluster, account_id)
		
	
	frappe.db.commit()
	
	# Send notifications
									
	sending_mail_api(request_id=request_id, doctype_name=doctype_name,property= property,cluster= cluster,reason= reason,timestamp= timestamp,skip_user_role= None,user=None )
	
	return {"success": True, "message": reason or 'Request Raised', "request_ids": request_id}


def process_bulk_request(ids, doctype_name, doctype_field, property, cluster,
						reason, roadmap_title, url_for_request_id, ip_address,
						employee_id, be_half_of, is_linked, timestamp):
	"""Process bulk workflow request"""
	# Create child references for all IDs
	child_ids = [{"doctype_name_wf": account_id} for account_id in ids if account_id.strip()]
	
	# Create single workflow request for all IDs
	workflow_request = create_workflow_request(
		doctype_name, property, cluster, child_ids, reason,
		ip_address, employee_id, be_half_of, is_linked
	)
	
	request_id = workflow_request.name
	
	# Update all source documents with request ID
	for account_id in ids:
		if account_id.strip():
			frappe.db.set_value(
				doctype_name,
				account_id,
				{
					"wf_generated_request_id": request_id,
					"wf_generated_request_status": reason or 'Request Raised'
				}
			)
	
	# Create activity log
	activity_log_id, user_role = create_activity_log(request_id, reason, timestamp)
	
	# Handle auto-approval
	handle_auto_approval(roadmap_title, user_role, doctype_name, request_id,
					   property, cluster, url_for_request_id)
	
	# Create todos for next level
	create_next_level_todos(doctype_name, request_id, property, cluster, ids[0])
	
	frappe.db.commit()
	
	# Send notifications
	sending_mail_api(request_id=request_id, doctype_name=doctype_name,property= property,cluster= cluster,reason= reason,timestamp= timestamp,skip_user_role= None,user=None )
	
	return {"success": True, "message": reason or 'Request Raised', "request_id": request_id}


def handle_auto_approval(roadmap_title, user_role, doctype_name, request_id, 
						property, cluster, url_for_request_id):
	"""Handle auto-approval if configured for the user role"""
	auto_approval = frappe.db.get_value(
		"WF Requestors",
		{"parent": roadmap_title, "requestor": user_role},
		"auto_approval"
	)
	
	if auto_approval:
		# Call auto approval function (assuming it exists)
		try:
			frappe.get_attr("ezy_forms.api.v1.ezy_form_rasie_request.auto_approval_after_request_raising")(
				doctype_name, request_id, 
				property=property, 
				cluster_name=cluster,
				current_level=1,
				url_for_approval_id=url_for_request_id
			)
		except Exception as e:
			frappe.log_error(f"Auto-approval failed: {str(e)}", "Auto Approval Error")




@frappe.whitelist()
def combination_of_roadmap_and_request(document_type, request_id, property=None, cluster_name=None):
	try:
		# First for preparing Request table as per roadmap we need to pick the table data
		if property is not None:
			roadmap_title = "_".join(property.split()).upper() + "_" + "_".join(document_type.split()).upper().replace(" ", "_")
		elif cluster_name is not None:
			roadmap_title = "_".join(cluster_name.split()).upper() + "_" + "_".join(document_type.split()).upper().replace(" ", "_")

		roadmap_data = frappe.get_doc("WF Roadmap", roadmap_title).as_dict()
		roadmap_data_wf_level_setup = roadmap_data["wf_level_setup"]

		dataframe_roadmap_wf_level_setup = pd.DataFrame.from_records(roadmap_data_wf_level_setup)
		dataframe_roadmap_wf_level_setup = dataframe_roadmap_wf_level_setup[["level", "idx", "role", "action", "cancel_request", "on_rejection", "mandatory", "escalation_time", 'requester_as_a_approver','view_only_reportee', 'all_approvals_required',"approval_required"]]
		dataframe_roadmap_wf_level_setup = dataframe_roadmap_wf_level_setup.sort_values(['level'], ascending=[True])

		# Now creating the dataframe of request id
		wf_reasons_data = frappe.get_doc("WF Activity Log", request_id).as_dict()
		wf_reasons_data = wf_reasons_data["reason"]

		# Remove duplicate rows for same (level, role) keeping the latest one (by time)
		dataframe_wf_reasons = pd.DataFrame.from_records(wf_reasons_data)
		if not dataframe_wf_reasons.empty:
			dataframe_wf_reasons = dataframe_wf_reasons[['name', 'level', 'role', 'user', 'reason', 'action', 'time']]
			# Convert time to string for sorting (if not already)
			dataframe_wf_reasons['time'] = dataframe_wf_reasons['time'].astype(str)
			# Keep only the latest entry for each (level, role)
			dataframe_wf_reasons = dataframe_wf_reasons.sort_values('time').drop_duplicates(subset=['level', 'role'], keep='last')

		merging_dataframes = pd.merge(
			dataframe_wf_reasons,
			dataframe_roadmap_wf_level_setup,
			how="outer",
			left_on=['level', 'role'],
			right_on=['level', 'role']
		)
		merging_dataframes[['on_rejection', 'cancel_request', 'mandatory', 'requester_as_a_approver','view_only_reportee', 'all_approvals_required',"approval_required"]] = merging_dataframes[
			['on_rejection', 'cancel_request', 'mandatory', 'requester_as_a_approver','view_only_reportee', 'all_approvals_required',"approval_required"]
		].fillna(value=0)

		merging_dataframes.rename(columns={"action_x": "action"}, inplace=True)

		# columns to convert to int datatype
		merging_dataframes["on_rejection"] = merging_dataframes["on_rejection"].astype(int)
		merging_dataframes["cancel_request"] = merging_dataframes["cancel_request"].astype(int)
		merging_dataframes["mandatory"] = merging_dataframes["mandatory"].astype(int)
		merging_dataframes["requester_as_a_approver"] = merging_dataframes["requester_as_a_approver"].astype(int)
		merging_dataframes["view_only_reportee"] = merging_dataframes["view_only_reportee"].astype(int)
		merging_dataframes["all_approvals_required"] = merging_dataframes["all_approvals_required"].astype(int)
		merging_dataframes["approval_required"] = merging_dataframes["approval_required"].astype(int)

		# Remove the requestor row (level 0) for approvals
		removing_requestor_row_in_the_view = merging_dataframes[merging_dataframes['level'] != 0]
		removing_requestor_row_in_the_view = removing_requestor_row_in_the_view[
			["name", "level", "action", "role", "user", "reason", "time", "cancel_request", "on_rejection", "mandatory", "escalation_time", 'requester_as_a_approver',"approval_required",'view_only_reportee', 'all_approvals_required']
		].sort_values("time").reset_index(drop=True)

		approvals = removing_requestor_row_in_the_view.to_dict("records")

		def filter_and_remove_entries(data):
			filtered_data = []
			for entry in data:
				if entry['action'] == 'Rejected':
					on_rejection_value = entry['on_rejection']
					filtered_data = [e for e in filtered_data if e['level'] != on_rejection_value and e['level'] < on_rejection_value]
				else:
					filtered_data.append(entry)
			return filtered_data

		removing_if_nan_in_approvals = pd.DataFrame.from_records(approvals)
		if not removing_if_nan_in_approvals.empty:
			removing_if_nan_in_approvals = removing_if_nan_in_approvals.dropna(subset=['action', "role", 'time', 'user'])
			approvals = removing_if_nan_in_approvals.to_dict("records")
		else:
			approvals = []

		filtered_data = filter_and_remove_entries(approvals)

		if len(filtered_data) <= 0:
			filtered_data = [{
				'name': None, 'level': 0, 'action': None, 'role': None, 'user': None, 'reason': None, 'time': None,
				'cancel_request': 0, 'on_rejection': 0, 'mandatory': 0, 'escalation_time': None,
				'requester_as_a_approver': 0,'view_only_reportee': 0, 'all_approvals_required': 0,"approval_required":0
			}]

		filtered_data_df = pd.DataFrame.from_records(filtered_data)
		dataframe_roadmap_wf_level_setup.drop(columns=["idx", "action"], inplace=True)
		filtered_data_df['escalation_time'] = filtered_data_df['escalation_time'].astype(str)
		dataframe_roadmap_wf_level_setup['escalation_time'] = dataframe_roadmap_wf_level_setup['escalation_time'].astype(str)

		merging_dataframes = pd.merge(filtered_data_df, dataframe_roadmap_wf_level_setup, how="outer")
		merging_dataframes = merging_dataframes.drop_duplicates(subset=["level", "role"], keep='first')
		merging_dataframes = merging_dataframes[
			["name", "level", "role", "user", "action", "reason", "cancel_request", "on_rejection", "mandatory", "escalation_time", "time",'requester_as_a_approver', 'view_only_reportee', 'all_approvals_required','approval_required']
		]
		merging_dataframes = merging_dataframes.replace(np.nan, '')
		merging_dataframes['role'].replace('', np.nan, inplace=True)
		merging_dataframes.dropna(subset=['role'], inplace=True)
		records_of_merging = merging_dataframes.to_dict("records")

		# Always pick the latest requestor row (level 0)
		requestor_line_in_dataframe_from_reasons = dataframe_wf_reasons.loc[dataframe_wf_reasons['level'] == 0]
		if not requestor_line_in_dataframe_from_reasons.empty:
			requestor_line_in_dataframe_from_reasons = requestor_line_in_dataframe_from_reasons.sort_values('time').iloc[[-1]]
		records_of_requestor_reasons = requestor_line_in_dataframe_from_reasons.to_dict("records")

		return {"success": True, "message": {"requestor_reasons": records_of_requestor_reasons, "approvals_reasons": records_of_merging}}
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		frappe.log_error("Error In Roadmap and Requests", "line No:{}\n{}".format(
			exc_tb.tb_lineno, traceback.format_exc()))
		return {"success": False, "error": str(e)}




@frappe.whitelist()
def todo_tab(document_type, request_id, property=None, cluster_name=None, current_level=None,account_ids=None,status=None):
	try:
		road_map = int(frappe.db.get_value('WF Roadmap',{"document_type":document_type},'workflow_levels'))
		current_level = int(current_level)
		now = add_to_date(None,as_datetime=True)
		my_time = f"{now.year}/{now.month}/{now.day} {now.hour}:{now.minute}:{now.second}:{now.microsecond}"
		for level in range(1,int(road_map)+1):
			
			return_message = combination_of_roadmap_and_request(document_type, request_id, property=property, cluster_name=cluster_name)
			
			approvals_reasons = return_message["message"]["approvals_reasons"]
			activate_log_roles = frappe.get_doc("WF Activity Log",request_id)
			workflow_requests = frappe.get_doc("WF Workflow Requests", request_id)
			# Get current user's role
			current_user_role = frappe.db.get_value("Ezy Employee", {"name": frappe.session.user}, 'designation')
	
			# Check if the current user has any pending approval at this level
			picking_remaining_roles_for_approval = [remaining_role["role"]  for remaining_role in approvals_reasons  if int(remaining_role["level"]) == int(current_level) and not remaining_role["action"].strip() and not remaining_role["user"].strip() ]
			
			all_approvals_required = [
				remaining_role["role"]
				for remaining_role in approvals_reasons
				if int(remaining_role["level"]) == int(current_level) and not remaining_role["action"].strip() and not remaining_role["user"].strip() and remaining_role.get("all_approvals_required", 0) == 1
			]
			
			view_only_roles = [
				remaining_role["role"]
				for remaining_role in approvals_reasons
				if int(remaining_role["level"]) == int(current_level) and not remaining_role["action"].strip() and not remaining_role["user"].strip() and remaining_role.get("view_only_reportee", 0) == 1
			]
			
			requester_as_a_approver = [
				remaining_role["role"]
				for remaining_role in approvals_reasons
				if int(remaining_role["level"]) == int(current_level) and not remaining_role["action"].strip() and not remaining_role["user"].strip() and remaining_role.get("requester_as_a_approver", 0) == 1
			]
			approvar_excits = [
				remaining_role["role"]
				for remaining_role in approvals_reasons
				if int(remaining_role["level"]) == int(current_level) and not remaining_role["action"].strip() and not remaining_role["user"].strip() and remaining_role.get("approval_required", 0) == 0
			]
			
			if approvar_excits and not status:
				approval_list = [role.role for role in activate_log_roles.reason if role.level != 0 and role.action != "Rejected"]
				role_user_map = {role.role: role.user for role in activate_log_roles.reason	if role.level != 0 and role.action != "Rejected"}
				approvar_excits_list = list(set(approval_list))
				has_match = any(map(lambda role: role in approvar_excits_list, approvar_excits))
				match_role = next((role for role in approvar_excits if role in role_user_map), None)
				match_role_user = role_user_map.get(match_role) if match_role else None
				if has_match:
					if all_approvals_required:
						all_approvals_required.remove(match_role)
    
					new_record = {
						"level": current_level,
						"role": match_role,
						"user":match_role_user,
						"action": "Approved",
						"reason": "Auto Approved by the system",
						"time": my_time,
						"random_string": ''.join(random.choices(string.ascii_letters + string.digits, k=10))
					}
					existing_roles = activate_log_roles.get("reason") or []
					record_exists = any(int(r.get("level")) == int(current_level) and r.get("role") == match_role and r.get("action") != "Rejected"  for r in existing_roles)
					if not record_exists and  not requester_as_a_approver:
						activate_log_roles.append("reason", new_record)
						activate_log_roles.save(ignore_permissions=True)
					if not requester_as_a_approver:
						doctype_ids = frappe.get_doc(document_type,account_ids)
						doctype_ids.wf_generated_request_status =  "In Progress" if int(current_level) < road_map  else "Completed"
						doctype_ids.save(ignore_permissions=True)
						workflow_requests.status = "In Progress" if int(current_level) < road_map else "Completed"
						current_level += 1  if int(current_level) < road_map and not all_approvals_required else  0 # move to next level
						workflow_requests.current_level = current_level if current_level<road_map else road_map
						workflow_requests.save()
						workflow_requests.reload()	
						frappe.db.commit()
						sending_mail_api(request_id=request_id, doctype_name=document_type,property= property,cluster= cluster_name,reason= "Auto Approved by the system",timestamp= my_time,skip_user_role= match_role,user = match_role_user )
				picking_remaining_roles_for_approval = [remaining_role["role"]  for remaining_role in approvals_reasons  if int(remaining_role["level"]) == int(current_level) and not remaining_role["action"].strip() and not remaining_role["user"].strip() ]
			else:
				picking_remaining_roles_for_approval = [remaining_role["role"]  for remaining_role in approvals_reasons  if int(remaining_role["level"]) == int(current_level) and not remaining_role["action"].strip() and not remaining_role["user"].strip() ]
		
			
			role_list = list( set( map( lambda r: r.role, filter(lambda r: int(r.level) == int(current_level), activate_log_roles.reason) ) )  )
			if current_user_role in picking_remaining_roles_for_approval and not view_only_roles and not requester_as_a_approver and not all_approvals_required and not status and  approvar_excits:
				doctype_ids = frappe.get_doc(document_type,account_ids)
				new_record = {
					"level": current_level,
					"role": current_user_role,
					"user":frappe.session.user,
					"action": "Approved",
					"reason": "Auto Approved by the system",
					"time": my_time,
					"random_string": ''.join(random.choices(string.ascii_letters + string.digits, k=10))
				}
				existing_roles = activate_log_roles.get("reason") or []
				record_exists = any(int(r.get("level")) == int(current_level) and r.get("role") == match_role and r.get("action") != "Rejected"  for r in existing_roles)
				if not record_exists:
					activate_log_roles.append("reason", new_record)
					activate_log_roles.save(ignore_permissions=True)
				doctype_ids.wf_generated_request_status =  "In Progress" if   len(approvals_reasons)>1 else "Completed"
				doctype_ids.save(ignore_permissions=True)
				workflow_requests.status = "In Progress" if int(current_level) < road_map else "Completed"
				current_level += 1  if int(current_level) < road_map else 0 # move to next level
				workflow_requests.current_level = current_level if current_level<road_map else road_map
				workflow_requests.save()
				workflow_requests.reload()
				frappe.db.commit()
				sending_mail_api(request_id=request_id, doctype_name=document_type,property= property,cluster= cluster_name,reason= "Auto Approved by the system",timestamp= my_time,skip_user_role= current_user_role,user = frappe.session.user )
			# Find the next level's approver role(s)
			picking_remaining_roles_for_approval = [remaining_role["role"] for remaining_role in approvals_reasons if int(remaining_role["level"]) == int(current_level) and not remaining_role["action"].strip() and not remaining_role["user"].strip()]
			
			if view_only_roles:
				be_half_of = workflow_requests.get("be_half_of", None)
				if be_half_of and not status:
					# Assign to the reporting manager of be_half_of user
					reporting_manager = frappe.db.get_value("Ezy Employee", be_half_of, "reporting_designation")
					picking_remaining_roles_for_approval = [reporting_manager]
				else:
					reporting_manager = frappe.db.get_value("Ezy Employee",workflow_requests.requested_by ,"reporting_designation")
					if reporting_manager in view_only_roles:
						picking_remaining_roles_for_approval = [reporting_manager]
					else:
						picking_remaining_roles_for_approval = ['No Role Assigned - View Only']
			if all_approvals_required and not status:
				prives_level_role_list = list( set( map( lambda r: r.role, filter(lambda r: int(r.level) == int(current_level)-1, activate_log_roles.reason) ) )  )
				all_approvals_required = list(filter(lambda x: True if not x in prives_level_role_list else False, all_approvals_required))
				# # # if the privies level approver in the same role, then assign to the next level approver skip
				############################################################# 
				picking_remaining_roles_for_approval = all_approvals_required


								
			if requester_as_a_approver and not status :
				if workflow_requests.role in requester_as_a_approver:
					picking_remaining_roles_for_approval = [workflow_requests.role]
				else:
					picking_remaining_roles_for_approval = ['No Role Assigned - Requester as Approver']

			if len(picking_remaining_roles_for_approval) > 0:
				frappe.db.set_value("WF Workflow Requests", request_id, "assigned_to_users", str(picking_remaining_roles_for_approval))
				frappe.db.commit()
			else:
				
				picking_remaining_roles_for_approval = [remaining_role["role"] for remaining_role in approvals_reasons if remaining_role["level"]== int(current_level)+1 and not remaining_role["action"].strip() and not remaining_role["user"].strip()]
				if current_user_role in picking_remaining_roles_for_approval :
					current_level =  int(current_level)+1
					workflow_requests = frappe.get_doc("WF Workflow Requests", request_id)
					doctype_ids = frappe.get_doc(document_type,account_ids)
					doctype_ids.wf_generated_request_status =  "In Progress" if len(approvals_reasons)>1 else "Completed"
					doctype_ids.save(ignore_permissions=True)
					workflow_requests.status = "In Progress" if current_level < road_map else "Completed"
					current_level += 1  if len(approvals_reasons)>1 else 0 # move to next level             
					workflow_requests.current_level = current_level if current_level<road_map else road_map
					workflow_requests.save()
					frappe.db.commit()
				picking_remaining_roles_for_approval = [remaining_role["role"] for remaining_role in approvals_reasons if int(remaining_role["level"]) == int(current_level) and not remaining_role["action"].strip() and not remaining_role["user"].strip()]
				

				frappe.db.set_value("WF Workflow Requests", request_id, {"assigned_to_users":str(picking_remaining_roles_for_approval),"current_level": ( int(current_level) if not status and int(current_level) < int(road_map) else  int(current_level) if  int(current_level) < int(road_map) else int(road_map)) })
				frappe.db.commit()
	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		frappe.log_error("Error In TO DO Tab.", "line No:{}\n{}".format(
			exc_tb.tb_lineno, traceback.format_exc()))
		return {"success": False, "error": str(e)}



@frappe.whitelist()
def auto_approval_after_request_raising(document_type, request_id, property=None, cluster_name=None, current_level=None, url_for_approval_id=None):
	"""
	Automatically approve a workflow request if the requestor's role exists 
	in the approval flow at the given level.
	"""
	from ezy_forms.api.v1.ezy_form_update_worflow import updating_wf_workflow_requests
	try:
		# Get request + roadmap data

		return_message = combination_of_roadmap_and_request(
			document_type, request_id, property=property, cluster_name=cluster_name
		)
		approvals_reasons = return_message["message"].get("approvals_reasons", [])

		# Resolve current user role
		roles = frappe.get_all(
			"Has Role",
			fields=["role"],
			filters={"parent": frappe.session.user},
			pluck="role",
		)
		# Prefer Employee.designation over roles, exclude System Manager
		employee_role = frappe.db.get_value("Ezy Employee", frappe.session.user, "designation")
		role = employee_role or next((r for r in roles if r != "System Manager"), None)

		if not role:
			return {"success": False, "error": "No valid role found for user"}

		# Check if user's role is part of approvals at current level
		is_approver = any(
			r["level"] == current_level and r["role"] == role
			for r in approvals_reasons
		)

		if is_approver:
			frappe.log_error("Auto Approving", request_id)
			request_details = {
				"doctype": document_type,
				"request_ids": [request_id],
				"current_level": current_level,
				"action": "Approve",
				"reason": f"Auto Approve Done By Requestor - '{role}'.",
				"url_for_approval_id": url_for_approval_id,
				"files": None,
				"property": property,
				"cluster_name": cluster_name,
			}
			# Small delay before updating (safeguard against race conditions)
			time.sleep(1)
			updating_wf_workflow_requests([request_details])

		return {"success": True}

	except Exception as e:
		exc_type, exc_obj, exc_tb = sys.exc_info()
		frappe.log_error(
			title="Error In Auto Approving",
			message=f"Line No: {exc_tb.tb_lineno}\n{traceback.format_exc()}",
		)
		return {"success": False, "error": str(e)}

		

def create_next_level_todos(doctype_name, request_id, property, cluster, account_id):
	"""Create TODO items for next level approvers"""
	try:
		# Call todo creation function (assuming it exists)
		# apps.ezy_flow.ezy_flow.ezy_flow.doctype.wf_workflow_requests.wf_workflow_requests.todo_tab
		frappe.get_attr("ezy_forms.api.v1.ezy_form_rasie_request.todo_tab")(
			document_type=doctype_name,
			request_id=request_id,
			property=property,
			cluster_name=cluster,
			current_level=1,
			account_ids=account_id,
			status=None
		)
	except Exception as e:
		frappe.log_error(f"TODO creation failed: {str(e)}", "TODO Creation Error")

# Utility function to get linked form status
def get_linked_form_status(doctype_name):
	"""Get linked form status for the doctype"""
	try:
		return frappe.db.get_value(
			"Ezy Form Definitions",
			{"form_name": doctype_name},
			"is_linked_form"
		)
	except Exception:
		return None