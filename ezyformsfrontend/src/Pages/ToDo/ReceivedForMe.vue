<template>
  <div>
    <div class="d-flex justify-content-between align-items-center py-2">
      <div>
        <h1 class="m-0 font-13">Requests Assigned to me</h1>
        <p class="m-0 font-11 pt-1">{{ totalRecords }} request</p>
      </div>
      <!-- <div>
        <input type="checkbox" id="ViewOnlyReportee" v-model="ViewOnlyReportee" class="me-2 mt-1 form-check-input" @change="ViewOnlyRe" />
              <label for="ViewOnlyReportee " class="SelectallDesignation  font-12 m-0 form-check-label">View Only Reportee</label>
        
        
      </div> -->
    </div>
    <div class="mt-2">
      <div class=" d-none d-lg-block">

      <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction="true" viewType="viewPdf" isCheckbox="true"
        @updateFilters="inLineFiltersData" :field-mapping="fieldMapping" @cell-click="viewPreview"
        isFiltersoption="true" :actions="actions" @actionClicked="actionCreated" />
      </div>
      <div class=" d-block d-lg-none">
        <GlobalCard :tHeaders="tableheaders" :tData="tableData" isAction="true" viewType="viewPdf" isCheckbox="true"
          @updateFilters="inLineFiltersData" :field-mapping="fieldMapping" @cell-click="viewPreview"
          isFiltersoption="false" :actions="actions" @actionClicked="actionCreated" />
      </div>
      <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords" :items-per-page="filterObj.limitPageLength"
        @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
    </div>
    <div class="modal fade" id="viewRequest" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
      aria-labelledby="viewRequestLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title font-13" id="viewRequestLabel">
              Request Id: {{ selectedRequest.name?.replace(/_/g, " ") }}
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" @click="closeModal"
              aria-label="Close"></button>
          </div>
          <div class="modal-body approvermodalbody">
            <!-- <ApproverPreview :blockArr="showRequest" :current-level="selectedcurrentLevel" :childData="responseData"
              :childHeaders="tableHeaders" :employeeData="employeeData" @updateField="updateFormData" /> -->
          </div>
          <div class="p-2">
            <div class="activity-log-container">
              <div v-for="(item, index) in activityData" :key="index" class="activity-log-item"
                :class="{ 'last-item': index === activityData.length - 1 }">
                <div class="activity-log-dot"></div>def add_roles_to_wf_requestors
                <div class="activity-log-content">
                  <p class="font-12 mb-1">
                    On
                    <strong class="strong-content">{{ formatDate(item.creation) }}</strong>,
                    <strong class="strong-content">{{ item.user_name }}</strong>
                    ({{ item.role }}) has
                    <strong class="strong-content">{{
                      formatAction(item.action)
                    }}</strong>
                    the request<span v-if="index !== 0 && item.reason">with the comments:</span>
                    <strong v-if="index !== 0 && item.reason" class="strong-content">{{ item.reason || "N/A"
                      }}</strong>
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
                <!-- <button class="btn btn-outline-danger font-12 py-0 rejectbtn" type="button"
                  @click="ApproverCancelSubmission(formData, 'Request Cancelled')">
                  <span><i class="bi bi-x-lg me-2"></i></span>Reject
                </button> -->
                <button type="submit" class="btn btn-outline-danger font-12 py-0 rejectbtn" :disabled="Rejectloading"
                  @click.prevent="ApproverCancelSubmission(formData, 'Request Cancelled')">
                  <span v-if="Rejectloading" class="spinner-border spinner-border-sm" role="status"
                    aria-hidden="true"></span>
                  <span v-if="!Rejectloading"><i class="bi bi-x-lg me-2"></i><span class="font-12">Reject</span></span>
                </button>
              </div>
              <div>
                <!-- <ButtonComp type="button" icon="check2" class="approvebtn border-1 text-nowrap font-10"
                  @click="ApproverFormSubmission('formData','Approve')" name="Approve" /> -->
                <button type="submit" class="btn btn-success approvebtn" :disabled="loading"
                  @click.prevent="ApproverFormSubmission(emittedFormData, 'Approve')">
                  <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                  <span v-if="!loading"><i class="bi bi-check-lg font-15 me-2"></i><span
                      class="font-12">Approve</span></span>
                </button>


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
import GlobalCard from "../../Components/GlobalCard.vue";
import axiosInstance from "../../shared/services/interceptor";
import { apis, doctypes } from "../../shared/apiurls";
import { onMounted, ref, reactive, computed, watch } from "vue";
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import PaginationComp from "../../Components/PaginationComp.vue";
import { rebuildToStructuredArray } from "../../shared/services/field_format";
// import ApproverPreview from "../../Components/ApproverPreview.vue";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
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
const docTypeName = ref([]);
const statusOptions = ref([]);
const emittedFormData = ref([]);
const selectedcurrentLevel = ref("");
const activityData = ref([]);
const responseData = ref([]);
const ViewOnlyReportee = ref(false);
const tableheaders = ref([
  { th: "Request ID", td_key: "name" },
  { th: "Requester Name", td_key: "requester_name" },
  { th: "Requested on", td_key: "requested_on" },
  { th: "Requester Department", td_key: "department_name" },
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
const tableData = ref([]);
const selectedRequest = ref({});
const showRequest = ref(null);
const doctypeForm = ref([]);
const ApproverReason = ref("");
const employeeData = ref([]);
const tableHeaders = ref([]);

const loading = ref(false)
const Rejectloading = ref(false)

onMounted(() => {
  // getClientIP()
  const storedData = localStorage.getItem("employeeData");
  employeeData.value = JSON.parse(storedData);

});

const viewlist = ref([])
function ViewOnlyReport() {

  // console.log(ViewOnlyReportee.value); 
  axiosInstance
    .post(apis.view_only_reportee,)
    .then((response) => {
      // console.log(response.message,"list");
      viewlist.value = response.message;

      // const filters = [ "name","in", viewlist.value];
      //    if (route.query.status) {
      //   filterObj.value.filters = [
      //     ["name", "in", viewlist.value],
      //     ["status", "=", route.query.status],
      //   ];


      //   // filterObj.value.filters.push(["status", "=", route.query.status]);
      // }
      receivedForMe(filterObj.value.filters);

    })
    .catch((error) => {
      console.log(error);
    });


}
function actionCreated(rowData, actionEvent) {
  if (actionEvent.name === "View Request") {
    if (rowData) {
      selectedRequest.value = { ...rowData };
      selectedcurrentLevel.value = selectedRequest.value.current_level;


      // Rebuild the structured array from JSON
      showRequest.value = rebuildToStructuredArray(
        JSON.parse(selectedRequest.value?.json_columns)?.fields
      );

      tableHeaders.value = JSON.parse(
        selectedRequest.value?.json_columns
      ).child_table_fields;
      // console.log(tableHeaders.value, "lll");

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

            axiosInstance
              .get(
                `${apis.resource}${selectedRequest.value.doctype_name}/${res.data[0].name}`
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
                  // console.log("Response Data:", responseData.value);
                }

              })
              .catch((error) => {
                console.error(`Error fetching data for :`, error);
              });

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
        designation: employeeData.value

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
    isCommentsValid.value = false; // Show validation error
    return; // Stop execution
  }

  isCommentsValid.value = true;
  loading.value = true; // Start loader




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
    })
    .catch((error) => {
      console.error("Error submitting form:", error);
    })

}
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

function approvalStatusFn(dataObj, type) {


  // console.log(dataObj);
  let data = {
    property: selectedRequest.value.property,
    doctype: selectedRequest.value.doctype_name,
    request_ids: [selectedRequest.value.name],
    reason: ApproverReason.value,
    action: type,
    files: null,
    cluster_name: null,
    url_for_approval_id: "",
    // ip_address:ip_address.value,
    // employee_id:employeeData.value.emp_code,
    // https://ezyrecon.ezyinvoicing.com/home/wf-requests
    current_level: selectedRequest.value.current_level,
  };

  // need to check this api not working
  axiosInstance
    .post(apis.requestApproval, { request_details: [data] })
    .then((response) => {
      if (response?.message?.success === true) {
        toast.success(`Request ${type}ed`, { autoClose: 1000, transition: "zoom" });
        const modal = bootstrap.Modal.getInstance(document.getElementById("viewRequest"));
        modal.hide();
        ApproverReason.value = ""; // Clear reason after success


        receivedForMe();
      } else {
        toast.error(`Failed to ${type} request`, { autoClose: 1000, transition: "zoom" });
      }
    })
    .catch((error) => {
      console.error("Error processing request:", error);
      // toast.error("An error occurred while processing your request.", { autoClose: 1000, transition: "zoom" });
    })
    .finally(() => {
      loading.value = false; // Ensure loader stops
    });
}


function ApproverCancelSubmission(dataObj, type) {

  if (ApproverReason.value.trim() === "") {
    // Set the validation flag to false if the comment is empty
    isCommentsValid.value = false;

    return; // Stop function execution
  }
  // Proceed if comments are valid
  isCommentsValid.value = true;

  Rejectloading.value = true; // Start loader



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
        const modal = bootstrap.Modal.getInstance(document.getElementById("viewRequest"));
        modal.hide();
        approvalCancelFn(dataObj, type);
      }
    });
}
function approvalCancelFn(dataObj, type) {


  // console.log(dataObj, "data", type);
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

  axiosInstance
    .post(apis.wf_cancelling_request, data)
    .then((response) => {
      if (response?.message) {
        ApproverReason.value = "";
        if (type == "Request Cancelled") {
          toast.success(`${type}`, { autoClose: 1000, transition: "zoom" });
        }
        const modal = bootstrap.Modal.getInstance(document.getElementById("viewRequest"));
        modal.hide();
        receivedForMe();
      }
    })
    .catch((error) => {
      console.error("Error processing cancellation:", error);
      toast.error("An error occurred while processing your request.", { autoClose: 1000, transition: "zoom" });
    })
    .finally(() => {
      Rejectloading.value = false; // Ensure loader stops
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
  if (filterObj.value.filters.length) {
    receivedForMe(filterObj.value.filters);
  } else {
    receivedForMe();
  }
};
// Handle updating the limit start
const PaginationLimitStart = ([itemsPerPage, start]) => {
  filterObj.value.limitPageLength = itemsPerPage;
  filterObj.value.limit_start = start;
  if (filterObj.value.filters.length) {
    receivedForMe(filterObj.value.filters);
  } else {
    receivedForMe();
  }
};

const filters = ref([]);
const timeout = ref(null);

function inLineFiltersData(searchedData) {
  clearTimeout(timeout.value); // Clear previous timeout

  timeout.value = setTimeout(() => {
    // Initialize filters array
    filterObj.value.filters = [];

    // Loop through the table headers and build dynamic filters
    tableheaders.value.forEach((header) => {
      const key = header.td_key;

      if (searchedData[key]) {
        // Push as an array of 3 items
        filterObj.value.filters.push([key, "like", `%${searchedData[key]}%`]);
      }
    });

    // Check if status is present in the route query params


    // Call receivedForMe with or without filters
    if (filterObj.value.filters.length) {
      filterObj.value.limit_start = 0;
      receivedForMe(filterObj.value.filters);
    } else {
      receivedForMe();
    }
  }, 500); // Adjust debounce delay as needed
}
function receivedForMe(data) {
  // Initialize filters array for building dynamic query parameters

  const EmpRequestdesignation = JSON.parse(localStorage.getItem("employeeData"));
  employeeData.value = EmpRequestdesignation.designation;

  const filters = [
    // assigned_to_users
    ["assigned_to_users", "like", `%${EmpRequestdesignation?.designation}%`],
    ["property", "like", `%${newBusinessUnit.value.business_unit}%`],
    ["status", "!=", "Request Cancelled"],

    ["name", "in", viewlist.value],
    ["status", "!=", "Completed"]
  ];
  if (data) {
    filters.push(...data);
    // console.log(data);
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
      if (filterObj.value.limit_start === 0) {

        tableData.value = res.data;
        idDta.value = [...new Set(res.data.map((id) => id.name))];
        docTypeName.value = [
          ...new Set(res.data.map((docTypeName) => docTypeName.doctype_name)),
        ];
        statusOptions.value = [...new Set(res.data.map((status) => status.status))];
      }
      else {
        tableData.value = tableData.value.concat(res.data);
      }

    })
    .catch((error) => {
      console.error("Error fetching records:", error);
    });
}
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
