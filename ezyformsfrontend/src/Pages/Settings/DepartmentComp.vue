<template>
    <div>
        <div class="d-flex justify-content-between align-items-center ">
            <div>
                <h1 class="m-0 font-13">
                    Departments
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
                        Create Departments
                    </button>
                </div>
                <div class="modal fade" id="createDepartments" tabindex="-1" aria-labelledby="createDepartmentsLabel"
                    aria-hidden="true">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">

                            <div class="modal-body">
                                <label class="font-13 ps-1" for="DepartmentCode">Department Code</label>
                                <FormFields class="mb-3" tag="input" type="text" name="DepartmentCode"
                                    id="DepartmentCode" placeholder="Enter department code"
                                    v-model="CreateDepartments.department_code" />

                                <label class="font-13 ps-1" for="Requedepartment_namested">Department name</label>
                                <FormFields class="mb-3" tag="input" type="text" name="department_name"
                                    id="department_name" placeholder="Enter department name"
                                    v-model="CreateDepartments.department_name" />
                                <label class="font-13 ps-1" for="business_unit">Business Unit</label>

                                <FormFields tag="select" placeholder="" class="mb-3" name="business_unit"
                                    id="business_unit" v-model="CreateDepartments.business_unit"
                                    :options="EzyFormsCompanys" />
                                <div class="d-flex align-items-center">
                                    <div class="w-100">
                                        <label class="font-13 ps-1" for="ezy_departments_items">Ezy Departments
                                            Items</label>
                                        <FormFields class="mb-3" tag="input" type="text" name="ezy_departments_items"
                                            id="ezy_departments_items" placeholder="Enter category"
                                            v-model="newCategory" />
                                    </div>
                                    <ButtonComp class="buttoncomp mt-2" name="Add" @click="addCategory" />
                                </div>
                                <div v-if="CreateDepartments.ezy_departments_items.length > 0">
                                    <table class="table mt-3 global-table">
                                        <thead>
                                            <tr>
                                                <th>#</th>
                                                <th>Category Name</th>
                                                <th>Actions</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            <tr v-for="(item, index) in CreateDepartments.ezy_departments_items"
                                                :key="index">
                                                <td>{{ index + 1 }}</td>
                                                <td v-if="editIndex !== index">{{ item.category }}</td>
                                                <td v-else>
                                                    <input type="text" v-model="editCategory" @change="saveEdit(index)"
                                                        placeholder="Edit Category" />
                                                </td>
                                                <td>
                                                    <!-- Pencil icon for editing -->
                                                    <i v-if="editIndex !== index" class="bi bi-pencil"
                                                        @click="startEdit(index, item.category)"></i>
                                                    <i v-else class="bi bi-check font-20" @click="saveEdit(index)"></i>
                                                    <!-- Trash icon for removing -->
                                                    <i class="bi bi-trash ms-2" @click="removeCategory(index)"></i>
                                                </td>
                                            </tr>
                                        </tbody>
                                    </table>
                                </div>

                            </div>
                            <div class="modal-footer">
                                <button type="button" class="cancelfilter border-1 text-nowrap font-10 "
                                    @click="cancelCreate" data-bs-dismiss="modal">Cancel
                                </button>

                                <button type="button"
                                    class="applyfilter btn btn-dark text-nowrap font-10 d-flex justify-content-center align-items-center"
                                    data-bs-dismiss="modal" @click="createDepart"><span class="font-16 me-1"><i
                                            class="bi bi-check2 "></i></span>
                                    Create Department</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="mt-2">
            <GlobalTable :tHeaders="tableheaders" :tData="tableData" @actionClicked="actionCreated" isAction='true'
                :actions="actions" actionType="dropdown" isCheckbox="true" />
        </div>
        <div class="modal fade" id="viewCategory" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
            aria-labelledby="viewCategoryLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="viewCategoryLabel">Modal title</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <table class="table mt-3 global-table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Category Name</th>
                                    <th>Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in categoriesData" :key="index">
                                    <td>{{ index + 1 }}</td>
                                    <td v-if="editIndex !== index">{{ item.category }}</td>
                                    <td v-else>
                                        <input type="text" v-model="editCategory" @change="saveEditCategory(index)"
                                            placeholder="Edit Category" />
                                    </td>
                                    <td>
                                        <i v-if="editIndex !== index" class="bi bi-pencil"
                                            @click="startEditCategory(index, item.category)"></i>
                                        <i v-else class="bi bi-check font-20" @click="saveEditCategory(index)"></i>
                                        <i class="bi bi-trash ms-2" @click="removeCategory(index)"></i>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
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
import { onMounted, ref, computed, watch } from 'vue';
import { EzyBusinessUnit } from "../../shared/services/business_unit";


const businessUnit = computed(() => {
    return EzyBusinessUnit.value;
});
onMounted(() => {
    deptData();
    ezyForms();
})
const tableData = ref([]);
const radioOptions = ref(["yes", "no"])
const EzyFormsCompanys = ref([]);
const newCategory = ref("");
const editIndex = ref(null);
const editCategory = ref("");
const categoriesData = ref([])
const actions = ref(
    [
        { name: 'View Categories', icon: 'fa-solid fa-eye' },

    ]
)
function actionCreated(rowData, actionEvent) {
    if (actionEvent.name === 'View Categories') {
        if (rowData) {
            console.log(rowData.name, "jjjjjjjjjjjjj");
            axiosInstance.get(apis.resource + doctypes.departments + `/${rowData.name}`)
                .then((res) => {
                    if (res.data) {
                        console.log(res.data, "================================");
                        if (res?.data?.ezy_departments_items) {
                            categoriesData.value = res.data.ezy_departments_items;
                        }
                        console.log(categoriesData.value);

                    }
                })
                .catch((error) => {
                    console.error("Error fetching categories data:", error);
                });



            const modal = new bootstrap.Modal(document.getElementById('viewCategory'), {});
            modal.show();

        } else {
            console.warn(" There is no form fields ")
            formCreation(rowData)
        }
    }

}
const tableheaders = ref([
    { th: "Department Code", td_key: "department_code" },
    { th: "Department Name", td_key: "department_name" },
    { th: "Business Unit", td_key: "business_unit" },
    { th: "Ezy Departments Items", td_key: "ezy_departments_items" },

])
const CreateDepartments = ref({
    department_code: "",
    department_name: "",
    business_unit: "",
    ezy_departments_items: [

    ]
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
        CreateDepartments.value.business_unit = newVal;

        if (newVal) {
            console.log(newVal, "new value of business unit");

        }
    },
    { immediate: true }
);

function addCategory() {
    if (newCategory.value) {
        CreateDepartments.value.ezy_departments_items.push({
            category: newCategory.value,
            parentfield: 'ezy_departments_items'
        });
        newCategory.value = "";
    }
}
function startEdit(index, category) {
    editIndex.value = index;
    editCategory.value = category;
}

function saveEdit(index) {
    if (editCategory.value.trim()) {
        CreateDepartments.value.ezy_departments_items[index].category = editCategory.value;
        editIndex.value = null;
        editCategory.value = "";
    }
}

function removeCategory(index) {
    CreateDepartments.value.ezy_departments_items.splice(index, 1);
}

function startEditCategory(index, category) {
    editIndex.value = index;
    editCategory.value = category;
}


function saveEditCategory(index) {
    if (editCategory.value.trim()) {
        categoriesData.value[index].category = editCategory.value;
        editIndex.value = null;
        editCategory.value = "";
    }
}


function applyFilters() {
    deptData();
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
    deptData()
}

function deptData() {
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
        filters.push(["department_name", "like", `%${filterOnModal.value.department_name}%`]);
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

    axiosInstance.get(apis.resource + doctypes.departments, { params: queryParams })
        .then((res) => {
            if (res.data) {

                tableData.value = res.data;
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
    CreateDepartments.value = {
        department_code: "",
        department_name: "",
        ezy_departments_items: [
        ]
    }
}
function createDepart() {
    const dataObj = {
        ...CreateDepartments.value,
        "doctype": doctypes.departments
    }
    console.log(dataObj, "------------------");
    axiosInstance.post(apis.resource + doctypes.departments, dataObj).then((res) => {
        if (res.data) {
            deptData()
        }

    })
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