<template>
    <div class="container xjdvsdvs">
        <div v-if="!route.query.id" class="backBtn">
            <h5 class="m-0 p-3 font-13 px-4">
                <router-link :to="backTo" @click="backToForm" class="text-dark text-decoration-none"><i
                        class="bi bi-arrow-left font-14 pe-2"></i></router-link>
                Back
            </h5>

        </div>
        <div class="container card form-containe-div border-0 mt-4">
            
                <!-- Top-Level Fields -->
                <div v-if="topLevelFields.length">
                    <div class="row mb-1" v-for="(pair, index) in groupedTopLevelFields" :key="index">
                        <div class="col-md-6" v-for="[key, value] in pair" :key="key">
                            <label class="form-label fw-semibold font-13 text-capitalize">{{ key.replace(/_/g, ' ') }}:</label>
                            <input type="text" class="form-control font-12" :value="value" readonly />
                        </div>
                    </div>
                </div>

                <!-- Nested Arrays as Tables -->
                <div v-for="(arrayData, key) in arrayFields" :key="key" class="mt-4">
                    <h5 class="text-capitalize font-13">{{ key.replace(/_/g, ' ') }}</h5>
                    <div v-if="arrayData.length">
                    <table class="table table-bordered table-sm table-responsive overflow-auto overflow-scroll">
                        <thead>
                            <tr>
                                
                                <th v-for="header in getTableHeaders(arrayData)" :key="header" class="text-capitalize text-center text-block">
                                    {{ header.replace(/_/g, ' ') }}
                                </th>
                            </tr>
                        </thead>
                        <tbody>
                            
                            <tr v-for="(row, rowIndex) in arrayData" :key="rowIndex">
                                <td class="text-center" v-for="header in getTableHeaders(arrayData)" :key="header">{{ row[header] }}</td>
                            </tr>
                        </tbody>
                    </table>
                    </div>
                    <div v-else><span class="font-12">No Child Data</span></div>
                    
                </div>
            
        </div>
    </div>
</template>


<script setup>
import { onMounted } from "vue";
import { computed, ref} from "vue";
import { useRoute, useRouter } from "vue-router";
import "vue3-toastify/dist/index.css";
import axiosInstance from "../shared/services/interceptor";
import { apis } from '../shared/apiurls';


const route = useRoute();
const router = useRouter();
const formDescriptions = ref({})
const backTo = ref(route.query.routepath);

const displayedBlocks = ref([]);

const selectedData = ref({
    business_unit: route.query.business_unit || "", 
    doctype_name: route.query.LinkDoctype || "", 
    doctype_id: route.query.LinkDoctypeId || "", 
    formname: route.query.formname || "", 
    form_short_name: route.query.form_short_name || "", 
    type: route.query.type || "", 
    readOnly: route.query.readOnly || '', 
    routepath:route.query.routepath || ''
   
});




onMounted(() => {
    fetchDepartmentDetails();
console.log(selectedData.value,";;;;");
})



// Fetch data from API
function fetchDepartmentDetails() {
    const queryParams = {
        fields: JSON.stringify(['*']),
    }

    axiosInstance
        .get(`${apis.resource}${selectedData.value.doctype_name}/${selectedData.value.doctype_id}`, {
            params: queryParams,
        })
        .then((response) => {
            displayedBlocks.value = response.data
        })
        .catch((error) => {
            console.error('Error fetching data:', error)
        })
}

// Separate flat fields and nested arrays
const topLevelFields = computed(() => {
    const hiddenFields = [
        'name', 'owner', 'creation', 'modified', 'modified_by','company_field',
        'docstatus', 'idx', 'doctype', 'parent', 'parenttype', 'parentfield'
    ]

    return Object.entries(displayedBlocks.value || {}).filter(
        ([key, value]) => !Array.isArray(value) && !hiddenFields.includes(key)
    )
})


const groupedTopLevelFields = computed(() => {
    const grouped = []
    for (let i = 0; i < topLevelFields.value.length; i += 2) {
        grouped.push(topLevelFields.value.slice(i, i + 2))
    }
    return grouped
})

const arrayFields = computed(() => {
    const arrays = {}
    Object.entries(displayedBlocks.value || {}).forEach(([key, value]) => {
        if (Array.isArray(value)) {
            arrays[key] = value
        }
    })
    return arrays
})

// Extract table headers from first object in array
function getTableHeaders(dataArray) {
  if (!dataArray.length) return []
  const hiddenFields = ['name', 'owner', 'creation', 'modified', 'modified_by', 'docstatus', 'idx', 'parent', 'parentfield', 'parenttype', 'doctype']
  return Object.keys(dataArray[0]).filter(key => !hiddenFields.includes(key))
}

function backToForm(){
router.push({
    name: "ApproveRequest",
    query: {
      routepath: selectedData.value.routepath,
      name: selectedData.value.formname,
      doctype_name: selectedData.value.form_short_name,
      type: selectedData.value.type,
      business_unit: selectedData.value.business_unit,
      status:selectedData.value.status,
      readOnly: selectedData.value.readOnly || ''

    },
  });
}

</script>


<style lang="scss" scoped>
.previewInputHeight {
    /* height: 35px; */
    margin-bottom: 5px;
}

.download_btn {
    border: 1px solid rgb(36, 220, 36);
    color: rgb(36, 220, 36);
    background: transparent;
    border-radius: 10px;
}

.dynamicColumn {
    border: 1px dotted #cccccc;
    border-radius: 7px;
    margin: 3px 3px 10px 3px;
    background-color: #ffffff;
    padding: 0;
    padding-bottom: 5px;
}

.section-label {
    padding: 10px 14px;
}

.description-div {
    padding: 0px 3px;
}

.blockName {
    box-shadow: 0px 4px 4px 0px #0000000d;
    padding: 18px 12px;
    font-weight: 500;
    font-size: 15px;
}

/* .block-container {
    background-color: #f5f5f5;
} */

.modal-body {
    overflow-y: scroll;
    overflow-x: hidden;
    height: 70vh;
}

input::-webkit-input-placeholder {
    font-size: 10px;
}

.accordion-button:focus {
    box-shadow: None;
}

.accordion-button {
    background-color: #fff;
    font-size: 14px;
    font-weight: 500;
}

.accordion-button:not(.collapsed) {
    background-color: #fff;
    color: #000;
    box-shadow: None;
}

table {
    border-collapse: collapse;
    background-color: #000;
}

th {
    background-color: #f2f2f2 !important;
    text-align: left;
    color: #999999;
    font-size: 12px;
}

td {
    font-size: 12px;
}

.tableborder-child {
    border: 1px solid #ccc !important;
    border-radius: 10px !important;
    padding: 0;
    margin: 1px;
}

.backBtn {
    box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.form-containe-div {
    height: 80vh;
    overflow-y: scroll;
}
input:focus{
box-shadow: none;
}
</style>