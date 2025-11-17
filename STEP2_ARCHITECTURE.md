# Step 2 Frappe Interface - Technical Architecture

## 📚 Overview

This document explains the technical implementation of the new Frappe v15-style form builder interface for Step 2, including the adapter pattern used to bridge between the simple UI and complex backend structure.

---

## 🏗️ Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         FRAPPE UI LAYER                              │
│  ┌──────────────┐  ┌──────────────┐  ┌─────────────────────────┐   │
│  │   Field      │  │   Canvas     │  │   Properties Panel      │   │
│  │   Library    │  │   (Flat      │  │   (Edit Selected Field) │   │
│  │   (37 types) │  │   Field      │  │                         │   │
│  └──────────────┘  └──────────────┘  └─────────────────────────┘   │
│          │                 │                      │                  │
│          └─────────────────┴──────────────────────┘                  │
│                              │                                       │
└──────────────────────────────┼───────────────────────────────────────┘
                               │
                    ┌──────────▼──────────┐
                    │  ADAPTER FUNCTIONS  │
                    │  (Data Conversion)  │
                    └──────────┬──────────┘
                               │
┌──────────────────────────────▼───────────────────────────────────────┐
│                    COMPLEX BACKEND STRUCTURE                         │
│                                                                      │
│  blockArr[blockIndex] = {                                           │
│    sections: [{                                                     │
│      rows: [{                                                       │
│        columns: [{                                                  │
│          fields: [{ label, fieldtype, options, reqd, ... }]        │
│        }]                                                           │
│      }]                                                             │
│    }]                                                               │
│  }                                                                  │
│                                                                      │
│  extractFieldsWithBreaks(blockArr) → Flat Array for Backend Save   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 🔄 Data Flow

### 1. **Loading Existing Form**

```
Backend Response (JSON)
  ↓
rebuildToStructuredArray() [from field_format.js]
  ↓
blockArr[].sections[].rows[].columns[].fields[]
  ↓
extractFieldsFromBlock() [Adapter]
  ↓
Flat Fields Array → Displayed in Frappe UI Canvas
```

### 2. **Adding New Field**

```
User Clicks Field Type in Library
  ↓
addFieldToCanvas(fieldType)
  ↓
Create New Field Object {label, fieldtype, ...}
  ↓
addFieldToBlock() [Adapter]
  ↓
blockArr[0].sections[0].rows[0].columns[0].fields.push(newField)
  ↓
Force Reactivity: blockArr.splice()
  ↓
extractFieldsFromBlock() → Display Updated List
```

### 3. **Editing Field Properties**

```
User Changes Property (e.g., label, type, options)
  ↓
updateField() Called on @input/@change
  ↓
getSelectedField() → Get Current UI State
  ↓
updateFieldInBlock(block, index, updatedField) [Adapter]
  ↓
Traverse sections/rows/columns, update field in-place
  ↓
blockArr.splice() → Force Reactivity
  ↓
UI Re-renders with Updated Field
```

### 4. **Deleting Field**

```
User Clicks Delete Button
  ↓
deleteField(index)
  ↓
deleteFieldFromBlock(block, index) [Adapter]
  ↓
Traverse structure, splice field from array
  ↓
blockArr.splice() → Force Reactivity
  ↓
extractFieldsFromBlock() → Display Updated List
```

### 5. **Saving Form**

```
User Clicks Save
  ↓
saveFormData()
  ↓
extractFieldsWithBreaks(blockArr) [from field_format.js]
  ↓
Flat Array with Column/Row/Section/Block Breaks
  ↓
POST to Backend API /method/ezy_forms.api.v1.add_dynamic_doctype
  ↓
Backend Saves to Ezy Form Definitions DocType
```

---

## 🛠️ Key Components

### File: `FormStepper.vue`

#### **Reactive State Variables**

```javascript
// Block navigation
const currentBuilderTab = ref(0);        // Which block tab is active (0=Requestor, 1=Approver1, etc.)

// Field selection
const selectedFieldIndex = ref(null);    // Index of selected field in flat array
const draggedFieldIndex = ref(null);     // Index of field being dragged

// Field library visibility
const showFieldLibrary = ref(true);      // Toggle left panel

// Complex backend structure
let blockArr = reactive([]);             // Main data structure
```

#### **Adapter Functions** (Lines 3167-3303)

##### 1. **extractFieldsFromBlock(block)**
- **Purpose:** Convert complex nested structure to flat array for UI display
- **Input:** Block object with sections/rows/columns/fields
- **Output:** Flat array of field objects
- **Algorithm:**
  ```javascript
  for each section in block.sections:
    for each row in section.rows:
      for each column in row.columns:
        for each field in column.fields:
          flatArray.push(field)
  return flatArray
  ```

##### 2. **addFieldToBlock(block, field)**
- **Purpose:** Add new field to complex structure
- **Strategy:** Always adds to first section, first row, first column
- **Why:** Simplest consistent approach; backend doesn't care about layout
- **Creates structure if missing:**
  ```javascript
  if (!block.sections[0]) create section
  if (!block.sections[0].rows[0]) create row
  if (!block.sections[0].rows[0].columns[0]) create column
  ```

##### 3. **updateFieldInBlock(block, flatIndex, updatedField)**
- **Purpose:** Update field properties in complex structure
- **Algorithm:**
  ```javascript
  currentIndex = 0
  for each section/row/column:
    for each field in column.fields:
      if currentIndex === flatIndex:
        Object.assign(field, updatedField)  // Update in-place
        return true
      currentIndex++
  ```

##### 4. **deleteFieldFromBlock(block, flatIndex)**
- **Purpose:** Remove field from complex structure
- **Algorithm:**
  ```javascript
  currentIndex = 0
  for each section/row/column:
    if flatIndex is in current column:
      localIndex = flatIndex - currentIndex
      column.fields.splice(localIndex, 1)
      return true
    currentIndex += column.fields.length
  ```

##### 5. **reorderFieldsInBlock(block, fromIndex, toIndex)**
- **Purpose:** Drag-drop reordering of fields
- **Strategy:** Extract all fields, reorder, clear structure, re-add all
- **Algorithm:**
  ```javascript
  allFields = extractFieldsFromBlock(block)
  [movedField] = allFields.splice(fromIndex, 1)
  allFields.splice(toIndex, 0, movedField)

  // Clear all fields
  for each section/row/column:
    column.fields = []

  // Re-add in new order
  for each field in allFields:
    addToFirstColumn(field)
  ```

---

## 🎨 UI Helper Functions (Lines 3305-3502)

### **fieldCategories** (Computed)
```javascript
// Extracts unique categories from fieldTypes array
const fieldCategories = computed(() => {
  return [...new Set(fieldTypes.map(ft => ft.category))];
});
// Result: ["Basic", "Number", "Selection", "DateTime", "Media", "Special", "Table", "Layout"]
```

### **getFieldsByCategory(category)**
```javascript
// Filters field types by category for left panel display
return fieldTypes.filter(ft => ft.category === category);
```

### **getFieldIcon(fieldtype)**
```javascript
// Returns Bootstrap icon class for field type
const field = fieldTypes.find(ft => ft.type === fieldtype);
return field?.icon || 'bi-file-text';
// Example: "Data" → "bi-input-cursor-text"
```

### **getCurrentBlockFields()**
```javascript
// Gets flat array of fields for currently active block
const block = blockArr[currentBuilderTab.value];
return extractFieldsFromBlock(block);
```

### **getSelectedField()**
```javascript
// Gets the currently selected field object
const fields = getCurrentBlockFields();
return fields[selectedFieldIndex.value] || {};
```

---

## 🔧 Field Operations

### **addFieldToCanvas(fieldType)**
```javascript
1. Create new field object with defaults
2. Call addFieldToBlock(currentBlock, newField) [Adapter]
3. Force reactivity: blockArr.splice(currentBuilderTab.value, 1, {...currentBlock})
4. Auto-select: selectedFieldIndex.value = allFields.length - 1
5. Show success toast
```

### **updateField()**
```javascript
1. Get selected field from UI state
2. Call updateFieldInBlock(block, selectedFieldIndex, updatedField) [Adapter]
3. Force reactivity: blockArr.splice()
```

### **duplicateField(index)**
```javascript
1. Extract all fields from block
2. Clone field at index
3. Modify label: "Field (Copy)" and fieldname: "field_copy_[timestamp]"
4. Call addFieldToBlock(currentBlock, duplicatedField) [Adapter]
5. Force reactivity
6. Select duplicated field
```

### **deleteField(index)**
```javascript
1. Adjust selectedFieldIndex if needed
2. Call deleteFieldFromBlock(block, index) [Adapter]
3. Force reactivity
4. Show success toast
```

### **Drag-Drop Reorder**
```javascript
@dragstart: draggedFieldIndex.value = index
@dragover.prevent: Allow drop
@drop:
  1. Call reorderFieldsInBlock(block, dragIndex, dropIndex) [Adapter]
  2. Force reactivity
  3. Update selectedFieldIndex if dragging selected field
  4. Clear draggedFieldIndex
```

---

## 📋 Field Types Array (37 Types)

Located at lines 3890-4197:

```javascript
const fieldTypes = [
  { label: "Data", type: "Data", icon: "bi-input-cursor-text", category: "Basic", description: "Single line text input" },
  { label: "Select", type: "Select", icon: "bi-menu-button-wide", category: "Selection", description: "Dropdown selection" },
  // ... 35 more types
];
```

**Categories:**
- Basic (4): Data, Small Text, Text Editor, Code
- Number (4): Int, Float, Currency, Percent
- Selection (6): Check, Select, Table MultiSelect, Link, Dynamic Link, Rating
- DateTime (4): Date, Datetime, Time, Duration
- Media (4): Attach, Attach Image, Image, Signature
- Special (7): Password, Color, Barcode, Geolocation, HTML, JSON, Read Only
- Table (1): Table
- Layout (4): Column Break, Section Break, Heading, Button

---

## 💾 Backend Integration

### **Save Function Flow**

```javascript
// FormStepper.vue:4107
function formData(status) {
  // 1. Extract flat fields with breaks
  let fields = extractFieldsWithBreaks(blockArr);  // From field_format.js

  // 2. Prepare data object
  const dataObj = {
    ...filterObj.value,              // Step 1 form metadata
    fields,                          // Flat fields array
    doctype: 'Ezy Form Definitions',
    workflow_setup: workflowSetup,   // From Step 3
    form_status: status === "save" ? "Created" : "Draft"
  };

  // 3. Send to backend
  axiosInstance.post(apis.savedata, dataObj)
    .then(res => {
      // Handle success
      paramId.value = res.message.message;
      router.push({ params: { paramid: paramId.value } });
    });
}
```

### **extractFieldsWithBreaks() Algorithm**

From `field_format.js:2-185`:

```javascript
function extractFieldsWithBreaks(blockArr) {
  const result = [];
  let index = 0;

  for each block:
    for each section:
      for each row:
        for each column:
          for each field:
            // Add actual field
            result.push({
              fieldname: convertLabelToFieldName(field.label),
              fieldtype: field.fieldtype,
              label: field.label,
              reqd: field.reqd ? 1 : 0,
              options: cleanedOptions,
              idx: index++
            });

          // Add Column Break marker
          result.push({
            fieldtype: "Column Break",
            fieldname: convertLabelToFieldName(column.label),
            idx: index++
          });

        // Add Row Break marker (stored as Column Break with description)
        result.push({
          fieldtype: "Column Break",
          description: "Row Break",
          idx: index++
        });

      // Add Section Break marker
      result.push({
        fieldtype: "Section Break",
        fieldname: convertLabelToFieldName(section.label),
        idx: index++
      });

    // Add Block Break marker (stored as Section Break with description)
    result.push({
      fieldtype: "Section Break",
      description: "Block Break",
      idx: index++
    });

  return result;
}
```

---

## 🎯 Vue Reactivity Pattern

### **Why blockArr.splice()?**

Vue 3's reactivity system tracks object/array mutations, but sometimes needs explicit updates:

```javascript
// ❌ This doesn't trigger re-render reliably
currentBlock.sections[0].rows[0].columns[0].fields.push(newField);

// ✅ This forces Vue to detect the change
blockArr.splice(currentBuilderTab.value, 1, {...currentBlock});
```

**How it works:**
1. `splice(index, 1, newValue)` replaces the item at index
2. Spreading `{...currentBlock}` creates a new object reference
3. Vue detects the reference change and re-renders components

---

## 🔍 Template Bindings

### **Field Library (Left Panel)**

```vue
<div v-for="category in fieldCategories" :key="category">
  <div class="category-title">{{ category }}</div>
  <div v-for="field in getFieldsByCategory(category)"
       :key="field.type"
       @click="addFieldToCanvas(field)">
    <i :class="field.icon"></i>
    <div>{{ field.label }}</div>
  </div>
</div>
```

### **Field Canvas (Center Panel)**

```vue
<div v-for="(field, index) in getCurrentBlockFields()"
     :key="'field-' + index"
     :class="{ 'selected': selectedFieldIndex === index }"
     @click="selectField(index)"
     draggable="true"
     @dragstart="onFieldDragStart(index)"
     @drop="onFieldDrop(index)">

  <div class="field-label">
    {{ field.label || 'Unnamed Field' }}
    <span v-if="field.reqd">*</span>
  </div>

  <button @click.stop="duplicateField(index)">Duplicate</button>
  <button @click.stop="deleteField(index)">Delete</button>
</div>
```

### **Properties Panel (Right Panel)**

```vue
<div v-if="selectedFieldIndex !== null">
  <!-- Label -->
  <input v-model="getSelectedField().label" @input="updateField">

  <!-- Field Type -->
  <select v-model="getSelectedField().fieldtype" @change="onFieldTypeChange">
    <option v-for="ft in fieldTypes" :value="ft.type">
      {{ ft.label }}
    </option>
  </select>

  <!-- Mandatory -->
  <input type="checkbox"
         v-model="getSelectedField().reqd"
         :true-value="1"
         :false-value="0"
         @change="updateField">
</div>
```

---

## 🚀 Performance Considerations

### **Optimizations Applied:**

1. **Computed Properties:**
   - `fieldCategories` only recalculates when `fieldTypes` changes
   - Cached category list for left panel rendering

2. **Event Delegation:**
   - Using `@click.stop` to prevent event bubbling
   - Prevents unnecessary parent re-renders

3. **Lazy Rendering:**
   - Only active block's fields are rendered
   - Inactive blocks are hidden with `v-show`

4. **Shallow Cloning:**
   - Using spread operator `{...currentBlock}` instead of deep clone
   - Faster for large structures

---

## 🐛 Debugging Tips

### **Vue DevTools Inspection:**

1. Open Vue DevTools
2. Navigate to Components → FormStepper
3. Check reactive data:
   ```
   blockArr: Array[1-10] ← Current blocks
     [0]: Object
       sections: Array[1] ← Nested structure
         [0]: Object
           rows: Array[1]
             [0]: Object
               columns: Array[1]
                 [0]: Object
                   fields: Array[N] ← Actual fields

   selectedFieldIndex: 2 ← Currently selected field
   currentBuilderTab: 0 ← Active block
   ```

### **Console Logging:**

```javascript
// Add to adapter functions for debugging
console.log('extractFieldsFromBlock:', {
  block,
  extractedFields: fields,
  count: fields.length
});

console.log('updateFieldInBlock:', {
  flatIndex,
  updatedField,
  success: updateFieldInBlock(block, flatIndex, updatedField)
});
```

---

## ✅ Testing Checklist

See `STEP2_TESTING_GUIDE.md` for complete testing procedures.

**Quick Smoke Test:**
1. Add 3 fields (Data, Select, Date)
2. Edit properties of Select field (add options)
3. Duplicate Data field
4. Drag Date field to top
5. Delete one field
6. Save form
7. Reload and verify all changes persisted

---

## 📝 Future Enhancements

**Potential improvements:**

1. **Performance:**
   - Virtualize field list for 100+ fields
   - Debounce updateField() calls
   - Memoize extractFieldsFromBlock()

2. **UX:**
   - Undo/Redo functionality
   - Keyboard shortcuts (Del to delete, Ctrl+D to duplicate)
   - Multi-select fields for batch operations
   - Field search/filter in library

3. **Features:**
   - Import fields from another form
   - Export field template
   - Field validation preview
   - Conditional field visibility rules

---

## 📚 Related Files

| File | Purpose |
|------|---------|
| `FormStepper.vue` | Main form builder component |
| `field_format.js` | Conversion utilities (extractFieldsWithBreaks, rebuildToStructuredArray) |
| `apiurls.js` | API endpoint definitions |
| `api_req_data.js` | Axios request wrappers |
| `CLAUDE.md` | Project documentation |
| `STEP2_TESTING_GUIDE.md` | Complete testing procedures |

---

**Architecture Version:** 2.0 (Frappe v15 Interface)
**Last Updated:** {{ current_date }}
**Author:** Claude Code AI Assistant
