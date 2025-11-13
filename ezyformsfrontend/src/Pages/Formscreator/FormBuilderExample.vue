<template>
  <div class="form-builder-example">
    <div class="container-fluid">
      <div class="row">
        <div class="col-12">
          <div class="header-section">
            <h2 class="page-title">Advanced Form Builder</h2>
            <p class="page-subtitle">
              Create dynamic forms with Frappe-compatible field types, validations, and drag-and-drop ordering
            </p>
          </div>

          <!-- Form Builder Component -->
          <FrappeFormBuilder
            ref="formBuilderRef"
            :formName="formName"
            :existingFields="existingFields"
            @save="handleFormSave"
            @update="handleFormUpdate"
            @preview="handleFormPreview"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import FrappeFormBuilder from '@/Components/FrappeFormBuilder.vue';
import { api_post_data } from '@/shared/services/api_req_data';
import { apis } from '@/shared/apiurls';

const route = useRoute();
const formBuilderRef = ref(null);
const formName = ref('');
const existingFields = ref([]);

// Load existing form if editing
onMounted(async () => {
  // Check if we're editing an existing form
  if (route.query.form_name) {
    formName.value = route.query.form_name;
    await loadExistingForm(route.query.form_name);
  } else if (route.query.id) {
    // Load by ID
    await loadFormById(route.query.id);
  }
});

/**
 * Load an existing form by name
 */
const loadExistingForm = async (name) => {
  try {
    const response = await api_post_data(apis.getFormDefinition, {
      form_name: name
    });

    if (response && response.success) {
      existingFields.value = response.fields || [];
      formName.value = response.form_name;
      console.log('Form loaded successfully:', response.form_name);
    } else {
      console.error('Failed to load form:', response.message);
    }
  } catch (error) {
    console.error('Error loading form:', error);
  }
};

/**
 * Load form by ID (if using different identifier)
 */
const loadFormById = async (id) => {
  // Implement if you use form IDs instead of names
  console.log('Loading form by ID:', id);
};

/**
 * Handle form save event
 */
const handleFormSave = (fields) => {
  console.log('Form saved successfully!');
  console.log('Total fields:', fields.length);

  // Show success message
  showSuccessNotification('Form saved successfully!');

  // You can add additional logic here:
  // - Redirect to form list
  // - Update parent component
  // - Trigger other actions
};

/**
 * Handle form update event (real-time updates)
 */
const handleFormUpdate = (fields) => {
  console.log('Form updated:', fields.length, 'fields');
  existingFields.value = fields;
};

/**
 * Handle form preview event
 */
const handleFormPreview = (fields) => {
  console.log('Preview requested for', fields.length, 'fields');
  // You can open a preview modal or navigate to preview page
};

/**
 * Show success notification
 */
const showSuccessNotification = (message) => {
  // Implement your notification system here
  // For now, using alert as fallback
  alert(message);
};

/**
 * Get current form fields programmatically
 */
const getCurrentFields = () => {
  if (formBuilderRef.value) {
    return formBuilderRef.value.getFields();
  }
  return [];
};

/**
 * Trigger save programmatically
 */
const saveForm = async () => {
  if (formBuilderRef.value) {
    await formBuilderRef.value.saveFormSchema();
  }
};

// Expose methods for parent components if needed
defineExpose({
  getCurrentFields,
  saveForm,
  formBuilderRef
});
</script>

<style scoped>
.form-builder-example {
  min-height: 100vh;
  background: #f8f9fa;
  padding: 20px 0;
}

.header-section {
  background: white;
  padding: 30px;
  border-radius: 8px;
  margin-bottom: 30px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.page-title {
  font-size: 28px;
  font-weight: 700;
  color: #2c3e50;
  margin-bottom: 10px;
}

.page-subtitle {
  font-size: 14px;
  color: #6c757d;
  margin: 0;
}

/* Responsive design */
@media (max-width: 768px) {
  .header-section {
    padding: 20px;
  }

  .page-title {
    font-size: 22px;
  }

  .page-subtitle {
    font-size: 13px;
  }
}
</style>
