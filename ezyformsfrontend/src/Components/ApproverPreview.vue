<template>
  <section>
    <div v-if="filteredBlocks.length" class="card">
      <div v-for="(block, blockIndex) in filteredBlocks" :key="blockIndex" class="block-container rounded-2">
        <div v-for="(section, sectionIndex) in block.sections" :key="'preview-' + sectionIndex"
          class="preview-section m-2">
          <div class="section-label">
            <h5 class="m-0 font-13">{{ section.label }}</h5>
          </div>
          <div class="container-fluid">
            <div class="row" v-for="(row, rowIndex) in section.rows" :key="rowIndex">
              <div v-for="(column, columnIndex) in row.columns" :key="'column-preview-' + columnIndex"
                :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'border-0 bg-transparent' : 'border-0 bg-transparent'"
                class="col dynamicColumn">
                <div v-if="column.label" class="p-3 border-bottom">
                  <h6 class="m-0 font-12">{{ column.label }}</h6>
                </div>
                <div class="mx-3 my-2">
                  <div v-for="(field, fieldIndex) in column.fields" :key="'field-preview-' + fieldIndex"
                    :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'd-flex align-items-end mb-2' : ''">
                    <div v-if="field.label">
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
                        }}

                        </span>
                        <span class="pe-2" v-if="props.readonlyFor === 'true' || blockIndex < currentLevel">:</span>
                      </label>
                    </div>
                    <!-- field.fieldtype === 'Select' || -->
                    <!-- Field Type Select or Multiselect -->
                    <template v-if="field.fieldtype === 'multiselect'">
                      <select :multiple="field.fieldtype === 'multiselect'" :value="field.value" @input="
                        logFieldValue(
                          blockIndex,
                          sectionIndex,
                          rowIndex,
                          columnIndex,
                          fieldIndex
                        )
                        " class="form-select mb-2 font-13">
                        <option v-for="(option, index) in field.options?.split('\n')" :key="index" :value="option">
                          {{ option }}
                        </option>
                      </select>
                    </template>

                    <!-- Field Type Check or Radio -->
                    <template v-else-if="
                      field.fieldtype === 'Check' ||

                      field.fieldtype === 'radio'
                    ">
                      <div class="container-fluid">
                        <div class="row">
                          <div class="form-check col-4 mb-1" v-for="(option, index) in field?.options?.split(
                            '\n'
                          )" :key="index">
                            <div>
                              <input v-if="
                                field.fieldtype === 'Check' ||
                                index !== 0
                              " class="form-check-input" type="checkbox" :disabled="blockIndex === 0 || props.readonlyFor === 'true'
                                " :checked="field.value === option" :value="option"
                                :name="`${field.fieldtype}-${blockIndex}-${sectionIndex}-${rowIndex}-${columnIndex}-${fieldIndex}`"
                                :id="`${option}-${index}`" @blur="
                                  (event) =>
                                    logFieldValue(
                                      event,
                                      blockIndex,
                                      sectionIndex,
                                      rowIndex,
                                      columnIndex,
                                      fieldIndex
                                    )
                                " />

                              <input v-else-if="field.fieldtype === 'radio'" :disabled="blockIndex === 0 || props.readonlyFor === 'true'
                                " class="form-check-input" type="radio"
                                :name="`${field.fieldtype}-${blockIndex}-${sectionIndex}-${rowIndex}-${columnIndex}-${fieldIndex}`"
                                :id="`${option}-${index}`" :value="option" :checked="field.value === option" @blur="
                                  (event) =>
                                    logFieldValue(
                                      event,
                                      blockIndex,
                                      sectionIndex,
                                      rowIndex,
                                      columnIndex,
                                      fieldIndex
                                    )
                                " />
                            </div>
                            <div>
                              <label class="form-check-label m-0" :for="`${option}-${index}`">
                                {{ option }}
                              </label>
                            </div>
                          </div>
                        </div>
                      </div>
                    </template>

                    <!-- @click="openInNewWindow(field.value)" -->
                    <template v-else-if="field.fieldtype == 'Attach'">
                      <div v-if="field.value" class="position-relative d-inline-block"
                        :class="props.readonlyFor === 'true' ? 'image-border-bottom' : ''">
                        <img v-if="isImageFile(field.value) || field.value" :src="field.value"
                          class="img-thumbnail mt-2 cursor-pointer border-0" style="max-width: 100px; max-height: 100px"
                          @mouseover="showPreview = true" @mouseleave="showPreview = false" />

                        <!-- Close Icon to Remove Image -->
                        <i class="bi bi-x-lg position-absolute  text-danger cursor-pointer"
                          :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'd-none' : ''" style="
                            top: -10px;
                            right: -5px;
                            font-size: 13px;
                            background: white;
                            border-radius: 50%;
                            padding: 3px;
                          " @click="
                            clearImage(
                              blockIndex,
                              sectionIndex,
                              rowIndex,
                              columnIndex,
                              fieldIndex
                            )
                            "></i>

                        <!-- Pop-up Enlarged Image -->
                        <div v-if="showPreview" class="image-popup position-absolute" style="
                            top: 0;
                            left: 110%;
                            width: 200px;
                            height: auto;
                            z-index: 10;
                            background: white;
                            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.2);
                            border-radius: 5px;
                            padding: 5px;
                          ">
                          <img :src="field.value" alt="Enlarged Preview" style="
                              width: 100%;
                              height: auto;
                              border-radius: 5px;
                            " />
                        </div>
                      </div>

                      <input :disabled="props.readonlyFor === 'true'
                        " v-else type="file" accept="image/jpeg,image/png,application/pdf"
                        :class="props.readonlyFor === 'true' ? 'd-none ' : ' '" :id="'field-' +
                          sectionIndex +
                          '-' +
                          columnIndex +
                          '-' +
                          fieldIndex
                          " class="form-control previewInputHeight font-10" multiple @change="
                            logFieldValue(
                              $event,
                              blockIndex,
                              sectionIndex,
                              rowIndex,
                              columnIndex,
                              fieldIndex
                            )
                            " />
                    </template>

                    <template v-else-if="field.fieldtype == 'Datetime'">
                      <input type="datetime-local" v-model="field.value"
                        :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'border-0 image-border-bottom w-50 pb-0 bg-transparent ' : ' '"
                        :disabled="blockIndex < currentLevel || props.readonlyFor === 'true'" :readOnly="blockIndex < currentLevel || props.readonlyFor === 'true'
                          " :placeholder="'Enter ' + field.label" :name="'field-' +
                            sectionIndex +
                            '-' +
                            columnIndex +
                            '-' +
                            fieldIndex
                            " class="form-control previewInputHeight" />
                    </template>

                    <!-- Field Type Default -->
                    <template v-else>
                      <input v-if="field.fieldtype == 'Int'"
                        :disabled="blockIndex < currentLevel || props.readonlyFor === 'true'" :readOnly="blockIndex < currentLevel || props.readonlyFor === 'true'
                          " type="number" v-model="field.value"
                        :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'border-0 image-border-bottom w-50' : ' '"
                        :placeholder="'Enter ' + field.label" :value="field.value" :name="'field-' +
                          sectionIndex +
                          '-' +
                          columnIndex +
                          '-' +
                          fieldIndex
                          " class="form-control previewInputHeight" />
                      <textarea v-if="field.fieldtype == 'Text'" :disabled="blockIndex < currentLevel"
                        :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'border-0 image-border-bottom bg-transparent ' : ' '"
                        :readOnly="blockIndex === 0 || props.readonlyFor === 'true'
                          " v-model="field.value" :placeholder="'Enter ' + field.label" :value="field.value" :name="'field-' +
                            sectionIndex +
                            '-' +
                            columnIndex +
                            '-' +
                            fieldIndex
                            " class="form-control previewInputHeight"></textarea>
                      <component v-if="field.fieldtype !== 'Int' && field.fieldtype !== 'Text'"
                        :disabled="blockIndex < currentLevel || props.readonlyFor === 'true'"
                        :is="getFieldComponent(field.fieldtype)"
                        :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'border-0 image-border-bottom w-50 bg-transparent ' : ' '"
                        :value="field.value" :type="field.fieldtype" :readOnly="blockIndex < currentLevel || props.readonlyFor === 'true'
                          " :name="'field-' +
                            sectionIndex +
                            '-' +
                            columnIndex +
                            '-' +
                            fieldIndex
                            " @blur="
                              (event) =>
                                logFieldValue(
                                  event,
                                  blockIndex,
                                  sectionIndex,
                                  rowIndex,
                                  columnIndex,
                                  fieldIndex
                                )
                            " class="form-control previewInputHeight"></component>
                    </template>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-if="blockIndex === 0" class="mt-2 mx-2">
          <div v-if="props.childHeaders && Object.keys(props.childHeaders).length" class="mt-2 mx-2">
            <div v-for="(headers, tableName) in props.childHeaders" :key="tableName">
              <div>
                <span class="font-13 fw-bold tablename">{{ tableName.replace(/_/g, " ") }}</span>
              </div>
              <div class="tableborder-child">
                <table class="table mb-0">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th v-for="field in headers" :key="field.fieldname">
                        {{ field.label }}
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(row, index) in props.childData[tableName]" :key="index">
                      <td>{{ index + 1 }}</td>
                      <td v-for="field in headers" :key="field.fieldname">
                        <span v-if="isFilePath(row[field.fieldname])" class="cursor-pointer"
                          @click="openFile(row[field.fieldname])">
                          <span>View Attachment <i class="bi bi-eye-fill ps-1"></i></span>
                        </span>
                        <span v-else>
                          {{ row[field.fieldname] || "-" }}
                        </span>
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
  </section>
</template>

<script setup>
import { computed, defineProps, onMounted, ref, watch } from "vue";
import { apis, domain } from "../shared/apiurls";
import axiosInstance from "../shared/services/interceptor";

const props = defineProps({
  blockArr: {
    type: [Array, null],
    required: true,
  },
  currentLevel: {
    type: String,
    // required: true,
  },
  childHeaders: {
    type: Object,
  },
  childData: {
    type: Object,
  },
  readonlyFor: {
    type: String,
  },
  employeeData: {
    type: Array,
  },
});


const emit = defineEmits();
const filePaths = ref([]);
const tableName = ref("");
const errorMessages = ref({});

const showPreview = ref(false);

const isImageFile = (value) => {
  if (!value) return false;
  return /\.(png|jpg|jpeg|gif)$/i.test(value);
};



// const openInNewWindow = (url) => {
//   window.open(url, '_blank');
// };
// Watch for changes in childData and update tableName
watch(
  () => props.childData,
  (newValue) => {
    if (newValue?.length && newValue[0]?.doctype) {
      tableName.value = newValue[0].doctype.replace(/_/g, " ");
    } else {
      tableName.value = "";
    }
  },
  { immediate: true }
); // Runs immediately in case childData already has a value


const filteredBlocks = computed(() => {

  if (!props.blockArr || props.blockArr.length === 0) return [];

  const filtered = [props.blockArr[0]];

  for (let i = 1; i <= props.currentLevel; i++) {
    if (props.blockArr[i]) {
      filtered.push(props.blockArr[i]);
    }
  }

  // Ensure employeeData is valid
  if (!props.employeeData || props.employeeData.length === 0) {
    console.warn("No employeeData available.");
    return filtered;
  }

  const employee = props.employeeData[0]; // Access first item

  // Create a deep copy before modifying the data
  const updatedBlocks = JSON.parse(JSON.stringify(filtered));

  // Add employeeData values to the last block
  const lastBlock = updatedBlocks[updatedBlocks.length - 1];

  lastBlock.sections?.forEach((section) => {
    section.rows?.forEach((row) => {
      row.columns?.forEach((column) => {
        column.fields?.forEach((field) => {
          if (!props.employeeData || props.readonlyFor === 'true') return;
          if (field.label === "Approver") {
            field.value = employee.emp_name;
            emit("updateField", field);
          }
          if (field.label === "Approved By") {
            if (employee.signature) {

              field.value = employee.signature;
              emit("updateField", field);
            }

            // if (field.value) {
            //   logFieldValue({ target: { value: field.value } }, lastBlock, sectionIndex, rowIndex, columnIndex, fieldIndex);
            // }
          }
          if (field.label === "Approved On") {
            const localTime = new Date().toLocaleString("en-CA", {
              timeZone: "Asia/Kolkata", // Change this to your target timezone
              year: "numeric",
              month: "2-digit",
              day: "2-digit",
              hour: "2-digit",
              minute: "2-digit",
              hour12: false,
            }).replace(/,/, "").replace(/\//g, "-");


            field.value = localTime;
            emit("updateField", field);

            // const now = new Date();

            // // Get local time offset in minutes and convert to milliseconds
            // const offset = now.getTimezoneOffset() * 60000;

            // // Adjust time to local timezone
            // const localTime = new Date(now.getTime() - offset)
            //   .toISOString()
            //   .slice(0, 16); // Format to 'YYYY-MM-DDTHH:mm'
            //   console.log(localTime,"----");

            // field.value = localTime;
            // emit("updateField", field);  
          }

        });
      });
    });
  });

  return updatedBlocks;
});

// Get all fields data
const getAllFieldsData = () => {

  const fieldsData = [];
  filteredBlocks.value.forEach((block) => {
    block.sections?.forEach((section) => {
      section.rows?.forEach((row) => {
        row.columns?.forEach((column) => {
          column.fields?.forEach((field) => {
            fieldsData.push({ ...field });
            if (field.fieldtype === "Attach" && field.value) {
              filePaths.value = field.value
                .split(",")
                .map((path) => path.trim());
            }
          });
        });
      });
    });
  });
  return fieldsData;
};
// const getAllFieldsData = () => {
//     const fieldsData = [];

//     // Iterate through blockArr to extract fields data with null checks
//     props.blockArr?.forEach(block => {
//         block.sections?.forEach(section => {
//             section.rows?.forEach(row => {
//                 row.columns?.forEach(column => {
//                     column.fields?.forEach(field => {
//                         fieldsData.push({ ...field });
//                         if (field.fieldtype === 'Attach' && field.value) {
//                             filePaths.value = field.value.split(',').map(path => path.trim());
//                         }
//                     });
//                 });
//             });
//         });
//     });

//     return fieldsData;
// };

const openFile = (filePath) => {
  const fileUrl = `${filePath}`;
  window.open(fileUrl, "_blank");
};
const isFilePath = (value) => {
  if (!value) return false;
  return /\.(png|jpg|jpeg|gif|pdf|docx|xlsx|txt)$/i.test(value);
};

onMounted(() => {
  emit("updateField", getAllFieldsData());
});

watch(
  () => props.blockArr,
  () => {
    emit("updateField", getAllFieldsData());
  },
  { deep: true }
);

const getFieldComponent = (type) => {
  switch (type) {
    case "Data":
      return "input";
    case "Int":
      return "input";
    case "Text":
      return "textarea";
    case "Time":
      return "input";
    case "Color":
      return "input";
    case "Check":
      return "input";
    case "Select":
      return "input";
    case "Date":
      return "input";
    case "Datetime":
      return "input";
    case "Attach":
      return "file";
    case "radio":
      return "input";
    default:
      return "input";
  }
};

const logFieldValue = (
  eve,
  blockIndex,
  sectionIndex,
  rowIndex,
  columnIndex,
  fieldIndex
) => {
  const field =
    props.blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[
      columnIndex
    ].fields[fieldIndex];

  if (eve.target.files && eve.target.files.length > 0) {
    const files = eve.target.files;
    field["value"] = "";
    for (let i = 0; i < files.length; i++) {
      uploadFile(files[i], field);
    }
    // emit('updateField', field);
  } else if (eve.target.type === "checkbox") {
    if (field.fieldtype === "Check") {
      // Ensure value is a string, not an array
      if (eve.target.checked) {
        // If checked, set the value as a string
        field["value"] = eve.target.value;

      } else {
        // If unchecked, set the value as an empty string (or use any default value)
        field.value = "";
      }
    } else {
      // For other types of fields, store the checkbox checked state as boolean (true/false)
      field["value"] = eve.target.checked;
    }
    // emit('updateField', field);
  } else {
    // field['value'] = eve.target.value;
    let inputValue = eve.target.value;

    // Ensure only numbers are stored and +91 is prefixed
    if (field.fieldtype === "Phone") {
      inputValue = inputValue.replace(/\D/g, ""); // Remove non-numeric characters

      if (inputValue.length > 10) {
        inputValue = inputValue.slice(-10); // Keep only last 10 digits
      }

      inputValue = "+91" + inputValue; // Add +91 prefix
    }

    field["value"] = inputValue;
  }
  validateField(
    field,
    blockIndex,
    sectionIndex,
    rowIndex,
    columnIndex,
    fieldIndex
  );
  emit("updateField", field);
};

const validateField = (
  field,
  blockIndex,
  sectionIndex,
  rowIndex,
  columnIndex,
  fieldIndex
) => {
  const fieldKey = `${blockIndex}-${sectionIndex}-${rowIndex}-${columnIndex}-${fieldIndex}`;

  if (
    field.reqd === 1 &&
    (!field.value || field.value.toString().trim() === "")
  ) {
    errorMessages.value[fieldKey] = `${field.label || "This field"
      } is required.`;
  } else if (field.fieldtype === "Phone") {
    const phoneRegex = /^\+91[0-9]{10}$/; // Accepts +91 followed by exactly 10 digits

    if (!phoneRegex.test(field.value)) {
      errorMessages.value[fieldKey] = "Enter a valid 10-digit phone number.";
    } else {
      delete errorMessages.value[fieldKey]; // Clear error if valid
    }
  } else {
    delete errorMessages.value[fieldKey]; // Clear error if valid
  }
};

const generateRandomNumber = () => {
  return Math.floor(Math.random() * 1000000);
};

const uploadFile = (file, field) => {
  const randomNumber = generateRandomNumber();
  let fileName = `${props.formName}-${randomNumber}-@${file.name}`;

  const formData = new FormData();
  formData.append("file", file, fileName);
  formData.append("is_private", "0");
  formData.append("folder", "Home");
  axiosInstance
    .post(apis.uploadfile, formData)
    .then((res) => {
      console.log(res, res.message.file_url);
      if (res.message && res.message.file_url) {
        if (field["value"]) {
          field["value"] += `, ${res.message.file_url}`;
        } else {
          field["value"] = res.message.file_url;
        }
        emit("updateField", field);
        console.log(field);
      } else {
        console.error("file_url not found in the response.");
      }
    })
    .catch((error) => {
      console.error("Upload error:", error);
    });
};
const clearImage = (
  blockIndex,
  sectionIndex,
  rowIndex,
  columnIndex,
  fieldIndex
) => {
  const field =
    props.blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[
      columnIndex
    ].fields[fieldIndex];
  field.value = ""; // Reset the field value
};

// const logFieldValue = (
//   event,
//   blockIndex,
//   sectionIndex,
//   rowIndex,
//   columnIndex,
//   fieldIndex
// ) => {
//   const field =
//     props.blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[
//       columnIndex
//     ].fields[fieldIndex];
//   field.value = event.target.value;
//   emit("updateField", getAllFieldsData());
//   // console.log('Field Value Updated:', field);
// };
</script>

<style lang="scss" setup scoped>
.image-border-bottom {
  border: none;
  padding-bottom: 0;
  border-radius: 0;
  border-bottom: 1px solid #ccc !important;
}

.previewInputHeight {
  /* height: 35px; */
  margin-bottom: 5px;
  font-size: 12px;
}

.dynamicColumn {
  border: 1px solid #cccccc;
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

.tablename {
  color: #999999;
}

.block-container {
  background-color: #fff;
}

input::-webkit-input-placeholder {
  font-size: 10px;
}

.file-cards {
  transition: all 0.1s ease-in-out;
}

.file-cards:hover {
  box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px,
    rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;
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
  border-radius: 5px !important;
  padding: 0;
  margin: 1px;
}

.cursor-pointer {
  cursor: pointer;
}

.img-thumbnail {
  cursor: pointer;
}
</style>
