<template>
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
                        <div class="mt-1">
                            <FormFields tag="select" placeholder="" class="mb-3" name="roles" id="roles"
                                :Required="false" v-model="options"
                                :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire hyd']" />
                        </div>
                        <div class="logooutbtn">
                            <img src="../assets/Image.jpg" />
                        </div>

                    </div>
                </div>
            </div>
        </div>
    </div>


</template>
<script>
import FormFields from './FormFields.vue';
import TabsComp from './TabsComp.vue';

export default {
    components: {
        TabsComp,
        FormFields
    },
    props: {

    },
    data() {
        return {
            tabsData: [
                { name: 'Dashboard', icon: 'bi bi-columns-gap' },
                { name: 'To do', icon: 'fa-solid fa-list-check' },
                { name: 'Documents', icon: 'fa-solid fa-file' },
                { name: 'Forms', icon: 'fa-solid fa-clipboard' },
                { name: 'Settings', icon: 'fa-solid fa-gear' },
                { name: 'Master', icon: 'fa-solid fa-layer-group' }
            ],
            activeTab: 'Master',
            options: ''
        };
    },
    methods: {
        updateActiveTab(tab) {
            this.activeTab = tab;
            console.log(this.activeTab,);
        },
    },
}
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

.imgmix {
    mix-blend-mode: darken !important;
}

@media (min-width: 1604px) and (max-width: 2400px) {
    .col-3 {
        width: 27%;

    }

}
</style>
