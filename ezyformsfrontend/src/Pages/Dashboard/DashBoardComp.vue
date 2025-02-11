<template>
    <div class="container-fluid">
        <div class="d-flex justify-content-end m-3 mb-2">
            <FormFields class="w-auto" tag="input" type="date" name="dateId" placeholder="Date of report" id="dateId"
                @change="selectedDate" v-model="dateId" :Required="false" />
        </div>
        <div class="row">
            <!-- Total Checks Status -->
            <div class="col-4">
                <div class="chart-wrapper">
                    <div>
                        <h6 class="fw13">Total Forms in Circulation</h6>
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
                                    <span class="label"><b>{{ scanned }}</b> Approved</span>
                                </div>
                                <div class="legend-item">
                                    <span class="color-box InProgress"></span>
                                    <span class="label"><b>{{ unScanned }}</b> In Progress</span>
                                </div>
                                <!-- </div>
                            <div class="legend"> -->
                                <div class="legend-item">
                                    <span class="color-box Rejected"></span>
                                    <span class="label"><b>{{ scanned }}</b> Rejected</span>
                                </div>
                                <div class="legend-item">
                                    <span class="color-box Pending"></span>
                                    <span class="label"><b>{{ unScanned }}</b> Pending</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>


            <!-- Scanned Checks -->
            <!-- <div class="col-4">
                <div class="chart-wrapper">
                    <div>
                        <h6 class="fw13">Scanned checks</h6>
                        <div class="chart-container" ref="scannedChecksChartRef"></div>
                    </div>
                    <div class="chart-info">
                        <div class="total-count">
                            <strong>{{ totalscannedChecksData }}</strong>
                            <span>Total checks scanned</span>
                        </div>
                        <div class="legend">
                            <div class="legend-item">
                                <span class="color-box Pending "></span>
                                <span class="label"><b>{{ scannedChecks }}</b> Reviewed</span>
                            </div>
                            <div class="legend-item">
                                <span class="color-box Reviewed"></span>
                                <span class="label"><b>{{ pendingReview }}</b> Pending review</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="col-4">
                <div class="chart-wrapper">
                    <div>
                        <h6 class="fw13">Reviewed status</h6>
                        <div class="chart-container" ref="reviewedStatusChartRef"></div>
                    </div>
                    <div class="chart-info">
                        <div class="total-count">
                            <strong>{{ reviewChecks }}</strong>
                            <span>Total reviewed checks</span>
                        </div>
                        <div class="legend">
                            <div class="legend-item">
                                <span class="color-box Missing"></span>
                                <span class="label"><b>{{ orphanChecks }}</b> Orphaned checks</span>
                            </div>
                            <div class="legend-item">
                                <span class="color-box Orphaned "></span>
                                <span class="label"><b>{{ missingSymphony }}</b> Missing in symphony</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div> -->

        </div>
    </div>

</template>

<script setup>
import { ref, onMounted } from 'vue';
import FormFields from '../../Components/FormFields.vue';
import * as echarts from 'echarts';
import { getPreviousDate } from "@/shared/services/Default_prev_date";

// Dummy data
const scanned = ref(50);
const unScanned = ref(30);
const InProgress = ref(30);
const pending = ref(30);

const totalChecks = ref(scanned.value + unScanned.value + InProgress.value + pending.value);

const reviewChecks = ref(120);
const orphanChecks = ref(10);
const missingSymphony = ref(5);

const scannedChecks = ref(80);
const pendingReview = ref(40);
const totalscannedChecksData = ref(scannedChecks.value + pendingReview.value);

const totalChecksChartRef = ref(null);
const scannedChecksChartRef = ref(null);
const reviewedStatusChartRef = ref(null);
const dateId = ref(getPreviousDate());

async function selectedDate(e) {
    dateId.value = await e.target.value;
    // Simulate the data fetching
    DailyTracking();
}

// Simulated function to update charts with dummy data
function updateCharts() {
    if (totalChecksChartRef.value) {
        const chart = echarts.init(totalChecksChartRef.value);
        const options = {
            tooltip: {
                trigger: 'item',
                formatter: '{b}: {c} ({d}%)',
            },
            series: [
                {
                    name: 'Check Status',
                    type: 'pie',
                    radius: ['55%', '80%'],
                    avoidLabelOverlap: false,
                    label: {
                        show: false,
                    },
                    data: [
                        { value: unScanned.value, name: 'Un-Scanned', itemStyle: { color: '#FF0000' } },
                        { value: scanned.value, name: 'Scanned', itemStyle: { color: '#00FF00' } },
                        { value: pending.value, name: 'Pending', itemStyle: { color: '#ECE51F' } },
                        { value: InProgress.value, name: 'In Progress', itemStyle: { color: '#594DFA' } },
                    ],
                },
            ],
        };
        chart.setOption(options);
    }

    if (scannedChecksChartRef.value) {
        const chart = echarts.init(scannedChecksChartRef.value);
        const options = {
            tooltip: {
                trigger: 'item',
                formatter: '{b}: {c} ({d}%)',
            },
            series: [
                {
                    name: 'Scanned Checks',
                    type: 'pie',
                    radius: ['55%', '80%'],
                    avoidLabelOverlap: false,
                    label: {
                        show: false,
                    },
                    data: [
                        { value: scannedChecks.value, name: 'Reviewed', itemStyle: { color: '#2FEB1E' } },
                        { value: pendingReview.value, name: 'Pending Review', itemStyle: { color: '#1511EC' } },
                    ],
                },
            ],
        };
        chart.setOption(options);
    }

    if (reviewedStatusChartRef.value) {
        const chart = echarts.init(reviewedStatusChartRef.value);
        const options = {
            tooltip: {
                trigger: 'item',
                formatter: '{b}: {c} ({d}%)',
            },
            series: [
                {
                    name: 'Reviewed Status',
                    type: 'pie',
                    radius: ['55%', '80%'],
                    avoidLabelOverlap: false,
                    label: {
                        show: false,
                    },
                    data: [
                        { value: orphanChecks.value, name: 'Orphaned Checks', itemStyle: { color: '#FF8992' } },
                        { value: missingSymphony.value, name: 'Missing Symphony', itemStyle: { color: '#979797' } },
                    ],
                },
            ],
        };
        chart.setOption(options);
    }
}

onMounted(async () => {
    // Call updateCharts immediately for dummy data
    updateCharts();
});
</script>


<style scoped>
.chart-wrapper {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 20px;
    border: 1px solid #EEEEEE;
    border-radius: 4px;
    box-shadow: 0px 2px 2px 0px #0000000D;
    background-color: #fff;
}

.chart-container {
    width: 180px;
    height: 180px;
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

.Rejected {
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
    font-size: 14px;
    color: #333;
}

.bar-chart {
    margin-top: 20px;
    height: 280px;
    /* width: 100%; */
    background-color: white;
}
</style>
