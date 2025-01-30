<template>
    <div>
        <div class=" backtofromPage py-2">

            <router-link to="/todo/receivedform" class=" text-decoration-none text-dark font-13"><span> <i
                        class="bi bi-arrow-left"></i></span>Asset request
                form</router-link>
        </div>
        <div class="container">
            <div v-if="blockArr.length" class="position-relative">
                <div class="requestPreviewDiv">

                    <RequestPreview :blockArr="blockArr" :formName="selectedData.selectedform"
                        @updateField="handleFieldUpdate" @formValidation="isFormValid = $event" />
                </div>
                <!-- @formValidation="isFormValid = $event" -->
                <div class="raiserequestBtnDiv">
                    <div class=" d-flex justify-content-end align-items-center p-3">
                        <button class=" btn btn-white font-13" @click="clearFrom"> <span> <i
                                    class=" bi bi-x"></i></span>Clear
                            form</button>
                        <!-- :disabled="!isFormValid" -->
                        <button :disabled="!isFormValid" class="btn btn-dark font-12 " type="submit"
                            @click="raiseRequestSubmission">Raise
                            Request</button>
                    </div>
                </div>
            </div>
            <div v-else>
                <div class=" no-form">

                    No Form
                </div>
            </div>
        </div>

    </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import { apis, doctypes } from '../shared/apiurls';
import RequestPreview from './RequestPreview.vue';
import Multiselect from "@vueform/multiselect";
import "@vueform/multiselect/themes/default.css";
import { rebuildToStructuredArray } from '../shared/services/field_format';
import axiosInstance from '../shared/services/interceptor';
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import { EzyBusinessUnit } from "../shared/services/business_unit";
import { useRoute, useRouter } from 'vue-router';



const router = useRouter();
const route = useRoute(); // Get query params from route

//  Extract query parameters from URL
const selectedData = ref({
    selectedCategory: route.query.selectedCategory || "",  // Retrieve from query
    selectedform: route.query.selectedForm || ""          // Retrieve from query
});
const business_unit = ref(route.query.business_unit || ""); // Retrieve from query
const isFormValid = ref(false);
const blockArr = ref([])
const categoryOptions = ref([])
const employeeData = ref({});
const formList = ref([])
const emittedFormData = ref([]);
const filepaths = ref('')
const filterObj = ref({
    limit_start: 0,
    limitPageLength: 100,
})
onMounted(() => {

    formDefinations()
    raiseRequest()
})
watch(business_unit, (newBu, oldBu) => {
    EzyBusinessUnit.value = newBu;
    localStorage.setItem("Bu", EzyBusinessUnit.value)

    if (oldBu) {
        deptData(true);
    } else {

        deptData();
    }
});
function clearFrom() {

}
function deptData(value = null) {
    const filters = [
        ["business_unit", "like", `%${business_unit.value}%`]
    ];
    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify(filters),
    };

    axiosInstance.get(apis.resource + doctypes.departments, { params: queryParams })
        .then((res) => {
            if (res.data) {
                deptartmentData.value = res.data;

                // Update the route for the "Forms" tab with the first department's route
                const newFormsRoute = deptartmentData.value.length > 0
                    ? `/forms/department/${deptartmentData.value[0].name.replace(/\s+/g, '-').toLowerCase()}`
                    : '/forms';

                tabsData.value = tabsData.value.map(tab => {
                    if (tab.name === 'Forms') {
                        return { ...tab, route: newFormsRoute };
                    }
                    return tab;
                });


                formSideBarData.value = deptartmentData.value.map(department => ({
                    route: department.name.replace(/\s+/g, '-').toLowerCase(),
                }));

                if (value && activeTab.value.includes("/forms")) {
                    handleBuChange({ route: newFormsRoute })
                }

            }
        })
        .catch((error) => {
            console.error("Error fetching department data:", error);
        });
}
function raiseRequest() {

    const storedData = localStorage.getItem("employeeData");
    if (storedData) {
        employeeData.value = JSON.parse(storedData);
        categoriesdata(employeeData?.value.department);
    } else {
        console.error("No employee data found in local storage.");
    }
}
function categoriesdata(departmentId) {
    axiosInstance.get(`${apis.resource}${doctypes.departments}/${departmentId}`)
        .then((res) => {
            if (res.data && res.data.ezy_departments_items) {
                categoryOptions.value = res.data.ezy_departments_items.map(item => item.category);
            }
        })
        .catch((error) => {
            console.error("Error fetching categories data:", error);
        });
}


function formDefinations() {
    const filters = [
        ["business_unit", "like", `%${business_unit.value}%`]
    ];
    if (selectedData.value.selectedCategory) {
        filters.push(["form_category", "like", `${selectedData.value?.selectedCategory}`]);
    }
    if (selectedData.value.selectedform) {
        filters.push(["form_short_name", "like", `%${selectedData.value?.selectedform}%`]);
    }

    const queryParams = {
        fields: JSON.stringify(["*"]),
        limit_page_length: filterObj.value.limitPageLength,
        limit_start: filterObj.value.limit_start,
        filters: JSON.stringify(filters),
        order_by: "`tabEzy Form Definitions`.`creation` desc"
    };
    // const queryParamsCount = {
    //     fields: JSON.stringify(["count( `tabEzy Form Definitions`.`name`) AS total_count"]),
    //     limitPageLength: "None",
    //     filters: JSON.stringify(filters),
    // }
    // axiosInstance.get(`${apis.resource}${doctypes.EzyFormDefinitions}`, { params: queryParamsCount })
    //     .then((res) => {
    //       
    //         totalRecords.value = res.data[0].total_count

    //     })
    //     .catch((error) => {
    //         console.error("Error fetching ezyForms data:", error);
    //     });


    axiosInstance.get(`${apis.resource}${doctypes.EzyFormDefinitions}`, { params: queryParams })
        .then(res => {

            const form_json = res.data[0].form_json
            blockArr.value = rebuildToStructuredArray(JSON.parse(form_json).fields)
            blockArr.value.splice(1)
        })
        .catch(error => {
            console.error("Error fetching ezyForms data:", error);
        });
}



const handleFieldUpdate = (field) => {

    const fieldExists = emittedFormData.value.some(item => item.fieldname === field.fieldname);


    if (!fieldExists) {
        if (field.fieldtype === 'Attach') {
            if (!Array.isArray(field.value)) {
                filepaths.value = field.value;

            }
            emittedFormData.value.push(field);
        } else {
            emittedFormData.value = emittedFormData.value.concat(field);
        }
    } else {
        console.log(`Field with name "${field.fieldname}" already exists in emittedFormData.`);
    }
};

function raiseRequestSubmission() {
    let form = {};
    form['doctype'] = selectedData.value.selectedform;
    form['company_field'] = business_unit.value;
    // form['supporting_files'] = [];
    if (emittedFormData.value.length) {
        emittedFormData.value.map((each) => {
            form[each.fieldname] = each.value
        })
    }



    // form['form_json']
    const formData = new FormData();
    formData.append('doc', JSON.stringify(form));
    formData.append('action', 'Save');
    axiosInstance.post(apis.savedocs, formData)
        .then((response) => {

            request_raising_fn(response.docs[0])

        })
        .catch((error) => {
            console.error("Error fetching data:", error);
        });
}

function request_raising_fn(item) {
    const filesArray = filepaths.value ? filepaths.value.split(',').map(filePath => filePath.trim()) : [];
    let data_obj = {
        module_name: 'Ezy Forms',
        doctype_name: selectedData.value.selectedform,
        ids: [item.name],
        reason: '',
        url_for_request_id: '',
        files: filesArray,
        property: business_unit.value,
    }; axiosInstance.post(apis.raising_request, data_obj).then(async (resp) => {

        if (resp?.message?.success) {
            toast.success("Request Raised", { autoClose: 1000 });

            await router.push({ path: '/todo/raisedbyme' });
            // window.location.reload();
        }
    });
}















</script>

<style scoped>
.requestPreviewDiv {
    height: 80vh;
    overflow-y: auto;
    padding: 20px 0px;
}

.raiserequestBtnDiv {
    position: sticky;
    bottom: 0;
    left: 0;
    right: 0;
    background-color: #fff;
    z-index: 1;
}

.raisePreview {
    background-color: #EEEEEE;
    padding: 10px;
    border: 1px solid #CCCCCC;
    border-radius: 10px;
    margin-bottom: 5px;
    margin-top: 15px;
}

.raisefrom {
    background-color: #FFFFFF;
    padding: 10px;
    border-radius: 10px;
    border: 1px solid #CCCCCC;
}

.raise-label {
    font-size: 12px;
    font-weight: 500;
    margin-bottom: 2px;
}

.backtofromPage {
    background-color: #ffffff;
    padding: 5px;
}

.no-form {
    width: 100%;
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 15px;
    font-weight: 500;

}
</style>