<template>
  <div class="position-relative">
    <div class=" back-to-same">

      <div class="container-fluid  p-0">
        <div class="backtofromPage asset_request px-2 py-2">
          <router-link :to="backTo" class="text-decoration-none text-dark font-13"><span> <i
                class="bi bi-arrow-left px-2"></i></span>Back</router-link>
        </div>
      </div>
    </div>


    <div class="approve_height">
      <div class="container-fluid">
        <div class="row">
          <div class="col-3"></div>
          <div class="col-6">
            <div class="mt-1">
              <div class="text-center">
                <div class="card border-0 shadow-none">
                  <div class="card-body pb-2 d-flex gap-2 align-items-center justify-content-center">
                    <h5 class="card-title">{{ selectedData.doctype_name }}</h5>
                    <div class="d-flex align-items-baseline gap-2 ps-1 ">
                      <span v-if="tableData?.status !== 'Completed' && tableData.status !== 'Request Cancelled'"
                        class="text-warning font-11 text-nowrap fw-bold">
                        Pending ({{ tableData.current_level }} /
                        {{ tableData?.total_levels }})</span>
                      <span class=" font-11 status_completed text-nowrap" v-if="tableData?.status === 'Completed'">
                        Approved
                      </span>
                      <span class=" font-11 requestRejected text-nowrap"
                        v-if="tableData?.status === 'Request Cancelled'">
                        Request Rejected
                      </span>
                    </div>
                    <!-- <span v-if="tableData?.status === 'Completed'"><i
                        class="bi approved-icon bi-check2-circle "></i></span>
                    <span v-if="tableData?.status === 'Request Cancelled'"><i
                        class="bi rejected-icon bi-x-circle"></i></span> -->
                  </div>
                </div>
              </div>                                                                                                                                                 
              <div class="position-relative ">
                <div class="requestPreviewDiv pb-5">

                  <ApproverPreview :blockArr="showRequest" :current-level="selectedcurrentLevel"
                    @updateTableData="approvalChildData" :childData="responseData" :readonly-for="selectedData.readOnly"
                    :childHeaders="tableHeaders" :employee-data="employeeData" @updateField="updateFormData" />

                </div>

                <div
                      v-if="selectedData?.type === 'myforms' &&
                            (tableData?.status === 'Request Raised' || tableData?.status === 'Request Cancelled') &&
                            selectedData?.type !== 'myapprovals'"
                      class="d-flex justify-content-end approveBtns">

                  <button type="submit" class="btn Edit_btn" @click.prevent="EditformSubmission()">
                    <span v-if="loading" class="spinner-border spinner-border-sm" role="status"
                      aria-hidden="true"></span>
                    <span v-if="!loading"><i class="bi bi-pencil-fill font-15 me-2"></i><span
                        class="font-12">Edit</span></span>
                  </button>
                </div>

                <div v-if="selectedData.type === 'mytasks'" class="">

                  <!-- v-if="!requestcancelled" -->
                  <div class="approveBtns pb-2 mb-2 mt-3 flex-column px-0 pe-4">
                    <!-- <div v-if="!canApprove & view_only_reportee === 1" class=" d-flex align-items-center gap-1">

                      <span class=" font-12 text-danger">
                        Note:
                      </span>
                      <span class=" fw-bold font-12">You don’t have permission to
                        Approve</span>
                    </div> -->

                    <div class="form-floating mb-2 p-1">
                      <!-- :disabled="view_only_reportee === 1" -->
                      <textarea  class="form-control font-12"
                        placeholder="Leave a comment here" id="floatingTextarea" @input="resetCommentsValidation"
                        :class="{ 'is-invalid': !isCommentsValid }" v-model="ApproverReason"></textarea>
                      <label class="font-11" for="floatingTextarea">Comments..</label>
                      <span v-if="!isCommentsValid" class="font-11 text-danger ps-1">Please enter comments**</span>
                    </div>
                    <div class=" d-flex justify-content-between ">
                      <div>
                        <button :disabled="rejectLoad "
                          class="btn btn-outline-danger font-10 py-0 rejectbtn" type="button"
                          @click="ApproverCancelSubmission(formData, 'Reject')">
                          <span v-if="rejectLoad" class="spinner-border spinner-border-sm" role="status"
                            aria-hidden="true"></span>
                          <span v-if="!rejectLoad"><i class="bi bi-x-lg fw-bolder font-12 me-2"></i><span
                              class="font-12">Reject</span></span>
                        </button>
                      </div>
                      <!-- v-if="selectedData.designation.includes('Security')" -->
                      <div class=" d-flex gap-2">


                        <!-- <div v-if="selectedData.designation?.toLowerCase().includes('security')">
                          <button :disabled="saveloading || (!canApprove & view_only_reportee === 1)" type="submit"
                            class="btn btn-outline-secondary" @click.prevent="SaveDocWithoutApprove(route.query.name)">
                            <span v-if="saveloading" class="spinner-border spinner-border-sm" role="status"
                              aria-hidden="true"></span>
                            <span v-if="!saveloading">
                              <span class="font-12 fw-bold">Save</span>
                            </span>
                          </button>

                        </div> -->
                        <div>
                          <button :disabled="loading " type="submit"
                            class="btn btn-success approvebtn"
                            @click.prevent="ApproverFormSubmission(emittedFormData, 'Approve')">
                            <span v-if="loading" class="spinner-border spinner-border-sm" role="status"
                              aria-hidden="true"></span>
                            <span v-if="!loading"><i class="bi bi-check-lg font-15 me-2"></i><span
                                class="font-12">Approve</span></span>
                          </button>

                        </div>
                      </div>
                    </div>

                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="col-3">
            <div class="activity-log-container px-1">
              <!-- <div class=" w-100  mb-2">
              <div class=" py-2 px-3">

                <h5 class="font-13 fw-bold">{{ selectedData.doctype_name }} form approval</h5>
              </div>
              <div class="py-2 px-3">
                <span class="text-warning font-12  fw-bold">
                  Pending ({{ tableData.current_level }} /
                  {{ tableData.total_levels }})</span>
              </div>
            </div> -->
              <!-- <div class="mt-5 mb-3 pt-2 d-flex justify-content-between align-items-center">
              <h6 class="font-14 ps-3  mb-0">Activity log <span
                  v-if="tableData?.status !== 'Completed' && tableData.status !== 'Request Cancelled'"
                  class="text-warning font-12  fw-bold">
                  Pending ({{ tableData.current_level }} /
                  {{ tableData?.total_levels }})</span>
                <span class=" font-11 status_completed" v-if="tableData?.status === 'Completed'">
                  Completed
                </span>
                <span class=" font-11 requestRejected" v-if="tableData?.status === 'Request Cancelled'">
                  Request Rejected
                </span>
              </h6>
              <button v-if="tableData.status === 'Completed'"
                class="btn btn-light font-12 fw-bold text-decoration-underline" type="button" @click="downloadPdf"><i
                  class="bi bi-arrow-down-circle fw-bold px-1"></i>Download
                PDF</button>
            </div> -->
              <div class="row mb-3">
                <!-- <div class="col-xl-3 col-lg-12 col-md-12">
                  <div class="d-flex  align-items-baseline  mt-2">
                   
                    <div class="d-flex align-items-baseline gap-2 ps-1 ">
                      <span v-if="tableData?.status !== 'Completed' && tableData.status !== 'Request Cancelled'"
                        class="text-warning font-11 text-nowrap fw-bold">
                        Pending ({{ tableData.current_level }} /
                        {{ tableData?.total_levels }})</span>
                      <span class=" font-11 status_completed text-nowrap" v-if="tableData?.status === 'Completed'">
                        Approved
                      </span>
                      <span class=" font-11 requestRejected text-nowrap"
                        v-if="tableData?.status === 'Request Cancelled'">
                        Request Rejected
                      </span>
                    </div>
                  </div>


                </div> -->
                <div class="col-xl-12 col-lg-12 col-md-12">
                  <div class=" d-flex justify-content-between gap-2">
                    
                    <div>
                      <button v-if="(selectedData.type === 'myforms' || selectedData.type === 'myteam' || selectedData.type === 'myapprovals' || selectedData.type === 'linkedForm') &&
                        linked_status !== 'Completed' &&
                        tableData?.status === 'Completed' &&
                        tableData?.is_linked_form &&

                        Object.keys(tableData.is_linked_form).length > 0" type="button"
                        class="btn btn-light font-14 nowrap h-auto fw-bold border border-dark CreateDepartments"
                        data-bs-target="#pdfView" @click="toLinkedForm">
                        Raise Inbound <i class="bi bi-arrow-right px-2"></i>
                      </button>



                    </div>
                    <div>
                      <button 
                      v-if="tableData.status === 'Completed' && linked_status !== 'Completed' || linked_status === 'Completed'"
                        
                        class="btn btn-light font-14 fw-bold h-0 nowrap border border-dark h-auto " type="button"
                        @click="downloadPdf"><i class="bi bi-download px-2 fw-bold"></i>Download
                      </button>
                    </div>
                    <!-- <button type="button" class="btn btn-outline-light font-12  CreateDepartments "
                      data-bs-toggle="modal" data-bs-target="#pdfView" @click="viewasPdfView">
                      Preview
                    </button> -->

                  </div>
                </div>
              </div>
              <div class="activity_height">
                <!-- Tabs -->
                <div class="d-flex mb-2 tabs_list">
                  <button class="btn btn-light tab_btn"
                    :class="{ active: activeTab === 'activity', 'border-0': !tableData.is_linked_form }"
                    @click="activeTab = 'activity'">
                    Activity Log
                  </button>
                  <button v-if="tableData.is_linked_form" class="btn btn-light tab_btn"
                    :class="{ active: activeTab === 'linked' }" @click="linked_list_btn">
                    Inbound Forms
                  </button>
                </div>

                <!-- Activity Log -->
                <div v-if="activeTab === 'activity'">
                  <!-- <div class="py-2">
                    <span class="font-12 text-nowrap fw-bold mb-0">Activity Log</span>
                  </div> -->
                  <div v-for="(item, index) in activityData" :key="index" class="activity-log-item"
                    :class="{ 'last-item': index === activityData.length - 1 }">
                    <div :class="item.action === 'Approved' || item.action === 'Request Raised' || item.action === '' || item.action === 'Completed'
                      ? 'activity-log-dot'
                      : 'activityRedDot'"></div>
                    <div class="activity-log-content">
                      <p class="font-12 mb-1">
                        
                        <span class="strong-content">{{ formatAction(item.action) }} on </span>
                        <span class="strong-content">{{ formatCreation( item.time) }}</span><br />
                        <span class="strong-content">{{ item.user_name }}</span><br />
                        <span>{{ item.role }}</span><br />
                        <span class="font-12 text-secondary">{{ item.reason || "N/A" }}</span>.
                        
                      </p>
                    </div>
                  </div>
                </div>

                <!-- Linked Forms -->
                <div v-else-if="activeTab === 'linked'">
                  <div v-if="linkedForms.length === 0" class="text-center py-3">
                    <p class="font-12 text-secondary">No linked forms available.</p>

                  </div>
                  <div v-else class="px-1">

                    <table class="table overflow-scroll  table-sm">
                      <thead class="table-light">
                        <tr>
                          <th class="font-12">S.No</th>
                          <th class="font-12">Request ID</th>
                          <th class="font-12">Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(item, index) in linkedForms" :key="index">
                          <td class="font-12 align-middle text-center">{{ index + 1 }}</td>
                          <td class="font-12 nowrap align-middle">{{ item.link_form_id.replace(/_/g, ' ') }}</td>
                          <td>
                            <button class="btn btn-light btn-sm font-14" data-bs-toggle="modal"
                              data-bs-target="#listofLinkedForms" @click="openModal(item)">
                              View
                            </button>
                          </td>
                        </tr>
                      </tbody>
                    </table>
                  </div>

                </div>
              </div>

              <!-- Modal -->
              <div class="modal fade" id="listofLinkedForms" tabindex="-1" aria-labelledby="exampleModalLabel"
                aria-hidden="true">
                <div class="modal-dialog modal-lg">
                  <div class="modal-content">
                    <div class="modal-header py-2">
                      <h5 class="modal-title font-14">Linked Form Details</h5>
                      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body linkedformspreview p-4">
                      <!-- Show key-value -->
                      <!-- <table class="table table-bordered table-sm">
                        <tbody>
                          <tr v-for="(item, index) in normalFields" :key="index">
                            <th class="font-12 text-nowrap">
                              {{ formatKey(item.key) }}
                            </th>
                            <td class="font-12">{{ item.value }}</td>
                          </tr>
                        </tbody>
                      </table> -->
                      <div class="row">
                        <div class=" col-md-12">
                          <div class="row">
                            <div class="col-md-6 mb-2 " v-for="(item, index) in normalFields" :key="index">
                              <label class="fw-bold font-12">{{ formatKey(item.key) }}</label>
                              <p class="font-12 mb-2">{{ item.value }}</p>
                            </div>
                          </div>
                        </div>
                        <!-- <div class=" col-md-6 ">
                          <div v-for="(item, index) in linkedActivity" :key="index" class="activity-log-item"
                            :class="{ 'last-item': index === linkedActivity.length - 1 }">
                            <div :class="item.action === 'Approved' || item.action === 'Request Raised' || item.action === '' || item.action === 'Completed'
                              ? 'activity-log-dot'
                              : 'activityRedDot'"></div>
                            <div class="activity-log-content">
                              <p class="font-12 mb-1">
                                <span class="strong-content">{{ formatAction(item.action) }} on </span>
                                <span class="strong-content">{{ formatCreation(item.creation) }}</span><br />
                                <span class="strong-content">{{ item.user_name }}</span><br />
                                <span>{{ item.role }}</span><br />
                                <span class="font-12 text-secondary">{{ item.reason || "N/A" }}</span>.
                              </p>
                            </div>
                          </div>
                        </div> -->
                      </div>



                      <!-- 🔥 Array Fields -->
                      <div v-for="(arrayItem, key) in arrayFields" :key="key" class="mb-3 overflow-auto">
                        <strong class="font-12">{{ formatKey(key) }}</strong>
                        <table class="table table-bordered table-sm">
                          <thead class="table-light">
                            <tr>
                              <th v-for="header in getFilteredKeys(arrayItem)" :key="header" class="font-12">
                                {{ formatKey(header) }}
                              </th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="(row, rowIndex) in arrayItem" :key="rowIndex">
                              <td v-for="header in getFilteredKeys(arrayItem)" :key="header" class="font-12">
                                {{ row[header] }}
                              </td>
                            </tr>
                          </tbody>
                        </table>
                      </div>



                    </div>
                  </div>
                </div>
              </div>


            </div>
            <div class="modal fade" id="pdfView" tabindex="-1" aria-labelledby="pdfViewLabel" aria-hidden="true">
              <div class="modal-dialog modal-xl">
                <div class="modal-content">
                  <div class="modal-header py-2 d-block bg-dark text-white">
                    <div class="d-flex justify-content-between align-items-center">
                      <div>
                        <h5 class="m-0 text-white font-13" id="exampleModalLabel">
                          PDF format
                        </h5>
                      </div>
                      <div class="">
                        <button button="button" class="btn btn-dark text-white font-13" @click="downloadPdf">
                          Download Pdf<span class="ms-2"><i class="bi bi-download"></i></span>
                        </button>
                        <button type="button" class="btn btn-dark text-white font-13" @click="closemodal"
                          data-bs-dismiss="modal">
                          Close <i class="bi bi-x"></i>
                        </button>
                      </div>
                    </div>
                  </div>
                  <div class="modal-body pdf-body">
                    <div v-html="pdfPreview"></div>
                  </div>
                  <div class="modal-footer"></div>
                </div>
              </div>
            </div>

            <!-- <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">

            <div class="offcanvas-header">
              <h5 class="offcanvas-title" id="offcanvasRightLabel">Offcanvas right</h5>
              <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
            </div>
            <div class="offcanvas-body">
              <div v-html="pdfPreview"></div>
            </div>
          </div> -->
          </div>
        </div>
      </div>
    </div>


  </div>
</template>

<script setup>
import {ref, watch, computed } from "vue";
import ApproverPreview from "./ApproverPreview.vue";
import { useRoute, useRouter } from "vue-router";
import axiosInstance from "../shared/services/interceptor";
import { apis, doctypes, domain } from "../shared/apiurls";
import { EzyBusinessUnit } from "../shared/services/business_unit";
import { rebuildToStructuredArray } from "../shared/services/field_format";
// import ButtonComp from "./ButtonComp.vue";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
const route = useRoute();

const selectedData = ref({
  routepath: route.query.routepath,
  formname: route.query.name || "", // Retrieve from query
  doctype_name: route.query.doctype_name || "", // Retrieve from query
  type: route.query.type || "", // Retrieve from query
  readOnly: route.query.readOnly, // Retrieve from query
  business_unit: route.query.business_unit || "", // Retrieve from query
  designation: route.query.designation || "", // Retrieve from query
});
const backTo = ref(selectedData.value.routepath);


const router = useRouter();
const linked_status = ref('')
const businessUnit = computed(() => EzyBusinessUnit.value);
const business_unit = ref('');
const filterObj = ref({ limitPageLength: "None", limit_start: 0 });
const totalRecords = ref(0);
const tableData = ref([]);
const emittedFormData = ref([]);
const showRequest = ref(null);
const isCommentsValid = ref(true);
const activityData = ref([]);
const ApproverReason = ref("");
const selectedcurrentLevel = ref("");
const selectedtotalLevels = ref("");
const doctypeForm = ref([]);
const loading = ref(false);
const rejectLoad = ref(false)
const saveloading = ref(false)
const pdfPreview = ref("");
const tableRows = ref([]);
const tableHeaders = ref([]);
const tableName = ref("");
const responseData = ref([]);
const employeeData = ref([]);
const viewlist = ref([])
// const view_only_reportee = ref(0);
const linkedNew_Id = ref([]);
const mainStandardForm = ref('')
const activeTab = ref("activity");
const linkedActivity = ref([]);

const resetCommentsValidation = () => {
  if (ApproverReason.value.trim() !== "") {
    // If comment is not empty, set isCommentsValid to true
    isCommentsValid.value = true;
  }
};
function formatCreation(dateStr) {
  const [datePart, timePart] = dateStr.split(' ');
  const [year, month, day] = datePart.split('/');
  const [hour = '00', minute = '00', second = '00'] = timePart.split(':');

  const formattedDate = [
    day.padStart(2, '0'),
    month.padStart(2, '0'),
    year
  ].join('-');

  const formattedTime = [
    hour.padStart(2, '0'),
    minute.padStart(2, '0'),
    second.padStart(2, '0')
  ].join(':');

  return `${formattedDate} ${formattedTime}`;
}


const ApprovePDF = ref(true)

// Format the date for display
// const formatDate = (dateString) => {
//   if (!dateString) return "N/A";
//   const date = new Date(dateString);
//   return date.toLocaleDateString("en-GB");
// };

// Format action text (cancelled or raised)

// onMounted(() => {
//   const storedData = localStorage.getItem("employeeData");
//   try {
//     const parsedData = JSON.parse(storedData);

//     // Ensure parsedData is an array
//     employeeData.value = Array.isArray(parsedData) ? parsedData : [parsedData];

//   } catch (error) {
//     console.error("Error parsing employeeData from localStorage:", error);
//     employeeData.value = []; // Fallback to empty array if there's an error
//   }

// });


function EditformSubmission() {
  const query = {
    routepath: '/todo/raisedbyme',
    business_unit: route.query.property,
    selectedForm: route.query.doctype_name,
    selectedFormId: route.query.name,
    selectedFormStatus: route.query.status,
    ...(tableData.value.linked_form_id && { main_form_Id: tableData.value.linked_form_id }),
    ...(doctypeForm.value.return_gate_pass_name && { main_form: doctypeForm.value.return_gate_pass_name })
  };

  router.push({
    name: "RaiseRequest",
    query
  });
}

// console.log("emittedFormData", emittedFormData.value);
watch(
  businessUnit,
  (newVal) => {
    const local = localStorage.getItem("Bu")
    business_unit.value = newVal;
    business_unit.value = local
    if (newVal) {
      // console.log(business_unit.value, newVal, "ll");
      // if (selectedData.value.type === "mytasks") {
      //   ViewOnlyRe();
      // } else {
        receivedForMe()
      // }
    }
  },
  { immediate: true }
);

const childtablesData = ref({});
function approvalChildData(data) {
  childtablesData.value = data;
  // console.log(data);
}



const formatAction = (action) => {
  if (!action) return "performed an action on";
  const actionMap = {
    "Request Cancelled": "cancelled",
    "Request Raised": "Request initiated",
  };
  return actionMap[action] || action;
};
// Function to capture the form data from ApproverPreview
const updateFormData = (fieldValues) => {
  // console.log(fieldValues, "pp");
  // console.log(emittedFormData.value);

  // Ensure emittedFormData.value is an array before updating
  emittedFormData.value = [
    ...emittedFormData.value.filter(field => field.fieldname !== fieldValues.fieldname),
    fieldValues
  ];

  // console.log(emittedFormData.value, "======");
};
const linkedForms = ref([]);

// Modal Selected Item
const selectedLinkedForm = ref({});

function openModal(item) {
  // selectedLinkedForm.value = item;
  axiosInstance
    .get(
      `${apis.resource}${tableData.value.is_linked_form}/${item.link_form_id}`
    )
    .then((res) => {
      selectedLinkedForm.value = res.data;

    })
    .catch((error) => {
      console.error(`Error fetching data for :`, error);
    });
  // axiosInstance
  //   .get(`${apis.resource}${doctypes.WFActivityLog}/${item.link_form_id}`)
  //   .then((res) => {
  //     if (res.data) {
  //       // console.log(res.data);
  //       linkedActivity.value = res.data.reason;
  //       // activityData.value = res.data.reason || []; // Ensure it's always an array
  //     }
  //   })
  //   .catch((error) => {
  //     console.log(error)
  //   });



}
const excludedFields = [
  "name",
  "owner",
  "creation",
  "modified",
  "modified_by",
  "docstatus",
  "idx",
  "parent",
  "parentfield",
  "parenttype",
  "doctype"
];

// ✅ Normal key-value fields
const normalFields = computed(() => {
  return Object.entries(selectedLinkedForm.value)
    .filter(
      ([key, value]) =>
        !excludedFields.includes(key) && !Array.isArray(value)
    )
    .map(([key, value]) => ({ key, value }));
});

// ✅ Array fields (like items)
const arrayFields = computed(() => {
  const result = {};
  for (const [key, value] of Object.entries(selectedLinkedForm.value)) {
    if (Array.isArray(value) && !excludedFields.includes(key)) {
      result[key] = value;
    }
  }
  return result;
});

// ✅ Filter keys in table headers
function getFilteredKeys(arr) {
  if (!arr.length) return [];
  return Object.keys(arr[0]).filter(
    (key) => !excludedFields.includes(key)
  );
}

// ✅ Format key to look pretty
function formatKey(key) {
  return key
    .replace(/_/g, " ")
    .replace(/\b\w/g, (l) => l.toUpperCase());
}
function linked_list_btn() {
  activeTab.value = 'linked'
  fetching_linked_doc_list()
}

function fetching_linked_doc_list() {
  // console.log(selectedData.value.name);
  let data = {
    standard_form_id: route.query.name ? route.query.name : '',
    linked_form_name: tableData.value.is_linked_form ? tableData.value.is_linked_form : '',
  }

  // console.log(ViewOnlyReportee.value); 
  axiosInstance
    .post(apis.linked_doc_list, data)
    .then((response) => {
      // console.log(response.message);
      linkedForms.value = response.message;

    })
    .catch((error) => {
      console.log(error);
    });


}

const ChildTableData = async () => {
  const childEntries = Object.entries(childtablesData.value);

  if (!childEntries.length) return;

  const formPromises = childEntries.map(([tableName, rows]) => {
    if (!rows || !rows.length) {
      console.warn(`⚠ Skipping empty child table: ${tableName}`);
      return null;
    }

    const form = {
      doctype: selectedData.value.doctype_name,
      company_field: business_unit.value,
      [tableName]: rows
    };

    const formData = new FormData();
    formData.append("doc", JSON.stringify(form));
    formData.append("action", "Save");

    return axiosInstance.post(apis.savedocs, formData);
  }).filter(Boolean);

  try {
    const responses = await Promise.all(formPromises);
    return responses; // Return if needed
  } catch (error) {
    console.error("❌ Error submitting child tables:", error);
    throw error; // Important: so raiseRequestSubmission halts
  }
};
// Function to handle form submission
async function ApproverFormSubmission(dataObj, type) {
  // if (ApproverReason.value.trim() === "") {
  //   isCommentsValid.value = false; // Show validation error
  //   return; // Stop execution
  // }


  // isCommentsValid.value = true;
  loading.value = true; // Start loader

  let form = {
    // ...childtablesData.value
  };
  if (Array.isArray(emittedFormData.value) && emittedFormData.value.length) {
    emittedFormData.value.forEach((each) => {
      form[each.fieldname] = each.value;
    });
  }
  // try {
  //   // ✅ Submit child table data first
  //   await ChildTableData();
  // } catch (error) {
  //   toast.error("❌ Child table submission failed");
  //   loading.value = false;
  //   return;
  // }


  axiosInstance
    .put(`${apis.resource}${selectedData.value.doctype_name}/${doctypeForm.value.name}`, form)
    .then((response) => {
      if (response?.data) {
        approvalStatusFn(dataObj, type);
      } else {
        loading.value = false; // Stop loader on failure
        toast.error("Failed to submit form", { autoClose: 1000, transition: "zoom" });
      }
    })
    .catch((error) => {
      console.error("Error submitting form:", error);
      loading.value = false; // Stop loader on error
      toast.error("An error occurred while submitting the form.", { autoClose: 1000, transition: "zoom" });
    });
}


const dataObje = ref([])
// Function to handle approval status
function approvalStatusFn(dataObj, type) {
  dataObje.value = dataObj;
  // console.log("Approval Data:", dataObj);

  let data = {
    property: tableData.value.property,
    doctype: tableData.value.doctype_name,
    request_ids: [tableData.value.name],
    reason: ApproverReason.value ? ApproverReason.value : "Approved",
    action: type,
    files: null,
    cluster_name: null,
    url_for_approval_id: "",
    current_level: tableData.value.current_level,
  };

  axiosInstance
    .post(apis.requestApproval, { request_details: [data] })
    .then((response) => {
      // console.log("API Response:", response);


      // console.log(selectedcurrentLevel.value === selectedtotalLevels.value, "current level and total level");
      if (response?.message?.success === true) {
        if (selectedcurrentLevel.value === selectedtotalLevels.value && mainStandardForm.value.length && doctypeForm.value.return_gate_pass_name.length) {
          DynamicCalculateMethod(); // Call this only if it's the last level
        }
        // DynamicCalculateMethod()
        ApproverReason.value = ""; // Clear reason after success
        toast.success(`Request ${type}ed`, {
          autoClose: 500,
          transition: "zoom",
          onClose: () => {
            router.push({ path: selectedData.value.routepath }); // Navigate after toast closes
          }
        });
      } else {
        toast.error(`Failed to ${type} request`, { autoClose: 1000, transition: "zoom" });
      }
    })
    .catch((error) => {
      console.error("Error processing request:", error);
      toast.error("An error occurred while processing your request.", { autoClose: 1000, transition: "zoom" });
    })
    .finally(() => {
      loading.value = false; // Ensure loader stops
    });
}
function DynamicCalculateMethod() {
  const dataObj = {
    request_id: linkedNew_Id.value,
    doctype_1: mainStandardForm.value,
    doctype_2: tableData.value.doctype_name
  };

  axiosInstance
    .post(apis.dynmic_calculations, dataObj)
    .then((response) => {
      console.log(response);

    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}
// async function SaveDocWithoutApprove(request_id) {
//   saveloading.value = true;
//   let form = {
//     ...childtablesData.value
//   };
//   if (Array.isArray(emittedFormData.value) && emittedFormData.value.length) {
//     emittedFormData.value.forEach((each) => {
//       form[each.fieldname] = each.value;
//     });
//   }
//   // try {
//   //   // ✅ Submit child table data first
//   //   await ChildTableData();
//   // } catch (error) {
//   //   toast.error("❌ Child table submission failed");
//   //   loading.value = false;
//   //   return;
//   // }
//   // console.log(loading.value, dataObj, type, form);

//   axiosInstance
//     .put(`${apis.resource}${selectedData.value.doctype_name}/${doctypeForm.value.name}`, form)
//     .then((response) => {
//       if (response?.data) {

//         const EmpRequestdesignation = JSON.parse(
//           localStorage.getItem("employeeData")
//         );
//         // console.log(EmpRequestdesignation,"emp data");

//         let data = {
//           request_id: request_id,
//           reason: ApproverReason.value ? ApproverReason.value : "Approved",
//           current_level: selectedcurrentLevel.value,
//           user: EmpRequestdesignation.emp_mail_id,
//           role: EmpRequestdesignation.designation
//         };

//         axiosInstance
//           .post(apis.ActivitySaveComment, data)
//           .then((response) => {
//             if (response?.message?.success === true) {
//               ApproverReason.value = ""; // Clear reason after success
//               saveloading.value = false
//               window.location.reload()
//               // receivedForMe()

//             } else {
//               toast.error(`Failed to request`, { autoClose: 1000, transition: "zoom" });
//             }
//           })
//           .catch((error) => {
//             console.error("Error processing request:", error);
//             toast.error("An error occurred while processing your request.", { autoClose: 1000, transition: "zoom" });
//           })



//       } else {
//         loading.value = false; // Stop loader on failure
//         toast.error("Failed to submit form", { autoClose: 1000, transition: "zoom" });
//       }
//     })
//     .catch((error) => {
//       console.error("Error submitting form:", error);
//       loading.value = false; // Stop loader on error
//       toast.error("An error occurred while submitting the form.", { autoClose: 1000, transition: "zoom" });
//     });
//   // console.log(request_id,"data");
//   // console.log(selectedcurrentLevel.value,"current level");
//   // console.log(ApproverReason.value,"reason");

// }


function ApproverCancelSubmission(dataObj, type) {

  // if (ApproverReason.value.trim() === "") {
  //   isCommentsValid.value = false;
  //   return;
  // }

  // isCommentsValid.value = true;
  rejectLoad.value = true; // Start loader




  let form = {};
  if (emittedFormData.value.length) {
    emittedFormData.value.map((each) => {
      form[each.fieldname] = each.value;
    });
  }
  axiosInstance
    .put(`${apis.resource}${selectedData.value.doctype_name}/${doctypeForm.value.name}`, form)
    .then((response) => {
      if (response?.data) {
        approvalCancelFn(dataObj, type);
      } else {
        rejectLoad.value = false; // Stop loader on failure
        toast.error("Failed to cancel request", { autoClose: 1000, transition: "zoom" });
      }
    })
    .catch((error) => {
      console.error("Error cancelling request:", error);
      rejectLoad.value = false; // Stop loader on error
      toast.error("An error occurred while cancelling the request.", { autoClose: 1000, transition: "zoom" });
    });
}



// function approvalCancelFn(dataObj, type) {
//   // let files = this.selectedFileAttachments.map((res: any) => res.url);

//   console.log(dataObj, "data");

//   let data = {
//     property: selectedRequest.value.property,
//     doctype: selectedRequest.value.doctype_name,
//     request_id: selectedRequest.value.name,
//     reason: type == "Request Cancelled" ? "Cancelled" : "",
//     action: type,
//     files: [],
//     url_for_cancelling_id: "",
//     current_level: selectedRequest.value.current_level,
//   };
//   axiosInstance.post(apis.wf_cancelling_request, data).then((response) => {
//     if (response?.message?.success) {
//       router.push({
//         name: "ReceivedForMe",
//       });
//     }
//   });
// }

function approvalCancelFn(dataObj, type) {
  // console.log("approvalCancelFn Data:", dataObj);
  dataObje.value = dataObj;

  let data = {
    property: tableData.value.property,
    doctype: tableData.value.doctype_name,
    request_ids: [tableData.value.name],
    reason: ApproverReason.value ? ApproverReason.value : "Reject",
    action: type,
    files: null,
    cluster_name: null,
    url_for_approval_id: "",
    current_level: tableData.value.current_level,
  };

  axiosInstance
    .post(apis.requestApproval, { request_details: [data] })
    .then((response) => {
      if (response?.message) {
        toast.success(`${type}`, {
          autoClose: 500,
          transition: "zoom",
          onClose: () => {
            router.push({ name: "ReceivedForMe" }); // Navigate after toast
          },
        });
      } else {
        toast.error(`Failed to ${type} request`, { autoClose: 1000, transition: "zoom" });
      }
    })
    .catch((error) => {
      console.error("Error processing cancellation:", error);
      toast.error("An error occurred while cancelling the request.", { autoClose: 1000, transition: "zoom" });
    })
    .finally(() => {
      rejectLoad.value = false; // Ensure loader stops
    });
}

function receivedForMe(data) {
  // Initialize filters array for building dynamic query parameters
  const EmpRequestdesignation = JSON.parse(
    localStorage.getItem("employeeData")
  );
  const filters = [
    ["property", "like", `%${businessUnit.value}%`],
    ["name", "like", `%${selectedData.value.formname}%`],
  ];
  if (data) {
    filters.push(data);
  }
  if (selectedData.value.type !== 'myteam' && selectedData.value.type !== 'myapprovals' && selectedData.value.type !== 'linkedForm') {
    if (selectedData.value.type == "myforms") {
      filters.push(["requested_by", "like", EmpRequestdesignation.emp_mail_id]);
    } else {
      filters.push([
        "assigned_to_users",
        "like",
        `%${EmpRequestdesignation?.designation}%`,
      ]);
    }
  }

  const queryParams = {
    fields: JSON.stringify(["*"]),
    filters: JSON.stringify(filters),
  };

  // const queryParamsCount = {
  //   fields: JSON.stringify(["count(name) AS total_count"]),
  //   limitPageLength: "None",
  //   filters: JSON.stringify(filters),
  // };

  // // Fetch total count of records matching filters
  // axiosInstance
  //   .get(`${apis.resource}${doctypes.WFWorkflowRequests}`, {
  //     params: queryParamsCount,
  //   })
  //   .then((res) => {
  //     totalRecords.value = res.data[0].total_count;
  //   })
  //   .catch((error) => {
  //     console.error("Error fetching total count:", error);
  //   });

  // Fetch the records matching filters
  axiosInstance
    .get(`${apis.resource}${doctypes.WFWorkflowRequests}`, {
      params: queryParams,
    })
    .then((res) => {
      tableData.value = res.data[0];

      selectedcurrentLevel.value = tableData.value?.current_level;
      selectedtotalLevels.value = tableData.value?.total_levels;
      selectedData.value.doctype_name = tableData.value?.doctype_name
      // console.log(selectedcurrentLevel.value, " current_level");
      //  console.log(tableData.value.is_linked_form, "is_linked_form==========");

      showRequest.value = rebuildToStructuredArray(
        JSON.parse(tableData.value?.json_columns).fields
      );
      // console.log(JSON.parse(
      //   tableData.value?.json_columns
      // ).workflow, "workflow");
      // view_only_reportee.value = JSON.parse(tableData.value?.json_columns)?.workflow[selectedcurrentLevel.value]?.view_only_reportee;
      // console.log(" wrk === =>", view_only_reportee.value);
      tableHeaders.value = JSON.parse(
        tableData.value?.json_columns
      ).child_table_fields;

      // console.log(tableHeaders.value, "req");
      if (res.data.length) {
        Wfactivitylog(tableData.value.name);
        getdata(tableData.value.name);


      }

    })
    .catch((error) => {
      console.error("Error fetching records:", error);
    });
}

function getdata(formname) {
  const filters = [["wf_generated_request_id", "like", `%${formname}%`]];
  const queryParams = {
    fields: JSON.stringify(["*"]),
    limit_page_length: "None",
    limit_start: 0,
    filters: JSON.stringify(filters),
    order_by: `\`tab${selectedData.value.doctype_name}\`.\`creation\` desc`,
  };

  // Fetch the doctype data
  axiosInstance
    .get(`${apis.resource}${selectedData.value.doctype_name}`, {
      params: queryParams,
    })
    .then((res) => {
      if (res.data) {
        doctypeForm.value = res.data[0];

        if (doctypeForm.value.returnable_gate_pass_id) {
          // console.log(doctypeForm.value.returnable_gate_pass_id, 'returnable_gate_pass_id');
          linkedNew_Id.value = doctypeForm.value.returnable_gate_pass_id;
        }

        if (doctypeForm.value.form_status == "Completed") {
          // console.log(doctypeForm.value.form_status, 'linked_status');
          linked_status.value = doctypeForm.value.form_status;

        }
        // console.log(doctypeForm.value.return_gate_pass_name);

        if (doctypeForm.value.return_gate_pass_name) {
          mainStandardForm.value = doctypeForm.value.return_gate_pass_name;
        }


        mapFormFieldsToRequest(doctypeForm.value, showRequest.value);

        // axiosInstance
        //   .get(`${apis.resource}${selectedData.value.doctype_name}`)
        //   .then((res) => {
        //     datanew.value =res.data[0]
        //     // console.log(`Data for :`, res.data[0]);
        //   })
        //   .catch((error) => {
        //     console.error(`Error fetching data for :`, error);
        //   });
        axiosInstance
          .get(
            `${apis.resource}${selectedData.value.doctype_name}/${doctypeForm.value.name}`
          )
          .then((res) => {
            // console.log(`Data for :`, res.data);
            // Identify the child table key dynamically
            const childTables = Object.keys(res.data).filter((key) =>
              Array.isArray(res.data[key])
            );
            if (childTables.length) {
              responseData.value = {};

              childTables.forEach((tableKey) => {
                responseData.value[tableKey] = res.data[tableKey] || [];
              });
              // NewActivityLogData(res.data.name) 
              // console.log("Response Data:", responseData.value);
            }
          })
          .catch((error) => {
            console.error(`Error fetching data for :`, error);
          });

        // Map values from doctypeForm to showRequest fields
      }
    })
    .catch((error) => {
      console.error("Error fetching categories data:", error);
    });
}
// function ViewOnlyRe() {
//   const queryParams = {
//     fields: JSON.stringify(["*"]),
//     limit_page_length: "None",
//     limit_start: 0,

//   };

//   axiosInstance
//     .post(apis.view_only_reportee, {
//       params: queryParams,
//     })
//     .then((response) => {

//       viewlist.value = response.message;

//       canApprove.value = viewlist.value.includes(selectedData.value.formname);
//       receivedForMe()

//     })
//     .catch((error) => {
//       console.log(error);
//     });

// }
function viewasPdfView() {

  ApprovePDF.value = !ApprovePDF.value;
  const dataObj = {
    form_short_name: tableData.value.doctype_name,
    name: doctypeForm.value.name,
    business_unit: business_unit.value

  };

  axiosInstance
    .post(apis.preview_dynamic_form, dataObj)
    .then((response) => {
      pdfPreview.value = response.message;
      if (response.message) {

      }



    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}


function downloadPdf() {
  const dataObj = {
    form_short_name: tableData.value.doctype_name,
    name: doctypeForm.value.name,
    business_unit: business_unit.value
  };

  axiosInstance
    .post(apis.download_pdf_form, dataObj)
    .then((response) => {
      if (!response || !response.message) {
        console.error("Invalid response:", response);
        return;
      }

      let pdfUrl = domain + response.message;

      // Remove '/api' from the URL if present
      pdfUrl = pdfUrl.replace("/api", "");

      // Extract filename safely
      const fileName = response.message.includes("/")
        ? response.message.split("/").pop()
        : "download.pdf";

      // Create and trigger download
      const link = document.createElement("a");
      link.href = pdfUrl;
      link.download = fileName;
      link.target = "_blank"; // Helps with some browser restrictions
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    })
    .catch((error) => {
      console.error("Error downloading PDF:", error);
    });
}

// const openFile = (filePath) => {
//   if (!filePath) return;
//   const fileUrl = `${filePath}`;
//   window.open(fileUrl, "_blank");
// };

// const isFilePath = (value) => {
//   if (!value) return false;
//   return /\.(png|jpg|jpeg|gif|pdf|docx|xlsx|txt)$/i.test(value);
// };

// function childFunction() {
//   axiosInstance
//     .get(
//       `${apis.resource}${selectedData.value?.selectedform}/${childIDs.value}`
//     )
//     .then((res) => {
//       console.log(`Data for :`, res.data);
//       responseData.value = res.data;
//     })
//     .catch((error) => {
//       console.error(`Error fetching data for :`, error);
//     });
// }

// function Wfactivitylog(formname) {
//   axiosInstance
//     .get(`${apis.resource}${doctypes.WFActivityLog}/${formname}`)
//     .then((res) => {
//       if (res.data && Array.isArray(res.data.reason)) {
//         const sortedReasons = res.data.reason.sort((a, b) => {
//           const parseTime = (str) => {
//             const [datePart, timePart] = str.split(' ');
//             const [year, month, day] = datePart.split('/').map(Number);
//             const [hour, minute, second, millisecond = 0] = timePart.split(':').map(Number);
//             return new Date(year, month - 1, day, hour, minute, second, millisecond);
//           };

//           return parseTime(a.time) - parseTime(b.time); // ascending order
//         });

//         activityData.value = sortedReasons;
//       } else {
//         activityData.value = [];
//       }
//     })
//     .catch((error) => {
//       console.error("Error fetching activity data:", error);
//     });
// }

function Wfactivitylog(name) {
  // console.log(route.query.name, "wf_generated_request_id"); 
 let FormId = {
  wf_generated_request_id : name,
 }
  axiosInstance
  .post(apis.get_wf_activate_log, FormId)
  .then((responce)=>{
    // console.log(responce, "activity log data"); 
    activityData.value = responce.message || []; // Ensure it's always an array

  })
   .catch((error) => {
      console.error("Error fetching data:", error);
    });
  // axiosInstance
  //   .get(`${apis.resource}${doctypes.WFActivityLog}/${formname}`)
  //   .then((res) => {
  //     if (res.data && Array.isArray(res.data.reason)) {
  //       const sortedReasons = res.data.reason.sort((a, b) => {
  //         const parseTime = (str) => {
  //           // str = "2025/7/16 12:9:56:795919"
  //           const [datePart, timePart] = str.split(' ');
  //           const [year, month, day] = datePart.split('/').map(Number);

  //           const timeParts = timePart.split(':').map(Number);
  //           const hour = timeParts[0] || 0;
  //           const minute = timeParts[1] || 0;
  //           const second = timeParts[2] || 0;
  //           const millisecond = timeParts[3] || 0;

  //           return new Date(year, month - 1, day, hour, minute, second, millisecond);
  //         };

  //         return parseTime(a.time) - parseTime(b.time); // Sort in ascending order
  //       });

  //       activityData.value = sortedReasons;
  //     } else {
  //       activityData.value = [];
  //     }
  //   })
  //   .catch((error) => {
  //     console.error("Error fetching activity data:", error);
  //   });
}

function toLinkedForm() {
  if (tableData.value.is_linked_form && linked_status.value !== 'Completed') {
    router.push({
      name: "RaiseRequest",
      query: {
        routepath: route.path,
        linkedForm: tableData.value.is_linked_form,
        has_workflow: 'Yes',
        type: selectedData.value.type,
        main_form: selectedData.value.doctype_name,
        business_unit: selectedData.value.business_unit,
        main_form_Id: selectedData.value.formname,
        
      },
    });
  } else {
    toast.error("No linked form available", { autoClose: 1000, transition: "zoom" });
  }

  // console.log("Linked Form Data:", tableData.value.is_linked_form);
  // console.log("Selected Data:", selectedData.value);

}

function NewActivityLogData(name) {

  const dataObj = {
    doctype: selectedData.value.doctype_name,
    docname: name,

  };

  axiosInstance
    .post(apis.activityLogWithChild, dataObj)
    .then((response) => {
      pdfPreview.value = response.message;
      if (response.message) {

      }



    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}
function mapFormFieldsToRequest(doctypeData, showRequestData) {
  showRequestData.forEach((block) => {
    block.sections.forEach((section) => {
      section.rows.forEach((row) => {
        row.columns.forEach((column) => {
          column.fields.forEach((field) => {
            // Check if the fieldname exists in the doctypeForm and assign the value
            if (doctypeData?.hasOwnProperty(field?.fieldname)) {
              field.value = doctypeData[field?.fieldname]; // Assign the value from doctypeForm to the field
            }
          });
        });
      });
    });
  });
}

const requestcancelled = computed(() => {
  if (activityData.value.length === 0) return false;
  const lastAction = activityData.value[activityData.value.length - 1];
  return lastAction.action === "Request Cancelled";
});
const activityDatalog = ref([]);
watch(activityData, (newVal) => {
  // console.log("Updated Activity Data:", newVal);
  activityDatalog.value = newVal;
  // console.log("Request Cancelled?", requestcancelled.value);
  activityDatalog.value = requestcancelled.value
});


</script>

<style lang="scss" scoped>
// .backtofromPage {
//   position: sticky !important;
//   top: 0 !important;
//   z-index: 1000 !important;

// }
.linkedformspreview {
  height: 700px;
  overflow: scroll;
}

.approve_height {
  overflow: hidden;
  height: 85vh;
}

.approved-icon {
  color: #2BED12;
  font-size: 24px;
}

.rejected-icon {
  color: #d75159;
  font-size: 24px;
}

.Edit_btn {
  width: 100px;
  background: rgb(34, 33, 33);
  color: white;
  padding: 5px 15px 5px 15px;
  gap: 7px;
  border-radius: 4px;
  opacity: 0px;
  font-weight: bold;
}


.approvebtn {
  width: 146px;
  //height: 30px;
  background: #099819;
  color: white;
  padding: 5px 15px 5px 15px;
  gap: 7px;
  border-radius: 4px;
  opacity: 0px;
  font-weight: bold;
}

.requestPreviewDiv {
  height: 75vh;
  overflow-y: auto;
  //padding-bottom: 100px;
  margin-bottom: 100px;

}

.rejectbtn {
  width: 146px;
  //height: 30px;
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

.approvediv {
  position: fixed !important;
  bottom: 0;
  z-index: 10;
  background-color: #fff;
}

.approveBtns {
  position: fixed !important;
  bottom: 0;
  z-index: 10;
  background-color: #fff;
  padding: 5px 10px;
  display: flex;
  justify-content: space-between;
  width: 50%;
}

.asset_request {
  //box-shadow: 0px 2px 4px 0px #0000000D;
  box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
}

.is-invalid {
  border: 1px solid red;
}

/* Activity log container */
.activity-log-container {
  width: 100%;
  margin-top: 20px;
  //padding-left: 30px;
  position: relative;
}

/* Activity log item */
.activity-log-item {
  position: relative;
  display: flex;
  align-items: flex-start;
  /* Ensure dot and text align properly */
  gap: 10px;
  padding-left: 15px;
  /* Space between dot and text */
  margin-bottom: 10px;
  /* Space between logs */
}

.activity_height {
  height: 80vh;
  overflow-y: scroll;
  position: relative;
}
.tabs_list{
    position: sticky;
    top: 0;
    background-color: #fff !important;
    padding-bottom: 5px;
    z-index: 1;
}

.pending {
  position: relative;
  width: 12px;
  height: 12px;
  background-color: #676767;
  border-radius: 50%;
  border: 2px solid white;
  z-index: 1;
  margin-top: 3px;
  /* Ensure dot is above */
}

/* Activity log dot with inner padding and dotted border */
.activity-log-dot {
  position: relative;
  width: 16px;
  /* Increase size to accommodate padding */
  height: 16px;
  background-color: white;
  /* Inner padding effect */
  border-radius: 50%;
  border: 2px dotted #ccc;
  /* Dotted border */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 0;
  margin-top: 3px;
}

/* Inner dot */
.activity-log-dot::before {
  content: "";
  width: 8px;
  /* Inner dot size */
  height: 8px;
  background-color: #2BED12;
  /* Inner dot color */
  border-radius: 50%;
  display: block;
}

/* Add vertical line using ::after */
.activity-log-dot::after {
  content: "";
  position: absolute;
  top: 18px;
  /* Position below the dot */
  left: 50%;
  width: 1px;
  height: calc(100% + 50px);

  /* Adjust line length */
  background: repeating-linear-gradient(to bottom,
      rgb(133, 133, 133),
      rgb(133, 133, 133) 4px,
      transparent 4px,
      transparent 8px);
  transform: translateX(-50%);
}


/* Remove line for the last item */
.activity-log-item.last-item .activity-log-dot::after {
  content: none;
}

.activityRedDot {
  position: relative;
  width: 16px;
  /* Increase size to accommodate padding */
  height: 16px;
  background-color: white;
  /* Inner padding effect */
  border-radius: 50%;
  border: 2px dotted #ccc;
  /* Dotted border */
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1;
  margin-top: 3px;
}

/* Inner dot */
.activityRedDot::before {
  content: "";
  width: 8px;
  /* Inner dot size */
  height: 8px;
  background-color: #ed1212;
  /* Inner dot color */
  border-radius: 50%;
  display: block;
}

/* Add vertical line using ::after */
.activityRedDot::after {
  content: "";
  position: absolute;
  top: 18px;
  /* Position below the dot */
  left: 50%;
  width: 1px;
  height: calc(100% + 50px);

  /* Adjust line length */
  background: repeating-linear-gradient(to bottom,
      rgb(133, 133, 133),
      rgb(133, 133, 133) 4px,
      transparent 4px,
      transparent 8px);
  transform: translateX(-50%);
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

.strong-content {
  font-weight: 500;
}

.status_completed {
  color: #2BED12;
  border: 2px solid #2BED12;
  border-radius: 10px;
  padding: 2px 5px;
  margin: 0px 5px;
}

.requestRejected {
  color: #fe212e;
  border: 1px solid #fe212e;
  border-radius: 10px;
  padding: 2px 5px;
  margin: 0px 5px;
}

.back-to-same {
  position: sticky;
  top: 0;
  background-color: #fff;
  z-index: 10;
}


.activity-log-content {
  flex-grow: 1;
}

.tab_btn {
  border-radius: 0px;
  border-top-right-radius: 5px;
  border-top-left-radius: 5px;
  border-bottom: 1px solid #ddd;
  font-size: 14px;
  background-color: #fff;

}

.tab_btn.active {
  background-color: #fff;
  color: #000;
  border-bottom: 0px;
  font-weight: bold;
}

.tab_btn:hover {
  background-color: #f2f2f2;
}
</style>
