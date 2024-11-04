<template>
    <div class="d-flex justify-content-between align-items-center ">
        <div>
            <h1 class="m-0 font-13">
                Accounts in IT department
            </h1>
            <p class="m-0 font-11 pt-1">
                2 forms available
            </p>
        </div>
        <div class="d-flex gap-3 align-items-center">
            <div class="d-flex mt-2">
                <div>
                    <FormFields labeltext="" class="mb-3" tag="input" type="search" placeholder="Search File Name"
                        name="Value" id="Value" v-model="filterObj.search" />
                </div>
                <div>
                    <FormFields tag="select" placeholder="Filter By" class="mb-3" name="roles"
                        v-model="filterObj.selectoption" id="roles" :Required="false"
                        :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']" />
                </div>
            </div>

            <div class="d-flex align-items-center mb-1">
                <ButtonComp class="buttoncomp font-10" name="CreateForm"></ButtonComp>
            </div>
        </div>
    </div>
    <div class="mt-2">
        <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction='true' actionType="dropdown" />
    </div>
</template>
<script setup>
import FormFields from '../../Components/FormFields.vue';
import ButtonComp from '../../Components/ButtonComp.vue';
import GlobalTable from '../../Components/GlobalTable.vue';
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from '../../shared/apiurls';
import { callWithErrorHandling, onMounted, ref } from 'vue';
const filterObj = ref({
    search: '',
    selectoption: ''


})
const tableheaders = ref([
    { th: "Form name", td_key: "name" },
    { th: "Form category", td_key: "form_category" },

    { th: "Accessible departments", td_key: "acess" },
    { th: "Status", td_key: "status" },
    { th: "WorkFlow", td_key: "status" },

]

)
const tableData = ref([]);
console.log(tableData.value, "tableeee");
// function fetchData() {
//     const queryparams = {
//         fields: ['*']
//     };
//     axiosInstance.get(apis.resource + doctypes.poschecks, queryparams).then(res => {
//         console.log(res, "resposne");
//         // tableData.value = res.data
//         console.log(tableData.value, "rrrrrrrrrr");
//     })
// }
onMounted(() => {
    // fetchData();
})
</script>