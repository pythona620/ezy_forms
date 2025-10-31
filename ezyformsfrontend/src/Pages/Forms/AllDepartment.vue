<template>
  <div class="">
    <div>
      <div class="d-flex align-items-center justify-content-between py-3">
        <div>
          <h1 class="m-0 font-13">
            {{ id === 'allforms' ? 'All Active Forms' : id.toUpperCase() }}
          </h1>
          <p class="m-0 font-11 pt-1">
            {{ totalRecords }} Forms Available
          </p>
        </div>
     

      </div>
      <div class="mt-1">
        <!-- d-none d-lg-block -->
        <div class="d-none d-lg-block">

        <GlobalTable :tHeaders="tableheaders" :tData="tableData" isCheckbox="true" isAction="true" viewType="viewPdf"  raiseRequest="true"
          :enableDisable="isEnable" @cell-click="viewPreview" @actionClicked="actionCreated" QR_Code="true"
          @toggle-click="toggleFunction" :actions="actions" @updateFilters="inLineFiltersData"
          :field-mapping="fieldMapping" isFiltersoption="true" />
        </div>
         <div class=" d-block d-lg-none">
        <GlobalCard :tHeaders="tableheaders" :tData="tableData" isCheckbox="true" isAction="true" viewType="viewPdf"  raiseRequest="true"
          :enableDisable="isEnable" @cell-click="viewPreview" @actionClicked="actionCreated" QR_Code="true"
          @toggle-click="toggleFunction" :actions="actions" @updateFilters="inLineFiltersData"
          :field-mapping="fieldMapping" isFiltersoption="flase"  />
      </div>
        <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords" :items-per-page="filterObj.limitPageLength"
          @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
      </div>

    </div>
    <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="offcanvasRightLabel">Asset Request Form</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body">
        <div class="d-flex align-items-baseline position-relative gap-3">
          <div class="d-flex flex-column">
            <span>
              <i class="dashedcircle ri-checkbox-blank-circle-fill"></i>
            </span>
            <div class="dashed_line mt-4"></div>
          </div>
          <div>data</div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="pdfView" tabindex="-1" aria-labelledby="pdfViewLabel" aria-hidden="true">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="d-block modal-header bg-dark text-white py-2">
            <div class="d-flex align-items-center justify-content-between">
              <div>
                <h5 class="m-0 text-white font-13" id="exampleModalLabel">
                  PDF format
                </h5>
              </div>
              <div class="">
                <button button="button" class="btn btn-dark text-white font-13" @click="downloadPdf">Download Pdf<span
                    class="ms-2"><i class="bi bi-download"></i></span> </button>
                <button type="button" class="btn btn-dark text-white font-13" @click="closemodal"
                  data-bs-dismiss="modal">Close
                  <i class="bi bi-x"></i></button>
              </div>
            </div>
          </div>
          <div class="modal-body">

            <div v-html="pdfPreview"></div>
          </div>
          <div class="modal-footer">

          </div>
        </div>
      </div>
    </div>

    <div class="modal fade py-2" id="showQRModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-md modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title font-16">{{ formName.form_name }}</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <!-- Tabs Header -->
            <ul class="nav nav-tabs mb-3" id="qrTabs" role="tablist">
              <li class="nav-item" role="presentation">
                <button
                  class="nav-link active text-black"
                  id="static-tab"
                  data-bs-toggle="tab"
                  data-bs-target="#staticQR"
                  type="button"
                  role="tab"
                  aria-controls="staticQR"
                  aria-selected="true"
                >
                  Static QR
                </button>
              </li>
              <li class="nav-item" role="presentation">
                <button
                  class="nav-link text-black"
                  id="dynamic-tab"
                  data-bs-toggle="tab"
                  data-bs-target="#dynamicQR"
                  type="button"
                  role="tab"
                  aria-controls="dynamicQR"
                  aria-selected="false"
                >
                  Dynamic QR
                </button>
              </li>
            </ul>

            <!-- Tabs Content -->
            <div class="tab-content" id="qrTabsContent">
              <!-- Static QR Tab -->
              <div class="tab-pane fade show active" id="staticQR" role="tabpanel" aria-labelledby="static-tab">
                <div class="text-center">
                  <qrcode-vue :value="formName.qr_url" :size="180" level="H" class="qrCodeDiv" />
                </div>
                <div class="input-group my-3">
                  <input
                    type="text"
                    class="form-control shadow-none font-12"
                    :value="formName.qr_url"
                    readonly
                  />
                  <button
                    class="btn bg-secondary text-white shadow-none"
                    @click="copyQR('static')"
                  >
                    <i class="bi bi-copy h-100"></i>
                  </button>
                </div>
                <div>
                  <button
                    class="btn download-btn font-14 w-100 shadow-none"
                    @click="downloadQR('static')"
                  >
                    <i class="bi bi-download me-2"></i> Download
                  </button>
                </div>
              </div>

              <!-- Dynamic QR Tab -->
              <div class="tab-pane fade" id="dynamicQR" role="tabpanel" aria-labelledby="dynamic-tab">
                <div>
                  <div v-if="dynamicQrData.dynamic_link" class="text-center">
                  <qrcode-vue :value="dynamicQrData.dynamic_link" :size="180" level="H" class="qrCodeDiv"/>
                  </div>
                <div class="d-flex gap-2 mt-4">
                  <div class="w-100">
                    <label class="font-13 ms-1">Form Valid From</label>
                    <input class="form-control shadow-none mt-2 font-13" type="datetime-local" name="Value" id="formNameSeries"
                      v-model="dynamicQrData.form_valid_from" />
                  </div>
                  <div class="w-100">
                    <label class="font-13 ms-1">Form Valid To</label>
                    <input class="form-control shadow-none mt-2 font-13" type="datetime-local" name="Value" id="formNameSeries"
                      v-model="dynamicQrData.form_valid_to" />
                  </div>
                </div>
                <button class="btn CreateQrBtn font-14 w-100 shadow-none my-3" @click="generateDynamicQR">
                     <i class="bi bi-qr-code-scan me-2"></i>
                      {{ dynamicQrData.dynamic_link ? 'Update QR Code' : 'Generate QR Code' }}
                </button>
                </div>
              </div>
            </div>
          </div>

        </div>
      </div>
    </div>


    <!-- Modal -->
    <div class="modal fade" id="EnableDisable" tabindex="-1" aria-labelledby="EnableDisableLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="EnableDisableLabel">Confirm Action</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Are you sure you want to <span id="actionTextSpan"></span> <span class=" fw-bold font-13"
              id="rowNameSpan"></span> Form?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-dark" @click="confirmAction">Yes, Proceed</button>

          </div>
        </div>
      </div>
    </div>


    <!-- <FormPreview :blockArr="selectedForm" :formDescriptions="formDescriptions" :childHeaders="childtableHeaders" /> -->

  </div>
</template>

<script setup>
import { ref, computed, watch, reactive, onMounted } from 'vue';
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes, domain } from '../../shared/apiurls';
import GlobalTable from '../../Components/GlobalTable.vue';
import { EzyBusinessUnit } from '../../shared/services/business_unit';
// import { rebuildToStructuredArray } from '../../shared/services/field_format';
import PaginationComp from "../../Components/PaginationComp.vue"
// import FormPreview from '../../Components/FormPreview.vue'

import router from '../../router';
import { useRoute } from 'vue-router';
import GlobalCard from '../../Components/GlobalCard.vue';
import QrcodeVue from "qrcode.vue";
import { showInfo, showSuccess, showWarning } from '../../shared/services/toast';
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
// import ButtonComp from '../../Components/ButtonComp.vue';
const totalRecords = ref(0);
const tableheaders = ref([
  { th: "Form Name", td_key: "form_name" },
  // { th: "Form Short Code", td_key: "form_short_name" },
  { th: "Department", td_key: "form_department" },
  { th: "Form Type", td_key: "as_web_view" },
  // { th: "Status", td_key: "form_status" },
  // { th: "Form Status", td_key: "enable" },

]);

const props = defineProps(['id']);
const formDescriptions = ref({})
const selectedForm = ref(null);
const tableData = ref([]);
const formCategory = ref([]);
const route = useRoute();
const pdfPreview = ref('')

const childtableHeaders = ref([]);
const is_admin = ref('');
const isEnable = ref("");
const userDept=ref([]);


// Business unit and filter object
const businessUnit = computed(() => EzyBusinessUnit.value);
const newBusinessUnit = ref({ business_unit: '' });
const filterObj = ref({ limitPageLength: 20, limit_start: 0, filters: [] });
const actions = computed(() => {
  const baseActions = [
    { name: 'View form', icon: 'fa-solid fa-eye' },
    { name: 'Raise Request', icon: 'fa fa-file-text' },
  ]


  return baseActions
})

const formName = ref("");


/**
 * Copy QR URL to clipboard
 * @param {string} type - 'static' or 'dynamic'
 */
const copyQR = (type) => {
  const url =
    type === "dynamic" ? dynamicQrData.value.dynamic_link : formName.value.qr_url;
  navigator.clipboard.writeText(url);
  toast.success(
    `Copied ${type === "dynamic" ? "Dynamic" : "Static"} QR for ${formName.value.form_name}`,
    { autoClose: 600 }
  );
};

/**
 * Download QR code image
 * @param {string} type - 'static' or 'dynamic'
 */
const downloadQR = (type) => {
  const canvasSelector = type === "dynamic" ? "#dynamicQR canvas" : "#staticQR canvas";
  const canvas = document.querySelector(canvasSelector);
  if (!canvas) return;

  const url = canvas.toDataURL("image/png");
  const a = document.createElement("a");
  const suffix = type === "dynamic" ? "_dynamic" : "_static";
  const fileName = formName.value.form_name
    ? `${formName.value.form_name}${suffix}.png`
    : `qrcode${suffix}.png`;

  a.href = url;
  a.download = fileName;
  a.click();
};

const dynamicQrData = ref({});

function generateDynamicQR(){
  const dataObj = {
      "form_name": formName.value.form_short_name,
      "form_valid_from": dynamicQrData.value.form_valid_from,
      "form_valid_to": dynamicQrData.value.form_valid_to,
  };

  axiosInstance.post(apis.generate_dynamic_qr_code, dataObj)
    .then((response) => {
      dynamicQrData.value=response.message;
      showSuccess(dynamicQrData.value.message);
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

// const showShareOptions = ref(false);

// const shareQR = async () => {
//   try {
//     const canvas = document.querySelector("canvas");
//     const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/png"));
//     const fileName = formName.value.form_name ? `${formName.value.form_name}.png` : "qrcode.png";
//     const file = new File([blob], fileName, { type: "image/png" });

//     const shareData = {
//       title: formName.value.form_name,
//       text: `Check out this form:\n${formName.value.qr_url}`,
//       files: [file],
//     };

//     if (navigator.canShare && navigator.canShare({ files: [file] })) {
//       await navigator.share(shareData);
//     } else {
//       showShareOptions.value = true;
//     }
//   } catch (err) {
//     console.error("Sharing failed:", err);
//     showShareOptions.value = true;
//   }
// };




const fieldMapping = ref({
  // invoice_type: { type: "select", options: ["B2B", "B2G", "B2C"] },
  form_short_name: { type: "input" },
  form_category: { type: "input" },
  form_status: { type: "select", options: ["Active", "Retired"] },
  form_name: { type: "input" },
  enable: { type: "select", options: ["Enabled", "Disabled"] }

  // requested_on: { type: "date" },
});
function formCreation(item = null) {
  if (item == null) {
    router.push({
      name: "FormStepper", query: {
        routepath: route.path,
        business_unit: businessUnit.value,

      },
    });

  } else {
    router.push({
      name: "FormStepper",
      params: { paramid: item.name },
      query: {
        routepath: route.path,
        business_unit: businessUnit.value,
        id: item.name

      }

    });
  }
  localStorage.setItem('routepath', route.path)
}

function viewPreview(data, index, type) {
  if (type === "view") {
    if (data) {
      router.push({
        name: "FormPreviewComp",
        query: {
          routepath: route.path,
          form_short_name: data.form_short_name,
          business_unit: businessUnit.value,

        },
      });
    }

  }
  if (type === "QR Code") {
    formName.value = data;

    const dataObj = {
      "form_name": formName.value.form_short_name,
    };

  axiosInstance.post(apis.fetchDynamicQrData, dataObj)
    .then((response) => {
      dynamicQrData.value = response.message;
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });

    if(formName.value.qr_url && data.as_web_view===1){
      const modal = new bootstrap.Modal(document.getElementById('showQRModal'), {});
      modal.show();
    }
    else{
      toast.info("No QR Code Available", { autoClose: 500 })
    }

  }
  if (type === 'raiseRequest') {
    const parsedData = JSON.parse(data.form_json);
    const storedData = localStorage.getItem("employeeData");
    // console.log(parsedData);

    if (storedData) {
      const designation = JSON.parse(storedData).designation;
      // console.log(designation);

      if (!parsedData.workflow.length) {
        showInfo("No Roles Added")
      }
      const roles = parsedData.workflow[0].roles;
      // console.log(roles);

      let hasAccess = false;

      for (let i = 0; i < roles.length; i++) {
        if (roles[i] === designation) {
          hasAccess = true;
          break;
        }
      }
      // console.log(route.path, "sadasda");

      if (hasAccess) {
         if(data.form_name === 'VENDOR COMPARISON'){
            router.push({
          name: "vendorcomparison",
 
          });

        } else{

        router.push({
          name: "RaiseRequest",
          query: {
            routepath: route.path,
            selectedForm: data.form_short_name,
            business_unit: data.business_unit,


          },
        });
        }

      } else {
        showInfo("You do not have permission to access this Form.");
      }
    }
    //  else {
    //   console.log("No employee data found in localStorage.");
    // }
  }


}
function actionCreated(rowData, actionEvent) {
  if (actionEvent.name === 'View form') {
    if (rowData) {
      // formDescriptions.value = { ...rowData }
      // selectedForm.value = rebuildToStructuredArray(JSON.parse(rowData?.form_json).fields)
      // childtableHeaders.value = JSON.parse(
      //     rowData.form_json
      //   ).child_table_fields;
      // const modal = new bootstrap.Modal(document.getElementById('formViewModal'), {});// raise a modal
      // modal.show();


      router.push({
        name: "FormPreviewComp",
        query: {
          routepath: route.path,
          form_short_name: rowData.form_short_name,
          business_unit: businessUnit.value,

        },
      });

    } else {
      showWarning(" There is no form fields ")
    }
  }
  else if (actionEvent.name === 'Edit Form') {
    formCreation(rowData);
  }

  if (actionEvent.name === 'Raise Request') {
    // console.log(rowData);
    const parsedData = JSON.parse(rowData.form_json);
    const storedData = localStorage.getItem("employeeData");

    if (storedData) {
      const designation = JSON.parse(storedData).designation;
      // console.log(designation);
      if (!parsedData.workflow?.length) {
        showInfo("No Roles Added");
      }
      const roles = parsedData.workflow[0].roles;
      // console.log(roles);

      let hasAccess = false;

      for (let i = 0; i < roles.length; i++) {
        if (roles[i] === designation) {
          hasAccess = true;
          break;
        }
      }
      // console.log(route.path, "sadasda");

      if (hasAccess && rowData.enable === 1) {
        
        router.push({
          name: "RaiseRequest",
          query: {
            routepath: route.path,
            selectedForm: rowData.form_short_name,
            business_unit: rowData.business_unit,
            has_workflow:rowData.has_workflow


          },
        });
      } else if (rowData.enable === 0) {
      showInfo("This form is currently disabled.");
    } else {
      showInfo("You do not have permission to access this Form.");
    }
    }
    //  else {
    //   console.log("No employee data found in localStorage.");
    // }
  }

  if (actionEvent.name === 'Download Print format') {
    // pdfView
    formDescriptions.value = rowData

    const dataObj = {
      "form_short_name": rowData.form_short_name,
      business_unit: businessUnit.value

    };

    axiosInstance.post(apis.preview_dynamic_form, dataObj)
      .then((response) => {

        pdfPreview.value = response.message

      })
      .catch((error) => {
        console.error("Error fetching data:", error);
      });
    const modal = new bootstrap.Modal(document.getElementById('pdfView'), {});
    modal.show();
  }
}

function downloadPdf() {

  const dataObj = {
    "form_short_name": formDescriptions.value.form_short_name,
    "name": null,
    business_unit: businessUnit.value
  };

  axiosInstance.post(apis.download_pdf_form, dataObj)
    .then((response) => {

      let pdfUrl = domain + response.message;

      // Remove 'api' from the URL if present
      pdfUrl = pdfUrl.replace('/api', '');

      // Create an anchor element to trigger the download
      const link = document.createElement('a');
      link.href = pdfUrl;
      link.download = response.message.split('/').pop(); // Use the file name from the URL
      link.click();
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

const responcedata = ref([]);

// Toggle function triggered when a checkbox is clicked
const selectedRowData = ref(null);
const selectedActionText = ref('');

function toggleFunction(rowData, rowIndex, event) {
  selectedRowData.value = rowData;
  const isCurrentlyEnabled = rowData.enable == '1' || rowData.enable === 1;
  selectedActionText.value = isCurrentlyEnabled ? 'Disable' : 'Restore';

  document.getElementById('actionTextSpan').innerText = selectedActionText.value;
  document.getElementById('rowNameSpan').innerText = rowData.name;

  const modal = new bootstrap.Modal(document.getElementById('EnableDisable'));
  modal.show();
  window.currentModal = modal;
}

function confirmAction() {
  if (!selectedRowData.value) return;

  const isCurrentlyEnabled = selectedRowData.value.enable == '1' || selectedRowData.value.enable === 1;
  selectedRowData.value.enable = isCurrentlyEnabled ? 0 : 1;

  axiosInstance
    .put(`${apis.resource}${doctypes.EzyFormDefinitions}/${selectedRowData.value.name}`, selectedRowData.value)
    .then((response) => {
      responcedata.value = response.data;
      showSuccess(`Form ${selectedActionText.value}d successfully`);
      setTimeout(() => {
        fetchDepartmentDetails();
      }, 1000);
      if (window.currentModal) window.currentModal.hide();
    })
    .catch((error) => {
      console.error("Error updating toggle:", error);
    });
}



// Watch business unit and department ID changes
watch(
  [() => businessUnit.value, () => props.id],
  ([newBusinessUnitVal, newId]) => {
    newBusinessUnit.value.business_unit = newBusinessUnitVal;
    if (newBusinessUnitVal.length && newId && props.id !== ':id') {
      filterObj.value.limit_start = 0;
      filterObj.value.filters = [];
      fetchDepartmentDetails(newId || props.id, null);
    }
  },
  { immediate: true }
);

// Handle updating the current value
// // Handle updating the current value
// const PaginationUpdateValue = (itemsPerPage) => {
//   filterObj.value.limitPageLength = itemsPerPage;
//   filterObj.value.limit_start = 0;

//   fetchDepartmentDetails(); // always uses current filterObj.value.filters
// };

// // Handle updating the limit start
// const PaginationLimitStart = ([itemsPerPage, start]) => {
//   filterObj.value.limitPageLength = itemsPerPage;
//   filterObj.value.limit_start = start;

//   fetchDepartmentDetails();
// };



const timeout = ref(null);

// function inLineFiltersData(searchedData) {
//   clearTimeout(timeout.value);

//   timeout.value = setTimeout(() => {
//     filterObj.value.filters = [];

//     // Special handling
//     if (searchedData.form_status === 'Active') {
//       filterObj.value.filters.push(["form_status", "like", "Created"]);
//     } else if (searchedData.form_status === 'Retired') {
//       filterObj.value.filters.push(["form_status", "like", "Draft"]);
//     }

//     if (searchedData.enable === 'Enabled') {
//       filterObj.value.filters.push(["enable", "=", 1]);
//     } else if (searchedData.enable === 'Disabled') {
//       filterObj.value.filters.push(["enable", "=", 0]);
//     }

//     // Other filters
//     tableheaders.value.forEach((header) => {
//       const key = header.td_key;
//       const value = searchedData[key];
//       if (key === 'form_status' || key === 'enable') return;

//       if (value) {
//         filterObj.value.filters.push([key, "like", `%${value}%`]);
//       }
//     });

//     // Reset pagination
//     filterObj.value.limit_start = 0;
//     filterObj.value.limitPageLength = 20;

//     fetchDepartmentDetails();
//   }, 500);
// }

// // Fetch department details function
// function fetchDepartmentDetails() {
//   // Base filters (fresh every time)
//   let filters = [
//     ["business_unit", "=", `${newBusinessUnit.value.business_unit}`],
//     ["form_status", "like", "Created"],  // fixed case
//     ["accessible_departments", "like", `%${userDept.value}%`]
//   ];

//   // Add owner filter if needed
//   if (props.id && props.id !== "allforms") {
//     filters.push(["owner_of_the_form", "=", props.id]);
//   }

//   // Inline filters: override base if same key, otherwise append
//   if (filterObj.value.filters.length) {
//     const inline = filterObj.value.filters;

//     // Filter out duplicates: keep inline over base
//     filters = filters.filter(([key]) => {
//       return !inline.some(([inlineKey]) => inlineKey === key);
//     });

//     filters.push(...inline);
//   }

//   // Replace instead of pushing duplicates
//   filterObj.value.filters = filters;

//   const queryParams = {
//     fields: JSON.stringify(["*"]),
//     limit_page_length: filterObj.value.limitPageLength,
//     limit_start: filterObj.value.limit_start,
//     filters: JSON.stringify(filterObj.value.filters),
//     order_by: "`tabEzy Form Definitions`.`enable` DESC, `tabEzy Form Definitions`.`creation` DESC"
//   };

//   const queryParamsCount = {
//     fields: JSON.stringify(["count(name) AS total_count"]),
//     limitPageLength: "None",
//     filters: JSON.stringify(filterObj.value.filters),
//   };

//   // Count query
//   axiosInstance.get(`${apis.resource}${doctypes.EzyFormDefinitions}`, { params: queryParamsCount })
//     .then((res) => {
//       totalRecords.value = res.data[0].total_count;
//     })
//     .catch((error) => {
//       console.error("Error fetching ezyForms data:", error);
//     });

//   // Data query
//   axiosInstance.get(`${apis.resource}${doctypes.EzyFormDefinitions}`, { params: queryParams })
//     .then((response) => {
//       if (filterObj.value.limit_start === 0) {
//         tableData.value = response.data;
//         formCategory.value = [...new Set(tableData.value.map((form) => form.form_category))];
//       } else {
//         tableData.value = tableData.value.concat(response.data);
//       }
//     })
//     .catch((error) => {
//       console.error("Error fetching department details:", error);
//     });
// }

const fullData = ref([]);
const filteredData = ref([]);
const VendorComparison=ref("");

function fetchDepartmentDetails() {
  const userDetails = JSON.parse(localStorage.getItem('employeeData'));

const queryParams = {
  designation: userDetails.designation || "",
  property: `${newBusinessUnit.value.business_unit}`,
  fields: JSON.stringify(["accessible_departments","active","business_unit","count",
    "creation",
    "docstatus",
    "enable",
    "form_category",
    "form_department",
    "form_json",
    "form_name",
    "form_short_name",
    "form_status",
    "has_workflow",
    "idx",
    "is_landscape",
    "is_linked",
    "is_linked_form",
    "is_predefined_doctype",
    "modified",
    "modified_by",
    "name",
    "owner",
    "owner_of_the_form",
    "print_format",
    "series",
    "workflow_check",
    "qr_url",
    "as_web_view",
    "dynamic_link",
  ]),
};

  if (props.id && props.id !== "allforms") {
    queryParams.department = props.id;
  }

  axiosInstance
    .get(apis.GetAccessibleDeptForms, { params: queryParams })
    .then((response) => {
      if (Array.isArray(response.message)) {
      fullData.value = response.message;
    } else {
      fullData.value = [];
    }
    filteredData.value = [...fullData.value];
    totalRecords.value = filteredData.value.length;
    filterObj.value.limit_start = 0;
    tableData.value = filteredData.value.slice(0, filterObj.value.limitPageLength);
    
    if (props.id === "allforms") {
      const hasVendorComparison = fullData.value.some(
        (item) => item.form_name === "Vendor Comparison"
      );
      VendorComparison.value = hasVendorComparison;
      sessionStorage.setItem("VendorComparison", hasVendorComparison);
    }
    
  })
    .catch((error) => {
      console.error(error);
    });
}

function paginateData(filtered = filteredData.value) {
  const paginated = filtered.slice(filterObj.value.limit_start, filterObj.value.limit_start + filterObj.value.limitPageLength);
  tableData.value = paginated;
  totalRecords.value = filtered.length;
}

function inLineFiltersData(searchedData) {
  clearTimeout(timeout.value);

  timeout.value = setTimeout(() => {
    filteredData.value = fullData.value.filter((row) => {
      return tableheaders.value.every((header) => {
        const key = header.td_key;
        if (searchedData[key]) {
          return String(row[key] || "").toLowerCase().includes(String(searchedData[key]).toLowerCase());
        }
        return true;
      });
    });

    totalRecords.value = filteredData.value.length;
    filterObj.value.limitPageLength = 20;
    filterObj.value.limit_start = 0;

    tableData.value = filteredData.value.slice(0, filterObj.value.limitPageLength);
  }, 500);
}

function PaginationUpdateValue(newLimit) {
  filterObj.value.limitPageLength = newLimit;
  filterObj.value.limit_start = 0;
  paginateData();
}

function PaginationLimitStart() {
  filterObj.value.limit_start += filterObj.value.limitPageLength;
  const nextBatch = filteredData.value.slice(filterObj.value.limit_start, filterObj.value.limit_start + filterObj.value.limitPageLength);
  tableData.value = [...tableData.value, ...nextBatch];
}








// // Handle updating the current value
// const PaginationUpdateValue = (itemsPerPage) => {
//   filterObj.value.limitPageLength = itemsPerPage;
//   filterObj.value.limit_start = 0;
//     fetchDepartmentDetails(); 

// };
// // Handle updating the limit start
// const PaginationLimitStart = ([itemsPerPage, start]) => {
//   filterObj.value.limitPageLength = itemsPerPage;
//   filterObj.value.limit_start = start;
//     fetchDepartmentDetails(); 

// };


// const timeout = ref(null);

// function inLineFiltersData(searchedData) {
//   clearTimeout(timeout.value); // Clear previous timeout

//   timeout.value = setTimeout(() => {
//     filterObj.value.filters = [];


//     // Loop through the table headers and build dynamic filters
//     if (searchedData.form_status === 'Active') {
//       filterObj.value.filters.push(["form_status", "like", "Created"]);
//     }
//     if (searchedData.form_status === 'Retired') {
//       filterObj.value.filters.push(["form_status", "like", "Draft"]);
//     }
//     // console.log(searchedData.enable);
//     if (searchedData.enable === 'Enabled') {
//       filterObj.value.filters.push(["enable", "=", 1]);
//     } else if (searchedData.enable === 'Disabled') {
//       filterObj.value.filters.push(["enable", "=", 0]);
//     }


//     // Loop through other table headers and add filters
//     tableheaders.value.forEach((header) => {
//       const key = header.td_key;
//       const value = searchedData[key];

//       if (key === 'form_status' || key === 'enable') return; // Skip since we already handled it above

//       if (value) {
//         filterObj.value.filters.push([key, "like", `%${value}%`]);
//       }
//     });

//     // Call fetchDepartmentDetails with or without filters
//     if (filterObj.value.filters.length) {
//       fetchDepartmentDetails(null, filterObj.value.filters);
//     } else {
//       fetchDepartmentDetails();
//     }
//   }, 500); // Adjust debounce delay as needed
// }
// // Fetch department details function
// function fetchDepartmentDetails(id, data) {

//   const filters = [
//     ["business_unit", "=", `${newBusinessUnit.value.business_unit}`],
//     ["form_status", "like", "created"],
//     ["accessible_departments", "like", `%${userDept.value}%`]

//   ];
//   if (props.id && props.id !== "allforms" && props.id !== "allforms") {
//     // console.log(props.id); 
//     filters.push(["owner_of_the_form", "=", props.id]);
//   }
//   if (data) {
//     filters.push(...data)
//   }
//   filterObj.value.filters.push(...filters);

//   const queryParams = {
//     fields: JSON.stringify(["*"]),
//     limit_page_length: filterObj.value.limitPageLength,
//     limit_start: filterObj.value.limit_start,
//     filters: JSON.stringify(filterObj.value.filters),
//     order_by: "`tabEzy Form Definitions`.`enable` DESC, `tabEzy Form Definitions`.`creation` DESC"
//   };
//   const queryParamsCount = {
//     fields: JSON.stringify(["count(name) AS total_count"]),
//     limitPageLength: "None",
//     filters: JSON.stringify(filterObj.value.filters),
//   }
//   axiosInstance.get(`${apis.resource}${doctypes.EzyFormDefinitions}`, { params: queryParamsCount })
//     .then((res) => {

//       totalRecords.value = res.data[0].total_count

//     })
//     .catch((error) => {
//       console.error("Error fetching ezyForms data:", error);
//     });

//   axiosInstance
//     .get(`${apis.resource}${doctypes.EzyFormDefinitions}`, { params: queryParams })
//     .then((response) => {

//       if (filterObj.value.limit_start === 0) {
//         tableData.value = response.data;
//         formCategory.value = [...new Set(tableData.value.map((formCategory) => formCategory.form_category))];

//       } else {
//         tableData.value = tableData.value.concat(response.data);
//       }
//     })
//     .catch((error) => {
//       console.error("Error fetching department details:", error);
//     });
// }


onMounted(() => {
  localStorage.removeItem('routepath')

  const userData = JSON.parse(localStorage.getItem('employeeData'));
  is_admin.value = userData.is_admin || '';

  if (is_admin.value == 1) {
    isEnable.value = "true";
  }
  if (route.path === "/forms/department/allforms" || route.path === "/forms/department/allforms") {
    router.replace("/forms/department/allforms");
  }

})

</script>

<style>
.dashedcircle {
  border: 1px dashed #AAAAAA;
  height: 30px;
  width: 30px;
  padding: 0;
  margin: 0;
  border-radius: 50%;
  color: #14D82B;
}

.dashed_line {
  height: 100px;
  border: 1px dashed #AAAAAA;
  width: 1px;
  position: absolute;
  left: 2%;
}


.cancelfilter {
  width: 150px;
  height: 34px;
  border-radius: 6px;
  background-color: #f1f1f1;
  color: #111111;
  padding: 8px 20px;
}

.applyfilter {
  width: 150px;
  height: 34px;
  border-radius: 6px;
  /* background-color: #f1f1f1; 
  color: #111111;  */
  padding: 8px 20px;
}


.filterbtn {
  border: 1px solid #CCCCCC;
  font-size: 16px;
  border-radius: 4px;
  color: #999999;
  padding: 8px;
  width: 100%;
}

.download-btn{
  padding: 10px;
  border: 1px dashed #6c757d;
  display: flex;
  justify-content: center;
  align-items: center;

}
.download-btn:hover{
  background-color: #6c757d;
  color: white;
}
.qrCodeDiv{
  border: 1px solid black;
  padding: 10px;
  border-radius: 6px;
}
.CreateQrBtn{
  background-color: #343a40;
  color: white;
}

.CreateQrBtn:hover{
  border:1px solid #6c757d;
  color: black;
}

.nav-tabs {
  border-bottom: 2px solid #dee2e6;
  justify-content: center;
}

.nav-tabs .nav-link {
  border: none;
  background: transparent;
  color: #555;
  font-weight: 500;
  position: relative;
  transition: color 0.3s;
}

.nav-tabs .nav-link::after {
  content: "";
  position: absolute;
  left: 0;
  bottom: -2px;
  width: 0%;
  height: 3px;
  background-color: #007bff;
  transition: width 0.3s ease;
}

.nav-tabs .nav-link:hover::after {
  width: 100%;
}

.nav-tabs .nav-link.active {
  color: #007bff;
}

.nav-tabs .nav-link.active::after {
  width: 100%;
}
</style>
