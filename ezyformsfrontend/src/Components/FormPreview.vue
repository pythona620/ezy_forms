<template>
    <!-- <div> -->
    <!-- <button class="btn btn-light font-10 border" type="button" data-bs-toggle="modal" data-bs-target="#exampleModal"
            @click="createForm">
            <i class="bi bi-eye me-1"></i>Preview
        </button> -->
    <div class="modal fade" id="formViewModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog modal-xl">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title m-0 font-13" id="exampleModalLabel">
                        Preview Form
                    </h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <div>
                        <div class=" card py-1 mb-2 description-div">
                            <div class=" container">
                                <div class="row">
                                    <div class="col p-0">
                                        <div class="container">
                                            <div class="row">
                                                <div class="col-3">
                                                    <div class=" d-flex align-items-center justify-content-between">
                                                        <span class="font-10">
                                                            Form Name
                                                        </span>
                                                        <span class=" text-right">:</span>
                                                    </div>
                                                </div>
                                                <div class="col-9">
                                                    <span class=" font-12 fw-bold">
                                                        {{ $props.formDescriptions.form_name || "Untitled" }}
                                                    </span>
                                                </div>
                                                <div class="col-3">
                                                    <div class=" d-flex align-items-center justify-content-between">
                                                        <span class="font-10">
                                                            Form Short Code
                                                        </span>
                                                        <span class=" text-right">:</span>
                                                    </div>
                                                </div>
                                                <div class="col-9">
                                                    <span class="font-12 fw-bold">
                                                        {{ $props.formDescriptions.form_short_name }}
                                                    </span>
                                                </div>
                                                <div class="col-3">
                                                    <div class=" d-flex align-items-center justify-content-between">
                                                        <span class="font-10">
                                                            Form category
                                                        </span>
                                                        <span class=" text-right">:</span>
                                                    </div>
                                                </div>
                                                <div class="col-9">
                                                    <span class="font-12 fw-bold">
                                                        {{ $props.formDescriptions.form_category }}
                                                    </span>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col">
                                        <div class=" container">
                                            <div class="row">
                                                <div class="col-6">
                                                    <div class=" d-flex align-items-center justify-content-between">
                                                        <span class="font-10">
                                                            Owner of the form
                                                        </span>
                                                        <span class=" text-right">:</span>
                                                    </div>
                                                </div>
                                                <div class="col-6">
                                                    <span class="font-12 fw-bold">
                                                        {{ $props.formDescriptions.owner_of_the_form }}

                                                    </span>
                                                </div>
                                                <div class="col-6">
                                                    <div class=" d-flex align-items-center justify-content-between">
                                                        <span class="font-10">
                                                            Accessibility to departments
                                                        </span>
                                                        <span class=" text-right">:</span>
                                                    </div>
                                                </div>
                                                <div class="col-6">
                                                    <span class="font-12 fw-bold ">
                                                        <template
                                                            v-if="Array.isArray(props.formDescriptions.accessible_departments) && props.formDescriptions.accessible_departments.length === 1">
                                                            {{ props.formDescriptions.accessible_departments[0] }}
                                                        </template>
                                                        <template
                                                            v-else-if="Array.isArray(props.formDescriptions.accessible_departments) && props.formDescriptions.accessible_departments.length > 1">
                                                            <ul class=" p-0 mb-0 list-unstyled mt-1">
                                                                <li v-for="(department, index) in props.formDescriptions.accessible_departments"
                                                                    :key="index">
                                                                    {{ department }},
                                                                </li>
                                                            </ul>
                                                        </template>
                                                        <template v-else>
                                                            {{ props.formDescriptions.accessible_departments }}
                                                        </template>
                                                    </span>
                                                </div>

                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="card border-0 ">
                            <div class="accordion" id="blockAccordion">
                                <div v-for="(blockItem, blockIndex) in blockArr" :key="blockIndex"
                                    class="accordion-item">
                                    <h2 class="accordion-header " :id="'heading-' + blockIndex">
                                        <button class="accordion-button  d-flex justify-content-between" type="button"
                                            data-bs-toggle="collapse" :data-bs-target="'#collapse-' + blockIndex"
                                            aria-expanded="true" :aria-controls="'collapse-' + blockIndex">
                                            {{ blockIndex === 0 ? 'Requestor' : 'Approver' }}

                                        </button>
                                    </h2>

                                    <div :id="'collapse-' + blockIndex" class="accordion-collapse collapse"
                                        :class="{ show: blockIndex === 0 }" aria-labelledby="'heading-' + blockIndex"
                                        data-bs-parent="#blockAccordion">
                                        <div class="accordion-body block-container">
                                            <div v-for="(section, sectionIndex) in blockItem.sections"
                                                :key="'preview-' + sectionIndex" class="preview-section">
                                                <div class="section-label d-flex justify-content-between">
                                                    <h5 class="m-0 font-13">{{ section.label || 'Untitled Section' }}
                                                    </h5>
                                                    <div>
                                                        <!-- Displaying roles based on workflowRoles -->
                                                        <span class="font-12" v-if="workFlowRoles.length > 0">
                                                            Role : <b>{{ workFlowRoles[blockIndex]?.roles?.join(', ')
                                                            || 'No Role' }}</b>
                                                        </span>
                                                    </div>
                                                </div>
                                                <div class="px-2">
                                                    <div class="container-fluid">
                                                        <div class="row" v-for="(row, rowIndex) in section.rows"
                                                            :key="rowIndex">
                                                            <div v-for="(column, columnIndex) in row.columns"
                                                                :key="'column-preview-' + columnIndex"
                                                                class="col dynamicColumn">
                                                                <div class="p-3 border-bottom">
                                                                    <h6 class="m-0 font-12">{{ column.label || '-' }}
                                                                    </h6>
                                                                </div>
                                                                <div class="mx-3 my-2">
                                                                    <div v-for="(field, fieldIndex) in column.fields"
                                                                        :key="'field-preview-' + fieldIndex">
                                                                        <div v-if="field.label">
                                                                            <label
                                                                                :for="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex">
                                                                                <span class="font-12">{{ field.label
                                                                                    }} </span>
                                                                                <span class="ms-1 text-danger">{{
                                                            field.reqd
                                                                === 1 ? '*' : ''
                                                        }}</span>

                                                                            </label>
                                                                            <template
                                                                                v-if="field.fieldtype == 'Select' || field.fieldtype == 'multiselect'">
                                                                                <select
                                                                                    :multiple="field.fieldtype == 'multiselect'"
                                                                                    :placeholder="'Select ' + field.label"
                                                                                    v-model="field.value"
                                                                                    class="form-select mb-2 font-13">
                                                                                    <option
                                                                                        v-for="(option, index) in field.options?.split('\n')"
                                                                                        :key="index" :value="option">
                                                                                        {{ option }}
                                                                                    </option>
                                                                                </select>
                                                                            </template>
                                                                            <template
                                                                                v-else-if="field.fieldtype == 'Check' || field.fieldtype == 'radio'">
                                                                                <div class="container-fluid">
                                                                                    <div class="row">
                                                                                        <div class="form-check col-4 mb-4"
                                                                                            v-for="(option, index) in field?.options?.split('\n')"
                                                                                            :key="index">
                                                                                            <div
                                                                                                class="d-flex gap-2 align-items-center">
                                                                                                <div>
                                                                                                    <input
                                                                                                        class=" form-check-input"
                                                                                                        :type="field.fieldtype"
                                                                                                        :name="option"
                                                                                                        :id="option"
                                                                                                        readonly />
                                                                                                </div>
                                                                                                <div>
                                                                                                    <label
                                                                                                        class="form-check-label m-0"
                                                                                                        :for="option">
                                                                                                        {{ option }}
                                                                                                    </label>
                                                                                                </div>
                                                                                            </div>
                                                                                        </div>
                                                                                    </div>
                                                                                </div>
                                                                            </template>
                                                                            <template
                                                                                v-else-if="field.fieldtype == 'Attach'">
                                                                                <input type="file"
                                                                                    :id="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex"
                                                                                    class="form-control previewInputHeight"
                                                                                    @change="handleFileChange($event, field)"
                                                                                    disabled />
                                                                            </template>
                                                                            <template v-else>
                                                                                <input
                                                                                    v-if="field.fieldtype === 'Datetime'"
                                                                                    type="datetime-local"
                                                                                    v-model="field.value"
                                                                                    :placeholder="'Enter ' + field.label"
                                                                                    :name="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex"
                                                                                    class="form-control previewInputHeight" />

                                                                                <component readOnly
                                                                                    :is="getFieldComponent(field.fieldtype)"
                                                                                    v-model="field.value"
                                                                                    :type="field.fieldtype"
                                                                                    :placeholder="'Enter ' + field.label"
                                                                                    :name="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex"
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
                                    </div>
                                </div>
                            </div>

                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>
    <!-- </div> -->
</template>

<script setup>
import { defineProps, watch, ref } from "vue";

const props = defineProps({
    blockArr: {
        type: [Array, null],
        required: true
    },

    formDescriptions: {
        type: Object,
        required: true,
    },
});
const workFlowRoles = ref([]);

watch(
    () => props.formDescriptions,
    (newVal) => {
        console.log("Updated formDescriptions in child:", newVal);

        if (newVal && newVal.form_json) {
            try {
                workFlowRoles.value = JSON.parse(newVal.form_json).workflow || [];
            } catch (e) {
                console.error("Error parsing form_json:", e);
            }
        }

        console.log(workFlowRoles.value, "============");
    },
    { deep: true }
);


const getFieldComponent = (type) => {
    switch (type) {
        case "Data":
        case "number":
        case "Check":
        case "Date":
        case "Datetime":
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
</script>

<style scoped>
.previewInputHeight {
    height: 35px;
    margin-bottom: 5px;
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
    box-shadow: 0px 4px 4px 0px #0000000D;
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
    background-color: #eeeeee;
    overflow-y: scroll;
    overflow-x: hidden;
    height: 40vh;

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
</style>