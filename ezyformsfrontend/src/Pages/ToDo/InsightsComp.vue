<template>
  <div class="insights-container">
    <!-- View Mode: Show Saved Dashboards -->
    <div v-if="viewMode === 'list'" class="dashboard-list-view">
      <div class="page-header">
        <div class="header-left">
          <h2 class="page-title">
            <i class="pi pi-chart-bar"></i>
            My Dashboards
          </h2>
          <p class="page-subtitle">Create and view custom dashboards for your forms</p>
        </div>
        <button class="create-btn" @click="startCreateDashboard">
          <i class="pi pi-plus"></i>
          Create New Dashboard
        </button>
      </div>

      <!-- Saved Dashboards Grid -->
      <div v-if="savedDashboards.length > 0" class="dashboards-grid">
        <div
          v-for="dashboard in savedDashboards"
          :key="dashboard.name"
          class="dashboard-card"
          @click="viewDashboard(dashboard)"
        >
          <div class="dashboard-card-header">
            <h3>{{ dashboard.dashboard_name }}</h3>
            <button
              class="delete-icon-btn"
              @click.stop="confirmDeleteDashboard(dashboard)"
              v-if="dashboard.created_by === currentUser || isSystemManager"
            >
              <i class="pi pi-trash"></i>
            </button>
          </div>
          <div class="dashboard-card-body">
            <p class="form-name">
              <i class="pi pi-file"></i>
              {{ dashboard.form_name }}
            </p>
            <p class="chart-count">
              <i class="pi pi-chart-line"></i>
              {{ getChartCount(dashboard.chart_config) }} charts configured
            </p>
            <p class="created-by">
              <i class="pi pi-user"></i>
              Created by {{ dashboard.created_by }}
            </p>
          </div>
          <div class="dashboard-card-footer">
            <button class="view-btn" @click.stop="viewDashboard(dashboard)">
              <i class="pi pi-eye"></i>
              View Dashboard
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <i class="pi pi-chart-line empty-icon"></i>
        <h3>No Dashboards Yet</h3>
        <p>Create your first custom dashboard by clicking the button above</p>
      </div>
    </div>

    <!-- Create Mode: Select Form and Configure Charts -->
    <div v-else-if="viewMode === 'create'" class="dashboard-create-view">
      <div class="page-header">
        <button class="back-btn" @click="cancelCreate">
          <i class="pi pi-arrow-left"></i>
          Back to Dashboards
        </button>
        <h2 class="page-title">Create New Dashboard</h2>
      </div>

      <!-- Step 1: Form Selection -->
      <div class="step-card" v-if="createStep === 1">
        <h3 class="step-title">Step 1: Select Form</h3>
        <div class="form-grid">
          <div
            v-for="form in availableForms"
            :key="form.form_name"
            class="form-option-card"
            :class="{ selected: selectedForm === form.form_name }"
            @click="selectForm(form.form_name)"
          >
            <i class="pi pi-file"></i>
            <h4>{{ form.form_name }}</h4>
            <p>{{ form.total_submissions }} submissions</p>
          </div>
        </div>
        <div class="step-actions">
          <button class="next-btn" :disabled="!selectedForm" @click="nextStep">
            Next: Configure Charts
            <i class="pi pi-arrow-right"></i>
          </button>
        </div>
      </div>

      <!-- Step 2: Chart Configuration -->
      <div class="step-card" v-if="createStep === 2">
        <h3 class="step-title">Step 2: Select Charts to Display</h3>
        <p class="step-subtitle">Choose which visualizations you want in your dashboard</p>

        <div class="chart-options-grid">
          <div
            v-for="chart in availableCharts"
            :key="chart.id"
            class="chart-option-card"
            :class="{ selected: chartConfig[chart.id] }"
            @click="toggleChart(chart.id)"
          >
            <div class="chart-icon">
              <i :class="chart.icon"></i>
            </div>
            <h4>{{ chart.name }}</h4>
            <p>{{ chart.description }}</p>
            <div class="checkbox-indicator">
              <i :class="chartConfig[chart.id] ? 'pi pi-check-circle' : 'pi pi-circle'"></i>
            </div>
          </div>
        </div>

        <div class="step-actions">
          <button class="back-btn-secondary" @click="prevStep">
            <i class="pi pi-arrow-left"></i>
            Back
          </button>
          <button class="next-btn" :disabled="!hasSelectedCharts" @click="nextStep">
            Next: Save Dashboard
            <i class="pi pi-arrow-right"></i>
          </button>
        </div>
      </div>

      <!-- Step 3: Name and Save -->
      <div class="step-card" v-if="createStep === 3">
        <h3 class="step-title">Step 3: Name Your Dashboard</h3>
        <div class="name-input-section">
          <label>Dashboard Name</label>
          <input
            type="text"
            v-model="dashboardName"
            placeholder="e.g., Monthly Sales Overview"
            class="dashboard-name-input"
          >

          <div class="summary-section">
            <h4>Summary</h4>
            <p><strong>Form:</strong> {{ selectedForm }}</p>
            <p><strong>Charts:</strong> {{ getSelectedChartNames().join(', ') }}</p>
          </div>
        </div>

        <div class="step-actions">
          <button class="back-btn-secondary" @click="prevStep">
            <i class="pi pi-arrow-left"></i>
            Back
          </button>
          <button class="save-btn" :disabled="!dashboardName.trim() || saving" @click="saveDashboard">
            <i class="pi pi-save"></i>
            {{ saving ? 'Saving...' : 'Save Dashboard' }}
          </button>
        </div>
      </div>
    </div>

    <!-- View Mode: Display Dashboard -->
    <div v-else-if="viewMode === 'view'" class="dashboard-view">
      <div class="page-header">
        <button class="back-btn" @click="backToList">
          <i class="pi pi-arrow-left"></i>
          Back to Dashboards
        </button>
        <div class="header-center">
          <h2 class="page-title">{{ currentDashboard?.dashboard_name }}</h2>
          <p class="page-subtitle">{{ currentDashboard?.form_name }}</p>
        </div>
        <button class="export-btn" @click="toggleExportMenu" v-if="insightsData">
          <i class="pi pi-download"></i>
          Export
        </button>
        <div v-if="showExportMenu" class="export-menu">
          <div class="export-option" @click="exportData('csv')">
            <i class="pi pi-file"></i>
            Export as CSV
          </div>
        </div>
      </div>

      <!-- Filters -->
      <div class="filters-section">
        <div class="filter-group">
          <label><i class="pi pi-building"></i> Department</label>
          <select v-model="viewFilters.department" @change="loadDashboardData" class="form-select">
            <option value="">All Departments</option>
            <option v-for="dept in departments" :key="dept.name" :value="dept.name">
              {{ dept.department_name }}
            </option>
          </select>
        </div>

        <div class="filter-group">
          <label><i class="pi pi-calendar"></i> Date Range</label>
          <select v-model="viewFilters.dateRange" @change="onDateRangeChange" class="form-select">
            <option value="last30days">Last 30 Days</option>
            <option value="last90days">Last 90 Days</option>
            <option value="last6months">Last 6 Months</option>
            <option value="lastyear">Last Year</option>
          </select>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading dashboard...</p>
      </div>

      <!-- Dashboard Content -->
      <div v-else-if="insightsData" class="dashboard-content">
        <!-- Summary Cards (always shown) -->
        <div class="summary-cards">
          <div class="summary-card card-blue">
            <div class="card-icon"><i class="pi pi-file"></i></div>
            <div class="card-content">
              <h4>Total Submissions</h4>
              <p class="card-value">{{ getTotalSubmissions() }}</p>
            </div>
          </div>
          <div class="summary-card card-green">
            <div class="card-icon"><i class="pi pi-check-circle"></i></div>
            <div class="card-content">
              <h4>Completed</h4>
              <p class="card-value">{{ getStatusCount('Completed') }}</p>
              <span class="card-percentage">{{ getStatusPercentage('Completed') }}%</span>
            </div>
          </div>
          <div class="summary-card card-yellow">
            <div class="card-icon"><i class="pi pi-clock"></i></div>
            <div class="card-content">
              <h4>Pending</h4>
              <p class="card-value">{{ getStatusCount('Pending') }}</p>
              <span class="card-percentage">{{ getStatusPercentage('Pending') }}%</span>
            </div>
          </div>
          <div class="summary-card card-purple">
            <div class="card-icon"><i class="pi pi-hourglass"></i></div>
            <div class="card-content">
              <h4>Avg. Processing Time</h4>
              <p class="card-value">{{ getAvgProcessingTime() }}</p>
              <span class="card-subtitle">hours</span>
            </div>
          </div>
        </div>

        <!-- Configured Charts -->
        <div class="charts-container">
          <!-- Status Chart -->
          <div v-if="currentDashboard?.chart_config?.statusChart" class="chart-card">
            <div class="chart-header">
              <h3>Status Distribution</h3>
            </div>
            <div ref="statusChart" class="chart-content"></div>
          </div>

          <!-- Department Chart -->
          <div v-if="currentDashboard?.chart_config?.departmentChart" class="chart-card">
            <div class="chart-header">
              <h3>Department Breakdown</h3>
            </div>
            <div ref="departmentChart" class="chart-content"></div>
          </div>

          <!-- Trend Chart -->
          <div v-if="currentDashboard?.chart_config?.trendChart" class="chart-card chart-wide">
            <div class="chart-header">
              <h3>Monthly Trends</h3>
            </div>
            <div ref="trendChart" class="chart-content"></div>
          </div>

          <!-- Top Requestors Table -->
          <div v-if="currentDashboard?.chart_config?.requestorsTable" class="table-card">
            <div class="table-header">
              <h3><i class="pi pi-users"></i> Top Requestors</h3>
            </div>
            <div class="table-responsive">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>#</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Department</th>
                    <th>Total</th>
                    <th>Completed</th>
                    <th>Rate</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(req, idx) in insightsData.top_requestors" :key="idx">
                    <td>{{ idx + 1 }}</td>
                    <td>{{ req.requestor_name }}</td>
                    <td>{{ req.requestor_email }}</td>
                    <td>{{ req.department || 'N/A' }}</td>
                    <td>{{ req.total_requests }}</td>
                    <td>{{ req.completed }}</td>
                    <td>
                      <span class="completion-badge" :class="getCompletionClass(req)">
                        {{ ((req.completed / req.total_requests) * 100).toFixed(1) }}%
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Submissions Table -->
          <div v-if="currentDashboard?.chart_config?.submissionsTable" class="table-card">
            <div class="table-header">
              <h3><i class="pi pi-list"></i> All Submissions</h3>
            </div>
            <div class="table-responsive">
              <table class="data-table">
                <thead>
                  <tr>
                    <th>Request ID</th>
                    <th>Date</th>
                    <th>Requestor</th>
                    <th>Department</th>
                    <th>Status</th>
                    <th>Processing (hrs)</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="sub in insightsData.submissions.slice(0, 50)" :key="sub.request_id">
                    <td>{{ sub.request_id }}</td>
                    <td>{{ formatDate(sub.requested_on) }}</td>
                    <td>{{ sub.requestor }}</td>
                    <td>{{ sub.department || 'N/A' }}</td>
                    <td>
                      <span class="status-badge" :class="getStatusClass(sub.status)">
                        {{ sub.status }}
                      </span>
                    </td>
                    <td>{{ sub.processing_hours }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Delete Confirmation Modal -->
    <div v-if="showDeleteModal" class="modal-overlay" @click="showDeleteModal = false">
      <div class="modal-content" @click.stop>
        <h3>Delete Dashboard</h3>
        <p>Are you sure you want to delete "{{ dashboardToDelete?.dashboard_name }}"?</p>
        <div class="modal-actions">
          <button class="cancel-btn" @click="showDeleteModal = false">Cancel</button>
          <button class="confirm-delete-btn" @click="deleteDashboard">Delete</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue';
import * as echarts from 'echarts';
import { apis, doctypes } from '../../shared/apiurls';
import axiosInstance from '../../shared/services/interceptor';
import frappe from '../../shared/services/auth';

// View modes
const viewMode = ref('list'); // 'list', 'create', 'view'
const createStep = ref(1); // 1: select form, 2: configure charts, 3: name dashboard

// Data
const savedDashboards = ref([]);
const availableForms = ref([]);
const departments = ref([]);
const currentUser = ref(frappe.session?.user || '');
const isSystemManager = ref(false);

// Create dashboard state
const selectedForm = ref('');
const chartConfig = ref({
  statusChart: false,
  departmentChart: false,
  trendChart: false,
  requestorsTable: false,
  submissionsTable: false
});
const dashboardName = ref('');
const saving = ref(false);

// View dashboard state
const currentDashboard = ref(null);
const insightsData = ref(null);
const loading = ref(false);
const viewFilters = ref({
  department: '',
  dateRange: 'last90days',
  dateFrom: '',
  dateTo: ''
});

// Export and delete
const showExportMenu = ref(false);
const showDeleteModal = ref(false);
const dashboardToDelete = ref(null);

// Chart refs
const statusChart = ref(null);
const departmentChart = ref(null);
const trendChart = ref(null);
let statusChartInstance = null;
let departmentChartInstance = null;
let trendChartInstance = null;

// Available chart types
const availableCharts = [
  { id: 'statusChart', name: 'Status Distribution', description: 'Pie chart showing form statuses', icon: 'pi pi-chart-pie' },
  { id: 'departmentChart', name: 'Department Breakdown', description: 'Bar chart by departments', icon: 'pi pi-chart-bar' },
  { id: 'trendChart', name: 'Monthly Trends', description: 'Line chart showing trends over time', icon: 'pi pi-chart-line' },
  { id: 'requestorsTable', name: 'Top Requestors', description: 'Table of top form requestors', icon: 'pi pi-users' },
  { id: 'submissionsTable', name: 'Submissions List', description: 'Detailed submissions table', icon: 'pi pi-list' }
];

// Computed
const hasSelectedCharts = computed(() => {
  return Object.values(chartConfig.value).some(v => v === true);
});

// Methods
async function loadSavedDashboards() {
  try {
    const response = await axiosInstance.get(apis.getSavedDashboards);
    if (response.data?.message?.success) {
      savedDashboards.value = response.data.message.data;
    }
  } catch (error) {
    console.error('Error loading dashboards:', error);
  }
}

async function loadAvailableForms() {
  try {
    const response = await axiosInstance.get(apis.getAvailableForms);
    if (response.data?.message?.success) {
      availableForms.value = response.data.message.data;
    }
  } catch (error) {
    console.error('Error loading forms:', error);
  }
}

async function loadDepartments() {
  try {
    const queryParams = {
      fields: JSON.stringify(['name', 'department_name']),
      limit_page_length: 'none'
    };
    const response = await axiosInstance.get(`${apis.resource}${doctypes.departments}`, { params: queryParams });
    if (response.data?.data) {
      departments.value = response.data.data;
    }
  } catch (error) {
    console.error('Error loading departments:', error);
  }
}

function startCreateDashboard() {
  viewMode.value = 'create';
  createStep.value = 1;
  selectedForm.value = '';
  chartConfig.value = {
    statusChart: false,
    departmentChart: false,
    trendChart: false,
    requestorsTable: false,
    submissionsTable: false
  };
  dashboardName.value = '';
}

function cancelCreate() {
  viewMode.value = 'list';
  createStep.value = 1;
}

function selectForm(formName) {
  selectedForm.value = formName;
}

function toggleChart(chartId) {
  chartConfig.value[chartId] = !chartConfig.value[chartId];
}

function nextStep() {
  createStep.value++;
}

function prevStep() {
  createStep.value--;
}

function getSelectedChartNames() {
  return availableCharts
    .filter(chart => chartConfig.value[chart.id])
    .map(chart => chart.name);
}

async function saveDashboard() {
  if (!dashboardName.value.trim()) return;

  saving.value = true;
  try {
    const response = await axiosInstance.post(apis.saveDashboard, {
      dashboard_name: dashboardName.value,
      form_name: selectedForm.value,
      chart_config: JSON.stringify(chartConfig.value),
      filters: JSON.stringify(viewFilters.value)
    });

    if (response.data?.message?.success) {
      alert('Dashboard saved successfully!');
      await loadSavedDashboards();
      viewMode.value = 'list';
      createStep.value = 1;
    } else {
      alert('Failed to save dashboard: ' + (response.data?.message?.message || 'Unknown error'));
    }
  } catch (error) {
    console.error('Error saving dashboard:', error);
    alert('Error saving dashboard');
  } finally {
    saving.value = false;
  }
}

async function viewDashboard(dashboard) {
  currentDashboard.value = dashboard;
  viewMode.value = 'view';
  selectedForm.value = dashboard.form_name;
  await loadDashboardData();
}

async function loadDashboardData() {
  if (!selectedForm.value) return;

  loading.value = true;
  try {
    const params = {
      form_name: selectedForm.value,
      department: viewFilters.value.department || null,
      date_from: viewFilters.value.dateFrom || null,
      date_to: viewFilters.value.dateTo || null
    };

    const response = await axiosInstance.get(apis.getFormInsights, { params });
    if (response.data?.message?.success) {
      insightsData.value = response.data.message.data;
      await nextTick();
      renderCharts();
    }
  } catch (error) {
    console.error('Error loading dashboard data:', error);
  } finally {
    loading.value = false;
  }
}

function onDateRangeChange() {
  const today = new Date();
  const ranges = {
    'last30days': 30,
    'last90days': 90,
    'last6months': 180,
    'lastyear': 365
  };

  const days = ranges[viewFilters.value.dateRange];
  viewFilters.value.dateTo = today.toISOString().split('T')[0];
  const fromDate = new Date(today);
  fromDate.setDate(fromDate.getDate() - days);
  viewFilters.value.dateFrom = fromDate.toISOString().split('T')[0];
  loadDashboardData();
}

function backToList() {
  viewMode.value = 'list';
  currentDashboard.value = null;
  insightsData.value = null;
}

function confirmDeleteDashboard(dashboard) {
  dashboardToDelete.value = dashboard;
  showDeleteModal.value = true;
}

async function deleteDashboard() {
  if (!dashboardToDelete.value) return;

  try {
    const response = await axiosInstance.post(apis.deleteDashboard, {
      dashboard_name: dashboardToDelete.value.dashboard_name
    });

    if (response.data?.message?.success) {
      alert('Dashboard deleted successfully');
      await loadSavedDashboards();
    } else {
      alert('Failed to delete: ' + (response.data?.message?.message || 'Unknown error'));
    }
  } catch (error) {
    console.error('Error deleting dashboard:', error);
    alert('Error deleting dashboard');
  } finally {
    showDeleteModal.value = false;
    dashboardToDelete.value = null;
  }
}

function getChartCount(config) {
  if (!config) return 0;
  return Object.values(config).filter(v => v === true).length;
}

// Chart rendering
function renderCharts() {
  if (currentDashboard.value?.chart_config?.statusChart) renderStatusChart();
  if (currentDashboard.value?.chart_config?.departmentChart) renderDepartmentChart();
  if (currentDashboard.value?.chart_config?.trendChart) renderTrendChart();
}

function renderStatusChart() {
  if (!statusChart.value || !insightsData.value) return;
  if (statusChartInstance) statusChartInstance.dispose();
  statusChartInstance = echarts.init(statusChart.value);

  const statusData = insightsData.value.status_breakdown.map(item => ({
    name: item.status,
    value: item.count
  }));

  statusChartInstance.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
    legend: { orient: 'vertical', left: 'left', top: 'center' },
    series: [{
      name: 'Status',
      type: 'pie',
      radius: ['40%', '70%'],
      data: statusData,
      color: ['#10b981', '#f59e0b', '#3b82f6', '#ef4444', '#6b7280']
    }]
  });
}

function renderDepartmentChart() {
  if (!departmentChart.value || !insightsData.value) return;
  if (departmentChartInstance) departmentChartInstance.dispose();
  departmentChartInstance = echarts.init(departmentChart.value);

  const deptData = insightsData.value.department_breakdown;

  departmentChartInstance.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'value' },
    yAxis: { type: 'category', data: deptData.map(d => d.department) },
    series: [{
      name: 'Submissions',
      type: 'bar',
      data: deptData.map(d => d.count),
      itemStyle: { color: '#3b82f6' }
    }]
  });
}

function renderTrendChart() {
  if (!trendChart.value || !insightsData.value) return;
  if (trendChartInstance) trendChartInstance.dispose();
  trendChartInstance = echarts.init(trendChart.value);

  const trendData = insightsData.value.monthly_trends;

  trendChartInstance.setOption({
    tooltip: { trigger: 'axis' },
    legend: { data: ['Total', 'Completed', 'Pending'] },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: trendData.map(t => t.month) },
    yAxis: { type: 'value' },
    series: [
      { name: 'Total', type: 'line', data: trendData.map(t => t.total), smooth: true, itemStyle: { color: '#3b82f6' } },
      { name: 'Completed', type: 'line', data: trendData.map(t => t.completed), smooth: true, itemStyle: { color: '#10b981' } },
      { name: 'Pending', type: 'line', data: trendData.map(t => t.pending), smooth: true, itemStyle: { color: '#f59e0b' } }
    ]
  });
}

// Helper functions
function getTotalSubmissions() {
  if (!insightsData.value?.status_breakdown) return 0;
  return insightsData.value.status_breakdown.reduce((sum, item) => sum + item.count, 0);
}

function getStatusCount(status) {
  if (!insightsData.value?.status_breakdown) return 0;
  const item = insightsData.value.status_breakdown.find(i => i.status === status);
  return item ? item.count : 0;
}

function getStatusPercentage(status) {
  const total = getTotalSubmissions();
  if (total === 0) return 0;
  return ((getStatusCount(status) / total) * 100).toFixed(1);
}

function getAvgProcessingTime() {
  if (!insightsData.value?.processing_time) return '0';
  return Math.round(insightsData.value.processing_time.avg_hours || 0);
}

function formatDate(dateString) {
  if (!dateString) return 'N/A';
  return new Date(dateString).toLocaleString('en-US', {
    year: 'numeric', month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
  });
}

function getStatusClass(status) {
  const classes = {
    'Completed': 'status-completed',
    'Pending': 'status-pending',
    'In Progress': 'status-progress',
    'Request Cancelled': 'status-cancelled'
  };
  return classes[status] || 'status-other';
}

function getCompletionClass(requestor) {
  const rate = (requestor.completed / requestor.total_requests) * 100;
  if (rate >= 80) return 'completion-high';
  if (rate >= 50) return 'completion-medium';
  return 'completion-low';
}

function toggleExportMenu() {
  showExportMenu.value = !showExportMenu.value;
}

async function exportData(format) {
  try {
    const params = {
      form_name: selectedForm.value,
      department: viewFilters.value.department || null,
      date_from: viewFilters.value.dateFrom || null,
      date_to: viewFilters.value.dateTo || null,
      export_format: format
    };

    const response = await axiosInstance.get(apis.exportFormInsights, { params });
    if (response.data?.message?.success) {
      const data = response.data.message.data;
      const blob = new Blob([data.content], { type: 'text/csv' });
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = data.filename;
      a.click();
      window.URL.revokeObjectURL(url);
    }
  } catch (error) {
    console.error('Error exporting:', error);
  } finally {
    showExportMenu.value = false;
  }
}

// Lifecycle
onMounted(async () => {
  await loadSavedDashboards();
  await loadAvailableForms();
  await loadDepartments();

  // Check if user is System Manager
  const roles = frappe.session?.roles || [];
  isSystemManager.value = roles.includes('System Manager');
});
</script>

<style scoped>
.insights-container {
  width: 100%;
  min-height: 100vh;
  background: #f8fafc;
  padding: 24px;
}

/* Header */
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.header-left {
  flex: 1;
}

.header-center {
  flex: 1;
  text-align: center;
}

.page-title {
  font-size: 1.75rem;
  font-weight: 700;
  color: #1f2937;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 12px;
}

.page-title i {
  color: #3b82f6;
}

.page-subtitle {
  margin: 4px 0 0 0;
  color: #6b7280;
  font-size: 0.95rem;
}

/* Buttons */
.create-btn, .save-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}

.create-btn:hover, .save-btn:hover {
  transform: translateY(-1px);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.4);
}

.back-btn, .back-btn-secondary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  background: white;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  color: #374151;
  transition: all 0.2s;
}

.back-btn:hover, .back-btn-secondary:hover {
  border-color: #3b82f6;
  color: #3b82f6;
}

.next-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}

.next-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

/* Dashboard Grid */
.dashboards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.dashboard-card {
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  padding: 20px;
  cursor: pointer;
  transition: all 0.2s;
}

.dashboard-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0,0,0,0.15);
}

.dashboard-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.dashboard-card-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #1f2937;
}

.delete-icon-btn {
  background: none;
  border: none;
  color: #ef4444;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background 0.2s;
}

.delete-icon-btn:hover {
  background: #fee2e2;
}

.dashboard-card-body p {
  margin: 8px 0;
  color: #6b7280;
  display: flex;
  align-items: center;
  gap: 8px;
}

.dashboard-card-footer {
  margin-top: 16px;
  padding-top: 16px;
  border-top: 1px solid #e5e7eb;
}

.view-btn {
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 8px;
  background: #f3f4f6;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  color: #3b82f6;
  transition: all 0.2s;
}

.view-btn:hover {
  background: #e5e7eb;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.empty-icon {
  font-size: 4rem;
  color: #d1d5db;
  margin-bottom: 20px;
}

/* Step Card */
.step-card {
  background: white;
  padding: 30px;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  margin-bottom: 20px;
}

.step-title {
  font-size: 1.5rem;
  color: #1f2937;
  margin-bottom: 8px;
}

.step-subtitle {
  color: #6b7280;
  margin-bottom: 24px;
}

.step-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 24px;
}

/* Form Grid */
.form-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.form-option-card {
  padding: 20px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  text-align: center;
  cursor: pointer;
  transition: all 0.2s;
}

.form-option-card:hover {
  border-color: #3b82f6;
  background: #f9fafb;
}

.form-option-card.selected {
  border-color: #3b82f6;
  background: #eff6ff;
}

.form-option-card i {
  font-size: 2rem;
  color: #3b82f6;
  margin-bottom: 12px;
}

.form-option-card h4 {
  margin: 8px 0;
  color: #1f2937;
}

.form-option-card p {
  margin: 0;
  color: #6b7280;
  font-size: 0.9rem;
}

/* Chart Options */
.chart-options-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}

.chart-option-card {
  position: relative;
  padding: 24px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
}

.chart-option-card:hover {
  border-color: #3b82f6;
  background: #f9fafb;
}

.chart-option-card.selected {
  border-color: #3b82f6;
  background: #eff6ff;
}

.chart-icon {
  width: 50px;
  height: 50px;
  border-radius: 10px;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 12px;
}

.chart-icon i {
  font-size: 1.5rem;
  color: white;
}

.chart-option-card h4 {
  margin: 8px 0;
  color: #1f2937;
}

.chart-option-card p {
  margin: 0;
  color: #6b7280;
  font-size: 0.85rem;
}

.checkbox-indicator {
  position: absolute;
  top: 12px;
  right: 12px;
  font-size: 1.5rem;
  color: #3b82f6;
}

/* Name Input */
.name-input-section {
  max-width: 600px;
}

.name-input-section label {
  display: block;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
}

.dashboard-name-input {
  width: 100%;
  padding: 12px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.2s;
}

.dashboard-name-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.summary-section {
  margin-top: 24px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
}

.summary-section h4 {
  margin: 0 0 12px 0;
  color: #1f2937;
}

.summary-section p {
  margin: 8px 0;
  color: #6b7280;
}

/* Filters */
.filters-section {
  display: flex;
  gap: 16px;
  margin-bottom: 24px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.filter-group {
  flex: 1;
}

.filter-group label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-weight: 600;
  color: #374151;
  margin-bottom: 8px;
  font-size: 0.9rem;
}

.form-select {
  width: 100%;
  padding: 10px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.95rem;
}

/* Loading */
.loading-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
}

.spinner {
  width: 50px;
  height: 50px;
  margin: 0 auto 20px;
  border: 4px solid #e5e7eb;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Dashboard Content */
.dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.summary-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  display: flex;
  align-items: center;
  gap: 16px;
}

.card-icon {
  width: 60px;
  height: 60px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  color: white;
}

.card-blue .card-icon { background: linear-gradient(135deg, #3b82f6, #2563eb); }
.card-green .card-icon { background: linear-gradient(135deg, #10b981, #059669); }
.card-yellow .card-icon { background: linear-gradient(135deg, #f59e0b, #d97706); }
.card-purple .card-icon { background: linear-gradient(135deg, #8b5cf6, #7c3aed); }

.card-content h4 {
  margin: 0;
  font-size: 0.85rem;
  color: #6b7280;
  font-weight: 600;
  text-transform: uppercase;
}

.card-value {
  margin: 8px 0 0 0;
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
}

.card-percentage {
  display: inline-block;
  margin-top: 4px;
  padding: 4px 8px;
  background: #f3f4f6;
  border-radius: 6px;
  font-size: 0.75rem;
  font-weight: 600;
}

.card-subtitle {
  display: block;
  margin-top: 4px;
  font-size: 0.85rem;
  color: #6b7280;
}

/* Charts */
.charts-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.chart-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.chart-wide {
  grid-column: 1 / -1;
}

.chart-header h3 {
  margin: 0 0 16px 0;
  font-size: 1.25rem;
  color: #1f2937;
}

.chart-content {
  width: 100%;
  height: 350px;
}

/* Tables */
.table-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  grid-column: 1 / -1;
}

.table-header h3 {
  margin: 0 0 16px 0;
  font-size: 1.25rem;
  color: #1f2937;
  display: flex;
  align-items: center;
  gap: 10px;
}

.table-responsive {
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 0.9rem;
}

.data-table thead {
  background: #f9fafb;
}

.data-table th {
  padding: 12px 16px;
  text-align: left;
  font-weight: 600;
  color: #374151;
  border-bottom: 2px solid #e5e7eb;
}

.data-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #f3f4f6;
  color: #6b7280;
}

.data-table tbody tr:hover {
  background: #f9fafb;
}

/* Badges */
.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.status-completed { background: #d1fae5; color: #065f46; }
.status-pending { background: #fef3c7; color: #92400e; }
.status-progress { background: #dbeafe; color: #1e40af; }
.status-cancelled { background: #fee2e2; color: #991b1b; }
.status-other { background: #f3f4f6; color: #374151; }

.completion-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.completion-high { background: #d1fae5; color: #065f46; }
.completion-medium { background: #fef3c7; color: #92400e; }
.completion-low { background: #fee2e2; color: #991b1b; }

/* Export Menu */
.export-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #10b981, #059669);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
}

.export-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  min-width: 180px;
  z-index: 100;
}

.export-option {
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  color: #374151;
  font-weight: 500;
  transition: background 0.2s;
}

.export-option:hover {
  background: #f3f4f6;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: white;
  padding: 30px;
  border-radius: 12px;
  max-width: 400px;
  width: 90%;
}

.modal-content h3 {
  margin: 0 0 16px 0;
  color: #1f2937;
}

.modal-content p {
  margin: 0 0 24px 0;
  color: #6b7280;
}

.modal-actions {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
}

.cancel-btn {
  padding: 8px 16px;
  background: #f3f4f6;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  color: #374151;
}

.confirm-delete-btn {
  padding: 8px 16px;
  background: #ef4444;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  color: white;
}

/* Responsive */
@media (max-width: 768px) {
  .page-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .dashboards-grid {
    grid-template-columns: 1fr;
  }

  .form-grid, .chart-options-grid {
    grid-template-columns: 1fr;
  }

  .charts-container {
    grid-template-columns: 1fr;
  }

  .filters-section {
    flex-direction: column;
  }
}
</style>
