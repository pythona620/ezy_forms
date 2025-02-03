<template>
    <section>
        <div v-if="filteredBlocks.length" class="card">
            <div v-for="(block, blockIndex) in filteredBlocks" :key="blockIndex" class="block-container">
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
                                            v-else-if="field.fieldtype === 'Check' || field.fieldtype === 'radio'">
                                            <div class="container-fluid">
                                                <div class="row">
                                                    <div class="form-check col-4 mb-4"
                                                        v-for="(option, index) in field?.options?.split('\n')"
                                                        :key="index">
                                                        <div>
                                                            <input v-if="field.fieldtype === 'Check'"
                                                                class="form-check-input" type="checkbox"
                                                                :checked="field.value === 1" :value="field.value"
                                                                disabled
                                                                :name="`${field.fieldtype}-${blockIndex}-${sectionIndex}-${rowIndex}-${columnIndex}-${fieldIndex}`"
                                                                :id="`${option}-${index}`"
                                                                @blur="(event) => logFieldValue(event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)" />

                                                            <input v-else-if="field.fieldtype === 'radio'" disabled
                                                                class="form-check-input" type="radio"
                                                                :name="`${field.fieldtype}-${blockIndex}-${sectionIndex}-${rowIndex}-${columnIndex}-${fieldIndex}`"
                                                                :id="`${option}-${index}`" :value="field.value"
                                                                :checked="field.value === 1"
                                                                @blur="(event) => logFieldValue(event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)" />
                                                        </div>
                                                        <div>
                                                            <label class="form-check-label m-0"
                                                                :for="`${option}-${index}`">
                                                                {{ option }}
                                                            </label>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </template>

                                        <!-- Field Type File (Attach) -->
                                        <!-- <template v-else-if="field.fieldtype == 'Attach'">
                                            <input type="file"
                                                :id="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex"
                                                class="form-control previewInputHeight" disabled
                                                @change="logFieldValue($event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)" />
                                            <iframe :src="field.value" type="application/pdf" width="100%"
                                                height="300px">
                                                Your Browser Do not support pdf
                                            </iframe>

                                        </template> -->
                                        <template v-else-if="field.fieldtype == 'Attach'">
                                            <div class=" container">
                                                <div class="row">
                                                    <div class="col-3 card file-cards m-1"
                                                        v-for="(filePath, index) in filePaths" :key="index">
                                                        <div class="card-body p-2">
                                                            <div
                                                                class="d-flex gap-1 align-items-center justify-content-between">
                                                                <div>
                                                                    <i class="bi bi-file-earmark-text"></i>
                                                                    <span class="font-12 fw-bold ps-1">
                                                                        {{ `File ${index + 1}` }}
                                                                    </span>
                                                                </div>
                                                                <i title="view file" class="bi bi-eye"
                                                                    @click="openFile(filePath)"></i>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </template>
                                        <template v-else-if="field.fieldtype == 'Datetime'">
                                            <input type="datetime-local" v-model="field.value"
                                                :placeholder="'Enter ' + field.label" :value="field.value"
                                                :name="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex"
                                                class="form-control previewInputHeight" />
                                        </template>

                                        <!-- Field Type Default -->
                                        <template v-else>
                                            <component :is="getFieldComponent(field.fieldtype)" :value="field.value"
                                                :type="field.fieldtype" :readOnly="blockIndex === 0"
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
import { computed, defineProps, onMounted, ref, watch } from 'vue';

const props = defineProps({
    blockArr: {
        type: [Array, null],
        required: true,
    },
    currentLevel: {
        type: String,
        // required: true,
    }
});


const emit = defineEmits();
const filePaths = ref([]);


const filteredBlocks = computed(() => {
    if (!props.blockArr || props.blockArr.length === 0) return [];

    // Always include the first block (Requestor Block)
    const filtered = [props.blockArr[0]];

    // Include approver blocks based on the current level
    for (let i = 1; i <= props.currentLevel; i++) {
        if (props.blockArr[i]) {
            filtered.push(props.blockArr[i]);
        }
    }
    return filtered;
});

// Get all fields data
const getAllFieldsData = () => {
    const fieldsData = [];
    filteredBlocks.value.forEach(block => {
        block.sections?.forEach(section => {
            section.rows?.forEach(row => {
                row.columns?.forEach(column => {
                    column.fields?.forEach(field => {
                        fieldsData.push({ ...field });
                        if (field.fieldtype === 'Attach' && field.value) {
                            filePaths.value = field.value.split(',').map(path => path.trim());
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
    window.open(fileUrl, '_blank');
};

onMounted(() => {
    emit('updateField', getAllFieldsData());
});

watch(
    () => props.blockArr,
    () => {
        emit('updateField', getAllFieldsData());
    },
    { deep: true }
);


const getFieldComponent = (type) => {
    switch (type) {
        case "Data":
            return "input";
        case "number":
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
            return "select";
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


const logFieldValue = (event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex) => {
    const field = props.blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex];
    field.value = event.target.value;
    emit('updateField', getAllFieldsData());
    // console.log('Field Value Updated:', field);
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
    background-color: #f5f5f5;
}

input::-webkit-input-placeholder {
    font-size: 10px;

}

.file-cards {
    transition: all 0.1s ease-in-out;
}

.file-cards:hover {
    box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px, rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;
}
</style>