<template>
  <div>
    <div class="d-flex justify-content-between align-items-center py-2">
      <div>
        <h1 class="m-0 font-13">My Approval Forms</h1>
        <p class="m-0 font-11 pt-1">{{ totalRecords }} Forms</p>
      </div>
     
    </div>
    <div class="mt-2">
      <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction="true" viewType="viewPdf" isCheckbox="true"
        @updateFilters="inLineFiltersData" :field-mapping="fieldMapping" @cell-click="viewPreview"
        isFiltersoption="true" :actions="actions"  />
      <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords" :items-per-page="filterObj.limitPageLength"
        @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
    </div>
   
  </div>
</template>
<script setup>

import GlobalTable from "../../Components/GlobalTable.vue";
import axiosInstance from "../../shared/services/interceptor";
import { apis } from "../../shared/apiurls";
import {  ref,  computed, watch } from "vue";
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import PaginationComp from "../../Components/PaginationComp.vue";
import { useRoute, useRouter } from "vue-router";
const router = useRouter();
const route = useRoute();
const businessUnit = computed(() => {
  return EzyBusinessUnit.value;
});
const newBusinessUnit = ref({ business_unit: "" });
const filterObj = ref({ limitPageLength: 20, limit_start: 0, filters: [] });
const totalRecords = ref(0);
const limit = ref(20);
const limitStart = ref(0);
const filteredData = ref([]); 
const tableheaders = ref([
  { th: "Request ID", td_key: "name" },
  { th: "Requester Name", td_key: "requester_name" },
  { th: "Requester Department", td_key: "department_name" },
  { th: "Last Action On", td_key: "modified" },
  { th: "Approval Status", td_key: "status" },
  { th: "Pending With", td_key: "assigned_to_users" },
  { th: "Linked ID", td_key: "linked_form_id" },

]);

const actions = ref([
  { name: "View Request", icon: "fa-solid fa-eye" },

]);
const tableData = ref([]);
const timeout = ref(null);
const fullData = ref([]); 


function ViewOnlyReport() {
    const EmpRequestMail = JSON.parse(localStorage.getItem("employeeData"));

  const queryParams = {
    employee: EmpRequestMail.emp_mail_id,
    approved_by_me: "1",
    property_field: newBusinessUnit.value.business_unit,
  }
  axiosInstance
    .get(apis.GetEmployeeForms, { params: queryParams })
    .then((response) => {
      fullData.value = response.message || [];
      // Initially filteredData = fullData
      filteredData.value = [...fullData.value];

      totalRecords.value = filteredData.value.length;
      limitStart.value = 0;
      tableData.value = filteredData.value.slice(0, limit.value);
    })
    .catch((error) => {
      console.error(error);
    });
}



function paginateData(filtered = fullData.value) {
  const paginated = filtered.slice(limitStart.value, limitStart.value + limit.value);
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
    limit.value = 20;
    limitStart.value = 0;

    tableData.value = filteredData.value.slice(0, limit.value);
  }, 500);
}

function PaginationUpdateValue(newLimit) {
  limit.value = newLimit;
  limitStart.value = 0;
  paginateData();
}

function PaginationLimitStart() {
  limitStart.value += limit.value;
  const nextBatch = filteredData.value.slice(limitStart.value, limitStart.value + limit.value);
  tableData.value = [...tableData.value, ...nextBatch];
}




function viewPreview(data, index, type) {
  // console.log(data);
  if (type === 'view') {
    router.push({
      name: "ApproveRequest",
      query: {
        routepath: route.path,
        name: data.name,
        doctype_name: data.doctype_name,
        type: 'myapprovals',
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


const fieldMapping = computed(() => ({
  name: { type: "input" },
  requester_name: { type: "input" },
  department_name: { type: "input" },
  status: { type: "select", options: ["In Progress", "Completed", "Request Cancelled"] },
}));


watch(
  businessUnit,
  (newVal) => {
    newBusinessUnit.value.business_unit = newVal;

    if (newVal.length) {
      ViewOnlyReport();
    }
  },
  { immediate: true }
);

</script>
<style scoped>
.approvebtn {
  width: 146px;
  /* height: 30px; */
  background: #099819;
  color: white;
  padding: 5px 15px 5px 15px;
  gap: 7px;
  border-radius: 4px;
  opacity: 0px;
  font-weight: bold;
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
  /* height: 30px; */
  background: #fe212e;
  color: white;
  padding: 5px 15px 5px 15px;
  gap: 7px;
  border-radius: 4px;
  opacity: 0px;
  font-weight: bold;
}

.cancelbtn {
  width: 146px;
  height: 30px;
  background: #d1d0d0;
  color: white;
  padding: 5px 15px 5px 15px;
  gap: 7px;
  border-radius: 4px;
  opacity: 0px;
}

.is-invalid {
  border: 1px solid red;
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
</style>
