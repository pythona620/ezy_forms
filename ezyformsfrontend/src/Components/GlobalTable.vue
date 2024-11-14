<template>
  <div class="table-responsive mb-2">
    <table class="global-table border-0 position-relative" :class="props.class">
      <thead class="position-sticky">
        <tr>
          <!-- <th v-if="isCheckbox == 'true'">
            <input type="checkbox" class="checkbox form-check-input" @change="SelectedAll()" />
          </th> -->
          <th>#</th>
          <th v-for="(column, index) in tHeaders" :key="index" :class="{ 'text-center': column.th === 'Users' }">
            {{ column.th }}
          </th>
          <th class="text-center fixed-column" v-if="isAction == 'true'">Action</th>
        </tr>
      </thead>
      <tbody>
        <template v-if="tData.length">
          <tr v-for="(row, rowIndex) in tData" :key="rowIndex">
            <!-- <td>
              <input type="checkbox" class="form-check-input" v-model="row.isSelected"
                @change="selectedCheckList(row, rowIndex)" />
            </td> -->
            <td class="">{{ rowIndex + 1 }}</td>
            <td v-for="(column, colIndex) in tHeaders" :key="colIndex">
  <!-- Condition for Action Column -->
  <span v-if="column.td_key === 'status'" :class="{
      'text-warning': row[column.td_key] === 'Request Raised',
      'textcompleted': row[column.td_key] === 'Completed',
      'text-primary': row[column.td_key] === 'In Progress',
      'textcancel': row[column.td_key] === 'Cancel',
      'text-danger': row[column.td_key] === 'Rejected',
    }">
    <i class="bi bi-circle-fill status-circle font-10 text-center pe-2"></i>
    {{ row[column.td_key] }}
  </span>

  <!-- Condition for Active Column -->
  <span v-else-if="column.td_key === 'active'" :class="{
      activeform: row[column.td_key] == '1',
      'text-danger': row[column.td_key] == '0',
    }">
    <i class="bi bi-circle-fill status-circle font-10 text-center pe-2"></i>
    {{ row[column.td_key] === 1 ? 'Active' : 'Inactive' }}
  </span>

  <!-- Default Column Rendering -->
  <span v-else>
    {{ row[column.td_key] || '-' }}
  </span>
</td>

            <td v-if="actionType === 'viewPdf'" class="text-center">
              <span>
                <i @click="handleCellClick(row, rowIndex)" class="ri-eye-line eye-cursor"></i>
              </span>
            </td>
            <!-- 'Reviewpending': row[column.td_key] == 'Pending Review',
      'Reviewed': row[column.td_key] == 'Reviewed',
      'Completed': row[column.td_key] == 'Completed',
      'text-danger': row[column.td_key] == 'Error' -->

            <!-- <td :selectedText="text"></td>
          <td :selectedOption="selectoption"></td>
          column.td_key, -->

            <td v-if="actionType === 'dropdown'" class="text-center fixed-column position-relative">
              <div class="dropdown">
                <p class="p-0 actions" data-bs-toggle="dropdown" aria-expanded="false">
                  <span>...</span>
                </p>
                <ul class="dropdown-menu actionsdropdown">
                  <li class="" @click="selectedAction(row, action)" v-for="(action, index) in actions" :key="index">
                    <a class="dropdown-item d-flex gap-2"> <i :class="action.icon"></i>
                      <h1 class="font-10"> {{ action.name }}</h1>
                    </a>
                  </li>
                </ul>
              </div>
            </td>
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
import { defineProps, defineEmits, ref, onMounted, watch } from "vue";
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
  actionType: {
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
});

const emits = defineEmits([
  "actionClicked"
]);


function selectedAction(row, action) {
  emits("actionClicked", row, action);

}
const allCheck = ref(false);

function SelectedAll() {
  allCheck.value = !allCheck.value;
  console.log("All Check Toggled:", allCheck.value);

  props.tData.forEach(row => {
    row.isSelected = allCheck.value;
  });
  const selectedData = props.tData.filter(row => row.isSelected);
  console.log("Selected Data:", selectedData);
  emits("all-Check", allCheck.value);
}

function selectedCheckList(row, index) {
  const allChecked = props.tData.every(row => row.isSelected);
  allCheck.value = allChecked;
  const selectedData = props.tData.filter(row => row.isSelected);
  console.log("Selected Data:", selectedData);
  emits("checkbox-click", row, index);
}

watch(
  () => props.tData.map(row => row.isSelected),
  (newVal) => {
    const allChecked = newVal.every(selected => selected);
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
//   // console.log(file.name,'jkgbjd')
// }
// function handleCellClick(check, index) {
//   emits("cell-click", check, index);
// }
// function formatDate(dateString) {
//   return moment(dateString).format("DD-MM-YYYY");
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
.activeform {
  font-size: 11px;
  font-weight: 400;
  text-align: left;
  color: green;
}

.spinner-grow {
  width: 13px !important;
  height: 13px !important;
}

.global-table {
  width: 100%;
  white-space: nowrap;
  font-size: var(--font-size-xs);
  font-weight: 400;
  // table-layout: fixed;

  td {
    // max-width: 80px;
    // overflow: hidden;
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
  border-bottom: 1px solid var(--border-bottom) !important;
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
.textcompleted{
  color: green ;
}
.textcancel{
  color:#17a2b8 ;
}
</style>
