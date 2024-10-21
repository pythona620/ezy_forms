<template>
    <div>
        <button class="btn btn-light font-13" type="button" data-bs-toggle="modal" data-bs-target="#exampleModal"
            @click="createForm">
            <i class="bi bi-eye me-1"></i>Preview
        </button>
        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
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
                            <div class="card p-1">
                                <div v-for="(section, sectionIndex) in sections" :key="'preview-' + sectionIndex"
                                    class="preview-section mb-2">
                                    <h5>{{ section.label }}</h5>
                                    <div class="row" v-for="(row, rowIndex) in section.rows" :key="rowIndex">
                                        <div v-for="(column, columnIndex) in row.columns"
                                            :key="'column-preview-' + columnIndex" class="col">
                                            <h6>{{ column.label }}</h6>
                                            <div class="mb-2 ms-2">
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
                                                        <template v-if="field.fieldtype == 'Select' ||
                field.fieldtype == 'multiselect'
                ">
                                                            <select :multiple="field.fieldtype == 'multiselect'
                " v-model="field.value" class="form-select mb-2 font-13">
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
                                                      ) in field.options.split('\n')" :key="index">
                                                                    <div class="d-flex gap-2 align-items-center">
                                                                        <div>
                                                                            <input class="" :type="field.fieldtype"
                                                                                :name="option" :id="option" />
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
                                                            <component :is="getFieldComponent(field.fieldtype)"
                                                                v-model="field.value" :type="field.fieldtype" :name="'field-' +
                sectionIndex +
                '-' +
                columnIndex +
                        '-' +
                        fieldIndex
                        " :class="form - control" class="form-control previewInputHeight">
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
    </div>
</template>

<script setup>
import { defineProps } from "vue";


const props = defineProps({
    sections: {
        type: Array,
        required: true,
    }
});


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

<style lang="sass" scoped>

</style>