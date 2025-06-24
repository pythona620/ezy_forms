<template>
    <div class="container-fluid">
        <div class="row mt-3">
            <!-- Loop over the dynamic chartsData array -->
            <div v-for="(chart, index) in chartsData" :key="index" class="col-6">
                <div class="chart-wrapper">
                    <div>
                        <h6 class="fw13 font-14 text-nowrap">
                            {{ chart.title }} (<b>{{ chart.data.total }}</b> requests)
                        </h6>
                        <!-- Each chart container gets its own ref and a fixed height -->
                        <div class="chart-container" :ref="el => chartRefs[index] = el" style="height: 300px"></div>
                    </div>
                    <div class="chart-info">
                        <div class="total-count">
                            <strong>{{ chart.data.total }}</strong>
                            <span class="font-14">Total Forms</span>
                        </div>
                        <div>
                            <!-- Loop over the keys to create dynamic legends -->
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
    </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue';
import * as echarts from 'echarts';
import { apis } from "../../shared/apiurls";
import axiosInstance from "../../shared/services/interceptor";
// import { useRouter } from 'vue-router'; 

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
    try {
        const response = await axiosInstance.get(`${apis.dashboard}`);
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
onMounted(fetchData);
</script>

<style scoped>
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
</style>