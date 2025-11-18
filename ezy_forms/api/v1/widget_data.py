"""
Widget Data API
Provides data for dashboard widgets with aggregations and filtering
"""

import frappe
from frappe import _
import json
from datetime import datetime


@frappe.whitelist()
def get_widget_data(form_name, widget_config):
    """
    Get data for a widget based on its configuration

    Args:
        form_name: Name of the form/doctype
        widget_config: JSON string with widget configuration
            {
                "x_field": "department",
                "y_field": "amount",
                "aggregate": "sum",
                "filters": [...],
                "group_by": "department",
                "sort_by": "amount",
                "sort_order": "desc",
                "limit": 10
            }

    Returns:
        dict: Widget data formatted for visualization
    """
    try:
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        # Parse configuration
        if isinstance(widget_config, str):
            config = json.loads(widget_config)
        else:
            config = widget_config

        x_field = config.get('x_field')
        y_field = config.get('y_field')
        aggregate = config.get('aggregate', 'count')
        filters = config.get('filters', [])
        group_by = config.get('group_by', x_field)
        sort_by = config.get('sort_by', y_field)
        sort_order = config.get('sort_order', 'desc')
        limit = config.get('limit', 100)

        # Build aggregation query
        data = get_aggregated_data(
            form_name=form_name,
            x_field=x_field,
            y_field=y_field,
            aggregate=aggregate,
            filters=filters,
            group_by=group_by,
            sort_by=sort_by,
            sort_order=sort_order,
            limit=limit
        )

        return data

    except Exception as e:
        frappe.log_error(f"Error in get_widget_data: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_aggregated_data(form_name, x_field=None, y_field=None, aggregate="count",
                        filters=None, group_by=None, sort_by=None, sort_order="desc", limit=100):
    """
    Get aggregated data for charts and widgets

    Args:
        form_name: Form/DocType name
        x_field: Field for X-axis (categories)
        y_field: Field for Y-axis (values)
        aggregate: Aggregation function (count, sum, avg, min, max)
        filters: List of filter conditions
        group_by: Field to group by
        sort_by: Field to sort by
        sort_order: Sort order (asc/desc)
        limit: Maximum records to return

    Returns:
        dict: Aggregated data
    """
    try:
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        # Parse filters if string
        if isinstance(filters, str):
            filters = json.loads(filters) if filters else []

        # Build base query
        conditions = ["wfr.docstatus != 2", "wfr.doctype_name = %(form_name)s"]
        values = {"form_name": form_name}

        # Add filters
        if filters:
            for idx, filter_item in enumerate(filters):
                field = filter_item.get('field')
                operator = filter_item.get('operator', 'equals')
                value = filter_item.get('value')

                if not field or value is None:
                    continue

                param_name = f"filter_{idx}"

                if operator == 'equals':
                    conditions.append(f"wfr.{field} = %({param_name})s")
                    values[param_name] = value
                elif operator == 'not_equals':
                    conditions.append(f"wfr.{field} != %({param_name})s")
                    values[param_name] = value
                elif operator == 'contains':
                    conditions.append(f"wfr.{field} LIKE %({param_name})s")
                    values[param_name] = f"%{value}%"
                elif operator == 'greater_than':
                    conditions.append(f"wfr.{field} > %({param_name})s")
                    values[param_name] = value
                elif operator == 'less_than':
                    conditions.append(f"wfr.{field} < %({param_name})s")
                    values[param_name] = value
                elif operator == 'between' and isinstance(value, list) and len(value) == 2:
                    conditions.append(f"wfr.{field} BETWEEN %({param_name}_start)s AND %({param_name}_end)s")
                    values[f"{param_name}_start"] = value[0]
                    values[f"{param_name}_end"] = value[1]

        where_clause = " AND ".join(conditions)

        # Determine aggregation
        if aggregate == 'count':
            agg_expr = "COUNT(*)"
        elif aggregate == 'sum' and y_field:
            agg_expr = f"SUM(CAST(wfr.{y_field} AS DECIMAL(15,2)))"
        elif aggregate == 'avg' and y_field:
            agg_expr = f"AVG(CAST(wfr.{y_field} AS DECIMAL(15,2)))"
        elif aggregate == 'min' and y_field:
            agg_expr = f"MIN(CAST(wfr.{y_field} AS DECIMAL(15,2)))"
        elif aggregate == 'max' and y_field:
            agg_expr = f"MAX(CAST(wfr.{y_field} AS DECIMAL(15,2)))"
        else:
            agg_expr = "COUNT(*)"

        # Build SELECT clause
        if x_field and group_by:
            select_clause = f"wfr.{x_field} as label, {agg_expr} as value"
            group_clause = f"GROUP BY wfr.{x_field}"
        else:
            select_clause = f"{agg_expr} as value"
            group_clause = ""

        # Build ORDER clause
        if sort_by:
            order_clause = f"ORDER BY {sort_by} {sort_order.upper()}"
        else:
            order_clause = "ORDER BY value DESC"

        # Build final query
        query = f"""
            SELECT {select_clause}
            FROM `tabWF Workflow Requests` wfr
            LEFT JOIN `tabEzy Employee` emp ON wfr.requested_by = emp.emp_mail_id
            LEFT JOIN `tabEzy Departments` dept ON emp.department = dept.name
            WHERE {where_clause}
            {group_clause}
            {order_clause}
            LIMIT {int(limit)}
        """

        results = frappe.db.sql(query, values=values, as_dict=True)

        # Format data for charts
        if x_field and group_by:
            labels = [row.get('label') or 'Unknown' for row in results]
            data = [float(row.get('value') or 0) for row in results]
        else:
            labels = []
            data = [float(results[0].get('value') or 0)] if results else [0]

        return {
            "success": True,
            "data": {
                "labels": labels,
                "values": data,
                "raw": results,
                "aggregate": aggregate,
                "total": sum(data) if data else 0
            }
        }

    except Exception as e:
        frappe.log_error(f"Error in get_aggregated_data: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_kpi_data(form_name, field_name, aggregate="count", filters=None, compare_period=None):
    """
    Get KPI card data with optional period comparison

    Args:
        form_name: Form name
        field_name: Field to aggregate
        aggregate: Aggregation function
        filters: Filter conditions
        compare_period: Previous period for comparison (e.g., "last_month")

    Returns:
        dict: KPI value with comparison
    """
    try:
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        # Get current value
        current_data = get_aggregated_data(
            form_name=form_name,
            y_field=field_name,
            aggregate=aggregate,
            filters=filters
        )

        result = {
            "value": current_data["data"]["values"][0] if current_data["success"] else 0,
            "aggregate": aggregate
        }

        # Get comparison if requested
        if compare_period:
            # TODO: Implement period comparison logic
            result["comparison"] = {
                "previous_value": 0,
                "change_percent": 0,
                "trend": "up"
            }

        return {
            "success": True,
            "data": result
        }

    except Exception as e:
        frappe.log_error(f"Error in get_kpi_data: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }


@frappe.whitelist()
def get_time_series_data(form_name, date_field, value_field=None, aggregate="count",
                         period="daily", filters=None, limit=30):
    """
    Get time series data for line/area charts

    Args:
        form_name: Form name
        date_field: Date/datetime field
        value_field: Field to aggregate
        aggregate: Aggregation function
        period: Time period (daily, weekly, monthly, yearly)
        filters: Filter conditions
        limit: Maximum data points

    Returns:
        dict: Time series data
    """
    try:
        if frappe.session.user == "Guest":
            frappe.throw("Authentication required", frappe.AuthenticationError)

        # Parse filters
        if isinstance(filters, str):
            filters = json.loads(filters) if filters else []

        # Build conditions
        conditions = ["wfr.docstatus != 2", "wfr.doctype_name = %(form_name)s"]
        values = {"form_name": form_name}

        # Add filters
        for idx, filter_item in enumerate(filters):
            field = filter_item.get('field')
            operator = filter_item.get('operator', 'equals')
            value = filter_item.get('value')

            if not field or value is None:
                continue

            param_name = f"filter_{idx}"
            if operator == 'equals':
                conditions.append(f"wfr.{field} = %({param_name})s")
                values[param_name] = value

        where_clause = " AND ".join(conditions)

        # Determine date grouping
        if period == 'daily':
            date_format = "DATE(wfr.{})".format(date_field)
        elif period == 'weekly':
            date_format = "YEARWEEK(wfr.{})".format(date_field)
        elif period == 'monthly':
            date_format = "DATE_FORMAT(wfr.{}, '%Y-%m')".format(date_field)
        elif period == 'yearly':
            date_format = "YEAR(wfr.{})".format(date_field)
        else:
            date_format = "DATE(wfr.{})".format(date_field)

        # Determine aggregation
        if aggregate == 'count':
            agg_expr = "COUNT(*)"
        elif aggregate == 'sum' and value_field:
            agg_expr = f"SUM(CAST(wfr.{value_field} AS DECIMAL(15,2)))"
        elif aggregate == 'avg' and value_field:
            agg_expr = f"AVG(CAST(wfr.{value_field} AS DECIMAL(15,2)))"
        else:
            agg_expr = "COUNT(*)"

        # Build query
        query = f"""
            SELECT
                {date_format} as period,
                {agg_expr} as value
            FROM `tabWF Workflow Requests` wfr
            WHERE {where_clause}
            GROUP BY period
            ORDER BY period DESC
            LIMIT {int(limit)}
        """

        results = frappe.db.sql(query, values=values, as_dict=True)

        # Reverse to show chronological order
        results.reverse()

        labels = [str(row.get('period')) for row in results]
        data = [float(row.get('value') or 0) for row in results]

        return {
            "success": True,
            "data": {
                "labels": labels,
                "values": data,
                "period": period,
                "raw": results
            }
        }

    except Exception as e:
        frappe.log_error(f"Error in get_time_series_data: {str(e)}")
        return {
            "success": False,
            "message": str(e)
        }
