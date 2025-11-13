<template>
  <div class="frappe-form-builder">
    <!-- Toolbar -->
    <div class="builder-toolbar">
      <button @click="addNewField" class="btn btn-primary">
        <i class="bi bi-plus-circle"></i> Add Field
      </button>
      <button @click="saveFormSchema" class="btn btn-success" :disabled="formFields.length === 0">
        <i class="bi bi-save"></i> Save Schema
      </button>
      <button @click="previewForm" class="btn btn-info" :disabled="formFields.length === 0">
        <i class="bi bi-eye"></i> Preview
      </button>
      <button @click="loadExistingForm" class="btn btn-secondary">
        <i class="bi bi-folder-open"></i> Load Form
      </button>
    </div>

    <!-- Field List with Drag & Drop -->
    <div class="fields-container">
      <draggable
        v-if="formFields.length > 0"
        v-model="formFields"
        :item-key="(item) => item.idx"
        handle=".drag-handle"
        @start="drag = true"
        @end="drag = false"
        :animation="200"
        ghost-class="ghost"
      >
        <template #item="{ element, index }">
          <div class="field-item" :class="{ 'dragging': drag }">
            <div class="field-header">
              <div class="drag-handle">
                <i class="bi bi-grip-vertical"></i>
              </div>
              <div class="field-info">
                <strong>{{ element.label || 'Untitled Field' }}</strong>
                <span class="field-type-badge">{{ element.fieldtype }}</span>
              </div>
              <div class="field-actions">
                <button @click="editField(index)" class="btn-icon" title="Edit">
                  <i class="bi bi-pencil"></i>
                </button>
                <button @click="duplicateField(index)" class="btn-icon" title="Duplicate">
                  <i class="bi bi-files"></i>
                </button>
                <button @click="deleteField(index)" class="btn-icon text-danger" title="Delete">
                  <i class="bi bi-trash"></i>
                </button>
              </div>
            </div>

            <!-- Field Preview -->
            <div class="field-preview" v-if="!element.editing">
              <span class="text-muted">{{ element.fieldname }}</span>
              <span v-if="element.reqd" class="text-danger ms-2">*</span>
              <span v-if="element.read_only" class="badge bg-secondary ms-2">Read Only</span>
              <span v-if="element.hidden" class="badge bg-dark ms-2">Hidden</span>
              <span v-if="element.unique" class="badge bg-info ms-2">Unique</span>
            </div>

            <!-- Field Editor -->
            <div v-if="element.editing" class="field-editor">
              <FieldConfigurator
                :field="element"
                :fieldTypes="fieldTypes"
                @update="updateField(index, $event)"
                @cancel="cancelEdit(index)"
                @save="saveFieldEdit(index)"
              />
            </div>
          </div>
        </template>
      </draggable>

      <!-- Empty State -->
      <div v-if="formFields.length === 0" class="empty-state">
        <i class="bi bi-inbox" style="font-size: 48px;"></i>
        <p>No fields added yet. Click "Add Field" to get started.</p>
      </div>
    </div>

    <!-- Preview Modal -->
    <div v-if="showPreview" class="preview-modal" @click="closePreview">
      <div class="preview-content" @click.stop>
        <div class="preview-header">
          <h4>Form Preview</h4>
          <button @click="closePreview" class="btn-close"></button>
        </div>
        <div class="preview-body">
          <pre>{{ JSON.stringify(formFields, null, 2) }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue';
import draggable from 'vuedraggable';
import FieldConfigurator from './FieldConfigurator.vue';
import { api_req_data, api_post_data } from '@/shared/services/api_req_data';
import { apis } from '@/shared/apiurls';

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
const fieldTypes = ref([]);
const drag = ref(false);
const showPreview = ref(false);
const loading = ref(false);

// Fetch available field types from Frappe
onMounted(async () => {
  await fetchFieldTypes();

  // Load existing fields if provided
  if (props.existingFields && props.existingFields.length > 0) {
    formFields.value = props.existingFields.map((field, idx) => ({
      ...field,
      idx: idx + 1,
      editing: false
    }));
  }
});

/**
 * Fetch all available field types from Frappe
 */
const fetchFieldTypes = async () => {
  try {
    loading.value = true;

    // Try to fetch from API
    if (apis.getFieldTypes) {
      const response = await api_req_data(apis.getFieldTypes);

      if (response && response.field_types) {
        fieldTypes.value = response.field_types;
        loading.value = false;
        return;
      }
    }

    // Fallback to default types
    fieldTypes.value = getDefaultFieldTypes();
    loading.value = false;
  } catch (error) {
    console.error('Error fetching field types:', error);
    fieldTypes.value = getDefaultFieldTypes();
    loading.value = false;
  }
};

/**
 * Default Frappe field types
 */
const getDefaultFieldTypes = () => {
  return [
    'Data',
    'Select',
    'Link',
    'Table',
    'Table MultiSelect',
    'Date',
    'Datetime',
    'Time',
    'Int',
    'Float',
    'Currency',
    'Check',
    'Small Text',
    'Long Text',
    'Text Editor',
    'Code',
    'HTML',
    'HTML Editor',
    'Image',
    'Attach',
    'Attach Image',
    'Signature',
    'Color',
    'Barcode',
    'Geolocation',
    'Duration',
    'Rating',
    'Password',
    'Read Only',
    'Section Break',
    'Column Break',
    'Tab Break',
    'Heading',
    'Button',
    'Dynamic Link',
    'Autocomplete',
    'JSON',
    'Phone',
    'Icon',
    'Percent'
  ].sort();
};

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
 * Update field data
 */
const updateField = (index, updatedField) => {
  formFields.value[index] = { ...formFields.value[index], ...updatedField };
  emit('update', formFields.value);
};

/**
 * Save field edit
 */
const saveFieldEdit = (index) => {
  formFields.value[index].editing = false;

  // Re-index fields
  formFields.value.forEach((field, idx) => {
    field.idx = idx + 1;
  });

  emit('update', formFields.value);
};

/**
 * Cancel field edit
 */
const cancelEdit = (index) => {
  const field = formFields.value[index];

  // Remove if it's a new unsaved field (fieldname still has default pattern)
  if (!field.fieldname || field.fieldname.startsWith('field_')) {
    const fieldnameParts = field.fieldname.split('_');
    const lastPart = fieldnameParts[fieldnameParts.length - 1];

    // Check if it's still the default generated name
    if (!isNaN(lastPart) && field.label === `Field ${lastPart}`) {
      formFields.value.splice(index, 1);

      // Re-index remaining fields
      formFields.value.forEach((f, idx) => {
        f.idx = idx + 1;
      });
      return;
    }
  }

  // Otherwise just close the editor
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

  // Close other editing fields
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

    // Re-index remaining fields
    formFields.value.forEach((field, idx) => {
      field.idx = idx + 1;
    });

    emit('update', formFields.value);
  }
};

/**
 * Generate and save form schema
 */
const saveFormSchema = async () => {
  try {
    // Check if there are unsaved fields in editing mode
    const hasUnsavedFields = formFields.value.some(field => field.editing);
    if (hasUnsavedFields) {
      alert('Please save all fields before saving the form schema.');
      return;
    }

    // Clean up editing flags and prepare schema
    const schema = formFields.value.map((field, idx) => {
      const cleanField = { ...field };
      delete cleanField.editing;
      cleanField.idx = idx + 1;
      return cleanField;
    });

    const payload = {
      form_name: props.formName || 'Untitled Form',
      fields: JSON.stringify(schema)
    };

    // Save via API
    if (apis.saveFormDefinition) {
      loading.value = true;
      const response = await api_post_data(apis.saveFormDefinition, payload);
      loading.value = false;

      if (response && response.success) {
        alert('Form schema saved successfully!');
        emit('save', schema);
      } else {
        throw new Error('Failed to save form schema');
      }
    } else {
      // Emit for parent to handle
      emit('save', schema);
    }
  } catch (error) {
    loading.value = false;
    console.error('Error saving form schema:', error);
    alert('Failed to save form schema. Please try again.');
  }
};

/**
 * Preview the form
 */
const previewForm = () => {
  showPreview.value = true;
  emit('preview', formFields.value);
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
      const response = await api_post_data(apis.getFormDefinition, { form_name: formName });
      loading.value = false;

      if (response && response.success && response.fields) {
        const fields = typeof response.fields === 'string'
          ? JSON.parse(response.fields)
          : response.fields;

        formFields.value = fields.map((field, idx) => ({
          ...field,
          idx: idx + 1,
          editing: false
        }));

        alert('Form loaded successfully!');
      } else {
        throw new Error('Form not found');
      }
    }
  } catch (error) {
    loading.value = false;
    console.error('Error loading form:', error);
    alert('Failed to load form. Please check the form name and try again.');
  }
};

// Expose methods and data for parent components
defineExpose({
  formFields,
  saveFormSchema,
  addNewField,
  getFields: () => formFields.value
});
</script>

<style scoped>
.frappe-form-builder {
  padding: 20px;
  background: #f8f9fa;
  min-height: 100vh;
}

.builder-toolbar {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
  padding: 15px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.builder-toolbar button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.fields-container {
  background: white;
  border-radius: 8px;
  padding: 20px;
  min-height: 400px;
}

.field-item {
  background: #fff;
  border: 2px solid #e9ecef;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  transition: all 0.3s ease;
}

.field-item:hover {
  border-color: #007bff;
  box-shadow: 0 4px 8px rgba(0,123,255,0.1);
}

.field-item.dragging {
  opacity: 0.5;
}

.field-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 10px;
}

.drag-handle {
  cursor: move;
  color: #6c757d;
  font-size: 20px;
  display: flex;
  align-items: center;
}

.drag-handle:hover {
  color: #007bff;
}

.field-info {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}

.field-type-badge {
  background: #e7f3ff;
  color: #007bff;
  padding: 4px 12px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.field-actions {
  display: flex;
  gap: 8px;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  padding: 5px 10px;
  color: #6c757d;
  transition: color 0.2s;
}

.btn-icon:hover {
  color: #007bff;
}

.btn-icon.text-danger:hover {
  color: #dc3545 !important;
}

.field-preview {
  padding: 10px;
  background: #f8f9fa;
  border-radius: 4px;
  font-size: 14px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 5px;
}

.field-editor {
  margin-top: 15px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
}

.empty-state {
  text-align: center;
  padding: 60px 20px;
  color: #6c757d;
}

.ghost {
  opacity: 0.4;
  background: #c8ebfb;
}

/* Preview Modal */
.preview-modal {
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

.preview-content {
  background: white;
  border-radius: 8px;
  width: 90%;
  max-width: 800px;
  max-height: 80vh;
  display: flex;
  flex-direction: column;
}

.preview-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 20px;
  border-bottom: 1px solid #e9ecef;
}

.preview-header h4 {
  margin: 0;
}

.btn-close {
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: #6c757d;
}

.btn-close:hover {
  color: #000;
}

.preview-body {
  padding: 20px;
  overflow: auto;
  flex: 1;
}

.preview-body pre {
  background: #f8f9fa;
  padding: 15px;
  border-radius: 4px;
  overflow: auto;
  font-size: 12px;
}

/* Badges */
.badge {
  font-size: 11px;
  padding: 4px 8px;
}
</style>
