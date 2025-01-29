<template>
    <div>
        <div class="d-flex justify-content-between align-items-center p-2">
            <div>
                <h1 class="m-0 font-13">
                    User Management
                </h1>
                <!-- <p class="m-0 font-11 pt-1">
                374 users
            </p> -->
            </div>
            <div class="d-flex align-items-center ">
                <button type="button" class="btn btn-dark buttoncomp CreateDepartments d-flex align-items-center "
                    data-bs-toggle="modal" data-bs-target="#createDepartments" @click="createEmplBtn">
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
                                        <FormFields class="mb-3" tag="input" type="text" name="emp_code" id="emp_code"
                                            placeholder="Enter Emp code" v-model="createEmployee.emp_code" />
                                        <label class="font-13 ps-1" for="emp_name">Emp Name</label>
                                        <FormFields class="mb-3" tag="input" type="text" name="emp_name" id="emp_name"
                                            placeholder="Enter Emp Name" v-model="createEmployee.emp_name" />

                                        <label class="font-13 ps-1" for="emp_mail_id">Emp Mail ID</label>
                                        <FormFields class="mb-3" tag="input" type="text" name="emp_mail_id"
                                            id="emp_mail_id" placeholder="Enter Email"
                                            v-model="createEmployee.emp_mail_id" />
                                        <label class="font-13 ps-1 fw-medium" for="dept">Departments</label>
                                        <FormFields tag="select" placeholder="Select Department" class="mb-3"
                                            name="dept" v-model="createEmployee.department" id="dept" :Required="false"
                                            :options="departmentsList" />
                                    </div>
                                    <div class=" col">
                                        <label class="font-13 ps-1" for="Designation">Designation</label>
                                        <!-- <FormFields class="mb-3" tag="input" type="text" name="Designation"
                                                id="Designation" placeholder="Enter Designation"
                                                v-model="createEmployee.designation" /> -->
                                        <FormFields tag="select" placeholder="Select Desigination" class="mb-0"
                                            name="Designation" v-model="createEmployee.designation" id="dept"
                                            :Required="false" :options="designiations" />
                                        <!-- <div class=""><button @click="addnewDesignation" type="button"
                                                class="btn btn-white text-decoration-underline font-11">Add new
                                                designation <span><i class=" bi bi-plus"></i></span></button>
                                        </div>
                                        <FormFields v-if="newDesignation" class="mb-3" tag="input" type="text"
                                            name="emp_code" id="emp_code" placeholder="Enter Designation"
                                            v-model="inputDesignation" /> -->
                                        <label class="font-13 ps-1" for="reporting_to">Reporting To</label>
                                        <FormFields class="mb-3" tag="input" type="text" name="reporting_to"
                                            id="reporting_to" placeholder="Enter Reporting To"
                                            v-model="createEmployee.reporting_to" />
                                        <label class="font-13 ps-1" for="reporting_designation">Reporting
                                            Designation</label>
                                        <FormFields class="mb-3" tag="input" type="text" name="reporting_designation"
                                            id="reporting_designation" placeholder="Enter Reporting Designation"
                                            v-model="createEmployee.reporting_designation" />
                                    </div>

                                </div>
                            </div>

                        </div>
                        <div class="modal-footer">
                            <ButtonComp type="button" class="cancelfilter border-1 text-nowrap font-10 " name="Cancel"
                                @click="cancelCreate" data-bs-dismiss="modal" />


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
        <div class="mt-2">
            <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction='true' :actions="actions"
                @actionClicked="actionCreated" actionType="dropdown" isCheckbox="true" isFiltersoption="true"
                :field-mapping="fieldMapping" @updateFilters="inLineFiltersData" />
            <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords"
                @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
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
import PaginationComp from '../../Components/PaginationComp.vue';
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from '../../shared/apiurls';
import { onMounted, reactive, ref, computed, watch } from 'vue';
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import { EzyBusinessUnit } from "../../shared/services/business_unit";

const businessUnit = computed(() => {
    return EzyBusinessUnit.value;
});

const tableData = ref([]);
const newbusiness = ref("");
const totalRecords = ref(0);
const designiations = ref([]);
const reportingTo = ref([]);
const reportingDesigination = ref([]);
const departmentsList = ref([])
// const newDesignation = ref(false);
const createEmployee = ref({
    emp_code: "",
    emp_name: "",
    emp_mail_id: "",
    department: "",
    designation: "",
    reporting_to: "",
    reporting_designation: "",
    company_field: "",

});
// function addnewDesignation() {
//     newDesignation.value = !newDesignation.value
// }
const actions = ref(
    [
        { name: 'Edit Employee', icon: 'fa-solid fa-eye' },

    ]
)
function createEmplBtn() {
    deptData();
    designationData();

}
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
    limit_start: 0
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
const fieldMapping = ref({

    emp_code: { type: "input" },
    emp_name: { type: "input" }

});
// const filtersBeforeApplyingCount = computed(() => {
//     return [filterOnModal.designation, filterOnModal.emp_code, filterOnModal.department, filterOnModal.emp_mail_id, filterOnModal.emp_name, filterOnModal.reporting_designation, filterOnModal.reporting_to].filter(
//         (value) => value
//     ).length;
// });
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
        limit_start: filterObj.value.limit_start,
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

// Handle updating the current value
const PaginationUpdateValue = (itemsPerPage) => {
    filterObj.value.limitPageLength = itemsPerPage;
    filterObj.value.limit_start = 0;
    fetchTable();

};
// Handle updating the limit start
const PaginationLimitStart = ([itemsPerPage, start]) => {
    filterObj.value.limitPageLength = itemsPerPage;
    filterObj.value.limit_start = start;
    fetchTable();

};




function inLineFiltersData(searchedData) {
    console.log("Applied searchedData:", searchedData);

    //   // Initialize filters array
    const filters = [];

    //   // Loop through the tableheaders and build dynamic filters based on the `searchedData`
    tableheaders.value.forEach((header) => {
        const key = header.td_key;

        //     // If there is a match for the key in searchedData, create a 'like' filter
        if (searchedData[key]) {
            filters.push(key, "like", `%${searchedData[key]}%`);
        }
        //     // Add filter for selected option
        //     if (key === "selectedOption" && searchedData.selectedOption) {
        //       filters.push([key, "=", searchedData.selectedOption]);
        //     }
        //     // Special handling for 'invoice_date' to create a 'Between' filter (if it's a date)
        //     if (key === "invoice_date" && searchedData[key]) {
        //       filters.push([key, "Between", [searchedData[key], searchedData[key]]]);
        //     }

        //     // Special handling for 'invoice_type' or 'irn_generated' to create an '=' filter
        //     if ((key === "invoice_type" || key === "credit_irn_generated") && searchedData[key]) {
        //       filters.push([key, "=", searchedData[key]]);
        //     }
    });
    console.log(filters.length == 0, "------------filters--------");

    //   // Log filters to verify
    //   console.log("Dynamic Filters:", filters);

    //   // Once the filters are built, pass them to fetchData function
    if (filters.length) {
        employeeData(filters);
    }
    else {
        employeeData();
    }
    //   fetchTotalRecords(filters);
}

function employeeData(data) {
    const filters = [
        ["company_field", "like", `%${newbusiness.value}%`]
    ];
    if (data) {
        filters.push(data)
    }

    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify(filters),
        limit_page_length: filterObj.value.limitPageLength,
        limit_start: filterObj.value.limit_start,
        order_by: "`tabEzy Employee`.`creation` desc"
    };
    const queryParamsCount = {
        fields: JSON.stringify(["count(name) AS total_count"]),
        limitPageLength: "None",
        filters: JSON.stringify(filters),
    }
    axiosInstance.get(`${apis.resource}${doctypes.EzyEmployeeList}`, { params: queryParamsCount })
        .then((res) => {
            // console.log(res.data[0].total_count);
            totalRecords.value = res.data[0].total_count

        })
        .catch((error) => {
            console.error("Error fetching ezyForms data:", error);
        });


    axiosInstance.get(apis.resource + doctypes.EzyEmployeeList, { params: queryParams })
        .then((res) => {
            if (res.data) {
                console.log(res.data, "Fetched departments");
                tableData.value = res.data;
                // designiations.value = [...new Set(res.data.map((designation) => designation.designation))];
                reportingTo.value = [...new Set(res.data.map((reporting) => reporting.reporting_to))];
                reportingDesigination.value = [...new Set(res.data.map((reportingDesigination) => reportingDesigination.reporting_designation))]
                console.log(designiations.value, "%%%%%%%%%%%%");

            }
        })
        .catch((error) => {
            console.error("Error fetching department data:", error);
        });
}
function designationData() {
    const filters = [];
    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify(filters),
        limit_page_length: filterObj.value.limitPageLength,
        limit_start: filterObj.value.limit_start,
        order_by: "`tabWF Roles`.`creation` desc"
    };


    axiosInstance.get(apis.resource + doctypes.designations, { params: queryParams })
        .then((res) => {
            if (res.data) {
                console.log(res.data.name, "Fetched Designations");
                designiations.value = [
                    ...new Set(res.data.map((user) => user.role)),
                ];
                console.log(designiations.value, "%%%%%%%%%");
            }
        })
        .catch((error) => {
            console.error("Error fetching designations data:", error);
        });
}




watch(
    businessUnit,
    (newVal) => {
        createEmployee.value.company_field = newVal;
        newbusiness.value = newVal;

        if (newVal.length) {
            console.log(newVal, "new value of business unit");
            employeeData();
        }
    },
    { immediate: true }
);
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