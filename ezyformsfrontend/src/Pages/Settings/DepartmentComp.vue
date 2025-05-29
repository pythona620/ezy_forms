<template>
    <div>
        <div class="d-flex justify-content-between align-items-center  py-2">
            <div>
                <h1 class="m-0 font-13">
                    Departments
                </h1>
                <!-- <p class="m-0 font-11 pt-1">
                374 users
            </p> -->
            </div>
            <div class="d-flex gap-2 align-items-center">


                <div class="d-flex align-items-center ">

                    <button type="button" class="btn btn-dark buttoncomp CreateDepartments d-flex align-items-center " @click="CreateDeprtModal"
                        data-bs-toggle="modal" data-bs-target="#createDepartments">
                        Create Department
                    </button>
                </div>
                <div class="modal fade" id="createDepartments" tabindex="-1" aria-labelledby="createDepartmentsLabel"
                    aria-hidden="true">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">

                            <div class="modal-body">
                                <div class="mb-3">
                                    <label class="font-13 ps-1" for="DepartmentCode">Department Code</label>
                                    <FormFields tag="input" type="text" name="DepartmentCode" id="DepartmentCode"
                                        placeholder="Enter department code"
                                        v-model="CreateDepartments.department_code" />
                                    <span v-if="formErrors.department_code" class="text-danger font-12">
                                        {{ formErrors.department_code }}
                                    </span>
                                </div>

                                <div class="mb-3">
                                    <label class="font-13 ps-1" for="Requedepartment_namested">Department name</label>
                                    <FormFields tag="input" type="text" name="department_name"
                                        id="department_name" placeholder="Enter department name"
                                        v-model="CreateDepartments.department_name" />
                                    <span v-if="formErrors.department_name" class="text-danger font-12">
                                        {{ formErrors.department_name }}
                                    </span>
                                </div>

                                <label class="font-13 ps-1" for="business_unit">Business Unit</label>
                                <FormFields tag="input" type="text" :disabled="CreateDepartments.business_unit ? true : false"
                                    placeholder="" class="mb-3" name="business_unit" id="business_unit"
                                    v-model="CreateDepartments.business_unit" />
                                <!-- <VueMultiselect v-model="CreateDepartments.business_unit" :options="EzyFormsCompanys"
                                    :multiple="false" :close-on-select="false" :clear-on-select="false"
                                    :preserve-search="true" placeholder="Select Business unit" class="font-11 mb-3"> -->
                                <!-- taggable @tag="addDepartment"
                                            tag-placeholder="Press enter to add department" -->
                                <!-- <template #option="{ option }">
                                                <div class="custom-option">
                                                    <input type="checkbox" :checked="createEmployee.department.includes(
                        option
                    )
                        " class="custom-checkbox" />
                                                    <span>{{ option }}</span>
                                                </div>
                                            </template> -->

                                <!-- <template #selection="{ values, isOpen }">
                                        <span class="multiselect__single font-10" v-if="values.length" v-show="!isOpen">
                                            {{ values.join(", ") }}
                                        </span>
                                    </template>
                                </VueMultiselect> -->
                                <div class="d-flex align-items-center gap-2">
                                    <div class="w-100">
                                        <label class="font-13 ps-1" for="ezy_departments_items">ADD Department
                                            Categories
                                        </label>
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
                                                <th class="text-center">Actions</th>
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
                                                <td class="text-center">
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
                                <button type="button"
                                    class="cancelfilter border-1 text-nowrap font-10 d-flex justify-content-center align-items-center"
                                    @click="cancelCreate" data-bs-dismiss="modal"><span class="font-16 me-1"><i
                                            class="bi bi-x "></i></span>Cancel
                                </button>

                                <button type="button"
                                    class="applyfilter btn btn-dark text-nowrap font-10 d-flex justify-content-center align-items-center"
                                    data-bs-dismiss="modal"
                                    :disabled="!CreateDepartments.department_code || !CreateDepartments.department_name || !CreateDepartments.business_unit"
                                    @click="createDepart"><span class="font-16 me-1"><i
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
                :actions="actions" actionType="dropdown" isCheckbox="true" isFiltersoption="true"
                :field-mapping="fieldMapping" @updateFilters="inLineFiltersData" />
            <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords"
                @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
        </div>
        <div class="modal fade" id="viewCategory" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
            aria-labelledby="viewCategoryLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="viewCategoryLabel">Departments Items</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="d-flex w-100 gap-3">
                            <FormFields class="w-100" tag="input" type="text" name="ezy_departments_items"
                                id="ezy_departments_items" placeholder="Enter category" v-model="newCategory" />
                            <ButtonComp class="buttoncomp" name="Add" @click="addCategoryInView" />
                        </div>

                        <table v-if="categoriesDataEdit.ezy_departments_items.length > 0"
                            class="table mt-3 global-table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Category Name</th>
                                    <th class="text-center">Actions</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(item, index) in categoriesDataEdit.ezy_departments_items" :key="index">
                                    <td>{{ index + 1 }}</td>
                                    <td v-if="editIndex !== index">{{ item.category }}</td>
                                    <td v-else>
                                        <input type="text" v-model="editCategory" @change="saveEditForm(index)"
                                            placeholder="Edit Category" />
                                    </td>
                                    <td class="text-center">
                                        <i v-if="editIndex !== index" class="bi bi-pencil"
                                            @click="startEditForm(index, item.category)"></i>
                                        <i v-else class="bi bi-check font-20" @click="saveEditForm(index)"></i>
                                        <i class="bi bi-trash ms-2" @click="removeCategoryForm(index)"></i>
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <div class="modal-footer">
                        <ButtonComp class="btn btn-dark  font-11" name="Save Categories" @click="saveCategories()" />
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
import PaginationComp from '../../Components/PaginationComp.vue'
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from '../../shared/apiurls';
import { onMounted, ref, computed, watch, reactive } from 'vue';
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import "@vueform/multiselect/themes/default.css";
import VueMultiselect from "vue-multiselect";

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
const formErrors = ref({
    department_code: "",
    department_name: ""
});
const departmenCodeData = ref([]);

const filterObj = ref({
    limitPageLength: 'None',
    limit_start: 0
});
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
function actionCreated(rowData, actionEvent) {
    if (actionEvent.name === 'View Categories') {
        if (rowData) {
            axiosInstance.get(`${apis.resource}${doctypes.departments}/${rowData.name}`)
                .then((res) => {
                    if (res.data) {
                        categoriesDataEdit.value = res.data;

                    }
                })
                .catch((error) => {
                    console.error("Error fetching categories data:", error);
                });

            const modal = new bootstrap.Modal(document.getElementById('viewCategory'), {});
            modal.show();
        } else {
            console.warn("No form fields provided.");
            formCreation(rowData);
        }
    }
}
const tableheaders = ref([
    { th: "Name", td_key: "name" },
    { th: "Department Code", td_key: "department_code" },
    { th: "Department Name", td_key: "department_name" },
    { th: "Business Unit", td_key: "business_unit" },
    // { th: "Status", td_key: "docstatus" },

])
const fieldMapping = ref({
    // invoice_type: { type: "select", options: ["B2B", "B2G", "B2C"] },
    // invoice_date: { type: "date" },
    department_code: { type: "input" },
    department_name: { type: "input" },
    form_category: { type: "select", options: ["Software", "Hardware"] },

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

            deptData()
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

function addCategoryInView() {
    if (newCategory.value) {
        categoriesDataEdit.value.ezy_departments_items.push({
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

function startEditForm(index, category) {
    editIndex.value = index;
    editCategory.value = category;
}

function saveEditForm(index) {
    if (editCategory.value.trim()) {
        categoriesDataEdit.value.ezy_departments_items[index].category = editCategory.value;
        editIndex.value = null;
        editCategory.value = "";
    }
}

function removeCategoryForm(index) {
    categoriesDataEdit.value.ezy_departments_items.splice(index, 1);
}

function saveCategories() {

    axiosInstance.put(`${apis.resource}${doctypes.departments}/${categoriesDataEdit.value.name}`, categoriesDataEdit.value)
        .then((response) => {
            toast.success("Changes Saved", { autoClose: 500, "transition": "zoom" })
            const modal = bootstrap.Modal.getInstance(document.getElementById('viewCategory'));
            modal.hide();

        })
        .catch((error) => {
            console.error("Error saving categories:", error);
        });
}

function inLineFiltersData(searchedData) {


    //   // Initialize filters array
    const filters = [];

    //   // Loop through the tableheaders and build dynamic filters based on the `searchedData`
    tableheaders.value.forEach((header) => {
        const key = header.td_key;

        //     // If there is a match for the key in searchedData, create a 'like' filter
        if (searchedData[key]) {
            filters.push([key, "like", `%${searchedData[key]}%`]);
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

    //   // Log filters to verify
    //   console.log("Dynamic Filters:", filters);

    //   // Once the filters are built, pass them to fetchData function
    if (filters.length) {
        deptData(filters);
    }
    else {
        deptData();
    }
    //   fetchTotalRecords(filters);
}
function CreateDeprtModal(){
    const filters = [
        ["business_unit", "like", `%${CreateDepartments.value.business_unit}%`]
    ];
   
    const queryParams = {
        fields: JSON.stringify(["department_name","department_code"]),
        filters: JSON.stringify(filters),
        limit_page_length: 'None',
        limit_start: filterObj.value.limit_start,
        order_by: "`tabEzy Departments`.`creation` desc"
    };
   
    axiosInstance.get(apis.resource + doctypes.departments, { params: queryParams })
        .then((res) => {
            if (res.data) {

               
                designiations.value = [...new Set(res.data.map((designation) => designation.department_name))];
                departmenCodeData.value = [...new Set(res.data.map((designation) => designation.department_code))];


            }
        })
        .catch((error) => {
            console.error("Error fetching department data:", error);
        });
}


function deptData(data) {
    const filters = [
        ["business_unit", "like", `%${CreateDepartments.value.business_unit}%`]
    ];
    if (data) {
        filters.push(...data)
    }



    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify(filters),
        limit_page_length: filterObj.value.limitPageLength,
        limit_start: filterObj.value.limit_start,
        order_by: "`tabEzy Departments`.`creation` desc"
    };
    const queryParamsCount = {
        fields: JSON.stringify(["count(name) AS total_count"]),
        limitPageLength: "None",
        filters: JSON.stringify(filters),
    }
    axiosInstance.get(`${apis.resource}${doctypes.departments}`, { params: queryParamsCount })
        .then((res) => {
            // console.log(res.data[0].total_count);
            totalRecords.value = res.data[0].total_count

        })
        .catch((error) => {
            console.error("Error fetching ezyForms data:", error);
        });

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
    CreateDepartments.value.business_unit = businessUnit.value

}

function createDepart() {
    const dataObj = {
        ...CreateDepartments.value,
        "doctype": doctypes.departments
    }
    console.log(dataObj, "------------------");
    axiosInstance.post(apis.resource + doctypes.departments, dataObj).then((res) => {
        if (res.data) {
            toast.success("Department Created", { autoClose: 500, "transition": "zoom" })
            deptData()
            CreateDepartments.value = {
                department_code: "",
                department_name: "",
                ezy_departments_items: [
                ]
            }
        }

    })
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