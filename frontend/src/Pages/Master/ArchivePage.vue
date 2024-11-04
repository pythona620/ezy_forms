<template>
    <div class="d-flex justify-content-between align-items-center ">
        <div>
            <h1 class="m-0 font-13">
                Archived
            </h1>
            <p class="m-0 font-11 pt-2">
                477 documents archived
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
            <div>
                <FormFields tag="input" type="date" placeholder="Last 3 months" class="mb-3" name="date"
                    v-model="filterObj.dateId" id="date" :Required="false" />
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
    selectoption: '',
    dateId: ''


})
const tableheaders = ref([
    { th: "Request ID", td_key: "" },
    { th: "Form name", td_key: "" },
    { th: "Form category", td_key: "" },
    { th: "Owner of form", td_key: "" },
    { th: "Request dept.", td_key: "" },
    { th: "Approval Stats", td_key: "" },

]

)
const tableData = ref([])
</script>