<template>
    <div>
        <div class="d-flex align-items-center justify-content-between py-2">
            <div>
                <h1 class="m-0 font-13">
                    Designations
                </h1>
                <!-- <p class="m-0 font-11 pt-1">
                374 users
            </p> -->
            </div>
            <div class="d-flex align-items-center gap-2">

                <div>
                    <FormFields labeltext="" class="my-1" tag="input" type="search" placeholder="Search Designation"
                        name="Value" id="Value" v-model="filterObj.search" @input="designationData()" />
                </div>

            </div>
        </div>
        <div class="mt-2">
            <GlobalTable :tHeaders="tableheaders" :tData="tableData" isCheckbox="true" />
            <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords"
                @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
        </div>
    </div>
</template>
<script setup>
import FormFields from '../../Components/FormFields.vue';
import GlobalTable from '../../Components/GlobalTable.vue';
import PaginationComp from '../../Components/PaginationComp.vue'
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from '../../shared/apiurls';
import { onMounted, ref, computed, watch } from 'vue';
import { EzyBusinessUnit } from "../../shared/services/business_unit";
const businessUnit = computed(() => {
    return EzyBusinessUnit.value;
});
onMounted(() => {
    designationData();

})
const totalRecords = ref(0);

const tableData = ref([]);
const tableheaders = ref([
    { th: "Designation", td_key: "role" },

])
const createDesignation = ref({
    ezy_business_unit: "",
});
const filterObj = ref({
    limitPageLength: 20,
    limit_start: 0,
    search: ""
});
// Handle updating the current value
const PaginationUpdateValue = (itemsPerPage) => {
    filterObj.value.limitPageLength = itemsPerPage;
    filterObj.value.limit_start = 0;
    designationData();

};
// Handle updating the limit start
const PaginationLimitStart = ([itemsPerPage, start]) => {
    filterObj.value.limitPageLength = itemsPerPage;
    filterObj.value.limit_start = start;
    designationData();

};
watch(
    businessUnit,
    (newVal) => {
        createDesignation.value.ezy_business_unit = newVal;

        // if (newVal) {
        //     console.log(newVal, "new value of business unit");

        // }
    },
    { immediate: true }
);

function designationData() {
    const filters = [

    ];
    if (filterObj.value.search.trim()) {
        filters.push(["name", "like", `%${filterObj.value.search}%`]);
    }

    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify(filters),
        limit_page_length: filterObj.value.limitPageLength,
        limit_start: filterObj.value.limit_start,
        order_by: "`tabWF Roles`.`creation` desc"
    };
    const queryParamsCount = {
        fields: JSON.stringify(["count(name) AS total_count"]),
        limitPageLength: "None",
        filters: JSON.stringify(filters),
    }
    axiosInstance.get(`${apis.resource}${doctypes.designations}`, { params: queryParamsCount })
        .then((res) => {

            totalRecords.value = res.data[0].total_count

        })
        .catch((error) => {
            console.error("Error fetching ezyForms data:", error);
        });

    axiosInstance.get(apis.resource + doctypes.designations, { params: queryParams })
        .then((res) => {
            if (res.data) {
                const newData = res.data
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




</script>
<style scoped>
.global-table th {
    background-color: #f2f2f2 !important;
    text-align: left;
    color: #999999;
    font-size: 12px;
}

.filterbtn {
    border: 1px solid #CCCCCC;
    font-size: 16px;
    border-radius: 4px;
    color: #999999;
    padding: 8px;
    width: 100%;
}

.CreateDepartments {
    width: 100% !important;
    padding: 5px 10px !important;
}

.cancelfilter {
    width: 150px;
    height: 34px;
    border-radius: 6px;
    background-color: #f1f1f1;
    color: #111111;
    padding: 8px 20px;
}

.applyfilter {
    width: 150px;
    height: 34px;
    border-radius: 6px;
    /* background-color: #f1f1f1; */
    /* color: #111111; */
    padding: 8px 20px;
}
</style>