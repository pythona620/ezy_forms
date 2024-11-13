<template>
    <section>
        <div v-if="blockArr" class="card">
            <div v-for="(block, blockIndex) in blockArr" :key="blockIndex" class="block-container">
                <div v-for="(section, sectionIndex) in block.sections" :key="'preview-' + sectionIndex"
                    class="preview-section m-2">
                    <div class="section-label">
                        <h5 class="m-0 font-13">{{ section.label || 'Untitled Section' }}</h5>
                    </div>
                    <div class="container-fluid">
                        <div class="row" v-for="(row, rowIndex) in section.rows" :key="rowIndex">
                            <div v-for="(column, columnIndex) in row.columns" :key="'column-preview-' + columnIndex"
                                class="col dynamicColumn">
                                <div class="p-3 border-bottom">
                                    <h6 class="m-0 font-12">{{ column.label || '-' }}</h6>
                                </div>
                                <div class="mx-3 my-2">
                                    <div v-for="(field, fieldIndex) in column.fields"
                                        :key="'field-preview-' + fieldIndex">
                                        <div v-if="field.label">
                                            <label
                                                :for="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex">
                                                <span class="font-12">{{ field.label }}</span>
                                                <span class="ms-1 text-danger">{{ field.reqd === 1 ? '*' : '' }}</span>
                                            </label>
                                        </div>

                                        <!-- Field Type Select or Multiselect -->
                                        <template
                                            v-if="field.fieldtype === 'Select' || field.fieldtype === 'multiselect'">
                                            <select :multiple="field.fieldtype === 'multiselect'" :value="field.value"
                                                @input="logFieldValue(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)"
                                                class="form-select mb-2 font-13">
                                                <option v-for="(option, index) in field.options?.split('\n')"
                                                    :key="index" :value="option">
                                                    {{ option }}
                                                </option>
                                            </select>
                                        </template>

                                        <!-- Field Type Check or Radio -->
                                        <template
                                            v-else-if="field.fieldtype === 'check' || field.fieldtype === 'radio'">
                                            <div class="row">
                                                <div class="form-check col-4 mb-4"
                                                    v-for="(option, index) in field?.options?.split('\n')" :key="index">
                                                    <div class="d-flex gap-2 align-items-center">
                                                        <input :type="field.fieldtype" :name="option" :id="option"
                                                            :value="field.value"
                                                            @blur="(event) => logFieldValue(event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)" />
                                                        <label class="form-check-label m-0" :for="option">{{ option
                                                            }}</label>
                                                    </div>
                                                </div>
                                            </div>
                                        </template>

                                        <!-- Field Type File (Attach) -->
                                        <template v-else-if="field.fieldtype == 'Attach'">
                                            <input type="file"
                                                :id="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex"
                                                class="form-control previewInputHeight"
                                                @change="logFieldValue($event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)" />
                                        </template>

                                        <!-- Field Type Default -->
                                        <template v-else>
                                            <component :is="getFieldComponent(field.fieldtype)" :value="field.value"
                                                :type="field.fieldtype"
                                                :name="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex"
                                                @blur="(event) => logFieldValue(event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)"
                                                class="form-control previewInputHeight"></component>
                                        </template>
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
import { defineProps, onMounted, watch } from 'vue';

const props = defineProps({
    blockArr: {
        type: [Array, null],
        required: true,
    },
});
const emit = defineEmits();

const getAllFieldsData = () => {
    const fieldsData = [];

    // Iterate through blockArr to extract fields data with null checks
    props.blockArr?.forEach(block => {
        block.sections?.forEach(section => {
            section.rows?.forEach(row => {
                row.columns?.forEach(column => {
                    column.fields?.forEach(field => {
                        fieldsData.push({ ...field });
                    });
                });
            });
        });
    });

    return fieldsData;
};


// Emit all fields' data when component is mounted
onMounted(() => {
    emit('updateField', getAllFieldsData());
});

// Watch for any changes in blockArr and emit the updated fields
watch(
    () => props.blockArr,
    () => {
        emit('updateField', getAllFieldsData());
    },
    { deep: true }
);

// Function to dynamically get the field component based on field type
const getFieldComponent = (type) => {
    switch (type) {
        case 'Data':
        case 'number':
        case 'Text':
        case 'Check':
        case 'Date':
        case 'radio':
            return 'input';
        case 'Attach':
            return 'file';
        case 'Select':
            return 'select';
        default:
            return 'input';
    }
};

// Function to log the field value on change or blur
const logFieldValue = (event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex) => {
    const field = props.blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex];
    field.value = event.target.value;

    // Emit all fields' data after any field change
    emit('updateField', getAllFieldsData());
    console.log('Field Value Updated:', field);
};
</script>

<style setup>
.previewInputHeight {
    height: 35px;
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
    box-shadow: 0px 4px 4px 0px #0000000D;
    padding: 18px 12px;
    font-weight: 500;
    font-size: 15px;
}

.block-container {
    background-color: #eeeeee;
}

input::-webkit-input-placeholder {
    font-size: 10px;

}
</style>