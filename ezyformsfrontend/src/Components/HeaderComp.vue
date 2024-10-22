<template>
    <div class=" position-sticky top-0 stickyheader ">
        <div class="container-fluid">

            <div class="headerbackgound mt-2">

                <div class="row">

                    <div class="col-2">
                        <div class="d-flex gap-2 p-2 align-items-center">
                            <div><img class="imgmix" src="../assets/Group 1.jpg" /></div>
                            <div class="m-0">
                                <p class="font-13 m-0 ">EZY | Forms</p>
                            </div>

                        </div>
                    </div>
                    <div class="col-7">
                        <div class="mt-2">
                            <TabsComp :tabs="tabsData" :activeTab="activeTab" @activeTabValue="updateActiveTab" />

                        </div>
                    </div>
                    <div class="col-3">
                        <div class="d-flex gap-3 justify-content-end align-items-center  m-0 ">
                            <div class="mb-1">
                                <ButtonComp class="btn-outline-primary text-nowrap font-10" name="Raise request" />
                            </div>
                            <div class="mt-1">
                                <FormFields tag="select" placeholder="" class="mb-3" name="roles" id="roles"
                                    :Required="false" v-model="business_unit" :options="EzyFormsCompanys" />
                            </div>
                            <div class="logooutbtn">
                                <img src="../assets/Image.svg" />
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
import { apis, doctypes } from '../shared/apiurls';
import axiosInstance from '../shared/services/interceptor';
import ButtonComp from './ButtonComp.vue';
import FormFields from './FormFields.vue';
import TabsComp from './TabsComp.vue';
import { EzyBusinessUnit } from '../shared/services/business_unit'
// Define reactive variables
const tabsData = [
    { name: 'Dashboard', icon: 'bi bi-columns-gap', route: '/dashboard' },
    { name: 'To do', icon: 'fa-solid fa-list-check', route: '/todo' },
    { name: 'Forms', icon: 'fa-solid fa-clipboard', route: '/forms' },
    { name: 'Settings', icon: 'fa-solid fa-gear', route: '/settings' },
    { name: 'Archive', icon: 'bi bi-archive', route: '/archived' },
    { name: 'Form', icon: 'fa-solid fa-clipboard', route: '/new' }
];
const activeTab = ref('');
const business_unit = ref('');
const EzyFormsCompanys = ref([]);


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

const updateActiveTab = (tab) => {
    activeTab.value = tab.name;
};

watch(business_unit, (newBusinessUnit) => {
    EzyBusinessUnit.value = newBusinessUnit;
});

onMounted(() => {
    ezyForms();
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
