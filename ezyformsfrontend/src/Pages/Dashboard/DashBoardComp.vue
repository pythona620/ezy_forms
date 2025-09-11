<template>
    <div class="container-fluid">
        <div class="row mt-3">
            <div v-if="showSubscriptionAlert" class="subscription-div font-13 col-12">
                <i class="bi bi-exclamation-triangle text-danger me-2 fs-5"></i> 
                <span class="d-flex mt-1 flex-wrap">
                    Your subscription will expire in 
                    <span class="text-danger mx-2 text-underline">{{ remainingDaysCount }}</span>
                    days, on 
                    <span class="text-danger mx-2 text-underline">{{ subscriptionEndDateStr }}</span>
                </span>
            </div>

            <!-- Dynamic charts -->
            <div v-for="(chart, index) in chartsData" :key="index" class="col-lg-6 col-md-6 mb-3">
                <div class="chart-wrapper flex-column flex-lg-row">
                    <div>
                        <h6 class="fw13 font-14 text-nowrap">
                            {{ chart.title }} (<b>{{ chart.data.total }}</b> requests)
                        </h6>
                        <div class="chart-container" :ref="el => chartRefs[index] = el" style="height: 300px"></div>
                    </div>
                    <div class="chart-info mt-3 mt-md-0">
                        <div class="total-count">
                            <strong>{{ chart.data.total }}</strong>
                            <span class=" responsive-title ">Total Forms</span>
                        </div>
                        <div>
                            <div v-for="(key, i) in filteredKeys(chart.title)" :key="i" class="legend">
                                <div class="legend-item">
                                    <span class="color-box" :style="{ backgroundColor: colorMapping[key] }"></span>
                                    <span class="label">
                                        <b>{{ chart.data[key] || 0 }}</b> {{ displayMapping[key] }}
                                    </span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Tasks Table -->
        <div class="row mt-3">
            <div class="col-12 mb-2">
                <h6 class="fw-bold">My Tasks</h6>
            </div>
            <div class="col-12 table-responsive">
                <GlobalTable
                    class="dashboard-table"
                    :tHeaders="tableheaders"
                    :tData="tableData"
                    isAction="true"
                    viewType="viewPdf"
                    isCheckbox="true"
                    @updateFilters="inLineFiltersData"
                    :field-mapping="fieldMapping"
                    @cell-click="viewPreview"
                    isFiltersoption="true"
                    :actions="actions"
                />
            </div>
        </div>
    </div>
</template>
<script setup>
import { ref, onMounted, nextTick } from 'vue';
import * as echarts from 'echarts';
import { apis, doctypes } from "../../shared/apiurls";
import axiosInstance from "../../shared/services/interceptor";
import GlobalTable from "../../Components/GlobalTable.vue";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import { useRoute, useRouter } from "vue-router";
import { computed } from 'vue';
import { watch } from 'vue';
import { EzyBusinessUnit } from "../../shared/services/business_unit";
const router = useRouter();
const route = useRoute();

const businessUnit = computed(() => {
  return EzyBusinessUnit.value;
});
const newBusinessUnit = ref({ business_unit: "" });

const idDta = ref([]);
const tableData = ref([]);
const employeeData = ref([]);
const filterObj = ref({ limitPageLength: 20, limit_start: 0, filters: [] });
const docTypeName = ref([]);
const totalRecords = ref(0);
const statusOptions = ref([]);
const subEndDate=ref("");
const remainingDaysCount = ref(0);
const subscriptionEndDateStr = ref("");
const showSubscriptionAlert = ref(false);
const timeout = ref(null);

const fullData = ref([]); 
const filteredData = ref([]);
const tableheaders = ref([
  { th: "Request ID", td_key: "name" },
  // { th: "Form name", td_key: "name" },
  // { th: "Form category", td_key: "doctype_name" },
  // { th: "Owner of form", td_key: "owner" },
  { th: "Requester Name", td_key: "requester_name" },
  { th: "Requested On", td_key: "requested_on" },
  { th: "Requester Department", td_key: "department_name" },
  // { th: "Property", td_key: "property" },
  { th: "Approval Status", td_key: "status" },
  { th: "Pending With", td_key: "assigned_to_users" },

]);

const actions = ref([
  { name: "View Request", icon: "fa-solid fa-eye" },

  // { name: 'Share this form', icon: 'fa-solid fa-share-alt' },
  // { name: 'Download Form', icon: 'fa-solid fa-download' },
  // { name: 'Edit Form', icon: 'fa-solid fa-edit' },
]);
// Define keys used for legends and chart series
const keys = ['Approved', 'Pending', 'request_raised', 'Request_cancelled'];

// Color mapping for each key
const colorMapping = {
    Approved: '#00FF00',
    Pending: '#594DFA',
    request_raised: '#ECE51F',
    Request_cancelled: '#FF0000'
};

// Display mapping to show proper labels in legends
const displayMapping = {
    Approved: 'Approved',
    Pending: 'Pending',
    request_raised: 'Request Raised',
    Request_cancelled: 'Request Cancelled'
};

const filteredKeys = (title) => {
    return title === "Requests Assigned to me"
        ? ["Pending", "request_raised"]  // Show only these for this chart
        : keys; // Show all keys for other charts
};

// Array to hold chart data for each dataset
const chartsData = ref([]);

// Array to store refs for each dynamically rendered chart container
const chartRefs = [];

// const router = useRouter();

// API call that fetches the data and processes it
async function fetchData() {
    const queryParams = {
        property : businessUnit.value
        };

    try {
        const response = await axiosInstance.get(`${apis.dashboard}`, { params: queryParams });
        if (response.message) {
            // Extract the two datasets from the API response
            const receivedByUser = response.message.data.received_by_user;
            const requestedByUser = response.message.data.requested_by_user;

            // Calculate totals for each dataset
            const receivedTotal =
                (receivedByUser.Approved || 0) +
                (receivedByUser.Pending || 0) +
                (receivedByUser.request_raised || 0) +
                (receivedByUser.Request_cancelled || 0);

            const requestedTotal =
                (requestedByUser.Approved || 0) +
                (requestedByUser.Pending || 0) +
                (requestedByUser.request_raised || 0) +
                (requestedByUser.Request_cancelled || 0);

 // Build an array for the charts.
            // Only add the "received" chart if receivedTotal > 0.
            // const tempCharts = [];
            // if (receivedTotal > 0) {
            //     tempCharts.push({
            //         title: "Requests Assigned to me",
            //         data: {
            //             ...receivedByUser,
            //             total: receivedTotal
            //         }
            //     });
            // }

            // // Always add the "requested" chart regardless of requestedTotal value.
            // tempCharts.push({
            //     title: "Requests Submitted",
            //     data: {
            //         ...requestedByUser,
            //         total: requestedTotal
            //     }
            // });

            // chartsData.value = tempCharts;

            chartsData.value = [
                {
                    title: "Requests Assigned to me",
                    data: {
                        request_raised: receivedByUser.request_raised || 0,
                        Pending: receivedByUser.Pending || 0,
                        total: (receivedByUser.request_raised || 0) + (receivedByUser.Pending || 0)
                    }
                },
                {
                    title: "Requests Submitted",
                    data: {
                        ...requestedByUser,
                        total: requestedTotal
                    }
                }
            ];



            // Wait for the DOM to update so refs are populated, then initialize charts
            await nextTick();
            updateCharts();
        }
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}
// Google Charts loader
onMounted(() => {
    fetchData()
    subEndDate.value = (localStorage.getItem("subEndDate"));
    if (subEndDate.value) {
    const today = new Date();
    const endDate = new Date(subEndDate.value);

    const diffTime = endDate - today;
    remainingDaysCount.value = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    subscriptionEndDateStr.value = subEndDate.value;

    // Show alert only if subscription ends in 30 days or less
    if (remainingDaysCount.value <= 30 && remainingDaysCount.value > 0) {
      showSubscriptionAlert.value = true;
    }
  }

    // Load Google Charts script
    // const script = document.createElement('script')
    // script.src = 'https://www.gstatic.com/charts/loader.js'
    // script.onload = () => {
    //     google.charts.load('current', { packages: ['corechart'] })
    //     google.charts.setOnLoadCallback(drawDonutChart)
    // }
    // document.head.appendChild(script)
})
const viewlist = ref([])
function ViewOnlyReport() {
  axiosInstance
    .post(apis.view_only_reportee)
    .then((response) => {
      // Filter out items with status 'Completed' or 'Request Cancelled'
      const filtered = (response.message || []).filter(
        item => item.status !== 'Completed' && item.status !== 'Request Cancelled'
      );

      fullData.value = filtered;
      filteredData.value = [...filtered];

      totalRecords.value = filteredData.value.length;
      limitStart.value = 0;
      tableData.value = filteredData.value.slice(0, limit.value);
    })
    .catch((error) => {
      console.error(error);
    });
}

const limit = ref(20);
const limitStart = ref(0);

function paginateData(filtered = fullData.value) {
  const paginated = filtered.slice(limitStart.value, limitStart.value + limit.value);
  tableData.value = paginated;
  totalRecords.value = filtered.length;
}

function inLineFiltersData(searchedData) {
  clearTimeout(timeout.value);

  timeout.value = setTimeout(() => {
    filteredData.value = fullData.value.filter((row) => {
      return tableheaders.value.every((header) => {
        const key = header.td_key;
        if (searchedData[key]) {
          return String(row[key] || "").toLowerCase().includes(String(searchedData[key]).toLowerCase());
        }
        return true;
      });
    });

    totalRecords.value = filteredData.value.length;
    limit.value = 20;
    limitStart.value = 0;

    tableData.value = filteredData.value.slice(0, limit.value);
  }, 500);
}

function PaginationUpdateValue(newLimit) {
  limit.value = newLimit;
  limitStart.value = 0;
  paginateData();
}

function PaginationLimitStart() {
  limitStart.value += limit.value;

  const nextBatch = filteredData.value.slice(limitStart.value, limitStart.value + limit.value);

  tableData.value = [...tableData.value, ...nextBatch];
}





watch(
  businessUnit,
  (newVal) => {
    newBusinessUnit.value.business_unit = newVal;

    if (newVal.length) {
      ViewOnlyReport();
    }
  },
  { immediate: true }
);
function viewPreview(data) {
  // console.log(data);
  router.push({
    name: "ApproveRequest",
    query: {
      routepath: route.path,
      name: data.name,
      doctype_name: data.doctype_name,
      type: "mytasks",
      designation: employeeData.value

    },
  });
}



const fieldMapping = computed(() => ({
  // invoice_type: { type: "select", options: ["B2B", "B2G", "B2C"] },
  // credit_irn_generated: { type: "select", options: ["Pending", "Completed", "Error"] },
  // role: { type: "input" },
  name: { type: "input" },
  requester_name: { type: "input" },
  requested_on: { type: "date" },
  department_name: { type: "input" },


  status: { type: "select", options:["Request Raised","In Progress"] },

}));



// Function to initialize and update each chart dynamically
function updateCharts() {
    chartsData.value.forEach((chartData, index) => {
        const el = chartRefs[index];
        if (el) {
            const chartInstance = echarts.init(el);

            // Build series data dynamically based on the keys
            const seriesData = keys.map(key => ({
                value: chartData.data[key] || 0,
                name: displayMapping[key],
                itemStyle: { color: colorMapping[key] }
            }));

            chartInstance.setOption({
                tooltip: {
                    trigger: 'item',
                    formatter: '{c}'
                },
                series: [{
                    type: 'pie',
                    radius: ['40%', '75%'],
                    center: ['50%', '50%'],
                    label: {
                        show: true,
                        position: 'inside',
                        color: '#fff',
                        fontSize: 16,
                        formatter: params => params.value === 0 ? '' : params.value
                    },
                    labelLine: { show: false },
                    data: seriesData
                }],
                graphic: {
                    type: 'text',
                    left: 'center',
                    top: 'center',
                    style: {
                        text: `${chartData.data.total}\nTotal Forms`,
                        textAlign: 'center',
                        fontSize: 16,
                        fontWeight: 'bold',
                        fill: '#000'
                    }
                }
            });
//                        chartInstance.setOption({
//     tooltip: {
//         trigger: 'axis'
//     },
//     xAxis: {
//         type: 'category',
//         data: keys.map(key => displayMapping[key]), // legend names
//         axisLabel: {
//             rotate: 30
//         }
//     },
//     yAxis: {
//         type: 'value'
//     },
//     series: [{
//         type: 'bar',
//         data: keys.map(key => chartData.data[key] || 0),
//         itemStyle: {
//             color: (params) => {
//                 const key = keys[params.dataIndex];
//                 return colorMapping[key];
//             }
//         },
//         label: {
//             show: true,
//             position: 'top'
//         }
//     }]
// });

            // // Add click event for chart values
            // chartInstance.off('click'); // Remove previous listeners if any
            // chartInstance.on('click', function(params) {
            //     // Route based on chart title
            //     let path = chartData.title === "Requests Assigned to me"
            //         ? '/todo/receivedform'
            //         : '/todo/raisedbyme';
            //     // If the clicked name is "Pending", send "In Progress" instead
            //     let status = params.name === 'Pending' ? 'In Progress' : params.name;
            //     router.push({ path, query: { status } });
            // });

            // Ensure the chart resizes when the window size changes
            window.addEventListener('resize', () => chartInstance.resize());
        }
    });
}

// Fetch data and initialize charts when the component mounts
// onMounted(fetchData);
</script>

<style scoped>



.dashboard-table{
    height: 40dvh !important;
    overflow: auto;
}
.main-div {
    background-color: #fafafa;
}

.chart-wrapper {
    display: flex;
    align-items: center;
    justify-content: space-evenly;
    padding: 20px;
    border: 1px solid #EEEEEE;
    border-radius: 4px;
    box-shadow: 0px 2px 2px 0px #0000000D;
    background-color: #f7f7f7;
}

.chart-container {
    width: 280px;
    height: 280px;
}

.chart-info {
    margin-left: 20px;
}

h3 {
    font-size: 18px;
    font-weight: 600;
    margin-bottom: 10px;
}

.total-count {
    font-size: 12px;
    font-weight: 400;
    margin-bottom: 15px;
}
.responsive-title {
  font-size: 12px !important; /* default mobile */
}

@media (min-width: 768px) {
  .responsive-title {
    font-size: 14px;
  }
}

@media (min-width: 1200px) {
  .responsive-title {
    font-size: 14px;
  }
}


.total-count strong {
    font-size: 13px;
    display: block;
    font-weight: 700;
}

.legend {
    display: flex;
    flex-direction: column;
    line-height: 25px;
}

.legend-item {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.color-box {
    width: 17px;
    height: 15px;
    margin-right: 10px;
    border-radius: 3px;
}

.InProgress {
    background-color: #594DFA;
}

.scanned {
    background-color: #00ff00;
}

.request_raised {
    background-color: #ff0000;
}

.Reviewed {
    background-color: #1511EC;
}

.Pending {
    background-color: #ECE51F;
}

.Orphaned {
    background-color: #979797;
}

.Missing {
    background-color: #FF8992;
}

.label {
    font-size: 13px;
    color: #333;
}
.subscription-div {
    background-color: #f3ea6b;
    padding: 8px 10px;
    border-radius: 5px;
    margin-bottom: 15px;
    font-weight: 600;
    display: flex;
    align-items: center;
}
.dashboard-table {
    max-height: 40dvh;
    overflow-x: auto;
}

/* Charts */
.chart-wrapper {
    display: flex;
    /* align-items: flex-start;
    justify-content: space-between; */
    padding: 20px;
    border: 1px solid #EEEEEE;
    border-radius: 4px;
    box-shadow: 0px 2px 2px 0px #0000000D;
    background-color: #f7f7f7;
    flex-wrap: wrap;
}

.chart-container {
    width: 100%;
    max-width: 280px;
    height: 280px;
}

.chart-info {
    margin-left: 0;
    margin-top: 20px;
}

@media (min-width: 768px) {
    .chart-wrapper {
        flex-wrap: nowrap;
    }
    .chart-info {
        margin-left: 20px;
        margin-top: 0;
    }
}

/* Legends */
.legend {
    display: flex;
    flex-direction: column;
    line-height: 25px;
}

.legend-item {
    display: flex;
    align-items: center;
    margin-bottom: 10px;
}

.color-box {
    width: 17px;
    height: 15px;
    margin-right: 10px;
    border-radius: 3px;
}

/* Subscription alert */
.subscription-div {
    background-color: #f3ea6b;
    padding: 8px 10px;
    border-radius: 5px;
    margin-bottom: 15px;
    font-weight: 600;
    display: flex;
    align-items: center;
    flex-wrap: wrap;
}

/* Table responsiveness */
.table-responsive {
    overflow-x: auto;
}
</style>