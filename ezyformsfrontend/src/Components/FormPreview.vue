<template>
  <div class="modal fade" id="formViewModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog modal-xl">
      <div class="modal-content">
        <div class="modal-header py-2 d-block bg-dark text-white">
          <div class="d-flex justify-content-between align-items-center">
            <div>
              <h5 class="m-0 text-white font-13" id="exampleModalLabel">
                Preview -
                {{ props.formDescriptions.form_name || "Untitled" }} ({{
                  props.formDescriptions.form_category
                }})
              </h5>
            </div>
            <div class="d-flex gap-2">
              <!-- Dropdown for selecting approver -->
              <div class="dropdown">
                <button class="btn btn-dark text-white dropdown-toggle font-13" type="button" id="dropdownMenuButton"
                  data-bs-toggle="dropdown" aria-expanded="false">
                  View as {{ selectedView }}
                </button>
                <!-- <ul class="dropdown-menu " aria-labelledby="dropdownMenuButton">
                                    <li><a class="dropdown-item" @click="setView('Requestor')"> Requestor</a></li>
                                    <li><a class="dropdown-item" @click="setView('Approver 1')">Approver 1</a>
                                    </li>
                                    <li><a class="dropdown-item" @click="setView('Approver 2')">Approver 2</a>
                                    </li>
                                    <li><a class="dropdown-item" @click="setView('Approver 3')">Approver 3</a>
                                    </li>
                                </ul> -->
                <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                  <!-- Loop through the blocks and generate the dropdown dynamically -->
                  <li v-for="(blockItem, index) in props.blockArr" :key="index">
                    <a class="dropdown-item" @click="setView(blockItem.label)">
                      {{ blockItem.label }}
                    </a>
                  </li>
                </ul>
              </div>
              <button type="button" class="btn btn-dark text-white font-13" @click="closemodal" data-bs-dismiss="modal">
                Close <i class="bi bi-x"></i>
              </button>
            </div>
          </div>
        </div>

        <div class="modal-body">
          <div class="card border-0">
            <div v-for="(blockItem, blockIndex) in displayedBlocks" :key="blockIndex" class="block-container">
              <div class="d-flex justify-content-end align-items-center">
                <span class="font-12 px-2 py-1" v-if="workFlowRoles[blockIndex]?.roles.length > 0">
                  {{
                    blockIndex === 0
                      ? "Requestor"
                      : `Approver ${blockIndex}
                  `
                  }}: <b>{{ workFlowRoles[blockIndex].roles.join(", ") }}</b>
                </span>
              </div>
              <div v-for="(section, sectionIndex) in blockItem.sections" :key="'preview-' + sectionIndex"
                class="preview-section">
                <div v-if="section.label" class="section-label d-flex justify-content-between">
                  <h5 class="m-0 font-13">{{ section.label }}</h5>
                </div>
                <div class="px-2">
                  <div class="container-fluid">
                    <div class="row" v-for="(row, rowIndex) in section.rows" :key="rowIndex">
                      <div v-for="(column, columnIndex) in row.columns" :key="'column-preview-' + columnIndex"
                        class="col dynamicColumn">
                        <div v-if="column.label" class="p-3 border-bottom">
                          <h6 class="m-0 font-12">{{ column.label || "-" }}</h6>
                        </div>
                        <div class="mx-3 my-2">
                          <div v-for="(field, fieldIndex) in column.fields" :key="'field-preview-' + fieldIndex">
                            <div v-if="field.label && field.fieldtype !== 'Table'" >
                            <div>
                              <label :for="'field-' +
                                sectionIndex +
                                '-' +
                                columnIndex +
                                '-' +
                                fieldIndex
                                ">
                                <span class="font-12">{{ field.label }}</span>
                                <span class="ms-1 text-danger">{{
                                  field.reqd === 1 ? "*" : ""
                                  }}</span>
                              </label>
                              <!-- field.fieldtype == 'Select' || -->
                              <template v-if="field.fieldtype == 'Table MultiSelect'">
                                <select :multiple="field.fieldtype == 'Table MultiSelect'
                                  " v-model="field.value" class="form-select mb-2 font-13">
                                  <option v-for="(option, index
                                  ) in field.options?.split('\n')" :key="index" :value="option">
                                    {{ option }}
                                  </option>
                                </select>
                              </template>
                              <template v-else-if="
                                field.fieldtype == 'Check' ||
                                field.fieldtype == 'radio' ||
                                field.fieldtype == 'Select' || field.fieldtype == 'Small Text'
                              ">
                                <div class="container-fluid">
                                  <div class="row">
                                    <div class="form-check col-4 mb-4" v-for="(
                                      option, index
                                      ) in field?.options?.split('\n')" :key="index"
                                      :class="{ 'd-none': index === 0 }">
                                      <div class="d-flex gap-2 align-items-center">
                                        <div>
                                          <input v-if="
                                            field.fieldtype === 'Check' || field.fieldtype === 'Select' || field.fieldtype == 'Small Text' &&
                                            index !== 0
                                          " class="form-check-input"
                                            :type="field.fieldtype == 'Small Text' ? 'Checkbox' : field.fieldtype"
                                            :name="option" :id="option" readonly />
                                        </div>
                                        <div>
                                          <label class="form-check-label font-12 m-0" :for="option">{{ option }}</label>
                                        </div>
                                      </div>
                                    </div>
                                  </div>
                                </div>
                              </template>
                              <template v-else-if="field.fieldtype == 'Attach'">
                                <input type="file" :id="'field-' +
                                  sectionIndex +
                                  '-' +
                                  columnIndex +
                                  '-' +
                                  fieldIndex
                                  " class="form-control font-10" @change="handleFileChange($event, field)" disabled />
                              </template>
                              <template v-else>
                                <input v-if="field.fieldtype === 'Int'" type="number" v-model="field.value" readonly
                                  class="form-control previewInputHeight font-10" />
                                <input v-if="field.fieldtype === 'Datetime'" type="datetime-local" v-model="field.value"
                                  class="form-control previewInputHeight font-10" />
                                <component v-if="
                                  field.fieldtype !== 'Datetime' &&
                                  field.fieldtype !== 'Int'
                                " readonly :is="getFieldComponent(field.fieldtype)" v-model="field.value"
                                  :type="field.fieldtype" class="form-control previewInputHeight font-10" />
                              </template>
                            </div>
                            <span v-if="field.description !== 'Field'" class="font-11"><span
                                class="fw-semibold">Description: </span>{{
                              field.description }}</span>
                            </div>
                            <div v-if="blockIndex === 0">


                              <div v-for="(table, tableName) in props.childHeaders" :key="tableName">
                                <!-- Table Title -->
                                <div v-if="tableName === field.options"> 
                                <div >
                                  <span class="font-13 fw-bold ps-1 tablename text-secondary">
                                    {{ tableName.toString().replace(/_/g, " ") }}
                                  </span>
                                </div>

                                <!-- Table -->
                                <div class="tableborder-child">
                                  <table class="table mt-2 table-striped">
                                    <thead>
                                      <tr>
                                        <th>#</th>
                                        <th v-for="field in table" :key="field.fieldname">
                                          {{ field.label }}
                                        </th>
                                      </tr>
                                    </thead>
                                    <tbody>
                                      <tr>
                                        <td>{{ '-' }}</td>
                                        <td v-for="(field, index) in table" :key="index">
                                          <span>-</span>
                                        </td>
                                      </tr>
                                    </tbody>
                                  </table>
                                </div>
                                </div>
                              </div>




                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
import { computed, ref, watch } from "vue";

const props = defineProps({
  blockArr: {
    type: [Array, null],
    required: true,
  },

  formDescriptions: {
    type: Object,
    required: false,
  },
  childHeaders: {
    type: Object,
  },

});



const selectedView = ref("All"); // Default to Requestor
const displayedBlocks = ref([]);
const workFlowRoles = ref([]);
// const tableName = ref("");
// // Watch for changes in childData and update tableName
// watch(() => props.childName, (newValue) => {
//   if (newValue?.length && newValue[0]?.doctype) {
//     tableName.value = newValue[0].doctype.replace(/_/g, " ");
//   } else {
//     tableName.value = "";
//   }
// }, { immediate: true }); // Runs immediately in case childData already has a value

// Parse form_json safely
const parsedFormJson = computed(() => {
  try {
    return JSON.parse(props.formDescriptions?.form_json || "{}");
  } catch (error) {
    console.error("Error parsing form_json:", error);
    return {};
  }
});

//  Extract workflow data
const workflowData = computed(() => parsedFormJson.value?.workflow || []);

//  Watch for changes in blockArr or workflow
watch(
  () => [props.blockArr, workflowData.value],
  () => {
    displayedBlocks.value = filterBlocksByFieldname(
      selectedView.value,
      props.blockArr
    );
    updateWorkFlowRoles();
  },
  { immediate: true, deep: true }
);

// Close modal and reset selection
function closemodal() {
  selectedView.value = "All";
}

// Update selected view
function setView(view) {
  if (!view) return;
  selectedView.value = view;
  displayedBlocks.value = filterBlocksByFieldname(view, props.blockArr);
  updateWorkFlowRoles();
}
function updateWorkFlowRoles() {
  let approverIndex = 0; // Keep track of approvers

  workFlowRoles.value = displayedBlocks.value.map((block) => {
    let roles = [];

    if (block.fieldname === "requestor") {
      // ✅ Find requestor roles
      const requestorWorkflow = workflowData.value.find(wf => wf.type === "requestor");
      roles = requestorWorkflow ? requestorWorkflow.roles : [];
    } else if (block.label.startsWith("approver-")) {
      // ✅ Get all approvers
      const approverWorkflow = workflowData.value.filter(wf => wf.type === "approver");

      // ✅ Assign correct role (removes `-1` mistake)
      if (approverWorkflow[approverIndex]) {
        roles = approverWorkflow[approverIndex].roles || [];
      }

      approverIndex++; // Move to the next approver
    }

    return { roles };
  });
}


//  Filter blocks based on the view
function filterBlocksByFieldname(view, blocks) {
  if (!blocks || !Array.isArray(blocks)) return []; // Ensure `blocks` is valid
  if (view === 'All') {
    return blocks; // Show all blocks
  }

  const blockOrder = {
    requestor: ["requestor"],
    "approver-1": ["requestor", "approver-1"],
    "approver-2": ["requestor", "approver-1", "approver-2"],
    "approver-3": ["requestor", "approver-1", "approver-2", "approver-3"],
    "approver-4": [
      "requestor",
      "approver-1",
      "approver-2",
      "approver-3",
      "approver-4",
    ],
    "approver-5": [
      "requestor",
      "approver-1",
      "approver-2",
      "approver-3",
      "approver-4",
      "approver-5",
    ],
    "approver-6": [
      "requestor",
      "approver-1",
      "approver-2",
      "approver-3",
      "approver-4",
      "approver-5",
      "approver-6",
    ],
    "approver-7": [
      "requestor",
      "approver-1",
      "approver-2",
      "approver-3",
      "approver-4",
      "approver-5",
      "approver-6",
      "approver-7",
    ],
    "approver-8": [
      "requestor",
      "approver-1",
      "approver-2",
      "approver-3",
      "approver-4",
      "approver-5",
      "approver-6",
      "approver-7",
      "approver-8",
    ],
  };

  const viewOrder = blockOrder[view] ?? ["requestor"];

  return viewOrder
    .map((type) => blocks?.find((b) => b?.label === type)) // Use optional chaining
    .filter(Boolean); // Remove null values
}
// watch(
//     () => props.blockArr,
//     (newVal) => {
//         if (newVal && Array.isArray(newVal)) {
//             // console.log(props.blockArr, "gggggggggggg");
//             // Set the default display block as Requestor
//             displayedBlocks.value = filterBlocksByFieldname('Requestor', newVal);
//             // console.log(displayedBlocks.value, "displayedBlocks");
//         }
//     },
//     { immediate: true }
// );

// function closemodal() {
//     selectedView.value = 'Requestor'
//     // props.blockArr = []
// }
// function setView(view) {
//     selectedView.value = view;

//     displayedBlocks.value = filterBlocksByFieldname(view, props.blockArr);
// }

// function filterBlocksByFieldname(view, blocks) {

//     let filteredBlocks = [];

//     // Define the block order for each view
//     // const blockOrder = {
//     //     'requestor': ['requestor'],
//     //     'approver-1': ['requestor', 'approver1'],
//     //     'approver-2': ['requestor', 'approver1', 'approver2'],
//     //     'approver-3': ['requestor', 'approver1', 'approver2', 'approver3']
//     // };
//     const blockOrder = {
//         'requestor': ['requestor'],
//         'approver-1': ['requestor', 'approver-1'],
//         'approver-2': ['requestor', 'approver-1', 'approver-2'],
//         'approver-3': ['requestor', 'approver-1', 'approver-2', 'approver-3'],
//         'approver-4': ['requestor', 'approver-1', 'approver-2', 'approver-3', 'approver-4'],
//         'approver-5': ['requestor', 'approver-1', 'approver-2', 'approver-3', 'approver-4', 'approver-5'],
//         'approver-6': ['requestor', 'approver-1', 'approver-2', 'approver-3', 'approver-4', 'approver-5', 'approver-6'],
//         'approver-7': ['requestor', 'approver-1', 'approver-2', 'approver-3', 'approver-4', 'approver-5', 'approver-6', 'approver-7'],
//         'approver-8': ['requestor', 'approver-1', 'approver-2', 'approver-3', 'approver-4', 'approver-5', 'approver-6', 'approver-7', 'approver-8']
//     };

//     // Get the fieldnames for the selected view from blockOrder
//     const viewOrder = blockOrder[view] || ['requestor'];

//     // Iterate through the fieldnames and push matching blocks into filteredBlocks
//     viewOrder.forEach(type => {
//         const block = blocks.find(b => b.label === type);

//         if (block) {
//             filteredBlocks.push(block); // Add the block if it exists
//         }
//     });

//     return filteredBlocks;
// }

const getFieldComponent = (type) => {
  switch (type) {
    case "Data":
    case "Phone":
    case "Check":
    case "Date":
    case "Int":
    case "Datetime":
    case "radio":
      return "input";
    case "Text":
      return "textarea";
    case "Time":
      return "input";
    case "Select":
      return "select";
    case "Table MultiSelect":
      return "select";
    case "Attach":
      return "file";
    case "Color":
      return "input";
  }
};
</script>


<style scoped>
.previewInputHeight {
  /* height: 35px; */
  margin-bottom: 5px;
}

.dynamicColumn {
  border: 1px dotted #cccccc;
  border-radius: 7px;
  margin: 3px 3px 10px 3px;
  background-color: #ffffff;
  padding: 0;
  padding-bottom: 5px;
}

.section-label {
  padding: 10px 14px;
}

.description-div {
  padding: 0px 3px;
}

.blockName {
  box-shadow: 0px 4px 4px 0px #0000000d;
  padding: 18px 12px;
  font-weight: 500;
  font-size: 15px;
}

.block-container {
  /* background-color: #f9f9f9; */
  /* border-radius: 10px; */
  /* border: 1px solid #cccccc; */
  /* margin-top: 10px;
    margin-bottom: 10px; */
  /* background-color: #fafafa; */
  background-color: #f5f5f5;
}

.modal-body {
  overflow-y: scroll;
  overflow-x: hidden;
  height: 70vh;
}

input::-webkit-input-placeholder {
  font-size: 10px;
}

.accordion-button:focus {
  box-shadow: None;
}

.accordion-button {
  background-color: #fff;
  font-size: 14px;
  font-weight: 500;
}

.accordion-button:not(.collapsed) {
  background-color: #fff;
  color: #000;
  box-shadow: None;
}

table {
  border-collapse: collapse;
  background-color: #000;
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

.tableborder-child {
  border: 1px solid #ccc !important;
  border-radius: 10px !important;
  padding: 0;
  margin: 1px;
}
</style>