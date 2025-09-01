<template>
  <div class="card-table-view">
    <!-- Filter row (if enabled) -->
    <div v-if="isFiltersoption == 'true'" class="filters-card mb-2">
      <div v-for="(column, index) in tHeaders" :key="index" class="filter-item">
        <template v-if="fieldMapping[column.td_key]">
          <!-- Text input -->
          <div v-if="fieldMapping[column.td_key].type === 'input'" class="input-group">
            <span v-show="!focusedFields[column.td_key]" class="input-group-text">
              <i class="bi bi-search"></i>
            </span>
            <input
              type="search"
              class="form-control font-12" placeholder="Search..."
              v-model="filters[column.td_key]"
              @input="handleFilterChange"
              @focus="focusedFields[column.td_key] = true"
              @blur="focusedFields[column.td_key] = false"
            />
          </div>

          <!-- Date input -->
          <input
            v-else-if="fieldMapping[column.td_key].type === 'date'"
            type="date"
            class="form-control"
            v-model="filters[column.td_key]"
            @input="handleFilterChange"
          />

          <!-- Select dropdown -->
          <select
            v-else-if="fieldMapping[column.td_key].type === 'select'"
            class="form-select"
            v-model="filters[column.td_key]"
            @change="handleFilterChange"
          >
            <option value="">All</option>
            <option v-for="(option, optionIndex) in fieldMapping[column.td_key].options" :key="optionIndex" :value="option">
              {{ option }}
            </option>
          </select>
        </template>
      </div>
    </div>

    <!-- Data Cards -->
    <div v-if="tData.length" class="cards-container">
      <div v-for="(row, rowIndex) in tData" :key="rowIndex" class="card shadow-sm p-3 mb-3 rounded-3">
        <div class="card-header d-flex justify-content-between align-items-center">
          <h6 class="mb-0 font-responsive">#{{ rowIndex + 1 }}</h6>
          <div v-if="isAction === 'true' && viewType === 'viewPdf'" class="card-actions d-flex gap-3">
            <i v-if="raiseRequest === 'true'" v-tooltip.top="'Raise Request'" class="bi bi-send eye-cursor"
              @click="handleCellClick(row, rowIndex, 'raiseRequest')"></i>
            <i v-tooltip.top="'View'" class="ri-eye-line eye-cursor"
              @click="handleCellClick(row, rowIndex, 'view')"></i>
            <i v-if="download === 'true'" class="bi bi-download eye-cursor"
              @click="handleCellClick(row, rowIndex, 'download')"></i>
          </div>
        </div>

        <div class="card-body row">
          <div v-for="(column, colIndex) in tHeaders" :key="colIndex" class="col-md-6 col-lg-4 pb-2 mb-2">
            <div class="field-label text-muted small font-label">{{ column.th }}</div>
            <div class="field-value font-responsive">
              <!-- Keep your existing conditions -->
              <span v-if="column.td_key === 'status'">
                <i class="bi bi-circle-fill status-circle me-1"
                   :class="{
                     'text-warning': row[column.td_key] === 'Request Raised',
                     'textcompleted': row[column.td_key] === 'Completed',
                     'text-primary': row[column.td_key] === 'In Progress',
                     'textcancel': row[column.td_key] === 'Cancelled',
                     'RequestCancelled': row[column.td_key] === 'Request Cancelled',
                     'text-success': row[column.td_key] === 'Success',
                     'text-danger': row[column.td_key] === 'Failed'
                   }"></i>
                {{ row[column.td_key] }}
              </span>

              <span v-else-if="column.td_key === 'active'" :class="{ 'text-success': row[column.td_key] == 1, 'text-danger': row[column.td_key] == 0 }">
                {{ row[column.td_key] == 1 ? 'Active' : 'Inactive' }}
              </span>
               <span v-else-if="column.td_key === 'assigned_to_users'">
                <div>
                  <span v-tooltip.top="getAssignedToUsers(row, column)">
                    <div>
                      <span>{{ getAssignedToUsers(row, column) }}</span>
                    </div>
                  </span>

                </div>
              </span>

              <span v-else-if="column.td_key === 'form_status'">
                {{ row[column.td_key] === 'Created' ? 'Active' : 'Retired' }}
              </span>

              <span v-else-if="column.td_key === 'installed'">
                <i class="bi bi-circle-fill me-1"
                   :class="{ 'text-success': row[column.td_key] === 'Yes', 'text-danger': row[column.td_key] === 'No' }"></i>
                {{ row[column.td_key] }}
              </span>

              <span v-else-if="column.td_key === 'requested_on' || column.td_key === 'invoice_date' || column.td_key === 'creation' || column.td_key === 'communication_date'">
                {{ formatDate(row[column.td_key]) }}
              </span>

              <span class="font-responsive" v-else>
                {{ row[column.td_key] || '-' }}
              </span>
            </div>
          </div>
        </div>
        <!-- <div class="card-footer d-flex justify-content-end align-items-center">
         
          <div v-if="isAction === 'true' && viewType === 'viewPdf'" class="card-actions d-flex gap-3">
            <i v-if="raiseRequest === 'true'" v-tooltip.top="'Raise Request'" class="bi bi-send eye-cursor"
              @click="handleCellClick(row, rowIndex, 'raiseRequest')"></i>
            <i v-tooltip.top="'View'" class="ri-eye-line eye-cursor"
              @click="handleCellClick(row, rowIndex, 'view')"></i>
            <i v-if="download === 'true'" class="bi bi-download eye-cursor"
              @click="handleCellClick(row, rowIndex, 'download')"></i>
          </div>
        </div> -->

        <!-- Raise Request button in card footer -->
        <div v-if="isRequest === 'true'" class="card-footer text-end">
          <button v-if="raiseRequest === 'true'" class="btn btn-sm btn-outline-primary"
            @click="handleCellClick(row, rowIndex, 'raiseRequest')">Raise Request</button>
        </div>
      </div>
    </div>

    <!-- No Data -->
    <div v-else class="text-center text-muted py-5">No Data Found</div>
  </div>
</template>

<script setup>
// import ButtonComp from "./ButtonComp.vue";
import { defineProps, defineEmits, ref, onMounted, watch, reactive } from "vue";
// import moment from "moment";
// import FormFields from "./FormFields.vue";
const props = defineProps({
  tHeaders: {
    type: Array,
    required: true,
  },

  selectedText: {
    type: String,
  },
  selectedOption: {
    type: Array,
    default: () => [],
  },
  tData: {
    type: Array,
    required: true,
  },
  actions: {
    type: Array,
  },
  download: {
    type: String,
  },
  raiseRequest: {
    type: String
  },
  actionType: {
    type: String,
  },
  viewType: {
    type: String,
  },
  view: {
    type: String
  },
  // class: {
  //   type: String,
  //   required: true,
  // },
  isAction: {
    type: String,
  },
  isRequest: {
    type: String,
  },
  isCheckbox: {
    type: String,
  },
  isFiltersoption: {
    type: String,
  },
  fieldMapping: {
    type: Object,
    required: false,
  },
  enableDisable: {
    type: String,

  }
});

const emits = defineEmits(["actionClicked", "updateFilters", "cell-click", "toggle-click", "actionClickedDropDown"]);

function selectedAction(row, action) {
  emits("actionClicked", row, action);
  // console.log(row, action);
}
function actionDropDown(row) {
  emits("actionClickedDropDown", row);
}

function handleToggle(row, index, event) {
  // Emit the custom event. The parent component will handle showing the confirmation.
  emits("toggle-click", row, index, event);
  // console.log("event", event);
}
const focusedFields = reactive({});

function getDisplayText(key, value) {
  if (key === 'modified') return '-';
  if (value == null) return '-';
  if (typeof value === 'object') return '-';
  return String(value).replace(/_/g, ' ');
}


function getTooltipText(value) {
  if (value == null || typeof value === 'object') return '-';
  return String(value).replace(/_/g, ' ');
}

const allCheck = ref(false);
// function formatDate(dateString) {
//   if (!dateString) return "-"; // Handle empty or null values

//   // Extract date and time parts
//   const [datePart, timePart] = dateString.split(" ");
//   const [year, month, day] = datePart.split("/");

//   // Extract hours, minutes, and seconds from timePart
//   let [hours, minutes, seconds] = timePart.split(":");

//   // Format output as DD.MM.YYYY @ HH:MM:SS
//   return `${day.padStart(2, "0")}.${month.padStart(
//     2,
//     "0"
//   )}.${year} @ ${hours}:${minutes}:${seconds.slice(0, 2)}`;
// }


// function formatDate(dateString) {
//   if (!dateString) return "-";

//   try {
//     let date;

//     // Format: YYYY/MM/DD HH:MM:SS:ms (colon-separated with optional ms)
//     if (dateString.includes("/") && dateString.includes(" ")) {
//       const [datePart, timePart] = dateString.split(" ");
//       const [year, month, day] = datePart.split("/");

//       let timeSegments = timePart.split(":");
//       let hours = timeSegments[0]?.padStart(2, "0") || "00";
//       let minutes = timeSegments[1]?.padStart(2, "0") || "00";
//       let seconds = timeSegments[2]?.padStart(2, "0") || "00";

//       if (timeSegments.length === 4) {
//         const milliseconds = timeSegments[3];
//         date = new Date(
//           `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}T${hours}:${minutes}:${seconds}.${milliseconds}`
//         );
//       } else {
//         date = new Date(
//           `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}T${hours}:${minutes}:${seconds}`
//         );
//       }
//     }

//     // Format: YYYY-MM-DD HH:MM:SS.milliseconds
//     else if (dateString.includes("-")) {
//       const [datePart, timePart] = dateString.split(" ");
//       const [year, month, day] = datePart.split("-");
//       const [timeRaw, milliseconds = ""] = timePart.split(".");
//       const [hours = "00", minutes = "00", seconds = "00"] = timeRaw
//         .split(":")
//         .map((t) => t.padStart(2, "0"));

//       const timeString = `${hours}:${minutes}:${seconds}`;
//       date = new Date(
//         `${year}-${month}-${day}T${timeString}${milliseconds ? "." + milliseconds : ""}`
//       );
//     } else {
//       return "-";
//     }

//     if (isNaN(date.getTime())) return "-";

//     const day = String(date.getDate()).padStart(2, "0");
//     const month = String(date.getMonth() + 1).padStart(2, "0");
//     const year = date.getFullYear();
//     const hours = String(date.getHours()).padStart(2, "0");
//     const minutes = String(date.getMinutes()).padStart(2, "0");
//     const seconds = String(date.getSeconds()).padStart(2, "0");

//     return `${day}.${month}.${year} @ ${hours}:${minutes}:${seconds}`;
//   } catch (err) {
//     return "-";
//   }
// }

function formatDate(dateString) {
  if (!dateString) return "-";

  try {
    let date;

    // Format: YYYY/MM/DD HH:MM:SS:ms
    if (dateString.includes("/") && dateString.includes(" ")) {
      const [datePart, timePart] = dateString.split(" ");
      const [year, month, day] = datePart.split("/");

      let timeSegments = timePart.split(":");
      let hours = timeSegments[0]?.padStart(2, "0") || "00";
      let minutes = timeSegments[1]?.padStart(2, "0") || "00";
      let seconds = timeSegments[2]?.padStart(2, "0") || "00";

      if (timeSegments.length === 4) {
        const milliseconds = timeSegments[3];
        date = new Date(
          `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}T${hours}:${minutes}:${seconds}.${milliseconds}`
        );
      } else {
        date = new Date(
          `${year}-${month.padStart(2, "0")}-${day.padStart(2, "0")}T${hours}:${minutes}:${seconds}`
        );
      }
    }

    // Format: YYYY-MM-DD HH:MM:SS.milliseconds
    else if (dateString.includes("-")) {
      const [datePart, timePart] = dateString.split(" ");
      const [year, month, day] = datePart.split("-");
      const [timeRaw, milliseconds = ""] = timePart.split(".");
      const [hours = "00", minutes = "00", seconds = "00"] = timeRaw
        .split(":")
        .map((t) => t.padStart(2, "0"));

      const timeString = `${hours}:${minutes}:${seconds}`;
      date = new Date(
        `${year}-${month}-${day}T${timeString}${milliseconds ? "." + milliseconds : ""}`
      );
    } else {
      return "-";
    }

    if (isNaN(date.getTime())) return "-";

    const day = String(date.getDate()).padStart(2, "0");
    const monthNames = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
    const month = monthNames[date.getMonth()];
    const year = date.getFullYear();

    let hours = date.getHours();
    const minutes = String(date.getMinutes()).padStart(2, "0");
    const ampm = hours >= 12 ? "pm" : "am";
    hours = hours % 12;
    hours = hours ? hours : 12; // 0 should be 12

    return `${day} ${month} ${year}, ${String(hours).padStart(2, "0")}:${minutes} ${ampm}`;
  } catch (err) {
    return "-";
  }
}

function getAssignedToUsers(row, column) {
  try {
    let value = JSON.parse(row[column.td_key].replace(/'/g, '"'));

    if (row.status === 'Completed') {
      return 'Completed';
    }
    if (row.status === 'Request Cancelled') {
      return 'Request Cancelled';
    }

    if (Array.isArray(value) && value.length === 0) {
      return "-";
    }

    return Array.isArray(value) ? `${value.join(", ")}` : `${value}`;
  } catch (error) {
    return row[column.td_key] || "User not assigned";
  }
}


function SelectedAll() {
  allCheck.value = !allCheck.value;
  // console.log("All Check Toggled:", allCheck.value);

  props.tData.forEach((row) => {
    row.isSelected = allCheck.value;
  });
  const selectedData = props.tData.filter((row) => row.isSelected);
  // console.log("Selected Data:", selectedData);
  emits("all-Check", allCheck.value);
}

function selectedCheckList(row, index) {
  const allChecked = props.tData.every((row) => row.isSelected);
  allCheck.value = allChecked;
  const selectedData = props.tData.filter((row) => row.isSelected);
  // console.log("Selected Data:", selectedData);
  emits("checkbox-click", row, index);
}
const filters = ref(
  props.tHeaders.reduce((acc, column) => {
    acc[column.td_key] = ""; // Initialize with empty strings
    return acc;
  }, {})
);
// Handle filter change
// function handleFilterChange() {
//   const activeFilters = Object.fromEntries(
//     Object.entries(filters.value).filter(([key, value]) => value.trim() !== "")
//   );
//   emits("updateFilters", activeFilters); // Emit only non-empty filters
//   // console.log(activeFilters, "========");
// }

function handleFilterChange() {
  const activeFilters = Object.fromEntries(
    Object.entries(filters.value).filter(([key, value]) => value !== "")
  );

  // Format only 'requested_on' differently
  for (const key in activeFilters) {
    const fieldType = props.fieldMapping[key]?.type;

    if (fieldType === "date" && activeFilters[key]) {
      if (key === "requested_on") {
        // Convert to YYYY/M/D format (no leading zeros)
        const [year, month, day] = activeFilters[key].split("-");
        activeFilters[key] = `${year}/${parseInt(month)}/${parseInt(day)}`;
      } else {
        // Keep as YYYY-MM-DD (do nothing)
      }
    }
  }

  emits("updateFilters", activeFilters);
}

watch(
  () => props.tData.map((row) => row.isSelected),
  (newVal) => {
    const allChecked = newVal.every((selected) => selected);
    if (allCheck.value !== allChecked) {
      allCheck.value = allChecked;
    }
  },
  { deep: true }
);

onMounted(() => {
  allCheck.value = false;
});

// function handleFileChange(event) {
//   const file = event.target.files[0];
//   emits("upload-file", file);
// console.log(file.name,'jkgbjd')
// }
function handleCellClick(check, index, type) {
  emits("cell-click", check, index, type);
}
// function formatDate(dateString) {
// 	return moment(dateString).format("DD-MM-YYYY");
// }
// function formatCellContent(content, key) {
//   if (key.includes("date") || key.includes("creation")) {
//     if (content) {
//       return formatDate(content);
//     }
//   }
//   return content;
// }
</script>

<style lang="scss" scoped>
// .fixed-column {
//   position: sticky !important;
//   right: 0 !important;
//   background: white !important;

// }
// .accessible-departments {
//   // max-width: 30%;
//   display: inline-block;
//   overflow: hidden;
//   text-overflow: ellipsis;
//   white-space: nowrap;
//   vertical-align: middle;
// }
// .tooltip-text {
//   position: relative;
//   display: inline-block;
//   cursor: help;
// }

// .tooltip-text::after {
//   content: attr(title);
//   position: absolute;
//   bottom: 100%; /* Show above the element */
//   left: 50%;
//   transform: translateX(-50%);
//   background-color: #333;
//   color: #fff;
//   padding: 4px 8px;
//   border-radius: 4px;
//   white-space: nowrap;
//   font-size: 12px;
//   z-index: 1000;
//   opacity: 0;
//   pointer-events: none;
//   transition: opacity 0.2s ease-in-out;
// }

// .tooltip-text:hover::after {
//   opacity: 1;
// }
.raiseRequest {
  background-color: transparent;
  border-bottom: 1px solid blue;
  font-size: 13px;
  color: blue;
  cursor: pointer;
  font-weight: 300;
}

// .raiseRequest:hover{
//   border-bottom: 1px solid blue;
// }

.form-check-input {
  font-size: 15px;
  margin-top: 5px;
}

.form-switch .form-check-input:checked {
  background-position: right center;
  background-color: #303030;
  border: 0;
}

.actionsdropdown {
  position: absolute !important;
  z-index: 1050;
  /* Ensures it appears above the table */
  left: auto;
  right: 0;
  /* Aligns the dropdown properly */
  min-width: 150px;
  /* Adjust as needed */
  background-color: white;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.activeform {
  font-size: 11px;
  font-weight: 500;
  text-align: left;
  color: #2EC400;
  background-color: #effbeb;
  // border: 0.5px dotted #2EC400; 
  opacity: 0.8;
  padding: 5px 10px;
  border-radius: 6px;
}

.draftForm {
  font-size: 11px;
  font-weight: 500;
  text-align: left;
  color: #ffbb00;
  background-color: #f6f4c9;
  opacity: 0.8;
  padding: 5px 10px;
  border: 1px dotted #ffbb00;
  border-radius: 6px;
}

.spinner-grow {
  width: 13px !important;
  height: 13px !important;
}

// td.accessible-departments {
//   max-width: 30%;
//   width: 30%;
//   overflow: hidden;
// }
td.fixed-column {
  position: relative;
  overflow: visible !important;
}

.global-table {
  width: 100%;
  white-space: nowrap;
  font-size: var(--font-size-xs);
  font-weight: 400;
  // table-layout: fixed;

  td {
    max-width: 100px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: var(--muted) !important;
    font-size: var(--twelve);
  }
}

.dropdown-menu {
  position: absolute;

  li {
    cursor: pointer;
    font-size: 12px;
  }
}

.text-decoration,
.text-decoration1 {
  cursor: pointer;
  transition: all 0.2s;
}

.text-decoration:is(:hover),
.text-decoration1:is(:hover) {
  text-decoration: underline;
  // font-weight: bold;
}

.global-table th,
.global-table td {
  padding: 8px;
  // border-bottom: 1px solid #eeeeee !important;
}

.global-table th {
  background-color: #f2f2f2 !important;
  text-align: left;
  color: #999999;
  font-size: 12px;
}

.global-table thead {
  th {
    position: sticky;
    top: -1px;
  }
}

.global-table tbody tr:hover {
  background-color: #f2f2f2;
}

.actions {
  display: flex;
  align-items: center;
  justify-content: center;
  width: fit-content;
  height: 10px;
  color: black;
  background-color: #f3f3f3;
  font-size: 19px;
  border-radius: 5px;
  padding: 5px 8px !important;
  margin: auto !important;
  cursor: pointer;

  span {
    position: relative;
    bottom: 5px;
    font-size: 22px;
  }
}

.table-responsive {
  height: 77vh;
  overflow: auto;
  overflow-x: unset;

  thead {
    z-index: 1;
  }
}

.completed_files {
  color: #4bcf0c;
}

.error_files {
  color: #4bcf0c;
}

// .file-upload {
//   position: relative;
//   border-radius: 3px;
//   border: none;
//   font-weight: 600;
//   background: none;
//   color: rgb(216, 78, 85);
//   overflow: hidden;
// }

// .file-upload input[type="file"] {
//   position: absolute;
//   left: 0%;
//   top: 0%;
//   opacity: 0;
// }

.column {
  min-width: 10%;
  overflow: hidden;
  text-overflow: ellipsis;
}

// td:not(:first-child),
// th:not(:first-child) {
//   width: 7%;
// }

td:first-child,
th:first-child {
  width: 3%;
}

@media (max-width: 1400px) {
  .table-responsive {
    height: 67vh;
  }

  .global-table td {
    border-bottom: 1px solid var(--border-bottom) !important;
    padding: 4px 10px;
  }
}

@media (min-width: 1401px) and (max-width: 1800px) {
  .table-responsive {
    height: 73vh !important;
  }

  .global-table td {
    border-bottom: 1px solid var(--border-bottom) !important;
    padding: 6px 10px;
  }
}

@media (min-width: 2561px) and (max-width: 2817px) {
  .table-responsive {
    height: 81vh !important;
  }

  .global-table td {
    border-bottom: 1px solid var(--border-bottom) !important;
    padding: 10px 10px;
  }
}

.no-data {
  height: 70vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.checkbox {
  margin-left: 2px;
}

.textcompleted {
  color: green;
}

.textcancel {
  color: #17a2b8;
}

.RequestCancelled {
  color: red;
}

/* Default border style */
.border-none-input {
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
  transition: border 0.3s ease-in-out, border-radius 0.3s ease-in-out;
}
.input-group{
  border: 1px solid #0000005e;
  border-radius: 5px;
  transition: border 0.3s ease-in-out, border-radius 0.3s ease-in-out;
}

/* When input is focused inside input-group */
.input-group:focus-within {
  border: 1px solid #0000005e;
  border-radius: 5px;
  transition: border 0.3s ease-in-out, border-radius 0.3s ease-in-out;
}

/* Search icon wrapper */
.input-group-text {
  border-right: 0px !important;
  height: 26px !important;
  display: flex;
  align-items: center;
  border: none;
  transition: opacity 0.3s ease-in-out;
}

/* When not focused, remove border-left */
.border-left-class {
  border-left: 0px !important;
  transition: border-left 0.3s ease-in-out;
}

/* Input inside input-group */
.input-group input {
  height: 26px !important;
  line-height: 30px;
  border: none;
  /* Default no border */
  outline: none;
  box-shadow: none;
  transition: border-left 0.3s ease-in-out, border-radius 0.3s ease-in-out;
}

/* Apply border-left and border-radius when focused */
.input-group input:focus {
  border-left: 1px solid #0000005e !important;
  border-radius: 5px !important;
  outline: none;
  box-shadow: none;
}

.eye-cursor {
  cursor: pointer;
  font-size: 14px;
}

.view-text {
  font-size: 13px;
  font-weight: 300;
}

.select-filetrs:focus {
  box-shadow: none;
  outline: none;
  border: 1px solid #dee2e6;

}

.fixed-action {
  position: sticky !important;
  right: 0 !important;
  background: white !important;
  // z-index: 1;

}

.linke-not-allow {
  cursor: none;
}

.linked-id-redirect {
  cursor: pointer;
}
.resizable-th {
  resize: horizontal;
  overflow: auto;
  min-width: 100px;
  max-width: 500px;
  white-space: nowrap;
}
.font-responsive {
  font-size: clamp(0.8rem, 1vw + 0.4rem, 1rem);
  // line-height: 1.4;
}

/* Labels slightly smaller */
.font-label {
  font-size: clamp(0.7rem, 0.8vw + 0.3rem, 0.9rem);
  font-weight: 500;
  text-transform: capitalize;
}

/* Icons also scale down a bit */
.card-actions i {
  font-size: clamp(0.9rem, 1vw + 0.3rem, 1.2rem);
  cursor: pointer;
}
</style>
