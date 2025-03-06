<template>
  <div>
    <div>
      <div class="d-flex justify-content-between align-items-center py-2">
        <div>
          <h1 class="m-0 font-13">
            Forms in {{ id }}
          </h1>
          <p class="m-0 font-11 pt-1">
            {{ totalRecords }} forms available
          </p>
        </div>

      </div>
      <div class="mt-3">
        <GlobalTable :tHeaders="tableheaders" :tData="tableData" isCheckbox="true" isAction="true" enableDisable="true"
          actionType="dropdown" @actionClicked="actionCreated" @toggle-click="toggleFunction" :actions="actions"
          @updateFilters="inLineFiltersData" :field-mapping="fieldMapping" isFiltersoption="true" />
        <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords"
          @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
      </div>

    </div>
    <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="offcanvasRightLabel">Asset Request Form</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body">
        <div class="d-flex gap-3 align-items-baseline position-relative">
          <div class="d-flex flex-column">
            <span>
              <i class="ri-checkbox-blank-circle-fill dashedcircle"></i>
            </span>
            <div class="dashed_line mt-4"></div>
          </div>
          <div>data</div>
        </div>
      </div>
    </div>
    <FormPreview :blockArr="selectedForm" :formDescriptions="formDescriptions" />

  </div>
</template>

<script setup>
import { ref, computed, watch, reactive } from 'vue';
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from '../../shared/apiurls';
import GlobalTable from '../../Components/GlobalTable.vue';
import { EzyBusinessUnit } from '../../shared/services/business_unit';
import { rebuildToStructuredArray } from '../../shared/services/field_format';
import PaginationComp from "../../Components/PaginationComp.vue"
import FormPreview from '../../Components/FormPreview.vue'
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import router from '../../router';
import { useRoute } from 'vue-router';
const totalRecords = ref(0);
const tableheaders = ref([
  { th: "Form name", td_key: "form_name" },
  { th: "Form Short Code", td_key: "form_short_name" },
  { th: "Form category", td_key: "form_category" },
  { th: "Accessible departments", td_key: "accessible_departments" },
  { th: "Status", td_key: "form_status" },
]);
const props = defineProps(['id']);
const formDescriptions = ref({})
const selectedForm = ref(null);
const tableData = ref([]);
const formCategory = ref([]);
const route = useRoute();



// Business unit and filter object
const businessUnit = computed(() => EzyBusinessUnit.value);
const newBusinessUnit = ref({ business_unit: '' });
const filterObj = ref({ limitPageLength: 'None', limit_start: 0 });
const actions = ref(
  [
    { name: 'View form', icon: 'fa-solid fa-eye' },
    { name: 'Raise Request', icon: 'fa fa-file-text' },
  ]
)
const fieldMapping = ref({
  // invoice_type: { type: "select", options: ["B2B", "B2G", "B2C"] },
  form_short_name: { type: "input" },
  form_category: { type: "select", options: formCategory.value },
  form_status: { type: "select", options: ["Created", "Draft"] },

  form_status: { type: "select", options: ["Created", "Draft"] },
  form_name: { type: "input" },

  // requested_on: { type: "date" },
});
function actionCreated(rowData, actionEvent) {
  if (actionEvent.name === 'View form') {
    if (rowData?.form_json) {
      formDescriptions.value = { ...rowData }
      selectedForm.value = rebuildToStructuredArray(JSON.parse(rowData?.form_json).fields)
      const modal = new bootstrap.Modal(document.getElementById('formViewModal'), {});// raise a modal
      modal.show();
      
    } else {
      toast.warn(" There is no form fields ")
    }
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
        // console.log(route.path,"sadasda");

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
          toast.info("You do not have permission to access this Form.");
        }
    } else {
        console.log("No employee data found in localStorage.");
    }
  }
}
// Toggle function triggered when a checkbox is clicked
function toggleFunction(rowData, rowIndex, event) {
  // console.log("rowData", rowData);

  // Decide the action based on the current state:
  const isCurrentlyEnabled = rowData.enable == '1' || rowData.enable === 1;
  const actionText = isCurrentlyEnabled ? 'delete' : 'restore';

  // Show the confirmation dialog with dynamic messaging:
  if (confirm(`Are you sure you want to ${actionText} this Form?`)) {
    // Toggle the state:
    rowData.enable = isCurrentlyEnabled ? 0 : 1;

    axiosInstance
      .put(`${apis.resource}${doctypes.EzyFormDefinitions}/${rowData.name}`, rowData)
      .then((response) => {
        console.log("Response:", response.data);
        // Adjust the toast message accordingly:
        toast.success(`Form ${actionText}d successfully`, { autoClose: 700 });
        // Refresh the table data after a short delay
        setTimeout(() => {
          fetchDepartmentDetails();
        }, 1000);
      })
      .catch((error) => {
        console.error("Error updating toggle:", error);
      });
  } else {
    // If canceled, do nothing – the checkbox remains unchanged.
    console.log("Action cancelled. Toggle remains unchanged.");
  }
}


// Watch business unit and department ID changes
watch(
  [() => businessUnit.value, () => props.id],
  ([newBusinessUnitVal, newId]) => {
    newBusinessUnit.value.business_unit = newBusinessUnitVal;
    if (newBusinessUnitVal.length && newId && props.id !== ':id') {
    
      fetchDepartmentDetails(newId || props.id, null);
    }
  },
  { immediate: true }
);

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
    fetchDepartmentDetails(null, filters);
  }
  else {
    fetchDepartmentDetails();
  }

}

// Fetch department details function
function fetchDepartmentDetails(id, data) {

  const filters = [
    ["business_unit", "like", `%${newBusinessUnit.value.business_unit}%`],
    ["enable", "=", 1]
  ];
  if (props.id && props.id !== "AllForms") {
    filters.push(["owner_of_the_form", "=", props.id]);
  }
  if (data) {
    filters.push(data)
  }

  const queryParams = {
    fields: JSON.stringify(["*"]),
    limit_page_length: filterObj.value.limitPageLength,
    limit_start: filterObj.value.limit_start,
    filters: JSON.stringify(filters),
    order_by: "`tabEzy Form Definitions`.`creation` desc",
  };
  const queryParamsCount = {
    fields: JSON.stringify(["count(name) AS total_count"]),
    limitPageLength: "None",
    filters: JSON.stringify(filters)
  }
  axiosInstance.get(`${apis.resource}${doctypes.EzyFormDefinitions}`, { params: queryParamsCount })
    .then((res) => {

      totalRecords.value = res.data[0].total_count

    })
    .catch((error) => {
      console.error("Error fetching ezyForms data:", error);
    });

  axiosInstance
    .get(`${apis.resource}${doctypes.EzyFormDefinitions}`, { params: queryParams })
    .then((response) => {
      tableData.value = response.data;

      formCategory.value = [...new Set(tableData.value.map((formCategory) => formCategory.form_category))];

    })
    .catch((error) => {
      console.error("Error fetching department details:", error);
    });
}

</script>

<style>
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
