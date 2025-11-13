<template>
  <div class="field-configurator">
    <div class="row g-3">
      <!-- Basic Information -->
      <div class="col-md-12">
        <h6 class="section-title">Basic Information</h6>
      </div>

      <!-- Field Type -->
      <div class="col-md-6">
        <label class="form-label">Field Type <span class="text-danger">*</span></label>
        <select v-model="localField.fieldtype" @change="onFieldTypeChange" class="form-select">
          <option v-for="type in fieldTypes" :key="type" :value="type">
            {{ type }}
          </option>
        </select>
      </div>

      <!-- Label -->
      <div class="col-md-6">
        <label class="form-label">Label <span class="text-danger">*</span></label>
        <input
          v-model="localField.label"
          @input="generateFieldname"
          type="text"
          class="form-control"
          placeholder="Enter field label"
        />
      </div>

      <!-- Fieldname -->
      <div class="col-md-6">
        <label class="form-label">Fieldname <span class="text-danger">*</span></label>
        <input
          v-model="localField.fieldname"
          type="text"
          class="form-control"
          placeholder="field_name"
          pattern="[a-z_][a-z0-9_]*"
        />
        <small class="text-muted">Use lowercase with underscores (e.g., customer_name)</small>
      </div>

      <!-- Description -->
      <div class="col-md-6">
        <label class="form-label">Description</label>
        <textarea
          v-model="localField.description"
          class="form-control"
          rows="2"
          placeholder="Field description"
        ></textarea>
      </div>

      <!-- Options (for Select, Link, etc.) -->
      <div v-if="requiresOptions" class="col-md-12">
        <label class="form-label">Options <span class="text-danger">*</span></label>
        <textarea
          v-model="localField.options"
          class="form-control"
          rows="3"
          :placeholder="getOptionsPlaceholder()"
        ></textarea>
        <small class="text-muted">{{ getOptionsHint() }}</small>
      </div>

      <!-- Default Value -->
      <div class="col-md-6">
        <label class="form-label">Default Value</label>
        <input
          v-model="localField.default"
          type="text"
          class="form-control"
          placeholder="Default value"
        />
      </div>

      <!-- Length (for Data, Small Text, etc.) -->
      <div v-if="supportsLength" class="col-md-6">
        <label class="form-label">Length</label>
        <input
          v-model.number="localField.length"
          type="number"
          class="form-control"
          placeholder="e.g., 140"
        />
      </div>

      <!-- Precision (for Float, Currency) -->
      <div v-if="supportsPrecision" class="col-md-6">
        <label class="form-label">Precision</label>
        <input
          v-model.number="localField.precision"
          type="number"
          class="form-control"
          placeholder="e.g., 2"
          min="0"
          max="9"
        />
      </div>

      <!-- Validations Section -->
      <div class="col-md-12 mt-4">
        <h6 class="section-title">Validations & Properties</h6>
      </div>

      <!-- Checkboxes for boolean fields -->
      <div class="col-md-4">
        <div class="form-check">
          <input
            v-model="localField.reqd"
            type="checkbox"
            class="form-check-input"
            :true-value="1"
            :false-value="0"
            id="reqd"
          />
          <label class="form-check-label" for="reqd">Mandatory</label>
        </div>
      </div>

      <div class="col-md-4">
        <div class="form-check">
          <input
            v-model="localField.read_only"
            type="checkbox"
            class="form-check-input"
            :true-value="1"
            :false-value="0"
            id="read_only"
          />
          <label class="form-check-label" for="read_only">Read Only</label>
        </div>
      </div>

      <div class="col-md-4">
        <div class="form-check">
          <input
            v-model="localField.hidden"
            type="checkbox"
            class="form-check-input"
            :true-value="1"
            :false-value="0"
            id="hidden"
          />
          <label class="form-check-label" for="hidden">Hidden</label>
        </div>
      </div>

      <div class="col-md-4">
        <div class="form-check">
          <input
            v-model="localField.unique"
            type="checkbox"
            class="form-check-input"
            :true-value="1"
            :false-value="0"
            id="unique"
          />
          <label class="form-check-label" for="unique">Unique</label>
        </div>
      </div>

      <div class="col-md-4">
        <div class="form-check">
          <input
            v-model="localField.in_list_view"
            type="checkbox"
            class="form-check-input"
            :true-value="1"
            :false-value="0"
            id="in_list_view"
          />
          <label class="form-check-label" for="in_list_view">In List View</label>
        </div>
      </div>

      <div class="col-md-4">
        <div class="form-check">
          <input
            v-model="localField.in_standard_filter"
            type="checkbox"
            class="form-check-input"
            :true-value="1"
            :false-value="0"
            id="in_standard_filter"
          />
          <label class="form-check-label" for="in_standard_filter">In Standard Filter</label>
        </div>
      </div>

      <div class="col-md-4">
        <div class="form-check">
          <input
            v-model="localField.in_global_search"
            type="checkbox"
            class="form-check-input"
            :true-value="1"
            :false-value="0"
            id="in_global_search"
          />
          <label class="form-check-label" for="in_global_search">In Global Search</label>
        </div>
      </div>

      <div class="col-md-4">
        <div class="form-check">
          <input
            v-model="localField.bold"
            type="checkbox"
            class="form-check-input"
            :true-value="1"
            :false-value="0"
            id="bold"
          />
          <label class="form-check-label" for="bold">Bold</label>
        </div>
      </div>

      <div class="col-md-4">
        <div class="form-check">
          <input
            v-model="localField.allow_on_submit"
            type="checkbox"
            class="form-check-input"
            :true-value="1"
            :false-value="0"
            id="allow_on_submit"
          />
          <label class="form-check-label" for="allow_on_submit">Allow on Submit</label>
        </div>
      </div>

      <div v-if="supportsNonNegative" class="col-md-4">
        <div class="form-check">
          <input
            v-model="localField.non_negative"
            type="checkbox"
            class="form-check-input"
            :true-value="1"
            :false-value="0"
            id="non_negative"
          />
          <label class="form-check-label" for="non_negative">Non Negative</label>
        </div>
      </div>

      <div class="col-md-4">
        <div class="form-check">
          <input
            v-model="localField.translatable"
            type="checkbox"
            class="form-check-input"
            :true-value="1"
            :false-value="0"
            id="translatable"
          />
          <label class="form-check-label" for="translatable">Translatable</label>
        </div>
      </div>

      <div class="col-md-4">
        <div class="form-check">
          <input
            v-model="localField.search_index"
            type="checkbox"
            class="form-check-input"
            :true-value="1"
            :false-value="0"
            id="search_index"
          />
          <label class="form-check-label" for="search_index">Search Index</label>
        </div>
      </div>

      <!-- Conditional Display Section -->
      <div class="col-md-12 mt-4">
        <h6 class="section-title">Conditional Display</h6>
      </div>

      <!-- Depends On -->
      <div class="col-md-12">
        <label class="form-label">Depends On</label>
        <input
          v-model="localField.depends_on"
          type="text"
          class="form-control"
          placeholder="eval:doc.field_name=='value'"
        />
        <small class="text-muted">
          e.g., eval:doc.status=='Active' or doc.is_enabled==1
        </small>
      </div>

      <!-- Mandatory Depends On -->
      <div class="col-md-6">
        <label class="form-label">Mandatory Depends On</label>
        <input
          v-model="localField.mandatory_depends_on"
          type="text"
          class="form-control"
          placeholder="eval:doc.field_name=='value'"
        />
      </div>

      <!-- Read Only Depends On -->
      <div class="col-md-6">
        <label class="form-label">Read Only Depends On</label>
        <input
          v-model="localField.read_only_depends_on"
          type="text"
          class="form-control"
          placeholder="eval:doc.field_name=='value'"
        />
      </div>

      <!-- Advanced Options -->
      <div class="col-md-12 mt-4">
        <details>
          <summary class="section-title" style="cursor: pointer;">
            Advanced Options
          </summary>
          <div class="row g-3 mt-2">
            <!-- Fetch From -->
            <div class="col-md-6">
              <label class="form-label">Fetch From</label>
              <input
                v-model="localField.fetch_from"
                type="text"
                class="form-control"
                placeholder="link_field.source_field"
              />
            </div>

            <!-- Fetch If Empty -->
            <div class="col-md-6">
              <div class="form-check mt-4">
                <input
                  v-model="localField.fetch_if_empty"
                  type="checkbox"
                  class="form-check-input"
                  :true-value="1"
                  :false-value="0"
                  id="fetch_if_empty"
                />
                <label class="form-check-label" for="fetch_if_empty">Fetch If Empty</label>
              </div>
            </div>

            <!-- Permlevel -->
            <div class="col-md-6">
              <label class="form-label">Permission Level</label>
              <input
                v-model.number="localField.permlevel"
                type="number"
                class="form-control"
                min="0"
                max="9"
              />
            </div>

            <!-- Columns (width in list view) -->
            <div class="col-md-6">
              <label class="form-label">Columns (Width)</label>
              <input
                v-model.number="localField.columns"
                type="number"
                class="form-control"
                min="0"
                max="12"
              />
            </div>

            <!-- Print Options -->
            <div class="col-md-4">
              <div class="form-check">
                <input
                  v-model="localField.print_hide"
                  type="checkbox"
                  class="form-check-input"
                  :true-value="1"
                  :false-value="0"
                  id="print_hide"
                />
                <label class="form-check-label" for="print_hide">Hide in Print</label>
              </div>
            </div>

            <div class="col-md-4">
              <div class="form-check">
                <input
                  v-model="localField.print_hide_if_no_value"
                  type="checkbox"
                  class="form-check-input"
                  :true-value="1"
                  :false-value="0"
                  id="print_hide_if_no_value"
                />
                <label class="form-check-label" for="print_hide_if_no_value">
                  Hide if No Value
                </label>
              </div>
            </div>

            <div class="col-md-4">
              <div class="form-check">
                <input
                  v-model="localField.report_hide"
                  type="checkbox"
                  class="form-check-input"
                  :true-value="1"
                  :false-value="0"
                  id="report_hide"
                />
                <label class="form-check-label" for="report_hide">Hide in Report</label>
              </div>
            </div>

            <!-- More advanced options -->
            <div class="col-md-4">
              <div class="form-check">
                <input
                  v-model="localField.allow_bulk_edit"
                  type="checkbox"
                  class="form-check-input"
                  :true-value="1"
                  :false-value="0"
                  id="allow_bulk_edit"
                />
                <label class="form-check-label" for="allow_bulk_edit">Allow Bulk Edit</label>
              </div>
            </div>

            <div class="col-md-4">
              <div class="form-check">
                <input
                  v-model="localField.allow_in_quick_entry"
                  type="checkbox"
                  class="form-check-input"
                  :true-value="1"
                  :false-value="0"
                  id="allow_in_quick_entry"
                />
                <label class="form-check-label" for="allow_in_quick_entry">
                  Allow in Quick Entry
                </label>
              </div>
            </div>

            <div class="col-md-4">
              <div class="form-check">
                <input
                  v-model="localField.remember_last_selected_value"
                  type="checkbox"
                  class="form-check-input"
                  :true-value="1"
                  :false-value="0"
                  id="remember_last_selected_value"
                />
                <label class="form-check-label" for="remember_last_selected_value">
                  Remember Last Value
                </label>
              </div>
            </div>

            <!-- Documentation URL -->
            <div class="col-md-12">
              <label class="form-label">Documentation URL</label>
              <input
                v-model="localField.documentation_url"
                type="url"
                class="form-control"
                placeholder="https://docs.example.com/field-help"
              />
            </div>
          </div>
        </details>
      </div>

      <!-- Action Buttons -->
      <div class="col-md-12 mt-4">
        <div class="d-flex gap-2 justify-content-end">
          <button @click="$emit('cancel')" class="btn btn-secondary">
            Cancel
          </button>
          <button @click="save" class="btn btn-primary">
            <i class="bi bi-check-circle"></i> Save Field
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
  field: {
    type: Object,
    required: true
  },
  fieldTypes: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits(['update', 'cancel', 'save']);

const localField = ref({ ...props.field });

// Watch for prop changes
watch(() => props.field, (newVal) => {
  localField.value = { ...newVal };
}, { deep: true });

// Computed properties for conditional display
const requiresOptions = computed(() => {
  return ['Select', 'Link', 'Table', 'Table MultiSelect', 'Dynamic Link'].includes(
    localField.value.fieldtype
  );
});

const supportsLength = computed(() => {
  return ['Data', 'Small Text', 'Password', 'Barcode'].includes(
    localField.value.fieldtype
  );
});

const supportsPrecision = computed(() => {
  return ['Float', 'Currency', 'Percent'].includes(localField.value.fieldtype);
});

const supportsNonNegative = computed(() => {
  return ['Int', 'Float', 'Currency'].includes(localField.value.fieldtype);
});

/**
 * Auto-generate fieldname from label
 */
const generateFieldname = () => {
  if (!localField.value.label) return;

  // Only auto-generate if fieldname is empty or still default
  if (!localField.value.fieldname || localField.value.fieldname.startsWith('field_')) {
    localField.value.fieldname = localField.value.label
      .toLowerCase()
      .replace(/[^a-z0-9]+/g, '_')
      .replace(/^_+|_+$/g, '');
  }
};

/**
 * Handle field type change
 */
const onFieldTypeChange = () => {
  // Reset type-specific options
  if (!requiresOptions.value) {
    localField.value.options = '';
  }
  if (!supportsPrecision.value) {
    localField.value.precision = '';
  }
  if (!supportsLength.value) {
    localField.value.length = 0;
  }

  emit('update', localField.value);
};

/**
 * Get placeholder text for options field
 */
const getOptionsPlaceholder = () => {
  const type = localField.value.fieldtype;
  if (type === 'Select') {
    return 'Option 1\nOption 2\nOption 3';
  } else if (type === 'Link') {
    return 'DocType Name (e.g., Customer)';
  } else if (type === 'Table') {
    return 'Child DocType Name';
  }
  return 'Enter options';
};

/**
 * Get hint text for options field
 */
const getOptionsHint = () => {
  const type = localField.value.fieldtype;
  if (type === 'Select') {
    return 'Enter each option on a new line';
  } else if (type === 'Link') {
    return 'Enter the DocType to link to';
  } else if (type === 'Table') {
    return 'Enter the Child DocType name';
  }
  return '';
};

/**
 * Save field configuration
 */
const save = () => {
  // Validate required fields
  if (!localField.value.fieldname || !localField.value.label) {
    alert('Fieldname and Label are required');
    return;
  }

  // Validate fieldname format
  const fieldnameRegex = /^[a-z_][a-z0-9_]*$/;
  if (!fieldnameRegex.test(localField.value.fieldname)) {
    alert('Fieldname must start with a letter or underscore and contain only lowercase letters, numbers, and underscores');
    return;
  }

  // Validate options for fields that require them
  if (requiresOptions.value && !localField.value.options) {
    alert(`Options are required for ${localField.value.fieldtype} fields`);
    return;
  }

  emit('update', localField.value);
  emit('save');
};

// Emit updates on any change
watch(localField, (newVal) => {
  emit('update', newVal);
}, { deep: true });
</script>

<style scoped>
.field-configurator {
  background: white;
  padding: 20px;
  border-radius: 8px;
}

.section-title {
  color: #495057;
  font-weight: 600;
  margin-bottom: 15px;
  padding-bottom: 8px;
  border-bottom: 2px solid #e9ecef;
}

.form-label {
  font-weight: 500;
  color: #495057;
  margin-bottom: 8px;
}

.form-control, .form-select {
  border-radius: 6px;
  border: 1px solid #ced4da;
  padding: 8px 12px;
  font-size: 14px;
}

.form-control:focus, .form-select:focus {
  border-color: #007bff;
  box-shadow: 0 0 0 0.2rem rgba(0,123,255,.25);
}

.form-check {
  padding: 8px 0;
}

.form-check-label {
  font-size: 14px;
  color: #495057;
}

.text-danger {
  color: #dc3545;
}

.text-muted {
  font-size: 12px;
  color: #6c757d;
  display: block;
  margin-top: 4px;
}

details summary {
  font-weight: 600;
  padding: 10px;
  background: #f8f9fa;
  border-radius: 4px;
  margin-bottom: 10px;
}

details[open] summary {
  margin-bottom: 15px;
}
</style>
