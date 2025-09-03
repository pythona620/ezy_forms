<template>
    <div>
        <div class="d-flex justify-content-between align-items-center  py-2">
            <div>
                <h1 class="mt-3 font-13">
                    Audit Log
                </h1>
            </div>
            <!-- <div class="d-flex gap-2 align-items-center">
                <div class="d-flex align-items-center ">
                    <button type="button" class="btn btn-dark buttoncomp CreateDepartments d-flex align-items-center " @click="CreateDeprtModal"
                        data-bs-toggle="modal" data-bs-target="#createDepartments">
                        Create Department
                    </button>
                </div>
            </div> -->
        </div>
        <div class="mt-2">
            <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction="true" viewType="viewPdf"
                @cell-click="viewPreview" isCheckbox="true" isFiltersoption="true" :field-mapping="fieldMapping"
                @updateFilters="inLineFiltersData" />
            <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords"
                @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
        </div>

        <div class="offcanvas offcanvas-end" data-bs-backdrop="static" tabindex="-1" id="staticBackdrop"
            aria-labelledby="staticBackdropLabel">
            <div class="offcanvas-header">
                <h5 class="offcanvas-title" id="staticBackdropLabel" :title="viewLogs.docname">{{ viewLogs.docname }}
                </h5>
                <button type="button" class="btn-close shadow-none" data-bs-dismiss="offcanvas"
                    aria-label="Close"></button>
            </div>

            <div class="offcanvas-body p-3">
                <!-- Added Logs -->
                <div v-if="addedLogs.length" class="mb-2">
                    <h6 class="text-muted fw-bold mb-3">➕ Added</h6>
                    <ul class="ps-0 list-unstyled">
                        <li v-for="(item, index) in addedLogs" :key="'added-' + index" class="px-3 rounded"
                            style="background-color: #f9fafb; color: #333;">
                            <!-- Field Name -->
                            <p class="m-0 mb-1" style="font-weight: 500; color: #4b5563;">
                                {{ item[0] }} added with:
                            </p>

                            <!-- Added Values -->
                            <div v-if="typeof item[1] === 'object' && item[1] !== null" class="ps-2">
                                <div v-for="(val, key) in item[1]" :key="key" class="mb-1"
                                    style="font-size: 13px; color: #6b7280;">
                                    <span class="text-muted">{{ key }}:</span>
                                    <span
                                        style="background-color: #e0e7ff; padding: 2px 6px; border-radius: 4px; color: #4338ca; margin-left: 5px; word-wrap: break-word; ">
                                        {{ val }}
                                    </span>
                                </div>
                            </div>

                            <div v-else style="font-size: 13px; color: #6b7280;">
                                <span>Value:</span>
                                <span style="background-color: #dbeafe; padding: 2px 6px; border-radius: 4px; color: #1e3a8a; margin-left: 5px; word-wrap: break-word; ">
                                    {{ item[1] }}
                                </span>
                            </div>
                        </li>
                    </ul>
                </div>

                <!-- Changed Logs -->
                <div v-if="changedLogs.length">
                    <h6 class="text-muted fw-bold mb-3">🔄 Changes</h6>
                    <ul class="list-unstyled ps-0">
                        <li v-for="(item, index) in changedLogs" :key="'changed-' + index"
                            class="mb-2 px-3 py-2 rounded" style="background-color: #f9fafb; color: #333;">
                            <!-- Field Name -->
                            <p class="m-0 mb-1" style="font-weight: 500; font-size:12px; color: #4b5563;">
                               {{ item[0].replace(/_/g, ' ') }}
                            </p>

                            <!-- Change Summary -->
                            <p class="m-0" style="font-size: 11px; color: #6b7280; line-height: 20px;">
                                Changed from
                                <span style="background-color: #e0e7ff; padding: 2px 6px; border-radius: 4px; color: #4338ca; word-wrap: break-word;">
                                    {{ item[1] }}
                                </span>
                                to
                                <span style="background-color: #d1fae5; padding: 2px 6px; border-radius: 4px; color: #065f46;">
                                    {{ item[2] }}
                                </span>
                            </p>
                        </li>
                    </ul>
                </div>

                <!-- No data -->
                <div v-if="!addedLogs.length && !changedLogs.length" class="text-center text-muted mt-4">
                    <i class="bi bi-info-circle me-2"></i>No added or changed data.
                </div>
            </div>
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
const timeout = ref(null);
const viewLogs = ref([])


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
    { th: "Document Name", td_key: "docname" },
    { th: "Doctype Name", td_key: "ref_doctype" },
    { th: "Modified By", td_key: "modified_by" },
    { th: "Modified Date", td_key: "modified" },
    // { th: "Property Name", td_key: "property" },
    // { th: "Old Value", td_key: "old_value" },
    // { th: "New Value", td_key: "new_value" },
])

const fieldMapping = ref({
    docname: { type: "input" },
    ref_doctype: { type: "input" },
    modified_by: { type: "input" },
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
        // console.log("teDepartments",CreateDepartments.value.business_unit);
        if (newVal.length) {

            activityData()
        }
    },
    { immediate: true }
);

function inLineFiltersData(searchedData) {
    // Clear the previous timeout to prevent multiple API calls while typing
    clearTimeout(timeout.value);

    // Set a new timeout to delay the API call
    timeout.value = setTimeout(() => {
        // Initialize filters array
        filterObj.value.filters = []

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

const activityDoctypes=ref([])

function activityData() {
    const docName="Ezy Dynamic Activate Log"
    const queryParams = {
        fields: JSON.stringify(["activate_log"]),
        limit_page_length: "none"
    };

    axiosInstance
        .get(`${apis.resource}${doctypes.EzyActivityLog}/${encodeURIComponent(docName)}`, { params: queryParams })
        .then((res) => {
            if (res.data) {
                activityDoctypes.value = res.data.activate_log;
                activitylog();
            }
        })
        .catch((error) => {
            console.error("Error fetching department data:", error);
        });
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
    filterObj.value.filters.push(["ref_doctype", "in", activityDoctypes.value]);

    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify(filterObj.value.filters),
        limit_page_length: filterObj.value.limitPageLength,
        limit_start: filterObj.value.limit_start,
        order_by: "`tabVersion`.`creation` desc"
    };
    const queryParamsCount = {
        fields: JSON.stringify(["count(name) AS total_count"]),
        limitPageLength: "None",
        filters: JSON.stringify(filterObj.value.filters),
    }
    axiosInstance.get(`${apis.resource}${doctypes.version}`, { params: queryParamsCount })
        .then((res) => {
            // console.log(res.data[0].total_count);
            totalRecords.value = res.data[0].total_count

        })
        .catch((error) => {
            console.error("Error fetching ezyForms data:", error);
        });

    axiosInstance.get(apis.resource + doctypes.version, { params: queryParams })
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


function viewPreview(rowData) {
    viewLogs.value = rowData;

    const parsedData = JSON.parse(rowData.data);

    // console.log("Changed array:", parsedData);

    parsedData.changed.forEach(change => {
        const [fieldName, oldValue, newValue] = change;
        // console.log(`Field Name = ${fieldName}, Old Value = ${oldValue}, New Value = ${newValue}`);
    });

    const offcanvasElement = document.getElementById('staticBackdrop');
    const offcanvas = new bootstrap.Offcanvas(offcanvasElement);
    offcanvas.show();
}

const parsedLogData = computed(() => {
  try {
    return viewLogs.value?.data ? JSON.parse(viewLogs.value.data) : {};
  } catch (e) {
    return {};
  }
});

const addedLogs = computed(() => parsedLogData.value.added || []);
const changedLogs = computed(() => parsedLogData.value.changed || []);




</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style lang="scss" scoped>
.global-table th {
    background-color: #f2f2f2 !important;
    text-align: left;
    color: #999999;
    font-size: 12px;
}
.offcanvas-title{
    overflow: hidden;
    text-overflow: ellipsis;
    width: 100%;
}
.offcanvas-div{
    background-color: #f2f2f2;
    padding: 10px;
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