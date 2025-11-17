<template>
  <div class="new-dashboard-container">
    <!-- Header -->
    <div class="dashboard-header">
      <h1>Insights Dashboard</h1>
      <p class="subtitle">Comprehensive analytics and insights for your forms</p>
    </div>

    <!-- Filters Section -->
    <div class="filters-section card">
      <h3>Filters</h3>
      <div class="filters-grid">
        <!-- Date Range Filter -->
        <div class="filter-item">
          <label>Date Range</label>
          <div class="date-range-buttons">
            <button
              v-for="range in dateRanges"
              :key="range.value"
              :class="['range-btn', { active: selectedDateRange === range.value }]"
              @click="selectDateRange(range.value)"
            >
              {{ range.label }}
            </button>
          </div>
        </div>

        <!-- Custom Date Range -->
        <div v-if="selectedDateRange === 'custom'" class="filter-item custom-dates">
          <div class="date-input">
            <label>From Date</label>
            <input type="date" v-model="customDateFrom" @change="applyFilters" />
          </div>
          <div class="date-input">
            <label>To Date</label>
            <input type="date" v-model="customDateTo" @change="applyFilters" />
          </div>
        </div>

        <!-- Department Filter -->
        <div class="filter-item">
          <label>Department</label>
          <select v-model="selectedDepartment" @change="applyFilters">
            <option value="">All Departments</option>
            <option
              v-for="dept in availableDepartments"
              :key="dept.name"
              :value="dept.name"
            >
              {{ dept.department_name }}
            </option>
          </select>
        </div>

        <!-- Form Type Filter -->
        <div class="filter-item">
          <label>Form Type</label>
          <select v-model="selectedFormType" @change="applyFilters">
            <option value="">All Forms</option>
            <option
              v-for="form in availableFormTypes"
              :key="form.form_type"
              :value="form.form_type"
            >
              {{ form.form_type }}
            </option>
          </select>
        </div>

        <!-- Business Unit Filter -->
        <div class="filter-item" v-if="availableBusinessUnits.length > 0">
          <label>Business Unit</label>
          <select v-model="selectedProperty" @change="applyFilters">
            <option value="">All Business Units</option>
            <option
              v-for="unit in availableBusinessUnits"
              :key="unit.name"
              :value="unit.name"
            >
              {{ unit.label }}
            </option>
          </select>
        </div>

        <!-- Period Filter (for trends) -->
        <div class="filter-item">
          <label>Trend Period</label>
          <select v-model="selectedPeriod" @change="applyFilters">
            <option value="daily">Daily</option>
            <option value="weekly">Weekly</option>
            <option value="monthly">Monthly</option>
          </select>
        </div>

        <!-- Apply/Reset Buttons -->
        <div class="filter-actions">
          <button class="btn-primary" @click="applyFilters" :disabled="loading">
            <span v-if="loading">Loading...</span>
            <span v-else>Apply Filters</span>
          </button>
          <button class="btn-secondary" @click="resetFilters">Reset</button>
        </div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="loading-container">
      <div class="spinner"></div>
      <p>Loading dashboard data...</p>
    </div>

    <!-- Dashboard Content -->
    <div v-else class="dashboard-content">
      <!-- Form Status Overview -->
      <div class="insight-section">
        <h2>Form Status Overview</h2>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon completed">
              <i class="pi pi-check-circle"></i>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ statusOverview.Completed || 0 }}</span>
              <span class="stat-label">Completed</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon pending">
              <i class="pi pi-clock"></i>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ statusOverview.Pending || 0 }}</span>
              <span class="stat-label">Pending</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon in-progress">
              <i class="pi pi-spin pi-spinner"></i>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ statusOverview['In Progress'] || 0 }}</span>
              <span class="stat-label">In Progress</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon cancelled">
              <i class="pi pi-times-circle"></i>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ statusOverview.Cancelled || 0 }}</span>
              <span class="stat-label">Cancelled</span>
            </div>
          </div>
          <div class="stat-card total">
            <div class="stat-icon">
              <i class="pi pi-chart-bar"></i>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ statusOverview.Total || 0 }}</span>
              <span class="stat-label">Total Forms</span>
            </div>
          </div>
        </div>

        <!-- Status Chart -->
        <div class="chart-container">
          <div ref="statusChart" style="width: 100%; height: 400px"></div>
        </div>
      </div>

      <!-- Department-Wise Analysis -->
      <div class="insight-section">
        <h2>Department-Wise Form Analysis</h2>
        <div class="chart-container">
          <div ref="departmentChart" style="width: 100%; height: 400px"></div>
        </div>

        <!-- Department Table -->
        <div class="data-table">
          <table>
            <thead>
              <tr>
                <th>Department</th>
                <th>Total Forms</th>
                <th>Completed</th>
                <th>Pending</th>
                <th>In Progress</th>
                <th>Top Form Types</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="dept in departmentAnalysis" :key="dept.department">
                <td>{{ dept.department }}</td>
                <td>{{ dept.total_forms }}</td>
                <td class="completed">{{ dept.completed }}</td>
                <td class="pending">{{ dept.pending }}</td>
                <td class="in-progress">{{ dept.in_progress }}</td>
                <td>
                  <span
                    v-for="(type, index) in dept.form_types.slice(0, 3)"
                    :key="index"
                    class="form-type-badge"
                  >
                    {{ type.form_type }} ({{ type.count }})
                  </span>
                </td>
              </tr>
              <tr v-if="departmentAnalysis.length === 0">
                <td colspan="6" class="no-data">No data available</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Form Value/Amount Tracking -->
      <div class="insight-section" v-if="valueTracking.forms_with_amount > 0">
        <h2>Form Value/Amount Tracking</h2>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-icon amount">
              <i class="pi pi-dollar"></i>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ formatCurrency(valueTracking.total_amount) }}</span>
              <span class="stat-label">Total Amount</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <i class="pi pi-file"></i>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ valueTracking.forms_with_amount }}</span>
              <span class="stat-label">Forms with Amount</span>
            </div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <i class="pi pi-calculator"></i>
            </div>
            <div class="stat-info">
              <span class="stat-value">{{ formatCurrency(valueTracking.average_amount) }}</span>
              <span class="stat-label">Average Amount</span>
            </div>
          </div>
        </div>

        <!-- Amount Details Table -->
        <div class="data-table" v-if="valueTracking.form_details && valueTracking.form_details.length > 0">
          <h3>Recent Forms with Amounts</h3>
          <table>
            <thead>
              <tr>
                <th>Request ID</th>
                <th>Form Type</th>
                <th>Department</th>
                <th>Amount</th>
                <th>Status</th>
                <th>Date</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="form in valueTracking.form_details.slice(0, 20)" :key="form.request_id">
                <td>{{ form.request_id }}</td>
                <td>{{ form.form_type }}</td>
                <td>{{ form.department || 'N/A' }}</td>
                <td class="amount">{{ formatCurrency(form.amount) }}</td>
                <td>
                  <span :class="['status-badge', getStatusClass(form.status)]">
                    {{ form.status }}
                  </span>
                </td>
                <td>{{ formatDate(form.date) }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Recurring Form Trends -->
      <div class="insight-section">
        <h2>Recurring Form Trends</h2>

        <!-- Most Frequent Forms -->
        <div class="frequent-forms">
          <h3>Most Frequently Raised Forms</h3>
          <div class="data-table">
            <table>
              <thead>
                <tr>
                  <th>Form Type</th>
                  <th>Total Count</th>
                  <th>Days Raised</th>
                  <th>Average per Day</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="form in recurringTrends.most_frequent" :key="form.form_type">
                  <td>{{ form.form_type }}</td>
                  <td>{{ form.total_count }}</td>
                  <td>{{ form.days_raised }}</td>
                  <td>{{ form.avg_per_day }}</td>
                </tr>
                <tr v-if="recurringTrends.most_frequent.length === 0">
                  <td colspan="4" class="no-data">No data available</td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Trend Chart -->
        <div class="chart-container">
          <div ref="trendChart" style="width: 100%; height: 400px"></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, watch } from 'vue';
import * as echarts from 'echarts';
import axiosInstance from '../../shared/services/interceptor';
import { apiurls } from '../../shared/apiurls';

export default {
  name: 'NewDashboard',
  setup() {
    // Refs
    const loading = ref(false);
    const statusOverview = ref({});
    const departmentAnalysis = ref([]);
    const valueTracking = ref({});
    const recurringTrends = ref({ most_frequent: [], trends: [] });
    const availableDepartments = ref([]);
    const availableFormTypes = ref([]);
    const availableBusinessUnits = ref([]);

    // Filter states
    const selectedDateRange = ref('last30days');
    const customDateFrom = ref('');
    const customDateTo = ref('');
    const selectedDepartment = ref('');
    const selectedFormType = ref('');
    const selectedProperty = ref('');
    const selectedPeriod = ref('weekly');

    // Chart refs
    const statusChart = ref(null);
    const departmentChart = ref(null);
    const trendChart = ref(null);

    // Date range options
    const dateRanges = [
      { label: 'Today', value: 'today' },
      { label: 'Last 7 Days', value: 'last7days' },
      { label: 'Last 30 Days', value: 'last30days' },
      { label: 'This Month', value: 'thismonth' },
      { label: 'Last Month', value: 'lastmonth' },
      { label: 'Custom', value: 'custom' }
    ];

    // Methods
    const getDateRange = () => {
      const today = new Date();
      let dateFrom, dateTo;

      switch (selectedDateRange.value) {
        case 'today':
          dateFrom = dateTo = today.toISOString().split('T')[0];
          break;
        case 'last7days':
          dateFrom = new Date(today.setDate(today.getDate() - 7)).toISOString().split('T')[0];
          dateTo = new Date().toISOString().split('T')[0];
          break;
        case 'last30days':
          dateFrom = new Date(today.setDate(today.getDate() - 30)).toISOString().split('T')[0];
          dateTo = new Date().toISOString().split('T')[0];
          break;
        case 'thismonth':
          dateFrom = new Date(today.getFullYear(), today.getMonth(), 1).toISOString().split('T')[0];
          dateTo = new Date().toISOString().split('T')[0];
          break;
        case 'lastmonth':
          const lastMonth = new Date(today.getFullYear(), today.getMonth() - 1, 1);
          dateFrom = lastMonth.toISOString().split('T')[0];
          dateTo = new Date(today.getFullYear(), today.getMonth(), 0).toISOString().split('T')[0];
          break;
        case 'custom':
          dateFrom = customDateFrom.value;
          dateTo = customDateTo.value;
          break;
        default:
          dateFrom = new Date(today.setDate(today.getDate() - 30)).toISOString().split('T')[0];
          dateTo = new Date().toISOString().split('T')[0];
      }

      return { dateFrom, dateTo };
    };

    const selectDateRange = (range) => {
      selectedDateRange.value = range;
      if (range !== 'custom') {
        applyFilters();
      }
    };

    const loadDashboardData = async () => {
      loading.value = true;
      try {
        const { dateFrom, dateTo } = getDateRange();

        const params = {
          property: selectedProperty.value || null,
          date_from: dateFrom,
          date_to: dateTo,
          department: selectedDepartment.value || null,
          form_type: selectedFormType.value || null,
          period: selectedPeriod.value
        };

        // Call consolidated API using Axios instance
        const response = await axiosInstance.get(
          '/api/method/ezy_forms.api.v1.new_dashboard.get_consolidated_dashboard',
          { params }
        );

        if (response.message && response.message.success) {
          const data = response.message.data;
          statusOverview.value = data.status_overview || {};
          departmentAnalysis.value = data.department_analysis || [];
          valueTracking.value = data.value_tracking || {};
          recurringTrends.value = data.recurring_trends || { most_frequent: [], trends: [] };

          // Load filters
          if (data.filters) {
            availableDepartments.value = data.filters.departments || [];
            availableFormTypes.value = data.filters.form_types || [];
            availableBusinessUnits.value = data.filters.business_units || [];
          }

          // Render charts
          setTimeout(() => {
            renderStatusChart();
            renderDepartmentChart();
            renderTrendChart();
          }, 100);
        }
      } catch (error) {
        console.error('Error loading dashboard data:', error);
      } finally {
        loading.value = false;
      }
    };

    const applyFilters = () => {
      loadDashboardData();
    };

    const resetFilters = () => {
      selectedDateRange.value = 'last30days';
      customDateFrom.value = '';
      customDateTo.value = '';
      selectedDepartment.value = '';
      selectedFormType.value = '';
      selectedProperty.value = '';
      selectedPeriod.value = 'weekly';
      applyFilters();
    };

    const renderStatusChart = () => {
      if (!statusChart.value) return;

      const chart = echarts.init(statusChart.value);
      const option = {
        title: {
          text: 'Form Status Distribution',
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          top: 'middle'
        },
        series: [
          {
            name: 'Status',
            type: 'pie',
            radius: '60%',
            data: [
              { value: statusOverview.value.Completed || 0, name: 'Completed', itemStyle: { color: '#10b981' } },
              { value: statusOverview.value.Pending || 0, name: 'Pending', itemStyle: { color: '#f59e0b' } },
              { value: statusOverview.value['In Progress'] || 0, name: 'In Progress', itemStyle: { color: '#3b82f6' } },
              { value: statusOverview.value.Cancelled || 0, name: 'Cancelled', itemStyle: { color: '#ef4444' } }
            ],
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            }
          }
        ]
      };

      chart.setOption(option);
    };

    const renderDepartmentChart = () => {
      if (!departmentChart.value) return;

      const chart = echarts.init(departmentChart.value);
      const departments = departmentAnalysis.value.map(d => d.department);
      const totals = departmentAnalysis.value.map(d => d.total_forms);
      const completed = departmentAnalysis.value.map(d => d.completed);
      const pending = departmentAnalysis.value.map(d => d.pending);
      const inProgress = departmentAnalysis.value.map(d => d.in_progress);

      const option = {
        title: {
          text: 'Forms by Department',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        legend: {
          data: ['Completed', 'Pending', 'In Progress'],
          top: 'bottom'
        },
        xAxis: {
          type: 'category',
          data: departments,
          axisLabel: {
            rotate: 45,
            interval: 0
          }
        },
        yAxis: {
          type: 'value'
        },
        series: [
          {
            name: 'Completed',
            type: 'bar',
            stack: 'total',
            data: completed,
            itemStyle: { color: '#10b981' }
          },
          {
            name: 'Pending',
            type: 'bar',
            stack: 'total',
            data: pending,
            itemStyle: { color: '#f59e0b' }
          },
          {
            name: 'In Progress',
            type: 'bar',
            stack: 'total',
            data: inProgress,
            itemStyle: { color: '#3b82f6' }
          }
        ]
      };

      chart.setOption(option);
    };

    const renderTrendChart = () => {
      if (!trendChart.value) return;

      const chart = echarts.init(trendChart.value);

      // Group trends by form type
      const trendsByType = {};
      recurringTrends.value.trends.forEach(trend => {
        if (!trendsByType[trend.form_type]) {
          trendsByType[trend.form_type] = [];
        }
        trendsByType[trend.form_type].push({
          period: trend.period,
          count: trend.count
        });
      });

      // Get all unique periods
      const periods = [...new Set(recurringTrends.value.trends.map(t => t.period))].sort();

      // Create series for each form type
      const series = Object.keys(trendsByType).slice(0, 5).map(formType => ({
        name: formType,
        type: 'line',
        data: periods.map(period => {
          const trend = trendsByType[formType].find(t => t.period === period);
          return trend ? trend.count : 0;
        })
      }));

      const option = {
        title: {
          text: 'Form Trends Over Time',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: Object.keys(trendsByType).slice(0, 5),
          top: 'bottom'
        },
        xAxis: {
          type: 'category',
          data: periods,
          axisLabel: {
            rotate: 45,
            interval: 0
          }
        },
        yAxis: {
          type: 'value'
        },
        series: series
      };

      chart.setOption(option);
    };

    const formatCurrency = (value) => {
      return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
      }).format(value || 0);
    };

    const formatDate = (date) => {
      if (!date) return 'N/A';
      return new Date(date).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      });
    };

    const getStatusClass = (status) => {
      const statusMap = {
        'Completed': 'completed',
        'Pending': 'pending',
        'Request Raised': 'pending',
        'Request Raised Via QR Code': 'pending',
        'In Progress': 'in-progress',
        'Request Cancelled': 'cancelled'
      };
      return statusMap[status] || '';
    };

    // Lifecycle
    onMounted(() => {
      loadDashboardData();
    });

    return {
      loading,
      statusOverview,
      departmentAnalysis,
      valueTracking,
      recurringTrends,
      availableDepartments,
      availableFormTypes,
      availableBusinessUnits,
      selectedDateRange,
      customDateFrom,
      customDateTo,
      selectedDepartment,
      selectedFormType,
      selectedProperty,
      selectedPeriod,
      dateRanges,
      statusChart,
      departmentChart,
      trendChart,
      selectDateRange,
      applyFilters,
      resetFilters,
      formatCurrency,
      formatDate,
      getStatusClass
    };
  }
};
</script>

<style scoped>
.new-dashboard-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.dashboard-header {
  margin-bottom: 30px;
}

.dashboard-header h1 {
  font-size: 2rem;
  color: #1f2937;
  margin-bottom: 8px;
}

.subtitle {
  color: #6b7280;
  font-size: 1rem;
}

.card {
  background: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
}

.filters-section h3 {
  margin-bottom: 20px;
  color: #1f2937;
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.filter-item {
  display: flex;
  flex-direction: column;
}

.filter-item label {
  font-weight: 500;
  margin-bottom: 8px;
  color: #374151;
}

.filter-item select,
.filter-item input {
  padding: 8px 12px;
  border: 1px solid #d1d5db;
  border-radius: 6px;
  font-size: 0.95rem;
}

.date-range-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.range-btn {
  padding: 8px 16px;
  border: 1px solid #d1d5db;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.2s;
}

.range-btn:hover {
  background: #f3f4f6;
}

.range-btn.active {
  background: #3b82f6;
  color: white;
  border-color: #3b82f6;
}

.custom-dates {
  grid-column: span 2;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.filter-actions {
  display: flex;
  gap: 10px;
  align-items: flex-end;
}

.btn-primary,
.btn-secondary {
  padding: 10px 20px;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s;
}

.btn-primary {
  background: #3b82f6;
  color: white;
}

.btn-primary:hover:not(:disabled) {
  background: #2563eb;
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.btn-secondary {
  background: #f3f4f6;
  color: #374151;
}

.btn-secondary:hover {
  background: #e5e7eb;
}

.loading-container {
  text-align: center;
  padding: 60px 20px;
}

.spinner {
  width: 40px;
  height: 40px;
  margin: 0 auto 20px;
  border: 4px solid #f3f4f6;
  border-top-color: #3b82f6;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.dashboard-content {
  margin-top: 20px;
}

.insight-section {
  background: white;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
  margin-bottom: 30px;
}

.insight-section h2 {
  font-size: 1.5rem;
  color: #1f2937;
  margin-bottom: 20px;
}

.insight-section h3 {
  font-size: 1.2rem;
  color: #374151;
  margin: 20px 0 15px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 20px;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.stat-card.total {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.stat-icon {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  margin-right: 15px;
  font-size: 1.5rem;
}

.stat-icon.completed {
  background: #d1fae5;
  color: #10b981;
}

.stat-icon.pending {
  background: #fef3c7;
  color: #f59e0b;
}

.stat-icon.in-progress {
  background: #dbeafe;
  color: #3b82f6;
}

.stat-icon.cancelled {
  background: #fee2e2;
  color: #ef4444;
}

.stat-icon.amount {
  background: #e0e7ff;
  color: #6366f1;
}

.stat-card.total .stat-icon {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.stat-info {
  display: flex;
  flex-direction: column;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
  color: #1f2937;
}

.stat-card.total .stat-value {
  color: white;
}

.stat-label {
  font-size: 0.875rem;
  color: #6b7280;
  margin-top: 4px;
}

.stat-card.total .stat-label {
  color: rgba(255, 255, 255, 0.9);
}

.chart-container {
  margin: 30px 0;
}

.data-table {
  margin-top: 20px;
  overflow-x: auto;
}

.data-table table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #e5e7eb;
}

.data-table th {
  background: #f9fafb;
  font-weight: 600;
  color: #374151;
}

.data-table tr:hover {
  background: #f9fafb;
}

.data-table .completed {
  color: #10b981;
  font-weight: 500;
}

.data-table .pending {
  color: #f59e0b;
  font-weight: 500;
}

.data-table .in-progress {
  color: #3b82f6;
  font-weight: 500;
}

.data-table .amount {
  font-weight: 600;
  color: #6366f1;
}

.no-data {
  text-align: center;
  color: #9ca3af;
  padding: 40px !important;
}

.form-type-badge {
  display: inline-block;
  padding: 4px 8px;
  background: #e0e7ff;
  color: #3730a3;
  border-radius: 4px;
  font-size: 0.75rem;
  margin-right: 6px;
  margin-bottom: 4px;
}

.status-badge {
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.875rem;
  font-weight: 500;
}

.status-badge.completed {
  background: #d1fae5;
  color: #065f46;
}

.status-badge.pending {
  background: #fef3c7;
  color: #92400e;
}

.status-badge.in-progress {
  background: #dbeafe;
  color: #1e40af;
}

.status-badge.cancelled {
  background: #fee2e2;
  color: #991b1b;
}

@media (max-width: 768px) {
  .filters-grid {
    grid-template-columns: 1fr;
  }

  .custom-dates {
    grid-column: span 1;
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .dashboard-header h1 {
    font-size: 1.5rem;
  }
}
</style>
