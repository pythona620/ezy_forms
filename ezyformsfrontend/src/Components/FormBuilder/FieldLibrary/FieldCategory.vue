<template>
  <div class="field-category" :class="{ 'field-category--collapsed': isCollapsed }">
    <div
      class="field-category-header"
      @click="toggleCollapse"
      role="button"
      tabindex="0"
      :aria-expanded="!isCollapsed"
      :aria-controls="`category-${category.id}`"
      @keydown.enter="toggleCollapse"
      @keydown.space.prevent="toggleCollapse"
    >
      <div class="field-category-title">
        <i :class="category.icon" class="field-category-icon"></i>
        <h3 class="field-category-name">{{ category.name }}</h3>
        <span class="field-category-count">({{ fields.length }})</span>
      </div>

      <i
        class="bi bi-chevron-down field-category-chevron"
        :class="{ 'field-category-chevron--collapsed': isCollapsed }"
      ></i>
    </div>

    <transition name="category-expand">
      <div
        v-show="!isCollapsed"
        :id="`category-${category.id}`"
        class="field-category-content"
      >
        <p v-if="category.description" class="field-category-description">
          {{ category.description }}
        </p>

        <div class="field-category-fields">
          <FieldCard
            v-for="field in fields"
            :key="field.id"
            :field="field"
            :compact="compact"
            @dragstart="handleFieldDragStart"
            @dragend="handleFieldDragEnd"
            @click="handleFieldClick"
            @add="handleFieldAdd"
          />
        </div>

        <div v-if="fields.length === 0" class="field-category-empty">
          <i class="bi bi-inbox"></i>
          <p>No fields in this category</p>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import FieldCard from './FieldCard.vue';

const props = defineProps({
  category: {
    type: Object,
    required: true
  },
  fields: {
    type: Array,
    default: () => []
  },
  initiallyCollapsed: {
    type: Boolean,
    default: false
  },
  compact: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['field-dragstart', 'field-dragend', 'field-click', 'field-add', 'toggle']);

const isCollapsed = ref(props.initiallyCollapsed || props.category.collapsed || false);

const toggleCollapse = () => {
  isCollapsed.value = !isCollapsed.value;
  emit('toggle', {
    categoryId: props.category.id,
    isCollapsed: isCollapsed.value
  });
};

const handleFieldDragStart = (data) => {
  emit('field-dragstart', {
    ...data,
    categoryId: props.category.id
  });
};

const handleFieldDragEnd = (event) => {
  emit('field-dragend', event);
};

const handleFieldClick = (field) => {
  emit('field-click', {
    field,
    categoryId: props.category.id
  });
};

const handleFieldAdd = (field) => {
  emit('field-add', {
    field,
    categoryId: props.category.id
  });
};
</script>

<style scoped lang="scss">
@import '@/Styles/design-tokens.scss';

.field-category {
  border-bottom: var(--border-width-thin) solid var(--color-border);

  &:last-child {
    border-bottom: none;
  }

  /* Header */
  .field-category-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-3) var(--space-4);
    cursor: pointer;
    user-select: none;
    transition: var(--transition-colors);

    &:hover {
      background: var(--color-surface-hover);
    }

    &:focus-visible {
      outline: none;
      box-shadow: inset 0 0 0 2px var(--color-primary-500);
    }
  }

  .field-category-title {
    display: flex;
    align-items: center;
    gap: var(--space-2);
  }

  .field-category-icon {
    font-size: var(--size-icon-sm);
    color: var(--color-primary-600);
  }

  .field-category-name {
    margin: 0;
    font-size: var(--font-size-sm);
    font-weight: var(--font-weight-semibold);
    color: var(--color-text-primary);
    line-height: var(--line-height-tight);
  }

  .field-category-count {
    font-size: var(--font-size-xs);
    color: var(--color-text-tertiary);
    font-weight: var(--font-weight-normal);
  }

  .field-category-chevron {
    font-size: var(--size-icon-sm);
    color: var(--color-text-secondary);
    transition: var(--transition-transform);

    &--collapsed {
      transform: rotate(-90deg);
    }
  }

  /* Content */
  .field-category-content {
    padding: 0 var(--space-4) var(--space-4);
  }

  .field-category-description {
    margin: 0 0 var(--space-3);
    font-size: var(--font-size-xs);
    color: var(--color-text-secondary);
    line-height: var(--line-height-relaxed);
  }

  .field-category-fields {
    display: flex;
    flex-direction: column;
    gap: var(--space-2);
  }

  /* Empty State */
  .field-category-empty {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: var(--space-8) var(--space-4);
    text-align: center;
    color: var(--color-text-tertiary);

    i {
      font-size: var(--size-icon-xl);
      margin-bottom: var(--space-2);
    }

    p {
      margin: 0;
      font-size: var(--font-size-sm);
    }
  }
}

/* Collapse Animation */
.category-expand-enter-active,
.category-expand-leave-active {
  transition: all var(--duration-normal) var(--ease-smooth);
  transform-origin: top;
  overflow: hidden;
}

.category-expand-enter-from,
.category-expand-leave-to {
  opacity: 0;
  max-height: 0;
  transform: scaleY(0.9);
}

.category-expand-enter-to,
.category-expand-leave-from {
  opacity: 1;
  max-height: 2000px;
  transform: scaleY(1);
}

/* Responsive */
@media (max-width: 768px) {
  .field-category {
    .field-category-header {
      padding: var(--space-2) var(--space-3);
    }

    .field-category-content {
      padding: 0 var(--space-3) var(--space-3);
    }

    .field-category-name {
      font-size: var(--font-size-xs);
    }
  }
}
</style>
