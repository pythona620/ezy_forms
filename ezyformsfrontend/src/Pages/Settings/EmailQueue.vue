<template>
    <div>
        <div class="d-flex align-items-center justify-content-between py-3">
            <div>
                <h1 class="m-0 font-13">Email Queue</h1>
            </div>
            <!-- <div class="d-flex align-items-center gap-2">
                <div>
                    <button type="button" class="btn btn-dark  CreateDepartments " data-bs-toggle="modal"
                        data-bs-target="#CreateDesignationModal" @click="checkDesignation">
                        Create Designation
                    </button>
                </div>
            </div> -->

        </div>
        <!-- <FormFields labeltext="" class="my-1 w-25" tag="input" type="search" placeholder="Search Designation"
            name="Value" id="Value" v-model="filterObj.search" @input="EmailQueueData()" /> -->

        <div class="">
            <GlobalTable :tHeaders="tableheaders" :tData="tableData" isCheckbox="true" @cell-click="viewPreview"
                isAction="true" viewType="viewPdf" isFiltersoption="true" :field-mapping="fieldMapping"
                @updateFilters="inLineFiltersData" />

            <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords" @limitStart="PaginationLimitStart"
                @updateValue="PaginationUpdateValue" />
        </div>

        <div class="modal fade" id="CreateDesignationModal" data-bs-backdrop="static" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h6 class="modal-title">Email Queue</h6>
                        <button type="button" class="btn-close shadow-none" data-bs-dismiss="modal"
                            @click="resetDesignation" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3 sender-div">
                            <label class="font-13 pe-2 ms-1">Sender : </label>
                            <span type="text" class="font-13 m-0 text-secondary">{{ rowData.sender }}</span>
                        </div>

                        <table class="table table-bordered font-12">
                            <thead class="emailTable">
                                <tr>
                                    <th>Recipient</th>
                                    <th>Status</th>
                                </tr>
                            </thead>
                            <tbody class="font-13">
                                <tr v-for="(email, index) in emailsData" :key="index">
                                    <td>{{ email.recipient }}</td>
                                    <td>{{ email.status }}</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                    <!-- <div class="modal-footer">
                            <button type="button" class="btn btn-outline-secondary" @click="resetDesignation"
                                data-bs-dismiss="modal">Cancel</button>
                            <button type="button" class="btn btn-dark" @click="SubmitDesignation">Save</button>
                        </div> -->
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
import { onMounted, ref, computed, watch } from 'vue';
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import { toast } from 'vue3-toastify';

const totalRecords = ref(0);
const Designation = ref("");
const checkEmailQueueData = ref("");
const errorMessage = ref('');
const emailsData = ref("");
const rowData = ref("");
const tableData = ref([]);

const tableheaders = ref([
    { th: "message", td_key: "message" },
    { th: "Sender", td_key: "sender" },
    { th: "creation", td_key: "creation" },
    { th: "Status", td_key: "status" },
])

const businessUnit = computed(() => {
    return EzyBusinessUnit.value;
});

const filterObj = ref({
    limitPageLength: 20,
    limit_start: 0,
    filters:[]
});

onMounted(() => {
    EmailQueueData();
})

function resetDesignation() {
    Designation.value = '';
    errorMessage.value = '';
}

const createDesignation = ref({
    ezy_business_unit: "",
});

const fieldMapping = ref({
    message: { type: "input" },
    sender: { type: "input" },
    creation:{type:"date"},
    status: {
    type: "select",
    options: ["Sent","Not Sent","Partially Sent","Sending","Error","Expired"],
  },
});
const timeout = ref(null);

function inLineFiltersData(searchedData) {
    // const filters = [];

  clearTimeout(timeout.value); // Clear previous timeout

  timeout.value = setTimeout(() => {
    // Initialize filters array
    filterObj.value.filters = [];

    // Loop through the table headers and build dynamic filters
    tableheaders.value.forEach((header) => {
      const key = header.td_key;

      if (searchedData[key]) {
        filterObj.value.filters.push([key, "like", `%${searchedData[key]}%`]);

      }
    });

    // Call receivedForMe with or without filters
    if (filterObj.value.filters.length) {
      filterObj.value.limit_start = 0;
      EmailQueueData(filterObj.value.filters);
    } else {
        EmailQueueData();
    }
},500)
    
}

const PaginationUpdateValue = (itemsPerPage) => {
    filterObj.value.limitPageLength = itemsPerPage;
    filterObj.value.limit_start = 0;
    EmailQueueData();
};

const PaginationLimitStart = ([itemsPerPage, start]) => {
    filterObj.value.limitPageLength = itemsPerPage;
    filterObj.value.limit_start = start;
    EmailQueueData();
};

watch(
    businessUnit,
    (newVal) => {
        createDesignation.value.ezy_business_unit = newVal;
    },
    { immediate: true }
);

function EmailQueueData() {
    // const filters = [];
    // if (filterObj.value.search.trim()) {
    //     filters.push(["name", "like", `%${filterObj.value.search}%`]);
    // }

    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify(filterObj.value.filters),
        limit_page_length: filterObj.value.limitPageLength,
        limit_start: filterObj.value.limit_start,
        order_by: `\`tab${doctypes.emailQueue}\`.\`creation\` desc`,
    };
    const queryParamsCount = {
        fields: JSON.stringify(["count(name) AS total_count"]),
        limitPageLength: "None",
        filters: JSON.stringify(filterObj.value.filters),
    }
    axiosInstance.get(`${apis.resource}${doctypes.emailQueue}`, { params: queryParamsCount })
        .then((res) => {

            totalRecords.value = res.data[0].total_count

        })
        .catch((error) => {
            console.error("Error fetching ezyForms data:", error);
        });

    axiosInstance.get(apis.resource + doctypes.emailQueue, { params: queryParams })
        .then((res) => {
            if (res.data) {
                const newData = res.data.map(item => {
                    // Extract Subject from the message
                    const subjectMatch = item.message.match(/Subject:\s*(.*)/);
                    const subject = subjectMatch ? subjectMatch[1].trim() : '';

                    // Replace message with only subject
                    return {
                        ...item,
                        message: subject
                    }
                });

                if (filterObj.value.limit_start === 0) {
                    tableData.value = newData;
                } else {
                    tableData.value = tableData.value.concat(newData);
                }
            }
        })
        .catch((error) => {
            console.error("Error fetching designations data:", error);
        });

}

function viewPreview(data, type) {
    rowData.value = data;
    axiosInstance
        .get(`${apis.resource}${doctypes.emailQueue}/${data.name}`)
        .then((res) => {
            if (res.data) {
                emailsData.value = res.data.recipients;
                console.log("emailsData.value", emailsData.value);
                const modal = new bootstrap.Modal(document.getElementById('CreateDesignationModal'), {});
                modal.show();
            }
        })
        .catch((error) => {
            console.error("Error fetching system settings:", error);
        });
}





function checkDesignation() {
    const queryParams = {
        fields: JSON.stringify(["role"]),
        limit_page_length: "none",
        order_by: "`tabWF Roles`.`creation` desc"
    };
    axiosInstance.get(apis.resource + doctypes.designations, { params: queryParams })
        .then((res) => {
            if (res.data) {
                checkEmailQueueData.value = res.data;
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
        checkEmailQueueData.value.some(
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
        }
        axiosInstance
            .post(apis.resource + doctypes.roles, payload)
            .then((response) => {
                if (response) {
                    //console.log(response);
                    EmailQueueData();
                    resetDesignation();
                    toast.success("Designation Created Successfully", { autoClose: 1000 });
                    const modal = bootstrap.Modal.getInstance(document.getElementById('CreateDesignationModal'));
                    modal.hide();
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

.emailTable th {
    background-color: #f2f2f2 !important;
    color: #736d6d;
}

.emailTable td {
    font-size: 12px;
}

.sender-div {
    background-color: #f2f2f2;
    color: #736d6d;
    padding: 3px;
    border-radius: 5px;
}
</style>