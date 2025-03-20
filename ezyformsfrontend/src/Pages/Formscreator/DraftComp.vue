<template>
    <div>
        <div class="d-flex formsticky align-items-center justify-content-between py-2">
            <div>
                <h1 class="m-0 font-13">Forms in Draft</h1>
                <p class="m-0 font-11 pt-1">{{ totalRecords }} forms available</p>
            </div>
            <div class="d-flex align-items-center gap-2">



                <!-- <div class="d-flex align-items-center">
                    <ButtonComp class="buttoncomp" @click="formCreation()" name="Create form"></ButtonComp>
                </div> -->
            </div>
        </div>
        <!-- v-if="tableForm" -->
        <div class="mt-2">

            <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction="true" actionType="dropdown"  enableDisable="true"
                @actionClicked="actionCreated" isFiltersoption="true" :field-mapping="fieldMapping" :actions="actions" @toggle-click="toggleFunction"
                @updateFilters="inLineFiltersData" isCheckbox="true" />
            <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords"
                @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
        </div>


        <FormPreview :blockArr="selectedForm" :formDescriptions="formDescriptions" />


    </div>
</template>
<script setup>

import GlobalTable from "../../Components/GlobalTable.vue";
import { callWithErrorHandling, onMounted, ref, computed, watch, reactive } from "vue";
import PaginationComp from '../../Components/PaginationComp.vue'
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from "../../shared/apiurls";
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import { useRouter } from "vue-router";
import { rebuildToStructuredArray } from "../../shared/services/field_format";
import FormPreview from '../../Components/FormPreview.vue'
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";



const totalRecords = ref(0);
const formDescriptions = ref({})
const tableData = ref([]);
const accessibleDepartments = ref([]);
const ownerForms = ref([])
const router = useRouter();
const selectedForm = ref(null);
const businessUnit = computed(() => {
    return EzyBusinessUnit.value;
});
const sections = reactive([]);
onMounted(() => {
    // fetchTable()

})



function actionCreated(rowData, actionEvent) {
    if (actionEvent.name === 'View form') {
        if (rowData?.form_json) {
            formDescriptions.value = { ...rowData }
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
        // { name: 'Edit accessibility to dept.', icon: 'fa-solid fa-users' },
        // { name: 'Share this form', icon: 'fa-solid fa-share-alt' },
        // { name: 'Download Print format', icon: 'fa-solid fa-download' },
        // { name: 'In-active this form', icon: 'fa-solid fa-ban' }
    ]
)

const filterObj = ref({
    limit_start: 0,
    limitPageLength: 20,
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
    { th: "Status", td_key: "form_status" },
]);


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

function toggleFunction(rowData, rowIndex, event) {
    const isCurrentlyEnabled = rowData.enable == '1' || rowData.enable === 1;
    const actionText = isCurrentlyEnabled ? 'Disable' : 'Enable';

    if (confirm(`Are you sure you want to ${actionText} this Form?`)) {
        rowData.enable = isCurrentlyEnabled ? 0 : 1;

        axiosInstance
            .put(`${apis.resource}${doctypes.EzyFormDefinitions}/${rowData.name}`, rowData)
            .then((response) => {
                toast.success(`Form ${actionText}d successfully`, { autoClose: 700 });
                // setTimeout(() => {
                //     fetchTable();
                // }, 1000);
                window.location.reload()
            })
            .catch((error) => {
                console.error("Error updating toggle:", error);
            });
    } else {
        console.log("Action cancelled. Toggle remains unchanged.");
    }
}

const timeout = ref(null); // Store the timeout reference

function inLineFiltersData(searchedData) {
    // Clear the previous timeout to prevent multiple API calls
    clearTimeout(timeout.value);

    // Set a new timeout to delay the API call
    timeout.value = setTimeout(() => {
        // Initialize filters array
        const filters = [];

        // Loop through the table headers and build dynamic filters
        tableheaders.value.forEach((header) => {
            const key = header.td_key;

            // If there is a match for the key in searchedData, create a 'like' filter
            if (searchedData[key]) {
                filters.push(key, "like", `%${searchedData[key]}%`);
            }
        });

        // Fetch data with filters
        fetchTable(filters.length ? filters : undefined);

        // Optional: Fetch total records if needed
        // fetchTotalRecords(filters);
    }, 500); // Adjust debounce delay as needed (e.g., 500ms)
}
const formCategory = ref([]);



function fetchTable(data) {
    const filters = [
        ["business_unit", "like", `%${filterObj.value.business_unit}%`],
        ["form_status", "=", "Draft"],
        ["enable", "=", 1]
    ];
    if (data) {
        filters.push(data)
    }

    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify(filters),
        limit_page_length: filterObj.value.limitPageLength,
        limit_start: filterObj.value.limit_start,
        order_by: "`tabEzy Form Definitions`.`creation` desc"
    };
    const queryParamsCount = {
        fields: JSON.stringify(["count(name) AS total_count"]),
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
                

                ownerForms.value = [...new Set(newData.map((ownerForms) => ownerForms.owner_of_the_form))]
            } else {
                tableData.value = tableData.value.concat(newData);
            }
        })
        .catch(error => {
            console.error("Error fetching ezyForms data:", error);
        });
}

const fieldMapping  = computed(() => ({
    // invoice_type: { type: "select", options: ["B2B", "B2G", "B2C"] },
    // invoice_date: { type: "date" },
    form_category: { type: "select", options: formCategory.value },
    form_name: { type: "input" },
    owner_of_the_form: { type: "input" }

}));


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
