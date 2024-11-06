<template>
    <div>
        <HeaderComp />

        <div class="container-fluid">
            <div class="row">
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
import { computed } from 'vue';
import HeaderComp from '../../Components/HeaderComp.vue'
import SideBar from '../../Components/SideBar.vue'
// Get current route
const route = useRoute();

// Check if the current route is '/archived'
const isArchivedRoute = computed(() => route.path.startsWith('/dashboard'));


</script>