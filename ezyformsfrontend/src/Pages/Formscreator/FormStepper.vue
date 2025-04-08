<template>
  <div>
    <div class="">
      <div class="">
        <div class="d-flex justify-content-between align-items-center CancelNdSave my-2 py-2">
          <div class="ps-1 my-2 d-flex align-items-center" @click="cancelForm()">
            <h1 class="font-13 ms-3">
              <i class="bi bi-arrow-left"></i><span class="ms-2">Back</span>
            </h1>
          </div>
          <div>
            <!-- <ButtonComp class="font-13 rounded-2" name="Save as Draft"></ButtonComp> -->
            <button v-if="activeStep === 2 && blockArr.length" :disabled="hasErrors || isNextDisabled"
              :style="{ cursor: hasErrors ? 'not-allowed' : 'pointer' }" type="butoon" class="btn font-13 btn-light"
              @click="saveFormData('draft')">
              <i class="bi bi-bookmark-check-fill"></i> Save As Draft
            </button>
          </div>
        </div>
        <div class="form-container p-0 container-fluid mt-1">
          <div class="row">
            <div class="col-2">
              <div class="steps-sticky-div">
                <ul class="steps">
                  <li v-for="step in steps" :key="step.id" :class="{
                    active: activeStep === step.id,
                    completed: activeStep > step.id,
                  }">
                    <div class="d-flex gap-3 align-items-center" @click="handleStepClick(step.id)" :class="{
                      'not-allowed': isNextDisabled && activeStep + 1 === step.id,
                    }">
                      <i v-if="activeStep > step.id" class="ri-checkbox-circle-fill completedStepIcon"></i>
                      <i v-else :class="step.icon"></i>
                      <div class="step-text">
                        <span class="font-11">{{ step.stepno }}</span><br />
                        <span class="font-14">{{ step.label }}</span>
                      </div>
                    </div>
                  </li>
                </ul>
              </div>
            </div>
            <div class="col-10 formbackground-color">
              <div class="">
                <div class="form-content stepsDiv">
                  <!-- About Form Step -->
                  <div v-if="activeStep === 1">
                    <div class="">
                      <div class="stepperbackground ps-2 pe-2 m-0 d-flex justify-content-between align-items-center">
                        <div></div>
                        <!-- <h1 class="font-14 m-0" @click="cancelForm()">
                          <i class="bi bi-chevron-left"></i><span class="ms-2">Cancel Form</span>
                        </h1> -->
                        <h1 class="font-14 fw-bold m-0">About Form</h1>
                        <div>
                          <button class=" btn btn-light font-12 mx-2" type="button" @click="clearForm">Clear
                            Form</button>

                          <ButtonComp class="btn btn-dark bg-dark text-white fw-bold font-13" name="Next"
                            v-if="activeStep < 3" @click="nextStep" />
                        </div>
                        <!-- :class="{ 'disabled-btn': isNextDisabled }" -->
                        <!-- :disabled="isNextDisabled" -->
                      </div>
                    </div>
                    <div class="container-fluid p-0">
                      <div class="row">
                        <div class="col-4"></div>
                        <div class="col-4">
                          <div class="mt-3">
                            <div class="">
                              <FormFields :disabled="paramId != undefined &&
                                paramId != null &&
                                paramId != 'new'
                                " labeltext="Form Name" class="formHeight" type="text" tag="input" name="Value"
                                id="formName" validationStar="true" placeholder="Untitled Form"
                                @change="(event) => handleInputChange(event, 'form_name')"
                                v-model="filterObj.form_name" />
                              <span v-if="formNameError" class="text-danger ErrorMsg ms-2">
                                {{ formNameError }}</span>
                            </div>
                          </div>
                          <div class="mt-3">
                            <div class="">
                              <FormFields :disabled="paramId != undefined &&
                                paramId != null &&
                                paramId != 'new'
                                " labeltext="Form Short Code" class="formHeight" type="text" tag="input" name="Value"
                                id="formShortCode" validationStar="true" placeholder="Untitled Form" @change="
                                  (event) => handleInputChange(event, 'form_short_name')
                                " v-model="filterObj.form_short_name" />
                              <span v-if="formShortNameError" class="text-danger ErrorMsg ms-2">
                                {{ formShortNameError }}</span>
                              <!-- <label for="">Form Short Code</label>

                                                        <Multiselect :options=formOptions
                                                            v-model="filterObj.form_short_name"
                                                            placeholder="Untitle Form" :multiple="true"
                                                            :searchable="true" /> -->
                            </div>
                          </div>
                          <div class="mt-3">
                            <div class="">
                              <!-- <FormFields labeltext="Owner Of The Form" class="mb-3 w-100"
                                                            tag="select" name="dept" id="dept"
                                                            placeholder="Select Department" :options=formOptions
                                                            v-model="filterObj.owner_of_the_form" /> -->
                              <label for="">Owner Of The Form
                                <span v-if="!filterObj.owner_of_the_form" class="text-danger">*</span></label>

                              <Multiselect :options="OwnerOfTheFormData" @change="OwnerOftheForm"
                                v-model="filterObj.owner_of_the_form" placeholder="Select Department" :multiple="false"
                                class="font-11 multiselect" :searchable="true" />
                            </div>
                          </div>
                          <div class="mt-3">
                            <div class="">
                              <!-- <FormFields labeltext="Form Cateogry" class="mb-3" tag="select"
                                                            name="desgination" id="desgination"
                                                            placeholder="Select Cateogry" :options=departments
                                                            v-model="filterObj.form_category" /> -->

                              <label for="">Form Cateogry
                                <span v-if="!filterObj.form_category" class="text-danger">*</span></label>

                              <Multiselect :options="departments" v-model="filterObj.form_category"
                                placeholder="Select Cateogry" :multiple="false" :searchable="true"
                                class="font-11 multiselect" />
                            </div>
                          </div>
                          <div class="mt-3">
                            <div class="">
                              <!-- <FormFields labeltext="Accessbility Departments" class="mb-3"
                            <Multiselect
                              :options="departments"
                              v-model="filterObj.form_category"
                              placeholder="Select Cateogry"
                              :multiple="false"
                              :searchable="true"
                              class="font-11 multiselect"
                            />
                          </div>
                        </div>
                        <div class="mt-3">
                          <div class=""> -->
                              <!-- <FormFields labeltext="Accessbility Departments" class="mb-3"
                                                            tag="multiselect" name="desgination" id="Departments"
                                                            placeholder="Select Desigination" :options=formOptions
                                                            v-model="filterObj.accessible_departments" /> -->
                              <!-- <v-select v-model="filterObj.accessible_departments"
                                                            :options="formOptions"></v-select> -->
                            </div>
                            <!-- <label for="">Accessbility Departments</label> -->
                            <!-- <Multiselect :options=formOptions
                                                        v-model="filterObj.accessible_departments"
                                                        placeholder="Select Desigination" :multiple="true"
                                                        track-by="code" :close-on-select="false"
                                                        :clear-on-select="false" :searchable="true" /> -->

                            <div>
                              <label class="typo__label">
                                <label for="">Accessibility Departments
                                  <span v-if="!filterObj.accessible_departments.length"
                                    class="text-danger">*</span></label>
                              </label>
                              <VueMultiselect v-model="filterObj.accessible_departments" :options="filteredOptions"
                                :multiple="true" :close-on-select="false" :clear-on-select="false"
                                :preserve-search="true" placeholder="Select Designation" class="font-11">
                                <template #option="{ option }">
                                  <div class="custom-option">
                                    <input type="checkbox" :checked="isChecked(option)" class="custom-checkbox"
                                      @change="toggleOption(option, $event)" />
                                    <span>{{ option }}</span>
                                  </div>
                                </template>

                                <template #selection="{ values, isOpen }">
                                  <span class="multiselect__single font-10" v-if="values.length" v-show="!isOpen">
                                    {{ formattedSelection }}
                                  </span>
                                </template>
                              </VueMultiselect>

                              <!-- <VueMultiselect
                              v-model="filterObj.accessible_departments"
                              :options="formOptions"
                              :multiple="true"
                              :close-on-select="false"
                              :clear-on-select="false"
                              :preserve-search="true"
                              placeholder="Select Designation"
                              class="font-11"
                            >
                              <template #option="{ option }">
                                <div class="custom-option">
                                  <input
                                    type="checkbox"
                                    :checked="
                                      filterObj.accessible_departments.includes(
                                        option
                                      )
                                    "
                                    class="custom-checkbox"
                                  />
                                  <span>{{ option }}</span>
                                </div>
                              </template>

                              <template #selection="{ values, isOpen }">
                                <span
                                  class="multiselect__single font-10"
                                  v-if="values.length"
                                  v-show="!isOpen"
                                >
                                  {{ values.join(", ") }} selected
                                </span>
                              </template>
                            </VueMultiselect> -->

                              <!-- <VueMultiselect v-model="filterObj.accessible_departments"
                                                            :options="formOptions" :multiple="true"
                                                            :close-on-select="false" :clear-on-select="false"
                                                            :preserve-search="true" placeholder="Select Designation"
                                                            class="font-11">
                                                            <template #selection="{ values, isOpen }">
                                                                <span class="multiselect__single font-10 d-flex"
                                                                    v-if="values.length" v-show="!isOpen">
                                                                    {{ values.join(", ") }}
                                                                    <span class=" ps-2 fw-bold"> selected</span>
                                                                </span>
                                                            </template>
                                                        </VueMultiselect> -->
                            </div>
                          </div>
                        </div>

                        <div class="col-4"></div>
                      </div>
                    </div>
                  </div>

                  <!-- Questions in Form Step -->
                  <div v-if="activeStep === 2">
                    <div class="">
                      <div class="stepperbackground ps-2 pe-2 m-0 d-flex justify-content-between align-items-center">
                        <h1 @click="prevStep(1)" class="font-11 m-0">
                          <i class="bi bi-chevron-left"></i><span class="ms-2">Back To About Form</span>
                        </h1>
                        <div class="d-flex gap-2 align-items-center">
                          <div>
                            <button v-if="isPreviewVisible"
                              class="btn btn-light previewBtn d-flex align-items-center font-13" type="button"
                              @click="previewForm">
                              <i class="bi bi-eye me-1 ms-1 mb-0"></i>Preview
                            </button>
                            <!-- <button
                              class="btn btn-light previewBtn d-flex align-items-center font-13"
                              type="button"
                              @click="previewForm"
                            >
                              <i class="bi bi-eye me-1 ms-1 mb-0"></i>Preview
                            </button> -->
                          </div>

                          <!-- <ButtonComp
                                                        class="buttoncomp btn btn-dark font-10 Withborder border"
                                                        name="Next" v-if="activeStep < 3" @click="nextStep" /> -->

                          <!-- :disabled="hasErrors || isNextDisabled"
                            :style="{
                              cursor: hasErrors ? 'not-allowed' : 'pointer',
                            }" -->
                          <button v-if="blockArr.length" class="btn btn-dark font-10 Withborder border" type="button"
                            @click="saveFormData('save')">
                            {{ paramId !== "new" ? "Update Form" : "Create Form" }}
                          </button>
                          <!-- <button class="btn btn-light font-10" type="button"
                                                        data-bs-toggle="modal" data-bs-target="#exampleModal"
                                                        @click="createForm">
                                                        <i class="bi bi-eye me-1"></i>Preview
                                                    </button> -->
                        </div>
                      </div>
                      <FormPreview :blockArr="selectedform" :formDescriptions="formDescriptions"
                        :childHeaders="childtableHeaders" />
                      <div class="main-block" ref="mainBlockRef">
                        <!-- Here is block level starts -->
                        <div class="block-level" v-for="(block, blockIndex) in blockArr" :key="blockIndex">
                          <div class="requestandAppHeader">
                            <div class="d-flex justify-content-between">
                              <div>
                                <h6 class="ps-2 pt-2">
                                  {{
                                    blockIndex === 0
                                      ? "Requestor Block"
                                      : `Approver
                                  Block ${blockIndex}
                                  `
                                  }}
                                  <!-- ${blockIndex++} -->
                                </h6>
                              </div>
                              <div class="d-flex">
                                <div v-if="paramId && workflowSetup.length" class="role-container">
                                  <label class="role-text d-flex align-items-center"
                                    v-if="getWorkflowSetup(blockIndex)">
                                    <span class="role-label">
                                      {{
                                        getWorkflowSetup(blockIndex).roles.length > 0
                                          ? blockIndex === 0
                                            ? "Requestor: "
                                            : "Approver: "
                                          : ""
                                      }}
                                    </span>
                                    <span class="role-names">
                                      {{
                                        getWorkflowSetup(blockIndex)
                                          .roles.slice(0, 2)
                                          .join(", ")
                                      }}
                                    </span>
                                    <span data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight"
                                      aria-controls="offcanvasRight" @click="AddDesignCanvas(blockIndex)"
                                      v-if="getWorkflowSetup(blockIndex).roles.length > 2" class="more-count">
                                      +{{ getWorkflowSetup(blockIndex).roles.length - 2 }}
                                      more
                                    </span>
                                  </label>
                                </div>

                                <button v-if="
                                  paramId != undefined &&
                                  paramId != null &&
                                  paramId != 'new' &&
                                  getWorkflowSetup(blockIndex).roles.length === 0
                                " class="btn btn-light designationBtn d-flex align-items-center" type="button"
                                  data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight"
                                  aria-controls="offcanvasRight" @click="AddDesignCanvas(blockIndex)">
                                  <img src="../../assets/oui_app-users-roles.svg" alt="Add" class="me-1" />
                                  Add designations
                                </button>

                                <!-- Edit Designation Button (only when roles are present for that block) -->
                                <button v-if="
                                  paramId != undefined &&
                                  paramId != null &&
                                  paramId != 'new' &&
                                  getWorkflowSetup(blockIndex).roles.length > 0
                                " class="btn btn-light designationBtn d-flex align-items-center" type="button"
                                  data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight"
                                  aria-controls="offcanvasRight" @click="AddDesignCanvas(blockIndex)">
                                  <i class="bi bi-pencil font-14"></i>
                                </button>
                                <button class="btn btn-light bg-transparent border-0 font-13 deleteBlock"
                                  @click="removeBlock(blockIndex)">
                                  <i class="bi bi-trash me-1"></i> Delete Block
                                </button>
                              </div>
                            </div>
                          </div>
                          <!-- draggable="true" @dragstart="handleDragStart($event, sectionIndex, 'section', blockIndex)"
                                                            @dragover="handleDragOver($event)"
                                                            @drop="handleDrop($event, sectionIndex, 'section', blockIndex)" -->
                          <div class="mt-2 section_block">
                            <div v-for="(section, sectionIndex) in block.sections" :key="'section-' + sectionIndex"
                              class="dynamicSection section">
                              <section class="d-flex justify-content-between align-items-center">
                                <div class="d-flex flex-column">
                                  <input v-model="section.label" type="text" :class="[
                                    'border-less-input',
                                    'font-14',
                                    { 'italic-style': !section.label },
                                    { 'fw-medium': section.label },
                                  ]" @change="handleFieldChange(blockIndex, sectionIndex)"
                                    placeholder="Untitled section" />
                                  <small v-if="section.errorMsg" class="text-danger font-10">
                                    {{ section.errorMsg }}
                                  </small>
                                </div>
                                <div class="d-flex align-items-center">
                                  <!-- Button trigger modal -->
                                  <!-- <button type="button" class="btn btn-white font-12" data-bs-toggle="modal"
                                    data-bs-target="#childtable">
                                    Add Table
                                  </button> -->

                                  <button class="btn btn-light bg-transparent border-0 font-13 deleteSection"
                                    @click="removeSection(blockIndex, sectionIndex)">
                                    <i class="bi bi-trash me-1"></i> Delete Section
                                  </button>
                                </div>
                              </section>
                              <!-- draggable="true" @dragstart="handleDragStart($event, rowIndex, 'row', blockIndex, sectionIndex)"
                                                                    @dragover="handleDragOver"
                                                                    @drop="handleDrop($event, rowIndex, 'row', blockIndex, sectionIndex)" -->
                              <div class="container-fluid">
                                <section class="row dynamicRow row-container" v-for="(row, rowIndex) in section.rows"
                                  :key="'row-' + rowIndex">
                                  <div class="d-flex justify-content-between align-items-center">
                                    <label class="rownames">{{
                                      getRowSuffix(rowIndex)
                                    }}</label>
                                    <div>
                                      <button v-if="row.columns.length < 3"
                                        class="btn btn-light bg-transparent border-0 font-12" @click="
                                          addColumn(blockIndex, sectionIndex, rowIndex)
                                          ">
                                        <i class="bi bi-plus font-14"></i> Add Column
                                      </button>
                                      <!-- <button class="btn btn-light bg-transparent border-0 font-12 deleteRow" @click="
                                        removeRow(blockIndex, sectionIndex, rowIndex)
                                        ">
                                        <i class="ri-subtract-line"></i> Delete row
                                      </button> -->
                                    </div>
                                  </div>
                                  <!-- draggable="true"
                                                                                @dragstart="handleDragStart($event, columnIndex, 'column', blockIndex, sectionIndex, rowIndex)"
                                                                                @dragover="handleDragOver"
                                                                                @drop="handleDrop($event, columnIndex, 'column', blockIndex, sectionIndex, rowIndex)" -->
                                  <div class="col">
                                    <div class="row">
                                      <div v-for="(column, columnIndex) in row.columns" :key="'column-' + columnIndex"
                                        @mouseenter="
                                          setHoveredColumn(
                                            blockIndex,
                                            sectionIndex,
                                            rowIndex,
                                            columnIndex
                                          )
                                          " @mouseleave="resetHoveredColumn"
                                        class="col p-0 dynamicColumn position-relative column-container">
                                        <div class="column_name d-flex align-items-center justify-content-between">
                                          <div class="d-flex flex-column ps-2">
                                            <input v-model="column.label" type="text" :class="[
                                              'border-less-input',
                                              'ps-1',
                                              'font-14',
                                              'inputHeight',
                                              {
                                                'italic-style': !column.label,
                                              },
                                              { 'fw-medium': column.label },
                                            ]" @change="
                                              handleFieldChange(
                                                blockIndex,
                                                sectionIndex,
                                                rowIndex,
                                                columnIndex
                                              )
                                              " placeholder="Column Name" />
                                            <small v-if="column.errorMsg" class="text-danger font-10">
                                              {{ column.errorMsg }}
                                            </small>
                                          </div>
                                          <div class="position-absolute top-0 end-0" v-show="isHoveredColumn(
                                            blockIndex,
                                            sectionIndex,
                                            rowIndex,
                                            columnIndex
                                          )
                                            ">
                                            <button class="btn btn-light bg-transparent me-1 btn-sm" @click="
                                              removeColumn(
                                                blockIndex,
                                                sectionIndex,
                                                rowIndex,
                                                columnIndex
                                              )
                                              ">
                                              <i class="bi bi-x-lg"></i>
                                            </button>
                                          </div>
                                        </div>
                                        <!-- draggable="true"
                                                                                    @dragstart="handleDragStart($event, fieldIndex, 'field', blockIndex, sectionIndex, rowIndex, columnIndex)"
                                                                                    @dragover="handleDragOver"
                                                                                    @drop="handleDrop($event, fieldIndex, 'field', blockIndex, sectionIndex, rowIndex, columnIndex)" -->
                                        <div v-for="(field, fieldIndex) in column.fields" :key="'field-' + fieldIndex"
                                          @mouseenter="
                                            setHoveredField(
                                              blockIndex,
                                              sectionIndex,
                                              rowIndex,
                                              columnIndex,
                                              fieldIndex
                                            )
                                            " @mouseleave="resetHoveredField" class="dynamicField">
                                          <div class="px-1 dynamic_fied field-border">
                                            <div class="d-flex justify-content-between">
                                              <div class="flex-column d-flex">
                                                <input v-model="field.label" placeholder="Name the field" :class="[
                                                  'border-less-input',
                                                  'font-14',
                                                  'p-0',
                                                  'inputHeight',
                                                  {
                                                    'italic-style': !field.label,
                                                  },
                                                  {
                                                    'fw-medium': field.label,
                                                  },
                                                ]" @change="
                                                  handleFieldChange(
                                                    blockIndex,
                                                    sectionIndex,
                                                    rowIndex,
                                                    columnIndex,
                                                    fieldIndex
                                                  )
                                                  " />
                                                <small v-if="field.errorMsg" class="text-danger font-10">
                                                  {{ field.errorMsg }}
                                                </small>
                                              </div>
                                              <div class="FieldcopyRemove" v-show="isHoveredField(
                                                blockIndex,
                                                sectionIndex,
                                                rowIndex,
                                                columnIndex,
                                                fieldIndex
                                              )
                                                ">
                                                <button class="btn btn-light btn-sm bg-transparent py-0" @click="
                                                  copyField(
                                                    blockIndex,
                                                    sectionIndex,
                                                    rowIndex,
                                                    columnIndex,
                                                    fieldIndex
                                                  )
                                                  ">
                                                  <i class="ri-file-copy-line font-13 copyIcon"></i>
                                                </button>
                                                <button class="btn btn-light btn-sm bg-transparent trash-btn py-0"
                                                  @click="
                                                    removeField(
                                                      blockIndex,
                                                      sectionIndex,
                                                      rowIndex,
                                                      columnIndex,
                                                      fieldIndex
                                                    )
                                                    ">
                                                  <i class="bi bi-x-lg font-13"></i>
                                                </button>
                                              </div>
                                            </div>

                                            <select v-model="field.fieldtype"
                                              class="form-select mb-2 mt-1 font-13 searchSelect" @change="
                                                onFieldTypeChange(
                                                  blockIndex,
                                                  sectionIndex,
                                                  rowIndex,
                                                  columnIndex,
                                                  fieldIndex
                                                )
                                                ">
                                              <option value="">Select Type</option>
                                              <option v-for="section in fieldTypes" :key="section"
                                                :value="section.type">
                                                {{ section.label }}
                                              </option>
                                            </select>

                                            <div v-if="
                                              [
                                                'Select',
                                                'Table MultiSelect',
                                                'Check', 'Small Text'
                                              ].includes(field.fieldtype)
                                            ">
                                              <label class="font-12 fw-light" for="options">Enter Options:</label>
                                              <textarea id="options" placeholder="Enter your Options"
                                                v-model="field.options"
                                                class="form-control shadow-none mb-1 font-12"></textarea>
                                              <small v-if="
                                                !field.options ||
                                                field.options.trim() === ''
                                              " class="text-danger font-10">
                                                Options are required for this field type.
                                              </small>
                                            </div>

                                            <div class="d-flex  align-items-center justify-content-between">
                                              <div class=" d-flex align-items-center gap-2">
                                                <div class="d-flex align-items-center">

                                                  <input class="font-12" v-model="field.reqd" :true-value="1"
                                                    :false-value="0" placeholder="Field Name" type="checkbox" />
                                                </div>
                                                <div>
                                                  <label for="mandatory" class="font-12 m-0 fw-light">Mandatory</label>
                                                </div>
                                              </div>
                                              <div>

                                                <button class="btn btn-sm  font-12"
                                                  @click="field.showDescription = !field.showDescription">
                                                  {{ field.showDescription ? 'Hide Description' : (field.description ?
                                                  'Edit Description'
                                                  : 'Add Description') }}
                                                </button>
                                              </div>
                                            </div>

                                            <!-- Description Textarea -->
                                            <textarea v-if="field.showDescription" v-model="field.description"
                                              class="form-control font-12 mt-2"
                                              placeholder="Enter field description"></textarea>

                                            <small v-if="field.error" class="text-danger font-10">{{ field.error
                                            }}</small>
                                          </div>
                                        </div>

                                        <div class="d-flex justify-content-center align-items-center my-2">
                                          <button class="btn btn-light btn-sm d-flex align-items-center addField m-2"
                                            @click="
                                              addField(
                                                blockIndex,
                                                sectionIndex,
                                                rowIndex,
                                                columnIndex
                                              )
                                              ">
                                            <i class="bi bi-plus fs-5"></i>
                                            <span>Add Field</span>
                                          </button>
                                        </div>
                                      </div>
                                    </div>

                                  </div>
                                </section>
                              </div>
                            </div>

                            <div class="d-flex justify-content-center align-items-center py-2 add-section-btn">
                              <button class="btn btn-light border font-12" @click="addSection(blockIndex)">
                                <i class="bi bi-plus-circle me-1 fs-6"></i> Add Section
                              </button>
                            </div>
                            <div v-if="
                              blockIndex === 0
                            " class="m-2">
                              <!-- <button
                                  class="btn btn-light addRow m-2"
                                  @click="
                                    addRow(blockIndex, sectionIndex, rowIndex)
                                  "
                                >
                                  <i class="bi bi-plus"></i> Add row in section
                                </button> -->

                              <div class="childtableShow">
                                <div>
                                  <div>
                                    <div v-if="blockIndex === 0" class="mt-2">

                                      <div class="childTableContainer">

                                        <div v-for="(table, tableName) in childtableHeaders" :key="tableName"
                                          class="childTable">
                                          <h5>{{ tableName.replace(/_/g, ' ') }}</h5>
                                          <table class="table table-bordered">
                                            <thead>
                                              <tr>
                                                <th>#</th>
                                                <th>Label</th>
                                                <th>Field Type</th>
                                                <!-- <th>Action</th> -->
                                              </tr>
                                            </thead>
                                            <tbody>
                                              <tr v-for="(field, index) in table" :key="index">
                                                <td>{{ index + 1 }}</td>

                                                <!-- Label Input -->
                                                <td v-if="editMode[tableName]">
                                                  <input v-model="field.label" placeholder="Field Label"
                                                    class="form-control "
                                                    :class="{ 'border-1 border-danger ': invalidFields[tableName]?.includes(index) }" />
                                                  <span v-if="invalidFields[tableName]?.includes(index)"
                                                    class="font-11 text-danger">Label
                                                    required**</span>
                                                </td>
                                                <td v-else>{{ field.label }}</td>

                                                <!-- Field Type Select -->
                                                <td v-if="editMode[tableName]">
                                                  <div class="d-flex gap-1">

                                                    <select v-model="field.fieldtype" class="form-select form-select-sm"
                                                      :class="{ 'border-1 border-danger ': invalidFields[tableName]?.includes(index) }">
                                                      <option value="">Select Type</option>
                                                      <option v-for="option in childfield" :key="option.type"
                                                        :value="option.type">
                                                        {{ option.label }}
                                                      </option>
                                                    </select>
                                                    <span v-if="editMode[tableName]">
                                                      <button class="btn btn-light btn-sm"
                                                        @click="deleteRow(tableName, index)">
                                                        <i class="bi bi-x-lg"></i>
                                                      </button>
                                                    </span>
                                                  </div>


                                                  <span v-if="invalidFields[tableName]?.includes(index)"
                                                    class="font-11 text-danger">Type
                                                    required**</span>

                                                </td>
                                                <td v-else>{{ field.fieldtype }}</td>

                                              </tr>
                                            </tbody>
                                          </table>

                                          <!-- Show error message below the table if any fields are invalid -->
                                          <!-- <div v-if="invalidFields[tableName]?.length" class="text-danger font-12 mt-2">
     Please fill in the required fields in the highlighted rows.
  </div> -->
                                          <div class="mb-2"> <button class="btn btn-light btn-sm mx-2 "
                                              @click="toggleEdit(tableName)">
                                              {{ editMode[tableName] ? 'Save' : 'Edit' }}
                                            </button>
                                            <button class="btn btn-light btn-sm " v-if="editMode[tableName]"
                                              @click="addNewFieldedit(tableName)">
                                              Add More Field
                                            </button>
                                          </div>

                                        </div>

                                        <!-- <div v-for="(field, fIndex) in table.newFields" :key="fIndex"
                                            class="newField dynamicField">
                                            <div class=" d-flex justify-content-between">

                                              <input v-model="field.label" placeholder="Field Label" :class="[
                                                'border-less-input',
                                                'font-14',
                                                'p-0 my-1',
                                                'inputHeight',
                                                { 'italic-style': !field.label },
                                                { 'fw-medium': field.label },
                                              ]" />
                                              
                                            </div>
                                            <select v-model="field.fieldtype" class="form-select font-13 mb-3">
                                              <option value="">Select Type</option>
                                              <option v-for="section in childfield" :key="section.type"
                                                :value="section.type">
                                                {{ section.label }}
                                              </option>
                                            </select>

                                          </div>

                                          <button class="btn btn-light btn-sm font-12 my-2" @click="toggleEdit(tableName)">
                                              {{ editMode[tableName] ? "Save" : "Edit" }}
                                            </button>
                                          <button class="btn btn-light btn-sm font-12 my-2"
                                            @click="addNewField(tableName, tableIndex)">Add Fields</button>

                                          <button v-if="table.newFields" class="btn btn-dark btn-sm font-12 my-2 ms-2"
                                            @click="saveNewFields(tableName, tableIndex)">Save</button> -->
                                      </div>
                                    </div>
                                  </div>


                                  <div>
                                    <div v-if="blockIndex === 0">
                                      <div>
                                        <button class="btn btn-light addRow mb-3 mt-4" @click="addChildTable">
                                          Add New Table
                                        </button>

                                        <div v-for="(table, tableIndex) in childTables" :key="tableIndex"
                                          class="child-table">
                                          <div class="d-flex justify-content-between align-items-center mt-1 mb-2">
                                            <div>

                                              <span :class="table.tableName ? 'd-none' : 'text-danger'">*</span>
                                              <input @change="(e) => formatTableName(tableIndex, e)"
                                                v-model="table.tableName" placeholder="Table Name" :class="[
                                                  'border-less-input',
                                                  'font-14',
                                                  'p-0',
                                                  'inputHeight',
                                                  { 'italic-style': !table.tableName },
                                                  { 'fw-medium': table.tableName },
                                                ]" />
                                            </div>
                                            <button class="btn btn-light bg-transparent border-0 font-13 deleteSection"
                                              @click="removeChildTable(tableIndex)">
                                              <i class=" bi bi-trash"></i> Remove Table
                                            </button>
                                          </div>

                                          <div v-for="(field, fieldIndex) in table.columns" :key="fieldIndex"
                                            class="dynamicField">
                                            <div class="px-1 field-border">
                                              <div class="d-flex justify-content-between">
                                                <input v-model="field.label" placeholder="Name the field" :class="[
                                                  'border-less-input',
                                                  'font-14',
                                                  'p-0',
                                                  'inputHeight',
                                                  { 'italic-style': !field.label },
                                                  { 'fw-medium': field.label },
                                                ]" />
                                                <button class="btn btn-sm trash-btn py-0"
                                                  @click="removeFieldFromTable(tableIndex, fieldIndex)">
                                                  <i class="bi bi-x-lg"></i>
                                                </button>
                                              </div>

                                              <select v-model="field.fieldtype" class="form-select font-13 mb-3">
                                                <option value="">Select Type</option>
                                                <option v-for="section in childfield" :key="section.type"
                                                  :value="section.type">
                                                  {{ section.label }}
                                                </option>
                                              </select>
                                            </div>
                                          </div>

                                          <button class="btn btn-light btn-sm addField mx-1"
                                            @click="addFieldToTable(tableIndex)">
                                            <i class="bi bi-plus"></i> Add Field
                                          </button>

                                          <button v-if="table.columns.length" class="btn btn-dark btn-sm font-12 mx-1"
                                            @click="processFields(tableIndex)">
                                            Create Table
                                          </button>



                                          <hr />
                                        </div>
                                      </div>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </div>
                          </div>
                        </div>

                        <div :class="[
                          'd-flex justify-content-center align-items-center add-block-btn-div py-4  ',
                          {
                            'background-color-white': blockArr.length,
                          },
                        ]">
                          <button class="btn btn-light border d-flex align-items-center font-12" @click="addBlock">
                            <i class="bi bi-plus-circle me-1 fs-6"></i>
                            {{
                              blockArr.length === 0
                                ? "Add Requestor Block"
                                : "Add Approval Block"
                            }}
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-if="activeStep === 3"></div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
      <div class="offcanvas-header add_designationHeader">
        <span id="offcanvasRightLabel" class="font-14">
          Add designation for
          {{ selectedBlockIndex == 0 ? "Requestor" : "Approver" }}
        </span>

        <button type="button" class="btn-close bg-light text-reset" data-bs-dismiss="offcanvas"
          aria-label="Close"></button>
      </div>
      <div class="offcanvas-body">
        <div class="">
          <div class="form-check ps-1" v-if="selectedBlockIndex !== 0">
            <div>

              <input type="checkbox" id="ViewOnlyReportee" v-model="ViewOnlyReportee"
                class="me-2 mt-1  form-check-input"  />
              <label for="ViewOnlyReportee " class="SelectallDesignation fw-bold mt-1 form-check-label">View Only
                Reportee</label>
            </div>
          </div>
          <input v-model="searchDesignation" class="px-2 py-1 rounded-2 form-control shadow-none my-3" type="text"
            placeholder="Search Designation" />

          <div class="form-check ps-1" v-if="DesignationList.length && selectedBlockIndex == 0">
            <div>
              <!-- :disabled="ViewOnlyReportee"  -->
              <input type="checkbox" id="selectAll" v-model="isAllSelected" class="me-2 mt-1 form-check-input" />
              <label for="selectAll fw-bold m-0" class="SelectallDesignation form-check-label">Select all</label>
            </div>

          </div>
        </div>
        <ul v-if="DesignationList.length" class="list-unstyled">
          <li v-for="(item, index) in filteredDesignationList" :key="index" class="designationList">
            <input type="checkbox" v-model="designationValue" :value="item" class="designationCheckBox" 
              @change="handleSingleSelect" />
            <span class="ps-2" :class="{ 'opacity-50': ViewOnlyReportee }">{{ item }}</span>
          </li>
        </ul>
        <div v-else>
          <div class="d-flex justify-content-center">
            <span>No Designations Found</span>
          </div>
        </div>
      </div>

      <div class="offcanvas-footer">
        <div class="text-end p-3">
          <ButtonComp class="btn btn-dark addingDesignations" data-bs-dismiss="offcanvas" @click="addDesignationBtn"
            name=" Add Designations" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import FormFields from "../../Components/FormFields.vue";
import { onMounted, ref, reactive, computed, watch, nextTick } from "vue";
import ButtonComp from "../../Components/ButtonComp.vue";
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import {
  extractFieldsWithBreaks,
  rebuildToStructuredArray,
  extractFieldnames,
  extractfieldlabels,
  addErrorMessagesToStructuredArray,
} from "../../shared/services/field_format";
import axiosInstance from "../../shared/services/interceptor";
import { apis, doctypes } from "../../shared/apiurls";
import { useRoute, useRouter } from "vue-router";
import FormPreview from "../../Components/FormPreview.vue";
import Multiselect from "vue-multiselect";
import "@vueform/multiselect/themes/default.css";
import VueMultiselect from "vue-multiselect";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
// import { nextTick } from "vue";
import { useDragAndDrop } from "../../shared/services/draggable";

const route = useRoute();
const router = useRouter();
const activeStep = ref(1);
const departments = ref([]);
const categories = ref([]);
const formOptions = ref([]);
const OwnerOfTheFormData = ref([]);
let sections = reactive([]);
let blockArr = reactive([]);
let deleted_items = reactive([]);
const DesignationList = ref([]);
// "intern", "Junior associate", "Associate", "Senior associate", "Supervisor"
const designationValue = ref([]);
const ezyFormsData = ref([]);
const formNameError = ref("");
const formShortNameError = ref("");
const selectedBlockIndex = ref("");
let workflowSetup = reactive([]);
const searchDesignation = ref("");
const ViewOnlyReportee = ref(0);
const wrkAfterGetData = ref([]);
// const hasWorkflowToastShown = ref(false);
const tableFieldsCache = ref([]);

// const childtableRows = ref([]);
const childtableHeaders = ref([]);
// const childtableName = ref("");
// const childTableresponseData = ref([]);

const tableName = ref("");
let paramId = ref("");
const businessUnit = computed(() => {
  return EzyBusinessUnit;
});
const childtableShow = ref(false);
const columns = reactive([]);

const filterObj = ref({
  form_name: "",
  form_short_name: "",
  accessible_departments: [],
  business_unit: `${businessUnit.value.value}`,
  form_category: "",
  owner_of_the_form: "",
});
const formDescriptions = computed(() => filterObj.value);
const child_id = ref("");
const updateBtnDiv = ref(false);
// const formDescriptions = ref({ ...filterObj.value });
function addMoreFieldsToTable(type) {
  if (type === "new") {
    childtableShow.value = !childtableShow.value;
  }
  if (type === "more") {
    updateBtnDiv.value = !updateBtnDiv.value;
  }
  // const newField = {
  //   label: "",
  //   fieldname: `field_${columns.length}`,
  //   fieldtype: "",
  //   idx: columns.length,
  //   reqd: false,
  // };
  // columns.push(newField);
}
// errorMsg: "",
watch(
  businessUnit,
  (newVal) => {
    if (newVal && newVal.value) {
      filterObj.value.business_unit = newVal.value;
    }
  },
  { immediate: true }
);
// const ViewOnlyReporteeFn = () => {
//   if (ViewOnlyReportee.value) {
//     designationValue = [];
//     isAllSelected = false;
//     employeeData()
//   }
// };




const filteredDesignationList = computed(() => {
  return DesignationList.value
    .filter((item) => item.toLowerCase().includes(searchDesignation.value.toLowerCase()))
    .sort((a, b) => {
      const aSelected = designationValue.value.includes(a);
      const bSelected = designationValue.value.includes(b);
      if (aSelected === bSelected) return 0;
      return aSelected ? -1 : 1;
    });
});

const hoveredIndexes = ref(null);
const hoveredColumnIndexes = ref(null);

// Functions for Field Hover
const setHoveredField = (blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex) => {
  hoveredIndexes.value = {
    blockIndex,
    sectionIndex,
    rowIndex,
    columnIndex,
    fieldIndex,
  };
};

const resetHoveredField = () => {
  hoveredIndexes.value = null;
};

const isHoveredField = (blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex) => {
  return (
    hoveredIndexes.value &&
    hoveredIndexes.value.blockIndex === blockIndex &&
    hoveredIndexes.value.sectionIndex === sectionIndex &&
    hoveredIndexes.value.rowIndex === rowIndex &&
    hoveredIndexes.value.columnIndex === columnIndex &&
    hoveredIndexes.value.fieldIndex === fieldIndex
  );
};

// Functions for Column Hover
const setHoveredColumn = (blockIndex, sectionIndex, rowIndex, columnIndex) => {
  hoveredColumnIndexes.value = {
    blockIndex,
    sectionIndex,
    rowIndex,
    columnIndex,
  };
};

const resetHoveredColumn = () => {
  hoveredColumnIndexes.value = null;
};

const isHoveredColumn = (blockIndex, sectionIndex, rowIndex, columnIndex) => {
  return (
    hoveredColumnIndexes.value &&
    hoveredColumnIndexes.value.blockIndex === blockIndex &&
    hoveredColumnIndexes.value.sectionIndex === sectionIndex &&
    hoveredColumnIndexes.value.rowIndex === rowIndex &&
    hoveredColumnIndexes.value.columnIndex === columnIndex
  );
};
onMounted(() => {
  deptData();
  paramId.value = route.params.paramid || "new";
  // console.log(paramId.value, "ggggg");

  if (paramId.value != undefined && paramId.value != null && paramId.value != "new") {
    getFormData();
    OwnerOftheForm();
  }
  let Bu_Unit = localStorage.getItem("Bu");
  filterObj.value.business_unit = Bu_Unit;
});


// Store multiple child tables
const childTables = ref([]);

// Function to add a new child table
const addChildTable = () => {
  const existingFieldsCount = Object.values(childtableHeaders.value).reduce((acc, table) => {
    return acc + (Array.isArray(table) ? table.length : 0);
  }, 0);

  // New index starts from the total existing fields
  const newIndex = existingFieldsCount + childTables.value.length;

  childTables.value.push({
    idx: newIndex,
    tableName: "",
    formattedTableName: "",
    columns: reactive([
      {
        label: "",
        fieldname: `field_${columns.length}`, // This will be updated once the label is entered
        fieldtype: "",
        idx: columns.length,
        reqd: false,
      }
    ]), // Use `ref([])` instead of `reactive([])`
    // Store new fields separately
  });
};

// Function to remove a specific child table
const removeChildTable = (tableIndex) => {
  childTables.value.splice(tableIndex, 1);
};

// Function to add a field to a specific table
const addFieldToTable = (tableIndex) => {
  const columns = childTables.value[tableIndex].columns;

  columns.push({
    label: "",
    fieldname: "", // This will be updated once the label is entered
    fieldtype: "",
    idx: columns.length,
    reqd: false,
  });

  // Watch for label changes and update fieldname dynamically
  watch(() => columns[columns.length - 1]?.label, (newLabel) => {
    columns[columns.length - 1].fieldname = `${newLabel.replace(/\s+/g, "_").toLowerCase()}_${columns.length - 1}`;
  });
};

// Function to remove a field from a specific table
const removeFieldFromTable = (tableIndex, fieldIndex) => {
  childTables.value[tableIndex].columns.splice(fieldIndex, 1);
};
// Format table name dynamically
const formatTableName = (tableIndex, event) => {
  if (event?.target?.value) {
    childTables.value[tableIndex].formattedTableName = event.target.value
      .trim()
      .toLowerCase()
      .replace(/\s+/g, "_")
      .replace(/[^a-z0-9_]/g, "");
  }
};

// Validate if table fields are complete
const isEmptyFieldType = (tableIndex) => {
  return (
    !childTables.value[tableIndex].tableName.length ||
    childTables.value[tableIndex].columns.some(
      (field) => !field.fieldtype || !field.label
    )
  );
};

// Process fields for a specific table
const processFields = (tableIndex) => {
  if (isEmptyFieldType(tableIndex)) {
    toast.error("Please fill in all required fields before proceeding.", {
      transition: "zoom",
    });
    return;
  }

  const data = {
    form_short_name: childTables.value[tableIndex].formattedTableName,
    fields: childTables.value[tableIndex].columns,
    idx: childTables.value[tableIndex].idx
  };



  axiosInstance
    .post(apis.childtable, data)
    .then((res) => {
      if (res) {
        toast.success("Table created successfully!", { autoClose: 500 }, {
          transition: "zoom",
        });
        const firstTableField = res.message[0][0].child_doc;
        if (firstTableField) {
          tableFieldsCache.value.push(firstTableField);
        }
      }
    })
    .catch((error) => {
      console.error("Error saving form data:", error);
    });
};

const editMode = reactive({});
// const toggleEdit = (tableName) => {
//   if (editMode[tableName]) {
//     console.log("Saving table:", tableName);

//     // Remove the 'value' key from each object in the child table
//     const filteredData = childtableHeaders.value[tableName].map(({ value, ...rest }) => rest);

//     console.log("Filtered Table Data:", JSON.parse(JSON.stringify(filteredData)));

//     // Construct form data
//     const form = {
//       "name": tableName,
//       "doctype": "DocType",
//       "fields": filteredData, // Child table data without 'value' key
//     };

//     const formData = new FormData();
//     formData.append("doc", JSON.stringify(form));
//     formData.append("action", "Save");

//     console.log("FormData to be sent:", formData);

//     // Send the data to the API
//     axiosInstance
//       .post(apis.savedocs, formData)
//       .then((response) => {
//         console.log("Save successful:", response.data);
//       })
//       .catch((error) => {
//         console.error("Save failed:", error);
//       });
//   }

//   // Toggle edit mode
//   editMode[tableName] = !editMode[tableName];
// };






const addNewFieldedit = (tableName) => {
  if (!childtableHeaders.value[tableName]) {
    childtableHeaders.value[tableName] = [];
  }

  // Assign idx based on existing field count
  const newIndex = childtableHeaders.value[tableName].length + 1;

  childtableHeaders.value[tableName].push({
    fieldname: `field_${newIndex - 1}`, // Ensuring unique fieldname
    fieldtype: "",
    idx: newIndex, // Assign idx dynamically
    label: "",
    value: "", // Keep value
    isNew: true,
  });
};
const deleteRow = (tableName, index) => {
  if (childtableHeaders.value[tableName]) {
    childtableHeaders.value[tableName].splice(index, 1);
  }
};


const invalidFields = ref({});

const toggleEdit = (tableName) => {
  if (editMode[tableName]) {


    // ✅ Reset validation errors
    invalidFields.value[tableName] = [];

    let isValid = true;

    // Validate all fields in the table
    childtableHeaders.value[tableName].forEach((field, index) => {
      if (!field.label || !field.fieldtype) {
        invalidFields.value[tableName].push(index); // Store index of invalid rows
        isValid = false;
      }
    });

    if (!isValid) {

      return; // Stop execution if validation fails
    }



    // Process all fields (both old and new)
    let allFields = childtableHeaders.value[tableName].map(({ isNew, ...rest }, index) => ({
      ...rest,
      idx: index + 1, // Ensure `idx` is correctly set in sequential order
    }));

    // ✅ Single API request to save both old and new fields
    const formData = {
      form_short_name: tableName,

      fields: allFields,
    };



    axiosInstance
      .post(apis.childtable, formData) // Use a single API endpoint
      .then((response) => {
        toast.success("Fields updated successfully!", { autoClose: 500 }, {
          transition: "zoom",
        });
        console.log("✅ All fields saved successfully:", response.data);
      })
      .catch((error) => {
        console.error("❌ Saving fields failed:", error);
      });
  }

  // Toggle edit mode for the table
  editMode[tableName] = !editMode[tableName];
};


watch(childtableHeaders, (newTables) => {
  Object.keys(newTables).forEach((tableName) => {
    newTables[tableName].forEach((field, index) => {
      if (field.label && field.fieldtype) {
        // ✅ Remove error dynamically when user enters a valid value
        invalidFields.value[tableName] = invalidFields.value[tableName]?.filter(i => i !== index);
      }
    });
  });
}, { deep: true });








// const getFieldLabel = (fieldtype) => {
//   if (!childfield.value || !Array.isArray(childfield.value)) return fieldtype;
//   const field = childfield.value.find((f) => f.type === fieldtype);
//   return field ? field.label : fieldtype;
// };


// const addNewField = (tableKey) => {
//   if (!childtableHeaders.value || typeof childtableHeaders.value !== "object") {
//     console.error("childtableHeaders is not a valid object:", childtableHeaders.value);
//     return;
//   }

//   const table = childtableHeaders.value[tableKey]; // Access by key

//   // ✅ Ensure `table` exists
//   if (!table) {
//     console.error(`Table with key "${tableKey}" not found.`);
//     return;
//   }

//   // ✅ Ensure `table` is an array
//   if (!Array.isArray(table)) {
//     console.error(`Table "${tableKey}" is not an array:`, table);
//     return;
//   }

//   const newIndex = table.length;

//   const newField = {
//     fieldname: `field_${newIndex + 1}`,
//     fieldtype: "",
//     idx: newIndex + 1,
//     label: "",
//     value: "",
//   };

//   table.push(newField);

//   // ✅ Ensure newIndex is within bounds before watching
//   if (table.length > newIndex) {
//     watch(
//       () => table[newIndex]?.label,
//       (newLabel) => {
//         if (table[newIndex]) {
//           table[newIndex].fieldname = newLabel?.trim().replace(/\s+/g, "_").toLowerCase();
//         }
//       }
//     );
//   }

//   console.log(`Updated table "${tableKey}":`, table);
// };





const steps = ref([
  {
    id: 1,
    label: "About Form",
    stepno: "Step 1",
    icon: "bi bi-info-circle",
  },
  {
    id: 2,
    label: "Fields & Workflow",
    stepno: "Step 2",
    icon: "bi bi-question-circle",
  },
  // {
  //     id: 3,
  //     label: "Preview & Save",
  //     stepno: "Step 3",
  //     icon: "ri-checkbox-circle-line",
  // },
]);

const childfield = [
  {
    label: "Text",
    type: "Data",
  },
  {
    label: "Number",
    type: "Int",
  },
  {
    label: "Attach",
    type: "Attach",
  },
  {
    label: "Date",
    type: "Date",
  },
  {
    label: "Datetime",
    type: "Datetime",
  },
];
const fieldTypes = [
  {
    label: "Text",
    type: "Data",
  },
  // {
  //   label: "Number",
  //   type: "Int",
  // },
  {
    label: "Attach",
    type: "Attach",
  },
  {
    label: "Phone",
    type: "Phone",
  },
  {
    label: "Time",
    type: "Time",
  },
  // {
  //   label: "Table",
  //   type: "Table",
  // },
  {
    label: "TextArea",
    type: "Text",
  },
  {
    label: "Date",
    type: "Date",
  },
  {
    label: "Datetime",
    type: "Datetime",
  },
  // {
  //     label: "Check",
  //     type: "Check",
  // },
  // {
  //     label: "Radio",
  //     type: "radio",
  // },
  {
    label: "Select",
    type: "Select",
  },
  {
    label: "MultiSelect",
    type: "Small Text",
  },
  // {
  //     label: "Signature",
  //     type: "Signature",
  // },
];
const SELECT_ALL = "Select All"; // Special option for "Select All"

// Computed property to include "Select All" at the top of the dropdown
const filteredOptions = computed(() => [SELECT_ALL, ...formOptions.value]);

// Compute formatted selection text
const formattedSelection = computed(() => {
  const selected = filterObj.value.accessible_departments;

  if (selected.includes(SELECT_ALL)) return "All Selected";
  if (selected.length > 1) {
    return `${selected[0]}.. +${selected.length - 1} more selected`;
  }
  return selected.join(", ");
});

// Check if an option should be checked
const isChecked = (option) => {
  if (option === SELECT_ALL) {
    return filterObj.value.accessible_departments.length === formOptions.value.length;
  }
  return filterObj.value.accessible_departments.includes(option);
};

// Toggle selection for an option
const toggleOption = (option, event) => {
  if (option === SELECT_ALL) {
    if (event.target.checked) {
      //  Select all options immediately
      filterObj.value.accessible_departments = [...formOptions.value];
    } else {
      // Unselect all options
      filterObj.value.accessible_departments = [];
    }
  } else {
    if (event.target.checked) {
      filterObj.value.accessible_departments.push(option);
    } else {
      filterObj.value.accessible_departments = filterObj.value.accessible_departments.filter(
        (item) => item !== option
      );
    }

    // If all options are selected, add "Select All"
    if (filterObj.value.accessible_departments.length === formOptions.value.length) {
      filterObj.value.accessible_departments = [...formOptions.value];
    } else {
      // Remove "Select All" if not all options are selected
      filterObj.value.accessible_departments = filterObj.value.accessible_departments.filter(
        (item) => item !== SELECT_ALL
      );
    }
  }
};

const isAllSelected = computed({
  get() {
    return (
      DesignationList.value.length > 0 &&
      DesignationList.value.every((item) => designationValue.value.includes(item))
    );
  },
  set(value) {
    if (value) {
      designationValue.value = [...DesignationList.value];
    } else {
      designationValue.value = [];
    }
  },
});

console;
function handleSingleSelect() {
  if (!isAllSelected.value && designationValue.value.length === 1) {
    // console.log("Selected only one designation:", designationValue.value[0]);
  }
}

function addDesignationBtn() {
  const block = blockArr[selectedBlockIndex.value];

  if (!block || !block.sections) {
    console.error("Error: Invalid block or sections not found.");
    return; // Prevent further execution
  }

  let xyz = {
    type: selectedBlockIndex.value == 0 ? "requestor" : "approver",
    roles: designationValue.value,
    fields: block.sections.flatMap(extractFieldnames),
    idx: selectedBlockIndex.value,
  };

  // workflowSetup.push(xyz)
  if (selectedBlockIndex.value !== 0) {
    xyz.view_only_reportee = ViewOnlyReportee.value === true ? 1 : 0;
  }
  console.log(xyz);

  const existingIndex = workflowSetup.findIndex((item) => item.idx === xyz.idx);
  if (existingIndex !== -1) {
    workflowSetup[existingIndex] = xyz;
  } else {
    workflowSetup.push(xyz);
    // console.log(workflowSetup, workflowSetup.length, "--workflowSetup---");
  }

  add_Wf_roles_setup();
}

// const getWorkflowSetup = (blockIndex) => {
//     return workflowSetup.find((setup) => setup.idx === blockIndex);
// };

function getWorkflowSetup(blockIndex) {
  return workflowSetup.find((setup) => setup.idx === blockIndex) || { roles: [] };
}

// Initialize `designationValue` based on the roles for the given block index
function initializeDesignationValue(blockIndex) {
  const rolesForBlock = getWorkflowSetup(blockIndex).roles || [];
  designationValue.value = [...rolesForBlock]; // Reset designationValue to match only roles for the current block
}

const AddDesignCanvas = (idx) => {
  // console.log(idx, "---clicked idex", selectedBlockIndex.value);
  if (filterObj.value.accessible_departments.length) {
    designationData(filterObj.value.accessible_departments);
  }
  selectedBlockIndex.value = idx;
  initializeDesignationValue(idx);
};
const userlist = ref([]);
function designationData(departments) {
  const filters = [];

  if (Array.isArray(departments) && departments.length > 0) {
    filters.push(["ezy_departments", "in", departments]);
  }

  axiosInstance
    .get(apis.resource + doctypes.WFRoleMatrix + `/${filterObj.value.business_unit}`)
    .then((res) => {
      if (res.data) {
        // console.log(res.data.users, "wf role matrix");
        userlist.value = res.data.users;

        DesignationList.value = [
          ...new Set(res.data.users.map((user) => user.role_name)),
        ];
      }
    })
    .catch((error) => {
      console.error("Error fetching designations data:", error);
    });
}
function add_Wf_roles_setup() {
  axiosInstance
    .post(apis.add_roles_WF, {
      workflow_setup: workflowSetup,
      doctype: filterObj.value.form_short_name,
      business_unit: filterObj.value.business_unit,
    })
    .then((res) => {
      console.log(res);

      if (selectedBlockIndex.value == 0) {
        toast.success("Requestor Added", {
          autoClose: 1000,
          transition: "zoom",
        });
      } else {
        toast.success(`Approver-${selectedBlockIndex.value} Added`, {
          autoClose: 1000,
          transition: "zoom",
        });
      }
    });
}

const selectedData = ref({
  routepath: route.query.routepath,

});
function cancelForm() {
  router.push({
    path: selectedData.value.routepath,
  });

}

function clearForm() {
  filterObj.value.form_name = ''
  filterObj.value.form_short_name = ''
  filterObj.value.owner_of_the_form = ''
  filterObj.value.business_unit = ''
  filterObj.value.form_category = ''
  filterObj.value.accessible_departments = []



}
const handleStepClick = (stepId) => {
  if (isNextDisabled.value) {
    toast.error("Please check all required fields before proceeding.", {
      autoClose: 2000,
      transition: "zoom",
    });
    return;
  }

  if (stepId < activeStep.value) {
    prevStep(stepId);
  } else if (stepId > activeStep.value) {
    nextStep(stepId);
  }
};

const nextStep = () => {
  if (isNextDisabled.value) {
    toast.error("Please check all required fields before proceeding.", {
      autoClose: 2000,
      transition: "zoom",
    });
    return;
  }

  if (activeStep.value < 3) {
    activeStep.value += 1;
  }
};

const prevStep = () => {
  if (activeStep.value > 1) {
    activeStep.value -= 1;
  }
};
const returTables = ref([])
// Get form by ID
function getFormData() {
  axiosInstance
    .get(apis.resource + doctypes.EzyFormDefinitions + `/${paramId.value}`)
    .then((res) => {
      let res_data = res?.data;
      if (res_data) {
        if (res_data.accessible_departments) {
          res_data.accessible_departments = res_data.accessible_departments.split(",");
        }
        filterObj.value = {
          ...filterObj.value,
          ...res_data,
          owner_of_the_form:
            res_data.owner_of_the_form || filterObj.value.owner_of_the_form || "",
        };

        // console.log(res.data, "7777777777777777");
        const parsedFormJson = JSON.parse(res.data?.form_json);
        wrkAfterGetData.value = parsedFormJson.workflow;
        // console.log(parsedFormJson.workflow, "parsedFormJson");
        tableName.value = parsedFormJson.fields.filter(
          (field) => field.fieldtype === "Table"
        );
        returTables.value = parsedFormJson.fields.filter(
          (field) => field.fieldtype === "Table"
        );


        // let structuredArr = rebuildToStructuredArray((JSON.parse(res_data?.form_json?.fields).fields)?.replace(/\\\"/g, '"'))
        let structuredArr = rebuildToStructuredArray(
          JSON.parse(res_data?.form_json).fields
        );
        childtableHeaders.value = JSON.parse(res.data.form_json).child_table_fields;

        childTables.value = []
        tableFieldsCache.value = []

        // workflowSetup.push(JSON.parse(res_data?.form_json).workflow)

        structuredArr.forEach((item, index) => {
          blockArr.push(item);
        });

        JSON.parse(res_data?.form_json).workflow.forEach((item, index) => {
          workflowSetup.push(item);
        });
      }
    })
    .catch((error) => {
      console.error("Error fetching  data:", error);
    });
}


function deptData() {
  const queryParams = {
    fields: JSON.stringify(["*"]),
  };

  axiosInstance
    .get(apis.resource + doctypes.departments, { params: queryParams })
    .then((res) => {
      if (res?.data?.length) {
        // Mapping department names
        // label="name" track-by="name"
        OwnerOfTheFormData.value = res.data.map((dept) => dept.name);
        formOptions.value = res.data.map((dept) => dept.name); // Store the full data for accessible departments
        // departments.value = res.data.map(item => item.category)
      }
    })
    .catch((error) => {
      console.error("Error fetching department data:", error);
    });
}
watch(
  () => filterObj.value.owner_of_the_form,
  (newVal) => {
    if (newVal) {
      OwnerOftheForm(newVal); // Fetch categories when owner_of_the_form changes
    }
  }
);

function OwnerOftheForm(newVal) {
  if (newVal && typeof newVal === "string" && newVal.trim() !== "") {
    // console.log("Owner Of The Form Changed:", newVal);
    categoriesData(newVal);
  }
}

function categoriesData(newVal) {
  axiosInstance
    .get(apis.resource + doctypes.departments + `/${newVal}`)
    .then((res) => {
      if (res?.data?.ezy_departments_items) {
        departments.value = res.data.ezy_departments_items.map((item) => item.category);
      }
    })
    .catch((error) => {
      console.error("Error fetching categories data:", error);
    });
}

function formData(status) {
  // console.log(blockArr, "blockarray");

  let fields = extractFieldsWithBreaks(blockArr);

  if (tableFieldsCache.value.length) {
    // Merge stored table fields
    fields = [...fields, ...tableFieldsCache.value];
  }

  if (returTables.value && returTables.value.length) {
    // Append child table headers instead of replacing
    fields = [...fields, ...returTables.value];
  }
  const dataObj = {
    ...filterObj.value,
    fields,
    doctype: doctypes.EzyFormDefinitions,
    workflow_setup: workflowSetup,
    form_status: status === "save" ? "Created" : "Draft",
  };

  dataObj.accessible_departments = dataObj.accessible_departments.toString();
  // console.log(dataObj, "---data obj");
  axiosInstance
    .post(apis.savedata, dataObj)
    .then((res) => {
      if (res && res.message && res.message.message) {
        // tableFieldsCache.value = [];
        router.push({
          params: { paramid: res.message.message },
        });
        paramId.value = res.message.message;
        // paramId = res.message.message;

        if (paramId && paramId !== "new") {
          blockArr.splice(0, blockArr.length);
          getFormData();
        }
        // console.log(paramId.value, "Updated paramId");

        if (workflowSetup.length < blockArr.length) {
          toast.info("Add Workflow", {
            autoClose: 2000,
            transition: "zoom",
          });
        } else {
          toast.success("Form Created Successfully!", {
            autoClose: 2000,
            transition: "zoom",
            onClose: () => {
              if (status === "save") {
                router.push({ name: "Created" });
              } else if (status === "draft") {
                router.push({ name: "Draft" });
              }
            },
          });
        }
      } else {
        console.error("Invalid response structure:", res);
      }
    })
    .catch((error) => {
      console.error("Error saving form data:", error);
    });
}
// setTimeout(() => {
//   console.log(blockArr.length, workflowSetup.length, "length");

//   if (workflowSetup.length < blockArr.length) {
//     // ✅ If workflows are missing, show error toast
//     const missingWorkflows = blockArr.length - workflowSetup.length;
//     toast.error(`${missingWorkflows} more workflow(s) left to add.`, {
//       autoClose: 2000,
//       transition: "zoom",
//     });
//   } else {
//     // ✅ If all workflows are added, show success toast
//     toast.success("Form Created Successfully!", {
//       autoClose: 2000,
//       transition: "zoom",
//       onClose: () => {
//         // ✅ Route only after success toast disappears
//         if (status === "save") {
//           router.push({ name: "Created" });
//         } else if (status === "draft") {
//           router.push({ name: "Draft" });
//         }
//       },
//     });
//   }
// }, 2000);

const mainBlockRef = ref("");
const addBlock = () => {
  const blockIndex = blockArr.length; // Get current length before adding new block

  const newBlock = {
    label: blockIndex === 0 ? "requestor" : `approver-${blockIndex}`,
    parent: `${businessUnit.value?.value}-${filterObj.value?.form_short_name}`,
    sections: [
      {
        label: "",
        parent: `${businessUnit.value.value}-${filterObj.value.form_short_name}`,
        rows:
          blockIndex === 0
            ? [
              {
                label: `row_0_0_${blockIndex}`,
                columns: [
                  {
                    label: "", // First column with "Requested by"
                    fields: [
                      {
                        label: "Requested by",
                        fieldtype: "Data",
                        options: "",
                        reqd: false,
                      },
                    ],
                  },
                  {
                    label: "", // Second column with "Requested On"
                    fields: [
                      {
                        label: "Requested On",
                        fieldtype: "Datetime",
                        options: "",
                        reqd: false,
                      },
                    ],
                  },
                ],
              },
              {
                label: `row_0_1_${blockIndex}`, // New row with an empty field
                columns: [
                  {
                    label: "",
                    fields: [{ label: "", fieldtype: "", options: "", reqd: false, description: "" }],
                  },
                ],
              },
            ]
            : [
              {
                label: `row_0_0_${blockIndex}`,
                columns: [
                  {
                    label: "", // First column with "Approver" & "Approved By"
                    fields: [
                      {
                        label: "Approver",
                        fieldtype: "Data",
                        options: "",
                        reqd: false,
                      },
                      {
                        label: "Approved By",
                        fieldtype: "Attach",
                        options: "",
                        reqd: false,
                      },
                    ],
                  },
                  {
                    label: "", // Second column with "Approved On"
                    fields: [
                      {
                        label: "Approved On",
                        fieldtype: "Datetime",
                        options: "",
                        reqd: false,
                      },
                    ],
                  },
                ],
              },
            ],
      },
    ],
  };

  blockArr.push(newBlock);
  nextTick(() => {
    if (mainBlockRef.value) {
      mainBlockRef.value.scrollTo({
        top: mainBlockRef.value.scrollHeight,
        behavior: "smooth",
      });
    }
  });
};
// const addBlock = () => {
//   const blockIndex = blockArr.length; // Get current length before adding new block

//   const newBlock = {
//     label: blockIndex === 0 ? "requestor" : `approver-${blockIndex}`,
//     parent: `${businessUnit.value?.value}-${filterObj.value?.form_short_name}`,
//     sections: [
//       {
//         label: "",
//         parent: `${businessUnit.value.value}-${filterObj.value.form_short_name}`,
//         rows: [
//           {
//             label: `row_0_0_${blockIndex}`,
//             columns:
//               blockIndex === 0
//                 ? [
//                   {
//                     label: "", // No extra empty column for the requestor block
//                     fields: [{ label: "", fieldtype: "", options: "", reqd: false }],
//                   },
//                 ]
//                 : [
//                   {
//                     label: "", // First column with "Approver" & "Approved By"
//                     fields: [
//                       {
//                         label: "Approver",
//                         fieldtype: "Data",
//                         options: "",
//                         reqd: false,
//                       },
//                       {
//                         label: "Approved By",
//                         fieldtype: "Attach",
//                         options: "",
//                         reqd: false,
//                       },
//                     ],
//                   },
//                   {
//                     label: "", // Second column with "Approved On"
//                     fields: [
//                       {
//                         label: "Approved On",
//                         fieldtype: "Datetime",
//                         options: "",
//                         reqd: false,
//                       },
//                     ],
//                   },
//                 ],
//           },
//         ],
//       },
//     ],
//   };

//   blockArr.push(newBlock);
//   nextTick(() => {
//     if (mainBlockRef.value) {
//       mainBlockRef.value.scrollTo({
//         top: mainBlockRef.value.scrollHeight,
//         behavior: "smooth",
//       });
//     }
//   });
// };

// function to delete block
const removeBlock = (blockIndex) => {
  let item = blockArr[blockIndex];
  if (item.parent) deleted_items.push(item);
  blockArr.splice(blockIndex, 1);
};

// Function to add a new section with a default column
const addSection = (blockIndex) => {
  let sectionIndex = blockArr[blockIndex].sections.length;
  // let rowIndex = blockArr[blockIndex].sections;

  blockArr[blockIndex].sections.push({
    label: "",
    parent: `${businessUnit.value.value}-${filterObj.value.form_short_name}`,
    rows: [
      {
        label: `row_0_${sectionIndex}_${blockIndex}`,
        columns: [
          {
            label: "",
            fields: [
              {
                label: "",
                fieldtype: "",
                // value: ref(""), // Keeping the value as a ref for reactivity
                options: "",
                reqd: false,
              },
            ], // Initialize with an empty fields array
          },
        ],
      },
    ],
  });
  // nextTick(() => {
  //   if (mainBlockRef.value) {
  //     mainBlockRef.value.scrollTo({
  //       top: mainBlockRef.value.scrollHeight,
  //       behavior: "smooth",
  //     });
  //   }
  // });
};
// Function to remove a section
const removeSection = (blockIndex, sectionIndex) => {
  let item = blockArr[blockIndex].sections[sectionIndex];
  if (item.parent) deleted_items.push(item);
  blockArr[blockIndex].sections.splice(sectionIndex, 1);
  // toast.success("Section removed", { autoClose: 500 })
};

// const addRow = (blockIndex, sectionIndex) => {
//   const rowIndex = blockArr[blockIndex].sections[sectionIndex].rows.length; // Get the current row index
//   const rowSuffix = getRowSuffix(rowIndex);

//   blockArr[blockIndex].sections[sectionIndex].rows.push({
//     label: `row_${rowIndex}_${sectionIndex}_${blockIndex}`,
//     columns: [
//       {
//         fields: [
//           {
//             label: "",
//             fieldtype: "",
//             // value: ref(""), // Keeping the value as a ref for reactivity
//             options: "",
//             reqd: false,
//           },
//         ], // Initialize with an empty fields array
//       },
//     ],
//   });
// };

// const removeRow = (blockIndex, sectionIndex, rowIndex) => {
//   let item = blockArr[blockIndex].sections[sectionIndex].rows[rowIndex];
//   if (item.parent) deleted_items.push(item);
//   blockArr[blockIndex].sections[sectionIndex].rows.splice(rowIndex, 1);
//   // toast.success("Row removed", { autoClose: 500 })
// };

// Function to add a new column inside a section
const addColumn = (blockIndex, sectionIndex, rowIndex) => {
  blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns.push({
    label: "",
    fields: [
      {
        label: "",
        fieldtype: "",
        // value: ref(""), // Keeping the value as a ref for reactivity
        options: "",
        reqd: false,
      },
    ],
  });
};

// Function to remove a column inside a section
const removeColumn = (blockIndex, sectionIndex, rowIndex, columnIndex) => {
  let item =
    blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex];
  if (item.parent) deleted_items.push(item);
  blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns.splice(
    columnIndex,
    1
  );
  // toast.success("Column removed", { autoClose: 500 })
};

// Function to add a new field inside a column
const addField = (blockIndex, sectionIndex, rowIndex, columnIndex) => {
  blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[
    columnIndex
  ].fields.push({
    label: "",
    fieldtype: "",
    // value: ref(""), // Keeping the value as a ref for reactivity
    options: "",
    reqd: false,
  });

  // nextTick(() => {
  //   if (mainBlockRef.value) {
  //     mainBlockRef.value.scrollTo({
  //       top: mainBlockRef.value.scrollHeight,
  //       behavior: "smooth",
  //     });
  //   }
  // });
};

// Function to remove a field inside a column
const removeField = (blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex) => {
  let item =
    blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex]
      .fields[fieldIndex];
  if (item.parent) deleted_items.push(item);
  blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[
    columnIndex
  ].fields.splice(fieldIndex, 1);
  // toast.success("Field removed", { autoClose: 500 })
};

// Function to copy a field and add it below the original field inside a column
const copyField = (blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex) => {
  // Get the field to copy
  const fieldToCopy =
    blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex]
      .fields[fieldIndex];

  // Create a shallow copy of the field
  const newField = { ...fieldToCopy };

  // Optionally, you can modify some properties (e.g., rename the field)
  newField.name = `${fieldToCopy.name} Name the field`;

  // Insert the copied field after the original one
  blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[
    columnIndex
  ].fields.splice(fieldIndex + 1, 0, newField);
};
// Handle the change of field type to display the correct input
const onFieldTypeChange = (
  blockIndex,
  sectionIndex,
  rowIndex,
  columnIndex,
  fieldIndex
) => {
  const checkFieldType = addErrorMessagesToStructuredArray(blockArr);
  blockArr.splice(0, blockArr.length, ...checkFieldType);

  let fieldType =
    blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex]
      .fields[fieldIndex].fieldtype;
  if (
    fieldType !== "Check" ||
    fieldType !== "Select" ||
    fieldType !== "radio" ||
    fieldType !== "multiselect"
  ) {
    blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[
      columnIndex
    ].fields[fieldIndex].options = "";
  }
  // if (fieldType === "Table") {
  //     processFields();
  // }
  // const field =
  //     sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex];
  // Handle additional logic for field type change if needed

  // const xyz = extractFieldsWithBreaks(sections)
};


// const hasDuplicates = (array) => new Set(array).size !== array.length;


const restrictedLabels = [
  "name", "parent", "creation", "owner", "modified", "modified_by",
  "parentfield", "parenttype", "file_list", "flags", "docstatus"
].map(label => label.toLowerCase().trim());

const excludedLabels = ["Approver", "Approved on", "Approved By"].map(label => label.toLowerCase().trim());

function isRestricted(label) {
  return restrictedLabels.includes(label?.trim().toLowerCase());
}

function hasInvalidCharacters(label) {
  return /[^a-zA-Z0-9 _]/.test(label) || label.includes('"') || label.includes("'");
}

function getAllLabels(blockArr) {
  return blockArr.flatMap(block => [
    block.label?.trim().toLowerCase(),
    ...block.sections.flatMap(section => [
      section.label?.trim().toLowerCase(),
      ...section.rows.flatMap(row =>
        row.columns.flatMap(column => [
          column.label?.trim().toLowerCase(),
          ...column.fields.map(field => field.label?.trim().toLowerCase())
        ])
      )
    ])
  ]).filter(label => label !== "" && !excludedLabels.includes(label));
}

function handleFieldChange(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex) {
  const allLabels = getAllLabels(blockArr);
  const duplicateLabels = allLabels.filter((label, index, arr) => arr.indexOf(label) !== index);

  const checkFieldType = addErrorMessagesToStructuredArray(blockArr);
  blockArr.splice(0, blockArr.length, ...checkFieldType);

  function validateLabel(label, errorPath) {
    if (isRestricted(label)) {
      errorPath.errorMsg = "Entered label is restricted";
    } else if (hasInvalidCharacters(label)) {
      errorPath.errorMsg = "Label should not contain special characters, double quotes (\") or single quotes (')";
    } else {
      errorPath.errorMsg = duplicateLabels.includes(label.trim().toLowerCase()) ? "Duplicate Label Name" : "";
    }
  }

  // Validate Field
  if (fieldIndex !== undefined) {
    validateLabel(
      blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex].label,
      blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex]
    );
  }

  // Validate Column
  if (fieldIndex === undefined && columnIndex !== undefined) {
    validateLabel(
      blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].label,
      blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex]
    );
  }

  // Validate Section
  if (columnIndex === undefined && fieldIndex === undefined) {
    validateLabel(
      blockArr[blockIndex].sections[sectionIndex].label,
      blockArr[blockIndex].sections[sectionIndex]
    );
  }
}
// function handleFieldChange(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex) {
//   const excludedLabels = ["Approver", "Approved on", "Approved By"].map((label) =>
//     label.toLowerCase().trim()
//   );

//   const restrictedLabels = [
//     "name",
//     "parent",
//     "creation",
//     "owner",
//     "modified",
//     "modified_by",
//     "parentfield",
//     "parenttype",
//     "file_list",
//     "flags",
//     "docstatus",
//   ].map((label) => label.toLowerCase().trim());

//   // Function to check for duplicates
//   const hasDuplicates = (array) => new Set(array).size !== array.length;

//   // Extract all labels except excluded ones
//   const flatArr = blockArr
//     .flatMap(extractfieldlabels)
//     .map((label) => label.trim().toLowerCase())
//     .filter((label) => label !== "" && !excludedLabels.includes(label));


//   function shouldSetError(fieldLabel) {
//     const normalizedLabel = fieldLabel?.trim().toLowerCase();
//     if (!normalizedLabel || excludedLabels.includes(normalizedLabel)) return false;

//     // Count occurrences of the label in `flatArr`
//     const occurrences = flatArr.filter((label) => label === normalizedLabel).length;

//     return occurrences > 1; // True if duplicate exists
//   }

//   function isRestricted(fieldLabel) {
//     return restrictedLabels.includes(fieldLabel?.trim().toLowerCase());
//   }

//   function hasInvalidCharacter(fieldLabel) {
//     return fieldLabel.includes('"'); // Check if label contains double quotes
//   }

//   if (
//     fieldIndex !== undefined &&
//     fieldIndex >= 0 &&
//     columnIndex !== undefined &&
//     columnIndex >= 0 &&
//     sectionIndex !== undefined
//   ) {
//     const fieldLabel =
//       blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex]
//         .fields[fieldIndex].label;

//     if (isRestricted(fieldLabel)) {
//       blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[
//         fieldIndex
//       ].errorMsg = "Entered label is restricted";
//     } else if (hasInvalidCharacter(fieldLabel)) {
//       blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[
//         fieldIndex
//       ].errorMsg = 'Label should not contain double quotes (")';
//     } else {
//       blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[
//         fieldIndex
//       ].errorMsg = shouldSetError(fieldLabel) ? "Duplicate Label Name" : "";
//     }
//   }

//   if (
//     fieldIndex === undefined &&
//     columnIndex !== undefined &&
//     columnIndex >= 0 &&
//     sectionIndex !== undefined
//   ) {
//     const columnLabel =
//       blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].label;

//     if (isRestricted(columnLabel)) {
//       blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].errorMsg =
//         "Entered label is restricted";
//     } else if (hasInvalidCharacter(columnLabel)) {
//       blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].errorMsg =
//         'Label should not contain double quotes (")';
//     } else {
//       blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].errorMsg =
//         shouldSetError(columnLabel) ? "Duplicate Label Name in Column" : "";
//     }
//   }

//   if (columnIndex === undefined && fieldIndex === undefined && sectionIndex !== undefined) {
//     const sectionLabel = blockArr[blockIndex].sections[sectionIndex].label;

//     if (isRestricted(sectionLabel)) {
//       blockArr[blockIndex].sections[sectionIndex].errorMsg = "Entered label is restricted";
//     } else if (hasInvalidCharacter(sectionLabel)) {
//       blockArr[blockIndex].sections[sectionIndex].errorMsg =
//         'Label should not contain double quotes (")';
//     } else {
//       blockArr[blockIndex].sections[sectionIndex].errorMsg =
//         shouldSetError(sectionLabel) ? "Duplicate Label Name in Section" : "";
//     }
//   }
// }


const hasErrors = computed(() => {
  function checkFieldErrors(obj) {
    if (!obj || typeof obj !== "object") return false;

    // Check for errors in fieldtype, error messages, or empty options for select types
    if (
      ("fieldtype" in obj && obj.fieldtype === "") ||
      ("error" in obj && obj.error) ||
      ("errorMsg" in obj && obj.errorMsg) ||
      (["Select", "Table MultiSelect", "Check"].includes(obj.fieldtype) &&
        (!obj.options || obj.options.trim() === ""))
    ) {
      return true;
    }

    if (Array.isArray(obj)) {
      return obj.some(checkFieldErrors);
    }

    return Object.values(obj).some(checkFieldErrors);
  }

  return checkFieldErrors(blockArr);
});

const isNextDisabled = computed(() => {
  return (
    formNameError.value.length > 0 ||
    formShortNameError.value.length > 0 ||
    !filterObj.value.form_category ||
    !filterObj.value.owner_of_the_form ||
    filterObj.value.accessible_departments.length === 0
  );
});

const isPreviewVisible = computed(() => {
  return blockArr.some((block) =>
    block.sections.some((section) =>
      section.rows.some((row) =>
        row.columns.some((column) =>
          column.fields.some((field) => field.label && field.fieldtype)
        )
      )
    )
  );
});
//spaces removed version
function handleInputChange(event, fieldType) {
  let inputValue = event.target.value.trim().replace(/\s+/g, "");

  // Check if the first character is a number
  if (/^\d/.test(inputValue)) {
    if (fieldType === "form_short_name") {
      formShortNameError.value = "First character must be a letter";
    }
    return;
  } else {
    formShortNameError.value = ""; // Clear error if input is valid
  }

  // Check for special characters (allow only letters and numbers)
  if (/[^a-zA-Z0-9&]/.test(inputValue)) {
    if (fieldType === "form_name") {
      formNameError.value = "Special characters are not allowed";
    } else if (fieldType === "form_short_name") {
      formShortNameError.value = "Special characters are not allowed";
    }
    return;
  } else {
    if (fieldType === "form_name") {
      formNameError.value = "";
    } else if (fieldType === "form_short_name") {
      formShortNameError.value = "";
    }
  }

  // Set filter based on fieldType
  const filters = [[fieldType, "like", `%${inputValue}%`]];
  const queryParams = {
    fields: JSON.stringify(["*"]),
    filters: JSON.stringify(filters),
  };

  axiosInstance
    .get(`${apis.resource}${doctypes.EzyFormDefinitions}`, {
      params: queryParams,
    })
    .then((res) => {
      ezyFormsData.value = res.data;

      // Check for duplicates
      if (fieldType === "form_name") {
        formNameError.value =
          inputValue &&
            ezyFormsData.value.some(
              (item) =>
                item.form_name &&
                item.form_name.replace(/\s+/g, "").toLowerCase() ===
                inputValue.toLowerCase()
            )
            ? "Name already exists"
            : "";
      } else if (fieldType === "form_short_name") {
        formShortNameError.value =
          inputValue &&
            ezyFormsData.value.some(
              (item) =>
                item.form_short_name &&
                item.form_short_name.replace(/\s+/g, "").toLowerCase() ===
                inputValue.toLowerCase()
            )
            ? "Short name already exists"
            : "";
      }
    })
    .catch((error) => {
      console.error("Error fetching ezyForms data:", error);
      if (fieldType === "form_name") formNameError.value = "";
      else if (fieldType === "form_short_name") formShortNameError.value = "";
    });
}

const getRowSuffix = (index) => {
  if (index === 0) {
    return "1st row";
  } else if (index === 1) {
    return "2nd row";
  } else if (index === 2) {
    return "3rd row";
  } else {
    return `${index + 1}th row`;
  }
};
const selectedform = ref([]);
// Trigger the creation of form and show the preview
const previewForm = () => {
  if (blockArr.length) {
    selectedform.value = blockArr;
    const modal = new bootstrap.Modal(document.getElementById("formViewModal")); // raise a modal
    modal.show();
  }
};

function delete_form_items_fields() {
  axiosInstance
    .post(apis.delete_form_items, {
      deleted_fields: deleted_items.flatMap(extractFieldnames),
      doctype: paramId,
    })
    .then((res) => {
      if (res?.message?.success) {
        // return res;
        formData();
      }
    });
}

async function saveFormData(type) {
  // Check for errors
  if (hasErrors.value) {
    toast.error("Please fix the errors before proceeding.");
    return;
  }

  let data = deleted_items.flatMap(extractFieldnames);

  if (paramId != undefined && paramId != null && paramId != "new" && data.length) {
    delete_form_items_fields();
  } else {
    formData(type);
  }
}

const hasDuplicates = (array) => new Set(array).size !== array.length;
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style lang="scss" scoped>
.dynamic_fied {
  position: relative;
}

.FieldcopyRemove {
  position: absolute;
  top: 0;
  right: 0;
}

.inputHeight {
  height: 36px;
  // min-width: 350px;
  padding-left: 4px !important;
}

/* @import '@vueform/multiselect/themes/default.css'; */
.formHeight input {
  border-radius: 3px !important;
}

.add_designationHeader {
  box-shadow: 0px 4px 4px 0px #0000000d;
  font-size: 14px;
}

.ErrorMsg {
  font-size: 11px;
}

.SelectallDesignation {
  color: #1b14df;
}

.CancelNdSave {
  background-color: #fafafa;
  position: sticky;
  top: 0;
  z-index: 1;
}

.stepsDiv {
  margin-top: 25px;
}

.steps-sticky-div {
  position: sticky;
  z-index: 1;
  top: 30px;
}

input {
  font-size: 13px !important;

  // height: 35px;
}

.rownames {
  opacity: 0;
}

.formsticky {
  position: sticky;
  top: 50px;
  z-index: 100;
  background: white;
}

.dynamicSection {
  border: 1px solid #eeeeee;
  margin-bottom: 20px;
  border-radius: 7px;
  background-color: #f5f5f5;
  position: relative;
  transition: all 2s ease-in;
  margin: 8px;
  padding: 10px;
}

.dynamicColumn {
  // border: 1px solid #cccccc;
  border: 1.5px dashed #cccccc;
  border-radius: 10px;
  margin: 5px;
  margin-top: 0;
  position: relative;
  background-color: #ffffff;
}

// .dynamicColumn {
//     border: 2px dashed #cccccc;
//     border-radius: 7px;
//     margin: 3px 3px 10px 3px;
//     background-color: #ffffff;
//     padding: 0;
//     padding-bottom: 5px;

// }

.dynamicColumn:hover {
  border: 1px solid rgb(119, 119, 119);
}

.column_name {
  /* border-bottom: 1px solid #f1f1f1; */
  padding: 1px 3px;
}

.main-section {
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
  border: 1px solid rgb(236, 236, 236);
  margin: 10px;
  position: relative;
}

.border-less-input {
  border: 0;
  background: transparent;
  padding-left: 10px;
}

.italic-style {
  font-style: italic;
}

.border-less-input:focus {
  border: 0;
  background: transparent;
  outline: 0;
}

.field-border {
  /* border: 1px solid rgb(221, 221, 221); */
  border-radius: 10px;
  // margin: 0px 10px 5px 10px;
  background-color: #fafafa;
  position: relative;
}

.preview-section {
  background-color: #eeeeee;
  // overflow-y: scroll;
  // overflow-x: hidden;
  // height: 40vh;
  padding: 8px;
  border-radius: 10px;
}

input[type="checkbox"] {
  margin-left: 5px;
  height: 15px;
}

has context menu .form-container {
  /* max-width: 900px; */
  margin: 0 auto;
  padding-top: 20px;

  border-radius: 8px;
  background-color: #fff;
}

.form-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.steps {
  /* display: flex;
    justify-content: space-evenly; */
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
  position: relative;
}

.steps li {
  padding: 25px 20px;
  font-size: 14px;
  font-weight: 400;
  cursor: pointer;
  transition: 0.3s all ease;
  width: 100%;
  position: relative;
}

.steps li.active {
  color: #1b14df;
  font-weight: bold;
}

.completedStepIcon {
  color: #1b14df;
  font-size: 14px;
}

.steps li.completed {
  color: #000;
  font-size: 14px;
  font-weight: 400;
  font-weight: normal;
  opacity: 0.7;
}

.steps li.completed::after {
  content: "";
  display: block;
  width: 1px;
  height: 40px;
  background-color: #d9d9d9;
  /* Customize the color */
  position: absolute;
  border-radius: 2px;
  left: 25px;
  /* Adjust position relative to the icon */
  top: 75%;
  /* Position the line below the step */
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 5px;
  font-weight: 500;
  margin-top: 5px;
  font-size: 13px;
}

input,
select {
  /* width: 100%; */
  // padding: 10px;
  border: 1px solid #ccc;
}

.searchSelect {
  border-radius: 10px !important;
}

.form-footer {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.backTo {
  color: #000;
  border: none;
  border-bottom: 2px solid black;
  background: transparent;
  padding-bottom: 0px;
  height: 25px;
}

.Savedraft {
  color: #000;
  border: none;
  background: transparent;
}

.NextSave {
  padding: 6px 12px;
  border: none;
  background-color: #000;
  color: #fff;
  cursor: pointer;
  border-radius: 4px;
}

.NextSave:hover {
  background-color: #444;
}

.saveForm {
  padding: 6px 12px;
  border: none;
  background-color: #000;
  color: #fff;
  cursor: pointer;
  border-radius: 4px;
  margin-top: 20px;
}

.saveForm:hover {
  background-color: #000;
}

.stepperbackground {
  background-color: #eeeeee;
  height: 50px;
  border-radius: 7px;
  position: sticky;
  z-index: 1;
  top: 36px;
}

// .previewInputHeight {
//     height: 35px;
// }

.addField {
  font-size: 12px;
  font-weight: 400;
}

.addRow {
  // border: 1px solid #ccc;
  font-size: 12px;
  font-weight: 400;
  border-radius: 6px;
  background-color: transparent;
  border: 1px solid #ccc;
}

.copyIcon {
  cursor: pointer;
}

.deleteSection {
  color: #fe212e;

  font-weight: 400;
}

.deleteBlock {
  color: #fe212e;
  font-weight: 400;
}

.designationBtn {
  color: #1b14df;
  font-size: 13px;
  font-weight: 400;
  background-color: transparent;
  border: none;
}

.designationList {
  border: 1px solid #eeeeee;
  font-size: 14px;
  font-weight: 400;
  padding: 15px 5px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  margin-bottom: 4px;
}

.designationCheckBox {
  font-size: 20px !important;
}

.designationCheckBox:focus {
  box-shadow: none;
}

.addingDesignations {
  font-size: 14px;
  font-weight: 600;
  /* margin-right: 30px; */
}

.Withborder {
  border: 1px solid #eeeeee;
}

.multiselect-option {
  font-size: 11px !important;
}

.multiselect {
  height: 30px !important;
  font-size: 12px !important;
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
  font-size: 11px;
}

.multiselect .multiselect__tags .multiselect__placeholder {
  font-size: 11px;
}

::v-deep(.multiselect__placeholder) {
  color: #adadad;
  display: inline-block;
  margin-bottom: 10px;
  padding-top: 2px;
  font-size: 12px !important;
}

.add-section-btn {
  position: sticky;
  bottom: 80px;
  z-index: 1;
  background-color: #ffffff;
}

.add-block-btn-div {
  position: sticky;
  bottom: 0;
  z-index: 1;
}

.background-color-white {
  background-color: #ffffff;
}

.block-level {
  margin-top: 10px;
  border: 1px solid #e5e5e5;
  border-radius: 5px;
  // padding: 5px 10px;
  background-color: #fff;
  position: relative;
}

.main-block {
  height: 80vh;
  overflow-y: scroll;
}

.section-label {
  padding: 10px 3px;
}

.formbackground-color {
  background-color: #fafafa;
  border: 1px solid #f1f1f1;
  height: 90vh;
  border-radius: 8px;
}

.requestandAppHeader {
  padding: 10px 6px;
  box-shadow: 0px 4px 4px 0px #0000000d;
}

.section_block {
  padding: 10px;
}

.border-less-input:focus {
  font-weight: 600;
}

.custom-option {
  display: flex;
  align-items: center;
  gap: 5px;
}

.custom-checkbox {
  width: 16px;
  height: 16px;
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

::v-deep(.multiselect__single) {
  font-size: 12px;
}

::v-deep(.multiselect__tags) {
  height: 32px !important;
  min-height: 32px !important;
  display: flex;
  align-items: center;
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

.disabled-btn {
  cursor: not-allowed;
  opacity: 0.6;
  /* Optional: Reduce opacity for a disabled effect */
}

.not-allowed {
  cursor: not-allowed;
  /* Show "not-allowed" cursor */
}

.role-container {
  max-width: 280px;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
  display: flex;
  align-items: center;
}

.role-label {
  font-size: 10px;
  padding-right: 4px;
}

.role-text {
  display: flex;
  max-width: 100%;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.role-names {
  display: inline-block;
  // max-width: calc(100% - 50px);
  /* Leave space for "+X more" */
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.more-count {
  color: #000;
  font-weight: 500;
  display: inline;
  cursor: pointer;
  padding-left: 5px;
}

table {
  border-collapse: collapse;
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
</style>
