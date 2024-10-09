<template>
  <div class="pagination-controls">
    <ul class="pagination">
      <li v-for="page in filteredPages" :key="page" class="p-0" @click.prevent="setItemsPerPage(page)">
        <a href="#" :itemsPerPage="itemsPerPage" :class="{ active: page === itemsPerPage }">{{ page }}</a>
      </li>
      <li v-if="props.currentRecords < props.totalRecords" class="more" @click="itemsIncrease()">more..</li>
    </ul>
  </div>
  <div>
    <span class="totalcount text-secondary">{{ props.currentRecords }} /
      <span class="fw-bold">{{ props.totalRecords }}</span> records</span>
  </div>
</template>

<script setup>
import { ref, watch, defineEmits, defineProps, computed } from "vue";

const props = defineProps({
  currentRecords: {
    type: Number,
    required: true,
  },
  totalRecords: {
    type: Number,
    required: true,
  },
  tab_name: String
});

const itemsPerPage = ref(100);
const newpages = ref([100, 200, 500]);
const emit = defineEmits(["updateValue", "limitStart"]);
const start = ref(0);

const filteredPages = computed(() => {
  return newpages.value.filter(page => page <= props.totalRecords);
});

// page size changes
const setItemsPerPage = (page) => {
  itemsPerPage.value = page;
  start.value = 0;
  emit("updateValue", itemsPerPage.value);
};

// load more items
const itemsIncrease = () => {
  start.value += itemsPerPage.value;
  emit("limitStart", [itemsPerPage.value, start.value]);
};

// watch currentRecords
watch(() => props.currentRecords, (newVal, oldVal) => {
  console.log(`Current records changed from ${oldVal} to ${newVal}`);
});
// watch(() => props.tab_name, (newVal, oldVal) => {
//   if (newVal !== oldVal) {
//     itemsPerPage.value = 100;
//     start.value = 0;
//     emit("updateValue", itemsPerPage.value);
//   }
// });

</script>
<!-- Styles -->
<style scoped></style>
