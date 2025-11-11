<template>
  <div
    class="field-card"
    :class="fieldCardClasses"
    :draggable="!disabled"
    @dragstart="handleDragStart"
    @dragend="handleDragEnd"
    @click="handleClick"
    role="button"
    tabindex="0"
    :aria-label="`Add ${field.name} field`"
    @keydown.enter="handleClick"
    @keydown.space.prevent="handleClick"
  >
    <div class="field-card-icon">
      <i :class="field.icon"></i>
    </div>

    <div class="field-card-content">
      <h4 class="field-card-title">{{ field.name }}</h4>
      <p class="field-card-description">{{ field.description }}</p>
    </div>

    <div class="field-card-actions">
      <i class="bi bi-plus-circle"></i>
    </div>

    <!-- Drag preview tooltip -->
    <div v-if="isDragging" class="field-card-drag-preview">
      <i :class="field.icon"></i>
      <span>{{ field.name }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  field: {
    type: Object,
    required: true
  },
  disabled: {
    type: Boolean,
    default: false
  },
  compact: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['dragstart', 'dragend', 'click', 'add']);

const isDragging = ref(false);
const isHovered = ref(false);

const fieldCardClasses = computed(() => ({
  'field-card--dragging': isDragging.value,
  'field-card--disabled': props.disabled,
  'field-card--compact': props.compact,
  'field-card--hovered': isHovered.value
}));

const handleDragStart = (event) => {
  if (props.disabled) return;

  isDragging.value = true;

  // Set drag data
  event.dataTransfer.effectAllowed = 'copy';
  event.dataTransfer.setData('application/json', JSON.stringify({
    fieldType: props.field.id,
    fieldData: props.field
  }));

  // Create custom drag image
  const dragImage = event.currentTarget.cloneNode(true);
  dragImage.style.opacity = '0.8';
  dragImage.style.transform = 'rotate(-2deg)';
  document.body.appendChild(dragImage);
  event.dataTransfer.setDragImage(dragImage, 75, 20);

  // Clean up drag image after a short delay
  setTimeout(() => {
    document.body.removeChild(dragImage);
  }, 0);

  emit('dragstart', {
    fieldType: props.field.id,
    fieldData: props.field,
    event
  });
};

const handleDragEnd = (event) => {
  isDragging.value = false;
  emit('dragend', event);
};

const handleClick = () => {
  if (props.disabled) return;
  emit('click', props.field);
  emit('add', props.field);
};
</script>

<style scoped lang="scss">
@import '@/Styles/design-tokens.scss';

.field-card {
  position: relative;
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3);
  background: var(--color-surface);
  border: var(--border-width-thin) solid var(--color-border);
  border-radius: var(--border-radius-lg);
  cursor: grab;
  transition: var(--transition-normal);
  user-select: none;

  &:hover:not(&--disabled) {
    background: var(--color-surface-hover);
    border-color: var(--color-primary-300);
    box-shadow: var(--shadow-sm);
    transform: translateY(-1px);
  }

  &:active:not(&--disabled) {
    cursor: grabbing;
    transform: scale(0.98);
  }

  &:focus-visible {
    outline: none;
    box-shadow: var(--focus-ring);
  }

  /* Icon */
  .field-card-icon {
    display: flex;
    align-items: center;
    justify-content: center;
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, var(--color-primary-50) 0%, var(--color-primary-100) 100%);
    border-radius: var(--border-radius-lg);
    flex-shrink: 0;

    i {
      font-size: var(--size-icon-md);
      color: var(--color-primary-600);
    }
  }

  /* Content */
  .field-card-content {
    flex: 1;
    min-width: 0;
  }

  .field-card-title {
    margin: 0;
    font-size: var(--font-size-sm);
    font-weight: var(--font-weight-semibold);
    color: var(--color-text-primary);
    line-height: var(--line-height-tight);
  }

  .field-card-description {
    margin: var(--space-1) 0 0;
    font-size: var(--font-size-xs);
    color: var(--color-text-secondary);
    line-height: var(--line-height-normal);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }

  /* Actions */
  .field-card-actions {
    display: flex;
    align-items: center;
    opacity: 0;
    transition: var(--transition-opacity);

    i {
      font-size: var(--size-icon-md);
      color: var(--color-primary-600);
    }
  }

  &:hover .field-card-actions {
    opacity: 1;
  }

  /* States */
  &--dragging {
    opacity: 0.5;
    cursor: grabbing;
  }

  &--disabled {
    opacity: 0.5;
    cursor: not-allowed;
    pointer-events: none;
  }

  &--compact {
    padding: var(--space-2);
    gap: var(--space-2);

    .field-card-icon {
      width: 32px;
      height: 32px;

      i {
        font-size: var(--size-icon-sm);
      }
    }

    .field-card-title {
      font-size: var(--font-size-xs);
    }

    .field-card-description {
      display: none;
    }
  }

  /* Drag Preview (shown at cursor during drag) */
  .field-card-drag-preview {
    display: none;
    position: fixed;
    pointer-events: none;
    z-index: var(--z-index-tooltip);
    padding: var(--space-2) var(--space-3);
    background: var(--color-primary-600);
    color: var(--color-text-inverse);
    border-radius: var(--border-radius-md);
    box-shadow: var(--shadow-lg);
    font-size: var(--font-size-sm);
    font-weight: var(--font-weight-medium);
    gap: var(--space-2);
    align-items: center;

    i {
      font-size: var(--size-icon-sm);
    }
  }
}

/* Responsive */
@media (max-width: 768px) {
  .field-card {
    padding: var(--space-2);
    gap: var(--space-2);

    .field-card-icon {
      width: 36px;
      height: 36px;

      i {
        font-size: var(--size-icon-sm);
      }
    }

    .field-card-title {
      font-size: var(--font-size-xs);
    }

    .field-card-description {
      font-size: 0.65rem;
    }
  }
}
</style>
