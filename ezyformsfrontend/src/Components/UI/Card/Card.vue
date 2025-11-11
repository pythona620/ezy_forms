<template>
  <div :class="cardClasses" class="card-component">
    <div v-if="$slots.header || title" class="card-header">
      <slot name="header">
        <h3 class="card-title">{{ title }}</h3>
      </slot>
      <div v-if="$slots.actions" class="card-actions">
        <slot name="actions"></slot>
      </div>
    </div>

    <div class="card-body" :class="{ 'card-body--padded': padded }">
      <slot></slot>
    </div>

    <div v-if="$slots.footer" class="card-footer">
      <slot name="footer"></slot>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  title: {
    type: String,
    default: ''
  },
  variant: {
    type: String,
    default: 'default',
    validator: (value) => ['default', 'bordered', 'elevated', 'flat'].includes(value)
  },
  padded: {
    type: Boolean,
    default: true
  },
  hoverable: {
    type: Boolean,
    default: false
  },
  clickable: {
    type: Boolean,
    default: false
  }
});

const cardClasses = computed(() => [
  `card--${props.variant}`,
  {
    'card--hoverable': props.hoverable,
    'card--clickable': props.clickable
  }
]);
</script>

<style scoped lang="scss">
@import '@/Styles/design-tokens.scss';

.card-component {
  display: flex;
  flex-direction: column;
  background: var(--color-surface);
  border-radius: var(--border-radius-xl);
  overflow: hidden;
  transition: var(--transition-normal);

  /* Variants */
  &.card--default {
    border: var(--border-width-thin) solid var(--color-border);
    box-shadow: var(--shadow-xs);
  }

  &.card--bordered {
    border: var(--border-width-medium) solid var(--color-border);
  }

  &.card--elevated {
    border: none;
    box-shadow: var(--shadow-lg);
  }

  &.card--flat {
    border: none;
    background: var(--color-background-secondary);
  }

  /* States */
  &.card--hoverable {
    &:hover {
      box-shadow: var(--shadow-xl);
      transform: translateY(-2px);
    }
  }

  &.card--clickable {
    cursor: pointer;

    &:hover {
      box-shadow: var(--shadow-lg);
      border-color: var(--color-primary-300);
    }

    &:active {
      transform: scale(0.98);
    }
  }

  /* Header */
  .card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-4) var(--space-5);
    border-bottom: var(--border-width-thin) solid var(--color-border);
    background: var(--color-background-secondary);
  }

  .card-title {
    margin: 0;
    font-size: var(--font-size-lg);
    font-weight: var(--font-weight-semibold);
    color: var(--color-text-primary);
    line-height: var(--line-height-tight);
  }

  .card-actions {
    display: flex;
    align-items: center;
    gap: var(--space-2);
  }

  /* Body */
  .card-body {
    flex: 1;

    &.card-body--padded {
      padding: var(--space-5);
    }
  }

  /* Footer */
  .card-footer {
    padding: var(--space-4) var(--space-5);
    border-top: var(--border-width-thin) solid var(--color-border);
    background: var(--color-background-secondary);
  }
}

/* Responsive */
@media (max-width: 768px) {
  .card-component {
    border-radius: var(--border-radius-lg);

    .card-header,
    .card-body.card-body--padded,
    .card-footer {
      padding: var(--space-4);
    }

    .card-title {
      font-size: var(--font-size-base);
    }
  }
}
</style>
