<template>
  <div>
    <div>
      <div class="d-flex justify-content-between align-items-center">
        <div>
          <h1 class="m-0 font-13">
            Forms in {{ id }}
          </h1>
          <p class="m-0 font-11 pt-1">
          {{ totalRecords }} forms available
          </p>
        </div>
        <div class="d-flex gap-2 align-items-center">
          <div class="d-flex  align-items-center">
            <div>
              <div class="me-2">
                <span v-if="filterOnModal.form_name && filterOnModal.appliedform_name" class="process-date font-12 m-0">
                  {{ filterOnModal.form_name }}
                  <span v-if="filterOnModal.form_name" class="badge badge-icon rounded-3   text-white "
                    @click="clearFilter('form_name')">
                    <i class="ri-close-line close-icon text-dark rounded-3"></i>
                  </span>
                </span>
                <span v-if="filterOnModal.form_category && filterOnModal.appliedform_category"
                  class="process-date font-12 m-0">
                  {{ filterOnModal.form_category }}
                  <span v-if="filterOnModal.form_category" class="badge badge-icon rounded-3   text-white "
                    @click="clearFilter('form_category')">
                    <i class="ri-close-line close-icon text-dark rounded-3"></i>
                  </span>
                </span>
                <span v-if="filterOnModal.accessible_departments && filterOnModal.appliedaccessible_departments"
                  class="process-date font-12 m-0">
                  {{ filterOnModal.accessible_departments }}
                  <span v-if="filterOnModal.accessible_departments" class="badge badge-icon rounded-3   text-white "
                    @click="clearFilter('accessible_departments')">
                    <i class="ri-close-line close-icon text-dark rounded-3"></i>
                  </span>
                </span>
                <span v-if="filterOnModal.active && filterOnModal.appliedStatus" class="process-date font-12 m-0">
                  {{ filterOnModal.active }}
                  <span v-if="filterOnModal.active" class="badge badge-icon rounded-3   text-white"
                    @click="clearFilter('active')">
                    <i class="ri-close-line close-icon text-dark rounded-3"></i>
                  </span>
                </span>
              </div>
            </div>
            <div>
              <button type="button" class=" filterbtn d-flex align-items-center position-relative "
                data-bs-toggle="modal" data-bs-target="#fileterModal">
                <span> <i class="ri-filter-2-line"></i></span>
                <span v-if="appliedFiltersCount !== 0" class=" badge badge-light colorappiled ">
                  ( {{ appliedFiltersCount }})
                </span>
              </button>

            </div>
          </div>
          
                <div class="modal fade" id="fileterModal" tabindex="-1" aria-labelledby="fileterModalLabel"
                    aria-hidden="true">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">

                            <div class="modal-body">
                                <div class="row">
                                  <div class="col-6">
                                        <label class="font-13 ps-1" for="Requested">Form Name:</label>
                                        <FormFields class="mb-3" tag="input" type="search" name="Requested"
                                            id="Requested" placeholder="Search" v-model="filterOnModal.form_name" />
                                    </div>
                                    <div class="col-6">
                                        <label class="font-13 ps-1" for="dept">Form Category:</label>
                                        <FormFields tag="select" placeholder="Form Category" class="mb-3"
                                            name="dept" v-model="filterOnModal.form_category" id="dept" :Required="false"
                                            :options="formCategory" />
                                    </div>
                                    <div class="col-6">
                                        <label class="font-13 ps-1" for="dept">Accessible departments:</label>
                                        <!-- <FormFields tag="select" placeholder="Accessible departments" class="mb-3"
                                            name="dept" v-model="filterOnModal.accessible_departments" id="dept" :Required="false"
                                            :options="accessibleDepartments" /> -->
                                            <FormFields class="" tag="input" type="search" name="Requested"
                                            id="Requested" placeholder="Search" v-model="filterOnModal.accessible_departments" />
                                           <span class="m-0 font-10 ps-2">Note:Please seperate departments with commas</span>
                                    </div>
                                    <div class="col-6">
                                        <label class="font-13 ps-1" for="dept">Status:</label>
                                        <FormFields tag="select" placeholder="Status" class="mb-3"
                                            name="dept" v-model="filterOnModal.active" id="dept" :Required="false"
                                            :options="['Yes','No']" />
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
                  <button type="button" class="cancelfilter border-0 text-nowrap font-10 " @click="resetFilters"
                    data-bs-dismiss="modal"><span class="font-14 me-1">x</span>Cancel
                    Filter</button>

                  <button type="button"
                    class=" applyfilter btn btn-dark text-nowrap border-0  text-white font-10 d-flex justify-content-center align-items-center"
                    data-bs-dismiss="modal" @click="applyFilters"><span class="font-16 me-1"><i
                        class="bi bi-check2 "></i></span>
                    Apply
                    Filter</button>
                </div>
              </div>
            </div>
          </div>
          <!-- <div class="d-flex align-items-center ">
            <ButtonComp class="buttoncomp font-10" name="CreateForm" ></ButtonComp>
            data-bs-toggle="offcanvas"
              data-bs-target="#offcanvasRight" aria-controls="offcanvasRight"
          </div> -->

        </div>
      </div>
      <div class="mt-3">
        <GlobalTable :tHeaders="tableheaders" :tData="tableData" isCheckbox="true" isAction="true" actionType="dropdown"
          @actionClicked="actionCreated" :actions="actions" />
        <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords"
          @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
      </div>

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
import { ref, computed, watch, reactive } from 'vue';
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from '../../shared/apiurls';
import FormFields from '../../Components/FormFields.vue';
import ButtonComp from '../../Components/ButtonComp.vue';
import GlobalTable from '../../Components/GlobalTable.vue';
import { EzyBusinessUnit } from '../../shared/services/business_unit';
import { rebuildToStructuredArray } from '../../shared/services/field_format';
import PaginationComp from "../../Components/PaginationComp.vue"
import FormPreview from '../../Components/FormPreview.vue'
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
const totalRecords = ref(0);
const tableheaders = ref([
  { th: "Form name", td_key: "form_name" },
  { th: "Form category", td_key: "form_category" },
  { th: "Accessible departments", td_key: "accessible_departments" },
  { th: "Status", td_key: "active" },
]);
const props = defineProps(['id']);
const formDescriptions = ref({})
const selectedForm = ref(null);
const tableData = ref([]);
const formCategory=ref([]);

const filterOnModal=reactive({
  appliedform_name:false,
  appliedform_category:false,
  appliedaccessible_departments:false,
  appliedStatus:false,
form_name:'',
form_category:'',
accessible_departments:'',
active:''
})
const appliedFiltersCount = computed(() => {
  return [
    { value: filterOnModal.form_category, applied: filterOnModal.appliedform_category },
    {
      value: filterOnModal.form_name,
      applied: filterOnModal.appliedform_name,
    },
    {
      value: filterOnModal.active,
      applied: filterOnModal.appliedStatus,
    },
    {
      value: filterOnModal.accessible_departments,
      applied: filterOnModal.appliedaccessible_departments,
    },


  ].filter((filter) => filter.applied && filter.value).length;
});
function clearFilter(type) {
  if (type === "form_name") {
    filterOnModal.form_name = "";
    filterOnModal.appliedform_name = false;
  } else if (type === "form_category") {
    filterOnModal.form_category = "";
    filterOnModal.appliedform_category = false;

  }
  else if (type === "accessible_departments") {
    filterOnModal.accessible_departments = "";
    filterOnModal.appliedaccessible_departments = false;

  }
  else if (type === "active") {
    filterOnModal.active = "";
    filterOnModal.appliedStatus = false;

  }


  applyFilters();
}
// Business unit and filter object
const businessUnit = computed(() => EzyBusinessUnit.value);
const newBusinessUnit = ref({ business_unit: '' });
const filterObj = ref({ limitPageLength: 'None', limit_start: 0 });
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
function applyFilters() {
  filterOnModal.appliedform_name = Boolean(filterOnModal.form_name);
  filterOnModal.appliedform_category = Boolean(filterOnModal.form_category);
  filterOnModal.appliedaccessible_departments = Boolean(filterOnModal.accessible_departments);
  filterOnModal.appliedStatus = Boolean(filterOnModal.active);

  fetchDepartmentDetails()
}
// Watch business unit and department ID changes
watch(
  [() => businessUnit.value, () => props.id],
  ([newBusinessUnitVal, newId]) => {
    newBusinessUnit.value.business_unit = newBusinessUnitVal;
    if (newBusinessUnitVal.length && newId) {
      fetchDepartmentDetails(newId || props.id);
    }
  },
  { immediate: true }
);

// Handle updating the current value
const PaginationUpdateValue = (itemsPerPage) => {
  filterObj.value.limitPageLength = itemsPerPage;
  filterObj.value.limit_start = 0;
  fetchTable();

};
// Handle updating the limit start
const PaginationLimitStart = ([itemsPerPage, start]) => {
  filterObj.value.limitPageLength = itemsPerPage;
  filterObj.value.limit_start = start;
  fetchTable();

};



// Fetch department details function
function fetchDepartmentDetails(id) {
  const filters = [
    ["business_unit", "like", `%${newBusinessUnit.value.business_unit}%`]
  ];
  if (props.id) {
    filters.push(["owner_of_the_form", "like", `%${props.id}%`]);
  }
  if (filterOnModal.form_name) {
    filters.push(["form_name", "like", `${filterOnModal.form_name}`]);
  }
  if (filterOnModal.form_category) {
    filters.push(["form_category", "like", `${filterOnModal.form_category}`]);
  }
  if (filterOnModal.accessible_departments) {
    filters.push(["accessible_departments", "like", `${filterOnModal.accessible_departments}`]);
  }
  if (filterOnModal.active) {
    filters.push(["active", "=", `${filterOnModal.active}`]);
  }
  const queryParams = {
    fields: JSON.stringify(["*"]),
    limit_page_length: filterObj.value.limitPageLength,
    limit_start: filterObj.value.limit_start,
    filters: JSON.stringify(filters),
    order_by: "`tabEzy Form Definitions`.`creation` desc",
  };
  const queryParamsCount = {
    fields: JSON.stringify(["count( `tabEzy Form Definitions`.`name`) AS total_count"]),
    limitPageLength: "None",
    filters: JSON.stringify(filters),
  }
  axiosInstance.get(`${apis.resource}${doctypes.EzyFormDefinitions}`, { params: queryParamsCount })
    .then((res) => {

      totalRecords.value = res.data[0].total_count

    })
    .catch((error) => {
      console.error("Error fetching ezyForms data:", error);
    });

  axiosInstance
    .get(`${apis.resource}${doctypes.EzyFormDefinitions}`, { params: queryParams })
    .then((response) => {
      tableData.value = response.data;

      formCategory.value = [...new Set(response.data.map((formCategory) => formCategory.form_category))];
      

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
   /* background-color: #f1f1f1; 
  color: #111111;  */
  padding: 8px 20px;
}


.filterbtn {
  border: 1px solid #CCCCCC;
  font-size: 16px;
  border-radius: 4px;
  color: #999999;
  padding: 8px;
  width: 100%;
}


</style>
