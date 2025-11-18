"""
Form Insights API
Provides detailed analytics and insights for specific forms
"""

import frappe
from frappe import _
from frappe.utils import nowdate, add_days, getdate
import json


@frappe.whitelist()
def get_available_forms(property=None):
    """
    Get list of all available forms for insights

    Args:
        property: Business unit filter (optional)

    Returns:
        dict: List of form types with submission counts
    """
    try:
        conditions = []
        values = {}

        if property:
            conditions.append("wfr.property = %(property)s")
            values["property"] = property

        where_clause = " AND " + " AND ".join(conditions) if conditions else ""

        query = f"""
            SELECT
                wfr.doctype_name as form_name,
                COUNT(*) as total_submissions,
                SUM(CASE WHEN wfr.status = 'Completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN wfr.status IN ('Request Raised', 'Request Raised Via QR Code') THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN wfr.status = 'In Progress' THEN 1 ELSE 0 END) as in_progress,
                MIN(wfr.requested_on) as first_submission,
                MAX(wfr.requested_on) as last_submission
            FROM `tabWF Workflow Requests` wfr
            WHERE wfr.docstatus != 2 {where_clause}
            GROUP BY wfr.doctype_name
            ORDER BY total_submissions DESC
        """

        results = frappe.db.sql(query, values=values, as_dict=True)

        return {
            "success": True,
            "data": results
        }

    except Exception as e:
        frappe.log_error(f"Error in get_available_forms: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_form_insights(form_name, property=None, date_from=None, date_to=None, department=None):
    """
    Get comprehensive insights for a specific form

    Args:
        form_name: Name of the form to analyze
        property: Business unit filter (optional)
        date_from: Start date for filtering
        date_to: End date for filtering
        department: Department filter (optional)

    Returns:
        dict: Comprehensive form insights including status breakdown, trends, departments, etc.
    """
    try:
        # Authentication check
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        # Set default date range if not provided (last 90 days)
        if not date_from or not date_to:
            date_to = nowdate()
            date_from = add_days(date_to, -90)

        # Build conditions
        conditions = ["wfr.doctype_name = %(form_name)s"]
        values = {"form_name": form_name}

        if property:
            conditions.append("wfr.property = %(property)s")
            values["property"] = property

        if date_from and date_to:
            conditions.append("DATE(wfr.requested_on) BETWEEN %(date_from)s AND %(date_to)s")
            values["date_from"] = date_from
            values["date_to"] = date_to

        if department:
            conditions.append("emp.department = %(department)s")
            values["department"] = department

        where_clause = " AND ".join(conditions)

        # Get status breakdown
        status_query = f"""
            SELECT
                CASE
                    WHEN wfr.status = 'Completed' THEN 'Completed'
                    WHEN wfr.status IN ('Request Raised', 'Request Raised Via QR Code') THEN 'Pending'
                    WHEN wfr.status = 'In Progress' THEN 'In Progress'
                    WHEN wfr.status = 'Request Cancelled' THEN 'Cancelled'
                    ELSE 'Other'
                END as status,
                COUNT(*) as count
            FROM `tabWF Workflow Requests` wfr
            LEFT JOIN `tabEzy Employee` emp ON wfr.requested_by = emp.emp_mail_id
            WHERE wfr.docstatus != 2 AND {where_clause}
            GROUP BY status
        """

        status_results = frappe.db.sql(status_query, values=values, as_dict=True)

        # Get department-wise breakdown
        dept_query = f"""
            SELECT
                COALESCE(dept.department_name, 'No Department') as department,
                COUNT(*) as count,
                SUM(CASE WHEN wfr.status = 'Completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN wfr.status IN ('Request Raised', 'Request Raised Via QR Code') THEN 1 ELSE 0 END) as pending
            FROM `tabWF Workflow Requests` wfr
            LEFT JOIN `tabEzy Employee` emp ON wfr.requested_by = emp.emp_mail_id
            LEFT JOIN `tabEzy Departments` dept ON emp.department = dept.name
            WHERE wfr.docstatus != 2 AND {where_clause}
            GROUP BY dept.department_name
            ORDER BY count DESC
            LIMIT 10
        """

        dept_results = frappe.db.sql(dept_query, values=values, as_dict=True)

        # Get monthly trends
        trend_query = f"""
            SELECT
                DATE_FORMAT(wfr.requested_on, '%Y-%m') as month,
                COUNT(*) as total,
                SUM(CASE WHEN wfr.status = 'Completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN wfr.status IN ('Request Raised', 'Request Raised Via QR Code') THEN 1 ELSE 0 END) as pending
            FROM `tabWF Workflow Requests` wfr
            LEFT JOIN `tabEzy Employee` emp ON wfr.requested_by = emp.emp_mail_id
            WHERE wfr.docstatus != 2 AND {where_clause}
            GROUP BY month
            ORDER BY month ASC
        """

        trend_results = frappe.db.sql(trend_query, values=values, as_dict=True)

        # Get top requestors
        requestor_query = f"""
            SELECT
                emp.emp_name as requestor_name,
                emp.emp_mail_id as requestor_email,
                dept.department_name as department,
                COUNT(*) as total_requests,
                SUM(CASE WHEN wfr.status = 'Completed' THEN 1 ELSE 0 END) as completed
            FROM `tabWF Workflow Requests` wfr
            LEFT JOIN `tabEzy Employee` emp ON wfr.requested_by = emp.emp_mail_id
            LEFT JOIN `tabEzy Departments` dept ON emp.department = dept.name
            WHERE wfr.docstatus != 2 AND {where_clause}
            GROUP BY emp.emp_name, emp.emp_mail_id, dept.department_name
            ORDER BY total_requests DESC
            LIMIT 10
        """

        requestor_results = frappe.db.sql(requestor_query, values=values, as_dict=True)

        # Get average processing time (for completed requests)
        processing_query = f"""
            SELECT
                AVG(TIMESTAMPDIFF(HOUR, wfr.requested_on, wfr.modified)) as avg_hours,
                MIN(TIMESTAMPDIFF(HOUR, wfr.requested_on, wfr.modified)) as min_hours,
                MAX(TIMESTAMPDIFF(HOUR, wfr.requested_on, wfr.modified)) as max_hours
            FROM `tabWF Workflow Requests` wfr
            LEFT JOIN `tabEzy Employee` emp ON wfr.requested_by = emp.emp_mail_id
            WHERE wfr.docstatus != 2
                AND wfr.status = 'Completed'
                AND {where_clause}
        """

        processing_results = frappe.db.sql(processing_query, values=values, as_dict=True)

        # Get all submissions for detailed table
        submissions_query = f"""
            SELECT
                wfr.name as request_id,
                wfr.requested_on,
                emp.emp_name as requestor,
                dept.department_name as department,
                wfr.status,
                wfr.property,
                TIMESTAMPDIFF(HOUR, wfr.requested_on,
                    CASE WHEN wfr.status = 'Completed' THEN wfr.modified ELSE NOW() END
                ) as processing_hours
            FROM `tabWF Workflow Requests` wfr
            LEFT JOIN `tabEzy Employee` emp ON wfr.requested_by = emp.emp_mail_id
            LEFT JOIN `tabEzy Departments` dept ON emp.department = dept.name
            WHERE wfr.docstatus != 2 AND {where_clause}
            ORDER BY wfr.requested_on DESC
            LIMIT 500
        """

        submissions_results = frappe.db.sql(submissions_query, values=values, as_dict=True)

        return {
            "success": True,
            "data": {
                "form_name": form_name,
                "date_range": {
                    "from": date_from,
                    "to": date_to
                },
                "status_breakdown": status_results,
                "department_breakdown": dept_results,
                "monthly_trends": trend_results,
                "top_requestors": requestor_results,
                "processing_time": processing_results[0] if processing_results else {
                    "avg_hours": 0,
                    "min_hours": 0,
                    "max_hours": 0
                },
                "submissions": submissions_results
            }
        }

    except Exception as e:
        frappe.log_error(f"Error in get_form_insights: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def export_form_insights(form_name, property=None, date_from=None, date_to=None, department=None, export_format="csv"):
    """
    Export form insights data in various formats

    Args:
        form_name: Name of the form to analyze
        property: Business unit filter (optional)
        date_from: Start date for filtering
        date_to: End date for filtering
        department: Department filter (optional)
        export_format: Export format (csv, excel)

    Returns:
        dict: Export file details
    """
    try:
        # Authentication check
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        # Get form insights data
        insights = get_form_insights(form_name, property, date_from, date_to, department)

        if not insights.get("success"):
            return insights

        data = insights.get("data", {})
        submissions = data.get("submissions", [])

        if export_format == "csv":
            # Create CSV content
            import csv
            from io import StringIO

            output = StringIO()
            if submissions:
                fieldnames = list(submissions[0].keys())
                writer = csv.DictWriter(output, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(submissions)

            csv_content = output.getvalue()

            return {
                "success": True,
                "data": {
                    "content": csv_content,
                    "filename": f"{form_name}_insights_{nowdate()}.csv",
                    "format": "csv"
                }
            }

        elif export_format == "excel":
            # For Excel export, return the data for frontend processing
            return {
                "success": True,
                "data": {
                    "submissions": submissions,
                    "filename": f"{form_name}_insights_{nowdate()}.xlsx",
                    "format": "excel"
                }
            }

        else:
            return {
                "success": False,
                "message": "Invalid export format"
            }

    except Exception as e:
        frappe.log_error(f"Error in export_form_insights: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }
