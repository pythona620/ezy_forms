<template>
    <div class="position-sticky top-0 stickyheader">
        <div class="container-fluid">
            <div class="headerbackgound mt-2">
                <div class="row">
                    <div class="col-2">
                        <div class="d-flex gap-2 p-2 align-items-center">
                            <div><img class="imgmix" src="../assets/favicon.jpg" /></div>
                            <div class="m-0">
                                <p class="font-13 m-0">EZY | Forms</p>
                            </div>
                        </div>
                    </div>
                    <div class="col-7">
                        <div class="mt-2">
                            <TabsComp :tabs="tabsData" @changeTab="handleTabChange" />
                        </div>
                    </div>
                    <div class="col-3">
                        <div class="d-flex gap-3 justify-content-end align-items-center m-0">
                            <div class="mb-1">
                                <ButtonComp class="btn-outline-primary text-nowrap font-10" name="Raise request" />
                            </div>
                            <div class="mt-1">
                                <FormFields tag="select" placeholder="" class="mb-3" name="roles" id="roles"
                                    :Required="false" v-model="business_unit" :options="EzyFormsCompanys" />
                            </div>
                            <div class="logooutbtn">
                                <div class="btn-group dropdown navbar-nav ms-auto">
                                    <button type="button" class="btn border-0 p-0 me-2 mt-0" data-bs-toggle="dropdown"
                                        aria-expanded="false">
                                        <img src="../assets/Image.svg" />
                                    </button>
                                    <ul class="dropdown-menu dropdown-menu-start">
                                        <li>
                                            <div class="d-flex justify-content-center align-items-center">
                                                <ButtonComp class="buttoncomp rounded-2" @click="logout()"
                                                    name="Log Out"></ButtonComp>
                                            </div>
                                        </li>
                                    </ul>
                                </div>

                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRouter } from 'vue-router'; // Import useRouter
import { apis, doctypes } from '../shared/apiurls';
import axiosInstance from '../shared/services/interceptor';
import ButtonComp from './ButtonComp.vue';
import FormFields from './FormFields.vue';
import TabsComp from './TabsComp.vue';
import { EzyBusinessUnit } from '../shared/services/business_unit';

const router = useRouter(); // Initialize router

// Define reactive variables
const tabsData = ref([
    { name: 'Dashboard', icon: 'bi bi-columns-gap', route: '/dashboard' },
    { name: 'To do', icon: 'fa-solid fa-list-check', route: '/todo' },
    { name: 'Forms', icon: 'fa-solid fa-clipboard', route: '/forms' },
    { name: 'Settings', icon: 'fa-solid fa-gear', route: '/settings' },
    { name: 'Archive', icon: 'bi bi-archive', route: '/archived' },
    { name: 'Form', icon: 'fa-solid fa-clipboard', route: '/create-form' }
]);

const business_unit = ref('');
const EzyFormsCompanys = ref([]);
const formSideBarData = ref([]);
const deptartmentData = ref([]);
function logout() {
    localStorage.removeItem('UserName');
    router.push({ path: '/' }).then(() => {
        window.location.reload();
    });
}
const ezyForms = () => {
    const queryParams = {
        fields: JSON.stringify(["*"]),
    };

    axiosInstance.get(apis.resource + doctypes.wfSettingEzyForms, {
        params: queryParams,
    }).then((res) => {
        if (res?.data?.length) {
            EzyFormsCompanys.value = res.data.map((company) => company.bu_code);
            if (EzyFormsCompanys.value.length) {
                business_unit.value = EzyFormsCompanys.value[0];
            }
        }
    }).catch((error) => {
        console.error("Error fetching ezyForms data:", error);
    });
};

watch(business_unit, (newBusinessUnit) => {
    EzyBusinessUnit.value = newBusinessUnit;
});

function deptData() {
    const queryParams = {
        fields: JSON.stringify(["*"]),
    };

    axiosInstance.get(apis.resource + doctypes.departments, { params: queryParams })
        .then((res) => {
            if (res.data) {
                deptartmentData.value = res.data;


                // Update tabsData with new route for Forms tab
                const newFormsRoute = deptartmentData.value.map(department =>
                    department.name.replace(/\s+/g, '-').toLowerCase()
                );


                if (newFormsRoute.length > 0) {
                    tabsData.value = tabsData.value.map(tab => {
                        if (tab.name === 'Forms') {
                            return { ...tab, route: `/forms/department/${newFormsRoute[0]}` };
                        }
                        return tab;
                    });
                }

                formSideBarData.value = deptartmentData.value.map(department => ({
                    route: department.name.replace(/\s+/g, '-').toLowerCase(),
                }));
            }
        })
        .catch((error) => {
            console.error("Error fetching department data:", error);
        });
}

// Handle tab change
const handleTabChange = (tab) => {
    router.push(tab.route);
};

onMounted(() => {
    ezyForms();
    deptData();
});
</script>

<style scoped>
.headerbackgound {
    height: 50px;
    background-color: var(--sidebar-color);

}

.logooutbtn {
    background-color: #D1D0FF !important;
    border-radius: 3px;
    width: 28px;
    height: 28px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 7px;
}



@media (min-width: 1604px) and (max-width: 2400px) {
    .col-3 {
        width: 27%;

    }

}

.stickyheader {
    z-index: 10;
}
</style>
