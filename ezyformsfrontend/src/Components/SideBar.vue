<template>
    <div class="container-fluid">
        <div class="sidebar pt-2">
            <!-- Title for the overall sidebar -->
            <h1 class="font-12 m-0 text-muted ps-2">{{ sidebarTitle }}</h1>

            <aside class="mt-1">
                <!-- Settings section title for first group -->
                <template v-if="isSettingsRoute">
                    <h2 class="font-10 m-0 text-muted ps-2">{{ firstSettingsTitle }}</h2>
                    <ul class="list-unstyled">
                        <router-link v-for="(list, index) in firstSettingsGroup" :key="index"
                            :to="`${baseRoute}/${list.route.toLowerCase()}`" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li :title="list.name">
                                <i :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                                {{ list.name }}
                            </li>
                        </router-link>
                    </ul>

                    <!-- Settings section title for second group -->
                    <h2 class="font-10 m-0 text-muted ps-2 mt-3">{{ secondSettingsTitle }}</h2>
                    <ul class="list-unstyled">
                        <router-link v-for="(list, index) in secondSettingsGroup" :key="index"
                            :to="`${baseRoute}/${list.route.toLowerCase()}`" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li :title="list.name">
                                <i :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                                {{ list.name }}
                            </li>
                        </router-link>
                    </ul>
                    <h2 class="font-10 m-0 text-muted ps-2">{{ thirdSettingsTitle }}</h2>
                    <ul class="list-unstyled">
                        <router-link v-for="(list, index) in thirdSettingsGroup" :key="index"
                            :to="`${baseRoute}/${list.route.toLowerCase()}`" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li :title="list.name">
                                <i :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                                {{ list.name }}
                            </li>
                        </router-link>
                    </ul>
                    <h2 class="font-10 m-0 text-muted ps-2">{{ forthSettingsTitle }}</h2>
                    <ul class="list-unstyled">
                        <router-link v-for="(list, index) in forthSettingsGroup" :key="index"
                            :to="`${baseRoute}/${list.route.toLowerCase()}`" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li :title="list.name">
                                <i :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                                {{ list.name }}
                            </li>
                        </router-link>
                    </ul>
                </template>

                <!-- Other sidebar items if not on settings route -->
                <template v-else>
                    <ul class="list-unstyled">
                        <router-link v-for="(list, index) in sidebarData" :key="index"
                            :to="`${baseRoute}/${list.route.toLowerCase()}`" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li :title="list.name">
                                <i :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                                {{ list.name }}
                            </li>
                        </router-link>
                    </ul>
                </template>
            </aside>
        </div>
    </div>
</template>




<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router'; // Import the useRoute hook

// Define sidebar data for different routes
const formSideBarData = [
    { name: 'IT', icon: 'bi bi-display', route: 'it' },
    { name: 'F & B', icon: 'bi bi-cup-straw', route: 'f&b' },
    { name: 'Sales', icon: 'bi bi-bar-chart', route: 'sales' },
    { name: 'HR', icon: 'bi bi-people-fill', route: 'hr' },
    { name: 'Finance', icon: 'bi bi-wallet2', route: 'finance' },
    { name: 'Administration', icon: 'bi bi-building', route: 'admin' },
    { name: 'House keeping', icon: 'bi bi-bucket', route: 'housekeeping' },
    { name: 'Front office', icon: 'fa-solid fa-concierge-bell', route: 'frontoffice' },
    { name: 'Revenue', icon: 'bi bi-cash-stack', route: 'revenue' },
];

const settingsSideBarData = [
    { name: 'Profile', icon: 'bi bi-person-circle', route: 'profile' },
    { name: 'E-Signature', icon: 'bi bi-person-circle', route: 'esign' },
    { name: 'Role', icon: 'bi bi-shield-lock', route: 'role' },
    { name: 'Role Matrix', icon: 'bi bi-grid-3x3-gap', route: 'rolematrix' },
    { name: 'Work Flow', icon: 'bi bi-diagram-3', route: 'workflow' },
    { name: 'Notifications', icon: 'bi bi-bell', route: 'notifications' },
    { name: 'Department', icon: 'bi bi-clock-history', route: 'department' },
    { name: 'Designation', icon: 'bi bi-people', route: 'designations' },
    { name: 'User Management', icon: 'bi bi-people', route: 'usermanagement' },
    { name: 'Categories', icon: 'bi bi-tags', route: 'categories' },

];
// Define the title for the first and second settings sections
const firstSettingsTitle = 'My Details';
const secondSettingsTitle = 'Workflow';
const thirdSettingsTitle = 'Master';
const forthSettingsTitle = 'Form';



const todoSideBarData = [
    { name: 'Received for me', icon: 'bi bi-bucket', route: 'receivedform' },

    { name: 'Raised by me', icon: 'bi bi-send', route: 'raisedbyme' },
    { name: 'My team', icon: 'bi bi-microsoft-teams', route: 'myteam' },
    { name: 'History', icon: 'bi bi-clock-history', route: 'history' },

];
const userFormSideBarData = [
    { name: 'Created', icon: 'bi bi-file-earmark-plus', route: 'created' },
    { name: 'Draft', icon: 'bi bi-file-earmark-text', route: 'draft' },
    { name: 'Trash', icon: 'bi bi-trash3', route: 'trash' },
];


const route = useRoute();

// Determine if the current route is /forms, /settings, /todo, or /archived
const isMasterRoute = computed(() => route.path.startsWith('/forms'));
const isSettingsRoute = computed(() => route.path.startsWith('/settings'));
// const isArchivedRoute = computed(() => route.path.startsWith('/archived'));
const isToDoRoute = computed(() => route.path.startsWith('/todo'));
const isUserFormsRoute = computed(() => route.path.startsWith('/create-form'));
// Compute sidebar data based on the current route
const sidebarData = computed(() => {
    if (isMasterRoute.value) {
        return formSideBarData;
    } else if (isSettingsRoute.value) {
        return settingsSideBarData;
    } else if (isToDoRoute.value) {
        return todoSideBarData;
    } else if (isUserFormsRoute.value) {
        return userFormSideBarData;
    }
    return [];
});
const firstSettingsGroup = computed(() => settingsSideBarData.slice(0, 2)); // First 4 items
const secondSettingsGroup = computed(() => settingsSideBarData.slice(2, 6));
const thirdSettingsGroup = computed(() => settingsSideBarData.slice(6, 9)); // Remaining items
const forthSettingsGroup = computed(() => settingsSideBarData.slice(9));
// Define the title based on the current route
const sidebarTitle = computed(() => {
    if (isMasterRoute.value) {
        return 'Departments';
    } else if (isToDoRoute.value) {
        return 'Requests';
    } else if (isUserFormsRoute.value) {
        return 'Forms';
    }
    return '';
});


const baseRoute = computed(() => {
    if (isMasterRoute.value) {
        return '/forms';
    } else if (isSettingsRoute.value) {
        return '/settings';
    } else if (isToDoRoute.value) {
        return '/todo';
    } else if (isUserFormsRoute.value) {
        return '/create-form';
    }
    return '/';
});

</script>

<style scoped>
li {
    font-size: var(--twelve);
    font-weight: var(--font-weight-normal);
    color: var(--text-color);
    padding: 8px 0px;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
    margin: 0px 0px 0px 11px;
}

.bi-icon {
    font-size: var(--sixteen);
}

.sidebar {
    height: 93.5dvh;
    background-color: var(--sidebar-color);
    padding-top: 12px;

}

.active-link>li {
    background-color: var(--white-color);
    color: var(--text-color);
    font-size: var(--thirteen);
    font-weight: var(--font-weight-medium);
    line-height: 26px;
    text-align: left;
    border-radius: 4px;
    padding: 5px 0px;

}

.active-link>li:hover {
    background-color: var(--white-color);
    color: var(--black-color);
    font-size: var(--thirteen);
    font-weight: var(--font-weight-normal);
    line-height: 26px;
    text-align: left;
    border-radius: 4px;
}
</style>
