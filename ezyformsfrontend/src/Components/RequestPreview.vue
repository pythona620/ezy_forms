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
                                <div v-if="column.label" class="p-2 border-bottom">
                                    <h6 class="m-0 font-12">{{ column.label }}</h6>
                                </div>
                                <div class="mx-3 my-2">
                                    <div v-for="(field, fieldIndex) in column.fields"
                                        :key="'field-preview-' + fieldIndex">
                                        <div v-if="field.fieldtype !== 'Table'">
                                            <div v-if="field.label">
                                                <label :for="'field-' +
                                                    sectionIndex +
                                                    '-' +
                                                    columnIndex +
                                                    '-' +
                                                    fieldIndex
                                                    ">
                                                    <span class="font-12" :class="field.fieldtype === 'Small Text' ? 'fw-bold': ''">{{ field.label }}</span>
                                                    <span class="ms-1 text-danger">{{
                                                        field.reqd === 1 ? "*" : ""
                                                        }}</span>
                                                </label>
                                            </div>

                                            <template v-if="
                                                field.fieldtype === 'Select' ||
                                                field.fieldtype === 'Table MultiSelect'
                                            ">
                                                <!-- <select :multiple="field.fieldtype === 'Table MultiSelect'"
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
                                                </select> -->
                                                <Multiselect :multiple="field.fieldtype === 'Table MultiSelect'"
                                                    :maxlength="getMaxLength(field)"
                                                    :options="field.options?.split('\n') || []"
                                                    :modelValue="field.value" placeholder="Select"
                                                    @update:modelValue="(val) => handleSelectChange(val, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)"
                                                    class="font-11 multiselect" />


                                            </template>

                                            <template v-else-if="
                                                field.fieldtype === 'Check' ||
                                                field.fieldtype === 'radio' || field.fieldtype === 'Small Text'
                                            ">
                                                <div class="container-fluid">
                                                    <div class="row">
                                                        <div class="form-check col-4 mb-1" v-for="(option, index) in field?.options?.split(
                                                            '\n'
                                                        )" :key="index" :class="{ 'd-none': index === 0 }">
                                                            <div>
                                                                <input v-if="
                                                                    field.fieldtype === 'Check' || field.fieldtype === 'Small Text' && index !== 0
                                                                " class="form-check-input" type="checkbox"
                                                                    :value="option"
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
                                                                    :id="`${option}-${index}`" :value="field.value"
                                                                    @change="
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
                                                <input :disabled="props.readonlyFor === 'true'" type="file"
                                                    accept="image/jpeg,image/png,application/pdf"
                                                    :id="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex"
                                                    class="form-control previewInputHeight font-10 mt-2" multiple
                                                    @change="
                                                        logFieldValue(
                                                            $event,
                                                            blockIndex,
                                                            sectionIndex,
                                                            rowIndex,
                                                            columnIndex,
                                                            fieldIndex
                                                        )
                                                        " />
                                                <div v-if="field.value" class="d-flex flex-wrap gap-2">
                                                    <div v-for="(fileUrl, index) in field.value.split(',').map(f => f.trim())"
                                                        :key="index" class="position-relative d-inline-block"
                                                        @mouseover="hovered = index" @mouseleave="hovered = null">
                                                        <!-- Show image thumbnail -->
                                                        <img v-if="isImageFile(fileUrl)" :src="fileUrl"
                                                            class="img-thumbnail mt-2 cursor-pointer border-0"
                                                            style="max-width: 100px; max-height: 100px" />

                                                        <!-- Show PDF icon if not image -->
                                                        <div v-else
                                                            class="d-flex align-items-center justify-content-center border mt-2"
                                                            style="width: 100px; height: 100px; background: #f9f9f9">
                                                            <i class="bi bi-file-earmark-pdf fs-1 text-danger"></i>
                                                        </div>

                                                        <!-- Remove icon -->
                                                        <button v-if="hovered === index"
                                                            @click="removeFile(index, field)"
                                                            class="btn btn-sm btn-light position-absolute"
                                                            style="top: 2px; right: 5px; border-radius: 50%; padding: 0 5px">
                                                            <i class="bi bi-x fs-6"></i>
                                                        </button>
                                                    </div>
                                                </div>

                                                <!-- File input for uploading -->

                                            </template>

                                            <template v-else-if="field.fieldtype == 'Datetime'">
                                                <input type="datetime-local" :value="field.value"  :min="new Date().toISOString().slice(0, 16)"
                                                    @click="forceOpenCalendar" ref="datetimeInput"
                                                    :placeholder="'Enter ' + field.label" :name="'field-' +
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
                                            <template v-else-if="field.fieldtype == 'Link'">
                                                <input type="text" :value="field.value"
                                                    @input="(e) => onInputChange(e.target.value, field)" @change="(event) =>
                                                        logFieldValue(
                                                            event,
                                                            blockIndex,
                                                            sectionIndex,
                                                            rowIndex,
                                                            columnIndex,
                                                            fieldIndex
                                                        )" class="form-control font-12 mb-1"
                                                    @focus="() => setActiveField(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex, field)" />

                                                <ul v-if="isActiveField(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex) && linkSearchResults.length"
                                                    class="list-group mt-1"
                                                    style="max-height: 200px; overflow-y: auto;">
                                                    <li v-for="(result, index) in linkSearchResults" :key="index"
                                                        @click="selectDoctype(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex, result.name)"
                                                        class="list-group-item list-group-item-action">
                                                        {{ result.name }}
                                                    </li>
                                                </ul>
                                            </template>


                                            <template v-else>
                                                <!-- <input v-if="field.fieldtype === 'Datetime'" type="datetime-local"
                                                @click="forceOpenCalendar" ref="datetimeInput" :value="field.value"
                                                class="form-control previewInputHeight font-10" /> -->
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
                                                    <!-- :max="currentdate" -->
                                                <component v-if="
                                                    field.fieldtype !== 'Datetime' && field.fieldtype !== 'Text' 
                                                " :is="getFieldComponent(field.fieldtype)" :value="field.value" :min="past"
                                                     @click="forceOpenCalendar"
                                                    :maxlength="getMaxLength(field)"
                                                    :type="getInputType(field.fieldtype)" :name="'field-' +
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
                                            <span v-if="field.description !== 'Field'" class="font-11"><span
                                                    class="fw-semibold">Description: </span>{{
                                                        field.description }}</span>
                                        </div>
                                        <div v-if="blockIndex === 0 && field.fieldtype === 'Table'">

                                            <div v-if="field.fieldtype === 'Table' && field.description === 'true'">

                                                <div v-for="(table, tableIndex) in props.tableHeaders" :key="tableIndex"
                                                    class="mt-3">
                                                    <div v-if="tableIndex === field.options">
                                                        <div>
                                                            <span class="font-13  fw-medium">{{
                                                                tableIndex.replace(/_/g, " ") }}</span>
                                                        </div>

                                                        <div v-if="!tableRows[tableIndex] || tableRows[tableIndex].length === 0"
                                                            class="text-center text-muted">
                                                            <div class="d-flex flex-column align-items-center">
                                                                <i class="bi bi-card-list fs-3 mb-2"></i>
                                                                <span>No Data</span>
                                                            </div>
                                                        </div>

                                                        <!-- Block View -->
                                                        <div v-for="(row, rowIndex) in tableRows[tableIndex]"
                                                            :key="rowIndex"
                                                            class="border p-3 mb-3 rounded bg-light-subtle">
                                                            <div
                                                                class="d-flex justify-content-between align-items-center mb-2">
                                                                <span>Block {{ rowIndex + 1 }}</span>
                                                                <span class="text-danger cursor-pointer"
                                                                    @click="removeRow(tableIndex, rowIndex)">
                                                                    <i class="bi bi-x-lg"></i>
                                                                </span>
                                                            </div>

                                                            <div v-for="i in Math.ceil(table.length / 2)" :key="i"
                                                                class="row mb-2">
                                                                <div class="col-6"
                                                                    v-for="fieldItem in table.slice((i - 1) * 2, i * 2)"
                                                                    :key="fieldItem.fieldname">
                                                                    <label class="font-12 fw-medium">{{
                                                                        fieldItem.label
                                                                    }}</label>

                                                                    <input v-if="fieldItem.fieldtype === 'Data'"
                                                                        :title="row[fieldItem.fieldname]" type="text"
                                                                        class="form-control font-12 px-2"
                                                                        :maxlength="fieldItem.fieldtype === 'Phone' ? '10' : '140'"
                                                                        v-model="row[fieldItem.fieldname]" />

                                                                    <input v-else-if="fieldItem.fieldtype === 'Date'" :min="past"
                                                                        :max="today" :title="row[fieldItem.fieldname]"
                                                                        type="date" class="form-control font-12"
                                                                        v-model="row[fieldItem.fieldname]" />

                                                                    <input
                                                                        v-else-if="fieldItem.fieldtype === 'Datetime'"
                                                                        :title="row[fieldItem.fieldname]"
                                                                        type="datetime-local"
                                                                        class="form-control font-12"
                                                                        v-model="row[fieldItem.fieldname]" />
                                                                    <!-- <template v-else-if="fieldItem.fieldtype === 'Data' && row[fieldItem.fieldname] === 'Type of Manpower'">
                                                                            <Multiselect :multiple="field.fieldtype === 'Table MultiSelect'"
                                                    :maxlength="getMaxLength(field)"
                                                    :options="field.options?.split('\n') || []"
                                                    :modelValue="field.value" placeholder="Select"
                                                    @update:modelValue="(val) => handleSelectChange(val, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)"
                                                    class="font-11 multiselect" />
                                                                        </template> -->

                                                                    <input v-else-if="fieldItem.fieldtype === 'Attach'"
                                                                        type="file" class="form-control font-12"
                                                                        @change="handleFileUpload($event, row, fieldItem.fieldname)" />
                                                                </div>
                                                            </div>

                                                        </div>

                                                        <!-- Add Block Button -->
                                                        <div class="text-center">
                                                            <button
                                                                class="btn btn-outline-light text-secondary addRow-btn fw-medium btn-sm font-12"
                                                                @click="addRow(tableIndex)">
                                                                Add Block
                                                            </button>
                                                        </div>

                                                        <!-- <span v-if="field.description !== tableIndex" class="font-11">
                                                            <span class="fw-semibold">Description: </span>{{ field.description }}
                                                        </span> -->
                                                    </div>
                                                </div>
                                            </div>
                                            <div v-else>
                                                <div v-for="(table, tableIndex) in props.tableHeaders" :key="tableIndex"
                                                    class="mt-3">
                                                    <div v-if="tableIndex === field.options || tableIndex === field.fieldname">
                                                        <div>
                                                            <span class="font-13 text-secondary ">{{
                                                                tableIndex.replace(/_/g, " ")
                                                                }}</span>
                                                        </div>
                                                        <table class="table  rounded-table" border="1" width="100%">
                                                            <thead>
                                                                <tr class=" font-12 fw-lighter">
                                                                    <th class="fw-medium text-center">#</th>
                                                                    <th class=" fw-medium text-center" v-for="field in table"
                                                                        :key="field.fieldname">
                                                                        {{ field.label }}
                                                                    </th>
                                                                    <th></th>
                                                                </tr>
                                                            </thead>
                                                            <tbody>
                                                                <tr
                                                                    v-if="!tableRows[tableIndex] || tableRows[tableIndex].length === 0">
                                                                    <td :colspan="table.length + 2"
                                                                        class="text-center text-muted">
                                                                        <div
                                                                            class="d-flex bg-white py-3 flex-column align-items-center">
                                                                            <i class="bi bi-card-list fs-3 mb-2"></i>
                                                                            <span class=" font-13 text-secondary">No
                                                                                Data</span>
                                                                        </div>
                                                                    </td>
                                                                </tr>
                                                                <tr class=" position-relative"
                                                                    v-for="(row, rowIndex) in tableRows[tableIndex]"
                                                                    :key="rowIndex">
                                                                    <td style="text-align: center;">{{ rowIndex + 1 }}
                                                                    </td>
                                                                    <td v-for="field in table" :key="field.fieldname"
                                                                        :title="row[field.fieldname]"
                                                                        :style="field.label !== 'Type of Manpower' ? { width: row[field.fieldname] ? Math.max(row[field.fieldname].length * 10, 100) + 'px' : 'auto' } : {}">


                                                                        <template
                                                                            v-if="field.fieldtype === 'Data' && field.label !== 'Type of Manpower'">
                                                                            <input type="text"
                                                                                :maxlength="field.fieldtype === 'Phone' ? '10' : '140'"
                                                                                class="form-control font-12"
                                                                                :title="row[field.fieldname]"
                                                                                v-model="row[field.fieldname]" />
                                                                        </template>

                                                                        <template v-if="field.fieldtype === 'Select'">
                                                                            <div>
                                                                                <Multiselect
                                                                                    :multiple="field.fieldtype === 'Table MultiSelect'"
                                                                                    :options="field.options?.split('\n') || []"
                                                                                    :model-value="row[field.fieldname]"
                                                                                    placeholder="Select"
                                                                                    @update:model-value="val => row[field.fieldname] = val"
                                                                                    class="font-11 multiselect" />
                                                                            </div>
                                                                        </template>
                                                                        <template v-if="field.fieldtype === 'Date'">
                                                                            <input type="date"  :min="past"
                                                                                :title="row[field.fieldname]"
                                                                                class="form-control font-12"
                                                                                v-model="row[field.fieldname]" />
                                                                        </template>
                                                                        <template v-if="field.fieldtype === 'Int'">
                                                                            <input type="Number"
                                                                                class="form-control font-12"
                                                                                :title="row[field.fieldname]"
                                                                                v-model="row[field.fieldname]" />
                                                                        </template>
                                                                        <template v-if="field.fieldtype === 'Datetime'">
                                                                            <input type="datetime-local"
                                                                                :title="row[field.fieldname]"
                                                                                class="form-control font-12"
                                                                                v-model="row[field.fieldname]" />
                                                                        </template>

                                                                        <template
                                                                            v-else-if="field.fieldtype === 'Attach'">
                                                                            <input type="file"
                                                                                class="form-control font-12"
                                                                                @change="handleFileUpload($event, row, field.fieldname)" />
                                                                        </template>
                                                                    </td>
                                                                    <td class="d-table-cell text-center align-middle">
                                                                        <span class="tableRowRemoveBtn "
                                                                            @click="removeRow(tableIndex, rowIndex)">
                                                                            <i class="bi bi-x-lg "></i>
                                                                        </span>
                                                                    </td>
                                                                </tr>

                                                                <tr>
                                                                    <td :colspan="table.length + 2"
                                                                        class="text-center text-muted">

                                                                        <button
                                                                            class="btn btn-outline-light text-secondary fw-medium addRow-btn btn-sm font-12"
                                                                            @click="addRow(tableIndex)">Add Row</button>
                                                                    </td>

                                                                </tr>
                                                            </tbody>
                                                        </table>

                                                        <span
                                                            v-if="field.description !== tableIndex && field.description !== 'True' && field.description !== 'false'"
                                                            class="font-11"><span class="fw-semibold">
                                                            </span>{{
                                                                field.description }}</span>
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
    </section>
</template>
<script setup>
import { computed, defineProps, onMounted, ref, watch } from "vue";
// import moment from "moment";
import axiosInstance from "../shared/services/interceptor";
import { apis, doctypes } from "../shared/apiurls";
import { reactive } from "vue";
import Multiselect from "vue-multiselect";
import "@vueform/multiselect/themes/default.css";

const props = defineProps({
    blockArr: {
        type: [Array, null],
        required: true,
    },
    formName: {
        type: String,
        required: true,
    },
    tableHeaders: {
        type: [Array, Object]
    },
    tableRowsdata: {
        type: Object,
        default: () => ({}),
    },
});
// Reactive states
const linkSearchResults = ref([]);
const currentFieldOptions = ref('');
const tableRows = reactive({});

const past = new Date().toISOString().split('T')[0]
// const today = new Date().toISOString().split('T')[0]; 
const now = new Date();
const pad = (n) => n.toString().padStart(2, '0');

// Format: YYYY-MM-DDTHH:MM (suitable for datetime-local input)
const today = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}T${pad(now.getHours())}:${pad(now.getMinutes())}`;
const currentdate = new Date().toISOString().split('T')[0];

const getMaxLength = (field) => {
    const label = field.label?.toLowerCase() || '';

    if (label.includes('expense code')) return 6;
    if (label.includes('cost center')) return 4;
    if (field.fieldtype?.toLowerCase() === 'phone') return 10;

    return 140;
};
const getInputType = (type) => {
    const t = type?.toLowerCase();
    if (t === 'color') return 'color';
    if (t === 'int') return 'number';
    return t;
};
// Format as 'YYYY-MM-DDTHH:MM'
watch(
    () => tableRows,
    () => {
        emit('updateTableData', { ...tableRows });
    },
    { deep: true }
);
watch(
    () => props.tableRowsdata,
    (newData) => {
        Object.keys(newData).forEach((key) => {
            tableRows[key] = newData[key];
        });
    },
    { immediate: true, deep: true }
);


const addRow = (tableIndex) => {
    if (!tableRows[tableIndex]) {
        tableRows[tableIndex] = []; // Initialize it if undefined
    }

    const newRow = Object.fromEntries(
        props.tableHeaders[tableIndex].map((field) => [field.fieldname, ""])
    );

    tableRows[tableIndex].push(newRow);



};

const removeRow = (tableIndex, rowIndex) => {
    tableRows[tableIndex].splice(rowIndex, 1);
};

const handleSelectChange = (
    value,
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

    field.value = value;

    const mockEvent = { target: { value: field.value } };
    console.log(mockEvent, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex);

    logFieldValue(mockEvent, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex);
};


const activeSearch = reactive({
    query: '',
    key: '',
});

// Generate unique key for identifying field
function getFieldKey(b, s, r, c, f) {
    return `${b}-${s}-${r}-${c}-${f}`;
}

// Called when the input is focused
function setActiveField(b, s, r, c, f, field) {
    activeSearch.key = getFieldKey(b, s, r, c, f);
    activeSearch.query = '';
    currentFieldOptions.value = field.options;
    fetchDoctypeList(''); // Load initial list on focus
}

// Check if field is the currently active one
function isActiveField(b, s, r, c, f) {
    return activeSearch.key === getFieldKey(b, s, r, c, f);
}

// Fetch from /api/resource/{field.options} with optional searchText
function fetchDoctypeList(searchText) {
    const resourceName = currentFieldOptions.value;
    if (!resourceName || !activeSearch.key) return;

    const filters = [];

    if (searchText.trim()) {
        filters.push(['name', 'like', `%${searchText}%`]);
    }

    axiosInstance
        .get(`/api/resource/${encodeURIComponent(resourceName)}`, {
            params: {
                fields: JSON.stringify(['name']),
                limit_page_length: '10',
                filters: JSON.stringify(filters),
            },
        })
        .then((res) => {
            linkSearchResults.value = res.data || [];
        })
        .catch((error) => {
            console.error('Error fetching link options:', error);
        });
}

// Handle selection from dropdown
function selectDoctype(b, s, r, c, f, name) {
    const field = props.blockArr[b].sections[s].rows[r].columns[c].fields[f];
    field.value = name;

    // Manually trigger logFieldValue
    const mockEvent = { target: { value: name } };
    logFieldValue(mockEvent, b, s, r, c, f);

    linkSearchResults.value = [];
    activeSearch.query = '';
    activeSearch.key = '';
}


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

    Object.keys(props.tableRowsdata).forEach((key) => {
        tableRows[key] = props.tableRowsdata[key];
    });
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
    //     if (Object.keys(errorMessages.value).length > 0) {
    //     return false;
    //   }

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
    console.log(eve,
        blockIndex,
        sectionIndex,
        rowIndex,
        columnIndex,
        fieldIndex);


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
            // console.log(field.value, "selectedValues", selectedValues);



        } else {
            field.value = eve.target.checked;
        }
    } else if (eve.target?.type === "Select") {
        field.value = eve.target.value;
        console.log(field.value);
    } else if (eve.target?.type === "Table MultiSelect") {
        field.value = Array.from(
            eve.target.selectedOptions,
            (option) => option.value
        );
    }
    else if (field.fieldtype === "Text") {
        field["value"] = eve.target.value; // Capture textarea value
        emit("updateField", field.value); // Emit updated value
    }
    else if (field.fieldtype === "Data") {
        const inputValue = eve.target.value;
        // const fieldKey = `${blockIndex}-${sectionIndex}-${rowIndex}-${columnIndex}-${fieldIndex}`;

        // if (inputValue.length > 139) {
        //     errorMessages.value[fieldKey] = "Maximum 140 characters allowed.";
        //     return;
        // } else {
        //     delete errorMessages.value[fieldKey];
        // }

        field["value"] = inputValue;
        emit("updateField", field.value);
    }

    else {
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
        console.log(inputValue);
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
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style lang="scss" scoped>
.multiselect {
    height: 30px !important;
    font-size: 12px !important;
    width: 100% !important;
}

.multiselect {
    margin: initial;
    font-size: 11px !important;
    border: 1px solid #e2e2e2 !important;
    height: 30px !important;
    border-radius: 8px !important;

    .multiselect-wrapper {
        height: 30px !important;
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
    min-height: 30px !important;
}

.multiselect .multiselect--above {
    min-height: 30px !important;
}

.multiselect__tags {
    min-height: 30px !important;
    padding: 0px;
}

.multiselect .multiselect__tags {
    min-height: 30px !important;
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

::v-deep(.multiselect__placeholder) {
    color: #adadad;
    display: inline-block;
    margin-bottom: 10px;
    padding-top: 2px;
    font-size: 12px !important;
}


::v-deep(.multiselect__select) {
    position: absolute;
    width: 40px;
    height: 32px;
    right: 1px;
    /* top: 1px; */
    padding: 4px 8px;
    text-align: center;
    transition: transform 0.2s ease;
}

::v-deep(.multiselect) {
    height: 32px !important;
    min-height: 32px !important;
}

::v-deep(.multiselect__single) {
    font-size: 12px;
    color: #212529 !important;
}

::v-deep(.multiselect__tags) {
    height: 32px !important;
    min-height: 32px !important;
    display: flex;
    align-items: center;
    border: none;
}

::v-deep(.multiselect-wrapper),
::v-deep(.multiselect-search) {
    height: 32px !important;
    min-height: 32px !important;
    line-height: 32px !important;
    display: flex;
    align-items: center;
}

::v-deep(.multiselect-search) {
    height: 32px !important;
    min-height: 32px !important;
    display: flex;
    align-items: center;
}

::v-deep(.multiselect-wrapper) {
    height: 32px !important;
    min-height: 32px !important;
    line-height: 32px !important;
}

::v-deep(.multiselect-search) {
    position: absolute;
    width: 40px !important;
    height: 32px !important;
    right: 1px;

    padding: 4px 8px;
    text-align: center;
    transition: transform 0.2s ease;
    display: flex;
    align-items: center;
    justify-content: center;
}

::v-deep(.multiselect__element:hover) {
    background-color: #eeeeee !important;
}

::v-deep(.multiselect__element:hover .multiselect__option) {
    background-color: #eeeeee !important;
    color: #000 !important;
}

::v-deep(.multiselect__tags) {
    color: #000 !important;
    font-size: 12px !important;
}


::v-deep(.multiselect__element:hover .multiselect__option--highlight) {
    background-color: #eeeeee !important;
    color: #000 !important;
}

/* Additional specific rule for `.multiselect__option` when hovered */
::v-deep(.multiselect__option:hover) {
    background-color: #eeeeee !important;
    color: #000 !important;
}

.addRow-btn {
    border: 1px dotted #cccccc;
}

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

table th {
    color: #6c757d;
}

.tableRowRemoveBtn {

    border-radius: 50%;
    padding: 4px;
}

.tableRowRemoveBtn:hover {
    background-color: #cccccc;
    border-radius: 50%;
    padding: 4px;
}

.tableRowRemoveBtn i {
    cursor: pointer;
}

.rounded-table {
    border-radius: 10px;
    background-color: #ccc;
    // overflow: hidden;
    /* This ensures child elements respect the border radius */
}
</style>