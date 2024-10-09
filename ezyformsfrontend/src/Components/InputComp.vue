<template>
  <div class="input-wrapper">
    <!-- <label :for="inputId">{{ label }}</label> -->
    <input
      class="form-control shadow-none"
      :type="inputType"
      :id="inputId"
      :style="{ width: width }"
      v-model="inputValue"
      @input="handleChange"
      :placeholder="placeholder"
      :required="required"
      :maxlength="maxlength"
      :minlength="minlength"
      :class="{ 'input-error': errorMessage }"
    />
    <span v-if="errorMessage" class="error">{{ errorMessage }}</span>
  </div>
</template>


<script>
export default {
  props: {
    modelValue: {
      type: [String, Number],
      default: "",
    },
    type: {
      type: String,
      default: "text",
    },
    placeholder: {
      type: String,
      default: "Enter text",
    },
    label: {
      type: String,
      default: "Label",
    },
    required: {
      type: Boolean,
      default: false,
    },
    maxlength: {
      type: Number,
      default: null,
    },
    minlength: {
      type: Number,
      default: null,
    },
    validationRules: {
      type: Object,
      default: () => ({}),
    },
    id: {
      type: String,
      default: null,
    },
    styles: {
      type: Object,
      required: false,
    },
    width: {
      type: String,
      default: "100%",
    },
  },
  data() {
    return {
      inputValue: this.modelValue,
      inputType: this.type,
      errorMessage: "",
    };
  },
  computed: {
    inputId() {
      return this.id || `input-${Math.random().toString(36).substr(2, 9)}`;
    },
  },
  watch: {
    inputValue(newValue) {
      this.$emit("update:modelValue", newValue);
      this.validateInput();
    },
  },
  methods: {
    handleChange(event) {
      this.inputValue = event.target.value;
      this.$emit("update:modelValue", this.inputValue);
    },
    validateInput() {
      this.errorMessage = "";

      if (this.required && !this.inputValue) {
        this.errorMessage = "This field is required";
        return;
      }

      if (this.maxlength && this.inputValue.length > this.maxlength) {
        this.errorMessage = `Maximum length is ${this.maxlength}`;
        return;
      }

      if (this.minlength && this.inputValue.length < this.minlength) {
        this.errorMessage = `Minimum length is ${this.minlength}`;
        return;
      }

      if (this.inputType === "email" && !this.isValidEmail(this.inputValue)) {
        this.errorMessage = "Invalid email address";
        return;
      }

      if (
        this.inputType === "password" &&
        !this.isValidPassword(this.inputValue)
      ) {
        this.errorMessage = "Password must be at least 8 characters";
        return;
      }

      if (this.inputType === "text" && !this.isValidText(this.inputValue)) {
        this.errorMessage = "Text must be at least 4 characters";
        return;
      }

      if (
        this.inputType === "datetime-local" &&
        !this.isValidDate(this.inputValue)
      ) {
        this.errorMessage = "Please select a valid date";
        return;
      }

      if (this.inputType === "file" && !this.inputValue) {
        this.errorMessage = "Please select a file";
        return;
      }
    },
    isValidEmail(email) {
      const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      return emailPattern.test(email);
    },
    isValidPassword(password) {
      return password.length >= 8;
    },
    isValidText(text) {
      return text.length >= 4;
    },
    isValidDate(date) {
      return !isNaN(Date.parse(date));
    },
  },
};
</script>

<style scoped>
/* input {
  font-size: 12px;
  font-family: "Poppins";
  padding: 0px 10px;

} */

/* label {
  font-size: 15px;
} */

.input-wrapper {
  display: flex;
  flex-direction: column;
}

.input-error {
  border-color: #e23744;
}

.error {
  color: #e23744;
  font-size: 0.875em;
}
</style>
