<template>
    <div>
        <div class="d-flex justify-content-between align-items-center formsticky">
            <div>
                <h1 class="m-0 font-13">Forms Master</h1>
                <p class="m-0 font-11 pt-1">374 forms available</p>
            </div>
            <div class="d-flex gap-3 align-items-center">
                <div class="d-flex mt-2">
                    <div>
                        <FormFields labeltext="" class="mb-3" tag="input" type="search" placeholder="Search File Name"
                            name="Value" id="Value" v-model="filterObj.search" />
                    </div>
                    <div>
                        <FormFields tag="select" placeholder="Filter By" class="mb-3" name="roles"
                            v-model="filterObj.selectoption" id="roles" :Required="false" :options="[
                                'JW Marriott Golfshire Banglore',
                                'JW Marriott Golfshire Banglore',
                            ]" />
                    </div>
                </div>

                <div class="d-flex align-items-center mb-1">
                    <ButtonComp class="buttoncomp" @click="formCration()" name="Create form"></ButtonComp>
                </div>
            </div>
        </div>
        <div class="mt-2" v-if="tableForm">
            <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction="true" actionType="dropdown"
                isCheckbox="true" />
        </div>
        <div class="" v-if="creatForm">
            <div class="">
                <div class="d-flex justify-content-between align-items-center">
                    <div class="ps-1 m-0 d-flex align-items-center" @click="cancelForm()">
                        <h1 class="font-13">
                            <i class="bi bi-arrow-left"></i><span class="ms-2">Cancel Form</span>
                        </h1>
                    </div>
                    <div>
                        <ButtonComp class="font-10 rounded-2" name="Save as Draft"></ButtonComp>
                    </div>
                </div>
                <div class="form-container mt-1">
                    <div class="row">
                        <div class="col-2">
                            <ul class="steps">
                                <li v-for="step in steps" :key="step.id" :class="{
                                    active: activeStep === step.id,
                                    completed: activeStep > step.id,
                                }">
                                    <div class="d-flex gap-3 align-items-center" @click="handleStepClick(step.label)">
                                        <i v-if="activeStep > step.id"
                                            class="ri-checkbox-circle-fill completedStepIcon"></i>
                                        <i v-else :class="step.icon"></i>
                                        <div class="step-text">
                                            <span class="font-10">{{ step.stepno }}</span><br />
                                            <span>{{ step.label }}</span>
                                        </div>
                                    </div>
                                </li>
                            </ul>
                        </div>
                        <div class="col-10">
                            <div class="">
                                <div class="form-content stepsDiv">
                                    <!-- About Form Step -->
                                    <div v-if="activeStep === 1">
                                        <div class="">
                                            <div
                                                class="stepperbackground ps-2 pe-2 m-0 d-flex justify-content-between align-items-center">
                                                <h1 class="font-11 m-0">
                                                    <i class="bi bi-chevron-left"></i><span class="ms-2">Cancel
                                                        Form</span>
                                                </h1>
                                                <h1 class="font-11 m-0">About Form</h1>
                                                <ButtonComp class="buttoncomp" name="Next" v-if="activeStep < 3"
                                                    @click="nextStep" />
                                            </div>
                                        </div>
                                        <div class="row">
                                            <div class="col-4"></div>
                                            <div class="col-4">
                                                <div class="mt-4">
                                                    <div class="">
                                                        <FormFields labeltext="Form Name" class="mb-3" type="text"
                                                            tag="input" name="Value" id="Value"
                                                            placeholder="Untitle Form" orm
                                                            v-model="filterObj.form_name" />
                                                    </div>
                                                </div>
                                                <div class="mt-4">
                                                    <div class="">
                                                        <FormFields labeltext="Form Short Code" class="mb-3" type="text"
                                                            tag="input" name="Value" id="Value"
                                                            placeholder="Untitle Form"
                                                            v-model="filterObj.form_short_name" />
                                                    </div>
                                                </div>
                                                <div class="mt-4">
                                                    <div class="">
                                                        <FormFields labeltext="Owner Of The Form" class="mb-3 w-100"
                                                            tag="select" name="dept" id="dept"
                                                            placeholder="Select Department" :options=formOptions
                                                            v-model="filterObj.owner_of_the_form" />
                                                    </div>
                                                </div>
                                                <div class="mt-4">
                                                    <div class="">
                                                        <FormFields labeltext="Form Cateogry" class="mb-3" tag="select"
                                                            name="desgination" id="desgination"
                                                            placeholder="Select Cateogry" :options=departments
                                                            v-model="filterObj.form_category" />
                                                    </div>
                                                </div>
                                                <div class="mt-4">
                                                    <div class="">
                                                        <FormFields labeltext="Accessbility Departments" class="mb-3"
                                                            tag="select" name="desgination" id="Departments"
                                                            placeholder="Select Desigination" :options=formOptions
                                                            v-model="filterObj.accessible_departments" />
                                                    </div>
                                                </div>
                                            </div>

                                            <div class="col-4"></div>
                                        </div>
                                    </div>

                                    <!-- Questions in Form Step -->
                                    <div v-if="activeStep === 2">
                                        <div class="">
                                            <div
                                                class="stepperbackground ps-2 pe-2 m-0 d-flex justify-content-between align-items-center">
                                                <h1 class="font-11 m-0">
                                                    <i @click="prevStep" class="bi bi-chevron-left"></i><span
                                                        class="ms-2">Back To About Form</span>
                                                </h1>
                                                <button class="btn btn-light font-10" type="button" @click="formData()">
                                                    <i class="bi bi-eye me-1"></i>SaveData
                                                </button>
                                                <button class="btn btn-light font-10" type="button"
                                                    data-bs-toggle="modal" data-bs-target="#exampleModal"
                                                    @click="createForm">
                                                    <i class="bi bi-eye me-1"></i>Preview
                                                </button>
                                            </div>
                                            <div class="">
                                                <!-- <div class="d-flex justify-content-end">
                                            <button class="btn btn-light" type="button" data-bs-toggle="modal"
                                                data-bs-target="#exampleModal" @click="createForm">
                                                <i class="bi bi-eye me-1"></i>Preview
                                            </button>
                                        </div> -->
                                                <div class="modal fade" id="exampleModal" tabindex="-1"
                                                    aria-labelledby="exampleModalLabel" aria-hidden="true">
                                                    <div class="modal-dialog modal-xl">
                                                        <div class="modal-content">
                                                            <div class="modal-header">
                                                                <h5 class="modal-title m-0 font-13"
                                                                    id="exampleModalLabel">
                                                                    Preview Form
                                                                </h5>
                                                                <button type="button" class="btn-close"
                                                                    data-bs-dismiss="modal" aria-label="Close"></button>
                                                            </div>
                                                            <div class="modal-body">
                                                                <div v-if="formCreated">
                                                                    <div class="card p-1">
                                                                        <div v-for="(section, sectionIndex) in sections"
                                                                            :key="'preview-' + sectionIndex"
                                                                            class="preview-section mb-2">
                                                                            <h5>{{ section.label }}</h5>
                                                                            <div class="row"
                                                                                v-for="(row, rowIndex) in section.rows"
                                                                                :key="rowIndex">
                                                                                <div v-for="(column, columnIndex) in row.columns"
                                                                                    :key="'column-preview-' + columnIndex"
                                                                                    class="col">
                                                                                    <h6>{{ column.label }}</h6>
                                                                                    <div class="mb-2">
                                                                                        <div v-for="(field, fieldIndex) in column.fields"
                                                                                            :key="'field-preview-' + fieldIndex">
                                                                                            <div v-if="field.label">
                                                                                                <!-- Only show field if the name is not empty -->
                                                                                                <label :for="'field-' +
                                                                                                    sectionIndex +
                                                                                                    '-' +
                                                                                                    columnIndex +
                                                                                                    '-' +
                                                                                                    fieldIndex
                                                                                                    ">
                                                                                                    {{
                                                                                                        field.label
                                                                                                    }}</label>
                                                                                                <template v-if="field.fieldtype == 'select' ||
                                                                                                    field.fieldtype == 'multiselect'
                                                                                                ">
                                                                                                    <select :multiple="field.fieldtype == 'multiselect'
                                                                                                        "
                                                                                                        v-model="field.value"
                                                                                                        class="form-select mb-2 font-13">
                                                                                                        <option v-for="(
                                                        option, index
                                                      ) in field.options.split('\n')" :key="index" :value="option">
                                                                                                            {{ option }}
                                                                                                        </option>
                                                                                                    </select>
                                                                                                </template>
                                                                                                <template v-else-if="field.fieldtype == 'checkbox' ||
                                                                                                    field.fieldtype == 'radio'
                                                                                                ">
                                                                                                    <div class="row">
                                                                                                        <div class="form-check col-4 mb-4"
                                                                                                            v-for="(
                                                        option, index
                                                      ) in field.options.split('\n')" :key="index">
                                                                                                            <div
                                                                                                                class="d-flex gap-2 align-items-center">
                                                                                                                <div>
                                                                                                                    <input
                                                                                                                        class=""
                                                                                                                        :type="field.fieldtype"
                                                                                                                        :name="option"
                                                                                                                        :id="option" />
                                                                                                                </div>
                                                                                                                <div>
                                                                                                                    <label
                                                                                                                        class="form-check-label m-0"
                                                                                                                        :for="option">
                                                                                                                        {{
                                                                                                                            option
                                                                                                                        }}
                                                                                                                    </label>
                                                                                                                </div>
                                                                                                            </div>
                                                                                                        </div>
                                                                                                    </div>
                                                                                                </template>
                                                                                                <template v-else>
                                                                                                    <component
                                                                                                        :is="getFieldComponent(field.fieldtype)"
                                                                                                        v-model="field.value"
                                                                                                        :type="field.fieldtype"
                                                                                                        :name="'field-' +
                                                                                                            sectionIndex +
                                                                                                            '-' +
                                                                                                            columnIndex +
                                                                                                            '-' +
                                                                                                            fieldIndex
                                                                                                            "
                                                                                                        :class="form - control"
                                                                                                        class="form-control previewInputHeight">
                                                                                                    </component>
                                                                                                </template>
                                                                                            </div>
                                                                                        </div>
                                                                                    </div>
                                                                                </div>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <!-- <div class="modal-footer">
                                                        <button type="button" class="btn btn-secondary"
                                                            data-bs-dismiss="modal">Close</button>
                                                        <button class="btn btn-primary"
                                                            @click="saveFormFields">Save</button>
                                                    </div> -->
                                                        </div>
                                                    </div>
                                                </div>
                                                <div class="mt-4">
                                                    <div v-for="(section, sectionIndex) in sections" :key="sectionIndex"
                                                        class="dynamicSection">
                                                        <section class="d-flex justify-content-between">
                                                            <input v-model="section.label" type="text"
                                                                class="border-less-input font-14"
                                                                placeholder="Section Name" />
                                                            <button
                                                                class="btn btn-light bg-transparent border-0 font-13"
                                                                @click="removeSection(sectionIndex)">
                                                                <i class="bi bi-trash me-2"></i> Delete Section
                                                            </button>
                                                        </section>
                                                        <div class="container-fluid">
                                                            <section class="row" v-for="(row, rowIndex) in section.rows"
                                                                :key="rowIndex">
                                                                <div
                                                                    class="d-flex justify-content-between align-items-center">
                                                                    <label>{{ getRowSuffix(rowIndex) }}</label>
                                                                    <div>
                                                                        <button
                                                                            class="btn btn-light bg-transparent border-0 font-13"
                                                                            @click="removeRow(sectionIndex, rowIndex)">
                                                                            <i class="ri-subtract-line"></i> Remove Row
                                                                        </button>
                                                                        <button v-if="row.columns.length < 3"
                                                                            class="btn btn-light bg-transparent border-0 font-13"
                                                                            @click="addColumn(sectionIndex, rowIndex)">
                                                                            <i class="bi bi-plus"></i> Add Column
                                                                        </button>
                                                                    </div>
                                                                </div>
                                                                <div class="col">
                                                                    <div class="row">
                                                                        <div v-for="(column, columnIndex) in row.columns"
                                                                            :key="columnIndex"
                                                                            class="col p-0 dynamicColumn">
                                                                            <div
                                                                                class="column_name d-flex align-items-center justify-content-between">
                                                                                <input v-model="column.label"
                                                                                    type="text"
                                                                                    class="border-less-input columnFieldInput font-14"
                                                                                    placeholder="Column Name" />
                                                                                <button class="btn btn-light btn-sm"
                                                                                    @click="
                                                                                        removeColumn(
                                                                                            sectionIndex,
                                                                                            rowIndex,
                                                                                            columnIndex
                                                                                        )
                                                                                        ">
                                                                                    <i class="bi bi-trash"></i>
                                                                                </button>
                                                                            </div>
                                                                            <!-- Dynamically added fields within the column -->
                                                                            <div v-for="(field, fieldIndex) in column.fields"
                                                                                :key="fieldIndex" class="mt-2">
                                                                                <div class="px-3 py-1 field-border">
                                                                                    <div
                                                                                        class="d-flex justify-content-between">
                                                                                        <input v-model="field.label"
                                                                                            placeholder="Name the field"
                                                                                            class="border-less-input mb-1 columnFieldInput font-14 p-0" />
                                                                                        <div>
                                                                                            <button
                                                                                                class="btn btn-light btn-sm"><i
                                                                                                    class="ri-file-copy-line copyIcon"
                                                                                                    @click="copyField(sectionIndex, rowIndex, columnIndex, fieldIndex)"></i>
                                                                                            </button>

                                                                                            <button
                                                                                                class="btn btn-light btn-sm"
                                                                                                @click="
                                                                                                    removeField(
                                                                                                        sectionIndex,
                                                                                                        rowIndex,
                                                                                                        columnIndex,
                                                                                                        fieldIndex
                                                                                                    )
                                                                                                    ">
                                                                                                <i
                                                                                                    class="bi bi-trash"></i>
                                                                                            </button>
                                                                                        </div>
                                                                                    </div>
                                                                                    <select v-model="field.fieldtype"
                                                                                        class="form-select mb-2 font-13 searchSelect"
                                                                                        @change="
                                                                                            onFieldTypeChange(
                                                                                                sectionIndex,
                                                                                                rowIndex,
                                                                                                columnIndex,
                                                                                                fieldIndex
                                                                                            )
                                                                                            ">
                                                                                        <option value="">Select Type
                                                                                        </option>
                                                                                        <option
                                                                                            v-for="section in fieldTypes"
                                                                                            :key="section"
                                                                                            :value="section.type">
                                                                                            {{ section.label }}
                                                                                        </option>
                                                                                    </select>
                                                                                    <div v-if="field.fieldtype == 'checkbox' ||
                                                                                        field.fieldtype == 'radio' ||
                                                                                        field.fieldtype == 'select' ||
                                                                                        field.fieldtype == 'multiselect'
                                                                                    ">
                                                                                        <label class="font-12 fw-light"
                                                                                            for="options">Enter
                                                                                            Options:</label>
                                                                                        <textarea id="options"
                                                                                            placeholder="Enter your Options"
                                                                                            v-model="field.options"
                                                                                            class="form-control shadow-none mb-1 font-12">
                                        </textarea>
                                                                                    </div>
                                                                                    <div
                                                                                        class="d-flex gap-2 align-items-center">
                                                                                        <div>
                                                                                            <input class="font-12"
                                                                                                v-model="field.mandatory"
                                                                                                placeholder="Field Name"
                                                                                                type="checkbox" />
                                                                                        </div>
                                                                                        <div>
                                                                                            <label for="mandatory"
                                                                                                class="font-12 m-0 fw-light">Mandatory</label>
                                                                                        </div>

                                                                                        <!--- checkbox for mandatory -->
                                                                                    </div>
                                                                                </div>
                                                                            </div>
                                                                            <div
                                                                                class="d-flex justify-content-center align-items-center my-2">
                                                                                <button
                                                                                    class="btn btn-light btn-sm addField m-2"
                                                                                    @click="
                                                                                        addField(sectionIndex, rowIndex, columnIndex)
                                                                                        ">
                                                                                    <i class="bi bi-plus"></i> Add Field
                                                                                </button>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </section>
                                                        </div>
                                                        <div
                                                            class="d-flex justify-content-center align-items-center my-2">
                                                            <button class="btn btn-light btn-sm addRow m-2"
                                                                @click="addRow(sectionIndex, rowIndex)">
                                                                <i class="bi bi-plus"></i> Add Row
                                                            </button>
                                                        </div>
                                                    </div>
                                                    <div class="d-flex justify-content-center align-items-center my-4">
                                                        <button class="btn btn-light border font-12"
                                                            @click="addSection">
                                                            <i class="bi bi-plus-circle me-1 fs-6"></i> Add Section
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>

                    <div></div>
                </div>
            </div>
        </div>
    </div>
</template>
<script setup>
import FormFields from "../../Components/FormFields.vue";
import ButtonComp from "../../Components/ButtonComp.vue";
import GlobalTable from "../../Components/GlobalTable.vue";
import { callWithErrorHandling, onMounted, ref, reactive } from "vue";
import { extractFieldsWithBreaks } from '../../shared/services/field_format';
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from "../../shared/apiurls";
const filterObj = ref({
    form_name: "",
    form_short_name: "",
    accessible_departments: [],
    business_unit: "",
    form_category: "",
    owner_of_the_form: "",
});
const tableheaders = ref([
    { th: "Form name", td_key: "name" },
    { th: "Form category", td_key: "form_category" },
    { th: "Owner of form", td_key: "owner" },
    { th: "Accessible departments", td_key: "acess" },
    { th: "Status", td_key: "status" },
]);
const tableData = ref([]);
console.log(tableData.value, "tableeee");
const tableForm = ref(true);
const creatForm = ref(false);
function formCration() {
    tableForm.value = false;
    creatForm.value = true;
}
function cancelForm() {
    tableForm.value = true;
    creatForm.value = false;
}
const handleStepClick = (label) => {
    switch (label) {
        case "About Form":
            prevStep();
            break;
        case "Questions in Form":
            nextStep();
            break;
    }
};

// Current active step
const activeStep = ref(1);

// Form data structure
const form = ref({
    name: "",
    owner: "",
    category: "",
    accessibility: [],
    questions: [], // Array to hold added questions
});

// New question structure
const newQuestion = ref({
    text: "",
    answerType: "short", // Default answer type
});

// Dummy data for departments and categories
const departments = ["HR", "Finance", "IT", "Sales"];
const categories = ["Internal", "External", "Confidential"];

// List of steps with IDs and labels
const steps = [
    {
        id: 1,
        label: "About Form",
        stepno: "Step 1",
        icon: "bi bi-info-circle",
    },
    {
        id: 2,
        label: "Questions in Form",
        stepno: "Step 2",
        icon: "bi bi-question-circle",
    },
];

const fieldTypes = [
    {
        label: "Text",
        type: "dataText",
    },
    {
        label: "Checkbox",
        type: "checkbox",
    },
    {
        label: "Radio",
        type: "radio",
    },
    {
        label: "Attach",
        type: "file",
    },
    {
        label: "Number",
        type: "number",
    },
    {
        label: "TextArea",
        type: "textarea",
    },
    {
        label: "Date",
        type: "date",
    },
    {
        label: "Select",
        type: "select",
    },
    {
        label: "MultiSelect",
        type: "multiselect",
    },
];

// Save the form as a draft
const saveAsDraft = () => {
    console.log("Form saved as draft:", form.value);
};

// Move to the next step
const nextStep = () => {
    if (activeStep.value < 3) {
        activeStep.value += 1;
    }
    console.log(filterObj.value, 'fffffffffffff')

};
function formData() {
    const fields = extractFieldsWithBreaks(sections)
    const dataObj = {
        ...filterObj.value,
        fields
    }
    console.log(" Complete Data === ", dataObj)
    axiosInstance.post('http://192.168.1.134:8000/api/method/ezy_forms.ezy_forms.doctype.ezy_form_definitions.ezy_form_definitions.add_dynamic_doctype', dataObj).then((res) => {
        console.log(res, rrrrrrrrrrrrrrr);
    })


}

// Move to the previous step
const prevStep = () => {
    if (activeStep.value > 1) {
        activeStep.value -= 1;
    }
};


const sections = reactive([]);
const formCreated = ref(false); // To control form preview visibility

// Function to add a new section with a default column
const addSection = () => {
    sections.push({
        label: "", // Initialize section name
        rows: [
            {
                columns: [
                    {
                        label: "",
                        fields: [], // Initialize with an empty fields array
                    },
                ],
            },
        ],
    });
};
// Function to remove a section
const removeSection = (sectionIndex) => {
    sections.splice(sectionIndex, 1);
};

const addRow = (sectionIndex) => {
    sections[sectionIndex].rows.push({
        columns: [
            {
                // Initialize with a default column
                fields: [], // Initialize with an empty fields array
            },
        ],
    });
};

const removeRow = (sectionIndex, rowIndex) => {
    sections[sectionIndex].rows.splice(rowIndex, 1);
};

// Function to add a new column inside a section
const addColumn = (sectionIndex, rowIndex) => {
    sections[sectionIndex].rows[rowIndex].columns.push({
        label: "",
        fields: [],
    });
};

// Function to remove a column inside a section
const removeColumn = (sectionIndex, rowIndex, columnIndex) => {
    sections[sectionIndex].rows[rowIndex].columns.splice(columnIndex, 1);
};

// Function to add a new field inside a column
const addField = (sectionIndex, rowIndex, columnIndex) => {
    sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields.push({
        label: "",
        fieldtype: "",
        // value: ref(""), // Keeping the value as a ref for reactivity
        options: null,
        mandatory: false,
    });
};

// Function to remove a field inside a column
const removeField = (sectionIndex, rowIndex, columnIndex, fieldIndex) => {
    sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields.splice(fieldIndex, 1);
};


// Function to copy a field and add it below the original field inside a column
const copyField = (sectionIndex, rowIndex, columnIndex, fieldIndex) => {
    // Get the field to copy
    const fieldToCopy = sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex];

    // Create a shallow copy of the field
    const newField = { ...fieldToCopy };

    // Optionally, you can modify some properties (e.g., rename the field)
    newField.name = `${fieldToCopy.name} Name the field`;

    // Insert the copied field after the original one
    sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields.splice(fieldIndex + 1, 0, newField);
};
// Handle the change of field type to display the correct input
const onFieldTypeChange = (sectionIndex, rowIndex, columnIndex, fieldIndex) => {
    const field =
        sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex];
    // Handle additional logic for field type change if needed
    console.log("field === ", field);
    console.log(" sections === ", sections);

    const xyz = extractFieldsWithBreaks(sections)
    console.log(" extracted Format === ", xyz)


};
// Dynamically determine the input field type
const getFieldComponent = (type) => {
    switch (type) {
        case "dataText":
            return "input";
        case "number":
            return "input";
        case "textarea":
            return "textarea";
        case "checkbox":
            return "input"; // Checkbox input will need to handle checked state
        case "select":
            return "select"; // Handle options for dropdown separately
        case "date":
            return "input"; // Consider using type="date" for HTML5 date input
        case "radio":
            return "input";
        default:
            return "input";
    }
};
const getRowSuffix = (index) => {
    if (index === 0) {
        return "1st row";
    } else if (index === 1) {
        return "2nd row";
    } else if (index === 2) {
        return "3rd row";
    } else {
        return `${index + 1}th row`;
    }
};

// Trigger the creation of form and show the preview
const createForm = () => {
    formCreated.value = true;
};

const deptOptions = ref([])
const formOptions = ref([])
function deptData() {

    axiosInstance.get(apis.resource + doctypes.dept).then((res) => {
        deptOptions.value = res.data
        formOptions.value = deptOptions.value.map((dept) => dept.name);

        console.log(deptOptions.value, 'deptttttt');
    })

}
onMounted(() => {
    deptData();

})


</script>

<style scoped>
input {
    font-size: 13px !important;
    height: 35px;
}

.formsticky {
    position: sticky;
    top: 50px;
    z-index: 100;
    background: white;
}

.dynamicSection {
    border: 1px solid #cccccc;
    margin-bottom: 20px;
    border-radius: 7px;
    background-color: #eeeeee;
}

.dynamicColumn {
    border: 1px solid #cccccc;
    border-radius: 10px;
    margin: 5px;
    margin-top: 0;
    position: relative;
    background-color: #ffffff;
}

.dynamicColumn:hover {
    border: 1px solid rgb(119, 119, 119);
}

.column_name {
    /* border-bottom: 1px solid #f1f1f1; */
    padding: 1px 10px;
}

.main-section {
    background-color: #fff;
    border-radius: 10px;
    padding: 20px;
    border: 1px solid rgb(236, 236, 236);
    margin: 10px;
    position: relative;
}

.border-less-input {
    border: 0;
    background: transparent;
}

.border-less-input:focus {
    border: 0;
    background: transparent;
    outline: 0;
}

.field-border {
    /* border: 1px solid rgb(221, 221, 221); */
    border-radius: 10px;
    margin: 5px 10px;
    background-color: #fafafa;
}

.preview-section {
    background-color: #f9f9f9;
    padding: 8px;
    border-radius: 10px;
}

input[type="checkbox"] {
    margin-left: 5px;
    height: 10px;
}

has context menu .form-container {
    /* max-width: 900px; */
    margin: 0 auto;
    padding-top: 20px;

    border-radius: 8px;
    background-color: #fff;
}

.form-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.steps {
    /* display: flex;
    justify-content: space-evenly; */
    list-style: none;
    padding: 0;
    margin: 0;
    width: 100%;
    position: relative;
}

.steps li {
    padding: 10px 20px;
    font-size: 12px;
    cursor: pointer;
    transition: 0.3s all ease;
    width: 100%;
    position: relative;
}

.steps li.active {
    color: #1b14df;
    font-weight: bold;
}

.completedStepIcon {
    color: #1b14df;
    font-size: 12px;
}

.steps li.completed {
    color: #000;

    font-weight: normal;
    opacity: 0.7;
}

.steps li.completed::after {
    content: "";
    display: block;
    width: 1px;
    height: 20px;
    background-color: #d9d9d9;
    /* Customize the color */
    position: absolute;
    border-radius: 2px;
    left: 25px;
    /* Adjust position relative to the icon */
    top: 80%;
    /* Position the line below the step */
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    margin-bottom: 5px;
    font-weight: 500;
    margin-top: 5px;
    font-size: 13px;
}

input,
select {
    /* width: 100%; */
    padding: 10px;
    border: 1px solid #ccc;
}

.searchSelect {
    border-radius: 10px !important;
}

.form-footer {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
}

.backTo {
    color: #000;
    border: none;
    border-bottom: 2px solid black;
    background: transparent;
    padding-bottom: 0px;
    height: 25px;
}

.Savedraft {
    color: #000;
    border: none;
    background: transparent;
}

.NextSave {
    padding: 6px 12px;
    border: none;
    background-color: #000;
    color: #fff;
    cursor: pointer;
    border-radius: 4px;
}

.NextSave:hover {
    background-color: #444;
}

.saveForm {
    padding: 6px 12px;
    border: none;
    background-color: #000;
    color: #fff;
    cursor: pointer;
    border-radius: 4px;
    margin-top: 20px;
}

.saveForm:hover {
    background-color: #000;
}

.stepperbackground {
    background-color: #eeeeee;
    height: 50px;
    border-radius: 7px;
}

.previewInputHeight {
    height: 35px;
}

.addField,
.addRow {
    font-size: 14px;
    font-weight: 500;
}

.columnFieldInput {
    font-style: italic;
}

.copyIcon {
    cursor: pointer;
}
</style>
