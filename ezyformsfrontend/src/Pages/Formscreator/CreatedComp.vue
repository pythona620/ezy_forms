<template>
    <div>
        <div class="d-flex formsticky align-items-center justify-content-between py-2">
            <div>
                <h1 class="m-0 font-13">All Forms </h1>
                <p class="m-0 font-11 pt-1">{{ totalRecords }} forms available</p>
            </div>
            <div class="d-flex align-items-center gap-2">
                <div class="d-flex align-items-center">
                    <ButtonComp class="buttoncomp" @click="formCreation()" name="Create form"></ButtonComp>
                </div>
            </div>
        </div>
        <!-- v-if="tableForm" -->
        <div class="mt-2">

            <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction="true" actionType="dropdown"
                enableDisable="true" @actionClicked="actionCreated" @toggle-click="toggleFunction"
                isFiltersoption="true" :field-mapping="fieldMapping" :actions="actions"
                @updateFilters="inLineFiltersData" isCheckbox="true" />
            <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords"
                @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
        </div>

        <div class="modal fade" id="pdfView" tabindex="-1" aria-labelledby="pdfViewLabel" aria-hidden="true">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">
                    <div class="d-block modal-header bg-dark text-white py-2">
                        <div class="d-flex align-items-center justify-content-between">
                            <div>
                                <h5 class="m-0 text-white font-13" id="exampleModalLabel">
                                    PDF format
                                </h5>
                            </div>
                            <div class="">
                                <button button="button" class="btn btn-dark text-white font-13"
                                    @click="downloadPdf">Download Pdf<span class="ms-2"><i
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

        <FormPreview :blockArr="selectedForm" :formDescriptions="formDescriptions" :childHeaders="childtableHeaders" />


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
import { useRoute, useRouter } from "vue-router";
import { rebuildToStructuredArray } from "../../shared/services/field_format";
import FormPreview from '../../Components/FormPreview.vue'
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

const totalRecords = ref(0);
const pdfPreview = ref('')

const formDescriptions = ref({})
const tableData = ref([]);
const route = useRoute();
const businessUnit = computed(() => {
    return EzyBusinessUnit.value;
});
const sections = reactive([]);


onMounted(() => {
    // fetchTable()
    // fetchCategory()

})

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
            console.log(newVal, "new value of business unit");
            // localStorage.setItem("Bu", filterObj.value.business_unit)
            tableData.value = []
            fetchTable()
        }
    },
    { immediate: true }
);
const tableheaders = ref([
    { th: "Form name", td_key: "form_name" },
    { th: "Short Name", td_key: "form_short_name" },
    { th: "Form category", td_key: "form_category" },
    { th: "Owner of form", td_key: "owner_of_the_form" },
    { th: "Accessible departments", td_key: "accessible_departments" },
    { th: "Status", td_key: "form_status" },
]);

const router = useRouter();

const selectedForm = ref(null);
const actions = ref([
    { name: 'View form', icon: 'fa-solid fa-eye' },
    { name: 'Edit Form', icon: 'fa-solid fa-edit' },
    // { name: 'Download Print format', icon: 'fa-solid fa-download' },
    { name: 'Raise Request', icon: 'fa-solid fa-check-circle' },
    // { name: 'In-active this form', icon: 'fa-solid fa-ban' },
    // { name: 'Edit accessibility to dept.', icon: 'fa-solid fa-users' },
    // { name: 'Share this form', icon: 'fa-solid fa-share-alt' },
    // { name: 'Download Print format', icon: 'fa-solid fa-download' },
]);
const childtableHeaders = ref([]);

function actionCreated(rowData, actionEvent) {
    // console.log(rowData, actionEvent,"ppp");
    if (actionEvent.name === 'View form') {
        
        if (rowData?.form_json) {
            router.push({
        name: "FormPreviewComp",
        query: {
          routepath: route.path,
          form_short_name: rowData.form_short_name,

        },
      });
            // formDescriptions.value = { ...rowData };
            // // console.log(formDescriptions.value, "lllllllllll");
            // selectedForm.value = rebuildToStructuredArray(JSON.parse(rowData?.form_json).fields);


            // childtableHeaders.value = JSON.parse(
            //     rowData.form_json
            // ).child_table_fields;


            // // console.log(selectedForm.value, "ooooo");
            // const modal = new bootstrap.Modal(document.getElementById('formViewModal'), {});
            // modal.show();
        } else {
            console.warn("There are no form fields");
            formCreation(rowData);
        }
    } else if (actionEvent.name === 'Edit Form') {
        formCreation(rowData);
    }
    else if (actionEvent.name === 'Download Print format') {
        // pdfView
        formDescriptions.value = rowData

        const dataObj = {
            "form_short_name": rowData.form_short_name,
            business_unit: businessUnit.value

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
    if (actionEvent.name === 'Raise Request') {
        const parsedData = JSON.parse(rowData.form_json);
        const storedData = localStorage.getItem("employeeData");

        if (storedData) {
            const designation = JSON.parse(storedData).designation;
            // console.log(designation);

            const roles = parsedData.workflow[0].roles;
            // console.log(roles);

            let hasAccess = false;

            for (let i = 0; i < roles.length; i++) {
                if (roles[i] === designation) {
                    hasAccess = true;
                    break;
                }
            }

            if (hasAccess) {
                router.push({
                    name: "RaiseRequest",
                    query: {
                        routepath: route.path,
                        selectedForm: rowData.form_short_name,
                        business_unit: rowData.business_unit,

                    },
                });
            } else {
                toast.info("You are not assigned to raise a request.");

            }
        } else {
            console.log("No employee data found in localStorage.");
        }
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

function downloadPdf() {

    const dataObj = {
        "form_short_name": formDescriptions.value.form_short_name,
        "name": null,
        business_unit: businessUnit.value
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
const timeout = ref(null);
function inLineFiltersData(searchedData) {
    clearTimeout(timeout.value); // Clear previous timeout

    timeout.value = setTimeout(() => {
        const filters = [];

        tableheaders.value.forEach((header) => {
            const key = header.td_key;
            if (searchedData[key]) {
                filters.push(key, "like", `%${searchedData[key]}%`);
            }
        });

        fetchTable(filters.length ? filters : undefined);
    }, 500); // Delay API call by 500ms
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

// async function fetchCategory() {
//     try {
//         // Fetch all department names
//         const queryParams = { fields: JSON.stringify(["name"]) };
//         const response = await axiosInstance.get(`${apis.resource}${doctypes.departments}`, { params: queryParams });

//         if (response.data) {
//             const departments = response.data;

//             // Fetch full details of each department (including child table)
//             const departmentDetailsPromises = departments.map(department =>
//                 axiosInstance.get(`${apis.resource}${doctypes.departments}/${department.name}`)
//             );

//             // Resolve all department requests
//             const detailedResponses = await Promise.all(departmentDetailsPromises);
//             const detailedDepartments = detailedResponses.map(res => res.data);

//             // Extract all category names from child tables
//             const allCategories = [];
//             detailedDepartments.forEach(department => {

//                 if (department.ezy_departments_items) {
//                     department.ezy_departments_items.forEach(child => {
//                         if (child.category) {
//                             allCategories.push(child.category);
//                         }
//                     });
//                 } else {
//                     console.log("No child table found for:", department.name);
//                 }
//             });


//             // Remove duplicates and store in options
//             fieldMapping.value.form_category.options = [...new Set(allCategories)];
//             // console.log(fieldMapping.value.form_category.options, "======== Categories");
//         }
//     } catch (error) {
//         console.error("Error fetching categories:", error);
//     }
// }



const formCategory = ref([]);
const accessibleDepartments = ref([]);
const ownerForms = ref([])
function fetchTable(data) {
    const filters = [
        ["business_unit", "like", `%${filterObj.value.business_unit}%`],
        ["form_status", "=", "Created"]
    ];
    if (data) {
        filters.push(data)
    }


    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify(filters),
        limit_page_length: filterObj.value.limitPageLength,
        limit_start: filterObj.value.limit_start,
        order_by: "`tabEzy Form Definitions`.`enable` DESC, `tabEzy Form Definitions`.`creation` DESC"
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

const fieldMapping = computed(() => ({
    form_name: { type: "input" },
    form_short_name:{ type: "input" },
    form_category: { type: "input" },
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
