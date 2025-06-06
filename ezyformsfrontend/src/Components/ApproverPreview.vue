<template>
  <section>

    <div v-if="filteredBlocks.length" class="card p-3">
      <div v-for="(block, blockIndex) in filteredBlocks" :key="blockIndex" class="block-container rounded-2">
        <div v-if="blockIndex === 0"><label class=" fw-bold font-12 ps-2">Request ID: </label> <span class="font-13">
            {{ selectedData.formname }}</span> </div>
        <div v-for="(section, sectionIndex) in block.sections" :key="'preview-' + sectionIndex"
          class="preview-section m-1">
          <div v-if="section.label" class="section-label">
            <h5 class="m-0 fw-bold font-13">{{ section.label }}</h5>
          </div>
          <div class="container-fluid">
            <div class="row" v-for="(row, rowIndex) in section.rows" :key="rowIndex">
              <div v-for="(column, columnIndex) in row.columns" :key="'column-preview-' + columnIndex"
                :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'border-0 bg-transparent' : 'border-0 bg-transparent'"
                class="col dynamicColumn">
                <div v-if="column.label" class="p-1 border-bottom">
                  <h6 class="m-0 font-12">{{ column.label }}</h6>
                </div>
                <div class="mx-1 my-1">
                  <div v-for="(field, fieldIndex) in column.fields" :key="'field-preview-' + fieldIndex" :class="(props.readonlyFor === 'true' || blockIndex < currentLevel) && field.fieldtype !== 'Small Text' && field.fieldtype !== 'Text'
                    ? (field.label === 'Approved By' ? 'align-items-end' : 'align-items-start')
                    : ''">
                    <div :class="(props.readonlyFor === 'true' || blockIndex < currentLevel) && field.fieldtype !== 'Small Text' && field.fieldtype !== 'Text' || field.fieldtype === 'Check'
                      ? 'd-flex ' + (field.fieldtype === 'Check' ? 'mt-4 flex-row-reverse justify-content-end gap-2 w-0 align-items-start ' : '') + (field.label === 'Approved By' ? 'align-items-end' : 'align-items-center')
                      : ''">


                      <div v-if="field.label && field.fieldtype !== 'Table'">
                        <label :for="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex"
                          class=" label-text  whitespace-nowrap">
                          <span class="font-12 fw-medium">{{ field.label }}</span>
                          <span class="ms-1 text-danger">{{ field.reqd === 1 ? "*" : "" }}</span>
                          <span class="pe-2"
                            v-if="field.fieldtype !== 'Check' && (props.readonlyFor === 'true' || blockIndex < currentLevel)">:</span>
                        </label>
                      </div>
                      <div v-if="field.fieldtype !== 'Table'" :class="field.fieldtype === 'Check' ? 'w-0' : 'w-100'">
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
                          <div class="my-2">

                            <div v-if="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel">
                              <span class=" font-12">{{ field.value }}</span>
                            </div>
                            <div v-else>
                              <Multiselect :multiple="field.fieldtype === 'Table MultiSelect'"
                                :disabled="blockIndex === 0 || props.readonlyFor === 'true' || blockIndex < currentLevel"
                                :options="field.options?.split('\n').filter(opt => opt.trim() !== '') || []"
                                :modelValue="field.value" placeholder="Select"
                                @update:modelValue="(val) => handleSelectChange(val, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)"
                                class="font-11 multiselect" />
                            </div>
                          </div>


                        </template>
                        <template v-if="field.fieldtype === 'Small Text'">
                          <div class="container-fluid">
                            <div class="row">
                              <div class="form-check col-4 mb-1" v-for="(option, index) in field?.options?.split('\n')"
                                :key="index"
                                :class="{ 'd-none': !(JSON.parse(field.value || '[]') || []).includes(option) }">

                                <div>
                                  <input class="form-check-input" type="checkbox"
                                    :disabled="blockIndex === 0 || props.readonlyFor === 'true'"
                                    :checked="(JSON.parse(field.value || '[]') || []).includes(option)" :value="option"
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
                        </template>

                        <template v-else-if="field.fieldtype == 'Check'">
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
                        <!-- <i class="bi bi-x-lg position-absolute text-danger cursor-pointer"
                            :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'd-none' : ''"
                            style="top: -10px; right: -5px; font-size: 13px; background: white; border-radius: 50%; padding: 3px"
                            @click="removeFileAtIndex(i)"></i> -->

                        <!-- @click="openInNewWindow(field.value)" -->
                        <template v-else-if="field.fieldtype == 'Attach'">
                          <div v-if="field.value" class="d-flex gap-2 flex-wrap">
                            <div v-for="(file, i) in getFileArray(field.value)" :key="i"
                              class="position-relative d-inline-block"
                              :class="props.readonlyFor === 'true' ? ' border-bottom-0' : ''">
                              <!-- Show file input if flagged for replacement -->
                              <div v-if="replaceInputIndexes.includes(i)">
                                <input type="file" accept="image/jpeg,image/png,application/pdf"
                                  class="form-control previewInputHeight font-10"
                                  @change="logFieldValue($event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)" />
                              </div>

                              <!-- Image block -->
                              <template v-else-if="isImageFile(file)">
                                <img :src="file" class="img-thumbnail cursor-pointer border-0 border-bottom-0"
                                  @click="openFile(file)" style="max-width: 100px; max-height: 100px" />
                                <!-- @mouseover="handleMouseOver(blockIndex + '-' + fieldIndex, i)"
                                @mouseleave="handleMouseLeave(blockIndex + '-' + fieldIndex)" -->

                                <!-- Hover preview -->
                                <div v-if="hoverStates[blockIndex + '-' + fieldIndex] === i"
                                  class="image-popup position-absolute"
                                  style="top: 0; left: 110%; width: 200px; background: white; z-index: 10; box-shadow: 0px 0px 10px rgba(0,0,0,0.2); border-radius: 5px; padding: 5px;">
                                  <img :src="file" alt="Enlarged Preview" style="width: 100%; border-radius: 5px;" />
                                </div>

                                <!-- Remove icon -->
                                <!-- <button
                                      v-if="blockIndex !== 0 && props.readonlyFor !== 'true'"
                                      @click="replaceInput(i)"
                                      class="btn btn-sm btn-outline-secondary position-absolute top-0 end-0"
                                      style="z-index: 20; padding: 2px 6px; font-size: 12px;"
                                    >
                                      ×
                                    </button> -->
                              </template>

                              <!-- PDF block -->
                              <a v-else :href="file" target="_blank"
                                class="d-flex align-items-center justify-content-center mt-2 border rounded bg-light"
                                style="width: 100px; height: 100px; text-decoration: none;">
                                <i class="bi bi-file-earmark-pdf-fill fs-2 text-danger"></i>
                              </a>
                            </div>
                          </div>

                          <!-- Fallback input when there's no file yet -->
                          <input v-else :disabled="props.readonlyFor === 'true' || blockIndex < currentLevel"
                            type="file" accept="image/jpeg,image/png,application/pdf"
                            :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'd-none' : ''"
                            :id="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex"
                            class="form-control previewInputHeight font-10" multiple
                            @change="logFieldValue($event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)" />
                        </template>

                        <template v-else-if="field.fieldtype == 'Link'">
                          <div class="d-flex align-items-center gap-2">
                            <input type="text" :value="field.value"
                              :disabled="blockIndex < currentLevel || props.readonlyFor === 'true'"
                              @input="(e) => onInputChange(e.target.value, field)"
                              :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'border-0 image-border-bottom w-50 pb-0 bg-transparent' : ''"
                              @change="(event) =>
                                logFieldValue(
                                  event,
                                  blockIndex,
                                  sectionIndex,
                                  rowIndex,
                                  columnIndex,
                                  fieldIndex
                                )" class="form-control font-12 " />
                            <button class="btn btn-dark text-dark bg-white" @click="ClickLink(field)"> <i
                                class="bi bi-link-45deg font-15"></i></button>

                            <!-- <button type="button" class="btn btn-outline-secondary pb-0 btn-sm" data-bs-toggle="modal"
                              :data-bs-target="`#modal-${field.fieldname}`">
                              <i class="bi bi-link-45deg font-13"></i>
                            </button> -->
                          </div>

                          <!-- Bootstrap Modal -->
                          <!-- Bootstrap Modal -->
                          <div class="modal fade" :id="`modal-${field.fieldname}`" tabindex="-1"
                            :aria-labelledby="`label-${field.fieldname}`" aria-hidden="true"
                            :ref="el => setModalRef(el, field)">
                            <div class="modal-dialog modal-dialog-centered modal-lg">
                              <div class="modal-content">
                                <div class="modal-header">
                                  <h5 class="modal-title" :id="`label-${field.fieldname}`">
                                    <!-- Select a  -->
                                    {{ field.label }}
                                  </h5>
                                  <button type="button" class="btn-close" data-bs-dismiss="modal"
                                    aria-label="Close"></button>
                                </div>

                                <div class="modal-body">
                                  <div v-if="ModalData && Object.keys(ModalData).length">
                                    <div class="row mb-3" v-for="(pair, index) in chunkedModalData" :key="index">
                                      <div class="col-md-6" v-for="[key, value] in pair" :key="key">
                                        <label class="form-label fw-semibold text-capitalize">
                                          {{ key.replace(/_/g, ' ') }}:
                                        </label>
                                        <input type="text" class="form-control" :value="value" readonly />
                                      </div>
                                    </div>
                                  </div>
                                  <div v-else>
                                    <p>Loading data...</p>
                                  </div>

                                </div>

                                <!-- <div class="modal-footer">
                                  <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">
                                    Close
                                  </button>
                                  <button type="button" class="btn btn-primary">
                                    Save changes
                                  </button>
                                </div> -->
                              </div>
                            </div>
                          </div>

                        </template>



                        <template v-else-if="field.fieldtype == 'Datetime'">
                          <input type="datetime-local" v-model="field.value"
                            :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'border-0 image-border-bottom bg-white  pb-0 bg-transparent ' : ' '"
                            :disabled="blockIndex" :readOnly="blockIndex < currentLevel || props.readonlyFor === 'true'
                              " :placeholder="'Enter ' + field.label" :name="'field-' +
                                sectionIndex +
                                '-' +
                                columnIndex +
                                '-' +
                                fieldIndex
                                " class="form-control p-1 previewInputHeight" />
                        </template>

                        <!-- Field Type Default -->
                        <template v-else>
                          <input v-if="field.fieldtype == 'Int'"
                            :disabled="blockIndex < currentLevel || props.readonlyFor === 'true'" :readOnly="blockIndex < currentLevel || props.readonlyFor === 'true'
                              " type="number" v-model="field.value"
                            :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'border-0 image-border-bottom w-50 bg-white' : ' '"
                            :placeholder="'Enter ' + field.label" :value="field.value" :name="'field-' +
                              sectionIndex +
                              '-' +
                              columnIndex +
                              '-' +
                              fieldIndex
                              " class="form-control previewInputHeight" />
                          <textarea v-if="field.fieldtype === 'Text'" :disabled="blockIndex < currentLevel"
                            :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'border-0   bg-transparent' : ''"
                            :readOnly="blockIndex === 0 || props.readonlyFor === 'true'" v-model="field.value"
                            :placeholder="'Enter ' + field.label"
                            :name="'field-' + sectionIndex + '-' + columnIndex + '-' + fieldIndex"
                            class="form-control previewInputHeight mt-0 outline-none"
                            :ref="el => setRef(el, sectionIndex, columnIndex, fieldIndex)"
                            @input="adjustHeight(sectionIndex, columnIndex, fieldIndex)" />

                          <template
                            v-if="blockIndex === 0 && field.fieldtype !== 'Int' && field.fieldtype !== 'Text' && field.fieldtype !== 'Select'">
                            <span style="font-size: 12px;"
                              :class="props.readonlyFor === 'true' || blockIndex < currentLevel ? 'border-0 image-border-bottom w-50 bg-transparent' : ''"
                              :value="field.value" :type="field.fieldtype">
                              {{ field.fieldtype === 'Time' ? formatTime(field.value) : field.value }}
                            </span>
                          </template>
                          <template v-else>
                            <component
                              v-if="blockIndex !== 0 && field.fieldtype !== 'Int' && field.fieldtype !== 'Text' && field.fieldtype !== 'Select'"
                              :style="{
                                width: Math.min(100 + (field.value?.length * 2), 600) + 'px'
                              }" :disabled="blockIndex < currentLevel || props.readonlyFor === 'true'"
                              :is="getFieldComponent(field.fieldtype)" :class="props.readonlyFor === 'true' || blockIndex < currentLevel
                                ? 'border-0 image-border-bottom w-50 bg-transparent'
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
                    <div v-if="field.description !== 'Field' && field.fieldtype !== 'Table'"
                      class="w-100 font-11 description-block mt-1">
                      <!-- <span class="fw-semibold"></span><br> -->
                      <span v-html="field.description.replace(/\n/g, '<br>')"></span>
                    </div>
                    <div v-if="blockIndex === 0 && field.fieldtype === 'Table'">
                      <div v-if="props.childHeaders && Object.keys(props.childHeaders).length">
                        <div v-for="(headers, tableName) in props.childHeaders" :key="tableName">
                          <div v-if="field.fieldname === tableName" class="overTable">
                            <div>
                              <span class="font-13 fw-bold tablename">{{ field.label.replace(/_/g, " ") }}</span>
                            </div>

                            <!-- If description === 'true', use 2-column layout -->
                            <div v-if="field.description === 'true'">
                              <div v-for="(row, index) in props.childData[tableName]" :key="index"
                                class="border p-2 mb-3 rounded bg-light">
                                <div class="mb-2 font-12 fw-bold">Block #{{ index + 1 }}</div>
                                <div v-for="i in Math.ceil(headers.length / 2)" :key="i" class="row mb-2">
                                  <div class="col-6" v-for="field in headers.slice((i - 1) * 2, i * 2)"
                                    :key="field.fieldname">
                                    <label class="font-12 fw-semibold">{{ field.label }}</label>

                                    <template v-if="isFilePath(row[field.fieldname])">
                                      <div v-for="(file, i) in row[field.fieldname].split(',')" :key="i"
                                        class="cursor-pointer text-dark d-block" @click="openFile(file)">
                                        <span class="font-12">View Attachment </span><i class="bi bi-eye-fill ps-1"></i>
                                      </div>
                                    </template>


                                    <template v-else>
                                      <input type="text" class="form-control font-12" :value="row[field.fieldname]"
                                        disabled />
                                    </template>
                                  </div>
                                </div>
                              </div>
                            </div>

                            <!-- Else, show table view -->
                            <div v-else class="tableborder-child">
                              <table class="table mb-0">
                                <thead>
                                  <tr>
                                    <!-- <th>#</th> -->
                                    <th v-for="field in headers" :key="field.fieldname" class="text-center">{{
                                      field.label }}</th>
                                  </tr>
                                </thead>
                                <tbody>
                                  <tr v-for="(row, index) in props.childData[tableName]" :key="index">
                                   
                                    <!-- <td>{{ index + 1 }}</td> -->
                                    <td v-for="field in headers" :key="field.fieldname" class="text-center">
                                      <template v-if="isFilePath(row[field.fieldname])">
                                        <div class="d-flex flex-column align-items-center gap-1">
                                          <span
                                            v-for="(file, i) in row[field.fieldname].split(',').filter(f => f.trim() !== '')"
                                            :key="i">
                                            <span class="cursor-pointer text-decoration-underline d-flex mb-1"
                                              @click="openFile(file)">
                                              View <i class="bi bi-eye-fill ps-1"></i>
                                            </span>
                                          </span>
                                        </div>
                                      </template>


                                      <!-- Show normal value if not a file path -->
                                      <span v-else>
                                        {{ row[field.fieldname] || "" }}
                                      </span>
                                    </td>
                                  </tr>
                                </tbody>
                              </table>
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
});

const emit = defineEmits();
const filePaths = ref([]);
const tableName = ref("");
const errorMessages = ref({});

const hoverStates = ref({});
const textAreaRefs = reactive({});
const replaceInputIndexes = ref([]);

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

const isImageFile = (value) => {
  if (!value) return false;
  return /\.(png|jpg|jpeg|gif)$/i.test(value);
};

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
    fields: JSON.stringify(["emp_name", "signature"]),

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
          if (field.label === "Approved By") {
            if (emp_data.value.signature) {

              field.value = emp_data.value.signature;
              emit("updateField", field);
            }

            // if (field.value) {
            //   logFieldValue({ target: { value: field.value } }, lastBlock, sectionIndex, rowIndex, columnIndex, fieldIndex);
            // }
          }
          if (field.label === "Approved On") {
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

const openFile = (filePath) => {
  const fileUrl = filePath.trim();

  if (/\.(pdf)$/i.test(fileUrl)) {
    // For PDFs: open in new tab
    window.open(fileUrl, '_blank');
  } else if (/\.(jpg|jpeg|png|gif)$/i.test(fileUrl)) {
    // For images: create a new tab and write <img> inside it
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
    const files = eve.target.files;
    field["value"] = "";
    for (let i = 0; i < files.length; i++) {
      uploadFile(files[i], field);
    }
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
    } else {
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



</script>

<style lang="scss" scoped>
.overTable {
  overflow: auto;
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
  padding: 2px 2px;
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

.cursor-pointer {
  cursor: pointer;
}

.img-thumbnail {
  cursor: pointer;
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
</style>
