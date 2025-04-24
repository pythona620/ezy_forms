<template>
  <div class="table-responsive mb-2">
    <table class="global-table border-0 position-relative" :class="props.class">
      <thead class="position-sticky">
        <tr>
          <!-- <th v-if="isCheckbox == 'true'">
						<input type="checkbox" class="checkbox form-check-input" @change="SelectedAll()" />
					</th> -->
          <th>#</th>
          <th v-for="(column, index) in tHeaders" :key="index"
            :class="{ 'text-center': column.th === 'Users' || column.th === 'Status' || column.th === 'Enable/Disable' }">
            {{ column.th }}
          </th>
          <!-- <th class="text-center fixed-column" v-if="enableDisable == 'true'">Enable/Disable</th> -->
          <th class="text-center fixed-column" v-if="isAction == 'true'">Action</th>
        </tr>
      </thead>
      <tbody>
        <tr class="mb-1" v-if="isFiltersoption == 'true'">
          <td></td>

          <td class="p-1" v-for="(column, index) in tHeaders" :key="index">
            <template v-if="fieldMapping[column.td_key]">
              <!-- Text input -->
              <div v-if="fieldMapping[column.td_key].type === 'input'" class="input-group border-none-input">
                <span v-show="!focusedFields[column.td_key]" class="input-group-text font-12" id="basic-addon1">
                  <i class="bi bi-search"></i>
                </span>
                <input type="search" aria-describedby="basic-addon1"
                  class="form-control font-12 py-1 px-2  border-0  input-search" v-model="filters[column.td_key]"
                  @input="handleFilterChange" :class="{ 'border-left-class ': focusedFields[column.td_key] }"
                  @focus="focusedFields[column.td_key] = true" @blur="focusedFields[column.td_key] = false" />
              </div>

              <!-- Date input -->
              <input v-else-if="fieldMapping[column.td_key].type === 'date'" type="date"
                class="form-control font-12 input-search py-1 px-2" v-model="filters[column.td_key]"
                @input="handleFilterChange" />

              <!-- Select dropdown -->
              <select v-else-if="fieldMapping[column.td_key].type === 'select'"
                class="form-control form-select input-search font-12 select-filetrs py-1 px-2 w-100"
                v-model="filters[column.td_key]" @change="handleFilterChange">
                <option class="font-12" value="">All</option>
                <option class="font-12" v-for="(option, optionIndex) in fieldMapping[column.td_key].options"
                  :key="optionIndex" :value="option">
                  {{ option }}
                </option>
              </select>
            </template>

            <!-- Empty TD -->
            <template v-else>
              <span></span>
            </template>
          </td>
          <!-- <td class="text-center fixed-column" v-if="enableDisable == 'true'"></td> -->
          <td class="text-center fixed-column" v-if="isAction == 'true'"></td>
        </tr>
        <template v-if="tData.length">
          <tr v-for="(row, rowIndex) in tData" :key="rowIndex">
            <!-- <td>
							<input type="checkbox" class="form-check-input" v-model="row.isSelected"
								@change="selectedCheckList(row, rowIndex)" />
						</td> -->
            <td class="">{{ rowIndex + 1 }}</td>
            <td :title="row[column.td_key] ? row[column.td_key].toString() : '-'" v-for="(column, colIndex) in tHeaders"
              :class="column.td_key === 'form_status' ? 'text-center' : ''" :key="colIndex">

              <!-- <span :class="{'accessible-departments': column.td_key === 'accessible_departments'}" v-if="column.td_key === 'accessible_departments'">
                
              </span> -->
              <!-- Condition for Action Column -->
              <span v-if="column.td_key === 'status'">
                <i class="bi bi-circle-fill status-circle font-10 text-center pe-2" :class="{
                  'text-warning fw-medium': row[column.td_key] === 'Request Raised',
                  'textcompleted fw-medium': row[column.td_key] === 'Completed',
                  'text-primary fw-medium': row[column.td_key] === 'In Progress',
                  'textcancel fw-medium': row[column.td_key] === 'Cancelled',
                  'text-danger fw-medium': row[column.td_key] === 'Request Cancelled',
                }"></i>
                {{ row[column.td_key]
                }}<span v-if="row.current_level !== undefined && row.total_levels !== undefined">
                  ({{ row.current_level }} / {{ row.total_levels }})
                </span>
              </span>

              <!-- Condition for Active Column -->
              <span v-else-if="column.td_key === 'active'" :class="{
                activeform: row[column.td_key] == '1',
                'text-danger': row[column.td_key] == '0',
              }">
                <i class="bi bi-circle-fill status-circle font-10 text-center pe-2"></i>
                {{ row[column.td_key] === 1 ? "Active" : "In active" }}
              </span>

              <span v-else-if="column.td_key === 'form_status'" :class="{
                activeform: row[column.td_key] == 'Created',
                draftForm: row[column.td_key] == 'Draft',
              }">
                <i class="bi bi-circle-fill status-circle font-10 text-center pe-2"></i>
                {{ row[column.td_key] === 'Created' ? 'Active' : 'Retired' }}
              </span>
              <!-- Default Column Rendering -->
              <span v-else-if="
                column.td_key === 'requested_on' || column.td_key === 'invoice_date'">
                {{ formatDate(row[column.td_key]) }}
              </span>

              <!-- Show unformatted date for 'modified' when status === 'Request Raised' -->
              <span
  v-else-if="column.td_key === 'modified' && row.status !== 'Request Raised'"
>
  {{ formatDate(row[column.td_key]) }}
</span>
              <span v-else-if="column.td_key === 'signature'">
                <div v-if="row[column.td_key]">
                  <i class="bi bi-check2 fw-bolder font-13 text-success"></i>
                  <!-- <img :src="row[column.td_key]" alt="Signature" class="img-fluid"> -->
                </div>
                <span v-else>
                  <i class="bi bi-x-lg fw-bolder text-danger"></i>
                </span>
              </span>
              <span v-else-if="column.td_key === 'assigned_to_users'">
                <div>
                  <span>
                    {{
                      (() => {
                        try {
                          let value = JSON.parse(row[column.td_key].replace(/'/g, '"')); // Replace single quotes & parse

                          // If status is 'Completed', return 'Completed'
                          if (row.status === 'Completed') {
                            return 'Completed';
                          }
                          if (row.status === 'Request Cancelled') {
                            return 'Request Cancelled';
                          }

                          // If value is an empty array, return "-"
                          if (Array.isArray(value) && value.length === 0) {
                            return "-";
                          }

                          return Array.isArray(value) ? `Pending at- ${value.join(", ")}` : `Pending at- ${value}`;
                        } catch (error) {
                          return row[column.td_key] || "User not assigned"; // Fallback if parsing fails
                        }
                      })()
                    }}
                  </span>
                </div>
              </span>
              <span class="text-center fixed-column" v-else-if="column.td_key === 'enable'">
                <div class="d-flex justify-content-center align-items-center gap-2">
                  <span :class="row.enable == 0 ? 'text-secondary font-11' : ''">
                    {{ row.enable == '1' ? '' : 'Disabled' }}
                  </span>
                  <div class="form-check d-flex justify-content-center form-switch text-end">
                    <input class="form-check-input shadow-none" type="checkbox" role="switch"
                      :checked="row.enable == '0'" @click.prevent="handleToggle(row, index, $event)" />
                  </div>
                </div>
              </span>


              <!-- <span v-else-if="column.td_key === 'total_levels'">
                {{ row[column.td_key] }}
              </span> -->
              <!-- v-tooltip.top="row[column.td_key]" -->
              <!-- <span v-else>
                {{ row[column.td_key].replace(/_/g, " ") || "-" }}
              </span> -->
              <span v-else>
                {{ column.td_key === 'modified' ? '-' :  row[column.td_key]?.replace(/@[\w.-]+/, "") || "-" }}
              </span>
            </td>
            <!-- <td
              class="text-center d-flex justify-content-center position-relative"
              v-if="isAction == 'true' && viewType === 'viewPdf'"
            > -->

            <!-- 'Reviewpending': row[column.td_key] == 'Pending Review',
                'Reviewed': row[column.td_key] == 'Reviewed',
                'Completed': row[column.td_key] == 'Completed',
                'text-danger': row[column.td_key] == 'Error' -->

            <!-- <td :selectedText="text"></td>
                    <td :selectedOption="selectoption"></td>
                    column.td_key, -->

            <!-- <td class="text-center fixed-column" v-if="enableDisable === 'true'">
              <div class="d-flex justify-content-center align-items-center gap-2">
                <span :class="row.enable == 0 ? 'text-secondary font-11' : ''">
                  {{ row.enable == '1' ? '' : 'Disabled' }}
                </span>
                <div class="form-check d-flex justify-content-center form-switch text-end">
                  <input class="form-check-input shadow-none" type="checkbox" role="switch" :checked="row.enable == '0'"
                    @click.prevent="handleToggle(row, index, $event)" />
                </div>
              </div>
            </td> -->
            <div v-if="isAction == 'true' && viewType === 'viewPdf'" class="text-center">
              <span class="px-2">
                <i @click="handleCellClick(row, rowIndex, 'view')" class="ri-eye-line eye-cursor"></i>
              </span>
              <span v-if="download === 'true'">
                <i class="bi bi-download eye-cursor" @click="handleCellClick(row, rowIndex, 'download')"></i>
              </span>
              <span v-if="raiseRequest === 'true'">
                <i class="bi bi-send eye-cursor mx-1" @click="handleCellClick(row, rowIndex, 'raiseRequest')"></i>
              </span>
            </div>
            <td v-if="actionType === 'dropdown'" class="text-center fixed-column position-relative">
              <div class="dropdown">
                <p class="p-0 actions" data-bs-toggle="dropdown" aria-expanded="false">
                  <span>...</span>
                </p>
                <ul class="dropdown-menu actionsdropdown">
                  <li class="py-1" @click="selectedAction(row, action)" v-for="(action, index) in actions" :key="index">
                    <a class="dropdown-item py-2 d-flex align-items-center gap-2">
                      <i :class="action.icon"></i>
                      <h1 class="font-10 mb-0">{{ action.name }}</h1>
                    </a>
                  </li>
                </ul>
              </div>
            </td>



            <!-- <td v-if="actionType === 'Toogle&dropdown'"
              class="text-end d-flex justify-content-end align-items-center fixed-column position-relative">
            </td>
              <td
                v-if="actionType === 'dropdown'"
                class="fixed-column position-relative"
              >
                <div class="dropdown">
                  <p class="p-0 actions" data-bs-toggle="dropdown" aria-expanded="false">
                    <span>...</span>
                  </p>
                  <ul class="dropdown-menu actionsdropdown">
                    <li
                      class="py-1"
                      @click="selectedAction(row, action)"
                      v-for="(action, index) in actions"
                      :key="index"
                    >
                      <a class="dropdown-item py-2 d-flex align-items-center gap-2">
                        <i :class="action.icon"></i>
                        <h1 class="font-10 mb-0">{{ action.name }}</h1>
                      </a>
                    </li>
                  </ul>
                </div>
              </td>
            <td v-if="actionType === 'Toogle&dropdown' " 
              class="text-end d-flex p-0 justify-content-center align-items-center gap-2 fixed-column ">
              <div class="dropdown">
                <p class="p-0 actions" data-bs-toggle="dropdown" aria-expanded="false">
                  <span>...</span>
                </p>
                <ul class="dropdown-menu actionsdropdown">
                  <li class="py-1" @click="selectedAction(row, action)" v-for="(action, index) in actions" :key="index">
                    <a class="dropdown-item py-2 d-flex align-items-center gap-2">
                      <i :class="action.icon"></i>
                      <h1 class="font-10 mb-0">{{ action.name }}</h1>
                    </a>
                  </li>
                </ul>
              </div>


            </td> -->
            <!-- <div  class="form-check d-flex justify-content-end form-switch text-end ">
                <input class="form-check-input shadow-none" type="checkbox" role="switch" :checked="row.enable == '1'"
                  @click.prevent="handleToggle(row, index, $event)" />
              </div> -->
            <!-- </td> -->



            <!-- <td
						v-if="actionType === 'Modal'"
						class="text-center d-flex justify-content-center"
					>
						<button
							type="button"
							@change="handleFileChange"
							class="file-upload d-flex gap-2 text-center"
						>
							<i class="bi bi-upload"></i>Upload<input type="file" />
						</button>
					</td> -->
            <!-- <td v-if="actionType === 'download'" class="text-center">
						<button>Download report</button>
					</td> -->
            <!-- <td v-if="actionType === 'right-icon'" class="text-center">
						<ButtonComp
							class="bg-transparent"
							icon="chevron-right"
						></ButtonComp>
					</td> -->
          </tr>
        </template>
        <template v-else>
          <tr>
            <td colspan="100%" class="text-center">No Data Found</td>
          </tr>
        </template>
      </tbody>
    </table>
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
  // class: {
  //   type: String,
  //   required: true,
  // },
  isAction: {
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

const emits = defineEmits(["actionClicked", "updateFilters", "cell-click", "toggle-click"]);

function selectedAction(row, action) {
  emits("actionClicked", row, action);
  // console.log(row, action);
}


function handleToggle(row, index, event) {
  // Emit the custom event. The parent component will handle showing the confirmation.
  emits("toggle-click", row, index, event);
  // console.log("event", event);
}
const focusedFields = reactive({});


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
function formatDate(dateString) {
  if (!dateString) return "-";

  try {
    let date;

    // Format: YYYY/MM/DD HH:MM:SS:ms (colon-separated with optional ms)
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
    const month = String(date.getMonth() + 1).padStart(2, "0");
    const year = date.getFullYear();
    const hours = String(date.getHours()).padStart(2, "0");
    const minutes = String(date.getMinutes()).padStart(2, "0");
    const seconds = String(date.getSeconds()).padStart(2, "0");

    return `${day}.${month}.${year} @ ${hours}:${minutes}:${seconds}`;
  } catch (err) {
    return "-";
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
function handleFilterChange() {
  const activeFilters = Object.fromEntries(
    Object.entries(filters.value).filter(([key, value]) => value.trim() !== "")
  );
  emits("updateFilters", activeFilters); // Emit only non-empty filters
  // console.log(activeFilters, "========");
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

<style lang="scss">
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
  border: 0.5px dotted #2EC400;
  opacity: 0.8;
  padding: 5px 10px;
  border-radius: 6px;
}
.draftForm{
  font-size: 11px;
  font-weight: 500;
  text-align: left;
  color: #ffbb00;
  background-color: #f6f4c9;
  opacity: 0.8;
  padding: 5px 10px;
  border:1px dotted #ffbb00; 
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

/* Default border style */
.border-none-input {
  border: 1px solid #dee2e6;
  border-radius: 0.375rem;
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
}

.select-filetrs:focus {
  box-shadow: none;
  outline: none;
  border: 1px solid #dee2e6;

}
</style>
