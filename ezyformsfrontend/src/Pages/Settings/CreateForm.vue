<template>
  <div class="">
    <div>
      <div class="d-flex align-items-center justify-content-between py-3">
        <div>
          <h1 class="m-0 font-13">
            <!-- {{ id === 'allforms' ? 'All Forms' : id }}  -->
            All Forms
          </h1>
          <p class="m-0 font-11 pt-1">
            {{ totalRecords }} Forms Available
          </p>
        </div>
        <div v-if="is_admin == 1" class="d-flex align-items-center gap-2">
          <div class="d-flex align-items-center gap-2">
            <!-- <button class="btn btn-dark font-12 h-auto" @click="toWorkOrder">Work order</button>  -->
            <ButtonComp class="buttoncomp" @click="formCreation()" name="Create Form"></ButtonComp>
          </div>
        </div>

      </div>
      <div class="mt-1">
        <GlobalTable :tHeaders="tableheaders" :tData="tableData" isCheckbox="true" isAction="true" actionType="dropdown"
          @actionClickedDropDown="actionClickedDropDown" raiseRequest="true" :enableDisable="isEnable"
          @cell-click="viewPreview" @actionClicked="actionCreated" @toggle-click="toggleFunction" :actions="actions"
          @updateFilters="inLineFiltersData" :field-mapping="fieldMapping" isFiltersoption="true" />
        <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords" :items-per-page="filterObj.limitPageLength"
          @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
      </div>

    </div>
    <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="offcanvasRightLabel">Asset Request Form</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body">
        <div class="d-flex align-items-baseline position-relative gap-3">
          <div class="d-flex flex-column">
            <span>
              <i class="dashedcircle ri-checkbox-blank-circle-fill"></i>
            </span>
            <div class="dashed_line mt-4"></div>
          </div>
          <div>data</div>
        </div>
      </div>
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
                <button button="button" class="btn btn-dark text-white font-13" @click="downloadPdf">Download Pdf<span
                    class="ms-2"><i class="bi bi-download"></i></span> </button>
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
    <!-- Button trigger modal -->
    <!-- <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#EnableDisable">
      Launch demo modal
    </button> -->

    <!-- Modal -->
    <div class="modal fade" id="EnableDisable" tabindex="-1" aria-labelledby="EnableDisableLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="EnableDisableLabel">Confirm Action</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Are you sure you want to <span id="actionTextSpan"></span> <span class=" fw-bold font-13"
              id="rowNameSpan"></span> Form?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-dark" @click="confirmAction">Yes, Proceed</button>

          </div>
        </div>
      </div>
    </div>
  
   <div class="modal fade" id="reportmodal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1" aria-labelledby="reportmodalLabel" aria-hidden="true">
  <div class="modal-dialog modal-dialog-centered modal-lg">
    <div class="modal-content">
      <div class="modal-header">
        <h5 class="modal-title font-16" id="reportmodalLabel">Report Creation</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
      </div>
      <div class="modal-body">
       <div class="d-flex justify-content-between align-items-center mb-2">
  <p class="font-13 mb-0">Select the fields you want to include in the report:</p>

  <div class="form-check m-0">
    <input
      id="select-all-fields"
      type="checkbox"
      class="form-check-input me-1"
      v-model="selectAll"
      @change="toggleSelectAll"
    />
    <label for="select-all-fields" class="form-check-label font-12">Select All Fields</label>
  </div>
</div>

        <div class="report-fields row">
          <div 
            v-for="(field, index) in reportFields" 
            :key="index" 
            class="col-md-4 mb-3"
          >
          <div class="d-flex align-items-center">
            <input
              :id="'field-' + index"
              type="checkbox"
              class="form-check-input me-2"
              v-model="field.selected"
            />
            <label :for="'field-' + index" class="form-label font-12 mb-0">
              {{ getDisplayLabel(field) }}
            </label>
          </div>
        </div>

        </div>
      </div>

      <div class="modal-footer">
        <button type="button" class="btn btn-light font-13" data-bs-dismiss="modal">Close</button>
        <button type="button" class="btn btn-dark font-13 text-white" @click="generateReport">Generate Report</button>
      </div>
    </div>
  </div>
</div>
  </div>
</template>

<script setup>
import { ref, computed, watch, reactive, onMounted } from 'vue';
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes, domain } from '../../shared/apiurls';
import GlobalTable from '../../Components/GlobalTable.vue';
import { EzyBusinessUnit } from '../../shared/services/business_unit';
import { rebuildToStructuredArray } from '../../shared/services/field_format';
import PaginationComp from "../../Components/PaginationComp.vue"
import FormPreview from '../../Components/FormPreview.vue'
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import router from '../../router';
import { useRoute } from 'vue-router';
import ButtonComp from '../../Components/ButtonComp.vue';
import { showError, showInfo, showSuccess, showWarning } from '../../shared/services/toast';
const totalRecords = ref(0);
const tableheaders = ref([
  { th: "Form Name", td_key: "form_name" },
  { th: "Form Short Code", td_key: "form_short_name" },
  // { th: "Form Category", td_key: "form_category" },
  { th: "Accessible Departments", td_key: "accessible_departments" },
  { th: "Status", td_key: "form_status" },
  // { th: "Form Status", td_key: "enable" },

]);
const props = defineProps(['id']);
const formDescriptions = ref({})
const selectedForm = ref(null);
const tableData = ref([]);
const formCategory = ref([]);
const route = useRoute();
const pdfPreview = ref('')

const childtableHeaders = ref([]);
const is_admin = ref('');
const isEnable = ref("");
const reportFields = ref([])
const responcedata = ref([]);
const selectAll = ref(false);
// Toggle function triggered when a checkbox is clicked
const selectedRowData = ref(null);
const selectedActionText = ref('');
// Business unit and filter object
const businessUnit = computed(() => {
  return EzyBusinessUnit.value});
const newBusinessUnit = ref('');
const filterObj = ref({ limitPageLength: 20, limit_start: 0, filters: [] });



const fieldMapping = ref({
  // invoice_type: { type: "select", options: ["B2B", "B2G", "B2C"] },
  form_short_name: { type: "input" },
  form_category: { type: "input" },
  form_status: { type: "select", options: ["Active", "Retired"] },
  form_name: { type: "input" },
  enable: { type: "select", options: ["Enabled", "Disabled"] }

  // requested_on: { type: "date" },
});
function formCreation(item = null) {
  if (item == null) {
    router.push({
      name: "FormStepper", query: {
        routepath: route.path,
        business_unit: businessUnit.value,

      },
    });

  } else {
    router.push({
      name: "FormStepper",
      params: { paramid: item.name },
      query: {
        routepath: route.path,
        business_unit: businessUnit.value,
        id: item.name

      }

    });
  }
  localStorage.setItem('routepath', route.path)
}

function toWorkOrder (){
  router.push({
    name: "vendorcomparison",
 
      });
} 
function viewPreview(data, index, type) {
  // console.log(route.path);
  if (type === "view") {
    if (data) {
      // console.log(data, "------------");
      router.push({
        name: "FormPreviewComp",
        query: {
          routepath: route.path,
          form_short_name: data.form_short_name,
          business_unit: businessUnit.value,

        },
      });
    }
  }
  if (type === 'raiseRequest') {
    const parsedData = JSON.parse(data.form_json);
    const storedData = localStorage.getItem("employeeData");
    // console.log(parsedData);

    if (storedData) {
      const designation = JSON.parse(storedData).designation;
      // console.log(designation);

      if (!parsedData.workflow.length) {
        showInfo("No Roles Added")
      }
      const roles = parsedData.workflow[0].roles;
      // console.log(roles);

      let hasAccess = false;

      for (let i = 0; i < roles.length; i++) {
        if (roles[i] === designation) {
          hasAccess = true;
          break;
        }
      }
      // console.log(route.path, "sadasda");

      if (hasAccess) {
        router.push({
          name: "RaiseRequest",
          query: {
            routepath: route.path,
            selectedForm: data.form_short_name,
            business_unit: data.business_unit,


          },
        });
      } else {
        showInfo("You do not have permission to access this Form.");
      }
    }
    //  else {
    //   console.log("No employee data found in localStorage.");
    // }
  }


}


const actions = ref([]);

function actionClickedDropDown(row) {
  const baseActions = [
    { name: 'View form', icon: 'fa-solid fa-eye' },

  ];

  if (row.form_status === 'Created') {
    baseActions.push({ name: 'Raise Request', icon: 'fa fa-file-text'})
    baseActions.push({ name: 'In-active this form', icon: 'fa-solid fa-ban' });
  }
  if (row.form_status === 'Draft') {
    baseActions.push({ name: 'Actived this form', icon: 'fa-solid fa-check' });
  }
  if (is_admin.value == 1) {
    baseActions.push({ name: 'Edit Form', icon: 'fa-solid fa-edit' });
  }
  if (is_admin.value == 1) {
     baseActions.push({ name: 'Create Report', icon: 'fa fa-file-text' });
   }  

  actions.value = baseActions;

}

function toggleSelectAll() {
  reportFields.value.forEach(field => {
    field.selected = selectAll.value;
  });
}

// ✅ Watch for manual changes
watch(
  () => reportFields.value.map(f => f.selected),
  (newVals) => {
    // If every field is selected -> selectAll = true
    if (newVals.every(v => v)) {
      selectAll.value = true;
    } else {
      // If even one field is unselected -> selectAll = false
      selectAll.value = false;
    }
  },
  { deep: true }
);

function getDisplayLabel(field) {
  const suffixMatch = field.fieldname.match(/_(\d+)$/);
  const suffixNumber = suffixMatch ? parseInt(suffixMatch[1]) + 1 : null;

  // Check if this field belongs to the "Approver" group
  const approverGroup = ["approver", "approved_on", "approved_by"];
  const baseField = field.fieldname.replace(/_\d+$/, "");

  if (approverGroup.includes(baseField)) {
    // Add number: if has suffix (_1) → 2, else → 1
    return suffixNumber ? `${field.label} ${suffixNumber}` : `${field.label} 1`;
  }

  // For all other fields, just show the label
  return field.label;
}

// function actionClickedDropDown(row){

//   console.log(row.form_status, "actionClickedDropDown");
//   if(row.form_status === 'Created'){
//     actions.value.push({ name: 'In-active this form', icon: 'fa-solid fa-ban' });
//   }
//   if(row.form_status === 'Draft'){
//     actions.value.push({ name: 'Active this form', icon: 'fa-solid fa-check' });
//   }
// }

// const actions = computed(() => {
//   const baseActions = [
//     { name: 'View form', icon: 'fa-solid fa-eye' },
//     { name: 'Raise Request', icon: 'fa fa-file-text' },

//   ]


//   return baseActions
// })
const reportShortCode = ref('');
function actionCreated(rowData, actionEvent) {
  if (actionEvent.name === 'View form') {
    if (rowData) {
      // formDescriptions.value = { ...rowData }
      // selectedForm.value = rebuildToStructuredArray(JSON.parse(rowData?.form_json).fields)
      // childtableHeaders.value = JSON.parse(
      //     rowData.form_json
      //   ).child_table_fields;
      // const modal = new bootstrap.Modal(document.getElementById('formViewModal'), {});// raise a modal
      // modal.show();


      router.push({
        name: "FormPreviewComp",
        query: {
          routepath: route.path,
          form_short_name: rowData.form_short_name,
          business_unit: businessUnit.value,

        },
      });

    } else {
      showWarning(" There is no form fields ")
    }
  }
  else if (actionEvent.name === 'Edit Form') {
    formCreation(rowData);
  }

  if (actionEvent.name === 'Raise Request') {
    // console.log(rowData);
    const parsedData = JSON.parse(rowData.form_json);
    const storedData = localStorage.getItem("employeeData");

    if (storedData) {
      const designation = JSON.parse(storedData).designation;
      // console.log(designation);
      if (!parsedData.workflow?.length) {
        showInfo("No Roles Added");
      }
      const roles = parsedData.workflow[0].roles;
      // console.log(roles);

      let hasAccess = false;

      for (let i = 0; i < roles.length; i++) {
        if (roles[i] === designation) {
          hasAccess = true;
          break;
        }
      }
      // console.log(route.path, "sadasda");

      if (hasAccess && rowData.enable === 1) {
        if(rowData.form_name === 'VENDOR COMPARISON'){
            router.push({
          name: "vendorcomparison",
 
          });

        } else{
          router.push({
            name: "RaiseRequest",
            query: {
              routepath: route.path,
              selectedForm: rowData.form_short_name,
              business_unit: rowData.business_unit,
              has_workflow: rowData.has_workflow
              
              
            },
          });
        }
      } else if (rowData.enable === 0) {
        showInfo("This form is currently disabled.");
      } else {
        showInfo("You do not have permission to access this Form.");
      }
    }
    //  else {
    //   console.log("No employee data found in localStorage.");
    // }
  }

  if (actionEvent.name === 'Download Print format') {
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
  if (actionEvent.name === 'Actived this form') {
    toggleFunction(rowData, null, null);
  }
  if (actionEvent.name === 'In-active this form') {
    toggleFunction(rowData, null, null);
  }
if (actionEvent.name === 'Create Report') {
  console.log(rowData, "rowData");

  // Store document name for PUT request
  reportShortCode.value = rowData.name;

  // Parse all available fields from form_json
  const fields = JSON.parse(rowData?.form_json)?.fields || [];

  // Convert saved report_fields string into an array of fieldnames
  let alreadySelected = [];
  if (rowData.report_fields) {
    alreadySelected = rowData.report_fields
      .split(",")
      .map(item => item.trim().split(" as ")[0]); // ["requested_by", "requested_on", "file_one"]
  }
  

  // Filter valid fields and mark them as selected if previously saved
  reportFields.value = fields
    .filter(f => f.label && f.fieldtype !== "Column Break" && f.fieldtype !== "Section Break")
    .map(f => ({
      ...f,
      selected: alreadySelected.includes(f.fieldname) // pre-check
    }));

  // Open the modal
  const modal = new bootstrap.Modal(document.getElementById("reportmodal"), {});
  modal.show();
}

}
async function generateReport() {
  // collect only selected fields
  const selectedFields = reportFields.value
    .filter(f => f.selected)
    .map(f => `${f.fieldname} as '${f.label}'`);

  // add static field
  selectedFields.unshift("Name as name"); // or push() if you want it at the end

  const payload = selectedFields.join(","); // comma separated string

  const data = {};
  if (payload) {
    data.report_fields = payload;
  }

  try {
    const response = await axiosInstance.put(
      apis.resource + doctypes.EzyFormDefinitions + `/${reportShortCode.value}`,
      data
    );

    console.log("Report fields updated:", response.data);

    // close modal
    const modal = bootstrap.Modal.getInstance(document.getElementById('reportmodal'));
    if (modal) modal.hide();

    // show success toast
    showSuccess("Report Created Successfully");
  } catch (error) {
    console.error("Error updating report fields:", error);
    showError("Failed to update report fields");
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



function toggleFunction(rowData, rowIndex, event) {
  selectedRowData.value = rowData;
  const isCurrentlyEnabled = rowData.enable == '1' || rowData.enable === 1;
  selectedActionText.value = isCurrentlyEnabled ? 'Disable' : 'Restore';

  document.getElementById('actionTextSpan').innerText = selectedActionText.value;
  document.getElementById('rowNameSpan').innerText = rowData.name;

  const modal = new bootstrap.Modal(document.getElementById('EnableDisable'));
  modal.show();
  window.currentModal = modal;
}

function confirmAction() {
  if (!selectedRowData.value) return;

  const isCurrentlyEnabled = selectedRowData.value.enable == '1' || selectedRowData.value.enable === 1;
  selectedRowData.value.enable = isCurrentlyEnabled ? 0 : 1;
  selectedRowData.value.form_status = isCurrentlyEnabled ? 'Draft' : 'Created';

  axiosInstance
    .put(`${apis.resource}${doctypes.EzyFormDefinitions}/${selectedRowData.value.name}`, selectedRowData.value)
    .then((response) => {
      responcedata.value = response.data;
      showSuccess(`Form ${selectedActionText.value}d successfully`);
      setTimeout(() => {
        fetchDepartmentDetails();
      }, 1000);
      if (window.currentModal) window.currentModal.hide();
    })
    .catch((error) => {
      console.error("Error updating toggle:", error);
    });
}



// Watch business unit and department ID changes
// watch(
//   businessUnit.value,
//   (newBusinessUnitVal) => {
//     businessUnit.value = newBusinessUnitVal;
//     fetchDepartmentDetails();
//   },
//   { immediate: true }
// );
watch(
  businessUnit,
  (newVal) => {
    if (newVal && newVal.length) {
      newBusinessUnit.value = newVal;
    fetchDepartmentDetails();
    }
  },
  { immediate: true }
);

// watch(
//   [() => businessUnit.value, () => props.id],
//   ([newBusinessUnitVal, newId]) => {
//     newBusinessUnit.value.business_unit = newBusinessUnitVal;
//     // if (newBusinessUnitVal.length && newId && props.id !== ':id') {
//     //   filterObj.value.limit_start = 0;
//     //   filterObj.value.filters = [];
//     fetchDepartmentDetails();
//     // }
//   },
//   { immediate: true }
// );

// Handle updating the current value
const PaginationUpdateValue = (itemsPerPage) => {
  filterObj.value.limitPageLength = itemsPerPage;
  filterObj.value.limit_start = 0;

  
      fetchDepartmentDetails(filterObj.value.filters); 
   
};
// Handle updating the limit start
const PaginationLimitStart = ([itemsPerPage, start]) => {
  filterObj.value.limitPageLength = itemsPerPage;
  filterObj.value.limit_start = start;
  
      fetchDepartmentDetails(filterObj.value.filters); 
   
};


const timeout = ref(null);

function inLineFiltersData(searchedData) {
  clearTimeout(timeout.value); // Clear previous timeout

  timeout.value = setTimeout(() => {
    filterObj.value.filters = [];


    // Loop through the table headers and build dynamic filters
    if (searchedData.form_status === 'Active') {
      filterObj.value.filters.push(["form_status", "like", "Created"]);
    }
    if (searchedData.form_status === 'Retired') {
      filterObj.value.filters.push(["form_status", "like", "Draft"]);
    }
    // console.log(searchedData.enable);
    if (searchedData.enable === 'Enabled') {
      filterObj.value.filters.push(["enable", "=", 1]);
    } else if (searchedData.enable === 'Disabled') {
      filterObj.value.filters.push(["enable", "=", 0]);
    }


    // Loop through other table headers and add filters
    tableheaders.value.forEach((header) => {
      const key = header.td_key;
      const value = searchedData[key];

      if (key === 'form_status' || key === 'enable') return; // Skip since we already handled it above

      if (value) {
        filterObj.value.filters.push([key, "like", `%${value}%`]);
      }
    });

    // Call fetchDepartmentDetails with or without filters
    
      filterObj.value.limit_start = 0; // Reset pagination
      filterObj.value.limitPageLength = 20; // Reset pagination
      fetchDepartmentDetails(filterObj.value.filters);
    
  }, 500); // Adjust debounce delay as needed
}

function fetchDepartmentDetails(data) {

  filterObj.value.filters = [
    ["business_unit", "=", `${businessUnit.value}`],


  ];
  
  if (data) {
    
    filterObj.value.filters.push(...data);
  }

  const queryParams = {
    fields: JSON.stringify(["name",
              "business_unit",
              "form_category",
              "owner_of_the_form",
              "active",
              "count",
              "accessible_departments",
              "form_short_name",
              "form_json",
              "form_name",
              "form_status",
              "enable",
              "print_format",
              "is_landscape",
              "has_workflow",
              "workflow_check",
              "is_linked",
              "is_linked_form",
              "form_department",
              "series",
              "report_fields"
]),
    limit_page_length: filterObj.value.limitPageLength,
    limit_start: filterObj.value.limit_start,
    filters: JSON.stringify(filterObj.value.filters),
    doctype:doctypes.EzyFormDefinitions,
    order_by: "`tabEzy Form Definitions`.`enable` DESC, `tabEzy Form Definitions`.`creation` DESC"
  };

  axiosInstance.get(apis.GetDoctypeData, { params: queryParams })
    .then((response) => {
      totalRecords.value=response.message.total_count;
      if (filterObj.value.limit_start === 0) {
        tableData.value = response.message.data;
        formCategory.value = [...new Set(tableData.value.map((formCategory) => formCategory.form_category))];

      } else {
        tableData.value = tableData.value.concat(response.message.data);
      }
    })
    .catch((error) => {
      console.error("Error fetching department details:", error);
    });
}


onMounted(() => {
  localStorage.removeItem('routepath')

  const userData = JSON.parse(localStorage.getItem('employeeData'));
  is_admin.value = userData.is_admin || '';

  if (is_admin.value == 1) {
    isEnable.value = "true";
  }
  if (route.path === "/forms/department/allforms" || route.path === "/forms/department/allforms") {
    router.replace("/forms/department/allforms");
  }

})

</script>

<style scoped lang="scss">
.report-fields{
  max-height: 400px;
  overflow-y: auto;
}
.dashedcircle {
  border: 1px dashed #AAAAAA;
  height: 30px;
  width: 30px;
  padding: 0;
  margin: 0;
  border-radius: 50%;
  color: #14D82B;
}

.dashed_line {
  height: 100px;
  border: 1px dashed #AAAAAA;
  width: 1px;
  position: absolute;
  left: 2%;
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
  /* background-color: #f1f1f1; 
  color: #111111;  */
  padding: 8px 20px;
}


.filterbtn {
  border: 1px solid #CCCCCC;
  font-size: 16px;
  border-radius: 4px;
  color: #999999;
  padding: 8px;
  width: 100%;
}
</style>
