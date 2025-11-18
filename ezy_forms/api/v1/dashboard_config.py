"""
Dashboard Configuration API
Manages dashboard configurations with save, load, export, and import
"""

import frappe
from frappe import _
import json
from datetime import datetime


@frappe.whitelist()
def save_dashboard_config(dashboard_name, form_name, description="", widgets=None,
                          layout=None, filters=None, refresh_interval=0, is_public=0):
    """
    Save or update dashboard configuration

    Args:
        dashboard_name: Unique dashboard name
        form_name: Form this dashboard is for
        description: Dashboard description
        widgets: JSON string/dict of widget configurations
        layout: JSON string/dict of layout configuration
        filters: JSON string/dict of default filters
        refresh_interval: Auto-refresh interval in seconds
        is_public: Whether dashboard is public

    Returns:
        dict: Success status
    """
    try:
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        # Parse JSON inputs
        if isinstance(widgets, str):
            widgets = json.loads(widgets) if widgets else []
        if isinstance(layout, str):
            layout = json.loads(layout) if layout else {}
        if isinstance(filters, str):
            filters = json.loads(filters) if filters else {}

        # Check if dashboard exists
        existing = frappe.db.get_value(
            "Ezy Dashboard Configuration",
            {"dashboard_name": dashboard_name},
            "name"
        )

        if existing:
            # Update existing
            doc = frappe.get_doc("Ezy Dashboard Configuration", existing)
            doc.description = description
            doc.form_name = form_name
            doc.layout_config = json.dumps(layout)
            doc.filters = json.dumps(filters)
            doc.refresh_interval = int(refresh_interval)
            doc.is_public = int(is_public)

            # Clear and re-add widgets
            doc.widgets = []
            for widget in widgets:
                doc.append("widgets", {
                    "widget_id": widget.get("widget_id"),
                    "widget_type": widget.get("widget_type"),
                    "title": widget.get("title"),
                    "widget_config": json.dumps(widget.get("config", {})),
                    "position_x": widget.get("position_x", 0),
                    "position_y": widget.get("position_y", 0),
                    "width": widget.get("width", 6),
                    "height": widget.get("height", 4)
                })

            doc.save(ignore_permissions=True)
            frappe.db.commit()

            message = "Dashboard updated successfully"
        else:
            # Create new
            doc = frappe.get_doc({
                "doctype": "Ezy Dashboard Configuration",
                "dashboard_name": dashboard_name,
                "form_name": form_name,
                "description": description,
                "layout_config": json.dumps(layout),
                "filters": json.dumps(filters),
                "refresh_interval": int(refresh_interval),
                "is_public": int(is_public),
                "created_by_user": frappe.session.user,
                "widgets": []
            })

            for widget in widgets:
                doc.append("widgets", {
                    "widget_id": widget.get("widget_id"),
                    "widget_type": widget.get("widget_type"),
                    "title": widget.get("title"),
                    "widget_config": json.dumps(widget.get("config", {})),
                    "position_x": widget.get("position_x", 0),
                    "position_y": widget.get("position_y", 0),
                    "width": widget.get("width", 6),
                    "height": widget.get("height", 4)
                })

            doc.insert(ignore_permissions=True)
            frappe.db.commit()

            message = "Dashboard created successfully"

        return {
            "success": True,
            "message": message,
            "dashboard_id": doc.name
        }

    except Exception as e:
        frappe.log_error(f"Error in save_dashboard_config: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_dashboard_configs(form_name=None):
    """
    Get all dashboard configurations for a user

    Args:
        form_name: Optional filter by form name

    Returns:
        dict: List of dashboard configurations
    """
    try:
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        filters = {}
        if form_name:
            filters["form_name"] = form_name

        # Get user's dashboards and public dashboards
        user_dashboards = frappe.get_all(
            "Ezy Dashboard Configuration",
            filters={**filters, "created_by_user": frappe.session.user},
            fields=["name", "dashboard_name", "form_name", "description", "created_by_user", "creation", "modified"]
        )

        public_dashboards = frappe.get_all(
            "Ezy Dashboard Configuration",
            filters={**filters, "is_public": 1},
            fields=["name", "dashboard_name", "form_name", "description", "created_by_user", "creation", "modified"]
        )

        # Merge and deduplicate
        all_dashboards = {d.name: d for d in user_dashboards + public_dashboards}.values()

        # Add widget count
        for dash in all_dashboards:
            widget_count = frappe.db.count("Ezy Dashboard Widget", {"parent": dash.name})
            dash["widget_count"] = widget_count

        return {
            "success": True,
            "data": list(all_dashboards)
        }

    except Exception as e:
        frappe.log_error(f"Error in get_dashboard_configs: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_dashboard_config(dashboard_id=None, dashboard_name=None):
    """
    Get a specific dashboard configuration with all widgets

    Args:
        dashboard_id: Dashboard document name
        dashboard_name: Dashboard name

    Returns:
        dict: Complete dashboard configuration
    """
    try:
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        if dashboard_id:
            doc = frappe.get_doc("Ezy Dashboard Configuration", dashboard_id)
        elif dashboard_name:
            name = frappe.db.get_value("Ezy Dashboard Configuration", {"dashboard_name": dashboard_name}, "name")
            if not name:
                return {"success": False, "message": "Dashboard not found"}
            doc = frappe.get_doc("Ezy Dashboard Configuration", name)
        else:
            return {"success": False, "message": "Dashboard ID or name required"}

        # Parse JSON fields
        layout_config = json.loads(doc.layout_config) if doc.layout_config else {}
        filters = json.loads(doc.filters) if doc.filters else {}

        # Get widgets
        widgets = []
        for widget in doc.widgets:
            widgets.append({
                "widget_id": widget.widget_id,
                "widget_type": widget.widget_type,
                "title": widget.title,
                "config": json.loads(widget.widget_config) if widget.widget_config else {},
                "position_x": widget.position_x,
                "position_y": widget.position_y,
                "width": widget.width,
                "height": widget.height
            })

        return {
            "success": True,
            "data": {
                "id": doc.name,
                "dashboard_name": doc.dashboard_name,
                "form_name": doc.form_name,
                "description": doc.description,
                "layout": layout_config,
                "widgets": widgets,
                "filters": filters,
                "refresh_interval": doc.refresh_interval,
                "is_public": doc.is_public,
                "created_by": doc.created_by_user,
                "created_on": doc.creation,
                "modified_on": doc.modified
            }
        }

    except Exception as e:
        frappe.log_error(f"Error in get_dashboard_config: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def update_dashboard_layout(dashboard_id, layout):
    """
    Update only the layout configuration (for drag-drop)

    Args:
        dashboard_id: Dashboard document name
        layout: JSON string/dict of new layout

    Returns:
        dict: Success status
    """
    try:
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        if isinstance(layout, str):
            layout = json.loads(layout)

        doc = frappe.get_doc("Ezy Dashboard Configuration", dashboard_id)

        # Check permissions
        if doc.created_by_user != frappe.session.user and not doc.is_public:
            frappe.throw("You don't have permission to edit this dashboard")

        doc.layout_config = json.dumps(layout)
        doc.save(ignore_permissions=True)
        frappe.db.commit()

        return {
            "success": True,
            "message": "Layout updated successfully"
        }

    except Exception as e:
        frappe.log_error(f"Error in update_dashboard_layout: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def delete_dashboard_config(dashboard_id):
    """
    Delete a dashboard configuration

    Args:
        dashboard_id: Dashboard document name

    Returns:
        dict: Success status
    """
    try:
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        doc = frappe.get_doc("Ezy Dashboard Configuration", dashboard_id)

        # Check permissions
        if doc.created_by_user != frappe.session.user:
            # Check if System Manager
            if "System Manager" not in frappe.get_roles():
                frappe.throw("You don't have permission to delete this dashboard")

        frappe.delete_doc("Ezy Dashboard Configuration", dashboard_id, ignore_permissions=True)
        frappe.db.commit()

        return {
            "success": True,
            "message": "Dashboard deleted successfully"
        }

    except Exception as e:
        frappe.log_error(f"Error in delete_dashboard_config: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def export_dashboard_json(dashboard_id):
    """
    Export dashboard configuration as JSON

    Args:
        dashboard_id: Dashboard document name

    Returns:
        dict: Dashboard configuration in exportable format
    """
    try:
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        config = get_dashboard_config(dashboard_id=dashboard_id)

        if not config["success"]:
            return config

        dashboard_data = config["data"]

        export_data = {
            "version": "1.0",
            "exported_at": datetime.now().isoformat(),
            "exported_by": frappe.session.user,
            "dashboard": {
                "dashboard_name": dashboard_data["dashboard_name"],
                "form_name": dashboard_data["form_name"],
                "description": dashboard_data["description"],
                "widgets": dashboard_data["widgets"],
                "layout": dashboard_data["layout"],
                "filters": dashboard_data["filters"],
                "refresh_interval": dashboard_data["refresh_interval"]
            }
        }

        return {
            "success": True,
            "data": export_data,
            "filename": f"{dashboard_data['dashboard_name']}.json"
        }

    except Exception as e:
        frappe.log_error(f"Error in export_dashboard_json: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def import_dashboard_json(json_data, dashboard_name=None):
    """
    Import dashboard configuration from JSON

    Args:
        json_data: JSON string of dashboard configuration
        dashboard_name: Optional new name for imported dashboard

    Returns:
        dict: Success status
    """
    try:
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        # Parse JSON
        if isinstance(json_data, str):
            import_data = json.loads(json_data)
        else:
            import_data = json_data

        # Validate format
        if "version" not in import_data or "dashboard" not in import_data:
            frappe.throw("Invalid dashboard JSON format")

        dashboard_data = import_data["dashboard"]

        # Use provided name or generate unique name
        if not dashboard_name:
            dashboard_name = dashboard_data.get("dashboard_name", "Imported Dashboard")

        # Check if name exists, append number if needed
        base_name = dashboard_name
        counter = 1
        while frappe.db.exists("Ezy Dashboard Configuration", {"dashboard_name": dashboard_name}):
            dashboard_name = f"{base_name} ({counter})"
            counter += 1

        # Create dashboard
        result = save_dashboard_config(
            dashboard_name=dashboard_name,
            form_name=dashboard_data.get("form_name"),
            description=dashboard_data.get("description", ""),
            widgets=dashboard_data.get("widgets", []),
            layout=dashboard_data.get("layout", {}),
            filters=dashboard_data.get("filters", {}),
            refresh_interval=dashboard_data.get("refresh_interval", 0),
            is_public=0  # Imported dashboards are private by default
        )

        return result

    except Exception as e:
        frappe.log_error(f"Error in import_dashboard_json: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def duplicate_dashboard(dashboard_id, new_name):
    """
    Duplicate an existing dashboard

    Args:
        dashboard_id: Source dashboard ID
        new_name: Name for the new dashboard

    Returns:
        dict: Success status with new dashboard ID
    """
    try:
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        # Get source dashboard
        config = get_dashboard_config(dashboard_id=dashboard_id)
        if not config["success"]:
            return config

        source_data = config["data"]

        # Create duplicate
        result = save_dashboard_config(
            dashboard_name=new_name,
            form_name=source_data["form_name"],
            description=f"Copy of {source_data['dashboard_name']}",
            widgets=source_data["widgets"],
            layout=source_data["layout"],
            filters=source_data["filters"],
            refresh_interval=source_data["refresh_interval"],
            is_public=0
        )

        return result

    except Exception as e:
        frappe.log_error(f"Error in duplicate_dashboard: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }
