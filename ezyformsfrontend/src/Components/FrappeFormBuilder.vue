<template>
  <div class="frappe-form-builder">
    <!-- Simplified Toolbar -->
    <div class="builder-toolbar-simple">
      <button @click="addNewField" class="btn btn-primary btn-sm">
        <i class="bi bi-plus-circle"></i> Add Field
      </button>
      <button @click="addFieldsToCurrentBlock" class="btn btn-success btn-sm" :disabled="formFields.length === 0">
        <i class="bi bi-check-circle"></i> Add to Form ({{ formFields.length }})
      </button>
      <button @click="clearAllFields" class="btn btn-outline-secondary btn-sm" :disabled="formFields.length === 0">
        <i class="bi bi-trash"></i> Clear All
      </button>
    </div>

    <!-- Field List with Drag & Drop -->
    <div class="fields-container-simple">
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
            class="field-item-simple"
            :class="{ 'dragging': drag }"
            @mouseenter="hoveredField = index"
            @mouseleave="hoveredField = null"
          >
            <div class="field-content">
              <!-- Drag Handle -->
              <div class="drag-handle">
                <i class="bi bi-grip-vertical"></i>
              </div>

              <!-- Field Editor (Always Visible) -->
              <div class="field-editor-inline">
                <!-- Label -->
                <input
                  v-model="element.label"
                  placeholder="Field Label"
                  class="form-control form-control-sm mb-1"
                  @input="generateFieldnameFromLabel(index)"
                />

                <div class="row g-2">
                  <!-- Field Type -->
                  <div class="col-md-4">
                    <select
                      v-model="element.fieldtype"
                      class="form-select form-select-sm"
                      @change="onFieldTypeChange(index)"
                    >
                      <option value="">Select Type</option>
                      <option v-for="ft in fieldTypes" :key="ft.type" :value="ft.type">
                        {{ ft.label }}
                      </option>
                    </select>
                  </div>

                  <!-- Fieldname -->
                  <div class="col-md-4">
                    <input
                      v-model="element.fieldname"
                      type="text"
                      class="form-control form-control-sm"
                      placeholder="fieldname"
                    />
                  </div>

                  <!-- Validation Checkboxes -->
                  <div class="col-md-4">
                    <div class="d-flex gap-2 flex-wrap">
                      <div class="form-check form-check-inline">
                        <input
                          v-model="element.reqd"
                          type="checkbox"
                          class="form-check-input"
                          :id="`reqd-${index}`"
                          :true-value="1"
                          :false-value="0"
                        />
                        <label class="form-check-label small" :for="`reqd-${index}`">Required</label>
                      </div>
                      <div class="form-check form-check-inline">
                        <input
                          v-model="element.unique"
                          type="checkbox"
                          class="form-check-input"
                          :id="`unique-${index}`"
                          :true-value="1"
                          :false-value="0"
                        />
                        <label class="form-check-label small" :for="`unique-${index}`">Unique</label>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Options (for Select, Link, etc.) -->
                <div v-if="requiresOptions(element.fieldtype)" class="mt-2">
                  <textarea
                    v-if="element.fieldtype === 'Select' || element.fieldtype === 'Small Text'"
                    v-model="element.options"
                    class="form-control form-control-sm"
                    rows="2"
                    :placeholder="getOptionsPlaceholder(element.fieldtype)"
                  ></textarea>
                  <input
                    v-else
                    v-model="element.options"
                    type="text"
                    class="form-control form-control-sm"
                    :placeholder="getOptionsPlaceholder(element.fieldtype)"
                  />
                </div>

                <!-- Description -->
                <input
                  v-model="element.description"
                  type="text"
                  class="form-control form-control-sm mt-1"
                  placeholder="Description (optional)"
                />
              </div>

              <!-- Action Icons -->
              <div class="field-actions">
                <button class="btn btn-sm btn-link text-primary p-0" @click="duplicateField(index)" title="Duplicate">
                  <i class="bi bi-files"></i>
                </button>
                <button class="btn btn-sm btn-link text-danger p-0" @click="deleteField(index)" title="Delete">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>
          </div>
        </template>
      </draggable>

      <!-- Empty State -->
      <div v-if="formFields.length === 0" class="empty-state-simple">
        <i class="bi bi-inbox"></i>
        <p>No fields yet. Click "Add Field" to start.</p>
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
  },
  currentBlockIndex: {
    type: Number,
    default: 0
  }
});

// Emits
const emit = defineEmits(['save', 'update', 'addFields']);

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
const loading = ref(false);
const hoveredField = ref(null);

// Load existing fields
onMounted(async () => {
  if (props.existingFields && props.existingFields.length > 0) {
    formFields.value = props.existingFields.map((field, idx) => ({
      ...field,
      idx: idx + 1
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
    label: '',
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
    documentation_url: ''
  };
};

/**
 * Add a new field
 */
const addNewField = () => {
  const newIdx = formFields.value.length + 1;
  const newField = createNewField(newIdx);
  formFields.value.push(newField);
  emit('update', getCleanFields());
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

  formFields.value.push(fieldToDuplicate);
  emit('update', getCleanFields());
};

/**
 * Delete a field
 */
const deleteField = (index) => {
  const fieldName = formFields.value[index].label || 'this field';

  if (confirm(`Delete "${fieldName}"?`)) {
    formFields.value.splice(index, 1);

    // Re-index remaining fields
    formFields.value.forEach((field, idx) => {
      field.idx = idx + 1;
    });

    emit('update', getCleanFields());
  }
};

/**
 * Clear all fields
 */
const clearAllFields = () => {
  if (confirm('Clear all fields?')) {
    formFields.value = [];
    emit('update', []);
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
  emit('update', getCleanFields());
};

/**
 * Handle field type change
 */
const onFieldTypeChange = (index) => {
  const field = formFields.value[index];

  if (!requiresOptions(field.fieldtype)) {
    field.options = '';
  }
  emit('update', getCleanFields());
};

/**
 * Check if field type requires options
 */
const requiresOptions = (fieldtype) => {
  return ['Select', 'Link', 'Table', 'Table MultiSelect', 'Small Text'].includes(fieldtype);
};

/**
 * Get options placeholder
 */
const getOptionsPlaceholder = (fieldtype) => {
  if (fieldtype === 'Select' || fieldtype === 'Small Text') {
    return 'Option 1\nOption 2\nOption 3';
  } else if (fieldtype === 'Link') {
    return 'DocType Name (e.g., Customer)';
  } else if (fieldtype === 'Table') {
    return 'Child DocType Name';
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
    cleanField.idx = idx + 1;
    return cleanField;
  });
};

/**
 * Add fields to current block
 */
const addFieldsToCurrentBlock = () => {
  // Validate all fields
  for (const field of formFields.value) {
    if (!field.label || !field.fieldname || !field.fieldtype) {
      showError('All fields must have a label, fieldname, and type');
      return;
    }

    if (!isValidFieldname(field.fieldname)) {
      showError(`Invalid fieldname: ${field.fieldname}`);
      return;
    }

    if (requiresOptions(field.fieldtype) && (!field.options || !field.options.trim())) {
      showError(`Options required for ${field.fieldtype} field: ${field.label}`);
      return;
    }
  }

  const cleanFields = getCleanFields();
  emit('addFields', cleanFields);
  showSuccess(`${cleanFields.length} field(s) added to form!`);

  // Clear fields after adding
  formFields.value = [];
};

// Expose methods
defineExpose({
  formFields,
  addFieldsToCurrentBlock,
  addNewField,
  getFields: () => getCleanFields()
});
</script>

<style scoped>
.frappe-form-builder {
  background: #fff;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.builder-toolbar-simple {
  padding: 15px;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  display: flex;
  gap: 10px;
  flex-shrink: 0;
}

.fields-container-simple {
  flex: 1;
  overflow-y: auto;
  padding: 15px;
}

.field-item-simple {
  background: #fff;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  padding: 12px;
  margin-bottom: 12px;
  transition: all 0.2s ease;
}

.field-item-simple:hover {
  border-color: #007bff;
  box-shadow: 0 2px 8px rgba(0,123,255,0.1);
}

.field-item-simple.dragging {
  opacity: 0.5;
}

.field-content {
  display: flex;
  gap: 12px;
  align-items: start;
}

.drag-handle {
  color: #6c757d;
  cursor: move;
  padding-top: 8px;
  flex-shrink: 0;
}

.drag-handle:hover {
  color: #007bff;
}

.field-editor-inline {
  flex: 1;
}

.field-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
  padding-top: 8px;
}

.empty-state-simple {
  text-align: center;
  padding: 60px 20px;
  color: #6c757d;
}

.empty-state-simple i {
  font-size: 48px;
  margin-bottom: 16px;
  display: block;
}

.ghost-field {
  opacity: 0.4;
  background: #e7f3ff;
}

.form-control-sm,
.form-select-sm {
  font-size: 13px;
}

.form-check-label {
  font-size: 12px;
}
</style>
