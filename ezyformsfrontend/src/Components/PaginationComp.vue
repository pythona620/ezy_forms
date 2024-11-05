<template>
  <div class="pagination-controls">
    <ul class="pagination">
      <li v-for="page in filteredPages" :key="page" class="p-0" @click.prevent="setItemsPerPage(page)">
        <a href="#" :itemsPerPage="itemsPerPage" :class="{ active: page === itemsPerPage }">{{ page }}</a>
      </li>
      <li v-if="props.currentRecords < props.totalRecords" class="more" @click="itemsIncrease()">more..</li>
      <!-- v-if="props.currentRecords < props.totalRecords" -->
    </ul>
    <div>
      <span class="totalcount text-secondary">{{ props.currentRecords }} /
        <span class="fw-bold">{{ props.totalRecords }}</span> records</span>
    </div>
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
<style scoped>
.pagination-controls {
  display: flex;
  justify-content: space-between;
  width: 100%;
  /* max-width: 300px; */
  align-items: center;
}

.pagination .active {
  font-weight: bold;
}

.pagination-controls button {
  padding: 5px 10px;
  border: 1px solid #ccc;
}

.pagination-controls {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 100%;
}

ul.pagination {
  display: flex;
  padding: 0;
  margin: 0;
  list-style: none;
  background-color: #f4f5f6;
  border-radius: 8px;
}

ul.pagination li {
  display: inline;
  padding: 4px 7px !important;
  cursor: pointer;
  font-size: 14px;
}

ul.pagination li:last-child {
  border-radius: 0px 8px 8px 0px !important;
}

ul.pagination li:first-child {
  border-radius: 8px 0px 0px 8px !important;
}

ul.pagination li a {
  /* border-radius: 5px; */
  color: #ccc;
  text-decoration: none;
  /* background-color: #F4F5F6; */
  /* border: 1px solid black; */
}

ul.pagination li:has(a.active) {
  background-color: #ccc;
}

ul.pagination li:has(a.active):hover {
  background: grey !important;
}

ul.pagination li:has(a.active) a {
  color: white !important;
}

ul.pagination li:hover:not(.active) {
  background-color: #f4f5f6 !important;
}

button[disabled] {
  opacity: 0.6;
  cursor: not-allowed;
}

.more {
  color: var(--secondary);
}

.totalcount {
  font-size: 12px;
}
</style>
