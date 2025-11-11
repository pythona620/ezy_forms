<template>
  <div
    class="drop-zone"
    :class="dropZoneClasses"
    @dragover.prevent="handleDragOver"
    @dragleave="handleDragLeave"
    @drop.prevent="handleDrop"
    role="region"
    :aria-label="`Drop zone ${position || 'default'}`"
  >
    <div class="drop-zone-content">
      <div class="drop-zone-icon">
        <i :class="icon"></i>
      </div>
      <p class="drop-zone-text">
        {{ isActive ? activeText : text }}
      </p>
      <p v-if="helpText" class="drop-zone-help">
        {{ helpText }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const props = defineProps({
  position: {
    type: String,
    default: '', // 'top', 'bottom', 'between', ''
    validator: (value) => ['', 'top', 'bottom', 'between'].includes(value)
  },
  index: {
    type: Number,
    default: null
  },
  text: {
    type: String,
    default: 'Drop field here'
  },
  activeText: {
    type: String,
    default: 'Release to add field'
  },
  helpText: {
    type: String,
    default: ''
  },
  icon: {
    type: String,
    default: 'bi bi-plus-circle'
  },
  show: {
    type: Boolean,
    default: true
  },
  compact: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['drop', 'dragover', 'dragleave']);

const isActive = ref(false);
const dragCounter = ref(0);

const dropZoneClasses = computed(() => ({
  'drop-zone--active': isActive.value,
  'drop-zone--hidden': !props.show,
  'drop-zone--compact': props.compact,
  [`drop-zone--${props.position}`]: props.position
}));

const handleDragOver = (event) => {
  if (dragCounter.value === 0) {
    isActive.value = true;
  }
  dragCounter.value++;

  event.dataTransfer.dropEffect = 'copy';
  emit('dragover', { event, index: props.index, position: props.position });
};

const handleDragLeave = (event) => {
  dragCounter.value--;

  if (dragCounter.value === 0) {
    isActive.value = false;
  }

  emit('dragleave', { event, index: props.index, position: props.position });
};

const handleDrop = (event) => {
  isActive.value = false;
  dragCounter.value = 0;

  try {
    const data = JSON.parse(event.dataTransfer.getData('application/json'));
    emit('drop', {
      data,
      event,
      index: props.index,
      position: props.position
    });
  } catch (error) {
    console.error('Error parsing drop data:', error);
  }
};
</script>

<style scoped lang="scss">
@import '@/Styles/design-tokens.scss';

.drop-zone {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: var(--drop-zone-height);
  padding: var(--space-6);
  background: var(--color-background);
  border: 2px dashed var(--color-border);
  border-radius: var(--border-radius-lg);
  transition: var(--transition-normal);
  opacity: 1;

  /* Content */
  .drop-zone-content {
    text-align: center;
    pointer-events: none;
  }

  .drop-zone-icon {
    margin-bottom: var(--space-2);

    i {
      font-size: var(--size-icon-xl);
      color: var(--color-text-tertiary);
      transition: var(--transition-colors);
    }
  }

  .drop-zone-text {
    margin: 0;
    font-size: var(--font-size-sm);
    font-weight: var(--font-weight-medium);
    color: var(--color-text-secondary);
    transition: var(--transition-colors);
  }

  .drop-zone-help {
    margin: var(--space-1) 0 0;
    font-size: var(--font-size-xs);
    color: var(--color-text-tertiary);
  }

  /* States */
  &--active {
    background: var(--color-primary-50);
    border-color: var(--color-primary-500);
    border-style: solid;
    transform: scale(1.02);
    box-shadow: var(--shadow-primary);

    .drop-zone-icon i {
      color: var(--color-primary-600);
      animation: pulse 0.6s ease-in-out infinite;
    }

    .drop-zone-text {
      color: var(--color-primary-700);
    }
  }

  &--hidden {
    display: none;
  }

  &--compact {
    min-height: 60px;
    padding: var(--space-3);

    .drop-zone-icon i {
      font-size: var(--size-icon-md);
    }

    .drop-zone-text {
      font-size: var(--font-size-xs);
    }

    .drop-zone-help {
      display: none;
    }
  }

  /* Position Variants */
  &--top,
  &--bottom,
  &--between {
    min-height: 80px;
    margin: var(--space-4) 0;
  }

  &--between {
    min-height: 60px;
    margin: var(--space-2) 0;
    background: transparent;
    opacity: 0;
    transition: opacity var(--duration-fast) var(--ease-out);

    &:hover,
    &.drop-zone--active {
      opacity: 1;
    }
  }
}

/* Pulse Animation */
@keyframes pulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.1);
    opacity: 0.8;
  }
}

/* Responsive */
@media (max-width: 768px) {
  .drop-zone {
    min-height: 100px;
    padding: var(--space-4);

    .drop-zone-icon i {
      font-size: var(--size-icon-lg);
    }

    .drop-zone-text {
      font-size: var(--font-size-xs);
    }

    &--compact {
      min-height: 60px;
      padding: var(--space-2);
    }
  }
}
</style>
