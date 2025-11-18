# Advanced Insights Dashboard - System Architecture

## Overview
A complete dashboard builder system that allows users to create custom, interactive dashboards from form data with drag-and-drop widgets, field-level customization, and real-time updates.

## Architecture Components

### 1. Database Schema

#### Ezy Dashboard Configurations (New DocType)
```json
{
  "doctype": "Ezy Dashboard Configuration",
  "fields": [
    {
      "fieldname": "dashboard_name",
      "fieldtype": "Data",
      "label": "Dashboard Name",
      "unique": 1,
      "reqd": 1
    },
    {
      "fieldname": "form_name",
      "fieldtype": "Link",
      "options": "DocType",
      "label": "Form Name",
      "reqd": 1
    },
    {
      "fieldname": "description",
      "fieldtype": "Small Text",
      "label": "Description"
    },
    {
      "fieldname": "layout_config",
      "fieldtype": "Long Text",
      "label": "Layout Configuration (JSON)"
    },
    {
      "fieldname": "widgets",
      "fieldtype": "Table",
      "options": "Ezy Dashboard Widget",
      "label": "Widgets"
    },
    {
      "fieldname": "filters",
      "fieldtype": "Long Text",
      "label": "Default Filters (JSON)"
    },
    {
      "fieldname": "refresh_interval",
      "fieldtype": "Int",
      "label": "Auto Refresh (seconds)",
      "default": 0
    },
    {
      "fieldname": "is_public",
      "fieldtype": "Check",
      "label": "Public Dashboard",
      "default": 0
    },
    {
      "fieldname": "created_by_user",
      "fieldtype": "Link",
      "options": "User",
      "label": "Created By"
    }
  ]
}
```

#### Ezy Dashboard Widget (Child Table)
```json
{
  "doctype": "Ezy Dashboard Widget",
  "istable": 1,
  "fields": [
    {
      "fieldname": "widget_id",
      "fieldtype": "Data",
      "label": "Widget ID",
      "reqd": 1
    },
    {
      "fieldname": "widget_type",
      "fieldtype": "Select",
      "label": "Widget Type",
      "options": "Chart\nTable\nKPI Card\nPie Chart\nBar Chart\nLine Chart\nDonut Chart\nArea Chart\nScatter Chart\nHeatmap",
      "reqd": 1
    },
    {
      "fieldname": "title",
      "fieldtype": "Data",
      "label": "Widget Title",
      "reqd": 1
    },
    {
      "fieldname": "widget_config",
      "fieldtype": "Long Text",
      "label": "Widget Configuration (JSON)",
      "description": "x_field, y_field, aggregate, filters, etc."
    },
    {
      "fieldname": "position_x",
      "fieldtype": "Int",
      "label": "Position X",
      "default": 0
    },
    {
      "fieldname": "position_y",
      "fieldtype": "Int",
      "label": "Position Y",
      "default": 0
    },
    {
      "fieldname": "width",
      "fieldtype": "Int",
      "label": "Width (grid units)",
      "default": 6
    },
    {
      "fieldname": "height",
      "fieldtype": "Int",
      "label": "Height (grid units)",
      "default": 4
    }
  ]
}
```

### 2. API Endpoints

#### Form Management APIs
```
GET  /api/method/ezy_forms.api.v1.insights_forms.get_forms_list
     → Returns list of all forms with metadata

GET  /api/method/ezy_forms.api.v1.insights_forms.get_form_fields
     → Returns fields for a specific form with types

GET  /api/method/ezy_forms.api.v1.insights_forms.get_form_records
     → Returns paginated records with filters

POST /api/method/ezy_forms.api.v1.insights_forms.search_records
     → Search records with advanced filters
```

#### Dashboard Builder APIs
```
POST /api/method/ezy_forms.api.v1.dashboard_advanced.create_dashboard
     → Create new dashboard configuration

GET  /api/method/ezy_forms.api.v1.dashboard_advanced.get_dashboards
     → Get all user dashboards

GET  /api/method/ezy_forms.api.v1.dashboard_advanced.get_dashboard
     → Get specific dashboard with config

PUT  /api/method/ezy_forms.api.v1.dashboard_advanced.update_dashboard
     → Update dashboard configuration

DELETE /api/method/ezy_forms.api.v1.dashboard_advanced.delete_dashboard
       → Delete dashboard

POST /api/method/ezy_forms.api.v1.dashboard_advanced.export_dashboard
     → Export dashboard as JSON file

POST /api/method/ezy_forms.api.v1.dashboard_advanced.import_dashboard
     → Import dashboard from JSON
```

#### Widget Data APIs
```
POST /api/method/ezy_forms.api.v1.widget_data.get_widget_data
     → Get data for a specific widget configuration

POST /api/method/ezy_forms.api.v1.widget_data.get_aggregated_data
     → Get aggregated data (sum, count, avg, etc.)

GET  /api/method/ezy_forms.api.v1.widget_data.get_field_values
     → Get unique values for a field (for filters)
```

### 3. Frontend Components Architecture

```
/src/Pages/Insights/
├── InsightsMain.vue              # Main container with navigation
├── FormsList.vue                 # List all forms with search
├── FormRecords.vue               # Display form records in table
├── DashboardBuilder.vue          # Dashboard builder UI
├── DashboardView.vue             # View saved dashboard
│
├── /components/
│   ├── WidgetLibrary/
│   │   ├── ChartWidget.vue       # ECharts wrapper
│   │   ├── TableWidget.vue       # Data table widget
│   │   ├── KPICard.vue           # KPI card widget
│   │   ├── PieChart.vue          # Pie chart
│   │   ├── BarChart.vue          # Bar chart
│   │   ├── LineChart.vue         # Line chart
│   │   ├── DonutChart.vue        # Donut chart
│   │   ├── AreaChart.vue         # Area chart
│   │   └── WidgetContainer.vue   # Wrapper with actions
│   │
│   ├── DashboardBuilder/
│   │   ├── FieldSelector.vue     # Select X/Y axis fields
│   │   ├── AggregateSelector.vue # Choose aggregate function
│   │   ├── FilterBuilder.vue     # Build complex filters
│   │   ├── WidgetConfigurator.vue # Configure widget
│   │   └── LayoutGrid.vue        # Drag-drop grid
│   │
│   └── Common/
│       ├── RecordTable.vue       # Reusable data table
│       ├── SearchFilter.vue      # Search and filter
│       ├── Pagination.vue        # Pagination control
│       └── ExportButton.vue      # Export functionality
│
└── /composables/
    ├── useDashboard.js           # Dashboard state management
    ├── useWidget.js              # Widget operations
    └── useFormData.js            # Form data fetching
```

### 4. Widget Configuration Schema

```json
{
  "widget_id": "widget_123",
  "widget_type": "bar_chart",
  "title": "Sales by Department",
  "config": {
    "x_field": "department",
    "y_field": "total_amount",
    "aggregate": "sum",
    "group_by": "department",
    "filters": [
      {
        "field": "status",
        "operator": "equals",
        "value": "Completed"
      },
      {
        "field": "requested_on",
        "operator": "between",
        "value": ["2024-01-01", "2024-12-31"]
      }
    ],
    "sort_by": "total_amount",
    "sort_order": "desc",
    "limit": 10,
    "chart_options": {
      "colors": ["#3b82f6", "#10b981"],
      "show_legend": true,
      "show_labels": true,
      "orientation": "vertical"
    }
  },
  "layout": {
    "x": 0,
    "y": 0,
    "w": 6,
    "h": 4
  }
}
```

### 5. Layout Management

Using **vue-grid-layout** for drag-and-drop:

```javascript
{
  "layout": [
    { "i": "widget_1", "x": 0, "y": 0, "w": 6, "h": 4 },
    { "i": "widget_2", "x": 6, "y": 0, "w": 6, "h": 4 },
    { "i": "widget_3", "x": 0, "y": 4, "w": 12, "h": 6 }
  ],
  "cols": 12,
  "rowHeight": 80,
  "isDraggable": true,
  "isResizable": true
}
```

### 6. Performance Optimizations

#### Backend
- **Query Optimization**: Use indexed fields for filters
- **Caching**: Redis cache for frequently accessed data
- **Pagination**: Server-side pagination with cursor-based navigation
- **Data Aggregation**: Push aggregations to database level
- **Connection Pooling**: Reuse database connections

#### Frontend
- **Lazy Loading**: Load widgets on viewport entry
- **Virtual Scrolling**: For large data tables
- **Debouncing**: Search and filter inputs
- **Memoization**: Cache computed widget data
- **Code Splitting**: Lazy load chart libraries
- **Web Workers**: Heavy computations in background

### 7. Real-time Updates

```javascript
// WebSocket connection for real-time updates
frappe.socketio.on('doc_update', (data) => {
  if (data.doctype === currentForm) {
    refreshDashboard();
  }
});

// Polling fallback
setInterval(() => {
  if (autoRefresh && refreshInterval > 0) {
    refreshDashboard();
  }
}, refreshInterval * 1000);
```

### 8. Export/Import Format

```json
{
  "version": "1.0",
  "dashboard": {
    "name": "Sales Dashboard",
    "description": "Monthly sales analysis",
    "form_name": "Sales Order",
    "created_at": "2024-01-01",
    "widgets": [...],
    "layout": [...],
    "filters": {...}
  }
}
```

### 9. Security Considerations

- **Permission Checks**: Validate user has access to form data
- **SQL Injection**: Use parameterized queries
- **XSS Prevention**: Sanitize all user inputs
- **CSRF Protection**: Use Frappe's built-in CSRF tokens
- **Rate Limiting**: Limit API calls per user
- **Data Isolation**: Users only see their allowed data

### 10. Scalability Best Practices

1. **Database Indexing**:
   - Index commonly filtered fields
   - Composite indexes for multi-field queries

2. **Caching Strategy**:
   - Cache dashboard configurations
   - Cache aggregated data with TTL
   - Invalidate cache on data updates

3. **API Design**:
   - Use pagination for all list endpoints
   - Support field selection to reduce payload
   - Batch requests where possible

4. **Frontend Optimization**:
   - Virtualize large lists
   - Lazy load components
   - Use service workers for offline support

5. **Monitoring**:
   - Log slow queries
   - Track API response times
   - Monitor memory usage

## Implementation Priority

### Phase 1: Core (Week 1)
- Form listing and records view
- Basic dashboard creation
- Simple chart widgets (Bar, Pie, Line)

### Phase 2: Advanced (Week 2)
- Drag-and-drop layout
- Advanced filters
- All widget types
- Save/Load dashboards

### Phase 3: Polish (Week 3)
- Export/Import
- Real-time updates
- Performance optimization
- Documentation

## Tech Stack

- **Backend**: Python 3, Frappe Framework
- **Frontend**: Vue 3, TypeScript (optional)
- **Charts**: ECharts 5.6
- **Drag-Drop**: vue-grid-layout
- **Tables**: TanStack Table / Frappe DataTable
- **State**: Pinia (optional) or Composition API
- **HTTP**: Axios
- **Real-time**: Frappe SocketIO

## File Size Estimates

- Backend APIs: ~2000 lines
- Frontend Components: ~4000 lines
- Composables/Utils: ~800 lines
- Total: ~7000 lines of code

This architecture provides a scalable, performant, and user-friendly dashboard builder system.
