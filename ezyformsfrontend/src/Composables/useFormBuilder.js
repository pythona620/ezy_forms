/**
 * useFormBuilder Composable
 *
 * Central state management for the form builder.
 * Handles form data, field management, sections, and workflow.
 */

import { ref, computed, watch } from 'vue';
import { nanoid } from 'nanoid';

export function useFormBuilder(initialData = null) {
  // ============================================
  // STATE
  // ============================================

  const formData = ref({
    // Form Metadata
    formId: initialData?.formId || null,
    formName: initialData?.formName || '',
    formShortCode: initialData?.formShortCode || '',
    formCategory: initialData?.formCategory || '',
    formDescription: initialData?.formDescription || '',
    ownerOfTheForm: initialData?.ownerOfTheForm || '',
    accessibleDepartments: initialData?.accessibleDepartments || [],
    formType: initialData?.formType || 'internal', // internal, public
    hasWorkflow: initialData?.hasWorkflow || 'No',
    series: initialData?.series || '',
    publicFormResponse: initialData?.publicFormResponse || '',
    mailId: initialData?.mailId || '',

    // Form Structure
    sections: initialData?.sections || [],
    fields: initialData?.fields || [],

    // Workflow Configuration
    workflow: initialData?.workflow || [],

    // Settings
    settings: initialData?.settings || {
      showProgressBar: true,
      allowSaveDraft: true,
      submitButtonText: 'Submit',
      successMessage: 'Form submitted successfully!'
    }
  });

  // Selection State
  const selectedFieldId = ref(null);
  const selectedSectionId = ref(null);
  const selectedBlockIndex = ref(null);

  // UI State
  const isDirty = ref(false);
  const isPreviewMode = ref(false);

  // ============================================
  // COMPUTED
  // ============================================

  const selectedField = computed(() => {
    if (!selectedFieldId.value) return null;
    return findFieldById(selectedFieldId.value);
  });

  const selectedSection = computed(() => {
    if (!selectedSectionId.value) return null;
    return formData.value.sections.find(s => s.id === selectedSectionId.value);
  });

  const totalFields = computed(() => formData.value.fields.length);

  const hasUnsavedChanges = computed(() => isDirty.value);

  // Validation
  const isFormValid = computed(() => {
    return (
      formData.value.formName &&
      formData.value.formShortCode &&
      formData.value.formCategory &&
      formData.value.ownerOfTheForm &&
      formData.value.accessibleDepartments.length > 0 &&
      formData.value.fields.length > 0
    );
  });

  const validationErrors = computed(() => {
    const errors = [];

    if (!formData.value.formName) {
      errors.push({ field: 'formName', message: 'Form name is required' });
    }

    if (!formData.value.formShortCode) {
      errors.push({ field: 'formShortCode', message: 'Form short code is required' });
    }

    if (!formData.value.formCategory) {
      errors.push({ field: 'formCategory', message: 'Form category is required' });
    }

    if (!formData.value.ownerOfTheForm) {
      errors.push({ field: 'ownerOfTheForm', message: 'Owner of the form is required' });
    }

    if (formData.value.accessibleDepartments.length === 0) {
      errors.push({ field: 'accessibleDepartments', message: 'At least one department must be selected' });
    }

    if (formData.value.fields.length === 0) {
      errors.push({ field: 'fields', message: 'At least one field must be added' });
    }

    // Validate individual fields
    formData.value.fields.forEach((field, index) => {
      if (!field.label) {
        errors.push({
          field: `fields[${index}].label`,
          message: `Field ${index + 1}: Label is required`
        });
      }

      if (!field.fieldname) {
        errors.push({
          field: `fields[${index}].fieldname`,
          message: `Field ${index + 1}: Field name is required`
        });
      }
    });

    return errors;
  });

  // ============================================
  // FIELD MANAGEMENT
  // ============================================

  /**
   * Add a new field to the form
   */
  function addField(fieldData, position = null) {
    const newField = {
      id: nanoid(),
      fieldname: fieldData.fieldname || generateFieldName(fieldData.type),
      label: fieldData.label || fieldData.name || 'Untitled Field',
      fieldtype: fieldData.type || 'Data',
      options: fieldData.options || '',
      description: fieldData.description || '',
      placeholder: fieldData.placeholder || '',
      default: fieldData.default || '',
      required: fieldData.required || false,
      readonly: fieldData.readonly || false,
      hidden: fieldData.hidden || false,

      // Validation
      validation: fieldData.validation || {
        required: false,
        minLength: null,
        maxLength: null,
        pattern: null,
        customValidator: null
      },

      // Appearance
      width: fieldData.width || '100%',
      cssClass: fieldData.cssClass || '',
      icon: fieldData.icon || '',

      // Conditional Logic
      conditions: fieldData.conditions || {
        show: [],
        enable: [],
        require: []
      },

      // Advanced
      isCustom: fieldData.isCustom || false,
      permissions: fieldData.permissions || {},

      // Metadata
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString()
    };

    if (position !== null && position >= 0 && position <= formData.value.fields.length) {
      formData.value.fields.splice(position, 0, newField);
    } else {
      formData.value.fields.push(newField);
    }

    isDirty.value = true;
    return newField;
  }

  /**
   * Remove a field by ID
   */
  function removeField(fieldId) {
    const index = formData.value.fields.findIndex(f => f.id === fieldId);
    if (index !== -1) {
      formData.value.fields.splice(index, 1);

      // Clear selection if the removed field was selected
      if (selectedFieldId.value === fieldId) {
        selectedFieldId.value = null;
      }

      isDirty.value = true;
      return true;
    }
    return false;
  }

  /**
   * Update field properties
   */
  function updateField(fieldId, updates) {
    const field = findFieldById(fieldId);
    if (field) {
      Object.assign(field, updates, {
        updatedAt: new Date().toISOString()
      });
      isDirty.value = true;
      return true;
    }
    return false;
  }

  /**
   * Duplicate a field
   */
  function duplicateField(fieldId) {
    const field = findFieldById(fieldId);
    if (field) {
      const index = formData.value.fields.findIndex(f => f.id === fieldId);
      const duplicatedField = {
        ...JSON.parse(JSON.stringify(field)),
        id: nanoid(),
        fieldname: `${field.fieldname}_copy`,
        label: `${field.label} (Copy)`,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString()
      };

      formData.value.fields.splice(index + 1, 0, duplicatedField);
      isDirty.value = true;
      return duplicatedField;
    }
    return null;
  }

  /**
   * Reorder fields (drag and drop)
   */
  function reorderFields(fromIndex, toIndex) {
    if (
      fromIndex < 0 ||
      fromIndex >= formData.value.fields.length ||
      toIndex < 0 ||
      toIndex >= formData.value.fields.length
    ) {
      return false;
    }

    const field = formData.value.fields.splice(fromIndex, 1)[0];
    formData.value.fields.splice(toIndex, 0, field);
    isDirty.value = true;
    return true;
  }

  /**
   * Find field by ID
   */
  function findFieldById(fieldId) {
    return formData.value.fields.find(f => f.id === fieldId);
  }

  /**
   * Get field index
   */
  function getFieldIndex(fieldId) {
    return formData.value.fields.findIndex(f => f.id === fieldId);
  }

  /**
   * Generate unique field name
   */
  function generateFieldName(fieldType) {
    const baseName = fieldType.toLowerCase().replace(/\s+/g, '_');
    const existingFields = formData.value.fields.filter(f =>
      f.fieldname.startsWith(baseName)
    );
    return existingFields.length > 0
      ? `${baseName}_${existingFields.length + 1}`
      : baseName;
  }

  // ============================================
  // SECTION MANAGEMENT
  // ============================================

  /**
   * Add a new section
   */
  function addSection(sectionData) {
    const newSection = {
      id: nanoid(),
      label: sectionData.label || 'Untitled Section',
      description: sectionData.description || '',
      collapsible: sectionData.collapsible || false,
      collapsed: sectionData.collapsed || false,
      fields: sectionData.fields || [],
      createdAt: new Date().toISOString()
    };

    formData.value.sections.push(newSection);
    isDirty.value = true;
    return newSection;
  }

  /**
   * Remove a section
   */
  function removeSection(sectionId) {
    const index = formData.value.sections.findIndex(s => s.id === sectionId);
    if (index !== -1) {
      formData.value.sections.splice(index, 1);
      isDirty.value = true;
      return true;
    }
    return false;
  }

  /**
   * Update section
   */
  function updateSection(sectionId, updates) {
    const section = formData.value.sections.find(s => s.id === sectionId);
    if (section) {
      Object.assign(section, updates);
      isDirty.value = true;
      return true;
    }
    return false;
  }

  // ============================================
  // SELECTION
  // ============================================

  function selectField(fieldId) {
    selectedFieldId.value = fieldId;
    selectedSectionId.value = null;
  }

  function selectSection(sectionId) {
    selectedSectionId.value = sectionId;
    selectedFieldId.value = null;
  }

  function clearSelection() {
    selectedFieldId.value = null;
    selectedSectionId.value = null;
  }

  // ============================================
  // FORM OPERATIONS
  // ============================================

  /**
   * Reset form to initial state
   */
  function resetForm() {
    formData.value = {
      formId: null,
      formName: '',
      formShortCode: '',
      formCategory: '',
      formDescription: '',
      ownerOfTheForm: '',
      accessibleDepartments: [],
      formType: 'internal',
      hasWorkflow: 'No',
      series: '',
      publicFormResponse: '',
      mailId: '',
      sections: [],
      fields: [],
      workflow: [],
      settings: {
        showProgressBar: true,
        allowSaveDraft: true,
        submitButtonText: 'Submit',
        successMessage: 'Form submitted successfully!'
      }
    };

    clearSelection();
    isDirty.value = false;
  }

  /**
   * Load form data
   */
  function loadFormData(data) {
    formData.value = { ...formData.value, ...data };
    isDirty.value = false;
  }

  /**
   * Export form data
   */
  function exportFormData() {
    return JSON.parse(JSON.stringify(formData.value));
  }

  /**
   * Toggle preview mode
   */
  function togglePreviewMode() {
    isPreviewMode.value = !isPreviewMode.value;
  }

  // ============================================
  // WATCH FOR CHANGES
  // ============================================

  watch(
    () => formData.value,
    () => {
      isDirty.value = true;
    },
    { deep: true }
  );

  // ============================================
  // RETURN API
  // ============================================

  return {
    // State
    formData,
    selectedFieldId,
    selectedField,
    selectedSectionId,
    selectedSection,
    selectedBlockIndex,
    isDirty,
    isPreviewMode,

    // Computed
    totalFields,
    hasUnsavedChanges,
    isFormValid,
    validationErrors,

    // Field Methods
    addField,
    removeField,
    updateField,
    duplicateField,
    reorderFields,
    findFieldById,
    getFieldIndex,

    // Section Methods
    addSection,
    removeSection,
    updateSection,

    // Selection Methods
    selectField,
    selectSection,
    clearSelection,

    // Form Operations
    resetForm,
    loadFormData,
    exportFormData,
    togglePreviewMode
  };
}

// Note: nanoid needs to be installed
// Run: npm install nanoid
