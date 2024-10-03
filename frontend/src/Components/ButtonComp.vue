<template>
  <button :disabled="disabled" :type="type" class="border-0 bg-danger">
    <i class="px-2" v-if="iconClass" :class="iconClass"></i>
    <span class="class-btn" v-if="name">{{ name }}</span>
    <span v-if="count !== null" class="ps-1 fw-bolder">( {{ count }} )</span>
    <i class="px-2" v-if="afterIconClass" :class="afterIconClass"></i>
  </button>
</template>

<script>
export default {
  props: {
    icon: {
      type: String,
    },
    count: {
      type: [Number, String],
      default: null,
    },
    afterIcon: {
      type: String,
    },
    name: {
      type: String,
    },
    type: {
      type: String,
      default: "button",
    },
    disabled: {
      type: Boolean,
    },
  },
  computed: {
    iconClass() {
      return this.icon ? `bi bi-${this.icon}` : null;
    },
    afterIconClass() {
      return this.afterIcon ? `bi bi-${this.afterIcon}` : null;
    },
  },
};
</script>

<style lang="scss">
button:disabled {
  opacity: 0.5;
}

button {
  height: 36px;
}

button:focus {
  outline: none;
}
</style>
