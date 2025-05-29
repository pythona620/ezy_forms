<template>
    <section>
        <template v-if="!viewReport">
            <div class="d-flex justify-content-between align-items-center py-2">
                <div>
                    <h1 class="m-0 font-13">Requests </h1>
                    <p class="m-0 font-11 pt-1"> Total</p>
                </div>

            </div>
            <div>
                <GlobalTable :tHeaders="tableheaders" :tData="tableData" @cell-click="viewPreview" isAction="true"
                    viewType="viewPdf"  isCheckbox="true" />
            </div>
        </template>
        <template v-else>
            <div class="d-flex justify-content-between align-items-center py-2">
                <div>
                    <h1 class="m-0 font-13">Requests list</h1>
                    <p class="m-0 font-11 pt-1"> Total</p>
                </div>

            </div>
            <section>
                <div class=" d-flex justify-content-between align-content-center">
                    <button type="button" class="font-12 btn btn-light" @click="backtoReportList">
                        <i class="bi bi-chevron-left"></i> Back to Report List
                    </button>

                </div>
            </section>
            sai
        </template>
    </section>
</template>

<script setup>
import GlobalTable from "../../Components/GlobalTable.vue";
import axiosInstance from "../../shared/services/interceptor";
import { apis, doctypes } from "../../shared/apiurls";
import { onMounted, ref } from "vue";

// const totalRecords = ref(0);
const viewReport = ref(false);
const tableData = ref([]);
function ReportsData() {
    // const filters = [
    //     ["module", "=", 'ezy_custom_forms']
    // ];
    const queryParams = {
        fields: JSON.stringify(["*"]),
        // filters: JSON.stringify(filters),


    };
    // const queryParamsCount = {
    //     fields: JSON.stringify(["count(name) AS total_count"]),
    //     limitPageLength: "None",
    //     filters: JSON.stringify(filters),
    // }
    // axiosInstance.get(`${apis.resource}${doctypes.}`, { params: queryParamsCount })
    //     .then((res) => {
    //         // console.log(res.data[0].total_count);
    //         totalRecords.value = res.data[0].total_count

    //     })
    //     .catch((error) => {
    //         console.error("Error fetching ezyForms data:", error);
    //     });

    axiosInstance.get(apis.resource + doctypes.reportsApi, { params: queryParams })
        .then((res) => {
            if (res.data) {
                tableData.value = res.data;
            }
        })
        .catch((error) => {
            console.error("Error fetching department data:", error);
        });
}
function viewPreview(data) {
    console.log(data);
    viewReport.value = true;

}
function backtoReportList() {
    viewReport.value = false;
}
const tableheaders = ref([
    { th: "Name", td_key: "name" },

])
onMounted(() => {
    ReportsData();
})

</script>

<style lang="sass" scoped>

</style>