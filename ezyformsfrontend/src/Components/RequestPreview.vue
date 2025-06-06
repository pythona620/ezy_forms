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
                                        <div v-if="field.fieldtype !== 'Table'"
                                            :class="field.fieldtype === 'Check' ? ' d-flex mt-4 flex-row-reverse justify-content-end gap-2' : ''">
                                            <div v-if="field.label">
                                                <label :for="'field-' +
                                                    sectionIndex +
                                                    '-' +
                                                    columnIndex +
                                                    '-' +
                                                    fieldIndex
                                                    ">
                                                    <span class="font-12"
                                                        :class="field.fieldtype === 'Small Text' ? 'fw-bold' : ''">{{
                                                            field.label }}</span>
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
                                                    :options="field.options?.split('\n').filter(opt => opt.trim() !== '') || []"
                                                    :modelValue="field.value" placeholder="Select"
                                                    @update:modelValue="(val) => handleSelectChange(val, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)"
                                                    class="font-11 multiselect" />


                                            </template>

                                            <template v-else-if="

                                                field.fieldtype === 'radio' || field.fieldtype === 'Small Text'
                                            ">
                                                <div class="container-fluid">
                                                    <div class="row">
                                                        <div class="form-check col-4 mb-1" v-for="(option, index) in field?.options?.split(
                                                            '\n'
                                                        )" :key="index" :class="{ 'd-none': index === 0 }">
                                                            <div>
                                                                <input v-if="
                                                                    field.fieldtype === 'Small Text' && index !== 0
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
                                                    @change="logFieldValue($event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)" />

                                                <div v-if="field.value" class="d-flex flex-wrap gap-2">
                                                    <div v-for="(fileUrl, index) in field.value.split(',').map(f => f.trim())"
                                                        :key="index" class="position-relative d-inline-block"
                                                        @mouseover="hovered = index" @mouseleave="hovered = null">
                                                        <!-- Click to open modal -->
                                                        <div @click="openPreview(fileUrl)" style="cursor: pointer">
                                                            <img v-if="isImageFile(fileUrl)" :src="fileUrl"
                                                                class="img-thumbnail mt-2 border-0"
                                                                style="max-width: 100px; max-height: 100px" />
                                                            <div v-else
                                                                class="d-flex align-items-center justify-content-center border mt-2"
                                                                style="width: 100px; height: 100px; background: #f9f9f9">
                                                                <i class="bi bi-file-earmark-pdf fs-1 text-danger"></i>
                                                            </div>
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

                                                <!-- Modal Preview -->
                                                <div v-if="showModal" class="modal-backdrop" @click.self="closePreview"
                                                    style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center; z-index: 1050;">
                                                    <div
                                                        style="background: white; padding: 20px; max-width: 90%; max-height: 90%; overflow: auto; border-radius: 8px; position: relative;">

                                                        <button @click="closePreview"
                                                            style="position: absolute; top: 10px; right: 10px; border: none; background: transparent; font-size: 20px;">&times;</button>

                                                        <!-- Image Preview -->
                                                        <img v-if="isImageFile(previewUrl)" :src="previewUrl"
                                                            style="max-width: 100%; max-height: 80vh;" />

                                                        <!-- PDF Preview -->
                                                        <iframe v-else :src="previewUrl"
                                                            style="width: 80vw; height: 80vh;" frameborder="0"></iframe>
                                                    </div>
                                                </div>
                                            </template>
                                            <template v-else-if="field.fieldtype == 'Check'">
                                                <input type="checkbox" :value="field.value"
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
                                                        "
                                                    class="form-control form-check-input previewInputHeight font-10" />
                                            </template>
                                            <template v-else-if="field.fieldtype == 'Datetime'">
                                                <input type="datetime-local" :value="field.value"
                                                    :min="new Date().toISOString().slice(0, 16)"
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
                                            <template v-else-if="field.fieldtype === 'Link'">
                                                <input type="text" v-model="field.value"
                                                    @input="() => fetchDoctypeList(field.options, field.value)"
                                                    @focus="() => fetchDoctypeList(field.options, field.value)"
                                                    @change="(event) => logFieldValue(event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)"
                                                    class="form-control font-12 mb-1" />


                                                <ul v-if="linkSearchResults.length" class="list-group mt-1"
                                                    style="max-height: 200px; overflow-y: auto;">
                                                    <li v-for="(result, index) in linkSearchResults" :key="index"
                                                        @click="selectDoctype(result.name, field, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)"
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
                                                {{ field.fieldname }}
                                                <component v-if="
                                                    field.fieldtype !== 'Datetime' && field.fieldtype !== 'Text'
                                                " :is="getFieldComponent(field.fieldtype)" :value="field.value"
                                                    :min="past" @click="forceOpenCalendar"
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
                                        </div>
                                        <span v-if="field.description !== 'Field' && field.fieldtype !== 'Table'"
                                            class="font-11"><span class="fw-semibold">Description: </span>{{
                                                field.description }}</span>
                                        <div v-if="blockIndex === 0 && field.fieldtype === 'Table'">

                                            <div v-if="field.fieldtype === 'Table' && field.description === 'true'">

                                                <div v-for="(table, tableIndex) in props.tableHeaders" :key="tableIndex"
                                                    class="mt-3">

                                                    <div v-if="tableIndex === field.fieldname">

                                                        <div>
                                                            <span class="font-13  fw-medium">{{
                                                                field.label.replace(/_/g, " ") }}</span>
                                                        </div>

                                                        <div v-if="!tableRows[tableIndex] || tableRows[tableIndex].length === 0"
                                                            class="text-center text-muted">
                                                            <div class="d-flex flex-column align-items-center">
                                                                <i class="bi bi-card-list fs-3 mb-2"></i>
                                                                <span class=" font-13 text-secondary">No Data</span>
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
                                                                    <label v-if="fieldItem.label !== 'Form Name'"
                                                                        class="font-12 fw-medium">{{
                                                                            fieldItem.label
                                                                        }}</label>
                                                                    <template v-if="fieldItem.label === 'Form Name'">
                                                                        <!-- Keep the same title tooltip and width logic -->
                                                                        <span class="font-12"
                                                                            :style="{ maxWidth: '100%' }"
                                                                            :title="row[fieldItem.fieldname]">
                                                                            {{ row[fieldItem.fieldname] || '—' }}
                                                                        </span>
                                                                    </template>
                                                                    <template
                                                                        v-if="fieldItem.fieldtype === 'Data' && fieldItem.label !== 'Form Name'">

                                                                        <input :title="row[fieldItem.fieldname]"
                                                                            type="text"
                                                                            class="form-control font-12 px-2"
                                                                            :maxlength="fieldItem.fieldtype === 'Phone' ? '10' : '140'"
                                                                            v-model="row[fieldItem.fieldname]" />
                                                                    </template>
                                                                    <template v-if="fieldItem.fieldtype === 'Select'">
                                                                        <div>

                                                                            <Multiselect
                                                                                :multiple="fieldItem.fieldtype === 'Table MultiSelect'"
                                                                                :options="(fieldItem.options?.split('\n').filter(opt => opt.trim() !== '') || [])"
                                                                                :model-value="row[fieldItem.fieldname]"
                                                                                placeholder="Select"
                                                                                @update:model-value="val => row[fieldItem.fieldname] = val"
                                                                                class="font-11 multiselect" />
                                                                        </div>
                                                                    </template>
                                                                    <template v-if="field.fieldtype === 'Text'">
                                                                        <textarea class="form-control font-12" rows="3"
                                                                            v-model="row[field.fieldname]"
                                                                            :title="row[field.fieldname]"></textarea>
                                                                    </template>
                                                                    <template
                                                                        v-else-if="fieldItem.fieldtype === 'Date'">
                                                                        <input :min="past" :max="today"
                                                                            :title="row[fieldItem.fieldname]"
                                                                            type="date" class="form-control font-12"
                                                                            v-model="row[fieldItem.fieldname]" />
                                                                    </template>
                                                                    <template v-if="fieldItem.fieldtype === 'Text'">
                                                                        <textarea class="form-control font-12" rows="3"
                                                                            v-model="row[fieldItem.fieldname]"
                                                                            :title="row[fieldItem.fieldname]"></textarea>
                                                                    </template>
                                                                    <template
                                                                        v-else-if="fieldItem.fieldtype === 'Datetime'">


                                                                        <input :title="row[fieldItem.fieldname]"
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
                                                                    </template>
                                                                    <template
                                                                        v-else-if="fieldItem.fieldtype === 'Attach'">
                                                                        <!-- File Input -->
                                                                        <input multiple type="file"
                                                                            class="form-control font-12"
                                                                            accept="image/jpeg,image/png,application/pdf"
                                                                            @change="handleFileUpload($event, row, fieldItem.fieldname)" />

                                                                        <!-- Preview Section -->
                                                                        <div v-if="row[fieldItem.fieldname]"
                                                                            class="d-flex flex-wrap gap-2">
                                                                            <div v-for="(fileUrl, index) in normalizeFileList(row[fieldItem.fieldname])"
                                                                                :key="index"
                                                                                class="position-relative d-inline-block"
                                                                                @mouseover="hovered = index"
                                                                                @mouseleave="hovered = null">
                                                                                <!-- Click to Preview -->
                                                                                <div @click="openPreview(fileUrl)"
                                                                                    style="cursor: pointer">
                                                                                    <!-- Show image thumbnail -->
                                                                                    <img v-if="isImageFile(fileUrl)"
                                                                                        :src="fileUrl"
                                                                                        class="img-thumbnail mt-2 border-0"
                                                                                        style="max-width: 100px; max-height: 100px" />

                                                                                    <!-- Show PDF icon -->
                                                                                    <div v-else
                                                                                        class="d-flex align-items-center justify-content-center border mt-2"
                                                                                        style="width: 100px; height: 100px; background: #f9f9f9">
                                                                                        <i
                                                                                            class="bi bi-file-earmark-pdf fs-1 text-danger"></i>
                                                                                    </div>
                                                                                </div>
                                                                            </div>
                                                                        </div>

                                                                        <!-- Modal Preview -->
                                                                        <div v-if="showModal" class="modal-backdrop"
                                                                            @click.self="closePreview" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%;
           background: rgba(0,0,0,0.5); display: flex; align-items: center;
           justify-content: center; z-index: 1050;">
                                                                            <div style="background: white; padding: 20px; max-width: 90%; max-height: 90%;
             overflow: auto; border-radius: 8px; position: relative;">
                                                                                <button @click="closePreview" style="position: absolute; top: 10px; right: 10px;
               border: none; background: transparent; font-size: 20px;">
                                                                                    &times;
                                                                                </button>

                                                                                <!-- Image Preview -->
                                                                                <img v-if="isImageFile(previewUrl)"
                                                                                    :src="previewUrl"
                                                                                    style="max-width: 100%; max-height: 80vh;" />

                                                                                <!-- PDF Preview -->
                                                                                <iframe v-else :src="previewUrl"
                                                                                    style="width: 80vw; height: 80vh;"
                                                                                    frameborder="0"></iframe>
                                                                            </div>
                                                                        </div>
                                                                    </template>


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
                                                    <div class="overTable" v-if="tableIndex === field.fieldname">
                                                        <div>
                                                            <span class="font-13 text-secondary ">{{
                                                                field.label.replace(/_/g, " ")
                                                                }}</span>
                                                        </div>
                                                        <table class="table  rounded-table" border="1" width="100%">
                                                            <thead>
                                                                <tr class=" font-12 fw-lighter">
                                                                    <!-- <th class="fw-medium text-center">#</th> -->
                                                                    <th class=" fw-medium text-center"
                                                                        v-for="field in table" :key="field.fieldname">
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
                                                                <tr v-for="(row, rowIndex) in tableRows[tableIndex]"
                                                                    :key="rowIndex">
                                                                    <!-- <td style="text-align: center;" class="font-12">
                                                                        {{
                                                                            rowIndex + 1 }}
                                                                    </td> -->
                                                                    <td v-for="field in table" :key="field.fieldname"
                                                                        :title="row[field.fieldname]" :style="field.label !== 'Type of Manpower'
                                                                            ? {
                                                                                width: row[field.fieldname] ? Math.max(row[field.fieldname].length * 10, 100) + 'px' : 'auto',
                                                                                maxWidth: '300px',
                                                                                textOverflow: 'ellipsis',
                                                                                whiteSpace: 'nowrap'
                                                                            }
                                                                            : {}">


                                                                        <!-- <template v-if="rowIndex === 0 && fieldIndex === 0 && field.label === ' field 1'">
                                                                            <span class="font-12 d-inline-block text-truncate text-center" :title="row[field.fieldname]" :style="{ maxWidth: '100%' }">
                                                                                {{ row[field.fieldname] || 'Name' }}
                                                                            </span>
                                                                            </template> -->
                                                                        <!-- <template
                                                                            v-if="field.label === 'Details' && field.fieldname == 'field_0'  && rowIndex === 0 && fieldIndex === 0">
                                                                            <span
                                                                                class="font-12 d-inline-block text-truncate"
                                                                                :style="{ maxWidth: '100%' }"
                                                                                :title="row[field.fieldname]">
                                                                                {{ row[field.fieldname] }}
                                                                            </span>
                                                                        </template> -->
                                                                        <!-- :disabled="rowIndex === 0 && fieldIndex === 0 && field.label !== 'Details' && field.fieldname == 'field_0'" -->
                                                                        <!-- :class="field.label === 'Details' && field.fieldname === 'field_0' && rowIndex === 0 && fieldIndex === 0 ? 'bg-white border-0' : 'border-1'" -->
                                                                        <template
                                                                            v-if="field.fieldtype === 'Data' && field.label !== 'Type of Manpower'">

                                                                            <input type="text"
                                                                                :maxlength="field.fieldtype === 'Phone' ? '10' : '140'"
                                                                                class="form-control font-12"
                                                                                :title="row[field.fieldname]"
                                                                                v-model="row[field.fieldname]" />
                                                                        </template>
                                                                        <template v-if="field.fieldtype === 'Text'">
                                                                            <textarea class="form-control font-12"
                                                                                rows="3" v-model="row[field.fieldname]"
                                                                                :title="row[field.fieldname]"></textarea>
                                                                        </template>

                                                                        <template
                                                                            v-else-if="field.fieldtype === 'Select'">
                                                                            <div>
                                                                                <Multiselect
                                                                                    :multiple="field.fieldtype === 'Table MultiSelect'"
                                                                                    :options="field.options?.split('\n').filter(opt => opt.trim() !== '') || []"
                                                                                    :model-value="row[field.fieldname]"
                                                                                    placeholder="Select"
                                                                                    @update:model-value="val => row[field.fieldname] = val"
                                                                                    class="font-11 multiselect" />
                                                                            </div>
                                                                        </template>
                                                                        <template v-if="field.fieldtype === 'Date'">

                                                                            <input type="date"
                                                                                :min="field.fieldname === 'expense_date' ? null : today"
                                                                                :max="field.fieldname === 'expense_date' ? today : null"
                                                                                :title="row[field.fieldname]"
                                                                                class="form-control font-12"
                                                                                v-model="row[field.fieldname]" />
                                                                        </template>

                                                                        <template v-else-if="field.fieldtype === 'Int'">
                                                                            <input
                                                                                v-if="field.description && /[+\-*/]/.test(field.description)"
                                                                                type="number"
                                                                                class="form-control font-12"
                                                                                :value="calculateFieldExpression(row, field.description, table)"
                                                                                readonly />
                                                                            <input v-else type="number"
                                                                                class="form-control font-12"
                                                                                v-model.number="row[field.fieldname]" />
                                                                        </template>


                                                                        <template
                                                                            v-else-if="field.fieldtype === 'Datetime'">
                                                                            <input type="datetime-local"
                                                                                :title="row[field.fieldname]"
                                                                                class="form-control font-12"
                                                                                v-model="row[field.fieldname]" />
                                                                        </template>


                                                                        <template
                                                                            v-else-if="field.fieldtype === 'Attach'">
                                                                            <!-- File Input -->
                                                                            <input type="file" multiple
                                                                                accept="image/jpeg,image/png,application/pdf"
                                                                                class="form-control font-12"
                                                                                @change="handleFileUpload($event, row, field.fieldname)" />

                                                                            <!-- Preview Section -->
                                                                            <div v-if="row[field.fieldname]"
                                                                                class="d-flex flex-wrap gap-2">
                                                                                <div v-for="(fileUrl, index) in normalizeFileList(row[field.fieldname])"
                                                                                    :key="index"
                                                                                    class="position-relative d-inline-block"
                                                                                    @mouseover="hovered = index"
                                                                                    @mouseleave="hovered = null">
                                                                                    <!-- Preview click -->
                                                                                    <div @click="openPreview(fileUrl)"
                                                                                        style="cursor: pointer">
                                                                                        <!-- Show Image Thumbnail -->
                                                                                        <img v-if="isImageChildFile(fileUrl)"
                                                                                            :src="fileUrl"
                                                                                            class="img-thumbnail mt-2 border-0"
                                                                                            style="max-width: 100px; max-height: 100px" />

                                                                                        <!-- Show PDF Icon -->
                                                                                        <div v-else
                                                                                            class="d-flex align-items-center justify-content-center border mt-2"
                                                                                            style="width: 100px; height: 100px; background: #f9f9f9">
                                                                                            <i
                                                                                                class="bi bi-file-earmark-pdf fs-1 text-danger"></i>
                                                                                        </div>
                                                                                    </div>

                                                                                    <!-- Remove Icon -->
                                                                                    <button v-if="hovered === index"
                                                                                        @click="removechildFile(index, field, row)"
                                                                                        class="btn btn-sm btn-light position-absolute"
                                                                                        style="top: 2px; right: 5px; border-radius: 50%; padding: 0 5px">
                                                                                        <i class="bi bi-x fs-6"></i>
                                                                                    </button>
                                                                                </div>
                                                                            </div>
                                                                        </template>





                                                                    </td>

                                                                    <td class="d-table-cell text-center align-middle">
                                                                        <span class="tableRowRemoveBtn "
                                                                            @click="removeRow(tableIndex, rowIndex)">
                                                                            <i class="bi bi-x-lg "></i>
                                                                        </span>
                                                                    </td>
                                                                </tr>

                                                            </tbody>
                                                            <tfoot>
                                                                <tr v-if="table.some(field => field.fieldtype === 'Int' && field.description && /[+\-*/]/.test(field.description))"
                                                                    class="bg-light">
                                                                    <td class="text-center font-12">Total</td>
                                                                    <td v-for="field in table" :key="field.fieldname"
                                                                        class="text-center font-12">

                                                                        <span
                                                                            v-if="field.fieldtype === 'Int' && field.description && /[+\-*/]/.test(field.description) && (field.label.includes('Total') || field.label.includes('Amount'))">
                                                                            {{
                                                                                tableTotals[tableIndex]?.[field.fieldname]
                                                                                ?? 0 }}
                                                                        </span>
                                                                    </td>
                                                                    <!-- <td></td> -->
                                                                </tr>
                                                                <tr>
                                                                    <td :colspan="table.length + 2"
                                                                        class="text-center text-muted">

                                                                        <button
                                                                            class="btn btn-outline-light text-secondary fw-medium addRow-btn btn-sm font-12"
                                                                            @click="addRow(tableIndex)">Add Row</button>
                                                                    </td>

                                                                </tr>
                                                            </tfoot>

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
import { watchEffect } from "vue";

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
// const now = new Date();
// const pad = (n) => n.toString().padStart(2, '0');

// // Format: YYYY-MM-DDTHH:MM (suitable for datetime-local input)
// const today = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}T${pad(now.getHours())}:${pad(now.getMinutes())}`;
const now = new Date();
const pad = (n) => n.toString().padStart(2, '0');

const today = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())}`;

const formQuestions = ref([
    "The Porch & Main Gate is manned and lighting is sufficient.",
    "Reception area is clean & all brand standards in place.",
    "Public Areas are clean, All furniture's in place, Kids corner is well organised, Music and lighting is right",
    "The Bar & Restaurant area clean and in order. Music level Normal.",
    "Meeting rooms area is clean and well maintained. If no Meetings then lights are off.",
    "Heart of the house areas are well maintained.",
    "Food at Staff dinning was served on time, Menu is as per the day. Taste of the Food to be checked and incorporate in MOD report.",
    "GYM is well maintained, fresh towels and water available.",
    "Pool area is well maintained. Guard is present.",
    "The surrounding and back of the house areas are well maintained.",
    "Check on General upkeep of Staff locker. Clean and pest free.",
    "Quality and condition of water bottling plant.",
    "Spa cleanliness and upkeep is inline with hotel standards.",
    "Pest Free in the hotel.",
    "Dishwasher area clean in main kitchen ibis / novotel",
    "Main kitchen Clean and Neat novotel / ibis",
    "Garbage Area neat and clean",
    "IRD Clean and Neat novotel / ibis.",
    "Square Restaurant and Bar",
    "Ibis Restaurant and Bar",
    "Any operation Hazzard for safety. (IF YES NEED DETAIL)",
]);

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


const previewUrl = ref('')
const showModal = ref(false)

const openPreview = (url) => {
    previewUrl.value = url
    showModal.value = true
}

const closePreview = () => {
    showModal.value = false
    previewUrl.value = ''
}
// console.log(tableRows);
// Format as 'YYYY-MM-DDTHH:MM'
watch(
    () => tableRows,
    () => {
        updateFirstRowName();
        const finalData = {};

        for (const [tableIndex, rows] of Object.entries(tableRows)) {
            const totalsRow = tableTotals.value?.[tableIndex];

            if (totalsRow && Object.keys(totalsRow).length > 0) {
                // Only add totals row if it has actual data
                finalData[tableIndex] = [...rows, totalsRow];
            } else {
                // Otherwise, just send the rows
                finalData[tableIndex] = [...rows];
            }
        }
        console.log(tableRows, "pppp");

        emit('updateTableData', { ...finalData });
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
function updateFirstRowName() {
    for (const tableIndex in tableRows) {
        const rows = tableRows[tableIndex];
        const headers = props.tableHeaders[tableIndex];

        if (rows && rows.length > 0 && headers?.length > 0) {
            const firstFieldName = headers[0].fieldname;

            // ✅ Use includes instead of exact match
            if (firstFieldName && firstFieldName.toLowerCase().includes('details')) {
                rows[0][firstFieldName] = 'Name';
            }
        }
    }
}



// function calculateFieldExpression(row, expression, fields) {
//     const labelToValue = {};

//     // Build a map: label -> value from row
//     fields.forEach(f => {
//         const value = parseFloat(row[f.fieldname]);
//         labelToValue[f.label] = isNaN(value) ? 0 : value;
//     });

//     // Sort labels by length descending to avoid partial replacements (e.g., "Cost" before "Cost per Casual")
//     const sortedLabels = Object.keys(labelToValue).sort((a, b) => b.length - a.length);

//     let formula = expression;

//     // Replace each label (with possible spaces) in expression with the corresponding value
//     for (const label of sortedLabels) {
//         // Use regex with word boundary-like pattern to replace safely
//         const safeLabel = label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // escape special regex characters
//         const regex = new RegExp(`\\b${safeLabel}\\b`, 'g');
//         formula = formula.replace(regex, labelToValue[label]);
//     }

//     try {
//         return new Function(`return ${formula}`)();
//     } catch (e) {
//         console.error('Error evaluating formula:', formula, e);
//         return 0;
//     }
// }

// function calculateFieldExpression(row, expression, fields) {
//     const labelToValue = {};

//     // Map: label -> value
//     fields.forEach(f => {
//         let value = parseFloat(row[f.fieldname]);
//         labelToValue[f.label] = isNaN(value) ? 0 : value;
//     });

//     // Replace percentages (e.g., "Tax%" -> "Tax / 100")
//     expression = expression.replace(/([a-zA-Z\s]+)%/g, (_, label) => {
//         return `(${label.trim()} / 100)`;
//     });

//     // Sort labels by length descending to avoid partial match issues
//     const sortedLabels = Object.keys(labelToValue).sort((a, b) => b.length - a.length);

//     let formula = expression;

//     // Replace label names with their numeric values
//     for (const label of sortedLabels) {
//         const safeLabel = label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
//         const regex = new RegExp(`\\b${safeLabel}\\b`, 'g');
//         formula = formula.replace(regex, labelToValue[label]);
//     }

//     try {
//         return new Function(`return ${formula}`)();
//     } catch (e) {
//         console.error('Error evaluating formula:', formula, e);
//         return 0;
//     }
// } 
function calculateFieldExpression(row, expression, fields) {
    const labelToValue = {};

    // Step 1: Map label -> value
    fields.forEach(f => {
        const value = parseFloat(row[f.fieldname]);
        labelToValue[f.label] = isNaN(value) ? 0 : value;
    });

    // Step 2: Convert "Label%" to "(Label / 100)"
    expression = expression.replace(/([a-zA-Z\s]+)%/g, (_, label) => {
        return `(${label.trim()} / 100)`;
    });

    // Step 3: Replace labels with actual numeric values
    const sortedLabels = Object.keys(labelToValue).sort((a, b) => b.length - a.length);
    let formula = expression;

    for (const label of sortedLabels) {
        const safeLabel = label.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // escape regex special chars
        const regex = new RegExp(`\\b${safeLabel}\\b`, 'g');
        formula = formula.replace(regex, labelToValue[label]);
    }

    // Step 4: Safely evaluate formula
    try {
        return new Function(`return ${formula}`)();
    } catch (e) {
        console.error('Error evaluating formula:', formula, e);
        return 0;
    }
}



const tableTotals = computed(() => {
    const totals = {};

    for (const [tableIndex, rows] of Object.entries(tableRows)) {
        totals[tableIndex] = {};

        const fields = props.tableHeaders[tableIndex] || [];
        fields.forEach((field) => {
            if (field.fieldtype === 'Int' && field.description && /[+\-*/]/.test(field.description) && field.label.includes('Total') || field.label.includes('Amount')) {
                let sum = 0;

                rows.forEach((row) => {
                    if (field.description && /[+\-*/]/.test(field.description) && field.label.includes('Total') || field.label.includes('Amount')) {
                        // Calculate expression dynamically using labels and row data
                        sum += Number(calculateFieldExpression(row, field.description, fields));
                    }
                    //   else {
                    //     // Sum raw values
                    //     const val = parseFloat(row[field.fieldname]);
                    //     sum += isNaN(val) ? 0 : val;
                    //   }
                });

                totals[tableIndex][field.fieldname] = sum;
            }
        });
    }

    return totals;
});
watchEffect(() => {
    for (const [tableIndex, rows] of Object.entries(tableRows)) {
        const fields = props.tableHeaders[tableIndex] || [];

        rows.forEach((row) => {
            // First: calculate all independent fields like tax_amount
            fields.forEach((field) => {
                if (
                    field.fieldtype === 'Int' &&
                    field.description &&
                    /[+\-*/]/.test(field.description)
                ) {
                    const result = calculateFieldExpression(row, field.description, fields);
                    row[field.fieldname] = result;
                }
            });

            // Second pass to ensure dependent fields like total_amount are recalculated
            fields.forEach((field) => {
                if (
                    field.fieldtype === 'Int' &&
                    field.description &&
                    /[+\-*/]/.test(field.description)
                ) {
                    const result = calculateFieldExpression(row, field.description, fields);
                    row[field.fieldname] = result;
                }
            });

        });
    }
});

// const handleFileUpload = (event, row, fieldname) => {
//     const selectedFiles = Array.from(event.target.files);
//     if (!selectedFiles.length) return;

//     // Initialize the field if it's not already an array
//     if (!Array.isArray(row[fieldname])) {
//         row[fieldname] = [];
//     }

//     // Calculate total number of files (existing + new)
//     const totalFiles = row[fieldname].length + selectedFiles.length;

//     if (totalFiles > 5) {
//         alert("You can only upload a maximum of 5 files.");
//         return;
//     }

//     // Proceed with uploading each file
//     selectedFiles.forEach((file) => {
//         tableFileUpload(file, row, fieldname);
//     });
// };
const handleFileUpload = async (event, row, fieldname) => {
    let selectedFiles = Array.from(event.target.files);
    if (!selectedFiles.length) return;

    const existingFiles = normalizeFileList(row[fieldname]);

    if (existingFiles.length >= 5) {
        alert("Maximum 5 files are allowed.");
        return;
    }

    const remainingSlots = 5 - existingFiles.length;
    if (selectedFiles.length > remainingSlots) {
        alert(`Only ${remainingSlots} more file(s) can be uploaded.`);
        selectedFiles = selectedFiles.slice(0, remainingSlots);
    }

    // Upload files sequentially to preserve order
    for (const file of selectedFiles) {
        await tableFileUpload(file, row, fieldname);
    }

    event.target.value = null;
};



const tableFileUpload = (file, row, fieldname) => {
    return new Promise((resolve, reject) => {
        const randomNumber = generateRandomNumber();
        const fileName = `mailfiles-${randomNumber}-@${file.name}`;

        const formData = new FormData();
        formData.append("file", file, fileName);
        formData.append("is_private", "0");
        formData.append("folder", "Home");

        axiosInstance
            .post(apis.uploadfile, formData)
            .then((res) => {
                if (res.message && res.message.file_url) {
                    const fileUrl = res.message.file_url;

                    // Get current list and append
                    let files = normalizeFileList(row[fieldname]);
                    files.push(fileUrl);

                    // Store back as comma-separated string
                    row[fieldname] = files.join(',');
                    resolve(); // ✅ done
                } else {
                    console.error("file_url not found in the response.");
                    reject();
                }
            })
            .catch((error) => {
                console.error("Upload error:", error);
                reject();
            });
    });
};



const normalizeFileList = (value) => {
    if (!value) return [];
    if (Array.isArray(value)) return value;
    if (typeof value === 'string') return value.split(',').map(f => f.trim());
    return [];
};

const removechildFile = (index, field, row) => {
    let files = normalizeFileList(row[field.fieldname]);
    files.splice(index, 1);
    row[field.fieldname] = files.join(',');
};

const isImageChildFile = (fileUrl) => {
    return /\.(jpg|jpeg|png)$/i.test(fileUrl);
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
    // console.log(mockEvent, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex);

    logFieldValue(mockEvent, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex);
};
// const linkSearchResults = ref([])

function fetchDoctypeList(resourceName, searchText) {
    if (!resourceName) return;

    const filters = [];

    if (searchText && searchText.trim()) {
        filters.push(['name', 'like', `%${searchText}%`]);
    }

    axiosInstance
        .get(`/api/resource/${encodeURIComponent(resourceName)}`, {
            params: {
                fields: JSON.stringify(['name']),
                filters: JSON.stringify(filters),
            },
        })
        .then((res) => {
            linkSearchResults.value = res.data || []; // Ensure .data exists
        })
        .catch((err) => {
            console.error('Error fetching doctype list:', err);
        });
}


function selectDoctype(name, field, b, s, r, c, f) {
    field.value = name;
    const event = { target: { value: name } };
    logFieldValue(event, b, s, r, c, f);
    linkSearchResults.value = [];
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
                            // if( field.fieldtype === 'Data' && field.label === 'Total'){
                            //     console.log(tableTotals.value);
                            //     field.value = tableTotals.value
                            //     emit("updateField", field)
                            // }

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
    // updateFormQuestionsInTableRows();

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
                            if (field.label.includes("Requested by") || field.label.includes("Requested By")) {
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


// function updateFormQuestionsInTableRows() {
//     for (const [tableIndex, fields] of Object.entries(props.tableHeaders)) {
//         const hasFormName = fields.some(f => f.label === 'Form Name');

//         if (hasFormName) {
//             const formNameField = fields.find(f => f.label === 'Form Name');

//             tableRows[tableIndex] = formQuestions.value.map((question) => {
//                 const row = Object.fromEntries(fields.map(f => [f.fieldname, ""]));
//                 row[formNameField.fieldname] = question;
//                 return row;
//             });
//         }
//     }
// }

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
    // console.log(eve,
    //     blockIndex,
    //     sectionIndex,
    //     rowIndex,
    //     columnIndex,
    //     fieldIndex);


    if (eve.target?.files && eve.target.files.length > 0) {
        let files = Array.from(eve.target.files); // Convert FileList to an array

        // Normalize existing files into an array
        let existingFiles = field["value"]
            ? field["value"].split(',').map(f => f.trim())
            : [];

        const totalFiles = existingFiles.length + files.length;
        if (totalFiles > 5) {
            alert("You can upload a maximum of 5 files.");
            files = files.slice(0, 5 - existingFiles.length); // Only allow up to 5 total
        }

        files.forEach((file) => uploadFile(file, field));

        // ✅ Reset file input to allow same file re-selection
        eve.target.value = null;
    }

    else if (eve.target?.type === "checkbox") {
        if (field.fieldtype === "Check") {
            field.value = eve.target.checked ? 1 : 0;
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
        // console.log(field.value);
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
        // console.log(inputValue);
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
watch(
    () => tableTotals.value,
    (totals) => {
        if (!props.blockArr) return;

        props.blockArr.forEach((block) => {
            // Find the dynamic table name inside this block
            let dynamicTableName = null;

            outerLoop:
            for (const section of block.sections) {
                for (const row of section.rows) {
                    for (const column of row.columns) {
                        for (const field of column.fields) {
                            // Check if field is a Table field and its name exists in totals
                            if (
                                (field.fieldtype === 'Table' || field.fieldtype === 'Link') &&
                                (field.fieldname in totals)
                            ) {
                                dynamicTableName = field.fieldname;
                                break outerLoop; // found it, stop searching
                            }
                        }
                    }
                }
            }

            if (!dynamicTableName) return; // no table field found in this block

            // Now update fields with fieldname 'gross_total' inside this block
            block.sections.forEach((section) => {
                section.rows.forEach((row) => {
                    row.columns.forEach((column) => {
                        column.fields.forEach((field) => {
                            if (/gross total|gross amount|total amount/i.test(field.label)) {
                                const obj = totals?.[dynamicTableName] || {};
                                const matchedKey = Object.keys(obj).find(key =>
                                    key.toLowerCase().includes('amount') || key.toLowerCase().includes('total') || key.toLowerCase().includes('total cost')
                                );
                                const totalValue = matchedKey ? obj[matchedKey] : 0;
                                field.value = totalValue;
                                emit("updateField", field);
                            }


                        });
                    });
                });
            });
        });
    },
    { deep: true, immediate: true }
);


const generateRandomNumber = () => {
    return Math.floor(Math.random() * 1000000);
};

// const uploadFile = (file, field, index) => {
//     const randomNumber = generateRandomNumber();
//     let fileName = `mailfiles-${props.formName}${randomNumber}-@${file.name}`;

//     const formData = new FormData();
//     formData.append("file", file, fileName);
//     formData.append("is_private", "0");
//     formData.append("folder", "Home");
//     axiosInstance
//         .post(apis.uploadfile, formData)
//         .then((res) => {
//             if (res.message && res.message.file_url) {
//                 if (field["value"]) {
//                     field["value"] += `, ${res.message.file_url}`;
//                 } else {
//                     field["value"] = res.message.file_url;
//                 }
//                 emit("updateField", field);
//             } else {
//                 console.error("file_url not found in the response.");
//             }
//         })
//         .catch((error) => {
//             console.error("Upload error:", error);
//         });
// };
const uploadFile = (file, field) => {
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
// .overTable {
//     overflow-x: auto;
// }

.text-ellipsis {
    max-width: 200px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    display: inline-block;
    vertical-align: middle;
}

// td:first-child,
// th:first-child {
//     width: 3%;
// } 

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
    min-width: 200px;

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