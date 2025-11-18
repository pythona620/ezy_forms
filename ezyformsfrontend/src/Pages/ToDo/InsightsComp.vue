<template>
  <div class="insights-container">
    <!-- Header -->
    <div class="insights-header">
      <div class="header-left">
        <h2 class="page-title">
          <i class="pi pi-chart-bar"></i>
          Form Insights & Analytics
        </h2>
        <p class="page-subtitle">Analyze form submissions with interactive dashboards</p>
      </div>
      <div class="header-right" v-if="selectedForm">
        <button class="export-btn" @click="toggleExportMenu">
          <i class="pi pi-download"></i>
          Export Data
          <i :class="showExportMenu ? 'pi pi-chevron-up' : 'pi pi-chevron-down'"></i>
        </button>
        <div v-if="showExportMenu" class="export-menu">
          <div class="export-option" @click="exportData('csv')">
            <i class="pi pi-file"></i>
            Export as CSV
          </div>
          <div class="export-option" @click="exportData('excel')">
            <i class="pi pi-file-excel"></i>
            Export as Excel
          </div>
        </div>
      </div>
    </div>

    <!-- Form Selection -->
    <div class="form-selection-section">
      <div class="filter-card">
        <div class="filter-row">
          <div class="filter-group">
            <label class="filter-label">
              <i class="pi pi-file"></i>
              Select Form
            </label>
            <select v-model="selectedForm" @change="onFormChange" class="form-select">
              <option value="">-- Choose a Form --</option>
              <option v-for="form in availableForms" :key="form.form_name" :value="form.form_name">
                {{ form.form_name }} ({{ form.total_submissions }} submissions)
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label class="filter-label">
              <i class="pi pi-building"></i>
              Department
            </label>
            <select v-model="filters.department" @change="loadInsights" class="form-select">
              <option value="">All Departments</option>
              <option v-for="dept in departments" :key="dept.name" :value="dept.name">
                {{ dept.department_name }}
              </option>
            </select>
          </div>

          <div class="filter-group">
            <label class="filter-label">
              <i class="pi pi-calendar"></i>
              Date Range
            </label>
            <select v-model="filters.dateRange" @change="onDateRangeChange" class="form-select">
              <option value="last30days">Last 30 Days</option>
              <option value="last90days">Last 90 Days</option>
              <option value="last6months">Last 6 Months</option>
              <option value="lastyear">Last Year</option>
              <option value="custom">Custom Range</option>
            </select>
          </div>

          <div class="filter-group" v-if="filters.dateRange === 'custom'">
            <label class="filter-label">From Date</label>
            <input type="date" v-model="filters.dateFrom" @change="loadInsights" class="form-input">
          </div>

          <div class="filter-group" v-if="filters.dateRange === 'custom'">
            <label class="filter-label">To Date</label>
            <input type="date" v-model="filters.dateTo" @change="loadInsights" class="form-input">
          </div>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
      <p>Loading insights...</p>
    </div>

    <!-- No Form Selected -->
    <div v-else-if="!selectedForm" class="empty-state">
      <i class="pi pi-chart-line empty-icon"></i>
      <h3>Select a Form to View Insights</h3>
      <p>Choose a form from the dropdown above to see detailed analytics and visualizations</p>
    </div>

    <!-- Insights Dashboard -->
    <div v-else-if="insightsData" class="insights-dashboard">
      <!-- Summary Cards -->
      <div class="summary-cards">
        <div class="summary-card card-blue">
          <div class="card-icon">
            <i class="pi pi-file"></i>
          </div>
          <div class="card-content">
            <h4>Total Submissions</h4>
            <p class="card-value">{{ getTotalSubmissions() }}</p>
          </div>
        </div>

        <div class="summary-card card-green">
          <div class="card-icon">
            <i class="pi pi-check-circle"></i>
          </div>
          <div class="card-content">
            <h4>Completed</h4>
            <p class="card-value">{{ getStatusCount('Completed') }}</p>
            <span class="card-percentage">{{ getStatusPercentage('Completed') }}%</span>
          </div>
        </div>

        <div class="summary-card card-yellow">
          <div class="card-icon">
            <i class="pi pi-clock"></i>
          </div>
          <div class="card-content">
            <h4>Pending</h4>
            <p class="card-value">{{ getStatusCount('Pending') }}</p>
            <span class="card-percentage">{{ getStatusPercentage('Pending') }}%</span>
          </div>
        </div>

        <div class="summary-card card-purple">
          <div class="card-icon">
            <i class="pi pi-hourglass"></i>
          </div>
          <div class="card-content">
            <h4>Avg. Processing Time</h4>
            <p class="card-value">{{ getAvgProcessingTime() }}</p>
            <span class="card-subtitle">hours</span>
          </div>
        </div>
      </div>

      <!-- Charts Row 1 -->
      <div class="charts-row">
        <div class="chart-card">
          <div class="chart-header">
            <h3>Status Distribution</h3>
            <span class="chart-subtitle">Overview of submission statuses</span>
          </div>
          <div ref="statusChart" class="chart-container"></div>
        </div>

        <div class="chart-card">
          <div class="chart-header">
            <h3>Department Breakdown</h3>
            <span class="chart-subtitle">Top 10 departments by submissions</span>
          </div>
          <div ref="departmentChart" class="chart-container"></div>
        </div>
      </div>

      <!-- Charts Row 2 -->
      <div class="charts-row">
        <div class="chart-card chart-card-wide">
          <div class="chart-header">
            <h3>Monthly Trends</h3>
            <span class="chart-subtitle">Submission trends over time</span>
          </div>
          <div ref="trendChart" class="chart-container"></div>
        </div>
      </div>

      <!-- Top Requestors Table -->
      <div class="table-card">
        <div class="table-header">
          <h3>
            <i class="pi pi-users"></i>
            Top Requestors
          </h3>
          <span class="table-subtitle">Top 10 users by submission count</span>
        </div>
        <div class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th>#</th>
                <th>Requestor Name</th>
                <th>Email</th>
                <th>Department</th>
                <th>Total Requests</th>
                <th>Completed</th>
                <th>Completion Rate</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(requestor, index) in insightsData.top_requestors" :key="index">
                <td>{{ index + 1 }}</td>
                <td>{{ requestor.requestor_name }}</td>
                <td>{{ requestor.requestor_email }}</td>
                <td>{{ requestor.department || 'N/A' }}</td>
                <td>{{ requestor.total_requests }}</td>
                <td>{{ requestor.completed }}</td>
                <td>
                  <span class="completion-badge" :class="getCompletionClass(requestor)">
                    {{ ((requestor.completed / requestor.total_requests) * 100).toFixed(1) }}%
                  </span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- All Submissions Table -->
      <div class="table-card">
        <div class="table-header">
          <h3>
            <i class="pi pi-list"></i>
            All Submissions
          </h3>
          <span class="table-subtitle">Recent {{ insightsData.submissions.length }} submissions (max 500)</span>
        </div>
        <div class="table-responsive">
          <table class="data-table">
            <thead>
              <tr>
                <th>Request ID</th>
                <th>Submitted On</th>
                <th>Requestor</th>
                <th>Department</th>
                <th>Property</th>
                <th>Status</th>
                <th>Processing Time</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="submission in insightsData.submissions" :key="submission.request_id">
                <td>{{ submission.request_id }}</td>
                <td>{{ formatDate(submission.requested_on) }}</td>
                <td>{{ submission.requestor }}</td>
                <td>{{ submission.department || 'N/A' }}</td>
                <td>{{ submission.property || 'N/A' }}</td>
                <td>
                  <span class="status-badge" :class="getStatusClass(submission.status)">
                    {{ submission.status }}
                  </span>
                </td>
                <td>{{ submission.processing_hours }} hrs</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, watch } from 'vue';
import * as echarts from 'echarts';
import { apis, doctypes } from '../../shared/apiurls';
import axiosInstance from '../../shared/services/interceptor';

// Reactive state
const availableForms = ref([]);
const departments = ref([]);
const selectedForm = ref('');
const loading = ref(false);
const insightsData = ref(null);
const showExportMenu = ref(false);

const filters = ref({
  department: '',
  dateRange: 'last90days',
  dateFrom: '',
  dateTo: ''
});

// Chart refs
const statusChart = ref(null);
const departmentChart = ref(null);
const trendChart = ref(null);

// Chart instances
let statusChartInstance = null;
let departmentChartInstance = null;
let trendChartInstance = null;

// Load available forms
async function loadAvailableForms() {
  try {
    const response = await axiosInstance.get(apis.getAvailableForms);
    if (response.data && response.data.message && response.data.message.success) {
      availableForms.value = response.data.message.data;
    }
  } catch (error) {
    console.error('Error loading forms:', error);
  }
}

// Load departments
async function loadDepartments() {
  try {
    const queryParams = {
      fields: JSON.stringify(['name', 'department_name']),
      limit_page_length: 'none'
    };
    const response = await axiosInstance.get(`${apis.resource}${doctypes.departments}`, { params: queryParams });
    if (response.data && response.data.data) {
      departments.value = response.data.data;
    }
  } catch (error) {
    console.error('Error loading departments:', error);
  }
}

// Load insights for selected form
async function loadInsights() {
  if (!selectedForm.value) return;

  loading.value = true;
  try {
    const params = {
      form_name: selectedForm.value,
      department: filters.value.department || null,
      date_from: filters.value.dateFrom || null,
      date_to: filters.value.dateTo || null
    };

    const response = await axiosInstance.get(apis.getFormInsights, { params });
    if (response.data && response.data.message && response.data.message.success) {
      insightsData.value = response.data.message.data;

      // Render charts after data is loaded
      await nextTick();
      renderCharts();
    }
  } catch (error) {
    console.error('Error loading insights:', error);
  } finally {
    loading.value = false;
  }
}

// Handle form change
function onFormChange() {
  insightsData.value = null;
  if (selectedForm.value) {
    loadInsights();
  }
}

// Handle date range change
function onDateRangeChange() {
  const today = new Date();
  const ranges = {
    'last30days': 30,
    'last90days': 90,
    'last6months': 180,
    'lastyear': 365
  };

  if (filters.value.dateRange !== 'custom') {
    const days = ranges[filters.value.dateRange];
    filters.value.dateTo = today.toISOString().split('T')[0];
    const fromDate = new Date(today);
    fromDate.setDate(fromDate.getDate() - days);
    filters.value.dateFrom = fromDate.toISOString().split('T')[0];
    loadInsights();
  }
}

// Render all charts
function renderCharts() {
  renderStatusChart();
  renderDepartmentChart();
  renderTrendChart();
}

// Render status distribution pie chart
function renderStatusChart() {
  if (!statusChart.value || !insightsData.value) return;

  if (statusChartInstance) {
    statusChartInstance.dispose();
  }

  statusChartInstance = echarts.init(statusChart.value);

  const statusData = insightsData.value.status_breakdown.map(item => ({
    name: item.status,
    value: item.count
  }));

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left',
      top: 'center'
    },
    series: [
      {
        name: 'Status',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}\n{d}%'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 16,
            fontWeight: 'bold'
          }
        },
        data: statusData,
        color: ['#10b981', '#f59e0b', '#3b82f6', '#ef4444', '#6b7280']
      }
    ]
  };

  statusChartInstance.setOption(option);
}

// Render department bar chart
function renderDepartmentChart() {
  if (!departmentChart.value || !insightsData.value) return;

  if (departmentChartInstance) {
    departmentChartInstance.dispose();
  }

  departmentChartInstance = echarts.init(departmentChart.value);

  const deptData = insightsData.value.department_breakdown;
  const departments = deptData.map(d => d.department);
  const counts = deptData.map(d => d.count);

  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'value'
    },
    yAxis: {
      type: 'category',
      data: departments,
      axisLabel: {
        interval: 0,
        rotate: 0,
        overflow: 'truncate',
        width: 100
      }
    },
    series: [
      {
        name: 'Submissions',
        type: 'bar',
        data: counts,
        itemStyle: {
          color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
            { offset: 0, color: '#667eea' },
            { offset: 1, color: '#764ba2' }
          ]),
          borderRadius: [0, 5, 5, 0]
        },
        label: {
          show: true,
          position: 'right',
          formatter: '{c}'
        }
      }
    ]
  };

  departmentChartInstance.setOption(option);
}

// Render monthly trend line chart
function renderTrendChart() {
  if (!trendChart.value || !insightsData.value) return;

  if (trendChartInstance) {
    trendChartInstance.dispose();
  }

  trendChartInstance = echarts.init(trendChart.value);

  const trendData = insightsData.value.monthly_trends;
  const months = trendData.map(t => t.month);
  const totals = trendData.map(t => t.total);
  const completed = trendData.map(t => t.completed);
  const pending = trendData.map(t => t.pending);

  const option = {
    tooltip: {
      trigger: 'axis'
    },
    legend: {
      data: ['Total', 'Completed', 'Pending']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: months
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: 'Total',
        type: 'line',
        smooth: true,
        data: totals,
        areaStyle: {
          opacity: 0.3
        },
        itemStyle: {
          color: '#3b82f6'
        }
      },
      {
        name: 'Completed',
        type: 'line',
        smooth: true,
        data: completed,
        areaStyle: {
          opacity: 0.3
        },
        itemStyle: {
          color: '#10b981'
        }
      },
      {
        name: 'Pending',
        type: 'line',
        smooth: true,
        data: pending,
        areaStyle: {
          opacity: 0.3
        },
        itemStyle: {
          color: '#f59e0b'
        }
      }
    ]
  };

  trendChartInstance.setOption(option);
}

// Helper functions
function getTotalSubmissions() {
  if (!insightsData.value || !insightsData.value.status_breakdown) return 0;
  return insightsData.value.status_breakdown.reduce((sum, item) => sum + item.count, 0);
}

function getStatusCount(status) {
  if (!insightsData.value || !insightsData.value.status_breakdown) return 0;
  const statusItem = insightsData.value.status_breakdown.find(item => item.status === status);
  return statusItem ? statusItem.count : 0;
}

function getStatusPercentage(status) {
  const total = getTotalSubmissions();
  if (total === 0) return 0;
  const count = getStatusCount(status);
  return ((count / total) * 100).toFixed(1);
}

function getAvgProcessingTime() {
  if (!insightsData.value || !insightsData.value.processing_time) return '0';
  return Math.round(insightsData.value.processing_time.avg_hours || 0);
}

function formatDate(dateString) {
  if (!dateString) return 'N/A';
  const date = new Date(dateString);
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
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
      department: filters.value.department || null,
      date_from: filters.value.dateFrom || null,
      date_to: filters.value.dateTo || null,
      export_format: format
    };

    const response = await axiosInstance.get(apis.exportFormInsights, { params });

    if (response.data && response.data.message && response.data.message.success) {
      const data = response.data.message.data;

      if (format === 'csv') {
        // Download CSV
        const blob = new Blob([data.content], { type: 'text/csv' });
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = data.filename;
        a.click();
        window.URL.revokeObjectURL(url);
      } else if (format === 'excel') {
        // For Excel, you would need a library like xlsx
        console.log('Excel export:', data);
        alert('Excel export functionality requires additional library implementation');
      }
    }
  } catch (error) {
    console.error('Error exporting data:', error);
  } finally {
    showExportMenu.value = false;
  }
}

// Handle window resize for charts
function handleResize() {
  if (statusChartInstance) statusChartInstance.resize();
  if (departmentChartInstance) departmentChartInstance.resize();
  if (trendChartInstance) trendChartInstance.resize();
}

// Lifecycle
onMounted(() => {
  loadAvailableForms();
  loadDepartments();
  window.addEventListener('resize', handleResize);
});

// Cleanup
watch(() => selectedForm.value, () => {
  showExportMenu.value = false;
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
.insights-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 24px;
  padding: 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.header-left {
  flex: 1;
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

.header-right {
  position: relative;
}

/* Export Button */
.export-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.2s;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.3);
}

.export-btn:hover {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.4);
  transform: translateY(-1px);
}

.export-menu {
  position: absolute;
  top: 100%;
  right: 0;
  margin-top: 8px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  min-width: 200px;
  z-index: 100;
  overflow: hidden;
}

.export-option {
  padding: 12px 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  cursor: pointer;
  transition: background 0.2s;
  color: #374151;
  font-weight: 500;
}

.export-option:hover {
  background: #f3f4f6;
}

.export-option i {
  color: #3b82f6;
}

/* Filter Section */
.form-selection-section {
  margin-bottom: 24px;
}

.filter-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.filter-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.filter-label {
  font-weight: 600;
  color: #374151;
  font-size: 0.9rem;
  display: flex;
  align-items: center;
  gap: 6px;
}

.filter-label i {
  color: #3b82f6;
  font-size: 0.85rem;
}

.form-select,
.form-input {
  padding: 10px 12px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.95rem;
  transition: all 0.2s;
  background: white;
  color: #374151;
}

.form-select:focus,
.form-input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

/* Loading State */
.loading-state {
  text-align: center;
  padding: 60px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
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

/* Empty State */
.empty-state {
  text-align: center;
  padding: 80px 20px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.empty-icon {
  font-size: 4rem;
  color: #d1d5db;
  margin-bottom: 20px;
}

.empty-state h3 {
  color: #374151;
  margin-bottom: 10px;
}

.empty-state p {
  color: #6b7280;
}

/* Dashboard */
.insights-dashboard {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

/* Summary Cards */
.summary-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 20px;
}

.summary-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  gap: 16px;
  transition: transform 0.2s, box-shadow 0.2s;
}

.summary-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
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

.card-blue .card-icon {
  background: linear-gradient(135deg, #3b82f6, #2563eb);
}

.card-green .card-icon {
  background: linear-gradient(135deg, #10b981, #059669);
}

.card-yellow .card-icon {
  background: linear-gradient(135deg, #f59e0b, #d97706);
}

.card-purple .card-icon {
  background: linear-gradient(135deg, #8b5cf6, #7c3aed);
}

.card-content h4 {
  margin: 0;
  font-size: 0.85rem;
  color: #6b7280;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
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
  color: #374151;
}

.card-subtitle {
  margin-top: 4px;
  font-size: 0.85rem;
  color: #6b7280;
  display: block;
}

/* Charts */
.charts-row {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
  gap: 20px;
}

.chart-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.chart-card-wide {
  grid-column: 1 / -1;
}

.chart-header {
  margin-bottom: 20px;
}

.chart-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #1f2937;
  font-weight: 700;
}

.chart-subtitle {
  color: #6b7280;
  font-size: 0.85rem;
}

.chart-container {
  width: 100%;
  height: 350px;
}

/* Tables */
.table-card {
  background: white;
  padding: 20px;
  border-radius: 12px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.table-header {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.table-header h3 {
  margin: 0;
  font-size: 1.25rem;
  color: #1f2937;
  font-weight: 700;
  display: flex;
  align-items: center;
  gap: 10px;
}

.table-header i {
  color: #3b82f6;
}

.table-subtitle {
  color: #6b7280;
  font-size: 0.85rem;
  margin-left: auto;
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
  white-space: nowrap;
}

.data-table td {
  padding: 12px 16px;
  border-bottom: 1px solid #f3f4f6;
  color: #6b7280;
}

.data-table tbody tr:hover {
  background: #f9fafb;
}

/* Status Badges */
.status-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
  white-space: nowrap;
}

.status-completed {
  background: #d1fae5;
  color: #065f46;
}

.status-pending {
  background: #fef3c7;
  color: #92400e;
}

.status-progress {
  background: #dbeafe;
  color: #1e40af;
}

.status-cancelled {
  background: #fee2e2;
  color: #991b1b;
}

.status-other {
  background: #f3f4f6;
  color: #374151;
}

/* Completion Badges */
.completion-badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.completion-high {
  background: #d1fae5;
  color: #065f46;
}

.completion-medium {
  background: #fef3c7;
  color: #92400e;
}

.completion-low {
  background: #fee2e2;
  color: #991b1b;
}

/* Responsive */
@media (max-width: 768px) {
  .insights-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .page-title {
    font-size: 1.5rem;
  }

  .charts-row {
    grid-template-columns: 1fr;
  }

  .summary-cards {
    grid-template-columns: 1fr;
  }
}
</style>
