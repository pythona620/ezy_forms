<template>
    <div class="p-0">
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
        <!-- <RouterView /> -->
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
const isArchivedRoute = computed(() => route.path.startsWith('/archived'));

// Check if the current route is '/new/formsteps'
const isFormStepsRoute = computed(() => route.path.includes('/create-form/formsteps'));
</script>