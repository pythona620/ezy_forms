# Quick Start: Drag-and-Drop Field Library

## 🚀 5-Minute Integration Guide

This guide shows you exactly what to add to FormStepper.vue to get the drag-and-drop field library working.

---

## Step 1: Add Imports (2 minutes)

Open `FormStepper.vue` and add these imports to the `<script setup>` section (around line 410):

```javascript
// ADD THESE LINES after existing imports:

// Drag-and-Drop Field Library
import FieldLibraryPanel from "@/Components/FormBuilder/FieldLibrary/FieldLibraryPanel.vue";
import DropZone from "@/Components/FormBuilder/Canvas/DropZone.vue";
import { FIELD_TYPES, FIELD_CATEGORIES } from "@/Components/FormBuilder/FieldLibrary/fieldTypes.js";

// Add reactive state for drag-and-drop
const draggedFieldType = ref(null);
const selectedFieldForEdit = ref(null);
const showFieldLibrary = ref(true);
```

---

## Step 2: Add Field Library Panel to Template (2 minutes)

Find the section with `activeStep === 2` (around line 321) and add the field library panel.

**BEFORE** the existing `<div class="main-block" ref="mainBlockRef">`, add:

```vue
<!-- FIELD LIBRARY PANEL (NEW) -->
<div class="form-builder-with-library">
  <!-- Left: Field Library -->
  <aside class="field-library-container" v-if="showFieldLibrary">
    <FieldLibraryPanel
      :collapsible="true"
      @field-add="handleFieldAddFromLibrary"
      @field-dragstart="handleFieldDragStart"
    />
  </aside>

  <!-- Right: Form Canvas (existing content) -->
  <div class="form-canvas-container">
    <!-- Your existing main-block code goes here -->
    <div class="main-block" ref="mainBlockRef">
      <!-- ... existing block code ... -->
    </div>
  </div>
</div>
```

---

## Step 3: Add Event Handlers (1 minute)

Add these functions in the `<script setup>` section (after existing functions):

```javascript
// Handle field added from library (click)
const handleFieldAddFromLibrary = (fieldType) => {
  console.log('Field added:', fieldType);

  // Get current block (default to first block if none selected)
  const currentBlockIndex = 0; // or track which block is active
  const currentBlock = blockArr.value[currentBlockIndex];

  // Create field from type
  const newField = createFieldFromLibraryType(fieldType);

  // Add to block's sections
  if (!currentBlock.sections) {
    currentBlock.sections = [];
  }

  if (currentBlock.sections.length === 0) {
    currentBlock.sections.push({
      rows: [[{ fields: [] }]]
    });
  }

  // Add to first section, first row, first column
  const firstSection = currentBlock.sections[0];
  const firstRow = firstSection.rows[0];
  const firstColumn = firstRow[0];

  if (!firstColumn.fields) {
    firstColumn.fields = [];
  }

  firstColumn.fields.push(newField);

  console.log('Field added successfully:', newField);
};

// Handle drag start from library
const handleFieldDragStart = (fieldType) => {
  console.log('Drag started:', fieldType);
  draggedFieldType.value = fieldType;
};

// Create field object from library field type
const createFieldFromLibraryType = (fieldType) => {
  const fieldDef = FIELD_TYPES[fieldType];

  if (!fieldDef) {
    console.error('Field type not found:', fieldType);
    return null;
  }

  // Generate unique field name
  const timestamp = Date.now();
  const fieldname = `${fieldType}_${timestamp}`;

  return {
    id: `field_${timestamp}`,
    fieldname: fieldname,
    label: fieldDef.name,
    fieldtype: fieldDef.frappe_fieldtype,
    options: fieldDef.defaultProps?.options || '',
    reqd: fieldDef.defaultProps?.required || 0,
    read_only: 0,
    hidden: 0,
    description: fieldDef.description || '',
    default: fieldDef.defaultProps?.default || '',
    // Add other properties as needed
  };
};
```

---

## Step 4: Add Styles (30 seconds)

Add these styles to the `<style>` section at the end:

```scss
<style scoped lang="scss">
// ... existing styles ...

// NEW: Drag-and-Drop Layout
.form-builder-with-library {
  display: flex;
  gap: 1.5rem;
  padding: 1rem;
  background: #f9fafb;
  min-height: calc(100vh - 200px);
}

.field-library-container {
  width: 320px;
  flex-shrink: 0;
  position: sticky;
  top: 1rem;
  height: fit-content;
  max-height: calc(100vh - 250px);
  overflow-y: auto;
}

.form-canvas-container {
  flex: 1;
  min-width: 0;
}

// Mobile responsive
@media (max-width: 992px) {
  .form-builder-with-library {
    flex-direction: column;
  }

  .field-library-container {
    width: 100%;
    position: relative;
    max-height: 400px;
  }
}
</style>
```

---

## ✅ That's It!

You now have a working drag-and-drop field library!

### What You Can Do Now:

1. **Click a field** in the library → It adds to the form
2. **Drag a field** from the library → Drop it in the form
3. **Search fields** using the search box
4. **Collapse the library** using the arrow button

---

## 🎨 Customize It

### Change Field Library Position

```vue
<!-- Move to right side -->
<div class="form-builder-with-library" style="flex-direction: row-reverse;">
  <aside class="field-library-container">...</aside>
  <div class="form-canvas-container">...</div>
</div>
```

### Change Which Block Fields Get Added To

```javascript
// Track active block
const activeBlockIndex = ref(0);

// Update handler
const handleFieldAddFromLibrary = (fieldType) => {
  const currentBlock = blockArr.value[activeBlockIndex.value];
  // ... rest of code
};
```

### Add Drop Zones Between Fields

```vue
<template v-for="(field, fieldIndex) in fields" :key="field.id">
  <!-- Drop zone before field -->
  <DropZone
    variant="between"
    @drop="handleDropBetweenFields(blockIndex, sectionIndex, fieldIndex)"
  />

  <!-- Field -->
  <div class="field-item">
    {{ field.label }}
  </div>
</template>

<!-- Drop zone after last field -->
<DropZone
  variant="bottom"
  @drop="handleDropAfterFields(blockIndex, sectionIndex)"
/>
```

---

## 🐛 Troubleshooting

### Issue: "Cannot find module FieldLibraryPanel"

**Fix**: Make sure the file exists at:
```
src/Components/FormBuilder/FieldLibrary/FieldLibraryPanel.vue
```

### Issue: "FIELD_TYPES is not defined"

**Fix**: Import it:
```javascript
import { FIELD_TYPES } from "@/Components/FormBuilder/FieldLibrary/fieldTypes.js";
```

### Issue: Fields not showing in library

**Fix**: Check that `fieldTypes.js` exports the field definitions:
```javascript
console.log('Available fields:', Object.keys(FIELD_TYPES));
```

### Issue: Drag-and-drop not working

**Fix**: Make sure FieldCard components have `draggable="true"` attribute.

---

## 📚 Next Steps

1. **Test it**: Add a few fields using the library
2. **Customize**: Adjust styles to match your theme
3. **Enhance**: Add drop zones between fields for reordering
4. **Extend**: Add more field types in `fieldTypes.js`

---

## 💡 Pro Tips

1. **Use Ctrl+K** to quickly search for fields
2. **Collapse the library** when you need more space
3. **Drag directly** instead of clicking for faster form building
4. **Check console logs** to see what's happening during drag-and-drop

---

**Time to Implement**: 5-10 minutes
**Difficulty**: Easy
**Result**: Professional drag-and-drop form builder!

