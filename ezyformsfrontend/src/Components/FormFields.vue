<template>
  <div class=" position-relative">
    <!-- Input Field -->
    <label v-if="labeltext" class="form-check-label mb-2" :for="id">
      {{ labeltext }}
      <span v-if="validationStar === 'true' && !localModel" class="text-danger">*</span>
    </label>

    <div class="shadow-none"
      v-if="tag === 'input' && (type === 'text' || type === 'number' || type === 'email' || type === 'search')">
      <input :type="type" :placeholder="placeholder" :labeltext="labeltext" :name="name" :id="id" :min="min" :max="max"
        v-model="localModel" :required="Required" class="form-control  input-width" :class="{
      'border-end-0 shadow-none': type === ('text' || type === 'number' || type === 'email' || type === 'search') && icon && label,
    }" />
      <!-- <span v-if="(type === 'number' || type === 'email' || type === 'search') && icon"
        class="input-group-text pe-3 bg-white border-start-0">
        <i class="ri-search-line"></i>
      </span> -->
    </div>

    <!-- Select Field -->

    <div class="select-div date-field" v-if="type === 'date' && tag === 'input'">
      <p v-if="placeholder" class="fw-normal ps-2 m-0 text-secondary">{{ placeholder }}</p>
      <div class="input-wrapper w-100">
        <input :type="type" :placeholder="placeholder" :name="name" :id="id" v-model="localModel" :required="Required"
          :max="maxDate" class="form-control pe-3 shadow-none" />
        <span v-if="localModel" class="icon-wrapper" @click="clearDate"><i class="bi bi-x"></i></span>
      </div>
    </div>

    <div class="input-group select-dropdown shadow-none" v-if="tag === 'select'">
      <p class="fw-normal ps-2 m-0 text-secondary">{{ placeholder }}</p>
      <div class="dropdown w-100">
        <button class="btn btn-white dropdown-toggle w-100 border-0 font-12" type="button" id="dropdownMenuButton"
          data-bs-toggle="dropdown" aria-expanded="false">
          {{ selectedOption }}
        </button>
        <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton">
          <li v-for="(item, index) in options" :key="index">
            <a class="dropdown-item" href="#" @click.prevent="selectOption(item)">
              {{ item }}
            </a>
          </li>
        </ul>
      </div>
    </div>
    <div class="input-group select-selection shadow-none" v-if="tag === 'multiselect'">
      <p class="fw-normal ps-2 m-0 text-secondary">{{ placeholder }}</p>
      <select v-if="tag === 'multiselect'" class="form-select selectForm shadow-none border-0" :required="Required"
        multiple :name="name" :id="id" v-model="localModel">
        <!-- <option class="selectOption" value="" selected>All</option> -->
        <option class="selectOption" v-for="(item, index) in options" :key="index" :value="item">{{ item }}</option>
      </select>
    </div>

    <!-- Radio Buttons -->
    <div v-if="tag === 'radio'" :class="{ 'form-check flex-layout': isFlex, 'form-check one-by-one-layout': !isFlex }">
      <div v-for="(item, index) in options" :key="index" class="form-check-item">
        <label :for="`${id}-${index}`" class="form-check-label">
          <input type="radio" :name="name" :id="`${id}-${index}`" :value="item" v-model="localModel"
            class="form-check-input" />
          {{ item }}
        </label>
      </div>
    </div>


    <!-- Checkboxes -->
    <div v-if="tag === 'checkbox'" class="form-check">
      <div v-for="(item, index) in checkOptions" :key="index">
        <label :for="`${id}-${index}`" class="form-check-label">
          <input type="checkbox" :name="name" :id="`${id}-${index}`" :value="item" v-model="localModel"
            class="form-check-input" />
          {{ item }}
        </label>
      </div>
    </div>

    <!-- Toggle Switch -->
    <div v-if="tag === 'toggle'" class="form-check form-switch">
      <input type="checkbox" :name="name" :id="id" v-model="localModel" class="form-check-input" />
      <label class="form-check-label" :for="id">{{ placeholder }}</label>
    </div>
    <!-- dropdowns -->
    <div v-if="tag === 'dropdown'" class="form-group">
      <label :for="id">{{ labeltext }}</label>
      <select :id="id" :name="name" v-model="localModel" class="form-control">
        <option v-for="(option, index) in dropDownOptions" :key="index" :value="option">
          {{ option }}
        </option>
      </select>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref, watch, computed } from "vue";

const props = defineProps({
  type: {
    type: String,
  },
  isFlex: {
    type: Boolean,
    default: true,
  },
  tag: { type: String, required: true },
  options: { type: Array, default: () => [] },
  checkOptions: { type: Array, default: () => [] },
  dropDownOptions: { type: Array, default: () => [] },
  placeholder: { type: String },
  labeltext: { type: String },
  name: { type: String, required: true },
  id: { type: String, required: true },
  modelValue: { type: [String, Number, Boolean, Array, null], required: true },
  value: { type: String, default: "" },
  validation: String,
  Required: {
    type: Boolean,
  },
  min: Number,
  max: Number,
  icon: {
    type: Boolean,
    default: true,
  },
  label: {
    type: Boolean,
    default: false,
  },
  validationStar: {
    type: String
  }
});

const emit = defineEmits(["update:modelValue"]);

const localModel = ref(props.modelValue);
const selectedOption = ref(props.modelValue);

const selectOption = (option) => {
  selectedOption.value = option;
  emit('update:modelValue', option);
};

// Sync v-model with selected option
watch(() => props.modelValue, (newVal) => {
  selectedOption.value = newVal;
});
watch(
  () => props.modelValue,
  (newVal) => {
    localModel.value = newVal;
  }
);

watch(localModel, (newVal) => {
  emit("update:modelValue", newVal);
});

const clearDate = () => {
  localModel.value = "";
};

// const today = computed(() => {
//   const date = new Date();
//   const year = date.getFullYear();
//   const month = String(date.getMonth() + 1).padStart(2, '0');
//   const day = String(date.getDate()).padStart(2, '0');
//   return `${year}-${month}-${day}`;
// });
const maxDate = computed(() => {
  const today = new Date();
  const maxDate = new Date(today.setDate(today.getDate() + 31));
  const year = maxDate.getFullYear();
  const month = String(maxDate.getMonth() + 1).padStart(2, '0');
  const day = String(maxDate.getDate()).padStart(2, '0');
  return `${year}-${month}-${day}`;
});
</script>

<style lang="scss" scoped>
.form-check {
  margin-bottom: 10px;
}

.form-control:focus {
  border: 1px solid #0000005e;
  box-shadow: none;
  outline: none;
}

.input-height {
  height: 32px !important;
}

.form-select {
  font-size: var(--ten);
}

select {
  cursor: pointer;
}

.select-div {
  height: 32px;

  border: 1px solid #e2e2e2;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--whiteColor);
  cursor: pointer;

  input {

    cursor: pointer;
    font-size: var(--ten);
    font-weight: 400;
    border-left: none;
    border-right: none;

  }

  padding: 0px 3px;
  border-radius:var(--border-radius-sm);
}

.date-field {
  display: flex;
  justify-content: start;
}

.select-dropdown {
  border: 1px solid #e2e2e2;
  display: flex;
  align-items: center;
  // justify-content: center;
  padding: 0px 3px;
  border-radius: var(--border-radius-sm);
  background-color: var(--whiteColor);
  font-size: var(--twelve);
  // max-width: 247px;
  width: 100%;
}

.select-section {
  border: 1px solid #e2e2e2;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0px 3px;
  border-radius: var(--border-radius-sm);
  background-color: var(--whiteColor);
  font-size: var(--twelve);
  // max-width: 247px;
  width: 100%;

  input {
    width: auto;
    border: none;
    cursor: pointer;
    font-size: var(--twelve);

  }
}

.input-group-text {
  position: absolute;
  right: 0;
  border-end-end-radius: 8px;
  top: 0;
  padding: 3px 3px;
}

.flex-layout {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.one-by-one-layout {
  display: block;
  margin-bottom: 10px;
}

.input-group {
  height: 32px !important;
  flex-wrap: nowrap;
}

.form-check-label {
  margin-right: 15px;
  font-size: var(--thirteen);
}

.form-switch {
  display: flex;
  align-items: center;
}

.text-secondary {
  color: var(--secondary) !important;
  white-space: nowrap;
  overflow: visible;
  font-size: var(--ten);
}

// .selectForm .selectOption {
//   padding: 2px 4px !important;
// }

// .input-group {
//   .selectionForm {
//     .selectionOption {
//       padding: 8px 16px !important;
//     }
//   }
// }

.input-wrapper {
  position: relative;
}

.form-control {
  width: 100%;
  height: 32px;
  font-size: var(--thirteen);
  border-radius: 3px;
  // max-width: 200px;
}



// .calendar-icon {
//   position: absolute;
//   right: 0px;
//   font-size: 10px;
//   top: 54%;
//   transform: translateY(-50%);
//   cursor: pointer;
// }

// input[type="date"]::-webkit-calendar-picker-indicator {
//   font-size: 10px;
//   cursor: pointer;
//   position: absolute;
//   bottom: 0;
//   left: 0;
//   right: 0;
//   top: 0;
//   width: auto;
//   height: auto;
//   background-position: right;
//   background-size: 13px 13px;
// }
.icon-wrapper {
  position: absolute;
  right: 33px;
  top: 54%;
  transform: translateY(-50%);
  cursor: pointer;
}

.selectForm .selectOption {
  padding: 10px 0px !important;
  background-color: white;
  color: black;
}

/* Style selected option */
// .selectForm option:checked {
//   background-color: #444;
//   color: white;
// }
/* Hover effect */
.selectOption:hover {
  background-color: #333;
  color: white;
}


.dropdown-item {
  cursor: pointer;
}
</style>
