<template>
  <div>

    <div class="d-flex justify-content-between align-items-center py-2 ">
      <div>
        <h1 class="m-0 font-13">
          Requests received for me
        </h1>
        <p class="m-0 font-11 pt-1">
          {{ totalRecords }} request
        </p>
      </div>

    </div>
    <div class="mt-2">
      <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction='true' actionType="dropdown" isCheckbox='true'
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
            <h5 class="modal-title font-13" id="viewRequestLabel">Request Id: {{ selectedRequest.name }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body approvermodalbody">
            <ApproverPreview :blockArr="showRequest" :current-level="selectedcurrentLevel"
              @updateField="updateFormData" />
          </div>
          <!-- v-if="selectedRequest.status !== 'In Progress'" -->
          <div  class="modal-footer">
            <div class="d-flex justify-content-between align-items-center mt-3 gap-2">
              <!-- <div>
                <ButtonComp type="button" icon="ban" class="cancelbtn border-1 text-nowrap font-10"
                  @click="approvalCancelFn(formData, 'Request Cancelled')" name="Cancel Request" />
              </div> -->
              <!-- <input type="text" class=" form-control" placeholder="Reason..."> -->
              <div>
                <!-- <ButtonComp @click="approvalCancelFn(formData, 'Request Cancelled')" type="button" icon="x"
                  class="rejectbtn border-1 text-nowrap font-10 " name="Reject" /> -->
                <button class=" btn btn-outline-danger font-10 py-0 rejectbtn" type="button" data-bs-dismiss="modal"
                  @click="approvalCancelFn(formData, 'Request Cancelled')">
                  <span><i class=" bi bi-x-lg me-2"></i></span>Reject
                </button>
              </div>
              <div>
                <ButtonComp type="button" icon="check2" class="approvebtn border-1 text-nowrap font-10 "
                  @click="ApproverFormSubmission(formData, 'Approve')" name="Approve" />
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>
  </div>


</template>
<script setup>

import ButtonComp from '../../Components/ButtonComp.vue';
import GlobalTable from '../../Components/GlobalTable.vue';
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from '../../shared/apiurls';
import { onMounted, ref, reactive, computed, watch } from 'vue';
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import PaginationComp from '../../Components/PaginationComp.vue';
import { rebuildToStructuredArray } from '../../shared/services/field_format';
import ApproverPreview from '../../Components/ApproverPreview.vue';
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
const businessUnit = computed(() => {
  return EzyBusinessUnit.value;
});
const newBusinessUnit = ref({ business_unit: '' });

const filterObj = ref({ limitPageLength: 'None', limit_start: 0 });
const totalRecords = ref(0);
const idDta = ref([]);
const docTypeName = ref([])
const statusOptions = ref([])
const emittedFormData = ref([]);
const selectedcurrentLevel = ref("");
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
const fieldMapping = ref({
  // invoice_type: { type: "select", options: ["B2B", "B2G", "B2C"] },
  // credit_irn_generated: { type: "select", options: ["Pending", "Completed", "Error"] },
  name: { type: "input" },
  doctype_name: { type: "input" },
  requested_on: { type: "date" },
});
const actions = ref(
  [
    { name: 'View Request', icon: 'fa-solid fa-eye' },

    // { name: 'Share this form', icon: 'fa-solid fa-share-alt' },
    // { name: 'Download Form', icon: 'fa-solid fa-download' },
    // { name: 'Edit Form', icon: 'fa-solid fa-edit' },

  ]
)
const tableData = ref([]);
const selectedRequest = ref({});
const showRequest = ref(null);
const doctypeForm = ref([]);

function actionCreated(rowData, actionEvent) {
  if (actionEvent.name === 'View Request') {
    if (rowData) {
      selectedRequest.value = { ...rowData };
      selectedcurrentLevel.value = selectedRequest.value.current_level

      // Rebuild the structured array from JSON
      showRequest.value = rebuildToStructuredArray(JSON.parse(selectedRequest.value?.json_columns)?.fields);

      // Prepare the filters for fetching data
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

      // Fetch the doctype data
      axiosInstance.get(`${apis.resource}${selectedRequest.value.doctype_name}`, { params: queryParams })
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

      const modal = new bootstrap.Modal(document.getElementById('viewRequest'), {});
      modal.show();
    } else {
      console.warn(" There is no form fields ");
    }
  }
}

// Function to capture the form data from ApproverPreview
const updateFormData = (fieldValues) => {
  emittedFormData.value = emittedFormData.value.concat(fieldValues);

};

// Function to handle form submission
function ApproverFormSubmission(dataObj, type) {
  let form = {};
  if (emittedFormData.value.length) {
    emittedFormData.value.map((each) => {
      form[each.fieldname] = each.value
    })
  }
  axiosInstance.put(`${apis.resource}${selectedRequest.value.doctype_name}/${doctypeForm.value.name}`, form).then((response) => {

    if (response?.data) {
      approvalStatusFn(dataObj, type)
    }
  })

};

function approvalStatusFn(dataObj, type) {
  console.log(dataObj);
  let data = {
    "property": selectedRequest.value.property,
    "doctype": selectedRequest.value.doctype_name,
    "request_ids": [selectedRequest.value.name],
    "reason": type,
    "action": type,
    "files": null,
    "cluster_name": null,
    "url_for_approval_id": '',
    // https://ezyrecon.ezyinvoicing.com/home/wf-requests
    "current_level": selectedRequest.value.current_level
  }

  // need to check this api not working 
  axiosInstance.post(apis.requestApproval, { request_details: [data] })
    .then((response) => {
      if (response?.message?.success) {
        if (type == 'Reject') {
          toast.error(`Request ${type}ed`, { autoClose: 1000 })
        } else {
          toast.success(`Request ${type}ed`, { autoClose: 1000 })
        }
        const modal = bootstrap.Modal.getInstance(document.getElementById('viewRequest'));
        modal.hide();
        receivedForMe()
      }
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

function approvalCancelFn(dataObj, type) {
  // let files = this.selectedFileAttachments.map((res: any) => res.url);

  let data = {
    "property": selectedRequest.value.property,
    "doctype": selectedRequest.value.doctype_name,
    "request_id": selectedRequest.value.name,
    "reason": type == 'Request Cancelled' ? "Cancelled" : "",
    "action": type,
    "files": [],
    'url_for_cancelling_id': '',
    "current_level": selectedRequest.value.current_level
  }
  axiosInstance.post(apis.wf_cancelling_request, data)
    .then((response) => {
      if (response?.message?.success) {
        const modal = bootstrap.Modal.getInstance(document.getElementById('viewRequest'));
        modal.hide();
        receivedForMe()
      }
    })
}

function mapFormFieldsToRequest(doctypeData, showRequestData) {
  showRequestData.forEach(block => {
    block.sections.forEach(section => {
      section.rows.forEach(row => {
        row.columns.forEach(column => {
          column.fields.forEach(field => {
            // Check if the fieldname exists in the doctypeForm and assign the value
            if (doctypeData?.hasOwnProperty(field?.fieldname)) {
              field.value = doctypeData[field.fieldname]; // Assign the value from doctypeForm to the field

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
  receivedForMe()


};
// Handle updating the limit start
const PaginationLimitStart = ([itemsPerPage, start]) => {
  filterObj.value.limitPageLength = itemsPerPage;
  filterObj.value.limit_start = start;
  receivedForMe()


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
  }
  else {
    receivedForMe();
  }

}
function receivedForMe(data) {
  // Initialize filters array for building dynamic query parameters
  const EmpRequestdesignation = JSON.parse(localStorage.getItem('employeeData'));

  const filters = [
    // assigned_to_users
    ["assigned_to_users", "like", `%${EmpRequestdesignation?.designation}%`],
    ["property", "like", `%${newBusinessUnit.value.business_unit}%`]

  ];
  if (data) {
    filters.push(data)
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

      receivedForMe()
    }
  },
  { immediate: true }
);
onMounted(() => {
  // receivedForMe()
})
</script>
<style scoped>
.approvebtn {
  width: 146px;
  height: 30px;
  background: #14D82B;
  color: white;
  padding: 5px 15px 5px 15px;
  gap: 7px;
  border-radius: 4px;
  opacity: 0px;

}

.rejectbtn {
  width: 146px;
  height: 30px;
  background: #FE212E;
  color: white;
  padding: 5px 15px 5px 15px;
  gap: 7px;
  border-radius: 4px;
  opacity: 0px;

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
</style>