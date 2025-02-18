<template>
    <div>
        <div class="d-flex justify-content-between align-items-center formsticky py-2">
            <div>
                <h1 class="m-0 font-13">Forms Master</h1>
                <p class="m-0 font-11 pt-1">{{ totalRecords }} forms available</p>
            </div>
            <div class="d-flex gap-2 align-items-center">
                <div class="d-flex align-items-center ">
                    <ButtonComp class="buttoncomp" @click="formCreation()" name="Create form"></ButtonComp>
                </div>
            </div>
        </div>
        <!-- v-if="tableForm" -->
        <div class="mt-2">

            <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction="true" actionType="dropdown"
                @actionClicked="actionCreated" isFiltersoption="true" :field-mapping="fieldMapping" :actions="actions"
                @updateFilters="inLineFiltersData" isCheckbox="true" />
            <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords"
                @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
        </div>

        <div class="modal fade" id="pdfView" tabindex="-1" aria-labelledby="pdfViewLabel" aria-hidden="true">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="modal-header py-2 d-block bg-dark text-white">
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h5 class="m-0 text-white font-13" id="exampleModalLabel">
                                    PDF format
                                </h5>
                            </div>
                            <div class="">
                                <button button="button" class=" btn btn-dark text-white font-13"
                                    @click="downloadPdf">Download Pdf<span class=" ms-2"><i
                                            class="bi bi-download"></i></span> </button>
                                <button type="button" class="btn btn-dark text-white font-13" @click="closemodal"
                                    data-bs-dismiss="modal">Close
                                    <i class="bi bi-x"></i></button>
                            </div>
                        </div>
                    </div>
                    <div class="modal-body">

                        <div v-html="pdfPreview"></div>
                    </div>
                    <div class="modal-footer">

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
import { onMounted, ref, computed, watch, reactive } from "vue";
import PaginationComp from '../../Components/PaginationComp.vue'
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes, domain } from "../../shared/apiurls";
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import { useRouter } from "vue-router";
import { rebuildToStructuredArray } from "../../shared/services/field_format";
import FormPreview from '../../Components/FormPreview.vue'

const totalRecords = ref(0);
const pdfPreview = ref('')

const formDescriptions = ref({})
const tableData = ref([]);

const businessUnit = computed(() => {
    return EzyBusinessUnit.value;
});
const sections = reactive([]);
onMounted(() => {
    // fetchTable()
    fetchCategory()

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

watch(
    businessUnit,
    (newVal) => {
        filterObj.value.business_unit = newVal;

        if (newVal.length) {
            // console.log(newVal, "new value of business unit");
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

const router = useRouter();
const fieldMapping = ref({
    // invoice_type: { type: "select", options: ["B2B", "B2G", "B2C"] },
    // invoice_date: { type: "date" },
    form_name: { type: "input" },
    form_category: { type: "select", options: [] },
    owner_of_the_form: { type: "input" }

});
const selectedForm = ref(null);
const actions = ref([
    { name: 'View form', icon: 'fa-solid fa-eye' },
    { name: 'Edit Form', icon: 'fa-solid fa-edit' },
    { name: 'PDF Format', icon: 'bi bi-filetype-pdf' },
    // { name: 'Activate this form', icon: 'fa-solid fa-check-circle' },
    // { name: 'In-active this form', icon: 'fa-solid fa-ban' },
    // { name: 'Edit accessibility to dept.', icon: 'fa-solid fa-users' },
    // { name: 'Share this form', icon: 'fa-solid fa-share-alt' },
    // { name: 'Download Print format', icon: 'fa-solid fa-download' },
]);

function actionCreated(rowData, actionEvent) {
    if (actionEvent.name === 'View form') {
        if (rowData?.form_json) {
            formDescriptions.value = { ...rowData };
            // console.log(formDescriptions.value, "lllllllllll");
            selectedForm.value = rebuildToStructuredArray(JSON.parse(rowData?.form_json).fields);
            // console.log(selectedForm.value, "ooooo");
            const modal = new bootstrap.Modal(document.getElementById('formViewModal'), {});
            modal.show();
        } else {
            console.warn("There are no form fields");
            formCreation(rowData);
        }
    } else if (actionEvent.name === 'Edit Form') {
        formCreation(rowData);
    }
    else if (actionEvent.name === 'PDF Format') {
        // pdfView
        formDescriptions.value = rowData

        const dataObj = {
            "form_short_name": rowData.form_short_name
        };

        axiosInstance.post(apis.preview_dynamic_form, dataObj)
            .then((response) => {

                pdfPreview.value = response.message

            })
            .catch((error) => {
                console.error("Error fetching data:", error);
            });
        const modal = new bootstrap.Modal(document.getElementById('pdfView'), {});
        modal.show();
    }
    else if (actionEvent.name === 'Edit accessibility to dept.') {
        formCreation(rowData);
    }
    else if (actionEvent.name === 'In-active this form') {
        // Inactivate the form
        updateFormStatus(rowData, '0');
    } else if (actionEvent.name === 'Activate this form') {
        // Activate the form
        updateFormStatus(rowData, '1');
    }
}
function downloadPdf() {

    const dataObj = {
        "form_short_name": formDescriptions.value.form_short_name,
        "name": null
    };

    axiosInstance.post(apis.download_pdf_form, dataObj)
        .then((response) => {

            let pdfUrl = domain + response.message;

            // Remove 'api' from the URL if present
            pdfUrl = pdfUrl.replace('/api', '');

            // Create an anchor element to trigger the download
            const link = document.createElement('a');
            link.href = pdfUrl;
            link.download = response.message.split('/').pop(); // Use the file name from the URL
            link.click();
        })
        .catch((error) => {
            console.error("Error fetching data:", error);
        });
}

// Function to update the form status based on active/inactive
function updateFormStatus(rowData, status) {
    if (rowData) {
        const formId = rowData.name;
        const statusUpdate = { active: status };

        axiosInstance.put(`${apis.resource}${doctypes.EzyFormDefinitions}/${formId}`, statusUpdate)
            .then((res) => {

                fetchTable();
            })
            .catch((error) => {
                console.error("Error updating form status:", error);
            });
    }
}

const hideModal = () => {
    const modal = bootstrap.Modal.getInstance(document.getElementById('formViewModal'));
    modal.hide();
};

function inLineFiltersData(searchedData) {


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


    //   // Log filters to verify


    //   // Once the filters are built, pass them to fetchData function
    if (filters.length) {
        fetchTable(filters);
    }
    else {
        fetchTable();
    }
    //   fetchTotalRecords(filters);
}




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

async function fetchCategory() {
    try {
        // Fetch all department names
        const queryParams = { fields: JSON.stringify(["name"]) };
        const response = await axiosInstance.get(`${apis.resource}${doctypes.departments}`, { params: queryParams });

        if (response.data) {
            const departments = response.data;

            // Fetch full details of each department (including child table)
            const departmentDetailsPromises = departments.map(department =>
                axiosInstance.get(`${apis.resource}${doctypes.departments}/${department.name}`)
            );

            // Resolve all department requests
            const detailedResponses = await Promise.all(departmentDetailsPromises);
            const detailedDepartments = detailedResponses.map(res => res.data);

            // Extract all category names from child tables
            const allCategories = [];
            detailedDepartments.forEach(department => {

                if (department.ezy_departments_items) {
                    department.ezy_departments_items.forEach(child => {
                        if (child.category) {
                            allCategories.push(child.category);
                        }
                    });
                } else {
                    console.log("No child table found for:", department.name);
                }
            });


            // Remove duplicates and store in options
            fieldMapping.value.form_category.options = [...new Set(allCategories)];
            // console.log(fieldMapping.value.form_category.options, "======== Categories");
        }
    } catch (error) {
        console.error("Error fetching categories:", error);
    }
}



const formCategory = ref([]);
const accessibleDepartments = ref([]);
const ownerForms = ref([])
function fetchTable(data) {
    const filters = [
        ["business_unit", "like", `%${filterObj.value.business_unit}%`]
        // ["form_status", "=", "Draft"]
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
