<template>
  <div>
    <div class="d-flex justify-content-between align-items-center py-2">
      <div>
        <h1 class="m-0 font-13">My Team Requests </h1>
        <p class="m-0 font-11 pt-1">{{ totalRecords }} request</p>
      </div>
    </div>
    <div class="mt-2">
      <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction="true" viewType="viewPdf" isCheckbox="true"
        :actions="actions" @actionClicked="actionCreated" isFiltersoption="true" :field-mapping="fieldMapping"
        @cell-click="viewPreview" @updateFilters="inLineFiltersData" />
      <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords" :items-per-page="filterObj.limitPageLength"
        @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
    </div>
  </div>
</template>
<script setup>

import GlobalTable from "../../Components/GlobalTable.vue";
import axiosInstance from "../../shared/services/interceptor";
import { apis, doctypes, domain } from "../../shared/apiurls";
import {
  
  ref,
  
  computed,
  watch,
} from "vue";
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import PaginationComp from "../../Components/PaginationComp.vue";
import { useRoute, useRouter } from "vue-router";
const businessUnit = computed(() => {
  return EzyBusinessUnit.value;
});
const newBusinessUnit = ref({ business_unit: "" });
const route = useRoute();
const router = useRouter();
const filterObj = ref({ limitPageLength: 20, limit_start: 0, filters: [] });
const totalRecords = ref(0);
const tableData = ref([]);
const timeout = ref(null);
const fullData = ref([]);
const filteredData = ref([]);
const tableheaders = ref([
  { th: "Request ID", td_key: "name" },
  { th: "Form Name", td_key: "doctype_name" },
  { th: "Requester Name", td_key: "requester_name" },
  { th: "Requested on", td_key: "requested_on" },
  { th: "Requester Department", td_key: "department_name" },
  { th: "Last Action On", td_key: "modified" },
  { th: "Approval Status", td_key: "status" },
  { th: "Pending With", td_key: "assigned_to_users" },
  { th: "Linked ID", td_key: "linked_form_id" },

]);
const fieldMapping = ref({
  name: { type: "input" },
  status: {
    type: "select",
    options: [
      "Request Raised",
      "In Progress",
      "Completed",
      "Request Cancelled",
    ],
  },
  department_name: { type: "input" },
  doctype_name: { type: "input" },
  requested_on: { type: "date" },
  requester_name: { type: "input" },
});

const actions = ref([
  { name: "View Request", icon: "fa-solid fa-eye" },
  { name: "PDF Format", icon: "bi bi-filetype-pdf" },
]);

function actionCreated(rowData, actionEvent) {
  if (actionEvent.name === "View Request") {
    console.log(rowData, "rowData");
  } else if (actionEvent.name === "PDF Format") {

  }
}


function viewPreview(data, index, type) {
  if (type === 'view') {

    router.push({
      name: "ApproveRequest",
      query: {
        routepath: route.path,
        name: data.name,
        doctype_name: data.doctype_name,
        type: 'myteam',
        readOnly: 'true'
      },
    });
  }


  if (type === 'td_key') {
    if (data.linked_form_id) {
      router.push({
        name: "ApproveRequest",
        query: {
          routepath: route.path,
          name: data.linked_form_id,
          business_unit: data.property,
          type: "linkedForm",
          readOnly: 'true'

        },
      });
    }

  }
}




function receivedForMe() {
  const EmpRequestMail = JSON.parse(localStorage.getItem("employeeData"));
  const queryParams = {
    property_field: newBusinessUnit.value.business_unit,
    // department: EmpRequestMail.department,
  }
  axiosInstance
    .get(apis.GetEmployeeForms, { params: queryParams })
    .then((response) => {
      fullData.value = response.message || [];

      // Initially filteredData = fullData
      filteredData.value = [...fullData.value];

      totalRecords.value = filteredData.value.length;
      filterObj.value.limit_start = 0;
      tableData.value = filteredData.value.slice(0, filterObj.value.limitPageLength);
    })
    .catch((error) => {
      console.error(error);
    });
}

function paginateData(filtered = filteredData.value) {
  const paginated = filtered.slice(filterObj.value.limit_start, filterObj.value.limit_start + filterObj.value.limitPageLength);
  tableData.value = paginated;
  totalRecords.value = filtered.length;
}

function inLineFiltersData(searchedData) {
  clearTimeout(timeout.value);

  timeout.value = setTimeout(() => {
    filteredData.value = fullData.value.filter((row) => {
      return tableheaders.value.every((header) => {
        const key = header.td_key;
        if (searchedData[key]) {
          return String(row[key] || "").toLowerCase().includes(String(searchedData[key]).toLowerCase());
        }
        return true;
      });
    });

    totalRecords.value = filteredData.value.length;
    filterObj.value.limitPageLength = 20;
    filterObj.value.limit_start = 0;

    tableData.value = filteredData.value.slice(0, filterObj.value.limitPageLength);
  }, 500);
}

function PaginationUpdateValue(newLimit) {
  filterObj.value.limitPageLength = newLimit;
  filterObj.value.limit_start = 0;
  paginateData();
}

function PaginationLimitStart() {
  filterObj.value.limit_start += filterObj.value.limitPageLength;
  const nextBatch = filteredData.value.slice(filterObj.value.limit_start, filterObj.value.limit_start + filterObj.value.limitPageLength);
  tableData.value = [...tableData.value, ...nextBatch];
}


watch(
  businessUnit,
  (newVal) => {
    newBusinessUnit.value.business_unit = newVal;

    if (newVal.length) {
      receivedForMe();
    }
  },
  { immediate: true }
);

</script>
<style lang="scss" scoped>
.approvebtn {
  width: 146px;
  height: 30px;
  /* background: #14D82B; */
  color: white;
  padding: 5px 15px 5px 15px;
  gap: 7px;
  border-radius: 4px;
  opacity: 0px;
}

.edit-btn {
  background-color: #333;
  color: white;
  padding: 5px 15px 5px 15px;
  border-radius: 4px;
  font-weight: bold;
}

.rejectbtn {
  width: 146px;
  height: 30px;
  background: #fe212e;
  color: white;
  padding: 5px 15px 5px 15px;
  gap: 7px;
  border-radius: 4px;
  opacity: 0px;
}

.pdf-body {
  width: 100%;
  height: 70vh;
  overflow-y: scroll;
  /* overflow: hidden; */
}

/* Activity log container */
.activity-log-container {
  width: 100%;
  margin-top: 20px;
  padding-left: 30px;
  position: relative;
}

/* Activity log item */
.activity-log-item {
  position: relative;
  display: flex;
  align-items: flex-start;
  /* Ensure dot and text align properly */
  gap: 10px;
  /* Space between dot and text */
  margin-bottom: 20px;
  /* Space between logs */
}

/* Dot styling */
.activity-log-dot {
  position: relative;
  width: 12px;
  height: 12px;
  background-color: #676767;
  border-radius: 50%;
  border: 2px solid white;
  z-index: 1;
  /* Ensure dot is above */
}

/* Add vertical line using ::after */
.activity-log-dot::after {
  content: "";
  position: absolute;
  top: 13px;
  /* Start line from bottom of dot */
  left: 50%;
  width: 2px;
  height: 22px;
  /* Adjust line height */
  background-color: #ddd;
  transform: translateX(-50%);
}

/* Remove line for the last item */
.activity-log-item.last-item .activity-log-dot::after {
  content: none;
}

/* Activity log content */
.activity-log-content {
  font-size: 16px;
  color: #333;
  flex: 1;
  /* Ensure text takes up remaining space */
}

.activity-log-content strong {
  color: #333;
}

table {
  border-collapse: collapse;
}

th {
  background-color: #f2f2f2 !important;
  text-align: left;
  color: #999999;
  font-size: 12px;
}

td {
  font-size: 12px;
}
</style>
