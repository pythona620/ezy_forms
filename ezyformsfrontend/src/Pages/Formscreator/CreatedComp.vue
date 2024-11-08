<template>
    <div>
        <div class="d-flex justify-content-between align-items-center formsticky">
            <div>
                <h1 class="m-0 font-13">Forms Master</h1>
                <p class="m-0 font-11 pt-1">{{ totalRecords }} forms available</p>
            </div>
            <div class="d-flex gap-2 align-items-center">
                <div>
                    <!-- <FormFields labeltext="" class="" tag="input" type="search" placeholder="Search Form Name"
                        name="Value" id="Value" v-model="filterObj.search" @input="fetchTable()" /> -->
                    <div class="me-2">
                        <span v-if="filterOnModal.form_name && filterOnModal.appliedform_name"
                            class="process-date font-12 m-0">
                            {{ filterOnModal.form_name }}
                            <span v-if="filterOnModal.form_name" class="badge badge-icon rounded-3   text-white "
                                @click="clearFilter('form_name')">
                                <i class="ri-close-line close-icon text-dark rounded-3"></i>
                            </span>
                        </span>
                        <span v-if="filterOnModal.form_category && filterOnModal.appliedform_category"
                            class="process-date font-12 m-0">
                            {{ filterOnModal.form_category }}
                            <span v-if="filterOnModal.form_category" class="badge badge-icon rounded-3   text-white "
                                @click="clearFilter('form_category')">
                                <i class="ri-close-line close-icon text-dark rounded-3"></i>
                            </span>
                        </span>
                        <span v-if="filterOnModal.accessible_departments && filterOnModal.appliedaccessible_departments"
                            class="process-date font-12 m-0">
                            {{ filterOnModal.accessible_departments }}
                            <span v-if="filterOnModal.accessible_departments"
                                class="badge badge-icon rounded-3   text-white "
                                @click="clearFilter('accessible_departments')">
                                <i class="ri-close-line close-icon text-dark rounded-3"></i>
                            </span>
                        </span>
                        <span v-if="filterOnModal.active && filterOnModal.appliedStatus"
                            class="process-date font-12 m-0">
                            {{ filterOnModal.active }}
                            <span v-if="filterOnModal.active" class="badge badge-icon rounded-3   text-white "
                                @click="clearFilter('active')">
                                <i class="ri-close-line close-icon text-dark rounded-3"></i>
                            </span>
                        </span>
                        <span v-if="filterOnModal.owner_of_the_form && filterOnModal.appledowner_of_the_form"
                            class="process-date font-12 m-0">
                            {{ filterOnModal.owner_of_the_form }}
                            <span v-if="filterOnModal.owner_of_the_form"
                                class="badge badge-icon rounded-3   text-white "
                                @click="clearFilter('owner_of_the_form')">
                                <i class="ri-close-line close-icon text-dark rounded-3"></i>
                            </span>
                        </span>
                    </div>
                </div>
                <div>
                    <button type="button" class=" filterbtn d-flex align-items-center position-relative "
                        data-bs-toggle="modal" data-bs-target="#exampleModal">
                        <span> <i class="ri-filter-2-line"></i></span>
                        <span v-if="appliedFiltersCount !== 0" class=" badge badge-light colorappiled ">
                            ( {{ appliedFiltersCount }})
                        </span>
                    </button>

                </div>

                <div class="d-flex align-items-center ">
                    <ButtonComp class="buttoncomp" @click="formCreation()" name="Create form"></ButtonComp>
                </div>
            </div>
        </div>
        <!-- v-if="tableForm" -->
        <div class="mt-2">

            <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction="true" actionType="dropdown"
                @actionClicked="actionCreated" :actions="actions" isCheckbox="true" />
            <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords"
                @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
        </div>
        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">

                    <div class="modal-body">
                        <div class="row">
                            <div class="col-4">
                                        <label class="font-13 ps-1" for="Requested">Form Name:</label>
                                        <FormFields class="mb-3" tag="input" type="search" name="Requested"
                                            id="Requested" placeholder="Search" v-model="filterOnModal.form_name" />
                                    </div>
                                    <div class="col-4">
                                        <label class="font-13 ps-1" for="dept">Form Category:</label>
                                        <FormFields tag="select" placeholder="Form Category" class="mb-3"
                                            name="dept" v-model="filterOnModal.form_category" id="dept" :Required="false"
                                            :options="formCategory" />
                                    </div>
                                    <div class="col-4">
                                        <label class="font-13 ps-1" for="dept">Accessible departments:</label>
                                        <!-- <FormFields tag="select" placeholder="Accessible departments" class="mb-3"
                                            name="dept" v-model="filterOnModal.accessible_departments" id="dept" :Required="false"
                                            :options="accessibleDepartments" /> -->
                                            <FormFields class="" tag="input" type="search" name="Requested"
                                            id="Requested" placeholder="Search" v-model="filterOnModal.accessible_departments" />
                                           <span class="m-0 font-10 ps-2">Note:Please seperate departments with commas</span>

                                    </div>
                                    <div class="col-4">
                                        <label class="font-13 ps-1" for="dept">Status:</label>
                                        <FormFields tag="select" placeholder="Status" class="mb-3"
                                            name="dept" v-model="filterOnModal.active" id="dept" :Required="false"
                                            :options="['Active','Draft']" />
                                    </div>
                                    <div class="col-4">
                                        <label class="font-13 ps-1" for="dept">Owner OF Form:</label>
                                        <FormFields tag="select" placeholder="Owner Of The Form" class="mb-3"
                                            name="dept" v-model="filterOnModal.owner_of_the_form" id="dept" :Required="false"
                                            :options="ownerForms" />
                                    </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="cancelfilter border-0 text-nowrap font-10 " @click="resetFilters"
                            data-bs-dismiss="modal"><span class="font-14 me-1">x</span>Cancel Filter</button>

                        <button type="button"
                            class="applyfilter text-nowrap border-0 btn btn-dark text-white font-10 d-flex justify-content-center align-items-center"
                            data-bs-dismiss="modal" @click="applyFilters"><span class="font-16 me-1"><i
                                    class="bi bi-check2 "></i></span>
                            Apply
                            Filter</button>
                    </div>
                </div>
            </div>
        </div>

        <FormPreview :blockArr="selectedForm" :formDescriptions="formDescriptions" />


    </div>
</template>
<script setup>
import FormFields from "../../Components/FormFields.vue";
import ButtonComp from "../../Components/ButtonComp.vue";
import GlobalTable from "../../Components/GlobalTable.vue";
import { callWithErrorHandling, onMounted, ref, computed, watch, reactive } from "vue";
import PaginationComp from '../../Components/PaginationComp.vue'
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from "../../shared/apiurls";
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import { useRouter } from "vue-router";
import { rebuildToStructuredArray } from "../../shared/services/field_format";
import FormPreview from '../../Components/FormPreview.vue'

const totalRecords = ref(0);

const businessUnit = computed(() => {
    return EzyBusinessUnit.value;
});
const sections = reactive([]);
onMounted(() => {
    // fetchTable()

})
const selectedForm = ref(null);
function actionCreated(rowData, actionEvent) {
    if (actionEvent.name === 'View form') {
        if (rowData?.form_json) {
            formDescriptions.value = { ...rowData }
            console.log(rowData, "iiiiiiiiiiiii");
            selectedForm.value = rebuildToStructuredArray(JSON.parse(rowData?.form_json).fields)
            const modal = new bootstrap.Modal(document.getElementById('formViewModal'), {});// raise a modal
            modal.show();

        } else {
            console.warn(" There is no form fields ")
            formCreation(rowData)
        }
    }
    if (actionEvent.name === 'Edit Form') {
        formCreation(rowData)
    }
}
const hideModal = () => {
    const modal = bootstrap.Modal.getInstance(document.getElementById('formViewModal'));
    modal.hide();
};


const actions = ref(
    [
        { name: 'View form', icon: 'fa-solid fa-eye' },
        { name: 'Edit Form', icon: 'fa-solid fa-edit' },
        { name: 'Edit accessibility to dept.', icon: 'fa-solid fa-users' },
        { name: 'Share this form', icon: 'fa-solid fa-share-alt' },
        { name: 'Download Print format', icon: 'fa-solid fa-download' },
        { name: 'In-active this form', icon: 'fa-solid fa-ban' }
    ]
)
const formDescriptions = ref({})
const tableData = ref([]);

const filterOnModal = reactive({
    appliedform_name: false,
    appliedform_category: false,
    appliedaccessible_departments: false,
    appliedStatus: false,
    appledowner_of_the_form: false,
    form_name: '',
    form_category: '',
    accessible_departments: '',
    active: '',
    owner_of_the_form: ''
})
const appliedFiltersCount = computed(() => {
    return [
        { value: filterOnModal.form_category, applied: filterOnModal.appliedform_category },
        {
            value: filterOnModal.form_name,
            applied: filterOnModal.appliedform_name,
        },
        {
            value: filterOnModal.active,
            applied: filterOnModal.appliedStatus,
        },
        {
            value: filterOnModal.accessible_departments,
            applied: filterOnModal.appliedaccessible_departments,
        },
        {
            value: filterOnModal.owner_of_the_form,
            applied: filterOnModal.appledowner_of_the_form,
        },


    ].filter((filter) => filter.applied && filter.value).length;
});
function clearFilter(type) {
    if (type === "form_name") {
        filterOnModal.form_name = "";
        filterOnModal.appliedform_name = false;
    } else if (type === "form_category") {
        filterOnModal.form_category = "";
        filterOnModal.appliedform_category = false;

    }
    else if (type === "accessible_departments") {
        filterOnModal.accessible_departments = "";
        filterOnModal.appliedaccessible_departments = false;

    }
    else if (type === "active") {
        filterOnModal.active = "";
        filterOnModal.appliedStatus = false;

    }
    else if (type === "owner_of_the_form") {
        filterOnModal.owner_of_the_form = "";
        filterOnModal.appledowner_of_the_form = false;

    }


    applyFilters();
}
function applyFilters() {
    filterOnModal.appliedform_name = Boolean(filterOnModal.form_name);
    filterOnModal.appliedform_category = Boolean(filterOnModal.form_category);
    filterOnModal.appliedaccessible_departments = Boolean(filterOnModal.accessible_departments);
    filterOnModal.appliedStatus = Boolean(filterOnModal.active);
    filterOnModal.appledowner_of_the_form = Boolean(filterOnModal.owner_of_the_form);




    // filterOnModal.applieddepartment_code=Boolean(filterOnModal.department_code);
    // filterOnModal.applieddepartment_name=Boolean(filterOnModal.department_name)

    fetchTable()
}
const filterObj = ref({
    limit_start: 0,
    limitPageLength: 100,
    form_name: "",
    form_short_name: "",
    accessible_departments: "[]",
    business_unit: '',
    form_category: "",
    owner_of_the_form: "",
    search: "",
});

watch(
    businessUnit,
    (newVal) => {
        filterObj.value.business_unit = newVal;

        if (newVal.length) {
            console.log(newVal, "new value of business unit");
            // localStorage.setItem("Bu", filterObj.value.business_unit)
            tableData.value = []
            fetchTable()
        }
    },
    { immediate: true }
);
const tableheaders = ref([
    { th: "Name", td_key: "name" },
    { th: "Form name", td_key: "form_name" },
    { th: "Form category", td_key: "form_category" },
    { th: "Owner of form", td_key: "owner_of_the_form" },
    { th: "Accessible departments", td_key: "accessible_departments" },
    { th: "Status", td_key: "active" },
]);

const router = useRouter();
function formCreation(item = null) {
    if (item == null) {
        router.push({ name: "FormStepper" });
    } else {
        router.push({
            name: "FormStepper",
            params: { paramid: item.name },

        });
    }
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
}
const formCategory = ref([]);
const accessibleDepartments = ref([]);
const ownerForms = ref([])
function fetchTable() {
    const filters = [
        ["business_unit", "like", `%${filterObj.value.business_unit}%`]
    ];
    if (filterOnModal.form_name) {
        filters.push(["form_name", "like", `%${filterOnModal.form_name}%`]);
    }
    if (filterOnModal.form_category) {
        filters.push(["form_category", "like", `${filterOnModal.form_category}`]);
    }
    if (filterOnModal.accessible_departments) {
        filters.push(["accessible_departments", "like", `${filterOnModal.accessible_departments}`]);
    }
    if (filterOnModal.active) {
        filters.push(["active", "like", `${filterOnModal.active}`]);
    }
    if (filterOnModal.owner_of_the_form) {
        filters.push(["owner_of_the_form", "like", filterOnModal.owner_of_the_form]);
    }

    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify(filters),
        limit_page_length: filterObj.value.limitPageLength,
        limit_start: filterObj.value.limit_start,
        order_by: "`tabEzy Form Definitions`.`creation` desc"
    };
    const queryParamsCount = {
        fields: JSON.stringify(["count( `tabEzy Form Definitions`.`name`) AS total_count"]),
        limitPageLength: "None",
        filters: JSON.stringify(filters),
    }
    axiosInstance.get(`${apis.resource}${doctypes.EzyFormDefinitions}`, { params: queryParamsCount })
        .then((res) => {
            // console.log(res.data[0].total_count);
            totalRecords.value = res.data[0].total_count

        })
        .catch((error) => {
            console.error("Error fetching ezyForms data:", error);
        });


    axiosInstance.get(`${apis.resource}${doctypes.EzyFormDefinitions}`, { params: queryParams })
        .then(res => {
            const newData = res.data;
            if (filterObj.value.limit_start === 0) {
                tableData.value = newData;
                formCategory.value = [...new Set(newData.map((formCategory) => formCategory.form_category))];
     
ownerForms.value=[...new Set(newData.map((ownerForms)=>ownerForms.owner_of_the_form))]
            } else {
                tableData.value = tableData.value.concat(newData);
            }
        })
        .catch(error => {
            console.error("Error fetching ezyForms data:", error);
        });
}

</script>

<style scoped>
.filterbtn {
    border: 1px solid #CCCCCC;
    font-size: 16px;
    border-radius: 4px;
    color: #999999;
    padding: 8px;
    width: 100%;
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

/* 
.formsticky {
    position: sticky;
    top: 50px;
    z-index: 100;
    background: white;
} */
</style>
