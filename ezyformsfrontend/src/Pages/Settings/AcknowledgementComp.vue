<template>
    <div>
        <div class="d-flex justify-content-between align-items-center  py-2">
            <div>
                <h1 class="mt-3 font-13">
                    Acknowledgement
                </h1>
            </div>
            <div class="d-flex gap-2 align-items-center">
                <div class="d-flex align-items-center ">
                    <button type="button" class="btn btn-dark CreateDepartments " data-bs-toggle="modal"
                        data-bs-target="#AcknowledgementModal" @click="openCreateModal">
                        Create Acknowledgement
                    </button>
                </div>

            </div>
        </div>
        <div class="mt-2">
            <GlobalTable :tHeaders="tableheaders" :tData="tableData" enableDisable="true" isAction="true"
                viewType="viewPdf" isFiltersoption="true" @cell-click="viewPreview" :field-mapping="fieldMapping"
                @updateFilters="inLineFiltersData" @toggle-click="toggleFunction" />
            <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords"
                @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
        </div>

        <!-- Modal -->
        <div class="modal fade" id="AcknowledgementModal" data-bs-backdrop="static" tabindex="-1"
            aria-labelledby="AcknowledgementLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="AcknowledgementLabel">Acknowledgement</h5>
                        <button @click="close" type="button" class="btn-close" data-bs-dismiss="modal"
                            aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <label for="password" class="font-13">Acknowledgement Name</label><br />
                        <FormFields tag="input" type="text" name="acknowledgementName" id="acknowledgementName"
                            placeholder="Enter Name" class="mb-4" v-model.trim="acknowledgementName" />

                        <label for="password" class="font-13">Acknowledgement</label><br />
                        <QuillEditor v-model:content="content" contentType="html" theme="snow" style="height: 300px" />
                    </div>
                    <div class="modal-footer">
                        <button @click="close" type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">
                            Close
                        </button>
                        <button v-if="isSubmitBtn" type="button" class="btn btn-dark" :disabled="!acknowledgementName" @click="createAcknowledgement">
                            Submit
                        </button>

                        <button v-else type="button" class="btn btn-dark" :disabled="!acknowledgementName" @click="UpdateAcknowledgement">
                            Update
                        </button>
                    </div>
                </div>
            </div>
        </div>


        <div class="modal fade" id="EmployeeToggleModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Confirm Acknowledgement Status</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        Are you sure you want to
                        <span class="fw-bold">{{ empActionText }}</span>
                        "<span class="fw-semibold">{{ selectedEmpRow.name }}</span>"?
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-dark" data-bs-dismiss="modal"
                            @click="confirmEmployeeToggle">Yes, Proceed</button>
                    </div>
                </div>
            </div>
        </div>


    </div>
</template>
<script setup>
import GlobalTable from '../../Components/GlobalTable.vue';
import FormFields from '../../Components/FormFields.vue';
import PaginationComp from '../../Components/PaginationComp.vue'
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from '../../shared/apiurls';
import { onMounted, ref, computed, watch, reactive } from 'vue';
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import "@vueform/multiselect/themes/default.css";
import { QuillEditor } from '@vueup/vue-quill';
// Quill styles (needed for toolbar, fonts, etc.)
import '@vueup/vue-quill/dist/vue-quill.snow.css'

const totalRecords = ref(0);
const departmenCodeData = ref([]);
const tableData = ref([]);
const categoriesDataEdit = ref({ ezy_departments_items: [] });
const designiations = ref([]);

const acknowledgementName = ref("");


const content = ref('')  // Reactive content binding
const isSubmitBtn=ref(false)

// Function to open Modal for Create
function openCreateModal() {
  isSubmitBtn.value = true;  // Show Submit button
  acknowledgementName.value = "";  // Reset form
  content.value = "";
}

function createAcknowledgement() {
    const dataObj = {
        acknowledgement: content.value,
        naming_series: acknowledgementName.value,
        doctype:doctypes.acknowledgement,
    }
    // console.log(dataObj, "------------------");
    axiosInstance.post(apis.DataUpdate, dataObj)
        .then((res) => {
            if (res.message.data) {
                // console.log("res", res.data);
                const modal = bootstrap.Modal.getInstance(
                    document.getElementById("AcknowledgementModal")
                );
                modal.hide();
                isSubmitBtn.value = false;
                activitylog()
            }
        })
}

function UpdateAcknowledgement(){
    const updatedData = {
        acknowledgement: content.value,
        naming_series: acknowledgementName.value,
        doctype:doctypes.acknowledgement,
        name:acknowledgementData.value.name,
      };
     axiosInstance
        .put(`${apis.DataUpdate}/${acknowledgementData.value.name}`, updatedData)
        .then((response) => {
            if (response.message.success==true) {
                toast.success(`acknowledgement Updated successfully`, { autoClose: 700 });
                activitylog()
                const modal = bootstrap.Modal.getInstance(
                    document.getElementById("AcknowledgementModal")
                );
                modal.hide();
            }
            if (response.message.success==false) {  
                toast.error(response.message.message)
            }

        })
        .catch((error) => {
            console.error("Error updating toggle:", error);
        });
}

const acknowledgementData=ref("")

function close() {
    acknowledgementName.value = '';  // use the correct key from your data
    content.value = '';
    isSubmitBtn.value = false;  // Show Submit button
}

function viewPreview(data) {
    acknowledgementName.value = data.naming_series || '';  // use the correct key from your data
    content.value = data.acknowledgement || '';
    acknowledgementData.value=data;


    // console.log("data",data);
    // console.log("acknowledgementName.value",acknowledgementName.value);
    // console.log("content.value",content.value);

    const modal = new bootstrap.Modal(document.getElementById('AcknowledgementModal'));
    modal.show();
}
const selectedEmpRow = ref({});
const empActionText = ref('');

function toggleFunction(rowData) {
    selectedEmpRow.value = rowData;
    const isEnabled = rowData.enable === 0;
    // empActionText.value = isEnabled ? 'Disable' : 'Enable';
    empActionText.value = isEnabled ? 'Enable' : 'Disable';

    const modal = new bootstrap.Modal(document.getElementById('EmployeeToggleModal'));
    modal.show();
}

 function confirmEmployeeToggle() {

    const isEnabled = selectedEmpRow.value.enable === '1' || selectedEmpRow.value.enable === 1;
    selectedEmpRow.value.enable = isEnabled ? 0 : 1;

    axiosInstance
        .put(`${apis.resource}${doctypes.acknowledgement}/${selectedEmpRow.value.name}`, selectedEmpRow.value)
        .then((response) => {
            if (response.data) {
                toast.success(`acknowledgement ${empActionText.value}d successfully`, { autoClose: 700 });
                activitylog()
            }

        })
        .catch((error) => {
            console.error("Error updating toggle:", error);
        });
}



const businessUnit = computed(() => {
    return EzyBusinessUnit.value;
});


const filterObj = ref({
    limitPageLength: 20,
    limit_start: 0,
    filters: []
});
const formErrors = ref({
    department_code: "",
    department_name: ""
});


const tableheaders = ref([
    { th: "Name", td_key: "name" },
    { th: "Status", td_key: "activate" },

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


// Handle updating the current value
const PaginationUpdateValue = (itemsPerPage) => {
    filterObj.value.limitPageLength = itemsPerPage;
    filterObj.value.limit_start = 0;
    activitylog();
};

// Handle updating the limit start
const PaginationLimitStart = ([itemsPerPage, start]) => {
    filterObj.value.limitPageLength = itemsPerPage;
    filterObj.value.limit_start = start;
    activitylog();
};

function activitylog(data) {
    if (data) {
        filterObj.value.filters.push(...data)
    }

    const queryParams = {
        fields: JSON.stringify(["name","acknowledgement","naming_series","enable"]),
        filters: JSON.stringify(filterObj.value.filters),
        limit_page_length: filterObj.value.limitPageLength,
        limit_start: filterObj.value.limit_start,
        doctype:doctypes.acknowledgement,
        order_by: "`tabAcknowledgement`.`creation` desc"
    };

    axiosInstance.get(apis.GetDoctypeData, { params: queryParams })
        .then((res) => {
            if (res) {
                const newData = res.message.data
                totalRecords.value=res.message.total_count;
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
    font-size: 13px;
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