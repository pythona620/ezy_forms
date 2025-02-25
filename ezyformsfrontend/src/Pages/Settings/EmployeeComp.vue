<template>
  <div>
    <div class="d-flex justify-content-between align-items-center py-2">
      <div>
        <h1 class="m-0 font-13">
          Employees
          <!-- ({{ totalRecords }}) -->
        </h1>
        <!-- <p class="m-0 font-11 pt-1">
                374 users
            </p> -->
      </div>
      <div class="d-flex align-items-center">
        <button
          type="button"
          class="btn btn-dark buttoncomp CreateDepartments d-flex align-items-center"
          data-bs-toggle="modal"
          data-bs-target="#createDepartments"
          @click="createEmplBtn"
        >
          Create Employee
        </button>
      </div>
      <div
        class="modal fade"
        id="createDepartments"
        data-bs-backdrop="static"
        tabindex="-1"
        data-bs-keyboard="false"
        aria-labelledby="createDepartmentsLabel"
        aria-hidden="true"
      >
        <div class="modal-dialog modal-lg">
          <div class="modal-content">
            <div class="modal-header">
              <h5 class="modal-title" id="createDepartmentsLabel">
                Ezy Employee
              </h5>
              <button
                type="button"
                class="btn-close"
                data-bs-dismiss="modal"
                @click="cancelCreate"
                aria-label="Close"
              ></button>
            </div>
            <div class="modal-body">
              <div class="container-fluid">
                <div class="row">
                  <div class="col">
                    <label class="font-13 ps-1" for="emp_name"
                      >Emp Name<span class="text-danger ps-1">*</span></label
                    >
                    <FormFields
                      class="mb-3"
                      tag="input"
                      type="text"
                      name="emp_name"
                      id="emp_name"
                      placeholder="Enter Emp Name"
                      v-model="createEmployee.emp_name"
                    />
                    <label class="font-13 ps-1" for="emp_code"
                      >Emp code<span class="text-danger ps-1">*</span></label
                    >
                    <FormFields
                      class="mb-3"
                      tag="input"
                      type="text"
                      name="emp_code"
                      id="emp_code"
                      placeholder="Enter Emp code"
                      v-model="createEmployee.emp_code"
                    />
                    <div class="mb-3">
                      <label class="font-13 ps-1" for="emp_phone"
                        >Emp Phone<span class="text-danger ps-1">*</span></label
                      >
                      <FormFields
                        tag="input"
                        type="text"
                        name="emp_phone"
                        id="emp_phone"
                        maxlength="10"
                        @change="validatephone"
                        placeholder="Enter Phone Numver"
                        v-model="createEmployee.emp_phone"
                      />
                      <p v-if="phoneError" class="text-danger font-11 ps-1">
                        {{ phoneError }}
                      </p>
                    </div>
                    <div class="mb-3">
                      <label class="font-13 ps-1" for="emp_mail_id"
                        >Emp Mail ID<span class="text-danger ps-1"
                          >*</span
                        ></label
                      >
                      <FormFields
                        class="mb-1"
                        tag="input"
                        type="email"
                        name="emp_mail_id"
                        @change="validateEmail"
                        :required="true"
                        id="emp_mail_id"
                        placeholder="Enter Email"
                        v-model="createEmployee.emp_mail_id"
                      />
                      <p v-if="emailError" class="text-danger font-11 ps-1">
                        {{ emailError }}
                      </p>
                    </div>
                    <label class="font-13 ps-1 fw-medium" for="dept"
                      >Departments<span class="text-danger ps-1">*</span></label
                    >
                    <!-- <FormFields tag="select" placeholder="Select Department" class="mb-3"
                                            name="dept" v-model="createEmployee.department" id="dept" :Required="false"
                                            :options="departmentsList" /> -->
                    <VueMultiselect
                      v-model="createEmployee.department"
                      :options="departmentsList"
                      :multiple="false"
                      :close-on-select="true"
                      :clear-on-select="false"
                      :preserve-search="true"
                      placeholder="Select department"
                      class="font-11 mb-3"
                    >
                      <!-- taggable @tag="addDepartment"
                                            tag-placeholder="Press enter to add department" -->
                      <!-- <template #option="{ option }">
                                                <div class="custom-option">
                                                    <input type="checkbox" :checked="createEmployee.department.includes(
                        option
                    )
                        " class="custom-checkbox" />
                                                    <span>{{ option }}</span>
                                                </div>
                                            </template> -->

                      <template #selection="{ values, isOpen }">
                        <span
                          class="multiselect__single font-10"
                          v-if="values.length"
                          v-show="!isOpen"
                        >
                          {{ values.join(", ") }}
                        </span>
                      </template>
                    </VueMultiselect>
                  </div>
                  <div class="col">
                    <label class="font-13 ps-1" for="Designation"
                      >Designation<span class="text-danger ps-1">*</span></label
                    >
                    <!-- <FormFields class="mb-3" tag="input" type="text" name="Designation"
                                                id="Designation" placeholder="Enter Designation"
                                                v-model="createEmployee.designation" /> -->
                    <!-- <FormFields tag="select" placeholder="Select Desigination" class="mb-3"
                                            name="Designation" v-model="createEmployee.designation" id="dept"
                                            :Required="false" :options="designations" /> -->
                    <VueMultiselect
                      v-model="createEmployee.designation"
                      :options="designations"
                      :multiple="false"
                      :close-on-select="true"
                      :clear-on-select="false"
                      :preserve-search="true"
                      placeholder="Select designation"
                      class="font-11 mb-3"
                      taggable
                      @tag="addDesignation"
                      tag-placeholder="Press enter to add designation"
                    >
                      <!-- <template #option="{ option }">
                                                <div class="custom-option">
                                                    <input type="checkbox" :checked="createEmployee.designation.includes(
                        option
                    )
                        " class="custom-checkbox" />
                                                    <span>{{ option }}</span>
                                                </div>
                                            </template> -->

                      <template #selection="{ values, isOpen }">
                        <span
                          class="multiselect__single font-10"
                          v-if="values.length"
                          v-show="!isOpen"
                        >
                          {{ values.join(", ") }}
                        </span>
                      </template>
                    </VueMultiselect>
                    <!-- <div class=""><button @click="addnewDesignation" type="button"
                                                class="btn btn-white text-decoration-underline font-11">Add new
                                                designation <span><i class=" bi bi-plus"></i></span></button>
                                        </div>
                                        <FormFields v-if="newDesignation" class="mb-3" tag="input" type="text"
                                            name="emp_code" id="emp_code" placeholder="Enter Designation"
                                            v-model="inputDesignation" /> -->
                    <label class="font-13 ps-1" for="reporting_to"
                      >Reporting To<span class="text-danger ps-1"
                        >*</span
                      ></label
                    >
                    <!-- <FormFields class="mb-3" tag="input" type="text" name="reporting_to"
                                            id="reporting_to" placeholder="Enter Reporting To"
                                            v-model="createEmployee.reporting_to" /> -->
                    <VueMultiselect
                      v-model="createEmployee.reporting_to"
                      :options="tableData.map((dept) => dept.emp_name)"
                      :multiple="false"
                      :close-on-select="true"
                      :clear-on-select="false"
                      :preserve-search="true"
                      placeholder="Select Reporting To"
                      class="font-11 mb-3"
                    >
                      <!-- taggable
                                            @tag="addReportingTo" tag-placeholder="Press enter to add reporting to" -->
                      <!-- <template #option="{ option }">
                                                <div class="custom-option">
                                                    <input type="checkbox" :checked="createEmployee.reporting_to.includes(
                        option
                    )
                        " class="custom-checkbox" />
                                                    <span>{{ option }}</span>
                                                </div>
                                            </template> -->

                      <template #selection="{ values, isOpen }">
                        <span
                          class="multiselect__single font-10"
                          v-if="values.length"
                          v-show="!isOpen"
                        >
                          {{ values.join(", ") }}
                        </span>
                      </template>
                    </VueMultiselect>
                    <label class="font-13 ps-1" for="reporting_designation"
                      >Reporting Designation<span class="text-danger ps-1"
                        >*</span
                      ></label
                    >
                    <!-- <FormFields class="mb-3" tag="input" type="text" name="reporting_designation"
                                            id="reporting_designation" placeholder="Enter Reporting Designation"
                                            v-model="createEmployee.reporting_designation" /> -->
                    <VueMultiselect
                      v-model="createEmployee.reporting_designation"
                      :options="designations"
                      :multiple="false"
                      :close-on-select="true"
                      :clear-on-select="false"
                      :preserve-search="true"
                      placeholder="Select Reporting Designation"
                      class="font-11 mb-3"
                      disable="true"
                    >
                      <!-- taggable
                                            @tag="addReportingDesignation"
                                            tag-placeholder="Press enter to add reporting designation" -->
                      <!-- <template #option="{ option }">
                                                <div class="custom-option">
                                                    <input type="checkbox" :checked="createEmployee.designation.includes(
                        option
                    )
                        " class="custom-checkbox" />
                                                    <span>{{ option }}</span>
                                                </div>
                                            </template> -->

                      <template #selection="{ values, isOpen }">
                        <span
                          class="multiselect__single font-10"
                          v-if="values.length"
                          v-show="!isOpen"
                        >
                          {{ values.join(", ") }} selected
                        </span>
                      </template>
                    </VueMultiselect>
                    <div class="mb-3 font-11">
                      <label
                        for="signatureInput"
                        class="form-label mb-0 font-13 ps-1"
                      >
                        Add Signature 
                      </label>
                      <input
                        type="file"
                        ref="signatureInputRef"
                        class="form-control font-12 mb-2"
                        id="signatureInput"
                        @change="selectedSignature"
                        aria-describedby="fileHelpId"
                      />

                      <div
                        v-if="createEmployee.signature" style="max-width: 100px; max-height: 100px;"
                        class="d-flex justify-center position-relative mt-2"
                      >
                        <i
                          class="bi bi-x-lg position-absolute text-danger cursor-pointer"
                          style="
                            top: -7px;
                            right: -5px;
                            font-size: 13px;
                            background: white;
                            border-radius: 50%;
                            padding: 3px;
                          "
                          @click="removeSignature"
                        >
                        </i>
                        <img
                          :src="createEmployee.signature" style="max-width: 100px; max-height: 100px;"
                          alt="Signature"
                          class="img-fluid signature-img border-1"
                        />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
            <div class="modal-footer">
              <ButtonComp
                type="button"
                class="cancelfilter border-1 text-nowrap font-10"
                name="Cancel"
                @click="cancelCreate"
                data-bs-dismiss="modal"
              />

              <!-- :disabled="isFormEmpty" -->
              <!-- :disabled="!isFormFilled" -->
              <button
                type="button"
                class="applyfilter btn btn-dark text-nowrap font-10 d-flex justify-content-center align-items-center"
                @click="createEmpl"
              >
                <span class="font-16 me-1"><i class="bi bi-check2"></i></span>
                Create Employee
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="mt-2">
      <GlobalTable
        :tHeaders="tableheaders"
        :tData="tableData"
        isAction="true"
        :actions="actions"
        @actionClicked="actionCreated" @toggle-click="toggleFunction"
        actionType="Toogle&dropdown"
        isCheckbox="true"
        isFiltersoption="true"
        :field-mapping="fieldMapping"
        @updateFilters="inLineFiltersData"
      />
      <PaginationComp
        :currentRecords="tableData.length"
        :totalRecords="totalRecords"
        @updateValue="PaginationUpdateValue"
        @limitStart="PaginationLimitStart"
      />
    </div>
    <div
      class="modal fade"
      id="viewEmployee"
      data-bs-backdrop="static"
      data-bs-keyboard="false"
      tabindex="-1"
      aria-labelledby="viewEmployeeLabel"
      aria-hidden="true"
    >
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="viewEmployeeLabel">Ezy Employee</h5>
            <button
              type="button"
              class="btn-close"
              data-bs-dismiss="modal"
              @click="cancelCreate"
              aria-label="Close"
            ></button>
          </div>
          <div class="modal-body">
            <div class="container-fluid">
              <div class="row">
                <div class="col">
                  <label class="font-13 ps-1" for="emp_name"
                    >Emp Name<span class="text-danger ps-1">*</span></label
                  >
                  <FormFields
                    class="mb-3"
                    tag="input"
                    type="text"
                    name="emp_name"
                    id="emp_name"
                    placeholder="Enter department code"
                    v-model="createEmployee.emp_name"
                  />
                  <label class="font-13 ps-1" for="emp_code"
                    >Emp code<span class="text-danger ps-1">*</span></label
                  >
                  <FormFields
                    class="mb-3"
                    tag="input"
                    type="text"
                    name="emp_code"
                    id="emp_code"
                    placeholder="Enter department code"
                    v-model="createEmployee.emp_code"
                  />
                  <div class="mb-3">
                    <label class="font-13 ps-1" for="emp_phone"
                      >Emp Phone<span class="text-danger ps-1">*</span></label
                    >
                    <FormFields
                      tag="input"
                      type="text"
                      name="emp_phone"
                      id="emp_phone"
                      maxlength="10"
                      @change="validatephone"
                      placeholder="Enter Phone Number"
                      v-model="createEmployee.emp_phone"
                    />
                    <p v-if="phoneError" class="text-danger font-11 ps-1">
                      {{ phoneError }}
                    </p>
                  </div>
                  <div class="mb-3">
                    <label class="font-13 ps-1" for="emp_mail_id"
                      >Emp Mail ID<span class="text-danger ps-1">*</span></label
                    >
                    <FormFields
                      class="mb-1"
                      tag="input"
                      type="email"
                      name="emp_mail_id"
                      @change="validateEmail"
                      :required="true"
                      id="emp_mail_id"
                      placeholder="Enter Email"
                      v-model="createEmployee.emp_mail_id"
                    />
                    <p v-if="emailError" class="text-danger font-11 ps-1">
                      {{ emailError }}
                    </p>
                  </div>
                  <label class="font-13 ps-1 fw-medium" for="dept"
                    >Departments<span class="text-danger ps-1">*</span></label
                  >
                  <VueMultiselect
                    v-model="createEmployee.department"
                    :options="departmentsList"
                    :multiple="false"
                    :close-on-select="true"
                    :clear-on-select="false"
                    :preserve-search="true"
                    placeholder="Select department"
                    class="font-11 mb-3"
                  >
                    <!-- taggable @tag="addDepartment"
                                            tag-placeholder="Press enter to add department" -->
                    <!-- <template #option="{ option }">
                                                <div class="custom-option">
                                                    <input type="checkbox" :checked="createEmployee.department.includes(
                        option
                    )
                        " class="custom-checkbox" />
                                                    <span>{{ option }}</span>
                                                </div>
                                            </template> -->

                    <template #selection="{ values, isOpen }">
                      <span
                        class="multiselect__single font-10"
                        v-if="values.length"
                        v-show="!isOpen"
                      >
                        {{ values.join(", ") }}
                      </span>
                    </template>
                  </VueMultiselect>
                </div>
                <div class="col">
                  <label class="font-13 ps-1" for="Designation"
                    >Designation<span class="text-danger ps-1">*</span></label
                  >
                  <VueMultiselect
                    v-model="createEmployee.designation"
                    :options="designations"
                    :multiple="false"
                    :close-on-select="true"
                    :clear-on-select="false"
                    :preserve-search="true"
                    placeholder="Select designation"
                    class="font-11 mb-3"
                    taggable
                    @tag="addDesignation"
                    tag-placeholder="Press enter to add designation"
                  >
                    <!-- <template #option="{ option }">
                                                <div class="custom-option">
                                                    <input type="checkbox" :checked="createEmployee.designation.includes(
                        option
                    )
                        " class="custom-checkbox" />
                                                    <span>{{ option }}</span>
                                                </div>
                                            </template> -->

                    <template #selection="{ values, isOpen }">
                      <span
                        class="multiselect__single font-10"
                        v-if="values.length"
                        v-show="!isOpen"
                      >
                        {{ values.join(", ") }}
                      </span>
                    </template>
                  </VueMultiselect>
                  <label class="font-13 ps-1" for="reporting_to"
                    >Reporting To<span class="text-danger ps-1">*</span></label
                  >
                  <VueMultiselect
                    v-model="createEmployee.reporting_to"
                    :options="tableData.map((dept) => dept.emp_name)"
                    :multiple="false"
                    :close-on-select="true"
                    :clear-on-select="false"
                    :preserve-search="true"
                    placeholder="Select Reporting To"
                    class="font-11 mb-3"
                  >
                    <!-- taggable
                                        @tag="addReportingTo" tag-placeholder="Press enter to add reporting to" -->
                    <!-- <template #option="{ option }">
                                                <div class="custom-option">
                                                    <input type="checkbox" :checked="createEmployee.reporting_to.includes(
                        option
                    )
                        " class="custom-checkbox" />
                                                    <span>{{ option }}</span>
                                                </div>
                                            </template> -->

                    <template #selection="{ values, isOpen }">
                      <span
                        class="multiselect__single font-10"
                        v-if="values.length"
                        v-show="!isOpen"
                      >
                        {{ values.join(", ") }}
                      </span>
                    </template>
                  </VueMultiselect>
                  <label class="font-13 ps-1" for="reporting_designation"
                    >Reporting Designation<span class="text-danger ps-1"
                      >*</span
                    ></label
                  >
                  <VueMultiselect
                    v-model="createEmployee.reporting_designation"
                    :options="designations"
                    :multiple="false"
                    :close-on-select="true"
                    :clear-on-select="false"
                    :preserve-search="true"
                    placeholder="Select Reporting Designation"
                    class="font-11 mb-3"
                    disable="true"
                  >
                    <!-- taggable
                                        @tag="addReportingDesignation"
                                        tag-placeholder="Press enter to add reporting designation" -->
                    <!-- <template #option="{ option }">
                                                <div class="custom-option">
                                                    <input type="checkbox" :checked="createEmployee.designation.includes(
                        option
                    )
                        " class="custom-checkbox" />
                                                    <span>{{ option }}</span>
                                                </div>
                                            </template> -->

                    <template #selection="{ values, isOpen }">
                      <span
                        class="multiselect__single font-10"
                        v-if="values.length"
                        v-show="!isOpen"
                      >
                        {{ values.join(", ") }} selected
                      </span>
                    </template>
                  </VueMultiselect>
                  <div class="mb-3 font-11">
                      <label
                        for="signatureInput"
                        class="form-label mb-0 font-13 ps-1"
                      >
                        Add Signature 
                      </label>
                      <input
                        type="file"
                        ref="signatureInputRef"
                        class="form-control font-12 mb-2"
                        id="signatureInput"
                        @change="selectedSignature"
                        aria-describedby="fileHelpId"
                      />

                      <div
                        v-if="createEmployee.signature"
                        class="d-flex justify-center position-relative mt-2"
                      >
                        <i
                          class="bi bi-x-lg position-absolute text-danger cursor-pointer"
                          style="
                            top: -7px;
                            right: -5px;
                            font-size: 13px;
                            background: white;
                            border-radius: 50%;
                            padding: 3px;
                          "
                          @click="removeSignature"
                        >
                        </i>
                        <img
                          :src="createEmployee.signature"
                          alt="Signature"
                          class="img-fluid signature-img"
                        />
                      </div>
                    </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <ButtonComp
              type="button"
              class="cancelfilter border-1 text-nowrap font-10"
              name="Cancel"
              @click="cancelCreate"
              data-bs-dismiss="modal"
            />

            <ButtonComp
              type="button"
              class="btn btn-dark font-11"
              name="Save Employee"
              data-bs-dismiss="modal"
              @click="SaveEditEmp"
            />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script setup>
import FormFields from "../../Components/FormFields.vue";
import ButtonComp from "../../Components/ButtonComp.vue";
import GlobalTable from "../../Components/GlobalTable.vue";
import PaginationComp from "../../Components/PaginationComp.vue";
import axiosInstance from "../../shared/services/interceptor";
import { apis, doctypes } from "../../shared/apiurls";
import { onMounted, reactive, ref, computed, watch } from "vue";
// import Multiselect from "@vueform/multiselect";
import "@vueform/multiselect/themes/default.css";
import VueMultiselect from "vue-multiselect";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import { domain } from "../../shared/apiurls";
const businessUnit = computed(() => {
  return EzyBusinessUnit.value;
});

const tableData = ref([]);
const newbusiness = ref("");
const totalRecords = ref(0);
const designations = ref([]);
const reportingTo = ref([]);
const reportingDesigination = ref([]);
const departmentsList = ref([]);
// const newDesignation = ref(false);
// const signaturePath = ref("");
const phoneError = ref("");
const signatureInputRef = ref(null);
const createEmployee = ref({
  emp_code: "",
  emp_name: "",
  emp_phone: "",
  emp_mail_id: "",
  department: "",
  designation: "",
  reporting_to: "",
  reporting_designation: "",
  company_field: "",
  signature: "",
});
const emailError = ref("");

const validateEmail = () => {
  const email = createEmployee.value.emp_mail_id;
  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

  if (!emailPattern.test(email)) {
    emailError.value = "Invalid email address.";
  } else {
    emailError.value = "";
  }
};
const validatephone = () => {
  const phone = createEmployee.value.emp_phone;
  const phonePattern = /^\d{10}$/;
  phoneError.value = phonePattern.test(phone) ? "" : "Invalid phone number.";
};
const filterObj = ref({
  limitPageLength: "None",
  limit_start: 0,
});
// const addDepartment = (newTag) => {
//     if (!designations.value.includes(newTag)) {
//         designations.value.push(newTag);
//     }
//     createEmployee.value.department = newTag;
// };
const addDesignation = (newTag) => {
  if (!designations.value.includes(newTag)) {
    // Send the new designation to the server
    axiosInstance
      .post(apis.resource + doctypes.roles, { role_name: newTag }) // Adjust payload as needed
      .then((response) => {
        if (response.data) {
          console.log("Role:", response.data);

          // Update local designations list
          // designations.value.push(newTag);
          // createEmployee.value.designation = newTag;
          axiosInstance
            .post(apis.resource + doctypes.designations, {
              role: response.data.role_name,
            }) // Adjust payload as needed
            .then((response) => {
              if (response.data) {
                console.log("Wf role:", response.data);

                // Update local designations list
                designations.value.push(response.data.role);
                createEmployee.value.designation = response.data.role;

                // Fetch updated roles after adding a new one
              }
            })
            .catch((error) => {
              console.error("Error creating designation:", error);
            });
          // Fetch updated roles after adding a new one
        }
      })
      .catch((error) => {
        console.error("Error creating designation:", error);
      });
  }
};
// const addReportingTo = (newTag) => {
//     if (!tableData.value.map(dept => dept.emp_name).includes(newTag)) {
//         tableData.value.push({ emp_name: newTag });
//     }
//     createEmployee.value.reporting_to = newTag;
// };

// const addReportingDesignation = (newTag) => {
//     if (!designations.value.includes(newTag)) {
//         designations.value.push(newTag);
//     }
//     createEmployee.value.reporting_designation = newTag;
// };
const removeSignature = () => {
  createEmployee.value.signature = null; // Reset the signature

  const fileInput = document.getElementById("signatureInput");
  if (fileInput) {
    fileInput.value = "";
  }
};
watch(
  () => createEmployee.value.reporting_to,
  (newValue) => {
    if (newValue) {
      const selectedEmployee = tableData.value.find(
        (emp) => emp.emp_name === newValue
      );
      if (selectedEmployee) {
        createEmployee.value.reporting_designation =
          selectedEmployee.designation || "";
      } else {
        createEmployee.value.reporting_designation = ""; // Reset if no match found
      }
    }
  }
);

// function addnewDesignation() {
//     newDesignation.value = !newDesignation.value
// }
const actions = ref([{ name: "Edit Employee", icon: "fa-solid fa-eye" }]);
const isFormFilled = computed(() => {
  return [
    createEmployee.value.emp_code,
    createEmployee.value.emp_name,
    createEmployee.value.emp_mail_id,
    createEmployee.value.department,
    createEmployee.value.designation,
    createEmployee.value.reporting_to,
    createEmployee.value.reporting_designation,
  ].every((field) => field && field.toString().trim() !== "");
});

// const isFormFilled = computed(() => {
//     return createEmployee.value.emp_code &&
//         createEmployee.value.emp_name &&
//         createEmployee.value.emp_mail_id &&
//         createEmployee.value.emp_phone &&
//         createEmployee.value.department &&
//         createEmployee.value.designation &&
//         createEmployee.value.reporting_to &&
//         createEmployee.value.reporting_designation
//         &&
//         createEmployee.value.signature; // Excludes company_field
// });
function createEmplBtn() {
  deptData();
  designationData();
}
function actionCreated(rowData, action, actionEvent) {
    if (action.name === 'Edit Employee') {
        if (rowData) {
            deptData();
            designationData();
            createEmployee.value = { ...rowData }
            const modal = new bootstrap.Modal(document.getElementById('viewEmployee'), {});
            modal.show();
        } else {
            console.warn("No form fields provided.");
            formCreation(rowData);
        }
    }

    // For enable action from the checkbox
   
}


// function actionCreated(rowData, action, actionType) {
//     if (action && action.name === 'Edit Employee') {
//         if (rowData) {
//             deptData();
//             designationData();
//             createEmployee.value = { ...rowData }
//             const modal = new bootstrap.Modal(document.getElementById('viewEmployee'), {});
//             modal.show();
//         } else {
//             console.warn("No form fields provided.");
//             formCreation(rowData);
//         }
//     }
//   }
// }

function toggleFunction(rowData) {
    // console.log("rowData", rowData);

    // Decide the action based on the current state:
    const isCurrentlyEnabled = rowData.enable == '1' || rowData.enable === 1;
    const actionText = isCurrentlyEnabled ? 'Disable' : 'Enable';

    // Show the confirmation dialog with dynamic messaging:
    if (confirm(`Are you sure you want to ${actionText} ${rowData.emp_name} this Employee?`)) {
        // Toggle the state:
        rowData.enable = isCurrentlyEnabled ? 0 : 1;

        axiosInstance
            .put(`${apis.resource}${doctypes.EzyEmployeeList}/${rowData.name}`, rowData)
            .then((response) => {
                console.log("Response:", response.data);
                // Adjust the toast message accordingly:
                toast.success(`Form ${actionText}d successfully`, { autoClose: 700 });
                // Refresh the table data after a short delay
                employeeData();
                window.location.reload()
            })
            .catch((error) => {
                console.error("Error updating toggle:", error);
            });
    } else {
        // If canceled, do nothing – the checkbox remains unchanged.
        console.log("Action cancelled. Toggle remains unchanged.");
    }
}

const tableheaders = ref([
  { th: "Emp Code", td_key: "emp_code" },
  { th: "Emp Name", td_key: "emp_name" },
  // { th: "Mail", td_key: "emp_mail_id" },
  { th: "Designation", td_key: "designation" },
  { th: "Department", td_key: "department" },
  { th: "Signature", td_key: "signature" },

  { th: "Reporting To", td_key: "reporting_to" },
  // { th: "Reporting Designation", td_key: "reporting_designation" },
]);

const fieldMapping = ref({
  emp_code: { type: "input" },
  emp_name: { type: "input" },
});
// const filtersBeforeApplyingCount = computed(() => {
//     return [filterOnModal.designation, filterOnModal.emp_code, filterOnModal.department, filterOnModal.emp_mail_id, filterOnModal.emp_name, filterOnModal.reporting_designation, filterOnModal.reporting_to].filter(
//         (value) => value
//     ).length;
// });
function cancelCreate() {
  createEmployee.value = {
    emp_code: "",
    emp_name: "",
    emp_phone: "",
    emp_mail_id: "",
    department: "",
    designation: "",
    reporting_to: "",
    reporting_designation: "",
    signature: null,
    company_field: businessUnit.value,
  };
  const fileInput = document.getElementById("signatureInput");
  if (fileInput) {
    fileInput.value = "";
  }
}

function selectedSignature(event) {
  const file = event.target.files[0];
  if (file) {
    uploadFile(file, "signature");
  }
}

// const generateRandomNumber = () => {
//     return Math.floor(Math.random() * 1000000);
// };

const uploadFile = (file, field) => {
  let fileName = `${file.name}`;

  const formData = new FormData();
  formData.append("file", file, fileName);
  formData.append("is_private", "0");
  formData.append("folder", "Home");

  axiosInstance
    .post(apis.uploadfile, formData)
    .then((res) => {
      if (res.message && res.message.file_url) {
        if (field === "signature") {
          createEmployee.value.signature = res.message.file_url;
        }
        console.log("Uploaded file URL:", res.message.file_url);
      } else {
        console.error("file_url not found in the response.");
      }
    })
    .catch((error) => {
      console.error("Upload error:", error);
    });
};
function deptData() {
  const queryParams = {
    fields: JSON.stringify(["*"]),
    limit_page_length: filterObj.value.limitPageLength,
    limit_start: filterObj.value.limit_start,
  };

  axiosInstance
    .get(apis.resource + doctypes.departments, { params: queryParams })
    .then((res) => {
      if (res.data) {
        departmentsList.value = res.data.map((department) => department.name);
      }
    })
    .catch((error) => {
      console.error("Error fetching department data:", error);
    });
}

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

function inLineFiltersData(searchedData) {
  //   // Initialize filters array
  const filters = [];

  //   // Loop through the tableheaders and build dynamic filters based on the `searchedData`
  tableheaders.value.forEach((header) => {
    const key = header.td_key;

    //     // If there is a match for the key in searchedData, create a 'like' filter
    if (searchedData[key]) {
      filters.push(key, "like", `%${searchedData[key]}%`);
    }
    //     // Add filter for selected option
    //     if (key === "selectedOption" && searchedData.selectedOption) {
    //       filters.push([key, "=", searchedData.selectedOption]);
    //     }
    //     // Special handling for 'invoice_date' to create a 'Between' filter (if it's a date)
    //     if (key === "invoice_date" && searchedData[key]) {
    //       filters.push([key, "Between", [searchedData[key], searchedData[key]]]);
    //     }

    //     // Special handling for 'invoice_type' or 'irn_generated' to create an '=' filter
    //     if ((key === "invoice_type" || key === "credit_irn_generated") && searchedData[key]) {
    //       filters.push([key, "=", searchedData[key]]);
    //     }
  });

  //   // Log filters to verify

  //   // Once the filters are built, pass them to fetchData function
  if (filters.length) {
    employeeData(filters);
  } else {
    employeeData();
  }
  //   fetchTotalRecords(filters);
}

function employeeData(data) {
  const filters = [["company_field", "like", `%${newbusiness.value}%`]];
  if (data) {
    filters.push(data);
  }

  const queryParams = {
    fields: JSON.stringify(["*"]),
    filters: JSON.stringify(filters),
    limit_page_length: filterObj.value.limitPageLength,
    limit_start: filterObj.value.limit_start,
    order_by: "`tabEzy Employee`.`creation` desc",
  };
  const queryParamsCount = {
    fields: JSON.stringify(["count(name) AS total_count"]),
    limitPageLength: "None",
    filters: JSON.stringify(filters),
  };
  axiosInstance
    .get(`${apis.resource}${doctypes.EzyEmployeeList}`, {
      params: queryParamsCount,
    })
    .then((res) => {
      totalRecords.value = res.data[0].total_count;
    })
    .catch((error) => {
      console.error("Error fetching ezyForms data:", error);
    });

  axiosInstance
    .get(apis.resource + doctypes.EzyEmployeeList, { params: queryParams })
    .then((res) => {
      if (res.data) {
        tableData.value = res.data;
        // designations.value = [...new Set(res.data.map((designation) => designation.designation))];
        reportingTo.value = [
          ...new Set(res.data.map((reporting) => reporting.reporting_to)),
        ];
        reportingDesigination.value = [
          ...new Set(
            res.data.map(
              (reportingDesigination) =>
                reportingDesigination.reporting_designation
            )
          ),
        ];
        createEmployee.value.company_field = businessUnit.value;
      }
    })
    .catch((error) => {
      console.error("Error fetching department data:", error);
    });
}

function designationData() {
  const filters = [];
  const queryParams = {
    fields: JSON.stringify(["*"]),
    filters: JSON.stringify(filters),
    limit_page_length: filterObj.value.limitPageLength,
    limit_start: filterObj.value.limit_start,
    order_by: "`tabWF Roles`.`creation` desc",
  };

  axiosInstance
    .get(apis.resource + doctypes.designations, { params: queryParams })
    .then((res) => {
      if (res.data) {
        designations.value = [...new Set(res.data.map((user) => user.role))];
      }
    })
    .catch((error) => {
      console.error("Error fetching designations data:", error);
    });
}

watch(
  businessUnit,
  (newVal) => {
    if (newVal && newVal.length) {
      createEmployee.value.company_field = newVal;
      newbusiness.value = newVal;
      console.log(createEmployee.value.company_field, "-----");

      employeeData();
    }
  },
  { immediate: true }
);

function createEmpl() {
  if (!isFormFilled.value) {
    toast.error("Please fill all required fields", {
      autoClose: 1000,
      transition: "zoom",
    });
    return;
  }
  createEmployee.value.company_field = businessUnit.value;
  const dataObj = {
    ...createEmployee.value,
    doctype: doctypes.EzyEmployeeList,
  };

  axiosInstance
    .post(apis.resource + doctypes.EzyEmployeeList, dataObj)
    .then((res) => {
      if (res.data) {
        toast.success("Employee Created", {
          autoClose: 500,
          transition: "zoom",
        });
        const modal = bootstrap.Modal.getInstance(
          document.getElementById("createDepartments")
        );
        modal.hide();

        cancelCreate();
        const fileInput = document.getElementById("signatureInput");
        if (fileInput) {
          fileInput.value = "";
        }
        employeeData();
      }
    });
}
function SaveEditEmp() {
  axiosInstance
    .put(
      `${apis.resource}${doctypes.EzyEmployeeList}/${createEmployee.value.name}`,
      createEmployee.value
    )
    .then((response) => {
      if (response.data) {
        toast.success("Changes Saved", { autoClose: 500, transition: "zoom" });
        employeeData();
      }
    })
    .catch((error) => {
      console.error("Error saving categories:", error);
    });
}
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss" scoped>
.global-table th {
  background-color: #f2f2f2 !important;
  text-align: left;
  color: #999999;
  font-size: 12px;
}

.filterbtn {
  border: 1px solid #cccccc;
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

::v-deep(.multiselect__select) {
  position: absolute;
  width: 40px;
  height: 32px;
  right: 1px;
  /* top: 1px; */
  padding: 4px 8px;
  text-align: center;
  transition: transform 0.2s ease;
}

::v-deep(.multiselect) {
  height: 32px !important;
  min-height: 32px !important;
}

::v-deep(.multiselect__tags) {
  height: 32px !important;
  min-height: 32px !important;
  display: flex;
  align-items: center;
}

::v-deep(.multiselect__single) {
  font-size: 11px !important;
  color: #000;
}

::v-deep(.multiselect-wrapper),
::v-deep(.multiselect-search) {
  height: 32px !important;
  min-height: 32px !important;
  line-height: 32px !important;
  display: flex;
  align-items: center;
}

::v-deep(.multiselect-search) {
  height: 32px !important;
  min-height: 32px !important;
  display: flex;
  align-items: center;
}

::v-deep(.multiselect-wrapper) {
  height: 32px !important;
  min-height: 32px !important;
  line-height: 32px !important;
}

::v-deep(.multiselect-search) {
  position: absolute;
  width: 40px !important;
  height: 32px !important;
  right: 1px;

  padding: 4px 8px;
  text-align: center;
  transition: transform 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

::v-deep(.multiselect__element:hover) {
  background-color: #eeeeee !important;
}

::v-deep(.multiselect__element:hover .multiselect__option) {
  background-color: #eeeeee !important;
  color: #000 !important;
}

::v-deep(.multiselect__element:hover .multiselect__option--highlight) {
  background-color: #eeeeee !important;
  color: #000 !important;
}

/* Additional specific rule for `.multiselect__option` when hovered */
::v-deep(.multiselect__option:hover) {
  background-color: #eeeeee !important;
  color: #000 !important;
}

.custom-option {
  display: flex;
  align-items: center;
  gap: 5px;
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

.signature-img {
  width: 80px;
}
</style>