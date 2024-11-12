<template>
  <div>

    <div class="d-flex justify-content-between align-items-center ">
      <div>
        <h1 class="m-0 font-13">
          Requests received for me
        </h1>
        <p class="m-0 font-11 pt-1">
          {{ totalRecords }} request
        </p>
      </div>
      <div class="d-flex gap-3 align-items-center">
        <div class="d-flex  align-items-center">
          <div>
            <div class="me-2">
              <span v-if="filterOnModal.form_name && filterOnModal.appliedform_name" class="process-date font-12 m-0">
                {{ filterOnModal.form_name }}
                <span v-if="filterOnModal.form_name" class="badge badge-icon rounded-3   text-white "
                  @click="clearFilter('form_name')">
                  <i class="ri-close-line close-icon text-dark rounded-3"></i>
                </span>
              </span>
              <span v-if="filterOnModal.form_category && filterOnModal.appliedform_category"
                class="process-date font-12 m-0">
                {{ filterOnModal.form_category }}
                <span v-if="filterOnModal.form_category" class="badge badge-icon rounded-3   text-white "
                  @click="clearFilter('form_category')">
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
              <span v-if="filterOnModal.form_status && filterOnModal.appliedStatus" class="process-date font-12 m-0">
                {{ filterOnModal.form_status }}
                <span v-if="filterOnModal.form_status" class="badge badge-icon rounded-3   text-white"
                  @click="clearFilter('form_status')">
                  <i class="ri-close-line close-icon text-dark rounded-3"></i>
                </span>
              </span>
              <span v-if="filterOnModal.request_id && filterOnModal.appliedrequest_id" class="process-date font-12 m-0">
                {{ filterOnModal.request_id }}
                <span v-if="filterOnModal.request_id" class="badge badge-icon rounded-3   text-white"
                  @click="clearFilter('form_status')">
                  <i class="ri-close-line close-icon text-dark rounded-3"></i>
                </span>
              </span>
              <span v-if="filterOnModal.requested_by && filterOnModal.appliedrequest_by"
                class="process-date font-12 m-0">
                {{ filterOnModal.requested_by }}
                <span v-if="filterOnModal.requested_by" class="badge badge-icon rounded-3   text-white"
                  @click="clearFilter('form_status')">
                  <i class="ri-close-line close-icon text-dark rounded-3"></i>
                </span>
              </span>
              <span v-if="filterOnModal.requested_department && filterOnModal.appliedrequested_department"
                class="process-date font-12 m-0">
                {{ filterOnModal.requested_department }}
                <span v-if="filterOnModal.requested_department" class="badge badge-icon rounded-3   text-white"
                  @click="clearFilter('form_status')">
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
                    <FormFields class="mb-3" tag="input" type="search" name="Requested" id="Requested"
                      placeholder="Search" v-model="filterOnModal.request_id" />
                  </div>
                  <div class="col-6">
                    <label class="font-13 ps-1" for="Requested">Form Name:</label>
                    <FormFields class="mb-3" tag="input" type="search" name="Requested" id="Requested"
                      placeholder="Search" v-model="filterOnModal.form_name" />
                  </div>
                  <div class="col-6">
                    <label class="font-13 ps-1" for="dept">Form Category:</label>
                    <FormFields tag="select" placeholder="Form Category" class="mb-3" name="dept"
                      v-model="filterOnModal.form_category" id="dept" :Required="false" />
                  </div>
                  <div class="col-6">
                    <label class="font-13 ps-1" for="dept">Accessible departments:</label>
                    <!-- <FormFields tag="select" placeholder="Accessible departments" class="mb-3"
                                            name="dept" v-model="filterOnModal.accessible_departments" id="dept" :Required="false"
                                            :options="accessibleDepartments" /> -->
                    <FormFields class="" tag="input" type="search" name="Requested" id="Requested" placeholder="Search"
                      v-model="filterOnModal.accessible_departments" />
                    <span class="m-0 font-10 ps-2">Note:Please seperate departments with commas</span>
                  </div>
                  <div class="col-6">
                    <label class="font-13 ps-1" for="dept">Status:</label>
                    <FormFields tag="select" placeholder="Status" class="mb-3" name="dept"
                      v-model="filterOnModal.form_status" id="dept" :Required="false" :options="['Active', 'Draft']" />
                  </div>

                  <div class="col-6">
                    <label class="font-13 ps-1" for="Requested">Requested By:</label>
                    <FormFields class="mb-3" tag="input" type="search" name="Requested" id="Requested"
                      placeholder="Search" v-model="filterOnModal.requested_by" />
                  </div>
                  <div class="col-6">
                    <label class="font-13 ps-1" for="Requested">Requested Department:</label>
                    <FormFields class="mb-3" tag="input" type="search" name="Requested" id="Requested"
                      placeholder="Search" v-model="filterOnModal.requested_department" />
                  </div>


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
            {{ selectedRequest }}
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
  { th: "Form name", td_key: "name" },
  { th: "Form category", td_key: "form_category" },
  { th: "Owner of form", td_key: "owner" },
  { th: "Requested by", td_key: "requested_by" },
  { th: "Requested department", td_key: "acess" },
  { th: "Approval Status", td_key: "status" },

]

)
const actions = ref(
  [
    { name: 'View Request', icon: 'fa-solid fa-eye' },

    { name: 'Share this form', icon: 'fa-solid fa-share-alt' },
    { name: 'Download Form', icon: 'fa-solid fa-download' },
    { name: 'Edit Form', icon: 'fa-solid fa-edit' },

  ]
)
const tableData = ref([]);
const filterOnModal = reactive({
  appliedform_name: false,
  appliedform_category: false,
  appliedaccessible_departments: false,
  appliedStatus: false,
  appliedrequest_id: false,
  appliedrequest_by: false,
  appliedrequested_department: false,
  form_name: '',
  form_category: '',
  accessible_departments: '',
  form_status: '',
  request_id: '',
  requested_by: '',
  requested_department: ''
})
const selectedRequest = ref({})
function actionCreated(rowData, actionEvent) {
  if (actionEvent.name === 'View Request') {
    if (rowData) {

      selectedRequest.value = { ...rowData }
      // selectedForm.value = rebuildToStructuredArray(JSON.parse(rowData?.form_json).fields)
      const modal = new bootstrap.Modal(document.getElementById('viewRequest'), {});// raise a modal
      modal.show();

    } else {
      console.warn(" There is no form fields ")

    }
  }

}
const appliedFiltersCount = computed(() => {
  return [
    { value: filterOnModal.form_category, applied: filterOnModal.appliedform_category },
    {
      value: filterOnModal.form_name,
      applied: filterOnModal.appliedform_name,
    },
    {
      value: filterOnModal.form_status,
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
      value: filterOnModal.requested_by,
      applied: filterOnModal.appliedrequest_by,
    },
    {
      value: filterOnModal.requested_department,
      applied: filterOnModal.appliedrequested_department,
    },


  ].filter((filter) => filter.applied && filter.value).length;
});
function clearFilter(type) {
  if (type === "form_name") {
    filterOnModal.form_name = "";
    filterOnModal.appliedform_name = false;
  } else if (type === "form_category") {
    filterOnModal.form_category = "";
    filterOnModal.appliedform_category = false;

  }
  else if (type === "accessible_departments") {
    filterOnModal.accessible_departments = "";
    filterOnModal.appliedaccessible_departments = false;

  }
  else if (type === "form_status") {
    filterOnModal.form_status = "";
    filterOnModal.appliedStatus = false;

  }
  else if (type === "request_id") {
    filterOnModal.request_id = "";
    filterOnModal.appliedrequest_id = false;

  }
  else if (type === "requested_by") {
    filterOnModal.requested_by = "";
    filterOnModal.appliedrequest_by = false;

  }
  else if (type === "requested_department") {
    filterOnModal.requested_department = "";
    filterOnModal.appliedrequested_department = false;

  }


  applyFilters();
}
function applyFilters() {
  filterOnModal.appliedform_name = Boolean(filterOnModal.form_name);
  filterOnModal.appliedform_category = Boolean(filterOnModal.form_category);
  filterOnModal.appliedaccessible_departments = Boolean(filterOnModal.accessible_departments);
  filterOnModal.appliedStatus = Boolean(filterOnModal.form_status);
  filterOnModal.appliedrequest_id = Boolean(filterOnModal.request_id);
  filterOnModal.appliedrequest_by = Boolean(filterOnModal.requested_by);
  filterOnModal.appliedrequested_department = Boolean(filterOnModal.requested_department);


}
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
function receivedForMe() {
  const filters = [
    // ["business_unit", "like", `%${newBusinessUnit.value.business_unit}%`]
  ];

  if (filterOnModal.form_name) {
    filters.push(["form_name", "like", `${filterOnModal.form_name}`]);
  }
  if (filterOnModal.form_category) {
    filters.push(["form_category", "like", `${filterOnModal.form_category}`]);
  }
  if (filterOnModal.accessible_departments) {
    filters.push(["accessible_departments", "like", `${filterOnModal.accessible_departments}`]);
  }
  if (filterOnModal.form_status) {
    filters.push(["form_status", "like", `${filterOnModal.form_status}`]);
  }
  if (filterOnModal.request_id) {
    filters.push(["request_id", "like", `${filterOnModal.request_id}`]);
  }
  if (filterOnModal.requested_by) {
    filters.push(["requested_by", "like", `${filterOnModal.requested_by}`]);
  }
  if (filterOnModal.requested_department) {
    filters.push(["requested_department", "like", `${filterOnModal.requested_department}`]);
  }
  const queryParams = {
    fields: JSON.stringify(["*"]),
    limit_page_length: filterObj.value.limitPageLength,
    limit_start: filterObj.value.limit_start,
    filters: JSON.stringify(filters),
    order_by: "`tabWF Workflow Requests`.`creation` desc",
  };
  const queryParamsCount = {
    fields: JSON.stringify(["count( `tabWF Workflow Requests`.`name`) AS total_count"]),
    limitPageLength: "None",
    filters: JSON.stringify(filters),
  }
  axiosInstance.get(`${apis.resource}${doctypes.WFWorkflowRequests}`, { params: queryParamsCount })
    .then((res) => {

      totalRecords.value = res.data[0].total_count

    })
    .catch((error) => {
      console.error("Error fetching ezyForms data:", error);
    });
  axiosInstance.get(apis.resource + doctypes.WFWorkflowRequests, { params: queryParams }).then((res) => {

    tableData.value = res.data;
  })
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