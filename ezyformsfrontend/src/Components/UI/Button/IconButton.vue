<template>
  <button
    :type="type"
    :disabled="disabled"
    :class="buttonClasses"
    :aria-label="ariaLabel"
    @click="handleClick"
    class="icon-button"
    v-tooltip="tooltip"
  >
    <i :class="icon"></i>
  </button>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  type: {
    type: String,
    default: 'button'
  },
  icon: {
    type: String,
    required: true
  },
  variant: {
    type: String,
    default: 'ghost',
    validator: (value) => ['solid', 'outline', 'ghost'].includes(value)
  },
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  color: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'primary', 'success', 'warning', 'error'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  ariaLabel: {
    type: String,
    required: true
  },
  tooltip: {
    type: String,
    default: ''
  }
});

const emit = defineEmits(['click']);

const buttonClasses = computed(() => [
  `icon-button--${props.variant}`,
  `icon-button--${props.size}`,
  `icon-button--${props.color}`,
  {
    'icon-button--disabled': props.disabled
  }
]);

const handleClick = (event) => {
  if (!props.disabled) {
    emit('click', event);
  }
};
</script>

<style scoped lang="scss">
@import '@/Styles/design-tokens.scss';

.icon-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border: var(--border-width-thin) solid transparent;
  transition: var(--transition-colors), var(--transition-transform);
  user-select: none;
  outline: none;
  flex-shrink: 0;

  &:focus-visible {
    box-shadow: var(--focus-ring);
  }

  /* Sizes */
  &--sm {
    width: var(--size-button-sm);
    height: var(--size-button-sm);
    border-radius: var(--border-radius-md);

    i {
      font-size: var(--size-icon-sm);
    }
  }

  &--md {
    width: var(--size-button-md);
    height: var(--size-button-md);
    border-radius: var(--border-radius-lg);

    i {
      font-size: var(--size-icon-md);
    }
  }

  &--lg {
    width: var(--size-button-lg);
    height: var(--size-button-lg);
    border-radius: var(--border-radius-xl);

    i {
      font-size: var(--size-icon-lg);
    }
  }

  /* Variants + Colors */
  &--solid {
    &.icon-button--default {
      background: var(--color-gray-600);
      color: var(--color-text-inverse);

      &:hover:not(.icon-button--disabled) {
        background: var(--color-gray-700);
        transform: translateY(-1px);
      }
    }

    &.icon-button--primary {
      background: var(--color-primary-600);
      color: var(--color-text-inverse);

      &:hover:not(.icon-button--disabled) {
        background: var(--color-primary-700);
        transform: translateY(-1px);
      }
    }

    &.icon-button--success {
      background: var(--color-success-600);
      color: var(--color-text-inverse);

      &:hover:not(.icon-button--disabled) {
        background: var(--color-success-700);
        transform: translateY(-1px);
      }
    }

    &.icon-button--warning {
      background: var(--color-warning-600);
      color: var(--color-text-inverse);

      &:hover:not(.icon-button--disabled) {
        background: var(--color-warning-700);
        transform: translateY(-1px);
      }
    }

    &.icon-button--error {
      background: var(--color-error-600);
      color: var(--color-text-inverse);

      &:hover:not(.icon-button--disabled) {
        background: var(--color-error-700);
        transform: translateY(-1px);
      }
    }
  }

  &--outline {
    background: var(--color-background);

    &.icon-button--default {
      color: var(--color-gray-700);
      border-color: var(--color-gray-300);

      &:hover:not(.icon-button--disabled) {
        background: var(--color-gray-50);
        border-color: var(--color-gray-400);
      }
    }

    &.icon-button--primary {
      color: var(--color-primary-600);
      border-color: var(--color-primary-600);

      &:hover:not(.icon-button--disabled) {
        background: var(--color-primary-50);
        border-color: var(--color-primary-700);
      }
    }

    &.icon-button--success {
      color: var(--color-success-600);
      border-color: var(--color-success-600);

      &:hover:not(.icon-button--disabled) {
        background: var(--color-success-50);
        border-color: var(--color-success-700);
      }
    }

    &.icon-button--warning {
      color: var(--color-warning-600);
      border-color: var(--color-warning-600);

      &:hover:not(.icon-button--disabled) {
        background: var(--color-warning-50);
        border-color: var(--color-warning-700);
      }
    }

    &.icon-button--error {
      color: var(--color-error-600);
      border-color: var(--color-error-600);

      &:hover:not(.icon-button--disabled) {
        background: var(--color-error-50);
        border-color: var(--color-error-700);
      }
    }
  }

  &--ghost {
    background: transparent;

    &.icon-button--default {
      color: var(--color-gray-700);

      &:hover:not(.icon-button--disabled) {
        background: var(--color-gray-100);
      }
    }

    &.icon-button--primary {
      color: var(--color-primary-600);

      &:hover:not(.icon-button--disabled) {
        background: var(--color-primary-50);
      }
    }

    &.icon-button--success {
      color: var(--color-success-600);

      &:hover:not(.icon-button--disabled) {
        background: var(--color-success-50);
      }
    }

    &.icon-button--warning {
      color: var(--color-warning-600);

      &:hover:not(.icon-button--disabled) {
        background: var(--color-warning-50);
      }
    }

    &.icon-button--error {
      color: var(--color-error-600);

      &:hover:not(.icon-button--disabled) {
        background: var(--color-error-50);
      }
    }
  }

  /* States */
  &--disabled {
    cursor: not-allowed;
    opacity: 0.4;
    pointer-events: none;
  }

  &:active:not(&--disabled) {
    transform: scale(0.95);
  }
}
</style>
