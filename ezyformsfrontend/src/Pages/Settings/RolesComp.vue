<template>
    <div>
        <div class="d-flex justify-content-between align-items-center py-2 ">
            <div>
                <h1 class="m-0 font-13">
                    Roles
                </h1>
                <!-- <p class="m-0 font-11 pt-1">
                    19 Roles
                </p> -->
            </div>
            <div class="d-flex gap-2 align-items-center">


                <div class="d-flex align-items-center ">

                    <button type="button" class="btn btn-dark buttoncomp CreateDepartments d-flex align-items-center "
                        @click="CreateNewRoleBtn" data-bs-toggle="modal" data-bs-target="#createDepartments">
                        Create Role
                    </button>
                </div>
                <div class="modal fade" id="createDepartments" tabindex="-1" aria-labelledby="createDepartmentsLabel"
                    aria-hidden="true">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">

                            <div class="modal-body">
                               <div class="mt-3">
                            <div class="">
                              <!-- <FormFields labeltext="Form Cateogry" class="mb-3" tag="select"
                                                            name="desgination" id="desgination"
                                                            placeholder="Select Cateogry" :options=departments
                                                            v-model="filterObj.form_category" /> -->

                              <label for="">New Role
                                </label>

                              <Multiselect 
                                :options="ExistRoles" v-model="filterObj.role" placeholder="Select Cateogry"
                                :multiple="false" :searchable="true" class="font-11 multiselect" />
                            </div>
                          </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button"
                                    class="cancelfilter border-1 text-nowrap font-10 d-flex justify-content-center align-items-center"
                                    @click="cancelCreate" data-bs-dismiss="modal"><span class="font-16 me-1"><i
                                            class="bi bi-x "></i></span>Cancel
                                </button>

                                <button type="button"
                                    class="applyfilter btn btn-dark text-nowrap font-10 d-flex justify-content-center align-items-center"
                                    data-bs-dismiss="modal" @click="createNewRoleFN"><span class="font-16 me-1"><i
                                            class="bi bi-check2 "></i></span>
                                    Create ROle</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="mt-2">
            <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction='true' isCheckbox="true"
                actionType="dropdown" />
            <PaginationComp :currentRecords="tableData.length" :totalRecords="tableData.length"
                            @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
        </div>
    </div>
    

</template>
<script setup>

import FormFields from '../../Components/FormFields.vue';
// import ButtonComp from '../../Components/ButtonComp.vue';
import GlobalTable from '../../Components/GlobalTable.vue';
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from '../../shared/apiurls';
import { onMounted, ref, computed, watch } from 'vue';
import Multiselect from "vue-multiselect";
import "@vueform/multiselect/themes/default.css";
import PaginationComp from '../../Components/PaginationComp.vue';
// import { EzyBusinessUnit } from "../../shared/services/business_unit";

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

// const businessUnit = computed(() => {
//     return EzyBusinessUnit.value;
// });
onMounted(() => {
    rolesData()
})
const ExistRoles = ref([])
const filterObj = ref({
    limitPageLength: 'None',
    limitstart: 0,
    business_unit: "",
    role:''
});

// watch(
//     businessUnit,
//     (newVal) => {
//         filterObj.value.business_unit = newVal;

//         if (newVal.length) {
//             
//             rolesData()
//         }
//     },
//     { immediate: true }
// );

const tableheaders = ref([
    { th: "Roles", td_key: "name" },
])
const tableData = ref([]);
function rolesData() {
    const filters = [

        // ["business_unit", "like", `%${filterObj.value.business_unit}%`]
    ];
   

    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify(filters),
        limit_page_length: filterObj.value.limitPageLength,
        limitstart: filterObj.value.limitstart,
        // order_by: "`tabWf Roles`.`creation` desc"
    };

    axiosInstance.get(apis.resource + '/' + doctypes.designations, { params: queryParams })
        .then((res) => {
            if (res.data) {

                tableData.value = res.data;
            }
        })
        .catch((error) => {
            console.error("Error fetching department data:", error);
        });
}
function CreateNewRoleBtn(){
 const filters = [];
  const queryParams = {
    fields: JSON.stringify(["*"]),
    filters: JSON.stringify(filters),
    limit_page_length:"None",
    // order_by: "`tabRoles`.`creation` desc",
  };

  axiosInstance
    .get(apis.resource + doctypes.roles, { params: queryParams })
    .then((res) => {
      if (res.data) {
        ExistRoles.value = [...new Set(res.data.map((user) => user.name))];
      }
    })
    .catch((error) => {
      console.error("Error fetching designations data:", error);
    });
}


function createNewRoleFN(){
    axiosInstance
            .post(apis.resource + doctypes.designations, {
              role: filterObj.value.role,
            }) // Adjust payload as needed
            .then((response) => {
              if (response.data) {
                rolesData()
              }
            })
            .catch((error) => {
              console.error("Error creating designation:", error);
            });
}
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