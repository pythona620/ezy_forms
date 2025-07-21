<template>
    <div>
        <HeaderComp @toggleSidebar="toggleSidebar" />
        <div class="container-fluid">
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