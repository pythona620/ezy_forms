<template>
    <div>

        <div class="position-sticky top-0 stickyheader">
            <div class="container-fluid">
                <div class="headerbackgound mt-2">
                    <div class="row">
                        <div class="col-2">
                            <div class="d-flex gap-2 p-2 align-items-center">
                                <div><img class="imgmix" src="../assets/favicon.jpg" /></div>
                                <div class="m-0">
                                    <p class="font-13 m-0">EZY | Forms</p>
                                </div>
                            </div>
                        </div>
                        <div class="col-7">
                            <div class="mt-2">
                                <TabsComp :tabs="filteredTabsData" @changeTab="handleTabChange" />
                            </div>
                        </div>
                        <div class="col-3">
                            <div class="d-flex gap-3 justify-content-end align-items-center m-0">
                                <div class="mb-1">
                                    <ButtonComp v-if="shouldShowButton" class="btn-outline-primary text-nowrap font-10"
                                        name="Raise request" data-bs-toggle="modal" data-bs-target="#riaseRequestModal"
                                        @click="raiseRequest" />
                                </div>
                                <div class="mt-1">
                                    <FormFields tag="select" placeholder="" class="mb-3" name="roles" id="roles"
                                        :Required="false" v-model="business_unit" :options="EzyFormsCompanys" />
                                </div>
                                <div class="logooutbtn">
                                    <div class="btn-group dropdown navbar-nav ms-auto">
                                        <button type="button" class="btn border-0 p-0 me-2 mt-0"
                                            data-bs-toggle="dropdown" aria-expanded="false">
                                            <img src="../assets/Image.svg" />
                                        </button>
                                        <ul class="dropdown-menu dropdown-menu-start p-2">
                                            <div class="d-flex gap-2 align-items-center">
                                                <div>
                                                    <li
                                                        class="d-flex justify-content-center align-items-center btn btn-dark">

                                                        {{ userInitial }}

                                                    </li>
                                                </div>
                                                <div>
                                                    <li>
                                                        <div class=" ">
                                                            <span class="fw-medium font-13 "> {{ userEmail }}</span>

                                                        </div>
                                                        <div class=" ">

                                                            <span class="fw-medium font-11">{{ userDesigination
                                                                }}</span>
                                                        </div>
                                                    </li>
                                                </div>
                                              
                                            </div>

                                            <li class="mt-2">
                                                <div class="d-flex justify-content-center align-items-center">
                                                    <ButtonComp class="changepass rounded-2 text-left" icon="lock"
                                                        data-bs-toggle="modal" data-bs-target="#changePassword"
                                                        name="Change Password"></ButtonComp>
                                                </div>
                                            </li>
                                            <li class="mt-2">
                                                <div class="d-flex justify-content-center align-items-center">
                                                    <ButtonComp class=" logout rounded-2 text-left"
                                                        icon="box-arrow-right" @click="logout()" name="Log Out">
                                                    </ButtonComp>
                                                </div>
                                            </li>
                                        </ul>
                                    </div>

                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
            <!-- Modal -->
        </div>
        <div class="modal fade" id="riaseRequestModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
            aria-labelledby="riaseRequestModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title font-14 fw-bold" id="riaseRequestModalLabel">Raise Request</h5>
                        <button @click="raiseRequstClearForm()" type="button" class="btn-close" data-bs-dismiss="modal"
                            aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <!-- <FormFields tag="select" placeholder="Category" class="mb-3" name="roles" id="roles"
                            @change="changingCategory" :Required="false" :options="categoryOptions"
                            v-model="selectedData.selectedCategory" /> -->
                        <div class="row">
                            <div class="col">
                                <div class=" mb-2">
                                    <label class="raise-label" for="">Category</label>
                                    <Multiselect :options="categoryOptions" @change="changingCategory"
                                        v-model="selectedData.selectedCategory" placeholder="Select" :multiple="false"
                                        class="font-11" :searchable="true" />
                                </div>
                            </div>
                            <div class="col">
                                <div class=" mb-2">
                                    <label class="raise-label" for="">Form</label>
                                    <Multiselect :options="formList" v-model="selectedData.selectedform"
                                        placeholder="Select" @change="SelectedFromchange" :multiple="false"
                                        class="font-11" :searchable="true" />
                                </div>
                            </div>

                        </div>
                        <div v-if="blockArr.length">
                            <RequestPreview :blockArr="blockArr" @updateField="handleFieldUpdate" />
                        </div>

                        <!-- <FormFields tag="select" placeholder="Form" class="mb-3" name="roles" id="roles"
                            :Required="false" :options="formList" v-model="selectedData.selectedform" /> -->
                    </div>
                    <div>
                        <div class=" d-flex justify-content-center align-items-center p-3">
                            <button class="btn btn-dark font-12 w-100" type="submit"
                                @click="raiseRequestSubmission">Raise
                                Request</button>
                        </div>
                    </div>

                </div>
            </div>
        </div>
        <div class="modal fade" id="changePassword" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
            aria-labelledby="changePasswordLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-sm">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title font-14 fw-bold" id="changePasswordLabel">Change Password</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <!-- <FormFields tag="select" placeholder="Category" class="mb-3" name="roles" id="roles"
                            @change="changingCategory" :Required="false" :options="categoryOptions"
                            v-model="selectedData.selectedCategory" /> -->
                        <div class=" mb-2">
                            <label class="raise-label" for="changepass">New Password</label>
                            <FormFields class="mb-3" tag="input" type="text" name="changepass" id="changepass"
                                placeholder="Enter" v-model="new_password" />
                        </div>
                        <div class=" mb-2">
                            <label class="raise-label" for="confirmpass">Confirm Password</label>
                            <FormFields class="" tag="input" type="text" name="confirmpass" id="confirmpass"
                                placeholder="Enter" v-model="confirm_password" />
                            <span v-if="passwordsMismatch" class="text-danger font-10 m-0 ps-2">Passwords do not
                                match.</span>
                        </div>
                        <!-- <FormFields tag="select" placeholder="Form" class="mb-3" name="roles" id="roles"
                            :Required="false" :options="formList" v-model="selectedData.selectedform" /> -->
                    </div>
                    <div>
                        <div class=" d-flex justify-content-center align-items-center p-3">
                            <button class="btn btn-dark font-12 w-100" type="submit" @click="passwordChange()">
                                Confirm New Password</button>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>

</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router'; // Import useRouter
import { apis, doctypes } from '../shared/apiurls';
import axiosInstance from '../shared/services/interceptor';
import ButtonComp from './ButtonComp.vue';
import FormFields from './FormFields.vue';
import TabsComp from './TabsComp.vue';
import Multiselect from "@vueform/multiselect";
import "@vueform/multiselect/themes/default.css";
import { EzyBusinessUnit } from "../shared/services/business_unit";
import { rebuildToStructuredArray } from "../shared/services/field_format";
import RequestPreview from './RequestPreview.vue';
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

const router = useRouter(); // Initialize router

// Define reactive variables
const tabsData = ref([
    { name: 'Dashboard', icon: 'bi bi-columns-gap', route: '/dashboard' },
    { name: 'To do', icon: 'fa-solid fa-list-check', route: '/todo' },
    { name: 'Forms', icon: 'fa-solid fa-clipboard', route: '/forms' },
    { name: 'Settings', icon: 'fa-solid fa-gear', route: '/settings' },
    { name: 'Archive', icon: 'bi bi-archive', route: '/archived' },
    { name: 'Form', icon: 'fa-solid fa-clipboard', route: '/create-form' }
]);

const selectedData = ref({
    selectedCategory: "",
    selectedform: ""
});

const route = useRoute(); // Initialize route to access route parameters
const categoryOptions = ref([])
const formList = ref([])
const business_unit = ref('');
const userInitial = ref('');
const new_password = ref("")
const username = ref('');

const confirm_password = ref('')
const userEmail = ref('');
const userDesigination = ref('')
const userAdmin = ref('')

const blockArr = ref([])
const EzyFormsCompanys = ref([]);
const formSideBarData = ref([]);
const deptartmentData = ref([]);
const activeTab = ref('')
const filterObj = ref({
    limit_start: 0,
    limitPageLength: 100,
})
const filteredTabsData = computed(() => {

return userDesigination.value === 'IT'
    ? tabsData.value
    : tabsData.value.filter(tab => tab.name !== 'Form');
});
function logout() {
    localStorage.removeItem('UserName');
    localStorage.removeItem('employeeData');
    localStorage.removeItem('Bu');


    router.push({ path: '/' }).then(() => {

    });
}
function raiseRequstClearForm() {
    selectedData.value.selectedCategory = '',
        selectedData.value.selectedform = '',
        blockArr.value = []
}
const props = defineProps(['id']);
onMounted(() => {
    ezyForms();
    activeTab.value = route.path;

    // Retrieve data from localStorage
    const userData = JSON.parse(localStorage.getItem('employeeData'));
    const userName = JSON.parse(localStorage.getItem('UserName'));
    const syetemmanger = JSON.parse(localStorage.getItem('systemManager'))
    if (userName) {
        // Set the username based on the UserName data, which is used to check if the user is Admin
        username.value = userName.full_name;

        if (userName.full_name === 'Administrator') {

            userAdmin.value = userName.full_name;
            userInitial.value = userName.full_name.charAt(0).toUpperCase();
        } else if (userData) {
            // Non-admin login: Set both employee and user-specific data
            userAdmin.value = userName.full_name;
            userInitial.value = userData.emp_name.charAt(0).toUpperCase();
            userEmail.value = userData.name;
            userDesigination.value = userData.designation;
        }
    } else {
        console.warn("No user data found in localStorage.");
    }
});

const shouldShowButton = computed(() => {
    const pathsToMatch = ['/forms/department', '/todo'];
    return pathsToMatch.some(path => route.path.includes(path));
});
const passwordsMismatch = computed(() =>
    new_password.value && confirm_password.value && new_password.value !== confirm_password.value
);
function passwordChange() {
    if (passwordsMismatch.value) {
        console.error("Passwords do not match.");
        return;
    }

    const userName = JSON.parse(localStorage.getItem('employeeData'));
    const payload = {
        new_password: new_password.value,
    };

    axiosInstance.put(`${apis.resource}${doctypes.users}/${userName.name}`, payload)
        .then((res) => {
            console.log("Password updated successfully:", res.data);
            toast.success('Password changed Successfully', { autoClose: 300 });
            const modal = bootstrap.Modal.getInstance(document.getElementById('changePassword'));
            modal.hide();
        })
        .catch((error) => {
            console.error("Error:", error);
        });
}
const ezyForms = () => {
    const queryParams = {
        fields: JSON.stringify(["*"]),
    };

    axiosInstance.get(apis.resource + doctypes.wfSettingEzyForms, {
        params: queryParams,
    }).then((res) => {
        if (res?.data?.length) {
            EzyFormsCompanys.value = res.data.map((company) => company.bu_code);
            if (EzyFormsCompanys.value.length) {
                business_unit.value = EzyFormsCompanys.value[0];
            }
        }
    }).catch((error) => {
        console.error("Error fetching ezyForms data:", error);
    });
};
watch(business_unit, (newBu, oldBu) => {
    EzyBusinessUnit.value = newBu;
    localStorage.setItem("Bu", EzyBusinessUnit.value)

    if (oldBu) {
        deptData(true);
    } else {

        deptData();
    }
});


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
const employeeData = ref({});

function raiseRequest() {
    console.log(" Raise req ")
    const storedData = localStorage.getItem("employeeData");
    if (storedData) {
        employeeData.value = JSON.parse(storedData);
        categoriesdata(employeeData.value.department);
    } else {
        console.error("No employee data found in local storage.");
    }
}
// watch(
//     () => selectedData.value.selectedCategory,
//     (newVal, oldVal) => {
//         if (newVal !== oldVal) {
//             changingCategory(newVal, oldVal);
//         }
//     }
// );

function changingCategory(value) {
    if (value) {
        const dataObj = {
            "role": employeeData.value.designation,
            "business_unit": EzyBusinessUnit.value
        };

        axiosInstance.post(apis.raiseFormdata, dataObj)
            .then((response) => {
                formList.value = response.message.list_of_roadmaps

            })
            .catch((error) => {
                console.error("Error fetching data:", error);
            });
    }
}
function SelectedFromchange(value) {
    if (value) {

        formDefinations(value)
    }
}
function formDefinations(value) {
    const filters = [
        ["business_unit", "like", `%${business_unit.value}%`]
    ];
    if (selectedData.value.selectedCategory) {
        filters.push(["form_category", "like", `${selectedData.value.selectedCategory}`]);
    }
    if (value) {
        filters.push(["form_short_name", "like", `%${value}%`]);
    }

    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify(filters),
        limit_page_length: filterObj.value.limitPageLength,
        limit_start: filterObj.value.limit_start,
        order_by: "`tabEzy Form Definitions`.`creation` desc"
    };
    // const queryParamsCount = {
    //     fields: JSON.stringify(["count( `tabEzy Form Definitions`.`name`) AS total_count"]),
    //     limitPageLength: "None",
    //     filters: JSON.stringify(filters),
    // }
    // axiosInstance.get(`${apis.resource}${doctypes.EzyFormDefinitions}`, { params: queryParamsCount })
    //     .then((res) => {
    //         // console.log(res.data[0].total_count);
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
const emittedFormData = ref([]);

const handleFieldUpdate = (fieldValues) => {
    emittedFormData.value = emittedFormData.value.concat(fieldValues);
};

function raiseRequestSubmission() {
    let form = {};
    form['doctype'] = selectedData.value.selectedform;
    form['company_field'] = business_unit.value
    if (emittedFormData.value.length) {
        emittedFormData.value.map((each) => {
            form[each.fieldname] = each.value
        })
    }

    console.log(" ==== ", form)

    // form['form_json']
    const formData = new FormData();
    formData.append('doc', JSON.stringify(form));
    formData.append('action', 'Save');
    axiosInstance.post(apis.savedocs, formData)
        .then((response) => {
            console.log(response);
            request_raising_fn(response.docs[0])
           
        })
        .catch((error) => {
            console.error("Error fetching data:", error);
        });
}

function request_raising_fn(item) {
    let data_obj = {
        module_name: 'Ezy Forms',
        doctype_name: selectedData.value.selectedform,
        ids: [item.name], //docs name,
        reason: '',
        url_for_request_id: '',
        files: [],
        property: business_unit.value,

    }
    axiosInstance.post(apis.raising_request, data_obj).then( async (resp) => {
        console.log(resp)
        if (resp?.message?.success) {
            toast.success("Request Raised", { autoClose: 1000 })
            const modal = await bootstrap.Modal.getInstance(document.getElementById('riaseRequestModal'));
            modal.hide();
            await router.push({ path: '/todo/raisedbyme' })
            window.location.reload()
        }
    })
}

const handleTabChange = (tab) => {
    activeTab.value = tab.route; // Update the active tab
    router.push(tab.route);
};

const handleBuChange = (tab) => {
    if (tab.route.includes('/forms')) {
        router.push(tab.route);
    }
    // Now you can handle the field update here, for example:
    //   const { blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex, value } = payload;
    // Update the field in your blockArr data
    //   blockArr.value[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex].value = value;
};


</script>

<style scoped>
.headerbackgound {
    height: 50px;
    background-color: var(--sidebar-color);

}

.logooutbtn {
    background-color: #D1D0FF !important;
    border-radius: 3px;
    width: 28px;
    height: 28px;
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 7px;
}

.changepass {
    width: 214px;
    height: 35px;
    border-radius: 4px;
    background-color: #F2F2FF;
    padding: 9px 30px 9px 9px;
    font-size: 11px;
    color: #2124FE;
    text-align: left;

}

.logout {
    width: 214px;
    height: 35px;
    border-radius: 4px;
    background-color: #FFF2F3;
    padding: 9px 30px 9px 9px;
    font-size: 11px;
    color: #FE212E;
    text-align: left;

}

@media (min-width: 1604px) and (max-width: 2400px) {
    .col-3 {
        width: 27%;

    }

}

.stickyheader {
    z-index: 10;
}

.raise-label {
    font-size: 12px;
    font-weight: 500;
    margin-bottom: 2px;
}
</style>
