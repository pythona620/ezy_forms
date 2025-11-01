<template>
  <div>
    <div class="d-flex justify-content-between align-items-center py-2">
      <div>
        <h1 class="m-0 font-13">Requests Assigned to me</h1>
        <p class="m-0 font-11 pt-1">{{ totalRecords }} request</p>
      </div>
    </div>
    <div class="mt-2">
      <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction="true" viewType="viewPdf" isCheckbox="true"
        @updateFilters="inLineFiltersData" :field-mapping="fieldMapping" @cell-click="viewPreview"
        isFiltersoption="true" :actions="actions" @actionClicked="actionCreated" />
      <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords" :items-per-page="filterObj.limitPageLength"
        @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
    </div>
    

  </div>
</template>
<script setup>

import GlobalTable from "../../Components/GlobalTable.vue";
import axiosInstance from "../../shared/services/interceptor";
import { apis, doctypes } from "../../shared/apiurls";
import { onMounted, ref, computed, watch } from "vue";
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import PaginationComp from "../../Components/PaginationComp.vue";
import { rebuildToStructuredArray } from "../../shared/services/field_format";
// import ApproverPreview from "../../Components/ApproverPreview.vue";

import { useRoute, useRouter } from "vue-router";
const router = useRouter();
const route = useRoute();

const businessUnit = computed(() => {
  return EzyBusinessUnit.value;
});
const newBusinessUnit = ref({ business_unit: "" });

const filterObj = ref({ limitPageLength: 20, limit_start: 0, filters: [] });
const totalRecords = ref(0);
const idDta = ref([]);

const selectedcurrentLevel = ref("");
const activityData = ref([]);
const responseData = ref([]);

const tableheaders = ref([
  { th: "Request ID", td_key: "name" },
  { th: "Requested By", td_key: "requester_name" },
  { th: "Requested on", td_key: "requested_on" },
  { th: "Requested Department", td_key: "department_name" },
  { th: "Last Action On", td_key: "modified" },
  { th: "Approval Status", td_key: "status" },
  { th: "Pending With", td_key: "assigned_to_users" },
  { th: "Linked ID", td_key: "linked_form_id" },

]);

const actions = ref([
  { name: "View Request", icon: "fa-solid fa-eye" },

  // { name: 'Share this form', icon: 'fa-solid fa-share-alt' },
  // { name: 'Download Form', icon: 'fa-solid fa-download' },
  // { name: 'Edit Form', icon: 'fa-solid fa-edit' },
]);
const selectedRequest = ref({});
const showRequest = ref(null);
const doctypeForm = ref([]);

const employeeData = ref([]);
const tableHeaders = ref([]);


const filteredData = ref([]);

onMounted(() => {
  // getClientIP()
  const storedData = localStorage.getItem("employeeData");
  employeeData.value = JSON.parse(storedData);

});

// function ViewOnlyReport() {

//   // console.log(ViewOnlyReportee.value); 
//   axiosInstance
//     .post(apis.view_only_reportee,)
//     .then((response) => {
//       // console.log(response.message,"list");
//       viewlist.value = response.message;
// //       receivedForMe(filterObj.value.filters);

//     })
//     .catch((error) => {
//       console.log(error);
//     });
// }

function actionCreated(rowData, actionEvent) {
  if (actionEvent.name === "View Request") {
    console.log(rowData, "rowData");
    
  }
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
        type: "mytasks",
        designation: employeeData.value.designation

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

// Computed property to determine if any action is cancelled
const requestcancelled = computed(() => {
  return activityData.value.some((item) => item.action === "Request Cancelled");
});

// Format the date for display
const formatDate = (dateString) => {
  if (!dateString) return "N/A";
  const date = new Date(dateString);
  return date.toLocaleDateString("en-GB");
};

// Format action text (cancelled or raised)
const formatAction = (action) => {
  if (!action) return "performed an action on";
  const actionMap = {
    "Request Cancelled": "cancelled",
    "Request Raised": "raised",
  };
  return actionMap[action] || action.toLowerCase();
};




// const ip_address = ref(null)

// const getClientIP = async () => {
//   try {
//     const response = await fetch('https://api.ipify.org?format=json')
//     const data = await response.json()
//     ip_address.value = data.ip

//   } catch (error) {
//     console.error('Error fetching IP:', error)
//   }
// }


// const PaginationUpdateValue = (itemsPerPage) => {
//   filterObj.value.limitPageLength = itemsPerPage;
//   filterObj.value.limit_start = 0;
//   if (filterObj.value.filters.length) {
//     receivedForMe(filterObj.value.filters);
//   } else {
//     receivedForMe();
//   }
// };
// Handle updating the limit start
// const PaginationLimitStart = ([itemsPerPage, start]) => {
//   filterObj.value.limitPageLength = itemsPerPage;
//   filterObj.value.limit_start = start;
//   if (filterObj.value.filters.length) {
//     receivedForMe(filterObj.value.filters);
//   } else {
//     receivedForMe();
//   }
// };

const filters = ref([]);
// function inLineFiltersData(searchedData) {
//   clearTimeout(timeout.value); // Clear previous timeout

//   timeout.value = setTimeout(() => {
//     // Initialize filters array
//     filterObj.value.filters = [];

//     // Loop through the table headers and build dynamic filters
//     tableheaders.value.forEach((header) => {
//       const key = header.td_key;

//       if (searchedData[key]) {
//         // Push as an array of 3 items
//         filterObj.value.filters.push([key, "like", `%${searchedData[key]}%`]);
//       }
//     });

//     // Check if status is present in the route query params


//     // Call receivedForMe with or without filters
//     if (filterObj.value.filters.length) {
//       filterObj.value.limit_start = 0;
//       receivedForMe(filterObj.value.filters);
//     } else {
//       receivedForMe();
//     }
//   }, 500); // Adjust debounce delay as needed
// }
// function receivedForMe(data) {
//   // Initialize filters array for building dynamic query parameters

//   const EmpRequestdesignation = JSON.parse(localStorage.getItem("employeeData"));
//   employeeData.value = EmpRequestdesignation.designation;

//   const filters = [
//     // assigned_to_users
//     ["assigned_to_users", "like", `%${EmpRequestdesignation?.designation}%`],
//     ["property", "=", `${newBusinessUnit.value.business_unit}`],
//     ["status", "!=", "Request Cancelled"],

//     ["name", "in", viewlist.value],
//     ["status", "!=", "Completed"]
//   ];
//   if (data) {
//     filters.push(...data);
//     // console.log(data);
//   }

//   const queryParams = {
//     fields: JSON.stringify(["*"]),
//     limit_page_length: filterObj.value.limitPageLength,
//     limit_start: filterObj.value.limit_start,
//     filters: JSON.stringify(filters),
//     order_by: "`tabWF Workflow Requests`.`creation` desc",
//   };

//   const queryParamsCount = {
//     fields: JSON.stringify(["count(name) AS total_count"]),
//     limitPageLength: "None",
//     filters: JSON.stringify(filters),
//   };

//   // Fetch total count of records matching filters
//   axiosInstance
//     .get(`${apis.resource}${doctypes.WFWorkflowRequests}`, {
//       params: queryParamsCount,
//     })
//     .then((res) => {
//       totalRecords.value = res.data[0].total_count;
//     })
//     .catch((error) => {
//       console.error("Error fetching total count:", error);
//     });

//   // Fetch the records matching filters
//   axiosInstance
//     .get(`${apis.resource}${doctypes.WFWorkflowRequests}`, {
//       params: queryParams,
//     })
//     .then((res) => {
//       if (filterObj.value.limit_start === 0) {

//         tableData.value = res.data;
//         idDta.value = [...new Set(res.data.map((id) => id.name))];
//         docTypeName.value = [
//           ...new Set(res.data.map((docTypeName) => docTypeName.doctype_name)),
//         ];
//         statusOptions.value = [...new Set(res.data.map((status) => status.status))];
//       }
//       else {
//         tableData.value = tableData.value.concat(res.data);
//       }

//     })
//     .catch((error) => {
//       console.error("Error fetching records:", error);
//     });
// }

const fieldMapping = computed(() => ({
  // invoice_type: { type: "select", options: ["B2B", "B2G", "B2C"] },
  // credit_irn_generated: { type: "select", options: ["Pending", "Completed", "Error"] },
  // role: { type: "input" },
  name: { type: "input" },
  requester_name: { type: "input" },
  department_name: { type: "input" },
  requested_on: { type: "date" },


  status: { type: "select", options: ["Request Raised", "In Progress"] },

}));



const tableData = ref([]);
const timeout = ref(null);
const fullData = ref([]); 


function ViewOnlyReport() {
  axiosInstance
    .post(apis.view_only_reportee)
    .then((response) => {
      // Filter out items with status 'Completed' or 'Request Cancelled'
      const filtered = (response.message || []).filter(
        item => item.status !== 'Completed' && item.status !== 'Request Cancelled'
      );

      fullData.value = filtered;
      filteredData.value = [...filtered];

      totalRecords.value = filteredData.value.length;
      filterObj.value.limit_start = 0;
      tableData.value = filteredData.value.slice(0, filterObj.value.limitPageLength);
    })
    .catch((error) => {
      console.error(error);
    });
}



const limit = ref(20);
// const limitStart = ref(0);

// function paginateData(filtered = fullData.value) {
//   const paginated = filtered.slice(filterObj.value.limit_start, filterObj.value.limit_start + filterObj.value.limitPageLength);
//   tableData.value = paginated;
//   totalRecords.value = filtered.length;
// }
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

// function PaginationLimitStart() {
//   filterObj.value.limit_start += filterObj.value.limitPageLength;

//   const nextBatch = filteredData.value.slice(filterObj.value.limit_start, filterObj.value.limit_start + filterObj.value.limitPageLength);

//   tableData.value = [...tableData.value, ...nextBatch];
// }

function PaginationLimitStart() {
  filterObj.value.limit_start += filterObj.value.limitPageLength;

  // Always take from filteredData instead of fullData
  const nextBatch = filteredData.value.slice(
    filterObj.value.limit_start,
    filterObj.value.limit_start + filterObj.value.limitPageLength
  );

  // Append next filtered records
  tableData.value = [...tableData.value, ...nextBatch];
}




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
