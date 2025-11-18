# Advanced Dashboard Builder - Implementation Plan

## What Has Been Completed

### ✅ Phase 1: Foundation
1. **Architecture Document** - Complete system architecture with database schema, API design, and component structure
2. **Forms API** (`insights_forms.py`) - Backend API for:
   - Listing all forms with metadata and counts
   - Getting form field definitions with types
   - Fetching paginated form records with filters
   - Getting unique field values for dropdowns

### ✅ Previous Implementation
- Basic dashboard listing
- Simple chart creation
- Form insights API
- Export functionality

## Next Steps - Complete Implementation

### Phase 2: Core Dashboard System (Priority 1)

#### Backend APIs to Create:

**1. `widget_data.py` - Widget Data Provider**
```python
@frappe.whitelist()
def get_widget_data(widget_config):
    """
    Get data for any widget based on configuration
    - Supports all aggregations (sum, count, avg, min, max)
    - Handles grouping and filtering
    - Returns data in format ready for charts
    """

@frappe.whitelist()
def get_aggregated_data(form_name, x_field, y_field, aggregate, filters, group_by):
    """
    Get aggregated data for charts
    - X-axis field
    - Y-axis field with aggregation
    - Complex filters
    - Group by support
    """
```

**2. `dashboard_config.py` - Dashboard Management**
```python
@frappe.whitelist()
def save_dashboard_config(dashboard_name, form_name, widgets, layout, filters):
    """
    Save complete dashboard configuration
    - Widget configurations
    - Layout positions (x, y, w, h)
    - Default filters
    """

@frappe.whitelist()
def update_dashboard_layout(dashboard_name, layout):
    """
    Update only layout (for drag-drop)
    """

@frappe.whitelist()
def export_dashboard_json(dashboard_name):
    """
    Export dashboard as downloadable JSON
    """

@frappe.whitelist()
def import_dashboard_json(json_data):
    """
    Import dashboard from JSON file
    """
```

#### Frontend Components to Create:

**1. Main Views** (`/src/Pages/Insights/`)

```vue
<!-- InsightsMain.vue -->
<template>
  <div class="insights-main">
    <nav>
      <router-link to="/insights/forms">Forms</router-link>
      <router-link to="/insights/dashboards">Dashboards</router-link>
    </nav>
    <router-view />
  </div>
</template>
```

```vue
<!-- FormsList.vue -->
<template>
  <div class="forms-list">
    <div class="header">
      <h2>Forms</h2>
      <input v-model="search" placeholder="Search forms..." />
    </div>

    <div class="forms-grid">
      <div v-for="form in filteredForms" :key="form.form_name"
           class="form-card"
           @click="viewForm(form)">
        <h3>{{ form.form_name }}</h3>
        <div class="stats">
          <span>{{ form.total_records }} records</span>
          <span>{{ form.completed_count }} completed</span>
        </div>
        <button @click.stop="createDashboard(form)">
          Create Dashboard
        </button>
      </div>
    </div>
  </div>
</template>
```

```vue
<!-- FormRecords.vue -->
<template>
  <div class="form-records">
    <div class="toolbar">
      <button @click="$router.back()">← Back</button>
      <h2>{{ formName }} - Records</h2>
      <button @click="createDashboard">Create Dashboard</button>
    </div>

    <!-- Filters -->
    <div class="filters">
      <input v-model="searchQuery" placeholder="Search..." />
      <FilterBuilder v-model="filters" :fields="formFields" />
    </div>

    <!-- Data Table with Pagination -->
    <RecordTable
      :records="records"
      :fields="displayFields"
      :loading="loading"
      @sort="handleSort"
    />

    <Pagination
      v-model="currentPage"
      :totalPages="totalPages"
      :totalRecords="totalRecords"
    />
  </div>
</template>
```

```vue
<!-- DashboardBuilder.vue -->
<template>
  <div class="dashboard-builder">
    <!-- Left Sidebar: Widget Library -->
    <aside class="widget-library">
      <h3>Add Widget</h3>
      <div class="widget-types">
        <div v-for="type in widgetTypes" :key="type.id"
             class="widget-type"
             draggable="true"
             @dragstart="onDragStart(type)">
          <i :class="type.icon"></i>
          <span>{{ type.name }}</span>
        </div>
      </div>
    </aside>

    <!-- Main Area: Grid Layout -->
    <main class="dashboard-canvas">
      <grid-layout
        v-model:layout="layout"
        :col-num="12"
        :row-height="80"
        :is-draggable="true"
        :is-resizable="true"
        @layout-updated="onLayoutChange">

        <grid-item
          v-for="widget in widgets"
          :key="widget.id"
          :x="widget.x"
          :y="widget.y"
          :w="widget.w"
          :h="widget.h"
          :i="widget.id">

          <WidgetContainer
            :widget="widget"
            @configure="configureWidget(widget)"
            @delete="deleteWidget(widget.id)" />

        </grid-item>
      </grid-layout>
    </main>

    <!-- Right Sidebar: Widget Configuration -->
    <aside class="widget-config" v-if="selectedWidget">
      <h3>Configure Widget</h3>

      <FieldSelector
        v-model:xField="selectedWidget.config.x_field"
        v-model:yField="selectedWidget.config.y_field"
        :fields="formFields"
      />

      <AggregateSelector
        v-model="selectedWidget.config.aggregate"
        :yFieldType="getFieldType(selectedWidget.config.y_field)"
      />

      <FilterBuilder
        v-model="selectedWidget.config.filters"
        :fields="formFields"
      />

      <button @click="saveWidget">Save Widget</button>
    </aside>

    <!-- Bottom Toolbar -->
    <div class="toolbar">
      <button @click="saveDashboard">Save Dashboard</button>
      <button @click="previewDashboard">Preview</button>
      <button @click="exportDashboard">Export JSON</button>
      <button @click="cancelEdit">Cancel</button>
    </div>
  </div>
</template>
```

**2. Widget Components** (`/src/Pages/Insights/components/WidgetLibrary/`)

```vue
<!-- ChartWidget.vue -->
<template>
  <div class="chart-widget">
    <div class="widget-header">
      <h4>{{ widget.title }}</h4>
      <button @click="refresh">↻</button>
    </div>
    <div ref="chartRef" class="chart-container"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import * as echarts from 'echarts';

const props = defineProps(['widget', 'data']);
const chartRef = ref(null);
let chartInstance = null;

onMounted(() => {
  chartInstance = echarts.init(chartRef.value);
  renderChart();
});

watch(() => props.data, renderChart);

function renderChart() {
  const option = generateChartOption(props.widget.type, props.data);
  chartInstance.setOption(option);
}
</script>
```

```vue
<!-- KPICard.vue -->
<template>
  <div class="kpi-card" :class="cardClass">
    <div class="kpi-icon">
      <i :class="icon"></i>
    </div>
    <div class="kpi-content">
      <h4>{{ title }}</h4>
      <div class="kpi-value">{{ formattedValue }}</div>
      <div class="kpi-change" v-if="change">
        <i :class="change > 0 ? 'pi pi-arrow-up' : 'pi pi-arrow-down'"></i>
        {{ Math.abs(change) }}%
      </div>
    </div>
  </div>
</template>
```

**3. Utility Components** (`/src/Pages/Insights/components/`)

```vue
<!-- FieldSelector.vue -->
<template>
  <div class="field-selector">
    <div class="field-group">
      <label>X-Axis (Categories)</label>
      <select v-model="localXField">
        <option v-for="field in categoricalFields" :key="field.fieldname" :value="field.fieldname">
          {{ field.label }}
        </option>
      </select>
    </div>

    <div class="field-group">
      <label>Y-Axis (Values)</label>
      <select v-model="localYField">
        <option v-for="field in numericFields" :key="field.fieldname" :value="field.fieldname">
          {{ field.label }}
        </option>
      </select>
    </div>
  </div>
</template>
```

```vue
<!-- AggregateSelector.vue -->
<template>
  <div class="aggregate-selector">
    <label>Aggregation Function</label>
    <select v-model="localAggregate">
      <option value="count">Count</option>
      <option value="sum" :disabled="!isNumeric">Sum</option>
      <option value="avg" :disabled="!isNumeric">Average</option>
      <option value="min" :disabled="!isNumeric">Minimum</option>
      <option value="max" :disabled="!isNumeric">Maximum</option>
    </select>
  </div>
</template>
```

```vue
<!-- FilterBuilder.vue -->
<template>
  <div class="filter-builder">
    <h4>Filters</h4>
    <div v-for="(filter, idx) in localFilters" :key="idx" class="filter-row">
      <select v-model="filter.field">
        <option v-for="field in fields" :key="field.fieldname" :value="field.fieldname">
          {{ field.label }}
        </option>
      </select>

      <select v-model="filter.operator">
        <option value="equals">Equals</option>
        <option value="not_equals">Not Equals</option>
        <option value="contains">Contains</option>
        <option value="greater_than">Greater Than</option>
        <option value="less_than">Less Than</option>
        <option value="between">Between</option>
      </select>

      <input v-model="filter.value" placeholder="Value" />

      <button @click="removeFilter(idx)">×</button>
    </div>

    <button @click="addFilter">+ Add Filter</button>
  </div>
</template>
```

### Phase 3: Advanced Features (Priority 2)

#### Features to Implement:

**1. Drag-and-Drop Layout**
- Install: `npm install vue-grid-layout`
- Configure responsive breakpoints
- Save layout positions

**2. Real-time Updates**
```javascript
// composables/useRealtimeUpdates.js
import { ref, onMounted, onUnmounted } from 'vue';

export function useRealtimeUpdates(formName, refreshCallback) {
  const isConnected = ref(false);

  onMounted(() => {
    // Connect to Frappe socketio
    frappe.socketio.on('doc_update', (data) => {
      if (data.doctype === formName) {
        refreshCallback();
      }
    });
    isConnected.value = true;
  });

  onUnmounted(() => {
    frappe.socketio.off('doc_update');
  });

  return { isConnected };
}
```

**3. Auto-refresh**
```javascript
// In DashboardView.vue
const refreshInterval = ref(0); // seconds

watchEffect(() => {
  if (refreshInterval.value > 0) {
    const intervalId = setInterval(() => {
      refreshAllWidgets();
    }, refreshInterval.value * 1000);

    onUnmounted(() => clearInterval(intervalId));
  }
});
```

**4. Export/Import Dashboards**
```javascript
function exportDashboard() {
  const config = {
    version: '1.0',
    dashboard: {
      name: dashboardName.value,
      form_name: formName.value,
      widgets: widgets.value,
      layout: layout.value,
      filters: defaultFilters.value
    }
  };

  const blob = new Blob([JSON.stringify(config, null, 2)], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${dashboardName.value}.json`;
  a.click();
  URL.revokeObjectURL(url);
}

function importDashboard(file) {
  const reader = new FileReader();
  reader.onload = (e) => {
    const config = JSON.parse(e.target.result);
    // Validate and load configuration
    loadDashboardConfig(config);
  };
  reader.readAsText(file);
}
```

### Phase 4: Performance Optimization (Priority 3)

**1. Virtual Scrolling for Tables**
```vue
<template>
  <RecycleScroller
    :items="records"
    :item-size="50"
    key-field="name"
    v-slot="{ item }">
    <div class="table-row">{{ item.name }}</div>
  </RecycleScroller>
</template>
```

**2. Lazy Loading Widgets**
```vue
<component
  :is="getWidgetComponent(widget.type)"
  v-if="isInViewport(widget.id)"
  :widget="widget"
  :data="widgetData[widget.id]"
/>
```

**3. Debounced Search**
```javascript
import { debounce } from 'lodash-es';

const debouncedSearch = debounce((query) => {
  searchRecords(query);
}, 300);
```

**4. Memoized Computations**
```javascript
const aggregatedData = computed(() => {
  return memoize((widgetId) => {
    return calculateAggregation(widgets.value.find(w => w.id === widgetId));
  });
});
```

### Phase 5: Testing & Documentation (Priority 4)

**1. Unit Tests**
```python
# test_insights_api.py
def test_get_forms_list():
    result = get_forms_list()
    assert result["success"] == True
    assert len(result["data"]) > 0

def test_get_widget_data():
    config = {
        "x_field": "department",
        "y_field": "amount",
        "aggregate": "sum"
    }
    result = get_widget_data("Sales Order", config)
    assert "data" in result
```

**2. User Documentation**
- How to create dashboards
- Widget configuration guide
- Filter syntax
- Export/import process
- Best practices

## Installation Steps

```bash
# 1. Navigate to frontend
cd /home/caratred/ezyinvoice-bench/apps/ezy_forms/ezyformsfrontend

# 2. Install dependencies
npm install vue-grid-layout
npm install vue-virtual-scroller
npm install lodash-es

# 3. Build
npm run build

# 4. Restart Frappe
cd /home/caratred/ezyinvoice-bench
bench restart
```

## API Endpoints Summary

```
Forms Management:
  GET  /api/method/ezy_forms.api.v1.insights_forms.get_forms_list
  GET  /api/method/ezy_forms.api.v1.insights_forms.get_form_fields
  GET  /api/method/ezy_forms.api.v1.insights_forms.get_form_records
  GET  /api/method/ezy_forms.api.v1.insights_forms.get_field_values

Widget Data:
  POST /api/method/ezy_forms.api.v1.widget_data.get_widget_data
  POST /api/method/ezy_forms.api.v1.widget_data.get_aggregated_data

Dashboard Config:
  POST /api/method/ezy_forms.api.v1.dashboard_config.save_dashboard_config
  GET  /api/method/ezy_forms.api.v1.dashboard_config.get_dashboard_configs
  PUT  /api/method/ezy_forms.api.v1.dashboard_config.update_dashboard_layout
  POST /api/method/ezy_forms.api.v1.dashboard_config.export_dashboard_json
  POST /api/method/ezy_forms.api.v1.dashboard_config.import_dashboard_json
  DEL  /api/method/ezy_forms.api.v1.dashboard_config.delete_dashboard_config
```

## Estimated Timeline

- **Phase 2 (Core)**: 3-4 days
- **Phase 3 (Advanced)**: 2-3 days
- **Phase 4 (Optimization)**: 1-2 days
- **Phase 5 (Testing)**: 1-2 days

**Total**: 7-11 days for complete implementation

## Next Immediate Steps

1. ✅ Create `widget_data.py` API
2. ✅ Create `dashboard_config.py` API
3. ✅ Update `apiurls.js` with new endpoints
4. ✅ Create `InsightsMain.vue` router setup
5. ✅ Create `FormsList.vue` component
6. ✅ Create `FormRecords.vue` component
7. ✅ Create `DashboardBuilder.vue` component
8. ✅ Create widget components (Chart, KPI, Table)
9. ✅ Create utility components (FieldSelector, FilterBuilder)
10. ✅ Add drag-drop with vue-grid-layout
11. ✅ Test and refine

The architecture is designed to be:
- **Modular**: Each component is self-contained
- **Scalable**: Can handle thousands of records with pagination and virtualization
- **Extensible**: Easy to add new widget types and features
- **Performant**: Optimized queries, caching, and lazy loading
- **User-friendly**: Intuitive drag-and-drop interface
