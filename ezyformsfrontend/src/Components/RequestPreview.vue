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
                                                <span class="ms-1 text-danger">{{ field.reqd
            === 1 ? '*' : ''
                                                    }}</span>
                                            </label>
                                        </div>

                                        <template
                                            v-if="field.fieldtype === 'Select' || field.fieldtype === 'multiselect'">
                                            <select :multiple="field.fieldtype === 'multiselect'" v-model="field.value"
                                                @input="logFieldValue(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)"
                                                class="form-select mb-2 font-13">
                                                <option v-for="(option, index) in field.options?.split('\n')"
                                                    :key="index" :value="option">
                                                    {{ option }}
                                                </option>
                                            </select>
                                        </template>

                                        <template
                                            v-else-if="field.fieldtype === 'check' || field.fieldtype === 'radio'">
                                            <div class="row">
                                                <div class="form-check col-4 mb-4"
                                                    v-for="(option, index) in field?.options?.split('\n')" :key="index">
                                                    <div class="d-flex gap-2 align-items-center">
                                                        <div>
                                                            <input :type="field.fieldtype" :name="option" :id="option"
                                                                v-model="field.value"
                                                                @blur="(event) => logFieldValue(event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)" />
                                                        </div>
                                                        <div>
                                                            <label class="form-check-label m-0" :for="option">{{ option
                                                                }}</label>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </template>
                                        <template v-else-if="field.fieldtype == 'Attach'">
                                            <input type="file"
                                                :id="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex"
                                                class="form-control previewInputHeight"
                                                @change="logFieldValue($event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)" />
                                        </template>


                                        <template v-else>
                                            <component :is="getFieldComponent(field.fieldtype)" v-model="field.value"
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
import { defineProps } from "vue";

const props = defineProps({
    blockArr: {
        type: [Array, null],
        required: true
    },
});
const emit = defineEmits();
const getFieldComponent = (type) => {
    switch (type) {
        case "Data":
            return "input";
        case "number":
            return "input";
        case "Text":
            return "textarea";
        case "Check":
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


const logFieldValue = (eve, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex) => {
    const field = props.blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex];
    field['value'] = eve.target.value
    emit('updateField',
        field
        // blockIndex,
        // sectionIndex,
        // rowIndex,
        // columnIndex,
        // fieldIndex,
        // value: field,  // Send the updated field value
    );
    //   console.log(`Block: ${blockIndex}, Section: ${sectionIndex}, Row: ${rowIndex}, Column: ${columnIndex}, Field: ${fieldIndex}`);
    console.log(eve.target.value, "Field Value:", field);

};
// const handleFileChange = (event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex) => {
//     const file = event.target.files[0]; // Get the first file selected
//     if (file) {
//         const field = props.blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex];
//         field.value = file.name; // Store the file name in the field's value
//         emit('updateField', field); // Emit the updated field to the parent
//         console.log("Selected file:", file.name);
//     }
// };

</script>
<style setup>
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
    background-color: #eeeeee;
}

input::-webkit-input-placeholder {
    font-size: 10px;

}
</style>