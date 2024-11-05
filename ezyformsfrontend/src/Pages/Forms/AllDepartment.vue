<template>
    <div>
      <h6> </h6>
      <div >
        <div class="d-flex justify-content-between align-items-center ">
        <div>
            <h1 class="m-0 font-13">
                Forms in {{ id }}
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
        <GlobalTable :tHeaders="tableheaders" :tData="tableData"  />
        <!-- isAction='true' actionType="dropdown" -->
    </div>
      </div>
      
    </div>
  </template>
  
  <script setup>
  import { ref, watch } from 'vue';
import { apis,doctypes } from '../../shared/apiurls';
  import axiosInstance from '../../shared/services/interceptor';
  import FormFields from '../../Components/FormFields.vue';
import ButtonComp from '../../Components/ButtonComp.vue';
import GlobalTable from '../../Components/GlobalTable.vue';
  // Define props
  const props = defineProps(['id']);
  
  // Local state for department details
  const department = ref(null);
  const filterObj = ref({
    search: '',
    selectoption: ''


})
const tableheaders = ref([
    { th: "Form name", td_key: "name" },
    { th: "Form category", td_key: "form_category" },

    { th: "Accessible departments", td_key: "acess" },
    { th: "Status", td_key: "status" },
    // { th: "WorkFlow", td_key: "status" },

]

)
const tableData = ref([]);
console.log(tableData.value, "tableeee");
  // Watch for changes in the id prop
  watch(
    () => props.id,
    (newId) => {
      if (newId) {
        fetchDepartmentDetails(newId);
      }
    },
    { immediate: true } // This will trigger the watch immediately on component mount
  );
  
  // Function to fetch department details
  function fetchDepartmentDetails(id) {
    console.log(id,'iiiiiiiiiiiiiiiiiiiiiiiii')
    axiosInstance.get(apis.resource+doctypes.departments) // Adjust the API endpoint as needed
      .then((response) => {
        department.value = response.data;
        console.log(department.value, 'Fetched department details');
      })
      .catch((error) => {
        console.error("Error fetching department details:", error);
      });
  }
  </script>
  