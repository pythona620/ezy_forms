<template>
  <div class="frappe-form-builder">
    <!-- Toolbar -->
    <div class="builder-toolbar">
      <div class="d-flex gap-2 align-items-center flex-wrap">
        <button @click="addField('field')" class="btn btn-primary btn-sm">
          <i class="bi bi-plus-circle"></i> Add Field
        </button>
        <button @click="addField('section_break')" class="btn btn-outline-primary btn-sm">
          <i class="bi bi-layout-split"></i> Section Break
        </button>
        <button @click="addField('column_break')" class="btn btn-outline-primary btn-sm">
          <i class="bi bi-layout-three-columns"></i> Column Break
        </button>
        <button @click="addField('html')" class="btn btn-outline-primary btn-sm">
          <i class="bi bi-code-square"></i> HTML
        </button>
        <div class="vr"></div>
        <button @click="addFieldsToBlock" class="btn btn-success btn-sm" :disabled="fields.length === 0">
          <i class="bi bi-check-circle"></i> Add to Form ({{ fields.length }})
        </button>
        <button @click="clearAll" class="btn btn-outline-secondary btn-sm" :disabled="fields.length === 0">
          <i class="bi bi-trash"></i> Clear All
        </button>
        <div class="ms-auto">
          <span class="badge bg-secondary">{{ fields.length }} field(s)</span>
        </div>
      </div>
    </div>

    <!-- Fields Container -->
    <div class="fields-container">
      <div v-if="fields.length === 0" class="empty-state">
        <i class="bi bi-inbox"></i>
        <p>No fields yet. Click "Add Field" or add Section/Column breaks to start.</p>
      </div>

      <!-- Fields List with Index -->
      <draggable
        v-if="fields.length > 0"
        v-model="fields"
        :item-key="(item) => item.id"
        handle=".field-drag-handle"
        @start="drag = true"
        @end="onDragEnd"
        :animation="200"
        ghost-class="ghost-field"
      >
        <template #item="{ element: field, index }">
          <div
            class="field-item"
            :class="{
              'dragging': drag,
              'field-section-break': field.fieldtype === 'Section Break',
              'field-column-break': field.fieldtype === 'Column Break',
              'field-html': field.fieldtype === 'HTML'
            }"
            @mouseenter="hoveredField = index"
            @mouseleave="hoveredField = null"
          >
            <!-- Index Badge -->
            <div class="field-index-badge">{{ field.idx }}</div>

            <!-- Field Type Indicator -->
            <div class="field-type-indicator" :title="field.fieldtype">
              <i :class="getFieldTypeIcon(field.fieldtype)"></i>
            </div>

            <div class="field-content">
              <!-- Drag Handle -->
              <div class="field-drag-handle">
                <i class="bi bi-grip-vertical"></i>
              </div>

              <!-- Field Editor -->
              <div class="field-editor">
                <!-- Basic Info Row -->
                <div class="row g-2 mb-2">
                  <div class="col-md-4">
                    <input
                      v-model="field.label"
                      :placeholder="getFieldPlaceholder(field.fieldtype)"
                      class="form-control form-control-sm"
                      @input="generateFieldname(index)"
                    />
                  </div>
                  <div class="col-md-3">
                    <select
                      v-model="field.fieldtype"
                      class="form-select form-select-sm"
                      @change="onFieldTypeChange(index)"
                    >
                      <option value="">Select Type</option>
                      <optgroup label="Text">
                        <option value="Data">Data (Single Line)</option>
                        <option value="Small Text">Small Text (Multi-select)</option>
                        <option value="Text">Text (Multi Line)</option>
                        <option value="Long Text">Long Text (Large)</option>
                        <option value="Text Editor">Text Editor (Rich Text)</option>
                        <option value="Markdown Editor">Markdown Editor</option>
                        <option value="HTML Editor">HTML Editor</option>
                        <option value="Code">Code</option>
                      </optgroup>
                      <optgroup label="Number">
                        <option value="Int">Int (Integer)</option>
                        <option value="Float">Float (Decimal)</option>
                        <option value="Currency">Currency</option>
                        <option value="Percent">Percent</option>
                        <option value="Duration">Duration</option>
                        <option value="Rating">Rating</option>
                      </optgroup>
                      <optgroup label="Date & Time">
                        <option value="Date">Date</option>
                        <option value="Datetime">Datetime</option>
                        <option value="Time">Time</option>
                      </optgroup>
                      <optgroup label="Link">
                        <option value="Link">Link (Foreign Key)</option>
                        <option value="Dynamic Link">Dynamic Link</option>
                        <option value="Table">Table (Child Table)</option>
                        <option value="Table MultiSelect">Table MultiSelect</option>
                      </optgroup>
                      <optgroup label="Select">
                        <option value="Select">Select (Dropdown)</option>
                        <option value="Autocomplete">Autocomplete</option>
                      </optgroup>
                      <optgroup label="Boolean">
                        <option value="Check">Check (Checkbox)</option>
                      </optgroup>
                      <optgroup label="Attachment">
                        <option value="Attach">Attach (File)</option>
                        <option value="Attach Image">Attach Image</option>
                      </optgroup>
                      <optgroup label="Layout">
                        <option value="Section Break">Section Break</option>
                        <option value="Column Break">Column Break</option>
                        <option value="HTML">HTML</option>
                      </optgroup>
                      <optgroup label="Other">
                        <option value="Button">Button</option>
                        <option value="Geolocation">Geolocation</option>
                        <option value="Barcode">Barcode</option>
                        <option value="Color">Color</option>
                        <option value="Icon">Icon</option>
                        <option value="Signature">Signature</option>
                        <option value="JSON">JSON</option>
                      </optgroup>
                    </select>
                  </div>
                  <div class="col-md-3" v-if="!isLayoutField(field.fieldtype)">
                    <div class="input-group input-group-sm">
                      <span class="input-group-text"><i class="bi bi-tag"></i></span>
                      <input
                        v-model="field.fieldname"
                        type="text"
                        class="form-control form-control-sm font-monospace"
                        placeholder="fieldname"
                        :readonly="!field.label"
                      />
                    </div>
                  </div>
                  <div class="col-md-2">
                    <div class="d-flex gap-2">
                      <button
                        class="btn btn-sm btn-outline-primary flex-fill"
                        @click="toggleAdvanced(index)"
                        title="Advanced Options"
                      >
                        <i class="bi bi-sliders"></i>
                      </button>
                      <button
                        class="btn btn-sm btn-outline-secondary"
                        @click="duplicateField(index)"
                        title="Duplicate"
                      >
                        <i class="bi bi-files"></i>
                      </button>
                      <button
                        class="btn btn-sm btn-outline-danger"
                        @click="deleteField(index)"
                        title="Delete"
                      >
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                  </div>
                </div>

                <!-- Quick Options Row (for non-layout fields) -->
                <div v-if="!isLayoutField(field.fieldtype)" class="quick-options mb-2">
                  <div class="row g-2">
                    <!-- Options (for Select, Link, etc.) -->
                    <div v-if="requiresOptions(field.fieldtype)" class="col-md-6">
                      <textarea
                        v-if="field.fieldtype === 'Select' || field.fieldtype === 'Small Text'"
                        v-model="field.options"
                        class="form-control form-control-sm"
                        rows="2"
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

                    <!-- Quick Checkboxes -->
                    <div class="col-md-6">
                      <div class="d-flex gap-3 flex-wrap">
                        <div class="form-check">
                          <input v-model="field.reqd" type="checkbox" class="form-check-input" :id="`reqd-${index}`" :true-value="1" :false-value="0" />
                          <label class="form-check-label small" :for="`reqd-${index}`">Mandatory</label>
                        </div>
                        <div class="form-check">
                          <input v-model="field.read_only" type="checkbox" class="form-check-input" :id="`ro-${index}`" :true-value="1" :false-value="0" />
                          <label class="form-check-label small" :for="`ro-${index}`">Read Only</label>
                        </div>
                        <div class="form-check">
                          <input v-model="field.hidden" type="checkbox" class="form-check-input" :id="`hide-${index}`" :true-value="1" :false-value="0" />
                          <label class="form-check-label small" :for="`hide-${index}`">Hidden</label>
                        </div>
                        <div class="form-check">
                          <input v-model="field.unique" type="checkbox" class="form-check-input" :id="`uniq-${index}`" :true-value="1" :false-value="0" />
                          <label class="form-check-label small" :for="`uniq-${index}`">Unique</label>
                        </div>
                        <div class="form-check">
                          <input v-model="field.bold" type="checkbox" class="form-check-input" :id="`bold-${index}`" :true-value="1" :false-value="0" />
                          <label class="form-check-label small" :for="`bold-${index}`">Bold</label>
                        </div>
                        <div class="form-check" v-if="field.fieldtype === 'Section Break'">
                          <input v-model="field.collapsible" type="checkbox" class="form-check-input" :id="`coll-${index}`" :true-value="1" :false-value="0" />
                          <label class="form-check-label small" :for="`coll-${index}`">Collapsible</label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- HTML Content (for HTML field type) -->
                <div v-if="field.fieldtype === 'HTML'" class="mb-2">
                  <textarea
                    v-model="field.options"
                    class="form-control form-control-sm font-monospace"
                    rows="4"
                    placeholder="Enter HTML content here..."
                  ></textarea>
                </div>

                <!-- Advanced Options Panel -->
                <div v-if="field.showAdvanced" class="advanced-panel">
                  <ul class="nav nav-tabs nav-tabs-sm mb-2">
                    <li class="nav-item">
                      <a class="nav-link" :class="{ active: field.advancedTab === 'config' }" @click="field.advancedTab = 'config'" href="javascript:void(0)">
                        Config
                      </a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link" :class="{ active: field.advancedTab === 'conditional' }" @click="field.advancedTab = 'conditional'" href="javascript:void(0)">
                        Conditional
                      </a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link" :class="{ active: field.advancedTab === 'validation' }" @click="field.advancedTab = 'validation'" href="javascript:void(0)">
                        Validation
                      </a>
                    </li>
                    <li class="nav-item">
                      <a class="nav-link" :class="{ active: field.advancedTab === 'formatting' }" @click="field.advancedTab = 'formatting'" href="javascript:void(0)">
                        Formatting
                      </a>
                    </li>
                  </ul>

                  <!-- Config Tab -->
                  <div v-if="field.advancedTab === 'config'" class="tab-content">
                    <div class="row g-2">
                      <div class="col-md-6">
                        <label class="form-label small">Description</label>
                        <textarea v-model="field.description" class="form-control form-control-sm" rows="2" placeholder="Help text for this field"></textarea>
                      </div>
                      <div class="col-md-6">
                        <label class="form-label small">Default Value</label>
                        <input v-model="field.default" type="text" class="form-control form-control-sm" placeholder="Default value" />
                      </div>
                      <div class="col-md-6" v-if="isNumericField(field.fieldtype)">
                        <label class="form-label small">Precision</label>
                        <input v-model.number="field.precision" type="number" class="form-control form-control-sm" placeholder="Decimal places" />
                      </div>
                      <div class="col-md-6" v-if="field.fieldtype === 'Data'">
                        <label class="form-label small">Max Length</label>
                        <input v-model.number="field.length" type="number" class="form-control form-control-sm" placeholder="Maximum characters" />
                      </div>
                      <div class="col-md-6">
                        <label class="form-label small">Placeholder</label>
                        <input v-model="field.placeholder" type="text" class="form-control form-control-sm" placeholder="Placeholder text" />
                      </div>
                      <div class="col-md-6">
                        <label class="form-label small">Columns (Grid Width)</label>
                        <input v-model.number="field.columns" type="number" class="form-control form-control-sm" placeholder="1-12" min="1" max="12" />
                      </div>
                      <div class="col-md-12">
                        <div class="form-check">
                          <input v-model="field.in_list_view" type="checkbox" class="form-check-input" :id="`list-${index}`" :true-value="1" :false-value="0" />
                          <label class="form-check-label small" :for="`list-${index}`">Show in List View</label>
                        </div>
                        <div class="form-check">
                          <input v-model="field.in_standard_filter" type="checkbox" class="form-check-input" :id="`filt-${index}`" :true-value="1" :false-value="0" />
                          <label class="form-check-label small" :for="`filt-${index}`">In Standard Filter</label>
                        </div>
                        <div class="form-check">
                          <input v-model="field.allow_on_submit" type="checkbox" class="form-check-input" :id="`subm-${index}`" :true-value="1" :false-value="0" />
                          <label class="form-check-label small" :for="`subm-${index}`">Allow on Submit</label>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Conditional Tab -->
                  <div v-if="field.advancedTab === 'conditional'" class="tab-content">
                    <div class="row g-2">
                      <div class="col-md-12">
                        <label class="form-label small">Depends On (Visibility)</label>
                        <input v-model="field.depends_on" type="text" class="form-control form-control-sm font-monospace" placeholder="eval:doc.field_name=='value'" />
                        <small class="text-muted">Example: eval:doc.status=='Active'</small>
                      </div>
                      <div class="col-md-12">
                        <label class="form-label small">Mandatory Depends On</label>
                        <input v-model="field.mandatory_depends_on" type="text" class="form-control form-control-sm font-monospace" placeholder="eval:doc.field_name=='value'" />
                      </div>
                      <div class="col-md-12">
                        <label class="form-label small">Read Only Depends On</label>
                        <input v-model="field.read_only_depends_on" type="text" class="form-control form-control-sm font-monospace" placeholder="eval:doc.field_name=='value'" />
                      </div>
                      <div class="col-md-12" v-if="field.fieldtype === 'Section Break'">
                        <label class="form-label small">Collapsible Depends On</label>
                        <input v-model="field.collapsible_depends_on" type="text" class="form-control form-control-sm font-monospace" placeholder="eval:doc.field_name=='value'" />
                      </div>
                    </div>
                  </div>

                  <!-- Validation Tab -->
                  <div v-if="field.advancedTab === 'validation'" class="tab-content">
                    <div class="row g-2">
                      <div class="col-md-12">
                        <label class="form-label small">Validation Rule (Regex)</label>
                        <div class="input-group input-group-sm mb-2">
                          <input v-model="field.validation_regex" type="text" class="form-control font-monospace" placeholder="^[A-Z0-9]+$" />
                          <button class="btn btn-outline-secondary dropdown-toggle" type="button" data-bs-toggle="dropdown">
                            Presets
                          </button>
                          <ul class="dropdown-menu dropdown-menu-end">
                            <li><a class="dropdown-item" href="javascript:void(0)" @click="field.validation_regex = '^[A-Za-z ]+$'">Letters Only</a></li>
                            <li><a class="dropdown-item" href="javascript:void(0)" @click="field.validation_regex = '^[0-9]+$'">Numbers Only</a></li>
                            <li><a class="dropdown-item" href="javascript:void(0)" @click="field.validation_regex = '^[A-Z0-9]+$'">Uppercase Alphanumeric</a></li>
                            <li><a class="dropdown-item" href="javascript:void(0)" @click="field.validation_regex = '^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$'">Email</a></li>
                            <li><a class="dropdown-item" href="javascript:void(0)" @click="field.validation_regex = '^[0-9]{10}$'">Phone (10 digits)</a></li>
                          </ul>
                        </div>
                        <small class="text-muted">Regex pattern for validation</small>
                      </div>
                      <div class="col-md-12">
                        <label class="form-label small">Validation Message</label>
                        <input v-model="field.validation_message" type="text" class="form-control form-control-sm" placeholder="Custom error message" />
                      </div>
                      <div class="col-md-6" v-if="isNumericField(field.fieldtype)">
                        <div class="form-check">
                          <input v-model="field.non_negative" type="checkbox" class="form-check-input" :id="`nonneg-${index}`" :true-value="1" :false-value="0" />
                          <label class="form-check-label small" :for="`nonneg-${index}`">Non-Negative Only</label>
                        </div>
                      </div>
                    </div>
                  </div>

                  <!-- Formatting Tab -->
                  <div v-if="field.advancedTab === 'formatting'" class="tab-content">
                    <div class="row g-2">
                      <div class="col-md-6" v-if="field.fieldtype === 'Data'">
                        <label class="form-label small">Text Transform</label>
                        <select v-model="field.text_transform" class="form-select form-select-sm">
                          <option value="">None</option>
                          <option value="uppercase">UPPERCASE</option>
                          <option value="lowercase">lowercase</option>
                          <option value="titlecase">Title Case</option>
                        </select>
                      </div>
                      <div class="col-md-6" v-if="field.fieldtype === 'Data'">
                        <label class="form-label small">Auto Trim</label>
                        <select v-model="field.auto_trim" class="form-select form-select-sm">
                          <option value="">No Trim</option>
                          <option value="trim">Trim Both Ends</option>
                          <option value="trim_start">Trim Start</option>
                          <option value="trim_end">Trim End</option>
                        </select>
                      </div>
                      <div class="col-md-12">
                        <div class="form-check">
                          <input v-model="field.translatable" type="checkbox" class="form-check-input" :id="`trans-${index}`" :true-value="1" :false-value="0" />
                          <label class="form-check-label small" :for="`trans-${index}`">Translatable</label>
                        </div>
                        <div class="form-check">
                          <input v-model="field.print_hide" type="checkbox" class="form-check-input" :id="`prthide-${index}`" :true-value="1" :false-value="0" />
                          <label class="form-check-label small" :for="`prthide-${index}`">Hide in Print</label>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
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
  formName: { type: String, default: '' },
  existingFields: { type: Array, default: () => [] },
  currentBlockIndex: { type: Number, default: 0 }
});

// Emits
const emit = defineEmits(['save', 'update', 'addFields']);

// State
const fields = ref([]);
const drag = ref(false);
const hoveredField = ref(null);
const nextFieldId = ref(1);

/**
 * Create a new field with complete Frappe metadata
 */
const createNewField = (fieldtype = 'Data') => {
  return {
    id: `field_${nextFieldId.value++}`,
    idx: fields.value.length + 1,
    fieldname: '',
    fieldtype: fieldtype,
    label: '',
    description: '',
    options: '',

    // Validation
    reqd: 0,
    unique: 0,
    read_only: 0,
    hidden: 0,

    // Defaults
    default: '',

    // Conditional Logic
    depends_on: '',
    mandatory_depends_on: '',
    read_only_depends_on: '',

    // Formatting
    bold: 0,
    placeholder: '',

    // Layout
    collapsible: 0,
    collapsible_depends_on: '',

    // Numeric Fields
    precision: '',
    length: 0,
    non_negative: 0,

    // List/Grid
    in_list_view: 0,
    in_standard_filter: 0,
    in_global_search: 0,
    allow_bulk_edit: 0,
    columns: 0,

    // Permissions
    permlevel: 0,
    allow_on_submit: 0,
    ignore_user_permissions: 0,
    ignore_xss_filter: 0,

    // Other
    translatable: 0,
    fetch_from: '',
    fetch_if_empty: 0,
    report_hide: 0,
    print_hide: 0,
    print_hide_if_no_value: 0,
    sort_options: 0,
    remember_last_selected_value: 0,
    is_virtual: 0,
    search_index: 0,
    documentation_url: '',

    // Custom Validation
    validation_regex: '',
    validation_message: '',

    // Custom Formatting
    text_transform: '',
    auto_trim: '',

    // UI State
    showAdvanced: false,
    advancedTab: 'config'
  };
};

/**
 * Add a new field
 */
const addField = (type = 'field') => {
  let fieldtype = 'Data';

  if (type === 'section_break') fieldtype = 'Section Break';
  else if (type === 'column_break') fieldtype = 'Column Break';
  else if (type === 'html') fieldtype = 'HTML';

  const newField = createNewField(fieldtype);
  fields.value.push(newField);
  reindexFields();
  emit('update', fields.value);
};

/**
 * Delete a field
 */
const deleteField = (index) => {
  const fieldName = fields.value[index].label || fields.value[index].fieldtype;

  if (confirm(`Delete "${fieldName}"?`)) {
    fields.value.splice(index, 1);
    reindexFields();
    emit('update', fields.value);
  }
};

/**
 * Duplicate a field
 */
const duplicateField = (index) => {
  const fieldToDuplicate = { ...fields.value[index] };

  fieldToDuplicate.id = `field_${nextFieldId.value++}`;
  fieldToDuplicate.fieldname = `${fieldToDuplicate.fieldname}_copy`;
  fieldToDuplicate.label = `${fieldToDuplicate.label} (Copy)`;

  fields.value.splice(index + 1, 0, fieldToDuplicate);
  reindexFields();
  emit('update', fields.value);
};

/**
 * Clear all fields
 */
const clearAll = () => {
  if (confirm('Clear all fields?')) {
    fields.value = [];
    emit('update', []);
  }
};

/**
 * Re-index all fields after drag/drop or add/remove
 */
const reindexFields = () => {
  fields.value.forEach((field, index) => {
    field.idx = index + 1;
  });
};

/**
 * Handle drag end - reindex all fields
 */
const onDragEnd = () => {
  drag.value = false;
  reindexFields();
  emit('update', fields.value);
};

/**
 * Generate fieldname from label
 */
const generateFieldname = (index) => {
  const field = fields.value[index];
  if (!field.label || isLayoutField(field.fieldtype)) return;

  field.fieldname = field.label
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '_')
    .replace(/^_+|_+$/g, '');

  emit('update', fields.value);
};

/**
 * Handle field type change
 */
const onFieldTypeChange = (index) => {
  const field = fields.value[index];

  if (!requiresOptions(field.fieldtype)) {
    field.options = '';
  }

  if (isLayoutField(field.fieldtype)) {
    field.fieldname = '';
  }

  emit('update', fields.value);
};

/**
 * Toggle advanced options panel
 */
const toggleAdvanced = (index) => {
  fields.value[index].showAdvanced = !fields.value[index].showAdvanced;
};

/**
 * Check if field type requires options
 */
const requiresOptions = (fieldtype) => {
  return ['Select', 'Link', 'Table', 'Table MultiSelect', 'Small Text', 'Autocomplete'].includes(fieldtype);
};

/**
 * Check if field is a layout field (Section Break, Column Break, HTML)
 */
const isLayoutField = (fieldtype) => {
  return ['Section Break', 'Column Break', 'HTML'].includes(fieldtype);
};

/**
 * Check if field is numeric
 */
const isNumericField = (fieldtype) => {
  return ['Int', 'Float', 'Currency', 'Percent'].includes(fieldtype);
};

/**
 * Get options placeholder
 */
const getOptionsPlaceholder = (fieldtype) => {
  if (fieldtype === 'Select' || fieldtype === 'Small Text' || fieldtype === 'Autocomplete') {
    return 'Option 1\nOption 2\nOption 3';
  } else if (fieldtype === 'Link') {
    return 'DocType Name (e.g., Customer)';
  } else if (fieldtype === 'Table' || fieldtype === 'Table MultiSelect') {
    return 'Child DocType Name';
  }
  return 'Enter options';
};

/**
 * Get field placeholder based on type
 */
const getFieldPlaceholder = (fieldtype) => {
  if (fieldtype === 'Section Break') return 'Section Label';
  if (fieldtype === 'Column Break') return 'Column Label (optional)';
  if (fieldtype === 'HTML') return 'HTML Field Label';
  return 'Field Label';
};

/**
 * Get field type icon
 */
const getFieldTypeIcon = (fieldtype) => {
  const icons = {
    'Data': 'bi bi-fonts',
    'Small Text': 'bi bi-textarea-t',
    'Text': 'bi bi-textarea',
    'Long Text': 'bi bi-file-text',
    'Text Editor': 'bi bi-file-richtext',
    'Int': 'bi bi-hash',
    'Float': 'bi bi-123',
    'Currency': 'bi bi-currency-dollar',
    'Percent': 'bi bi-percent',
    'Date': 'bi bi-calendar-date',
    'Datetime': 'bi bi-calendar-event',
    'Time': 'bi bi-clock',
    'Link': 'bi bi-link-45deg',
    'Dynamic Link': 'bi bi-diagram-3',
    'Table': 'bi bi-table',
    'Select': 'bi bi-list-ul',
    'Autocomplete': 'bi bi-search',
    'Check': 'bi bi-check-square',
    'Attach': 'bi bi-paperclip',
    'Attach Image': 'bi bi-image',
    'Section Break': 'bi bi-layout-split',
    'Column Break': 'bi bi-layout-three-columns',
    'HTML': 'bi bi-code-square',
    'Button': 'bi bi-mouse',
    'Rating': 'bi bi-star',
    'Signature': 'bi bi-pen',
    'Color': 'bi bi-palette',
    'Barcode': 'bi bi-upc',
  };
  return icons[fieldtype] || 'bi bi-question-circle';
};

/**
 * Validate fieldname
 */
const isValidFieldname = (fieldname) => {
  return /^[a-z_][a-z0-9_]*$/.test(fieldname);
};

/**
 * Build sections structure from flat fields list
 */
const buildSectionsStructure = () => {
  const sections = [];
  let currentSection = null;
  let currentRow = null;
  let currentColumn = null;

  fields.value.forEach((field, index) => {
    if (field.fieldtype === 'Section Break') {
      // Start new section
      currentSection = {
        label: field.label || '',
        collapsible: field.collapsible,
        collapsible_depends_on: field.collapsible_depends_on,
        depends_on: field.depends_on,
        rows: []
      };
      currentRow = { columns: [] };
      currentColumn = { fields: [] };
      currentRow.columns.push(currentColumn);
      currentSection.rows.push(currentRow);
      sections.push(currentSection);
    } else if (field.fieldtype === 'Column Break') {
      // Start new column in current row
      if (currentRow) {
        currentColumn = { fields: [] };
        currentRow.columns.push(currentColumn);
      }
    } else if (field.fieldtype !== 'HTML') {
      // Regular field - add to current column
      if (!currentSection) {
        // No section break yet, create default section
        currentSection = {
          label: '',
          rows: []
        };
        currentRow = { columns: [] };
        currentColumn = { fields: [] };
        currentRow.columns.push(currentColumn);
        currentSection.rows.push(currentRow);
        sections.push(currentSection);
      }

      if (!currentColumn) {
        currentColumn = { fields: [] };
        currentRow.columns.push(currentColumn);
      }

      currentColumn.fields.push(field);
    }
  });

  return sections;
};

/**
 * Add fields to current block
 */
const addFieldsToBlock = () => {
  // Validate all fields
  for (const field of fields.value) {
    if (isLayoutField(field.fieldtype)) continue;

    if (!field.label || !field.fieldname || !field.fieldtype) {
      showError('All fields must have a label, fieldname, and type');
      return;
    }

    if (!isValidFieldname(field.fieldname)) {
      showError(`Invalid fieldname: ${field.fieldname}. Use lowercase letters, numbers, and underscores only.`);
      return;
    }

    if (requiresOptions(field.fieldtype) && (!field.options || !field.options.trim())) {
      showError(`Options required for ${field.fieldtype} field: ${field.label}`);
      return;
    }
  }

  // Build sections structure from flat fields list
  const sectionsStructure = buildSectionsStructure();

  emit('addFields', sectionsStructure);
  showSuccess(`${fields.value.length} field(s) added to form!`);

  // Clear fields after adding
  fields.value = [];
};

// Expose methods
defineExpose({
  fields,
  addFieldsToBlock,
  addField
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
  border-bottom: 2px solid #dee2e6;
  flex-shrink: 0;
}

.vr {
  display: inline-block;
  width: 1px;
  min-height: 1.5rem;
  background-color: currentColor;
  opacity: 0.25;
}

.fields-container {
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

.field-item {
  position: relative;
  background: #fff;
  border: 2px solid #dee2e6;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 15px;
  transition: all 0.2s ease;
}

.field-item:hover {
  border-color: #007bff;
  box-shadow: 0 4px 12px rgba(0,123,255,0.15);
}

.field-item.dragging {
  opacity: 0.5;
}

.field-item.field-section-break {
  border-left: 4px solid #28a745;
  background: #f8fff9;
}

.field-item.field-column-break {
  border-left: 4px solid #ffc107;
  background: #fffef8;
}

.field-item.field-html {
  border-left: 4px solid #6f42c1;
  background: #f9f8ff;
}

.field-index-badge {
  position: absolute;
  top: 8px;
  right: 8px;
  background: #007bff;
  color: white;
  font-size: 11px;
  font-weight: bold;
  padding: 3px 8px;
  border-radius: 12px;
  z-index: 10;
}

.field-type-indicator {
  position: absolute;
  top: 8px;
  left: 8px;
  color: #6c757d;
  font-size: 18px;
  z-index: 10;
}

.field-content {
  display: flex;
  gap: 12px;
  margin-top: 25px;
}

.field-drag-handle {
  color: #6c757d;
  cursor: move;
  padding-top: 8px;
  flex-shrink: 0;
  font-size: 20px;
}

.field-drag-handle:hover {
  color: #007bff;
}

.field-editor {
  flex: 1;
}

.quick-options {
  padding: 10px;
  background: #f8f9fa;
  border-radius: 6px;
}

.advanced-panel {
  margin-top: 15px;
  padding: 15px;
  background: #f8f9fa;
  border-radius: 6px;
  border: 1px solid #dee2e6;
}

.nav-tabs-sm .nav-link {
  padding: 0.4rem 0.8rem;
  font-size: 13px;
}

.tab-content {
  padding-top: 10px;
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

.font-monospace {
  font-family: 'Courier New', monospace;
}

.dropdown-menu {
  font-size: 13px;
}

.dropdown-item {
  padding: 0.4rem 1rem;
}
</style>
