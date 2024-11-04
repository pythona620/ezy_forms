<template>
  <div>
    <LoaderPage v-if="loadValue"></LoaderPage>

    <HeaderComp />
    <div class="container-fluid">
      <div class="row">
        <div class="col-2 p-0">
          <SideBar />
        </div>
        <div class="col-10">
          <RouterView></RouterView>
        </div>
      </div>
    </div>



  </div>
</template>

<script setup>
import HeaderComp from './Components/HeaderComp.vue';
import LoaderPage from './Components/loader/LoaderPage.vue';
import SideBar from './Components/SideBar.vue';

</script>

<style>
@media (min-width: 1604px) and (max-width: 2400px) {
  .col-2 {
    width: 13.33%;

  }

  .col-10 {
    width: 85.777%
  }
}
</style>
