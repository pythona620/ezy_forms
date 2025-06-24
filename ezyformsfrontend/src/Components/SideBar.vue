<template>
    <div class="">
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
                    <!-- <h2 class="font-10 m-0 text-muted ps-2 mt-3">{{ secondSettingsTitle }}</h2>
                    <ul class="list-unstyled">
                        <router-link v-for="(list, index) in secondSettingsGroup" :key="index"
                            :to="`${baseRoute}/${list.route.toLowerCase()}`" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li :title="list.name">
                                <i :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                                {{ list.name }}
                            </li>
                        </router-link>
                    </ul> -->
                    <h2 v-if="filteredSettingsGroups.thirdSettingsGroup.length" class="font-10 m-0 text-muted ps-2">{{
                        thirdSettingsTitle }}</h2>
                    <ul class="list-unstyled" v-if="filteredSettingsGroups.thirdSettingsGroup.length">
                        <router-link v-for="(list, index) in filteredSettingsGroups.thirdSettingsGroup" :key="index"
                            :to="`${baseRoute}/${list.route.toLowerCase()}`" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li :title="list.name">
                                <i :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                                {{ list.name }}
                            </li>
                        </router-link>
                    </ul>
                    <h2 v-if="filteredSettingsGroups.forthSettingsGroup.length" class="font-10 m-0 text-muted ps-2">{{
                        forthSettingsTitle }}</h2>
                    <ul class="list-unstyled" v-if="filteredSettingsGroups.forthSettingsGroup.length">
                        <router-link v-for="(list, index) in filteredSettingsGroups.forthSettingsGroup" :key="index"
                            :to="`${baseRoute}/${list.route.toLowerCase()}`" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li :title="list.name">
                                <i :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                                {{ list.name }}
                            </li>
                        </router-link>
                    </ul>

                    <h2 v-if="filteredSettingsGroups.fifthSettingsGroup" class="font-10 m-0 text-muted ps-2">{{
                        fifthSettingsTitle }}</h2>
                    <ul class="list-unstyled" v-if="filteredSettingsGroups.fifthSettingsGroup">
                        <router-link v-for="(list, index) in filteredSettingsGroups.fifthSettingsGroup" :key="index"
                            :to="`${baseRoute}/${list.route.toLowerCase()}`" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li :title="list.name">
                                <i :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                                {{ list.name }}
                            </li>
                        </router-link>
                    </ul>


                </template>
                <template v-if="isMasterRoute">
                    <ul class="list-unstyled">
                        <router-link :to="'/forms/department/allforms' ? '/forms/department/allforms' : '/forms/department/allforms'" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li><i class="bi-icon fs-6 bi bi-file-earmark-richtext me-3"></i>All Forms</li>
                        </router-link>
                        <router-link v-for="(department, index) in formSideBarData" :key="department.route"
                            :to="`/forms/department/${department.route}`" class="text-decoration-none text-black"
                            active-class="active-link">

                            <li>

                                <!-- <i :class="`bi-icon ps-1 bg-transparent ${department.icon} me-3`"></i> -->
                                <i :class="[
                                    'bi-icon',
                                    'fs-6',
                                    'bg-transparent',

                                    iconClasses[index % iconClasses.length],
                                    'me-3',

                                ]"></i>

                                {{ department.name }}
                            </li>
                        </router-link>

                    </ul>
                </template>
                <!-- Other sidebar items if not on settings route -->
                <template v-else>
                    <ul class="list-unstyled">
                        <router-link v-for="(list, index) in sidebarData" :key="index"
                            :to="`${baseRoute}/${list.route ? list.route.toLowerCase() : ''}`"
                            class="text-decoration-none text-black"
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
import { computed, onMounted, ref, watch } from 'vue';
import { useRoute, useRouter } from 'vue-router';
// import { useRoute } from 'vue-router'; // Import the useRoute hook
import axiosInstance from '../shared/services/interceptor';
import { apis, doctypes } from '../shared/apiurls';
import { EzyBusinessUnit } from "../shared/services/business_unit";
const businessUnit = computed(() => {
    return EzyBusinessUnit.value;
});
const newBusinessUnit = ref({
    business_unit: ''
})
const filterObj = ref({
    limitPageLength: 'None',
    limitstart: 0
});

const formSideBarData = ref([])
const settingsSideBarData = [
    { name: 'Profile', icon: 'bi bi-person-circle', route: 'profile' },
    // { name: 'E-Signature', icon: 'bi bi-person-circle', route: 'esign' },
    // { name: 'Role', icon: 'bi bi-shield-lock', route: 'role' },
    // { name: 'Role Matrix', icon: 'bi bi-grid-3x3-gap', route: 'rolematrix' },
    // { name: 'Work Flow', icon: 'bi bi-diagram-3', route: 'workflow' },
    // { name: 'Notifications', icon: 'bi bi-bell', route: 'notifications' },
    { name: 'Department', icon: 'bi bi-clock-history', route: 'department' },
    { name: 'Designation', icon: 'bi bi-people', route: 'designations' },
    { name: 'Active Employees', icon: 'bi bi-people', route: 'employee' },
    { name: 'Inactive Employees', icon: 'bi bi-people', route: 'inactiveEmployee' },
    { name: 'Employee Approvals', icon: 'bi bi-people', route: 'employeeapproval' },
    { name: 'System Settings', icon: 'bi bi-tags', route: 'authenticationpage' },
    // {name: 'Roles',icon:' bi bi-people', route:'role'},
    // { name: 'Workflow Settings', icon: 'bi bi-gear', route: 'WorkflowSettings'}



];
// Define the title for the first and second settings sections
const firstSettingsTitle = 'My Details';
// const secondSettingsTitle = 'Workflow';
const thirdSettingsTitle = 'Master';
const forthSettingsTitle = 'Employee';

const fifthSettingsTitle = 'System Settings';





const todoSideBarData = [
    { name: 'My Tasks', icon: 'bi bi-bucket', route: 'receivedform' },
    { name: 'My Forms', icon: 'bi bi-send', route: 'raisedbyme' },
    { name: 'My Team', icon: 'bi bi-people', route: 'myteam' },
    { name: 'History', icon: 'bi bi-clock-history', route: 'history' },
    { name: 'Reports', icon: 'bi bi-gear', route: 'reports'}

];
const userFormSideBarData = [
    { name: 'Created', icon: 'bi bi-file-earmark-plus', route: 'created' },
    { name: 'Draft', icon: 'bi bi-file-earmark-text', route: 'draft' },
    { name: 'Trash', icon: 'bi bi-trash3', route: 'trash' },
];

const filteredSideBarData = computed(() => {
    return todoSideBarData.filter(item => {  
        if (item.name === "My Team") {
            return userDesigination.value.includes("IT") || userDesigination.value.includes("HOD");
        }
        return true;
    });
});



const route = useRoute();
const router = useRouter();


// Determine if the current route is /forms, /settings, /todo, or /archived
const isMasterRoute = computed(() => route.path.startsWith('/forms'));
const isSettingsRoute = computed(() => route.path.startsWith('/settings'));
// const isArchivedRoute = computed(() => route.path.startsWith('/archived'));
const isToDoRoute = computed(() => route.path.startsWith('/todo'));
const isUserFormsRoute = computed(() => route.path.startsWith('/create-form'));
// Compute sidebar data based on the current route

const sidebarData = computed(() => {
    if (isMasterRoute.value) {
        return formSideBarData.value;
    } else if (isToDoRoute.value) {
        return filteredSideBarData.value;
    } else if (isUserFormsRoute.value) {
        return userFormSideBarData ;
    }
    return [];
});

const firstSettingsGroup = computed(() => settingsSideBarData.slice(0, 1)); // First 4 items
// const secondSettingsGroup = computed(() => settingsSideBarData.slice(2, 6));
// const thirdSettingsGroup = computed(() => settingsSideBarData.slice(1, 3)); // Remaining items
// const forthSettingsGroup = computed(() => settingsSideBarData.slice(3));

const filteredSettingsGroups = computed(() => {
    return userDesigination.value.toLowerCase().includes('it')
        ? {
            thirdSettingsGroup: settingsSideBarData.slice(1, 3),
            forthSettingsGroup: settingsSideBarData.slice(3, 6),
            fifthSettingsGroup: settingsSideBarData.slice(6)

        }
        : { thirdSettingsGroup: [], forthSettingsGroup: [] };
});

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


const deptartmentData = ref([])
const username = ref('');
const userAdmin = ref('');
const userDesigination = ref('');

onMounted(() => {
    // Retrieve data from localStorage
    const userData = JSON.parse(localStorage.getItem('employeeData'));
    const userName = JSON.parse(localStorage.getItem('UserName'));
    // const syetemmanger = JSON.parse(localStorage.getItem('systemManager'))
    if (userName) {
        // Set the username based on the UserName data, which is used to check if the user is Admin
        username.value = userName.full_name;

        if (userName.full_name === 'Administrator') {

            userAdmin.value = userName.full_name;
            // userInitial.value = userName.full_name.charAt(0).toUpperCase();
        } else if (userData) {
            // Non-admin login: Set both employee and user-specific data
            userAdmin.value = userName.full_name;
            // userInitial.value = userData.emp_name.charAt(0).toUpperCase() || userData.full_name.charAt(0).toUpperCase();
            // userEmail.value = userData.name;
            userDesigination.value = userData.designation || '';

        }
    } else {
        console.warn("No user data found in localStorage.");
    }
})

function deptData() {
    const filters = [
        ["business_unit", "like", `%${newBusinessUnit.value.business_unit}%`]
    ];
    const queryParams = {
        fields: JSON.stringify(["*"]),
        limit_page_length: filterObj.value.limitPageLength,
        limitstart: filterObj.value.limitstart,
        filters: JSON.stringify(filters),

        order_by: "`tabEzy Departments`.`department_name` asc",

    };

    axiosInstance.get(apis.resource + doctypes.departments, { params: queryParams })
        .then((res) => {
            if (res.data) {
                deptartmentData.value = res.data;


                formSideBarData.value = deptartmentData.value
                    .sort((a, b) => a.department_name.localeCompare(b.department_name))
                    .map(department => ({
                        name: department.department_name,
                        route: department.name,
                    }));


            }
        })
        .catch((error) => {
            console.error("Error fetching department data:", error);
        });
}
const iconClasses = [
    "bi-file-earmark-check",
    "bi-question-octagon",
    "bi-file-earmark-bar-graph",
    "bi-card-checklist",
    "bi-file-earmark-ruled",
    "bi-journal-x",
    "bi-clock-history",
    "bi-percent",

];
watch(
    [businessUnit, isMasterRoute],
    ([newBusinessUnitVal, isMaster]) => {
        newBusinessUnit.value.business_unit = newBusinessUnitVal;

        if (isMaster && newBusinessUnitVal.length) {
            deptData();
        }
    },
    { immediate: true }
);
// function getIconByDepartmentName(name) {
//     const icons = {

//         'Sales Department': 'bi bi-bar-chart',
//         'HR Department': 'bi bi-people-fill',

//     };
//     return icons[name] || 'bi bi-file';
// }

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
    padding: 5px 10px;

    /* margin: 0px 0px 0px 11px; */
}
li:hover {
    background-color: var(--white-color);
    color: var(--black-color);
    font-weight: var(--font-weight-normal);
    text-align: left;
    /* font-size: var(--thirteen); */
    /* line-height: 26px; */
    /* border-radius: 4px; */

    /* margin: 0px 0px 0px 11px; */
}

.bi-icon {
    font-size: var(--sixteen);
}

.sidebar {
    height: 93.5dvh;
    background-color: var(--sidebar-color);
    padding-top: 12px;
    border-radius: 10px;
    margin-top: 10px;
    overflow-y: auto;
    /* box-shadow: 4px 0 4px -2px #00000040; */

}

.active-link>li {
    background-color: var(--white-color);
    color: var(--text-color);
    font-size: var(--thirteen);
    font-weight: var(--font-weight-medium);
    line-height: 26px;
    text-align: left;
    border-radius: 6px;
    




}


.active-link>li:hover {
    background-color: var(--white-color);
    color: var(--black-color);
    font-size: var(--thirteen);
    /* font-weight: var(--font-weight-normal); */
    line-height: 26px;
    text-align: left;
    border-radius: 4px;
}
</style>
