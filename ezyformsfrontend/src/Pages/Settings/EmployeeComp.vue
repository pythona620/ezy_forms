<template>
  <div>


    <div>
      <div class="d-flex justify-content-between align-items-center py-2">
        <div>
          <h1 class="m-0 font-13">
            Active Employees
            <!-- ({{ totalRecords }}) -->
          </h1>
          <!-- <p class="m-0 font-11 pt-1">
                374 users
            </p> -->
        </div>
        <div class="d-flex align-items-center gap-2">
          <button type="button" class=" btn export-btn  CreateDepartments font-12" data-bs-toggle="modal"
            data-bs-target="#ExportEmployeeModal">
            Export Employees
          </button>

          <button type="button" class=" btn export-btn  CreateDepartments  font-12 " @click="bulkEmp">
            Import Employees
          </button>

          <button type="button" class="btn btn-dark  CreateDepartments " data-bs-toggle="modal"
            data-bs-target="#createDepartments" @click="createEmplBtn">
            Create Employee
          </button>
        </div>
        <div class="modal fade" id="createDepartments" data-bs-backdrop="static" tabindex="-1" data-bs-keyboard="false"
          aria-labelledby="createDepartmentsLabel" aria-hidden="true">
          <div class="modal-dialog modal-lg">
            <div class="modal-content">
              <div class="modal-header">
                <h5 class="modal-title" id="createDepartmentsLabel">
                  Employee Creation
                </h5>
                <button type="button" class="btn-close" data-bs-dismiss="modal" @click="cancelCreate"
                  aria-label="Close"></button>
              </div>
              <div class="modal-body">
                <div class="container-fluid">
                  <div class="row">
                    <div class="col">
                      <label class="font-13 ps-1" for="create_emp_name">Emp Name<span class="text-danger ps-1">*</span></label>
                      <FormFields class="mb-3" tag="input" type="text" name="create_emp_name" id="create_emp_name"
                        placeholder="Enter Emp Name" v-model.trim="createEmployee.emp_name" @input="validateEmpName" />
                      <label class="font-13 ps-1" for="create_emp_code">Emp ID<span class="text-danger ps-1">*</span></label>
                      <FormFields class="mb-3" tag="input" type="text" name="create_emp_code" id="create_emp_code"
                        placeholder="Enter Emp ID" v-model="createEmployee.emp_code" />
                       <div class="mb-3">
                    <label class="font-13 ps-1" for="create_emp_phone">Emp Phone</label>
                    <div class="input-container">
                      <input type="text" name="create_emp_phone" id="create_emp_phone" maxlength="13" 
                        class="w-100 font-12  form-control" 
                        :value="isMasked ? maskNumber(createEmployee.emp_phone) : createEmployee.emp_phone"
                        @input="handleInput" @blur="formatPhoneNumber " placeholder="Enter Phone Number" />
                      <!-- <i :class="eyeIcon" class="eye-icon" @click="toggleMask"></i> -->
                    </div>

                    <p v-if="phoneError" class="text-danger font-11 ps-1">
                      {{ phoneError }}
                    </p>
                  </div>

                      <div class="mb-3">
                        <label class="font-13 ps-1" for="create_emp_mail_id">Emp Mail ID<span
                            class="text-danger ps-1">*</span></label>
                        <FormFields class="mb-1" tag="input" type="email" name="create_emp_mail_id"
                          v-model="createEmployee.emp_mail_id" @input="validateCreateUserEmail" :required="true"
                          id="create_emp_mail_id" placeholder="Enter Email Id" />
                        <p v-if="createEmailError" class="text-danger font-11 ps-1">
                          {{ createEmailError }}
                        </p>
                      </div>
                      <label class="font-13 ps-1 fw-medium" for="dept">Departments<span
                          class="text-danger ps-1">*</span></label>
                      <!-- <FormFields tag="select" placeholder="Select Department" class="mb-3"
                                            name="dept" v-model="createEmployee.department" id="dept" :Required="false"
                                            :options="departmentsList" /> -->
                      <VueMultiselect v-model="createEmployee.department" :options="departmentsList" :multiple="false"
                        @update:modelValue="onDepartmentChange" :close-on-select="true" :clear-on-select="false"
                        :preserve-search="true" placeholder="Select department" label="department_name" track-by="name"
                        class="font-11 mb-3">
                        <template #selection="{ values, isOpen }">
                          <span class="multiselect__single font-10" v-if="values.length" v-show="!isOpen">
                            {{values.map(v => v.department_name).join(", ")}}
                          </span>
                        </template>
                      </VueMultiselect>
                      <div class=" d-flex gap-3">


                        <div class="ms-1">
                          <input type="checkbox" id="isHOD" :true-value='1' :false-value='0'
                            v-model="createEmployee.is_hod" class="form-check-input mt-1 input-border border-1" />
                          <label class="font-13 ms-2 " for="isHOD">Is HOD</label>
                        </div>
                        <div class="ms-1">
                          <input type="checkbox" id="is_admin" :true-value='1' :false-value='0'
                            v-model="createEmployee.is_admin" class="form-check-input mt-1 input-border" />
                          <label class="font-13 ms-2 " for="is_admin">Is Admin</label>
                        </div>
                      </div>

                    </div>
                    <div class="col">
                      <div class="position-relative mb-3">
                        <label class="font-13 ps-1" for="Designation">
                          Designation<span class="text-danger ps-1">*</span>
                        </label>

                        <input type="text" v-model="searchText" @input="() => { filterDesignations(); validateInput(); }"
                        :class="['form-control font-12', errorMessage ? 'border-danger' : '']" class="form-control shadow-none font-12"
                                                placeholder="Search or type new role" />
                                                <p v-if="errorMessage" class="text-danger font-11 ps-1">
                                            {{ errorMessage }}
                                          </p>
                        <ul class="list-group position-absolute w-100 zindex-dropdown"
                          v-if="searchText && (filteredDesignations.length || showCreateButton) && !errorMessage">
                          <li v-for="(role, index) in filteredDesignations" :key="index"
                            class="list-group-item list-group-item-action font-12" @click="selectDesignation(role)"
                            style="cursor: pointer">
                            {{ role }}
                          </li>
                          <li v-if="searchText"
                            class="list-group-item list-group-item-action font-12 text-primary" style="cursor: pointer"
                            @click="showModal = true">
                            <i class="bi bi-plus-lg"></i> Create role "<strong>{{ searchText }}</strong>"
                          </li>
                        </ul>
                        <!-- Modal -->
                        <div class="modal fade" :class="{ show: showModal }" style="display: block;" v-if="showModal">
                          <div class="modal-dialog">
                            <div class="modal-content">
                              <div class="modal-header">
                                <h5 class="modal-title">Create New Role</h5>
                                <button type="button" class="btn-close" @click="closedesignmodal"></button>
                              </div>
                              <div class="modal-body">
                                <label for="" class="font-13 fw-bold">Designation<span class="text-danger ps-1">*</span></label>
                                <input type="text" class="form-control font-12 shadow-none" v-model="newRole" @input="validateRole"
                                  placeholder="Enter role name" :class="{ 'is-invalid': roleError }" />
                                  <span v-if="roleError" class="text-danger font-12 mt-2">{{ roleError }}</span>
                              </div>
                              <div class="modal-footer">
                                <button class="btn btn-secondary" @click="closedesignmodal">Cancel</button>
                                <button class="btn btn-dark" :disabled="!!roleError" @click="createRole">Save Role</button>
                              </div>
                            </div>
                          </div>

                        </div>
                      </div>
                      <!-- <div>
                       <label class="font-13 ps-1" for="Designation">Designation<span
                          class="text-danger ps-1">*</span></label>
                     
                      <VueMultiselect v-model="createEmployee.designation" :options="designations" :multiple="false"
                        :close-on-select="true" :clear-on-select="false" :preserve-search="true"
                        placeholder="Select designation" class="font-11 mb-3" taggable @tag="addDesignation"
                        tag-placeholder="Press enter to add designation">
                        

                        <template #selection="{ values, isOpen }">
                          <span class="multiselect__single font-10" v-if="values.length" v-show="!isOpen">
                            {{ values.join(", ") }}
                          </span>
                        </template>
                      </VueMultiselect>
                     </div> -->
                      <!-- <div class=""><button @click="addnewDesignation" type="button"
                                                class="btn btn-white text-decoration-underline font-11">Add new
                                                designation <span><i class=" bi bi-plus"></i></span></button>
                                        </div>
                                        <FormFields v-if="newDesignation" class="mb-3" tag="input" type="text"
                                            name="emp_code" id="emp_code" placeholder="Enter Designation"
                                            v-model="inputDesignation" /> -->
                      <label class="font-13 ps-1" for="reporting_to">Reports To</label>
                      <!-- <FormFields class="mb-3" tag="input" type="text" name="reporting_to"
                                            id="reporting_to" placeholder="Enter Reports To"
                                            v-model="createEmployee.reporting_to" /> -->
                      <VueMultiselect v-model="createEmployee.reporting_to"
                        :options="employeeEmails.map((dept) => dept.emp_mail_id)" :multiple="false"
                        :close-on-select="true" :clear-on-select="false" :preserve-search="true"
                        placeholder="Select Reports To" class="font-11 mb-3">


                        <template #selection="{ values, isOpen }">
                          <span class="multiselect__single font-10" v-if="values.length" v-show="!isOpen">
                            {{ values.join(", ") }}
                          </span>
                        </template>
                      </VueMultiselect>
                      <label class="font-13 ps-1" for="reporting_designation">Reporting Designation</label>
                      <!-- <FormFields class="mb-3" tag="input" type="text" name="reporting_designation"
                                            id="reporting_designation" placeholder="Enter Reporting Designation"
                                            v-model="createEmployee.reporting_designation" /> -->
                      <VueMultiselect v-model="createEmployee.reporting_designation" :options="designations"
                        :allow-empty="true" :multiple="false" :close-on-select="true" :clear-on-select="false"
                        :preserve-search="true" placeholder="Select Reporting Designation" class="font-11 mb-3"
                        :disabled="!!createEmployee.reporting_to">
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
                          <span class="multiselect__single font-10" v-if="values.length" v-show="!isOpen">
                            {{ values.join(", ") }} selected
                          </span>
                        </template>
                      </VueMultiselect>
                      <div class="mb-3 font-11">
                        <label for="signatureInput" class="form-label mb-0 font-13 ps-1">
                          Add Signature
                        </label>
                        <input type="file" ref="signatureInputRef" class="form-control font-12 mb-2" id="signatureInput"
                          @change="selectedSignature" aria-describedby="fileHelpId" />

                        <div v-if="createEmployee.signature" style="max-width: 100px; max-height: 100px;"
                          class="d-flex justify-center position-relative mt-2">
                          <i class="bi bi-x-lg position-absolute text-danger cursor-pointer" style="
                            top: -7px;
                            right: -5px;
                            font-size: 13px;
                            background: white;
                            border-radius: 50%;
                            padding: 3px;
                          " @click="removeSignature">
                          </i>
                          <img :src="createEmployee.signature" style="max-width: 100px; max-height: 100px;"
                            alt="Signature" class="img-fluid signature-img border-1" />
                        </div>
                      </div>

                    </div>
                  </div>
                </div>
              </div>
              <div class="modal-footer">
                <ButtonComp type="button" class="cancelfilter border-1 text-nowrap font-10" name="Cancel"
                  @click="cancelCreate" data-bs-dismiss="modal" />

                <!-- :disabled="isFormEmpty" -->
                <!-- :disabled="!isFormFilled" -->
                <button type="button"
                  class="applyfilter btn btn-dark text-nowrap font-10 d-flex justify-content-center align-items-center"
                  @click="createEmpl">
                  <span v-if="!loading" class="font-16 me-1"><i class="bi bi-check2"></i></span>
                  <span v-if="!loading">Create Employee</span>
                  <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-if="showEmployeebulk" class="mt-2">
        <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction="true" :actions="actions" enableDisable="true"
          @actionClicked="actionCreated" @toggle-click="toggleFunction" actionType="dropdown" isCheckbox="true"
          isFiltersoption="true" :field-mapping="fieldMapping" @updateFilters="inLineFiltersData" />
        <PaginationComp :currentRecords="tableData.length" :totalRecords="totalRecords"
          @updateValue="PaginationUpdateValue" @limitStart="PaginationLimitStart" />
      </div>
      <div v-else>
        <div class="bulkemployee">
          <div class=" d-flex justify-content-between align-content-center">
            <button type="button" class="font-12 btn btn-light" @click="backtoEmployeeList">
              <i class="bi bi-chevron-left"></i> Back to Employee List
            </button>

          </div>


          <div class="insideBulkEmp ">
            <div class="d-flex justify-content-center align-content-center mb-5 gap-2">
              <div :class="!bulkdata.length ? 'mb-5 mt-5' : ''">
                <button type="button" class="font-12 my-1 btn btn-light" @click="downloadTemplate">
                  <i class="bi bi-download"></i> Use template
                </button>

                <input type="file" ref="fileInput" @change="handleFileChange" hidden />
                <button type="button" class="font-12 my-1 btn btn-dark" @click="triggerFileInput">
                  <i class="bi bi-upload"></i> Upload Data
                </button>
              </div>
            </div>


            <!-- Progress Bar -->
            <transition name="fade">
              <div v-if="uploading" class="loader"></div>
            </transition>

            <div>
              <div class="table-container">
                <div v-if="formattedData.length > 0" class="d-flex justify-content-end align-content-center p-2">

                  <button type="button" class="btn btn-light font-12" @click="downloadExcel"><i
                      class="bi bi-download mx-2"></i>Download Excel</button>
                </div>
                <div v-if="templateWarnings.length" class="warning-box">
                  <h3 class="font-13">Template Warnings:</h3>
                  <ul>
                    <li v-for="(warning, i) in templateWarnings" :key="i">{{ warning }}</li>
                  </ul>
                </div>


                <table v-if="formattedData.length > 0" class="styled-table">
                  <thead>
                    <tr>
                      <th>#</th>
                      <th>Email</th>
                      <th>Status</th>
                      <th>Message</th>
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="(record, index) in formattedData" :key="index">
                      <td>{{ index + 1 }}</td>
                      <td>{{ record.email }}</td>
                      <td :class="record.status === 'success' ? 'status-success' : 'status-failed'">
                        {{ record.status }}
                      </td>
                      <td>{{ record.displayMessage }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>

            </div>
          </div>


        </div>
      </div>
    </div>
    <div class="modal fade" id="exampleModal" data-bs-backdrop="static" tabindex="-1"
      aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="viewEmployeeLabel">Employee Data</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" @click="cancelCreate"
              aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="container-fluid">
              <div class="row">
                <div class="col">
                  <label class="font-13 ps-1" for="emp_name">Emp Name<span class="text-danger ps-1">*</span></label>
                  <FormFields class="mb-3" tag="input" type="text" name="emp_name" id="emp_name"
                    placeholder="Enter Emp Name" v-model.trim="createEmployee.emp_name" @input="validateEmpName" />
                  <label class="font-13 ps-1" for="emp_code">Emp ID<span class="text-danger ps-1">*</span></label>
                  <FormFields class="mb-3" tag="input" type="text" name="emp_code" id="emp_code"
                    placeholder="Enter Emp Id" v-model="createEmployee.emp_code" />
                  <!-- <div class="mb-3">
                        <label class="font-13 ps-1" for="emp_phone">Emp Phone</label>
                        <FormFields tag="input" type="text" name="emp_phone" id="emp_phone" maxlength="10"
                          @change="validatephone" placeholder="Enter Phone Number" v-model="createEmployee.emp_phone" />
                        <p v-if="phoneError" class="text-danger font-11 ps-1">
                          {{ phoneError }}
                        </p>
                      </div> -->
                  <!-- <div class="mb-3">
                    <label class="font-13 ps-1" for="emp_phone">Emp Phone</label>
                    <div class="input-container">
                      <FormFields tag="input" type="text" name="emp_phone" id="emp_phone" maxlength="10" class="w-100"
                        :readonly="true" placeholder="Enter Phone Number" v-model="createEmployee.emp_phone" @blur="maskPhoneNumber"
                        @change="validatePhone" />
                      <i :class="eyeIcon" class="eye-icon" @click="toggleMask"></i>
                    </div>
                    <p v-if="phoneError" class="text-danger font-11 ps-1">
                      {{ phoneError }}
                    </p>
                  </div> -->

                  <div class="mb-3">
                    <label class="font-13 ps-1" for="emp_phone">Emp Phone</label>
                    <div class="input-container">
                      <input type="text" name="emp_phone" id="emp_phone" maxlength="13"
                        class="w-100 font-12  form-control" :readonly="isMasked"
                        :value="isMasked ? maskNumber(createEmployee.emp_phone) : createEmployee.emp_phone"
                        @input="handleInput" @blur="formatPhoneNumber" placeholder="Enter Phone Number" />
                      <i :class="eyeIcon" class="eye-icon" @click="toggleMask"></i>
                    </div>

                    <p v-if="phoneError" class="text-danger font-11 ps-1">
                      {{ phoneError }}
                    </p>
                  </div>



                  <div class="mb-3">
                    <label class="font-13 ps-1" for="emp_mail_id">Emp Mail ID<span
                        class="text-danger ps-1">*</span></label>
                    <div class="input-container">
                      <FormFields class="mb-1 w-100" tag="input" type="email" name="emp_mail_id" id="emp_mail_id"
                        placeholder="Enter Email" v-model="createEmployee.emp_mail_id" @input="maskEmail" :disabled="true"
                        @change="validateEditUserEmail" :required="true" />
                      <i :class="eyeIconEmail" class="eye-icon" @click="toggleEmailMask"></i>
                    </div>
                   <p v-if="editEmailError" class="text-danger font-11 ps-1">
                      {{ editEmailError }}
                   </p>

                  </div>
                  <label class="font-13 ps-1 fw-medium" for="dept">Departments<span
                      class="text-danger ps-1">*</span></label>

                  <VueMultiselect v-model="createEmployee.department" :options="departmentsList" :multiple="false"
                    @update:modelValue="onDepartmentChange" :close-on-select="true" :clear-on-select="false"
                    :preserve-search="true" placeholder="Select department" label="department_name" track-by="name"
                    class="font-11 mb-3">
                    <template #selection="{ values, isOpen }">
                      <span class="multiselect__single font-10" v-if="values.length" v-show="!isOpen">
                        {{values.map(v => v.department_name).join(", ")}}
                      </span>
                    </template>
                  </VueMultiselect>
                  <div class=" d-flex gap-3">


                    <div class="ms-1">
                      <input type="checkbox" id="isHOD" :true-value="1" :false-value="0" v-model="createEmployee.is_hod"
                        class="form-check-input mt-1 input-border border-1" />
                      <label class="font-13 ms-2 " for="isHOD">Is HOD</label>
                    </div>
                    <div class="ms-1">
                      <input type="checkbox" id="is_admin" :true-value='1' :false-value='0'
                        v-model="createEmployee.is_admin" class="form-check-input mt-1 input-border" />
                      <label class="font-13 ms-2 " for="is_admin">Is Admin</label>
                    </div>
                  </div>


                </div>
                <div class="col">
                  <div class="position-relative mb-3">
                    <label class="font-13 ps-1" for="Designation">
                      Designation<span class="text-danger ps-1">*</span>
                    </label>

                    <input type="text" v-model="searchText" @input="() => { filterDesignations(); validateInput(); }" class="form-control font-12"
                      :class="['form-control font-12', errorMessage ? 'border-danger' : '']" placeholder="Search or type new role" />
                      <p v-if="errorMessage" class="text-danger font-11 ps-1">
                                            {{ errorMessage }}
                                          </p>
                    <ul class="list-group position-absolute w-100 zindex-dropdown"
                      v-if="searchText && (filteredDesignations.length || showCreateButton) && !errorMessage">
                      <li v-for="(role, index) in filteredDesignations" :key="index"
                        class="list-group-item list-group-item-action font-12" @click="selectDesignation(role)"
                        style="cursor: pointer">
                        {{ role }}
                      </li>

                      <!-- Create Role option as part of the dropdown -->
                      <li v-if="searchText" class="list-group-item list-group-item-action font-12 text-primary" style="cursor: pointer"
                        @click="showModal = true">
                        <i class="bi bi-plus-lg"></i> Create role "<strong>{{ searchText }}</strong>"
                      </li>

                    </ul>




                    <!-- Modal -->
                    <div class="modal fade" :class="{ show: showModal }" style="display: block;" v-if="showModal">
                      <div class="modal-dialog">
                        <div class="modal-content">
                          <div class="modal-header">
                            <h5 class="modal-title">Create New Role</h5>
                            <button type="button" class="btn-close" @click="showModal = false"></button>
                          </div>
                          <div class="modal-body">
                            <label for="" class="font-12 fw-bold">Designation</label>
                            <input type="text" class="form-control font-12" v-model="newRole"
                              placeholder="Enter role name" />
                          </div>
                          <div class="modal-footer">
                            <button class="btn btn-secondary" @click="showModal = false">Cancel</button>
                            <button class="btn btn-dark" @click="createRole">Save Role</button>
                          </div>
                        </div>
                      </div>

                    </div>
                  </div>
                  <label class="font-13 ps-1" for="reporting_to">Reports To</label>
                  <VueMultiselect v-model="createEmployee.reporting_to"
                    :options="employeeEmails.map((dept) => dept.emp_mail_id)" :multiple="false" :close-on-select="true"
                    :allow-empty="true" :clear-on-select="false" :preserve-search="true" placeholder="Select Reports To"
                    class="font-11 mb-3">


                    <template #selection="{ values, isOpen }">
                      <span class="multiselect__single font-10" v-if="values.length" v-show="!isOpen">
                        {{ values.join(", ") }}
                      </span>
                    </template>
                  </VueMultiselect>
                  <label class="font-13 ps-1" for="reporting_designation">Reporting Designation</label>

                  <VueMultiselect v-model="createEmployee.reporting_designation" :options="designations"
                    :multiple="false" :close-on-select="true" :clear-on-select="false" :preserve-search="true"
                    placeholder="Select Reporting Designation" class="font-11 mb-3"
                    :disabled="!!createEmployee.reporting_to">


                    <template #selection="{ values, isOpen }">
                      <span class="multiselect__single font-10" v-if="values.length" v-show="!isOpen">
                        {{ values.join(", ") }} selected
                      </span>
                    </template>
                  </VueMultiselect>
                  <div class="mb-3">
                    <label class="font-13 ps-1" for="reporting_to">Acknowledge On</label><br>
                    <input class="mb-3 date-time form-control font-12 " tag="input" type="datetime-local"
                      name="acknowledge_on" id="acknowledge_on" placeholder="Enter department code"
                      :value="trimMilliseconds(createEmployee.acknowledge_on)" readonly />
                  </div>
                  <div class="mb-3 font-11">
                    <label for="signatureInput" class="form-label mb-0 font-13 ps-1">
                      Add Signature
                    </label>
                    <input type="file" ref="signatureInputRef" class="form-control font-12 mb-2" id="signatureInput"
                      @change="selectedSignature" aria-describedby="fileHelpId" />

                    <div v-if="createEmployee.signature" class="d-flex justify-center position-relative mt-2">
                      <i class="bi bi-x-lg position-absolute text-danger cursor-pointer" style="
                            top: -7px;
                            right: -5px;
                            font-size: 13px;
                            background: white;
                            border-radius: 50%;
                            padding: 3px;
                          " @click="removeSignature">
                      </i>
                      <img :src="createEmployee.signature" alt="Signature" class="img-fluid signature-img" />
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <ButtonComp type="button" class="cancelfilter border-1 text-nowrap font-10" name="Cancel"
              @click="cancelCreate" data-bs-dismiss="modal" />

            <ButtonComp type="button" class="btn btn-dark font-11" name="Save Employee" @click="SaveEditEmp" />
          </div>
        </div>
      </div>
    </div>
    <div class="modal fade" id="EmployeeToggleModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Employee Status</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="text-center fw-bolder">
              Are you sure you want to <span id="empActionText"></span> "<span id="empRowName"></span>"?<br>
            </div>

            <div class="mt-4">
              <label class="font-13 mb-1" for="emp_name">Remarks<span class="text-danger ps-1">*</span></label>
              <textarea v-model.trim="remarks" class="w-100 font-13 remarks"></textarea>
            </div>


            <!-- <label for="name" class="font-13 mt-3">Attachments</label>
            <input type="file" @change="handleSingleAttach" class="form-control mb-3" :disabled="uploadedFields.length >= 4" />
            <div v-if="uploadedFields.length >= 4" class="text-success mt-2">
              All attachments uploaded.
            </div>

            <div class="row mt-3">
              <div
                v-for="(field, index) in uploadedFields"
                :key="index"
                class="col-3 mb-3 text-center"
              >
                <img
                  :src="selectedEmpRow[field]"
                  alt="Uploaded"
                  class="img-thumbnail"
                  style="height: 100px; object-fit: cover;"
                />
                <button
                  @click="removeImage(field)"
                  class="btn btn-sm btn-danger mt-2"
                >
                  Remove
                </button>
              </div>

            </div> -->

          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-dark" :disabled="!remarks" @click="confirmEmployeeToggle">Yes,
              Proceed</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="ExportEmployeeModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Export Employee</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            Are you sure you want to export the employee details?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-dark" @click="exportEmployeesToExcel">Yes, Proceed</button>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="ForgotPasswordModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Confirm Reset Password</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div class="text-center">
              Are you sure you want to reset "{{ forgotData.emp_name }}" password?<br>
            </div>

          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
            <button type="button" class="btn btn-dark" :disabled="saveloading" @click="forgotpassword()">
              <span v-if="saveloading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              <span v-if="!saveloading">
                <span class="font-12 fw-bold">Yes, Proceed</span>
              </span>
            </button>
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
const showEmployeebulk = ref(true);
const tableData = ref([]);
const newbusiness = ref("");
const totalRecords = ref(0);
const designations = ref([]);
const reportingTo = ref([]);
const reportingDesigination = ref([]);
const departmentsList = ref([]);
const remarks = ref("");
const saveloading = ref(false)
// const newDesignation = ref(false);
// const signaturePath = ref("");
const phoneError = ref("");
const signatureInputRef = ref(null);
const loading = ref(false);
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

onMounted(() => {
  const url = window.location.href;
  if (url.includes('ncomr')) {
    createEmployee.value.emp_code = 'NICO-';
  }
})

const selectedEmpRow = ref(null);
const empActionText = ref('');
const searchText = ref('')
const showModal = ref(false)
const filteredDesignations = ref([])

const bulkdata = ref([])

const tableheaders = ref([
  { th: "Employee ID", td_key: "emp_code" },
  { th: "Employee Name", td_key: "emp_name" },
  // { th: "Mail", td_key: "emp_mail_id" },
  { th: "Designation", td_key: "designation" },
  { th: "Department", td_key: "department" },
  { th: "Reporting Designation", td_key: "reporting_designation" },
  { th: "Signature", td_key: "signature" },
  { th: 'Hod', td_key: 'is_hod' },
  { th: 'Admin', td_key: 'is_admin' },
  { th: "Status", td_key: "enable" },
  // { th: "last Login", td_key: "last_login" },
  // { th: "Creation Date", td_key: "creation" },
  // { th: "last Login IP", td_key: "last_ip" }, 

  // { th: "Reporting Designation", td_key: "reporting_designation" },
]);


// const bulktableHeaders = ref([
//   {
//     th: "Employee Mail", td_key: "message"
//   },
//   {
//     th: "Status", td_key: "status"
//   },

// ])


// Extract and format data

function trimMilliseconds(datetime) {
  if (!datetime) return '';
  return datetime.split('.')[0];
}

const fileInput = ref(null);
const progress = ref(0);
const uploading = ref(false);
const bulkfileUrl = ref("");


const roleError = ref('');

function validateRole() {
  if (newRole.value.trim() === '') {
    roleError.value = 'Designation is required';
  } else if (!/^[a-zA-Z0-9 ]*$/.test(newRole.value)) {
    roleError.value = 'Special characters are not allowed';
  } else {
    roleError.value = '';
  }
}

function closedesignmodal(){
  showModal.value = false
  newRole.value = ''
  roleError.value = ''
}

const triggerFileInput = () => {
  fileInput.value.click();
};

const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    uploadbulkFile(file);
    if (fileInput.value) {
      fileInput.value.value = "";
    }
  }
};

function validateEmpName() {
  createEmployee.value.emp_name = createEmployee.value.emp_name.trim().toUpperCase();
}

const generateRandomNumber = () => {
  return Math.floor(Math.random() * 1000000);
};


const uploadbulkFile = (file) => {
  const randomNumber = generateRandomNumber();
  let fileName = `${randomNumber}-@${file.name}`;

  const formData = new FormData();
  formData.append("file", file, fileName);
  formData.append("is_private", "0");
  formData.append("folder", "Home");

  uploading.value = true;
  progress.value = 0;


  axiosInstance
    .post(apis.uploadfile, formData, {
      headers: { "Content-Type": "multipart/form-data" },
      onUploadProgress: (progressEvent) => {
        progress.value = Math.round(
          (progressEvent.loaded / progressEvent.total) * 100
        );
      },
    })
    .then((res) => {
      if (res.message && res.message.file_url) {
        bulkfileUrl.value = res.message.file_url;

        // toast.success("File uploaded successfully! Processing import...");

        if (res.message.file_url && bulkfileUrl.value) {
          buluploding();
        }
      } else {
        toast.error("File upload failed: file_url not found in response.");
      }
    })
    .catch((error) => {
      console.error("Upload error:", error);
      toast.error("File upload failed. Please try again.");
    })
    .finally(() => {
      setTimeout(() => {
        uploading.value = false;
        progress.value = 0;
      }, 2000);
    });
};
const buluploding = () => {
  const data = {
    file: bulkfileUrl.value,
    doctype: doctypes.EzyEmployeeList,
  };

  axiosInstance
    .post(apis.uploadbulkEmployeefile, data)
    .then((res) => {
      if (!res?.data) {
        toast.error("Import response not found.");
        return;
      }

      bulkdata.value = res.data;

      // Handle API failure immediately
      if (res.data.success === false) {
        let errorMessage = res._error_message || res.data.message || "Import failed.";

        // Remove anything inside parentheses (including the parentheses)
        errorMessage = errorMessage.replace(/\s*\(.*?\)\s*/g, "").trim();

        toast.error(errorMessage);

        // Parse and display _server_messages if available
        if (res.data._server_messages) {
          try {
            const serverMessages = JSON.parse(res.data._server_messages);
            if (Array.isArray(serverMessages)) {
              serverMessages.forEach((msg) => {
                const parsedMessage = JSON.parse(msg);
                let parsedErrorMessage = parsedMessage.message || "Permission error.";

                // Remove anything inside parentheses
                parsedErrorMessage = parsedErrorMessage.replace(/\s*\(.*?\)\s*/g, "").trim();

                toast.error(parsedErrorMessage);
              });
            }
          } catch (err) {
            console.error("Error parsing _server_messages:", err);
          }
        }
        return; // Stop further execution
      }

      // Show warnings if present
      if (bulkdata.value.template_warnings?.length) {
        bulkdata.value.template_warnings.forEach((warning) => {
          toast.warning(`Warning: ${warning}`);
        });
      }

      // Ensure records exist
      if (bulkdata.value.records) {
        bulkdata.value.records = bulkdata.value.records.map(record => ({
          ...record,
          message: record.message, // Keep as a string
        }));
      }
      // Handle different statuses
      if (bulkdata.value.template_status === "success") {
        toast.success("Bulk data imported successfully!");
      } else if (bulkdata.value.template_status === "failed") {
        toast.error(`Import Failed: ${bulkdata.value.message}`);
      } else if (bulkdata.value.status === "Partial Success") {
        toast.warning("Partial Success: Some records failed.");
      }
    })
    .catch((error) => {
      console.error("Upload error:", error);
      toast.error("Upload failed. Please try again.");
    });
};



const formattedData = computed(() => {
  const data = bulkdata.value?.records || [];

  return data.map((record, index) => {
    let email = "N/A";
    let messageText = "N/A";

    try {
      if (record.status.toLowerCase() === "success") {
        email = extractEmail(record.message);
        messageText = "Successfully imported";
      } else if (record.status.toLowerCase() === "failed") {
        // Parse JSON from the message field
        const parsedMessages = JSON.parse(record.message);

        if (Array.isArray(parsedMessages) && parsedMessages.length > 0) {
          messageText = parsedMessages[0].title || "Unknown Issue";

          // Check for invalid email error
          const invalidEmail = extractInvalidEmail(parsedMessages);
          if (invalidEmail) {
            email = invalidEmail;
            messageText = "Invalid Email Address";
          } else {
            email = extractEmail(parsedMessages);
          }
        }
      }
    } catch (error) {
      messageText = "Parsing Error"; // Fallback if JSON parsing fails
    }

    return {
      sNo: index + 1, // Serial number
      email,
      status: record.status,
      displayMessage: messageText, // Extract only the title
    };
  });
});

// **Fixed Email Extraction Function**
const extractEmail = (message) => {
  if (typeof message === "string") {
    message = message.toLowerCase(); // Ensure case insensitivity
    if (message.includes("successfully imported ")) {
      return message.split("successfully imported ")[1] || "N/A";
    }
  }
  if (Array.isArray(message)) {
    return message[0]?.message?.match(/<strong>(.*?)<\/strong>/)?.[1] || "N/A";
  }
  return "N/A";
};

// **Extract Invalid Email**
const extractInvalidEmail = (messages) => {
  if (Array.isArray(messages)) {
    for (const msg of messages) {
      if (msg.message.includes("is not a valid Email Address")) {
        return msg.message.split(" is not a valid Email Address")[0];
      }
    }
  }
  return null;
};

// **Template Warnings Computed Property**
const templateWarnings = computed(() => {
  return bulkdata.value?.template_warnings || [];
});
// Function to Download Excel
const downloadExcel = () => {
  const XLSX = window.XLSX; // Access XLSX from the global window object

  if (!XLSX) {
    console.error("XLSX library is not loaded.");
    return;
  }

  const worksheet = XLSX.utils.json_to_sheet(formattedData.value);
  const workbook = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(workbook, worksheet, "Records");

  // Convert to Blob and trigger download
  const excelBuffer = XLSX.write(workbook, { bookType: "xlsx", type: "array" });
  const blob = new Blob([excelBuffer], { type: "application/octet-stream" });

  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.download = "Records.xlsx";
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};


// const downloadTemplate = () => {
//   axiosInstance
//     .get("/download-template", { responseType: "blob" })
//     .then((response) => {
//       const url = window.URL.createObjectURL(new Blob([response.data]));
//       const link = document.createElement("a");
//       link.href = url;
//       link.setAttribute("download", "template.xlsx");
//       document.body.appendChild(link);
//       link.click();
//     })
//     .catch((error) => {
//       console.error("Download error:", error);
//     });
// };
// const downloadTemplate = () => {
//   const link = document.createElement("a");
//   link.href = "/Employee_import.xlsx"; // Reference from the public folder
//   link.setAttribute("download", "Employee_import.xlsx"); // Force download
//   document.body.appendChild(link);
//   link.click();
//   document.body.removeChild(link);
// };

// const downloadTemplate = () => {
//   const fileUrl = `${import.meta.env.BASE_URL}Employee_import.xlsx`; // Vue 3 Base URL
//   const link = document.createElement("a");
//   link.href = fileUrl;
//   link.setAttribute("download", "Employee_import.xlsx");
//   document.body.appendChild(link);
//   link.click();
//   document.body.removeChild(link);
// };

const downloadTemplate = async () => {
  const company = businessUnit.value;

  // Load the template
  const response = await fetch(`${import.meta.env.BASE_URL}Employee_import.xlsx`);
  const arrayBuffer = await response.arrayBuffer();
  const workbook = XLSX.read(arrayBuffer, { type: "array" });

  // Access first sheet
  const sheetName = workbook.SheetNames[0];
  const worksheet = workbook.Sheets[sheetName];

  // Insert company name in A2 (assuming A1 has "Company")
  worksheet["A2"] = { t: "s", v: company };

  // Update sheet range if needed
  const range = XLSX.utils.decode_range(worksheet["!ref"]);
  if (range.e.r < 1) range.e.r = 1; // ensure at least 2 rows
  worksheet["!ref"] = XLSX.utils.encode_range(range);

  // Export modified workbook
  const updatedWorkbook = XLSX.write(workbook, {
    bookType: "xlsx",
    type: "array"
  });

  const blob = new Blob([updatedWorkbook], {
    type: "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
  });

  // Trigger download
  const link = document.createElement("a");
  link.href = URL.createObjectURL(blob);
  link.setAttribute("download", "Employee_import.xlsx");
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
};

const emailError = ref("");
const editEmailError = ref("");
const createEmailError = ref("");

// const validateEmail = () => {
//   const email = createEmployee.value.emp_mail_id;
//   const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

//   if (!emailPattern.test(email)) {
//     emailError.value = "Invalid email address.";
//   } else {
//     emailError.value = "";
//   }
// };
// const validateEmail = () => {
//   const email = originalEmail.value || createEmployee.value.emp_mail_id;
//   const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

//   if (!emailPattern.test(email)) {
//     emailError.value = "Invalid email address";
//   } else {
//     emailError.value = "";
//   }
// };

// Edit Employee Email Validation
function validateEditUserEmail() {
  const email = (originalEmail.value || "").trim().toLowerCase();

  if (!email) {
    editEmailError.value = "Email is required";
    return;
  }

  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!emailPattern.test(email)) {
    editEmailError.value = "Invalid email address";
    return;
  }

  const exists = employeeEmails.value.some(
    (emp) => emp.emp_mail_id?.toLowerCase() === email
  );

  editEmailError.value = exists ? "Email already exists" : "";
}

// Create Employee Email Validation
function validateCreateUserEmail() {
  const email = (createEmployee.value.emp_mail_id || "").trim().toLowerCase();

  if (!email) {
    createEmailError.value = "Email is required";
    return;
  }

  const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;
  if (!emailPattern.test(email)) {
    createEmailError.value = "Invalid email address";
    return;
  }

  const exists = employeeEmails.value.some(
    (emp) => emp.emp_mail_id?.toLowerCase() === email
  );
  

  createEmailError.value = exists ? "Email already exists" : "";
}


function bulkEmp() {
  showEmployeebulk.value = false
}

function backtoEmployeeList() {
  showEmployeebulk.value = true
}
// const validatephone = () => {
//   if (createEmployee.value.emp_phone) {
//     const phone = createEmployee.value.emp_phone;
//     const phonePattern = /^\d{10}$/;
//     phoneError.value = phonePattern.test(phone) ? "" : "Invalid phone number.";
//   }
// };

function onDepartmentChange(selectedDepartment) {
  fetchingIsHod(selectedDepartment.name); // Call your API function here
}

function fetchingIsHod(department) {
  const filters = [["company_field", "=", `${newbusiness.value}`], ["enable", "=", "1"],
  ["department", "like", `%${department}%`], ["is_hod", "=", 1]];

  const queryParams = {
    fields: JSON.stringify(["*"]),
    filters: JSON.stringify(filters),
    limit_page_length: "none",
    order_by: "`tabEzy Employee`.`enable` DESC,`tabEzy Employee`.`creation` DESC",
  };
  axiosInstance
    .get(apis.resource + doctypes.EzyEmployeeList, { params: queryParams })
    .then((res) => {
      createEmployee.value.reporting_to = res.data[0].name;
      createEmployee.reporting_designation = res.data[0].designation;

    })
    .catch((error) => {
      createEmployee.value.reporting_to = "";
      createEmployee.reporting_designation = "";
      console.error("Error fetching department data:", error);
    });

}


const isMasked = ref(true);
// const originalPhone = ref("");


const eyeIcon = computed(() => (isMasked.value ? "bi bi-eye-slash-fill" : "bi bi-eye-fill"));

// Ensure +91 is always prefixed
// const existformatPhoneNumber = (phone) => {
//   phone = phone.replace(/\D/g, ""); // Remove non-numeric characters
//   if (phone.startsWith("91") && phone.length === 12) {
//     phone = "+" + phone;
//   } else if (phone.length === 10) {
//     phone = "+91" + phone;
//   }
//   return phone;
// };

// // Watch input field for changes
// watch(
//   () => createEmployee.value.emp_phone,
//   (newVal) => {
//     if (!newVal.startsWith("+91")) {
//       createEmployee.value.emp_phone = existformatPhoneNumber(newVal);
//     }

//     // Update originalPhone only when unmasked
//     if (!isMasked.value) {
//       originalPhone.value = createEmployee.value.emp_phone;
//     }
//   },
//   { immediate: true } // Run immediately to set +91 on initial load
// );

// Mask phone number
// const maskPhoneNumber = () => {
//   let phone = createEmployee.value.emp_phone || "";

//   if (!phone.startsWith("+91")) {
//     phone = existformatPhoneNumber(phone);
//   }

//   if (!/^\+91\d{10}$/.test(phone)) {
//     phoneError.value = "Phone number must start with +91 and have 10 digits.";
//     return;
//   } else {
//     phoneError.value = "";
//   }

//   // Store the unmasked phone
//   originalPhone.value = phone;

//   // Mask only if isMasked is true
//   if (isMasked.value) {
//     createEmployee.value.emp_phone = "+91 ******" + phone.slice(-4);
//   } else {
//     createEmployee.value.emp_phone = phone;
//   }
// };
// watch(
//   () => createEmployee.value.emp_phone,
//   (newVal, oldVal) => {
//     // You could add validation here, but avoid masking during typing
//     if (!newVal.startsWith("+91") && newVal.length === 10) {
//       createEmployee.value.emp_phone = "+91" + newVal;
//     }
//   },
//   { immediate: true }
// );
// Toggle between masked and unmasked
// const toggleMask = () => {
//   if (!originalPhone.value) return;

//   if (isMasked.value) {
//     const confirmView = window.confirm("Are you sure you want to see the phone number?");
//     if (!confirmView) return;
//   }

//   isMasked.value = !isMasked.value;
//   createEmployee.value.emp_phone = isMasked.value
//     ? "+91 ******" + originalPhone.value.slice(-4)
//     : originalPhone.value;
// };

// Validate phone number
// const validatePhone = () => {
//   let phone = originalPhone.value.replace("+91", ""); // Remove +91 for validation
//   if (!/^\d{10}$/.test(phone)) {
//     phoneError.value = "Phone number must be 10 digits.";
//   } else {
//     phoneError.value = "";
//   }
// };
// const phoneError = ref('');
// const isMasked = ref(true);


// function maskNumber(phone) {
//   if (!phone || phone.length < 13) return phone;
//   return '+91 ******' + phone.slice(-4);
// }

// // ✅ Handle input: DO NOT format while typing
// function handleInput(e) {
//   createEmployee.value.emp_phone = e.target.value;
// }

// // ✅ Format on blur (or when saving)
// function formatPhoneNumber() {
//   let value = createEmployee.value.emp_phone.replace(/\D/g, ''); // Keep only digits
//   if (value.startsWith('91') && value.length > 10) {
//     value = value.slice(2);
//   }
//   if (value.length === 10) {
//     createEmployee.value.emp_phone = '+91' + value;
//     phoneError.value = '';
//   } else {
//     phoneError.value = 'Phone number must be 10 digits.';
//   }
// }

// // Toggle mask
// function toggleMask() {
//   isMasked.value = !isMasked.value;
//   eyeIcon.value = isMasked.value ? 'bi-eye' : 'bi-eye-slash';
// }

// const validatephone = () => {
//   if (createEmployee.value.emp_phone) {
//     const phone = createEmployee.value.emp_phone;
//     const phonePattern = /^\d{10}$/;
//     phoneError.value = phonePattern.test(phone) ? "" : "Invalid phone number.";
//   }
// };
// ✅ Display as ******1234 when masked
function maskNumber(phone) {
  if (!phone || phone.length < 13) return phone;
  return '+91 ******' + phone.slice(-4);
}

// ✅ Allow input when unmasked
function handleInput(e) {
  createEmployee.value.emp_phone = e.target.value;
}

// ✅ Format to +91xxxxxxxxxx on blur
// function formatPhoneNumber() {
//   let value = createEmployee.value.emp_phone.replace(/\D/g, '');

//   if (value.startsWith('91') && value.length > 10) {
//     value = value.slice(2);
//   }

//   if (value.length === 10) {
//     createEmployee.value.emp_phone = '+91' + value;
//     phoneError.value = '';
//   } else {
//     phoneError.value = 'Phone number must be 10 digits.';
//   }
// }
function formatPhoneNumber() {
  let value = createEmployee.value.emp_phone.replace(/\D/g, '');

  // Remove country code if included
  if (value.startsWith('91') && value.length > 10) {
    value = value.slice(2);
  }

  if (value.length === 10) {
    createEmployee.value.emp_phone = '+91' + value;
    phoneError.value = '';
  } else {
    // Keep the raw digits
    createEmployee.value.emp_phone = value;

    // Show error only if user has entered something (not empty)
    if (value.length > 0) {
      phoneError.value = 'Phone number must be 10 digits.';
    } else {
      phoneError.value = '';
    }
  }
}

// ✅ Toggle mask & readonly
function toggleMask() {
    if (isMasked.value) {
    const confirmView = window.confirm("Are you sure you want to see the phone number?");
    if (!confirmView) return;
  }
  isMasked.value = !isMasked.value;
  eyeIcon.value = isMasked.value ? 'bi-eye' : 'bi-eye-slash';
}

const isEmailMasked = ref(true);
const originalEmail = ref("");

const eyeIconEmail = computed(() => (isEmailMasked.value ? "bi bi-eye-slash-fill" : "bi bi-eye-fill"));


const maskEmail = () => {
  if (!isEmailMasked.value || !createEmployee.value.emp_mail_id.includes("@")) return;

  originalEmail.value = createEmployee.value.emp_mail_id;
  const [localPart, domain] = originalEmail.value.split("@");

  if (localPart.length > 3) {
    createEmployee.value.emp_mail_id = localPart.slice(0, 3) + "***@" + domain;
  }
};


const toggleEmailMask = () => {
  if (!originalEmail.value) return;

  if (isEmailMasked.value) {
    const confirmView = window.confirm("Are you sure you want to see the email address?");
    if (!confirmView) return; // If user cancels, do nothing
  }

  isEmailMasked.value = !isEmailMasked.value;
  createEmployee.value.emp_mail_id = isEmailMasked.value
    ? maskEmailFormat(originalEmail.value)
    : originalEmail.value;
};

// const toggleEmailMask = () => {
//   if (!originalEmail.value) return;

//   isEmailMasked.value = !isEmailMasked.value;
//   createEmployee.value.emp_mail_id = isEmailMasked.value
//     ? maskEmailFormat(originalEmail.value)
//     : originalEmail.value;
// };

const maskEmailFormat = (email) => {
  const [localPart, domain] = email.split("@");
  return localPart.length > 3 ? localPart.slice(0, 3) + "***@" + domain : email;
};
// // Ensure +91 is always prefixed
// const formatPhoneNumber = (event) => {
//   let value = event.target.value;

//   // Remove non-numeric characters except '+'
//   value = value.replace(/[^0-9+]/g, "");

//   // Ensure +91 is always at the start
//   if (!value.startsWith("+91")) {
//     value = "+91" + value.replace(/^91/, ""); // Remove leading '91' if entered without '+'
//   }

//   // Limit total length to 13 characters
//   if (value.length > 13) {
//     value = value.slice(0, 13);
//   }

//   createEmployee.value.emp_phone = value;
// };

// Validate phone number
const validatephonenew = () => {
  if (createEmployee.value.emp_phone) {
    const phone = createEmployee.value.emp_phone.replace("+91", ""); // Remove +91 for validation
    const phonePattern = /^\d{10}$/;
    phoneError.value = phonePattern.test(phone) ? "" : "Invalid phone number.";
  }
};


const filterObj = ref({
  limitPageLength: 20,
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

          // Update local designations list
          // designations.value.push(newTag);
          // createEmployee.value.designation = newTag;
          axiosInstance
            .post(apis.resource + doctypes.designations, {
              role: response.data.role_name,
            }) // Adjust payload as needed
            .then((response) => {
              if (response.data) {

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
const newRole = ref('')
watch(showModal, (visible) => {
  if (visible) newRole.value = searchText.value
})
const errorMessage = ref('')

const validateInput = () => {
  const pattern = /[^a-zA-Z0-9 ]/
  if (pattern.test(searchText.value)) {
    errorMessage.value = 'Special characters are not allowed in the role name.'
  } else {
    errorMessage.value = ''
  }
}
const filterDesignations = () => {
  const search = searchText.value.toLowerCase().trim()
  filteredDesignations.value = designations.value.filter((role) =>
    role.toLowerCase().includes(search)
  )
}

const selectDesignation = (role) => {
  createEmployee.value.designation = role
  searchText.value = role
  filteredDesignations.value = []
}

const showCreateButton = computed(() => {
  const text = searchText.value.trim()
  return text && !designations.value.includes(text) && text.length > 1
})

const createRole = () => {
  const roleName = searchText.value.trim()
  if (!roleName) return

  axiosInstance
    .post(apis.resource + doctypes.roles, { role_name: roleName })
    .then((response) => {
      if (response.data?.role_name) {
        axiosInstance
          .post(apis.resource + doctypes.designations, {
            role: response.data.role_name,
          })
          .then((res) => {
            if (res.data?.role) {
              designations.value.push(res.data.role)
              createEmployee.value.designation = res.data.role
              searchText.value = res.data.role
              filteredDesignations.value = []
              showModal.value = false
            }
          })
      }
    })
    .catch((err) => {
      console.error('Error creating role:', err)
    })
}
const removeSignature = () => {
  createEmployee.value.signature = null; // Reset the signature

  const fileInput = document.getElementById("signatureInput");
  if (fileInput) {
    fileInput.value = "";
  }
};

// watch(
//   () => createEmployee.value.reporting_to,
//   (newValue) => {
//     if (newValue) {
//       const selectedEmployee = tableData.value.find(
//         (emp) => emp.emp_mail_id === newValue
//       );
//       if (selectedEmployee) {
//         createEmployee.value.reporting_designation = selectedEmployee.designation;
//       }
//     }
//   },
//   { immediate: true } // <-- this will trigger the watcher on setup
// );
// function addnewDesignation() {
//     newDesignation.value = !newDesignation.value
// }
const actions = ref([{ name: "Edit Employee", icon: "fa-solid fa-eye" }, { name: "Reset Password", icon: "fa fa-lock" }]);
const isFormFilled = computed(() => {
  return [
    createEmployee.value.emp_code,
    createEmployee.value.emp_name,
    createEmployee.value.emp_mail_id,
    createEmployee.value.department,
    createEmployee.value.designation,
  ].every((field) => field && field.toString().trim() !== "");
});
// createEmployee.value.reporting_to,
// createEmployee.value.reporting_designation,

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
  employeeOptions();
}

const forgotData = ref("")

function actionCreated(rowData, actionEvent) {
  if (actionEvent?.name === 'Edit Employee') {
    searchText.value = '';
    filteredDesignations.value = [];
    if (rowData) {
      designationData();
      employeeOptions();
      phoneError.value = "";
      emailError.value = "";

      // Assign base employee data (excluding department for now)
      createEmployee.value = {
        ...rowData,
        department: "", // set after deptData loads
      };


      // Set searchText to current designation
      searchText.value = rowData.designation || ''
      
      deptData(() => {
        const matchedDept = departmentsList.value.find(
          (dept) => dept.name === rowData.department
        );
        createEmployee.value.department = matchedDept || "";
      });
      

     
      isMasked.value = true;
      isEmailMasked.value = true;
      maskEmail();

      const modal = new bootstrap.Modal(document.getElementById('exampleModal'), {});
      modal.show();
    } else {
      console.warn("No form fields provided.");
      formCreation(rowData);
    }
  }
  if (actionEvent?.name === 'Reset Password') {
    forgotData.value = rowData;
    const modal = new bootstrap.Modal(document.getElementById('ForgotPasswordModal'), {});
    modal.show();
  }
}

function forgotpassword() {
  saveloading.value = true;
  const payload = {
    cmd: "frappe.core.doctype.user.user.reset_password",
    user: forgotData.value.name,
  }
  axiosInstance.post(apis.forgotPassword, payload)
    .then((res) => {
      if (res) {
        const messages = JSON.parse(res._server_messages);
        const messageObj = JSON.parse(messages[0]);
        if (messageObj.message) {
          toast.success("Password reset instructions have been sent to the user email.");
          const modal = bootstrap.Modal.getInstance(document.getElementById('ForgotPasswordModal'));
          modal.hide();
        }
      }
    })
    .catch((error) => {
      console.error("Upload error:", error);
    })
    .finally(() => {
      saveloading.value = false;

    })
};


watch(
  () => createEmployee.value.reporting_to,
  (newValue) => {
    if (newValue) {
      const selectedEmployee = employeeEmails.value.find(
        (emp) => emp.emp_mail_id === newValue
      );
      if (selectedEmployee) {
        createEmployee.value.reporting_designation = selectedEmployee.designation;
      }
    } else {
      // ✅ Clear reporting_designation if reporting_to is cleared
      createEmployee.value.reporting_designation = "";
    }
  },
  { immediate: true }
);

// watch(
//   () => createEmployee.reporting_to,
//   (newVal) => {
//     if (newVal) {
//       const matchedEmployee = employeeEmails.find(emp => emp.emp_mail_id === newVal);
//       createEmployee.reporting_designation = matchedEmployee?.designation || '';
//     } else {
//       createEmployee.reporting_designation = '';
//     }
//   }
// );




function toggleFunction(rowData) {
  selectedEmpRow.value = rowData;
  const isEnabled = rowData.enable === '1' || rowData.enable === 1;
  empActionText.value = isEnabled ? 'Disable' : 'Enable';

  document.getElementById('empActionText').innerText = empActionText.value;
  document.getElementById('empRowName').innerText = rowData.emp_name;

  const modal = new bootstrap.Modal(document.getElementById('EmployeeToggleModal'));
  modal.show();
}

function confirmEmployeeToggle() {
  const isEnabled = selectedEmpRow.value.enable === '1' || selectedEmpRow.value.enable === 1;
  selectedEmpRow.value.enable = isEnabled ? 0 : 1;
  selectedEmpRow.value.remarks = remarks.value

  if (selectedEmpRow.value.enable == 0) {
    // Get current date and time in "YYYY-MM-DD HH:mm:ss" format
    const now = new Date();
    const pad = (n) => n.toString().padStart(2, '0');
    const currentDateTime = `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;

    // Add current_date to the payload
    selectedEmpRow.value.enable_on = currentDateTime;

  }

  axiosInstance
    .put(`${apis.resource}${doctypes.EzyEmployeeList}/${selectedEmpRow.value.name}`, selectedEmpRow.value)
    .then(() => {
      const userData = { enabled: selectedEmpRow.value.enable };
      return axiosInstance.put(`${apis.resource}${doctypes.users}/${selectedEmpRow.value.name}`, userData);
    })
    .then(() => {
      toast.success(`Employee ${empActionText.value}d successfully`);
      window.location.reload();
    })
    .catch((err) => {
      console.error('Toggle employee error:', err);
    });
}


const fieldMapping = ref({
  emp_code: { type: "input" },
  emp_name: { type: "input" },
  designation: { type: "input" },
  department: { type: "input" },
  reporting_designation: { type: "input" },
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
    searchText: "",
    designation: "",
    reporting_to: "",
    reporting_designation: "",
    signature: null,
    company_field: businessUnit.value,
  };
  searchText.value=""
  filterDesignations.value = [];
  createEmailError.value = '';
  const fileInput = document.getElementById("signatureInput");
  if (fileInput) {
    fileInput.value = "";
  }
  const url = window.location.href;
  if (url.includes('ncomr')) {
    createEmployee.value.emp_code = 'NICO-';
  }
}

function selectedSignature(event) {
  const file = event.target.files[0];
  if (file) {
    uploadFile(file, "signature");
  }
}

// Export function
const exportEmployeesToExcel = async () => {
  const filters = [["company_field", "=", `${newbusiness.value}`], ["is_web_form", "=", "0"], ["enable", "=", "1"]];
  const queryParams = {
    fields: JSON.stringify(["*"]),
    limit_start: 0,
    limit_page_length: "none",
    filters: JSON.stringify(filters),
  }
  try {
    const response = await axiosInstance.get(
      apis.resource + doctypes.EzyEmployeeList,
      { params: queryParams }
    )

    if (response.data) {
      const employees = response.data
      if (employees.length) {
        const modal = bootstrap.Modal.getInstance(
          document.getElementById("ExportEmployeeModal")
        );
        modal.hide();
        toast.success("Successfully Completed")

        const worksheet = XLSX.utils.json_to_sheet(employees)
        const workbook = XLSX.utils.book_new()
        XLSX.utils.book_append_sheet(workbook, worksheet, 'Employees')
        XLSX.writeFile(workbook, 'EmployeeDetails.xlsx')
      }
      else {
        toast.error("No Employee Details")
      }
    }
  } catch (error) {
    console.error('Error exporting employee data:', error)
  }
}

// const generateRandomNumber = () => {
//     return Math.floor(Math.random() * 1000000);
// };

const uploadedFields = ref([]);  // to track filled fields

const handleSingleAttach = (event) => {
  const file = event.target.files[0];
  if (file) {
    const nextField = getNextField();
    if (nextField) {
      uploadFile(file, nextField);
    } else {
      console.warn('All fields are filled.');
    }
  }
  event.target.value = '';  // Clear file input after each selection
};

const getNextField = () => {
  const fields = ['attachment_one', 'attachment_two', 'attachment_three', 'attachment_four'];
  return fields.find((field) => !selectedEmpRow.value[field]);
};

const removeImage = (field) => {
  selectedEmpRow.value[field] = '';
  uploadedFields.value = uploadedFields.value.filter(f => f !== field);
};

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
        selectedEmpRow.value[field] = res.message.file_url;
        uploadedFields.value.push(field);
      } else {
        console.error("file_url not found in the response.");
      }
    })
    .catch((error) => {
      console.error("Upload error:", error);
    });
};

function deptData(callback) {
  const queryParams = {
    fields: JSON.stringify(["*"]),
    limit_page_length: "None",
    limit_start: filterObj.value.limit_start,
  };

  axiosInstance
    .get(apis.resource + doctypes.departments, { params: queryParams })
    .then((res) => {
      if (res.data) {
        departmentsList.value = res.data;
        if (callback) callback(); // Execute after fetch
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
  employeeData();
};
// Handle updating the limit start
const PaginationLimitStart = ([itemsPerPage, start]) => {
  filterObj.value.limitPageLength = itemsPerPage;
  filterObj.value.limit_start = start;
  employeeData();
};
const timeout = ref(null);

function inLineFiltersData(searchedData) {
  //   // Initialize filters array
  // const filters = [];

  // //   // Loop through the tableheaders and build dynamic filters based on the `searchedData`
  // tableheaders.value.forEach((header) => {
  //   const key = header.td_key;

  //   //     // If there is a match for the key in searchedData, create a 'like' filter
  //   if (searchedData[key]) {
  //     filters.push([key, "like", `%${searchedData[key]}%`]);
  //   }
  //   //     // Add filter for selected option
  //   //     if (key === "selectedOption" && searchedData.selectedOption) {
  //   //       filters.push([key, "=", searchedData.selectedOption]);
  //   //     }
  //   //     // Special handling for 'invoice_date' to create a 'Between' filter (if it's a date)
  //   //     if (key === "invoice_date" && searchedData[key]) {
  //   //       filters.push([key, "Between", [searchedData[key], searchedData[key]]]);
  //   //     }

  //   //     // Special handling for 'invoice_type' or 'irn_generated' to create an '=' filter
  //   //     if ((key === "invoice_type" || key === "credit_irn_generated") && searchedData[key]) {
  //   //       filters.push([key, "=", searchedData[key]]);
  //   //     }
  // });

  // //   // Log filters to verify

  // //   // Once the filters are built, pass them to fetchData function
  // if (filters.length) {
  //   employeeData(filters);
  // } else {
  //   employeeData();
  // }
  //   fetchTotalRecords(filters);



  clearTimeout(timeout.value); // Clear previous timeout

  timeout.value = setTimeout(() => {
    // Initialize filters array
    filterObj.value.filters = [];

    // Loop through the table headers and build dynamic filters
    tableheaders.value.forEach((header) => {
      const key = header.td_key;

      if (searchedData[key]) {
        // Push as an array of 3 items
        filterObj.value.filters.push([key, "like", `%${searchedData[key]}%`]);
      }
    });

    // Call receivedForMe with or without filters
    if (filterObj.value.filters.length) {
      filterObj.value.limit_start = 0;

      employeeData(filterObj.value.filters);
    } else {
      employeeData();
    }
  }, 500);
}

function employeeData(data) {
  const filters = [["company_field", "=", `${newbusiness.value}`], ["enable", "=", "1"]];
  if (data) {
    filters.push(...data);
  }

  const queryParams = {
    fields: JSON.stringify(["*"]),
    filters: JSON.stringify(filters),
    limit_page_length: filterObj.value.limitPageLength,
    limit_start: filterObj.value.limit_start,
    order_by: "`tabEzy Employee`.`enable` DESC,`tabEzy Employee`.`modified` DESC",
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
        const newData = res.data
        if (filterObj.value.limit_start === 0) {

          tableData.value = newData;
          // designations.value = [...new Set(res.data.map((designation) => designation.designation))];
          // reportingTo.value = [
          //   ...new Set(res.data.map((reporting) => reporting.reporting_to)),
          // ];
          // reportingDesigination.value = [
          //   ...new Set(
          //     res.data.map(
          //       (reportingDesigination) =>
          //         reportingDesigination.reporting_designation
          //     )
          //   ),
          // ];
          // createEmployee.value.company_field = businessUnit.value;
        }
        else {
          tableData.value = tableData.value.concat(newData);
        }
      }
    })
    .catch((error) => {
      console.error("Error fetching department data:", error);
    });
}

const employeeEmails = ref([]);


function employeeOptions() {
  const queryParams = {
    fields: JSON.stringify(["*"]),
    limit_page_length: "None",
    filters: JSON.stringify([["company_field", "=", `${newbusiness.value}`]]),
    order_by: "`tabEzy Employee`.`modified` desc",
  };
  axiosInstance
    .get(apis.resource + doctypes.EzyEmployeeList, { params: queryParams })
    .then((res) => {
      if (res.data) {
        const newData = res.data
        if (filterObj.value.limit_start === 0) {

          employeeEmails.value = newData;
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
        else {
          employeeEmails.value = employeeEmails.value.concat(newData);
        }
      }
    })
    .catch((error) => {
      console.error("Error fetching department data:", error);
    });
}
// watch(
//   () => createEmployee.value.reporting_to,
//   (newValue) => {
//     const selected = employeeEmails.value.find(
//       (emp) => emp.emp_mail_id === newValue
//     );
//     createEmployee.value.reporting_designation = selected?.designation;
//   },
//   { immediate: true } // ✅ if editing existing record
// );
function designationData() {
  const filters = [];
  const queryParams = {
    fields: JSON.stringify(["*"]),
    filters: JSON.stringify(filters),
    limit_page_length: "None",
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

      employeeData();
    }
  },
  { immediate: true }
);
function createEmpl() {

  if (!isFormFilled.value || searchText.value.trim() === "") {
    toast.error("Please fill all required fields", {
      autoClose: 1000,
      transition: "zoom",
    });
    return;
  }
  if(!searchText.value){
    toast.error("Please select or enter a designation", {
      autoClose: 1000,
      transition: "zoom",
    });
    return;

  }
  if(errorMessage.value) {
    toast.error(errorMessage.value, {
      autoClose: 1000,
      transition: "zoom",
    });
    return;
  }
  if (emailError.value) {
    toast.error("Employee Email Id already exists", {
      autoClose: 1000,
      transition: "zoom",
    });
    return;
  }
  if(phoneError.value) {
    toast.error("Please enter a valid phone number.", {
      autoClose: 1000,
      transition: "zoom",                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         
    });
    return;
  }
  if(createEmployee.value.designation !== searchText.value.trim()) {
     toast.error("Please create the role before creating an employee.", {
      autoClose: 1000,
      transition: "zoom",
    });
    return;
  }


  createEmployee.value.company_field = businessUnit.value;

  const dataObj = {
    ...createEmployee.value,
    department: createEmployee.value.department?.name || "", // ✅ only send name
    doctype: doctypes.EzyEmployeeList,
  };
  // console.log(dataObj);
  loading.value = true;

  axiosInstance
    .post(apis.resource + doctypes.EzyEmployeeList, dataObj)
    .then((res) => {
      if (res.data) {
        toast.success("Employee Created", {
          autoClose: 500,
          transition: "zoom",
        });
        newRole.value = ''
        searchText.value = ''
        const modal = bootstrap.Modal.getInstance(
          document.getElementById("createDepartments")
        );
        modal.hide();

        cancelCreate();
        createEmployee.value = {}
        newRole.value = ''
        searchText.value = ''
        const fileInput = document.getElementById("signatureInput");
        if (fileInput) {
          fileInput.value = "";
        }
        employeeData();
        loading.value = false;
      }
    })
    .catch((error) => {
      console.error("Error creating employee:", error);
    })
    .finally(() => {
      loading.value = false;
    });
}

const asfv = ref(false)

function SaveEditEmp() {
  
  if (!isFormFilled.value || searchText.value.trim()=== "") {
    toast.error("Please fill all required fields", {
      autoClose: 1000,
      transition: "zoom",
    });
    return;
  }
  if(phoneError.value) {
    toast.error("Invalid phone number", {
      autoClose: 1000,
      transition: "zoom",
    });
    return;
  }
  if(!searchText.value){
      toast.error("Please select or enter a designation", {
      autoClose: 1000,
      transition: "zoom",
    });
    return;
  }
   if(createEmployee.value.designation !== searchText.value) {
     toast.error("Please create the role before updating employee.", {
      autoClose: 1000,
      transition: "zoom",
    });
    return;
  }

  if (!createEmployee.value.designation && searchText.value) {
    createEmployee.value.designation = searchText.value;
  }

  // Auto-set reporting_designation based on selected reporting_to
  if (createEmployee.value.reporting_to) {
    const selectedReportee = employeeEmails.value.find(
      emp => emp.emp_mail_id === createEmployee.value.reporting_to
    );
    if (selectedReportee) {
      createEmployee.value.reporting_designation = selectedReportee.designation;
    }
  } else {
    createEmployee.value.reporting_designation = ""; // Clear if reporting_to is empty
  }

  const payload = {
    ...createEmployee.value,
    department: createEmployee.value.department?.name || "", // Only send name
  };

  axiosInstance
    .put(
      `${apis.resource}${doctypes.EzyEmployeeList}/${createEmployee.value.name}`,
      payload
    )
    .then((response) => {
      if (response.data) {
        toast.success("Changes Saved", { autoClose: 500, transition: "zoom" });
        employeeData(); // refresh list
        const modal = bootstrap.Modal.getInstance(document.getElementById('exampleModal'));
        modal.hide();
        createEmployee.value = {}; // clear form
        searchText.value=""
      }
    })
    .catch((error) => {
      console.error("Error saving employee:", error);
    });
}

</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss" scoped>
.list-group {
  z-index: 1;
}

.zindex-dropdown {
  z-index: 1055;
  /* higher than .modal's z-index */
  max-height: 200px;
  overflow-y: auto;
}

.global-table th {
  background-color: #f2f2f2 !important;
  text-align: left;
  color: #999999;
  font-size: 12px;
}

.modal.show {
  display: block;
  background: rgba(0, 0, 0, 0.6);
}

.remove-btn {
  padding: 6px;
  position: relative;
  top: 36px;
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
  // width: 100% !important;
  padding: 5px 10px !important;

  border: none;
  border-radius: 4px;
  font-size: var(--eleven);

  // height: 32px;
}

.export-btn {
  background-color: #99999961;
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

// .employeeShow{
//   box-shadow: 0 0 10px rgba(0, 0, 0
//   , 0.1);
// }
.bulkemployee {
  // display: flex;
  // flex-direction: column;
  // align-items: center;
  // justify-content: center;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  width: 100%;
  margin-top: 20px;
  height: 85vh;
}

.insideBulkEmp {
  height: 70vh;
  // display: flex; 
  // flex-direction: column;
  // align-items: center;
  // justify-content: center;

}

.warning-box {
  background: #fff3cd;
  color: #856404;
  border: 1px solid #ffeeba;
  padding: 10px;
  margin: 10px 0;
  border-radius: 5px;
  font-size: 14px;
}

.warning-box h3 {
  margin-bottom: 5px;
  // font-size: 16px;
}

.warning-box ul {
  padding-left: 20px;
}

/* Table Container */
.table-container {
  width: 100%;
  overflow-x: auto;
}

/* Styled Table */
.styled-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  // font-family: Arial, sans-serif;
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

/* Table Head */
.styled-table thead {
  background: #ccc;
  color: #000;
  text-align: left;
  font-weight: bold;
}

.styled-table th {
  padding: 12px;
  text-transform: uppercase;
}

/* Table Body */
.styled-table tbody tr {
  border-bottom: 1px solid #ddd;
}

.styled-table tbody tr:nth-of-type(even) {
  background: #f9f9f9;
}

.styled-table td {
  padding: 12px;
}

/* Status Colors */
.status-success {
  color: #28a745;
  font-weight: bold;
}

.status-failed {
  color: #dc3545;
  font-weight: bold;
}

/* Responsive */
@media (max-width: 768px) {

  .styled-table th,
  .styled-table td {
    padding: 10px;
    font-size: 14px;
  }
}

.loader {
  width: 50px;
  aspect-ratio: 1;
  display: grid;
  mask: conic-gradient(from 15deg, transparent, black);
  -webkit-mask: conic-gradient(from 15deg, transparent, black);
  animation: l26 1s infinite steps(12);
  margin: 10px auto;
}

.loader,
.loader:before,
.loader:after {
  background:
    radial-gradient(closest-side at 50% 12.5%, #f03355 96%, transparent) 50% 0/20% 80% repeat-y,
    radial-gradient(closest-side at 12.5% 50%, #f03355 96%, transparent) 0 50%/80% 20% repeat-x;
}

.loader:before,
.loader:after {
  content: "";
  grid-area: 1/1;
  transform: rotate(30deg);
}

.loader:after {
  transform: rotate(60deg);
}

@keyframes l26 {
  100% {
    transform: rotate(1turn);
  }
}

/* Fade Animation */
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

.input-container {
  position: relative;
  display: flex;
  align-items: center;
}


.eye-icon {
  position: absolute;
  right: 10px;
  cursor: pointer;
}

.date-time {
  display: block;
  width: 100%;
  padding: .375rem .75rem;
  font-size: 13px;
  font-weight: 400;
  line-height: 1.5;
  color: var(--bs-body-color);
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  background-color: var(--bs-body-bg);
  background-clip: padding-box;
  border: var(--bs-border-width) solid var(--bs-border-color);
  border-radius: var(--bs-border-radius);
  transition: border-color .15s ease-in-out, box-shadow .15s ease-in-out;
}

.remarks {
  border: 1px solid #c5bdbd;
  border-radius: 5px;
}
</style>