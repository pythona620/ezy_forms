<template>
  <div>
    <div class="">
      <div class="">
        <div class="d-flex justify-content-between align-items-center CancelNdSave">
           <div class="d-flex align-items-center">
            <div class="ps-1 my-2 d-flex align-items-center" @click="cancelForm()">
            <button class="btn font-13 ms-3">
              <i class="bi bi-arrow-left"></i><span class="ms-2">Back</span>
            </button>
          </div>
          <span v-if="$route.query.id || $route.query.preId" class="font-16">({{ selectedData.formId || route.query.form_name }})</span>
          </div>
          <div>
            <!-- <ButtonComp class="font-13 rounded-2" name="Save as Draft"></ButtonComp> -->
            <button v-if="activeStep === 2 && blockArr.length && !$route.query.id"
              :disabled="hasErrors || isNextDisabled" :style="{ cursor: hasErrors ? 'not-allowed' : 'pointer' }"
              type="butoon" class="btn font-13 btn-light" @click="saveFormData('Draft')">
              <i class="bi bi-bookmark-check-fill"></i> Save As Draft
            </button>


            
          </div>
        </div>
        <div class="form-container p-0 container-fluid mt-3">
          <div class="row g-4">
            <div class="col-lg-2 col-md-3 col-sm-12">
              <div class="steps-sticky-div">
                <ul class="steps d-sm-inline-flex d-md-block m-0 p-0">
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
            <div class="col-lg-10 col-md-9 col-sm-12 formbackground-color">
              <div class="px-2">
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
                          <button v-if="!$route.query.id && !$route.query.preId" class=" btn btn-light font-12 mx-2" type="button"
                            @click="clearForm">Clear
                            Form</button>

                          <ButtonComp class="btn btn-dark bg-dark text-white fw-bold font-13" name="Next"
                            v-if="activeStep < 3" @click="nextStep" />
                        </div>
                        <!-- :class="{ 'disabled-btn': isNextDisabled }" -->
                        <!-- :disabled="isNextDisabled" -->
                      </div>
                    </div>
                    <div class="container-fluid aboutFields p-0">
                      <div class="row">
                        <div class="col-sm-none col-md-4"></div>
                        <div class="col-sm-12 col-md-12 mt-lg-3 p-lg-4">
  <div class="container-fluid">
    <div class="row g-3"> 
      <!-- Form Name -->
      <div class="col-md-6">
        <div class=" position-relative">
            <span v-if="route.query.preId" class=" font-12 position-absolute PredefinedLabel">Predefined
              <i class="bi bi-check2-circle"></i></span>
                <FormFields
                  :disabled="(selectedData.formId && selectedData.formId.length > 0 || route.query.form_name) && isDuplicate!=='1'"
                  labeltext="Form Name" class="formHeight" type="text" tag="input" name="Value"
                  id="formName" validationStar="true" placeholder="Untitled Form"
                  @change="(event) => handleInputChange(event, 'form_name')" v-model="formNameModel" />
                  <span v-if="formNameError" class="text-danger ErrorMsg ms-2">
                  {{ formNameError }}</span>
                  </div>
      </div>

      <!-- Form Short Code -->
      <div class="col-md-6">
        <FormFields
          :disabled="(selectedData.formId && selectedData.formId.length > 0 || route.query.form_name) && isDuplicate!=='1'"
          labeltext="Form Short Code"
          class="formHeight"
          type="text"
          tag="input"
          name="Value"
          id="formShortCode"
          validationStar="true"
          placeholder="Untitled Form"
          @change="(event) => handleInputChange(event, 'form_short_name')"
          v-model="filterObj.form_short_name"
        />
        <span v-if="formShortNameError" class="text-danger ErrorMsg ms-2">{{ formShortNameError }}</span>
      </div>

      <!-- Form Naming Series -->
      <div class="col-md-6">
        <FormFields
          :disabled="(selectedData.formId && selectedData.formId.length > 0) && isDuplicate!=='1'"
          labeltext="Form Naming series"
          class="formHeight"
          type="text"
          tag="input"
          name="Value"
          id="formNameSeries"
          placeholder="Form Naming series"
          v-model="filterObj.series"
        />
        <small class="text-muted" style="font-size:12px"> Note : Enter <code>YY-YY</code>, <code>YYYY</code>, or <code>ABC</code>. The system will default to the format <code> 24-25-0001</code>, <code> 2025-0001</code>, or <code> ABC-0001</code> respectively. </small>
      </div>
      
      <!-- Owner Of The Form -->
      <div class="col-md-6">
        <label>Owner Of The Form
          <span v-if="!filterObj.owner_of_the_form" class="text-danger">*</span>
        </label>
        <Multiselect
          :disabled="(selectedData.formId && selectedData.formId.length > 0) && isDuplicate!=='1'"
          @open="deptData"
          :options="OwnerOfTheFormData"
          @change="OwnerOftheForm"
          v-model="filterObj.owner_of_the_form"
          placeholder="Select Department"
          :multiple="false"
          class="font-11 multiselect"
          :searchable="true"
          openDirection="bottom"
        />
      </div>

      <!-- Form Category -->
      <div class="col-md-6">
        <label>Form Category
          <span v-if="!filterObj.form_category" class="text-danger">*</span>
        </label>
        <Multiselect
          :disabled="(selectedData.formId && selectedData.formId.length > 0) && isDuplicate!=='1'"
          :options="departments"
          v-model="filterObj.form_category"
          placeholder="Select Category"
          :multiple="false"
          :searchable="true"
          class="font-11 multiselect"
        />
      </div>

      <!-- Accessible to department -->
      <div class="col-md-6">
        <label>Accessible to Department
          <span v-if="!filterObj.accessible_departments.length" class="text-danger">*</span>
        </label>
        <VueMultiselect
          v-model="filterObj.accessible_departments"
          :options="filteredOptions"
          :multiple="true"
          :close-on-select="false"
          :clear-on-select="false"
          :preserve-search="true"
          placeholder="Select Department"
          class="font-11"
          @select="handleSelect"
          @remove="handleRemove"
          openDirection="bottom"
        >
          <template #option="{ option }">
            <div class="custom-option">
              <input type="checkbox" :checked="isChecked(option)" class="custom-checkbox"
                     @change="toggleOption(option, $event)" @click.stop />
              <span>{{ option }}</span>
            </div>
          </template>
          <template #selection="{ values, isOpen }">
            <span class="multiselect__single font-10" v-if="values.length" v-show="!isOpen">
              {{ formattedSelection }}
            </span>
          </template>
        </VueMultiselect>
      </div>

      <!-- Form Type -->
      <div class="col-md-6">
        <label>Form Type</label>
        <Multiselect
          :options="formTypeOptions"
          v-model="selectedFormType"
          placeholder="Select Form Type"
          :multiple="false"
          :searchable="true"
          label="label"
          track-by="value"
          :reduce="option => option.value"
          class="font-11 multiselect"
          openDirection="top"
        />
        <small class="text-muted font-12 ms-2">Note: Public form is accessible by anyone through QR code.</small>
      </div>

      <!-- Has Workflow -->
      <div class="col-md-6">
        <label>Has Workflow <span class="fw-normal font-11 text-secondary">(optional)</span></label>
        <Multiselect
          :options="['Yes', 'No']"
          v-model="filterObj.has_workflow"
          placeholder="Select"
          :multiple="false"
          class="font-11 multiselect"
          :searchable="true"
        />
      </div>

      <!-- Form Submit Response -->
      <div class="col-md-6" v-if="filterObj.as_web_view===1">
      <label>Form Submit Response <span class="fw-normal font-11 text-secondary">(optional)</span></label>
      <FormFields
        class="formHeight mt-2"
        type="text"
        tag="input"
        name="Value"
        id="formNameSeries"
        placeholder="Form Submit Response"
        v-model="filterObj.public_form_response"
        />
      </div>
 
      <!-- Form Submit Send Mail -->
      <div class="col-md-6" v-if="filterObj.as_web_view===1">
        <label>Submit Notification Email <span class="fw-normal font-11 text-secondary">(optional)</span></label>
            <FormFields
              class="formHeight mt-2"
              type="text"
              tag="input"
              name="Value"
              id="formNameSeries"
              placeholder="Form Submit mail"
              v-model="filterObj.mail_id"
            />
        <small class="text-muted font-12 ms-2">Note : If multiple Emails, separate with commas (,).</small>
        <!-- <Multiselect
          @open="EmployeeData"
          :options="EmpMailsList"
          v-model="filterObj.mail_id"
          placeholder="Select Mail Id"
          :multiple="false"
          class="font-11 multiselect"
          :searchable="true"
          openDirection="top"
          /> -->
      </div>

      <!-- Linked Checkbox and Linked Form -->
      <div class="col-md-6" v-if="route.query.preId">
        <div class="form-check d-flex align-items-center p-0 pe-3">
          <input
            class="form-check-input linketoCheck p-1"
            :disabled="filterObj.is_predefined_doctype == 1"
            type="checkbox"
            id="is_linked"
            v-model="filterObj.is_linked"
            :true-value="1"
            :false-value="0"
          />
          <label class="form-check-label font-12 mx-2 mb-0 ps-1" for="is_linked">
            Link
          </label>
        </div>
      </div>

      <div class="col-md-6" v-if="filterObj.is_linked">
        <label for="standardFormInput">Form</label>
        <input
          type="text"
          class="form-control standardFormInput"
          id="standardFormInput"
          :disabled="filterObj.is_predefined_doctype == 1"
          v-model="filterObj.is_linked_form"
          placeholder="Type to search Form Name..."
          @input="searchForm"
          @focus="showSuggestions = true"
          @blur="hideSuggestions"
        />
        <ul
          v-if="showSuggestions && filteredForms.length"
          class="list-group position-absolute w-100 z-3 formslist"
        >
          <li
            class="list-group-item formlistitem"
            v-for="(item, index) in filteredForms"
            :key="index"
            @mousedown.prevent="selectForm(item.name)"
          >
            {{ item.name }}
          </li>
        </ul>
      </div>
    </div>
  </div>
</div>

                        <div class="col-sm-none col-md-4"></div>
                      </div>
                    </div>
                  </div>

                  <!-- Questions in Form Step - NEW ZOHO-STYLE LAYOUT -->
                  <div v-if="activeStep === 2" class="zoho-form-builder">
                    <!-- Top Toolbar -->
                    <div class="zoho-toolbar">
                      <div class="toolbar-left">
                        <button @click="prevStep(1)" class="btn btn-sm btn-light">
                          <i class="bi bi-chevron-left"></i> Back
                        </button>
                      </div>

                      <!-- Tab Navigation -->
                      <div class="zoho-tabs">
                        <button
                          v-for="(block, index) in blockArr"
                          :key="index"
                          :class="['zoho-tab', { active: currentBuilderTab === index }]"
                          @click="currentBuilderTab = index">
                          <i class="bi bi-file-earmark-text me-1"></i>
                          {{ index === 0 ? 'Requestor Block' : `Approver Block ${index}` }}
                          <i v-if="blockArr.length > 1" class="bi bi-x-lg ms-2" @click.stop="removeBlock(index)"></i>
                        </button>
                      </div>

                      <div class="toolbar-right">
                        <button class="btn btn-sm btn-primary me-2" @click="addBlock">
                          <i class="bi bi-plus-lg me-1"></i>Add Block
                        </button>
                        <button v-if="isPreviewVisible" class="btn btn-sm btn-light me-2" @click="previewForm">
                          <i class="bi bi-eye me-1"></i>Preview
                        </button>
                        <button v-if="blockArr.length" class="btn btn-sm btn-dark" @click="saveFormData('save')">
                          {{ paramId !== "new" ? "Update Form" : "Create Form" }}
                        </button>
                      </div>
                    </div>

                    <!-- Main Builder Area -->
                    <div class="zoho-builder-container">
                      <!-- Left: Field Library -->
                      <aside :class="['zoho-field-library', { 'collapsed': !showFieldLibrary }]">
                        <div class="library-header" @click="showFieldLibrary = !showFieldLibrary">
                          <div class="d-flex align-items-center justify-content-between w-100">
                            <h6 class="mb-0 font-14 fw-bold">
                              <i class="bi bi-grid-3x3-gap me-2"></i>
                              {{ showFieldLibrary ? 'Field Types' : 'Fields' }}
                            </h6>
                            <button class="btn btn-sm btn-link p-0 text-dark">
                              <i :class="showFieldLibrary ? 'bi bi-chevron-left' : 'bi bi-chevron-right'"></i>
                            </button>
                          </div>
                        </div>

                        <div v-if="showFieldLibrary" class="library-content">
                          <SimpleFieldLibrary
                            :fields="fieldTypes"
                            @field-add="handleFieldAddFromLibrary"
                            @field-dragstart="handleFieldDragStart"
                            @field-dragend="handleFieldDragEnd"
                          />
                        </div>
                      </aside>

                      <!-- Center: Form Canvas -->
                      <div class="zoho-form-canvas">
                        <div class="canvas-inner" ref="mainBlockRef">
                          <!-- Current Block Content -->
                        <!-- Here is block level starts -->
                        <div class="block-level" v-for="(block, blockIndex) in blockArr" :key="blockIndex" v-show="blockIndex === currentBuilderTab">
                          <div class="requestandAppHeader">
                            <div class="d-flex justify-content-between align-items-center">
                              <div class=" ">
                                <h6 class="ps-2 mb-0 fw-bolder font-14 blockTitle">
                                  {{
                                    blockIndex === 0
                                      ? "Requestor Block"
                                      : `Approver
                                  Block ${blockIndex}
                                  `
                                  }}
                                  <!-- ${blockIndex++} -->
                                </h6>
                                  <div class="text-center ms-2 mt-1">
                                    <div v-if="blockIndex !== 0 && getWorkflowSetup(blockIndex).view_only_reportee || getWorkflowSetup(blockIndex).all_approvals_required || getWorkflowSetup(blockIndex).requester_as_a_approver" class="font-12 d-flex align-items-center">
                                      <!-- <span class="">
                                        <i class="bi bi-circle"></i>
                                      </span> -->
                                      <span class="font-12  approver_type_div">


                                      {{getWorkflowSetup(blockIndex).view_only_reportee === 1 ? 'Reporting Manager only' : ''}}
                                      {{getWorkflowSetup(blockIndex).all_approvals_required === 1 ? 'All of the selected approvers' : ''}}
                                      {{getWorkflowSetup(blockIndex).requester_as_a_approver === 1 ? 'Approval by Requestor' : ''}}
                                      </span>
                                      
                                      
                                      <span>
                                        <span class="ms-1">
                                          
                                          on rejection escalating to 
                                        </span>
                                          <span class="font-12 fw-bold">
                                        {{ getWorkflowSetup(blockIndex).on_rejection ? `Level ${getWorkflowSetup(blockIndex).on_rejection}` : 'Requestor' }}
                                          </span>

                                      </span>
                                      <span class="font-12 text-danger ms-1">
                                        {{ getWorkflowSetup(blockIndex).all_approvals_required === 1 ? '' : '(Skipping multi approval)' }}
                                        
                                      </span>


                                      
                                    </div>

                                  </div>
                              </div>
                              <div class="d-flex align-items-center">
                                <div v-if="paramId && workflowSetup.length" class="role-container">
                                  <label class="role-text d-flex align-items-center"
                                    v-if="getWorkflowSetup(blockIndex)">
                                    <span class="role-label fw-bold">
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
                                  canShowDesignationButton(blockIndex) &&
                                  paramId != undefined &&
                                  paramId != null &&
                                  paramId != 'new' &&
                                  getWorkflowSetup(blockIndex).roles.length === 0
                                " class="btn btn-light designationBtn d-flex align-items-center" type="button"
                                  data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight"
                                  aria-controls="offcanvasRight" @click="AddDesignCanvas(blockIndex)">
                                  <img src="../../assets/oui_app-users-roles.svg" alt="Add" class="me-1" />
                                  {{ blockIndex === 0 ? 'Add Requestors' :'Add Approvers' }}
                                  
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
                          <div class=" pt-0 section_block">
                            <div v-for="(section, sectionIndex) in block.sections" :key="'section-' + sectionIndex"
                              class="dynamicSection mt-0 section">
                              <section class="d-flex justify-content-between align-items-center">
                                <div class="d-flex flex-column">
                                  <input v-model="section.label" type="text" :class="[
                                    'border-less-input',
                                    'font-14',
                                    { 'italic-style': !section.label },
                                    { 'fw-medium': section.label },
                                  ]" @change="handleFieldChange(blockIndex, sectionIndex)" @input="handleFieldChange(blockIndex, sectionIndex)"
                                    placeholder="Untitled section" />
                                  <small v-if="section.errorMsg" class="text-danger ps-3 font-10">
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
                                    <label class="rownames m-0">{{
                                      getRowSuffix(rowIndex)
                                    }}</label>
                                    <div>
                                      <button v-if="row.columns.length < 3"
                                        class="btn btn-light bg-transparent border-0 p-1 font-12" @click="
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
                                              " @input="handleFieldChange(blockIndex,sectionIndex,rowIndex,columnIndex)" placeholder="Column Name" />
                                            <small v-if="column.errorMsg" class="text-danger ps-2 font-10">
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
                                        <div v-if="column.fields.length === 0" class="empty-drop-zone" @dragover.prevent
                                          @drop="(e) => handleFieldDropAtIndex(e, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)">
                                        </div>
                                        <div v-for="(field, fieldIndex) in column.fields" :key="'field-' + fieldIndex"
                                          @mouseenter="
                                            setHoveredField(
                                              blockIndex,
                                              sectionIndex,
                                              rowIndex,
                                              columnIndex,
                                              fieldIndex
                                            )
                                            " @mouseleave="resetHoveredField" class="dynamicField m-1 draggable-item"
                                          draggable="true"
                                          @dragstart="handleDragStart($event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)"
                                          @dragover.prevent
                                          @drop="handleFieldDropAtIndex($event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)">

                                          <div class="drop-zone" @dragover.prevent
                                            @drop="(e) => handleFieldDropAtIndex(e, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)">
                                          </div>

                                          <div v-if="field.fieldtype !== 'Table'" class="px-1 dynamic_fied field-border"
                                            draggable="true"
                                            @dragstart="handleDragStart($event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)"
                                            @dragover.prevent
                                            @drop="(e) => handleFieldDropAtIndex(e, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)">
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
                                                  " @input="handleFieldChange(blockIndex,sectionIndex,rowIndex,columnIndex,fieldIndex)" />
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
                                                    );
              handleFieldChange(blockIndex, sectionIndex, rowIndex, columnIndex);
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
                                                'Small Text'
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
                                            <div v-if="field.fieldtype === 'Link'">
                                             
  <label class="font-11 fw-light" :for="'link-search-' + getFieldKey(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)">
    Search Doctype:
  </label>

  <!-- Single Search + Select Input -->
  <input
    :id="'link-search-' + getFieldKey(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)"
    type="text"
    v-model="blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex].options"
    @input="fetchDoctypeList(blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex].options, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)"
    @focus="showDropdown(getFieldKey(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex))"
    class="form-control font-12 mb-1"
    placeholder="Type to search..."
  />

  <!-- Search Results Dropdown -->
  <ul
    v-if="linkSearchResults[getFieldKey(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)]?.length && dropdownVisible[getFieldKey(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)]"
    class="list-group mt-1"
    style="max-height: 200px; overflow-y: auto;"
  >
    <li
      v-for="(result, index) in linkSearchResults[getFieldKey(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)]"
      :key="index"
      @click="selectDoctype(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex, result.name)"
      class="list-group-item list-group-item-action"
    >
      {{ result.name }}
    </li>
  </ul>
</div>

  <!-- <label class="font-12 fw-light" :for="'link-search-' + getFieldKey(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)">
    Search Doctype:
  </label>

  
  <input
    :id="'link-search-' + getFieldKey(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)"
    type="text"
    v-model="linkSearchQueries[getFieldKey(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)]"
    @input="fetchDoctypeList(linkSearchQueries[getFieldKey(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)], blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)"
    @focus="showDropdown(getFieldKey(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex))"
    class="form-control font-12 mb-1"
    placeholder="Type to search..."
  />

  
  <ul
    v-if="linkSearchResults[getFieldKey(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)]?.length && dropdownVisible[getFieldKey(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)]"
    class="list-group mt-1"
    style="max-height: 200px; overflow-y: auto;"
  >
    <li
      v-for="(result, index) in linkSearchResults[getFieldKey(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)]"
      :key="index"
      @click="selectDoctype(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex, result.name)"
      class="list-group-item list-group-item-action"
    >
      {{ result.name }}
    </li>
  </ul>

  
  <input
    type="text"
    v-model="blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex].options"
    class="form-control font-12 mb-1"
    placeholder="Selected doctype will appear here"
    readonly
  />
</div> -->

                                              <!-- <input id="link-search" type="text" v-model="linkSearchQuery"
                                                @input="fetchDoctypeList(linkSearchQuery)"
                                                @focus="dropdownVisible = true" class="form-control font-12 mb-1"
                                                placeholder="Type to search..." />

                                              <ul v-if="linkSearchResults.length && dropdownVisible"
                                                class="list-group mt-1" style="max-height: 200px; overflow-y: auto;">
                                                <li v-for="(result, index) in linkSearchResults" :key="index"
                                                  @click="selectDoctype(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex, result.name)"
                                                  class="list-group-item list-group-item-action">
                                                  {{ result.name }}
                                                </li>
                                              </ul> -->


                                              <!-- <input type="text"
                                                v-model="blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex].options"
                                                class="form-control font-12 mb-1"
                                                :placeholder="linkSearchQuery ? 'Select from list' : 'Selected doctype will appear here'"
                                                readonly />
                                            </div>
                                            <div v-if="field.fieldtype === 'Table'">
                                              <label class="font-12 fw-light" for="link-search">Search Doctype:</label>
                                              <input id="link-search" type="text" v-model="linkSearchQuery"
                                                @input="fetchChildDoctypeList(linkSearchQuery)"
                                                @focus="dropdownVisible = true" class="form-control font-12 mb-1"
                                                placeholder="Type to search..." />

                                              <ul v-if="linkSearchResults.length && dropdownVisible"
                                                class="list-group mt-1" style="max-height: 200px; overflow-y: auto;">
                                                <li v-for="(result, index) in linkSearchResults" :key="index"
                                                  @click="selectDoctype(blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex, result.name)"
                                                  class="list-group-item list-group-item-action">
                                                  {{ result.name }}
                                                </li>
                                              </ul> -->


                                            <div class="d-flex  align-items-center justify-content-between">
                                              <div class=" d-flex align-items-center gap-2">
                                                <div class="d-flex align-items-center">

                                                  <input  class="font-12" v-model="field.reqd" :true-value="1" :id="'mandatory-' + blockIndex + '-' + sectionIndex + '-' + rowIndex + '-' + columnIndex + '-' + fieldIndex"
                                                    :false-value="0" placeholder="Field Name" type="checkbox" />
                                                  <!-- :id="'mandatory-' + blockIndex + '-' + sectionIndex + '-' + rowIndex + '-' + columnIndex + '-' + fieldIndex" -->
                                                </div>
                                                <div>
                                                  <label  class="font-12 m-0 fw-light" :for="'mandatory-' + blockIndex + '-' + sectionIndex + '-' + rowIndex + '-' + columnIndex + '-' + fieldIndex"
                                                   >Mandatory</label>
                                                   <!-- :for="'mandatory-' + blockIndex + '-' + sectionIndex + '-' + rowIndex + '-' + columnIndex + '-' + fieldIndex" -->
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
                                          <div class="drop-zone" @dragover.prevent
                                            @drop="(e) => handleFieldDropAtIndex(e, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex)">
                                          </div>
                                          <div class="childtableShow">
                                            <div>
                                              <div>
                                                <div class="mt-2">

                                                  <div v-if="field.fieldtype === 'Table'" class="childTableContainer">

                                                    <div v-for="(table, tableName) in childtableHeaders"
                                                      :key="tableName" class="childTable">
                                                      <h5 class=" font-13"
                                                        v-if="tableName === field.fieldname || tableName === field.options">
                                                        {{
                                                          tableName.replace(/_/g,
                                                            ' ') }}</h5>
                                                      <div
                                                        v-if="editMode[tableName] && tableName === currentEditingTable"
                                                        class=" d-flex align-items-center gap-2">
                                                        <!-- <div class="d-flex align-items-center">

                                                          <input class="font-12" v-model="field.description"
                                                            true-value="true" false-value="fasle" id="field-description"
                                                            placeholder="Field Name" type="text" />
                                                        </div>
                                                        <div>
                                                          <label  class="font-12 m-0 fw-light">Show as
                                                            Blocks</label>
                                                        </div> -->
                                                        <div class="d-flex align-items-center">
                                                <input v-if="field.showDescription" v-model="field.description"
                                                  class="form-control font-12 " placeholder="Enter field description" />
                                                <button class="btn btn-sm text-nowrap font-12"
                                                  @click="field.showDescription = !field.showDescription">
                                                  {{ field.showDescription ? 'Hide Description' : (field.description ?
                                                    'Edit Description'
                                                    : 'Add Description') }}
                                                </button>
                                            </div>
                                                      </div>
                                                      <table
                                                        v-if="tableName === field.options || tableName === field.fieldname"
                                                        class="table table-bordered rounded-table">
                                                        <thead>
                                                          <tr>
                                                            <th>#</th>
                                                            <th>Label</th>
                                                            <th>Field Type</th>
                                                            <!-- <th>Action</th> -->
                                                          </tr>
                                                        </thead>
                                                        <!-- :draggable="editMode[tableName]" -->
                                                        <tbody @dragover.prevent="onDragOver"
                                                          @drop="onDrop($event, table)">
                                                          <tr v-for="(field, index) in table" :key="index"
                                                            :draggable="editMode[tableName]"
                                                            @dragstart="onDragStart(index)" @dragend="onDragEnd"
                                                            :class="{ dragging: draggingIndex === index }">
                                                            <td>{{ index + 1 }}</td>

                                                            <!-- Label Input -->
                                                            <td v-if="editMode[tableName]">
                                                              <input
                                                                  v-model="field.label"
                                                                  @input="validateField(field, tableName, index)"
                                                                  placeholder="Field Label"
                                                                  class="form-control"
                                                                  :class="{ 'border-1 border-danger': fieldErrors[tableName]?.[index]?.length }"
                                                                />
                                                                <div v-if="fieldErrors[tableName]?.[index]?.length" class="text-danger font-11">
                                                                  <div v-for="(err, i) in fieldErrors[tableName][index]" :key="i">{{ err }}</div>
                                                                </div>

                                                            </td>
                                                            <td v-else>{{ field.label }}</td>

                                                            <!-- Field Type Select -->
                                                            <td v-if="editMode[tableName]">
                                                              <div class="d-flex gap-1">
                                                                <select v-model="field.fieldtype"
                                                                    @change="validateField(field, tableName, index)"
                                                                    class="form-select form-select-sm"
                                                                    :class="{ 'border-1 border-danger': fieldErrors[tableName]?.[index]?.length }">
                                                                  <option value="">Select Type</option>
                                                                  <option v-for="option in childfield" :key="option.type" :value="option.type">
                                                                    {{ option.label }}
                                                                  </option>
                                                                </select>

                                                                <div class=" d-flex">
                                                                  <div class=" d-flex align-items-center gap-2">

                                                                    <div class="d-flex align-items-center">
                                                                      <input class="font-12 form-control-sm"
                                                                        v-model="field.description"
                                                                        placeholder="description" type="text" />
                                                                    </div>
                                                                    <!-- <div>
                                                                      <label for="mandatory"
                                                                        class="font-12 m-0 fw-light">Calculate</label>
                                                                    </div> -->
                                                                  </div>
                                                                  <button class="btn btn-light btn-sm"
                                                                    @click="deleteRow(tableName, index)">
                                                                    <i class="bi bi-x-lg"></i>
                                                                  </button>
                                                                </div>
                                                              </div>
                                                              <div v-if="
                                                                [
                                                                  'Select'
                                                                ].includes(field.fieldtype)
                                                              ">
                                                                <label class="font-12 fw-light" for="options">Enter
                                                                  Options:</label>
                                                                <textarea id="options" placeholder="Enter your Options"
                                                              v-model="field.options"
                                                              @input="validateField(field, tableName, index)"
                                                              class="form-control shadow-none mb-1 font-12"></textarea>

                                                                <small v-if="
                                                                  !field.options ||
                                                                  field.options.trim() === ''
                                                                " class="text-danger font-10">
                                                                  Options are required for this field type.
                                                                </small>
                                                              </div>
                                                              <span v-if="invalidFields[tableName]?.includes(index)"
                                                                class="font-11 text-danger">Type required**</span>
                                                            </td>
                                                            <td v-else>{{ field.fieldtype }}</td>
                                                          </tr>
                                                        </tbody>
                                                      </table>

                                                      <!-- Show error message below the table if any fields are invalid -->
                                                      <!-- <div v-if="invalidFields[tableName]?.length" class="text-danger font-12 mt-2">
                                                    Please fill in the required fields in the highlighted rows.
                                                  </div> -->
                                                      <div
                                                        v-if="field.fieldtype === 'Table' && (field.label === tableName || field.fieldname === tableName)"
                                                        class="mb-2 mt-3">
                                                        <button class="btn btn-light btn-sm mx-2 "
                                                          @click="toggleEdit(tableName, field.description)">
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



                                            </div>
                                          </div>
                                        </div>
                                        <div class="drop-zone-bottom" @dragover.prevent
                                          @drop="handleFieldDropAtIndex($event, blockIndex, sectionIndex, rowIndex, columnIndex, column.fields.length)"
                                          style="background-color: #f0f0f0; border: 1px dashed #ccc; margin: 4px;">
                                        </div>

                                        <div class="drop-zone" @dragover.prevent
                                          @drop="(e) => handleFieldDropAtIndex(e, blockIndex, sectionIndex, rowIndex, columnIndex, fields.length)"
                                          style="height: 10px; background-color: transparent" />
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
                                <div>
                                  <div v-for="(table, tableIndex) in section.afterCreated" :key="tableIndex"
                                    class="childTable dynamicColumn m-0 p-2 ">
                                    <h5 class="font-13">{{ table.tableName }}</h5>
                                    <div v-if="editMode[table.tableName]" class=" d-flex align-items-center gap-2">
                                      <!-- <div class="d-flex align-items-center">

                                        <input class="font-12" v-model="table.description" true-value="true" 
                                          false-value="fasle" placeholder="Field Name" type="text" />
                                      </div>
                                      <div>
                                        <label class="font-12 m-0 fw-light">Show as
                                          Blocks</label>
                                      </div> -->
                                       <div class="d-flex align-items-center">
                                                <input v-if="table.showDescription" v-model="table.description"
                                                  class="form-control font-12 " placeholder="Enter field description" />
                                                <button class="btn btn-sm text-nowrap font-12"
                                                  @click="table.showDescription = !table.showDescription">
                                                  {{ table.showDescription ? 'Hide Description' : (table.description ?
                                                    'Edit Description'
                                                    : 'Add Description') }}
                                                </button>
                                            </div>
                                    </div>

                                    <table class="table table-bordered rounded-table">
                                      <thead>
                                        <tr>
                                          <th>#</th>
                                          <th>Label</th>
                                          <th>Field Type</th>
                                        </tr>
                                      </thead>
                                      <tbody>
                                        <tr v-for="(field, index) in table.columns" :key="index">
                                          <td>{{ index + 1 }}</td>

                                          <!-- Label Input -->
                                          <td v-if="editMode[table.tableName]">
                                           <input
 v-model="field.label"
  placeholder="Field Label"
  class="form-control"
  @blur="field.label = field.label?.trim(); validateTableField(field, table.tableName, index, table.columns)"
  :class="{ 'border-1 border-danger': invalidFields[table.tableName]?.includes(index) }"
/>

<div v-if="fieldErrors[table.tableName]?.[index]" class="text-danger font-11 mt-1">
  <span v-for="(msg, i) in fieldErrors[table.tableName][index]" :key="i">{{ msg }} <br/></span>
</div>

                                          </td>
                                          <td v-else>{{ field.label }}</td>

                                          <!-- Field Type Select -->
                                          <td v-if="editMode[table.tableName]">
                                            <div class="d-flex gap-1 align-items-center">
                                              <select
                                                v-model="field.fieldtype"
                                                class="form-select form-select-sm"
                                                 @change="validateTableField(field, table.tableName, index, table.columns)"
  :class="{ 'border-1 border-danger': invalidFields[table.tableName]?.includes(index) }"
                                              >
                                                <option value="">Select Type</option>
                                                <option v-for="option in childfield" :key="option.type" :value="option.type">
                                                  {{ option.label }}
                                                </option>
                                              </select>

                                              <button class="btn btn-light btn-sm" @click="afterImmediateEditdeleteRow(blockIndex, sectionIndex, table.tableName, index)">
                                                <i class="bi bi-x-lg"></i>
                                              </button>
                                            </div>

                                            <!-- Options for Select type -->
                                            <div v-if="field.fieldtype === 'Select'" class="mt-1">
                                              <label class="font-12 fw-light" for="options">Enter Options:</label>
                                              <textarea
                                                id="options"
                                                placeholder="Enter your Options"
                                                v-model="field.options"
                                                class="form-control shadow-none mb-1 font-12"
                                                @input="validateTableField(field, table.tableName, index,table.columns)"
                                              ></textarea>
                                            </div>

                                           <div v-if="fieldErrors[table.tableName]?.[index]" class="text-danger font-11 mt-1">
  <span v-for="(msg, i) in fieldErrors[table.tableName][index]" :key="i">{{ msg }}<br/></span>
</div>
                                          </td>
                                          <td v-else>{{ field.fieldtype }}</td>
                                        </tr>
                                      </tbody>

                                    </table>

                                    <!-- Edit/Add buttons -->
                                    <div class="mb-2">
                                      <button class="btn btn-light btn-sm mx-2"
                                        @click="afterImmediateEdit(blockIndex, sectionIndex, table.tableName)">
                                        {{ editMode[table.tableName] ? 'Save' : 'Edit' }}
                                      </button>
                                      <button class="btn btn-light btn-sm" v-if="editMode[table.tableName]"
                                        @click="afterImmediateEditaddNewFieldedit(blockIndex, sectionIndex, table.tableName)">
                                        Add More Field
                                      </button>
                                    </div>
                                  </div>
                                </div>
                              </div>
                              <div>
                                <div>

                                  <button v-if="blockIndex==0" class="btn btn-light addRow mb-3 mt-4"
                                    @click="addChildTable(blockIndex, sectionIndex)">
                                    Add New Table
                                  </button>
                                  <div v-for="(table, tableIndex) in section.childTables"
                                    :key="`table-${blockIndex}-${sectionIndex}-${tableIndex}`" class="child-table">
                                    <div v-if="table.newTable">
                                      <div class="d-flex justify-content-between align-items-center mt-1 mb-2">
                                        <div>
                                          <span :class="table.tableName ? 'd-none' : 'text-danger'">*</span>
                                          <input v-model="table.tableName" placeholder="Table Name"
                                            @blur="updateFieldname(table)"
                                            class="border-less-input font-14 p-0 inputHeight" :class="{
                                              'italic-style': !table.tableName,
                                              'fw-medium': table.tableName,
                                            }" />
                                          <div
                                            v-if="fieldErrors[`${blockIndex}-${sectionIndex}-${tableIndex}`]?.tableName"
                                            class="text-danger font-12">
                                            {{ fieldErrors[`${blockIndex}-${sectionIndex}-${tableIndex}`].tableName }}
                                          </div>
                                          <div v-if="tableExistsMessage" class="text-danger font-12">
                                            {{ tableExistsMessage }}
                                          </div>
                                          <div class=" d-flex align-items-center gap-2">
                                            <div class="d-flex align-items-center">
                                                <input v-if="table.showDescription" v-model="table.as_a_block"
                                                  class="form-control font-12 " placeholder="Enter field description" />
                                                <button class="btn btn-sm text-nowrap font-12"
                                                  @click="table.showDescription = !table.showDescription">
                                                  {{ table.showDescription ? 'Hide Description' : (table.description ?
                                                    'Edit Description'
                                                    : 'Add Description') }}
                                                </button>
                                            </div>
                                            <!-- <div>
                                              <label class="font-12 m-0 fw-light">Show as Blocks</label>
                                            </div> -->
                                          </div>
                                        </div>
                                        <button class="btn btn-light bg-transparent border-0 font-13 deleteSection"
                                          @click="removeChildTable(blockIndex, sectionIndex, tableIndex)">
                                          <i class="bi bi-trash"></i> Remove Table
                                        </button>
                                      </div>

                                      <div v-for="(field, fieldIndex) in table.columns" :key="fieldIndex"
                                        class="dynamicField">
                                        <div class="px-1 field-border">
                                          <div class="d-flex justify-content-between">
                                            <div>
                                              <span :class="field.label ? 'd-none' : 'text-danger'">*</span>
                                              <input v-model="field.label" placeholder="Name the field"
                                              @blur="() => { 
  updateFieldname(field); 
  validateFieldLabel(field, blockIndex, sectionIndex, tableIndex, fieldIndex, table.columns); 
}"

                                                class="border-less-input font-14 p-0 inputHeight" :class="{
                                                  'italic-style': !field.label,
                                                  'fw-medium': field.label,
                                                  'is-invalid': fieldErrors[`${blockIndex}-${sectionIndex}-${tableIndex}`]?.columns?.[fieldIndex]?.label
                                                }" />
                                              <div
                                                v-if="fieldErrors[`${blockIndex}-${sectionIndex}-${tableIndex}`]?.columns?.[fieldIndex]?.label"
                                                class="text-danger font-12">
                                                {{
                                                  fieldErrors[`${blockIndex}-${sectionIndex}-${tableIndex}`].columns[fieldIndex].label
                                                }}
                                              </div>
                                            </div>
                                            <div class="d-flex align-items-center">
                                              <!-- <div class=" d-flex align-items-center gap-2">
                                                <div class="d-flex align-items-center">
                                                                      <input class="font-12 form-control-sm" v-model="field.description"
                                                                        placeholder="Description"
                                                                        type="text" />  
                                                                    </div>
                                                <div>
                                                  <label for="mandatory" class="font-12 m-0 fw-light">Calculate</label>
                                                </div>
                                              </div> -->
                                              <div class=" d-flex my-1">

                                                <input v-if="field.showDescription" v-model="field.description"
                                                  class="form-control font-12 " placeholder="Enter field description" />
                                                <button class="btn btn-sm text-nowrap font-12"
                                                  @click="field.showDescription = !field.showDescription">
                                                  {{ field.showDescription ? 'Hide Description' : (field.description ?
                                                    'Edit Description'
                                                    : 'Add Description') }}
                                                </button>
                                              </div>

                                              <button class="btn btn-sm trash-btn py-0"
                                                @click="removeFieldFromTable(blockIndex, sectionIndex, tableIndex, fieldIndex)">
                                                <i class="bi bi-x-lg"></i>
                                              </button>
                                            </div>
                                          </div>

                                          <select v-model="field.fieldtype" class="form-select font-13 mb-1"
                                            :class="{ 'is-invalid': fieldErrors[`${blockIndex}-${sectionIndex}-${tableIndex}`]?.columns?.[fieldIndex]?.fieldtype }">
                                            <option value="">Select Type</option>
                                            <option v-for="section in childfield" :key="section.type"
                                              :value="section.type">
                                              {{ section.label }}
                                            </option>
                                          </select>
                                          <div v-if="
                                            [
                                              'Select'
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
                                          <div
                                            v-if="fieldErrors[`${blockIndex}-${sectionIndex}-${tableIndex}`]?.columns?.[fieldIndex]?.fieldtype"
                                            class="text-danger font-12">
                                            {{
                                              fieldErrors[`${blockIndex}-${sectionIndex}-${tableIndex}`].columns[fieldIndex].fieldtype
                                            }}
                                          </div>
                                        </div>
                                      </div>

                                      <button class="btn btn-light btn-sm addField mx-1"
                                        @click="addFieldToTable(blockIndex, sectionIndex, tableIndex)">
                                        <i class="bi bi-plus"></i> Add Field
                                      </button>

                                      <button class="btn btn-dark btn-sm font-12 mx-1"
                                        @click="processFields(blockIndex, sectionIndex, tableIndex)">
                                        Create Table
                                      </button>

                                      <hr />
                                    </div>
                                  </div>
                                </div>
                              </div>

                              <div class="d-flex justify-content-center align-items-center py-2 add-section-btn">
                                <button class="btn btn-light border font-12"
                                  @click="addSection(blockIndex, sectionIndex)">
                                  <i class="bi bi-plus-circle me-1 fs-6"></i> Add Section
                                </button>
                              </div>
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


                            </div>
                          </div>
                        </div>

                        <!-- Add Approval Block button removed - use tabs instead -->
                      </div>
                      <!-- End Canvas Inner -->
                    </div>
                    <!-- End Zoho Form Canvas -->

                      <!-- Right: Field Properties Panel (Optional - for future enhancement) -->
                      <aside class="zoho-properties-panel" v-if="selectedFieldForEdit">
                        <div class="properties-header">
                          <h6 class="mb-0">Field Properties</h6>
                          <button class="btn btn-sm btn-link p-0" @click="selectedFieldForEdit = null">
                            <i class="bi bi-x-lg"></i>
                          </button>
                        </div>
                        <div class="properties-content">
                          <!-- Field properties will go here -->
                          <p class="text-muted small">Select a field to edit its properties</p>
                        </div>
                      </aside>
                    </div>
                    <!-- End Zoho Builder Container -->
                  </div>
                  <!-- End Zoho Form Builder -->

                  <div v-if="activeStep === 3">
                    <div class="stepperbackground d-flex align-items-center justify-content-end gap-2 ">

                      <div>
                        <button class="btn btn btn-light previewBtn font-13" data-bs-toggle="modal"
                          data-bs-target="#customFormatModal">Print Format
                        </button>

                      </div>
                      <div>
                        <!-- <button class="download_btn font-13 " @click="downloadPdf"><i
                            class="bi bi-download me-2"></i>Download
                          Pdf</button> -->
                      </div>
                    </div>
                    <FormPreviewComp :blockArr="selectedform" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="modal fade" id="customFormatModal" tabindex="-1" aria-labelledby="customFormatModalLabel"
      aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title" id="customFormatModalLabel">Print Format</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
                <label for="">Form Name</label>
            <input v-model="printFormatID" :multiple="false" :placeholder="route.query.id" class="font-11 form-control " id="Form_name_print"
              :searchable="true" />
            <div class=" d-flex align-items-center gap-2">
              <div class="d-flex align-items-center py-2">

                <input  class="font-12" v-model="is_landscape" :true-value="1" :false-value="0" placeholder="Field Name"
                  type="checkbox" />
              </div>
              <div>
                <label for="mandatory" class="font-12 fw-bold m-0 fw-light">Print Landscape Mode</label>
              </div>
            </div>


          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal">Close</button>
            <button type="button" class="btn btn-dark " @click="SetPrintFormatFn">Add Print Format</button>
          </div>
        </div>
      </div>
    </div>

    <div class="offcanvas addOffCanvas offcanvas-end" tabindex="-1" id="offcanvasRight"
      aria-labelledby="offcanvasRightLabel">
      <div class="offcanvas-header add_designationHeader">
        <span id="offcanvasRightLabel" class="font-14 fw-bold">

          {{ selectedBlockIndex == 0 ? "Add designation for Requestors" : `Approval Settings For
          Level-${selectedBlockIndex}`
          }}
        </span>

        <button type="button" class="btn-close bg-light text-reset" data-bs-dismiss="offcanvas"
          aria-label="Close"></button>
      </div>
      <div class="offcanvas-body add_desig_offCanvas_body p-0">
        <div class="">
          <div class="">
            
           



            <div v-if="selectedBlockIndex !== 0"
              class=" p-3 approval-border-bottom ">
              <!-- <div class="d-flex gap-1">

                <div class="px-2 mt-2 d-flex align-items-center user-select-none">
                  <input v-model="approval_required" type="checkbox" :true-value="1" :false-value="0" id="Approver"  class="me-2 m-0 form-check-input designationCheckBox" />
                  <label for="Approver" class="m-0">Approval Mandatory</label>
                </div>
                <div v-if="allowEditSettingType === true" class="px-2 mt-2 d-flex align-items-center user-select-none">
                  <input
                    v-model="approver_can_edit"
                    type="checkbox"
                    :true-value="1"
                    :false-value="0"
                    id="approver_can_edit"
                    class="me-2 m-0 form-check-input designationCheckBox"
                  />
                  <label for="approver_can_edit" class="m-0">
                  Allow to Edit
                  </label>
              
                </div>
              </div>  -->

               <div v-if="selectedBlockIndex !== 0" class=" ">
              <label class="fw-bold font-12 mb-2">Approver Type</label>
              <select v-model="selectedApproverType" class="form-select shadow-none font-12 ">
                <option value="">Any one of the selected approvers</option>
                <option value="ViewOnlyReportee">Reporting Manager only</option>
                <option value="all_approvals_required">All of the selected approvers</option>
                <option value="requester_as_a_approver">Approval by Requestor</option>
              </select>
            </div>

              <!-- <div>
                <div class=" form-control" aria-disabled="">

                  <span class=" font-12">Approver Level {{ selectedBlockIndex }}</span>
                </div>
              </div> -->
             
          

            </div>
            

          </div>

        </div>
          <!-- <input v-model="searchDesignation" class="SearchDesignation rounded-2 form-control shadow-none my-1"
            type="text" placeholder="Search Designation" />
            <span class="font-12 SelectallDesignation ps-2  ">Selected Designations ({{ designationValue.length }})</span> -->

              <!-- :disabled="ViewOnlyReportee"  -->
          <!-- <div class="form-check ps-1 mt-3" v-if="DesignationList.length">
            <div>
              <input type="checkbox" id="selectAll" v-model="isAllSelected"
                class="me-2 mt-0 designationCheckBox form-check-input" />
              <label for="selectAll" class="SelectallDesignation fw-bold mx-2 form-check-label">Select all</label>
            </div>

          </div> -->
          <!-- Selected Items Display -->
          <!-- <div v-if="designationValue.length" class="d-flex flex-wrap gap-2 mt-3">
            <span v-for="(selected, i) in designationValue" :key="i"
              class="badge bg-secondary d-flex align-items-center">
              <label for="" class="font-12">

              {{ selected }}
              </label> 
              <button type="button" class="btn-close btn-close-white ms-2" aria-label="Remove"
                @click="removeDesignation(selected)" style="font-size: 0.6rem;"></button>
            </span>
          </div> -->
         <div class="px-3 listofdesignations">
    <div class="my-1 d-flex justify-content-between">
      <span class="font-12 fw-bold">
        Select {{ selectedBlockIndex === 0 ? "Requestors" : "Approvers" }}
      </span>
      <span class="italic-style text-secondary font-12">
        {{ designationValue.length }} Selected
      </span>
    </div>

    <div ref="resizableDiv" class="my-1 disgnationlist_div" v-if="DesignationList.length">
      <div class="d-flex align-items-center justify-content-between gap-1">
        <!-- ✅ Select All -->
        <div class="form-check ps-1 d-flex align-items-center m-0">
          <input
            type="checkbox"
            id="selectAll"
            :checked="isAllSelected"
            @change="toggleSelectAll"
            class="form-check-input me-2 designationCheckBox"
          />
          <label
            for="selectAll"
            class="form-check-label SelectallDesignation mt-2 fw-bold"
          >
            Select all designation ({{ filteredDesignationList.length }})
          </label>
        </div>

        <!-- ✅ Show HODs -->
        <div v-if="selectedBlockIndex !== 0" class="form-check d-flex align-items-center m-0">
          <input
            type="checkbox"
            id="showHods"
            v-model="showHods"
            class="form-check-input me-2 designationCheckBox"
          />
          <label for="showHods" class="form-check-label mt-2 fw-bold">
            Show HODs Only
          </label>
        </div>

        <!-- ✅ Clear All -->
        <div>
          <button v-if="designationValue.length"
            type="button"
            class="btn btn-sm font-12 text-danger"
            @click="clearall_designations"
          >
            <i class="bi bi-x"></i> Clear all
          </button>
        </div>
      </div>

      <!-- ✅ Multi-select -->
      <Vue3Select
        v-if="DesignationList.length"
        :multiple="true"
        v-model="designationValue"
        :options="filteredDesignationList"
        :close-on-select="false"
        :clear-search-on-select="true"
        placeholder="Search & Select Designations"
      />
    </div>

    <div v-else>
      <div class="d-flex justify-content-center">
        <span>No Designations Found</span>
      </div>
    </div>
  </div>
         <div v-if="selectedBlockIndex !== 0 " class="p-3">
              <div>
                <label for="" class="fw-bold font-12 ">On Rejection</label>
              </div>
                <select v-model.number="OnRejection" class="form-select shadow-none font-12 mt-1  me-2">
                  <!-- <option disabled value="">Select Lower Level</option> -->
                  <option v-for="level in lowerApproverLevels" :key="level" :value="level">
                    {{ level === 0 ? 'Requestor' : 'Approver Level ' + level }}
                  </option> 
                </select>
              </div>
              <div v-if="selectedBlockIndex !== 0 ">
                <div class="">

                <div class="px-4 py-1 mt-2 d-flex align-items-center user-select-none">
              <input v-model="approval_required" type="checkbox" :true-value="1" :false-value="0" id="Approver"  class="me-2 m-0 form-check-input designationCheckBox" />
              <label for="Approver" class="m-0">Approval Mandatory</label>
            </div>
            <div v-if="allowEditSettingType === true" class="px-4 py-1 mt-2 d-flex align-items-center user-select-none">
              <input
                v-model="approver_can_edit"
                type="checkbox"
                :true-value="1"
                :false-value="0"
                id="approver_can_edit"
                class="me-2 m-0 form-check-input designationCheckBox"
              />
              <label for="approver_can_edit" class="m-0">
               Allow this approver to edit the form
              </label>
              
              </div>
            </div>
              </div>

      </div>

      <div class="offcanvas-footer">
        <div class="text-end p-3">
          
          
          <div>

          <ButtonComp class="btn btn-dark addingDesignations" data-bs-dismiss="offcanvas" @click="addDesignationBtn"
            :name="selectedBlockIndex === 0 ? 'Add Requestor':'Add Approvers'" />
        </div>
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
// import { toast } from "vue3-toastify";
// import "vue3-toastify/dist/index.css";
// import { nextTick } from "vue";
import { useDragAndDrop } from "../../shared/services/draggable";
import FormPreviewComp from "../../Components/FormPreviewComp.vue";
import { showError, showInfo, showSuccess } from "../../shared/services/toast";
import Vue3Select from 'vue3-select'
import 'vue3-select/dist/vue3-select.css';

// Drag-and-Drop Field Library
import SimpleFieldLibrary from "../../Components/FormBuilder/SimpleFieldLibrary.vue";

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
const ViewOnlyReportee = ref(false);
const all_approvals_required = ref(false);
const requester_as_a_approver = ref(false);
const OnRejection = ref('');
const approval_required=ref('');
const approver_can_edit=ref('');
const wrkAfterGetData = ref([]);
// const hasWorkflowToastShown = ref(false);
const tableFieldsCache = ref([]);
const fieldErrors = reactive({});
// const childtableRows = ref([]);
const childtableHeaders = ref([]);
const allowEditSettingType = ref(false);
// const childtableName = ref("");
// const childTableresponseData = ref([]);
const filteredForms = ref([]);
const showSuggestions = ref(false);
let debounceTimeout = null;
const tableName = ref("");
let paramId = ref("");

// Drag-and-Drop State
const draggedFieldType = ref(null);
const selectedFieldForEdit = ref(null);
const showFieldLibrary = ref(true);

// Zoho-style Tab State
const currentBuilderTab = ref(0);

const businessUnit = computed(() => {
  return EzyBusinessUnit;
});
const childtableShow = ref(false);
const columns = reactive([]);
const selectedData = ref({
  routepath: route.query.routepath,
  business_unit: route.query.business_unit,
  formId: route.query.id

});
const printFormatID = ref('')
const is_landscape = ref(false)
const showHods = ref(false);

const formTypeOptions = [
  { label: "Public", value: 1 },
  { label: "Private", value: 0 },
];

const selectedFormType = computed({
  get() {
    // This returns the option object that matches filterObj.as_web_view
    return formTypeOptions.find(
      (opt) => opt.value === filterObj.value.as_web_view
    );
  },
  set(selected) {
    // 👇 This line updates filterObj.as_web_view every time user selects a new option
    filterObj.value.as_web_view = selected ? selected.value : null;
  },
});


// const computedDisabled = computed(() => {
//   return paramId.value.length > 0
// })
const formNameModel = computed({
  get() {
    return filterObj.value.form_name || route.query.form_name || "";
  },
  set(val) {
    filterObj.value.form_name = val;
  }
});

// const mailInput = ref("");
// function updateMailArray() {
//   // Split input by commas, trim spaces, and remove empty entries
//   filterObj.value.mail_id = mailInput.value
//     .split(",")
//     .map(email => email.trim())
//     .filter(email => email);
// }

const filterObj = ref({
  form_name: "",
  form_short_name: "",
  accessible_departments: [],
  business_unit: `${businessUnit.value.value || selectedData.value.business_unit || route.query.business_unit}`,
  form_category: "",
  owner_of_the_form: "",
  series: "",
  has_workflow: "",
  workflow_check: "",
  is_linked: 0,
  is_linked_form: "",
  is_predefined_doctype: route.query.id ? 1 : 0,
  as_web_view: 0,
  mail_id: "",


});
// route.query.preId ? 1: 0

watch(
  () => route.query.form_name,
  (newVal) => {
    if (newVal) {
      filterObj.value.form_name = newVal;
      filterObj.value.form_short_name = newVal;
    }
  },
  { immediate: true }
);
const restrictedLabels = [
  "name", "parent", "creation", "owner", "modified", "modified_by",
  "parentfield", "parenttype", "file_list", "flags", "docstatus","idx", "doctype","company_field","business_unit"
].map(label => label.toLowerCase().trim());

const excludedLabels = ["Approver", "Approved on", "Approved By"].map(label => label.toLowerCase().trim());
function generateFieldname(label) {
  return label.toLowerCase().replace(/\s+/g, '_').replace(/[^\w_]/g, '');
}
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

function canShowDesignationButton(blockIndex) {
  if (paramId === undefined || paramId === null || paramId === 'new') return false;

  const roles = getWorkflowSetup(blockIndex).roles;

  // First approver (blockIndex = 0)
  if (blockIndex === 0) {
    return roles.length === 0;
  }

  const prevRoles = getWorkflowSetup(blockIndex - 1).roles;
  return (
    prevRoles.length > 0 &&
    prevRoles[0] !== null &&
    prevRoles[0] !== '' &&
    roles.length === 0
  );
}
function removeDesignation(item) {
  const index = designationValue.value.indexOf(item);
  if (index !== -1) {
    designationValue.value.splice(index, 1);
  }
}
// Watch and trim spaces
watch(() => filterObj.value.form_name, (newVal) => {
  filterObj.value.form_name = newVal.trim()
})

watch(() => filterObj.value.form_short_name, (newVal) => {
  filterObj.value.form_short_name = newVal.trim()
})
watch(() => filterObj.value.series, (newVal) => {
  filterObj.value.series = newVal.trim()
})

const draggedField = ref(null);

const handleDragStart = (event, blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex) => {
  draggedField.value = {
    blockIndex,
    sectionIndex,
    rowIndex,
    columnIndex,
    fieldIndex,
  };
};

const handleFieldDropAtIndex = (
  event,
  targetBlock,
  targetSection,
  targetRow,
  targetColumn,
  insertIndex
) => {
  event.preventDefault();
  event.stopPropagation();

  console.log('Field dropped at index:', {
    targetBlock,
    targetSection,
    targetRow,
    targetColumn,
    insertIndex,
    draggedField: draggedField.value,
    draggedFieldType: draggedFieldType.value
  });

  // Check if we're dragging from the field library
  if (draggedFieldType.value) {
    console.log('Dropping from field library:', draggedFieldType.value);

    // Create new field from Frappe fieldtype
    const newField = createFieldFromFrappeType(draggedFieldType.value);

    if (!newField) {
      console.error('Failed to create field from type:', draggedFieldType.value);
      return;
    }

    // Get target location
    const currentBlock = blockArr[targetBlock];
    if (!currentBlock) {
      showError('Target block not found');
      return;
    }

    // Ensure sections exist
    if (!currentBlock.sections) {
      currentBlock.sections = [];
    }

    if (!currentBlock.sections[targetSection]) {
      currentBlock.sections[targetSection] = {
        label: '',
        rows: []
      };
    }

    // Ensure rows exist
    if (!currentBlock.sections[targetSection].rows) {
      currentBlock.sections[targetSection].rows = [];
    }

    if (!currentBlock.sections[targetSection].rows[targetRow]) {
      currentBlock.sections[targetSection].rows[targetRow] = {
        label: '',
        columns: []
      };
    }

    // Ensure columns exist
    if (!currentBlock.sections[targetSection].rows[targetRow].columns) {
      currentBlock.sections[targetSection].rows[targetRow].columns = [];
    }

    if (!currentBlock.sections[targetSection].rows[targetRow].columns[targetColumn]) {
      currentBlock.sections[targetSection].rows[targetRow].columns[targetColumn] = {
        label: '',
        fields: []
      };
    }

    const targetFields = currentBlock.sections[targetSection].rows[targetRow].columns[targetColumn].fields;

    // Insert field at specific index
    targetFields.splice(insertIndex, 0, newField);

    console.log('Field added successfully:', newField);
    showSuccess(`${newField.label} field added`);

    // Clear dragged field type
    draggedFieldType.value = null;
    return;
  }

  // Handle existing field reordering
  if (!draggedField.value) {
    console.log('No dragged field found');
    return;
  }

  const {
    blockIndex: fromBlock,
    sectionIndex: fromSection,
    rowIndex: fromRow,
    columnIndex: fromColumn,
    fieldIndex: fromFieldIndex,
  } = draggedField.value;

  const fromFields =
    blockArr[fromBlock].sections[fromSection].rows[fromRow].columns[fromColumn].fields;

  const targetFields =
    blockArr[targetBlock].sections[targetSection].rows[targetRow].columns[targetColumn].fields;

  // Avoid self-drop at same position
  if (
    fromBlock === targetBlock &&
    fromSection === targetSection &&
    fromRow === targetRow &&
    fromColumn === targetColumn &&
    fromFieldIndex === insertIndex
  ) return;

  // Remove dragged field
  const movedField = fromFields.splice(fromFieldIndex, 1)[0];

  // Adjust insert index if dragging within same list and moving forward
  if (
    fromFields === targetFields &&
    fromFieldIndex < insertIndex
  ) {
    insertIndex--;
  }

  // Insert at new position
  targetFields.splice(insertIndex, 0, movedField);

  draggedField.value = null;
};

const tableExistsMessage = ref('');
const GetDoctypeList = async (searchText) => {
  const filters = [
    ["module", "in", ["User Forms"]],
    ["istable", "=", 1],
  ];

  if (searchText?.trim()) {
    filters.push(["name", "=", `${searchText}`]);
  }

  const queryParams = {
    fields: JSON.stringify(["name"]),
    filters: JSON.stringify(filters),
    limit_page_length: "None",
    doctype:doctypes.doctypesList,
  };

  try {
    const res = await axiosInstance.get(apis.GetDoctypeData, { params: queryParams });
    return res.message.data || [];
  } catch (error) {
    console.error("Error fetching doctype list:", error);
    return [];
  }
};

const matched = ref(null)

const updateFieldname = async (field) => {
  tableExistsMessage.value = ''; // reset message
  matched.value = null; // reset matched

  if (field.tableName) {
    // 🚀 Remove leading/trailing spaces
    let searchText = field.tableName.trim();

    // 🚨 Condition 1: Check length
    if (searchText.length > 64) {
      tableExistsMessage.value = 'Table name cannot exceed 64 characters';
      return;
    }

    // 🚨 Condition 2: Only letters and spaces allowed in the middle
    const validNameRegex = /^[a-zA-Z]+( [a-zA-Z]+)*$/;
    if (!validNameRegex.test(searchText)) {
      tableExistsMessage.value = 'Table name can only contain letters and spaces (no leading/trailing spaces or special characters)';
      return;
    }

    // Check if table already exists
    const existing = await GetDoctypeList(searchText);
    matched.value = existing.find(item => item.name.toLowerCase() === searchText.toLowerCase());

    if (matched.value) {
      tableExistsMessage.value = 'Table already exists';
    }

    // Update field.tableName with trimmed version
    field.tableName = searchText;
  }

  // Auto-generate fieldname from label
  if (field.label) {
    field.fieldname = generateFieldname(field.label);
  }
};




function searchForm() {
  const searchValue = filterObj.value.is_linked_form;
  if (!searchValue) {
    filteredForms.value = [];
    return;
  }

  // Debounce to avoid too many API calls
  clearTimeout(debounceTimeout);
  debounceTimeout = setTimeout(() => {
    const filters = [
      ["business_unit", "=", `${businessUnit.value.value}`],
      ["name", "like", `%${searchValue}%`]
    ];

    const queryParams = {
      fields: JSON.stringify(["name"]),
      limit_page_length: 10,
      limit_start: 0,
      filters: JSON.stringify(filters),
      doctype:doctypes.EzyFormDefinitions,
      order_by: "`tabEzy Form Definitions`.`enable` DESC, `tabEzy Form Definitions`.`creation` DESC"
    };

    axiosInstance
      .get(`${apis.GetDoctypeData}`, { params: queryParams })
      .then((response) => {
        filteredForms.value = response.message.data || [];
      })
      .catch((error) => {
        console.error("Error fetching form definitions:", error);
      });
  }, 300); // ✅ Debounce delay 300ms
}

// ✅ Select item from suggestion
function selectForm(name) {
  filterObj.value.is_linked_form = name;
  showSuggestions.value = false;
}

// ✅ Hide suggestions when input loses focus (small delay to allow click)
function hideSuggestions() {
  setTimeout(() => {
    showSuggestions.value = false;
  }, 200);
}
// const linkSearchQuery = ref('');
// const linkSearchResults = ref([]);
// const dropdownVisible = ref(false); // Controls dropdown visibility

// function fetchDoctypeList(searchText) {
//   const filters = [
//     ['module', 'in', ['User Forms', 'Ezy Forms', 'Ezy Flow']],
//   ];

//   if (searchText?.trim()) {
//     filters.push(['name', 'like', `%${searchText}%`]);
//   }

//   const queryParams = {
//     fields: JSON.stringify(['name']),
//     filters: JSON.stringify(filters),
//     limit_page_length: '10',
//   };

//   axiosInstance
//     .get(apis.resource + doctypes.doctypesList, { params: queryParams })
//     .then((res) => {
//       console.log("Fetched response:", res);  // Check the whole response
//       console.log("Fetched data:", res.data); // Check if `data` exists directly
//       linkSearchResults.value = res.data || [];
//     })
//     .catch((error) => {
//       console.error('Error fetching doctype list:', error);
//     });
// }

// const selectDoctype = (blockIndex, sectionIndex, rowIndex, columnIndex, fieldIndex, doctypeName) => {
//   // Access the specific field in the nested structure
//   const field = blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex].fields[fieldIndex];

//   // Update the field's value with the selected doctype
//   field.options = doctypeName;

//   // Hide the dropdown after selecting a doctype
//   dropdownVisible.value = false;

//   // Optionally reset the search query or show the selected name
//   linkSearchQuery.value = doctypeName;
// };


// const linkSearchResults = ref([]);
const activeSearch = reactive({
  query: '',
  key: '', // A unique key to match the field
});

// Create a unique key based on all indices
function getFieldKey(b, s, r, c, f) {
  return `${b}-${s}-${r}-${c}-${f}`;
}
const linkSearchQueries = reactive({});
const linkSearchResults = reactive({});
const dropdownVisible = reactive({});

// Update dropdown visible state
function showDropdown(fieldKey) {
  dropdownVisible[fieldKey] = true;
}

// Fetch Doctype List specific to fieldKey
function fetchDoctypeList(searchText, b, s, r, c, f) {
  const fieldKey = getFieldKey(b, s, r, c, f);

  const filters = [['istable', '=', 0]];
  if (searchText?.trim()) {
    filters.push(['name', 'like', `%${searchText}%`]);
  }

  const queryParams = {
    fields: JSON.stringify(['name']),
    filters: JSON.stringify(filters),
    limit_page_length: 'none',
    doctype:doctypes.doctypesList,
  };

  axiosInstance
    .get(apis.GetDoctypeData, { params: queryParams })
    .then((res) => {
      linkSearchResults[fieldKey] = res.message.data || [];
    })
    .catch((error) => {
      console.error('Error fetching doctype list:', error);
      linkSearchResults[fieldKey] = [];
    });
}
function fetchChildDoctypeList(searchText) {
  const filters = [
    ['istable', '=', 1]
  ];

  if (searchText?.trim()) {
    filters.push(['name', 'like', `%${searchText}%`]);
  }

  const queryParams = {
    fields: JSON.stringify(['name']),
    filters: JSON.stringify(filters),
    limit_page_length: '10',
    doctype:doctypes.doctypesList,
  };

  axiosInstance
    .get(apis.GetDoctypeData, { params: queryParams })
    .then((res) => {
      linkSearchResults.value = res.message.data || [];
    })
    .catch((error) => {
      console.error('Error fetching doctype list:', error);
    });
}

function selectDoctype(b, s, r, c, f, selectedName) {
  blockArr[b].sections[s].rows[r].columns[c].fields[f].options = selectedName;

  // Close dropdown & clear search results
  const fieldKey = getFieldKey(b, s, r, c, f);
  linkSearchResults[fieldKey] = [];
  dropdownVisible[fieldKey] = false;
}

// function selectDoctype(b, s, r, c, f, selectedName) {
//   blockArr[b].sections[s].rows[r].columns[c].fields[f].options = selectedName;

//   // Clear search results & close dropdown
//   const fieldKey = getFieldKey(b, s, r, c, f);
//   linkSearchQueries[fieldKey] = '';
//   linkSearchResults[fieldKey] = [];
//   dropdownVisible[fieldKey] = false;
// }
// function selectDoctype(b, s, r, c, f, name) {
//   blockArr[b].sections[s].rows[r].columns[c].fields[f].options = name;
//   linkSearchResults.value = [];
//   activeSearch.query = '';
//   activeSearch.key = ''; // deactivate
// }
const lowerApproverLevels = computed(() => {
  if (!blockArr?.length) return []

  if (selectedBlockIndex.value === 1) {
    // Only show requester (index 0)
    return [0]
  }

  // For index > 1, show all levels below current (excluding requester if needed)
  return Array.from({ length: selectedBlockIndex.value }, (_, i) => i).filter(i => i < selectedBlockIndex.value)
})

//=========================================================
// const activeLinkField = ref({});

// const activateLinkField = (tableIndex, fieldIndex) => {
//   activeLinkField.value = { tableIndex, fieldIndex };
// };

// const isLinkFieldActive = (tableIndex, fieldIndex) => {
//   return (
//     activeLinkField.value.tableIndex === tableIndex &&
//     activeLinkField.value.fieldIndex === fieldIndex
//   );
// };


// const handleLinkSearch = (searchText) => {
//   if (!searchText?.trim()) {
//     linkSearchResults.value = [];
//     return;
//   }

//   const filters = [
//     ['module', 'in', ['User Forms']],
//     ['istable', '=', 0]
//   ];

//   if (searchText.trim()) {
//     filters.push(['name', 'like', `%${searchText}%`]);
//   }

//   const queryParams = {
//     fields: JSON.stringify(['name']),
//     filters: JSON.stringify(filters),
//     limit_page_length: '10',
//   };

//   axiosInstance
//     .get(apis.resource + doctypes.doctypesList, { params: queryParams })
//     .then((res) => {
//       linkSearchResults.value = res.data || [];
//     })
//     .catch((error) => {
//       console.error('Error fetching doctype list:', error);
//       linkSearchResults.value = [];
//     });
// };


// // Store selected doctype in field.options
// const assignLinkOption = (selected, field) => {
//   field.options = selected;
//   linkSearchResults.value = [];
// };


// const filteredDesignationList = computed(() => {
//   let list = DesignationList.value;

//   if (showHods.value) {
//     list = list.filter(item => item.is_hod === 1);
//   }

//   if (searchDesignation.value?.trim()) {
//     list = list.filter(item =>
//       item.role.toLowerCase().includes(searchDesignation.value.toLowerCase())
//     );
//   }

//   // Remove already selected items for display only
//   list = list.filter(item => !designationValue.value.includes(item.role));

//   return list.map(item => item.role);
// });


// const filteredDesignationList = computed(() => {
//   let list = DesignationList.value;

//   // Show only HODs if toggled
//   if (showHods.value) {
//     list = list.filter(item => item.is_hod === 1);
//   }

//   // Search filter
//   if (searchDesignation.value?.trim()) {
//     list = list.filter(item =>
//       item.role.toLowerCase().includes(searchDesignation.value.toLowerCase())
//     );
//   }

//   // Remove already selected items from the dropdown
//   list = list.filter(item => !designationValue.value.includes(item.role));

//   // Sort remaining items (optional)
//   list = list.sort((a, b) => a.role.localeCompare(b.role));

//   // Return array of strings for Vue3Select
//   return list.map(item => item.role);
// });



// const filteredDesignationList = computed(() => {
//   return DesignationList.value
//     .filter((item) => item.toLowerCase().includes(searchDesignation.value.toLowerCase()))
//     .sort((a, b) => {
//       const aSelected = designationValue.value.includes(a);
//       const bSelected = designationValue.value.includes(b);
//       if (aSelected === bSelected) return 0;
//       return aSelected ? -1 : 1;
//     });
// });

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
const Predata = ref([
  {

    "form_json": "",

  }
]);
const isDuplicate=ref("");

onMounted(() => {
  deptData();
  isDuplicate.value=route.query.Clone
  paramId.value = route.query.id || "new";

  if (isDuplicate.value === '1') {
    filterObj.value.series = '';
  }

  if (paramId.value != undefined && paramId.value != null && paramId.value != "new") {
    getFormData();
    OwnerOftheForm();
  }
  sessionStorage.getItem('allow_approver_to_edit_form') == '1' ? allowEditSettingType.value = true : allowEditSettingType.value = false
  let Bu_Unit = localStorage.getItem("Bu");
  filterObj.value.business_unit = Bu_Unit;
  if (route.query.preId === 'PreDefine') {
    // filterObj.value.is_linked = 1; 
    const formJsonFromStorage = localStorage.getItem("form_json");

    if (formJsonFromStorage) {
      // Update the Predata with stored form JSON
      Predata.value[0].form_json = formJsonFromStorage;

      const formData = Predata.value[0];


      // Parse and rebuild the structured array from form fields
      const parsedJson = JSON.parse(formData.form_json);
      const structuredArr = rebuildToStructuredArray(parsedJson.fields);

      // Assign child table headers
      childtableHeaders.value = parsedJson.child_table_fields;

      // Push each structured item into blockArr
      structuredArr.forEach(item => {
        blockArr.push(item);
      });

      // If needed: preserve or apply the form name
      // filterObj.value.form_name = { ...formData.form_name };
    }

  }
});


const draggingIndex = ref(null);
const invalidFields = reactive({});
const currentEditingTable = ref(null);

const onDragStart = (index) => {
  draggingIndex.value = index;
};

const onDragEnd = () => {
  draggingIndex.value = null;
};

const onDragOver = (event) => {
  event.preventDefault();
};

const onDrop = (event, table) => {
  const targetRow = event.target.closest("tr");
  if (!targetRow) return;

  const targetIndex = Array.from(targetRow.parentNode.children).indexOf(targetRow);
  if (targetIndex !== draggingIndex.value) {
    const draggingRow = table[draggingIndex.value];
    table.splice(draggingIndex.value, 1);
    table.splice(targetIndex, 0, draggingRow);
    draggingIndex.value = targetIndex;
  }
};

// Store multiple child tables
// const formatTableName = (tableIndex, event) => {
//   if (event?.target?.value) {
//     childTables.value[tableIndex].formattedTableName = event.target.value
//       .trim()
//       .toLowerCase()
//       .replace(/\s+/g, "_")
//       .replace(/[^a-z0-9_]/g, "");
//   }
// };
const childTables = ref([]);

const cleanFieldOptions = (field) => {
  if (
    ["Select", "Table MultiSelect", "Check", "Small Text"].includes(field.fieldtype) &&
    field.options
  ) {
    const rawOptions = field.options
      .split("\n")
      .map((opt) => opt.trim())
      .filter((opt) => opt); // Remove empty lines

    const uniqueOptions = [];
    const seen = new Set();

    rawOptions.forEach((opt) => {
      const lower = opt.toLowerCase();
      if (!seen.has(lower)) {
        seen.add(lower);
        uniqueOptions.push(opt); // Retain original case
      }
    });

    return "\n" + uniqueOptions.join("\n");
  } else if (
    ["Link", "Table"].includes(field.fieldtype) &&
    field.options
  ) {
    return field.options.trim();
  }

  return field.options;
};

const addChildTable = (blockIndex, sectionIndex) => {
  const section = blockArr[blockIndex].sections[sectionIndex];

  if (!section.childTables) {
    section.childTables = [];
  }

  const newIndex = section.childTables.length;

  // Push a new child table with its own columns array
  section.childTables.push({
    label: "",
    fieldname: "",
    fieldtype: "Table", // optional clarity
    idx: newIndex,
    reqd: false,
    as_a_block: '',
    description: 'false',
    columns: [
      {
        label: "",
        fieldname: "",
        fieldtype: "",
        idx: 0,
        description: '',
        reqd: false,
        ...(columns.fieldtype === "Select" && columns.options
          ? { options: columns.options ? `\n${columns.options}` : `\n${''}` }
          : {})
      }
    ], // this holds the fields inside the table
    newTable: true
  });

};

const addFieldToTable = (blockIndex, sectionIndex, tableIndex) => {
  const table = blockArr[blockIndex].sections[sectionIndex].childTables[tableIndex];

  // Ensure the table has a columns array
  if (!table.columns) {
    table.columns = [];
  }

  table.columns.push({
    label: "",
    fieldname: "",
    fieldtype: "",
    idx: table.columns.length,
    description: '',
    reqd: false,
    ...(table.columns.fieldtype === "Select" && table.columns.options
      ? { options: table.columns.options ? `\n${table.columns.options}` : `\n${''}` }
      : {}
    )

  });
};

const removeChildTable = (blockIndex, sectionIndex, tableIndex) => {
  blockArr[blockIndex].sections[sectionIndex].childTables.splice(tableIndex, 1);
};

const removeFieldFromTable = (blockIndex, sectionIndex, tableIndex, fieldIndex) => {
  blockArr[blockIndex].sections[sectionIndex].childTables[tableIndex].columns.splice(fieldIndex, 1);
};

function validateFieldLabel(field, blockIndex, sectionIndex, tableIndex, fieldIndex, tableFields) {
  const key = `${blockIndex}-${sectionIndex}-${tableIndex}`;
  if (!fieldErrors[key]) {
    fieldErrors[key] = { columns: [] };
  }

  const fieldError = {};
  const label = field.label?.trim() || "";

  // Empty label check
  if (!label) {
    fieldError.label = "Field Label is required";
  } else {
    const normalized = label.toLowerCase();

    // Restricted labels
    if (restrictedLabels.includes(normalized) && !excludedLabels.includes(normalized)) {
      fieldError.label = `"${label}" is a restricted field label`;
    }

    // Max length check
    else if (label.length > 64) {
      fieldError.label = "Field Label cannot exceed 64 characters";
    }

    // Special characters check
    else if (!/^[A-Za-z0-9]+(?: [A-Za-z0-9]+)*$/.test(label)) {
      fieldError.label =
        "Field Label can only contain letters, numbers, and single spaces between words";
    }

    // 🔴 Duplicate label check (only later duplicates show error)
    else {
      const duplicates = tableFields
        .map((f, idx) => ({
          label: f.label?.trim().toLowerCase(),
          index: idx,
        }))
        .filter((f) => f.label === normalized);

      if (duplicates.length > 1) {
        // Only mark as duplicate if this is NOT the first occurrence
        const firstIndex = duplicates[0].index;
        if (fieldIndex !== firstIndex) {
          fieldError.label = `"${label}" is already used in this table`;
        }
      }
    }
  }

  // Save error state
  fieldErrors[key].columns[fieldIndex] = fieldError;
}


function validateField(field, tableName, index) {
  if (!fieldErrors[tableName]) fieldErrors[tableName] = {};

  const errors = [];
  const label = field.label?.trim() || "";

  // Required
  if (!label) errors.push("Label is required");

  // Max 64 characters
  if (label.length > 64) errors.push("Label cannot exceed 64 characters");

  // Only letters, numbers, spaces in middle
  if (label && !/^[A-Za-z0-9]+(?: [A-Za-z0-9]+)*$/.test(label))
    errors.push("No special characters allowed");

  // Restricted labels
  if (label && restrictedLabels.includes(label.toLowerCase().trim()))
    errors.push("This label is restricted");

  // Duplicate check (only if label is not empty)
  if (label) {
    const allLabels = childtableHeaders.value[tableName]
      .map((f) => f.label?.trim().toLowerCase())
      .filter(Boolean);

    const count = allLabels.filter((l) => l === label.toLowerCase()).length;
    if (count > 1) {
      errors.push("Duplicate label is not allowed");
    }
  }

  // Field type required
  if (!field.fieldtype) errors.push("Field type is required");

  // Options required for 'Select'
  if (
    field.fieldtype === "Select" &&
    (!field.options || field.options.trim() === "")
  ) {
    errors.push("Options are required");
  }

  fieldErrors[tableName][index] = errors;
}



const isEmptyFieldType = (blockIndex, sectionIndex, tableIndex) => {
  const table = blockArr[blockIndex].sections[sectionIndex].childTables[tableIndex];
  const errors = {
    tableName: false,
    columns: [],
  };

  let hasError = false;

  if (!table.tableName?.trim()) {
    errors.tableName = "Table name is required.";
    hasError = true;
  }

  table.columns.forEach((field, fieldIndex) => {
    const fieldError = {};
    if (!field.label?.trim()) {
      fieldError.label = "Field Label is required";
      hasError = true;
    }
    if (!field.fieldtype?.trim()) {
      fieldError.fieldtype = "Please select field type";
      hasError = true;
    }
    errors.columns[fieldIndex] = fieldError;
  });

  // Save to fieldErrors
  fieldErrors[`${blockIndex}-${sectionIndex}-${tableIndex}`] = errors;

  return hasError;
};

const ensureArrayPath = (blockIndex, sectionIndex, key) => {
  const section = blockArr[blockIndex]?.sections?.[sectionIndex];
  if (section && !Array.isArray(section[key])) {
    section[key] = [];
  }
};


const formatTableName = (tableName) => {
  return tableName
    ? tableName.trim().replace(/\s+/g, "_").replace(/[^a-zA-Z0-9_]/g, "")
    : "";
};

const processFields = (blockIndex, sectionIndex, tableIndex) => {
  const hasErrors = isEmptyFieldType(blockIndex, sectionIndex, tableIndex);
  if (hasErrors) {
    showError("Please fix validation errors before creating the table", {
      transition: "zoom",
    });
    return;
  }
  if (matched.value) {
    //  tableExistsMessage.value = 'Table already exists';
    showError("Table already exists", {
      transition: "zoom",
    });
    return;
  }

  const table = blockArr[blockIndex].sections[sectionIndex].childTables[tableIndex];
  const section = blockArr[blockIndex].sections[sectionIndex];
  table.columns = table.columns.map((field, index) => ({
    ...field,
    idx: index,
    options: cleanFieldOptions(field),
  }));
  table.newTable = false
  const data = {
    form_short_name: table.tableName,
    fields: table.columns,
    idx: table.idx,
    as_a_block: table.as_a_block  ? table.as_a_block : 'false',
  };

  // // ensureArrayPath(blockIndex, sectionIndex, 'afterCreated');
  // // table.newTable = false

  // // section.afterCreated[tableIndex] = table;

  // // blockArr[blockIndex].sections[sectionIndex].childTables[tableIndex] = []
  // //showSuccess("Table created successfully!", {
  //  // autoClose: 500,
  //  // transition: "zoom",
  //  //});
  axiosInstance
  .post(apis.childtable, data)
  .then((res) => {
    if (res) {
      ensureArrayPath(blockIndex, sectionIndex, 'afterCreated');

      // Save original table to afterCreated
      section.afterCreated[tableIndex] = { ...table };

      showSuccess("Table created successfully!");

      const responseData = res.message?.[0]?.[0]?.child_doc;

      if (responseData) {
        // ✅ Merge response into the existing table instead of replacing
        blockArr[blockIndex].sections[sectionIndex].childTables[tableIndex] = {
          ...blockArr[blockIndex].sections[sectionIndex].childTables[tableIndex],
          ...responseData,
          newTable: false, // keep this flag under control
        };
      }
    }
  })

    .catch((error) => {
      console.error("Error creating table:", error);
    });
};
// Reactive object to track invalid fields per table


// Validation function
const validateTableField = (field, tableName, index, tableColumns = []) => {
  if (!invalidFields[tableName]) invalidFields[tableName] = [];
  invalidFields[tableName] = invalidFields[tableName].filter(i => i !== index);

  if (!fieldErrors[tableName]) fieldErrors[tableName] = [];
  fieldErrors[tableName][index] = [];

  const errors = [];
  const label = field.label?.trim() || "";

  // 1. Label required
  if (!label) errors.push("Label is required");

  // 2. Restricted labels
  else if (restrictedLabels.includes(label.toLowerCase())) errors.push("This label is restricted");

  // 3. Max length 64
  else if (label.length > 64) errors.push("Label cannot exceed 64 characters");

  // 4. Regex check
  else if (!/^[A-Za-z0-9]+(?: [A-Za-z0-9]+)*$/.test(label)) errors.push("Only letters, numbers, and single spaces allowed");

  // 5. Duplicate check
  if (tableColumns.length) {
    const normalized = label.toLowerCase();
    const duplicates = tableColumns
      .map((f, idx) => ({ label: f.label?.trim().toLowerCase(), idx }))
      .filter(f => f.label === normalized);

    if (duplicates.length > 1) {
      const firstIndex = duplicates[0].idx;
      if (index !== firstIndex) {
        errors.push("Duplicate label not allowed");
        field._duplicate = true;
      } else {
        field._duplicate = false;
      }
    } else {
      field._duplicate = false;
    }
  }

  // 6. Field type required
  if (!field.fieldtype) errors.push("Field type is required");

  // 7. Options required for Select type
  if (field.fieldtype === "Select" && (!field.options || !field.options.trim())) errors.push("Options are required");

  // Save errors
  fieldErrors[tableName][index] = errors;

  // Save invalid index
  if (errors.length > 0) {
    invalidFields[tableName].push(index);
  }

  return errors.length === 0;
};



const afterImmediateEditaddNewFieldedit = (blockIndex, sectionIndex, tableName) => {
  const section = blockArr[blockIndex].sections[sectionIndex];
  const table = section.afterCreated.find((t) => t.tableName === tableName);
  if (!table) return;

  const newIndex = table.columns.length;

  const newField = {
    fieldname: "",
    fieldtype: "",
    idx: newIndex + 1,
    label: "",
    value: "",
    isNew: true,
    description: '',
  };

  table.columns.push(newField);

  // Live validate the new field
  validateTableField(newField, tableName, newIndex, table.columns);
};


const afterdata = ref([])

const afterImmediateEditdeleteRow = (blockIndex, sectionIndex, tableName, index) => { 
  const section = blockArr[blockIndex].sections[sectionIndex]; const table = section.afterCreated.find((t) => t.tableName === tableName);
   if (!table) return; 
   // Remove the specified field 
    table.columns.splice(index, 1);
   //  // Recalculate idx for remaining fields 
   table.columns.forEach((field, i) => { field.idx = i + 1; }); // Also remove from invalidFields if needed
    const invalids = invalidFields.value[tableName];
     if (invalids) { invalidFields.value[tableName] = invalids.filter(i => i !== index) .map(i => (i > index ? i - 1 : i)); // Adjust index after removal
      } };
// const afterImmediateEdit = (blockIndex, sectionIndex, tableName) => {

//   const section = blockArr[blockIndex].sections[sectionIndex];
//   const table = section.afterCreated.find((t) => t.tableName === tableName);
//   if (!table) return;

//   if (editMode[tableName]) {
//     invalidFields.value[tableName] = [];
//     let isValid = true;

//     table.columns.forEach((field, index) => {
//       if (!field.label || !field.fieldtype) {
//         invalidFields.value[tableName].push(index);
//         isValid = false;
//       }
//     });

//     if (!isValid) return;

//    const allFields = table.columns.map(({ isNew, ...rest }, index) => ({
//   ...rest,
//   idx: index + 1,
//   options: cleanFieldOptions(rest),
// }));


//     const formData = {
//       form_short_name: formatTableName(tableName),
//       fields: allFields,
//       as_a_block: table.description
//     };

//     axiosInstance
//       .post(apis.childtable, formData)
//       .then((response) => {
//         afterdata.value = response.data;
//         showSuccess("Fields updated successfully!", { autoClose: 500 });

//       })
//       .catch((error) => {
//         console.error("❌ Saving fields failed:", error);
//       });
//   }

//   editMode[tableName] = !editMode[tableName];
// };


const afterImmediateEdit = (blockIndex, sectionIndex, tableName) => {
  const section = blockArr[blockIndex].sections[sectionIndex];
  const table = section.afterCreated.find((t) => t.tableName === tableName);
  if (!table) return;

  if (editMode[tableName]) {
    invalidFields[tableName] = [];
    let isValid = true;

   table.columns.forEach((field, index) => {
  if (!validateTableField(field, tableName, index, table.columns)) isValid = false;
});

    if (!isValid){
     showError("Please fix the errors in the highlighted fields before saving!");
      
      return; // stop save if invalid
    }

    const allFields = table.columns.map(({ isNew, ...rest }, index) => ({
      ...rest,
      idx: index + 1,
      options: cleanFieldOptions(rest),
    }));

    const formData = {
      form_short_name: formatTableName(tableName),
      fields: allFields,
      as_a_block: table.description
    };

    axiosInstance
      .post(apis.childtable, formData)
      .then((response) => {
        afterdata.value = response.data;
        showSuccess("Fields updated successfully!");
      })
      .catch((error) => {
        console.error("❌ Saving fields failed:", error);
      });
  }

  editMode[tableName] = !editMode[tableName];
};


const editMode = reactive({});

const addNewFieldedit = (tableName) => {
  if (!childtableHeaders.value[tableName]) {
    childtableHeaders.value[tableName] = [];
  }

  // Assign idx based on existing field count
  const newIndex = childtableHeaders.value[tableName].length + 1;

  childtableHeaders.value[tableName].push({
    fieldname: "", // Ensuring unique fieldname
    fieldtype: "",
    idx: newIndex, // Assign idx dynamically
    label: "",
    value: "", // Keep value
    isNew: true,
    description: "",
    options: childtableHeaders.value[tableName].options ? `\n${childtableHeaders.value[tableName].options}` : `${''}`
  });
  // console.log(childtableHeaders.value[tableName],"mmm");
};
const deleteRow = (tableName, index) => {
  if (childtableHeaders.value[tableName]) {
    childtableHeaders.value[tableName].splice(index, 1);
  }
};


const toggleEdit = (tableName, description) => {
  if (!tableName) return;

  if (!invalidFields.value) invalidFields.value = {};
  if (!invalidFields.value[tableName]) invalidFields.value[tableName] = [];

  const tableFields = childtableHeaders.value[tableName];
  if (!tableFields) return;

  if (editMode[tableName]) {
    invalidFields.value[tableName] = [];
    let isValid = true;

    tableFields.forEach((field, index) => {
      // Validate using your existing function
      validateField(field, tableName, index);

      const errors = fieldErrors[tableName]?.[index];
      if (errors && errors.length > 0) {
        invalidFields.value[tableName].push(index);
        isValid = false;
      }

      // Trim first/last spaces for label
      if (field.label) field.label = field.label.trim();
    });

    if (!isValid) {
      showError("Please fix the errors before saving");
      return;
    }

    const allFields = tableFields.map(({ isNew, ...rest }, idx) => ({
      ...rest,
      idx: idx + 1,
      options: cleanFieldOptions(rest),
    }));

    const formData = {
      form_short_name: tableName,
      fields: allFields,
      as_a_block: description,
    };

    axiosInstance
      .post(apis.childtable, formData)
      .then((response) => {
        afterdata.value = response.data;
        showSuccess("Fields updated successfully!");
      })
      .catch((error) => {
        console.error("❌ Saving fields failed:", error);
      });
  }

  // Toggle edit mode
  editMode[tableName] = !editMode[tableName];
  currentEditingTable.value = editMode[tableName] ? tableName : null;
};


// watch(childtableHeaders, (newTables) => {
//   if (!newTables) return;

//   Object.keys(newTables).forEach((tableName) => {
//     const fields = newTables[tableName];
//     if (!fields || !Array.isArray(fields)) return;

//     fields.forEach((field, index) => {
//       if (
//         field.label &&
//         field.fieldtype &&
//         !restrictedLabels.includes(field.label.toLowerCase().trim())
//       ) {
//         // Remove error dynamically when user enters a valid value
//         if (invalidFields.value[tableName]) {
//           invalidFields.value[tableName] = invalidFields.value[tableName].filter(i => i !== index);
//         }
//       }
//     });
//   });
// }, { deep: true });


// watch(childtableHeaders, (newTables) => {
//   Object.keys(newTables).forEach((tableName) => {
//     newTables[tableName].forEach((field, index) => {
//       if (field.label && field.fieldtype &&
//         !restrictedLabels.includes(field.label)) {
//         // ✅ Remove error dynamically when user enters a valid value
//         invalidFields.value[tableName] = invalidFields.value[tableName]?.filter(i => i !== index);
//       }
//     });
//   });
// }, { deep: true });

// Object.keys(newTables).forEach((tableName) => {
//   const fields = newTables[tableName];
//   if (Array.isArray(fields)) {
//     fields.forEach((field, index) => {
//       if (field.label && field.fieldtype) {
//         invalidFields.value[tableName] = invalidFields.value[tableName]?.filter(i => i !== index);
//       }
//     });
//   } else {
//     console.warn(`Expected array for table "${tableName}", but got`, fields);
//   }
// });


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
  {
    id: 3,
    label: "Print Format",
    stepno: "Step 3",
    icon: "ri-checkbox-circle-line",
  },
]);

const childfield = [
  {
    label: "Text",
    type: "Data",
  },
  {
    label: "Select",
    type: "Select",
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
  {
    label: "Number",
    type: "Int",
  },
  {
    label: "TextArea",
    type: "Text",
  },
  // {
  //   label: "Link",
  //   type: "Link"
  // }
];
const fieldTypes = [
  {
    label: "Text",
    type: "Data",
  },
  {
    label: "Time",
    type: "Time",
  },
  {
    label: "Text Area",
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
    label: "Attach",
    type: "Attach",
  },
  {
    label: "Phone",
    type: "Data",
  },
  {
    label: "Check",
    type: "Check",
  },
   {
    label: "Number",
    type: "Int",
  },
 
  {
    label: "Select",
    type: "Select",
  },
  {
    label: "Multi Select",
    type: "Small Text",
  },
  {
    label: "Link",
    type: "Link"
  }
  // {
  //     label: "Signature",
  //     type: "Signature",
  // },
   // {
  //     label: "Radio",
  //     type: "radio",
  // },
    // {
  //   label: "Table",
  //   type: "Table",
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
  // console.log(isChecked);
  if (option === SELECT_ALL) {
    if (event.target.checked) {
      //  Select all options immediately

      filterObj.value.accessible_departments = [...formOptions.value];
      // console.log(filterObj.value.accessible_departments); 
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

const handleSelect = (option) => {
  if (option === SELECT_ALL) {
    filterObj.value.accessible_departments = [...formOptions.value];
  }
};

const handleRemove = (option) => {
  if (option === SELECT_ALL) {
    filterObj.value.accessible_departments = [];
  }
};
const selectAllChecked = ref(false); // select-all checkbox state

// ✅ Computed filtered list
// ✅ Filtered list (based on HODs + search)
// const filteredDesignationList = computed(() => {
//   let list = [...DesignationList.value]; // copy original list

//   // ✅ Apply HOD filter
//   if (showHods.value) list = list.filter(item => item.is_hod === 1);

//   // ✅ Apply search filter
//   if (searchDesignation.value?.trim()) {
//     const search = searchDesignation.value.toLowerCase();
//     list = list.filter(item => item.role.toLowerCase().includes(search));
//   }

//   // ✅ Sort: move already selected items to the end
//   list = list.sort((a, b) => {
//     const aSelected = designationValue.value.includes(a.role);
//     const bSelected = designationValue.value.includes(b.role);

//     if (aSelected === bSelected) return 0;
//     return aSelected ? 1 : -1; // selected items go last
//   });

//   // ✅ Map to string for Vue3Select
//   return list.map(item => item.role);
// });
const filteredDesignationList = computed(() => {
  let list = [...DesignationList.value];

  // ✅ 1. Apply HOD filter
  if (showHods.value) list = list.filter(item => item.is_hod === 1);

  // ✅ 2. Apply search filter
  if (searchDesignation.value?.trim()) {
    const search = searchDesignation.value.toLowerCase();
    list = list.filter(item => item.role.toLowerCase().includes(search));
  }

  // ✅ 3. Sort alphabetically (A → Z)
  list.sort((a, b) => a.role.localeCompare(b.role));

  // ✅ 4. Move selected items to bottom
  list.sort((a, b) => {
    const aSelected = designationValue.value.includes(a.role);
    const bSelected = designationValue.value.includes(b.role);
    if (aSelected === bSelected) return 0;
    return aSelected ? 1 : -1;
  });

  // ✅ 5. Return only role names for dropdown
  return list.map(item => item.role);
});



// ✅ Computed to determine if all visible ones are selected
const isAllSelected = computed(() => {
  const visible = filteredDesignationList.value
  return (
    visible.length > 0 &&
    visible.every(role => designationValue.value.includes(role))
  )
})

// ✅ Watch to keep select-all checkbox synced
watch(
  [designationValue, filteredDesignationList],
  () => {
    const visible = filteredDesignationList.value
    selectAllChecked.value =
      visible.length > 0 &&
      visible.every(role => designationValue.value.includes(role))
  },
  { immediate: true, deep: true }
)
function toggleSelectAll(event) {
  const checked = event.target.checked;

  // Only consider visible roles for this filter
  const visibleRoles = DesignationList.value
    .filter(item => {
      if (showHods.value && item.is_hod !== 1) return false;
      if (searchDesignation.value?.trim() &&
          !item.role.toLowerCase().includes(searchDesignation.value.toLowerCase())
      ) return false;
      return true;
    })
    .map(item => item.role);

  if (checked) {
    // Add visible roles only
    designationValue.value = Array.from(
      new Set([...designationValue.value, ...visibleRoles])
    );
  } else {
    // Remove only visible roles
    designationValue.value = designationValue.value.filter(
      r => !visibleRoles.includes(r)
    );
  }

  selectAllChecked.value = checked;
}

// ✅ Select / Unselect all
// function toggleSelectAll(event) {
//   const checked = event.target.checked
//   const visibleRoles = filteredDesignationList.value

//   if (checked) {
//     // Add visible items to selected list
//     designationValue.value = Array.from(
//       new Set([...designationValue.value, ...visibleRoles])
//     )
//   } else {
//     // Remove only visible ones
//     designationValue.value = designationValue.value.filter(
//       r => !visibleRoles.includes(r)
//     )
//   }

//   selectAllChecked.value = checked
// }

// ✅ Clear all selections
function clearall_designations() {
  designationValue.value = []
  selectAllChecked.value = false
  showHods.value = false
}
// const isAllSelected = computed(() => {
//   return designationValue.value.length === DesignationList.value.length;
// });
// // Toggle Select All
// // Toggle Select All
// function toggleSelectAll(event) {
//   if (event.target.checked) {
//     // Select all items currently visible in the filtered dropdown
//     const itemsToSelect = DesignationList.value
//       .filter(item => {
//         // Respect HOD filter
//         if (showHods.value && item.is_hod !== 1) return false;

//         // Respect search filter
//         if (searchDesignation.value?.trim() && !item.role.toLowerCase().includes(searchDesignation.value.toLowerCase())) {
//           return false;
//         }

//         return true;
//       })
//       .map(item => item.role);

//     designationValue.value = itemsToSelect;
//   } else {
//     // Unselect all visible items
//     const itemsToRemove = DesignationList.value
//       .filter(item => {
//         if (showHods.value && item.is_hod !== 1) return false;
//         if (searchDesignation.value?.trim() && !item.role.toLowerCase().includes(searchDesignation.value.toLowerCase())) {
//           return false;
//         }
//         return true;
//       })
//       .map(item => item.role);

//     // Remove only the visible items from the selection
//     designationValue.value = designationValue.value.filter(role => !itemsToRemove.includes(role));
//   }
// }



// Toggle select all
// function toggleSelectAll(event) {
//   if (event.target.checked) {
//     console.log(designationValue.value);
//     // Select all
//     designationValue.value = [...DesignationList.value];
//   } else {
//     // Unselect all
//     designationValue.value = [];
//   }
// }
// function clearall_designations(){
//   designationValue.value = []
// }
// ✅ Toggle select all
// function toggleSelectAll(event) {
//   if (event.target.checked) {
//     // Add all filtered roles
//     const newSelection = [
//       ...new Set([...designationValue.value, ...filteredDesignationList.value]),
//     ];
//     designationValue.value = newSelection;
//   } else {
//     // Remove only filtered roles
//     designationValue.value = designationValue.value.filter(
//       (role) => !filteredDesignationList.value.includes(role)
//     );
//   }
// }

function handleSingleSelect() {
  if (!isAllSelected.value && designationValue.value.length === 1) {
    // console.log("Selected only one designation:", designationValue.value[0]);
  }
}
const selectedApproverType = ref('');
function addDesignationBtn() {
  const block = blockArr[selectedBlockIndex.value];

  if (!block || !block.sections) {
    console.error("Error: Invalid block or sections not found.");
    return; // Prevent further execution
  }

  let xyz = {
    type: selectedBlockIndex.value == 0 ? "requestor" : "approver",
    roles: designationValue.value,
    approval_required:approval_required.value,
    approver_can_edit:approver_can_edit.value,
    fields: block.sections.flatMap(extractFieldnames),
    idx: selectedBlockIndex.value,
  };

  // workflowSetup.push(xyz)
  // if (selectedBlockIndex.value !== 0) {
  //   xyz.view_only_reportee = ViewOnlyReportee.value === true ? 1 : 0;
  //   xyz.on_rejection = OnRejection.value ? OnRejection.value : 0;
  //   xyz.all_approvals_required = all_approvals_required.value === true ? 1 : 0;
  //   xyz.requester_as_a_approver = requester_as_a_approver.value === true ? 1 : 0;
  // }
 
  if (selectedBlockIndex.value !== 0) {
    xyz.view_only_reportee = selectedApproverType.value === 'ViewOnlyReportee' ? 1 : 0;
    xyz.all_approvals_required = selectedApproverType.value === 'all_approvals_required' ? 1 : 0;
    xyz.requester_as_a_approver = selectedApproverType.value === 'requester_as_a_approver' ? 1 : 0;
    xyz.on_rejection = OnRejection.value ? OnRejection.value : 0;
  }


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

function initializeDesignationValue(blockIndex) {
  const currentSetup = getWorkflowSetup(blockIndex);
  const rolesForBlock = currentSetup.roles || [];
  designationValue.value = [...rolesForBlock];

  OnRejection.value = currentSetup.on_rejection;
  approval_required.value=currentSetup.approval_required;
  approver_can_edit.value = currentSetup.approver_can_edit;
  // Check for view_only_reportee flag
  // ViewOnlyReportee.value = currentSetup.view_only_reportee === 1;
  // OnRejection.value = currentSetup.on_rejection
  // all_approvals_required.value = currentSetup.all_approvals_required === 1;
  // requester_as_a_approver.value = currentSetup.requester_as_a_approver === 1;

  // Set dropdown value based on which flag is 1
  if (currentSetup.view_only_reportee === 1) {
    selectedApproverType.value = 'ViewOnlyReportee';
  } else if (currentSetup.all_approvals_required === 1) {
    selectedApproverType.value = 'all_approvals_required';
  } else if (currentSetup.requester_as_a_approver === 1) {
    selectedApproverType.value = 'requester_as_a_approver';
  } else {
    selectedApproverType.value = '';
  }
}

// Initialize `designationValue` based on the roles for the given block index
// function initializeDesignationValue(blockIndex) {
//   const rolesForBlock = getWorkflowSetup(blockIndex).roles || [];
//   designationValue.value = [...rolesForBlock]; // Reset designationValue to match only roles for the current block
// }

// function canShowDesignationButton(blockIndex) {
//   if (paramId === undefined || paramId === null || paramId === 'new') return false;

//   const roles = getWorkflowSetup(blockIndex).roles;

//   // First approver (blockIndex = 0)
//   if (blockIndex === 0) {
//     return roles.length === 0;
//   }

//   // For subsequent approvers: check if previous approver has a role
//   const prevRoles = getWorkflowSetup(blockIndex - 1).roles;
//   return (
//     prevRoles.length > 0 &&
//     prevRoles[0] !== null &&
//     prevRoles[0] !== '' &&
//     roles.length === 0
//   );
// }


const AddDesignCanvas = (idx) => {
  showHods.value = false;
  searchDesignation.value = ''
  selectedApproverType.value = ''; 
  // ViewOnlyReportee.value = false;
  // all_approvals_required.value = false;
  // requester_as_a_approver.value = false;
  OnRejection.value = '';
  // console.log(idx, "---clicked idex", selectedBlockIndex.value);
  if (filterObj.value.accessible_departments.length) {
    designationData(idx,filterObj.value.accessible_departments);
  }
  selectedBlockIndex.value = idx;
  initializeDesignationValue(idx);
};
// const userlist = ref([]);
// function designationData(departments) {
//   const filters = [];

//   if (Array.isArray(departments) && departments.length > 0) {
//     filters.push(["ezy_departments", "in", departments]);
//   }

//   axiosInstance
//     .get(apis.resource + doctypes.WFRoleMatrix + `/${filterObj.value.business_unit}`)
//     .then((res) => {
//       if (res.data) {
//         // console.log(res.data.users, "wf role matrix");
//         userlist.value = res.data.users;

//         DesignationList.value = [
//           ...new Set(res.data.users.map((user) => user.role_name)),
//         ];
//       }
//     })
//     .catch((error) => {
//       console.error("Error fetching designations data:", error);
//     });
// }
// const filters = [];

// if (Array.isArray(departments) && departments.length > 0) {
//   filters.push(["ezy_departments", "in", departments]);
// }
// const queryParams = {
//   limit_page_length: 'None',
// }


//  Fetching Employee Designations based on Enabled Employees and Is Hods Only 
function designationData(blockIndex, departments) {
  let data = {
    index: blockIndex,                // The current step index (0 = requester, 1 = approver, etc.)
    departments: departments,         // Array of departments (must remain as array, not params)
    property: filterObj.value.business_unit // Business unit (property) selected from filters
  };

  axiosInstance
    .post(apis.addDesignationroles, data) 
    .then((res) => {
      //  Check if backend returned "message" key with data
      if (res.message) {
        //  Store the result in DesignationList (used in UI)
        DesignationList.value = res.message;
      }
    })
    .catch((error) => {
      //  Handle errors gracefully
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
        showSuccess("Requestor Added");
      } else {
        showSuccess(`Approver-${selectedBlockIndex.value} Added`);
      }
    });
}



function cancelForm() {
  router.push({
    path: selectedData.value.routepath || localStorage.getItem('routepath'),
  });
  localStorage.removeItem('form_json');

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
    showError("Please check all required fields before proceeding.");
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
    showError("Please check all required fields before proceeding.");
    return;
  }

  if (activeStep.value < 3) {
    activeStep.value += 1;
    if (activeStep.value === 3) {
      selectedform.value = blockArr;
      // console.log(selectedform.value);
    }
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
   const queryParams = {
        fields: JSON.stringify(["*"]),
        limit_page_length: "none",
        doctype:doctypes.EzyFormDefinitions,
        doc_id:paramId.value,
    };
  axiosInstance
    .get(apis.GetDoctypeData, { params: queryParams })
    .then((res) => {
      let res_data = res?.message.data;
      if (res_data) {
        // router.push({
        //   query: {
        //     id: res_data.name,
        //   }
        // })
        if (res_data.accessible_departments) {
          res_data.accessible_departments = res_data.accessible_departments.split(",");
        }
        filterObj.value = {
          ...filterObj.value,
          ...res_data,
          owner_of_the_form:
            res_data.owner_of_the_form || filterObj.value.owner_of_the_form || "",
        };

        const parsedFormJson = JSON.parse(res.message.data?.form_json);
        wrkAfterGetData.value = parsedFormJson.workflow;
        // console.log(parsedFormJson.workflow, "parsedFormJson");
        tableName.value = parsedFormJson.fields.filter(
          (field) => field.fieldtype === "Table"
        );
        returTables.value = parsedFormJson.fields.filter(
          (field) => field.fieldtype === "Table"
        );

        is_landscape.value = res.message.data.is_landscape;
        // let structuredArr = rebuildToStructuredArray((JSON.parse(res_data?.form_json?.fields).fields)?.replace(/\\\"/g, '"'))
        let structuredArr = rebuildToStructuredArray(
          JSON.parse(res_data?.form_json).fields
        );
        childtableHeaders.value = JSON.parse(res.message.data.form_json).child_table_fields;

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

function SetPrintFormatFn() {
  // console.log(is_landscape.value);
  const data = {};

  // Add print_format if it has a value
  if (printFormatID.value) {
    data.print_format = printFormatID.value;
  }

  // Add is_landscape if it has a value (you can also check === true if needed)
  if (is_landscape.value !== undefined && is_landscape.value !== null) {
    data.is_landscape = is_landscape.value;
  }

  axiosInstance
    .put(apis.resource + doctypes.EzyFormDefinitions + `/${route.query.id}`, data)
    .then((res) => {
      console.log(res);
      const modal = bootstrap.Modal.getInstance(document.getElementById('customFormatModal'));
      modal.hide();
      showSuccess("Print Format Added Successfully");

    })
    .catch((error) => {
      console.error("Error fetching  data:", error);
    });
}

function deptData() {
  const queryParams = {
    fields: JSON.stringify(["name","department_name"]),
    limit_page_length: "none",
    business_unit: `${selectedData.value.business_unit || route.query.business_unit}`,
    doctype:doctypes.departments,
  };

  axiosInstance
    .get(apis.GetDoctypeData, { params: queryParams })
    .then((res) => {
      if (res?.message.data?.length) {
        OwnerOfTheFormData.value = res.message.data.map((dept) => dept.name);
        formOptions.value = res.message.data.map((dept) => dept.name); // Store the full data for accessible departments
        // departments.value = res.message.data.map(item => item.category)
      }
    })
    .catch((error) => {
      console.error("Error fetching department data:", error);
    });
}

const EmpMailsList=ref("")
 
function EmployeeData() {
  const queryParams = {
    fields: JSON.stringify(["name"]),
    limit_page_length: "none",
    filters: JSON.stringify([["company_field", "=", `${selectedData.value.business_unit || route.query.business_unit}`],["enable", "=", "1"]]),
    doctype:doctypes.EzyEmployeeList,
  };
 
  axiosInstance
    .get(apis.GetDoctypeData, { params: queryParams })
    .then((res) => {
      if (res?.message.data?.length) {
        EmpMailsList.value = res.message.data.map((emp) => emp.name);
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
  const queryParams = {
    fields: JSON.stringify(["ezy_departments_items"]),
    doctype:doctypes.departments,
    doc_id:newVal,
  };
  axiosInstance
    .get(apis.GetDoctypeData, { params: queryParams })
    .then((res) => {
      if (res?.message.data?.ezy_departments_items) {
        departments.value = res.message.data.ezy_departments_items.map((item) => item.category);
      }
    })
    .catch((error) => {
      console.error("Error fetching categories data:", error);
    });
}

function formData(status) {
  // console.log(blockArr, "blockarray");
  // console.log(blockArr, 'blockArr');
  // console.log(tableFieldsCache.value, 'tableFieldsCache');
  // console.log(returTables.value, 'returTables');

  let fields = extractFieldsWithBreaks(blockArr);

  // if (tableFieldsCache.value.length) {
  //   // Merge stored table fields
  //   fields = [...fields, ...tableFieldsCache.value];
  // }

  // if (returTables.value && returTables.value.length) {
  //   // Append child table headers instead of replacing
  //   fields = [...fields, ...returTables.value];
  // }
  const dataObj = {
    ...filterObj.value,
    fields,
    doctype: doctypes.EzyFormDefinitions,
    workflow_setup: workflowSetup,
    form_status: status === "save" ? "Created" : "Draft",
  };

  dataObj.accessible_departments = dataObj.accessible_departments.toString();

  axiosInstance
    .post(apis.savedata, dataObj)
    .then((res) => {
      // console.log(res, "res");
      if (res && res.message && res.message.message) {
        let preId = localStorage.getItem("preName");
        if (preId) {

          let predData = {
            installed: 'Yes'
          }
          axiosInstance.put(`${apis.resource}${doctypes.preDefinedForm}/${preId}`, predData)
            .then(res => {
              const response=res
              localStorage.removeItem('preName')
            })
            .catch(error => {
              console.error("Error fetching ezyForms data:", error);
            });
        }
        // tableFieldsCache.value = [];
        router.push({
          params: { paramid: res.message.message },
          query: {
            id: res.message.message
          }
        });
        paramId.value = res.message.message;
        // paramId = res.message.message;

        if (paramId && paramId !== "new") {
          blockArr.splice(0, blockArr.length);
          getFormData();
        }
        // console.log(paramId.value, "Updated paramId");

        if (workflowSetup.length < blockArr.length) {
          showInfo("Add Workflow");
        } else {
          if (isBlockRemoved.value === true) {
            showSuccess("Form Created Successfully!", {
              autoClose: 2000,
              transition: "zoom",
              // onClose: () => {
              // },
            });
            let toPath = localStorage.getItem('routepath');
            if (status === "save") {
              router.push({ path: toPath });
            }
            else if (status === "Draft") {
              router.push({ path: toPath });

            }
          }
        }
      } else {
        console.error("Invalid response structure:", res);
      }
    })
    .catch((error) => {
      console.error("Error saving form data:", error);
    });
}


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
        childTables: [],
        afterCreated: {},
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
                        label: "Requested By",
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
                    label: "", // First column with "Approver" "
                    fields: [
                      {
                        label: "Approver",
                        fieldtype: "Data",
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
                  {
                    label: "", // third column with "Approved By"
                    fields: [
                      {
                        label: "Approved By",
                        fieldtype: "Attach",
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
const isBlockRemoved = ref(false);

const removeBlock = (blockIndex) => {
  let item = blockArr[blockIndex];
  if (item.parent) deleted_items.push(item);

  let rolesToDelete = [];
  if (workflowSetup.length > blockIndex && workflowSetup[blockIndex].roles) {
    rolesToDelete = [...workflowSetup[blockIndex].roles];
  }

  blockArr.splice(blockIndex, 1);
  if (workflowSetup.length > blockIndex) {
    workflowSetup.splice(blockIndex, 1);
  }
   blockArr.forEach((block, bIndex) => {
    block.sections.forEach((section, sIndex) => {
      section.rows.forEach((row, rIndex) => {
        row.columns.forEach((column, cIndex) => {
          handleFieldChange(bIndex, sIndex, rIndex, cIndex);
        });
      });
    });
  });
  if(rolesToDelete.length){
    delete_assigned_roles(rolesToDelete, blockIndex);
  }

};

function delete_assigned_roles(roles, blockIndex) {
  const payload = {
    role: roles,
    level: blockIndex,
    document_type: filterObj.value.form_name,
    short_name: filterObj.value.form_short_name,
    property: filterObj.value.business_unit
  };

  axiosInstance
    .post(apis.deleteAssigneRoles, payload)
    .then((res) => {
      if (res) {
        const response=res
        formData();
      }
    });
}

// Function to add a new section with a default column
// const addSection = (blockIndex) => {
//   let sectionIndex = blockArr[blockIndex].sections.length;
//   // let rowIndex = blockArr[blockIndex].sections;

//   blockArr[blockIndex].sections.push({
//     label: "",
//     parent: `${businessUnit.value.value}-${filterObj.value.form_short_name}`,
//     rows: [
//       {
//         label: `row_0_${sectionIndex}_${blockIndex}`,
//         columns: [
//           {
//             label: "",
//             fields: [
//               {
//                 label: "",
//                 fieldtype: "",
//                 // value: ref(""), // Keeping the value as a ref for reactivity
//                 options: "",
//                 reqd: false,
//               },
//             ], // Initialize with an empty fields array
//           },
//         ],
//       },
//     ],
//   });

// };

const addSection = (blockIndex, sectionIndex) => {
  const newSection = {
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
                options: "",
                reqd: false,
              },
            ],
          },
        ],
      },
    ],
  };
  blockArr[blockIndex].sections.splice(sectionIndex + 1, 0, newSection);
};
// Function to remove a section
// const removeSection = (blockIndex, sectionIndex) => {
//   let item = blockArr[blockIndex].sections[sectionIndex];
//   if (item.parent) deleted_items.push(item);
//   blockArr[blockIndex].sections.splice(sectionIndex, 1);
//   // showSuccess("Section removed", { autoClose: 500 })
// }; 
const removeSection = (blockIndex, sectionIndex) => {
  let item = blockArr[blockIndex].sections[sectionIndex];
  if (item.parent) deleted_items.push(item);

  // Remove the section
  blockArr[blockIndex].sections.splice(sectionIndex, 1);

  // Re-validate all remaining fields for duplicates
  blockArr[blockIndex].sections.forEach((section, sIndex) => {
    section.rows.forEach((row, rIndex) => {
      row.columns.forEach((column, cIndex) => {
        handleFieldChange(blockIndex, sIndex, rIndex, cIndex);
      });
    });
  });

  // Optionally show a toast
  // showSuccess("Section removed", { autoClose: 500 });
};


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


const removeColumn = (blockIndex, sectionIndex, rowIndex, columnIndex) => {
  const row = blockArr[blockIndex].sections[sectionIndex].rows[rowIndex];
  const columns = row.columns;

  const item = columns[columnIndex];
  if (item.parent) deleted_items.push(item);

  if (columns.length === 1) {
    // Remove entire row
    blockArr[blockIndex].sections[sectionIndex].rows.splice(rowIndex, 1);
  } else {
    // Remove only the column
    columns.splice(columnIndex, 1);
  }

  // Re-validate all remaining fields in the block for duplicates
  blockArr[blockIndex].sections.forEach((section, sIndex) => {
    section.rows.forEach((r, rIndex) => {
      r.columns.forEach((c, cIndex) => {
        handleFieldChange(blockIndex, sIndex, rIndex, cIndex);
      });
    });
  });

  // Optionally show toast
  // showSuccess("Column/Row removed", { autoClose: 500 });
};


// Function to remove a column inside a section
// const removeColumn = (blockIndex, sectionIndex, rowIndex, columnIndex) => {
//   let item =
//     blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns[columnIndex];
//   if (item.parent) deleted_items.push(item);
//   blockArr[blockIndex].sections[sectionIndex].rows[rowIndex].columns.splice(
//     columnIndex,
//     1
//   );
//   // showSuccess("Column removed", { autoClose: 500 })
// };

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
  // showSuccess("Field removed", { autoClose: 500 })
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



function isRestricted(label) {
  return restrictedLabels.includes(label?.trim().toLowerCase());
}

// function hasInvalidCharacters(label) {
//   return /[^a-zA-Z0-9 _/]/.test(label) || label.includes('"') || label.includes("'");
// }
function hasInvalidCharacters(label) {
  return /[^a-zA-Z0-9 _\/!@#$%^&*()?.:;|/\\[\]{}]/.test(label) || label.includes('"') || label.includes("'");
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

  // function validateLabel(label, errorPath) {
  //   if (isRestricted(label)) {
  //     errorPath.errorMsg = "Entered label is restricted";
  //   } else if (hasInvalidCharacters(label)) {
  //     errorPath.errorMsg = "Label should not contain special characters, double quotes (\") or single quotes (')";
  //   } else {
  //     errorPath.errorMsg = duplicateLabels.includes(label.trim().toLowerCase())
  //       ? "Duplicate Label Name"
  //       : "";
  //   }
  // }
    function validateLabel(label, errorPath) {
    if (!label) {
      errorPath.errorMsg = "";
      return;
    }

    if (isRestricted(label)) {
      errorPath.errorMsg = "Entered label is restricted";
    } else if (hasInvalidCharacters(label)) {
      errorPath.errorMsg =
        "Label should not contain special characters, double quotes (\") or single quotes (')";
    } else if (label.length > 64) {
      errorPath.errorMsg = "Label should not exceed 64 characters";
    } else {
      errorPath.errorMsg = duplicateLabels.includes(label.trim().toLowerCase())
        ? "Duplicate Label Name"
        : "";
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
   blockArr.forEach((block) => {
    block.sections.forEach((section) => {
      validateLabel(section.label, section);
      section.rows.forEach((row) => {
        row.columns.forEach((column) => {
          validateLabel(column.label, column);
          column.fields.forEach((field) => {
            validateLabel(field.label, field);
          });
        });
      });
    });
  });
}


const hasErrors = computed(() => {
  function checkFieldErrors(obj) {
    if (!obj || typeof obj !== "object") return false;

    // Check for errors in fieldtype, error messages, or empty options for select types
    if (
      ("fieldtype" in obj && obj.fieldtype === "") ||
      ("error" in obj && obj.error) ||
      ("errorMsg" in obj && obj.errorMsg) ||
      (["Select", "Table MultiSelect"].includes(obj.fieldtype) &&
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
  let inputValue = event.target.value.trim();  // ✅ only trims start and end
  if (!inputValue) {
    if (fieldType === "form_name") {
      formNameError.value = "Input cannot be empty or only spaces";
    } else if (fieldType === "form_short_name") {
      formShortNameError.value = "Input cannot be empty or only spaces";
    }
    return;
  }
   if (inputValue.length > 63) {
    if (fieldType === "form_name") {
      formNameError.value = "Name cannot exceed 63 characters";
    } else if (fieldType === "form_short_name") {
      formShortNameError.value = "Short name cannot exceed 63 characters";
    }
    return;
  }
  // Check if the first character is a number
  if (/^\d/.test(inputValue)) {
    if (fieldType === "form_short_name") {
      formShortNameError.value = "First character must be a letter";
    }
    return;
  } else {
    formShortNameError.value = ""; // Clear error if input is valid
  }
    if (fieldType === "form_short_name" && inputValue.length < 2) {
    formShortNameError.value = "Short name must have at least 2 letters";
    return;
  }
  if (fieldType === "form_short_name" && /[^a-zA-Z ]/.test(inputValue)) {
    formShortNameError.value = "Only alphabets and spaces are allowed";
    return;
  }
  // Check for special characters (allow only letters and numbers)
  if (/[^a-zA-Z0-9& ]/.test(inputValue)) {  // ✅ allow spaces inside
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
  const filters = [
    [fieldType, "=", `${inputValue}`],
    ["business_unit", "=", `${filterObj.value.business_unit}`],
  ];
  const queryParams = {
    fields: JSON.stringify(['form_name','form_short_name']),
    filters: JSON.stringify(filters),
    doctype:doctypes.EzyFormDefinitions,
  };

  axiosInstance
    .get(`${apis.GetDoctypeData}`, {
      params: queryParams,
    })
    .then((res) => {
      ezyFormsData.value = res.message.data;

      // Check for duplicates (ignore spaces when comparing)
      if (fieldType === "form_name") {
        formNameError.value =
          inputValue &&
            ezyFormsData.value.some(
              (item) =>
                item.form_name &&
                item.form_name.replace(/\s+/g, "").toLowerCase() ===
                inputValue.replace(/\s+/g, "").toLowerCase()
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
                inputValue.replace(/\s+/g, "").toLowerCase()
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
        // console.log(object);
        formData();
      }
    });
}

async function saveFormData(type) {
  // Check for errors
  if (hasErrors.value) {
    showError("Please fix the errors before proceeding.");
    return;
  }
  isBlockRemoved.value = true;
  let data = deleted_items.flatMap(extractFieldnames);

  if (paramId != undefined && paramId != null && paramId != "new" && data.length) {
    delete_form_items_fields();
  } else {
    formData(type);
  }
}

const hasDuplicates = (array) => new Set(array).size !== array.length;

// ===== DRAG-AND-DROP FIELD LIBRARY HANDLERS =====

// Handle field added from library (click)
const handleFieldAddFromLibrary = (frappeFieldType) => {
  console.log('Field added from library:', frappeFieldType);

  // Get current block based on active tab
  const currentBlockIndex = currentBuilderTab.value;
  const currentBlock = blockArr[currentBlockIndex];

  if (!currentBlock) {
    showError('Please create a block first before adding fields');
    return;
  }

  // Create field from Frappe fieldtype
  const newField = createFieldFromFrappeType(frappeFieldType);

  if (!newField) {
    return;
  }

  // Add to block's sections
  if (!currentBlock.sections) {
    currentBlock.sections = [];
  }

  if (currentBlock.sections.length === 0) {
    currentBlock.sections.push({
      label: '',
      rows: [[{ label: '', fields: [] }]]
    });
  }

  // Add to first section, first row, first column
  const firstSection = currentBlock.sections[0];
  const firstRow = firstSection.rows[0];
  const firstColumn = firstRow[0];

  if (!firstColumn.fields) {
    firstColumn.fields = [];
  }

  firstColumn.fields.push(newField);

  console.log('Field added successfully:', newField);
  showSuccess(`${newField.label} field added successfully`);
};

// Handle drag start from library
const handleFieldDragStart = (frappeFieldType) => {
  console.log('Drag started:', frappeFieldType);
  draggedFieldType.value = frappeFieldType;
};

// Handle drag end from library
const handleFieldDragEnd = () => {
  // Don't clear draggedFieldType here, let the drop handler do it
  console.log('Drag ended');
};

// Create field object from Frappe fieldtype
const createFieldFromFrappeType = (frappeFieldType) => {
  console.log('Creating field from Frappe type:', frappeFieldType);

  // Find the field definition from fieldTypes array
  const fieldDef = fieldTypes.find(ft => ft.type === frappeFieldType);

  if (!fieldDef) {
    console.error('Field type not found:', frappeFieldType);
    console.error('Available types:', fieldTypes.map(ft => ft.type));
    showError(`Field type "${frappeFieldType}" not found. Please try again.`);
    return null;
  }

  // Generate unique field name
  const timestamp = Date.now();
  const randomSuffix = Math.random().toString(36).substring(2, 6);
  const fieldname = `field_${timestamp}_${randomSuffix}`;

  return {
    id: `field_${timestamp}_${randomSuffix}`,
    fieldname: fieldname,
    label: fieldDef.label,
    fieldtype: fieldDef.type,
    options: '',
    reqd: 0,
    read_only: 0,
    hidden: 0,
    description: '',
    default: '',
    placeholder: '',
  };
};

</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>

<style lang="scss" scoped>

// ===== ZOHO-STYLE FORM BUILDER LAYOUT =====

.zoho-form-builder {
  display: flex;
  flex-direction: column;
  height: calc(100vh - 120px);
  background: #ffffff;
  margin: -1rem;
  margin-top: 0;
}

// Top Toolbar
.zoho-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0.75rem 1rem;
  background: #ffffff;
  border-bottom: 1px solid #e5e7eb;
  gap: 1rem;

  .toolbar-left {
    flex-shrink: 0;
  }

  .toolbar-right {
    flex-shrink: 0;
    display: flex;
    gap: 0.5rem;
  }
}

// Tab Navigation
.zoho-tabs {
  display: flex;
  gap: 0.25rem;
  overflow-x: auto;
  flex: 1;
  align-items: center;

  &::-webkit-scrollbar {
    height: 4px;
  }

  &::-webkit-scrollbar-thumb {
    background: #d1d5db;
    border-radius: 2px;
  }
}

.zoho-tab {
  display: flex;
  align-items: center;
  padding: 0.5rem 1rem;
  background: #f9fafb;
  border: 1px solid #e5e7eb;
  border-radius: 6px 6px 0 0;
  font-size: 13px;
  white-space: nowrap;
  transition: all 0.2s;
  cursor: pointer;

  &:hover {
    background: #f3f4f6;
  }

  &.active {
    background: #ffffff;
    border-bottom-color: #ffffff;
    font-weight: 500;
    margin-bottom: -1px;
  }

  i.bi-x-lg {
    font-size: 10px;
    opacity: 0.6;

    &:hover {
      opacity: 1;
      color: #ef4444;
    }
  }
}

.zoho-tab-add {
  background: transparent;
  border: 1px dashed #d1d5db;
  color: #6b7280;

  &:hover {
    border-color: #9ca3af;
    background: #f9fafb;
  }
}

// Main Builder Container
.zoho-builder-container {
  display: flex;
  flex: 1;
  overflow: hidden;
}

// Left: Field Library
.zoho-field-library {
  width: 300px;
  background: #ffffff;
  border-right: 2px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;
  transition: width 0.3s ease;

  &.collapsed {
    width: 60px;

    .library-header h6 {
      font-size: 12px;
      writing-mode: vertical-rl;
    }
  }

  .library-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-bottom: 2px solid #e5e7eb;
    background: #f9fafb;
    cursor: pointer;
    transition: background 0.2s;

    &:hover {
      background: #f3f4f6;
    }

    h6 {
      font-size: 14px;
      font-weight: 600;
      color: #111827;
    }

    .btn-link {
      color: #6b7280;
      text-decoration: none;
      transition: color 0.2s;

      &:hover {
        color: #111827;
      }
    }
  }

  .library-content {
    flex: 1;
    overflow-y: auto;
    padding: 0;

    &::-webkit-scrollbar {
      width: 6px;
    }

    &::-webkit-scrollbar-thumb {
      background: #d1d5db;
      border-radius: 3px;
    }
  }
}

// Center: Form Canvas
.zoho-form-canvas {
  flex: 1;
  overflow-y: auto;
  background: #f9fafb;
  padding: 1.5rem;

  .canvas-inner {
    min-height: 100%;
    background: #ffffff;
    border-radius: 8px;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);

    // Remove extra padding/margin from block content
    .block-level {
      padding: 0;
    }

    .requestandAppHeader {
      margin-bottom: 0;
      padding: 1.25rem 1.5rem;
      background: #f9fafb;
      border-bottom: 2px solid #e5e7eb;
      border-radius: 8px 8px 0 0;
    }

    .section_block {
      padding: 1.5rem;
    }
  }

  &::-webkit-scrollbar {
    width: 8px;
  }

  &::-webkit-scrollbar-thumb {
    background: #d1d5db;
    border-radius: 4px;

    &:hover {
      background: #9ca3af;
    }
  }
}

// Right: Properties Panel
.zoho-properties-panel {
  width: 320px;
  background: #ffffff;
  border-left: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
  flex-shrink: 0;

  .properties-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1rem;
    border-bottom: 1px solid #e5e7eb;

    h6 {
      font-size: 14px;
      font-weight: 600;
      color: #111827;
    }

    .btn-link {
      color: #6b7280;
      text-decoration: none;

      &:hover {
        color: #111827;
      }
    }
  }

  .properties-content {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
  }
}

// Mobile Responsive
@media (max-width: 992px) {
  .zoho-builder-container {
    flex-direction: column;
  }

  .zoho-field-library {
    width: 100%;
    max-height: 200px;
    border-right: none;
    border-bottom: 1px solid #e5e7eb;
  }

  .zoho-properties-panel {
    width: 100%;
    max-height: 250px;
    border-left: none;
    border-top: 1px solid #e5e7eb;
  }

  .zoho-form-canvas {
    padding: 1rem;

    .canvas-inner {
      padding: 1rem;
    }
  }

  .zoho-toolbar {
    flex-wrap: wrap;
    gap: 0.5rem;

    .toolbar-left,
    .toolbar-right {
      width: 100%;
      display: flex;
      justify-content: space-between;
    }
  }

  .zoho-tabs {
    width: 100%;
    overflow-x: auto;
  }
}

// ===== END ZOHO-STYLE STYLES =====

.approver_type_div{
  border: 1px solid #BAFFC2;
  border-radius: 6px;
  padding: 2px 4px;
  color: #00C917;
  background-color: #EAFFED;
}
.approver_type_div span{
  font-size: 11px;
  color: #23b207;
  font-weight: 500;
  padding: 0px 4px;
  
}
.approver_type_div i{
  color: #23b207;
  font-weight: 900;
  -webkit-text-stroke: 1px #23b207;
}
.formlist {
  max-height: 180px;
  /* 🔥 Set desired height */
  overflow-y: auto;
  /* 🔥 Enable vertical scroll */
  overflow-x: hidden;
  border: 1px solid #dcdcdc;
  border-radius: 4px;
  background-color: white;
  z-index: 999;
}

.formlistitem {
  cursor: pointer;
}

.formlistitem:hover {
  background-color: #f0f0f0;
}

.PredefinedLabel {
  font-size: 12px;
  margin-left: 10px;
  border: 1px solid #ccc;
  padding: 2px 5px;
  border-radius: 5px;
  background-color: #f9f9f9;
  left: 70px;
  // right: 0;



}

.standardFormInput:focus {
  box-shadow: none;
  outline: 0;
  border: 1px solid #000;

}

.linketoCheck {
  width: 18px;
}

.aboutFields {
  height: 80dvh;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 10px;
  padding-bottom: 40px;
}

.addOffCanvas {
  width: 530px;
}

.SearchDesignation {
  border: none;
  border-bottom: 1px solid #ccc;

}

// .approval-border-bottom {
//   border-bottom: 1px solid #ccc;
// } 

.rounded-table {
  border-radius: 10px;
  background-color: #ccc;
  overflow: hidden;
  /* This ensures child elements respect the border radius */
}

.draggable-item {
  border: 1px dashed #ccc;
  padding: 10px;
  margin-bottom: 8px;
  cursor: grab;
  background: #f9f9f9;
}

.draggable-item:active {
  cursor: grabbing;
}

.stepsDiv {
  margin-top: 0;
}

.note {
  display: flex;
  align-items: center;
  height: 93%;
}

.backBtn {
  box-shadow: rgba(100, 100, 111, 0.2) 0px 7px 29px 0px;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.download_btn {
  border: 1px solid rgb(36, 220, 36);
  color: rgb(36, 220, 36);
  background: transparent;
  border-radius: 10px;
}

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
  color: #000;
}

.designation-scroll {
  max-height: 500px;
  /* or any height you prefer */
  overflow-y: auto;
  padding-right: 8px;
  /* prevent content from hiding under scrollbar */
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
  background: #ffffff;
  border-radius: 12px;
  padding: 1.5rem 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  border: 1px solid #e5e7eb;
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
  margin: 8px 2px;
  padding: 5px;
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
  height: 18px;
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
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.steps li {
  padding: 1rem 1.25rem;
  font-size: 14px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  width: 100%;
  position: relative;
  border-radius: 8px;
  background: transparent;

  &:hover {
    background: #f9fafb;
  }

  .step-text {
    span:first-child {
      color: #6b7280;
      font-size: 11px;
      font-weight: 500;
      text-transform: uppercase;
      letter-spacing: 0.5px;
    }

    span:last-child {
      color: #374151;
      font-size: 14px;
      font-weight: 500;
      margin-top: 0.25rem;
    }
  }

  i {
    font-size: 20px;
    color: #9ca3af;
  }
}

.steps li.active {
  background: #eff6ff;
  border: 1px solid #dbeafe;

  .step-text {
    span {
      color: #1e40af;
    }
  }

  i {
    color: #2563eb;
  }
}

.completedStepIcon {
  color: #10b981;
  font-size: 20px;
}

.steps li.completed {
  opacity: 1;

  .step-text {
    span {
      color: #6b7280;
    }
  }

  i {
    color: #10b981;
  }
}

.steps li.completed::after {
  content: "";
  display: block;
  width: 2px;
  height: 1.5rem;
  background-color: #e5e7eb;
  position: absolute;
  border-radius: 2px;
  left: 1.85rem;
  top: calc(100% - 0.5rem);
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
  border: 1px solid #000;
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

// .add-section-btn {
//   position: sticky;
//   bottom: 80px;
//   z-index: 1;
//   // background-color: #ffffff; 
// }

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
  padding: 12px 6px;
  // box-shadow: 0px 4px 4px 0px #0000000d; 
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
  color: #1b14df;
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

.empty-drop-zone {
  border: 2px dashed #bbb;
  padding: 20px;
  text-align: center;
  color: #999;
  background-color: #f9f9f9;
}
:deep(.vs__selected) {
  background: #fff;
  border: 1px solid #dee2e6;
  border-radius: 16px;
  padding: 0px 8px;
  font-size: 12px;
}

:deep(.vs__selected-options) {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  padding: 1px;
}

:deep(.vs__dropdown-toggle) {
  height: auto !important;
}


:deep(.vs__deselect) svg {
  color: #000;
  background-color: #f1f1f1 ;
  border-radius: 50%;
  margin-left: 4px;
  margin-top: 8px;
  font-size: 5px !important;

  padding: 4px;

}

:deep(.vs__deselect:hover) {
  color: #000;
}
.vue3-select__dropdown,
.vue3-select-dropdown {
  z-index: 9999 !important;
}

/* Vue 3 SFC scoped style */
::v-deep(.vs__dropdown-toggle) {
  border: 1px solid transparent !important;
  border-radius: 6px;
  border-top-left-radius: 0 !important;
  border-top-right-radius: 0 !important;
  transition: border-color 0.15s ease;
  padding: 2px;

}

/* when dropdown is open or focused */
::v-deep(.vs__dropdown-toggle.vs--open),
::v-deep(.vs__dropdown-toggle:focus),
::v-deep(.vs__dropdown-toggle:focus-within) {
  border: 1px solid #1b14df !important;
  border-top-left-radius: 0 !important;
  border-top-right-radius: 0 !important;
  box-shadow: none !important;
  outline: none !important;
  padding:2px;
}
/* Placeholder styling for Vue3Select */
::v-deep(.vs__search::placeholder) {
  color: #9ca3af !important;  /* grey placeholder text */
  font-size: 13px !important; /* adjust size */
  opacity: 1;                 /* make sure it’s visible */
  padding: 2px 6px;
}




.disgnationlist_div{
  border: 1px solid #CCCCCC !important;
  border-radius: 6px;
  
  // padding: 0px 4px;
}
::v-deep(.vs__selected) {
  // min-width: 100px; /* adjust per tag */
  margin: 1px;
  max-height: 30px;
}
::v-deep(.vs__selected-options) {
  max-height: 130px; /* 4 rows * 40px per tag */
  overflow-y: auto;
  flex-wrap: wrap;
}
/* Selected tags container */
::v-deep(.vs__selected-options) {
  display: flex;
  max-width: calc(4 * 120px); /* show 4 tags */
  overflow-x: auto;            /* scroll only if needed */
  scrollbar-width: thin;       /* Firefox */
  white-space: nowrap;          /* prevent wrapping */
}

/* Hide scrollbar by default */
::v-deep(.vs__selected-options::-webkit-scrollbar) {
  display: none;
}

/* Show scrollbar on hover */
::v-deep(.vs__selected-options:hover::-webkit-scrollbar) {
  display: block;
}

/* Optional: Firefox */
::v-deep(.vs__selected-options) {
  scrollbar-color: #ccc transparent;
  scrollbar-width: thin;
}

</style>
