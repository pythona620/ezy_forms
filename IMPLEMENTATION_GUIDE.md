# EzyForms UI/UX Redesign - Implementation Guide

## 📚 Table of Contents
1. [Overview](#overview)
2. [What Has Been Created](#what-has-been-created)
3. [Installation & Setup](#installation--setup)
4. [Component Usage](#component-usage)
5. [Composables Usage](#composables-usage)
6. [Next Steps](#next-steps)
7. [Code Examples](#code-examples)

---

## 🎯 Overview

This guide provides detailed instructions for implementing the modernized EzyForms form builder UI/UX redesign. The project includes a comprehensive design system, reusable UI components, form builder logic composables, and structured architecture.

### Goals Achieved So Far
✅ Modern design system with 50+ design tokens
✅ Reusable UI component library (buttons, inputs, cards)
✅ Form builder composables (state management, undo/redo, auto-save)
✅ Field type definitions with 25+ field types
✅ Modular architecture for maintainability

---

## 📦 What Has Been Created

### 1. Design System
**File**: `/src/Styles/design-tokens.scss`

A comprehensive modern design system featuring:
- Color palette (primary, secondary, success, warning, error, info, neutrals)
- Typography system (6 font sizes with responsive scaling)
- Spacing system (8px grid, 13 sizes)
- Shadow system (7 elevation levels)
- Border radius system
- Animation & transition presets
- Accessibility features (focus rings, reduced motion)

**Usage**:
```scss
// Import in any component
@import '@/Styles/design-tokens.scss';

// Use CSS variables
.my-component {
  color: var(--color-primary-600);
  padding: var(--space-4);
  border-radius: var(--border-radius-lg);
  box-shadow: var(--shadow-md);
  transition: var(--transition-normal);
}
```

---

### 2. UI Components

#### **PrimaryButton.vue**
**Location**: `/src/Components/UI/Button/PrimaryButton.vue`

Modern button component with multiple variants and states.

**Props**:
- `variant`: 'solid' | 'outline' | 'ghost' (default: 'solid')
- `size`: 'sm' | 'md' | 'lg' (default: 'md')
- `disabled`: boolean
- `loading`: boolean
- `iconLeft`: string (icon class)
- `iconRight`: string (icon class)
- `fullWidth`: boolean

**Usage**:
```vue
<template>
  <PrimaryButton
    variant="solid"
    size="md"
    :loading="isSaving"
    icon-left="bi bi-save"
    @click="handleSave"
  >
    Save Form
  </PrimaryButton>
</template>

<script setup>
import PrimaryButton from '@/Components/UI/Button/PrimaryButton.vue';
const isSaving = ref(false);

const handleSave = () => {
  isSaving.value = true;
  // Save logic...
};
</script>
```

---

#### **SecondaryButton.vue**
**Location**: `/src/Components/UI/Button/SecondaryButton.vue`

Similar to PrimaryButton but with neutral/gray color scheme for secondary actions.

**Usage**:
```vue
<SecondaryButton
  variant="outline"
  size="md"
  @click="handleCancel"
>
  Cancel
</SecondaryButton>
```

---

#### **IconButton.vue**
**Location**: `/src/Components/UI/Button/IconButton.vue`

Compact icon-only button for toolbar actions.

**Props**:
- `icon`: string (required - icon class)
- `variant`: 'solid' | 'outline' | 'ghost'
- `size`: 'sm' | 'md' | 'lg'
- `color`: 'default' | 'primary' | 'success' | 'warning' | 'error'
- `ariaLabel`: string (required for accessibility)
- `tooltip`: string

**Usage**:
```vue
<IconButton
  icon="bi bi-trash"
  variant="ghost"
  color="error"
  aria-label="Delete field"
  tooltip="Delete this field"
  @click="handleDelete"
/>
```

---

#### **TextInput.vue**
**Location**: `/src/Components/UI/Input/TextInput.vue`

Enhanced text input with validation, icons, and error states.

**Props**:
- `modelValue`: string | number
- `label`: string
- `type`: 'text' | 'email' | 'password' | 'url' | 'tel' | 'number' | 'search'
- `placeholder`: string
- `helpText`: string
- `errorMessage`: string
- `disabled`: boolean
- `readonly`: boolean
- `required`: boolean
- `clearable`: boolean
- `iconLeft`: string
- `iconRight`: string
- `size`: 'sm' | 'md' | 'lg'
- `maxLength`: number
- `minLength`: number

**Usage**:
```vue
<template>
  <TextInput
    v-model="formData.email"
    label="Email Address"
    type="email"
    placeholder="Enter your email"
    icon-left="bi bi-envelope"
    :required="true"
    :error-message="emailError"
    help-text="We'll never share your email"
    @blur="validateEmail"
  />
</template>

<script setup>
import TextInput from '@/Components/UI/Input/TextInput.vue';
import { ref } from 'vue';

const formData = ref({ email: '' });
const emailError = ref('');

const validateEmail = () => {
  if (!formData.value.email.includes('@')) {
    emailError.value = 'Please enter a valid email address';
  } else {
    emailError.value = '';
  }
};
</script>
```

---

#### **Card.vue**
**Location**: `/src/Components/UI/Card/Card.vue`

Flexible card container with header, body, and footer slots.

**Props**:
- `title`: string
- `variant`: 'default' | 'bordered' | 'elevated' | 'flat'
- `padded`: boolean (default: true)
- `hoverable`: boolean
- `clickable`: boolean

**Slots**:
- `header`: Custom header content
- `actions`: Header actions (top-right)
- `default`: Body content
- `footer`: Footer content

**Usage**:
```vue
<template>
  <Card
    title="Field Properties"
    variant="elevated"
    :padded="true"
  >
    <template #actions>
      <IconButton icon="bi bi-x" @click="close" />
    </template>

    <!-- Body content -->
    <div>
      <TextInput v-model="fieldLabel" label="Field Label" />
    </div>

    <template #footer>
      <div class="d-flex justify-content-end gap-2">
        <SecondaryButton @click="cancel">Cancel</SecondaryButton>
        <PrimaryButton @click="save">Save</PrimaryButton>
      </div>
    </template>
  </Card>
</template>
```

---

### 3. Composables

#### **useFormBuilder.js**
**Location**: `/src/Composables/useFormBuilder.js`

Central state management for form builder operations.

**API**:
```javascript
const {
  // State
  formData,                    // ref: Form metadata and structure
  selectedFieldId,             // ref: Currently selected field ID
  selectedField,               // computed: Selected field object
  isDirty,                     // ref: Has unsaved changes

  // Computed
  totalFields,                 // computed: Total number of fields
  isFormValid,                 // computed: Form validation status
  validationErrors,            // computed: Array of validation errors

  // Field Methods
  addField,                    // (fieldData, position) => newField
  removeField,                 // (fieldId) => boolean
  updateField,                 // (fieldId, updates) => boolean
  duplicateField,              // (fieldId) => newField
  reorderFields,               // (fromIndex, toIndex) => boolean

  // Selection Methods
  selectField,                 // (fieldId) => void
  clearSelection,              // () => void

  // Form Operations
  resetForm,                   // () => void
  loadFormData,                // (data) => void
  exportFormData,              // () => object
} = useFormBuilder(initialData);
```

**Usage**:
```vue
<script setup>
import { useFormBuilder } from '@/Composables/useFormBuilder';

// Initialize form builder
const {
  formData,
  selectedField,
  addField,
  removeField,
  updateField,
  selectField,
  isFormValid,
  exportFormData
} = useFormBuilder();

// Add a text field
const handleAddTextField = () => {
  const newField = addField({
    type: 'text',
    label: 'Full Name',
    placeholder: 'Enter your name',
    required: true
  });

  selectField(newField.id);
};

// Update field when properties change
const handleUpdateLabel = (newLabel) => {
  if (selectedField.value) {
    updateField(selectedField.value.id, { label: newLabel });
  }
};

// Save form
const handleSave = async () => {
  if (isFormValid.value) {
    const formDataToSave = exportFormData();
    await saveToBackend(formDataToSave);
  }
};
</script>
```

---

#### **useUndoRedo.js**
**Location**: `/src/Composables/useUndoRedo.js`

Undo/redo functionality with history management and keyboard shortcuts.

**API**:
```javascript
const {
  // State
  history,                     // ref: Array of history states
  currentIndex,                // ref: Current position in history

  // Computed
  canUndo,                     // computed: Can undo
  canRedo,                     // computed: Can redo
  undoCount,                   // computed: Number of undo steps
  redoCount,                   // computed: Number of redo steps

  // Methods
  pushState,                   // (newState, immediate) => void
  undo,                        // () => previousState
  redo,                        // () => nextState
  jumpTo,                      // (index) => targetState
  clearHistory,                // () => void
} = useUndoRedo(initialState, options);
```

**Options**:
- `maxHistorySize`: number (default: 50)
- `debounceMs`: number (default: 300)
- `enableKeyboardShortcuts`: boolean (default: true)

**Usage**:
```vue
<script setup>
import { useFormBuilder } from '@/Composables/useFormBuilder';
import { useUndoRedo } from '@/Composables/useUndoRedo';
import { watch } from 'vue';

const { formData, exportFormData } = useFormBuilder();

// Initialize undo/redo with form data
const {
  canUndo,
  canRedo,
  pushState,
  undo,
  redo
} = useUndoRedo(exportFormData(), {
  maxHistorySize: 50,
  enableKeyboardShortcuts: true
});

// Watch for form changes and push to history
watch(formData, (newFormData) => {
  pushState(newFormData); // Debounced by default
}, { deep: true });

// Manual undo/redo (keyboard shortcuts work automatically)
const handleUndo = () => {
  if (canUndo.value) {
    const previousState = undo();
    if (previousState) {
      // Load previous state back into form
      loadFormData(previousState);
    }
  }
};

const handleRedo = () => {
  if (canRedo.value) {
    const nextState = redo();
    if (nextState) {
      loadFormData(nextState);
    }
  }
};
</script>

<template>
  <div class="toolbar">
    <IconButton
      icon="bi bi-arrow-counterclockwise"
      :disabled="!canUndo"
      aria-label="Undo"
      @click="handleUndo"
    />
    <IconButton
      icon="bi bi-arrow-clockwise"
      :disabled="!canRedo"
      aria-label="Redo"
      @click="handleRedo"
    />
  </div>
</template>
```

---

#### **useAutoSave.js**
**Location**: `/src/Composables/useAutoSave.js`

Automatic form saving with debounce and visual feedback.

**API**:
```javascript
const {
  // State
  isSaving,                    // ref: Currently saving
  lastSaved,                   // ref: Date of last save
  saveError,                   // ref: Last save error

  // Computed
  saveStatus,                  // computed: 'saving' | 'saved' | 'error' | 'idle'
  saveStatusText,              // computed: Human-readable status
  saveStatusIcon,              // computed: Icon class for status
  hasPendingSave,              // computed: Has debounced save pending

  // Methods
  triggerSave,                 // (data, immediate) => void
  forceSave,                   // (data) => Promise
  cancelSave,                  // () => void
  enable,                      // () => void
  disable,                     // () => void
} = useAutoSave(saveFunction, options);
```

**Options**:
- `debounceMs`: number (default: 2000)
- `enabled`: boolean (default: true)
- `onSaveStart`: function
- `onSaveSuccess`: function
- `onSaveError`: function

**Usage**:
```vue
<script setup>
import { useFormBuilder } from '@/Composables/useFormBuilder';
import { useAutoSave } from '@/Composables/useAutoSave';
import { watch } from 'vue';
import axiosInstance from '@/shared/services/interceptor';
import { apis } from '@/shared/apiurls';

const { formData, exportFormData } = useFormBuilder();

// Define save function
const saveFormToBackend = async (data) => {
  const response = await axiosInstance.post(apis.savedata, data);
  return response.data;
};

// Initialize auto-save
const {
  isSaving,
  saveStatus,
  saveStatusText,
  saveStatusIcon,
  triggerSave,
  forceSave
} = useAutoSave(saveFormToBackend, {
  debounceMs: 2000,
  onSaveSuccess: () => {
    console.log('Form saved successfully');
  },
  onSaveError: (error) => {
    console.error('Save failed:', error);
  }
});

// Watch for changes and trigger auto-save
watch(formData, () => {
  const dataToSave = exportFormData();
  triggerSave(dataToSave); // Debounced save
}, { deep: true });

// Force immediate save (e.g., on form submission)
const handleSubmit = async () => {
  const dataToSave = exportFormData();
  await forceSave(dataToSave);
};
</script>

<template>
  <div class="auto-save-indicator">
    <i :class="saveStatusIcon"></i>
    <span>{{ saveStatusText }}</span>
  </div>
</template>
```

---

### 4. Field Type Definitions
**Location**: `/src/Components/FormBuilder/FieldLibrary/fieldTypes.js`

Comprehensive field type configuration with 25+ field types organized into 6 categories:

1. **Basic Fields**: text, textarea, number, email, phone, url
2. **Choice Fields**: select, multiselect, radio, checkbox, toggle
3. **Date & Time**: date, time, datetime
4. **File & Media**: fileupload, imageupload, signature
5. **Layout Elements**: sectionbreak, columnbreak, heading, paragraph, divider
6. **Advanced Fields**: table, link, dynamiclist, formula, qrcode

**Usage**:
```javascript
import {
  FIELD_CATEGORIES,
  FIELD_TYPES,
  getFieldsByCategory,
  getFieldType,
  searchFieldTypes
} from '@/Components/FormBuilder/FieldLibrary/fieldTypes';

// Get all basic fields
const basicFields = getFieldsByCategory('basic');

// Get specific field type
const textFieldConfig = getFieldType('text');
console.log(textFieldConfig.defaultProps);

// Search fields
const results = searchFieldTypes('date');
```

---

## 🚀 Installation & Setup

### 1. Install Required Dependencies

```bash
cd apps/ezy_forms/ezyformsfrontend

# Install nanoid for unique ID generation
npm install nanoid

# Ensure existing dependencies are installed
npm install
```

### 2. Import Design Tokens

Add to your `main.js` or global styles:

```javascript
// main.js
import './Styles/design-tokens.scss';
```

Or in your main SCSS file:

```scss
// styles.scss
@import './design-tokens.scss';
```

### 3. Register Components Globally (Optional)

```javascript
// main.js
import { createApp } from 'vue';
import App from './App.vue';

// Import UI components
import PrimaryButton from './Components/UI/Button/PrimaryButton.vue';
import SecondaryButton from './Components/UI/Button/SecondaryButton.vue';
import IconButton from './Components/UI/Button/IconButton.vue';
import TextInput from './Components/UI/Input/TextInput.vue';
import Card from './Components/UI/Card/Card.vue';

const app = createApp(App);

// Register globally
app.component('PrimaryButton', PrimaryButton);
app.component('SecondaryButton', SecondaryButton);
app.component('IconButton', IconButton);
app.component('TextInput', TextInput);
app.component('Card', Card);

app.mount('#app');
```

Or import locally in components as needed.

---

## 📖 Next Steps

### Immediate Tasks (Priority Order)

1. **Complete Remaining UI Components** (2-3 hours)
   - [ ] SelectInput.vue
   - [ ] MultiSelect.vue
   - [ ] Toggle.vue
   - [ ] Modal.vue
   - [ ] Tooltip.vue

2. **Build Field Library Panel** (3-4 hours)
   - [ ] FieldLibraryPanel.vue (main container)
   - [ ] FieldCategory.vue (collapsible categories)
   - [ ] FieldCard.vue (draggable field cards)
   - Integrate fieldTypes.js configuration

3. **Implement Form Canvas** (4-5 hours)
   - [ ] FormCanvas.vue (main workspace)
   - [ ] DropZone.vue (visual drop indicators)
   - [ ] FieldRenderer.vue (render fields based on type)
   - [ ] Implement drag-and-drop with vuedraggable

4. **Build Properties Panel** (3-4 hours)
   - [ ] PropertiesPanel.vue (main container)
   - [ ] FieldProperties.vue (basic settings)
   - [ ] ValidationRules.vue (validation config)
   - [ ] ConditionalLogic.vue (show/hide rules)

5. **Create Live Preview Panel** (2-3 hours)
   - [ ] LivePreview.vue (real-time rendering)
   - [ ] DeviceToggle.vue (desktop/tablet/mobile views)

6. **Integrate with Existing FormStepper** (4-6 hours)
   - [ ] Read existing FormStepper.vue logic
   - [ ] Replace step 2 (form fields) with new components
   - [ ] Maintain backward compatibility
   - [ ] Test workflow integration

7. **Polish & Testing** (3-4 hours)
   - [ ] Add animations and transitions
   - [ ] Accessibility testing
   - [ ] Cross-browser testing
   - [ ] Performance optimization

---

## 💡 Code Examples

### Example 1: Simple Form Builder Page

```vue
<template>
  <div class="form-builder-page">
    <div class="toolbar">
      <IconButton
        icon="bi bi-arrow-counterclockwise"
        :disabled="!canUndo"
        aria-label="Undo"
        @click="handleUndo"
      />
      <IconButton
        icon="bi bi-arrow-clockwise"
        :disabled="!canRedo"
        aria-label="Redo"
        @click="handleRedo"
      />

      <div class="auto-save-status">
        <i :class="saveStatusIcon"></i>
        <span>{{ saveStatusText }}</span>
      </div>

      <PrimaryButton
        :loading="isSaving"
        @click="handleSave"
      >
        Save Form
      </PrimaryButton>
    </div>

    <div class="form-builder-content">
      <Card title="Form Fields" variant="elevated">
        <div v-for="field in formData.fields" :key="field.id" class="field-item">
          <TextInput
            v-if="field.fieldtype === 'Data'"
            v-model="field.label"
            :label="field.label"
            @update:model-value="updateFieldLabel(field.id, $event)"
          />
        </div>

        <PrimaryButton
          variant="outline"
          icon-left="bi bi-plus"
          @click="handleAddField"
        >
          Add Field
        </PrimaryButton>
      </Card>
    </div>
  </div>
</template>

<script setup>
import { useFormBuilder } from '@/Composables/useFormBuilder';
import { useUndoRedo } from '@/Composables/useUndoRedo';
import { useAutoSave } from '@/Composables/useAutoSave';
import { watch } from 'vue';

// Initialize composables
const {
  formData,
  addField,
  updateField,
  exportFormData,
  loadFormData
} = useFormBuilder();

const {
  canUndo,
  canRedo,
  pushState,
  undo,
  redo
} = useUndoRedo(exportFormData());

const {
  isSaving,
  saveStatusText,
  saveStatusIcon,
  triggerSave,
  forceSave
} = useAutoSave(async (data) => {
  // Save to backend
  await saveToBackend(data);
});

// Watch for changes
watch(formData, (newData) => {
  pushState(newData);
  triggerSave(newData);
}, { deep: true });

// Methods
const handleAddField = () => {
  addField({
    type: 'text',
    label: 'New Field'
  });
};

const updateFieldLabel = (fieldId, newLabel) => {
  updateField(fieldId, { label: newLabel });
};

const handleUndo = () => {
  const previousState = undo();
  if (previousState) loadFormData(previousState);
};

const handleRedo = () => {
  const nextState = redo();
  if (nextState) loadFormData(nextState);
};

const handleSave = async () => {
  await forceSave(exportFormData());
};
</script>

<style scoped lang="scss">
@import '@/Styles/design-tokens.scss';

.form-builder-page {
  display: flex;
  flex-direction: column;
  height: 100vh;
}

.toolbar {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  padding: var(--space-4);
  background: var(--color-background-secondary);
  border-bottom: 1px solid var(--color-border);
}

.auto-save-status {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-left: auto;
  margin-right: var(--space-4);
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
}

.form-builder-content {
  flex: 1;
  padding: var(--space-6);
  overflow-y: auto;
}

.field-item {
  margin-bottom: var(--space-4);
  padding: var(--space-4);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius-lg);
}
</style>
```

---

## 📋 Component Checklist

### ✅ Completed
- [x] Design system (design-tokens.scss)
- [x] PrimaryButton component
- [x] SecondaryButton component
- [x] IconButton component
- [x] TextInput component
- [x] Card component
- [x] useFormBuilder composable
- [x] useUndoRedo composable
- [x] useAutoSave composable
- [x] Field type definitions (fieldTypes.js)

### 🔄 In Progress
- [ ] Field Library Panel components

### 📝 To Do
- [ ] SelectInput component
- [ ] MultiSelect component
- [ ] Toggle component
- [ ] Modal component
- [ ] Tooltip component
- [ ] Form Canvas components
- [ ] Properties Panel components
- [ ] Live Preview Panel components
- [ ] Integration with existing FormStepper.vue

---

## 🤝 Support & Questions

For questions or issues during implementation:
1. Check this guide first
2. Review the code comments in each component
3. Refer to FORM_BUILDER_REDESIGN_PLAN.md for detailed specifications

---

**Last Updated**: November 11, 2025
**Version**: 1.0
**Status**: Phase 1 Complete - Ready for Phase 2 Implementation
