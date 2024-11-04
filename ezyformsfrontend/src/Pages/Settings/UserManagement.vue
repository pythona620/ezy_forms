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
                                                id="emp_code" placeholder="Enter department code"
                                                v-model="createEmployee.emp_code" />
                                            <label class="font-13 ps-1" for="emp_name">Emp Name</label>
                                            <FormFields class="mb-3" tag="input" type="text" name="emp_name"
                                                id="emp_name" placeholder="Enter department code"
                                                v-model="createEmployee.emp_name" />

                                            <label class="font-13 ps-1" for="emp_mail_id">Emp Mail ID</label>
                                            <FormFields class="mb-3" tag="input" type="text" name="emp_mail_id"
                                                id="emp_mail_id" placeholder="Enter department code"
                                                v-model="createEmployee.emp_mail_id" />
                                            <label class="font-13 ps-1 fw-medium" for="dept">Departments</label>
                                            <FormFields tag="select" placeholder="Select Department" class="mb-3"
                                                name="dept" v-model="createEmployee.department" id="dept"
                                                :Required="false" :options="departmentsList" />
                                        </div>
                                        <div class=" col">
                                            <label class="font-13 ps-1" for="Designation">Designation</label>
                                            <FormFields class="mb-3" tag="input" type="text" name="Designation"
                                                id="Designation" placeholder="Enter department code"
                                                v-model="createEmployee.designation" />
                                            <label class="font-13 ps-1" for="reporting_to">Reporting To</label>
                                            <FormFields class="mb-3" tag="input" type="text" name="reporting_to"
                                                id="reporting_to" placeholder="Enter department code"
                                                v-model="createEmployee.reporting_to" />
                                            <label class="font-13 ps-1" for="reporting_designation">Reporting
                                                Designation</label>
                                            <FormFields class="mb-3" tag="input" type="text"
                                                name="reporting_designation" id="reporting_designation"
                                                placeholder="Enter department code"
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
import { onMounted, ref } from 'vue';
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";


onMounted(() => {
    deptData();
    employeeData();
})
const radioOptions = ref(["yes", "no"])
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
const filterOnModal = ref({
    emp_code: "",
    emp_name: "",
    emp_mail_id: "",
    Requested_dept: "",
    Owner_OF_Form: "",
    Form_Category: "",
    Requested_Period: "",
    Approval_status: "",
    RequestedId: ""

})
const tableData = ref([]);

function applyFilters() {
    employeeData(); // Calls employeeData to send filters
}

function resetFilters() {
    filterOnModal.value = {
        emp_code: "",
        Requested_dept: "",
        Owner_OF_Form: "",
        Form_Category: "",
        Form_Name: "",
        Requested_Period: "",
        Approval_status: "",
        RequestedId: ""
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


function employeeData() {
    const filters = [];
    if (filterOnModal.value.emp_code) {
        filters.push(["emp_code", "like", `%${filterOnModal.value.emp_code}%`]);
    }
    if (filterOnModal.value.emp_name) {
        filters.push(["emp_name", "like", `%${filterOnModal.value.emp_name}%`]);
    }
    if (filterOnModal.value.emp_mail_id) {
        filters.push(["emp_mail_id", "like", `%${filterOnModal.value.emp_mail_id}%`]);
    }
    if (filterOnModal.value.Owner_OF_Form) {
        filters.push(["Owner_OF_Form", "like", `%${filterOnModal.value.Owner_OF_Form}%`]);
    }
    if (filterOnModal.value.Form_Category) {
        filters.push(["Form_Category", "like", `%${filterOnModal.value.Form_Category}%`]);
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
        // order_by: "`tabEzy Employee`.`creation` desc"
    };

    axiosInstance.get(apis.resource + doctypes.EzyEmployeeList, { params: queryParams })
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