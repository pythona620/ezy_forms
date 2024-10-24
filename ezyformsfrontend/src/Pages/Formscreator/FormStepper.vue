<template>
    <div>
        <div class="">
            <div class="">
                <div class="d-flex justify-content-between align-items-center CancelNdSave my-2 mx-1">
                    <div class="ps-1 m-0 d-flex align-items-center" @click="cancelForm()">
                        <h1 class="font-13 m-0">
                            <i class="bi bi-arrow-left"></i><span class="ms-2">Back</span>
                        </h1>
                    </div>
                    <div>


                        <!-- <ButtonComp class="font-13 rounded-2" name="Save as Draft"></ButtonComp> -->
                        <button type="butoon" class="btn font-13 btn-light " @click="SaveAsDrafts()"><i
                                class="bi bi-bookmark-check-fill"></i>
                            Save As Draft</button>
                    </div>
                </div>
                <div class="form-container container-fluid mt-1">
                    <div class="row">
                        <div class="col-2">
                            <ul class="steps">
                                <li v-for="step in steps" :key="step.id" :class="{
                                    active: activeStep === step.id,
                                    completed: activeStep > step.id && index === steps.length - 1,
                                }">
                                    <div class="d-flex gap-3 align-items-center" @click="handleStepClick(step.label)">
                                        <i v-if="activeStep > step.id"
                                            class="ri-checkbox-circle-fill completedStepIcon"></i>
                                        <i v-else :class="step.icon"></i>
                                        <div class="step-text">
                                            <span class="font-11">{{ step.stepno }}</span><br />
                                            <span class=" font-14">{{ step.label }}</span>
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
                                                <h1 class="font-14 m-0" @click="cancelForm()">
                                                    <i class="bi bi-chevron-left"></i><span class="ms-2">Cancel
                                                        Form</span>
                                                </h1>
                                                <h1 class="font-14 fw-bold m-0">About Form</h1>
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
                                                        <!-- <label for="">Form Short Code</label>

                                                        <Multiselect :options=formOptions
                                                            v-model="filterObj.form_short_name"
                                                            placeholder="Untitle Form" :multiple="true"
                                                            :searchable="true" /> -->
                                                    </div>
                                                </div>
                                                <div class="mt-4">
                                                    <div class="">
                                                        <!-- <FormFields labeltext="Owner Of The Form" class="mb-3 w-100"
                                                            tag="select" name="dept" id="dept"
                                                            placeholder="Select Department" :options=formOptions
                                                            v-model="filterObj.owner_of_the_form" /> -->
                                                        <label for="">Owner Of The Form</label>

                                                        <Multiselect :options="OwnerOfTheFormData"
                                                            @change="OwnerOftheForm"
                                                            v-model="filterObj.owner_of_the_form"
                                                            placeholder="Select Department" :multiple="false"
                                                            class=" font-11" :searchable="true" />

                                                    </div>
                                                </div>
                                                <div class="mt-4">
                                                    <div class="">
                                                        <!-- <FormFields labeltext="Form Cateogry" class="mb-3" tag="select"
                                                            name="desgination" id="desgination"
                                                            placeholder="Select Cateogry" :options=departments
                                                            v-model="filterObj.form_category" /> -->

                                                        <label for="">Form Cateogry</label>

                                                        <Multiselect :options=departments
                                                            v-model="filterObj.form_category"
                                                            placeholder="Select Cateogry" :multiple="false"
                                                            :searchable="true" class=" font-11" />
                                                    </div>
                                                </div>
                                                <div class="mt-4">
                                                    <div class="">
                                                        <!-- <FormFields labeltext="Accessbility Departments" class="mb-3"
                                                            tag="multiselect" name="desgination" id="Departments"
                                                            placeholder="Select Desigination" :options=formOptions
                                                            v-model="filterObj.accessible_departments" /> -->
                                                        <!-- <v-select v-model="filterObj.accessible_departments"
                                                            :options="formOptions"></v-select> -->
                                                    </div>
                                                    <!-- <label for="">Accessbility Departments</label> -->
                                                    <!-- <Multiselect :options=formOptions
                                                        v-model="filterObj.accessible_departments"
                                                        placeholder="Select Desigination" :multiple="true"
                                                        track-by="code" :close-on-select="false"
                                                        :clear-on-select="false" :searchable="true" /> -->

                                                    <div>
                                                        <label class="typo__label">
                                                            <label for="">Accessibility Departments</label>
                                                        </label>
                                                        <VueMultiselect v-model="filterObj.accessible_departments"
                                                            :options="formOptions" :multiple="true"
                                                            :close-on-select="false" :clear-on-select="false"
                                                            :preserve-search="true" placeholder="Select Designation"
                                                            class=" font-11">
                                                            <template #selection="{ values, isOpen }">
                                                                <span class="multiselect__single font-10"
                                                                    v-if="values.length" v-show="!isOpen">
                                                                    {{ values.length }} options selected
                                                                </span>
                                                            </template>
                                                        </VueMultiselect>
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
                                                <div class=" d-flex gap-2">
                                                    <div v-if="sections.length">
                                                        <button class="btn btn-light font-13" type="button"
                                                            @click="previewForm">
                                                            <i class="bi bi-eye me-1"></i>Preview
                                                        </button>
                                                        <FormPreview :sections="sections" />
                                                    </div>
                                                    <button :disabled="!sections.length"
                                                        class="btn btn-dark font-10  Withborder border " type="button"
                                                        @click="saveFormData()">
                                                        Save Data
                                                    </button>
                                                    <!-- <button class="btn btn-light font-10" type="button"
                                                        data-bs-toggle="modal" data-bs-target="#exampleModal"
                                                        @click="createForm">
                                                        <i class="bi bi-eye me-1"></i>Preview
                                                    </button> -->
                                                </div>
                                            </div>
                                            <div class="">
                                                <div class="mt-4">
                                                    <div v-for="(section, sectionIndex) in sections" :key="sectionIndex"
                                                        class="dynamicSection">
                                                        <section class="d-flex justify-content-between">
                                                            <input v-model="section.label" type="text"
                                                                class="border-less-input font-14"
                                                                placeholder="Untitled approval flow" />
                                                            <div class=" d-flex">
                                                                <!-- <button
                                                                    class="btn btn-light designationBtn d-flex align-items-center"
                                                                    type="button" data-bs-toggle="offcanvas"
                                                                    data-bs-target="#offcanvasRight"
                                                                    aria-controls="offcanvasRight"><img
                                                                        src="../../assets/oui_app-users-roles.svg"
                                                                        alt="" class="me-1"> Add
                                                                    designations</button> -->

                                                                <!-- <div class="offcanvas offcanvas-end" tabindex="-1"
                                                                    id="offcanvasRight"
                                                                    aria-labelledby="offcanvasRightLabel">
                                                                    <div class="offcanvas-header">
                                                                        <h5 id="offcanvasRightLabel">Add designation for
                                                                            requestor
                                                                        </h5>
                                                                        <button type="button"
                                                                            class="btn-close bg-light text-reset"
                                                                            data-bs-dismiss="offcanvas"
                                                                            aria-label="Close"></button>
                                                                    </div>
                                                                    <div class="offcanvas-body">
                                                                        <ul class=" list-unstyled">
                                                                            <li class="designationList">
                                                                                <input type="checkbox" name="" id=""
                                                                                    class="designationCheckBox">
                                                                                <span class="ps-2">intern</span>
                                                                            </li>
                                                                        </ul>
                                                                    </div>
                                                                    <div class=" offcanvas-footer">
                                                                        <div class=" text-end p-3">
                                                                            <ButtonComp
                                                                                class="btn btn-dark addingDesignations"
                                                                                name=" Add Designations" />
                                                                        </div>
                                                                    </div>
                                                                </div> -->

                                                                <button
                                                                    class="btn btn-light bg-transparent border-0 font-13 deleteSection"
                                                                    @click="removeSection(sectionIndex)">
                                                                    <i class="bi bi-trash me-1"></i> Delete Section
                                                                </button>
                                                            </div>
                                                        </section>
                                                        <div class="container-fluid">
                                                            <section class="row" v-for="(row, rowIndex) in section.rows"
                                                                :key="rowIndex">
                                                                <div
                                                                    class="d-flex justify-content-between align-items-center">
                                                                    <label class="rownames">{{ getRowSuffix(rowIndex)
                                                                        }}</label>
                                                                    <div>
                                                                        <button v-if="row.columns.length < 3"
                                                                            class="btn btn-light bg-transparent border-0 font-13"
                                                                            @click="addColumn(sectionIndex, rowIndex)">
                                                                            <i class="bi bi-plus"></i> Add Column
                                                                        </button>
                                                                        <button
                                                                            class="btn btn-light bg-transparent border-0 font-13"
                                                                            @click="removeRow(sectionIndex, rowIndex)">
                                                                            <i class="ri-subtract-line"></i> Delete row
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
                                                                                    <div
                                                                                        v-if="field.fieldtype == 'checkbox' || field.fieldtype == 'radio' || field.fieldtype == 'Select' || field.fieldtype == 'multiselect'">
                                                                                        <label class="font-12 fw-light"
                                                                                            for="options">Enter
                                                                                            Options:</label>
                                                                                        <textarea id="options"
                                                                                            placeholder="Enter your Options"
                                                                                            v-model="field.options"
                                                                                            class="form-control shadow-none mb-1 font-12"></textarea>
                                                                                    </div>
                                                                                    <div
                                                                                        class="d-flex gap-2 align-items-center">
                                                                                        <div>
                                                                                            <input class="font-12"
                                                                                                v-model="field.reqd"
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
                                                                                    class="btn btn-light btn-sm d-flex align-items-center addField m-2"
                                                                                    @click="
                                                                                        addField(sectionIndex, rowIndex, columnIndex)
                                                                                        ">
                                                                                    <i class="bi bi-plus fs-4"></i>
                                                                                    <span>Add Field</span>
                                                                                </button>
                                                                            </div>
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                            </section>
                                                        </div>
                                                        <div
                                                            class="d-flex justify-content-start align-items-center my-2">
                                                            <button class="btn btn-light addRow m-2 "
                                                                @click="addRow(sectionIndex, rowIndex)">
                                                                <i class="bi bi-plus"></i> Add row in section
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


                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import FormFields from "../../Components/FormFields.vue";
import { onMounted, ref, reactive, computed, watch } from "vue";
import ButtonComp from "../../Components/ButtonComp.vue";
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import { extractFieldsWithBreaks, rebuildToStructuredArray, extractFieldnames } from '../../shared/services/field_format';
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from "../../shared/apiurls";
import { useRoute, useRouter } from "vue-router";
import FormPreview from './FormPreview.vue'
import Multiselect from '@vueform/multiselect';
import '@vueform/multiselect/themes/default.css';
import VueMultiselect from 'vue-multiselect'

const route = useRoute();
const router = useRouter();
// Current active step
const activeStep = ref(1);
// Dummy data for departments and categories
const departments = ref([]);
const categories = ref([]);
const formOptions = ref([]); // Stores accessible departments
const OwnerOfTheFormData = ref([]); // Stores departments for owner_of_the_form
let sections = reactive([]);
let deleted_items = reactive([])
let deleted_flat_arr = reactive([])


const businessUnit = computed(() => {
    return EzyBusinessUnit;
});

let paramId = ref("")

onMounted(() => {
    deptData();

    paramId = route.params.paramid || 'new'; // Default to 'new' if no param is provided
    console.log(' === paramId:', paramId);
    if (paramId != undefined && paramId != null && paramId != 'new') {
        getFormData()
    }
})

const selectedAccdept = ref("")
const filterObj = ref({
    form_name: "",
    form_short_name: "",
    accessible_departments: [],
    business_unit: `${businessUnit.value.value}`,
    form_category: "",
    owner_of_the_form: "",
});
watch(
    businessUnit,
    (newVal) => {
        filterObj.value.business_unit = newVal;
    },
    { immediate: true }
);
const steps = [
    {
        id: 1,
        label: "About Form",
        stepno: "Step 1",
        icon: "bi bi-info-circle",
    },
    {
        id: 2,
        label: "Fields & Workflow",
        stepno: "Step 2",
        icon: "bi bi-question-circle",
    },
];
const fieldTypes = [
    {
        label: "Text",
        type: "Data",
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
        type: "Attach",
    },
    {
        label: "Number",
        type: "number",
    },
    {
        label: "TextArea",
        type: "Text",
    },
    {
        label: "Date",
        type: "Date",
    },
    {
        label: "Select",
        type: "Select",
    },
    {
        label: "MultiSelect",
        type: "multiselect",
    },
];


function cancelForm() {
    router.push({
        name: 'Created'
    })
}
const handleStepClick = (label) => {
    switch (label) {
        case "About Form":
            prevStep();
            break;
        case "Fields & Workflow":
            nextStep();
            break;
    }
};
// Move to the next step
const nextStep = () => {
    if (activeStep.value < 3) {
        activeStep.value += 1;
    }
};
watch(
    () => filterObj.owner_of_the_form,
    (newVal, oldVal) => {
        if (newVal !== oldVal) {
            OwnerOftheForm(newVal, oldVal);
        }
    }
);
function formData() {
    const fields = extractFieldsWithBreaks(sections)
    const dataObj = {
        ...filterObj.value,
        fields,
        "doctype": doctypes.EzyFormDefinitions
    }
    dataObj.accessible_departments = dataObj.accessible_departments.toString(); //JSON.stringify(dataObj.accessible_departments)
    axiosInstance.post(apis.savedata, dataObj).then((res) => {
        console.log(res, "saved From Responces");
    })
}
// Move to the previous step
const prevStep = () => {
    if (activeStep.value > 1) {
        activeStep.value -= 1;
    }
};

// Function to add a new section with a default column
const addSection = () => {
    console.log(" Add Section ", sections)
    sections.push({
        label: "",
        parent: `${businessUnit.value.value}-${filterObj.value.form_short_name}`,
        rows: [
            {
                label: getRowSuffix(0),
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
    let item = sections[sectionIndex]
    if (item.parent) deleted_items.push(item)
    sections.splice(sectionIndex, 1);
};

const addRow = (sectionIndex) => {
    const rowIndex = sections[sectionIndex].rows.length;  // Get the current row index
    const rowSuffix = getRowSuffix(rowIndex);
    console.log(" Rowsuffix == ", rowSuffix)
    sections[sectionIndex].rows.push({
        label: rowSuffix,
        columns: [
            {

                fields: [], // Initialize with an empty fields array
            },
        ],
    });
};

const removeRow = (sectionIndex, rowIndex) => {
    let item = sections[sectionIndex].rows[rowIndex]
    if (item.parent) deleted_items.push(item)
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
    let item = sections[sectionIndex].rows[rowIndex].columns[columnIndex]
    if (item.parent) deleted_items.push(item)
    sections[sectionIndex].rows[rowIndex].columns.splice(columnIndex, 1);
};

// Function to add a new field inside a column
const addField = (sectionIndex, rowIndex, columnIndex) => {
    sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields.push({
        label: "",
        fieldtype: "",
        // value: ref(""), // Keeping the value as a ref for reactivity
        options: null,
        reqd: false,
    });

};

// Function to remove a field inside a column
const removeField = (sectionIndex, rowIndex, columnIndex, fieldIndex) => {
    let item = sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex]
    if (item.parent) deleted_items.push(item)
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
    let fieldType = sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex].fieldtype
    if (fieldType !== 'checkbox' || fieldType !== 'Select' || fieldType !== 'radio' || fieldType !== 'multiselect') {
        sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex].options = null
    }
    const field =
        sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex];
    // Handle additional logic for field type change if needed
    console.log(fieldType, "field === ", field);
    console.log(" sections === ", sections);

    console.log(" deleted items sections === ", deleted_items)

    const xyz = extractFieldsWithBreaks(sections)
    console.log(" extracted Format === ", xyz)


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
const previewForm = () => {
    // sections = rebuildToStructuredArray(JSON.parse(rowData?.form_json?.replace(/\\\"/g, '"')))
    // console.log(" Rebuild form  === ", selectedForm.value)

    const modal = new bootstrap.Modal(document.getElementById('formViewModal'), {});// raise a modal
    modal.show();
    // selectedForm.value = rowData; // Store the selected form data
    // const result = dataObj.fields.map(({ fieldtype, fieldname,label, _user_tags}) => ({ fieldtype, fieldname,label,_user_tags }));


};

function deptData() {
    const queryParams = {
        fields: JSON.stringify(["*"]),
    };

    axiosInstance.get(apis.resource + doctypes.departments, { params: queryParams })
        .then((res) => {
            if (res?.data?.length) {
                // console.log(res.data, "Fetched departments");
                // Mapping department names
                // label="name" track-by="name"
                OwnerOfTheFormData.value = res.data.map((dept) => dept.name);
                formOptions.value = res.data.map((dept) => dept.name); // Store the full data for accessible departments
                // console.log(formOptions.value, 'Accessible Departments');
            }
        })
        .catch((error) => {
            console.error("Error fetching department data:", error);
        });
}

function OwnerOftheForm(newVal) {
    categoriesData(newVal);
}

function categoriesData(newVal) {
    axiosInstance.get(apis.resource + doctypes.departments + `/${newVal}`)
        .then((res) => {
            if (res?.data?.ezy_departments_items) {
                departments.value = res.data.ezy_departments_items.map((item) => item.category);
            }
        })
        .catch((error) => {
            console.error("Error fetching categories data:", error);
        });
}
// Get form by ID
function getFormData() {
    axiosInstance.get(apis.resource + doctypes.EzyFormDefinitions + `/${paramId}`)
        .then((res) => {
            let res_data = res?.data
            if (res_data) {
                filterObj.value = res_data
                OwnerOftheForm(filterObj.value.owner_of_the_form);
                console.log(" Flat array === ", JSON.parse(res_data?.form_json?.replace(/\\\"/g, '"')))
                let structuredArr = rebuildToStructuredArray(JSON.parse(res_data?.form_json?.replace(/\\\"/g, '"')))
                console.log(" structuredArr === ", structuredArr[0])
                structuredArr.forEach((item, index) => {
                    sections.push(item)
                })
            }
        })
        .catch((error) => {
            console.error("Error fetching  data:", error);
        });
}

function delete_form_items_fields() {
    axiosInstance.post(apis.delete_form_items, {
        deleted_fields: deleted_items.flatMap(extractFieldnames),
        doctype: paramId
    }).then((res) => {
        console.log(" delete resp === ", res)
        if (res?.message?.success) {
            // return res;
            formData()
        }
    })
}

async function saveFormData() {
    let data = deleted_items.flatMap(extractFieldnames)
    if ((paramId != undefined && paramId != null && paramId != 'new') && data.length) {
        delete_form_items_fields()
        //    console.log(" result", result)

    } else {
        formData()
    }
}
// watch(sections, (newSections) => {
//     console.log(sections, "---------------------");
//     console.log('Sections changed:', newSections);
// }, { deep: true });

</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style lang="scss" scoped>
/* @import '@vueform/multiselect/themes/default.css'; */

.CancelNdSave {
    background-color: #fafafa;
}

.stepsDiv {
    margin-top: 25px;
}

input {
    font-size: 13px !important;
    height: 35px;
}

.rownames {
    opacity: 0;
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
    height: 15px;
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
    padding: 25px 20px;
    font-size: 14px;
    font-weight: 400;
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
    font-size: 14px;
}

.steps li.completed {
    color: #000;
    font-size: 14px;
    font-weight: 400;
    font-weight: normal;
    opacity: 0.7;
}

.steps li.completed::after {
    content: "";
    display: block;
    width: 1px;
    height: 40px;
    background-color: #d9d9d9;
    /* Customize the color */
    position: absolute;
    border-radius: 2px;
    left: 25px;
    /* Adjust position relative to the icon */
    top: 75%;
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

.addField {
    font-size: 14px;
    font-weight: 400;
}

.addRow {
    // border: 1px solid #ccc;
    font-size: 12px;
    font-weight: 400;
    border-radius: 6px;
    background-color: transparent;
}

.columnFieldInput {
    font-style: italic;
}

.copyIcon {
    cursor: pointer;
}

.deleteSection {
    color: #FE212E;
}

.designationBtn {
    color: #1B14DF;
    font-size: 13px;
    font-weight: 400;
    background-color: transparent;
    border: none;
}

.designationList {
    border: 1px solid #eeeeee;
    font-size: 14px;
    font-weight: 400;
    padding: 15px 5px;
    border-radius: 6px;
    display: flex;
    align-items: center;
}

.designationCheckBox {
    font-size: 20px !important;
}

.addingDesignations {
    font-size: 14px;
    font-weight: 600;
    /* margin-right: 30px; */
}

.Withborder {
    border: 1px solid #eeeeee;

}


.multiselect-option {
    font-size: 11px !important;
}

.multiselect {
    margin: initial;
    font-size: 11px !important;
    border: 1px solid #e2e2e2 !important;
    min-height: 35px !important;

    .multiselect-wrapper {
        min-height: 35px !important;
    }

    .multiselect-dropdown {
        .multiselect-options {
            font-size: 11px;


            li.multiselect-option span {
                font-size: 11px !important;

            }

            li.multiselect-option .is-selected {
                background-color: grey !important;
                font-size: 11px;
            }
        }
    }

}

.multiselect__option span {
    font-size: 11px;
    /* Change this value to whatever size you need */
}

.multiselect .multiselect-option {
    font-size: 11px;
}

.multiselect .multiselect-wrapper {
    min-height: 35px !important;
}

.multiselect .multiselect--above {
    min-height: 35px !important;

}

.multiselect .multiselect__tags {

    min-height: 35px;
    font-size: 11px !important;


}

.multiselect .multiselect__placeholder {
    font-size: 11px;
}

.multiselect .multiselect__single {
    font-size: 11px;
}

.multiselect .multiselect__tags .multiselect__placeholder {
    font-size: 11px;
}
</style>
