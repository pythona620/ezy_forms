<template>
    <div>
        <div class="d-flex formsticky align-items-center justify-content-between py-2">
            <div>
                <h1 class="m-0 font-13 py-2">Form Template</h1>
            </div>

        </div>
        <!-- v-if="tableForm" -->
        <div class="mt-2">

            <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction="true" view="edit"
                @cell-click="viewPreview" isFiltersoption="true" :field-mapping="fieldMapping" :actions="actions"
                @updateFilters="inLineFiltersData" isCheckbox="true" />
            <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords" :items-per-page="filterObj.limitPageLength"
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

        <div class="modal fade" id="FormSetupModal" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Form Setup</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="text-center">
                            Are you sure you want to set up the <strong>{{ formData.form_name }}</strong><br>
                        </div>

                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-dark" @click="SetupForm()">
                            Yes, Proceed
                        </button>
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
const pdfPreview = ref('');
const formData = ref("");
const formCategory = ref([]);
const accessibleDepartments = ref([]);
const ownerForms = ref([])

const formDescriptions = ref({})
const tableData = ref([]);
const route = useRoute();
const newChngedValue = ref('')
const router = useRouter();
const selectedForm = ref(null);
const childtableHeaders = ref([]);
const actions = ref([]);
const businessUnit = computed(() => {
    return EzyBusinessUnit.value;
});
const sections = reactive([]);


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

const tableheaders = ref([
    { th: "Form name", td_key: "form_name" },
    { th: "Installed", td_key: "installed" },
]);

watch(
    businessUnit,
    (newVal) => {
        filterObj.value.business_unit = newVal;

        if (newVal.length) {
            newChngedValue.value = newVal
            // localStorage.setItem("Bu", filterObj.value.business_unit)
            tableData.value = []
            fetchTable()
        }
    },
    { immediate: true }
);

function viewPreview(rowData, rowIndex, type) {
  formData.value = rowData;

  if (type === 'edit' && formData.value.installed === 'No') {
    const modal = new bootstrap.Modal(document.getElementById('FormSetupModal'), {});
    modal.show();
  }

  if (type === 'FormPreview') {
    router.push({
      name: "FormPreviewComp",
      query: {
        routepath: route.path,
        form_short_name: rowData.form_name,
        business_unit: businessUnit.value,
      },
    });
  }
}


function SetupForm() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('FormSetupModal'));
    modal.hide();

    router.push({
        name: "FormStepper",
        query: {
            routepath: route.path,
            preId: 'PreDefine',
            business_unit: businessUnit.value,
            form_name: formData.value.form_name,
            preName: formData.value.name
        },
    });
    localStorage.setItem("form_json", formData.value.form_json)
    localStorage.setItem("preName", formData.value.name)
    localStorage.setItem("routepath", route.path)
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


const timeout = ref(null);
function inLineFiltersData(searchedData) {
    clearTimeout(timeout.value); // Clear previous timeout

    timeout.value = setTimeout(() => {
        const filters = [];

        tableheaders.value.forEach((header) => {
            const key = header.td_key;
            if (searchedData[key]) {
                filters.push([key, "like", `%${searchedData[key]}%`]);
            }
        });

        fetchTable(filters.length ? filters : undefined);
    }, 500); // Delay API call by 500ms
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

function fetchTable(data) {
    const filters = [

    ];
    if (data) {
        filters.push(...data)
    }


    const queryParams = {
        fields: JSON.stringify(["form_name", "installed","form_json","name"]),
        filters: JSON.stringify(filters),
        limit_page_length: "None",
        limit_start: filterObj.value.limit_start,
        order_by: "`installed` DESC",

    };
    const queryParamsCount = {
        fields: JSON.stringify(["count(name) AS total_count"]),
        limitPageLength: "None",
        filters: JSON.stringify(filters),
    }
    axiosInstance.get(`${apis.resource}${doctypes.preDefinedForm}`, { params: queryParamsCount })
        .then((res) => {

            totalRecords.value = res.data[0].total_count

        })
        .catch((error) => {
            console.error("Error fetching ezyForms data:", error);
        });


    axiosInstance.get(`${apis.resource}${doctypes.preDefinedForm}`, { params: queryParams })
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
    installed: { type: "input" },
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
