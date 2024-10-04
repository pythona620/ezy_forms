<template>
  <div class="tabs-div">
    <ul class="tab-list m-0 p-0">
      <!-- Loop through tabs and display the icon and tab name -->
      <li @click="passActiveTab(tab)" :class="{ active: activeTab === tab.name }" class="tab-item"
        v-for="(tab, index) in tabs" :key="index">
        <!-- Display icon and tab name -->
        <i :class="tab.icon"></i> {{ tab.name }}
      </li>
    </ul>
  </div>
</template>
<script setup>
import { defineProps, defineEmits } from "vue";

const emits = defineEmits(["activeTabValue"]);

const props = defineProps({
  tabs: {
    type: Array,
    required: true,
  },
  activeTab: {
    type: String,
    required: true,
  },
});

function passActiveTab(tab) {
  emits("activeTabValue", tab);
}
</script>

<style scoped>
ul {
  display: flex;
  align-items: center;
  gap: 25px;
  list-style: none;
}

li {
  font-size: 13px;
  color: var(--text-color);
  font-weight: var(--font-weight-normal);
  /* Default font weight */
  cursor: pointer;
  transition: all 0.1s ease-in-out;
  position: relative;
  display: flex;
  align-items: center;
  padding-bottom: 8px;
}

li i {
  margin-right: 8px;
  /* Space between icon and text */
}

/* Active state for the tab */
/* li.active {
  color: var(--text-color);
  font-weight: var(--font-weight-medium);
 
  border-bottom: 3px solid var(--text-color);

} */

/* Transition for the bottom border */
li::after {
  content: "";
  width: 100%;
  position: absolute;
  height: 2px;
  /* Default height */
  bottom: 3px;
  background: transparent;
  left: 0;
  transition: all 0.2s ease-in-out;
}

li.active::after {
  content: "";
  width: 100%;
  position: absolute;
  height: 4px;
  bottom: 0;
  color: var(--text-color);
  font-weight: var(--font-weight-medium);
  border-bottom: 3px solid var(--text-color);

}
</style>
