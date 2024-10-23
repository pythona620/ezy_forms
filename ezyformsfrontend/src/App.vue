<template>
  <div>
    <!-- Conditionally show the loader -->
    <LoaderPage v-if="loadValue"></LoaderPage>

    <!-- Conditionally show the header and sidebar if not on '/new/formsteps' -->
    <HeaderComp v-if="!isFormStepsRoute" />

    <div class="container-fluid">
      <div class="row">
        <!-- Conditionally render the sidebar based on the current route -->
        <div class="col-2 p-0" v-if="!isFormStepsRoute && !isArchivedRoute">
          <SideBar />
        </div>

        <!-- Adjust column size based on route -->
        <div :class="[(isFormStepsRoute || isArchivedRoute) ? 'col-12' : 'col-10']">
          <RouterView></RouterView>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router';
import { computed } from 'vue';
import HeaderComp from './Components/HeaderComp.vue';
import LoaderPage from './Components/loader/LoaderPage.vue';
import SideBar from './Components/SideBar.vue';
import '@vueform/multiselect/themes/default.css';

// Get current route
const route = useRoute();

// Check if the current route is '/archived'
const isArchivedRoute = computed(() => route.path.startsWith('/archived'));

// Check if the current route is '/new/formsteps'
const isFormStepsRoute = computed(() => route.path.includes('/create-form/formsteps'));
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
