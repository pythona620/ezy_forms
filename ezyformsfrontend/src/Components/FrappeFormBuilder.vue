<template>
  <div class="frappe-form-builder">
    <!-- Toolbar -->
    <div class="builder-toolbar">
      <div class="d-flex gap-2">
        <button @click="addNewSection" class="btn btn-primary btn-sm">
          <i class="bi bi-plus-circle"></i> Add Section
        </button>
        <button @click="addFieldsToCurrentBlock" class="btn btn-success btn-sm" :disabled="sections.length === 0">
          <i class="bi bi-check-circle"></i> Add to Form
        </button>
        <button @click="clearAll" class="btn btn-outline-secondary btn-sm" :disabled="sections.length === 0">
          <i class="bi bi-trash"></i> Clear All
        </button>
      </div>
    </div>

    <!-- Sections Container -->
    <div class="sections-container">
      <div v-if="sections.length === 0" class="empty-state">
        <i class="bi bi-inbox"></i>
        <p>No sections yet. Click "Add Section" to start building your form.</p>
      </div>

      <!-- Section List -->
      <draggable
        v-if="sections.length > 0"
        v-model="sections"
        :item-key="(item) => item.id"
        handle=".section-drag-handle"
        @start="drag = true"
        @end="drag = false"
        :animation="200"
        ghost-class="ghost-section"
      >
        <template #item="{ element: section, index: sectionIndex }">
          <div class="section-card" :class="{ 'dragging': drag }">
            <!-- Section Header -->
            <div class="section-header">
              <div class="section-drag-handle">
                <i class="bi bi-grip-vertical"></i>
              </div>
              <div class="section-info flex-grow-1">
                <input
                  v-model="section.label"
                  placeholder="Section Label (e.g., Customer Details)"
                  class="form-control form-control-sm fw-bold"
                />
              </div>
              <div class="section-actions d-flex gap-2 align-items-center">
                <!-- Column Layout Selector -->
                <select v-model.number="section.columns" class="form-select form-select-sm" style="width: auto;">
                  <option :value="1">1 Column</option>
                  <option :value="2">2 Columns</option>
                  <option :value="3">3 Columns</option>
                  <option :value="4">4 Columns</option>
                </select>
                <button class="btn btn-sm btn-link text-danger p-0" @click="removeSection(sectionIndex)" title="Remove Section">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>

            <!-- Section Fields -->
            <div class="section-body">
              <!-- Add Field Button -->
              <button @click="addFieldToSection(sectionIndex)" class="btn btn-outline-primary btn-sm mb-3">
                <i class="bi bi-plus"></i> Add Field to Section
              </button>

              <!-- Fields Grid -->
              <div v-if="section.fields.length > 0" class="fields-grid" :style="{ gridTemplateColumns: `repeat(${section.columns}, 1fr)` }">
                <draggable
                  v-model="section.fields"
                  :item-key="(item) => item.id"
                  handle=".field-drag-handle"
                  :animation="200"
                  ghost-class="ghost-field"
                  class="fields-draggable-container"
                  :style="{ display: 'contents' }"
                >
                  <template #item="{ element: field, index: fieldIndex }">
                    <div class="field-card">
                      <div class="field-header">
                        <div class="field-drag-handle">
                          <i class="bi bi-grip-vertical"></i>
                        </div>
                        <div class="field-actions">
                          <button class="btn btn-sm btn-link text-primary p-0" @click="duplicateField(sectionIndex, fieldIndex)" title="Duplicate">
                            <i class="bi bi-files"></i>
                          </button>
                          <button class="btn btn-sm btn-link text-danger p-0" @click="deleteField(sectionIndex, fieldIndex)" title="Delete">
                            <i class="bi bi-trash"></i>
                          </button>
                        </div>
                      </div>

                      <div class="field-body">
                        <!-- Label -->
                        <input
                          v-model="field.label"
                          placeholder="Field Label"
                          class="form-control form-control-sm mb-2"
                          @input="generateFieldnameFromLabel(sectionIndex, fieldIndex)"
                        />

                        <!-- Field Type -->
                        <select
                          v-model="field.fieldtype"
                          class="form-select form-select-sm mb-2"
                          @change="onFieldTypeChange(sectionIndex, fieldIndex)"
                        >
                          <option value="">Select Type</option>
                          <option v-for="ft in fieldTypes" :key="ft.type" :value="ft.type">
                            {{ ft.label }}
                          </option>
                        </select>

                        <!-- Fieldname (auto-generated, read-only display) -->
                        <div class="mb-2">
                          <small class="text-muted d-block">Fieldname:</small>
                          <code class="small">{{ field.fieldname }}</code>
                        </div>

                        <!-- Options (for Select, Link, etc.) -->
                        <div v-if="requiresOptions(field.fieldtype)" class="mb-2">
                          <textarea
                            v-if="field.fieldtype === 'Select' || field.fieldtype === 'Small Text'"
                            v-model="field.options"
                            class="form-control form-control-sm"
                            rows="3"
                            :placeholder="getOptionsPlaceholder(field.fieldtype)"
                          ></textarea>
                          <input
                            v-else
                            v-model="field.options"
                            type="text"
                            class="form-control form-control-sm"
                            :placeholder="getOptionsPlaceholder(field.fieldtype)"
                          />
                        </div>

                        <!-- Validation Checkboxes -->
                        <div class="d-flex gap-2 mb-2 flex-wrap">
                          <div class="form-check">
                            <input
                              v-model="field.reqd"
                              type="checkbox"
                              class="form-check-input"
                              :id="`reqd-${sectionIndex}-${fieldIndex}`"
                              :true-value="1"
                              :false-value="0"
                            />
                            <label class="form-check-label small" :for="`reqd-${sectionIndex}-${fieldIndex}`">Required</label>
                          </div>
                          <div class="form-check">
                            <input
                              v-model="field.unique"
                              type="checkbox"
                              class="form-check-input"
                              :id="`unique-${sectionIndex}-${fieldIndex}`"
                              :true-value="1"
                              :false-value="0"
                            />
                            <label class="form-check-label small" :for="`unique-${sectionIndex}-${fieldIndex}`">Unique</label>
                          </div>
                        </div>

                        <!-- Description -->
                        <input
                          v-model="field.description"
                          type="text"
                          class="form-control form-control-sm"
                          placeholder="Description (optional)"
                        />
                      </div>
                    </div>
                  </template>
                </draggable>
              </div>

              <div v-else class="empty-fields-state">
                <small class="text-muted">No fields in this section. Click "Add Field to Section" above.</small>
              </div>
            </div>
          </div>
        </template>
      </draggable>
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
const sections = ref([]);
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
const nextFieldId = ref(1);
const nextSectionId = ref(1);

/**
 * Create a new section
 */
const createNewSection = () => {
  return {
    id: `section_${nextSectionId.value++}`,
    label: '',
    columns: 2, // Default to 2 columns
    fields: []
  };
};

/**
 * Add a new section
 */
const addNewSection = () => {
  const newSection = createNewSection();
  sections.value.push(newSection);
  emit('update', getAllFields());
};

/**
 * Remove a section
 */
const removeSection = (sectionIndex) => {
  const section = sections.value[sectionIndex];
  const label = section.label || 'this section';

  if (confirm(`Delete "${label}" and all its fields?`)) {
    sections.value.splice(sectionIndex, 1);
    emit('update', getAllFields());
  }
};

/**
 * Create a new field with default values
 */
const createNewField = () => {
  return {
    id: `field_${nextFieldId.value++}`,
    fieldname: '',
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
 * Add a new field to a section
 */
const addFieldToSection = (sectionIndex) => {
  const newField = createNewField();
  sections.value[sectionIndex].fields.push(newField);
  emit('update', getAllFields());
};

/**
 * Duplicate a field
 */
const duplicateField = (sectionIndex, fieldIndex) => {
  const fieldToDuplicate = { ...sections.value[sectionIndex].fields[fieldIndex] };

  fieldToDuplicate.id = `field_${nextFieldId.value++}`;
  fieldToDuplicate.fieldname = `${fieldToDuplicate.fieldname}_copy`;
  fieldToDuplicate.label = `${fieldToDuplicate.label} (Copy)`;

  sections.value[sectionIndex].fields.push(fieldToDuplicate);
  emit('update', getAllFields());
};

/**
 * Delete a field
 */
const deleteField = (sectionIndex, fieldIndex) => {
  const fieldName = sections.value[sectionIndex].fields[fieldIndex].label || 'this field';

  if (confirm(`Delete "${fieldName}"?`)) {
    sections.value[sectionIndex].fields.splice(fieldIndex, 1);
    emit('update', getAllFields());
  }
};

/**
 * Clear all sections and fields
 */
const clearAll = () => {
  if (confirm('Clear all sections and fields?')) {
    sections.value = [];
    emit('update', []);
  }
};

/**
 * Generate fieldname from label
 */
const generateFieldnameFromLabel = (sectionIndex, fieldIndex) => {
  const field = sections.value[sectionIndex].fields[fieldIndex];
  if (!field.label) return;

  // Always generate fieldname from label
  field.fieldname = field.label
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '');

  emit('update', getAllFields());
};

/**
 * Handle field type change
 */
const onFieldTypeChange = (sectionIndex, fieldIndex) => {
  const field = sections.value[sectionIndex].fields[fieldIndex];

  if (!requiresOptions(field.fieldtype)) {
    field.options = '';
  }
  emit('update', getAllFields());
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
 * Get all fields from all sections
 */
const getAllFields = () => {
  const allFields = [];
  sections.value.forEach(section => {
    section.fields.forEach(field => {
      allFields.push(field);
    });
  });
  return allFields;
};

/**
 * Add fields to current block
 */
const addFieldsToCurrentBlock = () => {
  // Validate all sections and fields
  for (const section of sections.value) {
    for (const field of section.fields) {
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
  }

  // Emit sections with their layout information
  emit('addFields', sections.value);

  const totalFields = getAllFields().length;
  showSuccess(`${sections.value.length} section(s) with ${totalFields} field(s) added to form!`);

  // Clear sections after adding
  sections.value = [];
};

// Expose methods
defineExpose({
  sections,
  addFieldsToCurrentBlock,
  addNewSection,
  getAllFields: () => getAllFields()
});
</script>

<style scoped>
.frappe-form-builder {
  background: #fff;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.builder-toolbar {
  padding: 15px;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  flex-shrink: 0;
}

.sections-container {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #6c757d;
}

.empty-state i {
  font-size: 48px;
  margin-bottom: 16px;
  display: block;
}

.section-card {
  background: #fff;
  border: 2px solid #dee2e6;
  border-radius: 8px;
  margin-bottom: 20px;
  transition: all 0.2s ease;
}

.section-card:hover {
  border-color: #007bff;
  box-shadow: 0 2px 12px rgba(0,123,255,0.15);
}

.section-card.dragging {
  opacity: 0.5;
}

.section-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 15px;
  background: #f8f9fa;
  border-bottom: 1px solid #dee2e6;
  border-radius: 8px 8px 0 0;
}

.section-drag-handle {
  color: #6c757d;
  cursor: move;
  flex-shrink: 0;
}

.section-drag-handle:hover {
  color: #007bff;
}

.section-info {
  flex: 1;
}

.section-body {
  padding: 20px;
}

.fields-grid {
  display: grid;
  gap: 15px;
  margin-bottom: 15px;
}

.fields-draggable-container {
  display: contents;
}

.field-card {
  background: #fff;
  border: 1px solid #dee2e6;
  border-radius: 6px;
  padding: 12px;
  transition: all 0.2s ease;
}

.field-card:hover {
  border-color: #007bff;
  box-shadow: 0 2px 8px rgba(0,123,255,0.1);
}

.field-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.field-drag-handle {
  color: #6c757d;
  cursor: move;
  font-size: 14px;
}

.field-drag-handle:hover {
  color: #007bff;
}

.field-actions {
  display: flex;
  gap: 8px;
}

.field-body {
  /* Field content */
}

.empty-fields-state {
  text-align: center;
  padding: 30px;
  background: #f8f9fa;
  border-radius: 6px;
  border: 1px dashed #dee2e6;
}

.ghost-section {
  opacity: 0.4;
  background: #e7f3ff;
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

code {
  background: #f8f9fa;
  padding: 2px 6px;
  border-radius: 3px;
  font-size: 12px;
}
</style>
