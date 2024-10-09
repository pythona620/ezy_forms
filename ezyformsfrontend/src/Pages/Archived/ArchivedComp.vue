<template>
    <div class="ps-2">
        <div class="d-flex justify-content-between align-items-center ">
            <div>
                <h1 class="m-0 font-13">
                    Archived forms
                </h1>
                <p class="m-0 font-11 pt-1">
                    1239 Requests
                </p>
            </div>
            <div class="d-flex gap-3 align-items-center">
                <div class="d-flex mt-2">
                    <div>
                        <FormFields labeltext="" class="mb-3" tag="input" type="search" placeholder="Search File Name"
                            name="Value" id="Value" v-model="filterObj.search" isCheckbox='true' />
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
    </div>
    <div v-if="formarchived" class="form_archived">
        <div>
            <img class="m-auto d-flex" src="../../assets/box with files.svg" />
            <h1 class="font-14 fw-bold m-0 text-center">
                The forms are archived.
            </h1>
            <p class="m-0 fw-normal font-12">You can access your archived forms by filtering.</p>
            <div class=" mt-3">
                <!-- Button trigger modal -->
                <button type="button" class=" filterbtn d-flex m-auto" data-bs-toggle="modal"
                    data-bs-target="#exampleModal">
                    Filters
                </button>

                <!-- Modal -->
                <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel"
                    aria-hidden="true">
                    <div class="modal-dialog modal-xl">
                        <div class="modal-content">

                            <div class="modal-body">
                                <div class="row">
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="Requested">Requested By:</label>
                                        <FormFields class="mb-3" tag="input" type="search" name="Requested"
                                            id="Requested" placeholder="Search" v-model="filterObj.search" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1 fw-medium" for="dept">Requested Dept:</label>
                                        <FormFields tag="select" placeholder="Select Department" class="mb-3"
                                            name="dept" v-model="filterObj.selectoption" id="dept" :Required="false"
                                            :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="dept">Owner OF Form:</label>
                                        <FormFields tag="select" placeholder="Select Department" class="mb-3"
                                            name="dept" v-model="filterObj.selectoption" id="dept" :Required="false"
                                            :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="dept">Form Category:</label>
                                        <FormFields tag="select" placeholder="Select Department" class="mb-3"
                                            name="dept" v-model="filterObj.selectoption" id="dept" :Required="false"
                                            :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="Requested">Form Name:</label>
                                        <FormFields class="mb-3" tag="input" type="search" name="Requested"
                                            id="Requested" placeholder="Search" v-model="filterObj.search" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="Requested">Requested Period:</label>
                                        <FormFields class="mb-3" tag="input" type="date" name="Requested" id="Requested"
                                            placeholder="Jan-2024-Dec-2024" v-model="filterObj.search" />
                                    </div>
                                    <div class="col-3"></div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="Requested">Requested Id:</label>
                                        <FormFields class="mb-3" tag="input" type="search" name="Requested"
                                            id="Requested" placeholder="Search" v-model="filterObj.search" />
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn font-12" data-bs-dismiss="modal">Cancel
                                    Filter</button>
                                <button type="button" class="btn btn-primary font-12" data-bs-dismiss="modal"
                                    @click="applyFilter()">Apply
                                    Filter</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

        </div>

    </div>
    <div v-if="tableShow">
        <div class="mt-2">
            <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction='true' actionType="dropdown" />
        </div>
    </div>
</template>
<script setup>
import FormFields from '../../Components/FormFields.vue';
import ButtonComp from '../../Components/ButtonComp.vue';
import GlobalTable from '../../Components/GlobalTable.vue';

import { ref } from 'vue';
const filterObj = ref({
    search: '',
    selectoption: ''


})
const tableShow = ref(false)
const tableheaders = ref([
    { th: "Requested By", td_key: "name" },
    { th: "Requested On", td_key: "name" },
    { th: "Requested Id", td_key: "name" },
    { th: "Requested dept", td_key: "name" },
    { th: "Form name", td_key: "name" },
    { th: "Form category", td_key: "form_category" },
    { th: "Owner of Form", td_key: "acess" },
    { th: "Approvsl Status", td_key: "status" },
    { th: "WorkFlow", td_key: "status" },

]

)
const formarchived = ref(true)
const tableData = ref([]);
function applyFilter() {
    tableShow.value = true;
    formarchived.value = false;
    // const modal = new bootstrap.Modal(document.getElementById('exampleModal'));
    // modal.hide();
}
</script>
<style>
.form_archived {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
}

.filterbtn {
    background-color: var(--sidebar-color);
    border: 1px solid #D8D6FF;
    height: 34px;
    width: 90px;
    font-size: var(--fourteen);
    padding: 5px 23px;
    border-radius: 4px;
    color: #3021FE;
}
</style>