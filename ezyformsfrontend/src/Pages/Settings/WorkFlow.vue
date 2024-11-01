<template>
    <div class="d-flex justify-content-between align-items-center ">
            <div>
                <h1 class="m-0 font-13">
                   Workflow
                </h1>
                <p class="m-0 font-11 pt-1">
                   15 Workflows
                </p>
            </div>
            <div class="d-flex gap-2 align-items-center">
                <div class="d-flex">
                    <div>
                        <!-- <FormFields labeltext="" class="mb-3" tag="input" type="search" placeholder="Search File Name"
                        name="Value" id="Value" v-model="filterObj.search" /> -->
                    </div>
                    <div>
                        <button type="button" class=" filterbtn d-flex align-items-center " data-bs-toggle="modal"
                            data-bs-target="#fileterModal">
                            <span> <i class="ri-filter-2-line"></i></span>
                        </button>

                    </div>
                </div>
                <div class="modal fade" id="fileterModal" tabindex="-1" aria-labelledby="fileterModalLabel"
                    aria-hidden="true">
                    <div class="modal-dialog modal-xl">
                        <div class="modal-content">

                            <div class="modal-body">
                                <div class="row">
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="Requested">Roles:</label>
                                        <FormFields class="mb-3" tag="input" type="search" name="Requested"
                                            id="Requested" placeholder="Search" v-model="filterOnModal.roles" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="Requested">Users:</label>
                                        <FormFields class="mb-3" tag="input" type="search" name="Requested"
                                            id="Requested" placeholder="Search" v-model="filterOnModal.users" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1 fw-medium" for="dept">Requested Dept:</label>
                                        <FormFields tag="select" placeholder="Select Department" class="mb-3"
                                            name="dept" v-model="filterOnModal.Requested_dept" id="dept"
                                            :Required="false"
                                            :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="dept">Owner OF Form:</label>
                                        <FormFields tag="select" placeholder="Select Department" class="mb-3"
                                            name="dept" v-model="filterOnModal.Owner_OF_Form" id="dept"
                                            :Required="false"
                                            :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="dept">Form Category:</label>
                                        <FormFields tag="select" placeholder="Select Department" class="mb-3"
                                            name="dept" v-model="filterOnModal.Form_Category" id="dept"
                                            :Required="false"
                                            :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="Requested">Form Name:</label>
                                        <FormFields class="mb-3" tag="input" type="search" name="Requested"
                                            id="Requested" placeholder="Search"
                                            v-model="filterOnModal.department_name" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="Requested">Requested Period:</label>
                                        <FormFields class="mb-3" tag="input" type="date" name="Requested" id="Requested"
                                            placeholder="Jan-2024-Dec-2024" v-model="filterOnModal.Requested_Period" />
                                    </div>
                                    <div class="col-3">
                                        <FormFields tag="radio" :options="radioOptions" name="exampleRadio"
                                            id="exampleRadio" v-model="filterOnModal.Approval_status"
                                            labeltext="Approval Status" />
                                    </div>
                                    <div class="col-3">
                                        <label class="font-13 ps-1" for="Requested">Requested Id:</label>
                                        <FormFields class="mb-3" tag="input" type="search" name="Requested"
                                            id="Requested" placeholder="Search" v-model="filterOnModal.RequestedId" />
                                    </div>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="cancelfilter border-0 text-nowrap font-10 "
                                    @click="resetFilters" data-bs-dismiss="modal"><span
                                        class="font-14 me-1">x</span>Cancel
                                    Filter</button>

                                <button type="button"
                                    class="applyfilter text-nowrap border-0 bg-primary text-white font-10 d-flex justify-content-center align-items-center"
                                    data-bs-dismiss="modal" @click="applyFilters"><span class="font-16 me-1"><i
                                            class="bi bi-check2 "></i></span>
                                    Apply
                                    Filter</button>
                            </div>
                        </div>
                    </div>
                </div>
                <div class="d-flex align-items-center mb-1">
                    <ButtonComp class="buttoncomp" name="Action"></ButtonComp>
                </div>
            </div>
        </div>
        <div class="mt-2">
            <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction='true' actionType="dropdown" />
        </div>
        <!-- <div>help
            <div class="text-center position-relative">
            </div>
            <div class="dropdown">
                <p class="p-0 actions" data-bs-toggle="dropdown" aria-expanded="false">
                    <span>...</span>
                </p>
                <ul class="dropdown-menu actionsdropdown">
                    <li v-for="(action, index) in actions" :key="index">
                        <a class="dropdown-item "> <i :class="action.icon"></i> {{ action.name }}</a>
                    </li>
                </ul>
            </div>
        </div> -->
    
    </template>
    <script setup>
    import { ref } from 'vue';
    import FormFields from '../../Components/FormFields.vue';
        import ButtonComp from '../../Components/ButtonComp.vue';
        import GlobalTable from '../../Components/GlobalTable.vue';
    // const actions = ref(
    //     [
    //         { name: 'View form', icon: 'fa-solid fa-eye' },
    //         { name: 'Edit accessibility to dept.', icon: 'fa-solid fa-users' },
    //         { name: 'Share this form', icon: 'fa-solid fa-share-alt' },
    //         { name: 'Download Print format', icon: 'fa-solid fa-download' },
    //         { name: 'Edit Form', icon: 'fa-solid fa-edit' },
    //         { name: 'In-active this form', icon: 'fa-solid fa-ban' }
    //     ]
    // )
    const radioOptions = ref(["yes", "no"])

const filterOnModal = ref({
    roles: "",
    users:'',
    Requested_dept: "",
    Owner_OF_Form: "",
    Form_Category: "",
    department_name: "",
    Requested_Period: "",
    Approval_status: "",
    RequestedId: ""

})
        const tableheaders = ref([
            { th: "Form name", td_key: "name" },
            { th: "Final approver", td_key: "name" },
            { th: "Accessible departments", td_key: "name" },
            { th: "Module", td_key: "name" },
            { th: "Doctype", td_key: "name" },
            { th: "Max Workflow levels", td_key: "name" },

            
           
    
        ]
    
        )
        const tableData = ref([]);
    </script>
<style scoped>
.global-table th {
    background-color: #f2f2f2 !important;
    text-align: left;
    color: #999999;
    font-size: 12px;
}

.filterbtn {
    border: 1px solid #CCCCCC;
    font-size: 16px;
    border-radius: 4px;
    color: #999999;
    padding: 8px;
    width: 100%;
}

.CreateDepartments {
    width: 100% !important;
    padding: 5px 10px !important;
}

.cancelfilter {
    width: 150px;
    height: 34px;
    border-radius: 6px;
    background-color: #f1f1f1;
    color: #111111;
    padding: 8px 20px;
}

.applyfilter {
    width: 150px;
    height: 34px;
    border-radius: 6px;
    /* background-color: #f1f1f1; */
    /* color: #111111; */
    padding: 8px 20px;
}
</style>