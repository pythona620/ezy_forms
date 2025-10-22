<template>
    <section>
        <template v-if="!viewReport">
            <div class="d-flex justify-content-between align-items-center py-2">
                <div>

                </div>

            </div>
            <div>
                <GlobalTable :tHeaders="tableheaders" :tData="tableData" @cell-click="viewPreview" isAction="true"
                    viewType="viewPdf" isCheckbox="true" />
            </div>
        </template>
        <template v-else>
            <div class="d-flex justify-content-between align-items-center py-2">


            </div>
            <section>
                <div class=" d-flex justify-content-between align-content-center   py-3">
                    <div class="d-flex align-items-center gap-2">

                    <button type="button" class="font-12 btn btn-light backtoListbtn" @click="backtoReportList">
                        <i class="bi bi-chevron-left"></i> Back to Report List
                    </button>
                    <div class=" position-relative">

                    <button type="button" class=" btn btn-dark font-12" @click="OpenFilterModal">Filters</button>
                    <button v-tooltip.bottom="'Clear Filters'" v-if="dateFilter.date_field.length || dateFilter.start_date.length || dateFilter.end_date.length" type="button" class="btn btn-light btn-sm clear_filters position-absolute top-0 right-0" @click="clearFilters">
                      <i class="bi bi-x"></i>
                        </button>
                    </div>
                    </div>
                    <!-- <button class=" btn btn-outline-danger font-12" @click="exportReport('Excel')">Export</button> -->
                    <div class=" d-flex gap-2 ">

                        <div class="btn-group dropdown">
                            <ButtonComp
                                class="btn-outline-primary  m-0 dropdown-toggle d-flex justify-content-center align-items-center bg-white"
                                name="Export" type="button" id="exportDropdown" data-bs-toggle="dropdown"
                                aria-expanded="false" />
                            <ul class="dropdown-menu font-12" style="transform: translate(-124px, 42px) !important">
                                <li><a class="dropdown-item" @click="exportReport('Csv')">Download Csv</a></li>
                                <li>
                                    <a class="dropdown-item" @click="exportReport('Excel')">Download Excel</a>
                                </li>
                            </ul>
                        </div>
                    </div>

                </div>
            </section>
            <section>
                <!-- <div id="datatable" tabindex="0" border="1" style="border-collapse: collapse; width: 100%;"></div> -->
                <GlobalTable class=" newtable" :tHeaders="listDataheaders" :tData="listData" @cell-click="downloadPdf"
                    isAction="true" download="true" />

                <div class="modal fade" id="SendMailModal" tabindex="-1" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Send Mail</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"
                                    aria-label="Close"></button>
                            </div>
                            <div class="modal-body">
                                Are you sure you want to send the mail?
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-outline-secondary"
                                    data-bs-dismiss="modal">Cancel</button>
                                <!-- <button type="button" class="btn btn-dark" @click="sendMail()">Yes,
                                    Proceed</button> -->
                                <button type="button" class="btn btn-dark" :disabled="saveloading" @click="sendMail()">
                                    <span v-if="saveloading" class="spinner-border spinner-border-sm" role="status"
                                        aria-hidden="true"></span>
                                    <span v-if="!saveloading">
                                        <span class="font-12 fw-bold">Yes, Proceed</span>
                                    </span>

                                </button>
                            </div>
                        </div>
                    </div>
                </div>
                <!-- Filter Modal -->
<div class="modal fade" id="filtersModal" tabindex="-1" aria-hidden="true">
  <div class="modal-dialog modal-lg modal-dialog-centered">
    <div class="modal-content">
      <!-- Header -->
      <div class="modal-header">
        <h5 class="modal-title font-14">{{ SelectedReportName }} Filters</h5>
        <button type="button" class="btn-close" data-bs-dismiss="modal" @click="closeFilterModal" aria-label="Close"></button>
      </div>

      <!-- Body -->
      <div class="modal-body">
        <!-- Date Filter (Static) -->
        <div class="pb-3 mb-3">
          <h6 class="font-13 fw-bold mb-2">Date Filter</h6>
          <div class="row g-2 align-items-end">
            <div class="col-md-3">
              <label class="form-label font-12">Label</label>
              <select v-model="dateFilter.date_field" placeholder="Select" class="form-select font-12">
                <option value="" disabled>Select</option>
                <option value="creation">Created On</option>
                <option value="modified">Last Updated On</option>
              </select>
            </div>

            <div class="col-md-3">
              <label class="form-label font-12">Start Date</label>
              <input type="date" v-model="dateFilter.start_date" class="form-control font-12" />
            </div>

            <div class="col-md-3">
              <label class="form-label font-12">End Date</label>
              <input type="date" v-model="dateFilter.end_date" class="form-control font-12" />
            </div>
          </div>
        </div>

        <!-- Dynamic Field Filters -->
        <!-- <div v-for="(filter, index) in filtersArray" :key="index" class="row mb-3 align-items-end border-top pt-2 mt-2">
          <div class="col-md-3">
            <label class="form-label font-12">Field</label>
            <select v-model="filter.field" class="form-select font-12">
              <option value="">Select Field</option>
              <option v-for="(field, i) in listDataheaders" :key="i" :value="field.th">
                {{ field.th }}
              </option>
            </select>
          </div>

          <div class="col-md-3">
            <label class="form-label font-12">Condition</label>
            <select v-model="filter.condition" class="form-select font-12">
              <option value="is">is</option>
              <option value="equal">Equal</option>
              <option value="not_equal">Not Equal</option>
            </select>
          </div>

          <div class="col-md-4">
            <label class="form-label font-12">Value</label>
            <input type="text" v-model="filter.value" class="form-control font-12" placeholder="Enter value" />
          </div>

          <div class="col-md-2 text-start">
            <button type="button" class="btn btn-outline-dark border-0 btn-sm" @click="removeFilterRow(index)">
              ✕
            </button>
          </div>
        </div>

        <div class="text-center mb-3">
          <button type="button" class="btn btn-light font-12 btn-sm" @click="addFilterRow">
            + Add Filter
          </button>
        </div> -->
      </div>
        <!-- Add Filter Button -->

      <!-- Footer -->
      <div class="modal-footer">
        <button type="button" class="btn btn-outline-secondary font-12" data-bs-dismiss="modal">Cancel</button>
        <button type="button" class="btn btn-dark h-auto " :disabled="saveloading" @click="applyFiltersToReport">
          <span class="font-12 fw-bold">Apply Filters</span>
        </button>
      </div>
    </div>
  </div>
</div>



            </section>
        </template>
    </section>
</template>

<script setup>

import GlobalTable from "../../Components/GlobalTable.vue";
import axiosInstance from "../../shared/services/interceptor";
import { apis, doctypes, domain } from "../../shared/apiurls";
import { onBeforeUnmount, onMounted, ref } from "vue";
// import DataTable from "frappe-datatable";
// import "frappe-datatable/dist/frappe-datatable.min.css";
import ButtonComp from "../../Components/ButtonComp.vue";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import { showSuccess } from "../../shared/services/toast";

const saveloading = ref(false)
// const totalRecords = ref(0);
const viewReport = ref(false);
const tableData = ref([]);
const frappeTH = ref([]);
function ReportsData() {
   
    axiosInstance.get(apis.getReportList)
        .then((res) => {
            if (res.message) {
                tableData.value = res.message;
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}
const listData = ref([]);
const listDataheaders = ref([])
const frappeBody = ref([]);
const SelectedReportName = ref("");
const source = ref('')



function viewPreview(data) {
    SelectedReportName.value = data.name;
    
    source.value = data.source
    viewReport.value = true;
    const payload = {
        doctype_name:SelectedReportName.value,
        source:source.value,
        filters:null
    }
    gettingReportData(payload)


}
function simulateCtrlF() {
    const datatableEl = document.getElementById("datatable");

    if (datatableEl) {
        // 1. Focus the table
        datatableEl.focus();

        // 2. Trigger internal keydown event
        const event = new KeyboardEvent("keydown", {
            key: "f",
            keyCode: 70,
            ctrlKey: true,
            bubbles: true,
        });
        datatableEl.dispatchEvent(event);
    }
}

function handleCtrlF(e) {
    if (e.ctrlKey && e.key === 'f') {
        e.preventDefault(); // prevent browser search
        simulateCtrlF();    // simulate datatable search
    }
}

function backtoReportList() {
    viewReport.value = false;
}
const tableheaders = ref([
    { th: "Name", td_key: "name" },

])

function exportReport(type) {
    if(source.value ==='report'){

    const reportName = SelectedReportName.value;
    const fileType = type;
    const url = apis.ExportReport + `?report_name=${encodeURIComponent(reportName)}&file_format_type=${encodeURIComponent(fileType)}`;
    // Trigger the file download
    window.open(url, '_blank');



    }else{

  if (!listData.value.length) {
    alert("No data to export!");
    return;
  }
  console.log(listDataheaders.value);
  console.log(listData.value);

  // ✅ Get header labels and matching keys
  const headers = listDataheaders.value.map((h) => h.th);
  const keys = listDataheaders.value.map((h) => h.td_key);

  // ✅ Build rows from your listData
  const rows = listData.value.map((row) =>
    keys.map((key) => `"${(row[key] ?? "")?.replace(/\|/g, ",")}"`)?.join(",")
  );

  // ✅ Join headers + rows
  const csvContent = [headers.join(","), ...rows].join("\n");

  if (type === "Csv") {
    downloadFile(csvContent, "report.csv", "text/csv");
  } else if (type === "Excel") {
    downloadFile(csvContent, "report.xls", "application/vnd.ms-excel");
  }
          
    }
}

function downloadFile(content, fileName, mimeType) {
  const blob = new Blob([content], { type: mimeType });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = fileName;
  link.click();
  URL.revokeObjectURL(url);
}

const reportsData = ref("");

function downloadPdf(data, index, type) {
    reportsData.value = data;
    if (type === "download") {
        if (!data?.name || !SelectedReportName?.value) {
            console.error("Missing required data for PDF download");
            return;
        }

        const reportName = SelectedReportName.value;
        const name = data.name || data.Name || data.id || data.report_name;

        const url = apis.getReportData + `?doctype=${encodeURIComponent(reportName)}&name=${encodeURIComponent(name)}`;

        // Open the PDF in a new tab
        window.open(url, "_blank");
    }

    if (type === "mail") {
        const modal = new bootstrap.Modal(document.getElementById('SendMailModal'));
        modal.show();
    }
}

function sendMail() {
  saveloading.value = true;

    const payload = {
        docname: reportsData.value.name,
        doctype: SelectedReportName.value,
    }

    axiosInstance
        .post(apis.reportMailSend, payload)
        .then((res) => {
            if (res) {
                const response = res;
                showSuccess("Mail send successfully")
                const modal = bootstrap.Modal.getInstance(
                    document.getElementById("SendMailModal")
                );
                modal.hide();
                saveloading.value = false;

            }
        })
        .catch((error) => {
            console.error("Upload error:", error);
        })
        .finally(() => {
            saveloading.value = false;
        })

}
function OpenFilterModal(){ const modal = new bootstrap.Modal(document.getElementById('filtersModal')); modal.show(); }
const filtersArray = ref([
  {
    field: "",
    condition: "is",
    value: "",
  },
]);

// Static date filter
const dateFilter = ref({
  date_field: "",
  start_date: "",
  end_date: "",
});

// Add new filter row
function addFilterRow() {
  filtersArray.value.push({
    field: "",
    condition: "is",
    value: "",
  });
}

// Remove filter row
function removeFilterRow(index) {
  filtersArray.value.splice(index, 1);
}

// Apply filters
function applyFiltersToReport() {
  saveloading.value = true;
  const filters = [];

  // Add all field filters
  filtersArray.value.forEach((filter) => {
    if (filter.field && filter.value) {
      filters.push({ [filter.field]: filter.value });
    }
  });

  // Add static date filter if filled
  if (
    dateFilter.value.date_field &&
    dateFilter.value.start_date &&
    dateFilter.value.end_date
  ) {
    filters.push({
      [dateFilter.value.date_field]: [
        dateFilter.value.start_date,
        dateFilter.value.end_date,
      ],
    });
  }

  const payload = {
    doctype_name: SelectedReportName.value,
    source: source.value,
    filters: JSON.stringify(filters),
  };

  console.log("✅ Final Payload:", JSON.stringify(payload, null, 2));

  // Example API call
  gettingReportData(payload);

  setTimeout(() => {
    saveloading.value = false;
    const modal = bootstrap.Modal.getInstance(
      document.getElementById("filtersModal")
    );
    modal.hide();
  }, 500);
}
function closeFilterModal(){
  dateFilter.value = {
    date_field: "",
    start_date: "",
    end_date: "",
  };
  filtersArray.value = [
    {
      field: "",
      condition: "is",
      value: "",
    },
  ];
}
function clearFilters(){
   dateFilter.value = {
    date_field: "",
    start_date: "",
    end_date: "",
  };
  filtersArray.value = [
    {
      field: "",
      condition: "is",
      value: "",
    },
  ];
  let payload = {
    doctype_name: SelectedReportName.value,
    source: source.value
  }
  gettingReportData(payload)

}
function gettingReportData(payload) {
    axiosInstance.get(apis.repostListData, {
        params: payload
    })
        .then((res) => {
            if (res) {
                if (res?.message?.columns) {
                    // frappeBody.value = res?.message?.result.map((item) => ({ ...item }));

                    // frappeTH.value = res?.message?.columns.map((item) => ({
                    //     name: item?.fieldname,
                    //     label: item?.label
                    // }));

                    // new DataTable(document.getElementById("datatable"), {
                    //     columns: frappeTH.value,
                    //     data: frappeBody.value,
                    //     inlineFilters: true,
                    //     editable: false,
                    // });

                    // frappeBody.value = res?.message?.result.map((item) =>
                    //     Object.values(item)
                    // ); 
                    // frappeTH.value = res?.message?.columns.map((item) => {
                    //     let obj = {};
                    //     obj["name"] = item?.label;
                    //     // obj["width"] = 170;
                    //     return obj;
                    // });
                    // //   if (frappeBody.value) {
                    // //     simulateCtrlF();
                    // //   }
                    listData.value = res?.message?.result;
                    listDataheaders.value = res?.message?.columns.map((item) => {
                        let obj = {};
                        obj["th"] = item?.label;
                        obj["td_key"] = item?.fieldname;
                        return obj;
                    });

                    // new DataTable(document.getElementById("datatable"), {
                    //     columns: frappeTH.value,
                    //     data: frappeBody.value,
                    //     inlineFilters: true,
                    //     editable: false,
                    // });
                }
            }
        })
        .catch((error) => {
            console.error("Error", error);
        });

}

// function downloadPdf(data) {

//   const doctype = encodeURIComponent(SelectedReportName.value);
//   const name = encodeURIComponent(data.name);

//   // Remove /api if present
//   let baseUrl = apis.getReportData.replace("/api", "");
//   const separator = baseUrl.includes("?") ? "&" : "?";
//   const pdfUrl = `${window.location.origin}${baseUrl}${separator}doctype=${doctype}&name=${name}`;

//   // Use Axios to fetch the PDF as a Blob
//   axiosInstance
//     .get(pdfUrl, { responseType: "blob" })
//     .then((response) => {
//       const file = new Blob([response.data], { type: "application/pdf" });
//       const fileURL = URL.createObjectURL(file);

//       const link = document.createElement("a");
//       link.href = fileURL;
//       link.download = `${data.name}.pdf`;
//       document.body.appendChild(link);
//       link.click();
//       document.body.removeChild(link);

//       // Cleanup
//       URL.revokeObjectURL(fileURL);
//     })
//     .catch((error) => {
//       console.error("Failed to download PDF:", error);
//     });
// }


// function downloadPdf(data) {
//   const name = data.name;
//   const doctype = SelectedReportName.value;

//   if (!doctype || !name) {
//     console.error("Missing doctype or name in data");
//     return;
//   }

//   const pdfUrl = `${domain}/printview?doctype=${doctype}&name=${name}`;

//   // Trigger download
//   const link = document.createElement("a");
//   link.href = pdfUrl;
//   link.target = "_blank"; // or "_self" if you want same tab
//   link.download = `${name}.pdf`; // optional - will only work if `Content-Disposition: attachment` is set by server
//   document.body.appendChild(link);
//   link.click();
//   document.body.removeChild(link);
// }


onMounted(() => {
    ReportsData();
    // simulateCtrlF();
    document.addEventListener("keydown", handleCtrlF);

})
onBeforeUnmount(() => {
    document.removeEventListener("keydown", handleCtrlF);
});

</script>

<style lang="scss" scoped>
.dropdown-item {
    cursor: pointer;
}
.dropdown-menu {
  z-index: 2000 !important;
}
.backtoListbtn {
    border: 1px solid #ccc !important;
}

.filters_main {
    min-height: 200px;
    overflow: auto;
}
.modal-title {
  font-weight: 600;
}
.form-label {
  font-weight: 500;
  color: #333;
}
.form-select,
.form-control {
  border-radius: 6px;
}
.btn-dark {
  border-radius: 6px;
  padding: 6px 16px;
}
.border {
  border: 1px solid #ddd !important;
}
.clear_filters{
  position: absolute;
    top: -15px;
    right: -14px;
    border-radius: 50%;
    background-color: #ccc;

}
</style>