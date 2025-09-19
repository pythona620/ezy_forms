<template>
    <div>
        <div class="d-flex justify-content-between align-items-center  py-2">
            <div>
                <h1 class="m-0 font-13">Departments</h1>
            </div>
            <div class="d-flex gap-2 align-items-center">
                <div class="d-flex align-items-center ">
                    <button type="button" class="btn btn-dark buttoncomp CreateDepartments d-flex align-items-center "
                        @click="CreateDeprtModal" data-bs-toggle="modal" data-bs-target="#viewCategory">
                        Create Department
                    </button>
                </div>
            </div>
        </div>
        <div class="mt-2">
            <GlobalTable :tHeaders="tableheaders" :tData="tableData" @actionClicked="actionCreated" isAction='true'
                :actions="actions" actionType="dropdown" isCheckbox="true" isFiltersoption="true"
                :field-mapping="fieldMapping" @updateFilters="inLineFiltersData" />
            <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords" :items-per-page="filterObj.limitPageLength"
                @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
        </div>

        <div class="modal fade" id="viewCategory" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
            aria-labelledby="viewCategoryLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h6 class="modal-title" id="viewCategoryLabel">Department</h6>
                        <button type="button" class="btn-close shadow-none" @click="clearModalData()" data-bs-dismiss="modal"
                            aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div>
                            <div class="mb-3">
                                <label class="font-13 ps-1" for="DepartmentCode">Department Code<span
                                        class="text-danger ps-1">*</span></label>
                                <FormFields tag="input" type="text" name="DepartmentCode" id="DepartmentCode"
                                    placeholder="Enter department code" v-model.trim="CreateDepartments.department_code" />
                                <span v-if="formErrors.department_code" class="text-danger font-12">
                                    {{ formErrors.department_code }}
                                </span>
                            </div>

                            <div class="mb-3">
                                <label class="font-13 ps-1" for="Requedepartment_namested">Department name<span
                                        class="text-danger ps-1">*</span></label>
                                <FormFields tag="input" type="text" name="department_name" id="department_name"
                                    placeholder="Enter department name" v-model.trim="CreateDepartments.department_name" />
                                <span v-if="formErrors.department_name" class="text-danger font-12">
                                    {{ formErrors.department_name }}
                                </span>
                            </div>

                            <label class="font-13 ps-1" for="business_unit">Business Unit</label>
                            <FormFields tag="input" type="text"
                                :disabled="CreateDepartments.business_unit ? true : false" placeholder="" class="mb-3"
                                name="business_unit" id="business_unit" v-model="CreateDepartments.business_unit" />
                        </div>
                        <label class="font-13 ps-1" for="Requedepartment_namested">Category<span class="text-danger ps-1">*</span></label>
                        <div class="d-flex w-100 gap-3">
                            <FormFields class="w-100" tag="input" type="text" name="ezy_departments_items"
                                id="ezy_departments_items" @keydown.enter="addCategoryInView" placeholder="Enter category" v-model.trim="newCategory" />
                            <ButtonComp class="buttoncomp" name="Add" @click="addCategoryInView" />
                        </div>

                        <table v-if="categoriesDataEdit.ezy_departments_items" class="table mt-3 global-table">
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
                                        <input type="text" class="shadow-none rounded-1" v-model.trim="editCategory" @change="saveEditForm(index)" placeholder="Enter Category" />
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
                        <!-- Save button (Edit Mode) -->
                        <button v-if="isEditMode" type="button"
                            class="applyfilter btn btn-dark text-nowrap font-10 d-flex justify-content-center align-items-center"
                            :disabled="!CreateDepartments.department_code || !CreateDepartments.department_name || !CreateDepartments.business_unit"
                            @click="UpdateDeprtment">
                            <span class="font-16 me-1"><i class="bi bi-check2"></i></span>
                            Save Department
                        </button>

                        <!-- Create button (Create Mode) -->
                        <button v-else type="button"
                            class="applyfilter btn btn-dark text-nowrap font-10 d-flex justify-content-center align-items-center"
                            :disabled="!CreateDepartments.department_code || !CreateDepartments.department_name || !CreateDepartments.business_unit"
                            @click="createDepart">
                            <span class="font-16 me-1"><i class="bi bi-check2"></i></span>
                            Create Department
                        </button>
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

const businessUnit = computed(() => {
    return EzyBusinessUnit.value;
});
const totalRecords = ref(0);

const tableData = ref([]);
const newCategory = ref("");
const editIndex = ref(null);
const editCategory = ref("");
const categoriesDataEdit = ref({ ezy_departments_items: [] });
const designiations = ref([]);
const actions = ref([{ name: 'View Categories', icon: 'fa-solid fa-eye' }]);

const formErrors = ref({
    department_code: "",
    department_name: ""
});
const departmenCodeData = ref([]);
const isEditMode = ref(false); // false = Create mode, true = Edit mode
const editingDepartmentId = ref(null); // optional: to track which department is being edited

const originalDepartmentCode = ref("");
const originalDepartmentName = ref("");

const filterObj = ref({
    limitPageLength: 20,
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


function clearModalData() {
    Object.assign(CreateDepartments.value, {
        department_code: "",
        department_name: "",
        ezy_departments_items: []
    });
    categoriesDataEdit.value.ezy_departments_items = [];
    newCategory.value = "";
}

const tableheaders = ref([
    { th: "Department Code", td_key: "department_code" },
    { th: "Department Name", td_key: "department_name" },
    { th: "Business Unit", td_key: "business_unit" },
])
const fieldMapping = ref({
    department_code: { type: "input" },
    department_name: { type: "input" },
    form_category: { type: "select", options: ["Software", "Hardware"] },

});
const CreateDepartments = ref({
    department_code: "",
    department_name: "",
    business_unit: "",
    ezy_departments_items: []
});

// Department Code Watcher
watch(() => CreateDepartments.value.department_code, (newVal) => {
    const trimmedVal = newVal.trim().toLowerCase();

    const existingCodes = departmenCodeData.value
        .filter(code => code !== null)
        .map(code => code.trim().toLowerCase());

    const originalVal = originalDepartmentCode.value.trim().toLowerCase();

    // Only check if value changed from original
    if (isEditMode.value && trimmedVal === originalVal) {
        formErrors.value.department_code = "";
    } else if (existingCodes.includes(trimmedVal)) {
        formErrors.value.department_code = "Department code already exists.";
    } else {
        formErrors.value.department_code = "";
    }
});


// Department Name Watcher
watch(() => CreateDepartments.value.department_name, (newVal) => {
    const trimmedVal = newVal.trim().toLowerCase();

    const existingNames = designiations.value
        .filter(name => name !== null)
        .map(name => name.trim().toLowerCase());

    const originalVal = originalDepartmentName.value.trim().toLowerCase();

    if (isEditMode.value && trimmedVal === originalVal) {
        formErrors.value.department_name = "";
    } else if (existingNames.includes(trimmedVal)) {
        formErrors.value.department_name = "Department name already exists.";
    } else {
        formErrors.value.department_name = "";
    }
});

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

function actionCreated(rowData, actionEvent) {
        CreateDeprtModal()
    if (actionEvent.name === 'View Categories') {
        isEditMode.value = true;
        originalDepartmentCode.value = rowData.department_code;
        originalDepartmentName.value = rowData.department_name;
        editingDepartmentId.value = rowData.id; // optional
        CreateDepartments.value = { ...rowData };
        // categoriesDataEdit.value.ezy_departments_items = [...rowData.ezy_departments_items];
        if (rowData) {
            CreateDepartments.value = { ...rowData }
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

function addCategoryInView() {
    if (newCategory.value) {
        categoriesDataEdit.value.ezy_departments_items.push({
            category: newCategory.value,
            parentfield: 'ezy_departments_items'
        });
        newCategory.value = "";
    }
}

function startEditForm(index, category) {
    editIndex.value = index;
    editCategory.value = category;
}

function saveEditForm(index) {
  const value = editCategory.value.trim();

  if (value) {
    categoriesDataEdit.value.ezy_departments_items[index].category = value;
  } else {
    // If the input is empty, remove the row
    categoriesDataEdit.value.ezy_departments_items.splice(index, 1);
  }

  // Reset the editing state regardless
  editIndex.value = null;
  editCategory.value = "";
}


function removeCategoryForm(index) {
    categoriesDataEdit.value.ezy_departments_items.splice(index, 1);
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
    filterObj.value.limit_start = 0; // Reset pagination to the first page
    filterObj.value.limitPageLength = 20; // Reset items per page to default
    if (filters.length) {
        deptData(filters);
    }
    else {
        deptData();
    }
    //   fetchTotalRecords(filters);
}


function CreateDeprtModal() {
    // openCreateModal()
    isEditMode.value = false;
    categoriesDataEdit.value.ezy_departments_items = [];
    CreateDepartments.value.business_unit = localStorage.getItem("Bu")

    const filters = [
        ["business_unit", "=", `${businessUnit.value}`]
    ];

    const queryParams = {
        fields: ["name","department_name", "department_code","business_unit"],
        filters: filters,
        limit_page_length: 999,
        limit_start: filterObj.value.limit_start,
        doctype:doctypes.departments,
        order_by: "`tabEzy Departments`.`creation` desc"
    };

    axiosInstance.post(apis.GetDoctypeData, queryParams)
        .then((res) => {
            if (res.message.data) {
                designiations.value = [...new Set(res.message.data.map((designation) => designation.department_name))];
                departmenCodeData.value = [...new Set(res.message.data.map((designation) => designation.department_code))];
            }
        })
        .catch((error) => {
            console.error("Error fetching department data:", error);
        });
}

function deptData(data) {
    const filters = [
        ["business_unit", "=", `${CreateDepartments.value.business_unit}`]
    ];
    if (data) {
        filters.push(...data)
    }
    const payload = {
        fields: ["name","department_code","department_name","business_unit"],
        filters: filters,
        limit_page_length: filterObj.value.limitPageLength,
        limit_start: filterObj.value.limit_start,
        doctype:doctypes.departments,
        order_by: "`tabEzy Departments`.`creation` desc"
    };

    axiosInstance.post(apis.GetDoctypeData, payload)
        .then((res) => {
            if (res) {
                totalRecords.value=res.message.total_count;
                tableData.value = res.message.data;
            }
        })
        .catch((error) => {
            console.error("Error fetching department data:", error);
        });
}

function createDepart() {
    if (editIndex.value !== null) {
        if (!editCategory.value.trim()) {
            removeCategoryForm(editIndex.value);
        } else {
            saveEditForm(editIndex.value);
        }
    }

    if (!categoriesDataEdit.value.ezy_departments_items || categoriesDataEdit.value.ezy_departments_items.length === 0) {
        toast.error("At least one category is required");
        return;
    }

    if (!formErrors.value.department_code && !formErrors.value.department_name) {
        CreateDepartments.value.ezy_departments_items = categoriesDataEdit.value.ezy_departments_items;
        const dataObj = {
            ...CreateDepartments.value,
            "doctype": doctypes.departments,

        }
        axiosInstance.post(apis.resource + doctypes.departments, dataObj).then((res) => {
            if (res.data) {
                toast.success("Department Created successfully", { autoClose: 500, "transition": "zoom" })
                deptData()
                CreateDepartments.value = {
                    department_code: "",
                    department_name: "",
                    ezy_departments_items: [],
                }
                CreateDepartments.value.business_unit = businessUnit.value
                newCategory.value = "";
                const modal = bootstrap.Modal.getInstance(document.getElementById('viewCategory'));
                modal.hide();
                CreateDepartments.value.business_unit = businessUnit.value;
            }

        })
    }
    else {
        toast.error("Please correct the required fields")
    }
}

function UpdateDeprtment() {
    if (editIndex.value !== null) {
        if (!editCategory.value.trim()) {
            removeCategoryForm(editIndex.value);
        } else {
            saveEditForm(editIndex.value);
        }
    }

    if (!categoriesDataEdit.value.ezy_departments_items || categoriesDataEdit.value.ezy_departments_items.length === 0) {
        toast.error("At least one category is required");
        return;
    }

    if (
        !CreateDepartments.value.department_code ||
        !CreateDepartments.value.department_name ||
        !CreateDepartments.value.business_unit ||
        formErrors.value.department_code ||
        formErrors.value.department_name
    ) {
        toast.error("Please correct the required fields", { autoClose: 1000, transition: "zoom" });
        return;
    }
        CreateDepartments.value.ezy_departments_items = categoriesDataEdit.value.ezy_departments_items;

        const dataObj = {
            ...CreateDepartments.value,
            doctype: doctypes.departments,
        };

        axiosInstance
            .put(`${apis.resource}${doctypes.departments}/${CreateDepartments.value.name}`, dataObj)
            .then((res) => {
                if (res.data) {
                    toast.success("Department Updated successfully", { autoClose: 500, transition: "zoom" });
                    deptData();

                    // Reset values
                    CreateDepartments.value = {
                        department_code: '',
                        department_name: '',
                        ezy_departments_items: []
                    };
                    newCategory.value = "";
                    const modal = bootstrap.Modal.getInstance(document.getElementById('viewCategory'));
                    modal.hide();
                }
            })
            .catch((error) => {
                console.error("Error updating department:", error.response?.data || error);
            });
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