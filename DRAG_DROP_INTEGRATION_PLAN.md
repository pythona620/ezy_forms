# Drag-and-Drop Field Library Integration Plan

## 🎯 Goal
Integrate the modern drag-and-drop field library (similar to Frappe DocType creation) into the FormStepper.vue form builder for a better user experience.

**Date**: November 11, 2025
**Status**: Ready for Implementation

---

## 📊 Current State

### Existing Components (Already Created)
✅ **Field Library Components** - Located in `src/Components/FormBuilder/FieldLibrary/`:
1. `FieldLibraryPanel.vue` - Main container with search functionality
2. `FieldCard.vue` - Draggable field cards
3. `FieldCategory.vue` - Collapsible category groups
4. `fieldTypes.js` - 27 field types in 6 categories
5. `DropZone.vue` - Visual drop indicators

✅ **UI Components** - Located in `src/Components/UI/`:
1. `PrimaryButton.vue`, `SecondaryButton.vue`, `IconButton.vue`
2. `TextInput.vue`
3. `Card.vue`

✅ **Design System** - `src/Styles/design-tokens.scss`:
- Complete color palette
- Typography scales
- Spacing system
- Animations

### Current Form Builder
📄 **File**: `src/Pages/Formscreator/FormStepper.vue` (202KB, 5000+ lines)

**Current Approach**:
- Click "Add Field" button → Opens modal/dropdown
- Manual field configuration
- No visual drag-and-drop
- Traditional form builder interface

---

## 🎨 Proposed Design

### Layout Structure

```
┌─────────────────────────────────────────────────────────────┐
│                    Form Header (Back, Save)                  │
├──────────┬─────────────────────────────────────────────────┤
│  Steps   │               Form Content Area                  │
│          │                                                   │
│  1. About│  ┌─────────────────────────┬─────────────────┐  │
│  2. Fields│  │  Field Library Panel    │  Form Canvas    │  │
│  3. Work  │  │  ┌─────────────────┐  │  ┌────────────┐ │  │
│     flow  │  │  │  🔍 Search       │  │  │ Requestor  │ │  │
│           │  │  │  ──────────────  │  │  │  Block     │ │  │
│           │  │  │                  │  │  │            │ │  │
│           │  │  │ 📋 Basic Fields  │  │  │ [Field 1]  │ │  │
│           │  │  │   • Text         │  │  │ [Field 2]  │ │  │
│           │  │  │   • Number       │  │  │            │ │  │
│           │  │  │   • Date         │  │  │ + Drop     │ │  │
│           │  │  │                  │  │  │   Zone     │ │  │
│           │  │  │ ✓ Choice Fields  │  │  └────────────┘ │  │
│           │  │  │   • Select       │  │                 │  │
│           │  │  │   • Checkbox     │  │  ┌────────────┐ │  │
│           │  │  │                  │  │  │ Approver   │ │  │
│           │  │  │ 📅 Date & Time   │  │  │  Block 1   │ │  │
│           │  │  │   • Date         │  │  └────────────┘ │  │
│           │  │  │   • DateTime     │  │                 │  │
│           │  │  │                  │  │                 │  │
│           │  │  └─────────────────┘  └─────────────────┘  │
└──────────┴──────────────────────────────────────────────────┘
```

### Key Features

1. **Field Library Panel** (Left Side):
   - Collapsible sidebar
   - Search functionality (Ctrl+K shortcut)
   - Categorized field types
   - Draggable field cards

2. **Form Canvas** (Right Side):
   - Visual drop zones between fields
   - Drag-and-drop field reordering
   - Block-level organization (Requestor, Approver blocks)
   - Inline field editing

3. **Interactions**:
   - Drag field from library → Drop in canvas
   - Drag field in canvas → Reorder fields
   - Click field → Edit properties in sidebar/modal
   - Hover → Show field controls (edit, duplicate, delete)

---

## 🔧 Implementation Steps

### Phase 1: Basic Integration (2-3 hours)

#### Step 1.1: Import Field Library Components (30 min)

**File**: `FormStepper.vue`

Add imports at the top of the script section:

```vue
<script setup>
import { ref, reactive, computed, onMounted, nextTick, watch } from "vue";

// Existing imports...
// ...

// NEW: Import Field Library Components
import FieldLibraryPanel from "@/Components/FormBuilder/FieldLibrary/FieldLibraryPanel.vue";
import DropZone from "@/Components/FormBuilder/Canvas/DropZone.vue";
import { FIELD_TYPES, FIELD_CATEGORIES, searchFieldTypes, getFieldsByCategory } from "@/Components/FormBuilder/FieldLibrary/fieldTypes.js";

// Rest of existing code...
</script>
```

#### Step 1.2: Add Field Library Panel to Layout (1 hour)

**Location**: Inside `activeStep === 2` section (around line 321)

Replace or enhance the existing form fields section:

```vue
<div v-if="activeStep === 2">
  <!-- Existing header -->
  <div class="stepperbackground ps-2 pe-2 m-0 d-flex justify-content-between align-items-center">
    <!-- ... existing header code ... -->
  </div>

  <!-- NEW: Field Library Layout -->
  <div class="form-builder-layout">
    <div class="form-builder-container">
      <!-- Field Library Panel (Left Side) -->
      <div class="field-library-sidebar">
        <FieldLibraryPanel
          :collapsible="true"
          @field-add="handleFieldAdd"
          @field-dragstart="handleFieldDragStart"
        />
      </div>

      <!-- Form Canvas (Right Side) -->
      <div class="form-canvas-area">
        <!-- Existing block-level code -->
        <div class="main-block" ref="mainBlockRef">
          <div class="block-level" v-for="(block, blockIndex) in blockArr" :key="blockIndex">
            <!-- ... existing block code ... -->

            <!-- Add drop zones between fields -->
            <DropZone
              v-if="!block.fields || block.fields.length === 0"
              text="Drop field here or click + to add"
              @drop="handleDrop(blockIndex, 0)"
            />

            <!-- Existing fields with drop zones -->
            <template v-for="(field, fieldIndex) in block.fields" :key="fieldIndex">
              <DropZone
                variant="between"
                @drop="handleDrop(blockIndex, fieldIndex)"
              />

              <!-- Existing field render -->
              <div class="field-item">
                <!-- ... existing field code ... -->
              </div>
            </template>

            <!-- Drop zone at end -->
            <DropZone
              variant="bottom"
              @drop="handleDrop(blockIndex, block.fields.length)"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
```

#### Step 1.3: Add Drag-and-Drop Event Handlers (1 hour)

Add these functions in the script section:

```javascript
// Field Library Event Handlers
const handleFieldAdd = (fieldType) => {
  // Handle direct add (click) from field library
  const currentBlock = blockArr.value[selectedBlockIndex.value] || blockArr.value[0];
  const newField = createFieldFromType(fieldType);

  // Add to current block
  if (!currentBlock.fields) {
    currentBlock.fields = [];
  }
  currentBlock.fields.push(newField);
};

const handleFieldDragStart = (fieldType) => {
  // Store field type being dragged
  draggedFieldType.value = fieldType;
};

const handleDrop = (blockIndex, position) => {
  if (!draggedFieldType.value) return;

  const block = blockArr.value[blockIndex];
  const newField = createFieldFromType(draggedFieldType.value);

  // Insert at position
  if (!block.fields) {
    block.fields = [];
  }
  block.fields.splice(position, 0, newField);

  // Clear dragged field
  draggedFieldType.value = null;
};

const createFieldFromType = (fieldType) => {
  const fieldDefinition = FIELD_TYPES[fieldType];

  return {
    id: generateUniqueId(),
    type: fieldType,
    label: fieldDefinition.name,
    fieldname: generateFieldName(fieldDefinition.name),
    ...fieldDefinition.defaultProps,
    // Add other properties as needed
  };
};

const generateFieldName = (label) => {
  return label.toLowerCase().replace(/\s+/g, '_').replace(/[^a-z0-9_]/g, '');
};

const generateUniqueId = () => {
  return `field_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
};
```

#### Step 1.4: Add Styles (30 min)

Add to the `<style>` section:

```scss
<style scoped lang="scss">
// Existing styles...

// NEW: Form Builder Layout
.form-builder-layout {
  background: var(--color-neutral-50, #f9fafb);
  min-height: calc(100vh - 200px);
}

.form-builder-container {
  display: flex;
  gap: var(--space-4, 1rem);
  padding: var(--space-4, 1rem);
  max-width: 100%;
  margin: 0 auto;
}

.field-library-sidebar {
  width: 320px;
  flex-shrink: 0;
  position: sticky;
  top: var(--space-4, 1rem);
  height: fit-content;
  max-height: calc(100vh - 250px);
  overflow-y: auto;

  @media (max-width: 992px) {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    z-index: 1000;
    width: 280px;
    transform: translateX(-100%);
    transition: transform 0.3s ease;

    &.show {
      transform: translateX(0);
    }
  }
}

.form-canvas-area {
  flex: 1;
  min-width: 0;
  background: white;
  border-radius: var(--radius-lg, 12px);
  padding: var(--space-6, 1.5rem);
  box-shadow: var(--shadow-sm, 0 1px 3px rgba(0,0,0,0.1));
}

.field-item {
  position: relative;
  padding: var(--space-4, 1rem);
  border: 1px solid var(--color-neutral-200, #e5e7eb);
  border-radius: var(--radius-md, 8px);
  margin-bottom: var(--space-3, 0.75rem);
  background: white;
  transition: all 0.2s ease;

  &:hover {
    border-color: var(--color-primary-300, #93c5fd);
    box-shadow: var(--shadow-md, 0 4px 6px rgba(0,0,0,0.1));
  }
}

// Mobile toggle button
.field-library-toggle {
  display: none;
  position: fixed;
  bottom: var(--space-4, 1rem);
  left: var(--space-4, 1rem);
  z-index: 999;

  @media (max-width: 992px) {
    display: block;
  }
}
</style>
```

---

### Phase 2: Enhanced Features (3-4 hours)

#### Step 2.1: Field Reordering within Canvas (1.5 hours)

Add drag-and-drop for existing fields:

```vue
<div
  class="field-item"
  draggable="true"
  @dragstart="handleFieldItemDragStart(blockIndex, fieldIndex)"
  @dragover.prevent
  @drop="handleFieldItemDrop(blockIndex, fieldIndex)"
>
  <!-- field content -->
</div>
```

```javascript
const handleFieldItemDragStart = (blockIndex, fieldIndex) => {
  draggedField.value = { blockIndex, fieldIndex };
};

const handleFieldItemDrop = (targetBlockIndex, targetFieldIndex) => {
  if (!draggedField.value) return;

  const { blockIndex: sourceBlockIndex, fieldIndex: sourceFieldIndex } = draggedField.value;

  // Get source field
  const sourceBlock = blockArr.value[sourceBlockIndex];
  const field = sourceBlock.fields[sourceFieldIndex];

  // Remove from source
  sourceBlock.fields.splice(sourceFieldIndex, 1);

  // Add to target
  const targetBlock = blockArr.value[targetBlockIndex];
  targetBlock.fields.splice(targetFieldIndex, 0, field);

  draggedField.value = null;
};
```

#### Step 2.2: Field Properties Sidebar (1.5 hours)

Create a properties panel for editing field properties:

```vue
<div class="field-properties-sidebar" v-if="selectedField">
  <div class="properties-header">
    <h3>Field Properties</h3>
    <IconButton icon="bi bi-x" @click="selectedField = null" />
  </div>

  <div class="properties-content">
    <!-- Label -->
    <TextInput
      v-model="selectedField.label"
      label="Label"
      placeholder="Field Label"
    />

    <!-- Field Name -->
    <TextInput
      v-model="selectedField.fieldname"
      label="Field Name"
      placeholder="field_name"
      help-text="Unique identifier (no spaces)"
    />

    <!-- Required -->
    <div class="form-check">
      <input
        type="checkbox"
        v-model="selectedField.required"
        class="form-check-input"
        id="field-required"
      />
      <label for="field-required">Required Field</label>
    </div>

    <!-- Field-type specific properties -->
    <component
      :is="getFieldPropertiesComponent(selectedField.type)"
      v-model="selectedField"
    />
  </div>
</div>
```

#### Step 2.3: Field Controls (1 hour)

Add hover controls to fields:

```vue
<div class="field-item">
  <div class="field-controls">
    <IconButton
      icon="bi bi-pencil"
      size="sm"
      @click="editField(field)"
      aria-label="Edit field"
    />
    <IconButton
      icon="bi bi-files"
      size="sm"
      @click="duplicateField(blockIndex, fieldIndex)"
      aria-label="Duplicate field"
    />
    <IconButton
      icon="bi bi-trash"
      size="sm"
      variant="error"
      @click="deleteField(blockIndex, fieldIndex)"
      aria-label="Delete field"
    />
    <IconButton
      icon="bi bi-grip-vertical"
      size="sm"
      class="drag-handle"
      aria-label="Drag to reorder"
    />
  </div>

  <!-- Field content -->
  <div class="field-content">
    <!-- ... -->
  </div>
</div>
```

```scss
.field-controls {
  position: absolute;
  top: var(--space-2, 0.5rem);
  right: var(--space-2, 0.5rem);
  display: flex;
  gap: var(--space-1, 0.25rem);
  opacity: 0;
  transition: opacity 0.2s ease;
}

.field-item:hover .field-controls {
  opacity: 1;
}
```

---

### Phase 3: Polish & Testing (2-3 hours)

#### Step 3.1: Mobile Responsiveness

- Collapsible field library (drawer on mobile)
- Touch-friendly drag-and-drop
- Responsive grid layouts

#### Step 3.2: Keyboard Shortcuts

```javascript
onMounted(() => {
  document.addEventListener('keydown', handleKeyboardShortcuts);
});

const handleKeyboardShortcuts = (e) => {
  // Ctrl+K: Open field search
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    focusFieldSearch();
  }

  // Delete: Remove selected field
  if (e.key === 'Delete' && selectedField.value) {
    deleteField(selectedField.value.blockIndex, selectedField.value.fieldIndex);
  }

  // Ctrl+D: Duplicate selected field
  if ((e.ctrlKey || e.metaKey) && e.key === 'd' && selectedField.value) {
    e.preventDefault();
    duplicateField(selectedField.value.blockIndex, selectedField.value.fieldIndex);
  }
};
```

#### Step 3.3: Visual Feedback

- Drag preview/ghost
- Drop zone highlighting
- Field selection indicators
- Loading states

---

## 📦 File Structure

```
ezyformsfrontend/src/
├── Components/
│   ├── FormBuilder/           ✅ Already exists
│   │   ├── Canvas/
│   │   │   └── DropZone.vue  ✅
│   │   └── FieldLibrary/
│   │       ├── FieldCard.vue          ✅
│   │       ├── FieldCategory.vue      ✅
│   │       ├── FieldLibraryPanel.vue  ✅
│   │       └── fieldTypes.js          ✅
│   └── UI/                    ✅ Already exists
│       ├── Button/
│       │   ├── PrimaryButton.vue     ✅
│       │   ├── SecondaryButton.vue   ✅
│       │   └── IconButton.vue        ✅
│       ├── Input/
│       │   └── TextInput.vue         ✅
│       └── Card/
│           └── Card.vue              ✅
├── Pages/
│   └── Formscreator/
│       └── FormStepper.vue           ⚠️ Needs integration
├── Styles/
│   └── design-tokens.scss            ✅ Already exists
└── Composables/                      ✅ Already exists
    ├── useFormBuilder.js             ✅
    ├── useUndoRedo.js                ✅
    └── useAutoSave.js                ✅
```

---

## 🔄 Migration Strategy

### Option 1: Side-by-Side (Recommended)

- Keep existing "Add Field" button
- Add new drag-and-drop library alongside
- Users can choose which method to use
- Gradually phase out old method

### Option 2: Toggle Feature

- Add feature flag: `USE_NEW_FIELD_LIBRARY`
- Allow users to switch between old and new
- Gather feedback before full rollout

### Option 3: Full Replacement

- Replace all "Add Field" buttons with drag-and-drop
- Immediate switch (higher risk)
- Better UX but requires thorough testing

**Recommended**: Option 1 (Side-by-Side)

---

## ✅ Testing Checklist

### Functional Testing
- [ ] Drag field from library to canvas
- [ ] Drop field at correct position
- [ ] Field properties are preserved
- [ ] Reorder fields within canvas
- [ ] Edit field properties
- [ ] Duplicate field
- [ ] Delete field
- [ ] Search fields in library
- [ ] Collapse/expand field library
- [ ] Undo/redo functionality
- [ ] Auto-save after changes

### Browser Testing
- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Mobile Safari (iOS)
- [ ] Chrome Mobile (Android)

### Responsive Testing
- [ ] Desktop (1920x1080)
- [ ] Laptop (1366x768)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)

### Performance Testing
- [ ] Smooth dragging with 100+ fields
- [ ] No lag during field operations
- [ ] Fast search/filter results
- [ ] Memory usage acceptable

---

## 📈 Success Metrics

### User Experience
- **Time to add field**: < 3 seconds (vs current ~10 seconds)
- **Learning curve**: Users can add field without training
- **Error rate**: < 5% failed field additions
- **User satisfaction**: > 4/5 rating

### Technical Metrics
- **Bundle size**: < +50KB added
- **Initial load**: < +200ms
- **Drag operation**: < 16ms (60fps)
- **Search results**: < 100ms

---

## 🚀 Deployment Plan

### Phase 1: Development (1 week)
1. Integrate FieldLibraryPanel into FormStepper
2. Implement basic drag-and-drop
3. Add field controls
4. Internal testing

### Phase 2: Beta Testing (1 week)
1. Deploy to staging environment
2. Enable for beta users
3. Gather feedback
4. Fix bugs

### Phase 3: Production (3 days)
1. Full rollout
2. Monitor performance
3. User support
4. Documentation update

---

## 📚 Documentation Needed

1. **User Guide**: How to use drag-and-drop field library
2. **Developer Guide**: How to extend field types
3. **API Reference**: Field type definitions
4. **Video Tutorial**: Screen recording of form creation
5. **Migration Guide**: Transitioning from old to new

---

## 🎯 Next Steps

1. **Review this plan** with the team
2. **Prioritize phases** based on timeline
3. **Start with Phase 1** (Basic Integration)
4. **Test thoroughly** before moving to Phase 2
5. **Gather feedback** continuously

---

**Created**: November 11, 2025
**Status**: Ready for Implementation
**Estimated Time**: 7-10 hours for full implementation
**Priority**: High - Improves UX significantly

