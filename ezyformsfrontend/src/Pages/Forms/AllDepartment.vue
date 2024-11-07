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
        <div class="d-flex gap-3 align-items-center">
          <div class="d-flex mt-2">
            <FormFields labeltext="" class="mb-3" tag="input" type="search" placeholder="Search File Name" name="Value"
              id="Value" v-model="filterObj.search" />
            <FormFields tag="select" placeholder="Filter By" class="mb-3" name="roles" v-model="filterObj.selectoption"
              id="roles" :Required="false"
              :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']" />
          </div>
          <ButtonComp class="buttoncomp font-10" name="CreateForm" data-bs-toggle="offcanvas"
            data-bs-target="#offcanvasRight" aria-controls="offcanvasRight"></ButtonComp>
        </div>
      </div>
      <GlobalTable :tHeaders="tableheaders" :tData="tableData" isCheckbox="true" />
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

// Props for dynamic ID
const props = defineProps(['id']);

// Business unit and filter object
const businessUnit = computed(() => EzyBusinessUnit.value);
const newBusinessUnit = ref({ business_unit: '' });
const filterObj = ref({ search: '', selectoption: '', limitPageLength: 'None', limitstart: 0 });

// Watch business unit and department ID changes
watch(
  businessUnit,
  (newVal) => {
    newBusinessUnit.value.business_unit = newVal;
    if (newVal.length) {

      fetchDepartmentDetails(props.id);
    }
  },
  { immediate: true }
);

watch(
  () => props.id,
  (newId) => {
    if (newId) {
      fetchDepartmentDetails(newId);
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
</style>
