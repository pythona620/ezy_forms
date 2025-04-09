<template>
    <section>
        <div v-if="blockArr" class="card">
            <div v-for="(block, blockIndex) in blockArr" :key="blockIndex" class="block-container">


                <div v-for="(section, sectionIndex) in block.sections" :key="'preview-' + sectionIndex"
                    class="preview-section m-2">
                    <div class="section-label">
                        <h5 class="m-0 font-13">{{ section.label }}</h5>
                    </div>
                    <div class="container-fluid">
                        <div class="row" v-for="(row, rowIndex) in section.rows" :key="rowIndex">
                            <div v-for="(column, columnIndex) in row.columns" :key="'column-preview-' + columnIndex"
                                class="col dynamicColumn">
                                <div v-if="column.label" class="p-3 border-bottom">
                                    <h6 class="m-0 font-12">{{ column.label }}</h6>
                                </div>
                                <div class="mx-3 my-2">
                                    <div v-for="(field, fieldIndex) in column.fields"
                                        :key="'field-preview-' + fieldIndex">
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
                                                }}</span>
                                            </label>
                                        </div>

                                        <template v-if="
                                            field.fieldtype === 'Select' ||
                                            field.fieldtype === 'Table MultiSelect'
                                        ">
                                            <select :multiple="field.fieldtype === 'Table MultiSelect'"
                                                :value="field.value" @change="
                                                    (event) =>
                                                        logFieldValue(
                                                            event,
                                                            blockIndex,
                                                            sectionIndex,
                                                            rowIndex,
                                                            columnIndex,
                                                            fieldIndex
                                                        )
                                                " class="form-select mb-2 font-13">
                                                <option v-for="(option, index) in field.options?.split('\n')"
                                                    :key="index" :value="option">
                                                    {{ option }}
                                                </option>
                                            </select>
                                        </template>

                                        <template v-else-if="
                                            field.fieldtype === 'Check' ||
                                            field.fieldtype === 'radio' || field.fieldtype === 'Small Text'
                                        ">
                                            <div class="container-fluid">
                                                <div class="row">
                                                    <div class="form-check col-4 mb-4"  v-for="(option, index) in field?.options?.split(
                                                        '\n'
                                                    )" :key="index" :class="{ 'd-none': index === 0 }">
                                                        <div>
                                                            <input v-if="
                                                                field.fieldtype === 'Check' || field.fieldtype === 'Small Text' && index !== 0
                                                            " class="form-check-input" type="checkbox" :value="option"
                                                                :name="`${field.fieldtype}-${blockIndex}-${sectionIndex}-${rowIndex}-${columnIndex}-${fieldIndex}`"
                                                                :id="`${option}-${index}`"
                                                                :checked="field.value === option" @change="
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

                                                            <input v-else-if="field.fieldtype === 'radio'"
                                                                class="form-check-input" type="radio"
                                                                :name="`${field.fieldtype}-${blockIndex}-${sectionIndex}-${rowIndex}-${columnIndex}-${fieldIndex}`"
                                                                :id="`${option}-${index}`" :value="field.value" @change="
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
                                                            <label class="form-check-label font-12 m-0"
                                                                :for="`${option}-${index}`">
                                                                {{ option }}
                                                            </label>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </template>

                                        <template v-else-if="field.fieldtype == 'Attach'">
                                            <input
    :disabled="props.readonlyFor === 'true'"
    type="file"
    accept="image/jpeg,image/png,application/pdf"
    :id="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex"
    class="form-control previewInputHeight font-10 mt-2"
    multiple
    @change="
      logFieldValue(
        $event,
        blockIndex,
        sectionIndex,
        rowIndex,
        columnIndex,
        fieldIndex
      )
    "
  />
  <div v-if="field.value" class="d-flex flex-wrap gap-2">
    <div
      v-for="(fileUrl, index) in field.value.split(',').map(f => f.trim())"
      :key="index"
      class="position-relative d-inline-block"
      @mouseover="hovered = index"
      @mouseleave="hovered = null"
    >
      <!-- Show image thumbnail -->
      <img
        v-if="isImageFile(fileUrl)"
        :src="fileUrl"
        class="img-thumbnail mt-2 cursor-pointer border-0"
        style="max-width: 100px; max-height: 100px"
      />

      <!-- Show PDF icon if not image -->
      <div
        v-else
        class="d-flex align-items-center justify-content-center border mt-2"
        style="width: 100px; height: 100px; background: #f9f9f9"
      >
        <i class="bi bi-file-earmark-pdf fs-1 text-danger"></i>
      </div>

      <!-- Remove icon -->
      <button
        v-if="hovered === index"
        @click="removeFile(index, field)"
        class="btn btn-sm btn-light position-absolute"
        style="top: 2px; right: 5px; border-radius: 50%; padding: 0 5px"
      >
        <i class="bi bi-x fs-6"></i>
      </button>
    </div>
  </div>

  <!-- File input for uploading -->

</template>

                                        <template v-else-if="field.fieldtype == 'Datetime'">
                                            <input type="datetime-local" :value="field.value" @click="forceOpenCalendar"
                                                ref="datetimeInput" :placeholder="'Enter ' + field.label" :name="'field-' +
                                                    sectionIndex +
                                                    '-' +
                                                    columnIndex +
                                                    '-' +
                                                    fieldIndex
                                                    " @change="
                                                        (event) =>
                                                            logFieldValue(
                                                                event,
                                                                blockIndex,
                                                                sectionIndex,
                                                                rowIndex,
                                                                columnIndex,
                                                                fieldIndex
                                                            )
                                                    " class="form-control previewInputHeight font-10" />
                                        </template>

                                        <template v-else>
                                            <input v-if="field.fieldtype === 'Datetime'" type="datetime-local"
                                                @click="forceOpenCalendar" ref="datetimeInput" :value="field.value"
                                                class="form-control previewInputHeight font-10" />
                                            <!-- <input v-if="field.fieldtype === 'Date'" type="date" :value="field.value"
                                                class="form-control previewInputHeight font-10" /> -->
                                            <!-- <input v-if="field.fieldtype == 'Int'" type="number"
                                                :placeholder="'Enter ' + field.label" :value="field.value" :name="'field-' +
                                                    sectionIndex +
                                                    '-' +
                                                    columnIndex +
                                                    '-' +
                                                    fieldIndex
                                                    " class="form-control previewInputHeight" /> -->
                                            <!-- :value="field.value"  -->
                                            <textarea v-if="field.fieldtype == 'Text'" @change="
                                                (event) =>
                                                    logFieldValue(
                                                        event,
                                                        blockIndex,
                                                        sectionIndex,
                                                        rowIndex,
                                                        columnIndex,
                                                        fieldIndex
                                                    )
                                            " v-model="field.value" :placeholder="'Enter ' + field.label" :name="'field-' +
                                                sectionIndex +
                                                '-' +
                                                columnIndex +
                                                '-' +
                                                fieldIndex
                                                " class="form-control previewInputHeight"></textarea>
                                            <component v-if="
                                                field.fieldtype !== 'Datetime' && field.fieldtype !== 'Text'
                                            " :is="getFieldComponent(field.fieldtype)" :value="field.value"
                                                :maxlength="field.fieldtype === 'Phone' ? '10' : null" :Type="field.fieldtype === 'Color'
                                                    ? 'color'
                                                    : field.fieldtype === 'Int'
                                                        ? 'number'
                                                        : field.fieldtype" :name="'field-' +
                                                            sectionIndex +
                                                            '-' +
                                                            columnIndex +
                                                            '-' +
                                                            fieldIndex
                                                            " @change="
                                                                (event) =>
                                                                    logFieldValue(
                                                                        event,
                                                                        blockIndex,
                                                                        sectionIndex,
                                                                        rowIndex,
                                                                        columnIndex,
                                                                        fieldIndex
                                                                    )
                                                            " class="form-control previewInputHeight font-10">
                                            </component>
                                        </template>
                                        <div v-if="
                                            errorMessages[
                                            `${blockIndex}-${sectionIndex}-${rowIndex}-${columnIndex}-${fieldIndex}`
                                            ]
                                        " class="text-danger font-10 mt-1">
                                            {{
                                                errorMessages[
                                                `${blockIndex}-${sectionIndex}-${rowIndex}-${columnIndex}-${fieldIndex}`
                                                ]
                                            }}
                                        </div>
                                    </div>
                                </div>
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
// import moment from "moment";
import axiosInstance from "../shared/services/interceptor";
import { apis } from "../shared/apiurls";

const props = defineProps({
    blockArr: {
        type: [Array, null],
        required: true,
    },
    formName: {
        type: String,
        required: true,
    },
});


const getCurrentDateTime = () => {
    const localTime = new Date().toLocaleString("en-CA", {
        timeZone: "Asia/Kolkata", // Change this to your target timezone
        year: "numeric",
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
    }).replace(/,/, "").replace(/\//g, "-");
    return localTime;
    // Adjust format as needed
};

// Function to update Datetime fields
const updateDateTimeFields = () => {
    if (props.blockArr) {
        props.blockArr.forEach((block) => {
            block.sections.forEach((section) => {
                section.rows.forEach((row) => {
                    row.columns.forEach((column) => {
                        column.fields.forEach((field) => {
                            if (field.fieldtype === "Datetime" && !field.value) {
                                field.value = getCurrentDateTime();
                                emit("updateField", field);
                            }
                            if (field.fieldtype === "Date" && !field.value) {
                                field.value = new Date().toISOString().split('T')[0]; // Ensure format is YYYY-MM-DD
                                // console.log("Setting field.value:", field.value); // Debugging log
                                emit("updateField", field);
                            }

                        });
                    });
                });
            });
        });
    }
};

// Initialize datetime fields on component mount
onMounted(() => {
    const storedData = localStorage.getItem("employeeData");
    let parsedData = [];
    if (storedData) {
        try {
            parsedData = JSON.parse(storedData) || [];
        } catch (error) {
            console.error("Error parsing employeeData from localStorage:", error);
        }
    }
    updateDateTimeFields();


    if (props.blockArr) {
        props.blockArr.forEach((block) => {
            block.sections.forEach((section) => {
                section.rows.forEach((row) => {
                    row.columns.forEach((column) => {
                        column.fields.forEach((field) => {
                            if (field.fieldtype === "Datetime" && !field.value) {
                                field.value = getCurrentDateTime();
                                emit("updateField", field);

                            }
                            if (field.label.includes("Requested by")) {
                                field.value = parsedData.emp_name;
                                emit("updateField", field);

                            }
                            if (field.fieldtype === "Date" && !field.value) {
                                field.value = new Date().toISOString().split('T')[0]; // Ensure format is YYYY-MM-DD
                                // console.log("Setting field.value:", field.value); // Debugging log
                                emit("updateField", field);
                            }



                        });
                    });
                });
            });
        });
    }
});

const datetimeInput = ref(null);


const hovered = ref(null)

const isImageFile = (url) => {
  return /\.(jpg|jpeg|png|gif|png)$/i.test(url)
}

const removeFile = (index, field) => {
  const files = field.value.split(',').map(f => f.trim())
  files.splice(index, 1)
  field.value = files.join(', ')
  emit('updateField', field)
}
const forceOpenCalendar = (event) => {
    if (event.target.showPicker) {
        event.target.showPicker(); // Opens the date picker in supported browsers
    }
    setTimeout(() => event.target.focus(), 50); // Ensures focus for unsupported browsers
};
// Watch blockArr for changes
watch(
    () => props.blockArr,
    () => {
        updateDateTimeFields();
    },
    { deep: true }
);
const emit = defineEmits();
const errorMessages = ref({});
const getFieldComponent = (type) => {
    switch (type) {
        case "Data":
        case "Phone":
        case "Date":
        case "Int":
        case "Check":
        case "radio":
            return "input";
        case "Text":
            return "textarea";
        case "Time":
            return "input";
        case "Select":
            return "select";
        case "Attach":
            return "file";
        case "Color":
            return "input";
    }
};
const allFieldsFilled = computed(() => {
    if (!props.blockArr || props.blockArr.length === 0) return false;

    for (const block of props.blockArr) {
        for (const section of block.sections) {
            for (const row of section.rows) {
                for (const column of row.columns) {
                    for (const field of column.fields) {
                        // If field is required and value is empty, return false
                        if (
                            field.reqd === 1 &&
                            (!field.value || field.value.toString().trim() === "")
                        ) {
                            return false;
                        }
                    }
                }
            }
        }
    }
    return true; // If all required fields are filled, return true
});

// Watch `allFieldsFilled` and emit value
watch(
    allFieldsFilled,
    (newValue) => {
        emit("formValidation", newValue);
    },
    { immediate: true }
);

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
    console.log(field.fieldtype);

    if (eve.target?.files && eve.target.files.length > 0) {
        let files = Array.from(eve.target.files); // Convert FileList to an array

        if (files.length > 5) {
            alert("You can upload a maximum of 5 files at a time.");
            files = files.slice(0, 5); // Restrict to the first 5 files
        }

        field["value"] = ""; // Clear previous values before adding new ones

        files.forEach((file) => uploadFile(file, field));
    } else if (eve.target?.type === "checkbox") {
        if (field.fieldtype === "Check") {
            field.value = eve.target.checked ? eve.target.value : "";
        } else if (field.fieldtype === "Small Text") {
            let selectedValues = field.value ? JSON.parse(field.value) : []; // Parse existing values or create an empty array

            if (eve.target.checked) {
                if (!selectedValues.includes(eve.target.value)) {
                    selectedValues.push(eve.target.value); // Add new selection
                }
            } else {
                selectedValues = selectedValues.filter(val => val !== eve.target.value); // Remove unchecked value
            }

            field.value = JSON.stringify(selectedValues); // Store as stringified array
            console.log(field.value, "selectedValues", selectedValues);



        } else {
            field.value = eve.target.checked;
        }
    } else if (eve.target?.type === "Select") {
        field.value = eve.target.value;
    } else if (eve.target?.type === "Table MultiSelect") {
        field.value = Array.from(
            eve.target.selectedOptions,
            (option) => option.value
        );
    }
    else if (field.fieldtype === "Text") {
        field["value"] = eve.target.value; // Capture textarea value
        emit("updateField", field.value); // Emit updated value
    } else {
        // field['value'] = eve.target.value;
        let inputValue = eve.target.value;

        // Ensure only numbers are stored and +91 is prefixed
        if (field.fieldtype === "Phone" || field.label.includes('phone' || 'telephone' || 'mobile')) {
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

const uploadFile = (file, field, index) => {
    const randomNumber = generateRandomNumber();
    let fileName = `mailfiles-${props.formName}${randomNumber}-@${file.name}`;

    const formData = new FormData();
    formData.append("file", file, fileName);
    formData.append("is_private", "0");
    formData.append("folder", "Home");
    axiosInstance
        .post(apis.uploadfile, formData)
        .then((res) => {
            if (res.message && res.message.file_url) {
                if (field["value"]) {
                    field["value"] += `, ${res.message.file_url}`;
                } else {
                    field["value"] = res.message.file_url;
                }
                emit("updateField", field);
            } else {
                console.error("file_url not found in the response.");
            }
        })
        .catch((error) => {
            console.error("Upload error:", error);
        });
};

// const handleFileChange = (event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex) => {
//     const file = event.target.files[0]; // Get the first file selected
//     if (file) {
//         const field = props.blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex];
//         field.value = file.name; // Store the file name in the field's value
//         emit('updateField', field); // Emit the updated field to the parent
//
//     }
// };
</script>
<style setup>
.previewInputHeight {
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
    background-color: #f5f5f5;
}

input::-webkit-input-placeholder {
    font-size: 10px;
}
</style>