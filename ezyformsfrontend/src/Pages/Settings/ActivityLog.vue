<template>
    <div>
        <div class="d-flex justify-content-between align-items-center  py-2">
            <div>
                <h1 class="mt-3 font-13">
                    Activity Log
                </h1>
            </div>
            <div class="d-flex gap-2 align-items-center">
                <!-- <div class="d-flex align-items-center ">
                    <button type="button" class="btn btn-dark buttoncomp CreateDepartments d-flex align-items-center " @click="CreateDeprtModal"
                        data-bs-toggle="modal" data-bs-target="#createDepartments">
                        Create Department
                    </button>
                </div> -->

            </div>
        </div>
        <div class="mt-2">
            <GlobalTable :tHeaders="tableheaders" :tData="tableData"
                 isCheckbox="true" isFiltersoption="true"
                :field-mapping="fieldMapping" @updateFilters="inLineFiltersData" />
            <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords"
                @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
        </div>

    </div>
</template>
<script setup>
import GlobalTable from '../../Components/GlobalTable.vue';
import PaginationComp from '../../Components/PaginationComp.vue'
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from '../../shared/apiurls';
import { onMounted, ref, computed, watch, reactive } from 'vue';
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import "@vueform/multiselect/themes/default.css";

const businessUnit = computed(() => {
    return EzyBusinessUnit.value;
});
// onMounted(() => {
//     ezyForms();
// })
const totalRecords = ref(0);

const tableData = ref([]);
const radioOptions = ref(["yes", "no"])
const EzyFormsCompanys = ref([]);
const newCategory = ref("");
const editIndex = ref(null);
const editCategory = ref("");
const categoriesData = ref([])
const categoriesDataEdit = ref({ ezy_departments_items: [] });
const designiations = ref([]);
const actions = ref(
    [
        { name: 'View Categories', icon: 'fa-solid fa-eye' },

    ]
)
const filterObj = ref({
  limitPageLength: 20,
  limit_start: 0,
  filters: []
});
const formErrors = ref({
    department_code: "",
    department_name: ""
});
const departmenCodeData = ref([]);

const tableheaders = ref([
    { th: "User Name", td_key: "full_name" },
    { th: "User Id", td_key: "user" },
    { th: "Type of Activity", td_key: "subject" },
    { th: "Date", td_key: "communication_date" },
    { th: "Ip Address", td_key: "ip_address" },
    { th: "Status", td_key: "status" },

])
const fieldMapping = ref({
    full_name: { type: "input" },
    subject: { type: "input" },
    status: { type: "select", options: ["Success", "Failed"] },
});
const CreateDepartments = ref({
    department_code: "",
    department_name: "",
    business_unit: "",
    ezy_departments_items: [

    ]
});
watch(() => CreateDepartments.value.department_code, (newVal) => {
    const trimmedVal = newVal.trim().toLowerCase();
    const existingCodes = departmenCodeData.value
        .filter(code => code !== null)
        .map(code => code.trim().toLowerCase());

    if (existingCodes.includes(trimmedVal)) {
        formErrors.value.department_code = "Department code already exists.";
    } else {
        formErrors.value.department_code = "";
    }
});

watch(() => CreateDepartments.value.department_name, (newVal) => {
    const trimmedVal = newVal.trim().toLowerCase();
    const existingNames = designiations.value
        .filter(name => name !== null)
        .map(name => name.trim().toLowerCase());

    if (existingNames.includes(trimmedVal)) {
        formErrors.value.department_name = "Department name already exists.";
    } else {
        formErrors.value.department_name = "";
    }
});


const filterOnModal = reactive({
    applieddepartment_name: false,
    applieddepartment_code: false,

    department_name: "",
    department_code: ''


})

watch(
    businessUnit,
    (newVal) => {
        CreateDepartments.value.business_unit = newVal;

        if (newVal.length) {

            activitylog()
        }
    },
    { immediate: true }
);


const timeout = ref(null);

function inLineFiltersData(searchedData) {
    // Clear the previous timeout to prevent multiple API calls while typing
    clearTimeout(timeout.value);

    // Set a new timeout to delay the API call
    timeout.value = setTimeout(() => {
        // Initialize filters array
        filterObj.value.filters=[]

        // Loop through the table headers and build dynamic filters
        tableheaders.value.forEach((header) => {
            const key = header.td_key;

            if (searchedData[key]) {
                filterObj.value.filters.push([key, "like", `%${searchedData[key]}%`]);
            }
        });

        if (filterObj.value.filters.length) {
            activitylog(filterObj.value.filters);
        } else {
            activitylog();
        }
    }, 500); // Adjust debounce delay as needed (e.g., 500ms)
}


// Handle updating the current value
const PaginationUpdateValue = (itemsPerPage) => {
  filterObj.value.limitPageLength = itemsPerPage;
  filterObj.value.limit_start = 0;
//   if(filterObj.value.filters){
//     activitylog(filterObj.value.filters)
//   }
//   else{

      activitylog();
    // }
};
// Handle updating the limit start
const PaginationLimitStart = ([itemsPerPage, start]) => {
  filterObj.value.limitPageLength = itemsPerPage;
  filterObj.value.limit_start = start;
//   if(filterObj.value.filters){
//     activitylog(filterObj.value.filters)
//   }
//   else{

      activitylog();
    // }
};

function activitylog(data) {
    

    if (data) {
        filterObj.value.filters.push(...data)
    }

    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify(filterObj.value.filters),
        limit_page_length: filterObj.value.limitPageLength,
        limit_start: filterObj.value.limit_start,
        order_by: "`tabActivity Log`.`creation` desc"
    };
    const queryParamsCount = {
        fields: JSON.stringify(["count(name) AS total_count"]),
        limitPageLength: "None",
        filters: JSON.stringify(filterObj.value.filters),
    }
    axiosInstance.get(`${apis.resource}${doctypes.ActivityLog}`, { params: queryParamsCount })
        .then((res) => {
            // console.log(res.data[0].total_count);
            totalRecords.value = res.data[0].total_count

        })
        .catch((error) => {
            console.error("Error fetching ezyForms data:", error);
        });

    axiosInstance.get(apis.resource + doctypes.ActivityLog, { params: queryParams })
        .then((res) => {
            if (res.data) {
                const newData = res.data
                if (filterObj.value.limit_start === 0) {
                tableData.value = newData;
                }
                else {
                tableData.value = tableData.value.concat(newData);
                }
      }
        })
        .catch((error) => {
            console.error("Error fetching department data:", error);
        });
}


</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style lang="scss" scoped>
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

::v-deep(.multiselect__select) {
    position: absolute;
    width: 40px;
    height: 32px;
    right: 1px;
    /* top: 1px; */
    padding: 4px 8px;
    text-align: center;
    transition: transform 0.2s ease;
}

::v-deep(.multiselect) {
    height: 32px !important;
    min-height: 32px !important;
}

::v-deep(.multiselect__tags) {
    height: 32px !important;
    min-height: 32px !important;
    display: flex;
    align-items: center;
}

::v-deep(.multiselect__single) {
    font-size: 11px !important;
    color: #000;
}

::v-deep(.multiselect-wrapper),
::v-deep(.multiselect-search) {
    height: 32px !important;
    min-height: 32px !important;
    line-height: 32px !important;
    display: flex;
    align-items: center;
}

::v-deep(.multiselect-search) {
    height: 32px !important;
    min-height: 32px !important;
    display: flex;
    align-items: center;
}

::v-deep(.multiselect-wrapper) {
    height: 32px !important;
    min-height: 32px !important;
    line-height: 32px !important;
}

::v-deep(.multiselect-search) {
    position: absolute;
    width: 40px !important;
    height: 32px !important;
    right: 1px;

    padding: 4px 8px;
    text-align: center;
    transition: transform 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

::v-deep(.multiselect__element:hover) {
    background-color: #eeeeee !important;
}

::v-deep(.multiselect__element:hover .multiselect__option) {
    background-color: #eeeeee !important;
    color: #000 !important;
}

::v-deep(.multiselect__element:hover .multiselect__option--highlight) {
    background-color: #eeeeee !important;
    color: #000 !important;
}

/* Additional specific rule for `.multiselect__option` when hovered */
::v-deep(.multiselect__option:hover) {
    background-color: #eeeeee !important;
    color: #000 !important;
}

.custom-option {
    display: flex;
    align-items: center;
    gap: 5px;
}

.multiselect-option {
    font-size: 11px !important;
}

.multiselect {
    height: 30px !important;
}

.multiselect {
    margin: initial;
    font-size: 11px !important;
    border: 1px solid #e2e2e2 !important;
    height: 30px !important;

    .multiselect-wrapper {
        height: 30px !important;
    }

    .multiselect-dropdown {
        .multiselect-options {
            font-size: 11px;

            li.multiselect-option span {
                font-size: 11px !important;
            }

            li.multiselect-option .is-selected {
                background-color: grey !important;
                font-size: 11px;
            }
        }
    }
}

.multiselect__option span {
    font-size: 11px;
    /* Change this value to whatever size you need */
}

.multiselect .multiselect-option {
    font-size: 11px;
}

.multiselect .multiselect-wrapper {
    min-height: 30px !important;
}

.multiselect .multiselect--above {
    min-height: 30px !important;
}

.multiselect__tags {
    min-height: 30px !important;
    padding: 0px;
}

.multiselect .multiselect__tags {
    min-height: 30px !important;
    font-size: 11px !important;
}

.multiselect .multiselect__placeholder {
    font-size: 11px;
}

.multiselect .multiselect__single {
    font-size: 11px !important;
}

.multiselect__single {
    font-size: 11px !important;
}

.multiselect__single {
    font-size: 11px !important;

}

.multiselect .multiselect__tags .multiselect__placeholder {
    font-size: 11px;
}

::v-deep(.multiselect__placeholder) {
    color: #343434;
    display: inline-block;
    margin-bottom: 10px;
    padding-top: 2px;
    font-size: 10px !important;
}
</style>