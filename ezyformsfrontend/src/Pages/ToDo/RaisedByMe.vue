<template>
  <div>
    <div class="d-flex justify-content-between align-items-center py-2">
      <div>
        <h1 class="m-0 font-13">Requests Submitted</h1>
        <p class="m-0 font-11 pt-1">{{ totalRecords }} request</p>
      </div>
    </div>
    <div class="mt-2">
      <!-- actionType="dropdown" -->
      <!-- raiseRequest="true" -->
      <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction="true" isCheckbox="true" viewType="viewPdf"
        @cell-click="viewPreview" :actions="actions" @actionClicked="actionCreated" isFiltersoption="true"
        :field-mapping="fieldMapping" @updateFilters="inLineFiltersData" />
      <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords" :items-per-page="filterObj.limitPageLength"
        @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
    </div>
    <div class="modal fade" id="viewRequest" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
      aria-labelledby="viewRequestLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
          <!-- <div class="modal-header">
            <h5 class="modal-title" id="viewRequestLabel">Request</h5>
            <button button="button" class=" btn btn-dark text-white font-13" @click="downloadPdf">Download Pdf<span
                class=" ms-2"><i class="bi bi-download"></i></span> </button>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div> -->
          <!-- bg-dark text-white -->
          <div class="modal-header py-2 d-block">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h5 class="m-0 font-13" id="viewRequest">Request Id: {{ selectedRequest.name?.replace(/_/g, " ") }}
                </h5>

              </div>
              <div class="">
                <button button="button" class="btn btn-white text-dark font-13" @click="downloadPdf">
                  Download Pdf<span class="ms-2"><i class="bi bi-download"></i></span>
                </button>
                <button type="button" class="btn btn-white text-dark font-13" @click="closemodal"
                  data-bs-dismiss="modal">
                  Close <i class="bi bi-x"></i>
                </button>
              </div>
            </div>
          </div>
          <div class="modal-body approvermodalbody">
            <!-- <ApproverPreview :blockArr="showRequest" :childHeaders="tableHeaders" :childData="responseData"
               :current-level="totalLevels" @updateField="updateFormData" /> -->
            <!-- <div v-if="tableName" class="mt-2">
              <div>
                <span class="font-13 fw-bold">{{ tableName }}</span>
              </div>
              <table class="table table-bordered table-striped">
                <thead>
                  <tr>
                    <th>#</th>
                    <th v-for="field in tableHeaders" :key="field.fieldname">
                      {{ field.label }}
                    </th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, index) in tableRows" :key="index">
                    <td>{{ index + 1 }}</td>
                    <td v-for="field in tableHeaders" :key="field.fieldname">
                      <span
                        v-if="isFilePath(row[field.fieldname])"
                        class="cursor-pointer"
                        @click="openFile(row[field.fieldname])"
                      >
                        
                        <span
                          >View Attachment <i class="bi bi-eye-fill ps-1"></i
                        ></span>
                      </span>
                      <span v-else>
                        {{ row[field.fieldname] || "-" }}
                      </span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div> -->
          </div>
          <div class="activity-log-container">
            <div v-for="(item, index) in activityData" :key="index" class="activity-log-item"
              :class="{ 'last-item': index === activityData.length - 1 }">
              <div class="activity-log-dot"></div>
              <div class="activity-log-content">
                <p class="font-12 mb-1">
                  On
                  <strong class="strong-content">{{
                    formatDate(item.creation)
                    }}</strong>,
                  <strong class="strong-content">
                    <span v-if="index == 0">you</span>
                    <span v-else>

                      {{ item.user_name }}
                    </span>
                  </strong>
                  ({{ item.role }})
                  <strong class="strong-content">{{
                    formatAction(item.action)
                    }}</strong>
                  the request with the comments:
                  <strong class="strong-content">{{
                    item.reason || "N/A"
                    }}</strong>.
                </p>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <div class="d-flex justify-content-between align-items-center gap-2">
              <!-- <button type="button" class="btn btn-white text-dark  font-13" @click="closemodal"
                data-bs-dismiss="modal">Close
                <i class="bi bi-x"></i></button> -->
              <!-- <div v-if="selectedRequestStatus == 'Request Raised'">
                <button :disabled="loading" type="submit" class="btn edit-btn"
                  @click="approvalCancelFn('Request Cancelled')">
                  <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                  <span v-if="!loading"><i class="bi bi-check-lg font-11 me-2"></i><span class="font-10">Cancel
                      Request</span></span>
                </button>

              </div> -->
            </div>
            <div v-if="selectedRequestStatus == 'Request Raised'">
              <ButtonComp type="button" class="border-1 edit-btn text-nowrap font-10" @click="handleEditClick"
                name="Edit Form" />
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
  </div>
</template>
<script setup>
// import FormFields from "../../Components/FormFields.vue";
import ButtonComp from "../../Components/ButtonComp.vue";
import GlobalTable from "../../Components/GlobalTable.vue";
import axiosInstance from "../../shared/services/interceptor";
import { apis, doctypes, domain } from "../../shared/apiurls";
import {
  callWithErrorHandling,
  onMounted,
  ref,
  reactive,
  computed,
  watch,
} from "vue";
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import PaginationComp from "../../Components/PaginationComp.vue";
import { rebuildToStructuredArray } from "../../shared/services/field_format";
// import ApproverPreview from "../../Components/ApproverPreview.vue";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import { useRoute, useRouter } from "vue-router";
const businessUnit = computed(() => {
  return EzyBusinessUnit.value;
});
const router = useRouter();

const newBusinessUnit = ref({ business_unit: "" });

const filterObj = ref({ limitPageLength: 20, limit_start: 0, filters: [] });
const totalRecords = ref(0);
const selectedRequest = ref({});
const showRequest = ref(null);
const doctypeForm = ref([]);
const idDta = ref([]);
const docTypeName = ref([]);
const statusOptions = ref([]);
const formData = ref([]);
const tableData = ref([]);
const totalLevels = ref("");
const pdfPreview = ref("");
const activityData = ref([]);
const selectedRequestStatus = ref("");
const tableRows = ref([]);
const tableHeaders = ref([]);
const tableName = ref("");
const responseData = ref([]);
const route = useRoute();

const loading = ref(false);

const tableheaders = ref([
  { th: "Request ID", td_key: "name" },
  { th: "Form Name", td_key: "doctype_name" },
  // { th: "Linked Form", td_key: "is_linked_form" },
  
  // { th: "Business Unit", td_key: "property" },
  // { th: "Form category", td_key: "doctype_name" },
  // { th: "Role", td_key: "role" },
  { th: "Requested on", td_key: "requested_on" },
  { th: "Approval Status", td_key: "status" },
  { th: "Pending With", td_key: "assigned_to_users" },
  { th: "Last Action On", td_key: "modified" },
  { th: "Linked ID", td_key: "linked_form_id" },
]);

const actions = ref([
  { name: "View Request", icon: "fa-solid fa-eye" },
  { name: "PDF Format", icon: "bi bi-filetype-pdf" },
  // { name: 'Share this form', icon: 'fa-solid fa-share-alt' },
  // { name: 'Download Form', icon: 'fa-solid fa-download' },
  // { name: 'Edit Form', icon: 'fa-solid fa-edit' },
]);

function viewPreview(data, index, type) {
  // console.log(data, ";;;", type);
  if (type === 'view') {

    router.push({
      name: "ApproveRequest",
      query: {
        routepath: route.path,
        name: data.name,
        doctype_name: data.doctype_name,
        business_unit: data.property,
        status: data.status,
        type: "myforms",
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
  // if(type === 'raiseRequest'){
  //   router.push({
  //     name: "RaiseRequest",
  //     query: {
  //       routepath: route.path,
  //       main_form: data.doctype_name,
  //       main_form_Id: data.name,
  //       business_unit:data.property,
  //       status:data.status,
  //       type: "myforms",
  //       readOnly: 'false',
  //       has_workflow: 'Yes',
  //       linkedForm:data.is_linked_form,
  //       selectedFormStatus: data.status
  //     }
  //     });

  // }
}
function handleEditClick() {
  const modalElement = document.getElementById("viewRequest");
  if (modalElement) {
    const modalInstance = bootstrap.Modal.getInstance(modalElement); // Get existing modal instance
    if (modalInstance) {
      modalInstance.hide();
    }
  }
  // console.log("selectedRequest",selectedRequest.value.status);

  // Navigate to the new route
  router.push({
    name: "RaiseRequest",
    query: {
      routepath: route.path,
      business_unit: selectedRequest.value.property,
      selectedForm: selectedRequest.value.doctype_name,
      selectedFormId: selectedRequest.value.name,
      selectedFormStatus: selectedRequest.value.status,

    },
  });
}

const requestcancelled = computed(() => {
  return activityData.value.some((item) => item.action === "Request Cancelled");
});

function actionCreated(rowData, actionEvent) {
  if (actionEvent.name === "View Request") {
    if (rowData) {
      selectedRequest.value = { ...rowData };
      selectedRequestStatus.value = rowData.status;

      totalLevels.value = selectedRequest.value?.total_levels;

      tableHeaders.value = JSON.parse(
        selectedRequest.value?.json_columns
      ).child_table_fields;
      // console.log(tableHeaders.value, "lll");

      // console.log(tableHeaders.value, "req");

      // console.log(selectedRequest.value,"0000");
      // Rebuild the structured array from JSON
      showRequest.value = rebuildToStructuredArray(
        JSON.parse(selectedRequest.value?.json_columns).fields
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
            doctypeForm.value = res.data;
            // console.log(typeof doctypeForm.value, "doctype", typeof showRequest.value);
            // Map values from doctypeForm to showRequest fields
            mapFormFieldsToRequest(doctypeForm.value[0], showRequest.value);
            axiosInstance
              .get(`${apis.resource}${selectedRequest.value.doctype_name}`)
              .then((res) => {
                console.log(`Data for :`, res.data[0]);
              })
              .catch((error) => {
                console.error(`Error fetching data for :`, error);
              });
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
        .get(
          `${apis.resource}${doctypes.WFActivityLog}/${selectedRequest.value.name}`
        )
        .then((res) => {
          if (res.data) {
            // console.log(res.data);
            activityData.value = res.data.reason || []; // Ensure it's always an array
          }
        })
        .catch((error) => {
          console.error("Error fetching activity data:", error);
        });
      const modal = new bootstrap.Modal(
        document.getElementById("viewRequest"),
        {}
      );
      modal.show();
    } else {
      console.warn(" There is no form fields ");
    }
  } else if (actionEvent.name === "PDF Format") {
    // pdfView
    selectedRequest.value = rowData;
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
          doctypeForm.value = res.data;

          const dataObj = {
            form_short_name: rowData.doctype_name,
            name: doctypeForm.value[0].name,
            business_unit: businessUnit.value
          };

          axiosInstance
            .post(apis.preview_dynamic_form, dataObj)
            .then((response) => {
              pdfPreview.value = response.message;
            })
            .catch((error) => {
              console.error("Error fetching data:", error);
            });
        }
      })
      .catch((error) => {
        console.error("Error fetching categories data:", error);
      });

    const modal = new bootstrap.Modal(document.getElementById("pdfView"), {});
    modal.show();
  }
}
function closemodal() {
  responseData.value = [];
  tableName.value = "";
}
const openFile = (filePath) => {
  if (!filePath) return;
  const fileUrl = `${filePath}`;
  window.open(fileUrl, "_blank");
};

const isFilePath = (value) => {
  if (!value) return false;
  return /\.(png|jpg|jpeg|gif|pdf|docx|xlsx|txt)$/i.test(value);
};

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
// function downloadPdf() {

//   const dataObj = {
//     "form_short_name": selectedRequest.value.doctype_name,
//     "name": doctypeForm.value[0].name
//   };

//   axiosInstance.post(apis.download_pdf_form, dataObj)
//     .then((response) => {

//       // Assuming 'domain' contains the base URL like 'https://example.com/api/'
//       let pdfUrl = domain + response.message;

//       // Remove 'api' from the URL if present
//       pdfUrl = pdfUrl.replace('/api', '');

//       window.open(pdfUrl);
//     })
//     .catch((error) => {
//       console.error("Error fetching data:", error);
//     });
// }
function downloadPdf() {
  const dataObj = {
    form_short_name: selectedRequest.value.doctype_name,
    name: doctypeForm.value[0]?.name,
    business_unit: businessUnit.value

  };

  axiosInstance
    .post(apis.download_pdf_form, dataObj)
    .then((response) => {
      // Assuming 'domain' contains the base URL like 'https://example.com/api/'
      let pdfUrl = domain + response.message;

      // Remove 'api' from the URL if present
      pdfUrl = pdfUrl.replace("/api", "");

      // Create an anchor element to trigger the download
      const link = document.createElement("a");
      link.href = pdfUrl;
      link.download = response.message.split("/").pop(); // Use the file name from the URL
      link.click();
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

// Function to capture the form data from ApproverPreview
const updateFormData = (fieldValues) => {
  formData.value = formData.value.concat(fieldValues);
};



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

const PaginationUpdateValue = (itemsPerPage) => {
  filterObj.value.limitPageLength = itemsPerPage;
  filterObj.value.limit_start = 0;
  if (filterObj.value.filters.length) {
    receivedForMe(filterObj.value.filters);
  }
  else {
    receivedForMe();
  }
};
// Handle updating the limit start
const PaginationLimitStart = ([itemsPerPage, start]) => {
  filterObj.value.limitPageLength = itemsPerPage;
  filterObj.value.limit_start = start;
  if (filterObj.value.filters.length) {
    receivedForMe(filterObj.value.filters);
  }
  else {
    receivedForMe();
  }
};

const timeout = ref(null);

function inLineFiltersData(searchedData) {
  console.log(searchedData);
  clearTimeout(timeout.value); // Clear previous timeout

  timeout.value = setTimeout(() => {
    // Initialize filters array
    filterObj.value.filters = [];

    // Loop through the table headers and build dynamic filters
    tableheaders.value.forEach((header) => {
      const key = header.td_key;

      if (searchedData[key]) {
        filterObj.value.filters.push([key, "like", `%${searchedData[key]}%`]);

      }
    });

    // Call receivedForMe with or without filters
    if (filterObj.value.filters.length) {
      filterObj.value.limit_start = 0;
      receivedForMe(filterObj.value.filters);
    } else {
      receivedForMe();
    }

    // Optionally call fetchTotalRecords
    // fetchTotalRecords(filters);
  }, 500); // Adjust debounce delay as needed
}

function receivedForMe(data) {
  // Initialize filters array for building dynamic query parameters
  const EmpRequestMail = JSON.parse(localStorage.getItem("employeeData"));
  const filters = [
    ["requested_by", "like", EmpRequestMail.emp_mail_id],
    ["property", "=", `${newBusinessUnit.value.business_unit}`],
  ];

  if (data) {
    filters.push(...data);
  }

  // Define query parameters for data and count retrieval
  const queryParams = {
    fields: JSON.stringify(["*"]),
    limit_page_length: filterObj.value?.limitPageLength,
    limit_start: filterObj.value?.limit_start,
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
    .get(`${apis?.resource}${doctypes?.WFWorkflowRequests}`, {
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
      const newData = res.data;
      if (filterObj.value.limit_start === 0) {
        tableData.value = newData;

        idDta.value = [...new Set(newData.map((id) => id.name))];
        docTypeName.value = [
          ...new Set(newData.map((docTypeName) => docTypeName.doctype_name)),
        ];
        statusOptions.value = [
          ...new Set(newData.map((status) => status.status)),
        ];
      }
      else {
        tableData.value = tableData.value.concat(newData)
      }


    })
    .catch((error) => {
      console.error("Error fetching records:", error);
    });
}

const fieldMapping = computed(() => ({

  // invoice_type: { type: "select", options: ["B2B", "B2G", "B2C"] },
  status: {
    type: "select",
    options: [
      "Request Raised",
      "In Progress",
      "Completed",
      "Request Cancelled",
    ],
  },
  name: { type: "input" },
  doctype_name: { type: "input" },
  requested_on: { type: "date" },
  role: { type: "input" },
  modified:{type:"date"},

}))



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
<style lang="scss" scoped>
.approvebtn {
  width: 146px;
  height: 30px;
  /* background: #14D82B; */
  color: white;
  padding: 5px 15px 5px 15px;
  gap: 7px;
  border-radius: 4px;
  opacity: 0px;
}

.edit-btn {
  background-color: #333;
  color: white;
  padding: 5px 15px 5px 15px;
  border-radius: 4px;
  font-weight: bold;
  width: 150px;
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
}

.pdf-body {
  width: 100%;
  height: 70vh;
  overflow-y: scroll;
  /* overflow: hidden; */
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
</style>
