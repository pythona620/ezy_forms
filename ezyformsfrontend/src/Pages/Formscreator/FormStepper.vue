<template>
  <div>
    <div class="">
      <div class="">
        <div
          class="d-flex justify-content-between align-items-center CancelNdSave my-2 py-2"
        >
          <div
            class="ps-1 my-2 d-flex align-items-center"
            @click="cancelForm()"
          >
            <h1 class="font-13 ms-3">
              <i class="bi bi-arrow-left"></i><span class="ms-2">Back</span>
            </h1>
          </div>
          <div>
            <!-- <ButtonComp class="font-13 rounded-2" name="Save as Draft"></ButtonComp> -->
            <button
              v-if="activeStep === 2 && blockArr.length"
              :disabled="hasErrors || isNextDisabled"
              :style="{ cursor: hasErrors ? 'not-allowed' : 'pointer' }"
              type="butoon"
              class="btn font-13 btn-light"
              @click="saveFormData('draft')"
            >
              <i class="bi bi-bookmark-check-fill"></i> Save As Draft
            </button>
          </div>
        </div>
        <div class="form-container p-0 container-fluid mt-1">
          <div class="row">
            <div class="col-2">
              <div class="steps-sticky-div">
                <ul class="steps">
                  <li
                    v-for="step in steps"
                    :key="step.id"
                    :class="{
                      active: activeStep === step.id,
                      completed: activeStep > step.id,
                    }"
                  >
                    <div
                      class="d-flex gap-3 align-items-center"
                      @click="handleStepClick(step.id)"
                      :class="{
                        'not-allowed':
                          isNextDisabled && activeStep + 1 === step.id,
                      }"
                    >
                      <i
                        v-if="activeStep > step.id"
                        class="ri-checkbox-circle-fill completedStepIcon"
                      ></i>
                      <i v-else :class="step.icon"></i>
                      <div class="step-text">
                        <span class="font-11">{{ step.stepno }}</span
                        ><br />
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
                      <div
                        class="stepperbackground ps-2 pe-2 m-0 d-flex justify-content-between align-items-center"
                      >
                        <h1 class="font-14 m-0" @click="cancelForm()">
                          <i class="bi bi-chevron-left"></i
                          ><span class="ms-2">Cancel Form</span>
                        </h1>
                        <h1 class="font-14 fw-bold m-0">About Form</h1>
                        <ButtonComp
                          class="btn btn-dark bg-dark text-white fw-bold font-13"
                          name="Next"
                          v-if="activeStep < 3"
                          @click="nextStep"
                        />
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
                              <FormFields
                                :disabled="
                                  paramId != undefined &&
                                  paramId != null &&
                                  paramId != 'new'
                                "
                                labeltext="Form Name"
                                class="formHeight"
                                type="text"
                                tag="input"
                                name="Value"
                                id="formName"
                                validationStar="true"
                                placeholder="Untitled Form"
                                @change="
                                  (event) =>
                                    handleInputChange(event, 'form_name')
                                "
                                v-model="filterObj.form_name"
                              />
                              <span
                                v-if="formNameError"
                                class="text-danger ErrorMsg ms-2"
                              >
                                {{ formNameError }}</span
                              >
                            </div>
                          </div>
                          <div class="mt-3">
                            <div class="">
                              <FormFields
                                :disabled="
                                  paramId != undefined &&
                                  paramId != null &&
                                  paramId != 'new'
                                "
                                labeltext="Form Short Code"
                                class="formHeight"
                                type="text"
                                tag="input"
                                name="Value"
                                id="formShortCode"
                                validationStar="true"
                                placeholder="Untitled Form"
                                @change="
                                  (event) =>
                                    handleInputChange(event, 'form_short_name')
                                "
                                v-model="filterObj.form_short_name"
                              />
                              <span
                                v-if="formShortNameError"
                                class="text-danger ErrorMsg ms-2"
                              >
                                {{ formShortNameError }}</span
                              >
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
                              <label for=""
                                >Owner Of The Form
                                <span
                                  v-if="!filterObj.owner_of_the_form"
                                  class="text-danger"
                                  >*</span
                                ></label
                              >

                              <Multiselect
                                :options="OwnerOfTheFormData"
                                @change="OwnerOftheForm"
                                v-model="filterObj.owner_of_the_form"
                                placeholder="Select Department"
                                :multiple="false"
                                class="font-11 multiselect"
                                :searchable="true"
                              />
                            </div>
                          </div>
                          <div class="mt-3">
                            <div class="">
                              <!-- <FormFields labeltext="Form Cateogry" class="mb-3" tag="select"
                                                            name="desgination" id="desgination"
                                                            placeholder="Select Cateogry" :options=departments
                                                            v-model="filterObj.form_category" /> -->

                              <label for=""
                                >Form Cateogry
                                <span
                                  v-if="!filterObj.form_category"
                                  class="text-danger"
                                  >*</span
                                ></label
                              >

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
                                <label for=""
                                  >Accessibility Departments
                                  <span
                                    v-if="
                                      !filterObj.accessible_departments.length
                                    "
                                    class="text-danger"
                                    >*</span
                                  ></label
                                >
                              </label>
                              <VueMultiselect
                                v-model="filterObj.accessible_departments"
                                :options="filteredOptions"
                                :multiple="true"
                                :close-on-select="false"
                                :clear-on-select="false"
                                :preserve-search="true"
                                placeholder="Select Designation"
                                class="font-11"
                              >
                                <!-- Custom Option Template -->
                                <template #option="{ option }">
                                  <div class="custom-option">
                                    <input
                                      type="checkbox"
                                      :checked="isChecked(option)"
                                      class="custom-checkbox"
                                      @change="toggleOption(option, $event)"
                                    />
                                    <span>{{ option }}</span>
                                  </div>
                                </template>

                                <!-- Custom Selection Template -->
                                <template #selection="{ values, isOpen }">
                                  <span
                                    class="multiselect__single font-10"
                                    v-if="values.length"
                                    v-show="!isOpen"
                                  >
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
                      <div
                        class="stepperbackground ps-2 pe-2 m-0 d-flex justify-content-between align-items-center"
                      >
                        <h1 @click="prevStep(1)" class="font-11 m-0">
                          <i class="bi bi-chevron-left"></i
                          ><span class="ms-2">Back To About Form</span>
                        </h1>
                        <div class="d-flex gap-2 align-items-center">
                          <div>
                            <button
                              v-if="isPreviewVisible"
                              class="btn btn-light previewBtn d-flex align-items-center font-13"
                              type="button"
                              @click="previewForm"
                            >
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
                          <button
                            v-if="blockArr.length"
                            class="btn btn-dark font-10 Withborder border"
                            type="button"
                            @click="saveFormData('save')"
                          >
                            {{
                              paramId !== "new" ? "Update Form" : "Create Form"
                            }}
                          </button>
                          <!-- <button class="btn btn-light font-10" type="button"
                                                        data-bs-toggle="modal" data-bs-target="#exampleModal"
                                                        @click="createForm">
                                                        <i class="bi bi-eye me-1"></i>Preview
                                                    </button> -->
                        </div>
                      </div>
                      <FormPreview
                        :blockArr="selectedform"
                        :formDescriptions="formDescriptions"
                        :childHeaders="childtableHeaders"
                        :child-name="childName"
                      />
                      <div class="main-block" ref="mainBlockRef">
                        <!-- Here is block level starts -->
                        <div
                          class="block-level"
                          v-for="(block, blockIndex) in blockArr"
                          :key="blockIndex"
                        >
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
                                <div
                                  v-if="paramId && workflowSetup.length"
                                  class="role-container"
                                >
                                  <label
                                    class="role-text d-flex align-items-center"
                                    v-if="getWorkflowSetup(blockIndex)"
                                  >
                                    <span class="role-label">
                                      {{
                                        getWorkflowSetup(blockIndex).roles
                                          .length > 0
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
                                    <span
                                      data-bs-toggle="offcanvas"
                                      data-bs-target="#offcanvasRight"
                                      aria-controls="offcanvasRight"
                                      @click="AddDesignCanvas(blockIndex)"
                                      v-if="
                                        getWorkflowSetup(blockIndex).roles
                                          .length > 2
                                      "
                                      class="more-count"
                                    >
                                      +{{
                                        getWorkflowSetup(blockIndex).roles
                                          .length - 2
                                      }}
                                      more
                                    </span>
                                  </label>
                                </div>

                                <button
                                  v-if="
                                    paramId != undefined &&
                                    paramId != null &&
                                    paramId != 'new' &&
                                    getWorkflowSetup(blockIndex).roles
                                      .length === 0
                                  "
                                  class="btn btn-light designationBtn d-flex align-items-center"
                                  type="button"
                                  data-bs-toggle="offcanvas"
                                  data-bs-target="#offcanvasRight"
                                  aria-controls="offcanvasRight"
                                  @click="AddDesignCanvas(blockIndex)"
                                >
                                  <img
                                    src="../../assets/oui_app-users-roles.svg"
                                    alt="Add"
                                    class="me-1"
                                  />
                                  Add designations
                                </button>

                                <!-- Edit Designation Button (only when roles are present for that block) -->
                                <button
                                  v-if="
                                    paramId != undefined &&
                                    paramId != null &&
                                    paramId != 'new' &&
                                    getWorkflowSetup(blockIndex).roles.length >
                                      0
                                  "
                                  class="btn btn-light designationBtn d-flex align-items-center"
                                  type="button"
                                  data-bs-toggle="offcanvas"
                                  data-bs-target="#offcanvasRight"
                                  aria-controls="offcanvasRight"
                                  @click="AddDesignCanvas(blockIndex)"
                                >
                                  <i class="bi bi-pencil font-14"></i>
                                </button>
                                <button
                                  class="btn btn-light bg-transparent border-0 font-13 deleteBlock"
                                  @click="removeBlock(blockIndex)"
                                >
                                  <i class="bi bi-trash me-1"></i> Delete Block
                                </button>
                              </div>
                            </div>
                          </div>
                          <!-- draggable="true" @dragstart="handleDragStart($event, sectionIndex, 'section', blockIndex)"
                                                            @dragover="handleDragOver($event)"
                                                            @drop="handleDrop($event, sectionIndex, 'section', blockIndex)" -->
                          <div class="mt-2 section_block">
                            <div
                              v-for="(section, sectionIndex) in block.sections"
                              :key="'section-' + sectionIndex"
                              class="dynamicSection section"
                            >
                              <section
                                class="d-flex justify-content-between align-items-center"
                              >
                                <div class="d-flex flex-column">
                                  <input
                                    v-model="section.label"
                                    type="text"
                                    :class="[
                                      'border-less-input',
                                      'font-14',
                                      { 'italic-style': !section.label },
                                      { 'fw-medium': section.label },
                                    ]"
                                    @change="
                                      handleFieldChange(
                                        blockIndex,
                                        sectionIndex
                                      )
                                    "
                                    placeholder="Untitled section"
                                  />
                                  <small
                                    v-if="section.errorMsg"
                                    class="text-danger font-10"
                                  >
                                    {{ section.errorMsg }}
                                  </small>
                                </div>
                                <div class="d-flex align-items-center">
                                  <!-- Button trigger modal -->
                                  <!-- <button type="button" class="btn btn-white font-12" data-bs-toggle="modal"
                                    data-bs-target="#childtable">
                                    Add Table
                                  </button> -->

                                  <button
                                    class="btn btn-light bg-transparent border-0 font-13 deleteSection"
                                    @click="
                                      removeSection(blockIndex, sectionIndex)
                                    "
                                  >
                                    <i class="bi bi-trash me-1"></i> Delete
                                    Section
                                  </button>
                                </div>
                              </section>
                              <!-- draggable="true" @dragstart="handleDragStart($event, rowIndex, 'row', blockIndex, sectionIndex)"
                                                                    @dragover="handleDragOver"
                                                                    @drop="handleDrop($event, rowIndex, 'row', blockIndex, sectionIndex)" -->
                              <div class="container-fluid">
                                <section
                                  class="row dynamicRow row-container"
                                  v-for="(row, rowIndex) in section.rows"
                                  :key="'row-' + rowIndex"
                                >
                                  <div
                                    class="d-flex justify-content-between align-items-center"
                                  >
                                    <label class="rownames">{{
                                      getRowSuffix(rowIndex)
                                    }}</label>
                                    <div>
                                      <button
                                        v-if="row.columns.length < 3"
                                        class="btn btn-light bg-transparent border-0 font-12"
                                        @click="
                                          addColumn(
                                            blockIndex,
                                            sectionIndex,
                                            rowIndex
                                          )
                                        "
                                      >
                                        <i class="bi bi-plus font-14"></i> Add
                                        Column
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
                                      <div
                                        v-for="(
                                          column, columnIndex
                                        ) in row.columns"
                                        :key="'column-' + columnIndex"
                                        @mouseenter="
                                          setHoveredColumn(
                                            blockIndex,
                                            sectionIndex,
                                            rowIndex,
                                            columnIndex
                                          )
                                        "
                                        @mouseleave="resetHoveredColumn"
                                        class="col p-0 dynamicColumn column-container"
                                      >
                                        <div
                                          class="column_name d-flex align-items-center justify-content-between"
                                        >
                                          <div class="d-flex flex-column ps-2">
                                            <input
                                              v-model="column.label"
                                              type="text"
                                              :class="[
                                                'border-less-input',
                                                'ps-1',
                                                'font-14',
                                                'inputHeight',
                                                {
                                                  'italic-style': !column.label,
                                                },
                                                { 'fw-medium': column.label },
                                              ]"
                                              @change="
                                                handleFieldChange(
                                                  blockIndex,
                                                  sectionIndex,
                                                  rowIndex,
                                                  columnIndex
                                                )
                                              "
                                              placeholder="Column Name"
                                            />
                                            <small
                                              v-if="column.errorMsg"
                                              class="text-danger font-10"
                                            >
                                              {{ column.errorMsg }}
                                            </small>
                                          </div>
                                          <div
                                            v-show="
                                              isHoveredColumn(
                                                blockIndex,
                                                sectionIndex,
                                                rowIndex,
                                                columnIndex
                                              )
                                            "
                                          >
                                            <button
                                              class="btn btn-light bg-transparent btn-sm"
                                              @click="
                                                removeColumn(
                                                  blockIndex,
                                                  sectionIndex,
                                                  rowIndex,
                                                  columnIndex
                                                )
                                              "
                                            >
                                              <i class="bi bi-x-lg"></i>
                                            </button>
                                          </div>
                                        </div>
                                        <!-- draggable="true"
                                                                                    @dragstart="handleDragStart($event, fieldIndex, 'field', blockIndex, sectionIndex, rowIndex, columnIndex)"
                                                                                    @dragover="handleDragOver"
                                                                                    @drop="handleDrop($event, fieldIndex, 'field', blockIndex, sectionIndex, rowIndex, columnIndex)" -->
                                        <div
                                          v-for="(
                                            field, fieldIndex
                                          ) in column.fields"
                                          :key="'field-' + fieldIndex"
                                          @mouseenter="
                                            setHoveredField(
                                              blockIndex,
                                              sectionIndex,
                                              rowIndex,
                                              columnIndex,
                                              fieldIndex
                                            )
                                          "
                                          @mouseleave="resetHoveredField"
                                          class="dynamicField"
                                        >
                                          <div class="px-1 field-border">
                                            <div
                                              class="d-flex justify-content-between"
                                            >
                                              <div class="flex-column d-flex">
                                                <input
                                                  v-model="field.label"
                                                  placeholder="Name the field"
                                                  :class="[
                                                    'border-less-input',
                                                    'font-14',
                                                    'p-0',
                                                    'inputHeight',
                                                    {
                                                      'italic-style':
                                                        !field.label,
                                                    },
                                                    {
                                                      'fw-medium': field.label,
                                                    },
                                                  ]"
                                                  @change="
                                                    handleFieldChange(
                                                      blockIndex,
                                                      sectionIndex,
                                                      rowIndex,
                                                      columnIndex,
                                                      fieldIndex
                                                    )
                                                  "
                                                />
                                                <small
                                                  v-if="field.errorMsg"
                                                  class="text-danger font-10"
                                                >
                                                  {{ field.errorMsg }}
                                                </small>
                                              </div>
                                              <div
                                                v-show="
                                                  isHoveredField(
                                                    blockIndex,
                                                    sectionIndex,
                                                    rowIndex,
                                                    columnIndex,
                                                    fieldIndex
                                                  )
                                                "
                                              >
                                                <button
                                                  class="btn btn-light btn-sm bg-transparent py-0"
                                                  @click="
                                                    copyField(
                                                      blockIndex,
                                                      sectionIndex,
                                                      rowIndex,
                                                      columnIndex,
                                                      fieldIndex
                                                    )
                                                  "
                                                >
                                                  <i
                                                    class="ri-file-copy-line font-13 copyIcon"
                                                  ></i>
                                                </button>
                                                <button
                                                  class="btn btn-light btn-sm bg-transparent trash-btn py-0"
                                                  @click="
                                                    removeField(
                                                      blockIndex,
                                                      sectionIndex,
                                                      rowIndex,
                                                      columnIndex,
                                                      fieldIndex
                                                    )
                                                  "
                                                >
                                                  <i
                                                    class="bi bi-x-lg font-13"
                                                  ></i>
                                                </button>
                                              </div>
                                            </div>

                                            <select
                                              v-model="field.fieldtype"
                                              class="form-select mb-2 mt-1 font-13 searchSelect"
                                              @change="
                                                onFieldTypeChange(
                                                  blockIndex,
                                                  sectionIndex,
                                                  rowIndex,
                                                  columnIndex,
                                                  fieldIndex
                                                )
                                              "
                                            >
                                              <option value="">
                                                Select Type
                                              </option>
                                              <option
                                                v-for="section in fieldTypes"
                                                :key="section"
                                                :value="section.type"
                                              >
                                                {{ section.label }}
                                              </option>
                                            </select>

                                            <div
                                              v-if="
                                                [
                                                  'Select',
                                                  'Table MultiSelect',
                                                  'Check',
                                                ].includes(field.fieldtype)
                                              "
                                            >
                                              <label
                                                class="font-12 fw-light"
                                                for="options"
                                                >Enter Options:</label
                                              >
                                              <textarea
                                                id="options"
                                                placeholder="Enter your Options"
                                                v-model="field.options"
                                                class="form-control shadow-none mb-1 font-12"
                                              ></textarea>
                                              <small
                                                v-if="
                                                  !field.options ||
                                                  field.options.trim() === ''
                                                "
                                                class="text-danger font-10"
                                              >
                                                Options are required for this
                                                field type.
                                              </small>
                                            </div>

                                            <div
                                              class="d-flex gap-2 align-items-center"
                                            >
                                              <div
                                                class="d-flex align-items-center"
                                              >
                                                <input
                                                  class="font-12"
                                                  v-model="field.reqd"
                                                  placeholder="Field Name"
                                                  type="checkbox"
                                                />
                                              </div>
                                              <div>
                                                <label
                                                  for="mandatory"
                                                  class="font-12 m-0 fw-light"
                                                  >Mandatory</label
                                                >
                                              </div>
                                            </div>
                                            <small
                                              v-if="field.error"
                                              class="text-danger font-10"
                                              >{{ field.error }}</small
                                            >
                                          </div>
                                        </div>

                                        <div
                                          class="d-flex justify-content-center align-items-center my-2"
                                        >
                                          <button
                                            class="btn btn-light btn-sm d-flex align-items-center addField m-2"
                                            @click="
                                              addField(
                                                blockIndex,
                                                sectionIndex,
                                                rowIndex,
                                                columnIndex
                                              )
                                            "
                                          >
                                            <i class="bi bi-plus fs-5"></i>
                                            <span>Add Field</span>
                                          </button>
                                        </div>
                                      </div>
                                    </div>
                                  </div>
                                </section>
                              </div>
                              <div
                                v-if="blockIndex === 0"
                                class="d-flex justify-content-start align-items-center my-2"
                              >
                                <!-- <button
                                  class="btn btn-light addRow m-2"
                                  @click="
                                    addRow(blockIndex, sectionIndex, rowIndex)
                                  "
                                >
                                  <i class="bi bi-plus"></i> Add row in section
                                </button> -->
                              </div>

                              <div class="childtableShow">
                                <div>
                                  <!-- <button
                                    v-if="blockIndex === 0 && !childName"
                                    class="btn btn-light addRow"
                                    @click="addMoreFieldsToTable('new')"
                                  >
                                    Add Table
                                  </button> -->
                                  <button
                                    v-if="blockIndex === 0"
                                    class="btn btn-light addRow"
                                    @click="
                                      childName
                                        ? addMoreFieldsToTable('more')
                                        : addMoreFieldsToTable('new')
                                    "
                                  >
                                    {{
                                      childName
                                        ? "Add more Fields to Table"
                                        : "Add Table"
                                    }}
                                  </button>
                                  <div v-if="childName">
                                    <div v-if="blockIndex === 0" class="mt-2">
                                      <div>
                                        <span class="font-13 fw-bold">{{
                                          childName
                                        }}</span>
                                      </div>
                                      <table
                                        class="table table-bordered table-striped"
                                      >
                                        <thead>
                                          <tr>
                                            <th>#</th>
                                            <th
                                              v-for="field in childtableHeaders"
                                              :key="field.fieldname"
                                            >
                                              {{ field.label }}
                                            </th>
                                          </tr>
                                        </thead>
                                        <tbody>
                                          <tr
                                            v-for="(
                                              row, index
                                            ) in childtableRows"
                                            :key="index"
                                          >
                                            <td>{{ index + 1 }}</td>
                                            <td
                                              v-for="field in childtableHeaders"
                                              :key="field.fieldname"
                                            >
                                              <span
                                                v-if="
                                                  isFilePath(
                                                    row[field.fieldname]
                                                  )
                                                "
                                                class="cursor-pointer"
                                                @click="
                                                  openFile(row[field.fieldname])
                                                "
                                              >
                                                <span
                                                  >View Attachment
                                                  <i
                                                    class="bi bi-eye-fill ps-1"
                                                  ></i
                                                ></span>
                                              </span>
                                              <span v-else>
                                                {{
                                                  row[field.fieldname] || "-"
                                                }}
                                              </span>
                                            </td>
                                          </tr>
                                        </tbody>
                                      </table>
                                    </div>
                                  </div>
                                  <div v-if="updateBtnDiv && blockIndex === 0">
                                    <div
                                      v-for="(field, fieldIndex) in columns"
                                      :key="'field-' + fieldIndex"
                                      class="dynamicField"
                                    >
                                      <div class="px-1 field-border">
                                        <div
                                          class="d-flex justify-content-between"
                                        >
                                          <div class="flex-column d-flex">
                                            <input
                                              v-model="field.label"
                                              placeholder="Name the field"
                                              :class="[
                                                'border-less-input',
                                                'font-14',
                                                'p-0',
                                                'inputHeight',
                                                {
                                                  'italic-style': !field.label,
                                                },
                                                { 'fw-medium': field.label },
                                              ]"
                                            />
                                          </div>
                                          <div>
                                            <button
                                              class="btn btn-light btn-sm bg-transparent trash-btn py-0"
                                              @click="removeField(fieldIndex)"
                                            >
                                              <i class="bi bi-x-lg"></i>
                                            </button>
                                          </div>
                                        </div>

                                        <select
                                          v-model="field.fieldtype"
                                          class="form-select mb-2 mt-1 font-13 searchSelect"
                                        >
                                          <!-- @change="validateField(field)" -->
                                          <option value="">Select Type</option>
                                          <option
                                            v-for="section in childfield"
                                            :key="section"
                                            :value="section.type"
                                          >
                                            {{ section.label }}
                                          </option>
                                        </select>
                                        <!-- <small v-if="field.errorMsg" class="text-danger font-10">{{ field.errorMsg
                                          }}</small>  -->

                                        <!-- <div class="d-flex gap-2 align-items-center">
                                                      <input class="font-12" v-model="field.reqd" type="checkbox" />
                                                      <label for="mandatory" class="font-12 m-0 fw-light">Mandatory</label>
                                                    </div>
                                                    <small v-if="field.error" class="text-danger font-10">{{ field.error }}</small> -->
                                      </div>
                                    </div>

                                    <div
                                      class="d-flex justify-content-center align-items-center my-2"
                                    >
                                      <button
                                        class="btn btn-light btn-sm d-flex align-items-center addField m-2"
                                        @click="addUpdatetablefield"
                                      >
                                        <i class="bi bi-plus fs-5"></i>
                                        <span>Add Field</span>
                                      </button>
                                      <div class="">
                                        <!-- <button type="button" class="btn btn-secondary btn-sm font-12">
                                          Close
                                        </button> -->
                                        <button
                                          type="button"
                                          class="btn btn-dark btn-sm font-12"
                                          @click="addmorechildfeildsFn"
                                        >
                                          Update Table
                                        </button>
                                      </div>
                                    </div>
                                  </div>
                                  <div>
                                    <div
                                      v-if="childtableShow && blockIndex === 0"
                                    >
                                      <div v-if="!childName">
                                        <div class="mb-3">
                                          <div>
                                            <div>
                                              <input
                                                @change="gettingTablename"
                                                placeholder="Table Name"
                                                :value="tableName"
                                                :class="[
                                                  'border-less-input',
                                                  'font-14',
                                                  'p-0',
                                                  'inputHeight',
                                                  {
                                                    'italic-style': !tableName,
                                                  },
                                                  { 'fw-medium': tableName },
                                                ]"
                                              />
                                            </div>
                                          </div>
                                        </div>

                                        <div>
                                          <div
                                            v-for="(
                                              field, fieldIndex
                                            ) in columns"
                                            :key="'field-' + fieldIndex"
                                            class="dynamicField"
                                          >
                                            <div class="px-1 field-border">
                                              <div
                                                class="d-flex justify-content-between"
                                              >
                                                <div class="flex-column d-flex">
                                                  <input
                                                    v-model="field.label"
                                                    placeholder="Name the field"
                                                    :class="[
                                                      'border-less-input',
                                                      'font-14',
                                                      'p-0',
                                                      'inputHeight',
                                                      {
                                                        'italic-style':
                                                          !field.label,
                                                      },
                                                      {
                                                        'fw-medium':
                                                          field.label,
                                                      },
                                                    ]"
                                                  />
                                                </div>
                                                <div>
                                                  <button
                                                    class="btn btn-light btn-sm bg-transparent trash-btn py-0"
                                                    @click="
                                                      removechildField(
                                                        fieldIndex
                                                      )
                                                    "
                                                  >
                                                    <i class="bi bi-x-lg"></i>
                                                  </button>
                                                </div>
                                              </div>

                                              <select
                                                v-model="field.fieldtype"
                                                class="form-select mb-2 mt-1 font-13 searchSelect"
                                              >
                                                <!-- @change="validateField(field)" -->
                                                <option value="">
                                                  Select Type
                                                </option>
                                                <option
                                                  v-for="section in childfield"
                                                  :key="section"
                                                  :value="section.type"
                                                >
                                                  {{ section.label }}
                                                </option>
                                              </select>
                                              <!-- <small v-if="field.errorMsg" class="text-danger font-10">{{ field.errorMsg
                                              }}</small> -->

                                              <!-- <div class="d-flex gap-2 align-items-center">
                                                      <input class="font-12" v-model="field.reqd" type="checkbox" />
                                                      <label for="mandatory" class="font-12 m-0 fw-light">Mandatory</label>
                                                    </div>
                                                    <small v-if="field.error" class="text-danger font-10">{{ field.error }}</small> -->
                                            </div>
                                          </div>

                                          <div
                                            class="d-flex justify-content-center align-items-center my-2"
                                          >
                                            <button
                                              class="btn btn-light btn-sm d-flex align-items-center addField m-2"
                                              @click="tableField"
                                            >
                                              <i class="bi bi-plus fs-5"></i>
                                              <span>Add Field</span>
                                            </button>
                                            <div class="">
                                              <!-- <button type="button" class="btn btn-secondary btn-sm font-12">
                                          Close
                                        </button> -->
                                              <button
                                                type="button"
                                                class="btn btn-dark btn-sm font-12"
                                                @click="processFields"
                                              >
                                                Create Table
                                              </button>
                                            </div>
                                          </div>
                                        </div>
                                      </div>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </div>

                            <div
                              class="d-flex justify-content-center align-items-center py-2 add-section-btn"
                            >
                              <button
                                class="btn btn-light border font-12"
                                @click="addSection(blockIndex)"
                              >
                                <i class="bi bi-plus-circle me-1 fs-6"></i> Add
                                Section
                              </button>
                            </div>
                          </div>
                        </div>
                        <!-- class="d-flex justify-content-center align-items-center add-block-btn-div py-4 pb-4" -->
                        <div
                          :class="[
                            'd-flex justify-content-center align-items-center add-block-btn-div py-4  ',
                            {
                              'background-color-white': blockArr.length,
                            },
                          ]"
                        >
                          <button
                            class="btn btn-light border d-flex align-items-center font-12"
                            @click="addBlock"
                          >
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

    <div
      class="offcanvas offcanvas-end"
      tabindex="-1"
      id="offcanvasRight"
      aria-labelledby="offcanvasRightLabel"
    >
      <div class="offcanvas-header add_designationHeader">
        <span id="offcanvasRightLabel font-14">
          Add designation for
          {{ selectedBlockIndex == 0 ? "Requestor" : "Approver" }}
        </span>

        <button
          type="button"
          class="btn-close bg-light text-reset"
          data-bs-dismiss="offcanvas"
          aria-label="Close"
        ></button>
      </div>
      <div class="offcanvas-body">
        <div class="">
          <div class="form-check ps-2" v-if="DesignationList.length">
            <input
              type="checkbox"
              id="selectAll"
              v-model="isAllSelected"
              class="me-2 form-check-input"
            />
            <label
              for="selectAll fw-bold"
              class="SelectallDesignation form-check-label"
              >Select all</label
            >
          </div>
        </div>
        <ul v-if="DesignationList.length" class="list-unstyled">
          <li
            v-for="(item, index) in DesignationList"
            :key="index"
            class="designationList"
          >
            <input
              type="checkbox"
              v-model="designationValue"
              :value="item"
              class="designationCheckBox"
              @change="handleSingleSelect"
            />
            <span class="ps-2">{{ item }}</span>
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
          <ButtonComp
            class="btn btn-dark addingDesignations"
            data-bs-dismiss="offcanvas"
            @click="addDesignationBtn"
            name=" Add Designations"
          />
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

const wrkAfterGetData = ref([]);
// const hasWorkflowToastShown = ref(false);
const tableFieldsCache = ref([]);
const childName = ref("");
const childtableRows = ref([]);
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

const hoveredIndexes = ref(null);
const hoveredColumnIndexes = ref(null);

// Functions for Field Hover
const setHoveredField = (
  blockIndex,
  sectionIndex,
  rowIndex,
  columnIndex,
  fieldIndex
) => {
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

const isHoveredField = (
  blockIndex,
  sectionIndex,
  rowIndex,
  columnIndex,
  fieldIndex
) => {
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
  console.log(paramId.value, "ggggg");

  if (
    paramId.value != undefined &&
    paramId.value != null &&
    paramId.value != "new"
  ) {
    getFormData();
    OwnerOftheForm();
  }
  let Bu_Unit = localStorage.getItem("Bu");
  filterObj.value.business_unit = Bu_Unit;
});

const tableField = () => {
  const newField = {
    label: "",
    fieldname: `field_${columns.length}`,
    fieldtype: "",
    idx: columns.length,
    reqd: false,
  };
  columns.push(newField);
};

const removechildField = (index) => {
  columns.splice(index, 1);
};
const addUpdatetablefield = () => {
  const newField = {
    label: "",
    fieldname: `field_${"sadcerdysasbdqjk"}`,
    fieldtype: "",
    idx: columns.length,
    reqd: false,
  };
  columns.push(newField);
};
//   const addUpdatetablefield = () => {
//   const randomNum = Math.floor(1000 + Math.random() * 9000); // Generates a 4-digit random number

//   const newField = {
//     label: "",
//     fieldname: "", // Placeholder, will be updated dynamically
//     fieldtype: "",
//     idx: columns.length,
//     reqd: false,
//   };

//   columns.push(newField);

//   // Watch for label changes and update fieldname with a random number
//   watch(() => newField.label, (newVal) => {
//     const sanitizedLabel = newVal.replace(/\s+/g, '_').toLowerCase();
//     newField.fieldname = `field_${sanitizedLabel}_${randomNum}`;
//   });
// };

// errorMsg: "",

// const validateField = (field) => {
//   if (!field.fieldtype) {
//     field.errorMsg = "Field type is required";
//   } else {
//     field.errorMsg = "";
//   }
// };
const gettingTablename = (e) => {
  if (e?.target?.value) {
    tableName.value = e.target.value
      .trim() // Remove leading/trailing spaces
      .toLowerCase() // Convert to lowercase
      .replace(/\s+/g, "_") // Replace spaces with underscores
      .replace(/[^a-z0-9_]/g, ""); // Remove non-alphanumeric characters except underscores
  }
};
const formattedData = computed(() => ({
  form_short_name: tableName.value,
  fields: columns,
}));

const isEmptyFieldType = computed(() => {
  return (
    !tableName.value ||
    columns.some((field) => !field.fieldtype || !field.label)
  );
});

// const updatedTableFields = computed(() => {

//   // console.log(columns,"=====", childtableHeaders.value);
//   // const field = {
//   //   ...columns,

//   // };

//   return {
//   //   form_short_name: tableName.value[0].options,
//   //   // business_unit: filterObj.business_unit,
//   //   fields: field,
//   form_short_name: tableName.value[0].options,
//   fields: field,
//   };
// });

const updatedTableFields = computed(() => ({
  form_short_name: tableName.value[0].options,
  fields: columns,
}));

const addmorechildfeildsFn = () => {
  const data = {
    ...updatedTableFields.value,
  };
  console.log(data, ",,,,,,,,,,");

  // Call the API to process the fields
  axiosInstance
    .post(`${apis.update_child_doctype}`, data)
    .then((res) => {
      if (res) {
        console.log(res); // Corrected response access

        // Extract the first "Table" field from the response

        getFormData();
      }
    })
    .catch((error) => {
      console.error("Error saving form data:", error); // Log any errors
    });
};

const processFields = () => {
  if (isEmptyFieldType.value) {
    toast.error("Please fill in all required fields before proceeding.", {
      transition: "zoom",
    });
    return;
  }

  console.log(isEmptyFieldType.value);
  console.log(tableName.value, "-=-=-=");
  console.log(JSON.stringify(formattedData.value));

  // console.log( filterObj.value,columns.value, tableName.value);
  const data = {
    ...formattedData.value,
  };
  console.log(data);

  // Call the API to process the fields
  axiosInstance
    .post(apis.childtable, data)
    .then((res) => {
      if (res) {
        console.log(res.message[0][0].child_doc); // Corrected response access

        // Extract the first "Table" field from the response
        const firstTableField = res.message[0][0].child_doc;

        // Store the first "Table" field in localStorage after the response
        // if (firstTableField) {
        //   localStorage.setItem(
        //     "tableFields",
        //     JSON.stringify([firstTableField])
        //   );
        // }
        if (firstTableField) {
          tableFieldsCache.value.push(firstTableField); // Store in ref instead of localStorage
        }
        // getFormData()
      }
    })
    .catch((error) => {
      console.error("Error saving form data:", error); // Log any errors
    });
};

// const modal = bootstrap.Modal.getInstance(
//           document.getElementById("childtable")
//         );
//         modal.hide();
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
    label: "Attach",
    type: "Attach",
  },
];
const fieldTypes = [
  {
    label: "Text",
    type: "Data",
  },

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
  {
      label: "Check",
      type: "Check",
  },  
  // {
  //     label: "Radio",
  //     type: "radio",
  // },
  {
    label: "Select",
    type: "Select",
  },
  // {
  //     label: "MultiSelect",
  //     type: "Table MultiSelect",
  // },
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
  if (selected.length > 2) {
    return `${selected.slice(0, 2).join(", ")}.. +${
      selected.length - 2
    } more selected`;
  }
  return selected.join(", ");
});

// Check if an option should be checked
const isChecked = (option) => {
  if (option === SELECT_ALL) {
    return (
      filterObj.value.accessible_departments.length === formOptions.value.length
    );
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
      filterObj.value.accessible_departments =
        filterObj.value.accessible_departments.filter(
          (item) => item !== option
        );
    }

    // If all options are selected, add "Select All"
    if (
      filterObj.value.accessible_departments.length === formOptions.value.length
    ) {
      filterObj.value.accessible_departments = [...formOptions.value];
    } else {
      // Remove "Select All" if not all options are selected
      filterObj.value.accessible_departments =
        filterObj.value.accessible_departments.filter(
          (item) => item !== SELECT_ALL
        );
    }
  }
};

const isAllSelected = computed({
  get() {
    return (
      DesignationList.value.length > 0 &&
      DesignationList.value.every((item) =>
        designationValue.value.includes(item)
      )
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

watch(designationValue, (newValue) => {
  console.log("Selected Designations:", typeof newValue);
  console.log(typeof designationValue.value, "designationValue");
  console.log(typeof DesignationList.value, "list");
  // console.log(listofselected.value, "------------------------");
});

function handleSingleSelect() {
  if (!isAllSelected.value && designationValue.value.length === 1) {
    console.log("Selected only one designation:", designationValue.value[0]);
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
  return (
    workflowSetup.find((setup) => setup.idx === blockIndex) || { roles: [] }
  );
}

// Initialize `designationValue` based on the roles for the given block index
function initializeDesignationValue(blockIndex) {
  const rolesForBlock = getWorkflowSetup(blockIndex).roles || [];
  designationValue.value = [...rolesForBlock]; // Reset designationValue to match only roles for the current block
}

const AddDesignCanvas = (idx) => {
  console.log(idx, "---clicked idex", selectedBlockIndex.value);
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

  // const queryParams = {
  //     fields: JSON.stringify(["*"]),
  //     // filters: JSON.stringify(filters),
  //     limit_page_length: filterObj.value.limitPageLength,
  //     limitstart: filterObj.value.limitstart,
  //     order_by: "`tabWF Role Matrix`.`creation` desc",
  // };

  axiosInstance
    .get(
      apis.resource +
        doctypes.WFRoleMatrix +
        `/${filterObj.value.business_unit}`
    )
    .then((res) => {
      if (res.data) {
        console.log(res.data.users, "wf role matrix");
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

function cancelForm() {
  router.push({
    name: "Created",
  });
}
const handleStepClick = (stepId) => {
  if (isNextDisabled.value) {
    toast.error("Please complete all required fields before proceeding.", {
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
    toast.error("Please complete all required fields before proceeding.", {
      autoClose: 2000,
      transition: "zoom",
    });
    return;
  }

  if (activeStep.value < 3) {
    activeStep.value += 1;
  }
};

// const handleStepClick = (stepId) => {
//   if (isNextDisabled.value === false) {
//     if (stepId < activeStep.value) {
//       prevStep(stepId);
//     } else if (stepId > activeStep.value) {
//       nextStep(stepId);
//     }
//   }
// };

// const nextStep = () => {
//   if (activeStep.value < 3) {
//     activeStep.value += 1;
//   }
// };

const prevStep = () => {
  if (activeStep.value > 1) {
    activeStep.value -= 1;
  }
};
// watch(
//     () => filterObj.owner_of_the_form,
//     (newVal, oldVal) => {
//         if (newVal !== oldVal) {
//             OwnerOftheForm(newVal, oldVal);
//         }
//     }
// );

// Get form by ID
function getFormData() {
  axiosInstance
    .get(apis.resource + doctypes.EzyFormDefinitions + `/${paramId.value}`)
    .then((res) => {
      let res_data = res?.data;
      if (res_data) {
        if (res_data.accessible_departments) {
          res_data.accessible_departments =
            res_data.accessible_departments.split(",");
        }
        filterObj.value = {
          ...filterObj.value,
          ...res_data,
          owner_of_the_form:
            res_data.owner_of_the_form ||
            filterObj.value.owner_of_the_form ||
            "",
        };

        // Only fetch categories if `form_category` is empty
        // if (!filterObj.value.form_category && filterObj.value.owner_of_the_form) {
        //     categoriesData(filterObj.value.owner_of_the_form);
        // }
        console.log(res.data.form_json, "jjjjj");
        childtableHeaders.value = JSON.parse(
          res.data.form_json
        ).child_table_fields;
        console.log(
          childtableHeaders.value,
          typeof childtableHeaders.value,
          "---child"
        );

        console.log(res.data, "7777777777777777");
        const parsedFormJson = JSON.parse(res.data?.form_json);
        wrkAfterGetData.value = parsedFormJson.workflow;
        console.log(parsedFormJson.workflow, "parsedFormJson");
        tableName.value = parsedFormJson.fields.filter(
          (field) => field.fieldtype === "Table"
        );
        childName.value = tableName.value[0]?.options.replace(/_/g, " ");
        console.log(childName.value, typeof childName.value, "5555");

        // let structuredArr = rebuildToStructuredArray((JSON.parse(res_data?.form_json?.fields).fields)?.replace(/\\\"/g, '"'))
        let structuredArr = rebuildToStructuredArray(
          JSON.parse(res_data?.form_json).fields
        );

        // workflowSetup.push(JSON.parse(res_data?.form_json).workflow)

        structuredArr.forEach((item, index) => {
          blockArr.push(item);
        });

        JSON.parse(res_data?.form_json).workflow.forEach((item, index) => {
          workflowSetup.push(item);
        });

        axiosInstance
          .get(`${apis.resource}${res.data.name}`)
          .then((responce) => {
            child_id.value = responce.data[0]?.name;

            if (child_id.value) {
              axiosInstance
                .get(`${apis.resource}${res.data.name}/${child_id.value}`)
                .then((res) => {
                  console.log(child_id.value, "llll");
                  console.log(`Data for66666666666666666 :`, res.data);
                  // Identify the child table key dynamically
                  // const childTableKey = Object.keys(res.data).find((key) =>
                  //   Array.isArray(res.data[key])
                  // );
                  // tableName.value = childTableKey?.replace(/_/g, " ");
                  // console.log(tableName.value,"yyyyyyyyyy");

                  // if (childTableKey) {
                  //   childTableresponseData.value = res.data[childTableKey];
                  //   childtableRows.value = childTableresponseData.value; // Assign table rows
                  //   console.log(childtableRows.value, "Dynamic Child Table Data");
                  // }
                })
                .catch((error) => {
                  console.error(`Error fetching data for :`, error);
                });
            }
          })
          .catch((error) => {
            console.error(`Error fetching data for :`, error);
          });
      }
    })
    .catch((error) => {
      console.error("Error fetching  data:", error);
    });
}

const openFile = (filePath) => {
  if (!filePath) return;
  const fileUrl = `${filePath}`;
  window.open(fileUrl, "_blank");
};

const isFilePath = (value) => {
  if (!value) return false;
  return /\.(png|jpg|jpeg|gif|pdf|docx|xlsx|txt)$/i.test(value);
};
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

// function OwnerOftheForm(newVal) {
//     if (newVal) {
//         console.log(newVal, "ppppp");
//         categoriesData(newVal); // No need to check filterObj.value.owner_of_the_form again
//     }
// }
function OwnerOftheForm(newVal) {
  if (newVal && typeof newVal === "string" && newVal.trim() !== "") {
    console.log("Owner Of The Form Changed:", newVal);
    categoriesData(newVal);
  } else {
    console.log("Owner Of The Form is empty or undefined.");
  }
}

function categoriesData(newVal) {
  axiosInstance
    .get(apis.resource + doctypes.departments + `/${newVal}`)
    .then((res) => {
      if (res?.data?.ezy_departments_items) {
        departments.value = res.data.ezy_departments_items.map(
          (item) => item.category
        );
      }
    })
    .catch((error) => {
      console.error("Error fetching categories data:", error);
    });
}
//   const hasTableField = fields.some((field) => field.fieldtype === "Table");

//   if (hasTableField) {
//     console.log("Table field found, hitting child table API...");
//     processFields(fields); // Call child table API first
//   }

// Retrieve the first "Table" field from localStorage
// const storedTableFields =
//   JSON.parse(localStorage.getItem("tableFields")) || [];

//   // If there is a stored "Table" field, merge it into fields and clear localStorage
// if (storedTableFields.length) {
//   console.log("Using stored Table field from localStorage...");
//   fields = [...fields, ...storedTableFields];
//   // Clear localStorage after merging and using the data
// }

function formData(status) {
  console.log(blockArr, "blockarray");

  let fields = extractFieldsWithBreaks(blockArr);
  console.log(fields, "Extracted Fields");
  if (tableFieldsCache.value.length) {
    console.log("Using stored Table field from variable cache...");
    fields = [...fields, ...tableFieldsCache.value];
  }
  const dataObj = {
    ...filterObj.value,
    fields,
    doctype: doctypes.EzyFormDefinitions,
    workflow_setup: workflowSetup,
    form_status: status === "save" ? "Created" : "Draft",
  };

  dataObj.accessible_departments = dataObj.accessible_departments.toString();
  console.log(dataObj, "---data obj");
  axiosInstance
    .post(apis.savedata, dataObj)
    .then((res) => {
      if (res && res.message && res.message.message) {
        tableFieldsCache.value = [];
        router.push({
          params: { paramid: res.message.message },
        });
        paramId.value = res.message.message;
        // paramId = res.message.message; 

        if (paramId && paramId !== "new") {
              blockArr.splice(0, blockArr.length);
              getFormData();
            }
        console.log(paramId.value, "Updated paramId");

       
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

// function formData(status) {
//     console.log(blockArr, "blockarray");

//     const fields = extractFieldsWithBreaks(blockArr);
//     const dataObj = {
//         ...filterObj.value,
//         fields,
//         doctype: doctypes.EzyFormDefinitions,
//         workflow_setup: workflowSetup,
//         form_status: status === "save" ? "Created" : "Draft",
//         // form_status: "Draft",

//     };
//     dataObj.accessible_departments = dataObj.accessible_departments.toString(); //JSON.stringify(dataObj.accessible_departments) dataObj.accessible_departments.toString()

//     axiosInstance
//         .post(apis.savedata, dataObj)
//         .then((res) => {
//             if (res) {
//                 toast.success("Form Created Successfully", { autoClose: 2000, "transition": "zoom" });
//                 router.push({
//                     params: { paramid: res.message.message },
//                 });
//                 paramId = res.message.message;
//                 if (paramId.value !== "new") {
//                     blockArr.splice(0, blockArr.length);
//                     getFormData();
//                 }
//                 // if (paramId.value === "new") {
//                 //     router.push({
//                 //         name: "Created"
//                 //     })

//                 // }
//                 if (status === "draft") {
//                     router.push({
//                         name: "Draft"
//                     })

//                 }
//             }
//         })
//         .catch((error) => {
//             console.error("Error saving form data:", error);
//         });
// }

// Function to add a new block

const mainBlockRef = ref("");
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
//             columns: [
//               {
//                 label: "",
//                 fields: [
//                   {
//                     label: "",
//                     fieldtype: "",
//                     options: "",
//                     reqd: false,
//                   },
//                 ],
//               },
//             ],
//           },
//         ],
//       },
//     ],
//   };

//   blockArr.splice(blockArr.length, 0, newBlock);
//   nextTick(() => {
//     if (mainBlockRef.value) {
//       mainBlockRef.value.scrollTo({
//         top: mainBlockRef.value.scrollHeight,
//         behavior: "smooth",
//       });
//     }
//   });
//   // console.log(blockArr.length, blockArr, "00000");
// };
const addBlock = () => {
  const blockIndex = blockArr.length; // Get current length before adding new block

  const newBlock = {
    label: blockIndex === 0 ? "requestor" : `approver-${blockIndex}`,
    parent: `${businessUnit.value?.value}-${filterObj.value?.form_short_name}`,
    sections: [
      {
        label: "",
        parent: `${businessUnit.value.value}-${filterObj.value.form_short_name}`,
        rows: [
          {
            label: `row_0_0_${blockIndex}`,
            columns:
              blockIndex === 0
                ? [
                    {
                      label: "", // No extra empty column for the requestor block
                      fields: [{ label: "", fieldtype: "", options: "", reqd: false }],
                    },
                  ]
                : [
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
};
// Function to remove a section
const removeSection = (blockIndex, sectionIndex) => {
  let item = blockArr[blockIndex].sections[sectionIndex];
  if (item.parent) deleted_items.push(item);
  blockArr[blockIndex].sections.splice(sectionIndex, 1);
  // toast.success("Section removed", { autoClose: 500 })
};

const addRow = (blockIndex, sectionIndex) => {
  const rowIndex = blockArr[blockIndex].sections[sectionIndex].rows.length; // Get the current row index
  const rowSuffix = getRowSuffix(rowIndex);

  blockArr[blockIndex].sections[sectionIndex].rows.push({
    label: `row_${rowIndex}_${sectionIndex}_${blockIndex}`,
    columns: [
      {
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
  });
};

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
    blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[
      columnIndex
    ];
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
};

// Function to remove a field inside a column
const removeField = (
  blockIndex,
  sectionIndex,
  rowIndex,
  columnIndex,
  fieldIndex
) => {
  let item =
    blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[
      columnIndex
    ].fields[fieldIndex];
  if (item.parent) deleted_items.push(item);
  blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[
    columnIndex
  ].fields.splice(fieldIndex, 1);
  // toast.success("Field removed", { autoClose: 500 })
};

// Function to copy a field and add it below the original field inside a column
const copyField = (
  blockIndex,
  sectionIndex,
  rowIndex,
  columnIndex,
  fieldIndex
) => {
  // Get the field to copy
  const fieldToCopy =
    blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[
      columnIndex
    ].fields[fieldIndex];

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
    blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[
      columnIndex
    ].fields[fieldIndex].fieldtype;
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
// const forChildTable = () => {

//     console.log("All Fields Data:", blockArr);

//     // Call an API or another function here
//     processFields(blockArr);
// };

function handleFieldChange(
  blockIndex,
  sectionIndex,
  rowIndex,
  columnIndex,
  fieldIndex
) {
  const flatArr = blockArr.flatMap(extractfieldlabels);
  const isDuplicate = hasDuplicates(flatArr); // Check once to reuse this result

  const checkFieldType = addErrorMessagesToStructuredArray(blockArr);
  blockArr.splice(0, blockArr.length, ...checkFieldType);

  // Assign error message for the specific field if fieldIndex is valid
  if (
    fieldIndex !== undefined &&
    fieldIndex >= 0 &&
    columnIndex !== undefined &&
    columnIndex >= 0 &&
    sectionIndex !== undefined
  ) {
    blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[
      columnIndex
    ].fields[fieldIndex].errorMsg = isDuplicate ? "Duplicate Label Name" : "";
  }

  // Assign error message for the column if fieldIndex is not valid
  if (
    fieldIndex === undefined &&
    columnIndex !== undefined &&
    columnIndex >= 0 &&
    sectionIndex !== undefined
  ) {
    blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[
      columnIndex
    ].errorMsg = isDuplicate ? "Duplicate Label Name in Column" : "";
  }

  // Assign error message for the section if both columnIndex and fieldIndex are not valid columnIndex === undefined &&
  if (
    columnIndex === undefined &&
    fieldIndex === undefined &&
    sectionIndex !== undefined
  ) {
    blockArr[blockIndex].sections[sectionIndex].errorMsg = isDuplicate
      ? "Duplicate Label Name in Section"
      : "";
  }
}

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

// const hasErrors = computed(() => {
//   function checkFieldErrors(obj) {
//     if (!obj || typeof obj !== "object") return false;

//     // Check if `fieldtype` is empty, or if `error` or `errorMsg` exist
//     if (
//       ("fieldtype" in obj && obj.fieldtype === "") ||
//       ("error" in obj && obj.error) ||
//       ("errorMsg" in obj && obj.errorMsg)
//     ) {
//       return true;
//     }

//     if (Array.isArray(obj)) {
//       return obj.some(checkFieldErrors);
//     }

//     return Object.values(obj).some(checkFieldErrors);
//   }

//   return checkFieldErrors(blockArr);
// });

// function handleFieldChange(
//     blockIndex,
//     sectionIndex,
//     rowIndex,
//     columnIndex,
//     fieldIndex
// ) {
//     const flatArr = blockArr.flatMap(extractfieldlabels);
//     const isDuplicate = hasDuplicates(flatArr); // Check once to reuse this result
//     const checkFieldType = addErrorMessagesToStructuredArray(blockArr);
//     blockArr.splice(0, blockArr.length, ...checkFieldType);

//     // Assign error message for the specific field if fieldIndex is valid
//     if (
//         fieldIndex !== undefined &&
//         fieldIndex >= 0 &&
//         columnIndex !== undefined &&
//         columnIndex >= 0 &&
//         sectionIndex !== undefined
//     ) {
//         blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[
//             columnIndex
//         ].fields[fieldIndex].errorMsg = isDuplicate ? "Duplicate Label Name" : "";
//     }

//     // Assign error message for the column if fieldIndex is not valid
//     if (
//         sectionIndex !== undefined &&
//         columnIndex !== undefined && // Ensure columnIndex is defined
//         fieldIndex === undefined
//     ) {
//         blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[
//             columnIndex
//         ].errorMsg = isDuplicate ? "Duplicate Label Name in Column" : "";
//     }

//     // Assign error message for the section if both columnIndex and fieldIndex are not valid
//     if (
//         columnIndex === undefined &&
//         fieldIndex === undefined &&
//         sectionIndex !== undefined
//     ) {
//
//         blockArr[blockIndex].sections[sectionIndex].errorMsg = isDuplicate
//             ? "Duplicate Label Name in Section"
//             : "";
//
//     }
// }
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

// function handleInputChange(event, fieldType) {
//     const inputValue = event.target.value;

//     // Set filter based on fieldType
//     const filters = [[fieldType, "like", `%${inputValue}%`]];
//     const queryParams = {
//         fields: JSON.stringify(["*"]),
//         filters: JSON.stringify(filters),
//     };

//     axiosInstance
//         .get(`${apis.resource}${doctypes.EzyFormDefinitions}`, {
//             params: queryParams,
//         })
//         .then((res) => {

//             ezyFormsData.value = res.data;

//             // Check for duplicates and set appropriate error message
//             if (fieldType === "form_name") {
//                 formNameError.value =
//                     inputValue &&
//                         ezyFormsData.value.some(
//                             (item) =>
//                                 item.form_name &&
//                                 item.form_name.toLowerCase() === inputValue.toLowerCase()
//                         )
//                         ? "Name already exists"
//                         : "";
//           } else if (fieldType === "form_short_name") {
//                 formShortNameError.value =
//                     inputValue &&
//                         ezyFormsData.value.some(
//                             (item) =>
//                                 item.form_short_name &&
//                                 item.form_short_name.toLowerCase() === inputValue.toLowerCase()
//                         )
//                         ? "Short name already exists"
//                         : "";
//             }
//         })
//         .catch((error) => {
//             console.error("Error fetching ezyForms data:", error);
//             // Clear error message on fetch error
//             if (fieldType === "form_name") formNameError.value = "";
//             else if (fieldType === "form_short_name") formShortNameError.value = "";
//         });
// }

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

  if (
    paramId != undefined &&
    paramId != null &&
    paramId != "new" &&
    data.length
  ) {
    delete_form_items_fields();
  } else {
    formData(type);
  }
}
// async function saveFormData(type) {
//   let data = deleted_items.flatMap(extractFieldnames);
//   if (
//     paramId != undefined &&
//     paramId != null &&
//     paramId != "new" &&
//     data.length
//   ) {
//     delete_form_items_fields();
//   } else {
//     formData(type);
//   }
// }

// const getFieldComponent = (type) => {
//   switch (type) {
//     case "Data":
//       return "input";
//     case "Phone":
//       return "input";
//     case "Time":
//       return "input";
//     case "Text":
//       return "textarea";
//     case "Color":
//       return "input";
//     case "Check":
//       return "input";
//     case "Select":
//       return "select";
//     case "Table MultiSelect":
//       return "select";
//     case "Date":
//       return "input";
//     case "Datetime":
//       return "input";
//     case "Attach":
//       return "file";
//     case "radio":
//       return "input";
//     default:
//       return "input";
//   }
// };
// const swapItems = (arr, fromIndex, toIndex) => {
//     if (!Array.isArray(arr) || fromIndex < 0 || toIndex < 0 || fromIndex >= arr.length || toIndex >= arr.length) {
//         console.warn(`Invalid swap indices: ${fromIndex}, ${toIndex} for array`, arr);
//         return;
//     }
//     [arr[fromIndex], arr[toIndex]] = [arr[toIndex], arr[fromIndex]];

// };

// // Swap Sections
// const swapSections = (fromIndex, toIndex, blockIndex) => {
//     if (blockArr?.[blockIndex]?.sections) {
//         swapItems(blockArr[blockIndex].sections, fromIndex, toIndex);
//     }
// };

// // Swap Rows
// const swapRows = (fromIndex, toIndex, sectionIndex, blockIndex) => {
//     if (blockArr?.[blockIndex]?.sections?.[sectionIndex]?.rows) {
//         swapItems(blockArr[blockIndex].sections[sectionIndex].rows, fromIndex, toIndex);
//     } else {
//         console.warn(`Row swap failed: Invalid section index ${sectionIndex} or block index ${blockIndex}`);
//     }
// };

// // Swap Columns
// const swapColumns = (fromIndex, toIndex, sectionIndex, rowIndex, blockIndex) => {
//     if (blockArr?.[blockIndex]?.sections?.[sectionIndex]?.rows?.[rowIndex]?.columns) {
//         swapItems(blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns, fromIndex, toIndex);
//     } else {
//         console.warn(`Column swap failed: Invalid indices - section: ${sectionIndex}, row: ${rowIndex}, block: ${blockIndex}`);
//     }
// };

// // Swap Fields (Corrected to move field between columns)
// const swapFields = (fromIndex, toIndex, sectionIndex, rowIndex, fromColumnIndex, toColumnIndex, blockIndex) => {
//     const fromColumn = blockArr?.[blockIndex]?.sections?.[sectionIndex]?.rows?.[rowIndex]?.columns?.[fromColumnIndex];
//     const toColumn = blockArr?.[blockIndex]?.sections?.[sectionIndex]?.rows?.[rowIndex]?.columns?.[toColumnIndex];

//     if (fromColumn?.fields && toColumn?.fields) {
//         if (fromColumnIndex !== toColumnIndex) {
//             // Move field between different columns
//             const fieldToMove = fromColumn.fields.splice(fromIndex, 1)[0];
//             toColumn.fields.splice(toIndex, 0, fieldToMove);
//
//         } else {
//             // Swap fields within the same column
//             swapItems(fromColumn.fields, fromIndex, toIndex);
//         }
//     } else {
//         console.warn(`Field swap failed: Invalid indices - section: ${sectionIndex}, row: ${rowIndex}, fromColumn: ${fromColumnIndex}, toColumn: ${toColumnIndex}, block: ${blockIndex}`);
//     }
// };

// // Drag-and-Drop Methods
// const handleDragStart = (event, index, type, blockIndex = null, sectionIndex = null, rowIndex = null, columnIndex = null) => {
//     event.dataTransfer.setData('index', index);
//     event.dataTransfer.setData('type', type);
//     if (blockIndex !== null) event.dataTransfer.setData('blockIndex', blockIndex);
//     if (sectionIndex !== null) event.dataTransfer.setData('sectionIndex', sectionIndex);
//     if (rowIndex !== null) event.dataTransfer.setData('rowIndex', rowIndex);
//     if (columnIndex !== null) event.dataTransfer.setData('columnIndex', columnIndex);
//
// };

// // Handle drag over event (necessary for drop to work)
// const handleDragOver = (event) => {
//     event.preventDefault();
// };

// // Handle drop event to swap items
// const handleDrop = (event, index, type, blockIndex = null, sectionIndex = null, rowIndex = null, columnIndex = null) => {
//     event.preventDefault();

//     const draggedIndex = Number(event.dataTransfer.getData('index'));
//     const draggedType = event.dataTransfer.getData('type');
//     const draggedBlockIndex = Number(event.dataTransfer.getData('blockIndex'));
//     const draggedSectionIndex = Number(event.dataTransfer.getData('sectionIndex'));
//     const draggedRowIndex = Number(event.dataTransfer.getData('rowIndex'));
//     const draggedColumnIndex = Number(event.dataTransfer.getData('columnIndex'));

//     if (draggedType === 'section' && type === 'section') {
//         swapSections(draggedIndex, index, draggedBlockIndex);
//     } else if (draggedType === 'row' && type === 'row') {
//         swapRows(draggedIndex, index, draggedSectionIndex, draggedBlockIndex);
//     } else if (draggedType === 'column' && type === 'column') {
//         swapColumns(draggedIndex, index, draggedSectionIndex, draggedRowIndex, draggedBlockIndex);
//     } else if (draggedType === 'field' && type === 'field') {
//         if (draggedColumnIndex !== columnIndex) {
//             swapFields(draggedIndex, index, draggedSectionIndex, draggedRowIndex, draggedColumnIndex, columnIndex, draggedBlockIndex);
//         } else {
//             swapItems(
//                 blockArr[draggedBlockIndex].sections[draggedSectionIndex].rows[draggedRowIndex].columns[draggedColumnIndex].fields,
//                 draggedIndex,
//                 index
//             );
//         }
//     }
// };

const hasDuplicates = (array) => new Set(array).size !== array.length;
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style lang="scss" scoped>
.inputHeight {
  height: 36px;
  min-width: 380px;
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
  margin: 0px 10px 5px 10px;
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
