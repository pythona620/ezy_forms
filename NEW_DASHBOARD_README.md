# Insights Dashboard - Implementation Guide

## Overview

A new comprehensive Insights Dashboard has been created for the EzyForms application. This dashboard provides advanced analytics and insights for form submissions with powerful filtering capabilities.

## Features Implemented

### 1. Form Status Overview
- Real-time counts of forms by status (Completed, Pending, In Progress, Cancelled)
- Visual pie chart representation of status distribution
- Color-coded stat cards for quick overview

### 2. Department-Wise Form Analysis
- Number of forms submitted by each department
- Types of forms raised per department
- Status breakdown (Completed, Pending, In Progress) per department
- Interactive stacked bar chart visualization
- Detailed table view with top form types per department

### 3. Form Value/Amount Tracking
- Tracks forms that include monetary amounts
- Displays total amount, average amount, and form count
- Detailed table showing recent forms with amounts
- Supports common amount field names: `amount`, `total_amount`, `value`, `total_value`, `total`, `grand_total`

### 4. Recurring Form Trends
- Identifies most frequently raised forms
- Tracks trends over time (daily/weekly/monthly)
- Line chart visualization showing form submission patterns
- Calculates average submissions per day

### 5. Comprehensive Filtering
All insights include the following filter options:

#### Date Filters
- **Today**: Current day only
- **Last 7 Days**: Previous week
- **Last 30 Days**: Previous month (default)
- **This Month**: Current month to date
- **Last Month**: Previous complete month
- **Custom**: User-defined date range

#### Category Filters
- **Department**: Filter by specific department
- **Form Type**: Filter by specific form/doctype
- **Business Unit**: Filter by property/business unit
- **Trend Period**: Choose between daily, weekly, or monthly grouping

## Files Created

### Backend API
**File**: `/apps/ezy_forms/ezy_forms/api/v1/new_dashboard.py`

API endpoints created:
1. `get_form_status_overview()` - Form status counts with filters
2. `get_department_wise_analysis()` - Department-wise statistics
3. `get_form_value_tracking()` - Form amount tracking
4. `get_recurring_form_trends()` - Trend analysis over time
5. `get_dashboard_filters()` - Available filter options
6. `get_consolidated_dashboard()` - All data in one call (recommended)

All APIs are whitelisted using `@frappe.whitelist()` and require authentication.

### Frontend Component
**File**: `/apps/ezy_forms/ezyformsfrontend/src/Pages/Dashboard/NewDashboard.vue`

Features:
- Responsive design with mobile support
- Interactive charts using ECharts library
- Real-time filtering without page refresh
- Professional UI with color-coded stats
- Data tables with sorting and display limits

### Router Configuration
**File**: `/apps/ezy_forms/ezyformsfrontend/src/Pages/Dashboard/dashboardroute.js`

New route added: `/dashboard/insights`

### API URLs Configuration
**File**: `/apps/ezy_forms/ezyformsfrontend/src/shared/apiurls.js`

Six new API endpoints added to the `apis` object.

## How to Access

### Option 1: Direct URL
Navigate to: `http://your-domain/ezyformsfrontend/#/dashboard/insights`

### Option 2: Add Navigation Link
Add the following link to your navigation menu/sidebar:

```vue
<router-link to="/dashboard/insights">Insights Dashboard</router-link>
```

Or programmatically navigate:

```javascript
this.$router.push('/dashboard/insights');
// or
this.$router.push({ name: 'InsightsDashboard' });
```

## Installation Steps

### 1. Backend Setup

No additional installation is required. The API file is already in place.

If you need to verify the API is accessible:

```bash
# From bench directory
bench --site [your-site] console
```

Then in the Python console:
```python
import ezy_forms.api.v1.new_dashboard
# If no errors, the module is accessible
```

### 2. Frontend Setup

Build the frontend to include the new component:

```bash
cd apps/ezy_forms/ezyformsfrontend
npm install  # If not already done
npm run build
```

### 3. Clear Cache

```bash
# From bench directory
bench --site [your-site] clear-cache
bench restart
```

## Usage Examples

### Basic Usage
1. Navigate to `/dashboard/insights`
2. Select desired filters (date range, department, etc.)
3. Click "Apply Filters" to refresh data
4. Click "Reset" to clear all filters

### Analyzing Department Performance
1. Select a date range (e.g., "This Month")
2. Leave department filter as "All Departments"
3. View the Department-Wise Analysis section
4. Check the bar chart and table for department comparison

### Tracking Form Amounts
1. Select date range
2. Optional: Filter by specific department or form type
3. Scroll to "Form Value/Amount Tracking" section
4. View total amounts, averages, and detailed breakdown

### Identifying Trends
1. Select a longer date range (e.g., "Last 30 Days")
2. Choose trend period (daily/weekly/monthly)
3. View "Recurring Form Trends" section
4. Check "Most Frequently Raised Forms" table
5. Analyze the trend chart for patterns

## API Response Structure

### Consolidated Dashboard API
**Endpoint**: `get_consolidated_dashboard()`

**Parameters**:
- `property` (optional): Business unit filter
- `date_from` (optional): Start date (YYYY-MM-DD)
- `date_to` (optional): End date (YYYY-MM-DD)
- `department` (optional): Department name/ID
- `form_type` (optional): Form/DocType name
- `period` (optional): 'daily', 'weekly', or 'monthly' (default: 'weekly')

**Response**:
```json
{
  "success": true,
  "data": {
    "status_overview": {
      "Completed": 150,
      "Pending": 45,
      "In Progress": 20,
      "Cancelled": 5,
      "Total": 220
    },
    "department_analysis": [
      {
        "department": "Finance",
        "total_forms": 80,
        "completed": 60,
        "pending": 15,
        "in_progress": 5,
        "form_types": [
          {"form_type": "Purchase Request", "count": 50},
          {"form_type": "Expense Claim", "count": 30}
        ]
      }
    ],
    "value_tracking": {
      "total_amount": 125000.50,
      "forms_with_amount": 75,
      "average_amount": 1666.67,
      "form_details": [...]
    },
    "recurring_trends": {
      "trends": [...],
      "most_frequent": [
        {
          "form_type": "Leave Request",
          "total_count": 120,
          "days_raised": 25,
          "avg_per_day": 4.8
        }
      ]
    },
    "filters": {
      "departments": [...],
      "form_types": [...],
      "business_units": [...]
    },
    "date_range": {
      "from": "2025-10-18",
      "to": "2025-11-17"
    }
  }
}
```

## Customization

### Adding New Metrics
To add new metrics to the dashboard:

1. **Backend**: Add a new function in `new_dashboard.py`:
```python
@frappe.whitelist()
def get_custom_metric(property=None, date_from=None, date_to=None):
    # Your logic here
    return {"success": True, "data": result}
```

2. **API URLs**: Add to `apiurls.js`:
```javascript
getCustomMetric: domain + `/method/ezy_forms.api.v1.new_dashboard.get_custom_metric`
```

3. **Frontend**: Call in `NewDashboard.vue`:
```javascript
const customData = await api_req_data(apis.getCustomMetric, params);
```

### Modifying Chart Colors
Edit the color values in the chart rendering methods:
- `renderStatusChart()` - Line 630+
- `renderDepartmentChart()` - Line 660+
- `renderTrendChart()` - Line 700+

### Changing Date Range Defaults
Modify the `selectedDateRange` ref in `NewDashboard.vue`:
```javascript
const selectedDateRange = ref('last30days'); // Change to desired default
```

## Performance Considerations

1. **Consolidated API**: The `get_consolidated_dashboard()` endpoint is recommended for better performance as it makes a single API call instead of multiple calls.

2. **Data Limits**: Form value details are limited to 100 records by default. Modify in `get_form_value_tracking()` if needed:
```python
"form_details": form_values[:100]  # Change limit here
```

3. **Chart Performance**: Only the top 5 form types are shown in the trend chart. Modify in `renderTrendChart()` if needed.

4. **Caching**: Consider implementing caching for frequently accessed data ranges.

## Security

All API endpoints:
- Require authentication (`@frappe.whitelist()`)
- Use parameterized SQL queries to prevent SQL injection
- Validate user permissions through Frappe's permission system
- Log errors for debugging without exposing sensitive information

## Troubleshooting

### Dashboard Not Loading
1. Check browser console for errors
2. Verify API endpoints are accessible: `/api/method/ezy_forms.api.v1.new_dashboard.get_consolidated_dashboard`
3. Clear browser cache
4. Rebuild frontend: `npm run build`

### No Data Showing
1. Verify workflow requests exist in `WF Workflow Requests` DocType
2. Check date range filters
3. Verify user has permission to view workflow requests
4. Check browser console for API errors

### Chart Not Rendering
1. Ensure ECharts library is installed: `npm install echarts`
2. Check console for initialization errors
3. Verify chart ref elements exist in DOM

### Permission Errors
1. Ensure user has read permission on:
   - WF Workflow Requests
   - Ezy Employee
   - Ezy Departments
2. Check role assignments

## Future Enhancements

Potential improvements:
1. Export dashboard data to Excel/PDF
2. Scheduled email reports
3. Custom dashboard widgets
4. Real-time updates using WebSocket
5. Drill-down capabilities for detailed analysis
6. Comparison views (e.g., month-over-month)
7. User-defined custom metrics
8. Dashboard sharing and collaboration

## Support

For issues or questions:
1. Check Frappe logs: `sites/[site]/logs/error.log`
2. Review browser console errors
3. Verify all files are in correct locations
4. Ensure dependencies are installed

## Version History

**Version 1.0** (November 2025)
- Initial implementation
- Core features: Status overview, department analysis, value tracking, trends
- Comprehensive filtering system
- Interactive charts and data tables

---

**Created**: November 2025
**Last Updated**: November 17, 2025
