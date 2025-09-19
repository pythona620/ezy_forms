<template>
  <div>
    <div class=" back-to-same">
      <div class="container-fluid p-0">
        <div class="d-flex justify-content-between asset_request">
          <div class="px-2 py-2 d-flex">
            <span @click="router.back()" class="font-14 back-btn"><i class="bi bi-arrow-left font-14 px-2"></i></span>
              <div class="d-flex align-items-center gap-2">
                <h1 class="m-0 font-13">{{ selectedData.EmpName }}</h1>
                <p class="m-0 p-0 font-10">( {{ totalRecords }} request )</p>
              </div>
          </div>
        </div>
      </div>
    </div>
    <div class="px-3">
      <div class="d-flex align-items-center gap-4 my-3">
        <!-- <div class="d-flex align-items-center gap-2">
          <h1 class="m-0 font-13">{{ selectedData.EmpName }}</h1>
          <p class="m-0 p-0 font-10">( {{ totalRecords }} request )</p>
        </div> -->
        <div class="card-container d-flex align-items-center gap-4 ms-2">
          <label class="card d-flex m-0" @click="switchTab('raised')" :class="{ active: activeTab === 'raised' }">
            Raised Forms
          </label>
          <label class="card d-flex m-0" @click="switchTab('approved')" :class="{ active: activeTab === 'approved' }">
            Approved Forms
          </label>
        </div>
      </div>

      <div class="mt-2">
        <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction="true" viewType="viewPdf" isCheckbox="true"
          @updateFilters="inLineFiltersData" :field-mapping="fieldMapping" @cell-click="viewPreview"
          isFiltersoption="true" :actions="actions" />
        <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords" :items-per-page="limit"
          @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
      </div>


    </div>
  </div>
</template>
<script setup>
import GlobalTable from "../Components/GlobalTable.vue";
import axiosInstance from "../shared/services/interceptor";
import { apis } from "../shared/apiurls";
import { onMounted, ref, computed, watch } from "vue";
import { EzyBusinessUnit } from "../shared/services/business_unit";
import PaginationComp from "../Components/PaginationComp.vue";
import { useRoute, useRouter } from "vue-router";
const router = useRouter();
const route = useRoute();

const businessUnit = computed(() => {
  return EzyBusinessUnit.value;
});

const tableData = ref([]);
const timeout = ref(null);
const fullData = ref([]);
const totalRecords = ref(0);
const filteredData = ref([]);
const limit = ref(20);
const limitStart = ref(0);

const tableheaders = ref([
  { th: "Request ID", td_key: "name" },
  { th: "Requester Name", td_key: "requester_name" },
  { th: "Requested On", td_key: "requested_on" },
  { th: "Requester Department", td_key: "department_name" },
  { th: "Approval Status", td_key: "status" },
  { th: "Pending With", td_key: "assigned_to_users" },
  { th: "Linked ID", td_key: "linked_form_id" },
]);

const actions = ref([
  { name: "View Request", icon: "fa-solid fa-eye" },
]);

const selectedData = ref({
  routepath: route.query.routepath,
  EmpId: route.query.name || "",
  EmpName: route.query.EmpName || "No Name",
  business_unit: route.query.business_unit || "",
  DeptName: route.query.Dept || "",
});

// const activeTab = ref('raised')

// function switchTab(tab) {
//   activeTab.value = tab
//   ViewOnlyReport()
// }
const activeTab = ref(route.query.tab || "raised"); // default to "raised"

// Function to switch tab
function switchTab(tab) {
  activeTab.value = tab;

  // Update query without reloading component
  router.replace({
    query: {
      ...route.query, // keep other query params if any
      tab: tab
    }
  });

  ViewOnlyReport(); // your existing function
}

// Keep activeTab in sync when route query changes (like on refresh or navigation)
watch(
  () => route.query.tab,
  (newTab) => {
    if (newTab) {
      console.log(route);
      activeTab.value = newTab;
    }
  }
);

function ViewOnlyReport() {
  const payload = {
    employee: selectedData.value.EmpId,
    department: selectedData.value.DeptName,
    ...(activeTab.value === 'raised' && { requested_by_me: "1" }),
    ...(activeTab.value === 'approved' && { approved_by_me: "1" }),
  }
  axiosInstance
    .post(apis.GetEmployeeForms, payload)
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
  requested_on: { type: "date" },
  department_name: { type: "input" },
  status: { type: "select", options: ["Request Raised", "In Progress", "Completed", "Request Cancelled"] },
}));

onMounted(() => {
  ViewOnlyReport()
})

// watch(
//   businessUnit,
//   (newVal) => {
//     newBusinessUnit.value.business_unit = newVal;

//     if (newVal.length) {
//       ViewOnlyReport();
//     }
//   },
//   { immediate: true }
// );

</script>

<style lang="scss" scoped>
.back-to-same {
  position: sticky;
  top: 0;
  background-color: #fff;
  z-index: 10;
}

.back-btn {
  cursor: pointer;
}

.asset_request {
  box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
}

.card {
  border: 1px solid #ccc;
  padding: 5px 10px;
  cursor: pointer;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
  font-size: 12px;
  user-select: none;
}

.card.active {
  background-color: #212529d9;
  color: white;
}
</style>
