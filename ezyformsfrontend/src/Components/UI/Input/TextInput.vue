<template>
  <div class="text-input-wrapper" :class="wrapperClasses">
    <label v-if="label" :for="inputId" class="text-input-label">
      {{ label }}
      <span v-if="required" class="text-input-required">*</span>
    </label>

    <div class="text-input-container">
      <span v-if="iconLeft" class="text-input-icon text-input-icon--left">
        <i :class="iconLeft"></i>
      </span>

      <input
        :id="inputId"
        :type="type"
        :value="modelValue"
        :placeholder="placeholder"
        :disabled="disabled"
        :readonly="readonly"
        :required="required"
        :maxlength="maxLength"
        :minlength="minLength"
        :class="inputClasses"
        class="text-input"
        @input="handleInput"
        @blur="handleBlur"
        @focus="handleFocus"
        :aria-describedby="helpText ? `${inputId}-help` : undefined"
        :aria-invalid="hasError"
      />

      <span v-if="iconRight || clearable" class="text-input-icon text-input-icon--right">
        <i
          v-if="clearable && modelValue && !disabled"
          class="bi bi-x-circle text-input-clear"
          @click="handleClear"
          role="button"
          tabindex="0"
          :aria-label="`Clear ${label || 'input'}`"
        ></i>
        <i v-else-if="iconRight" :class="iconRight"></i>
      </span>
    </div>

    <div v-if="helpText || errorMessage" class="text-input-hint">
      <p
        v-if="!hasError && helpText"
        :id="`${inputId}-help`"
        class="text-input-help"
      >
        {{ helpText }}
      </p>
      <p
        v-if="hasError && errorMessage"
        :id="`${inputId}-error`"
        class="text-input-error"
      >
        <i class="bi bi-exclamation-circle"></i>
        {{ errorMessage }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue';

const props = defineProps({
  modelValue: {
    type: [String, Number],
    default: ''
  },
  label: {
    type: String,
    default: ''
  },
  type: {
    type: String,
    default: 'text',
    validator: (value) => ['text', 'email', 'password', 'url', 'tel', 'number', 'search'].includes(value)
  },
  placeholder: {
    type: String,
    default: ''
  },
  helpText: {
    type: String,
    default: ''
  },
  errorMessage: {
    type: String,
    default: ''
  },
  disabled: {
    type: Boolean,
    default: false
  },
  readonly: {
    type: Boolean,
    default: false
  },
  required: {
    type: Boolean,
    default: false
  },
  clearable: {
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
  size: {
    type: String,
    default: 'md',
    validator: (value) => ['sm', 'md', 'lg'].includes(value)
  },
  maxLength: {
    type: Number,
    default: null
  },
  minLength: {
    type: Number,
    default: null
  }
});

const emit = defineEmits(['update:modelValue', 'blur', 'focus', 'clear']);

const inputId = computed(() => `text-input-${Math.random().toString(36).substr(2, 9)}`);
const isFocused = ref(false);

const hasError = computed(() => !!props.errorMessage);

const wrapperClasses = computed(() => [
  `text-input-wrapper--${props.size}`,
  {
    'text-input-wrapper--disabled': props.disabled,
    'text-input-wrapper--readonly': props.readonly,
    'text-input-wrapper--error': hasError.value,
    'text-input-wrapper--focused': isFocused.value
  }
]);

const inputClasses = computed(() => [
  `text-input--${props.size}`,
  {
    'text-input--with-icon-left': props.iconLeft,
    'text-input--with-icon-right': props.iconRight || props.clearable,
    'text-input--error': hasError.value
  }
]);

const handleInput = (event) => {
  emit('update:modelValue', event.target.value);
};

const handleBlur = (event) => {
  isFocused.value = false;
  emit('blur', event);
};

const handleFocus = (event) => {
  isFocused.value = true;
  emit('focus', event);
};

const handleClear = () => {
  emit('update:modelValue', '');
  emit('clear');
};
</script>

<style scoped lang="scss">
@import '@/Styles/design-tokens.scss';

.text-input-wrapper {
  display: flex;
  flex-direction: column;
  gap: var(--space-2);
  width: 100%;

  /* Label */
  .text-input-label {
    display: block;
    font-size: var(--font-size-sm);
    font-weight: var(--font-weight-medium);
    color: var(--color-text-primary);
    line-height: var(--line-height-normal);
  }

  .text-input-required {
    color: var(--color-error-600);
    margin-left: var(--space-1);
  }

  /* Container */
  .text-input-container {
    position: relative;
    display: flex;
    align-items: center;
  }

  /* Input */
  .text-input {
    width: 100%;
    font-family: var(--font-family-base);
    font-weight: var(--font-weight-normal);
    color: var(--color-text-primary);
    background: var(--color-background);
    border: var(--border-width-thin) solid var(--color-border);
    transition: var(--transition-colors), var(--transition-transform);
    outline: none;

    &::placeholder {
      color: var(--color-text-tertiary);
    }

    &:hover:not(:disabled):not(:focus) {
      border-color: var(--color-border-hover);
    }

    &:focus {
      border-color: var(--color-border-focus);
      box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
    }

    &:disabled {
      background: var(--color-gray-100);
      color: var(--color-text-disabled);
      cursor: not-allowed;
    }

    &:read-only {
      background: var(--color-gray-50);
      cursor: default;
    }

    /* Sizes */
    &--sm {
      height: var(--size-input-sm);
      padding: 0 var(--space-3);
      font-size: var(--font-size-xs);
      border-radius: var(--border-radius-md);
    }

    &--md {
      height: var(--size-input-md);
      padding: 0 var(--space-4);
      font-size: var(--font-size-sm);
      border-radius: var(--border-radius-lg);
    }

    &--lg {
      height: var(--size-input-lg);
      padding: 0 var(--space-5);
      font-size: var(--font-size-base);
      border-radius: var(--border-radius-xl);
    }

    /* With Icons */
    &--with-icon-left {
      &.text-input--sm { padding-left: var(--space-8); }
      &.text-input--md { padding-left: var(--space-10); }
      &.text-input--lg { padding-left: var(--space-12); }
    }

    &--with-icon-right {
      &.text-input--sm { padding-right: var(--space-8); }
      &.text-input--md { padding-right: var(--space-10); }
      &.text-input--lg { padding-right: var(--space-12); }
    }

    /* Error State */
    &--error {
      border-color: var(--color-error-500);

      &:focus {
        border-color: var(--color-error-600);
        box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.1);
      }
    }
  }

  /* Icons */
  .text-input-icon {
    position: absolute;
    display: flex;
    align-items: center;
    justify-content: center;
    color: var(--color-text-tertiary);
    pointer-events: none;

    i {
      font-size: var(--size-icon-sm);
    }

    &--left {
      left: var(--space-3);
    }

    &--right {
      right: var(--space-3);
    }
  }

  .text-input-clear {
    cursor: pointer;
    pointer-events: all;
    color: var(--color-text-secondary);
    transition: var(--transition-colors);

    &:hover {
      color: var(--color-text-primary);
    }
  }

  /* Hints */
  .text-input-hint {
    display: flex;
    flex-direction: column;
    gap: var(--space-1);
  }

  .text-input-help {
    margin: 0;
    font-size: var(--font-size-xs);
    color: var(--color-text-secondary);
    line-height: var(--line-height-normal);
  }

  .text-input-error {
    display: flex;
    align-items: center;
    gap: var(--space-1);
    margin: 0;
    font-size: var(--font-size-xs);
    color: var(--color-error-600);
    line-height: var(--line-height-normal);

    i {
      font-size: var(--size-icon-xs);
      flex-shrink: 0;
    }
  }

  /* State Classes */
  &--focused {
    .text-input-icon {
      color: var(--color-primary-600);
    }
  }

  &--error {
    .text-input-icon {
      color: var(--color-error-600);
    }
  }
}
</style>
