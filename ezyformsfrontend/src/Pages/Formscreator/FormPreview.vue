<template>
    <div>
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
                            <div class=" card p-1 mb-2">
                                <div class=" container">
                                    <div class="row">

                                        <div class="col">
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
                                                        <span class="font-12 fw-bold">
                                                            {{ $props.formDescriptions.accessible_departments }}
                                                        </span>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="card p-1">
                                <div v-for="(blockItem, blockIndex) in blockArr ">
                                    <div v-for="(section, sectionIndex) in blockItem.sections" :key="'preview-' + sectionIndex"
                                        class="preview-section m-2">
                                        <h5>{{ section.label || '-' }}</h5>
                                        <div class=" container-fluid">
                                            <div class="row" v-for="(row, rowIndex) in section.rows" :key="rowIndex">
                                                <div v-for="(column, columnIndex) in row.columns"
                                                    :key="'column-preview-' + columnIndex" class="col">
                                                    <h6>{{ column.label || '-' }}</h6>
                                                    <div class="mb-2 ms-2">
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

                                                                    <span class=" font-12">{{ field.label
                                                                        }}</span></label>
                                                                <template v-if="field.fieldtype == 'Select' ||
                                                                    field.fieldtype == 'multiselect'
                                                                ">
                                                                    <select :multiple="field.fieldtype == 'multiselect'
                                                                        " v-model="field.value"
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
                                                                        <div class="form-check col-4 mb-4" v-for="(
                                                        option, index
                                                      ) in field?.options?.split('\n')" :key="index">
                                                                            <div
                                                                                class="d-flex gap-2 align-items-center">
                                                                                <div>
                                                                                    <input class=""
                                                                                        :type="field.fieldtype"
                                                                                        :name="option" :id="option"
                                                                                        readonly />
                                                                                </div>
                                                                                <div>
                                                                                    <label class="form-check-label m-0"
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
                                                                    <component readonly
                                                                        :is="getFieldComponent(field.fieldtype)"
                                                                        v-model="field.value" :type="field.fieldtype"
                                                                        :name="'field-' +
                                                                            sectionIndex +
                                                                            '-' +
                                                                            columnIndex +
                                                                            '-' +
                                                                            fieldIndex
                                                                            " class="form-control previewInputHeight">
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
</template>

<script setup>
import { defineProps, watch } from "vue";

const props = defineProps({
    blockArr:{
        type: [Array, null],
        required: true
    },
    sections: {
        type: [Array, null],
        required: true,
    },
    formDescriptions: {
        type: Object,
        required: true,
    },
});

// Watch for changes in formDescriptions
watch(
    () => props.formDescriptions,
    (newVal) => {
        console.log("Updated formDescriptions in child:", newVal);
    },
    { deep: true } // Enables deep watching for nested object changes
);
const getFieldComponent = (type) => {
    switch (type) {
        case "Data":
            return "input";
        case "number":
            return "input";
        case "Text":
            return "textarea";
        case "checkbox":
            return "input";
        case "Select":
            return "select";
        case "Date":
            return "input";
        case "Attach":
            return "file";
        case "radio":
            return "input";
        default:
            return "input";
    }
};
</script>

<style scoped>
.previewInputHeight {
    height: 35px;
    margin-bottom: 5px;
}
</style>