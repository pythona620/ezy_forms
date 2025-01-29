<template>
  <div class="d-flex justify-content-between align-items-center ">
    <div>
      <h1 class="m-0 font-13">
        Requests raised for My Team
      </h1>
      <p class="m-0 font-11 pt-1">
        {{ totalRecords }} request
      </p>
    </div>

  </div>
  <div class="mt-2">
    <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction='true' actionType="dropdown" isCheckbox='true'
      :actions="actions" isFiltersoption="true" :field-mapping="fieldMapping" @updateFilters="inLineFiltersData" />
    <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords" @updateValue="PaginationUpdateValue"
      @limitStart="PaginationLimitStart" />
  </div>
</template>
<script setup>

import GlobalTable from '../../Components/GlobalTable.vue';
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from '../../shared/apiurls';
import { onMounted, ref, reactive, computed, watch } from 'vue';
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import PaginationComp from '../../Components/PaginationComp.vue';
const businessUnit = computed(() => {
  return EzyBusinessUnit.value;
});
const newBusinessUnit = ref({ business_unit: '' });
const idDta = ref([]);
const docTypeName = ref([]);
const statusOptions = ref([])
const filterObj = ref({ limitPageLength: 'None', limit_start: 0 });
const totalRecords = ref(0);

const tableheaders = ref([
  { th: "Request ID", td_key: "name" },
  { th: "Form name", td_key: "doctype_name" },
  // { th: "Form category", td_key: "doctype_name" },
  { th: "Owner of form", td_key: "owner" },
  { th: "Requested on", td_key: "requested_on" },
  // { th: "Requested department", td_key: "acess" },
  { th: "Approval Status", td_key: "status" },
])


const fieldMapping = ref({
  // invoice_type: { type: "select", options: ["B2B", "B2G", "B2C"] },
  status: { type: "select", options: ["Request Raised", "In Progress", "Completed", "Request Cancelled"] },
  name: { type: "input" },
  requested_on: { type: "date" },


});
const actions = ref(
  [
    { name: 'View Request', icon: 'fa-solid fa-eye' },

    { name: 'Share this form', icon: 'fa-solid fa-share-alt' },
    { name: 'Download Form', icon: 'fa-solid fa-download' },
    { name: 'Edit Form', icon: 'fa-solid fa-edit' },

  ]
)
const tableData = ref([]);


const PaginationUpdateValue = (itemsPerPage) => {
  filterObj.value.limitPageLength = itemsPerPage;
  filterObj.value.limit_start = 0;
  receivedForMe()


};
// Handle updating the limit start
const PaginationLimitStart = ([itemsPerPage, start]) => {
  filterObj.value.limitPageLength = itemsPerPage;
  filterObj.value.limit_start = start;
  receivedForMe()


};
function inLineFiltersData(searchedData) {
  console.log("Applied searchedData:", searchedData);

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
  console.log(filters.length == 0, "------------filters--------");

  //   // Log filters to verify
  //   console.log("Dynamic Filters:", filters);

  //   // Once the filters are built, pass them to fetchData function
  if (filters.length) {
    receivedForMe(filters);
  }
  else {
    receivedForMe();
  }
  //   fetchTotalRecords(filters);
}

function receivedForMe(data) {
  // Initialize filters array for building dynamic query parameters
  const filters = [
    ["property", "like", `%${newBusinessUnit.value.business_unit}%`]

  ];

  if (data) {
    filters.push(data)
  }

  // Define query parameters for data and count retrieval
  const queryParams = {
    fields: JSON.stringify(["*"]),
    limit_page_length: filterObj.value.limitPageLength,
    limit_start: filterObj.value.limit_start,
    filters: JSON.stringify(filters),
    order_by: "`tabWF Workflow Requests`.`creation` desc",
  };

  const queryParamsCount = {
    fields: JSON.stringify(["count(name) AS total_count"]),
    limitPageLength: "None",
    filters: JSON.stringify(filters),
  };

  // Fetch total count of records matching filters
  axiosInstance.get(`${apis.resource}${doctypes.WFWorkflowRequests}`, { params: queryParamsCount })
    .then((res) => {
      totalRecords.value = res.data[0].total_count;
    })
    .catch((error) => {
      console.error("Error fetching total count:", error);
    });

  // Fetch the records matching filters
  axiosInstance.get(`${apis.resource}${doctypes.WFWorkflowRequests}`, { params: queryParams })
    .then((res) => {
      console.log("output-res", res);
      tableData.value = res.data;
      idDta.value = [...new Set(res.data.map((id) => id.name))];
      docTypeName.value = [...new Set(res.data.map((docTypeName) => docTypeName.doctype_name))]
      statusOptions.value = [...new Set(res.data.map((status) => status.status))]


    })
    .catch((error) => {
      console.error("Error fetching records:", error);
    });
}

watch(
  businessUnit,
  (newVal) => {
    newBusinessUnit.value.business_unit = newVal;

    if (newVal.length) {
      console.log(newVal, "new value of business unit");
      receivedForMe()
    }
  },
  { immediate: true }
);
onMounted(() => {
  // receivedForMe()
})
</script>
<style scoped></style>