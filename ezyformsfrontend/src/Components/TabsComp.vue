<template>
  <div class="tabs-div">
    <ul class="tab-list m-0 p-0">
      <li v-for="(tab, index) in tabs" :key="index" class="tab-item">
        <router-link :to="tab.route" :class="['tab-link', isActiveTab(tab) ? 'active-link' : '']"
          @click="passActiveTab(tab.name)">
          <i :class="tab.icon"></i> {{ tab.name }}
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
  // Check for `Forms` tab and any route that starts with `/forms/department/`
  if (tab.name === 'Forms') {
    return route.path.startsWith('/forms/department/');
  }

  // For all other tabs, check if the current route path starts with the tab route
  return route.path.startsWith(tab.route);
}
</script>





<style scoped>
a {
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
  text-decoration: none;
}

.active-link>a {
  background-color: var(--white-color);
  color: var(--text-color);
  font-size: var(--thirteen);
  font-weight: var(--font-weight-normal);
  border-bottom: 2px solid red;
  padding: 5px 0px;
  margin-top: 8px;


}


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

ul li a.active-link {
  border-bottom: 3px solid var(--text-color);
  padding-bottom: 5px;
  font-weight: 600;
  
}

ul li a.active-link i {
  font-weight: 900;
  color: black;
}
</style>