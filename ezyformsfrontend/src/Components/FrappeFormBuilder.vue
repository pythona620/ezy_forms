<template>
  <div class="frappe-form-builder">
    <!-- Toolbar -->
    <div class="builder-toolbar stepperbackground ps-2 pe-2 m-0 d-flex justify-content-between align-items-center">
      <div></div>
      <h1 class="font-14 fw-bold m-0">Advanced Form Builder</h1>
      <div>
        <button @click="addNewField" class="btn btn-light font-13 mx-2">
          <i class="bi bi-plus-circle"></i> Add Field
        </button>
        <button @click="loadExistingForm" class="btn btn-light font-13 mx-2">
          <i class="bi bi-folder-open"></i> Load
        </button>
        <button @click="previewForm" class="btn btn-light font-13 mx-2" :disabled="formFields.length === 0">
          <i class="bi bi-eye"></i> Preview
        </button>
        <button @click="saveFormSchema" class="btn btn-dark bg-dark text-white fw-bold font-13" :disabled="formFields.length === 0">
          <i class="bi bi-save"></i> Save Schema
        </button>
      </div>
    </div>

    <!-- Field List with Drag & Drop -->
    <div class="fields-container mt-3">
      <draggable
        v-if="formFields.length > 0"
        v-model="formFields"
        :item-key="(item) => item.idx"
        handle=".drag-handle"
        @start="drag = true"
        @end="drag = false"
        :animation="200"
        ghost-class="ghost-field"
      >
        <template #item="{ element, index }">
          <div
            class="field-item dynamicColumn px-3 py-2"
            :class="{ 'dragging': drag }"
            @mouseenter="hoveredField = index"
            @mouseleave="hoveredField = null"
          >
            <div class="d-flex justify-content-between align-items-start">
              <div class="flex-grow-1">
                <!-- Field Header -->
                <div class="d-flex align-items-center gap-2 mb-2">
                  <div class="drag-handle" style="cursor: move;">
                    <i class="bi bi-grip-vertical font-16"></i>
                  </div>
                  <div class="flex-grow-1">
                    <input
                      v-if="element.editing"
                      v-model="element.label"
                      placeholder="Name the field"
                      :class="[
                        'border-less-input',
                        'font-14',
                        'p-0',
                        'inputHeight',
                        { 'italic-style': !element.label },
                        { 'fw-medium': element.label }
                      ]"
                      @input="generateFieldnameFromLabel(index)"
                    />
                    <strong v-else class="font-14">{{ element.label || 'Untitled Field' }}</strong>
                  </div>
                  <span class="badge bg-primary font-11">{{ element.fieldtype }}</span>
                </div>

                <!-- Field Preview -->
                <div v-if="!element.editing" class="field-preview-info">
                  <small class="text-muted font-12">{{ element.fieldname }}</small>
                  <span v-if="element.reqd" class="text-danger ms-1">*</span>
                  <span v-if="element.read_only" class="badge bg-secondary ms-1 font-10">Read Only</span>
                  <span v-if="element.hidden" class="badge bg-dark ms-1 font-10">Hidden</span>
                  <span v-if="element.unique" class="badge bg-info ms-1 font-10">Unique</span>
                </div>

                <!-- Field Editor (inline) -->
                <div v-if="element.editing" class="mt-2">
                  <!-- Field Type -->
                  <select
                    v-model="element.fieldtype"
                    class="form-select mb-2 font-13 searchSelect"
                    @change="onFieldTypeChange(index)"
                  >
                    <option value="">Select Type</option>
                    <option v-for="ft in fieldTypes" :key="ft.type" :value="ft.type">
                      {{ ft.label }}
                    </option>
                  </select>

                  <!-- Fieldname -->
                  <input
                    v-model="element.fieldname"
                    type="text"
                    class="form-control mb-2 font-12"
                    placeholder="fieldname (lowercase with underscores)"
                  />
                  <small v-if="!isValidFieldname(element.fieldname)" class="text-danger font-10 d-block mb-2">
                    Invalid fieldname format
                  </small>

                  <!-- Description -->
                  <textarea
                    v-model="element.description"
                    class="form-control mb-2 font-12"
                    rows="2"
                    placeholder="Field description"
                  ></textarea>

                  <!-- Options (for Select, Link, etc.) -->
                  <div v-if="requiresOptions(element.fieldtype)" class="mb-2">
                    <label class="font-12 fw-light">
                      {{ getOptionsLabel(element.fieldtype) }}
                    </label>
                    <textarea
                      v-if="element.fieldtype === 'Select' || element.fieldtype === 'Small Text'"
                      v-model="element.options"
                      class="form-control shadow-none font-12"
                      rows="3"
                      :placeholder="getOptionsPlaceholder(element.fieldtype)"
                    ></textarea>
                    <input
                      v-else
                      v-model="element.options"
                      type="text"
                      class="form-control font-12"
                      :placeholder="getOptionsPlaceholder(element.fieldtype)"
                    />
                    <small v-if="!element.options || !element.options.trim()" class="text-danger font-10">
                      Options are required for this field type
                    </small>
                  </div>

                  <!-- Default Value -->
                  <input
                    v-model="element.default"
                    type="text"
                    class="form-control mb-2 font-12"
                    placeholder="Default value"
                  />

                  <!-- Validation Checkboxes -->
                  <div class="d-flex flex-wrap gap-3 mb-2">
                    <div class="form-check">
                      <input
                        v-model="element.reqd"
                        type="checkbox"
                        class="form-check-input"
                        :id="`reqd-${index}`"
                        :true-value="1"
                        :false-value="0"
                      />
                      <label class="form-check-label font-12" :for="`reqd-${index}`">
                        Mandatory
                      </label>
                    </div>
                    <div class="form-check">
                      <input
                        v-model="element.read_only"
                        type="checkbox"
                        class="form-check-input"
                        :id="`readonly-${index}`"
                        :true-value="1"
                        :false-value="0"
                      />
                      <label class="form-check-label font-12" :for="`readonly-${index}`">
                        Read Only
                      </label>
                    </div>
                    <div class="form-check">
                      <input
                        v-model="element.hidden"
                        type="checkbox"
                        class="form-check-input"
                        :id="`hidden-${index}`"
                        :true-value="1"
                        :false-value="0"
                      />
                      <label class="form-check-label font-12" :for="`hidden-${index}`">
                        Hidden
                      </label>
                    </div>
                    <div class="form-check">
                      <input
                        v-model="element.unique"
                        type="checkbox"
                        class="form-check-input"
                        :id="`unique-${index}`"
                        :true-value="1"
                        :false-value="0"
                      />
                      <label class="form-check-label font-12" :for="`unique-${index}`">
                        Unique
                      </label>
                    </div>
                    <div class="form-check">
                      <input
                        v-model="element.in_list_view"
                        type="checkbox"
                        class="form-check-input"
                        :id="`listview-${index}`"
                        :true-value="1"
                        :false-value="0"
                      />
                      <label class="form-check-label font-12" :for="`listview-${index}`">
                        In List View
                      </label>
                    </div>
                  </div>

                  <!-- Conditional Display -->
                  <details class="mb-2">
                    <summary class="font-12 fw-medium cursor-pointer">Advanced Options</summary>
                    <div class="mt-2">
                      <input
                        v-model="element.depends_on"
                        type="text"
                        class="form-control mb-2 font-12"
                        placeholder="Depends on (e.g., eval:doc.field=='value')"
                      />
                      <input
                        v-model="element.fetch_from"
                        type="text"
                        class="form-control mb-2 font-12"
                        placeholder="Fetch from (e.g., link_field.source_field)"
                      />
                    </div>
                  </details>

                  <!-- Action Buttons -->
                  <div class="d-flex gap-2 mt-2">
                    <button @click="saveFieldEdit(index)" class="btn btn-dark btn-sm font-12">
                      <i class="bi bi-check"></i> Save
                    </button>
                    <button @click="cancelEdit(index)" class="btn btn-secondary btn-sm font-12">
                      Cancel
                    </button>
                  </div>
                </div>
              </div>

              <!-- Action Icons -->
              <div v-if="hoveredField === index && !element.editing" class="FieldcopyRemove">
                <button class="btn btn-light btn-sm bg-transparent py-0" @click="editField(index)" title="Edit">
                  <i class="bi bi-pencil font-13"></i>
                </button>
                <button class="btn btn-light btn-sm bg-transparent py-0" @click="duplicateField(index)" title="Duplicate">
                  <i class="ri-file-copy-line font-13 copyIcon"></i>
                </button>
                <button class="btn btn-light btn-sm bg-transparent trash-btn py-0" @click="deleteField(index)" title="Delete">
                  <i class="bi bi-x-lg font-13"></i>
                </button>
              </div>
            </div>
          </div>
        </template>
      </draggable>

      <!-- Empty State -->
      <div v-if="formFields.length === 0" class="empty-state text-center py-5">
        <i class="bi bi-inbox" style="font-size: 48px; color: #6c757d;"></i>
        <p class="text-muted mt-3">No fields added yet. Click "Add Field" to get started.</p>
      </div>
    </div>

    <!-- Preview Modal -->
    <div v-if="showPreview" class="modal-backdrop" @click="closePreview">
      <div class="modal-content-custom" @click.stop>
        <div class="modal-header-custom">
          <h5 class="font-16 fw-bold m-0">Form Schema Preview</h5>
          <button @click="closePreview" class="btn-close-custom">
            <i class="bi bi-x-lg"></i>
          </button>
        </div>
        <div class="modal-body-custom">
          <pre class="json-preview">{{ JSON.stringify(getCleanFields(), null, 2) }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import draggable from 'vuedraggable';
import axiosInstance from '@/shared/services/interceptor';
import { apis } from '@/shared/apiurls';
import { showSuccess, showError } from '@/shared/services/toast';

// Props
const props = defineProps({
  formName: {
    type: String,
    default: ''
  },
  existingFields: {
    type: Array,
    default: () => []
  }
});

// Emits
const emit = defineEmits(['save', 'preview', 'update']);

// State
const formFields = ref([]);
const fieldTypes = ref([
  { label: "Text", type: "Data" },
  { label: "Time", type: "Time" },
  { label: "Text Area", type: "Text" },
  { label: "Date", type: "Date" },
  { label: "Datetime", type: "Datetime" },
  { label: "Attach", type: "Attach" },
  { label: "Phone", type: "Data" },
  { label: "Check", type: "Check" },
  { label: "Number", type: "Int" },
  { label: "Select", type: "Select" },
  { label: "Multi Select", type: "Small Text" },
  { label: "Link", type: "Link" }
]);
const drag = ref(false);
const showPreview = ref(false);
const loading = ref(false);
const hoveredField = ref(null);

// Load existing fields
onMounted(async () => {
  if (props.existingFields && props.existingFields.length > 0) {
    formFields.value = props.existingFields.map((field, idx) => ({
      ...field,
      idx: idx + 1,
      editing: false
    }));
  }
});

/**
 * Create a new field with default values
 */
const createNewField = (idx) => {
  return {
    idx: idx,
    fieldname: `field_${idx}`,
    fieldtype: 'Data',
    label: `Field ${idx}`,
    description: '',
    options: '',
    reqd: 0,
    read_only: 0,
    hidden: 0,
    default: '',
    depends_on: '',
    mandatory_depends_on: '',
    read_only_depends_on: '',
    permlevel: 0,
    in_list_view: 0,
    in_standard_filter: 0,
    in_global_search: 0,
    bold: 0,
    allow_bulk_edit: 0,
    allow_in_quick_entry: 0,
    allow_on_submit: 0,
    ignore_user_permissions: 0,
    ignore_xss_filter: 0,
    translatable: 0,
    unique: 0,
    fetch_from: '',
    fetch_if_empty: 0,
    columns: 0,
    length: 0,
    precision: '',
    non_negative: 0,
    report_hide: 0,
    collapsible: 0,
    collapsible_depends_on: '',
    print_hide: 0,
    print_hide_if_no_value: 0,
    sort_options: 0,
    remember_last_selected_value: 0,
    is_virtual: 0,
    search_index: 0,
    documentation_url: '',
    editing: true
  };
};

/**
 * Add a new field
 */
const addNewField = () => {
  const newIdx = formFields.value.length + 1;
  const newField = createNewField(newIdx);

  // Close any other editing fields
  formFields.value.forEach(field => {
    field.editing = false;
  });

  formFields.value.push(newField);
};

/**
 * Edit an existing field
 */
const editField = (index) => {
  // Close any other editing fields
  formFields.value.forEach((field, idx) => {
    if (idx !== index) {
      field.editing = false;
    }
  });
  formFields.value[index].editing = true;
};

/**
 * Save field edit
 */
const saveFieldEdit = (index) => {
  const field = formFields.value[index];

  // Validate
  if (!field.label || !field.fieldname || !field.fieldtype) {
    showError('Label, fieldname, and field type are required');
    return;
  }

  if (!isValidFieldname(field.fieldname)) {
    showError('Invalid fieldname format');
    return;
  }

  if (requiresOptions(field.fieldtype) && (!field.options || !field.options.trim())) {
    showError('Options are required for this field type');
    return;
  }

  formFields.value[index].editing = false;

  // Re-index fields
  formFields.value.forEach((f, idx) => {
    f.idx = idx + 1;
  });

  emit('update', getCleanFields());
  showSuccess('Field saved successfully');
};

/**
 * Cancel field edit
 */
const cancelEdit = (index) => {
  const field = formFields.value[index];

  // Remove if it's a new unsaved field
  if (field.fieldname.startsWith('field_') && field.label.startsWith('Field ')) {
    formFields.value.splice(index, 1);
    formFields.value.forEach((f, idx) => {
      f.idx = idx + 1;
    });
    return;
  }

  formFields.value[index].editing = false;
};

/**
 * Duplicate a field
 */
const duplicateField = (index) => {
  const fieldToDuplicate = { ...formFields.value[index] };
  const newIdx = formFields.value.length + 1;

  fieldToDuplicate.idx = newIdx;
  fieldToDuplicate.fieldname = `${fieldToDuplicate.fieldname}_copy`;
  fieldToDuplicate.label = `${fieldToDuplicate.label} (Copy)`;
  fieldToDuplicate.editing = true;

  formFields.value.forEach(field => {
    field.editing = false;
  });

  formFields.value.push(fieldToDuplicate);
};

/**
 * Delete a field
 */
const deleteField = (index) => {
  const fieldName = formFields.value[index].label || 'this field';

  if (confirm(`Are you sure you want to delete "${fieldName}"?`)) {
    formFields.value.splice(index, 1);

    formFields.value.forEach((field, idx) => {
      field.idx = idx + 1;
    });

    emit('update', getCleanFields());
  }
};

/**
 * Generate fieldname from label
 */
const generateFieldnameFromLabel = (index) => {
  const field = formFields.value[index];
  if (!field.label) return;

  if (!field.fieldname || field.fieldname.startsWith('field_')) {
    field.fieldname = field.label
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '_')
      .replace(/^_+|_+$/g, '');
  }
};

/**
 * Handle field type change
 */
const onFieldTypeChange = (index) => {
  const field = formFields.value[index];

  if (!requiresOptions(field.fieldtype)) {
    field.options = '';
  }
};

/**
 * Check if field type requires options
 */
const requiresOptions = (fieldtype) => {
  return ['Select', 'Link', 'Table', 'Table MultiSelect', 'Small Text'].includes(fieldtype);
};

/**
 * Get options label
 */
const getOptionsLabel = (fieldtype) => {
  if (fieldtype === 'Select' || fieldtype === 'Small Text') {
    return 'Enter Options:';
  } else if (fieldtype === 'Link') {
    return 'Search Doctype:';
  } else if (fieldtype === 'Table') {
    return 'Child DocType:';
  }
  return 'Options:';
};

/**
 * Get options placeholder
 */
const getOptionsPlaceholder = (fieldtype) => {
  if (fieldtype === 'Select' || fieldtype === 'Small Text') {
    return 'Enter your Options';
  } else if (fieldtype === 'Link') {
    return 'Type to search DocType...';
  } else if (fieldtype === 'Table') {
    return 'Enter Child DocType name';
  }
  return 'Enter options';
};

/**
 * Validate fieldname
 */
const isValidFieldname = (fieldname) => {
  return /^[a-z_][a-z0-9_]*$/.test(fieldname);
};

/**
 * Get clean fields (without editing flag)
 */
const getCleanFields = () => {
  return formFields.value.map((field, idx) => {
    const cleanField = { ...field };
    delete cleanField.editing;
    cleanField.idx = idx + 1;
    return cleanField;
  });
};

/**
 * Save form schema
 */
const saveFormSchema = async () => {
  try {
    const hasUnsavedFields = formFields.value.some(field => field.editing);
    if (hasUnsavedFields) {
      showError('Please save all fields before saving the form schema');
      return;
    }

    const schema = getCleanFields();

    const payload = {
      form_name: props.formName || 'Untitled Form',
      fields: JSON.stringify(schema)
    };

    if (apis.saveFormDefinition) {
      loading.value = true;
      const response = await axiosInstance.post(apis.saveFormDefinition, payload);
      loading.value = false;

      if (response && response.data && response.data.message && response.data.message.success) {
        showSuccess('Form schema saved successfully!');
        emit('save', schema);
      } else {
        throw new Error('Failed to save form schema');
      }
    } else {
      emit('save', schema);
    }
  } catch (error) {
    loading.value = false;
    console.error('Error saving form schema:', error);
    showError('Failed to save form schema. Please try again.');
  }
};

/**
 * Preview the form
 */
const previewForm = () => {
  showPreview.value = true;
  emit('preview', getCleanFields());
};

/**
 * Close preview modal
 */
const closePreview = () => {
  showPreview.value = false;
};

/**
 * Load an existing form
 */
const loadExistingForm = async () => {
  const formName = prompt('Enter form name to load:');
  if (!formName) return;

  try {
    loading.value = true;

    if (apis.getFormDefinition) {
      const response = await axiosInstance.post(apis.getFormDefinition, { form_name: formName });
      loading.value = false;

      const data = response.data.message;
      if (data && data.success && data.fields) {
        const fields = typeof data.fields === 'string'
          ? JSON.parse(data.fields)
          : data.fields;

        formFields.value = fields.map((field, idx) => ({
          ...field,
          idx: idx + 1,
          editing: false
        }));

        showSuccess('Form loaded successfully!');
      } else {
        throw new Error('Form not found');
      }
    }
  } catch (error) {
    loading.value = false;
    console.error('Error loading form:', error);
    showError('Failed to load form. Please check the form name and try again.');
  }
};

// Expose methods
defineExpose({
  formFields,
  saveFormSchema,
  addNewField,
  getFields: () => getCleanFields()
});
</script>

<style scoped>
/* Match FormStepper Design */
.frappe-form-builder {
  background: #fff;
}

.stepperbackground {
  background-color: #f5f5f5;
  padding: 15px 20px;
  border-radius: 7px;
  margin-bottom: 15px;
}

.fields-container {
  padding: 10px;
}

.dynamicColumn {
  border: 1.5px dashed #cccccc;
  border-radius: 10px;
  margin: 5px;
  background-color: #ffffff;
  transition: all 0.2s ease;
}

.dynamicColumn:hover {
  border: 1px solid rgb(119, 119, 119);
}

.field-item {
  position: relative;
}

.field-item.dragging {
  opacity: 0.5;
}

.drag-handle {
  color: #6c757d;
  cursor: move;
}

.drag-handle:hover {
  color: #007bff;
}

.FieldcopyRemove {
  position: absolute;
  top: 5px;
  right: 5px;
  display: flex;
  gap: 4px;
}

.border-less-input {
  border: 0;
  background: transparent;
  padding-left: 10px;
  width: 100%;
}

.border-less-input:focus {
  border: 0;
  background: transparent;
  outline: 0;
}

.italic-style {
  font-style: italic;
}

.inputHeight {
  height: 36px;
}

.searchSelect {
  background-color: #fff;
  border: 1px solid #ced4da;
  border-radius: 4px;
}

.field-preview-info {
  padding: 8px 10px;
  background: #f8f9fa;
  border-radius: 4px;
  font-size: 12px;
}

.copyIcon {
  color: #6c757d;
}

.trash-btn:hover {
  color: #dc3545;
}

.empty-state {
  padding: 60px 20px;
}

.ghost-field {
  opacity: 0.4;
  background: #e7f3ff;
}

/* Modal Styles */
.modal-backdrop {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
}

.modal-content-custom {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.modal-header-custom {
  padding: 20px;
  border-bottom: 1px solid #e9ecef;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.btn-close-custom {
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: #6c757d;
  padding: 5px 10px;
}

.btn-close-custom:hover {
  color: #000;
}

.modal-body-custom {
  padding: 20px;
  overflow: auto;
  flex: 1;
}

.json-preview {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  overflow: auto;
  font-size: 12px;
  font-family: 'Courier New', monospace;
}

.cursor-pointer {
  cursor: pointer;
}

/* Responsive */
@media (max-width: 768px) {
  .builder-toolbar {
    flex-direction: column;
    align-items: stretch !important;
  }

  .builder-toolbar > div {
    margin-bottom: 10px;
  }
}
</style>
