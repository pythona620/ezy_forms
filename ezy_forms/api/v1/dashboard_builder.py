"""
Dashboard Builder API
Allows users to create, save, and load custom dashboards for forms
"""

import frappe
from frappe import _
import json


@frappe.whitelist()
def save_dashboard(dashboard_name, form_name, chart_config, filters=None):
    """
    Save a custom dashboard configuration to Ezy Insights

    Args:
        dashboard_name: Name of the dashboard
        form_name: Form this dashboard is for
        chart_config: JSON string with chart configuration
        filters: Optional default filters JSON string

    Returns:
        dict: Success status and dashboard info
    """
    try:
        # Authentication check
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        # Parse JSON strings
        if isinstance(chart_config, str):
            chart_config = json.loads(chart_config)

        if filters and isinstance(filters, str):
            filters = json.loads(filters)

        # Get or create the Ezy Insights single doctype
        if not frappe.db.exists("Ezy Insights", "Ezy Insights"):
            insights_doc = frappe.get_doc({
                "doctype": "Ezy Insights",
                "name": "Ezy Insights"
            })
            insights_doc.insert(ignore_permissions=True)
        else:
            insights_doc = frappe.get_doc("Ezy Insights", "Ezy Insights")

        # Create dashboard link (store configuration as JSON in link field)
        dashboard_data = {
            "form_name": form_name,
            "chart_config": chart_config,
            "filters": filters or {},
            "created_by": frappe.session.user
        }

        # Check if dashboard with same name exists
        existing = None
        if insights_doc.dashboards:
            for dash in insights_doc.dashboards:
                if dash.report_name == dashboard_name:
                    existing = dash
                    break

        if existing:
            # Update existing dashboard
            existing.link = json.dumps(dashboard_data)
            existing.status = 1
        else:
            # Add new dashboard
            insights_doc.append("dashboards", {
                "report_name": dashboard_name,
                "link": json.dumps(dashboard_data),
                "status": 1,
                "is_main_dashboard": 0
            })

        insights_doc.save(ignore_permissions=True)
        frappe.db.commit()

        return {
            "success": True,
            "message": "Dashboard saved successfully",
            "dashboard_name": dashboard_name
        }

    except json.JSONDecodeError as e:
        frappe.log_error(f"JSON decode error in save_dashboard: {str(e)}")
        return {
            "success": False,
            "message": "Invalid JSON format in configuration"
        }
    except Exception as e:
        frappe.log_error(f"Error in save_dashboard: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_saved_dashboards():
    """
    Get all saved dashboards for the current user

    Returns:
        dict: List of saved dashboards
    """
    try:
        # Authentication check
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        dashboards = []

        if frappe.db.exists("Ezy Insights", "Ezy Insights"):
            insights_doc = frappe.get_doc("Ezy Insights", "Ezy Insights")

            if insights_doc.dashboards:
                for dash in insights_doc.dashboards:
                    if dash.status == 1:  # Only enabled dashboards
                        try:
                            # Parse the link field which contains JSON config
                            config = json.loads(dash.link) if dash.link else {}

                            dashboards.append({
                                "name": dash.name,
                                "dashboard_name": dash.report_name,
                                "form_name": config.get("form_name", "Unknown"),
                                "chart_config": config.get("chart_config", {}),
                                "filters": config.get("filters", {}),
                                "created_by": config.get("created_by", ""),
                                "is_main": dash.is_main_dashboard
                            })
                        except (json.JSONDecodeError, Exception) as e:
                            # Skip invalid entries
                            frappe.log_error(f"Error parsing dashboard {dash.name}: {str(e)}")
                            continue

        return {
            "success": True,
            "data": dashboards
        }

    except Exception as e:
        frappe.log_error(f"Error in get_saved_dashboards: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_dashboard(dashboard_name):
    """
    Get a specific dashboard configuration

    Args:
        dashboard_name: Name of the dashboard to retrieve

    Returns:
        dict: Dashboard configuration
    """
    try:
        # Authentication check
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        if frappe.db.exists("Ezy Insights", "Ezy Insights"):
            insights_doc = frappe.get_doc("Ezy Insights", "Ezy Insights")

            if insights_doc.dashboards:
                for dash in insights_doc.dashboards:
                    if dash.report_name == dashboard_name and dash.status == 1:
                        config = json.loads(dash.link) if dash.link else {}

                        return {
                            "success": True,
                            "data": {
                                "dashboard_name": dash.report_name,
                                "form_name": config.get("form_name", ""),
                                "chart_config": config.get("chart_config", {}),
                                "filters": config.get("filters", {}),
                                "created_by": config.get("created_by", ""),
                                "is_main": dash.is_main_dashboard
                            }
                        }

        return {
            "success": False,
            "message": "Dashboard not found"
        }

    except Exception as e:
        frappe.log_error(f"Error in get_dashboard: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def delete_dashboard(dashboard_name):
    """
    Delete a saved dashboard

    Args:
        dashboard_name: Name of the dashboard to delete

    Returns:
        dict: Success status
    """
    try:
        # Authentication check
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        if frappe.db.exists("Ezy Insights", "Ezy Insights"):
            insights_doc = frappe.get_doc("Ezy Insights", "Ezy Insights")

            if insights_doc.dashboards:
                for idx, dash in enumerate(insights_doc.dashboards):
                    if dash.report_name == dashboard_name:
                        # Check if user created this dashboard
                        try:
                            config = json.loads(dash.link) if dash.link else {}
                            created_by = config.get("created_by", "")

                            # Allow deletion if user created it or is System Manager
                            if created_by == frappe.session.user or "System Manager" in frappe.get_roles():
                                insights_doc.dashboards.pop(idx)
                                insights_doc.save(ignore_permissions=True)
                                frappe.db.commit()

                                return {
                                    "success": True,
                                    "message": "Dashboard deleted successfully"
                                }
                            else:
                                return {
                                    "success": False,
                                    "message": "You don't have permission to delete this dashboard"
                                }
                        except Exception:
                            pass

        return {
            "success": False,
            "message": "Dashboard not found"
        }

    except Exception as e:
        frappe.log_error(f"Error in delete_dashboard: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }
