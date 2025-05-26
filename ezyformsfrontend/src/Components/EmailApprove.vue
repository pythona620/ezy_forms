<template>
  <div class="position-relative">
    <!-- <div class=" back-to-same">
  
        <div class="container-fluid  p-0">
          <div class="backtofromPage asset_request px-2 py-2">
            <router-link :to="backTo" class="text-decoration-none text-dark font-13"><span> <i
                  class="bi bi-arrow-left px-2"></i></span>Back</router-link>
          </div>
        </div>
      </div> -->

    <div v-if="expiryToken">
      <div v-if="approvedform" class="approve_height">
        <div class="container-fluid">
          <div class="row">
            <div class=" col-md-2 col-lg-3 d-none d-md-block"></div>
            <div class=" col-md-8 col-lg-6">
              <div class="mt-1">
                <div class="text-center">
                  <div class="card border-0 shadow-none">
                    <div class="card-body pb-2 d-flex gap-3 align-items-center justify-content-center">
                      <h5 class="card-title">{{ selectedData.doctype_name }}</h5>
                      <span v-if="tableData?.status === 'Completed'"><i
                          class="bi approved-icon bi-check2-circle "></i></span>
                      <span v-if="tableData?.status === 'Request Cancelled'"><i
                          class="bi rejected-icon bi-x-circle"></i></span>
                    </div>
                  </div>
                </div>
                <div class="position-relative ">
                  <div class="requestPreviewDiv pb-5">
                    <ApproverPreview :blockArr="showRequest" :childData="responseData"
                      :current-level="selectedcurrentLevel" :readonly-for="selectedData.readOnly"
                      :childHeaders="tableHeaders" :employee-data="employeeData" @updateField="updateFormData" />

                  </div>

                  <div v-if="selectedData.type == 'myforms' && tableData.status == 'Request Raised'"
                    class="d-flex justify-content-end approveBtns">
                    <button type="submit" class="btn Edit_btn" @click.prevent="EditformSubmission()">
                      <span v-if="loading" class="spinner-border spinner-border-sm" role="status"
                        aria-hidden="true"></span>
                      <span v-if="!loading"><i class="bi bi-pencil-fill font-15 me-2"></i><span
                          class="font-12">Edit</span></span>
                    </button>
                  </div>


                </div>
              </div>


              <div
                v-if="expiryToken"
                class="">

                <!-- v-if="!requestcancelled" -->
                <div  class="approveBtns pb-2 mb-2 mt-3 flex-column px-0 pe-4">
                  <div class="form-floating mb-2 p-1">
                    <textarea class="form-control font-12" placeholder="Leave a comment here" id="floatingTextarea"
                      @input="resetCommentsValidation" :class="{ 'is-invalid': !isCommentsValid }"
                      v-model="ApproverReason"></textarea>
                    <label class="font-11" for="floatingTextarea">Comments..</label>
                    <span v-if="!isCommentsValid" class="font-11 text-danger ps-1">Please enter comments**</span>
                  </div>
                  <div class=" d-flex justify-content-between ">
                    <div>
                      <button :disabled="rejectLoad" class="btn btn-outline-danger font-10 py-0 rejectbtn" type="button"
                        @click="ApproverCancelSubmissionNew('Request Cancelled')">
                        <span v-if="rejectLoad" class="spinner-border spinner-border-sm" role="status"
                          aria-hidden="true"></span>
                        <span v-if="!rejectLoad"><i class="bi bi-x-lg fw-bolder font-12 me-2"></i><span
                            class="font-12">Reject</span></span>
                      </button>
                    </div>
                    <div>
                      <button :disabled="loading" type="submit" class="btn btn-success approvebtn"
                        @click.prevent="ApproverFormSubmissionNew('Approve')">
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
            <div class=" col-md-2 col-lg-3 d-none d-md-block">
              <div class="activity-log-container ">
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
                <!-- <div class="row mb-3">
                <div class="col-xl-6 col-lg-12 col-md-12">
                  <div class="d-flex  align-items-baseline  mt-2">
                    <div>
                      <span class="font-12 text-nowrap fw-bold mb-0">Activity log
                      </span>
                    </div>
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


                </div>
                <div class="col-xl-6 col-lg-12 col-md-12">
                  <button v-if="tableData.status === 'Completed'"
                    class="btn btn-light font-11 fw-bold h-0 text-decoration-underline" type="button"
                    @click="downloadPdf"><i class="bi bi-arrow-down-circle fw-bold px-1"></i>Download
                  </button>
                </div>
              </div> -->
                <!-- <div class="activity_height">
                <div v-for="(item, index) in activityData" :key="index" class="activity-log-item"
                  :class="{ 'last-item': index === activityData.length - 1 }">
                  <div class="activity-log-dot"></div>
                  <div class="activity-log-content">
                    <p class="font-12 mb-1">
                      <span class="strong-content">{{ formatAction(item.action) }} on </span>
                      <span class="strong-content">{{ item.creation }} </span><br />
                      <span class="strong-content"> {{ item.user_name }}</span><br />
                      <span>{{ item.role }}</span><br />
                      <span class="font-12 text-secondary">{{
                        item.reason || "N/A"
                        }}</span>.

                    </p>
                  </div>
                </div>
              </div> -->
                <!-- <div class="activity-log-item">
                <div class="pending"></div>
                <div class="activity-log-content">
                  <p class="font-12 mb-1">
                    <span class="font-12 text-secondary">
                      Pending
                    </span>
                  </p>
                </div>
              </div> -->
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
      <!-- <div class="container-lg">
     
      </div> -->
      <div v-if="!approvedform" class="thank_div">
        <div>
          <div :class="actionStatus == 'Approve' ? 'thank-you-card-approve' : 'thank-you-card-reject'">

            <span>Form {{ actionStatus == 'Request Cancelled' ? 'Request Rejected' : actionStatus }} Successfully <span
                v-if="actionStatus == 'Approve'"><i class="bi approved-icon bi-check2-circle"></i></span>
              <span v-if="actionStatus == 'Request Cancelled'">
                <i class="bi bi-x-lg"></i>
              </span>
            </span>
          </div>
        </div>
      </div>
    </div>
    <div v-else>

      <div class="expiry-token-container">
        <div class="expiry-token-card">
          <!-- <h2>⚠️</h2> -->
          <p class="fw-bold">Form Already Submitted.</p>
        </div>
      </div>



    </div>


  </div>
</template>

<script setup>

import { onMounted, ref, watch, computed, watchEffect } from "vue";
import ApproverPreview from "./ApproverPreview.vue";
import { useRoute, useRouter } from "vue-router";
import axiosInstance from "../shared/services/interceptor";
import { apis } from "../shared/apiurls";

import { rebuildToStructuredArray } from "../shared/services/field_format";

import "vue3-toastify/dist/index.css";
const route = useRoute();
const approvedform = ref(true);
const selectedData = ref({
  routepath: route.query.routepath,
  formname: route.query.name || "", // Retrieve from query
  doctype_name: route.query.doctype_name || "", // Retrieve from query
  type: route.query.type || "", // Retrieve from query
  readOnly: route.query.readOnly, // Retrieve from query
  token: route.query.key, // Retrieve from query
});


const router = useRouter(); 


const tableData = ref([]);
const tableWFData = ref([]);
const emittedFormData = ref([]);
const showRequest = ref(null);
const isCommentsValid = ref(true);
const activityData = ref([]);
const ApproverReason = ref("");
const selectedcurrentLevel = ref("");

const loading = ref(false);
const rejectLoad = ref(false)

const tableHeaders = ref([]);

const responseData = ref([]);
const employeeData = ref([]);
const resetCommentsValidation = () => {
  if (ApproverReason.value.trim() !== "") {
    // If comment is not empty, set isCommentsValid to true
    isCommentsValid.value = true;
  }
};
const actionStatus = ref("");
const EmptyData = ref([])
const expiryToken = ref(true);
const ApprovePDF = ref(true)

onMounted(() => {
  approvedform.value = false;
  logout()
  user_id.value = getUserIdFromCookies();
  const cookiesToRemove = ['full_name', 'sid', 'system_user', 'user_id'];

  cookiesToRemove.forEach(cookie => {
    deleteCookie(cookie);
  });
  const storedData = localStorage.getItem("employeeData");
  try {
    const parsedData = JSON.parse(storedData);

    // Ensure parsedData is an array
    employeeData.value = Array.isArray(parsedData) ? parsedData : [parsedData];

  } catch (error) {
    console.error("Error parsing employeeData from localStorage:", error);
    employeeData.value = []; // Fallback to empty array if there's an error
  }

});

function logout() {
  // localStorage.removeItem('UserName');
  // localStorage.removeItem('employeeData');
  axiosInstance.post(apis.logout)
    .then((response) => {
      console.log(response);
      if (response) {

        localStorage.removeItem('UserName');
        localStorage.removeItem('employeeData');
        localStorage.removeItem('Bu');
        localStorage.removeItem('USERROLE');
        sessionStorage.removeItem('UserName');
        sessionStorage.removeItem('employeeData');
        sessionStorage.removeItem('Bu');
        sessionStorage.removeItem('USERROLE');
        receivedForMe();
      }
    })
}
const user_id = ref("");

// Function to get user_id from cookies
function getUserIdFromCookies() {
  return document.cookie
    .split("; ")
    .find((cookie) => cookie.startsWith("user_id="))
    ?.split("=")[1] || null;
}


function removeUserIdCookie() {
  document.cookie = "user_id=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/";
  document.cookie = "full_name=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/";
  user_id.value = ""; // Clear the reactive variable
  // console.log("user_id cookie removed");
}

// Function to remove user-related localStorage data
function clearLocalStorage() {
  localStorage.removeItem("UserName");
  localStorage.removeItem("employeeData");
  localStorage.removeItem("Bu");
  localStorage.removeItem("USERROLE");
  // console.log("Local storage cleared");
}

;

// Watch for changes in `sessionStorage` UserName
watchEffect(() => {
  const userName = sessionStorage.getItem("UserName");

  if (!userName) {
    clearLocalStorage();
    removeUserIdCookie();
  }
});
function EditformSubmission() {
  // Navigate to the new route
  router.push({
    name: "RaiseRequest",
    query: {
      routepath: '/todo/raisedbyme',
      business_unit: route.query.property,
      selectedForm: route.query.doctype_name,
      selectedFormId: route.query.name,
      selectedFormStatus: route.query.status,
    },
  });
  // console.log("emittedFormData", emittedFormData.value);
}






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
// function deleteCookie(name) {
//   document.cookie = `${name}=;expires=${new Date(0).toUTCString()};path=/`;
// }
function deleteCookie(name) {
  const expired = new Date(0).toUTCString();

  // Try different paths to ensure it's removed
  document.cookie = `${name}=; expires=${expired}; path=/;`;
  document.cookie = `${name}=; expires=${expired}; path=/; domain=${location.hostname}`;
  document.cookie = `${name}=; expires=${expired}; path=/`;
}

function ApproverFormSubmissionNew(action) {
  // clearSidCookie()
  // Trim and validate the reason input
  // logout()
  const cookiesToRemove = ['full_name', 'sid', 'system_user', 'user_id'];

  cookiesToRemove.forEach(cookie => {
    deleteCookie(cookie);
  });
  const reason = ApproverReason.value.trim();
  if (!reason) {
    isCommentsValid.value = false; // Show validation error
    return;
  }

  isCommentsValid.value = true;
  loading.value = true;

  const data = {
    token: selectedData.value.token,
    action: action,
    reason: reason
  };

  axiosInstance
    .get(apis.toMailApproval, { params: data })
    .then((res) => {
      actionStatus.value = action
      EmptyData.value = res.data; // Assuming you need the actual data
      approvedform.value = false;
    })
    .catch((error) => {
      console.error("Error fetching records:", error);
    })
    .finally(() => {
      loading.value = false; // Always reset loading state
    });
}


function ApproverCancelSubmissionNew(action) {
  const reason = ApproverReason.value.trim();

  if (!reason) {
    isCommentsValid.value = false; // Show validation error
    return;
  }

  isCommentsValid.value = true;
  rejectLoad.value = true;

  const data = {
    token: selectedData.value.token,
    action: action,
    reason: reason
  };

  axiosInstance
    .get(apis.toMailApproval, { params: data })
    .then((res) => {
      actionStatus.value = action
      EmptyData.value = res.data; // Store only the response data
      approvedform.value = false;
    })
    .catch((error) => {
      console.error("Error sending cancel request:", error);
    })
    .finally(() => {
      rejectLoad.value = false; // Always stop the loader
    });
}




function receivedForMe() {

  const data = {
    token: selectedData.value.token
  }


  axiosInstance
    .get(apis.toMailApproval, { params: data })
    .then((res) => {
      if (res.message.success === false) {
        expiryToken.value = false
      } else {
        approvedform.value = true;
        tableData.value = res.message.message.doc_data;
        tableWFData.value = res.message.message.wf_data

        showRequest.value = rebuildToStructuredArray(
          JSON.parse(tableWFData.value?.json_columns).fields
        );

        // console.log(showRequest.value, "pppa--------------");
        mapFormFieldsToRequest(tableData.value, showRequest.value);
        tableHeaders.value = JSON.parse(tableWFData.value?.json_columns).child_table_fields;


        const childTables = Object.keys(tableData.value).filter((key) =>
          Array.isArray(tableData.value[key])
        );
        if (childTables.length) {
          responseData.value = {};

          childTables.forEach((tableKey) => {
            responseData.value[tableKey] = tableData.value[tableKey] || [];
          });
          // console.log("Response Data:", responseData.value);
        }
        // console.log(tableHeaders.value, "req");

        // if (res.data.length) {
        //   Wfactivitylog(tableData.value.name);
        //   getdata(tableData.value.name);
        // }

        selectedcurrentLevel.value = tableWFData.value.current_level - 1;
      }
    })
    .catch((error) => {
      console.error("Error fetching records:", error);
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
watch(activityData, (newVal) => {
  console.log("Updated Activity Data:", newVal);
  console.log("Request Cancelled?", requestcancelled.value);
});



</script>

<style lang="scss" scoped>
// .backtofromPage {
//   position: sticky !important;
//   top: 0 !important;
//   z-index: 1000 !important;

// }
.expiry-token-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #ece9e6, #ffffff);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.expiry-token-card {
  background-color: #fff;
  padding: 40px 60px;
  border-radius: 20px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  text-align: center;
  animation: slideFadeIn 0.8s ease-in-out;
}

.expiry-token-card h2 {
  font-size: 32px;
  margin-bottom: 15px;
  color: #d9534f;
}

.expiry-token-card p {
  font-size: 18px;
  color: #555;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }

  to {
    opacity: 1;
    transform: scale(1);
  }
}

.thank_div {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f0f0;

}

@keyframes slideFadeIn {
  0% {
    opacity: 0;
    transform: translateY(20px) scale(0.95);
  }

  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

@keyframes bounceIcon {

  0%,
  100% {
    transform: translateY(0);
  }

  50% {
    transform: translateY(-5px);
  }
}

@keyframes glowPulse {

  0%,
  100% {
    box-shadow: 0 0 5px rgba(56, 158, 13, 0.3);
  }

  50% {
    box-shadow: 0 0 15px rgba(56, 158, 13, 0.6);
  }
}

.thank-you-card-approve {
  padding: 15px 25px;
  background-color: #e6f7ed;
  border: 1px solid #b7eb8f;
  border-radius: 12px;
  color: #389e0d;
  display: inline-block;
  font-weight: 600;
  font-size: 18px;
  animation: slideFadeIn 0.8s ease-out, glowPulse 2s ease-in-out infinite;
  transition: transform 0.3s ease;
}

.thank-you-card-reject {
  padding: 15px 25px;
  background-color: #e6f7ed;
  border: 1px solid #eb8f8f;
  border-radius: 12px;
  color: #d75159;
  display: inline-block;
  font-weight: 600;
  font-size: 18px;
  animation: slideFadeIn 0.8s ease-out, glowPulse 2s ease-in-out infinite;
  transition: transform 0.3s ease;
}

.thank-you-card:hover {
  transform: scale(1.03);
}

.thank-you-card i {
  margin-left: 10px;
  font-size: 20px;
  vertical-align: middle;
  animation: bounceIcon 1s infinite;
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

/* Width between 985px and 765px */
@media (max-width: 985px) and (min-width: 765px) {
  .approveBtns {
    width: 67%;
  }
}

/* Width less than 765px */
@media (max-width: 764px) {
  .approveBtns {
    width: 100%;
    padding: 0;
  }

  .form-floating {
    padding: 0 !important;
  }
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
  z-index: 1;
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
  border: 1px solid #2BED12;
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
</style>