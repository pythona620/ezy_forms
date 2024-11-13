<template>
  <div>
    <div class="d-flex justify-content-between align-items-center ">
      <div>
        <h1 class="m-0 font-13">
          Requests raised for me
        </h1>
        <p class="m-0 font-11 pt-1">
          {{ totalRecords }} request
        </p>
      </div>
      <div class="d-flex gap-3 align-items-center">
        <div class="d-flex  align-items-center">
          <div>
            <div class="me-2">
              <span v-if="filterOnModal.name && filterOnModal.appliedname" class="process-date font-12 m-0">
                {{ filterOnModal.name }}
                <span v-if="filterOnModal.name" class="badge badge-icon rounded-3   text-white "
                  @click="clearFilter('name')">
                  <i class="ri-close-line close-icon text-dark rounded-3"></i>
                </span>
              </span>
              <span v-if="filterOnModal.doctype_name && filterOnModal.applieddoctype_name"
                class="process-date font-12 m-0">
                {{ filterOnModal.doctype_name }}
                <span v-if="filterOnModal.doctype_name" class="badge badge-icon rounded-3   text-white "
                  @click="clearFilter('doctype_name')">
                  <i class="ri-close-line close-icon text-dark rounded-3"></i>
                </span>
              </span>
              <span v-if="filterOnModal.accessible_departments && filterOnModal.appliedaccessible_departments"
                class="process-date font-12 m-0">
                {{ filterOnModal.accessible_departments }}
                <span v-if="filterOnModal.accessible_departments" class="badge badge-icon rounded-3   text-white "
                  @click="clearFilter('accessible_departments')">
                  <i class="ri-close-line close-icon text-dark rounded-3"></i>
                </span>
              </span>
              <span v-if="filterOnModal.status && filterOnModal.appliedStatus" class="process-date font-12 m-0">
                {{ filterOnModal.status }}
                <span v-if="filterOnModal.status" class="badge badge-icon rounded-3   text-white"
                  @click="clearFilter('status')">
                  <i class="ri-close-line close-icon text-dark rounded-3"></i>
                </span>
              </span>
              <span v-if="filterOnModal.request_id && filterOnModal.appliedrequest_id" class="process-date font-12 m-0">
                {{ filterOnModal.request_id }}
                <span v-if="filterOnModal.request_id" class="badge badge-icon rounded-3   text-white"
                  @click="clearFilter('request_id')">
                  <i class="ri-close-line close-icon text-dark rounded-3"></i>
                </span>
              </span>
              <span v-if="filterOnModal.requested_on && filterOnModal.appiedrequestedOn"
                class="process-date font-12 m-0">
                {{ filterOnModal.requested_on }}
                <span v-if="filterOnModal.requested_on" class="badge badge-icon rounded-3   text-white"
                  @click="clearFilter('requested_on')">
                  <i class="ri-close-line close-icon text-dark rounded-3"></i>
                </span>
              </span>
              <span v-if="filterOnModal.owner && filterOnModal.appliedowner" class="process-date font-12 m-0">
                {{ filterOnModal.owner }}
                <span v-if="filterOnModal.owner" class="badge badge-icon rounded-3   text-white"
                  @click="clearFilter('owner')">
                  <i class="ri-close-line close-icon text-dark rounded-3"></i>
                </span>
              </span>
            </div>
          </div>
          <div>
            <button type="button" class=" filterbtn d-flex align-items-center position-relative " data-bs-toggle="modal"
              data-bs-target="#fileterModal">
              <span> <i class="ri-filter-2-line"></i></span>
              <span v-if="appliedFiltersCount !== 0" class=" badge badge-light colorappiled ">
                ( {{ appliedFiltersCount }})
              </span>
            </button>

          </div>
        </div>
        <div class="modal fade" id="fileterModal" tabindex="-1" aria-labelledby="fileterModalLabel" aria-hidden="true">
          <div class="modal-dialog modal-lg">
            <div class="modal-content">

              <div class="modal-body">
                <div class="row">
                  <div class="col-6">
                    <label class="font-13 ps-1" for="Requested">Request Id:</label>
                    <FormFields tag="select" placeholder="Requested Id" class="mb-3" name="dept"
                      v-model="filterOnModal.name" id="id" :Required="false" :options="idDta" />
                  </div>
                  <div class="col-6">
                    <label class="font-13 ps-1" for="Requested">Form Name:</label>
                    <FormFields tag="select" placeholder="Form Name" class="mb-3" name="dept"
                      v-model="filterOnModal.doctype_name" id="id" :Required="false" :options="docTypeName" />
                  </div>
                  <!-- <div class="col-6">
                                      <label class="font-13 ps-1" for="dept">Form Category:</label>
                                      <FormFields tag="select" placeholder="Form Category" class="mb-3"
                                          name="dept" v-model="filterOnModal.doctype_name" id="dept" :Required="false"
                                           />
                                  </div> -->
                  <div class="col-6">
                    <label class="font-13 ps-1" for="dept">Requested On:</label>

                    <FormFields class="" tag="input" type="search" name="Requested" id="Requested" placeholder="Search"
                      v-model="filterOnModal.requested_on" />
                    <!-- <span class="m-0 font-10 ps-2">Note:Please seperate departments with commas</span> -->
                  </div>
                  <div class="col-6">
                    <label class="font-13 ps-1" for="status">Status:</label>

                    <FormFields tag="select" placeholder="Status" class="mb-3" name="status"
                      v-model="filterOnModal.status" id="status" :Required="false" :options="statusOptions" />
                  </div>

                  <div class="col-6">
                    <label class="font-13 ps-1" for="Requested">Owner Of Form:</label>
                    <FormFields class="mb-3" tag="input" type="search" name="Requested" id="Requested"
                      placeholder="Search" v-model="filterOnModal.owner" />
                  </div>
                  <!-- <div class="col-6">
                                      <label class="font-13 ps-1" for="Requested">Requested Department:</label>
                                      <FormFields class="mb-3" tag="input" type="search" name="Requested"
                                          id="Requested" placeholder="Search" v-model="filterOnModal.owner" />
                                  </div> -->


                </div>
              </div>
              <div class="modal-footer">
                <button type="button" class="cancelfilter border-0 text-nowrap font-10 " @click="resetFilters"
                  data-bs-dismiss="modal"><span class="font-14 me-1">x</span>Cancel
                  Filter</button>

                <button type="button"
                  class="applyfilter text-nowrap border-0 btn btn-dark text-white font-10 d-flex justify-content-center align-items-center"
                  data-bs-dismiss="modal" @click="applyFilters"><span class="font-16 me-1"><i
                      class="bi bi-check2 "></i></span>
                  Apply
                  Filter</button>
              </div>
            </div>
          </div>
        </div>

        <div class="d-flex align-items-center mb-1">
          <ButtonComp class="buttoncomp" name="Action"></ButtonComp>
        </div>
      </div>
    </div>
    <div class="mt-2">
      <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction='true' actionType="dropdown" isCheckbox='true'
        :actions="actions" @actionClicked="actionCreated" />
      <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords"
        @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
    </div>
    <div class="modal fade" id="viewRequest" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
      aria-labelledby="viewRequestLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="viewRequestLabel">Request</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <!-- {{ selectedRequest }} -->
          </div>

        </div>
      </div>
    </div>
  </div>

</template>
<script setup>
import FormFields from '../../Components/FormFields.vue';
import ButtonComp from '../../Components/ButtonComp.vue';
import GlobalTable from '../../Components/GlobalTable.vue';
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from '../../shared/apiurls';
import { callWithErrorHandling, onMounted, ref, reactive, computed, watch } from 'vue';
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import PaginationComp from '../../Components/PaginationComp.vue';
const businessUnit = computed(() => {
  return EzyBusinessUnit.value;
});
const newBusinessUnit = ref({ business_unit: '' });

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

]

)
const selectedRequest = ref({})

function actionCreated(rowData, actionEvent) {
  if (actionEvent.name === 'View Request') {
    if (rowData) {
      selectedRequest.value = { ...rowData }
      console.log(selectedRequest.value, "selected Request")
      const filters = [
        ["wf_generated_request_id", "like", `%${selectedRequest.value.name}%`]
      ];
      const queryParams = {
        fields: JSON.stringify(["*"]),
        limit_page_length: "None",
        limit_start: 0,
        filters: JSON.stringify(filters),
        order_by: `\`tab${selectedRequest.value.doctype_name}\`.\`creation\` desc`
      };
      axiosInstance.get(`${apis.resource}${selectedRequest.value.doctype_name}`, { params: queryParams })
        .then((res) => {
          if (res.data) {
            console.log(res.data)
          }
        })
        .catch((error) => {
          console.error("Error fetching categories data:", error);
        });
      // selectedForm.value = rebuildToStructuredArray(JSON.parse(rowData?.form_json).fields)
      const modal = new bootstrap.Modal(document.getElementById('viewRequest'), {});// raise a modal
      modal.show();

    } else {
      console.warn(" There is no form fields ")

    }
  }

}
const actions = ref(
  [
    { name: 'View Request', icon: 'fa-solid fa-eye' },

    // { name: 'Share this form', icon: 'fa-solid fa-share-alt' },
    // { name: 'Download Form', icon: 'fa-solid fa-download' },
    // { name: 'Edit Form', icon: 'fa-solid fa-edit' },

  ]
)
const tableData = ref([]);
const filterOnModal = reactive({
  appliedname: false,
  applieddoctype_name: false,
  appliedaccessible_departments: false,
  appliedStatus: false,
  appliedrequest_id: false,
  appiedrequestedOn: false,
  appliedowner: false,
  name: '',
  doctype_name: '',
  accessible_departments: '',
  status: '',
  request_id: '',
  requested_on: '',
  owner: ''
})
const appliedFiltersCount = computed(() => {
  return [
    { value: filterOnModal.doctype_name, applied: filterOnModal.applieddoctype_name },
    {
      value: filterOnModal.name,
      applied: filterOnModal.appliedname,
    },
    {
      value: filterOnModal.status,
      applied: filterOnModal.appliedStatus,
    },
    {
      value: filterOnModal.accessible_departments,
      applied: filterOnModal.appliedaccessible_departments,
    },
    {
      value: filterOnModal.request_id,
      applied: filterOnModal.appliedrequest_id,
    },
    {
      value: filterOnModal.requested_on,
      applied: filterOnModal.appiedrequestedOn,
    },
    {
      value: filterOnModal.owner,
      applied: filterOnModal.appliedowner,
    },


  ].filter((filter) => filter.applied && filter.value).length;
});
function clearFilter(type) {
  if (type === "name") {
    filterOnModal.name = "";
    filterOnModal.appliedname = false;
  } else if (type === "doctype_name") {
    filterOnModal.doctype_name = "";
    filterOnModal.applieddoctype_name = false;

  }
  else if (type === "accessible_departments") {
    filterOnModal.accessible_departments = "";
    filterOnModal.appliedaccessible_departments = false;

  }
  else if (type === "status") {
    filterOnModal.status = "";
    filterOnModal.appliedStatus = false;

  }
  else if (type === "request_id") {
    filterOnModal.request_id = "";
    filterOnModal.appliedrequest_id = false;

  }
  else if (type === "requested_on") {
    filterOnModal.requested_on = "";
    filterOnModal.appiedrequestedOn = false;

  }
  else if (type === "owner") {
    filterOnModal.owner = "";
    filterOnModal.appliedowner = false;

  }


  applyFilters();
}
function applyFilters() {
  filterOnModal.appliedname = Boolean(filterOnModal.name);
  filterOnModal.applieddoctype_name = Boolean(filterOnModal.doctype_name);
  filterOnModal.appliedaccessible_departments = Boolean(filterOnModal.accessible_departments);
  filterOnModal.appliedStatus = Boolean(filterOnModal.status);
  filterOnModal.appliedrequest_id = Boolean(filterOnModal.request_id);
  filterOnModal.appiedrequestedOn = Boolean(filterOnModal.requested_on);
  filterOnModal.appliedowner = Boolean(filterOnModal.owner);

  receivedForMe()
}
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
const idDta = ref([]);
const docTypeName = ref([])
const statusOptions = ref([])

function receivedForMe() {
  // Initialize filters array for building dynamic query parameters
  const EmpRequestMail = JSON.parse(localStorage.getItem('employeeData'));
  const filters = [
    ["requested_by", "like", EmpRequestMail.emp_mail_id]
  ];

  // Conditionally add filters based on available fields in filterOnModal
  if (filterOnModal.name) {
    filters.push(["name", "=", filterOnModal.name]);
  }
  if (filterOnModal.doctype_name) {
    filters.push(["doctype_name", "=", filterOnModal.doctype_name]);
  }
  if (filterOnModal.accessible_departments) {
    filters.push(["accessible_departments", "like", filterOnModal.accessible_departments]);
  }
  if (filterOnModal.status) {
    filters.push(["status", "like", filterOnModal.status]);
  }
  if (filterOnModal.request_id) {
    filters.push(["request_id", "like", filterOnModal.request_id]);
  }
  if (filterOnModal.requested_on) {
    filters.push(["requested_on", "like", filterOnModal.requested_on]);
  }
  if (filterOnModal.owner) {
    filters.push(["owner", "like", filterOnModal.owner]);
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
    fields: JSON.stringify(["count(`tabWF Workflow Requests`.`name`) AS total_count"]),
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