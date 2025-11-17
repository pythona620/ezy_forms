"""
New Dashboard API
Provides insights and analytics for EzyForms dashboard
"""

import frappe
from frappe import _
from frappe.utils import nowdate, add_days


@frappe.whitelist()
def get_form_status_overview(property=None, date_from=None, date_to=None, department=None, form_type=None):
    """
    Get form status overview with counts by status

    Args:
        property: Business unit filter
        date_from: Start date for filtering
        date_to: End date for filtering
        department: Department filter
        form_type: Form type filter

    Returns:
        dict: Status counts (Completed, Pending, In Progress)
    """
    try:
        conditions = []
        values = {}

        # Build base query conditions
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

        if form_type:
            conditions.append("wfr.doctype_name = %(form_type)s")
            values["form_type"] = form_type

        where_clause = " AND " + " AND ".join(conditions) if conditions else ""

        # Query for status counts
        query = f"""
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
            LEFT JOIN `tabEzy Employee` emp ON wfr.requested_by = emp.user
            WHERE wfr.docstatus != 2 {where_clause}
            GROUP BY status
        """

        results = frappe.db.sql(query, values=values, as_dict=True)

        # Format results
        status_counts = {
            "Completed": 0,
            "Pending": 0,
            "In Progress": 0,
            "Cancelled": 0,
            "Other": 0
        }

        for row in results:
            status_counts[row.status] = row.count

        # Get total count
        status_counts["Total"] = sum([v for k, v in status_counts.items() if k != "Total"])

        return {
            "success": True,
            "data": status_counts
        }

    except Exception as e:
        frappe.log_error(f"Error in get_form_status_overview: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_department_wise_analysis(property=None, date_from=None, date_to=None, department=None):
    """
    Get department-wise form submission analysis

    Args:
        property: Business unit filter
        date_from: Start date for filtering
        date_to: End date for filtering
        department: Department filter (optional, for specific department)

    Returns:
        dict: Department-wise form counts and types
    """
    try:
        conditions = []
        values = {}

        if property:
            conditions.append("wfr.property = %(property)s")
            values["property"] = property

        if date_from and date_to:
            conditions.append("DATE(wfr.requested_on) BETWEEN %(date_from)s AND %(date_to)s")
            values["date_from"] = date_from
            values["date_to"] = date_to

        if department:
            conditions.append("dept.department_name = %(department)s")
            values["department"] = department

        where_clause = " AND " + " AND ".join(conditions) if conditions else ""

        # Query for department-wise analysis
        query = f"""
            SELECT
                COALESCE(dept.department_name, 'No Department') as department,
                wfr.doctype_name as form_type,
                COUNT(*) as count,
                SUM(CASE WHEN wfr.status = 'Completed' THEN 1 ELSE 0 END) as completed,
                SUM(CASE WHEN wfr.status IN ('Request Raised', 'Request Raised Via QR Code') THEN 1 ELSE 0 END) as pending,
                SUM(CASE WHEN wfr.status = 'In Progress' THEN 1 ELSE 0 END) as in_progress
            FROM `tabWF Workflow Requests` wfr
            LEFT JOIN `tabEzy Employee` emp ON wfr.requested_by = emp.user
            LEFT JOIN `tabEzy Departments` dept ON emp.department = dept.name
            WHERE wfr.docstatus != 2 {where_clause}
            GROUP BY dept.department_name, wfr.doctype_name
            ORDER BY count DESC
        """

        results = frappe.db.sql(query, values=values, as_dict=True)

        # Group by department
        department_data = {}
        for row in results:
            dept_name = row.department
            if dept_name not in department_data:
                department_data[dept_name] = {
                    "department": dept_name,
                    "total_forms": 0,
                    "form_types": [],
                    "completed": 0,
                    "pending": 0,
                    "in_progress": 0
                }

            department_data[dept_name]["total_forms"] += row.count
            department_data[dept_name]["completed"] += row.completed
            department_data[dept_name]["pending"] += row.pending
            department_data[dept_name]["in_progress"] += row.in_progress
            department_data[dept_name]["form_types"].append({
                "form_type": row.form_type,
                "count": row.count
            })

        return {
            "success": True,
            "data": list(department_data.values())
        }

    except Exception as e:
        frappe.log_error(f"Error in get_department_wise_analysis: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_form_value_tracking(property=None, date_from=None, date_to=None, department=None, form_type=None):
    """
    Get form value/amount tracking
    Note: This assumes forms have an 'amount' or 'value' field

    Args:
        property: Business unit filter
        date_from: Start date for filtering
        date_to: End date for filtering
        department: Department filter
        form_type: Form type filter

    Returns:
        dict: Form value statistics
    """
    try:
        conditions = []
        values = {}

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

        if form_type:
            conditions.append("wfr.doctype_name = %(form_type)s")
            values["form_type"] = form_type

        where_clause = " AND " + " AND ".join(conditions) if conditions else ""

        # Get all workflow requests
        query = f"""
            SELECT
                wfr.name,
                wfr.doctype_name,
                wfr.reference_id,
                wfr.status,
                wfr.requested_on,
                dept.department_name as department
            FROM `tabWF Workflow Requests` wfr
            LEFT JOIN `tabEzy Employee` emp ON wfr.requested_by = emp.user
            LEFT JOIN `tabEzy Departments` dept ON emp.department = dept.name
            WHERE wfr.docstatus != 2 {where_clause}
            ORDER BY wfr.requested_on DESC
        """

        requests = frappe.db.sql(query, values=values, as_dict=True)

        # Process each request to extract amount/value
        form_values = []
        total_amount = 0
        forms_with_amount = 0

        for req in requests:
            try:
                # Get reference IDs from child table
                ref_ids = frappe.db.sql("""
                    SELECT reference_id, reference_doctype
                    FROM `tabWF IDs`
                    WHERE parent = %s
                """, req.name, as_dict=True)

                amount = 0
                for ref in ref_ids:
                    if ref.reference_id and ref.reference_doctype:
                        # Try to get amount/value field from the referenced document
                        doc = frappe.get_doc(ref.reference_doctype, ref.reference_id)

                        # Check for common amount fields
                        amount_fields = ['amount', 'total_amount', 'value', 'total_value', 'total', 'grand_total']
                        for field in amount_fields:
                            if hasattr(doc, field) and doc.get(field):
                                amount += float(doc.get(field) or 0)
                                break

                if amount > 0:
                    forms_with_amount += 1
                    total_amount += amount
                    form_values.append({
                        "request_id": req.name,
                        "form_type": req.doctype_name,
                        "department": req.department,
                        "amount": amount,
                        "status": req.status,
                        "date": req.requested_on
                    })

            except Exception as e:
                # Skip if document doesn't exist or has no amount field
                continue

        # Calculate statistics
        avg_amount = total_amount / forms_with_amount if forms_with_amount > 0 else 0

        return {
            "success": True,
            "data": {
                "total_amount": total_amount,
                "forms_with_amount": forms_with_amount,
                "average_amount": avg_amount,
                "form_details": form_values[:100]  # Limit to 100 for performance
            }
        }

    except Exception as e:
        frappe.log_error(f"Error in get_form_value_tracking: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_recurring_form_trends(property=None, date_from=None, date_to=None, department=None, period="weekly"):
    """
    Get recurring form trends over time

    Args:
        property: Business unit filter
        date_from: Start date for filtering
        date_to: End date for filtering
        department: Department filter
        period: Grouping period (daily, weekly, monthly)

    Returns:
        dict: Form trends data
    """
    try:
        conditions = []
        values = {}

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

        where_clause = " AND " + " AND ".join(conditions) if conditions else ""

        # Determine date grouping based on period
        if period == "daily":
            date_group = "DATE(wfr.requested_on)"
        elif period == "weekly":
            date_group = "YEARWEEK(wfr.requested_on)"
        else:  # monthly
            date_group = "DATE_FORMAT(wfr.requested_on, '%Y-%m')"

        # Query for form trends
        query = f"""
            SELECT
                {date_group} as period,
                wfr.doctype_name as form_type,
                COUNT(*) as count
            FROM `tabWF Workflow Requests` wfr
            LEFT JOIN `tabEzy Employee` emp ON wfr.requested_by = emp.user
            WHERE wfr.docstatus != 2 {where_clause}
            GROUP BY period, wfr.doctype_name
            ORDER BY period DESC, count DESC
        """

        results = frappe.db.sql(query, values=values, as_dict=True)

        # Get most frequently raised forms
        frequency_query = f"""
            SELECT
                wfr.doctype_name as form_type,
                COUNT(*) as total_count,
                COUNT(DISTINCT DATE(wfr.requested_on)) as days_raised,
                ROUND(COUNT(*) / GREATEST(DATEDIFF(MAX(wfr.requested_on), MIN(wfr.requested_on)), 1), 2) as avg_per_day
            FROM `tabWF Workflow Requests` wfr
            LEFT JOIN `tabEzy Employee` emp ON wfr.requested_by = emp.user
            WHERE wfr.docstatus != 2 {where_clause}
            GROUP BY wfr.doctype_name
            ORDER BY total_count DESC
            LIMIT 10
        """

        frequent_forms = frappe.db.sql(frequency_query, values=values, as_dict=True)

        return {
            "success": True,
            "data": {
                "trends": results,
                "most_frequent": frequent_forms
            }
        }

    except Exception as e:
        frappe.log_error(f"Error in get_recurring_form_trends: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_dashboard_filters(property=None):
    """
    Get available filter options for the dashboard

    Args:
        property: Business unit filter

    Returns:
        dict: Available departments, form types, etc.
    """
    try:
        conditions = ""
        values = {}

        if property:
            conditions = "WHERE property = %(property)s"
            values["property"] = property

        # Get departments
        departments = frappe.db.sql("""
            SELECT DISTINCT dept.name, dept.department_name
            FROM `tabEzy Departments` dept
            ORDER BY dept.department_name
        """, as_dict=True)

        # Get form types
        form_types_query = f"""
            SELECT DISTINCT wfr.doctype_name as form_type
            FROM `tabWF Workflow Requests` wfr
            {conditions}
            ORDER BY wfr.doctype_name
        """

        form_types = frappe.db.sql(form_types_query, values=values, as_dict=True)

        # Get business units
        business_units = frappe.db.sql("""
            SELECT name, name as label
            FROM `tabEzy Business Unit`
            ORDER BY name
        """, as_dict=True)

        return {
            "success": True,
            "data": {
                "departments": departments,
                "form_types": form_types,
                "business_units": business_units
            }
        }

    except Exception as e:
        frappe.log_error(f"Error in get_dashboard_filters: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_consolidated_dashboard(property=None, date_from=None, date_to=None, department=None, form_type=None, period="weekly"):
    """
    Get all dashboard data in one API call for better performance

    Args:
        property: Business unit filter
        date_from: Start date for filtering
        date_to: End date for filtering
        department: Department filter
        form_type: Form type filter
        period: Period for trends (daily, weekly, monthly)

    Returns:
        dict: All dashboard data
    """
    try:
        # Set default date range if not provided (last 30 days)
        if not date_from or not date_to:
            date_to = nowdate()
            date_from = add_days(date_to, -30)

        # Get all insights
        status_overview = get_form_status_overview(property, date_from, date_to, department, form_type)
        department_analysis = get_department_wise_analysis(property, date_from, date_to, department)
        value_tracking = get_form_value_tracking(property, date_from, date_to, department, form_type)
        recurring_trends = get_recurring_form_trends(property, date_from, date_to, department, period)
        filters = get_dashboard_filters(property)

        return {
            "success": True,
            "data": {
                "status_overview": status_overview.get("data"),
                "department_analysis": department_analysis.get("data"),
                "value_tracking": value_tracking.get("data"),
                "recurring_trends": recurring_trends.get("data"),
                "filters": filters.get("data"),
                "date_range": {
                    "from": date_from,
                    "to": date_to
                }
            }
        }

    except Exception as e:
        frappe.log_error(f"Error in get_consolidated_dashboard: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }
