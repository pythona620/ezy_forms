<template>
    <div class="">
        <div class="d-flex justify-content-between align-items-center">
            <div class="ps-1 m-0 d-flex align-items-center">
                <h1 class="font-13"><i class="bi bi-arrow-left"></i><span class="ms-2">Cancel Form</span></h1>
            </div>
            <div>
                <ButtonComp class="font-10 rounded-2" name="Save as Draft"></ButtonComp>
            </div>
        </div>
        <div class="form-container mt-1">

            <div class="row">
                <div class=" col-2">
                    <ul class="steps">
                        <li v-for="step in steps" :key="step.id"
                            :class="{ active: activeStep === step.id, completed: activeStep > step.id }">
                            <div class="d-flex gap-3 align-items-center" @click="handleStepClick(step.label)">
                                <i :class="step.icon"></i>
                                <div class="step-text">
                                    <span class="font-10">{{ step.stepno }}</span><br>
                                    <span>{{ step.label }}</span>
                                </div>
                            </div>
                        </li>
                    </ul>

                </div>
                <div class=" col-10">

                    <div class="">

                        <div class="form-content stepsDiv">
                            <!-- About Form Step -->
                            <div v-if="activeStep === 1">
                                <div class="">
                                    <div
                                        class=" stepperbackground ps-2 pe-2 m-0 d-flex justify-content-between align-items-center">
                                        <h1 class="font-11 m-0"><i class="bi bi-chevron-left"></i><span
                                                class="ms-2">Cancel
                                                Form</span>
                                        </h1>
                                        <h1 class="font-11 m-0">About Form</h1>
                                        <ButtonComp class="buttoncomp" name="Next" v-if="activeStep < 3"
                                            @click="nextStep" />

                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-4">

                                    </div>
                                    <div class="col-4">

                                        <div class=" mt-4">
                                            <div class="">

                                                <FormFields labeltext="Form Name" class="mb-3" type="text" tag="input"
                                                    name="Value" id="Value" placeholder="Untitle Form" orm
                                                    v-model="filterObj.name" />

                                            </div>
                                        </div>
                                        <div class=" mt-4">
                                            <div class="">

                                                <FormFields labeltext="Form Short Code" class="mb-3" type="text"
                                                    tag="input" name="Value" id="Value" placeholder="Untitle Form"
                                                    v-model="filterObj.code" />

                                            </div>
                                        </div>
                                        <div class=" mt-4">
                                            <div class="">

                                                <FormFields labeltext="Owner Of The Form" class="mb-3 w-100"
                                                    tag="select" name="dept" id="dept" placeholder="Select Department"
                                                    :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']"
                                                    v-model="filterObj.owner" />

                                            </div>
                                        </div>
                                        <div class=" mt-4">
                                            <div class="">

                                                <FormFields labeltext="Form Cateogry" class="mb-3" tag="select"
                                                    name="desgination" id="desgination" placeholder="Select Cateogry"
                                                    :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']"
                                                    v-model="filterObj.categery" />

                                            </div>
                                        </div>
                                        <div class=" mt-4 ">
                                            <div class="">

                                                <FormFields labeltext="Accessbility Departments" class="mb-3"
                                                    tag="select" name="desgination" id="Departments"
                                                    placeholder="Select Desigination"
                                                    :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']"
                                                    v-model="filterObj.dept" />

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
                                        class=" stepperbackground ps-2 pe-2  m-0 d-flex justify-content-between align-items-center">
                                        <h1 class="font-11 m-0"><i @click="prevStep"
                                                class="bi bi-chevron-left"></i><span class="ms-2">Back To
                                                About
                                                Form</span>
                                        </h1>
                                        <button class="btn btn-light font-10" type="button" data-bs-toggle="modal"
                                            data-bs-target="#exampleModal" @click="createForm">
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
                                            <div class="modal-dialog modal-lg">
                                                <div class="modal-content">
                                                    <div class="modal-header">
                                                        <h5 class="modal-title m-0 font-13" id="exampleModalLabel">
                                                            Preview Form
                                                        </h5>
                                                        <button type="button" class="btn-close" data-bs-dismiss="modal"
                                                            aria-label="Close"></button>
                                                    </div>
                                                    <div class="modal-body">
                                                        <div v-if="formCreated">
                                                            <div v-for="(section, sectionIndex) in sections"
                                                                :key="'preview-' + sectionIndex"
                                                                class="preview-section mb-2">
                                                                <h5>{{ section.name }}</h5>
                                                                <div class="row">
                                                                    <div v-for="(column, columnIndex) in section.columns"
                                                                        :key="'column-preview-' + columnIndex"
                                                                        class="col">
                                                                        <div class="mb-3">
                                                                            <div v-for="(field, fieldIndex) in column.fields"
                                                                                :key="'field-preview-' + fieldIndex">
                                                                                <div v-if="field.name">
                                                                                    <!-- Only show field if the name is not empty -->
                                                                                    <label
                                                                                        :for="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex">
                                                                                        {{ field.name }}</label>
                                                                                    <template
                                                                                        v-if="field.type == 'select'">
                                                                                        <select
                                                                                            v-if="field.type === 'select'"
                                                                                            v-model="field.value"
                                                                                            class="form-select mb-2 font-13">
                                                                                            <option
                                                                                                v-for="(option, index) in field.options.split('\n')"
                                                                                                :key="index"
                                                                                                :value="option">
                                                                                                {{ option }}
                                                                                            </option>
                                                                                        </select>
                                                                                    </template>
                                                                                    <template
                                                                                        v-else-if="field.type == 'checkbox' || field.type == 'radio'">
                                                                                        <div class="row">
                                                                                            <div class="form-check col-6 mb-4"
                                                                                                v-for="(option, index) in field.options.split('\n')">
                                                                                                <div
                                                                                                    class="d-flex gap-2 align-items-center">
                                                                                                    <div><label
                                                                                                            class="form-check-label m-0"
                                                                                                            :for="option">
                                                                                                            {{ option }}
                                                                                                        </label></div>
                                                                                                    <div><input class=""
                                                                                                            :type="field.type"
                                                                                                            :name="option"
                                                                                                            :id="option">
                                                                                                    </div>
                                                                                                </div>



                                                                                            </div>
                                                                                        </div>
                                                                                    </template>
                                                                                    <template v-else>
                                                                                        <component
                                                                                            :is="getFieldComponent(field.type)"
                                                                                            v-model="field.value"
                                                                                            :type="field.type"
                                                                                            :name="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex"
                                                                                            :class="form - control">
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
                                                <input v-model="section.name" type="text"
                                                    class="border-less-input font-14" placeholder="Section Name">
                                                <section class="row">
                                                    <div class="d-flex justify-content-end">
                                                        <button v-if="section.columns.length < 3"
                                                            class="btn btn-light bg-transparent border-0 font-13"
                                                            @click="addColumn(sectionIndex)">
                                                            <i class="bi bi-plus"></i> Add Column
                                                        </button>
                                                        <button class="btn btn-light bg-transparent border-0 font-13"
                                                            @click="removeSection(sectionIndex)">
                                                            <i class="bi bi-trash me-2"></i> Delete Section
                                                        </button>
                                                    </div>
                                                    <div class="col">
                                                        <div class="row">
                                                            <div v-for="(column, columnIndex) in section.columns"
                                                                :key="columnIndex" class="col p-0 dynamicColumn">
                                                                <div
                                                                    class="column_name d-flex align-items-center justify-content-end">
                                                                    <button class="btn btn-light btn-sm"
                                                                        @click="removeColumn(sectionIndex, columnIndex)">
                                                                        <i class="bi bi-trash"></i>
                                                                    </button>
                                                                </div>
                                                                <!-- Dynamically added fields within the column -->
                                                                <div v-for="(field, fieldIndex) in column.fields"
                                                                    :key="fieldIndex" class="mt-2">
                                                                    <div class="px-3 py-1 field-border">
                                                                        <div class="d-flex justify-content-between">
                                                                            <input v-model="field.name"
                                                                                placeholder="Field Name"
                                                                                class="border-less-input mb-1 font-14 p-0" />
                                                                            <button class="btn btn-light btn-sm"
                                                                                @click="removeField(sectionIndex, columnIndex, fieldIndex)">
                                                                                <i class="bi bi-trash"></i>
                                                                            </button>
                                                                        </div>
                                                                        <select v-model="field.type"
                                                                            class="form-select mb-2 font-13"
                                                                            @change="onFieldTypeChange(sectionIndex, columnIndex, fieldIndex)">
                                                                            <option value="">Select Type</option>
                                                                            <option v-for="section in fieldTypes"
                                                                                :value="section.type">{{ section.label
                                                                                }}</option>

                                                                        </select>
                                                                        <div
                                                                            v-if="field.type == 'checkbox' || field.type == 'radio' || field.type == 'select'">
                                                                            <label class="font-12  fw-light"
                                                                                for="options">Enter
                                                                                Options:</label>
                                                                            <textarea id="options"
                                                                                placeholder="Enter your Options"
                                                                                v-model="field.options"
                                                                                class="form-control shadow-none mb-1 font-12 ">
                                    </textarea>
                                                                        </div>
                                                                        <div class="d-flex gap-2 align-items-center">

                                                                            <div><input class="font-12"
                                                                                    v-model="field.mandatory"
                                                                                    placeholder="Field Name"
                                                                                    type="checkbox" />
                                                                            </div>
                                                                            <div><label for="mandatory"
                                                                                    class="font-12 m-0 fw-light ">Mandatory</label>
                                                                            </div>


                                                                            <!--- checkbox for mandatory -->
                                                                        </div>
                                                                    </div>
                                                                </div>
                                                                <div
                                                                    class="d-flex justify-content-center align-items-center my-2">
                                                                    <button class="btn btn-light btn-sm fw-bold m-2"
                                                                        @click="addField(sectionIndex, columnIndex)">
                                                                        <i class="bi bi-plus"></i> Add Field
                                                                    </button>
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </section>
                                            </div>
                                            <div class="d-flex justify-content-center align-items-center my-4">
                                                <button class="btn btn-light border font-12" @click="addSection">
                                                    <i class="bi bi-plus-circle me-1 fs-6"></i> Add Section
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>

                        </div>
                    </div>

                    <div>

                    </div>
                </div>
            </div>

        </div>
    </div>
</template>

<script setup>
import FormFields from '../../Components/FormFields.vue';
import ButtonComp from '../../Components/ButtonComp.vue';
import InputComp from '../../Components/InputComp.vue';

import {
    onMounted,
    ref,
    reactive
} from 'vue';
const filterObj = ref({
    name: '',
    code: '',
    dept: '',
    categery: '',
    owner: ''

})

// Current active step
const activeStep = ref(1);

// Form data structure
const form = ref({
    name: '',
    owner: '',
    category: '',
    accessibility: [],
    questions: [], // Array to hold added questions
});
const tableForm = ref(true);
const creatForm = ref(false);
function formCration() {
    tableForm.value = false;
    creatForm.value = true;
}
function cancelForm() {
    tableForm.value = true;
    creatForm.value = false
}
const handleStepClick = (label) => {
    switch (label) {
        case 'About Form':
            prevStep();
            break;
        case 'Questions in Form':
            nextStep();
            break;

    }
};


// New question structure
const newQuestion = ref({
    text: '',
    answerType: 'short', // Default answer type
});

// Dummy data for departments and categories
const departments = ['HR', 'Finance', 'IT', 'Sales'];
const categories = ['Internal', 'External', 'Confidential'];

// List of steps with IDs and labels
const steps = [{
    id: 1,
    label: 'About Form',
    stepno: 'Step 1',
    icon: 'bi bi-info-circle'
},
{
    id: 2,
    label: 'Questions in Form',
    stepno: 'Step 2',
    icon: 'bi bi-question-circle'
},
];

const fieldTypes = [
    {
        label: 'Text',
        type: 'dataText'
    },
    {
        label: 'Checkbox',
        type: 'checkbox'
    },
    {
        label: 'Radio',
        type: 'radio'
    },
    {
        label: 'Attach',
        type: 'file'
    },
    {
        label: 'Number',
        type: 'number'
    },
    {
        label: 'TextArea',
        type: 'textarea'
    },
    {
        label: 'Date',
        type: 'date'
    },
    {
        label: "Select",
        type: 'select'
    }
]


// Save the form as a draft
const saveAsDraft = () => {
    console.log('Form saved as draft:', form.value);
};

// Move to the next step
const nextStep = () => {
    if (activeStep.value < 3) {
        activeStep.value += 1;
    }
};

// Move to the previous step
const prevStep = () => {
    if (activeStep.value > 1) {
        activeStep.value -= 1;
    }
};

// Save the form (final step)
const saveForm = () => {
    console.log('Form data saved:', form.value);
};

// Add a new question to the form
const addQuestion = () => {
    if (newQuestion.value.text) {
        form.value.questions.push({
            ...newQuestion.value
        });
        newQuestion.value.text = ''; // Clear input after adding
        newQuestion.value.answerType = 'short'; // Reset to default
    }
};

// Remove a question from the form
const removeQuestion = (index) => {
    form.value.questions.splice(index, 1);
};
const sections = reactive([]);
const formCreated = ref(false); // To control form preview visibility

// Function to add a new section with a default column
const addSection = () => {
    sections.push({
        name: '', // Initialize section name
        columns: [{
            fields: [] // Initialize with an empty fields array
        }]
    });
};

// Function to remove a section
const removeSection = (sectionIndex) => {
    sections.splice(sectionIndex, 1);
};

// Function to add a new column inside a section
const addColumn = (sectionIndex) => {
    sections[sectionIndex].columns.push({
        fields: []
    });
};

// Function to remove a column inside a section
const removeColumn = (sectionIndex, columnIndex) => {
    sections[sectionIndex].columns.splice(columnIndex, 1);
};

// Function to add a new field inside a column
const addField = (sectionIndex, columnIndex) => {
    sections[sectionIndex].columns[columnIndex].fields.push({
        name: '',
        type: '',
        value: ref(''), // Keeping the value as a ref for reactivity
        options: '',
        mandatory: false
    });
};

// Function to remove a field inside a column
const removeField = (sectionIndex, columnIndex, fieldIndex) => {
    sections[sectionIndex].columns[columnIndex].fields.splice(fieldIndex, 1);
};

// Handle the change of field type to display the correct input
const onFieldTypeChange = (sectionIndex, columnIndex, fieldIndex) => {
    const field = sections[sectionIndex].columns[columnIndex].fields[fieldIndex];
    // Handle additional logic for field type change if needed
    console.log("field === ", field)
    console.log(" sections === ", sections)

};


// Dynamically determine the input field type
const getFieldComponent = (type) => {
    switch (type) {
        case 'dataText':
            return 'input';
        case 'textarea':
            return 'textarea';
        case 'checkbox':
            return 'input'; // Checkbox input will need to handle checked state
        case 'select':
            return 'select'; // Handle options for dropdown separately
        case 'date':
            return 'input'; // Consider using type="date" for HTML5 date input
        case 'radio':
            return 'input';
        default:
            return 'input';
    }
};

// Trigger the creation of form and show the preview
const createForm = () => {
    formCreated.value = true;
};

// Save form data
const saveFormFields = () => {
    // Map through sections and extract field values
    const formData = sections.map(section => ({
        ...section,
        columns: section.columns.map(column => ({
            ...column,
            fields: column.fields.map(field => ({
                name: field.name,
                type: field.type,
                value: field.value.value // Accessing the value property of the ref
            })),
        })),
    }));

    console.log('Form Data:', formData);
};
</script>

<style scoped>
.dynamicSection {
    border: 1px solid #CCCCCC;
    margin-bottom: 20px;
    border-radius: 7px;
    background-color: #EEEEEE;
}

.dynamicColumn {
    border: 1px solid #CCCCCC;
    border-radius: 10px;
    margin: 20px;
    position: relative;
    background-color: #ffffff;
}

.dynamicColumn:hover {
    border: 1px solid rgb(119, 119, 119);

}

.column_name {
    border-bottom: 1px solid #f1f1f1;
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
    border: 1px solid rgb(221, 221, 221);
    border-radius: 10px;
    margin: 5px 10px;
}

.preview-section {
    background-color: #f9f9f9;
    padding: 20px;
    border-radius: 10px;
}

input[type="checkbox"] {
    margin-left: 5px;
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
}

.steps li {
    padding: 10px 20px;
    font-size: 12px;
    cursor: pointer;
    transition: border-color 0.3s ease;
    width: 100%;
}

.steps li.active {
    color: #1B14DF;
    font-weight: bold;
}

.steps li.completed {
    color: #000;

    font-weight: normal;
    opacity: 0.7;
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: block;
    font-size: 13px;
    margin-bottom: 8px;
    font-weight: 600;
}

input,
input::placeholder {
    font: 12px;
}

input,
select {
    width: 100%;
    padding: 10px;
    border: 1px solid #ccc;
    border-radius: 4px;
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
    background-color: #EEEEEE;
    height: 50px;
    border-radius: 7px;

}
</style>
