# EzyForms UI/UX Redesign - Usage Examples

## 📚 Complete Component Usage Guide

This document provides real-world examples of how to use all the components and composables created for the EzyForms form builder redesign.

---

## 🎨 Design System Usage

### Importing Design Tokens

```scss
// In any Vue component
<style scoped lang="scss">
@import '@/Styles/design-tokens.scss';

.my-component {
  /* Colors */
  background: var(--color-primary-600);
  color: var(--color-text-inverse);

  /* Spacing */
  padding: var(--space-4);
  margin-bottom: var(--space-6);

  /* Typography */
  font-size: var(--font-size-base);
  font-weight: var(--font-weight-medium);

  /* Borders */
  border-radius: var(--border-radius-lg);

  /* Shadows */
  box-shadow: var(--shadow-md);

  /* Transitions */
  transition: var(--transition-normal);

  &:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-2px);
  }
}
</style>
```

---

## 🧩 UI Components

### Example 1: Complete Form Builder Page

```vue
<template>
  <div class="form-builder-page">
    <!-- Toolbar -->
    <div class="toolbar">
      <!-- Undo/Redo -->
      <div class="toolbar-group">
        <IconButton
          icon="bi bi-arrow-counterclockwise"
          :disabled="!canUndo"
          aria-label="Undo"
          tooltip="Undo (Ctrl+Z)"
          @click="handleUndo"
        />
        <IconButton
          icon="bi bi-arrow-clockwise"
          :disabled="!canRedo"
          aria-label="Redo"
          tooltip="Redo (Ctrl+Y)"
          @click="handleRedo"
        />
      </div>

      <!-- Auto-save status -->
      <div class="auto-save-status">
        <i :class="saveStatusIcon" class="status-icon"></i>
        <span>{{ saveStatusText }}</span>
      </div>

      <!-- Actions -->
      <div class="toolbar-actions">
        <SecondaryButton
          variant="outline"
          size="md"
          @click="handlePreview"
        >
          <i class="bi bi-eye me-2"></i>
          Preview
        </SecondaryButton>

        <PrimaryButton
          size="md"
          :loading="isSaving"
          @click="handleSave"
        >
          <i class="bi bi-save me-2"></i>
          {{ formData.formId ? 'Update Form' : 'Create Form' }}
        </PrimaryButton>
      </div>
    </div>

    <!-- Main Content -->
    <div class="form-builder-content">
      <!-- Field Library (Left Panel) -->
      <FieldLibraryPanel
        :collapsible="true"
        @field-add="handleFieldAdd"
        @field-dragstart="handleFieldDragStart"
      />

      <!-- Form Canvas (Center) -->
      <div class="form-canvas-wrapper">
        <Card
          title="Form Builder"
          variant="elevated"
          :padded="true"
        >
          <template #actions>
            <IconButton
              icon="bi bi-gear"
              variant="ghost"
              aria-label="Form settings"
              @click="openFormSettings"
            />
          </template>

          <!-- Form metadata -->
          <div class="form-metadata">
            <TextInput
              v-model="formData.formName"
              label="Form Name"
              placeholder="Enter form name"
              :required="true"
              :error-message="validationErrors.formName"
            />

            <TextInput
              v-model="formData.formShortCode"
              label="Form Short Code"
              placeholder="e.g., FORM-001"
              :required="true"
              help-text="Unique identifier for this form"
            />
          </div>

          <!-- Drop zone (when no fields) -->
          <DropZone
            v-if="formData.fields.length === 0"
            text="Drop your first field here"
            help-text="Drag a field from the library or click a field to add it"
            @drop="handleFieldDrop"
          />

          <!-- Field list -->
          <div v-else class="field-list">
            <div
              v-for="(field, index) in formData.fields"
              :key="field.id"
              class="field-item"
              :class="{ 'field-item--selected': selectedFieldId === field.id }"
              @click="selectField(field.id)"
            >
              <div class="field-item-header">
                <IconButton
                  icon="bi bi-grip-vertical"
                  variant="ghost"
                  size="sm"
                  aria-label="Drag to reorder"
                />

                <div class="field-item-info">
                  <h4>{{ field.label }}</h4>
                  <span class="field-type">{{ field.fieldtype }}</span>
                </div>

                <div class="field-item-actions">
                  <IconButton
                    icon="bi bi-gear"
                    variant="ghost"
                    size="sm"
                    aria-label="Edit field"
                    @click.stop="selectField(field.id)"
                  />
                  <IconButton
                    icon="bi bi-files"
                    variant="ghost"
                    size="sm"
                    aria-label="Duplicate field"
                    @click.stop="duplicateField(field.id)"
                  />
                  <IconButton
                    icon="bi bi-trash"
                    variant="ghost"
                    size="sm"
                    color="error"
                    aria-label="Delete field"
                    @click.stop="confirmDeleteField(field.id)"
                  />
                </div>
              </div>

              <!-- Drop zone between fields -->
              <DropZone
                v-if="index < formData.fields.length - 1"
                position="between"
                :index="index + 1"
                compact
                @drop="handleFieldDrop"
              />
            </div>
          </div>
        </Card>
      </div>

      <!-- Properties Panel (Right) - Only shown when field is selected -->
      <Card
        v-if="selectedField"
        title="Field Properties"
        variant="default"
        class="properties-panel"
      >
        <template #actions>
          <IconButton
            icon="bi bi-x"
            variant="ghost"
            aria-label="Close properties"
            @click="clearSelection"
          />
        </template>

        <div class="properties-content">
          <TextInput
            v-model="selectedField.label"
            label="Field Label"
            required
            @update:model-value="updateSelectedField({ label: $event })"
          />

          <TextInput
            v-model="selectedField.placeholder"
            label="Placeholder Text"
            @update:model-value="updateSelectedField({ placeholder: $event })"
          />

          <div class="form-check">
            <input
              id="required-checkbox"
              v-model="selectedField.required"
              type="checkbox"
              class="form-check-input"
              @change="updateSelectedField({ required: $event.target.checked })"
            />
            <label for="required-checkbox" class="form-check-label">
              Required Field
            </label>
          </div>
        </div>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import { useFormBuilder } from '@/Composables/useFormBuilder';
import { useUndoRedo } from '@/Composables/useUndoRedo';
import { useAutoSave } from '@/Composables/useAutoSave';

// Components
import PrimaryButton from '@/Components/UI/Button/PrimaryButton.vue';
import SecondaryButton from '@/Components/UI/Button/SecondaryButton.vue';
import IconButton from '@/Components/UI/Button/IconButton.vue';
import TextInput from '@/Components/UI/Input/TextInput.vue';
import Card from '@/Components/UI/Card/Card.vue';
import FieldLibraryPanel from '@/Components/FormBuilder/FieldLibrary/FieldLibraryPanel.vue';
import DropZone from '@/Components/FormBuilder/Canvas/DropZone.vue';

// Form Builder State
const {
  formData,
  selectedFieldId,
  selectedField,
  addField,
  removeField,
  updateField,
  duplicateField,
  selectField,
  clearSelection,
  exportFormData,
  loadFormData,
  validationErrors
} = useFormBuilder();

// Undo/Redo
const {
  canUndo,
  canRedo,
  pushState,
  undo,
  redo
} = useUndoRedo(exportFormData());

// Auto-save
const {
  isSaving,
  saveStatusText,
  saveStatusIcon,
  triggerSave,
  forceSave
} = useAutoSave(async (data) => {
  // Save to backend
  console.log('Saving form:', data);
  await new Promise(resolve => setTimeout(resolve, 1000)); // Simulate API call
});

// Watch for form changes
watch(formData, (newData) => {
  pushState(newData);
  triggerSave(newData);
}, { deep: true });

// Methods
const handleUndo = () => {
  const previousState = undo();
  if (previousState) {
    loadFormData(previousState);
  }
};

const handleRedo = () => {
  const nextState = redo();
  if (nextState) {
    loadFormData(nextState);
  }
};

const handleFieldAdd = (fieldData) => {
  addField({
    type: fieldData.field.id,
    label: fieldData.field.defaultProps.label,
    ...fieldData.field.defaultProps
  });
};

const handleFieldDragStart = (data) => {
  console.log('Field drag started:', data);
};

const handleFieldDrop = (dropData) => {
  const { data, index } = dropData;
  addField({
    type: data.fieldType,
    label: data.fieldData.defaultProps.label,
    ...data.fieldData.defaultProps
  }, index);
};

const updateSelectedField = (updates) => {
  if (selectedField.value) {
    updateField(selectedField.value.id, updates);
  }
};

const confirmDeleteField = (fieldId) => {
  if (confirm('Are you sure you want to delete this field?')) {
    removeField(fieldId);
  }
};

const handlePreview = () => {
  console.log('Opening preview...');
};

const handleSave = async () => {
  await forceSave(exportFormData());
};

const openFormSettings = () => {
  console.log('Opening form settings...');
};
</script>

<style scoped lang="scss">
@import '@/Styles/design-tokens.scss';

.form-builder-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: var(--color-background-secondary);
}

.toolbar {
  display: flex;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-3) var(--space-4);
  background: var(--color-surface);
  border-bottom: var(--border-width-thin) solid var(--color-border);
  box-shadow: var(--shadow-sm);
}

.toolbar-group {
  display: flex;
  gap: var(--space-2);
}

.auto-save-status {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-left: auto;
  padding: var(--space-2) var(--space-3);
  background: var(--color-background-secondary);
  border-radius: var(--border-radius-md);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);

  .status-icon {
    font-size: var(--size-icon-sm);

    &.bi-arrow-clockwise {
      animation: spin 1s linear infinite;
    }

    &.bi-check-circle-fill {
      color: var(--color-success-600);
    }

    &.bi-exclamation-triangle-fill {
      color: var(--color-error-600);
    }
  }
}

.toolbar-actions {
  display: flex;
  gap: var(--space-2);
}

.form-builder-content {
  display: flex;
  flex: 1;
  overflow: hidden;
}

.form-canvas-wrapper {
  flex: 1;
  padding: var(--space-6);
  overflow-y: auto;
}

.form-metadata {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-4);
  margin-bottom: var(--space-6);
}

.field-list {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
}

.field-item {
  padding: var(--space-4);
  background: var(--color-surface);
  border: var(--border-width-thin) solid var(--color-border);
  border-radius: var(--border-radius-lg);
  cursor: pointer;
  transition: var(--transition-normal);

  &:hover {
    border-color: var(--color-primary-300);
    box-shadow: var(--shadow-sm);
  }

  &--selected {
    border-color: var(--color-primary-500);
    background: var(--color-primary-50);
    box-shadow: var(--shadow-md);
  }
}

.field-item-header {
  display: flex;
  align-items: center;
  gap: var(--space-3);
}

.field-item-info {
  flex: 1;

  h4 {
    margin: 0;
    font-size: var(--font-size-base);
    font-weight: var(--font-weight-semibold);
    color: var(--color-text-primary);
  }

  .field-type {
    font-size: var(--font-size-xs);
    color: var(--color-text-tertiary);
  }
}

.field-item-actions {
  display: flex;
  gap: var(--space-1);
  opacity: 0;
  transition: var(--transition-opacity);
}

.field-item:hover .field-item-actions {
  opacity: 1;
}

.properties-panel {
  width: var(--properties-panel-width);
  max-height: calc(100vh - 120px);
  overflow-y: auto;
  margin: var(--space-6) var(--space-6) var(--space-6) 0;
}

.properties-content {
  display: flex;
  flex-direction: column;
  gap: var(--space-4);
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

/* Responsive */
@media (max-width: 1024px) {
  .form-metadata {
    grid-template-columns: 1fr;
  }

  .properties-panel {
    width: 280px;
  }
}

@media (max-width: 768px) {
  .form-builder-content {
    flex-direction: column;
  }

  .properties-panel {
    width: 100%;
    margin: 0;
    max-height: none;
  }
}
</style>
```

---

## 🔧 Composables Usage

### Example 2: Using useFormBuilder

```vue
<script setup>
import { useFormBuilder } from '@/Composables/useFormBuilder';

// Initialize with existing data (edit mode)
const existingData = {
  formId: 'FORM-001',
  formName: 'Employee Onboarding',
  formShortCode: 'EMP-ONB',
  fields: [
    {
      id: '1',
      fieldname: 'full_name',
      label: 'Full Name',
      fieldtype: 'Data',
      required: true
    }
  ]
};

const {
  formData,
  addField,
  updateField,
  removeField,
  duplicateField,
  reorderFields,
  selectField,
  selectedField,
  isFormValid,
  validationErrors,
  exportFormData
} = useFormBuilder(existingData);

// Add a new field
const addEmailField = () => {
  const newField = addField({
    type: 'email',
    label: 'Email Address',
    placeholder: 'user@example.com',
    required: true
  });

  console.log('New field added:', newField);
};

// Update field properties
const updateFieldLabel = (fieldId, newLabel) => {
  const success = updateField(fieldId, { label: newLabel });
  if (success) {
    console.log('Field updated successfully');
  }
};

// Remove a field
const deleteField = (fieldId) => {
  const success = removeField(fieldId);
  if (success) {
    console.log('Field removed successfully');
  }
};

// Duplicate a field
const cloneField = (fieldId) => {
  const clonedField = duplicateField(fieldId);
  if (clonedField) {
    console.log('Field duplicated:', clonedField);
  }
};

// Reorder fields (drag and drop)
const moveFieldUp = (fieldId) => {
  const index = formData.value.fields.findIndex(f => f.id === fieldId);
  if (index > 0) {
    reorderFields(index, index - 1);
  }
};

// Validate form before save
const saveForm = async () => {
  if (!isFormValid.value) {
    console.error('Form validation errors:', validationErrors.value);
    return;
  }

  const dataToSave = exportFormData();
  // Save to backend...
  console.log('Saving:', dataToSave);
};
</script>
```

### Example 3: Using useUndoRedo with Custom State

```vue
<script setup>
import { ref, watch } from 'vue';
import { useUndoRedo } from '@/Composables/useUndoRedo';

// Your application state
const myState = ref({
  title: 'My Document',
  content: 'Hello world',
  tags: ['important']
});

// Initialize undo/redo
const {
  canUndo,
  canRedo,
  undoCount,
  redoCount,
  pushState,
  undo,
  redo,
  clearHistory
} = useUndoRedo(myState.value, {
  maxHistorySize: 100,
  debounceMs: 500,
  enableKeyboardShortcuts: true // Ctrl+Z, Ctrl+Y work automatically
});

// Watch for state changes and push to history
watch(myState, (newState) => {
  pushState(newState); // Debounced by default
}, { deep: true });

// Manual undo
const handleUndo = () => {
  const previousState = undo();
  if (previousState) {
    myState.value = previousState;
  }
};

// Manual redo
const handleRedo = () => {
  const nextState = redo();
  if (nextState) {
    myState.value = nextState;
  }
};

// Clear history (e.g., after saving)
const handleSave = async () => {
  // Save logic...
  clearHistory(); // Start fresh history after save
};
</script>

<template>
  <div>
    <div class="undo-redo-toolbar">
      <button :disabled="!canUndo" @click="handleUndo">
        Undo ({{ undoCount }})
      </button>
      <button :disabled="!canRedo" @click="handleRedo">
        Redo ({{ redoCount }})
      </button>
    </div>

    <input v-model="myState.title" placeholder="Title" />
    <textarea v-model="myState.content" placeholder="Content"></textarea>
  </div>
</template>
```

### Example 4: Using useAutoSave

```vue
<script setup>
import { ref, watch } from 'vue';
import { useAutoSave } from '@/Composables/useAutoSave';
import axiosInstance from '@/shared/services/interceptor';

// Your form data
const formData = ref({
  name: '',
  email: '',
  message: ''
});

// Define save function
const saveToBackend = async (data) => {
  const response = await axiosInstance.post('/api/save', data);
  return response.data;
};

// Initialize auto-save
const {
  isSaving,
  lastSaved,
  saveError,
  saveStatus,
  saveStatusText,
  saveStatusIcon,
  triggerSave,
  forceSave,
  cancelSave,
  enable,
  disable
} = useAutoSave(saveToBackend, {
  debounceMs: 2000, // Wait 2 seconds after last change
  enabled: true,
  onSaveStart: () => {
    console.log('Save started...');
  },
  onSaveSuccess: (result) => {
    console.log('Saved successfully at:', result.savedAt);
  },
  onSaveError: (error) => {
    console.error('Save failed:', error);
    alert('Failed to save. Please try again.');
  }
});

// Watch for changes and trigger auto-save
watch(formData, (newData) => {
  triggerSave(newData); // Debounced
}, { deep: true });

// Force immediate save (e.g., on form submission)
const handleSubmit = async () => {
  try {
    await forceSave(formData.value);
    alert('Form submitted successfully!');
  } catch (error) {
    alert('Submission failed. Please try again.');
  }
};

// Toggle auto-save on/off
const toggleAutoSave = () => {
  if (isEnabled.value) {
    disable();
  } else {
    enable();
  }
};
</script>

<template>
  <div class="form-container">
    <!-- Auto-save indicator -->
    <div class="auto-save-indicator" :class="`status-${saveStatus}`">
      <i :class="saveStatusIcon"></i>
      <span>{{ saveStatusText }}</span>
      <span v-if="lastSaved" class="last-saved">
        Last saved: {{ new Date(lastSaved).toLocaleTimeString() }}
      </span>
    </div>

    <!-- Form fields -->
    <input v-model="formData.name" placeholder="Name" />
    <input v-model="formData.email" type="email" placeholder="Email" />
    <textarea v-model="formData.message" placeholder="Message"></textarea>

    <!-- Actions -->
    <div class="form-actions">
      <button :disabled="isSaving" @click="handleSubmit">
        {{ isSaving ? 'Saving...' : 'Submit' }}
      </button>
      <button @click="cancelSave">
        Cancel Pending Save
      </button>
    </div>

    <!-- Error message -->
    <div v-if="saveError" class="error-message">
      <i class="bi bi-exclamation-triangle"></i>
      Save failed: {{ saveError.message }}
    </div>
  </div>
</template>
```

---

## 🎨 Component Styling Examples

### Custom Theming with Design Tokens

```vue
<template>
  <div class="custom-card">
    <h3>Custom Styled Component</h3>
    <p>Using design tokens for consistent styling</p>
  </div>
</template>

<style scoped lang="scss">
@import '@/Styles/design-tokens.scss';

.custom-card {
  /* Layout */
  padding: var(--space-6);
  margin-bottom: var(--space-4);

  /* Colors */
  background: linear-gradient(
    135deg,
    var(--color-primary-50) 0%,
    var(--color-secondary-50) 100%
  );
  border: var(--border-width-thin) solid var(--color-primary-200);

  /* Typography */
  h3 {
    font-size: var(--font-size-xl);
    font-weight: var(--font-weight-bold);
    color: var(--color-primary-700);
    margin-bottom: var(--space-2);
  }

  p {
    font-size: var(--font-size-base);
    color: var(--color-text-secondary);
    line-height: var(--line-height-relaxed);
  }

  /* Effects */
  border-radius: var(--border-radius-xl);
  box-shadow: var(--shadow-md);
  transition: var(--transition-normal);

  &:hover {
    box-shadow: var(--shadow-lg);
    transform: translateY(-2px);
  }
}
</style>
```

---

## 📱 Responsive Design Examples

### Mobile-First Approach

```vue
<template>
  <div class="responsive-container">
    <div class="content">
      <!-- Your content -->
    </div>
  </div>
</template>

<style scoped lang="scss">
@import '@/Styles/design-tokens.scss';

.responsive-container {
  /* Mobile first (default) */
  padding: var(--space-4);
  font-size: var(--font-size-sm);

  .content {
    display: flex;
    flex-direction: column;
    gap: var(--space-3);
  }

  /* Tablet */
  @media (min-width: 768px) {
    padding: var(--space-6);
    font-size: var(--font-size-base);

    .content {
      flex-direction: row;
      gap: var(--space-4);
    }
  }

  /* Desktop */
  @media (min-width: 1024px) {
    padding: var(--space-8);
    max-width: 1200px;
    margin: 0 auto;

    .content {
      gap: var(--space-6);
    }
  }

  /* Large Desktop */
  @media (min-width: 1440px) {
    max-width: 1400px;
  }
}
</style>
```

---

**This is a comprehensive guide! For more examples, check the individual component files and the main implementation plan.**

**Created**: November 11, 2025
**Last Updated**: November 11, 2025
**Version**: 1.0
