<template>
    <div>
        <div class="d-flex justify-content-between align-items-center ">
            <div>
                <h1 class="m-0 font-13">
                    User Management
                </h1>
                <!-- <p class="m-0 font-11 pt-1">
                374 users
            </p> -->
            </div>
            <div class="d-flex gap-2 align-items-center">
                <div class="d-flex align-items-center">
                    <div class="me-2">
                        <span v-if="filterOnModal.emp_code && filterOnModal.appliedeEmp_code"
                            class="process-date font-12 m-0">
                            {{ filterOnModal.emp_code }}
                            <span v-if="filterOnModal.emp_code" class="badge badge-icon rounded-3   text-white "
                                @click="clearFilter('emp_code')">
                                <i class="ri-close-line close-icon text-dark rounded-3"></i>
                            </span>
                        </span>

                        <span v-if="filterOnModal.designation && filterOnModal.applieddesignation"
                            class="process-date font-12 m-0"> {{
                                filterOnModal.designation }}
                            <span v-if="filterOnModal.designation" class="badge badge-icon rounded-3   text-white "
                                @click="clearFilter('designation')">
                                <i class="ri-close-line close-icon text-dark rounded-3"></i>
                            </span>
                        </span>
                        <span v-if="filterOnModal.department && filterOnModal.applieddepartment"
                            class="process-date font-12 m-0"> {{
                                filterOnModal.department }}
                            <span v-if="filterOnModal.department" class="badge badge-icon rounded-3   text-white "
                                @click="clearFilter('department')">
                                <i class="ri-close-line close-icon text-dark rounded-3"></i>
                            </span>
                        </span>
                        <span v-if="filterOnModal.emp_mail_id && filterOnModal.appliedEmp_mail_id"
                            class="process-date font-12 m-0"> {{
                                filterOnModal.emp_mail_id }}
                            <span v-if="filterOnModal.emp_mail_id" class="badge badge-icon rounded-3   text-white "
                                @click="clearFilter('emp_mail_id')">
                                <i class="ri-close-line close-icon text-dark rounded-3"></i>
                            </span>
                        </span>
                        <span v-if="filterOnModal.emp_code && filterOnModal.appliedeEmp_code"
                            class="process-date font-12 m-0"> {{
                                filterOnModal.emp_name }}
                            <span v-if="filterOnModal.emp_name" class="badge badge-icon rounded-3   text-white "
                                @click="clearFilter('emp_name')">
                                <i class="ri-close-line close-icon text-dark rounded-3"></i>
                            </span>
                        </span>
                        <span v-if="filterOnModal.reporting_designation && filterOnModal.appliedreporting_designation"
                            class="process-date font-12 m-0"> {{
                                filterOnModal.reporting_designation }}
                            <span v-if="filterOnModal.reporting_designation"
                                class="badge badge-icon rounded-3   text-white "
                                @click="clearFilter('reporting_designation')">
                                <i class="ri-close-line close-icon text-dark rounded-3"></i>
                            </span>
                        </span>
                        <span v-if="filterOnModal.reporting_to && filterOnModal.appliedreporting_to"
                            class="process-date font-12 m-0"> {{
                                filterOnModal.reporting_to }}
                            <span v-if="filterOnModal.reporting_to" class="badge badge-icon rounded-3   text-white "
                                @click="clearFilter('reporting_to')">
                                <i class="ri-close-line close-icon text-dark rounded-3"></i>
                            </span>
                        </span>
                    </div>
                    <div>
                        <button type="button" class=" filterbtn d-flex align-items-center position-relative " data-bs-toggle="modal"
                            data-bs-target="#fileterModal">
                            <span> <i class="ri-filter-2-line"></i></span>
                            <span v-if="appliedFiltersCount !== 0"
                            class=" badge badge-light colorappiled ">
                (  {{ appliedFiltersCount }})
                </span>
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
                                        <label class="font-13 ps-1" for="Employee">Employee Name:</label>
                                        <FormFields class="mb-3" tag="input" type="search" name="Employee" id="Employee"
                                            placeholder="Search" v-model="filterOnModal.emp_name" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="Requested">Employee code:</label>
                                        <FormFields class="mb-3" tag="input" type="search" name="Employee" id="Employee"
                                            placeholder="Search" v-model="filterOnModal.emp_code" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="emp_mail_id">Employee mail:</label>
                                        <FormFields class="mb-3" tag="input" type="search" name="emp_mail_id"
                                            id="emp_mail_id" placeholder="Search" v-model="filterOnModal.emp_mail_id" />
                                    </div>

                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="dept">Employee Department:</label>
                                        <FormFields tag="select" placeholder="Select Department" class="mb-3"
                                            name="dept" v-model="filterOnModal.department" id="dept" :Required="false"
                                            :options="departmentsList" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="dept">Employee Desigination:</label>
                                        <FormFields tag="select" placeholder="Select Desigination" class="mb-3"
                                            name="dept" v-model="filterOnModal.designation" id="dept" :Required="false"
                                            :options="designiations" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="Requested">Reporting To:</label>
                                        <FormFields tag="select" placeholder="Reporting To" class="mb-3" name="dept"
                                            v-model="filterOnModal.reporting_to" id="dept" :Required="false"
                                            :options="reportingTo" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="Requested">Reporting Desigination:</label>
                                        <FormFields tag="select" placeholder="Reporting To" class="mb-3" name="dept"
                                            v-model="filterOnModal.reporting_designation" id="dept" :Required="false"
                                            :options="reportingDesigination" />
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
                        Create Employee
                    </button>
                </div>
                <div class="modal fade" id="createDepartments" data-bs-backdrop="static" tabindex="-1"
                    data-bs-keyboard="false" aria-labelledby="createDepartmentsLabel" aria-hidden="true">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title" id="createDepartmentsLabel">Ezy Employee</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal" @click="cancelCreate"
                                    aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                <div class="container-fluid">
                                    <div class=" row">
                                        <div class=" col">
                                            <label class="font-13 ps-1" for="emp_code">Emp code</label>
                                            <FormFields class="mb-3" tag="input" type="text" name="emp_code"
                                                id="emp_code" placeholder="Enter Emp code"
                                                v-model="createEmployee.emp_code" />
                                            <label class="font-13 ps-1" for="emp_name">Emp Name</label>
                                            <FormFields class="mb-3" tag="input" type="text" name="emp_name"
                                                id="emp_name" placeholder="Enter Emp Name"
                                                v-model="createEmployee.emp_name" />

                                            <label class="font-13 ps-1" for="emp_mail_id">Emp Mail ID</label>
                                            <FormFields class="mb-3" tag="input" type="text" name="emp_mail_id"
                                                id="emp_mail_id" placeholder="Enter Email"
                                                v-model="createEmployee.emp_mail_id" />
                                            <label class="font-13 ps-1 fw-medium" for="dept">Departments</label>
                                            <FormFields tag="select" placeholder="Select Department" class="mb-3"
                                                name="dept" v-model="createEmployee.department" id="dept"
                                                :Required="false" :options="departmentsList" />
                                        </div>
                                        <div class=" col">
                                            <label class="font-13 ps-1" for="Designation">Designation</label>
                                            <FormFields class="mb-3" tag="input" type="text" name="Designation"
                                                id="Designation" placeholder="Enter Designation"
                                                v-model="createEmployee.designation" />
                                            <label class="font-13 ps-1" for="reporting_to">Reporting To</label>
                                            <FormFields class="mb-3" tag="input" type="text" name="reporting_to"
                                                id="reporting_to" placeholder="Enter Reporting To"
                                                v-model="createEmployee.reporting_to" />
                                            <label class="font-13 ps-1" for="reporting_designation">Reporting
                                                Designation</label>
                                            <FormFields class="mb-3" tag="input" type="text"
                                                name="reporting_designation" id="reporting_designation"
                                                placeholder="Enter Reporting Designation"
                                                v-model="createEmployee.reporting_designation" />
                                        </div>

                                    </div>
                                </div>

                            </div>
                            <div class="modal-footer">
                                <ButtonComp type="button" class="cancelfilter border-1 text-nowrap font-10 "
                                    name="Cancel" @click="cancelCreate" data-bs-dismiss="modal" />


                                <button type="button"
                                    class="applyfilter btn btn-dark text-nowrap font-10 d-flex justify-content-center align-items-center"
                                    data-bs-dismiss="modal" @click="createEmpl"><span class="font-16 me-1"><i
                                            class="bi bi-check2 "></i></span>
                                    Create Employee</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="mt-2">
            <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction='true' :actions="actions"
                @actionClicked="actionCreated" actionType="dropdown" isCheckbox="true" />
        </div>
        <div class="modal fade" id="viewEmployee" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
            aria-labelledby="viewEmployeeLabel" aria-hidden="true">
            <div class="modal-dialog modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="viewEmployeeLabel">Ezy Employee</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" @click="cancelCreate"
                            aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="container-fluid">
                            <div class=" row">
                                <div class=" col">
                                    <label class="font-13 ps-1" for="emp_code">Emp code</label>
                                    <FormFields class="mb-3" tag="input" type="text" name="emp_code" id="emp_code"
                                        placeholder="Enter department code" v-model="createEmployee.emp_code" />
                                    <label class="font-13 ps-1" for="emp_name">Emp Name</label>
                                    <FormFields class="mb-3" tag="input" type="text" name="emp_name" id="emp_name"
                                        placeholder="Enter department code" v-model="createEmployee.emp_name" />

                                    <label class="font-13 ps-1" for="emp_mail_id">Emp Mail ID</label>
                                    <FormFields class="mb-3" tag="input" type="text" name="emp_mail_id" id="emp_mail_id"
                                        placeholder="Enter department code" v-model="createEmployee.emp_mail_id" />
                                    <label class="font-13 ps-1 fw-medium" for="dept">Departments</label>
                                    <FormFields tag="select" placeholder="Select Department" class="mb-3" name="dept"
                                        v-model="createEmployee.department" id="dept" :Required="false"
                                        :options="departmentsList" />
                                </div>
                                <div class=" col">
                                    <label class="font-13 ps-1" for="Designation">Designation</label>
                                    <FormFields class="mb-3" tag="input" type="text" name="Designation" id="Designation"
                                        placeholder="Enter department code" v-model="createEmployee.designation" />
                                    <label class="font-13 ps-1" for="reporting_to">Reporting To</label>
                                    <FormFields class="mb-3" tag="input" type="text" name="reporting_to"
                                        id="reporting_to" placeholder="Enter department code"
                                        v-model="createEmployee.reporting_to" />
                                    <label class="font-13 ps-1" for="reporting_designation">Reporting
                                        Designation</label>
                                    <FormFields class="mb-3" tag="input" type="text" name="reporting_designation"
                                        id="reporting_designation" placeholder="Enter department code"
                                        v-model="createEmployee.reporting_designation" />
                                </div>

                            </div>
                        </div>



                    </div>
                    <div class="modal-footer">
                        <ButtonComp type="button" class="cancelfilter border-1 text-nowrap font-10 " name="Cancel"
                            @click="cancelCreate" data-bs-dismiss="modal" />

                        <ButtonComp type="button" class=" btn btn-dark font-11" name="Save Employee"
                            data-bs-dismiss="modal" @click="SaveEditEmp" />

                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import FormFields from '../../Components/FormFields.vue';
import ButtonComp from '../../Components/ButtonComp.vue';
import GlobalTable from '../../Components/GlobalTable.vue';
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from '../../shared/apiurls';
import { onMounted, reactive, ref, computed } from 'vue';
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";


onMounted(() => {
    deptData();
    employeeData();
})

const departmentsList = ref([])
const createEmployee = ref({
    emp_code: "",
    emp_name: "",
    emp_mail_id: "",
    department: "",
    designation: "",
    reporting_to: "",
    reporting_designation: ""
});

const actions = ref(
    [
        { name: 'Edit Employee', icon: 'fa-solid fa-eye' },

    ]
)
function actionCreated(rowData, actionEvent) {
    if (actionEvent.name === 'Edit Employee') {
        if (rowData) {
            createEmployee.value = { ...rowData }
            const modal = new bootstrap.Modal(document.getElementById('viewEmployee'), {});
            modal.show();
        } else {
            console.warn("No form fields provided.");
            formCreation(rowData);
        }
    }
}
const filterObj = ref({
    limitPageLength: 'None',
    limitstart: 0
});
const tableheaders = ref([
    { th: "Employee Code", td_key: "emp_code" },
    { th: "Name", td_key: "emp_name" },
    { th: "Mail", td_key: "emp_mail_id" },
    { th: "Department", td_key: "department" },
    { th: "Designation", td_key: "designation" },
    { th: "Reporting To", td_key: "reporting_to" },
    { th: "Reporting Designation", td_key: "reporting_designation" },

])

const filtersBeforeApplyingCount = computed(() => {
    return [filterOnModal.designation, filterOnModal.emp_code, filterOnModal.department, filterOnModal.emp_mail_id, filterOnModal.emp_name, filterOnModal.reporting_designation, filterOnModal.reporting_to].filter(
        (value) => value
    ).length;
});

// Count of filters that are both applied and have non-empty values
const appliedFiltersCount = computed(() => {
    return [
        { value: filterOnModal.designation, applied: filterOnModal.applieddesignation },
        {
            value: filterOnModal.emp_code,
            applied: filterOnModal.appliedeEmp_code,
        },
        {
            value: filterOnModal.emp_mail_id,
            applied: filterOnModal.appliedEmp_mail_id,
        },
        {
            value: filterOnModal.department,
            applied: filterOnModal.applieddepartment,
        },
        {
            value: filterOnModal.emp_name,
            applied: filterOnModal.appliedEmp_name,
        },

        {
            value: filterOnModal.reporting_designation,
            applied: filterOnModal.appliedreporting_designation,
        },
        {
            value: filterOnModal.reporting_to,
            applied: filterOnModal.appliedreporting_to,
        },
       
    ].filter((filter) => filter.applied && filter.value).length;
});
const filterOnModal = reactive({
    appliedeEmp_code: false,
    appliedEmp_name: false,
    appliedEmp_mail_id: false,
    applieddepartment: false,
    applieddesignation: false,
    appliedreporting_to: false,
    appliedreporting_designation: false,

    emp_code: "",
    emp_name: "",
    emp_mail_id: "",

    department: "",
    designation: "",
    reporting_to: "",
    reporting_designation: "",


})
function clearFilter(type) {
    if (type === "emp_code") {
        filterOnModal.emp_code = "";
        filterOnModal.appliedeEmp_code = false;
    } else if (type === "designation") {
        filterOnModal.designation = "";
        filterOnModal.applieddesignation = false;
    }
    else if (type === "department") {
        filterOnModal.department = "";
        filterOnModal.applieddepartment = false;
    }
    else if (type === "emp_mail_id") {
        filterOnModal.emp_mail_id = "";
        filterOnModal.appliedEmp_mail_id = false;
    }
    else if (type === "emp_name") {
        filterOnModal.emp_name = "";
        filterOnModal.appliedEmp_name = false;
    }
    else if (type === "reporting_designation") {
        filterOnModal.reporting_designation = "";
        filterOnModal.appliedreporting_designation = false;
    }
    else if (type === "reporting_to") {
        filterOnModal.reporting_to = "";
        filterOnModal.appliedreporting_to = false;
    }


    applyFilters();
}
const tableData = ref([]);

function applyFilters() {

    filterOnModal.appliedeEmp_code = Boolean(filterOnModal.emp_code);
    filterOnModal.appliedEmp_name = Boolean(filterOnModal.emp_name);
    filterOnModal.appliedEmp_mail_id = Boolean(filterOnModal.emp_mail_id);
    filterOnModal.applieddepartment = Boolean(filterOnModal.department);
    filterOnModal.applieddesignation = Boolean(filterOnModal.designation);
    filterOnModal.appliedreporting_to = Boolean(filterOnModal.reporting_to);
    filterOnModal.appliedreporting_designation = Boolean(filterOnModal.reporting_designation);

    employeeData();
}


function resetFilters() {
    filterOnModal.value = {
        emp_code: "",

        Owner_OF_Form: "",
        Form_Category: "",
        Form_Name: "",
        Requested_Period: "",
        Approval_status: "",

    };
    employeeData()
}
function cancelCreate() {
    createEmployee.value = {
        emp_code: "",
        emp_name: "",
        emp_mail_id: "",
        department: "",
        designation: "",
        reporting_to: "",
        reporting_designation: ""
    }
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

            }
        })
        .catch((error) => {
            console.error("Error fetching department data:", error);
        });
}

const designiations = ref([]);
const reportingTo = ref([]);
const reportingDesigination = ref([]);
function employeeData() {
    const filters = [];
    if (filterOnModal.emp_code) {
        filters.push(["emp_code", "like", `%${filterOnModal.emp_code}%`]);
    }
    if (filterOnModal.emp_name) {
        filters.push(["emp_name", "like", `%${filterOnModal.emp_name}%`]);
    }
    if (filterOnModal.emp_mail_id) {
        filters.push(["emp_mail_id", "like", `%${filterOnModal.emp_mail_id}%`]);
    }
    if (filterOnModal.department) {
        filters.push(["department", "=", `${filterOnModal.department}`]);
    }
    if (filterOnModal.designation) {
        filters.push(["designation", "like", `${filterOnModal.designation}`]);
    }
    if (filterOnModal.reporting_to) {
        filters.push(["reporting_to", "like", `${filterOnModal.reporting_to}`]);
    }
    if (filterOnModal.reporting_designation) {
        filters.push(["reporting_designation", "like", `%${filterOnModal.reporting_designation}%`]);
    }


    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify(filters),
        limit_page_length: filterObj.value.limitPageLength,
        limitstart: filterObj.value.limitstart,
        // order_by: "`tabEzy Employee`.`creation` desc"
    };

    axiosInstance.get(apis.resource + doctypes.EzyEmployeeList, { params: queryParams })
        .then((res) => {
            if (res.data) {
                console.log(res.data, "Fetched departments");
                tableData.value = res.data;
                designiations.value = [...new Set(res.data.map((designation) => designation.designation))];
                reportingTo.value = [...new Set(res.data.map((reporting) => reporting.reporting_to))];
                reportingDesigination.value = [...new Set(res.data.map((reportingDesigination) => reportingDesigination.reporting_designation))]

            }
        })
        .catch((error) => {
            console.error("Error fetching department data:", error);
        });
}

function createEmpl() {
    const dataObj = {
        ...createEmployee.value,
        "doctype": doctypes.EzyEmployeeList
    }
    console.log(dataObj, "------------------");
    axiosInstance.post(apis.resource + doctypes.EzyEmployeeList, dataObj).then((res) => {
        if (res.data) {
            toast.success("Employee Created", { autoClose: 500 })
            employeeData()
        }

    })
}
function SaveEditEmp() {
    console.log(createEmployee.value, "---------------", createEmployee.value.name);
    axiosInstance.put(`${apis.resource}${doctypes.EzyEmployeeList}/${createEmployee.value.name}`, createEmployee.value)
        .then((response) => {
            if (response.data) {
                toast.success("Changes Saved", { autoClose: 500 })
                employeeData()
            }
            console.log("Categories saved successfully:", response.data);
        })
        .catch((error) => {
            console.error("Error saving categories:", error);
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