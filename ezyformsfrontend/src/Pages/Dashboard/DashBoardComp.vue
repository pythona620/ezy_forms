<template>
    <div class="container-fluid">
        <div class="row mt-3">
            <!-- Total Checks Status -->
            <div class="col-6">
                <div class="chart-wrapper">
                    <div>
                        <h6 class="fw13 font-13 text-nowrap">Requests received for me (4 requests)</h6>
                        <div class="chart-container" ref="totalChecksChartRef"></div>
                    </div>
                    <div class="chart-info">
                        <div class="total-count">
                            <strong>{{ totalChecks }}</strong>
                            <span>Total forms</span>
                        </div>
                        <div class="d-flex gap-4">
                            <div class="legend">
                                <div class="legend-item">
                                    <span class="color-box scanned"></span>
                                    <span class="label"><b>{{ Approved || 0 }}</b> Approved</span>
                                </div>
                                <!-- </div>
                            <div class="legend"> -->
                                <div class="legend-item">
                                    <span class="color-box InProgress"></span>
                                    <span class="label"><b>{{ Pending || 0 }}</b> Pending</span>
                                </div>
                                <div class="legend-item">
                                    <span class="color-box Pending"></span>
                                    <span class="label"><b>{{ request_raised || 0 }}</b> Request Raised</span>
                                </div>
                                <div class="legend-item">
                                    <span class="color-box request_raised"></span>
                                    <span class="label"><b>{{ Request_cancelled || 0 }}</b> Request Cancelled</span>
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
import { ref, onMounted, watch } from 'vue';
import * as echarts from 'echarts';
import { apis } from "../../shared/apiurls";
import axiosInstance from "../../shared/services/interceptor";

// Reactive state for API data
const Approved = ref(0);
const Request_cancelled = ref(0);
const request_raised = ref(0);
const Pending = ref(0);
const totalChecks = ref(0);
const totalChecksChartRef = ref(null);

async function fetchData() {
    try {
        const response = await axiosInstance.get(`${apis.dashboard}`);
        if (response.message) {
            const newData = response.message;
            Approved.value = newData.Approved || 0;
            Request_cancelled.value = newData["Request_cancelled"] || 0;
            Pending.value = newData.Pending || 0;
            request_raised.value = newData.request_raised || 0;

            // Update total count
            totalChecks.value = Approved.value + Request_cancelled.value + request_raised.value + Pending.value;

            // Update the chart
            updateChart();
        }
    } catch (error) {
        console.error("Error fetching data:", error);
    }
}

// Function to render ECharts
function updateChart() {
    if (totalChecksChartRef.value) {
        const chart = echarts.init(totalChecksChartRef.value);
        chart.setOption({
            tooltip: {
                trigger: 'item',
                formatter: '{c}', // Show only value
            },
            series: [{
                type: 'pie',
                radius: ['40%', '70%'], // Adjust for a bigger donut chart
                center: ['50%', '50%'],
                label: {
                    show: true,
                    position: 'inside',
                    color: '#fff',
                    fontSize: 16, // Increase font size
                    formatter: '{c}', // Show values inside sections
                },
                labelLine: { show: false },
                data: [
                    { value: Approved.value, name: 'Approved', itemStyle: { color: '#00FF00' } },
                    { value: Pending.value, name: 'Pending', itemStyle: { color: '#594DFA' } },
                    { value: request_raised.value, name: 'request_raised', itemStyle: { color: '#ECE51F' } },
                    { value: Request_cancelled.value, name: 'Request_cancelled', itemStyle: { color: '#FF0000' } },
                ]
            }],
            graphic: {
                type: 'text',
                left: 'center',
                top: 'center',
                style: {
                    text: `${totalChecks.value}\nTotal forms`,
                    textAlign: 'center',
                    fontSize: 16, // Increase text size
                    fontWeight: 'bold',
                    fill: '#000',
                }
            }
        });

        window.addEventListener('resize', () => {
            chart.resize(); // Ensure chart resizes when window size changes
        });
    }
}


// Watch for changes in data & update chart
watch([Approved, Request_cancelled, request_raised, Pending], updateChart);

// Fetch data when component mounts
onMounted(fetchData);
</script>

<style scoped>
.main-div {
    background-color: #fafafa;
}

.chart-wrapper {
    display: flex;
    align-items: center;
    justify-content: space-evenly                                                                                                                                                                                                                                                                       ;
    padding: 20px;
    border: 1px solid #EEEEEE;
    border-radius: 4px;
    box-shadow: 0px 2px 2px 0px #0000000D;
    background-color: #fff;
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
    font-size: 12px;
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
    white-space: nowrap;
}
</style>
