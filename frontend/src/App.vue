<template>
  <div>
    <LoaderPage v-if="loadValue"></LoaderPage>

    <HeaderComp headertext="WorkFlow Settings" />
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

<style></style>
