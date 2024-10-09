<template>
  <div>
    <LoaderPage v-if="loadValue"></LoaderPage>

    <HeaderComp />
    <div class="container-fluid">
      <div class="row">
        <!-- Conditionally render the sidebar based on the current route -->
        <div class="col-2 p-0" v-if="!isArchivedRoute">
          <SideBar />
        </div>
        <div :class="[isArchivedRoute ? 'col-12' : 'col-10']">
          <RouterView></RouterView>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
import HeaderComp from './Components/HeaderComp.vue';
import LoaderPage from './Components/loader/LoaderPage.vue';
import SideBar from './Components/SideBar.vue';
import { computed } from 'vue';

// Import useRoute to get the current route
const route = useRoute();

// Check if the current route is "archived"
const isArchivedRoute = computed(() => route.path.startsWith('/archived'));
</script>

<style>
@media (min-width: 1604px) and (max-width: 2400px) {
  .col-2 {
    width: 13.33%;
  }

  .col-10 {
    width: 85.777%;
  }

  .col-12 {
    width: 100%;
  }
}
</style>
