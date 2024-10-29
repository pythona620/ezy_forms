<template>
    <div>
        <div class="d-flex justify-content-between align-items-center ">
            <div>
                <h1 class="m-0 font-13">
                    Designations
                </h1>
                <!-- <p class="m-0 font-11 pt-1">
                374 users
            </p> -->
            </div>
            <div class="d-flex gap-2 align-items-center">
                <div class="d-flex">
                    <div>
                        <!-- <FormFields labeltext="" class="mb-3" tag="input" type="search" placeholder="Search File Name"
                        name="Value" id="Value" v-model="filterObj.search" /> -->
                    </div>
                    <div>
                        <button type="button" class=" filterbtn d-flex align-items-center " data-bs-toggle="modal"
                            data-bs-target="#fileterModal">
                            <span> <i class="ri-filter-2-line"></i></span>
                        </button>

                    </div>
                </div>
                <div class="modal fade" id="fileterModal" tabindex="-1" aria-labelledby="fileterModalLabel"
                    aria-hidden="true">
                    <div class="modal-dialog modal-xl">
                        <div class="modal-content">

                            <div class="modal-body">
                                <div class="row">
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="Requested">Requested By:</label>
                                        <FormFields class="mb-3" tag="input" type="search" name="Requested"
                                            id="Requested" placeholder="Search" v-model="filterOnModal.Requested_id" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1 fw-medium" for="dept">Requested Dept:</label>
                                        <FormFields tag="select" placeholder="Select Department" class="mb-3"
                                            name="dept" v-model="filterOnModal.Requested_dept" id="dept"
                                            :Required="false"
                                            :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="dept">Owner OF Form:</label>
                                        <FormFields tag="select" placeholder="Select Department" class="mb-3"
                                            name="dept" v-model="filterOnModal.Owner_OF_Form" id="dept"
                                            :Required="false"
                                            :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="dept">Form Category:</label>
                                        <FormFields tag="select" placeholder="Select Department" class="mb-3"
                                            name="dept" v-model="filterOnModal.Form_Category" id="dept"
                                            :Required="false"
                                            :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="Requested">Form Name:</label>
                                        <FormFields class="mb-3" tag="input" type="search" name="Requested"
                                            id="Requested" placeholder="Search"
                                            v-model="filterOnModal.department_name" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="Requested">Requested Period:</label>
                                        <FormFields class="mb-3" tag="input" type="date" name="Requested" id="Requested"
                                            placeholder="Jan-2024-Dec-2024" v-model="filterOnModal.Requested_Period" />
                                    </div>
                                    <div class="col-3">
                                        <FormFields tag="radio" :options="radioOptions" name="exampleRadio"
                                            id="exampleRadio" v-model="filterOnModal.Approval_status"
                                            labeltext="Approval Status" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="Requested">Requested Id:</label>
                                        <FormFields class="mb-3" tag="input" type="search" name="Requested"
                                            id="Requested" placeholder="Search" v-model="filterOnModal.RequestedId" />
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="cancelfilter border-0 text-nowrap font-10 "
                                    @click="resetFilters" data-bs-dismiss="modal"><span
                                        class="font-14 me-1">x</span>Cancel
                                    Filter</button>

                                <button type="button"
                                    class="applyfilter text-nowrap border-0 bg-primary text-white font-10 d-flex justify-content-center align-items-center"
                                    data-bs-dismiss="modal" @click="applyFilters"><span class="font-16 me-1"><i
                                            class="bi bi-check2 "></i></span>
                                    Apply
                                    Filter</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="d-flex align-items-center ">
                    <button type="button" class="btn btn-dark buttoncomp CreateDepartments d-flex align-items-center "
                        data-bs-toggle="modal" data-bs-target="#createDepartments">
                        Create Designations
                    </button>
                </div>
                <div class="modal fade" id="createDepartments" tabindex="-1" aria-labelledby="createDepartmentsLabel"
                    aria-hidden="true">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">

                            <div class="modal-body">
                                <label class="font-13 ps-1" for="designation_name">Designation Name</label>
                                <FormFields class="mb-3" tag="input" type="text" name="designation_name"
                                    id="designation_name" placeholder="Enter department code"
                                    v-model="createDesignation.designation_name" />
                                <label class="font-13 ps-1" for="business_unit">Business Unit</label>
                                <FormFields tag="select" placeholder="" class="mb-3" name="business_unit"
                                    id="business_unit" v-model="createDesignation.ezy_business_unit"
                                    :options="EzyFormsCompanys" />
                                <label class="font-13 ps-1 fw-medium" for="dept">Departments</label>
                                <FormFields tag="select" placeholder="Select Department" class="mb-3" name="dept"
                                    v-model="createDesignation.ezy_departments" id="dept" :Required="false"
                                    :options="departmentsList" />
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="cancelfilter border-1 text-nowrap font-10 "
                                    @click="cancelCreate" data-bs-dismiss="modal">Cancel
                                </button>

                                <button type="button"
                                    class="applyfilter btn btn-dark text-nowrap font-10 d-flex justify-content-center align-items-center"
                                    data-bs-dismiss="modal" @click="createDesig"><span class="font-16 me-1"><i
                                            class="bi bi-check2 "></i></span>
                                    Create Department</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="mt-2">
            <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction='true' :actions="actions"
                actionType="dropdown" isCheckbox="true" />
        </div>
    </div>
</template>
<script setup>
import FormFields from '../../Components/FormFields.vue';
import ButtonComp from '../../Components/ButtonComp.vue';
import GlobalTable from '../../Components/GlobalTable.vue';
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from '../../shared/apiurls';
import { onMounted, ref, computed, watch } from 'vue';
import { EzyBusinessUnit } from "../../shared/services/business_unit";
const businessUnit = computed(() => {
    return EzyBusinessUnit.value;
});
onMounted(() => {
    designationData();
    ezyForms();
    deptData()
})
const tableData = ref([]);
const radioOptions = ref(["yes", "no"])
const EzyFormsCompanys = ref([]);
const newCategory = ref("");
const editIndex = ref(null);
const editCategory = ref("");
const departmentsList = ref([])

const actions = ref(
    [
        { name: 'View Categories', icon: 'fa-solid fa-eye' },

    ]
)

const tableheaders = ref([
    { th: "Designations Name", td_key: "designation_name" },
    { th: "Departments", td_key: "ezy_departments" },
    { th: "Business Unit", td_key: "ezy_business_unit" },
])
const createDesignation = ref({
    designation_name: "",
    ezy_business_unit: "",
    ezy_departments: ""
});
const filterObj = ref({
    limitPageLength: 'None',
    limitstart: 0
});
const filterOnModal = ref({
    Requested_id: "",
    Requested_dept: "",
    Owner_OF_Form: "",
    Form_Category: "",
    department_name: "",
    Requested_Period: "",
    Approval_status: "",
    RequestedId: ""

})
watch(
    businessUnit,
    (newVal) => {
        createDesignation.value.ezy_business_unit = newVal;

        if (newVal) {
            console.log(newVal, "new value of business unit");

        }
    },
    { immediate: true }
);


function applyFilters() {
    designationData(); // Calls designationData to send filters
}

function resetFilters() {
    filterOnModal.value = {
        Requested_id: "",
        Requested_dept: "",
        Owner_OF_Form: "",
        Form_Category: "",
        Form_Name: "",
        Requested_Period: "",
        Approval_status: "",
        RequestedId: ""
    };
    designationData()
}

function designationData() {
    const filters = [];
    if (filterOnModal.value.Requested_id) {
        filters.push(["Requested_id", "like", `%${filterOnModal.value.Requested_id}%`]);
    }
    if (filterOnModal.value.Requested_dept) {
        filters.push(["Requested_dept", "like", `%${filterOnModal.value.Requested_dept}%`]);
    }
    if (filterOnModal.value.Owner_OF_Form) {
        filters.push(["Owner_OF_Form", "like", `%${filterOnModal.value.Owner_OF_Form}%`]);
    }
    if (filterOnModal.value.Form_Category) {
        filters.push(["Form_Category", "like", `%${filterOnModal.value.Form_Category}%`]);
    }
    if (filterOnModal.value.department_name) {
        filters.push(["designation_name", "like", `%${filterOnModal.value.department_name}%`]);
    }
    if (filterOnModal.value.Requested_Period) {
        filters.push(["Requested_Period", "like", `%${filterOnModal.value.Requested_Period}%`]);
    }
    if (filterOnModal.value.Approval_status) {
        filters.push(["Approval_status", "like", `%${filterOnModal.value.Approval_status}%`]);
    }
    if (filterOnModal.value.RequestedId) {
        filters.push(["RequestedId", "like", `%${filterOnModal.value.RequestedId}%`]);
    }

    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify(filters),
        limit_page_length: filterObj.value.limitPageLength,
        limitstart: filterObj.value.limitstart,
        order_by: "`tabEzy Departments`.`creation` desc"
    };

    axiosInstance.get(apis.resource + doctypes.designations, { params: queryParams })
        .then((res) => {
            if (res.data) {
                console.log(res.data, "Fetched departments");
                tableData.value = res.data;
            }
        })
        .catch((error) => {
            console.error("Error fetching department data:", error);
        });
}

function deptData() {
    const queryParams = {
        fields: JSON.stringify(["*"]),
        limit_page_length: filterObj.value.limitPageLength,
        limitstart: filterObj.value.limitstart,
    };

    axiosInstance.get(apis.resource + doctypes.departments, { params: queryParams })
        .then((res) => {
            if (res.data) {
                console.log(res.data, "Fetched departments");

                departmentsList.value = res.data.map((department) => department.name);
                console.log(departmentsList.value, "000000000000000");
            }
        })
        .catch((error) => {
            console.error("Error fetching department data:", error);
        });
}

const ezyForms = () => {
    const queryParams = {
        fields: JSON.stringify(["*"]),
    };

    axiosInstance.get(apis.resource + doctypes.wfSettingEzyForms, {
        params: queryParams,
    }).then((res) => {
        if (res?.data?.length) {
            EzyFormsCompanys.value = res.data.map((company) => company.bu_code);
        }
    }).catch((error) => {
        console.error("Error fetching ezyForms data:", error);
    });
};
function cancelCreate() {
    createDesignation.value = {
        designation_name: "",
        ezy_business_unit: "",
        ezy_departments: ""
    }
}
function createDesig() {
    const dataObj = {
        ...createDesignation.value,
        "doctype": doctypes.designations
    }
    console.log(dataObj, "------------------");
    // axiosInstance.post(apis.resource + doctypes.designations, dataObj).then((res) => {
    //     if (res.data) {
    //         designationData()
    //     }

    // })
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