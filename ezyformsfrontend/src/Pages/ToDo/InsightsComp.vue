<template>
  <div class="dashboard-container py-3">
    <div v-if="ShowTable">
      <h1 class="mb-3 font-13">Insights</h1>
      <GlobalTable :tHeaders="tableheaders" :tData="tableData" isCheckbox="true" isAction="true" viewType="viewPdf"
      @cell-click="viewPreview" />
    </div>

    <div v-else class="dashboard-div">
      <div class="d-flex gap-3 align-items-center cursor-pointer">
        <h6 @click="backTo" class="font-13 d-flex align-items-center"><i class="bi bi-arrow-left me-2 fs-5 cursor-pointer"></i> Back</h6>
        <!-- <h6 class="font-13">( {{ reportsData.report_name }} )</h6> -->
      </div>
      <iframe :src="link" width="100%" height="96%" frameborder="0"></iframe>
    </div>
  </div>
</template>

<script setup>
import GlobalTable from '../../Components/GlobalTable.vue';

import axiosInstance from "../../shared/services/interceptor";
import { apis, doctypes } from "../../shared/apiurls";
import { onMounted, ref } from "vue";

const link = ref("");
const ShowTable=ref(true);
const reportsData=ref("");
const tableData = ref([]);

const filterObj = ref({
    limitPageLength: "none",
    limit_start: 0,
});

const tableheaders = ref([
    { th: "Report Name", td_key: "report_name" },
    // { th: "Report Link", td_key: "link" },
])

function backTo(){
  ShowTable.value=true;
}

function getInsights() {
  const docname = encodeURIComponent("Ezy Insights");

    const filters = [];

    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify(filters),
        limit_page_length: filterObj.value.limitPageLength,
        limit_start: filterObj.value.limit_start,
    };

    axiosInstance.get(`${apis.resource}${doctypes.EzyInsights}/${docname}}`, { params: queryParams })
        .then((res) => {
            if (res.data) {
                const newData = res.data.dashboards
                if (filterObj.value.limit_start === 0) {
                    tableData.value = newData;
                }else {
                    tableData.value = tableData.value.concat(newData)
                }
            }
        })
        .catch((error) => {
            console.error("Error fetching designations data:", error);
        });
}

function viewPreview(data) {
  reportsData.value=data;
  ShowTable.value=false;
  link.value = data.link;
}

onMounted(() => {
  getInsights();
});
</script>

<style scoped>
.dashboard-container {
  width: 100%;
  height: 100%;
}

.dashboard-div {
  height: 83vh;
}

.export-btn {
  /* background-color: #99999961; */
  padding: 5px 10px !important;
  border: none;
  border-radius: 4px;
  font-size: var(--eleven);
}
</style>
