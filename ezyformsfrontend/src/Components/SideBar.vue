<template>
    <div class="container-fluid">
        <div class="sidebar pt-2">
            <h1 class="font-12 m-0 text-muted ps-2">{{ sidebarTitle }}</h1>
            <aside class="mt-1">
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
    { name: 'User Management', icon: 'bi bi-people', route: 'usermanagement' },
    { name: 'Work Flow', icon: 'bi bi-diagram-3', route: 'workflow' },
    { name: 'Role', icon: 'bi bi-shield-lock', route: 'role' },
    { name: 'Role Matrix', icon: 'bi bi-grid-3x3-gap', route: 'rolematrix' },
    { name: 'Categories', icon: 'bi bi-tags', route: 'categories' },
    { name: 'Notifications', icon: 'bi bi-bell', route: 'notifications' },
    { name: 'Activity Log', icon: 'bi bi-clock-history', route: 'activitylog' },
    { name: 'Profile', icon: 'bi bi-person-circle', route: 'profile' },
];

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
const isUserFormsRoute = computed(() => route.path.startsWith('/new'));
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

// Define the title based on the current route
const sidebarTitle = computed(() => {
    if (isMasterRoute.value) {
        return 'Departments';
    } else if (isSettingsRoute.value) {
        return 'Settings';
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
        return '/new';
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
