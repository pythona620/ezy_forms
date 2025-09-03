<template>
  <div class="tabs-div">
    <ul class="tab-list m-0 p-0">
      <li v-for="(tab, index) in tabs" :key="index" class="tab-item">
        <router-link
          :to="tab.route"
          :class="['tab-link', isActiveTab(tab) ? 'active-link' : '']"
          @click="passActiveTab(tab.name)"
        >
          <i :class="tab.icon"></i>
          <span class=" ms-1">{{ tab.name }}</span>
        </router-link>
      </li>
    </ul>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";
import { useRoute } from "vue-router";

const emits = defineEmits(["activeTabValue"]);
const route = useRoute();

const props = defineProps({
  tabs: {
    type: Array,
    required: true,
  },
});

function passActiveTab(tab) {
  emits("activeTabValue", tab);
}

function isActiveTab(tab) {
  if (tab.name === "Forms") {
    return route.path.startsWith("/forms/department/");
  }
  return route.path.startsWith(tab.route);
}
</script>

<style scoped>
/* Tab list container */
ul.tab-list {
  display: flex;
  align-items: center;
  gap: 25px;
  list-style: none;
  padding: 0;
  margin: 0;
  overflow-x: auto; /* allow horizontal scroll if many tabs */
}

/* Each tab */
li.tab-item {
  display: flex;
  align-items: center;
  text-align: center;
}

/* Tab link */
.tab-link {
  font-size: 13px;
  color: var(--text-color);
  font-weight: var(--font-weight-normal);
  cursor: pointer;
  transition: all 0.2s ease-in-out;
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 5px 0;
  text-decoration: none;
  white-space: nowrap;
}

/* Active tab */
.tab-link.active-link {
  font-weight: 600;
  border-bottom: 3px solid var(--text-color);
  color: var(--text-color);
}

.tab-link.active-link i {
  font-weight: 900;
  color: black;
}

/* Icon spacing */
li i {
  margin-right: 8px;
}

/* === Mobile-specific styles === */
@media (max-width: 767px) {
  ul.tab-list {
    gap: 0;
    padding: 0 10px; /* Add starting and ending padding */
  }
  li.tab-item {
    flex: 1; /* each tab takes equal width */
  }
  li i {
    margin: 0;
  }
  .tab-link {
    flex-direction: column; /* icon on top */
    padding: 10px;
    margin-bottom: 5px;
  }
  .tab-link span {
    /* display: none;  */
    font-size: 11px;
  }
  
}

</style>
