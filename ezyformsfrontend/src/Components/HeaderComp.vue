<template>
    <div>

        <div class="position-sticky top-0 stickyheader">
            <div class="container-fluid p-0">
                <div class="headerbackgound py-1">
                    <div class="row">
                        <div class="col-2">
                            <div class="d-flex gap-2 align-items-center">
                                <div><img @click="logoClick" class="imgmix img-fluid"
                                        src="../assets/Final-logo-ezyforms-removebg-preview.png" /></div>
                                <!-- <div class="m-0">
                                    <p class="font-13 m-0">EZY | Forms</p>
                                </div> -->
                            </div>
                        </div>
                        <div class="col-7">
                            <div class="mt-2 ms-2">
                                <TabsComp :tabs="filteredTabsData" @changeTab="handleTabChange" />
                            </div>
                        </div>
                        <div class="col-3 d-flex justify-content-end align-items-center pe-1">
                            <div class="d-flex gap-3 justify-content-end align-items-center m-0 me-2">
                                <!-- <button class="btn btn-outline-danger" type="button" data-bs-toggle="offcanvas"
                                    data-bs-target="#offcanvasRight" aria-controls="offcanvasRight"><i
                                        class="bi bi-bell-fill"></i></button> -->

                                <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight"
                                    aria-labelledby="offcanvasRightLabel">
                                    <div class="offcanvas-header">
                                        <h5 id="offcanvasRightLabel">Notifications</h5>
                                        <button type="button" class="btn-close text-reset" data-bs-dismiss="offcanvas"
                                            aria-label="Close"></button>
                                    </div>
                                    <div class="offcanvas-body">
                                        <ul class="list-unstyled designation-scroll">
                                            <li v-for="(item, index) in SocketList" :key="index"
                                                class="designationList form-check">
                                                {{ item
                                                }}
                                            </li>
                                        </ul>

                                    </div>
                                </div>
                                <div class="">
                                    <!-- v-if="shouldShowButton" -->
                                    <ButtonComp
                                        class="btn btn-danger raiseReqBtn d-flex justify-content-center align-items-center  m-0 text-nowrap font-10"
                                        name="Raise Request" data-bs-toggle="modal" @click="raiseRequest"
                                        data-bs-target="#riaseRequestModal" />
                                    <!-- @click="raiseRequest" -->
                                </div>
                                <div class="">

                                    <FormFields tag="select" placeholder="" class="" name="roles" id="roles"
                                        :Required="false" v-model="business_unit" :options="EzyFormsCompanys" />
                                </div>
                                <div class="logooutbtn m-0">
                                    <div class="btn-group dropdown navbar-nav ms-auto">
                                        <button type="button" class="btn border-0 p-0 me-2 mt-0"
                                            data-bs-toggle="dropdown" aria-expanded="false">
                                            <img src="../assets/Image.svg" />
                                        </button>
                                        <ul class="dropdown-menu dropdown-menu-start p-2">
                                            <div class="d-flex gap-2 align-items-center">
                                                <div v-if="userInitial">
                                                    <li
                                                        class="d-flex justify-content-center align-items-center btn btn-dark">

                                                        {{ userInitial }}

                                                    </li>
                                                </div>
                                                <div>
                                                    <li>
                                                        <div v-if="userEmail" class=" ">
                                                            <span class="fw-medium font-13 "> {{ userEmail }}</span>

                                                        </div>
                                                        <div v-if="userDesigination" class=" ">

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
            <div class="modal-dialog modal-dialog-centered modal-md">
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
                        <!-- <div class="row">
                            <div class="col"> -->

                        <div class=" mb-2">
                            <label class="raise-label" for="">Department to raise</label>
                            <Multiselect :options="deptartmentData.map(dept => dept.name)" @change="SelectedDepartment"
                                v-model="selectedData.SelectedDepartment" placeholder="Select" :multiple="false"
                                class="font-11" :searchable="true" />
                        </div>
                        <!-- <div class=" mb-2">
                            <label class="raise-label" for="">Category</label>
                            <Multiselect :options="categoryOptions" @change="changingCategory"
                                v-model="selectedData.selectedCategory" placeholder="Select" :multiple="false"
                                class="font-11" :searchable="true" />
                        </div> -->
                        <!-- </div> -->
                        <!-- <div class="col"> -->
                        <div class=" mb-2">
                            <label class="raise-label" for="">Form list</label>
                            <Multiselect :options="formList.map(list => list.name)" v-model="selectedData.selectedform"
                                placeholder="Select" @change="SelectedFromchange" :multiple="false" class="font-11"
                                :searchable="true" />
                        </div>
                        <!-- </div> -->

                        <!-- </div> -->
                        <!-- <div v-if="blockArr.length && selectedData.selectedCategory && selectedData.selectedform">
                            <RequestPreview :blockArr="blockArr" :formName="selectedData.selectedform"
                                @formValidation="isFormValid = $event" @updateField="handleFieldUpdate" />
                        </div> -->

                        <!-- <FormFields tag="select" placeholder="Form" class="mb-3" name="roles" id="roles"
                            :Required="false" :options="formList" v-model="selectedData.selectedform" /> -->
                    </div>
                    <div>
                        <div class=" d-flex justify-content-center align-items-center p-3">
                            <!-- <button :disabled="!isFormValid" class="btn btn-dark font-12 w-100" type="submit"
                                @click="raiseRequestSubmission">Raise
                                Request</button> -->
                            <!-- <button class="btn btn-dark font-12 w-100" @click="toRaiseRequest" type="submit"> Raise
                                Request
                            </button> -->
                        </div>
                    </div>

                </div>
            </div>
        </div>
        <div class="modal fade" id="changePassword" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
            aria-labelledby="changePasswordLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-md">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title font-14 fw-bold" id="changePasswordLabel">Change Password</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-2">
                           <div class="position-relative">
                             <label class="raise-label" for="changepass">New Password</label>
                            <input class="form-control m-0 shadow-none font-13" v-model.trim="new_password"
                                placeholder="Enter New Password" :type="showNewPassword ? 'text' : 'password'"
                                id="changepass" @input="validatePassword" />
                            <span v-if="new_password" class="new-pwd-toggle-icon" @click="toggleNewPwdVisibility">
                                <i :class="showNewPassword ? 'bi bi-eye' : 'bi bi-eye-slash'"></i>
                            </span>
                           </div>
                            <span v-if="passwordError" class="text-danger font-10 m-0 ps-2">{{ passwordError }}</span>
                        </div>

                        <div class="mb-2">
                            <div class="position-relative">
                                <label class="raise-label" for="confirmpass">Confirm Password</label>
                            <input class="form-control m-0 shadow-none font-13" v-model.trim="confirm_password"
                                placeholder="Enter Confirm Password" :type="showConfPwdPassword ? 'text' : 'password'"
                                id="confirmpass" @input="checkPasswordsMatch" />
                            <span v-if="confirm_password" class="cnf-pwd-toggle-icon" @click="toggleConfPwdVisibility">
                                <i :class="showConfPwdPassword ? 'bi bi-eye' : 'bi bi-eye-slash'"></i>
                            </span>
                            </div>
                            <span v-if="passwordsMismatch" class="text-danger font-10 m-0 ps-2">Passwords do not
                                match.</span>
                        </div>

                        <label class="font-12">
                            Note : Password must be at least 12 characters with letters, numbers & symbols
                        </label>
                    </div>

                    <div>
                        <div class=" d-flex justify-content-center align-items-center p-3">
                            <button :disabled="isButtonDisabled" class="btn btn-dark font-12 w-100" type="submit" @click="passwordChange()">
                                Confirm New Password</button>
                        </div>
                    </div>

                </div>
            </div>
        </div>
    </div>

</template>

<script setup>
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
import { ref, onMounted, watch, computed, onUnmounted } from 'vue';
// import socket from '../socketService';
// import { io } from "socket.io-client";

// onMounted(() => {
//   socket.on("custom_event", handleCustomEvent);
// });

// onUnmounted(() => {
//   socket.off("custom_event", handleCustomEvent);
// });

// function handleCustomEvent(data) {
// }
const router = useRouter(); // Initialize router

// Define reactive variables
const tabsData = ref([
    { name: 'Dashboard', icon: 'bi bi-columns-gap', route: '/dashboard' },
    { name: 'To do', icon: 'fa-solid fa-list-check', route: '/todo' },
    { name: 'Forms', icon: 'bi bi-file-earmark-text', route: '/forms' },
    { name: 'Settings', icon: 'bi bi-gear', route: '/settings' },
    { name: 'Archive', icon: 'bi bi-archive', route: '/archived' },
    // { name: 'Form Creation', icon: 'bi bi-file-earmark-text', route: '/create-form' }
]);

const selectedData = ref({
    SelectedDepartment: '',
    selectedCategory: "",
    selectedform: ""
});
const isFormValid = ref(false);
const route = useRoute(); // Initialize route to access route parameters
const categoryOptions = ref([])
const formList = ref([])
const business_unit = ref(EzyBusinessUnit.value);
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
const departmentList = ref([]);
const activeTab = ref('')
const filterObj = ref({
    limit_start: 0,
    limitPageLength: 100,
});

const SocketList = ref([])

//IF THE USER DESIGNATION INCLUDES (IT) THEN ONLY FORM CREATION WILL APPREAR IN HEADER ""

const filteredTabsData = computed(() => {
    return userDesigination.value.toLowerCase().includes('it')
        ? tabsData.value
        : tabsData.value.filter(tab => tab.name !== 'Form Creation');
});
function logout() {
    // localStorage.removeItem('UserName');
    // localStorage.removeItem('employeeData');
    axiosInstance.post(apis.logout)
        .then((response) => {
            localStorage.removeItem('UserName');
            localStorage.removeItem('employeeData');
            localStorage.removeItem('Bu');
            localStorage.removeItem('USERROLE');
            sessionStorage.removeItem('UserName');
            sessionStorage.removeItem('employeeData');
            sessionStorage.removeItem('Bu');
            sessionStorage.removeItem('USERROLE');
            router.push({ path: '/' }).then(() => {
            });
        })
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
    localStorage.setItem("Bu", EzyBusinessUnit.value)
    // Retrieve data from localStorage
    const userData = JSON.parse(localStorage.getItem('employeeData'));
    const userName = JSON.parse(localStorage.getItem('UserName'));
    // const syetemmanger = JSON.parse(localStorage.getItem('systemManager'))
    if (userName) {
        // Set the username based on the UserName data, which is used to check if the user is Admin
        username.value = userName.full_name;

        if (userName.full_name === 'Administrator') {

            userAdmin.value = userName.full_name;
            userInitial.value = userName.full_name.charAt(0).toUpperCase();
        } else if (userData) {
            // Non-admin login: Set both employee and user-specific data
            userAdmin.value = userName.full_name;
            userInitial.value = userData.emp_name.charAt(0).toUpperCase() || userData.full_name.charAt(0).toUpperCase();
            userEmail.value = userData.name;
            userDesigination.value = userData.designation || '';

        }
    } else {
        console.warn("No user data found in localStorage.");
    }
});

// const new_password = ref("");
// const confirm_password = ref("");
const showNewPassword = ref(false);
const showConfPwdPassword = ref(false);
const passwordError = ref("");
// const passwordsMismatch = ref(false);

const toggleNewPwdVisibility = () => {
    showNewPassword.value = !showNewPassword.value;
};

const toggleConfPwdVisibility = () => {
    showConfPwdPassword.value = !showConfPwdPassword.value;
};

const validatePassword = () => {
    const pwd = new_password.value;

    const regex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,}$/;

    if (!regex.test(pwd)) {
        passwordError.value =
            "Password must be at least 12 characters with letters, numbers & symbols.";
    } else {
        passwordError.value = "";
    }

    checkPasswordsMatch();
};

const checkPasswordsMatch = () => {
    passwordsMismatch.value =
        new_password.value && confirm_password.value && new_password.value !== confirm_password.value;
};


const isPasswordValid = computed(() => {
  const regex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,}$/;
  return regex.test(new_password.value);
});

const isButtonDisabled = computed(() => {
  return (
    !new_password.value ||                  // New password is empty
    !confirm_password.value ||              // Confirm password is empty
    !isPasswordValid.value ||               // Password does not meet the regex
    new_password.value !== confirm_password.value // Passwords do not match
  );
});


// const shouldShowButton = computed(() => {
//     const pathsToMatch = ['/forms/department', '/todo'];
//     return pathsToMatch.some(path => route.path.includes(path));
// });
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
            toast.success('Password changed Successfully', { autoClose: 300 });
            const modal = bootstrap.Modal.getInstance(document.getElementById('changePassword'));
            modal.hide();
            new_password.value = '';
            confirm_password.value = '';
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
            if (EzyFormsCompanys.value.length && !business_unit.value.length) {
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
    sessionStorage.setItem("Bu", EzyBusinessUnit.value)

    if (route.path.includes('forms') && newBu !== oldBu) {
        gettingDepartmentNames(true);
    } else if (route.path.includes('forms') && newBu === oldBu) {

        gettingDepartmentNames();
    }
});

function logoClick() {
    router.push({
        path: '/dashboard/maindash'
    })
}
function gettingDepartmentNames() {
    let dataObj = {
        business_unit: business_unit.value
    };


    axiosInstance
        .post(apis.DepartmentNames, dataObj)
        .then((response) => {
            deptartmentData.value = response.message;
            formSideBarData.value = deptartmentData.value
                .sort((a, b) => a.department_name.localeCompare(b.department_name))
                .map(department => ({
                    name: department.department_name,
                    route: department.name,
                }));
        })
        .catch((error) => {
            console.log(error);
        });
}

function deptData(value = null) {
    const filters = [
        ["business_unit", "like", `%${business_unit.value}%`]
    ];
    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify(filters),
        order_by: "`tabEzy Departments`.`department_name` asc",

    };

    axiosInstance.get(apis.resource + doctypes.departments, { params: queryParams })
        .then((res) => {
            if (res.data) {
                deptartmentData.value = res.data;
                departmentList.value = deptartmentData.value

                // departmentList.value = res.data.map((dept) => (dept.name));
                // Update the route for the "Forms" tab with the first department's route
                const newFormsRoute = deptartmentData.value.length > 0
                    ? `/forms/department/allforms`
                    : '/forms/department/allforms';

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



function SelectedFromchange(value) {
    blockArr.value = [];
    selectedData.value.selectedform = value;

    if (!value) return;

    // Get USERROLE from localStorage and normalize
    let userRole = localStorage.getItem("USERROLE")?.trim().toLowerCase();
    // Remove any extra quotes (if present) around the userRole
    userRole = userRole?.replace(/^"|"$/g, ''); // Remove surrounding quotes

    if (!userRole) {
        toast.error("User role is missing. Please log in again.", { autoClose: 2000 });
        return;
    }

    // Find the selected form in formList
    const selectedForm = formList.value.find(form => form.form_short_name === value);

    if (!selectedForm) {
        toast.error("Selected form does not exist in the fetched list.", { autoClose: 2000 });
        return;
    }

    try {
        // Parse form_json since it's stored as a string
        const formJson = JSON.parse(selectedForm.form_json);

        // Find the requestor object in the workflow array
        const requestor = formJson.workflow?.find(item => item.type === "requestor");

        if (!requestor || !Array.isArray(requestor.roles)) {
            toast.error("Invalid requestor data.", { autoClose: 2000 });
            return;
        }

        // Ensure requestor.roles is an array of strings and normalize
        const normalizedRoles = requestor.roles.map(role => role.trim().toLowerCase());

        // Clean the strings to remove any non-alphanumeric characters (like invisible characters)
        const cleanRole = (str) => str.replace(/[^\x20-\x7E]/g, '').trim().toLowerCase();

        const cleanedNormalizedRoles = normalizedRoles.map(role => cleanRole(role));
        const cleanedNormalizedUserRole = cleanRole(userRole);


        // Explicit comparison check with logs
        cleanedNormalizedRoles.forEach((role, index) => {
            console.log(`Comparing role[${index}]: "${role}" with userRole: "${cleanedNormalizedUserRole}"`);
        });

        // Check if the user's role exists in the cleaned requestor's roles array
        const isRoleMatched = cleanedNormalizedRoles.some(role => role === cleanedNormalizedUserRole);

        if (isRoleMatched) {
            toRaiseRequest(); // Call toRaiseRequest() when there's a match
        } else {
            toast.error("You do not have permission to raise this request.", { autoClose: 2000 });
        }
    } catch (error) {

        toast.error("Invalid form data. Please contact support.", { autoClose: 2000 });
    }
}



// Function to fetch and filter forms based on role
function SelectedDepartment(departmentName) {

    // Get USERROLE from localStorage and normalize
    let userRole = localStorage.getItem("USERROLE")?.trim().toLowerCase();
    userRole = userRole?.replace(/^"|"$/g, ""); // Remove surrounding quotes

    if (!userRole) {
        toast.error("User role is missing. Please log in again.", { autoClose: 2000 });
        return;
    }

    const filters = [
        ["enable", "=", 1]
    ];
    if (departmentName) {
        filters.push(["owner_of_the_form", "like", departmentName]);
    }

    const queryParams = {
        fields: JSON.stringify(["*"]),
        limit_page_length: 'None',
        limit_start: filterObj.value.limit_start,
        filters: JSON.stringify(filters),
        order_by: "`tabEzy Form Definitions`.`creation` desc",
    };

    axiosInstance
        .get(`${apis.resource}${doctypes.EzyFormDefinitions}`, { params: queryParams })
        .then((res) => {
            let allForms = res.data; // Store fetched form list

            // Filter forms based on user role
            let allowedForms = allForms.filter((form) => {
                try {
                    const formJson = JSON.parse(form.form_json); // Parse JSON
                    const requestor = formJson?.workflow?.find((item) => item.type === "requestor");

                    if (!requestor || !Array.isArray(requestor.roles)) {
                        return false;
                    }

                    // Normalize and clean roles
                    const normalizedRoles = requestor.roles.map((role) => role.trim().toLowerCase());
                    const cleanRole = (str) => str.replace(/[^\x20-\x7E]/g, "").trim().toLowerCase();
                    const cleanedRoles = normalizedRoles.map(cleanRole);
                    const cleanedUserRole = cleanRole(userRole);


                    // Check if userRole exists in cleaned roles
                    return cleanedRoles.includes(cleanedUserRole);
                } catch (error) {
                    console.error("Error parsing form_json for form:", form.form_short_name, error);
                    return false;
                }
            });

            if (allowedForms.length === 0) {
                toast.warning("No forms have been created in this department.", { autoClose: 2000, transition: "zoom", });
            }
            formList.value = allowedForms; // Only store role-matched forms
        })
        .catch((error) => {
            console.error("Error fetching ezyForms data:", error);
            toast.error("Error fetching forms. Please try again.", { autoClose: 2000, transition: "zoom", });
        });
}



const emittedFormData = ref([]);
const filepaths = ref('')
function raiseRequest() {
    gettingDepartmentNames()
}


function toRaiseRequest() {
    const modal = bootstrap.Modal.getInstance(document.getElementById('riaseRequestModal'));
    modal.hide();
    router.push({
        name: "RaiseRequest", // Ensure this route is defined in your router
        query: {
            routepath: route.path,
            selectedCategory: selectedData.value.selectedCategory,
            selectedForm: selectedData.value.selectedform,
            business_unit: business_unit.value,
        }
    });
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

<style lang="scss" scoped>
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

.imgmix {
    cursor: pointer;
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

.raiseReqBtn {
    border: 1px solid #FE212E !important;
    font-size: 12px;
}

.raiseReqBtn:hover {

    background-color: #FE212E;
    color: #fff;

}

@media (min-width: 1604px) and (max-width: 2400px) {
    .col-3 {
        width: 27%;

    }

}

.stickyheader {
    z-index: 10;
    // box-shadow: rgba(0, 0, 0, 0.1) 0px 10px 15px -3px, rgba(0, 0, 0, 0.05) 0px 4px 6px -2px;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 3px 3px -3px, rgba(0, 0, 0, 0.05) 0px 4px 6px -2px;

    // box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.raise-label {
    font-size: 13px;
    font-weight: 500;
    margin-bottom: 2px;
}


.multiselect-option {
    font-size: 11px !important;
}

.multiselect {
    height: 30px !important;
}

.multiselect {
    margin: initial;
    font-size: 11px !important;
    border: 1px solid #e2e2e2 !important;
    height: 30px !important;

    .multiselect-wrapper {
        height: 30px !important;
    }

    .multiselect-dropdown {
        .multiselect-options {
            font-size: 11px;

            li.multiselect-option span {
                font-size: 11px !important;
            }

            li.multiselect-option .is-selected {
                background-color: grey !important;
                font-size: 11px;
            }
        }
    }
}

.multiselect__option span {
    font-size: 11px;
    /* Change this value to whatever size you need */
}

.multiselect .multiselect-option {
    font-size: 11px;
}

.multiselect .multiselect-wrapper {
    min-height: 30px !important;
}

.multiselect .multiselect--above {
    min-height: 30px !important;
}

.multiselect__tags {
    min-height: 30px !important;
    padding: 0px;
}

.multiselect .multiselect__tags {
    min-height: 30px !important;
    font-size: 11px !important;
}

.multiselect .multiselect__placeholder {
    font-size: 11px;
}

.multiselect .multiselect__single {
    font-size: 11px !important;
}

.multiselect__single {
    font-size: 11px !important;
}

.multiselect__single {
    font-size: 11px !important;

}

.multiselect .multiselect__tags .multiselect__placeholder {
    font-size: 11px;
}

::v-deep(.multiselect__placeholder) {
    color: #343434;
    display: inline-block;
    margin-bottom: 10px;
    padding-top: 2px;
    font-size: 10px !important;
}

input::placeholder {
    font-size: 12px;
}

.new-pwd-toggle-icon {
    position: absolute;
    top: 73%;
    right: 20px;
    transform: translateY(-50%);
    cursor: pointer;
}

.cnf-pwd-toggle-icon {
    position: absolute;
    top: 73%;
    right: 20px;
    transform: translateY(-50%);
    cursor: pointer;
}
</style>