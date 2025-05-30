<template>
    <section>
        <template v-if="!viewReport">
            <div class="d-flex justify-content-between align-items-center py-2">
                <div>

                </div>

            </div>
            <div>
                <GlobalTable :tHeaders="tableheaders" :tData="tableData" @cell-click="viewPreview" isAction="true"
                    viewType="viewPdf" isCheckbox="true" />
            </div>
        </template>
        <template v-else>
            <div class="d-flex justify-content-between align-items-center py-2">


            </div>
            <section>
                <div class=" d-flex justify-content-between align-content-center  py-3">
                    <button type="button" class="font-12 btn btn-light backtoListbtn" @click="backtoReportList">
                        <i class="bi bi-chevron-left"></i> Back to Report List
                    </button>
                    <!-- <button class=" btn btn-outline-danger font-12" @click="exportReport('Excel')">Export</button> -->
                    <div class="btn-group dropdown">
                        <ButtonComp
                            class="btn-outline-primary  m-0 dropdown-toggle d-flex justify-content-center align-items-center bg-white"
                            name="Export" type="button" id="exportDropdown" data-bs-toggle="dropdown"
                            aria-expanded="false" />
                        <ul class="dropdown-menu font-12" style="transform: translate(-124px, 42px) !important">
                            <li><a class="dropdown-item" @click="exportReport('Csv')">Download Csv</a></li>
                            <li>
                                <a class="dropdown-item" @click="exportReport('Excel')">Download Excel</a>
                            </li>
                        </ul>
                    </div>

                </div>
            </section>
            <section>
                <div id="datatable" tabindex="0" border="1" style="border-collapse: collapse; width: 100%;"></div>
            </section>
        </template>
    </section>
</template>

<script setup>

import GlobalTable from "../../Components/GlobalTable.vue";
import axiosInstance from "../../shared/services/interceptor";
import { apis, doctypes } from "../../shared/apiurls";
import { onBeforeUnmount, onMounted, ref } from "vue";
import DataTable from "frappe-datatable";
import "frappe-datatable/dist/frappe-datatable.min.css";
import ButtonComp from "../../Components/ButtonComp.vue";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";


// const totalRecords = ref(0);
const viewReport = ref(false);
const tableData = ref([]);
const frappeTH = ref([]);
function ReportsData() {
    const filters = [
        ["module", "=", 'ezy_custom_forms']
    ];
    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify(filters),


    };

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
const listData = ref([]);
const listDataheaders = ref([])
const frappeBody = ref([]);
const SelectedReportName = ref("");
function viewPreview(data) {
    console.log(data.name);
    SelectedReportName.value = data.name;
    viewReport.value = true;

    axiosInstance.get(apis.repostListData, {
        params: {
            report_name: SelectedReportName.value
        }
    })
        .then((res) => {
            if (res) {
                if (res?.message?.columns) {
                    frappeBody.value = res?.message?.result.map((item) => ({ ...item }));

                    frappeTH.value = res?.message?.columns.map((item) => ({
                        name: item?.fieldname,
                        label: item?.label
                    }));

                    new DataTable(document.getElementById("datatable"), {
                        columns: frappeTH.value,
                        data: frappeBody.value,
                        inlineFilters: true,
                        editable: false,
                    });

                    // frappeBody.value = res?.message?.result.map((item) =>
                    //     Object.values(item)
                    // ); 
                    // frappeTH.value = res?.message?.columns.map((item) => {
                    //     let obj = {};
                    //     obj["name"] = item?.label;
                    //     // obj["width"] = 170;
                    //     return obj;
                    // });
                    // //   if (frappeBody.value) {
                    // //     simulateCtrlF();
                    // //   }
                    // listData.value = res?.message?.result;
                    // listDataheaders.value = res?.message?.columns.map((item) => {
                    //     let obj = {};
                    //     obj["th"] = item?.label;
                    //     obj["td_key"] = item?.fieldname;
                    //     return obj;
                    // });

                    // new DataTable(document.getElementById("datatable"), {
                    //     columns: frappeTH.value,
                    //     data: frappeBody.value,
                    //     inlineFilters: true,
                    //     editable: false,
                    // });
                }
            }
        })
        .catch((error) => {
            console.error("Error fetching department data:", error);
        });
}
function simulateCtrlF() {
    const datatableEl = document.getElementById("datatable");

    if (datatableEl) {
        // 1. Focus the table
        datatableEl.focus();

        // 2. Trigger internal keydown event
        const event = new KeyboardEvent("keydown", {
            key: "f",
            keyCode: 70,
            ctrlKey: true,
            bubbles: true,
        });
        datatableEl.dispatchEvent(event);
    }
}

function handleCtrlF(e) {
    if (e.ctrlKey && e.key === 'f') {
        e.preventDefault(); // prevent browser search
        simulateCtrlF();    // simulate datatable search
    }
}

function backtoReportList() {
    viewReport.value = false;
}
const tableheaders = ref([
    { th: "Name", td_key: "name" },

])

function exportReport(type) {
    const reportName = SelectedReportName.value;
    const fileType = type;
    const url = apis.ExportReport + `?report_name=${encodeURIComponent(reportName)}&file_format_type=${encodeURIComponent(fileType)}`;
    // Trigger the file download
    window.open(url, '_blank');
}


onMounted(() => {
    ReportsData();
    // simulateCtrlF();
    document.addEventListener("keydown", handleCtrlF);

})
onBeforeUnmount(() => {
    document.removeEventListener("keydown", handleCtrlF);
});

</script>

<style lang="scss" scoped>
.dropdown-item {
    cursor: pointer;
}

.backtoListbtn {
    border: 1px solid #ccc !important;
}
</style>