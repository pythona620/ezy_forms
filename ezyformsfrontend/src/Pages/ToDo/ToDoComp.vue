<template>
    <div>
        <HeaderComp @toggleSidebar="toggleSidebar" />
        <div class="container-fluid conatiner_top">
            <div class="row">
                <div :class="['p-0', isCollapsed ? 'col-auto' : 'col-2']">
                    <SideBar :collapsed="isCollapsed" @toggleSidebar="toggleSidebar" />
                </div>


                <div :class="isCollapsed ? 'col' : 'col-10'">

                    <RouterView></RouterView>
                </div>
            </div>
        </div>

    </div>

</template>
<script setup>

import HeaderComp from '../../Components/HeaderComp.vue'
import SideBar from '../../Components/SideBar.vue'
import { ref } from 'vue'

const isCollapsed = ref(false)

function toggleSidebar() {
  isCollapsed.value = !isCollapsed.value
}

</script>
<style lang="scss" scoped>
@media (max-width: 767.98px) {
  .conatiner_top {
    padding-top: 60px;   /* adjust for mobile header */
    padding-bottom: 60px; /* adjust for mobile nav */
  }
}

/* For tablet (md screens: 768px - 991px) */
// @media (min-width: 768px) and (max-width: 991.98px) {
//   body {
//     padding-top: 70px;  
//     padding-bottom: 70px; 
//   }
// }

/* For desktop (lg and above) - keep default, no extra padding */
@media (min-width: 992px) {
  .conatiner_top {
    padding-top: 0;
    padding-bottom: 0;
  }
}
</style>