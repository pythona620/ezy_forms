<template>
    <div>
        <div class="d-flex formsticky align-items-center justify-content-between py-2">
            <div>
                <h1 class="m-0 font-13">Work Order </h1>
            </div>

        </div>
        <!-- v-if="tableForm" -->
        <div class="mt-2">
            <table class="table">
                <thead>
                    <tr>
                        <th>
                            Name
                        </th>
                        <th>
                            actions
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            Work order
                        </td>
                        <td>
                            <i @click="toWorkOrder" class="bi bi-eye"></i>
                        </td>
                    </tr>
                </tbody>
            </table>
            

        </div>

        

    </div>
</template>
<script setup>

import { onMounted, ref, computed, watch, reactive } from "vue";

import { EzyBusinessUnit } from "../../shared/services/business_unit";
import { useRoute, useRouter } from "vue-router";


const totalRecords = ref(0);
const pdfPreview = ref('')

const formDescriptions = ref({})
const tableData = ref([
    
  {
    "name": "o14sksk151",
    "owner": "Administrator",
    "creation": "2025-06-23 16:29:53.199911",
    "modified": "2025-07-04 18:37:19.906440",
    "modified_by": "ajay@gmail.com",
    "docstatus": 0,
    "idx": 0,
    "form_name": "Work order",
    "installed": "Yes",
    
  },
  

]);
const route = useRoute();
const businessUnit = computed(() => {
    return EzyBusinessUnit.value;
});
const sections = reactive([]);


onMounted(() => {
    // fetchTable()
    // fetchCategory()

})

const filterObj = ref({
    limit_start: 0,
    limitPageLength: 20,
    form_name: "",
    form_short_name: "",
    accessible_departments: "[]",
    business_unit: '',
    form_category: "",
    owner_of_the_form: "",
    search: "",
});
const newChngedValue = ref('')

const tableheaders = ref([
    { th: "Form name", td_key: "form_name" },
    { th: "Installed", td_key: "installed" },
    // { th: "Short Name", td_key: "form_short_name" },
  
]);

const router = useRouter();

const selectedForm = ref(null);
const actions = ref([
    { name: 'Set up Form', icon: 'fa-solid fa-edit' },
]);
const childtableHeaders = ref([]);

function toWorkOrder(){

    router.push({
        name: "WorkOrderDetails",
        query: {
            routepath: route.path,
            business_unit: businessUnit.value,
        },
    });
   
    
}










</script>
<style scoped>
.table {
    width: 100%;
    white-space: nowrap;
    font-size: var(--font-size-xs);
    font-weight: 400;
}

th {
    background-color: #f2f2f2 !important;
    text-align: left;
    color: #999999 !important;
    font-size: 12px;
}

th,
td {
    max-width: 100px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: var(--muted) !important;
    font-size: var(--twelve);
}
.bi-eye{
    cursor: pointer;
}
</style>
