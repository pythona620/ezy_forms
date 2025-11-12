<template>
  <div class="simple-field-library">
    <!-- Search Bar -->
    <div class="field-search">
      <i class="bi bi-search"></i>
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Search fields"
        class="search-input"
      />
    </div>

    <!-- Field Type Buttons -->
    <div class="field-types-grid">
      <button
        v-for="field in filteredFields"
        :key="field.type"
        class="field-type-btn"
        :draggable="true"
        @dragstart="handleDragStart($event, field)"
        @dragend="handleDragEnd"
        @click="handleClick(field)"
      >
        {{ field.label }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  fields: {
    type: Array,
    required: true
  }
});

const emit = defineEmits(['field-add', 'field-dragstart', 'field-dragend']);

const searchQuery = ref('');
const isDragging = ref(false);

// Filter fields based on search
const filteredFields = computed(() => {
  if (!searchQuery.value) {
    return props.fields;
  }
  const query = searchQuery.value.toLowerCase();
  return props.fields.filter(field =>
    field.label.toLowerCase().includes(query)
  );
});

const handleDragStart = (event, field) => {
  isDragging.value = true;

  // Set drag data - send the field type
  event.dataTransfer.effectAllowed = 'copy';
  event.dataTransfer.setData('text/plain', field.type);

  // Emit drag start event with field type
  emit('field-dragstart', field.type);
};

const handleDragEnd = () => {
  isDragging.value = false;
  emit('field-dragend');
};

const handleClick = (field) => {
  // Emit field-add event with field type
  emit('field-add', field.type);
};
</script>

<style scoped lang="scss">
.simple-field-library {
  display: flex;
  flex-direction: column;
  height: 100%;
  background: #ffffff;
}

.field-search {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  border-bottom: 1px solid #e5e7eb;

  i {
    color: #9ca3af;
    font-size: 14px;
  }

  .search-input {
    flex: 1;
    border: none;
    outline: none;
    font-size: 14px;
    color: #111827;

    &::placeholder {
      color: #9ca3af;
    }
  }
}

.field-types-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 0.5rem;
  padding: 1rem;
  overflow-y: auto;

  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-thumb {
    background: #d1d5db;
    border-radius: 3px;

    &:hover {
      background: #9ca3af;
    }
  }
}

.field-type-btn {
  padding: 0.75rem 1rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px;
  font-size: 13px;
  font-weight: 500;
  color: #374151;
  cursor: grab;
  transition: all 0.15s;
  text-align: left;

  &:hover {
    background: #f3f4f6;
    border-color: #d1d5db;
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  }

  &:active {
    cursor: grabbing;
    transform: scale(0.98);
  }
}
</style>
