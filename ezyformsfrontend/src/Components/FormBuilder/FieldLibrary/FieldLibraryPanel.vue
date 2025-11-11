<template>
  <div class="field-library-panel" :class="{ 'field-library-panel--collapsed': isCollapsed }">
    <!-- Header -->
    <div class="field-library-header">
      <div class="field-library-title">
        <i class="bi bi-grid-3x3-gap"></i>
        <h2>Add Fields</h2>
      </div>

      <IconButton
        v-if="collapsible"
        :icon="isCollapsed ? 'bi bi-chevron-right' : 'bi bi-chevron-left'"
        variant="ghost"
        size="sm"
        aria-label="Toggle field library"
        @click="toggleCollapse"
      />
    </div>

    <!-- Content (only shown when not collapsed) -->
    <div v-show="!isCollapsed" class="field-library-content">
      <!-- Search -->
      <div class="field-library-search">
        <TextInput
          v-model="searchQuery"
          type="search"
          placeholder="Search fields..."
          icon-left="bi bi-search"
          :clearable="true"
          size="sm"
          @update:model-value="handleSearch"
        />
      </div>

      <!-- Results count (when searching) -->
      <div v-if="searchQuery" class="field-library-results">
        <p v-if="searchResults.length > 0">
          {{ searchResults.length }} field{{ searchResults.length !== 1 ? 's' : '' }} found
        </p>
        <p v-else class="field-library-no-results">
          <i class="bi bi-search"></i>
          No fields found matching "{{ searchQuery }}"
        </p>
      </div>

      <!-- Search Results (flat list) -->
      <div v-if="searchQuery && searchResults.length > 0" class="field-library-search-results">
        <FieldCard
          v-for="field in searchResults"
          :key="field.id"
          :field="field"
          :compact="compactMode"
          @dragstart="handleFieldDragStart"
          @dragend="handleFieldDragEnd"
          @click="handleFieldClick"
          @add="handleFieldAdd"
        />
      </div>

      <!-- Categories (default view) -->
      <div v-else class="field-library-categories">
        <FieldCategory
          v-for="category in filteredCategories"
          :key="category.id"
          :category="category"
          :fields="getFieldsByCategory(category.id)"
          :compact="compactMode"
          @field-dragstart="handleFieldDragStart"
          @field-dragend="handleFieldDragEnd"
          @field-click="handleFieldClick"
          @field-add="handleFieldAdd"
          @toggle="handleCategoryToggle"
        />
      </div>

      <!-- Help Text -->
      <div class="field-library-help">
        <i class="bi bi-info-circle"></i>
        <p>Drag fields to the canvas or click to add</p>
      </div>
    </div>

    <!-- Collapsed State Indicator -->
    <div v-if="isCollapsed" class="field-library-collapsed-indicator">
      <i class="bi bi-grid-3x3-gap"></i>
      <span>Fields</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import FieldCard from './FieldCard.vue';
import FieldCategory from './FieldCategory.vue';
import TextInput from '@/Components/UI/Input/TextInput.vue';
import IconButton from '@/Components/UI/Button/IconButton.vue';
import {
  FIELD_CATEGORIES,
  FIELD_TYPES,
  getFieldsByCategory as getFieldsByCat,
  searchFieldTypes
} from './fieldTypes';

const props = defineProps({
  collapsible: {
    type: Boolean,
    default: true
  },
  initiallyCollapsed: {
    type: Boolean,
    default: false
  },
  compactMode: {
    type: Boolean,
    default: false
  },
  hiddenCategories: {
    type: Array,
    default: () => []
  },
  hiddenFields: {
    type: Array,
    default: () => []
  }
});

const emit = defineEmits([
  'field-dragstart',
  'field-dragend',
  'field-click',
  'field-add',
  'collapse',
  'expand'
]);

// State
const searchQuery = ref('');
const isCollapsed = ref(props.initiallyCollapsed);
const categoryStates = ref({});

// Computed
const filteredCategories = computed(() => {
  return FIELD_CATEGORIES.filter(
    category => !props.hiddenCategories.includes(category.id)
  );
});

const searchResults = computed(() => {
  if (!searchQuery.value) return [];

  const results = searchFieldTypes(searchQuery.value);
  return results.filter(
    field => !props.hiddenFields.includes(field.id)
  );
});

// Methods
function getFieldsByCategory(categoryId) {
  const fields = getFieldsByCat(categoryId);
  return fields.filter(
    field => !props.hiddenFields.includes(field.id)
  );
}

function toggleCollapse() {
  isCollapsed.value = !isCollapsed.value;
  emit(isCollapsed.value ? 'collapse' : 'expand');
}

function handleSearch(query) {
  // Search is handled by computed property
}

function handleFieldDragStart(data) {
  emit('field-dragstart', data);
}

function handleFieldDragEnd(event) {
  emit('field-dragend', event);
}

function handleFieldClick(data) {
  emit('field-click', data);
}

function handleFieldAdd(data) {
  emit('field-add', data);
}

function handleCategoryToggle(data) {
  categoryStates.value[data.categoryId] = data.isCollapsed;
}

// Keyboard shortcut to focus search
function handleGlobalKeydown(event) {
  // Ctrl/Cmd + K to focus search
  if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
    event.preventDefault();
    const searchInput = document.querySelector('.field-library-search input');
    if (searchInput) {
      searchInput.focus();
    }
  }
}

// Lifecycle
import { onMounted, onUnmounted } from 'vue';

onMounted(() => {
  document.addEventListener('keydown', handleGlobalKeydown);
});

onUnmounted(() => {
  document.removeEventListener('keydown', handleGlobalKeydown);
});
</script>

<style scoped lang="scss">
@import '@/Styles/design-tokens.scss';

.field-library-panel {
  display: flex;
  flex-direction: column;
  width: var(--field-library-width);
  height: 100%;
  background: var(--color-background);
  border-right: var(--border-width-thin) solid var(--color-border);
  transition: var(--transition-normal);

  /* Collapsed State */
  &--collapsed {
    width: 60px;

    .field-library-header h2,
    .field-library-content {
      display: none;
    }
  }

  /* Header */
  .field-library-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-4);
    border-bottom: var(--border-width-thin) solid var(--color-border);
    background: var(--color-background-secondary);
  }

  .field-library-title {
    display: flex;
    align-items: center;
    gap: var(--space-2);

    i {
      font-size: var(--size-icon-md);
      color: var(--color-primary-600);
    }

    h2 {
      margin: 0;
      font-size: var(--font-size-lg);
      font-weight: var(--font-weight-semibold);
      color: var(--color-text-primary);
      line-height: var(--line-height-tight);
    }
  }

  /* Content */
  .field-library-content {
    flex: 1;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  /* Search */
  .field-library-search {
    padding: var(--space-4);
    padding-bottom: var(--space-3);
    border-bottom: var(--border-width-thin) solid var(--color-border);
  }

  /* Results Count */
  .field-library-results {
    padding: var(--space-2) var(--space-4);
    background: var(--color-primary-50);
    border-bottom: var(--border-width-thin) solid var(--color-primary-200);

    p {
      margin: 0;
      font-size: var(--font-size-xs);
      color: var(--color-primary-700);
      font-weight: var(--font-weight-medium);
    }

    .field-library-no-results {
      display: flex;
      align-items: center;
      gap: var(--space-2);
      color: var(--color-text-secondary);

      i {
        font-size: var(--size-icon-sm);
      }
    }
  }

  /* Search Results */
  .field-library-search-results {
    flex: 1;
    overflow-y: auto;
    padding: var(--space-3);
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
  }

  /* Categories */
  .field-library-categories {
    flex: 1;
    overflow-y: auto;
  }

  /* Help Text */
  .field-library-help {
    display: flex;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-3) var(--space-4);
    background: var(--color-background-secondary);
    border-top: var(--border-width-thin) solid var(--color-border);

    i {
      font-size: var(--size-icon-sm);
      color: var(--color-info-600);
      flex-shrink: 0;
    }

    p {
      margin: 0;
      font-size: var(--font-size-xs);
      color: var(--color-text-secondary);
      line-height: var(--line-height-normal);
    }
  }

  /* Collapsed Indicator */
  .field-library-collapsed-indicator {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: var(--space-2);
    padding: var(--space-4) var(--space-2);
    text-align: center;

    i {
      font-size: var(--size-icon-lg);
      color: var(--color-primary-600);
    }

    span {
      font-size: var(--font-size-xs);
      color: var(--color-text-secondary);
      writing-mode: vertical-rl;
      text-orientation: mixed;
    }
  }
}

/* Scrollbar Styling */
.field-library-categories,
.field-library-search-results {
  &::-webkit-scrollbar {
    width: 6px;
  }

  &::-webkit-scrollbar-track {
    background: var(--color-background-secondary);
  }

  &::-webkit-scrollbar-thumb {
    background: var(--color-border);
    border-radius: var(--border-radius-full);

    &:hover {
      background: var(--color-border-hover);
    }
  }
}

/* Responsive */
@media (max-width: 1024px) {
  .field-library-panel {
    width: 240px;
  }
}

@media (max-width: 768px) {
  .field-library-panel {
    position: fixed;
    left: 0;
    top: 0;
    bottom: 0;
    width: 100%;
    max-width: 320px;
    z-index: var(--z-index-modal);
    box-shadow: var(--shadow-xl);
    transform: translateX(-100%);
    transition: transform var(--duration-normal) var(--ease-smooth);

    &:not(&--collapsed) {
      transform: translateX(0);
    }

    &--collapsed {
      width: 60px;
      transform: translateX(0);
    }
  }
}
</style>
