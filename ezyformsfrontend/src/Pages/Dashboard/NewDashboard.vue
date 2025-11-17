<template>
  <div class="new-dashboard-container">
    <!-- Header -->
    <div class="dashboard-header">
      <h1>Insights Dashboard</h1>
      <p class="subtitle">Comprehensive analytics and insights for your forms</p>
    </div>

    <!-- Filters Section -->
    <div class="filters-section card">
      <div class="filters-header" @click="toggleFilters">
        <div class="filters-title">
          <i class="pi pi-filter"></i>
          <h3>Filters</h3>
          <span v-if="activeFiltersCount > 0" class="active-count">{{ activeFiltersCount }} active</span>
        </div>
        <i :class="['pi', filtersExpanded ? 'pi-chevron-up' : 'pi-chevron-down']"></i>
      </div>

      <!-- Active Filters Badges -->
      <div v-if="activeFiltersCount > 0 && !filtersExpanded" class="active-filters-preview">
        <span v-if="selectedDateRange !== 'last30days'" class="filter-badge">
          <i class="pi pi-calendar"></i>
          {{ dateRanges.find(r => r.value === selectedDateRange)?.label || 'Custom Date' }}
          <i class="pi pi-times" @click.stop="clearDateRange"></i>
        </span>
        <span v-if="selectedDepartment" class="filter-badge">
          <i class="pi pi-building"></i>
          {{ getDepartmentLabel(selectedDepartment) }}
          <i class="pi pi-times" @click.stop="clearDepartment"></i>
        </span>
        <span v-if="selectedFormType" class="filter-badge">
          <i class="pi pi-file"></i>
          {{ selectedFormType }}
          <i class="pi pi-times" @click.stop="clearFormType"></i>
        </span>
        <span v-if="selectedProperty" class="filter-badge">
          <i class="pi pi-briefcase"></i>
          {{ getBusinessUnitLabel(selectedProperty) }}
          <i class="pi pi-times" @click.stop="clearProperty"></i>
        </span>
        <span v-if="selectedPeriod !== 'weekly'" class="filter-badge">
          <i class="pi pi-chart-line"></i>
          {{ selectedPeriod.charAt(0).toUpperCase() + selectedPeriod.slice(1) }}
          <i class="pi pi-times" @click.stop="clearPeriod"></i>
        </span>
      </div>

      <transition name="filter-expand">
        <div v-show="filtersExpanded" class="filters-content">
          <div class="filters-grid">
            <!-- Date Range Filter -->
            <div class="filter-item">
              <label>
                <i class="pi pi-calendar"></i>
                Date Range
              </label>
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
                <label>
                  <i class="pi pi-calendar-plus"></i>
                  From Date
                </label>
                <input type="date" v-model="customDateFrom" @change="applyFilters" />
              </div>
              <div class="date-input">
                <label>
                  <i class="pi pi-calendar-minus"></i>
                  To Date
                </label>
                <input type="date" v-model="customDateTo" @change="applyFilters" />
              </div>
            </div>

            <!-- Department Filter -->
            <div class="filter-item">
              <label>
                <i class="pi pi-building"></i>
                Department
              </label>
              <div class="select-wrapper">
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
                <i class="pi pi-chevron-down select-icon"></i>
              </div>
            </div>

            <!-- Form Type Filter -->
            <div class="filter-item">
              <label>
                <i class="pi pi-file"></i>
                Form Type
              </label>
              <div class="select-wrapper">
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
                <i class="pi pi-chevron-down select-icon"></i>
              </div>
            </div>

            <!-- Business Unit Filter -->
            <div class="filter-item" v-if="availableBusinessUnits.length > 0">
              <label>
                <i class="pi pi-briefcase"></i>
                Business Unit
              </label>
              <div class="select-wrapper">
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
                <i class="pi pi-chevron-down select-icon"></i>
              </div>
            </div>

            <!-- Period Filter (for trends) -->
            <div class="filter-item">
              <label>
                <i class="pi pi-chart-line"></i>
                Trend Period
              </label>
              <div class="select-wrapper">
                <select v-model="selectedPeriod" @change="applyFilters">
                  <option value="daily">Daily</option>
                  <option value="weekly">Weekly</option>
                  <option value="monthly">Monthly</option>
                </select>
                <i class="pi pi-chevron-down select-icon"></i>
              </div>
            </div>
          </div>

          <!-- Apply/Reset Buttons -->
          <div class="filter-actions">
            <button class="btn-primary" @click="applyFilters" :disabled="loading">
              <i class="pi pi-check"></i>
              <span v-if="loading">Applying...</span>
              <span v-else>Apply Filters</span>
            </button>
            <button class="btn-secondary" @click="resetFilters">
              <i class="pi pi-refresh"></i>
              Reset All
            </button>
          </div>
        </div>
      </transition>
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
import { ref, onMounted, computed } from 'vue';
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
    const filtersExpanded = ref(true);
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

    // Filter UI methods
    const toggleFilters = () => {
      filtersExpanded.value = !filtersExpanded.value;
    };

    const activeFiltersCount = computed(() => {
      let count = 0;
      if (selectedDateRange.value !== 'last30days') count++;
      if (selectedDepartment.value) count++;
      if (selectedFormType.value) count++;
      if (selectedProperty.value) count++;
      if (selectedPeriod.value !== 'weekly') count++;
      return count;
    });

    const clearDateRange = () => {
      selectedDateRange.value = 'last30days';
      customDateFrom.value = '';
      customDateTo.value = '';
      applyFilters();
    };

    const clearDepartment = () => {
      selectedDepartment.value = '';
      applyFilters();
    };

    const clearFormType = () => {
      selectedFormType.value = '';
      applyFilters();
    };

    const clearProperty = () => {
      selectedProperty.value = '';
      applyFilters();
    };

    const clearPeriod = () => {
      selectedPeriod.value = 'weekly';
      applyFilters();
    };

    const getDepartmentLabel = (name) => {
      const dept = availableDepartments.value.find(d => d.name === name);
      return dept ? dept.department_name : name;
    };

    const getBusinessUnitLabel = (name) => {
      const unit = availableBusinessUnits.value.find(u => u.name === name);
      return unit ? unit.label : name;
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
      filtersExpanded,
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
      toggleFilters,
      activeFiltersCount,
      clearDateRange,
      clearDepartment,
      clearFormType,
      clearProperty,
      clearPeriod,
      getDepartmentLabel,
      getBusinessUnitLabel,
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
  margin-bottom: 32px;
  padding: 24px 0;
  border-bottom: 2px solid #f3f4f6;
}

.dashboard-header h1 {
  font-size: 2.25rem;
  font-weight: 700;
  background: linear-gradient(135deg, #1f2937 0%, #4b5563 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin-bottom: 8px;
}

.subtitle {
  color: #6b7280;
  font-size: 1.05rem;
  font-weight: 400;
}

.card {
  background: white;
  border-radius: 12px;
  padding: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 24px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

.filters-section {
  transition: all 0.3s ease;
}

.filters-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px 24px;
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s;
  border-bottom: 1px solid #f3f4f6;
}

.filters-header:hover {
  background-color: #f9fafb;
}

.filters-title {
  display: flex;
  align-items: center;
  gap: 12px;
}

.filters-title i.pi-filter {
  font-size: 1.2rem;
  color: #3b82f6;
}

.filters-title h3 {
  margin: 0;
  color: #1f2937;
  font-size: 1.1rem;
  font-weight: 600;
}

.active-count {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 0.8rem;
  font-weight: 600;
}

.active-filters-preview {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  padding: 12px 24px 20px;
  animation: fadeIn 0.3s ease;
}

.filter-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  background: linear-gradient(135deg, #e0e7ff 0%, #dbeafe 100%);
  color: #1e40af;
  padding: 6px 12px;
  border-radius: 16px;
  font-size: 0.85rem;
  font-weight: 500;
  transition: all 0.2s;
}

.filter-badge i.pi-times {
  cursor: pointer;
  font-size: 0.75rem;
  opacity: 0.7;
  transition: opacity 0.2s;
  padding: 2px;
}

.filter-badge i.pi-times:hover {
  opacity: 1;
  color: #ef4444;
}

.filter-expand-enter-active,
.filter-expand-leave-active {
  transition: all 0.3s ease;
  max-height: 1000px;
  overflow: hidden;
}

.filter-expand-enter-from,
.filter-expand-leave-to {
  max-height: 0;
  opacity: 0;
}

.filters-content {
  padding: 20px 24px 24px;
  background: linear-gradient(to bottom, #fafbfc 0%, #ffffff 100%);
}

.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.filter-item {
  display: flex;
  flex-direction: column;
}

.filter-item label {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  margin-bottom: 10px;
  color: #374151;
  font-size: 0.9rem;
}

.filter-item label i {
  color: #6b7280;
  font-size: 0.95rem;
}

.select-wrapper {
  position: relative;
}

.select-wrapper select {
  width: 100%;
  appearance: none;
  padding-right: 40px;
}

.select-icon {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: #6b7280;
  pointer-events: none;
  font-size: 0.85rem;
}

.filter-item select,
.filter-item input {
  width: 100%;
  padding: 11px 14px;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.95rem;
  background: white;
  transition: all 0.2s;
  color: #1f2937;
}

.filter-item select:hover,
.filter-item input:hover {
  border-color: #d1d5db;
}

.filter-item select:focus,
.filter-item input:focus {
  outline: none;
  border-color: #3b82f6;
  box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}

.date-range-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.range-btn {
  padding: 9px 18px;
  border: 2px solid #e5e7eb;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s;
  font-size: 0.9rem;
  font-weight: 500;
  color: #4b5563;
}

.range-btn:hover {
  background: #f9fafb;
  border-color: #3b82f6;
  color: #3b82f6;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.1);
}

.range-btn.active {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  border-color: #3b82f6;
  box-shadow: 0 4px 6px rgba(59, 130, 246, 0.25);
}

.custom-dates {
  grid-column: span 2;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  padding: 16px;
  background: #f9fafb;
  border-radius: 8px;
  border: 1px solid #e5e7eb;
}

.date-input {
  display: flex;
  flex-direction: column;
}

.filter-actions {
  display: flex;
  gap: 12px;
  align-items: center;
  justify-content: flex-end;
  padding-top: 16px;
  border-top: 1px solid #f3f4f6;
}

.btn-primary,
.btn-secondary {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  font-size: 0.95rem;
  transition: all 0.2s;
  white-space: nowrap;
}

.btn-primary {
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
  color: white;
  box-shadow: 0 2px 4px rgba(59, 130, 246, 0.2);
}

.btn-primary:hover:not(:disabled) {
  background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.3);
  transform: translateY(-1px);
}

.btn-primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.btn-secondary {
  background: white;
  color: #374151;
  border: 2px solid #e5e7eb;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
}

.btn-secondary:hover {
  background: #f9fafb;
  border-color: #d1d5db;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(-4px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
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
  border-radius: 12px;
  padding: 32px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  margin-bottom: 32px;
  border: 1px solid #e5e7eb;
  transition: box-shadow 0.3s ease;
}

.insight-section:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.12);
}

.insight-section h2 {
  font-size: 1.6rem;
  font-weight: 700;
  color: #1f2937;
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 3px solid #e5e7eb;
  position: relative;
}

.insight-section h2::before {
  content: '';
  position: absolute;
  bottom: -3px;
  left: 0;
  width: 60px;
  height: 3px;
  background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
}

.insight-section h3 {
  font-size: 1.25rem;
  font-weight: 600;
  color: #374151;
  margin: 24px 0 16px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
  margin-bottom: 32px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 24px;
  background: linear-gradient(135deg, #fafbfc 0%, #f9fafb 100%);
  border-radius: 12px;
  border: 2px solid #e5e7eb;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.stat-card:hover {
  border-color: #3b82f6;
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.15);
  transform: translateY(-2px);
}

.stat-card:hover::before {
  opacity: 1;
}

.stat-card.total {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.stat-card.total:hover {
  box-shadow: 0 6px 16px rgba(102, 126, 234, 0.4);
  transform: translateY(-3px);
}

.stat-icon {
  width: 56px;
  height: 56px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 14px;
  margin-right: 16px;
  font-size: 1.6rem;
  transition: all 0.3s ease;
}

.stat-card:hover .stat-icon {
  transform: scale(1.1) rotate(5deg);
}

.stat-icon.completed {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  color: #059669;
  box-shadow: 0 4px 8px rgba(16, 185, 129, 0.15);
}

.stat-icon.pending {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #d97706;
  box-shadow: 0 4px 8px rgba(245, 158, 11, 0.15);
}

.stat-icon.in-progress {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #2563eb;
  box-shadow: 0 4px 8px rgba(59, 130, 246, 0.15);
}

.stat-icon.cancelled {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #dc2626;
  box-shadow: 0 4px 8px rgba(239, 68, 68, 0.15);
}

.stat-icon.amount {
  background: linear-gradient(135deg, #e0e7ff 0%, #c7d2fe 100%);
  color: #4f46e5;
  box-shadow: 0 4px 8px rgba(99, 102, 241, 0.15);
}

.stat-card.total .stat-icon {
  background: rgba(255, 255, 255, 0.25);
  color: white;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
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
  margin: 32px 0;
  padding: 20px;
  background: #fafbfc;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
}

.data-table {
  margin-top: 24px;
  overflow-x: auto;
  border-radius: 10px;
  border: 1px solid #e5e7eb;
}

.data-table table {
  width: 100%;
  border-collapse: collapse;
}

.data-table th,
.data-table td {
  padding: 14px 16px;
  text-align: left;
  border-bottom: 1px solid #f3f4f6;
}

.data-table th {
  background: linear-gradient(135deg, #f9fafb 0%, #f3f4f6 100%);
  font-weight: 600;
  color: #374151;
  font-size: 0.9rem;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 2px solid #e5e7eb;
}

.data-table tbody tr {
  transition: all 0.2s ease;
}

.data-table tbody tr:hover {
  background: #f9fafb;
  transform: scale(1.005);
}

.data-table tbody tr:last-child td {
  border-bottom: none;
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
  padding: 6px 12px;
  background: linear-gradient(135deg, #e0e7ff 0%, #dbeafe 100%);
  color: #3730a3;
  border-radius: 16px;
  font-size: 0.8rem;
  font-weight: 500;
  margin-right: 6px;
  margin-bottom: 6px;
  border: 1px solid #c7d2fe;
  transition: all 0.2s ease;
}

.form-type-badge:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(55, 48, 163, 0.15);
}

.status-badge {
  padding: 6px 14px;
  border-radius: 16px;
  font-size: 0.85rem;
  font-weight: 600;
  border: 1px solid;
  transition: all 0.2s ease;
}

.status-badge:hover {
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.status-badge.completed {
  background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
  color: #065f46;
  border-color: #6ee7b7;
}

.status-badge.pending {
  background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
  color: #92400e;
  border-color: #fcd34d;
}

.status-badge.in-progress {
  background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
  color: #1e40af;
  border-color: #93c5fd;
}

.status-badge.cancelled {
  background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
  color: #991b1b;
  border-color: #fca5a5;
}

@media (max-width: 768px) {
  .new-dashboard-container {
    padding: 12px;
  }

  .dashboard-header {
    margin-bottom: 20px;
    padding: 16px 0;
  }

  .dashboard-header h1 {
    font-size: 1.75rem;
  }

  .subtitle {
    font-size: 0.95rem;
  }

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

  .insight-section {
    padding: 20px;
  }

  .insight-section h2 {
    font-size: 1.35rem;
  }

  .stat-card {
    padding: 18px;
  }

  .stat-icon {
    width: 48px;
    height: 48px;
    font-size: 1.3rem;
  }

  .filter-actions {
    flex-direction: column;
    width: 100%;
  }

  .btn-primary,
  .btn-secondary {
    width: 100%;
    justify-content: center;
  }

  .data-table th,
  .data-table td {
    padding: 10px 12px;
    font-size: 0.85rem;
  }
}
</style>
