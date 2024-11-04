<template>
    <div class="d-flex justify-content-between align-items-center ">
        <div>
            <h1 class="m-0 font-13">
                Trash Master
            </h1>
            <p class="m-0 font-11 pt-2">
                374 trashfiles available
            </p>
        </div>
        <div class="d-flex gap-3">
            <div>
                <FormFields labeltext="" class="mb-3" tag="input" type="search" placeholder="Search File Name"
                    name="Value" id="Value" v-model="filterObj.search" />
            </div>
            <div>
                <FormFields tag="select" placeholder="Filter By" class="mb-3" name="roles"
                    v-model="filterObj.selectoption" id="roles" :Required="false"
                    :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']" />
            </div>
            <div class="mt-1">
                <ButtonComp class="buttoncomp" name="Action"></ButtonComp>
            </div>
        </div>
    </div>
    <div class="mt-2">
        <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction='true' isCheckbox='true' />
    </div>
</template>
<script setup>
import FormFields from '../../Components/FormFields.vue';
import ButtonComp from '../../Components/ButtonComp.vue';
import GlobalTable from '../../Components/GlobalTable.vue'
import { ref } from 'vue';
const filterObj = ref({
    search: '',
    selectoption: ''


})
const tableheaders = ref([
    { th: "Form name", td_key: "" },
    { th: "Form category", td_key: "" },
    { th: "Owner of form", td_key: "" },
    { th: "Accessible departments", td_key: "" },
    { th: "Status", td_key: "" },

]

)
const tableData = ref([])
</script>