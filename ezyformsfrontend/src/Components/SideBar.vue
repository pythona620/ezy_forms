<template>
    <div class="">
        <div :class="['sidebar', { collapsed: props.collapsed }]">
            <!-- Title for the overall sidebar -->
            <div class="d-flex justify-content-between align-items-center ">
                <h1 class="font-12 m-0 text-muted ps-2 d-none d-md-inline " v-if="!collapsed">{{ sidebarTitle }} 
            </h1>
               <button class="btn border me-2 ms-2 toggle-btn d-none d-md-inline" type="button" @click="toggleSidebar">
                    <i v-if="!collapsed" class="bi bi-chevron-double-left fs-6"></i>
                    <i v-if="collapsed" class="bi bi-chevron-double-right fs-6"></i>
                </button>
            </div>

            <aside class="mt-1">
                <!-- Settings section title for first group -->
                <template v-if="isSettingsRoute">
                    <h2 class="font-10 m-0 text-muted ps-2" v-if="!collapsed">{{ firstSettingsTitle }}</h2>
                    <ul class="list-unstyled">
                        <router-link v-for="(list, index) in firstSettingsGroup" :key="index"
                            :to="`${baseRoute}/${list.route.toLowerCase()}`" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li>
                                <i v-tooltip.right="list.name" :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                                <span v-if="!collapsed"  class="d-none d-md-inline">{{ list.name }}</span>
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
                                <span v-if="!collapsed"  class="d-none d-md-inline">{{ list.name }}</span>
                            </li>
                        </router-link>
                    </ul> -->
                    <h2 v-if="filteredSettingsGroups.thirdSettingsGroup.length && !collapsed" class="font-10 m-0 text-muted ps-2">{{
                        thirdSettingsTitle }}</h2>
                    <ul class="list-unstyled" v-if="filteredSettingsGroups.thirdSettingsGroup.length">
                        <router-link v-for="(list, index) in filteredSettingsGroups.thirdSettingsGroup" :key="index"
                            :to="`${baseRoute}/${list.route.toLowerCase()}`" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li>
                                <i v-tooltip.right="list.name" :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                                <span v-if="!collapsed"  class="d-none d-md-inline">{{ list.name }}</span>
                            </li>
                        </router-link>
                    </ul>
                    <h2 v-if="filteredSettingsGroups.forthSettingsGroup.length && !collapsed" class="font-10 m-0 text-muted ps-2">{{
                        forthSettingsTitle }}</h2>
                    <ul class="list-unstyled" v-if="filteredSettingsGroups.forthSettingsGroup.length">
                        <router-link v-for="(list, index) in filteredSettingsGroups.forthSettingsGroup" :key="index"
                            :to="`${baseRoute}/${list.route.toLowerCase()}`" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li>
                                <i v-tooltip.right="list.name" :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                                <span v-if="!collapsed"  class="d-none d-md-inline">{{ list.name }}</span>
                            </li>
                        </router-link>
                    </ul>

                    <h2 v-if="filteredSettingsGroups.fifthSettingsGroup && !collapsed" class="font-10 m-0 text-muted ps-2">{{
                        fifthSettingsTitle }}</h2>
                    <ul class="list-unstyled" v-if="filteredSettingsGroups.fifthSettingsGroup">
                        <router-link v-for="(list, index) in filteredSettingsGroups.fifthSettingsGroup" :key="index"
                            :to="`${baseRoute}/${list.route.toLowerCase()}`" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li>
                                <i v-tooltip.right="list.name" :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                                <span v-if="!collapsed"  class="d-none d-md-inline">{{ list.name }}</span>
                            </li>
                        </router-link>
                    </ul>

                    <h2 v-if="filteredSettingsGroups.sixthGroup && !collapsed" class="font-10 m-0 text-muted ps-2">{{
                        sixthTitle }}</h2>
                    <ul class="list-unstyled" v-if="filteredSettingsGroups.sixthGroup">
                        <router-link v-for="(list, index) in filteredSettingsGroups.sixthGroup" :key="index"
                            :to="`${baseRoute}/${list.route.toLowerCase()}`" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li>
                                <i v-tooltip.right="list.name" :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                                <span v-if="!collapsed"  class="d-none d-md-inline">{{ list.name }}</span>
                            </li>
                        </router-link>
                    </ul>
                    
                    <h2 v-if="filteredSettingsGroups.seventhGroup && !collapsed" class="font-10 m-0 text-muted ps-2">{{
                        seventhSettingsTitle }}</h2>
                    <ul class="list-unstyled" v-if="filteredSettingsGroups.seventhGroup">
                        <router-link v-for="(list, index) in filteredSettingsGroups.seventhGroup" :key="index"
                            :to="`${baseRoute}/${list.route.toLowerCase()}`" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li>
                                <i v-tooltip.right="list.name" :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                                <span v-if="!collapsed"  class="d-none d-md-inline">{{ list.name }}</span>
                            </li>
                        </router-link>
                    </ul>

                    <h2 v-if="filteredSettingsGroups.eightGroup && !collapsed" class="font-10 m-0 text-muted ps-2">{{
                        eightSettingsTitle }}</h2>
                    <ul class="list-unstyled" v-if="filteredSettingsGroups.eightGroup">
                        <router-link v-for="(list, index) in filteredSettingsGroups.eightGroup" :key="index"
                            :to="`${baseRoute}/${list.route.toLowerCase()}`" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li>
                                <i v-tooltip.right="list.name" :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                               <span v-if="!collapsed"  class="d-none d-md-inline">{{ list.name }}</span>
                            </li>
                        </router-link>
                    </ul>

                    <h2 v-if="filteredSettingsGroups.ninthGroup && !collapsed" class="font-10 m-0 text-muted ps-2">{{
                        ninthSettingsTitle }}</h2>
                    <ul class="list-unstyled" v-if="filteredSettingsGroups.ninthGroup">
                        <router-link v-for="(list, index) in filteredSettingsGroups.ninthGroup" :key="index"
                            :to="`${baseRoute}/${list.route.toLowerCase()}`" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li>
                                <i v-tooltip.right="list.name" :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                                <span v-if="!collapsed"  class="d-none d-md-inline">{{ list.name }}</span>
                            </li>
                        </router-link>
                    </ul>

                    <h2 v-if="filteredSettingsGroups.tenthGroup && !collapsed" class="font-10 m-0 text-muted ps-2">{{
                        tenthSettingsTitle }}</h2>
                    <ul class="list-unstyled" v-if="filteredSettingsGroups.tenthGroup">
                        <router-link v-for="(list, index) in filteredSettingsGroups.tenthGroup" :key="index"
                            :to="`${baseRoute}/${list.route.toLowerCase()}`" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li>
                                <i v-tooltip.right="list.name" :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                                <span v-if="!collapsed"  class="d-none d-md-inline">{{ list.name }}</span>
                            </li>
                        </router-link>
                    </ul>

                </template>
                <template v-if="isMasterRoute">
                    <ul class="list-unstyled">
                        <router-link :to="'/forms/department/allforms' ? '/forms/department/allforms' : '/forms/department/allforms'" class="text-decoration-none text-black"
                            active-class="active-link">
                            <li><i v-tooltip.right="'All Forms'" class="bi-icon fs-6 bi bi-file-earmark-richtext me-3"></i>All Forms</li>
                        </router-link>
                       
                        <router-link v-for="(department, index) in formSideBarData" :key="department.route"
                            :to="`/forms/department/${department.route}`" class="text-decoration-none text-black"
                            active-class="active-link">

                            <li>

                                <!-- <i :class="`bi-icon ps-1 bg-transparent ${department.icon} me-3`"></i> -->
                                <i v-tooltip.right="department.name" :class="[
                                    'bi-icon',
                                    'fs-6',
                                    'bg-transparent',

                                    iconClasses[index % iconClasses.length],
                                    'me-3',

                                ]"></i>

                                {{ department.name }}
                            </li>
                        </router-link>
                         <router-link v-if="VendorComparison" to="/settings/vendorcomparison" class="text-decoration-none text-black">
                            <li><i v-tooltip.right="'Vendor'" class="bi-icon fs-6 bi bi-file-earmark-richtext me-3"></i>Vendor Comparison</li>
                        
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
                            <li>
                                <i v-tooltip.right="list.name" :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                                <span v-if="!collapsed"  class="d-none d-md-inline">{{ list.name }}</span>
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

const props = defineProps({
  collapsed: Boolean
})

const emit = defineEmits(['toggleSidebar'])

const toggleSidebar = () => {
  emit('toggleSidebar')
}

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
    { name: 'Activity Log', icon: 'bi bi-clock-history', route: 'activitylog' },
    { name: 'Audit Log', icon: 'bi bi-clock', route: 'auditlog' },
    { name: 'Email Queue' , icon: 'bi bi-file-earmark-text', route: 'emailqueue' },
    { name: 'Form Creation' , icon: 'bi bi-file-earmark-text', route: 'CreateForm' },
    { name: 'Form Templates', icon: 'bi bi-file-earmark-text', route: 'predefinedforms' },
    // { name: 'Vendor Comparison', icon: 'bi bi-file-earmark-text', route: 'vendorcomparison' },
    { name: 'Acknowledgement' , icon: 'bi bi-file-earmark-text', route: 'acknowledgement' },
    { name: 'Email Template' , icon: 'bi bi-file-earmark-text', route: 'emailtemplate' },
    { name: 'Password Policy' , icon: 'bi bi-lock', route: 'passwordpolicy' },

    // {name: 'Roles',icon:' bi bi-people', route:'role'},
    // { name: 'Workflow Settings', icon: 'bi bi-gear', route: 'WorkflowSettings'}



];
// Define the title for the first and second settings sections
const firstSettingsTitle = 'My Details';
// const secondSettingsTitle = 'Workflow';
const thirdSettingsTitle = 'Master';
const forthSettingsTitle = 'Employee';

const fifthSettingsTitle = 'System Settings';
const sixthTitle = 'Audits';
const seventhSettingsTitle = 'Forms';
const eightSettingsTitle = 'Acknowledgement';
const ninthSettingsTitle = 'Email Template';
const tenthSettingsTitle = 'Password Policy';






const todoSideBarData = [
    { name: 'Assigned To Me', icon: 'bi bi-bucket', route: 'receivedform' },
    { name: 'My Requests', icon: 'bi bi-send', route: 'raisedbyme' },
    { name: 'My Team Requests', icon: 'bi bi-people', route: 'myteam' },
    { name: 'My Approvals', icon: 'bi bi-clock-history', route: 'history' },
    { name: 'Reports', icon: 'bi bi-gear', route: 'reports'},
    { name: 'insights', icon: 'bi-graph-up', route: 'insights'},

];
const userFormSideBarData = [
    { name: 'Created', icon: 'bi bi-file-earmark-plus', route: 'created' },
    { name: 'Draft', icon: 'bi bi-file-earmark-text', route: 'draft' },
    { name: 'Trash', icon: 'bi bi-trash3', route: 'trash' },
];

const filteredSideBarData = computed(() => {
    return todoSideBarData.filter(item => {  
        if (item.name === "My Team") {
            return is_admin.value == 1;
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
    return is_admin.value == 1
        ? {
            thirdSettingsGroup: settingsSideBarData.slice(1, 3),
            forthSettingsGroup: settingsSideBarData.slice(3, 6),
            fifthSettingsGroup: settingsSideBarData.slice(6,7),
            sixthGroup: settingsSideBarData.slice(7,10),
            seventhGroup: settingsSideBarData.slice(10,12),
            eightGroup: settingsSideBarData.slice(12,13),
            ninthGroup: settingsSideBarData.slice(13,14),
            tenthGroup: settingsSideBarData.slice(14),


        }
        : { thirdSettingsGroup: [], forthSettingsGroup: []};
});

// Define the title based on the current route
const sidebarTitle = computed(() => {
    if (isMasterRoute.value) {
        return 'Departments';
    } else if (isToDoRoute.value) {
        return 'Requests';
    } else if (isUserFormsRoute.value) {
        return 'Forms';
    }else if (isSettingsRoute.value) {
        return 'Settings';
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
const is_admin = ref('');
const VendorComparison=ref("");

onMounted(() => {
    // gettingDepartmentNames()
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
            is_admin.value = userData.is_admin || '';
            

        }
    } else {
        console.warn("No user data found in localStorage.");
    }
})

// function deptData() {
//     const filters = [
//         ["business_unit", "=", `${newBusinessUnit.value.business_unit}`]
//     ];
//     const queryParams = {
//         fields: JSON.stringify(["*"]),
//         limit_page_length: filterObj.value.limitPageLength,
//         limitstart: filterObj.value.limitstart,
//         filters: JSON.stringify(filters),

//         order_by: "`tabEzy Departments`.`department_name` asc",

//     };

//     axiosInstance.get(apis.resource + doctypes.departments, { params: queryParams })
//         .then((res) => {
//             if (res.data) {
//                 deptartmentData.value = res.data;


//                 formSideBarData.value = deptartmentData.value
//                     .sort((a, b) => a.department_name.localeCompare(b.department_name))
//                     .map(department => ({
//                         name: department.department_name,
//                         route: department.name,
//                     }));


//             }
//         })
//         .catch((error) => {
//             console.error("Error fetching department data:", error);
//         });
// }
function gettingDepartmentNames(){
   let dataObj = {
        business_unit: newBusinessUnit.value.business_unit
    };
   

   axiosInstance
    .post(apis.DepartmentNames,dataObj)
    .then((response) => {
            deptartmentData.value = response.message;
                formSideBarData.value = deptartmentData.value
                    .sort((a, b) => a.department_name.localeCompare(b.department_name))
                    .map(department => ({
                        name: department.department_name,
                        route: department.name,
                    }));

                    VendorComparison.value = sessionStorage.getItem("VendorComparison") === "true";
    })
    .catch((error) => {
      console.log(error);
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
            gettingDepartmentNames();
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
.sidebar li {
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
    /* font-weight: var(--font-weight-normal); */
    text-align: left;
    color: #DC3E45;
    font-weight: 500;
    font-size: var(--twelve);
    
    /* font-size: var(--thirteen); */
    /* line-height: 26px; */
    /* border-radius: 4px; */

    /* margin: 0px 0px 0px 11px; */
}

.bi-icon {
    font-size: var(--sixteen);
}

.sidebar {
    height: 90dvh;
    background-color: var(--sidebar-color);
    padding-top: 12px;
    /* border-radius: 10px;  */
    overflow-y: auto;
    overflow-x: hidden;
    /* box-shadow: 4px 0 4px -2px #00000040; */

}

.active-link>li {
    background-color: var(--white-color);
    color: #DC3E45;
    font-size: var(--thirteen);
    font-weight: var(--font-weight-medium);
    line-height: 26px;
    text-align: left;
    border-radius: 0px;
    border-left: 5px solid #DC3E45;
    




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

.sidebar {
  transition: all 0.3s ease;
}

.sidebar.collapsed {
  width: 44px;
}
.sidebar.collapsed li {
  overflow: visible;
  text-overflow: unset !important;
}

.sidebar li {
  white-space: nowrap;
}

.sidebar li i {
  width: 24px;
}
.toggle-btn{
  padding: 0px 4px;
  border-radius: 15px;
  color: black !important;
  font-weight: bold !important;
  height: 33px;
}
.sidebar {
  overflow: auto;
}

/* WebKit Browsers */
.sidebar::-webkit-scrollbar {
  width: 6px;
  height: 6px;
}

/* Track */
.sidebar::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px rgb(216, 216, 216);
  border-radius: var(--border-radius-lg);
  margin-top: 15px;
  background: transparent; /* keep it clean */
}

/* Thumb hidden by default */
.sidebar::-webkit-scrollbar-thumb {
  background: transparent;
  border-radius: var(--border-radius-lg);
}

/* Show styled thumb on hover */
.sidebar:hover::-webkit-scrollbar-thumb {
  background: #e2e2e2;
}

/* Thumb hover effect */
.sidebar:hover::-webkit-scrollbar-thumb:hover {
  background: var(--black-color);
}

/* Firefox */
.sidebar {
  scrollbar-width: thin;
  scrollbar-color: transparent transparent; /* hidden by default */
}

.sidebar:hover {
  scrollbar-color: #e2e2e2 transparent; /* visible on hover */
}


</style>
