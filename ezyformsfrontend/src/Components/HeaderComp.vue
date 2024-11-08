<template>
    <div>

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
                                    <ButtonComp v-if="shouldShowButton" class="btn-outline-primary text-nowrap font-10"
                                        name="Raise request" data-bs-toggle="modal" data-bs-target="#riaseRequestModal"
                                        @click="raiseRequest" />

                                </div>
                                <div class="mt-1">
                                    <FormFields tag="select" placeholder="" class="mb-3" name="roles" id="roles"
                                        :Required="false" v-model="business_unit" :options="EzyFormsCompanys" />
                                </div>
                                <div class="logooutbtn">
                                    <div class="btn-group dropdown navbar-nav ms-auto">
                                        <button type="button" class="btn border-0 p-0 me-2 mt-0"
                                            data-bs-toggle="dropdown" aria-expanded="false">
                                            <!-- <img src="../assets/Image.svg" /> -->
                                            {{ userInitial }}
                                        </button>
                                        <ul class="dropdown-menu dropdown-menu-start">
                                            <li>
                                                <div class="d-flex justify-content-center align-items-center ">
                                                    <span class=" fw-bold font-13 p-2"> {{ userFullName }}</span>
                                                </div>
                                            </li>
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
            <!-- Modal -->
        </div>
        <div class="modal fade" id="riaseRequestModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
            aria-labelledby="riaseRequestModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-sm">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title font-14 fw-bold" id="riaseRequestModalLabel">Raise Request</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <!-- <FormFields tag="select" placeholder="Category" class="mb-3" name="roles" id="roles"
                            @change="changingCategory" :Required="false" :options="categoryOptions"
                            v-model="selectedData.selectedCategory" /> -->
                        <div class=" mb-2">
                            <label class="raise-label" for="">Category</label>
                            <Multiselect :options="categoryOptions" @change="changingCategory"
                                v-model="selectedData.selectedCategory" placeholder="Select" :multiple="false"
                                class="font-11" :searchable="true" />
                        </div>
                        <div class=" mb-2">
                            <label class="raise-label" for="">Form</label>
                            <Multiselect :options="formList" v-model="selectedData.selectedform" placeholder="Select"
                                :multiple="false" class="font-11" :searchable="true" />
                        </div>
                        <!-- <FormFields tag="select" placeholder="Form" class="mb-3" name="roles" id="roles"
                            :Required="false" :options="formList" v-model="selectedData.selectedform" /> -->
                    </div>
                    <div>
                        <div class=" d-flex justify-content-center align-items-center p-3">
                            <button class="btn btn-dark font-12 w-100" type="submit"
                                @click="raiseRequestSubmission">Raise
                                Request</button>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>

</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router'; // Import useRouter
import { apis, doctypes } from '../shared/apiurls';
import axiosInstance from '../shared/services/interceptor';
import ButtonComp from './ButtonComp.vue';
import FormFields from './FormFields.vue';
import TabsComp from './TabsComp.vue';
import Multiselect from "@vueform/multiselect";
import "@vueform/multiselect/themes/default.css";

import { EzyBusinessUnit } from "../shared/services/business_unit";
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

const selectedData = ref({
    selectedCategory: "",
    selectedform: ""
});

const route = useRoute(); // Initialize route to access route parameters
const categoryOptions = ref([])
const formList = ref([])
const business_unit = ref('');
const userInitial = ref('');

const userFullName = ref('');

const EzyFormsCompanys = ref([]);
const formSideBarData = ref([]);
const deptartmentData = ref([]);
const activeTab = ref('')
function logout() {
    localStorage.removeItem('UserName');
    router.push({ path: '/' }).then(() => {

    });
}
const props = defineProps(['id']);
onMounted(() => {
    ezyForms();
    // console.log(route, "================");
    activeTab.value = route.path
    const userData = JSON.parse(localStorage.getItem('UserName'));
    if (userData && userData.full_name) {
        userInitial.value = userData.full_name.charAt(0).toUpperCase();
        userFullName.value = userData.full_name.toUpperCase()
    }

});

const shouldShowButton = computed(() => {
    const pathsToMatch = ['/forms/department', '/todo'];
    return pathsToMatch.some(path => route.path.includes(path));
});
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
watch(business_unit, (newBu, oldBu) => {
    EzyBusinessUnit.value = newBu;
    localStorage.setItem("Bu", EzyBusinessUnit.value)

    if (oldBu) {
        deptData(true);
    } else {

        deptData();
    }
});


function deptData(value = null) {
    const filters = [
        ["business_unit", "like", `%${business_unit.value}%`]
    ];
    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify(filters),
    };

    axiosInstance.get(apis.resource + doctypes.departments, { params: queryParams })
        .then((res) => {
            if (res.data) {
                deptartmentData.value = res.data;

                // Update the route for the "Forms" tab with the first department's route
                const newFormsRoute = deptartmentData.value.length > 0
                    ? `/forms/department/${deptartmentData.value[0].name.replace(/\s+/g, '-').toLowerCase()}`
                    : '/forms';

                tabsData.value = tabsData.value.map(tab => {
                    if (tab.name === 'Forms') {
                        return { ...tab, route: newFormsRoute };
                    }
                    return tab;
                });


                formSideBarData.value = deptartmentData.value.map(department => ({
                    route: department.name.replace(/\s+/g, '-').toLowerCase(),
                }));

                if (value && activeTab.value.includes("/forms")) {
                    handleBuChange({ route: newFormsRoute })
                }

            }
        })
        .catch((error) => {
            console.error("Error fetching department data:", error);
        });
}
const employeeData = ref({});

function raiseRequest() {
    const storedData = localStorage.getItem("employeeData");
    if (storedData) {
        employeeData.value = JSON.parse(storedData);
        categoriesdata(employeeData.value.department);
    } else {
        console.error("No employee data found in local storage.");
    }
}
// watch(
//     () => selectedData.value.selectedCategory,
//     (newVal, oldVal) => {
//         if (newVal !== oldVal) {
//             changingCategory(newVal, oldVal);
//         }
//     }
// );

function changingCategory(value) {
    if (value) {
        const dataObj = {
            "role": value,
            "business_unit": EzyBusinessUnit.value
        };

        axiosInstance.post(apis.raiseFormdata, dataObj)
            .then((response) => {
                formList.value = response.message.list_of_roadmaps

            })
            .catch((error) => {
                console.error("Error fetching data:", error);
            });
    }
}

function categoriesdata(departmentId) {
    axiosInstance.get(`${apis.resource}${doctypes.departments}/${departmentId}`)
        .then((res) => {
            if (res.data && res.data.ezy_departments_items) {
                categoryOptions.value = res.data.ezy_departments_items.map(item => item.category);
            }
        })
        .catch((error) => {
            console.error("Error fetching categories data:", error);
        });
}
function raiseRequestSubmission() {
    console.log(selectedData.value, "--------------");
    // const dataObj = {

    // }
    // axiosInstance.post(apis.raiseRequest, dataObj)
    //     .then((response) => {
    //         console.log(response);
    toast.success("Rquest Raised", { autoClose: 500 })

    const modal = bootstrap.Modal.getInstance(document.getElementById('riaseRequestModal'));
    modal.hide();
    //     })
    //     .catch((error) => {
    //         console.error("Error fetching data:", error);
    //     });
}

const handleTabChange = (tab) => {
    activeTab.value = tab.route; // Update the active tab
    router.push(tab.route);
};

const handleBuChange = (tab) => {
    if (tab.route.includes('/forms')) {
        router.push(tab.route);
    }
};


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

.raise-label {
    font-size: 12px;
    font-weight: 500;
    margin-bottom: 2px;
}
</style>
