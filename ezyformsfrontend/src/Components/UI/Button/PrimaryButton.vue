<template>
  <button
    :type="type"
    :disabled="disabled || loading"
    :class="buttonClasses"
    @click="handleClick"
    class="primary-button"
  >
    <span v-if="loading" class="button-spinner">
      <svg class="spinner-icon" viewBox="0 0 24 24">
        <circle class="spinner-circle" cx="12" cy="12" r="10" />
      </svg>
    </span>

    <i v-if="iconLeft && !loading" :class="iconLeft" class="button-icon-left"></i>

    <span class="button-text">
      <slot></slot>
    </span>

    <i v-if="iconRight && !loading" :class="iconRight" class="button-icon-right"></i>
  </button>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  type: {
    type: String,
    default: 'button'
  },
  variant: {
    type: String,
    default: 'solid', // solid, outline, ghost
    validator: (value) => ['solid', 'outline', 'ghost'].includes(value)
  },
  size: {
    type: String,
    default: 'md', // sm, md, lg
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  disabled: {
    type: Boolean,
    default: false
  },
  loading: {
    type: Boolean,
    default: false
  },
  iconLeft: {
    type: String,
    default: ''
  },
  iconRight: {
    type: String,
    default: ''
  },
  fullWidth: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['click']);

const buttonClasses = computed(() => [
  `primary-button--${props.variant}`,
  `primary-button--${props.size}`,
  {
    'primary-button--disabled': props.disabled,
    'primary-button--loading': props.loading,
    'primary-button--full-width': props.fullWidth
  }
]);

const handleClick = (event) => {
  if (!props.disabled && !props.loading) {
    emit('click', event);
  }
};
</script>

<style scoped lang="scss">
@import '@/Styles/design-tokens.scss';

.primary-button {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  font-family: var(--font-family-base);
  font-weight: var(--font-weight-medium);
  line-height: 1;
  text-align: center;
  white-space: nowrap;
  cursor: pointer;
  border: var(--border-width-medium) solid transparent;
  transition: var(--transition-colors), var(--transition-transform);
  user-select: none;
  outline: none;

  &:focus-visible {
    box-shadow: var(--focus-ring);
  }

  /* ==================== Sizes ==================== */
  &--sm {
    height: var(--size-button-sm);
    padding: 0 var(--space-3);
    font-size: var(--font-size-xs);
    border-radius: var(--border-radius-md);

    .button-icon-left,
    .button-icon-right {
      font-size: var(--size-icon-xs);
    }
  }

  &--md {
    height: var(--size-button-md);
    padding: 0 var(--space-4);
    font-size: var(--font-size-sm);
    border-radius: var(--border-radius-lg);

    .button-icon-left,
    .button-icon-right {
      font-size: var(--size-icon-sm);
    }
  }

  &--lg {
    height: var(--size-button-lg);
    padding: 0 var(--space-6);
    font-size: var(--font-size-base);
    border-radius: var(--border-radius-xl);

    .button-icon-left,
    .button-icon-right {
      font-size: var(--size-icon-md);
    }
  }

  /* ==================== Variants ==================== */

  /* Solid Variant */
  &--solid {
    background: linear-gradient(135deg, var(--color-primary-600) 0%, var(--color-primary-700) 100%);
    color: var(--color-text-inverse);
    border-color: transparent;
    box-shadow: var(--shadow-sm);

    &:hover:not(.primary-button--disabled):not(.primary-button--loading) {
      background: linear-gradient(135deg, var(--color-primary-700) 0%, var(--color-primary-800) 100%);
      box-shadow: var(--shadow-md);
      transform: translateY(-1px);
    }

    &:active:not(.primary-button--disabled):not(.primary-button--loading) {
      transform: translateY(0);
      box-shadow: var(--shadow-sm);
    }
  }

  /* Outline Variant */
  &--outline {
    background: var(--color-background);
    color: var(--color-primary-600);
    border-color: var(--color-primary-600);

    &:hover:not(.primary-button--disabled):not(.primary-button--loading) {
      background: var(--color-primary-50);
      border-color: var(--color-primary-700);
      color: var(--color-primary-700);
    }

    &:active:not(.primary-button--disabled):not(.primary-button--loading) {
      background: var(--color-primary-100);
    }
  }

  /* Ghost Variant */
  &--ghost {
    background: transparent;
    color: var(--color-primary-600);
    border-color: transparent;

    &:hover:not(.primary-button--disabled):not(.primary-button--loading) {
      background: var(--color-primary-50);
      color: var(--color-primary-700);
    }

    &:active:not(.primary-button--disabled):not(.primary-button--loading) {
      background: var(--color-primary-100);
    }
  }

  /* ==================== States ==================== */

  &--disabled {
    cursor: not-allowed;
    opacity: 0.5;
    pointer-events: none;
  }

  &--loading {
    cursor: wait;
    pointer-events: none;

    .button-text {
      opacity: 0.6;
    }
  }

  &--full-width {
    width: 100%;
  }

  /* ==================== Icons ==================== */

  .button-icon-left {
    display: flex;
    align-items: center;
    margin-right: calc(var(--space-1) * -1);
  }

  .button-icon-right {
    display: flex;
    align-items: center;
    margin-left: calc(var(--space-1) * -1);
  }

  /* ==================== Loading Spinner ==================== */

  .button-spinner {
    position: absolute;
    left: var(--space-3);
    display: flex;
    align-items: center;
  }

  .spinner-icon {
    width: 1em;
    height: 1em;
    animation: spin 0.8s linear infinite;
  }

  .spinner-circle {
    fill: none;
    stroke: currentColor;
    stroke-width: 3;
    stroke-linecap: round;
    stroke-dasharray: 50;
    stroke-dashoffset: 25;
    animation: spinner-dash 1.5s ease-in-out infinite;
  }

  @keyframes spin {
    to {
      transform: rotate(360deg);
    }
  }

  @keyframes spinner-dash {
    0% {
      stroke-dasharray: 1, 200;
      stroke-dashoffset: 0;
    }
    50% {
      stroke-dasharray: 100, 200;
      stroke-dashoffset: -50;
    }
    100% {
      stroke-dasharray: 100, 200;
      stroke-dashoffset: -150;
    }
  }
}

/* Responsive Adjustments */
@media (max-width: 768px) {
  .primary-button {
    &--md {
      height: 2.25rem;
      padding: 0 var(--space-3);
      font-size: var(--font-size-xs);
    }

    &--lg {
      height: 2.5rem;
      padding: 0 var(--space-4);
      font-size: var(--font-size-sm);
    }
  }
}
</style>
