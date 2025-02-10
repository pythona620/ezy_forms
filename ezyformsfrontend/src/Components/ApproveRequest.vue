<template>
  <div>
    <div class="container-fluid">
      <div class="backtofromPage px-2 py-2">
        <router-link
          to="/todo/receivedform"
          class="text-decoration-none text-dark font-13"
          ><span> <i class="bi bi-arrow-left"></i></span>Asset request form</router-link
        >
      </div>
    </div>
    <div class="container-fluid">
      <div class="row">
        <div class="col-3"></div>
        <div class="col-6">
          <div class="position-relative">
            <div class="requestPreviewDiv">
              <ApproverPreview
                :blockArr="showRequest"
                :current-level="selectedcurrentLevel"
                @updateField="updateFormData"
              />
            </div>
            <div class="d-flex justify-content-end align-item-center">
              <!-- v-if="!requestcancelled" -->
              <div class="form-floating p-1">
                <textarea
                  class="form-control font-12"
                  placeholder="Leave a comment here"
                  id="floatingTextarea"
                  @input="resetCommentsValidation"
                  :class="{ 'is-invalid': !isCommentsValid }"
                  v-model="ApproverReason"
                ></textarea>
                <label class="font-11" for="floatingTextarea">Comments..</label>
              </div>
              <div>
                <div class="d-flex justify-content-between align-items-center mt-3 gap-2">
                  <div>
                    <button
                      class="btn btn-outline-danger font-10 py-0 rejectbtn"
                      type="button"
                      data-bs-dismiss="modal"
                      @click="approvalCancelFn(formData, 'Request Cancelled')"
                    >
                      <span><i class="bi bi-x-lg me-2"></i></span>Reject
                    </button>
                  </div>
                  <div>
                    <ButtonComp
                      type="button"
                      icon="check2"
                      class="approvebtn border-1 text-nowrap font-10"
                      @click="handleApproveClick"
                      name="Approve"
                    />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div class="col-3">
          <div class="activity-log-container">
            <div class="shadow w-100">
              <h5 class="font-13 fw-bold py-3 ps-2">Asset request form approval</h5>
            </div>
            <div
              v-for="(item, index) in activityData"
              :key="index"
              class="activity-log-item"
              :class="{ 'last-item': index === activityData.length - 1 }"
            >
              <div class="activity-log-dot"></div>
              <div class="activity-log-content">
                <p class="font-12 mb-1">
                  On
                  <!-- formatDate(item.creation) -->
                  <strong class="strong-content">{{ item.creation }} </strong><br />
                  <strong class="strong-content"> {{ item.user_name }}</strong>
                  ({{ item.role }}) has
                  <strong class="strong-content">{{ formatAction(item.action) }}</strong>
                  the request with the comments:
                  <strong class="strong-content">{{ item.reason || "N/A" }}</strong
                  >.
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref, watch, computed } from "vue";
import ApproverPreview from "./ApproverPreview.vue";
import { useRoute, useRouter } from "vue-router";
import axiosInstance from "../shared/services/interceptor";
import { apis, doctypes } from "../shared/apiurls";
import { EzyBusinessUnit } from "../shared/services/business_unit";
import { rebuildToStructuredArray } from "../shared/services/field_format";
import ButtonComp from "./ButtonComp.vue";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

onMounted(() => {
  receivedForMe();
  Wfactivitylog();
  getdata();
});

const router = useRouter();

const businessUnit = computed(() => {
  return EzyBusinessUnit.value;
});
const newBusinessUnit = ref({ business_unit: "" });
const route = useRoute();
const filterObj = ref({ limitPageLength: "None", limit_start: 0 });
const selectedData = ref({
  formname: route.query.name || "", // Retrieve from query
  doctype_name: route.query.doctype_name || "", // Retrieve from query
});
const totalRecords = ref(0);
const tableData = ref([]);
const emittedFormData = ref([]);
const showRequest = ref(null);
const isCommentsValid = ref(true);
const activityData = ref([]);
const ApproverReason = ref("");
const selectedcurrentLevel = ref("");
const doctypeForm = ref([]);
const resetCommentsValidation = () => {
  if (ApproverReason.value.trim() !== "") {
    // If comment is not empty, set isCommentsValid to true
    isCommentsValid.value = true;
  }
};
// Format the date for display
// const formatDate = (dateString) => {
//   if (!dateString) return "N/A";
//   const date = new Date(dateString);
//   return date.toLocaleDateString("en-GB");
// };

// Format action text (cancelled or raised)
const formatAction = (action) => {
  if (!action) return "performed an action on";
  const actionMap = {
    "Request Cancelled": "cancelled",
    "Request Raised": "raised",
  };
  return actionMap[action] || action.toLowerCase();
};
// Function to capture the form data from ApproverPreview
const updateFormData = (fieldValues) => {
  emittedFormData.value = emittedFormData.value.concat(fieldValues);
};

// Function to handle approve button click
const handleApproveClick = () => {
  if (ApproverReason.value.trim() === "") {
    // Set the validation flag to false if comment is empty
    isCommentsValid.value = false;
  } else {
    // Proceed with the Approve action if comments are valid
    isCommentsValid.value = true;
    ApproverFormSubmission(emittedFormData.value, "Approve"); // Use emittedFormData instead of formData
  }
};

// Function to handle form submission
function ApproverFormSubmission(dataObj, type) {
  let form = {};
  if (emittedFormData.value.length) {
    emittedFormData.value.map((each) => {
      form[each.fieldname] = each.value;
    });
  }
  axiosInstance
    .put(
      `${apis.resource}${selectedData.value.doctype_name}/${doctypeForm.value.name}`,
      form
    )
    .then((response) => {
      if (response?.data) {
        approvalStatusFn(dataObj, type);
      }
    });
}

function approvalStatusFn(dataObj, type) {
  console.log(dataObj);
  let data = {
    property: tableData.value.property,
    doctype: tableData.value.doctype_name,
    request_ids: [tableData.value.name],
    reason: ApproverReason.value,
    action: type,
    files: null,
    cluster_name: null,
    url_for_approval_id: "",
    // https://ezyrecon.ezyinvoicing.com/home/wf-requests
    current_level: tableData.value.current_level,
  };

  // need to check this api not working
  axiosInstance
    .post(apis.requestApproval, { request_details: [data] })
    .then((response) => {
      if (response?.message?.success) {
        if (type == "Reject") {
          toast.error(`Request ${type}ed`, {
            autoClose: 1000,
            transition: "zoom",
          });
        } else {
          toast.success(`Request ${type}ed`, {
            autoClose: 1000,
            transition: "zoom",
          });
          ApproverReason.value = "";
        }
        router.push({
          name: "ReceivedForMe",
        });
      }
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

function approvalCancelFn(dataObj, type) {
  // let files = this.selectedFileAttachments.map((res: any) => res.url);

  let data = {
    property: selectedRequest.value.property,
    doctype: selectedRequest.value.doctype_name,
    request_id: selectedRequest.value.name,
    reason: type == "Request Cancelled" ? "Cancelled" : "",
    action: type,
    files: [],
    url_for_cancelling_id: "",
    current_level: selectedRequest.value.current_level,
  };
  axiosInstance.post(apis.wf_cancelling_request, data).then((response) => {
    if (response?.message?.success) {
      const modal = bootstrap.Modal.getInstance(document.getElementById("viewRequest"));
      modal.hide();
      receivedForMe();
    }
  });
}

function getdata() {
  const filters = [
    ["wf_generated_request_id", "like", `%${selectedData.value.formname}%`],
  ];
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
        console.log(res.data);
        doctypeForm.value = res.data[0];
        mapFormFieldsToRequest(doctypeForm.value, showRequest.value);
        // Map values from doctypeForm to showRequest fields
      }
    })
    .catch((error) => {
      console.error("Error fetching categories data:", error);
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

function Wfactivitylog() {
  axiosInstance
    .get(`${apis.resource}${doctypes.WFActivityLog}/${selectedData.value.formname}`)
    .then((res) => {
      if (res.data) {
        console.log("Activity Data:", res.data);
        activityData.value = res.data.reason || []; // Ensure it's always an array
      }
    })
    .catch((error) => {
      console.error("Error fetching activity data:", error);
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
function receivedForMe(data) {
  // Initialize filters array for building dynamic query parameters
  const EmpRequestdesignation = JSON.parse(localStorage.getItem("employeeData"));

  const filters = [
    // assigned_to_users
    ["assigned_to_users", "like", `%${EmpRequestdesignation?.designation}%`],
    ["property", "like", `%${newBusinessUnit.value.business_unit}%`],
    ["name", "like", `%${selectedData.value.formname}%`],
  ];
  if (data) {
    filters.push(data);
  }

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
  axiosInstance
    .get(`${apis.resource}${doctypes.WFWorkflowRequests}`, {
      params: queryParamsCount,
    })
    .then((res) => {
      totalRecords.value = res.data[0].total_count;
    })
    .catch((error) => {
      console.error("Error fetching total count:", error);
    });

  // Fetch the records matching filters
  axiosInstance
    .get(`${apis.resource}${doctypes.WFWorkflowRequests}`, {
      params: queryParams,
    })
    .then((res) => {
      tableData.value = res.data[0];
      showRequest.value = rebuildToStructuredArray(
        JSON.parse(tableData.value?.json_columns)?.fields
      );
      selectedcurrentLevel.value = tableData.value.current_level;
      console.log(selectedcurrentLevel.value);
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
  background: #099819;
  color: white;
  padding: 5px 15px 5px 15px;
  gap: 7px;
  border-radius: 4px;
  opacity: 0px;
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
  // margin-top: 20px;
  padding: 20px;
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
  top: 15px;
  /* Start line from bottom of dot */
  left: 50%;
  width: 2px;
  height: 50px;
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
.requestPreviewDiv {
  overflow-x: hidden;
  overflow-y: auto;
  padding: 10px;
  height: 80vh;
}
</style>
