<template>

  <!-- <button type="button" class="btn btn-dark btn-
                  " @click="toggleEdit">
              {{ isEditable ? 'Cancel' : 'Edit' }}
            </button> -->
  <section>

    <div v-if="filteredBlocks.length" class="card p-2">

      <div v-for="(block, blockIndex) in filteredBlocks" :key="blockIndex" class="block-container rounded-2">
        <div v-if="blockIndex === 0"><label class=" fw-bold font-12 ps-2">Request ID: </label> <span class="Request_ID">
            {{ selectedData.formname.replace(/_/g, ' ') }}</span> </div>
        <div v-for="(section, sectionIndex) in block.sections" :key="'preview-' + sectionIndex"
          class="preview-section m-1">
          <div v-if="section.label" class="section-label">
            <h5 class="m-0 fw-bold font-13">{{ section.label }}</h5>
          </div>
          <div class="container-fluid">
            <div class="row " v-for="(row, rowIndex) in section.rows" :key="rowIndex">
              <div v-for="(column, columnIndex) in row.columns" :key="'column-preview-' + columnIndex"
                :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'border-0 bg-transparent' : 'border-0 bg-transparent align-middle'"
                class="col dynamicColumn ">
                <div v-if="column.label" class="p-1 border-bottom">
                  <h6 class="m-0 font-12">{{ column.label }}</h6>
                </div>
                <div class=" m-1">
                  <div v-for="(field, fieldIndex) in column.fields" :key="'field-preview-' + fieldIndex" :class="(props.readonlyFor === 'true' || blockIndex < currentLevel) && field.fieldtype !== 'Small Text' && field.fieldtype !== 'Text'
                    ? (field.label === 'Approved By' ? ' d-flex align-items-end ' : 'd-flex align-items-start')
                    : ''">
                    <div
                      v-if="!(blockIndex !== 0 && !field.value && ['Approver', 'Approved On', 'Approved By', 'Acknowledged By'].includes(field.label))"
                      :class="(props.readonlyFor === 'true' || blockIndex < currentLevel) && field.fieldtype !== 'Small Text' && field.fieldtype !== 'Text' || field.fieldtype === 'Check'
                        ? 'd-flex mb-1 ' + (field.fieldtype === 'Check' ? 'mt-1 flex-row-reverse justify-content-end gap-2 w-0 align-items-start ' : '') + (field.label === 'Approved By' || field.label === 'Acknowledged By' || field.label === 'Requestor Signature' ? 'align-items-start' : '  align-items-start ')
                        : ''">
                      <div v-if="field.label && field.fieldtype !== 'Table' && field.fieldname !== 'auto_calculations'">

                        <label :for="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex"
                          class=" label-text  whitespace-nowrap">
                          <span class="font-12 fw-medium">{{ field.label }}</span>
                          <span class="ms-1 text-danger">{{ field.reqd === 1 ? "*" : "" }}</span>
                          <span class="pe-2"
                            v-if="field.fieldtype !== 'Check' && (props.readonlyFor === 'true' || blockIndex < currentLevel)">:</span>
                        </label>
                      </div>
                      <div v-if="field.fieldtype !== 'Table'" class="field-width"
                        :class="field.fieldtype === 'Check' ? '' : ''">

                        <!-- field.fieldtype === 'Select' || -->
                        <!-- Field Type Select or Multiselect -->
                        <template v-if="field.fieldtype === 'multiselect'">
                          <select :multiple="field.fieldtype === 'multiselect'" :value="field.value" @input="
                            logFieldValue(
                              blockIndex,
                              sectionIndex,
                              rowIndex,
                              columnIndex,
                              fieldIndex
                            )
                            " class="form-select mb-2 font-13">
                            <option v-for="(option, index) in field.options?.split('\n')" :key="index" :value="option">
                              {{ option }}
                            </option>
                          </select>
                        </template>
                        <template v-if="
                          field.fieldtype === 'Select'
                        ">
                          <div class="">

                            <div v-if="props.readonlyFor === 'true' || blockIndex < currentLevel">
                              <span class=" font-12">{{ field.value }}</span>
                            </div>
                            <div v-else>
                              <Multiselect :multiple="field.fieldtype === 'Table MultiSelect'"
                                :disabled="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel"
                                :options="field.options?.split('\n').filter(opt => opt.trim() !== '') || []"
                                :modelValue="field.value" placeholder="Select"
                                @update:modelValue="(val) => handleSelectChange(val, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)"
                                class="font-11 multiselect" />
                              <!-- <Vue3Select  class="font-11" style="min-width: 200px;" :append-to-body="true"
                                                                                  :multiple="field.fieldtype === 'Table MultiSelect'"
                                :disabled="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel"
                                :options="field.options?.split('\n').filter(opt => opt.trim() !== '') || []"
                                :modelValue="field.value" placeholder="Select"
                                @update:modelValue="(val) => handleSelectChange(val, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)" /> -->
                            </div>
                          </div>


                        </template>
                        <template v-if="field.fieldtype === 'Small Text'">
                          <div>
                            <div v-if="props.readonlyFor === 'true' || blockIndex < currentLevel">
                              <div class="row">
                                <template v-for="(option, index) in field?.options?.split('\n')">
                                  <div v-if="(JSON.parse(field.value || '[]') || []).includes(option)" :key="index"
                                    class="col-4  mb-2">
                                    <div class="form-check">
                                      <input class="form-check-input" type="checkbox" :checked="true" :disabled="true"
                                        :id="`${option}-${index}`" />
                                      <label class="form-check-label font-12 m-0 text-dark" :for="`${option}-${index}`">
                                        {{ option }}
                                      </label>
                                    </div>
                                  </div>
                                </template>
                              </div>
                            </div>


                            <div v-else>
                              <div class="container-fluid">
                                <div class="row">
                                  <div class="form-check col-4 mb-1"
                                    v-for="(option, index) in field?.options?.split('\n')" :key="index"
                                    :class="{ 'd-none': index === 0 }">

                                    <div>
                                      <input class="form-check-input" type="checkbox"
                                        :disabled="blockIndex === 0 || props.readonlyFor === 'true'"
                                        :checked="(JSON.parse(field.value || '[]') || []).includes(option)"
                                        :value="option"
                                        :name="`${field.fieldtype}-${blockIndex}-${sectionIndex}-${rowIndex}-${columnIndex}-${fieldIndex}`"
                                        :id="`${option}-${index}`"
                                        @change="(event) => logFieldValue(event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)" />
                                    </div>

                                    <div>
                                      <label class="form-check-label font-12 m-0" :for="`${option}-${index}`">
                                        {{ option }}
                                      </label>
                                    </div>

                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>

                        </template>



                        <template v-else-if="field.fieldtype == 'Check' && field.fieldname !== 'auto_calculations'">


                          <input type="checkbox" :checked="field.value"
                            :disabled="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel"
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
                              " class="form-control fs-6 border-dark form-check-input previewInputHeight font-10" />
                        </template>

                        <!-- Field Type Check or Radio -->
                        <template v-else-if="


                          field.fieldtype === 'radio'
                        ">
                          <div class="container-fluid">
                            <div class="row">
                              <div class="form-check col-4 mb-1" v-for="(option, index) in field?.options?.split(
                                '\n'
                              )" :key="index">
                                <div>
                                  <input v-if="

                                    index !== 0
                                  " class="form-check-input" type="checkbox" :disabled="blockIndex === 0 || props.readonlyFor === 'true'
                                    " :checked="field.value === option" :value="option"
                                    :name="`${field.fieldtype}-${blockIndex}-${sectionIndex}-${rowIndex}-${columnIndex}-${fieldIndex}`"
                                    :id="`${option}-${index}`" @blur="
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

                                  <input v-else-if="field.fieldtype === 'radio'" :disabled="blockIndex === 0 || props.readonlyFor === 'true'
                                    " class="form-check-input" type="radio"
                                    :name="`${field.fieldtype}-${blockIndex}-${sectionIndex}-${rowIndex}-${columnIndex}-${fieldIndex}`"
                                    :id="`${option}-${index}`" :value="option" :checked="field.value === option" @blur="
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
                                  <label class="form-check-label m-0" :for="`${option}-${index}`">
                                    {{ option }}
                                  </label>
                                </div>
                              </div>
                            </div>
                          </div>
                        </template>


                        <!-- @click="openInNewWindow(field.value)" -->
                        <template v-else-if="field.fieldtype == 'Attach'">
                          <div class=" d-flex gap-1">



                            <!-- File Input (if no value or for specific cases) -->
                            <!-- <input
                            v-if="(field.fieldname !== 'requestor_signature' && field.label !== 'Requestor Signature' && blockIndex !== 0 && !field.label.includes('Approved By') && !field.label.includes('Acknowledged By') && props.readonlyFor !== 'true') && (field.value && blockIndex !== 0) || !field.value && props.readonlyFor !== 'true' && blockIndex !== 0"
                            :disabled="props.readonlyFor === 'true' || blockIndex === 0 || blockIndex < currentLevel"
                            type="file" :class="blockIndex < currentLevel ? 'd-none' : ''"
                            accept=".jpeg,.jpg,.png,.pdf,.xlsx,.xls"
                            :id="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex"  :style="{ minWidth: '100px', maxWidth: '200px' }"
                            class="form-control previewInputHeight  font-10 mb-1 mt-1" multiple
                            @change="logFieldValue($event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)" /> -->

                            <input
                              v-if="(field.fieldname !== 'requestor_signature' && field.label !== 'Requestor Signature' && blockIndex !== 0 && !field.label.includes('Approved By') && !field.label.includes('Acknowledged By') && props.readonlyFor !== 'true') && (field.value && blockIndex !== 0) || !field.value && props.readonlyFor !== 'true' && blockIndex !== 0"
                              :disabled="props.readonlyFor === 'true' || blockIndex === 0 || blockIndex < currentLevel"
                              type="file" :class="blockIndex < currentLevel ? 'd-none' : ''"
                              accept=".jpeg,.jpg,.png,.pdf,.xlsx,.xls"
                              :id="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex" style="display: none"
                              class="form-control previewInputHeight font-10 mb-1 mt-1" multiple
                              @change="logFieldValue($event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)" />

                            <!-- Custom file input label (acts as button) -->
                            <label
                              v-if="(field.fieldname !== 'requestor_signature' && field.label !== 'Requestor Signature' && blockIndex !== 0 && !field.label.includes('Approved By') && !field.label.includes('Acknowledged By') && props.readonlyFor !== 'true') && (field.value && blockIndex !== 0) || !field.value && props.readonlyFor !== 'true' && blockIndex !== 0"
                              :for="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex"
                              class="btn btn-sm btn-light font-10 mb-1 mt-1"
                              :class="{ 'disabled': props.readonlyFor === 'true' || blockIndex === 0 || blockIndex < currentLevel }">
                              <i class="bi bi-paperclip me-1"></i> Attach
                            </label>
                            <!-- View Attachments Label -->
                            <!-- ✅ Direct Image Preview for Specific Fields -->
                            <template v-if="field.value && (
                              field.fieldname === 'requestor_signature' ||
                              field.label.includes('Approved By') ||
                              field.label.includes('Acknowledged By')
                            )">
                              <div class="d-flex gap-2 flex-wrap ">
                                <img v-for="(fileUrl, index) in field.value.split(',').map(f => f.trim())" :key="index"
                                  :src="fileUrl"
                                  class="img-thumbnail cursor-pointer imge_top border-0 p-0 border-bottom-0"
                                  style="max-width: 80px; max-height: 25px" @click="previewAttachment(fileUrl)" />
                              </div>
                            </template>

                            <!-- ✅ View Attachments Label for All Other Fields -->
                            <template v-else-if="field.value && field.value.length">
                              <span class="cursor-pointer font-12 d-inline-flex align-items-center mt-1 gap-1"
                                @click="openAttachmentList(field.value)">
                                <span class="text-dark text-decoration-underline font-12 ">View</span>
                                <span>({{field.value.split(',').filter(f => f.trim()).length}})</span>
                                <i class="bi bi-paperclip text-secondary "
                                  style="transform: rotate(-20deg) translateY(-1px); display: inline-block;"></i>
                              </span>
                            </template>
                          </div>
                          <!-- ✅ View Attachments Label for All Other Fields -->
                          <!-- <template v-else-if="field.value && field.value.length"> 
                            <template v-if=" 
                            field.fieldname === 'requestor_signature' ||
                            field.label.includes('Approved By') ||
                            field.label.includes('Acknowledged By')
                          ">
                            <div class="d-flex gap-2 flex-wrap mb-2">
                              <img v-for="(fileUrl, index) in field.value.split(',').map(f => f.trim())" :key="index" 
                                :src="fileUrl" class="img-thumbnail cursor-pointer imge_top border-0 border-bottom-0"
                                style="max-width: 80px; max-height: 60px" @click="previewAttachment(fileUrl)" />
                            </div>
                          </template>
                            
                            <div >
                              <span class="text-dark text-decoration-underline cursor-pointer font-12"
                                @click="openAttachmentList(field.value)">
                                View <i class="bi bi-paperclip"></i>
                              </span>
                            </div>
                          </template> -->


                          <!-- Attachment List Modal -->
                          <div v-if="showListModal" class="modal fade show"
                            style="display: block; background: rgba(0,0,0,0.5); position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 1050;">
                            <div class="modal-dialog modal-dialog-centered modal-lg">
                              <div class="modal-content">

                                <div class="modal-header">
                                  <h5 class="modal-title font-14">Attachments</h5>
                                  <button type="button" @click="closeAttachmentList" class="btn position-absolute"
                                    style="right: 10px; top: 10px;"> &times;</button>
                                </div>

                                <div class="modal-body">
                                  <ul class="list-group font-13">
                                    <li v-for="(url, i) in attachmentList" :key="i"
                                      class="list-group-item d-flex justify-content-between align-items-center">
                                      <!-- <button
                                v-if="hovered[`${field.fieldname}-${i}`] "
                                @click="removeFile(i, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)"
                                class="btn btn-sm btn-light border-0 position-absolute"
                                style="top: -15px; right: -10px; border-radius: 50%; padding: 0 5px; height: 27px;">
                                <i class="bi bi-x fs-6"></i>
                              </button> -->
                                      <!-- && props.readonlyFor !== 'true' && blockIndex !== 0 -->
                                      <span class="d-flex align-items-center gap-2">
                                        <!-- File Type Icon -->
                                        <i v-if="isImageFile(url)"
                                          class="bi bi-file-earmark-image text-secondary fs-5"></i>
                                        <i v-else-if="isPdfFile(url)"
                                          class="bi bi-file-earmark-pdf text-danger fs-5"></i>
                                        <i v-else-if="isExcelFile(url)"
                                          class="bi bi-file-earmark-spreadsheet text-success fs-5"></i>
                                        <i v-else class="bi bi-file-earmark fs-5"></i>

                                        <!-- File Name -->
                                        {{ getFilename(url) }}
                                      </span>
                                      <div class="d-flex gap-2">
                                        <button class="btn btn-sm font-13 btn-light"
                                          @click="previewAttachment(url)">Show</button>
                                        <a :href="url" class="btn font-13 btn-light" download>Download</a>

                                        <button v-if="props.readonlyFor !== 'true' || blockIndex < currentLevel"
                                          class="btn btn-sm btn-outline-dark rounded-circle"
                                          @click="removeFile(i, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)">
                                          <i class="bi bi-x fs-6"></i>
                                        </button>
                                      </div>
                                    </li>
                                  </ul>

                                </div>

                              </div>
                            </div>
                          </div>

                          <!-- Preview Modal -->
                          <div v-if="showPreviewModal" class="modal fade show"
                            style="display: block; background: rgba(0,0,0,0.5); position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 1055;">
                            <div class="modal-dialog modal-dialog-centered modal-xl">
                              <div class="modal-content">

                                <div class="modal-header">
                                  <h5 class="modal-title font-14">Preview: {{ getFilename(previewUrl) }}</h5>
                                  <button type="button" class="btn-close" @click="closePreviewModal">&times;</button>
                                </div>

                                <div class="modal-body text-center">
                                  <img v-if="isImageFile(previewUrl)" :src="previewUrl" class="img-fluid border rounded"
                                    style="max-height: 80vh;" />
                                  <iframe v-else-if="isPdfFile(previewUrl)" :src="previewUrl" width="100%"
                                    height="600px" style="border: none;"></iframe>
                                  <div v-else class="text-center font-12">
                                    <p>Preview not available for this file type. <a :href="previewUrl"
                                        download>Download</a></p>
                                  </div>
                                </div>

                              </div>
                            </div>
                          </div>


                        </template>


                        <!-- Modal -->



                        <!-- Hover preview -->
                        <!-- <div v-if="hoverStates[blockIndex + '-' + fieldIndex] === i"
                                  class="image-popup position-absolute"
                                  style="top: 0; left: 110%; width: 200px; background: white; z-index: 10; box-shadow: 0px 0px 10px rgba(0,0,0,0.2); border-radius: 5px; padding: 5px;">
                                  <img :src="file" alt="Enlarged Preview" style="width: 100%; border-radius: 5px;" />
                                </div> -->

                        <template v-else-if="field.fieldtype === 'Link'">

                          <div v-if="props.readonlyFor === 'true' || blockIndex < currentLevel">
                            <span class="font-12">
                              {{ field.value }}
                            </span>

                          </div>
                          <div v-else>


                            <input type="text" :value="field.value"
                              :disabled="blockIndex < currentLevel || props.readonlyFor === 'true'"
                              @input="(e) => onInputChange(e.target.value, field)"
                              :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'border-0  w-50 pb-0 bg-transparent' : ''"
                              @change="(event) =>
                                logFieldValue(
                                  event,
                                  blockIndex,
                                  sectionIndex,
                                  rowIndex,
                                  columnIndex,
                                  fieldIndex
                                )" class="form-control font-12 " />
                          </div>


                          <!-- <button v-if="field.value && field.label !== 'Department'"
                              class="btn btn-dark text-dark bg-white  p-1" @click="ClickLink(field)"> <i
                                class="bi bi-link-45deg font-15"></i></button> -->


                        </template>
                        <template v-else-if="field.fieldtype == 'Datetime'">
                          <template v-if="props.readonlyFor === 'true' || blockIndex < currentLevel">
                            <span style="font-size: 12px;"
                              :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'border-0  w-50 bg-transparent' : ''"
                              :value="field.value" :type="field.fieldtype">
                              {{ field.fieldtype === 'Time' ? formatTime(field.value) : field.value }}
                            </span>
                          </template>
                          <template v-else>

                            <input type="datetime-local" v-model="field.value"
                              :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'border-0 bg-white  pb-0 bg-transparent ' : ' '"
                              :disabled="['Approved On', 'Acknowledged On'].includes(field.label)"
                              :placeholder="'Enter ' + field.label" :name="'field-' +
                                sectionIndex +
                                '-' +
                                columnIndex +
                                '-' +
                                fieldIndex
                                " class="form-control p-1 previewInputHeight" @blur="
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
                          </template>
                        </template>


                        <!-- Field Type Default -->
                        <template v-else>

                          <textarea v-if="field.fieldtype === 'Text'" :disabled="blockIndex < currentLevel" :class="[
                            'form-control previewInputHeight mt-0 outline-none',
                            (props.readonlyFor === 'true' || blockIndex < currentLevel) ? 'border-0 bg-transparent no-drag' : ''
                          ]" :readOnly="blockIndex === 0 || props.readonlyFor === 'true'" v-model="field.value"
                            :placeholder="'Enter ' + field.label"
                            :name="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex"
                            class="form-control previewInputHeight mt-0 outline-none"
                            :ref="el => setRef(el, sectionIndex, columnIndex, fieldIndex)"
                            @input="adjustHeight(sectionIndex, columnIndex, fieldIndex)" @blur="
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

                          <input v-if="field.fieldtype == 'Int'"
                            :disabled="blockIndex < currentLevel || props.readonlyFor === 'true'" :readOnly="blockIndex < currentLevel || props.readonlyFor === 'true'
                              " type="number" v-model="field.value"
                            :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'border-0  w-50 bg-white' : ' '"
                            :placeholder="'Enter ' + field.label" :value="field.value" :name="'field-' +
                              sectionIndex +
                              '-' +
                              columnIndex +
                              '-' +
                              fieldIndex
                              " class="form-control previewInputHeight" @blur="
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




                          <template
                            v-if="field.fieldtype !== 'Text' && field.fieldtype !== 'Int' && field.fieldtype !== 'Select' && (blockIndex === 0 || props.readonlyFor === 'true')">
                            <span style="font-size: 12px;"
                              :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'border-0  w-50 bg-transparent' : ''"
                              :value="field.value" :type="field.fieldtype">
                              {{ field.fieldtype === 'Time' ? formatTime(field.value) : field.value }}
                            </span>
                          </template>

                          <template v-else>
                            <component
                              v-if="field.fieldtype !== 'Text' && field.fieldtype !== 'Int' && field.fieldtype !== 'Select' && blockIndex !== 0"
                              :style="{
                                width: Math.min(100 + (field.value?.length * 2), 600) + 'px'
                              }" :disabled="blockIndex < currentLevel || props.readonlyFor === 'true'"
                              :is="getFieldComponent(field.fieldtype)" :class="props.readonlyFor === 'true' || blockIndex < currentLevel
                                ? 'border-0  w-50 bg-transparent'
                                : ''" :value="field.fieldtype === 'Time' ? formatTime(field.value) : field.value"
                              :type="field.fieldtype"
                              :readOnly="blockIndex < currentLevel || props.readonlyFor === 'true'"
                              :name="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex" @blur="
                                (event) =>
                                  logFieldValue(
                                    event,
                                    blockIndex,
                                    sectionIndex,
                                    rowIndex,
                                    columnIndex,
                                    fieldIndex
                                  )
                              " class="form-control previewInputHeight w-100 p-1" />
                          </template>
                        </template>
                      </div>
                    </div>
                    <div
                      v-if="field.description !== 'Field' && field.fieldtype !== 'Table' && field.fieldname !== 'auto_calculations' && field.description !== 'Disable'"
                      class="w-100 font-11 description-block mt-1">
                      <!-- <span class="fw-semibold"></span><br> -->
                      <span v-html="field.description.replace(/\n/g, '<br>')"></span>
                    </div>

                    <div v-if="field.fieldtype === 'Table' && field.options !== 'Ezy Item Details'" class="field-width">
                      <div v-if="props.childHeaders && Object.keys(props.childHeaders).length">
                        <div v-for="(headers, tableName) in props.childHeaders" :key="tableName">
                          <!-- || tableName === field.options -->
                          <div v-if="field.fieldname === tableName || tableName === field.options" class="overTable">
                            <div v-if="field.description === 'true'">

                              <div v-for="(row, index) in props.childData[tableName]" :key="index"
                                class="border p-2 mb-3 rounded bg-light">
                                <div class="mb-2 font-12 fw-bold">#{{ blockIndex + 1 }}</div>
                                <div v-for="i in Math.ceil(headers.length / 2)" :key="i" class="row mb-2">
                                  <div class="col-6" v-for="field in headers.slice((i - 1) * 2, i * 2)"
                                    :key="field.fieldname">
                                    <label class="font-12 fw-semibold">{{ field.label }}</label>


                                    <template v-if="field.fieldtype === 'Data' && field.label !== 'Form Name'">

                                      <input :title="row[field.fieldname]" type="text"
                                        :class="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel ? 'bg-white border-0' : null"
                                        :disabled="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel"
                                        class="form-control font-12 px-2"
                                        :maxlength="field.fieldtype === 'Phone' ? '10' : '140'"
                                        v-model="row[field.fieldname]" />
                                    </template>
                                    <template v-if="field.fieldtype === 'Int'">

                                      <input :title="row[field.fieldname]" type="number"
                                        :class="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel ? 'bg-white border-0' : null"
                                        :disabled="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel"
                                        class="form-control font-12 px-2"
                                        :maxlength="field.fieldtype === 'Phone' ? '10' : '140'"
                                        v-model="row[field.fieldname]" />
                                    </template>
                                    <template v-if="field.fieldtype === 'Select'">
                                      <div>

                                        <Multiselect
                                          v-if="props.readonlyFor !== 'true' && blockIndex !== 0 && blockIndex == currentLevel"
                                          :multiple="field.fieldtype === 'Table MultiSelect'"
                                          :disabled="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel"
                                          :options="(field.options?.split('\n').filter(opt => opt.trim() !== '') || [])"
                                          :model-value="row[field.fieldname]" placeholder="Select"
                                          @update:model-value="val => row[field.fieldname] = val"
                                          class="font-11 multiselect" />
                                        <span v-else>
                                          {{ row[field.fieldname] }}

                                        </span>
                                      </div>
                                    </template>
                                    <template v-else-if="field.fieldtype === 'Attach'">
                                      <!-- File Input -->{{ field.value }}
                                      <input multiple type="file" class="form-control font-12"
                                        :disabled="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel"
                                        accept="image/jpeg,image/png,application/pdf"
                                        :class="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel ? 'bg-white d-none border-0' : null"
                                        @change="handleFileUpload($event, row, field.fieldname)" />

                                      <!-- Preview Section -->
                                      <div v-if="row[field.fieldname]" class="d-flex flex-wrap gap-2">
                                        <div v-for="(fileUrl, index) in normalizeFileList(row[field.fieldname])"
                                          :key="index" class="position-relative d-inline-block"
                                          @mouseover="hovered = index" @mouseleave="hovered = null">
                                          <!-- Click to Preview -->
                                          <div @click="openPreview(fileUrl)" style="cursor: pointer">
                                            <!-- Show image thumbnail -->
                                            <img v-if="isImageFile(fileUrl)" :src="fileUrl"
                                              class="img-thumbnail mt-2 border-0"
                                              style="max-width: 100px; max-height: 100px" />

                                            <!-- Show PDF icon -->
                                            <div v-else
                                              class="d-flex align-items-center justify-content-center border mt-2"
                                              style="width: 100px; height: 100px; background: #f9f9f9">
                                              <i class="bi bi-file-earmark-pdf fs-1 text-danger"></i>
                                            </div>
                                          </div>
                                        </div>
                                      </div>

                                      <!-- Modal Preview -->
                                      <div v-if="showModal" class="modal-backdrop" @click.self="closePreview" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                                        background: rgba(0,0,0,0.5); display: flex; align-items: center;
                                        justify-content: center; z-index: 1050;">
                                        <div style="background: white; padding: 20px; max-width: 90%; max-height: 90%;
                                          overflow: auto; border-radius: 8px; position: relative;">
                                          <button @click="closePreview" style="position: absolute; top: 10px; right: 10px;
                                            border: none; background: transparent; font-size: 20px;">
                                            &times;
                                          </button>

                                          <!-- Image Preview -->
                                          <img v-if="isImageFile(previewUrl)" :src="previewUrl"
                                            style="max-width: 100%; max-height: 80vh;" />

                                          <!-- PDF Preview -->
                                          <iframe v-else :src="previewUrl" style="width: 80vw; height: 80vh;"
                                            frameborder="0"></iframe>
                                        </div>
                                      </div>
                                    </template>
                                    <template v-if="field.fieldtype === 'Text'">
                                      <textarea class="form-control font-12" rows="3"
                                        :class="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel ? 'bg-white border-0' : null"
                                        v-model="row[field.fieldname]"
                                        :disabled="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel"
                                        :ref="el => setRef(el, sectionIndex, columnIndex, fieldIndex)"
                                        @input="adjustHeight(sectionIndex, columnIndex, fieldIndex)"
                                        :title="row[field.fieldname]"></textarea>
                                    </template>
                                    <template v-else-if="field.fieldtype === 'Date'">
                                      <input :min="past" :max="today" :title="row[field.fieldname]"
                                        :class="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel ? 'bg-white border-0' : null"
                                        type="date"
                                        :disabled="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel"
                                        class="form-control font-12" v-model="row[field.fieldname]" />
                                    </template>

                                    <template v-else-if="field.fieldtype === 'Datetime'">


                                      <input :title="row[field.fieldname]" type="datetime-local"
                                        :class="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel ? 'bg-white border-0' : null"
                                        :disabled="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel"
                                        class="form-control font-12" v-model="row[field.fieldname]" />
                                      <!-- <template v-else-if="field.fieldtype === 'Data' &&  row[field.fieldname] === 'Type of Manpower'">
                                                                            <Multiselect :multiple="field.fieldtype === 'Table MultiSelect'"
                                                    :maxlength="getMaxLength(field)"
                                                    :options="field.options?.split('\n') || []"
                                                    :modelValue="field.value" placeholder="Select"
                                                    @update:modelValue="(val) => handleSelectChange(val, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)"
                                                    class="font-11 multiselect" />
                                                                        </template> -->

                                    </template>

                                  </div>
                                </div>
                              </div>
                              <button
                                v-if="blockIndex !== 0 && selectedData.formStatus !== 'Completed' && props.readonlyFor !== 'true'"
                                class="btn btn-sm btn-light font-12 my-2" @click="addRow(tableName)">
                                + Add Block
                              </button>
                            </div>

                            <!-- Table layout -->
                            <div v-else class=" ">
                              <div v-if="tableName === 'Vendor Details'">
                                <div>
                                  <div class=" d-flex justify-content-between align-items-center">
                                    <span class="font-13 fw-bold tablename">{{ field.label.replace(/_/g, " ") }}</span>

                                  </div>

                                  <table class="table table-bordered">

                                    <thead class="table-light">
                                      <tr>
                                        <th>Item name</th>
                                        <th v-for="vendor in props.childData.vendor_details" :key="vendor.name">
                                          {{ vendor.vendor_name }} <span class="text-muted fw-normal">(rate/unit)</span>
                                        </th>
                                      </tr>
                                    </thead>

                                    <tbody>
                                      <!-- Item rows -->
                                      <tr v-for="item in props.childData.ezy_item_details" :key="item.name">
                                        <td>
                                          {{ item.item_name }}
                                          <span class="badge bg-secondary">{{ item.item_quantity }} {{
                                            item.item_unit_of_measure }}</span>
                                        </td>
                                        <td v-for="vendor in props.childData.vendor_details" :key="vendor.name">
                                          ₹ {{
                                            JSON.parse(vendor.pricing_details).find(p => p.item_name ===
                                              item.item_name)?.unitPrice || '-'
                                          }}
                                        </td>
                                      </tr>

                                      <!-- Total row -->
                                      <tr>
                                        <td><strong>Total</strong></td>
                                        <td v-for="vendor in props.childData.vendor_details" :key="vendor.name">
                                          <strong>
                                            ₹ {{
                                              JSON.parse(vendor.pricing_details)
                                                .reduce((sum, i) => sum + parseFloat(i.totalPrice), 0)
                                                .toFixed(2)
                                            }}
                                          </strong>
                                        </td>
                                      </tr>

                                      <!-- Separator -->
                                      <tr>
                                        <td colspan="100%" class="bg-light  text-start text-muted">Additional Information</td>
                                      </tr>

                                      <!-- Company Info -->
                                      <tr>
                                        <td>Payment Terms</td>
                                        <td v-for="vendor in props.childData.vendor_details" :key="vendor.name">
                                          {{ vendor.payment_terms || '-' }}
                                        </td>
                                      </tr>
                                      <tr>
                                        <td>GST</td>
                                        <td v-for="vendor in props.childData.vendor_details" :key="vendor.name">
                                          {{ vendor.gst_number || '-' }}
                                        </td>
                                      </tr>
                                      <tr>
                                        <td>Delivery</td>
                                        <td v-for="vendor in props.childData.vendor_details" :key="vendor.name">
                                          {{ vendor.delivery_time || '-' }}
                                        </td>
                                      </tr>
                                      <tr>
                                        <td>Biddle rank</td>
                                        <td v-for="vendor in props.childData.vendor_details" :key="vendor.name">
                                          {{ vendor.biddle_rank || '-' }}<span v-if="vendor.biddle_rank  === 1" class="badge bg-success font-12 "> <i class=" bi bi-check-circle-fill"></i></span>
                                        </td>
                                      </tr>
                                      <tr>
                                        <td>Transport Charges</td>
                                        <td v-for="vendor in props.childData.vendor_details" :key="vendor.name">
                                          {{ vendor.transportation_charges || '-' }}
                                        </td>
                                      </tr>
                                      <tr>
                                        <td>Attachments</td>
                                        <td v-for="vendor in props.childData.vendor_details" :key="vendor.name">
                                          <span v-if="vendor.attachmentUrl" class="text-primary"
                                            style="cursor: pointer">
                                            Preview attachment
                                          </span>
                                        </td>
                                      </tr>
                                      <tr>
                                        <td>Comments</td>
                                        <td v-for="vendor in props.childData.vendor_details" :key="vendor.name">
                                          {{ vendor.remark || '-' }}
                                        </td>
                                      </tr>
                                    </tbody>
                                  </table>
                                </div>



                              </div>
                              <div v-else>
                                <div class=" d-flex justify-content-between align-items-center">
                                  <span class="font-13 fw-bold tablename">{{ field.label.replace(/_/g, " ") }}</span>
                                </div>
                                <table class="table table-rounded tableborder-child mb-0">
                                  <thead>
                                    <tr>
                                      <th v-for="field in headers" :key="field.fieldname" class="text-center">
                                        {{ field.label }}
                                      </th>
                                      <th v-if="blockIndex !== 0 || props.readonlyFor === 'true'" width="3%"></th>
                                    </tr>
                                  </thead>
                                  <tbody>
                                    <!-- .toLowerCase() -->
                                    <tr
                                      v-for="(row, index) in props.childData[tableName.toLowerCase().replace(/ /g, '_')]"
                                      :key="index">
                                      <td v-for="field in headers" :key="field.fieldname"
                                        :style="getTdStyle(field, row[field.fieldname])"
                                        class="text-center align-middle">



                                        <!-- <template v-if="field.fieldtype === 'Attach'">
                                       
                                        <input
                                          v-if="props.readonlyFor !== 'true' && blockIndex !== 0 && blockIndex === currentLevel"
                                          type="file" accept=".jpeg,.jpg,.png,.pdf,.xlsx,.xls" multiple
                                          class="form-control font-12"
                                          @change="handleFileUpload($event, row, field.fieldname)" />

                                       
                                        <div v-if="row[field.fieldname]"
                                          class="d-flex flex-column align-items-center gap-1 mt-2">
                                          <div
                                            v-for="(fileUrl, index) in row[field.fieldname].split(',').map(f => f.trim()).filter(f => f)"
                                            :key="index">

                                            <span class="cursor-pointer text-decoration-underline d-flex mb-1"
                                              @click="openFileModal(fileUrl)">
                                              View <i class="bi bi-eye-fill ps-1"></i>
                                            </span>

                                            <button v-if="props.readonlyFor !== 'true' && blockIndex === currentLevel"
                                              class="btn btn-sm btn-outline-danger ms-2"
                                              @click="removechildFile(index, field, row)">
                                              <i class="bi bi-x"></i>
                                            </button>
                                          </div>
                                        </div>
                                      </template> -->
                                        <template v-if="field.fieldtype === 'Attach'">
                                          <!-- File Input (unchanged) -->
                                          <input
                                            v-if="props.readonlyFor !== 'true' && blockIndex !== 0 && blockIndex === currentLevel"
                                            type="file" accept=".jpeg,.jpg,.png,.pdf,.xlsx,.xls" multiple
                                            class="form-control font-12" style="display: none"
                                            :id="'upload-field-' + blockIndex + '-' + sectionIndex + '-' + columnIndex + '-' + rowIndex"
                                            @change="handleFileUpload($event, row, field.fieldname)" />

                                          <!-- Custom Label Button -->
                                          <label
                                            v-if="props.readonlyFor !== 'true' && blockIndex !== 0 && blockIndex === currentLevel"
                                            :for="'upload-field-' + blockIndex + '-' + sectionIndex + '-' + columnIndex + '-' + rowIndex"
                                            class="btn btn-sm btn-light font-10 mb-1 mt-1">
                                            <i class="bi bi-paperclip me-1"></i> Attach
                                          </label>

                                          <!-- View Attachments Label -->
                                          <div v-if="row[field.fieldname]" class="mt-2">
                                            <span class="cursor-pointer text-decoration-underline"
                                              @click="openAttachmentsList(row[field.fieldname])">
                                              View <i class="bi bi-paperclip"></i>
                                            </span>
                                          </div>

                                          <!-- Attachments List Modal -->
                                          <div class="modal fade" id="attachmentsListModal" tabindex="-1">
                                            <div class="modal-dialog modal-dialog-centered modal-lg">
                                              <div class="modal-content">
                                                <div class="modal-header">
                                                  <h5 class="modal-title">Attachments</h5>
                                                  <button type="button" data-bs-dismiss="modal"
                                                    class="btn position-absolute" style="right: 10px; top: 10px;">
                                                    &times;</button>
                                                </div>
                                                <div class="modal-body">
                                                  <ul class="list-group">
                                                    <li
                                                      class="list-group-item d-flex justify-content-between align-items-center"
                                                      v-for="(file, index) in attachmentFiles" :key="index">
                                                      <span class="d-flex align-items-center gap-2">
                                                        <!-- File Type Icon -->
                                                        <i v-if="isImageFile(file)"
                                                          class="bi bi-file-earmark-image text-secondary fs-5"></i>
                                                        <i v-else-if="isPdfFile(file)"
                                                          class="bi bi-file-earmark-pdf text-danger fs-5"></i>
                                                        <i v-else-if="isExcelFile(file)"
                                                          class="bi bi-file-earmark-spreadsheet text-success fs-5"></i>
                                                        <i v-else class="bi bi-file-earmark fs-5"></i>

                                                        <!-- File Name -->
                                                        {{ getFilename(file) }}
                                                      </span>
                                                      <div>
                                                        <button class="btn btn-sm btn-light me-2"
                                                          @click="ChildpreviewFile(file)">Show</button>
                                                        <a :href="file" target="_blank" download
                                                          class="btn btn-sm btn-light">Download</a>
                                                      </div>
                                                    </li>
                                                  </ul>
                                                </div>
                                              </div>
                                            </div>
                                          </div>

                                          <!-- Preview Modal -->
                                          <div class="modal fade" id="filePreviewModal" tabindex="-1">
                                            <div class="modal-dialog modal-dialog-centered modal-xl">
                                              <div class="modal-content">
                                                <div class="modal-header">
                                                  <h5 class="modal-title">Preview</h5>
                                                  <button type="button" data-bs-dismiss="modal"
                                                    class="btn position-absolute" style="right: 10px; top: 10px;">
                                                    &times; </button>
                                                </div>
                                                <div class="modal-body text-center">
                                                  <template v-if="isImage(previewUrl)">
                                                    <img :src="previewUrl" alt="Preview" class="img-fluid" />
                                                  </template>
                                                  <template v-else-if="isPDF(previewUrl)">
                                                    <iframe :src="previewUrl" class="w-100" style="height: 600px;" />
                                                  </template>
                                                  <template v-else>
                                                    <p>No preview available for this file type.<a :href="previewUrl"
                                                        download>Download</a></p>
                                                  </template>
                                                </div>
                                              </div>
                                            </div>
                                          </div>
                                        </template>


                                        <template v-if="field.fieldtype === 'Data'">
                                          <input
                                            v-if="props.readonlyFor !== 'true' && blockIndex !== 0 && blockIndex == currentLevel"
                                            type="text"
                                            :class="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel ? 'bg-white border-0' : null"
                                            :disabled="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel"
                                            class="form-control form-control-sm font-12 text-center"
                                            v-model="row[field.fieldname]" />
                                          <span v-else>
                                            {{ row[field.fieldname] }}

                                          </span>
                                        </template>
                                        <template v-if="field.fieldtype === 'Link'">
                                          <input
                                            v-if="props.readonlyFor !== 'true' && blockIndex !== 0 && blockIndex == currentLevel"
                                            type="text"
                                            :class="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel ? 'bg-white border-0' : null"
                                            :disabled="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel"
                                            class="form-control form-control-sm font-12 text-center"
                                            v-model="row[field.fieldname]" />
                                          <span v-else>
                                            {{ row[field.fieldname] }}

                                          </span>
                                        </template>



                                        <template v-if="field.fieldtype === 'Datetime'">
                                          <input
                                            v-if="props.readonlyFor !== 'true' && blockIndex !== 0 && blockIndex == currentLevel"
                                            type="datetime-local"
                                            :class="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel ? 'bg-white border-0' : null"
                                            :disabled="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel"
                                            class="form-control form-control-sm font-12 text-center"
                                            v-model="row[field.fieldname]" />
                                          <span v-else>
                                            {{ row[field.fieldname] }}

                                          </span>
                                        </template>
                                        <template v-if="field.fieldtype === 'Text'">
                                          <textarea
                                            v-if="props.readonlyFor !== 'true' && blockIndex !== 0 && blockIndex == currentLevel"
                                            type="text"
                                            :class="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel ? 'bg-white border-0' : null"
                                            :disabled="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel"
                                            class="form-control form-control-sm font-12 text-center"
                                            v-model="row[field.fieldname]"
                                            :ref="el => setRef(el, sectionIndex, columnIndex, fieldIndex)"
                                            @input="adjustHeight(sectionIndex, columnIndex, fieldIndex)" />
                                          <span v-else>
                                            {{ row[field.fieldname] }}

                                          </span>
                                        </template>
                                        <template v-if="field.fieldtype === 'Int'">
                                          <!-- Expression based field -->
                                          <!-- <template v-if="field.description && /[+\-*/]/.test(field.description)">
                                          <input disabled type="number" class="form-control text-center font-12"
                                            :class="blockIndex === 0 || props.readonlyFor === 'true' ? 'bg-white border-0' : null"
                                            :value="calculateFieldExpression(row, field.description, headers)"
                                            readonly />
                                        </template> -->

                                          <!-- Editable input -->
                                          <template v-if="!(blockIndex === 0 || props.readonlyFor === 'true')">
                                            <input type="number" class="form-control text-center font-12"
                                              :class="blockIndex === 0 || props.readonlyFor === 'true' ? 'bg-white border-0' : null"
                                              v-model.number="row[field.fieldname]" />
                                          </template>

                                          <!-- Read-only display -->
                                          <!-- v-else-if="(blockIndex === 0 || props.readonlyFor === 'true')" -->
                                          <template v-else-if="(blockIndex === 0 || props.readonlyFor === 'true')">
                                            <span>
                                              {{ row[field.fieldname] ? row[field.fieldname] : '' }}
                                            </span>
                                          </template>
                                        </template>


                                        <template v-if="field.fieldtype === 'Date'">
                                          <input
                                            v-if="props.readonlyFor !== 'true' && blockIndex !== 0 && blockIndex == currentLevel"
                                            type="date" class="form-control form-control-sm font-12 text-center"
                                            :class="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel ? 'bg-white border-0' : null"
                                            :disabled="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel"
                                            :max="field.fieldname === 'RetrunDate' ? today : null"
                                            :min="field.fieldname === 'RetrunDate' ? oneWeekAgo : null"
                                            v-model="row[field.fieldname]" />
                                          <span v-else>
                                            {{ row[field.fieldname] }}

                                          </span>
                                        </template>



                                        <template v-else-if="field.fieldtype === 'Select'">

                                          <div
                                            v-if="props.readonlyFor !== 'true' && blockIndex !== 0 && blockIndex == currentLevel">
                                            <Multiselect :multiple="field.fieldtype === 'Table MultiSelect'"
                                              :options="field.options?.split('\n').filter(opt => opt.trim() !== '') || []"
                                              :model-value="row[field.fieldname]" placeholder="Select"
                                              @update:model-value="val => row[field.fieldname] = val"
                                              class="font-11 multiselect" />
                                          </div>
                                          <span v-else>
                                            {{ row[field.fieldname] }}

                                          </span>
                                        </template>



                                      </td>
                                      <td v-if="blockIndex !== 0 || props.readonlyFor === 'true'"
                                        class="d-table-cell text-center align-middle removeRowTd">

                                        <span v-if="props.readonlyFor !== 'true'" class="tableRowRemoveBtn "
                                          :class="blockIndex !== 0 && blockIndex < currentLevel ? 'd-none' : null"
                                          @click="removeRow(tableName, index)">
                                          <i class="bi bi-x-lg "></i>
                                        </span>
                                      </td>
                                    </tr>
                                  </tbody>
                                </table>
                              </div>
                              <!-- File Preview Modal -->
                              <div class="modal fade" id="filePreviewModal" tabindex="-1" aria-hidden="true">
                                <div class="modal-dialog modal-lg modal-dialog-centered">
                                  <div class="modal-content">
                                    <div class="modal-header">
                                      <h5 class="modal-title">File Preview</h5>
                                      <button type="button" data-bs-dismiss="modal"
                                        style="position: absolute; top: 10px; right: 10px; border: none; background: transparent; font-size: 20px;">
                                        &times;</button>
                                    </div>
                                    <div class="modal-body text-center">
                                      <div class="d-flex justify-content-between align-items-center">
                                        <div>

                                          <i v-if="isImageFile(previewFile)" class="fas fa-file-image text-primary"></i>
                                          <i v-else-if="isPdfFile(previewFile)" class="fas fa-file-pdf text-danger"></i>
                                          <i v-else class="fas fa-file text-secondary"></i>
                                          <span class="font-13 ps-3">{{ previewFile.split('/').pop() }}</span>
                                        </div>
                                        <div class="d-flex gap-2 align-items-center">
                                          <button type="button" class="btn btn-light btn-sm"
                                            @click="showPreview = !showPreview">
                                            {{ showPreview ? 'Hide' : 'Show' }}
                                          </button>
                                          <a :href="previewFile" download class="btn btn-light btn-sm">Download</a>
                                        </div>
                                      </div>

                                      <div v-if="showPreview" class="preview-area mt-2">
                                        <img v-if="isImageFile(previewFile)" :src="previewFile"
                                          class="img-fluid border rounded" style="max-width: 100%;" />
                                        <iframe v-else-if="isPdfFile(previewFile)" :src="previewFile" width="100%"
                                          height="500px" style="border:1px solid #ccc;"></iframe>
                                        <div v-else class="text-center">
                                          <p>Preview not available for this file type. <a :href="previewFile"
                                              target="_blank">Download</a>
                                          </p>
                                        </div>
                                      </div>
                                    </div>
                                  </div>
                                </div>
                              </div>
                              <button
                                v-if="blockIndex !== 0 && selectedData.formStatus !== 'Completed' && props.readonlyFor !== 'true'"
                                class="btn btn-sm btn-light font-12 my-2" @click="addRow(tableName)">
                                + Add Row
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

  </section>
</template>

<script setup>
import { computed, defineProps, onMounted, ref, watch, nextTick, reactive } from "vue";
import { apis, doctypes, domain } from "../shared/apiurls";
import axiosInstance from "../shared/services/interceptor";
import { useRoute, useRouter } from "vue-router";
import Multiselect from "vue-multiselect";
import "@vueform/multiselect/themes/default.css";
import Vue3Select from 'vue3-select'
import 'vue3-select/dist/vue3-select.css';
const props = defineProps({
  blockArr: {
    type: [Array, null],
    required: true,
  },
  currentLevel: {
    type: String,
    // required: true,
  },
  childHeaders: {
    type: Object,
  },
  childData: {
    type: Object,
  },
  readonlyFor: {
    type: String || Boolean,
  },
  employeeData: {
    type: Array,
  },
});
const route = useRoute();
const router = useRouter();
const selectedData = ref({
  type: route.query.type || "", // Retrieve from query
  formname: route.query.name || "",
  doctype: route.query.doctype_name || "",
  businessUnit: route.query.business_unit || "",
  formStatus: route.query.status || "",
});
const todayDate = new Date();
const today = todayDate.toISOString().split('T')[0];

const lastWeek = new Date();
lastWeek.setDate(todayDate.getDate() - 6); // includes today, so use 6 instead of 7
const oneWeekAgo = lastWeek.toISOString().split('T')[0];
const emit = defineEmits();
const filePaths = ref([]);
const tableName = ref("");
const errorMessages = ref({});
// const editableTables = reactive({});
const hoverStates = ref({});
const textAreaRefs = reactive({});
const replaceInputIndexes = ref([]);
const previewUrl = ref('')
const showModal = ref(false)
const hovered = reactive({});
const showPreview = ref(false);
// const isEditable = ref(false);

// // Example function to toggle edit mode
// function toggleEdit() {
//   isEditable.value = !isEditable.value;
// } 
const openPreview = (url) => {
  previewUrl.value = url
  showModal.value = true
}

const closePreview = () => {
  showModal.value = false
  previewUrl.value = ''
  showPreview.value = false
}
const removechildFile = (index, field, row) => {
  let files = normalizeFileList(row[field.fieldname]);
  files.splice(index, 1);
  row[field.fieldname] = files.join(',');
};

const isImageChildFile = (fileUrl) => {
  return /\.(jpg|jpeg|png)$/i.test(fileUrl);
};
const replaceInput = (index) => {
  if (!replaceInputIndexes.value.includes(index)) {
    replaceInputIndexes.value.push(index);
  }
};
function setRef(el, sectionIndex, columnIndex, fieldIndex) {
  if (!el) return;
  const key = `${sectionIndex}-${columnIndex}-${fieldIndex}`;
  textAreaRefs[key] = el;
  nextTick(() => adjustHeight(sectionIndex, columnIndex, fieldIndex));
}

function adjustHeight(sectionIndex, columnIndex, fieldIndex) {
  const key = `${sectionIndex}-${columnIndex}-${fieldIndex}`;
  const el = textAreaRefs[key];
  if (el) {
    el.style.height = 'auto';
    el.style.height = el.scrollHeight + 'px';
  }
}
function getTdStyle(field, value) {
  if (field.label === 'Type of Manpower') return {};

  const contentLength = value?.length || 0;
  const dynamicWidth = Math.max(contentLength * 10, 100);

  return {
    width: `${dynamicWidth}px`,
    minWidth: '120px',
    maxWidth: '400px',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
    overflow: 'hidden'
  };
}

// const isImageFile = (value) => {
//   if (!value) return false;
//   return /\.(png|jpg|jpeg|gif)$/i.test(value);
// };
function addRow(tableName) {
  const headers = props.childHeaders[tableName];
  const newRow = {};

  headers.forEach((header) => {
    newRow[header.fieldname] = '';
  });

  if (!props.childData[tableName]) {
    props.childData[tableName] = [];
  }

  props.childData[tableName].push(newRow);
}

const removeRow = (tableName, rowIndex) => {
  if (props.childData[tableName]) {
    props.childData[tableName].splice(rowIndex, 1);
  }
};
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
const normalizeFileList = (value) => {
  if (!value) return [];
  if (Array.isArray(value)) return value;
  if (typeof value === 'string') return value.split(',').map(f => f.trim());
  return [];
};
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
    const fileName = `${randomNumber}-@${file.name}`;

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



watch(
  () => props.childData,
  (newVal) => {
    emit('updateTableData', { ...newVal });
  },
  { deep: true }
);
function formatTime(value) {
  if (!value) return '';
  const timeParts = value.split(':');
  return `${timeParts[0]}:${timeParts[1]}`;
}
function getFileArray(value) {
  return value.split(',').map(f => f.trim())
}
onMounted(() => {
  emit("updateField", getAllFieldsData());
  if (selectedData.value.type === 'mytasks') {
    getEmploye()
  }
  Object.values(textAreaRefs).forEach(el => {
    el.style.height = 'auto';
    el.style.height = el.scrollHeight + 'px';
  });


});



const modalRefs = ref({});

function setModalRef(el, field) {
  if (el) {
    modalRefs.value[field.fieldname] = el;
    el.addEventListener("shown.bs.modal", () => {
      if (field.value && field.options) {
        getData(field.value, field.options);
      }
    });
  }
}


const ModalData = ref([])
function getData(selectedFieldValue, selectedfieldOption) {
  const queryParams = {
    filters: JSON.stringify([[]]),
    fields: JSON.stringify(["*"]),
  };

  axiosInstance
    .get(`${apis.resource}${selectedfieldOption}/${selectedFieldValue}`, {
      params: queryParams,
    })
    .then((response) => {
      // console.log("API response:", response.data);
      ModalData.value = response.data
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

function ClickLink(field) {

  router.push({
    name: "LinkPreviewComp",
    query: {
      routepath: route.path,
      LinkDoctype: field.options,
      LinkDoctypeId: field.value,
      routepath: route.query.routepath,
      formname: route.query.name || "", // Retrieve from query
      form_short_name: route.query.doctype_name || "", // Retrieve from query
      type: route.query.type || "", // Retrieve from query
      readOnly: route.query.readOnly, // Retrieve from query
      business_unit: selectedData.value.businessUnit || "", // Retrieve from query
      status: route.query.status
    },

  });
}
const chunkedModalData = computed(() => {
  const entries = Object.entries(ModalData.value || {});
  const chunks = [];
  for (let i = 0; i < entries.length; i += 2) {
    chunks.push(entries.slice(i, i + 2)); // Two fields per row
  }
  return chunks;
});

const emp_data = ref({}); // Use an object to hold both name and signature

function getEmploye() {
  const storedData = JSON.parse(localStorage.getItem("employeeData"));
  // console.log(storedData, "=============================");
  const queryParams = {
    filters: JSON.stringify([["Ezy Employee", "emp_mail_id", "=", storedData?.emp_mail_id]]),
    fields: JSON.stringify(["emp_name", "signature", "designation", "department"]),

  };


  axiosInstance
    .get(`${apis.resource}${doctypes.EzyEmployeeList}`, {
      params: queryParams,
    })
    .then((response) => {
      emp_data.value = {
        emp_name: response.data[0]?.emp_name,
        signature: response.data[0]?.signature,
      };
      // console.log(response);
      // console.log(emp_data.value, "response");
    })
    .catch((error) => {
      console.error("Error fetching user data:", error);
    });
}

// const openInNewWindow = (url) => {
//   window.open(url, '_blank');
// };
// Watch for changes in childData and update tableName
watch(
  () => props.childData,
  (newValue) => {
    if (newValue?.length && newValue[0]?.doctype) {
      tableName.value = newValue[0].doctype.replace(/_/g, " ");
    } else {
      tableName.value = "";
    }
  },
  { immediate: true }
); // Runs immediately in case childData already has a value

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
const filteredBlocks = computed(() => {

  if (!props.blockArr || props.blockArr.length === 0) return [];

  const filtered = [props.blockArr[0]];

  for (let i = 1; i <= props.currentLevel; i++) {
    if (props.blockArr[i]) {
      filtered.push(props.blockArr[i]);
    }
  }

  // Ensure employeeData is valid
  // if (!props.employeeData || props.employeeData.length === 0) {
  //   console.warn("No employeeData available.");
  //   return filtered;
  // }

  // const employee = props.employeeData[0]; // Access first item

  // Create a deep copy before modifying the data
  const updatedBlocks = JSON.parse(JSON.stringify(filtered));

  // Add employeeData values to the last block
  const lastBlock = updatedBlocks[updatedBlocks.length - 1];

  lastBlock.sections?.forEach((section) => {
    section.rows?.forEach((row) => {
      row.columns?.forEach((column) => {
        column.fields?.forEach((field) => {
          if (props.readonlyFor === 'true') return;
          if (field.label === "Approver") {
            if (emp_data.value?.emp_name) {

              field.value = emp_data.value?.emp_name;
              emit("updateField", field);
            }
          }
          if (field.label === "Approved By" || field.label === 'Acknowledged By') {
            if (emp_data.value.signature) {

              field.value = emp_data.value.signature;
              emit("updateField", field);
            }

            // if (field.value) {
            //   logFieldValue({ target: { value: field.value } }, lastBlock, sectionIndex, rowIndex, columnIndex, fieldIndex);
            // }
          }
          if (field.label === "Approved On" || field.label === 'Acknowledged On') {
            const localTime = new Date().toLocaleString("en-CA", {
              timeZone: "Asia/Kolkata", // Change this to your target timezone
              year: "numeric",
              month: "2-digit",
              day: "2-digit",
              hour: "2-digit",
              minute: "2-digit",
              hour12: false,
            }).replace(/,/, "").replace(/\//g, "-");


            field.value = localTime;
            emit("updateField", field);

            // const now = new Date();

            // // Get local time offset in minutes and convert to milliseconds
            // const offset = now.getTimezoneOffset() * 60000;

            // // Adjust time to local timezone
            // const localTime = new Date(now.getTime() - offset)
            //   .toISOString()
            //   .slice(0, 16); // Format to 'YYYY-MM-DDTHH:mm'
            //   console.log(localTime,"----");

            // field.value = localTime;
            // emit("updateField", field);  
          }

        });
      });
    });
  });

  return updatedBlocks;
});

// Get all fields data
const getAllFieldsData = () => {

  const fieldsData = [];
  filteredBlocks.value.forEach((block) => {
    block.sections?.forEach((section) => {
      section.rows?.forEach((row) => {
        row.columns?.forEach((column) => {
          column.fields?.forEach((field) => {
            fieldsData.push({ ...field });
            if (field.fieldtype === "Attach" && field.value) {
              filePaths.value = field.value
                .split(",")
                .map((path) => path.trim());
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

// const selectedFile = ref('');


// const previewVisible = ref(false);

// const openFileModal = (file) => {
//   selectedFile.value = file;
//   previewVisible.value = false;  // Reset preview
//   showModal.value = true;
// };

// const closeModal = () => {
//   showModal.value = false;
//   selectedFile.value = '';
//   previewVisible.value = false;
// };

// const isImageFile = (file) => {
//   return /\.(jpg|jpeg|png|gif)$/i.test(file);
// };

// const isPdfFile = (file) => {
//   return /\.(pdf)$/i.test(file);
// };

// const getFileName = (file) => {
//   try {
//     return decodeURIComponent(file.split('/').pop());
//   } catch {
//     return file;
//   }
// }; 

const previewFile = ref('')

function openFileModal(fileUrl) {
  previewFile.value = fileUrl
  const modal = new bootstrap.Modal(document.getElementById('filePreviewModal'))
  modal.show()
}

// Your helper methods
// function isImageFile(fileUrl) {
//   return /\.(jpeg|jpg|png)$/i.test(fileUrl)
// }
// function isPdfFile(fileUrl) {
//   return /\.pdf$/i.test(fileUrl)
// }
// const removeFile = (
//   fileIndex,
//   blockIndex,
//   sectionIndex,
//   rowIndex,
//   columnIndex,
//   fieldIndex
// ) => {
//   const field =
//     props.blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[
//       columnIndex
//     ].fields[fieldIndex];

//   const files = field.value ? field.value.split(',').map(f => f.trim()) : [];
//   files.splice(fileIndex, 1); // Remove the selected file

//   field.value = files.join(','); // ✅ Important: update the value first

//   emit('updateField', field); // ✅ Now emit the updated field
// };



// const isExcelFile = (url) => {
//   return url.match(/\.(xlsx|xls)$/i);
// };



const openFile = (filePath) => {
  const fileUrl = filePath.trim();

  if (/\.(pdf)$/i.test(fileUrl)) {
    // For PDFs: open in a new tab
    window.open(fileUrl, '_blank');
  } else if (/\.(jpg|jpeg|png|gif)$/i.test(fileUrl)) {
    // For images: open in a new tab with an <img> tag
    const win = window.open();
    win.document.write(`
      <html>
        <head><title>Image Preview</title></head>
        <body style="margin:0;display:flex;justify-content:center;align-items:center;height:100vh;background:#000">
          <img src="${fileUrl}" style="max-width:100%;max-height:100%;" />
        </body>
      </html>
    `);
    win.document.close();
  } else {
    alert('Unsupported file type');
  }
};

const isFilePath = (value) => {
  if (!value) return false;
  return /\.(png|jpg|jpeg|gif|pdf|docx|xlsx|txt)$/i.test(value);
};


watch(
  () => props.blockArr,
  () => {
    emit("updateField", getAllFieldsData());
  },
  { deep: true }
);

const getFieldComponent = (type) => {
  switch (type) {
    case "Data":
      return "input";
    case "Int":
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
      return "input";
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

  if (eve.target.files && eve.target.files.length > 0) {
    let files = Array.from(eve.target.files); // Convert FileList to an array

    // Normalize existing files into an array
    let existingFiles = field["value"]
      ? field["value"].split(',').map(f => f.trim())
      : [];

    const totalFiles = existingFiles.length + files.length;
    if (totalFiles > 10) {
      alert("You can upload a maximum of 10 files.");
      files = files.slice(0, 10 - existingFiles.length); // Only allow up to 5 total
    }

    files.forEach((file) => uploadFile(file, field));

    // ✅ Reset file input to allow same file re-selection
    eve.target.value = null;
    // emit('updateField', field);
  } else if (eve.target.type === "checkbox") {
    if (field.fieldtype === "Check") {
      // Ensure value is a string, not an array
      if (eve.target.checked) {
        // If checked, set the value as a string
        field["value"] = eve.target.checked ? 1 : 0;

      } else {
        // If unchecked, set the value as an empty string (or use any default value)
        field.value = "";
      }
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
      console.log(field.value);
      // console.log(field.value, "selectedValues", selectedValues);



    }

    else {
      // For other types of fields, store the checkbox checked state as boolean (true/false)
      field["value"] = eve.target.checked;
    }
    // emit('updateField', field);
  } else {
    // field['value'] = eve.target.value;
    let inputValue = eve.target.value;

    // Ensure only numbers are stored and +91 is prefixed
    if (field.fieldtype === "Phone") {
      inputValue = inputValue.replace(/\D/g, ""); // Remove non-numeric characters

      if (inputValue.length > 10) {
        inputValue = inputValue.slice(-10); // Keep only last 10 digits
      }

      inputValue = "+91" + inputValue; // Add +91 prefix
    }

    field["value"] = inputValue;
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

const uploadFile = (file, field) => {
  const randomNumber = generateRandomNumber();
  let fileName = `${props.formName}-${randomNumber}-@${file.name}`;

  const formData = new FormData();
  formData.append("file", file, fileName);
  formData.append("is_private", "0");
  formData.append("folder", "Home");
  axiosInstance
    .post(apis.uploadfile, formData)
    .then((res) => {
      // console.log(res, res.message.file_url);
      if (res.message && res.message.file_url) {
        if (field["value"]) {
          field["value"] += `, ${res.message.file_url}`;
        } else {
          field["value"] = res.message.file_url;
        }
        emit("updateField", field);
        // console.log(field);
      } else {
        console.error("file_url not found in the response.");
      }
    })
    .catch((error) => {
      console.error("Upload error:", error);
    });
};
const clearImage = (
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
  field.value = ""; // Reset the field value
};


// Modal handling
// const selectedFileName = ref('');
// const selectedFileUrl = ref('');

// function openFileModal(file) {
//   selectedFileUrl.value = file;
//   const parts = file.split('/');
//   selectedFileName.value = parts[parts.length - 1];
//   showPreview.value = false; // Reset preview when opening modal again

//   const modal = new bootstrap.Modal(document.getElementById('fileModal'));
//   modal.show();
// }

const showListModal = ref(false)
const showPreviewModal = ref(false)

const attachmentList = ref([])

function openAttachmentList(value) {
  attachmentList.value = value.split(',').map(f => f.trim())
  showListModal.value = true
}

function closeAttachmentList() {
  showListModal.value = false
}

function previewAttachment(url) {
  previewUrl.value = url
  showPreviewModal.value = true
}

function closePreviewModal() {
  showPreviewModal.value = false
}

function getFilename(path) {
  return path.split('/').pop()
}

function isImageFile(file) {
  return /\.(jpe?g|png|gif|bmp|webp)$/i.test(file)
}

function isPdfFile(file) {
  return /\.pdf$/i.test(file)
}

function isExcelFile(file) {
  return /\.(xls|xlsx)$/i.test(file)
}
// const removeFile = (
//   fileIndex,
//   blockIndex,
//   sectionIndex,
//   rowIndex,
//   columnIndex,
//   fieldIndex
// ) => {
//   const field =
//     props.blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[
//       columnIndex
//     ].fields[fieldIndex];
//     console.log(field, "field in remove file");

//   const files = field.value ? field.value.split(',').map(f => f.trim()) : [];
//   files.splice(fileIndex, 1); // Remove the selected file

//   field.value = files.join(','); // Update the value

//   emit('updateField', field); // Emit updated field
// };

const removeFile = (
  fileIndex,
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

  console.log(field, "field in remove file");

  const files = field.value ? field.value.split(',').map(f => f.trim()) : [];

  files.splice(fileIndex, 1); // Remove from field value
  attachmentList.value.splice(fileIndex, 1); // ✅ Remove from visible list
  if (attachmentList.value.length === 0) {
    showListModal.value = false; // Close modal if no files left
  }

  field.value = files.join(','); // Update field value string

  emit('updateField', field); // Emit updated field
};


const attachmentFiles = ref([])


// Extract filename
const getFileName = (path) => {
  return path.split('/').pop()
}

// Open modal with list of attachments
const openAttachmentsList = (fileString) => {
  attachmentFiles.value = fileString
    .split(',')
    .map(f => f.trim())
    .filter(f => f)

  const modal = new bootstrap.Modal(document.getElementById('attachmentsListModal'))
  modal.show()
}

// Open preview modal
const ChildpreviewFile = (fileUrl) => {
  previewUrl.value = fileUrl
  const modal = new bootstrap.Modal(document.getElementById('filePreviewModal'))
  modal.show()
}

// Helper to check file type
const isImage = (url) => /\.(jpeg|jpg|png)$/i.test(url)
const isPDF = (url) => /\.pdf$/i.test(url)

</script>

<style lang="scss" scoped>
// .imge_top{
//       position: absolute; top: -4px;
// }
.btn-close {
  background: transparent;
  border: none;
  font-size: 18px;
  cursor: pointer;
}

.overTable {
  overflow: auto;
}

.no-drag {
  user-select: none;
  /* Prevent text selection */
  -webkit-user-drag: none;
  /* Disable drag in Safari/Chrome */
  pointer-events: none;
  /* Prevent interaction (if needed) */
}

.label-text {
  white-space: nowrap;
}

.image-border-bottom {
  border: none;
  padding-bottom: 0;
  border-radius: 0;
  border-bottom: 1px solid #ccc !important;
}

.previewInputHeight {
  /* height: 35px; */
  // margin-top: 5px;
  // margin-bottom: 5px;
  font-size: 12px;
  padding: 3px 3px;
}

.dynamicColumn {
  border: 1px solid #cccccc;
  border-radius: 7px;
  margin: 1px 2px 1px 2px;
  background-color: #ffffff;
  padding: 0;
  padding-bottom: 1px;

}

.section-label {
  padding: 10px 4px;
  font-weight: bold;
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

.tablename {
  color: #999999;
}

.block-container {
  background-color: #fff;
}

input::-webkit-input-placeholder {
  font-size: 10px;
}

.file-cards {
  transition: all 0.1s ease-in-out;
}

.file-cards:hover {
  box-shadow: rgba(50, 50, 93, 0.25) 0px 2px 5px -1px,
    rgba(0, 0, 0, 0.3) 0px 1px 3px -1px;
}

table {
  border-collapse: collapse;
  background-color: #000;
}

th {
  background-color: #f2f2f2 !important;
  text-align: left;
  color: #999999;
  font-size: 12px;
}

td {
  font-size: 12px;
}

// td:first-child {
//   min-width: 50px;

//   width: auto !important;
// }

.tableborder-child {
  border: 1px solid #ccc !important;
  border-radius: 5px !important;
  padding: 0;
  margin: 1px;
}

.rounded-table {
  border-radius: 6px;
  overflow: hidden;
  border-spacing: 0;
  /* remove gaps */
}

.cursor-pointer {
  cursor: pointer;
}

.img-thumbnail {
  cursor: pointer;
  max-height: 30px;
}

.tableborder-child table td {
  word-break: break-word;
  max-width: 150px;
  /* Adjust as needed */
  overflow-wrap: break-word;
  white-space: normal;
}

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

.vs__selected-options {
  font-size: 12px !important;

}

.v-select * {
  box-sizing: border-box;
  font-size: 12px !important;
  height: 32px !important;
  // background-color: white;
}

.form-check-label {
  color: #212529 !important;
  /* Bootstrap's default text color */
  cursor: default;
  opacity: 1 !important;
  /* Remove greyed-out appearance */
}

/* Base font size (desktop) */
.Request_ID {
  font-size: 12px;
}

/* Medium screens (tablet) */
@media (max-width: 992px) {
  .Request_ID {
    font-size: 11px;
  }
}

/* Small screens (mobile) */
@media (max-width: 768px) {
  .Request_ID {
    font-size: 10px;
  }
}

/* Extra small screens */
@media (max-width: 480px) {
  .Request_ID {
    font-size: 9px;
  }
}

.field-width {
  width: 100%;
}
</style>
