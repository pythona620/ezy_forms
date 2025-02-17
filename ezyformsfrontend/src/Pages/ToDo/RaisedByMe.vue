<template>
  <div>
    <div class="d-flex justify-content-between align-items-center py-2">
      <div>
        <h1 class="m-0 font-13">Requests raised for me</h1>
        <p class="m-0 font-11 pt-1">{{ totalRecords }} request</p>
      </div>
    </div>
    <div class="mt-2">
      <!-- actionType="dropdown" -->
      <GlobalTable
        :tHeaders="tableheaders"
        :tData="tableData"
        isAction="true"
        viewType="viewPdf"
        isCheckbox="true"
        @cell-click="viewPreview"
        :actions="actions"
        @actionClicked="actionCreated"
        isFiltersoption="true"
        :field-mapping="fieldMapping"
        @updateFilters="inLineFiltersData"
      />
      <PaginationComp
        :currentRecords="tableData.length"
        :totalRecords="totalRecords"
        @updateValue="PaginationUpdateValue"
        @limitStart="PaginationLimitStart"
      />
    </div>
    <div
      class="modal fade"
      id="viewRequest"
      data-bs-backdrop="static"
      data-bs-keyboard="false"
      tabindex="-1"
      aria-labelledby="viewRequestLabel"
      aria-hidden="true"
    >
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
                <h5 class="m-0 font-13" id="viewRequest">Request</h5>
              </div>
              <div class="">
                <button
                  button="button"
                  class="btn btn-white text-dark font-13"
                  @click="downloadPdf"
                >
                  Download Pdf<span class="ms-2"><i class="bi bi-download"></i></span>
                </button>
                <button
                  type="button"
                  class="btn btn-white text-dark font-13"
                  @click="closemodal"
                  data-bs-dismiss="modal"
                >
                  Close <i class="bi bi-x"></i>
                </button>
              </div>
            </div>
          </div>
          <div class="modal-body approvermodalbody">
            <ApproverPreview
              :blockArr="showRequest"
              :current-level="totalLevels"
              @updateField="updateFormData"
            />
          </div>
          <div class="activity-log-container">
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
                  <strong class="strong-content">{{ formatDate(item.creation) }}</strong
                  >,
                  <strong class="strong-content">
                    <!-- {{ item.user_name }} -->
                    you
                  </strong>
                  ({{ item.role }})
                  <strong class="strong-content">{{ formatAction(item.action) }}</strong>
                  the request
                  <!-- with the comments: <strong class="strong-content">{{ item.reason || 'N/A' }}</strong>. -->
                </p>
              </div>
            </div>
          </div>
          <!-- <div class="modal-footer">
            <div class="d-flex justify-content-between align-items-center mt-3 gap-2">
              <button type="button" class="btn btn-white text-dark  font-13" @click="closemodal"
                data-bs-dismiss="modal">Close
                <i class="bi bi-x"></i></button>
              <div>
                <ButtonComp type="button" icon="x"
                  class="btn btn-dark d-flex align-items-center  approvebtn border-1 text-nowrap font-10 "
                  @click="approvalCancelFn(formData, 'Request Cancelled')" name="Cancel Request" />
              </div>
            </div>
          </div> -->
        </div>
      </div>
    </div>
    <div
      class="modal fade"
      id="pdfView"
      tabindex="-1"
      aria-labelledby="pdfViewLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-header py-2 d-block bg-dark text-white">
            <div class="d-flex justify-content-between align-items-center">
              <div>
                <h5 class="m-0 text-white font-13" id="exampleModalLabel">PDF format</h5>
              </div>
              <div class="">
                <button
                  button="button"
                  class="btn btn-dark text-white font-13"
                  @click="downloadPdf"
                >
                  Download Pdf<span class="ms-2"><i class="bi bi-download"></i></span>
                </button>
                <button
                  type="button"
                  class="btn btn-dark text-white font-13"
                  @click="closemodal"
                  data-bs-dismiss="modal"
                >
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
// import ButtonComp from "../../Components/ButtonComp.vue";
import GlobalTable from "../../Components/GlobalTable.vue";
import axiosInstance from "../../shared/services/interceptor";
import { apis, doctypes, domain } from "../../shared/apiurls";
import { callWithErrorHandling, onMounted, ref, reactive, computed, watch } from "vue";
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import PaginationComp from "../../Components/PaginationComp.vue";
import { rebuildToStructuredArray } from "../../shared/services/field_format";
import ApproverPreview from "../../Components/ApproverPreview.vue";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import { useRoute, useRouter } from "vue-router";

const businessUnit = computed(() => {
  return EzyBusinessUnit.value;
});
const router = useRouter();
const route = useRoute();

const newBusinessUnit = ref({ business_unit: "" });

const filterObj = ref({ limitPageLength: "None", limit_start: 0 });
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

const tableheaders = ref([
  { th: "Request ID", td_key: "name" },
  { th: "Form name", td_key: "doctype_name" },
  // { th: "Form category", td_key: "doctype_name" },
  { th: "Owner of form", td_key: "role" },
  { th: "Requested on", td_key: "requested_on" },
  // { th: "Total Levels", td_key: "total_levels" },
  { th: "Approval Status", td_key: "status" },
]);
const fieldMapping = ref({
  // invoice_type: { type: "select", options: ["B2B", "B2G", "B2C"] },
  status: {
    type: "select",
    options: ["Request Raised", "In Progress", "Completed", "Request Cancelled"],
  },
  // name: { type: "input" },
  doctype_name: { type: "input" },
  // requested_on: { type: "date" },
});

const actions = ref([
  { name: "View Request", icon: "fa-solid fa-eye" },
  { name: "PDF Format", icon: "bi bi-filetype-pdf" },
  // { name: 'Share this form', icon: 'fa-solid fa-share-alt' },
  // { name: 'Download Form', icon: 'fa-solid fa-download' },
  // { name: 'Edit Form', icon: 'fa-solid fa-edit' },
]);

function viewPreview(data) {
  router.push({
    name: "ApproveRequest",
    query: {
      routepath: route.path,
      name: data.name,
      doctype_name: data.doctype_name,
      type: "myforms",
    },
  });
}

function actionCreated(rowData, actionEvent) {
  if (actionEvent.name === "View Request") {
    if (rowData) {
      selectedRequest.value = { ...rowData };
      totalLevels.value = selectedRequest.value.total_levels;
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
            // Map values from doctypeForm to showRequest fields
            mapFormFieldsToRequest(doctypeForm.value[0], showRequest.value);
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

function ApproverFormSubmission(dataObj, type) {
  let form = {};
  form["doctype"] = selectedRequest.value.doctype_name;
  form["company_field"] = selectedRequest.value.property;
  form["name"] = doctypeForm.value.name;
  if (emittedFormData.value.length) {
    emittedFormData.value.map((each) => {
      form[each.fieldname] = each.value;
    });
  }

  // form['form_json']
  const formData = new FormData();
  formData.append("doc", JSON.stringify(form));
  formData.append("action", "Save");
  axiosInstance
    .post(apis.savedocs, formData)
    .then((response) => {
      if (response?.docs) {
        approvalCancelFn(dataObj, type);
      }
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

function approvalCancelFn(dataObj, type) {
  let data = {
    property: selectedRequest.value.property,
    doctype: selectedRequest.value.doctype_name,
    current_level: selectedRequest.value.current_level,
    request_id: selectedRequest.value.name,
    reason: type == "Request Cancelled" ? "Cancelled" : "",
    files: [],
    url_for_cancelling_id: "",
    // "action": type,
    // "cluster_name": null,
    // https://ezyrecon.ezyinvoicing.com/home/wf-requests
  };

  // need to check this api not working
  axiosInstance
    .post(apis.wf_cancelling_request, data)
    .then((response) => {
      if (response?.message?.success) {
        toast.success(`${type}`, { autoClose: 1000 });
        const modal = bootstrap.Modal.getInstance(document.getElementById("viewRequest"));
        modal.hide();
        receivedForMe();
      }
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

// // Function to handle form submission
// const ApproverFormSubmission = () => {

//   // if (emittedFormData.value.length) {
//   //       emittedFormData.value.map((each) => {
//   //           form[each.fieldname] = each.value
//   //       })
//   //   }

//   let data = {
//     "property": selectedRequest.value.property,
//     "doctype": selectedRequest.value.doctype_name,
//     "request_ids": selectedRequest.value.name,
//     "reason": "",
//     "action": selectedRequest.value.action,
//     "files": "[]",
//     "cluster_name": null,
//     "url_for_approval_id": '',
//     // https://ezyrecon.ezyinvoicing.com/home/wf-requests
//     "current_level": selectedRequest.value.current_level
//   }

//   // axiosInstance.post(apis.requestApproval, { request_details: [data] })
//   //   .then((response) => {

//   toast.success("Rquest Approved", { autoClose: 1000 })
//   const modal = bootstrap.Modal.getInstance(document.getElementById('viewRequest'));
//   modal.hide();
//   // })
//   // .catch((error) => {
//   //   console.error("Error fetching data:", error);
//   // });

// };

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
  //   fetchTotalRecords(filters);
}

function receivedForMe(data) {
  // Initialize filters array for building dynamic query parameters
  const EmpRequestMail = JSON.parse(localStorage.getItem("employeeData"));
  const filters = [
    ["requested_by", "like", EmpRequestMail.emp_mail_id],
    ["property", "like", `%${newBusinessUnit.value.business_unit}%`],
    // ["status", "!=", "Completed"],
  ];

  if (data) {
    filters.push(data);
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
    .get(`${apis?.resource}${doctypes?.WFWorkflowRequests}`, { params: queryParamsCount })
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
  /* background: #14D82B; */
  color: white;
  padding: 5px 15px 5px 15px;
  gap: 7px;
  border-radius: 4px;
  opacity: 0px;
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
</style>
