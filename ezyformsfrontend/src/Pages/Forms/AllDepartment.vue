<template>
  <div>
    <div>
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h1 class="m-0 font-13">
            Forms in {{ id }}
          </h1>
          <p class="m-0 font-11 pt-1">
            2 forms available
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
                                        <label class="font-13 ps-1" for="Requested">Form Name:</label>
                                        <!-- <FormFields class="mb-3" tag="input" type="search" name="Requested"
                                            id="Requested" placeholder="Search" v-model="filterOnModal.form_name" /> -->

                                            <div>
                    <FormFields labeltext="" class="" tag="input" type="search" placeholder="Search Form Name"
                        name="Value" id="Value" v-model="filterObj.search" @input="fetchDepartmentDetails(id)" />
                </div>
                                    </div>
                                    
                                    <!-- <div class="col-3">
                                        <label class="font-13 ps-1 fw-medium" for="dept">Requested Dept:</label>
                                        <FormFields tag="select" placeholder="Select Department" class="mb-3"
                                            name="dept" v-model="filterOnModal.department_name" id="dept"
                                            :Required="false"
                                            :options="designiations" />
                                    </div> -->
                                  
                                  

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
                <div class="d-flex align-items-center ">
                  <ButtonComp class="buttoncomp font-10" name="CreateForm" data-bs-toggle="offcanvas"
            data-bs-target="#offcanvasRight" aria-controls="offcanvasRight"></ButtonComp>
                </div>
              
            </div>
      </div>
      <GlobalTable :tHeaders="tableheaders" :tData="tableData" isCheckbox="true" isAction="true" actionType="dropdown"
        @actionClicked="actionCreated" :actions="actions" />
    </div>
    <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
      <div class="offcanvas-header">
        <h5 class="offcanvas-title" id="offcanvasRightLabel">Asset Request Form</h5>
        <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
      </div>
      <div class="offcanvas-body">
        <div class="d-flex gap-3 align-items-baseline position-relative">
          <div class="d-flex flex-column">
            <span>
              <i class="ri-checkbox-blank-circle-fill dashedcircle"></i>
            </span>
            <div class="dashed_line mt-4"></div>
          </div>
          <div>data</div>
        </div>
      </div>
    </div>
    <FormPreview :blockArr="selectedForm" :formDescriptions="formDescriptions" />

  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from '../../shared/apiurls';
import FormFields from '../../Components/FormFields.vue';
import ButtonComp from '../../Components/ButtonComp.vue';
import GlobalTable from '../../Components/GlobalTable.vue';
import { EzyBusinessUnit } from '../../shared/services/business_unit';
import { rebuildToStructuredArray } from '../../shared/services/field_format';
import FormPreview from '../../Components/FormPreview.vue'
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

// Props for dynamic ID
const props = defineProps(['id']);
const formDescriptions = ref({})
const selectedForm = ref(null);

// Business unit and filter object
const businessUnit = computed(() => EzyBusinessUnit.value);
const newBusinessUnit = ref({ business_unit: '' });
const filterObj = ref({ search: '', selectoption: '', limitPageLength: 'None', limitstart: 0 });
const actions = ref(
  [
    { name: 'View form', icon: 'fa-solid fa-eye' },

  ]
)
function actionCreated(rowData, actionEvent) {
  if (actionEvent.name === 'View form') {
    if (rowData?.form_json) {
      formDescriptions.value = { ...rowData }
      selectedForm.value = rebuildToStructuredArray(JSON.parse(rowData?.form_json).fields)
      const modal = new bootstrap.Modal(document.getElementById('formViewModal'), {});// raise a modal
      modal.show();

    } else {
      toast.warn(" There is no form fields ")
    }
  }

}
// Watch business unit and department ID changes
watch(
  [() => businessUnit.value, () => props.id],
  ([newBusinessUnitVal, newId]) => {
    newBusinessUnit.value.business_unit = newBusinessUnitVal;
    if (newBusinessUnitVal.length || newId) {
      fetchDepartmentDetails(newId || props.id);
    }
  },
  { immediate: true }
);


// Table headers and data
const tableheaders = ref([
  { th: "Form name", td_key: "form_name" },
  { th: "Form category", td_key: "form_category" },
  { th: "Accessible departments", td_key: "accessible_departments" },
  { th: "Status", td_key: "status" },
]);
const tableData = ref([]);

// Fetch department details function
function fetchDepartmentDetails(id) {
  const filters = [
    ["business_unit", "like", `%${newBusinessUnit.value.business_unit}%`]
  ];
  if (props.id) {
    filters.push(["owner_of_the_form", "like", `%${props.id}%`]);
  }
  if (filterObj.value.search.trim()) {
        filters.push(["name", "like", `${filterObj.value.search}`]);
    }
  const queryParams = {
    fields: JSON.stringify(["*"]),
    limit_page_length: filterObj.value.limitPageLength,
    limitstart: filterObj.value.limitstart,
    filters: JSON.stringify(filters),
    order_by: "`tabEzy Form Definitions`.`creation` desc",
  };

  axiosInstance
    .get(`${apis.resource}${doctypes.EzyFormDefinitions}`, { params: queryParams })
    .then((response) => {
      tableData.value = response.data;
    })
    .catch((error) => {
      console.error("Error fetching department details:", error);
    });
}
// const filterOnModal = ref({
//   form_name: "",
   
//     department_name: "",
   

// })
</script>

<style>
.dashedcircle {
  border: 1px dashed #AAAAAA;
  height: 30px;
  width: 30px;
  padding: 0;
  margin: 0;
  border-radius: 50%;
  color: #14D82B;
}

.dashed_line {
  height: 100px;
  border: 1px dashed #AAAAAA;
  width: 1px;
  position: absolute;
  left: 2%;
}


.filterbtn {
    border: 1px solid #CCCCCC;
    font-size: 16px;
    border-radius: 4px;
    color: #999999;
    padding: 8px;
    width: 100%;
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

