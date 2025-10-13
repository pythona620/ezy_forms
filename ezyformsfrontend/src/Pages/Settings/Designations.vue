<template>
    <div>
        <div class="d-flex align-items-center justify-content-between py-2">
            <div>
                <h1 class="m-0 font-13">Designations</h1>
            </div>
            <div class="d-flex align-items-center gap-2">
                <div>
                    <!-- <FormFields labeltext="" class="my-1" tag="input" type="search" placeholder="Search Designation"
                        name="Value" id="Value" v-model="filterObj.search" @input="designationData()" /> -->

                    <button type="button" class="btn btn-dark  CreateDepartments " data-bs-toggle="modal"
                        data-bs-target="#CreateDesignationModal" @click="checkDesignation">
                        Create Designation
                    </button>
                </div>
            </div>
        </div>
        <FormFields labeltext="" class="my-1 w-25" tag="input" type="search" placeholder="Search Designation"
            name="Value" id="Value" v-model="filterObj.search" @input="designationData()" />

        <div class="mt-2">
            <GlobalTable :tHeaders="tableheaders" :tData="tableData" isCheckbox="true"  />
            <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords" :items-per-page="filterObj.limitPageLength"
                @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
        </div>

        <div class="modal fade" id="CreateDesignationModal" data-bs-backdrop="static" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Create Designation</h5>
                        <button type="button" class="btn-close shadow-none" data-bs-dismiss="modal" @click="resetDesignation"
                            aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <label class="font-12 fw-bold">Designation<span class="text-danger ps-1">*</span></label>
                        <input type="text" class="form-control shadow-none font-12" v-model.trim="Designation"
                            @input="validateDesignation" :class="{ 'is-invalid': errorMessage }"
                            placeholder="Enter Designation" />

                        <div v-if="errorMessage" class="text-danger mt-1 font-11">{{ errorMessage }}</div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary" @click="resetDesignation"
                            data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-dark" :disabled="errorMessage || !Designation"
                            @click="SubmitDesignation">Save</button>
                    </div>
                </div>
            </div>
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
import { showError, showSuccess } from '../../shared/services/toast';

const businessUnit = computed(() => {
    return EzyBusinessUnit.value;
});
onMounted(() => {
    designationData();

})
const totalRecords = ref(0);
const Designation = ref("");
const checkDesignationData = ref("");
const errorMessage = ref('');

const tableData = ref([]);
const tableheaders = ref([
    { th: "Designation", td_key: "role" },
])

function resetDesignation() {
    Designation.value = '';
    errorMessage.value = '';
}

const createDesignation = ref({
    ezy_business_unit: "",
});
const filterObj = ref({
    limitPageLength: 20,
    limit_start: 0,
    search: ""
});

const PaginationUpdateValue = (itemsPerPage) => {
    filterObj.value.limitPageLength = itemsPerPage;
    filterObj.value.limit_start = 0;
    designationData();
};

const PaginationLimitStart = ([itemsPerPage, start]) => {
    filterObj.value.limitPageLength = itemsPerPage;
    filterObj.value.limit_start = start;
    designationData();
};
watch(
    businessUnit,
    (newVal) => {
        createDesignation.value.ezy_business_unit = newVal;
        
    },
    { immediate: true }
);

let debounceTimeout = null;

function designationData() {
  // Clear previous timeout if user is still typing
  if (debounceTimeout) clearTimeout(debounceTimeout);

  // Set a new timeout
  debounceTimeout = setTimeout(() => {
    const filters = [];
    if (filterObj.value.search.trim()) {
      filters.push(["name", "like", `%${filterObj.value.search}%`]);
    }

    const queryParams = {
        fields: JSON.stringify(["role"]),
        filters: JSON.stringify(filters),
        limit_page_length: filterObj.value.limitPageLength,
        limit_start: filterObj.value.limit_start,
        doctype:doctypes.designations,
        order_by: "`tabWF Roles`.`creation` desc"
    };

        axiosInstance.get(apis.GetDoctypeData, { params: queryParams })
        .then((res) => {
            if (res.message.data) {
                const newData = res.message.data;
                totalRecords.value=res.message.total_count;
                if (filterObj.value.limit_start === 0) {
                    tableData.value = newData;
                } else {
                    tableData.value = tableData.value.concat(newData)
                }

            }
        })
        .catch((error) => {
            console.error("Error fetching designations data:", error);
        });
    }, 500); // Adjust the delay as needed (300ms in this case)
}
function checkDesignation() {
    const queryParams = {
        fields: JSON.stringify(["role"]),
        limit_page_length: "none",
        order_by: "`tabWF Roles`.`creation` desc",
        doctype:doctypes.designations,
    };
    axiosInstance.get(apis.GetDoctypeData, { params: queryParams })
        .then((res) => {
            if (res.message.data) {
                checkDesignationData.value = res.message.data;

            }
        })
        .catch((error) => {
            console.error("Error fetching designations data:", error);
        });
}

function validateDesignation() {
  const invalidCharRegex = /[^a-zA-Z .]/;

  if (!Designation.value.trim()) {
    errorMessage.value = 'Designation is required';
  } else if (invalidCharRegex.test(Designation.value)) {
    errorMessage.value = 'Only letters, spaces, and dot (.) are allowed';
  } else if (
    checkDesignationData.value.some(
      item => item.role?.toLowerCase() === Designation.value.trim().toLowerCase()
    )
  ) {
    errorMessage.value = 'This designation already exists';
  } else {
    errorMessage.value = '';
  }
}

function SubmitDesignation() {
    if (!errorMessage.value && Designation.value.trim()) {
        const payload = {
            role_name: Designation.value.trim(),
            doctype:doctypes.roles,
        }
        axiosInstance
            .post(apis.DataUpdate, payload)
            .then((response) => {
                if (response.message.success==true) {
                    designationData();
                    resetDesignation();
                    showSuccess("Designation Created Successfully");
                    const modal = bootstrap.Modal.getInstance(document.getElementById('CreateDesignationModal'));
                    modal.hide();
                } else {
                    // Parse the server messages
                    const serverMessages = JSON.parse(response._server_messages);
                    const parsedMessage = JSON.parse(serverMessages[0]);
                    // Remove HTML tags from message
                    const cleanMessage = parsedMessage.message.replace(/<[^>]*>/g, '');
                    showError(cleanMessage, { autoClose: 2000 });
                }
            })
            .catch((err) => {
                console.error('Error creating role:', err)
            })
    }
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
    padding: 8px 20px;
}
</style>