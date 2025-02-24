<template>
  <div>
    <div class="d-flex justify-content-between align-items-center py-2">
      <div>
        <h1 class="m-0 font-13">Requests received for me</h1>
        <p class="m-0 font-11 pt-1">{{ totalRecords }} request</p>
      </div>
    </div>
    <div class="mt-2">
      <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction="true" actionType="dropdown" isCheckbox="true"
        @updateFilters="inLineFiltersData" :field-mapping="fieldMapping" isFiltersoption="true" :actions="actions"
        @actionClicked="actionCreated" />
      <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords"
        @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
    </div>
    <div class="modal fade" id="viewRequest" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
      aria-labelledby="viewRequestLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title font-13" id="viewRequestLabel">
              Request Id: {{ selectedRequest.name }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" @click="closeModal"
              aria-label="Close"></button>
          </div>
          <div class="modal-body approvermodalbody">
            <ApproverPreview :blockArr="showRequest" :current-level="selectedcurrentLevel"
              @updateField="updateFormData" />
          </div>
          <div class="p-2">
            <div class="activity-log-container">
              <div v-for="(item, index) in activityData" :key="index" class="activity-log-item"
                :class="{ 'last-item': index === activityData.length - 1 }">
                <div class="activity-log-dot"></div>
                <div class="activity-log-content">
                  <p class="font-12 mb-1">
                    On
                    <strong class="strong-content">{{ formatDate(item.creation) }}</strong>, <strong
                      class="strong-content">{{ item.user_name }}</strong> ({{
                        item.role
                      }}) has
                    <strong class="strong-content">{{
                      formatAction(item.action)
                      }}</strong>
                      the request<span v-if="index !== 0 && item.reason">with the comments:</span>
                    <strong v-if="index !== 0 && item.reason" class="strong-content">{{ item.reason || "N/A" }}</strong>.
                  </p>
                </div>
              </div>
            </div>
            <div v-if="!requestcancelled" class="form-floating p-1">
              <textarea class="form-control font-12" placeholder="Leave a comment here" id="floatingTextarea"
                @input="resetCommentsValidation" :class="{ 'is-invalid': !isCommentsValid }"
                v-model="ApproverReason"></textarea>
              <label class="font-11" for="floatingTextarea">Comments..</label>
              <span v-if="!isCommentsValid" class="font-11 text-danger ps-1">Please enter comments**</span>
            </div>
          </div>
          <div class="modal-footer">
            <div v-if="!requestcancelled" class="d-flex justify-content-between align-items-center mt-3 gap-2">
              <div>
                <button class="btn btn-outline-danger font-10 py-0 rejectbtn" type="button" 
                  @click="approvalCancelFn(formData, 'Request Cancelled')">
                  <span><i class="bi bi-x-lg me-2"></i></span>Reject
                </button>
              </div>
              <div>
                <ButtonComp type="button" icon="check2" class="approvebtn border-1 text-nowrap font-10"
                  @click="ApproverFormSubmission('formData','Approve')" name="Approve" />
              </div>
            </div>

            <!-- <div v-if="requestcancelled">
              <ButtonComp type="button" class="border-1 edit-btn text-nowrap font-10" @click="handleEditClick"
                name="Edit" />
            </div> -->
          </div>

        </div>
      </div>
    </div>
    <!-- <div>
								<ButtonComp type="button" icon="ban" class="cancelbtn border-1 text-nowrap font-10"
									@click="approvalCancelFn(formData, 'Request Cancelled')" name="Cancel Request" />
							</div> -->

    <!-- <ButtonComp @click="approvalCancelFn(formData, 'Request Cancelled')" type="button" icon="x"
									class="rejectbtn border-1 text-nowrap font-10 " name="Reject" /> -->
  </div>
</template>
<script setup>
import ButtonComp from "../../Components/ButtonComp.vue";
import GlobalTable from "../../Components/GlobalTable.vue";
import axiosInstance from "../../shared/services/interceptor";
import { apis, doctypes } from "../../shared/apiurls";
import { onMounted, ref, reactive, computed, watch } from "vue";
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import PaginationComp from "../../Components/PaginationComp.vue";
import { rebuildToStructuredArray } from "../../shared/services/field_format";
import ApproverPreview from "../../Components/ApproverPreview.vue";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import router from "../../router";
const businessUnit = computed(() => {
  return EzyBusinessUnit.value;
});
const newBusinessUnit = ref({ business_unit: "" });

const filterObj = ref({ limitPageLength: "None", limit_start: 0 });
const totalRecords = ref(0);
const idDta = ref([]);
const docTypeName = ref([]);
const statusOptions = ref([]);
const emittedFormData = ref([]);
const selectedcurrentLevel = ref("");
const activityData = ref([]);

const tableheaders = ref([
  // { th: "Request ID", td_key: "name" },
  { th: "Form name", td_key: "doctype_name" },
  // { th: "Form category", td_key: "doctype_name" },
  // { th: "Owner of form", td_key: "owner" },
  { th: "Requested By", td_key: "requested_by" },
  { th: "Requested department", td_key: "role" },
  // { th: "Requested on", td_key: "requested_on" },
  { th: "Approval Status", td_key: "status" },
]);
const fieldMapping = ref({
  // invoice_type: { type: "select", options: ["B2B", "B2G", "B2C"] },
  // credit_irn_generated: { type: "select", options: ["Pending", "Completed", "Error"] },
  // role: { type: "input" },
  doctype_name: { type: "input" },
  // requested_on: { type: "date" },
});
const actions = ref([
  { name: "View Request", icon: "fa-solid fa-eye" },

  // { name: 'Share this form', icon: 'fa-solid fa-share-alt' },
  // { name: 'Download Form', icon: 'fa-solid fa-download' },
  // { name: 'Edit Form', icon: 'fa-solid fa-edit' },
]);
const tableData = ref([]);
const selectedRequest = ref({});
const showRequest = ref(null);
const doctypeForm = ref([]);
const ApproverReason = ref("");
function actionCreated(rowData, actionEvent) {
  if (actionEvent.name === "View Request") {
    if (rowData) {
      selectedRequest.value = { ...rowData };
      selectedcurrentLevel.value = selectedRequest.value.current_level;
      // console.log("doctype_name",selectedRequest.value.doctype_name);
      // console.log("Property name",selectedRequest.value.property);


      // Rebuild the structured array from JSON
      showRequest.value = rebuildToStructuredArray(
        JSON.parse(selectedRequest.value?.json_columns)?.fields
      );

      // Prepare the filters for fetching data
      const filters = [
        ["wf_generated_request_id", "like", `%${selectedRequest.value.name}%`],
      ];
      const queryParams = {
        fields: JSON.stringify(["*"]),
        limit_page_length: "None",
        limit_start: 0,
        filters: JSON.stringify(filters),
        order_by: `\`tab${selectedRequest.value.doctype_name}\`.\`creation\` desc`,
      };

      // Fetch the doctype data
      axiosInstance
        .get(`${apis.resource}${selectedRequest.value.doctype_name}`, {
          params: queryParams,
        })
        .then((res) => {
          if (res.data) {
            doctypeForm.value = res.data[0];

            // Map values from doctypeForm to showRequest fields
            mapFormFieldsToRequest(doctypeForm.value, showRequest.value);
          }
        })
        .catch((error) => {
          console.error("Error fetching categories data:", error);
        });

      axiosInstance
        .get(`${apis.resource}${doctypes.WFActivityLog}/${selectedRequest.value.name}`)
        .then((res) => {
          if (res.data) {
            // console.log(res.data);
            activityData.value = res.data.reason || []; // Ensure it's always an array
          }
        })
        .catch((error) => {
          console.error("Error fetching activity data:", error);
        });
      const modal = new bootstrap.Modal(document.getElementById("viewRequest"), {});
      modal.show();
    } else {
      console.warn(" There is no form fields ");
    }
  }
}

function viewPreview(data) {
  console.log(data);
  router.push({
    name: "ApproveRequest",
    query: {
      name: data.name,
      doctype_name: data.doctype_name,
    },
  });
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
// Function to capture the form data from ApproverPreview
const updateFormData = (fieldValues) => {
  emittedFormData.value = emittedFormData.value.concat(fieldValues);
};
const isCommentsValid = ref(true); // Flag to validate comment field

// function handleEditClick() {
//   console.log("item", selectedRequest.value);

//   // Hide the modal properly
//   const modalElement = document.getElementById('viewRequest');
//   if (modalElement) {
//     const modalInstance = bootstrap.Modal.getInstance(modalElement); // Get existing modal instance
//     if (modalInstance) {
//       modalInstance.hide();
//     }
//   }

//   // Navigate to the new route
//   router.push({
//     name: "RaiseRequest",
//     query: {
//       business_unit: selectedRequest.value.property,
//       selectedForm: selectedRequest.value.doctype_name,
//     }
//   });
// }




// Function to handle approve button click
// const handleApproveClick = () => {
//   if (ApproverReason.value.trim() === "") {
//     // Set the validation flag to false if comment is empty
//     isCommentsValid.value = false;
//   } else {
//     // Proceed with the Approve action if comments are valid
//     isCommentsValid.value = true;
//     ApproverFormSubmission(emittedFormData.value, "Approve"); // Use emittedFormData instead of formData
//   }
// };

const resetCommentsValidation = () => {
  if (ApproverReason.value.trim() !== "") {
    // If comment is not empty, set isCommentsValid to true
    isCommentsValid.value = true;
  }
};
// Function to handle form submission
function ApproverFormSubmission(dataObj, type) {

  if (ApproverReason.value.trim() === "") {
    // Set the validation flag to false if the comment is empty
    isCommentsValid.value = false;

    return; // Stop function execution
  } else {
    // Proceed if comments are valid
    isCommentsValid.value = true;
  }



  let form = {};
  if (emittedFormData.value.length) {
    emittedFormData.value.map((each) => {
      form[each.fieldname] = each.value;
    });
  }
  axiosInstance
    .put(
      `${apis.resource}${selectedRequest.value.doctype_name}/${doctypeForm.value.name}`,
      form
    )
    .then((response) => {
      if (response?.data) {
        approvalStatusFn(dataObj, type);
      }
    });
}


function approvalStatusFn(dataObj, type) {
  const storedData = localStorage.getItem("employeeData");
  const employee = JSON.parse(storedData);
  console.log([employee.signature]);

  console.log(dataObj);
  let data = {
    property: selectedRequest.value.property,
    doctype: selectedRequest.value.doctype_name,
    request_ids: [selectedRequest.value.name],
    reason: ApproverReason.value,
    action: type,
    files: null,
    cluster_name: null,
    url_for_approval_id: "",
    // https://ezyrecon.ezyinvoicing.com/home/wf-requests
    current_level: selectedRequest.value.current_level,
  };

  // need to check this api not working
  axiosInstance
    .post(apis.requestApproval, { request_details: [data] })
    .then((response) => {
      if (response?.message?.success) {
        if (type == "Reject") {
          toast.error(`Request ${type}ed`, { autoClose: 1000, transition: "zoom" });
        } else {
          toast.success(`Request ${type}ed`, { autoClose: 1000, transition: "zoom" });
          ApproverReason.value = "";
        }
        const modal = bootstrap.Modal.getInstance(document.getElementById("viewRequest"));
        modal.hide();
        receivedForMe();
      }
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

function approvalCancelFn(dataObj, type) {
  // let files = this.selectedFileAttachments.map((res: any) => res.url);

  if (ApproverReason.value.trim() === "") {
    // Set the validation flag to false if the comment is empty
    isCommentsValid.value = false;
    return; // Stop function execution
  } else {
    // Proceed if comments are valid
    isCommentsValid.value = true;
  }

  let data = {
    property: selectedRequest.value.property,
    doctype: selectedRequest.value.doctype_name,
    request_id: selectedRequest.value.name,
    reason: ApproverReason.value,
    action: type,
    files: [],
    url_for_cancelling_id: "",
    current_level: selectedRequest.value.current_level,
  };
  axiosInstance.post(apis.wf_cancelling_request, data).then((response) => {
    if (response?.message) {
      const modal = bootstrap.Modal.getInstance(document.getElementById("viewRequest"));
      modal.hide();
      receivedForMe();
    }
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

function closeModal() {
  isCommentsValid.value = true;
}

const PaginationUpdateValue = (itemsPerPage) => {
  filterObj.value.limitPageLength = itemsPerPage;
  filterObj.value.limit_start = 0;
  receivedForMe();
};
// Handle updating the limit start
const PaginationLimitStart = ([itemsPerPage, start]) => {
  filterObj.value.limitPageLength = itemsPerPage;
  filterObj.value.limit_start = start;
  receivedForMe();
};

function inLineFiltersData(searchedData) {
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

  //   // Log filters to verify

  //   // Once the filters are built, pass them to fetchData function
  if (filters.length) {
    receivedForMe(filters);
  } else {
    receivedForMe();
  }
}

function receivedForMe(data) {
  // Initialize filters array for building dynamic query parameters
  const EmpRequestdesignation = JSON.parse(localStorage.getItem("employeeData"));

  const filters = [
    // assigned_to_users
    ["assigned_to_users", "like", `%${EmpRequestdesignation?.designation}%`],
    ["property", "like", `%${newBusinessUnit.value.business_unit}%`],
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
    .get(`${apis.resource}${doctypes.WFWorkflowRequests}`, { params: queryParamsCount })
    .then((res) => {
      totalRecords.value = res.data[0].total_count;
    })
    .catch((error) => {
      console.error("Error fetching total count:", error);
    });

  // Fetch the records matching filters
  axiosInstance
    .get(`${apis.resource}${doctypes.WFWorkflowRequests}`, { params: queryParams })
    .then((res) => {
      tableData.value = res.data;
      idDta.value = [...new Set(res.data.map((id) => id.name))];
      docTypeName.value = [
        ...new Set(res.data.map((docTypeName) => docTypeName.doctype_name)),
      ];
      statusOptions.value = [...new Set(res.data.map((status) => status.status))];
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

onMounted(() => {
  // receivedForMe()
});
</script>
<style scoped>
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
