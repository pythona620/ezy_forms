<template>
    <div>
        <div class="d-flex justify-content-between align-items-center formsticky">
            <div>
                <h1 class="m-0 font-13">Forms Master</h1>
                <p class="m-0 font-11 pt-1">374 forms available</p>
            </div>
            <div class="d-flex gap-2 align-items-center">
                <div>
                    <FormFields labeltext="" class="" tag="input" type="search" placeholder="Search Form Name"
                        name="Value" id="Value" v-model="filterObj.search" @input="fetchTable()" />
                </div>
                <div>
                    <button type="button" class=" filterbtn d-flex align-items-center justify-content-between"
                        data-bs-toggle="modal" data-bs-target="#exampleModal">
                        <span> <i class="ri-filter-2-line"></i></span>
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
                            <div class="col-3">
                                <label class="font-13 ps-1" for="Requested">Requested By:</label>
                                <FormFields class="mb-3" tag="input" type="search" name="Requested" id="Requested"
                                    placeholder="Search" v-model="filterOnModal.Requested_id" />
                            </div>
                            <div class="col-3">
                                <label class="font-13 ps-1 fw-medium" for="dept">Requested Dept:</label>
                                <FormFields tag="select" placeholder="Select Department" class="mb-3" name="dept"
                                    v-model="filterOnModal.Requested_dept" id="dept" :Required="false"
                                    :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']" />
                            </div>
                            <div class="col-3">
                                <label class="font-13 ps-1" for="dept">Owner OF Form:</label>
                                <FormFields tag="input" type="search" placeholder="Select Department" class="mb-3"
                                    name="dept" v-model="filterOnModal.Owner_OF_Form" id="dept" :Required="false" />
                            </div>
                            <div class="col-3">
                                <label class="font-13 ps-1 " type="search" for="dept">Form Category:</label>
                                <FormFields tag="input" placeholder="Select Department" class="mb-3" name="dept"
                                    v-model="filterOnModal.Form_Category" id="dept" :Required="false" />
                            </div>
                            <div class="col-3">
                                <label class="font-13 ps-1" for="Requested">Form Name:</label>
                                <FormFields class="mb-3" tag="input" type="search" name="Requested" id="Requested"
                                    placeholder="Search" v-model="filterOnModal.Form_Name" />
                            </div>
                            <div class="col-3">
                                <label class="font-13 ps-1" for="Requested">Requested Period:</label>
                                <FormFields class="mb-3" tag="input" type="date" name="Requested" id="Requested"
                                    placeholder="Jan-2024-Dec-2024" v-model="filterOnModal.Requested_Period" />
                            </div>
                            <div class="col-3">
                                <FormFields tag="radio" :options="radioOptions" name="exampleRadio" id="exampleRadio"
                                    v-model="filterOnModal.Approval_status" labeltext="Approval Status" />
                            </div>
                            <div class="col-3">
                                <label class="font-13 ps-1" for="Requested">Requested Id:</label>
                                <FormFields class="mb-3" tag="input" type="search" name="Requested" id="Requested"
                                    placeholder="Search" v-model="filterOnModal.RequestedId" />
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="cancelfilter border-0 text-nowrap font-10 " @click="resetFilters"
                            data-bs-dismiss="modal"><span class="font-14 me-1">x</span>Cancel Filter</button>

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
import FormPreview from './FormPreview.vue'

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

const filterOnModal = ref({
    Requested_id: "",
    Requested_dept: "",
    Owner_OF_Form: "",
    Form_Category: "",
    Form_Name: "",
    Requested_Period: "",
    Approval_status: "",
    RequestedId: ""

})

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
const radioOptions = ref(["yes", "no"])
watch(
    businessUnit,
    (newVal) => {
        filterObj.value.business_unit = newVal;

        if (newVal.length) {
            console.log(newVal, "new value of business unit");
            localStorage.setItem("Bu", filterObj.value.business_unit)
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
function applyFilters() {
    fetchTable(); // Calls deptData to send filters
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
}
function fetchTable() {
    const filters = [
        ["business_unit", "like", `%${filterObj.value.business_unit}%`]
    ];
    if (filterObj.value.search.trim()) {
        filters.push(["name", "like", `%${filterObj.value.search}%`]);
    }
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
    if (filterOnModal.value.Form_Name) {
        filters.push(["name", "like", `%${filterOnModal.value.Form_Name}%`]);
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


.formsticky {
    position: sticky;
    top: 50px;
    z-index: 100;
    background: white;
}
</style>
