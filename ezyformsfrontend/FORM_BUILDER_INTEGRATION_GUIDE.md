# Frappe Form Builder Integration Guide

## Overview

A complete Frappe-compatible form builder has been integrated into your EzyForms project. This allows you to create dynamic forms with all Frappe field types, validations, and drag-and-drop ordering.

## Files Created

### Frontend Components

1. **`src/Components/FrappeFormBuilder.vue`**
   - Main form builder component
   - Handles field list, drag-and-drop, save/load operations
   - Can be used standalone or integrated into existing components

2. **`src/Components/FieldConfigurator.vue`**
   - Field configuration editor
   - All Frappe field properties and validations
   - Used by FrappeFormBuilder

### Backend API

3. **`ezy_forms/api/v1/form_builder.py`**
   - Complete backend API for form builder
   - Methods:
     - `get_field_types()` - Fetch all available field types
     - `save_form_definition()` - Save form schema
     - `get_form_definition()` - Load existing form
     - `get_docfield_meta()` - Get DocField structure
     - `validate_fieldname()` - Validate field names
     - `get_link_options()` - Get DocTypes for Link fields
     - `get_child_table_options()` - Get child tables

### Configuration

4. **`src/shared/apiurls.js`**
   - Added form builder API endpoints

## Usage

### Option 1: Standalone Component

Use the form builder as a separate page or component:

```vue
<template>
  <div class="page-container">
    <h2>Create Custom Form</h2>
    <FrappeFormBuilder
      ref="formBuilderRef"
      :formName="currentFormName"
      @save="handleFormSave"
      @update="handleFormUpdate"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import FrappeFormBuilder from '@/Components/FrappeFormBuilder.vue';

const formBuilderRef = ref(null);
const currentFormName = ref('My Custom Form');

const handleFormSave = (fields) => {
  console.log('Form saved with fields:', fields);
  // Additional logic after save
};

const handleFormUpdate = (fields) => {
  console.log('Form updated:', fields);
  // Real-time update handling
};
</script>
```

### Option 2: Integration into FormStepper.vue

Add the form builder as a new step in your existing FormStepper:

```vue
<!-- In FormStepper.vue -->
<template>
  <!-- Existing steps -->

  <!-- Add new step for Advanced Form Builder -->
  <div v-if="activeStep === 3">
    <div class="stepperbackground">
      <h1 class="font-14 fw-bold">Advanced Field Designer</h1>
    </div>

    <FrappeFormBuilder
      ref="formBuilderRef"
      :formName="formNameModel"
      :existingFields="existingFormFields"
      @save="handleAdvancedFormSave"
      @update="syncFormFields"
    />
  </div>
</template>

<script setup>
import FrappeFormBuilder from '@/Components/FrappeFormBuilder.vue';

const formBuilderRef = ref(null);
const existingFormFields = ref([]);

const handleAdvancedFormSave = (fields) => {
  // Merge with existing form data
  existingFormFields.value = fields;
  // Continue with your existing save logic
};

const syncFormFields = (fields) => {
  // Keep form fields in sync
  existingFormFields.value = fields;
};
</script>
```

### Option 3: Programmatic Usage

Access form builder methods programmatically:

```vue
<script setup>
import { ref } from 'vue';
import FrappeFormBuilder from '@/Components/FrappeFormBuilder.vue';

const formBuilderRef = ref(null);

// Add a field programmatically
const addCustomField = () => {
  formBuilderRef.value.addNewField();
};

// Get all fields
const getAllFields = () => {
  const fields = formBuilderRef.value.getFields();
  console.log('Current fields:', fields);
  return fields;
};

// Trigger save
const saveForm = async () => {
  await formBuilderRef.value.saveFormSchema();
};
</script>
```

## Features

### 1. All Frappe Field Types

The form builder supports all standard Frappe field types:

- **Text Fields**: Data, Small Text, Long Text, Text Editor
- **Numeric**: Int, Float, Currency, Percent
- **Date/Time**: Date, Datetime, Time, Duration
- **Selection**: Select, Link, Dynamic Link, Autocomplete
- **Tables**: Table, Table MultiSelect
- **Media**: Image, Attach, Attach Image, Signature
- **Layout**: Section Break, Column Break, Tab Break, Heading
- **Special**: Check, Color, Barcode, Geolocation, Rating, JSON, Phone, Button, Icon, Code, HTML

### 2. Field Properties & Validations

Each field can be configured with:

**Basic Properties:**
- Fieldname (auto-generated from label)
- Label
- Field Type
- Description
- Default Value

**Validation Options:**
- Mandatory (required)
- Unique
- Read Only
- Hidden
- Length (for text fields)
- Precision (for numeric fields)
- Non-negative (for numbers)

**Display Options:**
- Bold
- In List View
- In Standard Filter
- In Global Search
- Hide in Print
- Hide in Report

**Conditional Logic:**
- Depends On (show/hide based on conditions)
- Mandatory Depends On
- Read Only Depends On

**Advanced Options:**
- Fetch From (fetch values from linked documents)
- Permission Level
- Columns (width in list view)
- Allow on Submit
- Allow Bulk Edit
- Allow in Quick Entry
- Remember Last Value
- Search Index
- Translatable

### 3. Drag & Drop Ordering

- Reorder fields by dragging the grip icon
- Visual feedback during drag operations
- Automatic re-indexing after reorder

### 4. Field Operations

- **Add Field** - Create new field with defaults
- **Edit Field** - Modify field configuration
- **Duplicate Field** - Clone existing field
- **Delete Field** - Remove field with confirmation

### 5. Form Operations

- **Save Schema** - Save to Ezy Form Definitions
- **Preview** - View JSON structure
- **Load Form** - Load existing form by name

## API Endpoints

All endpoints follow security best practices with authentication checks:

### Get Field Types
```javascript
import { apis } from '@/shared/apiurls';
import { api_req_data } from '@/shared/services/api_req_data';

const response = await api_req_data(apis.getFieldTypes);
// Returns: { success: true, field_types: [...] }
```

### Save Form Definition
```javascript
import { api_post_data } from '@/shared/services/api_req_data';

const response = await api_post_data(apis.saveFormDefinition, {
  form_name: 'Customer Request',
  fields: JSON.stringify(fieldArray)
});
// Returns: { success: true, form_id: "...", message: "..." }
```

### Get Form Definition
```javascript
const response = await api_post_data(apis.getFormDefinition, {
  form_name: 'Customer Request'
});
// Returns: { success: true, fields: [...], form_name: "...", ... }
```

### Validate Fieldname
```javascript
const response = await api_post_data(apis.validateFieldname, {
  fieldname: 'customer_name'
});
// Returns: { success: true, valid: true, message: "..." }
```

### Get Link Options (DocTypes)
```javascript
const response = await api_post_data(apis.getLinkOptions, {
  doctype_filter: 'Customer' // optional
});
// Returns: { success: true, doctypes: [...] }
```

### Get Child Table Options
```javascript
const response = await api_req_data(apis.getChildTableOptions);
// Returns: { success: true, child_doctypes: [...] }
```

## Frappe DocField Structure

The form builder generates JSON that matches Frappe's DocField structure:

```json
{
  "idx": 1,
  "fieldname": "customer_name",
  "fieldtype": "Data",
  "label": "Customer Name",
  "description": "Full name of the customer",
  "options": "",
  "reqd": 1,
  "read_only": 0,
  "hidden": 0,
  "default": "",
  "depends_on": "eval:doc.customer_type=='Individual'",
  "mandatory_depends_on": "",
  "read_only_depends_on": "",
  "permlevel": 0,
  "in_list_view": 1,
  "in_standard_filter": 0,
  "in_global_search": 1,
  "bold": 0,
  "unique": 0,
  "length": 140,
  "precision": "",
  "non_negative": 0,
  "allow_bulk_edit": 0,
  "allow_in_quick_entry": 1,
  "allow_on_submit": 0,
  "translatable": 1,
  "search_index": 0,
  "fetch_from": "",
  "fetch_if_empty": 0,
  "columns": 0,
  "print_hide": 0,
  "print_hide_if_no_value": 0,
  "report_hide": 0,
  "documentation_url": ""
}
```

## Security Features

All backend APIs include:

1. **Authentication Check**
   ```python
   if frappe.session.user == "Guest":
       frappe.throw(_("Authentication required"), frappe.AuthenticationError)
   ```

2. **Parameterized Queries**
   ```python
   query = "SELECT name FROM `tabDocType` WHERE name = %s"
   frappe.db.sql(query, (form_name,), as_dict=True)
   ```

3. **Input Validation**
   ```python
   if not re.match(r'^[a-z_][a-z0-9_]*$', fieldname):
       frappe.throw("Invalid fieldname format")
   ```

4. **Reserved Keyword Check**
   - Prevents using Frappe reserved keywords as fieldnames
   - Examples: `name`, `owner`, `creation`, `modified`, `docstatus`, `idx`

## Styling

The form builder uses Bootstrap classes and custom styles that integrate with your existing EzyForms theme:

- Responsive design (mobile-friendly)
- Bootstrap 5 grid system
- Custom color scheme matching EzyForms
- Smooth animations and transitions

## Tips & Best Practices

1. **Fieldname Convention**
   - Use lowercase letters, numbers, and underscores only
   - Start with a letter or underscore
   - Example: `customer_name`, `date_of_birth`, `is_active`

2. **Field Dependencies**
   - Use `depends_on` for conditional display
   - Format: `eval:doc.field_name=='value'`
   - Example: `eval:doc.customer_type=='Individual'`

3. **Options Field**
   - **Select**: One option per line
     ```
     Option 1
     Option 2
     Option 3
     ```
   - **Link**: Single DocType name (e.g., `Customer`)
   - **Table**: Child DocType name (e.g., `Sales Invoice Item`)

4. **Performance**
   - Avoid too many fields in list view
   - Use collapsible sections for large forms
   - Enable search index only on frequently searched fields

5. **Validation**
   - Set `reqd: 1` for mandatory fields
   - Use `unique: 1` for unique constraints
   - Set appropriate field lengths
   - Use `non_negative: 1` for positive numbers only

## Troubleshooting

### Build Errors

If you encounter build errors, ensure:
- `vuedraggable` is installed: `npm list vuedraggable`
- All imports are correct
- Run `npm run build` from the frontend directory

### API Errors

If API calls fail:
- Check user authentication
- Verify `form_builder.py` exists in `ezy_forms/api/v1/`
- Ensure backend is running
- Check browser console for errors

### Form Not Saving

If the form doesn't save:
- Ensure all fields are valid (close editing mode)
- Check required fields (fieldname, label, fieldtype)
- Verify fieldname format (lowercase, underscores only)
- Check for reserved keywords

### Drag & Drop Not Working

If drag-and-drop doesn't work:
- Verify `vuedraggable` version 4.x is installed
- Check browser console for errors
- Ensure `.drag-handle` class is present

## Next Steps

1. **Customize UI**: Modify component styles to match your branding
2. **Add Validation**: Add custom field validation rules
3. **Extend Features**: Add more field types or custom properties
4. **Integration**: Connect with your workflow system
5. **Testing**: Create test forms and validate all field types

## Support

For issues or questions:
- Check the component code comments
- Review Frappe DocType documentation
- Test with small forms first
- Use browser DevTools for debugging

## Example: Complete Integration

Here's a complete example showing all features:

```vue
<template>
  <div class="form-builder-page">
    <div class="page-header">
      <h2>Custom Form Builder</h2>
      <div class="actions">
        <button @click="loadForm" class="btn btn-secondary">
          Load Existing
        </button>
        <button @click="saveAndPublish" class="btn btn-primary">
          Save & Publish
        </button>
      </div>
    </div>

    <FrappeFormBuilder
      ref="formBuilderRef"
      :formName="formName"
      :existingFields="existingFields"
      @save="handleSave"
      @update="handleUpdate"
      @preview="handlePreview"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import FrappeFormBuilder from '@/Components/FrappeFormBuilder.vue';
import { api_post_data } from '@/shared/services/api_req_data';
import { apis } from '@/shared/apiurls';

const formBuilderRef = ref(null);
const formName = ref('');
const existingFields = ref([]);

onMounted(() => {
  // Load form if editing
  const formId = new URLSearchParams(window.location.search).get('form');
  if (formId) {
    loadFormById(formId);
  }
});

const loadFormById = async (formId) => {
  try {
    const response = await api_post_data(apis.getFormDefinition, {
      form_name: formId
    });

    if (response.success) {
      formName.value = response.form_name;
      existingFields.value = response.fields;
    }
  } catch (error) {
    console.error('Error loading form:', error);
    alert('Failed to load form');
  }
};

const loadForm = async () => {
  const name = prompt('Enter form name to load:');
  if (name) {
    await loadFormById(name);
  }
};

const handleSave = (fields) => {
  console.log('Form saved successfully with fields:', fields);
  alert('Form saved successfully!');
};

const handleUpdate = (fields) => {
  console.log('Form fields updated:', fields.length);
  existingFields.value = fields;
};

const handlePreview = (fields) => {
  console.log('Preview requested:', fields);
};

const saveAndPublish = async () => {
  if (!formName.value) {
    formName.value = prompt('Enter form name:');
    if (!formName.value) return;
  }

  await formBuilderRef.value.saveFormSchema();
  // Additional publish logic here
};
</script>

<style scoped>
.form-builder-page {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding: 20px;
  background: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.actions {
  display: flex;
  gap: 10px;
}
</style>
```

---

**Version**: 1.0
**Last Updated**: November 2025
**Author**: Claude Code Integration
