<template>
  <div class="container-fluid">
    <div class="main-div">

    <!-- Comparison Modal -->
    <div class="modal fade" id="comparisonModal" tabindex="-1">
      <div class="modal-dialog modal-dialog-centered modal-xl">
        <div class="modal-content p-4">
          <div class="d-flex justify-content-between mb-3">
            <h6 class="fw-bold">Preview Comparison</h6>
            <button class="btn btn-outline-danger btn-sm" data-bs-dismiss="modal">Close</button>
          </div>





        </div>
      </div>
    </div>
    <!-- Preview Modal -->
    <div class="modal fade" id="filePreviewModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-xl modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Attachment Preview</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body d-flex">
            <!-- Left panel: file list -->
            <div class="me-3" style="min-width: 200px;">
              <ul class="list-group">
                <li class="list-group-item" v-for="(url, index) in vendorForm.attachments"
                  :class="{ 'selected-file': previewUrl === url }" :key="index" @click="previewUrl = url"
                  style="cursor: pointer;">
                  {{ url.split('/').pop() }}
                </li>
              </ul>
            </div>

            <!-- Right panel: preview -->
            <div style="flex-grow: 1;">
              <iframe v-if="previewUrl" :src="previewUrl" style="width: 100%; height: 600px;" frameborder="0"></iframe>
              <p v-else>No preview available.</p>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="d-flex flex-column justify-content-between" style="min-height: 300px">
      <!-- Main Content Area Based on Step -->
      <div class="flex-grow-1">
        <div v-if="currentStep === 0">
          <!-- Step 1: Vendor & Item Details -->
          <!-- <h5>Step 1: Vendor & Item Details</h5> -->
          <!-- Put Item & Vendor Accordions Here -->
          <div class="">

            <div class="d-flex justify-content-between align-items-center back_div mb-2">
              <div><button class="font-12 m-0 btn" @click="router.back()"> <i class="bi bi-chevron-left"></i>
                  Back</button>
              </div>
              <div>
                <!-- <button class="btn btn-outline-secondary btn-sm me-2" @click="previewComparison">Preview
            comparison</button>
          <button class="btn btn-dark btn-sm" :class="{ 'bg-dark': itemDetails.length && vendorMasterList.length }"
            @click="submitComparison">Submit comparison</button> -->
              </div>
            </div>

            <div class="accordion container-fluid " id="accordionExample">
              <!-- Item Details Accordion -->
              <div class="accordion-item">
                <h2 class="accordion-header">
                  <button class="accordion-button" type="button" data-bs-toggle="collapse"
                    data-bs-target="#collapseItems" aria-expanded="true">
                    Item details
                  </button>
                </h2>
                <div id="collapseItems" class="accordion-collapse collapse show">
                  <div class="accordion-body">

                    <table class="table shadow-sm  rounded-table">
                      <thead class="table-light  ">
                        <tr>
                          <th scope="col"><input type="checkbox"></th>
                          <th>Item name</th>
                          <th>Unit of measure</th>
                          <th>Item Quantity</th>
                          <th>Action</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(item, index) in itemDetails" :key="index">
                          <td width="3%"><input type="checkbox" v-model="item.selected"></td>
                          <td class="editable-row  position-relative " @click="editItem(index)">
                             <template v-if="editingIndex === index">
                           
                              <input
                                :id="`item-name-${index}`"
                                class="form-control form-control-sm"
                                v-model="item.item_name"
                                @focus="activeDropdown = index"
                                @input="activeDropdown = index"
                                @blur="closeDropdown(index)"
                                placeholder="Search item"
                                ref="itemInputs"
                              />
                             
                              <ul v-if="activeDropdown === index"
                                
                                class="dropdown-menu show w-100"
                                style="position: absolute; top: 100%; left: 0; max-height: 200px; overflow-y: auto; z-index: 1055;"
                              >
                                <li
                                  v-for="option in filteredOptions(item.item_name)"
                                  :key="option"
                                  class="dropdown-item font-12"
                                  @mousedown.prevent="selectItem(option, index)"
                                >
                                  {{ option }}
                                </li>
                                <li class="dropdown-item text-primary font-12" @mousedown.prevent="openNewItemModal">
                                  + Add new item
                                </li>
                              </ul>
                            
                          </template>
                            <!-- <template v-if="editingIndex === index">
                              <input v-model="item.item_name" class="form-control form-control-sm">

                            </template>  -->
                            <template v-else>{{ item.item_name }}</template>
                          </td>
                          <td class="editable-row" @click="editItem(index)">
                            <template v-if="editingIndex === index">
                              <input v-model="item.unit_of_measure" class="form-control form-control-sm">
                            </template>
                            <template v-else>
                              {{ item.unit_of_measure }}
                            </template>
                          </td>
                          <td class="editable-row" @click="editItem(index)">
                            <template v-if="editingIndex === index">
                              <input v-model="item.quantity" type="number" class="form-control form-control-sm">
                            </template>
                            <template v-else>
                              {{ item.quantity }}
                            </template>
                          </td>
                          <td>
                            <template v-if="editingIndex === index">
                              <i class="bi bi-check-lg text-success me-2" @click="saveItem()"></i>
                              <i class="bi bi-x-lg text-danger" @click="cancelEdit()"></i>
                            </template>
                            <template v-else>
                              <i class="bi bi-pencil-square me-2" @click.stop="editItem(index)"></i>
                              <i class="bi bi-trash" @click="deleteItem(index)"></i>
                            </template>
                          </td>
                        </tr>
                      </tbody>
                    </table>

                    <div>
                      <button v-if="hasSelectedItems" class="btn btn-danger btn-sm" @click="deleteSelectedItems"><i
                          class="bi bi-trash"></i>
                        Delete Item</button>
                      <button class="btn  add_item_btn  ms-2" @click="openItemModal"><i class="bi bi-plus "></i> Add
                        Item</button>
                    </div>
                    <!-- <button v-if="itemDetails.length" class="btn btn-success btn-sm ms-2" @click="saveItems">Save
                  Items</button> -->

                  </div>
                </div>
              </div>
              <!-- Add Item Modal -->
              <div class="modal fade" id="itemModal" tabindex="-1" aria-labelledby="itemModalLabel" aria-hidden="true">
                <div class="modal-dialog modal-lg modal-dialog-scrollable">
                  <div class="modal-content">
                    <div class="modal-header">
                      <h5 class="modal-title">Select Items</h5>
                      <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                      <!-- Search Input -->
                       <!-- <input type="text" class="form-control mb-3" placeholder="Search items..." v-model="searchItem" /> -->

                      <!-- Add New Item -->
                      <div class="d-flex gap-2 mb-3">
                        <input type="text" class="form-control" placeholder="Item name" v-model="newItem.name" />
                        <input type="text" class="form-control" placeholder="Unit" v-model="newItem.unit" />
                        <button class="btn btn-sm btn-dark" @click="addNewItem">Add</button>
                      </div>

                      <!-- Item Table -->
                      <div style="max-height: 300px; overflow-y: auto;">
                        <table class="table table-sm table-hover">
                          <thead>
                            <tr>
                              <th><input type="checkbox" @change="toggleSelectAll($event)" /></th>
                              <th>Item Name</th>
                              <th>Unit of Measure</th>
                            </tr>
                          </thead>
                          <tbody>
                            <tr v-for="(item, index) in filteredItems" :key="index">
                              <td><input type="checkbox" v-model="item.selected" /></td>
                              <td @click="toggleItemSelection(item)">{{ item.item_name }}</td>
                              <td @click="toggleItemSelection(item)">{{ item.unit_of_measure }}</td>
                            </tr>
                          </tbody>
                        </table>
                      </div>
                    </div>

                    <div class="modal-footer">
                      <button class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
                      <button class="btn btn-dark" @click="confirmItemSelection">Add Selected Items</button>
                    </div>
                  </div>
                </div>
              </div>


              <!-- Vendor Details Accordion (unchanged) -->
              <div class="accordion-item">
                <h2 class="accordion-header">
                  <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse"
                    data-bs-target="#collapseVendors">
                    Vendor details
                  </button>
                </h2>
                <div id="collapseVendors" class="accordion-collapse collapse">
                  <div class="accordion-body">


                    <table class="table table-bordered shadow-sm rounded-table">
                      <thead class="table-light">
                        <tr>
                          <th scope="col"><input type="checkbox"></th>
                          <th>Bidder Rank</th>
                          <th>Vendor name</th>
                          <th>GST number</th>
                          <th>Contact</th>
                          <th>Email</th>
                          <th>Total value in &#8377;</th>
                          <th>Action</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(vendor, index) in vendorDetails" :key="index">
                          <td width="3%"><input type="checkbox" v-model="vendor.selected"></td>

                          <td class="d-flex justify-content-between">{{ vendor.rank }} <span v-if="vendor.rank === 'L1'"
                              class="badge font-12 "> <i class=" text-success bi bi-check-circle-fill"></i></span></td>
                          <td>{{ vendor.vendor_name }}</td>
                          <td>{{ vendor.gst_number }}</td>
                          <td>{{ vendor.phone_number }}</td>
                          <td>{{ vendor.mail_id }}</td>
                          <td>{{ vendor.total_value }}</td>
                          <td>
                            <i class="bi bi-pencil-square" @click="openVendorModal(index)"></i>
                          </td>
                        </tr>
                      </tbody>
                    </table>

                    <div>
                      <button v-if="hasSelectedVendor" class="btn btn-danger btn-sm" @click="deleteSelectedVendors"><i
                          class="bi bi-trash"></i> Delete
                        Vendor</button>
                      <button class="btn  add_vendor_btn btn-sm ms-2" @click="addVendorModal"><i class="bi bi-plus"></i>
                        Add
                        Vendor</button>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Vendor Edit Modal -->
            <div class="modal fade" id="vendorModal" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1">
              <div class="modal-dialog modal-xl">
                <div class="modal-content p-4">
                  <div class="d-flex justify-content-between mb-3">
                    <h6 class="fw-bold">Editing Row #{{ vendorDetails.length + 1 }}</h6>
                    <div>
                      <button class="btn btn-outline-danger btn-sm me-2" @click="filterVendors == ''"
                        data-bs-dismiss="modal">Close</button>
                      <button class="btn btn-dark  btn-sm" @click="saveVendorDetails">Save Vendor
                        details</button>
                    </div>
                  </div>



                  <div class="row g-2 mb-3">
                    <div class="col-md-3">

                      <label class="form-label">Vendor Name</label>
                      <input type="text" class="form-control form-control-sm" placeholder="Type vendor name..."
                        v-model="vendorForm.vendor_name" @input="filterVendors" />
                      <div v-if="filteredVendorOptions.length" class="border rounded mt-1 bg-light"
                        style="max-height: 150px; overflow-y: auto;z-index: 1000;">
                        <div v-for="vendor in filteredVendorOptions" :key="vendor.vendor_name"
                          class="py-2 px-2  border-1   font-12" style="cursor: pointer; border-bottom: 1px solid #ccc;"
                          @click="selectVendor(vendor)">
                          {{ vendor.vendor_name }}
                        </div>
                      </div>

                      <!-- <label class="form-label">Vendor name</label>
                <input v-model="vendorForm.vendor_name" class="form-control form-control-sm"> -->
                    </div>
                    <div class="col-md-3">
                      <label class="form-label">GST number</label>
                      <input v-model="vendorForm.gst_number" class="form-control form-control-sm">
                    </div>
                    <div class="col-md-3">
                      <label class="form-label">Phone number</label>
                      <input v-model="vendorForm.phone_number" class="form-control form-control-sm">
                    </div>
                  </div>
                  <div class=" row g-2 mb-3">
                    <div class="col-md-6">
                      <label class="form-label">Email ID</label>
                      <input v-model="vendorForm.mail_id" class="form-control form-control-sm">
                    </div>


                    <div class="col-md-6">
                      <label class="form-label">Attachments</label>
                      <input type="file" multiple accept=".jpeg,.jpg,.png,.pdf,.xlsx,.xls"
                        class="form-control form-control-sm" @change="handleFileUpload">
                    </div>
                    <div class=" col-md-3">
                      <label class="form-label">Address</label>
                      <textarea v-model="vendorForm.address" class="form-control form-control-sm"></textarea>
                    </div>
                  </div>

                  <div class="mb-3">
                    <h6 class="fw-bold">Pricing details</h6>
                    <table class="table table-bordered ">
                      <thead class="table-light">
                        <tr>
                          <th scope="col"><input type="checkbox"></th>
                          <th>Item name</th>
                          <th>Quantity</th>
                          <th>Price / unit</th>
                          <th>Price / total Qty</th>
                          <th>Action</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(item, index) in vendorForm.ezy_item_details" :key="index">
                          <td width="3%"><input type="checkbox" v-model="item.selected"></td>
                          <td>

                            {{ item.item_name }}

                          </td>
                          <td>

                            {{ item.quantity }}

                          </td>
                          <td @click="editItemInModal(index)">
                            <template v-if="editingItemIndex === index">
                              <input @blur="saveEditedItem" @focus="editItemInModal(index)"
                                v-model.number="item.unitPrice" @change="updateTotalPrice(item)" type="number"
                                class="form-control form-control-sm">
                            </template>
                            <template v-else>
                              ₹ {{ item.unitPrice }}
                            </template>
                          </td>
                          <td>
                            ₹ {{ item.totalPrice }}
                          </td>

                          <td>
                            <template v-if="editingItemIndex === index">
                              <i class="bi bi-check-lg text-success me-2" @click="saveEditedItem"></i>
                              <i class="bi bi-x-lg text-danger" @click="cancelEditItem"></i>
                            </template>
                            <template v-else>
                              <i class="bi bi-pencil-square" @click="editItemInModal(index)"></i>
                              <i class="bi bi-trash text-danger ms-2" @click="deleteChildItem(index)"></i>
                            </template>
                          </td>
                        </tr>
                      </tbody>
                    </table>

                    <!-- <button class="btn btn-danger btn-sm" @click="deleteSelectedChildItems">Delete Item</button>
              <button class="btn btn-outline-secondary btn-sm ms-2" @click="addChildItem">+ Add Item</button> -->
                  </div>

                  <div class="row g-2">
                    <div class="col-md-3">
                      <label class="form-label">Transportation charges</label>
                      <select v-model="vendorForm.transport" class="form-select form-select-sm">
                        <option>Free delivery</option>
                        <option>Paid delivery</option>
                      </select>
                    </div>

                    <div class="col-md-3">
                      <label class="form-label">Bidder rank</label>
                      <select v-model="vendorForm.rank" class="form-select form-select-sm">
                        <option>L1</option>
                        <option>L2</option>
                        <option>L3</option>
                      </select>
                    </div>
                    <div class="col-md-3">
                      <label class="form-label">Total price</label>
                      <input v-model="vendorForm.total_value" class="form-control form-control-sm" readonly>
                    </div>
                  </div>
                  <div class="row g-2">
                    <div class="col-md-3">
                      <label class="form-label">Delivery time (in days)</label>
                      <input v-model="vendorForm.deliveryTime" class="form-control form-control-sm">
                    </div>
                    <div class="col-md-3">
                      <label class="form-label">Payment terms (in days)</label>
                      <input v-model="vendorForm.paymentTerms" class="form-control form-control-sm">
                    </div>
                  </div>

                  <div class="mt-3">
                    <label class="form-label">Remark</label>
                    <textarea v-model="vendorForm.remark" name="remarks" class=" form-control" id=""></textarea>
                    <!-- <input v-model="vendorForm.remark" class="form-control form-control-sm"> -->
                  </div>

                </div>
              </div>
            </div>
          </div>
        </div>
        <div v-else-if="currentStep === 1">
          <div class="d-flex justify-content-between align-items-center back_div mb-2">
            <div><button class="font-12 m-0 btn" @click="prevStep" :disabled="currentStep === 0"> <i
                  class="bi bi-chevron-left"></i>
                Back</button>
            </div>
            <div>
              <button class="btn export_btn btn-sm me-2"><i class="bi bi-download me-2"></i> Export
              </button>

            </div>
          </div>
          <!-- Step 2: Preview Comparison -->
          <!-- <h5>Step 2: Preview Comparison</h5> -->
          <div class="container">
            <table v-if="vendorDetails.length" class="table table-bordered">
              <thead class="table-light">
                <tr>
                  <th>Item name</th>
                  <th v-for="vendor in vendorDetails" :key="vendor.vendor_name">
                    {{ vendor.vendor_name }} <span class="text-muted">(rate/unit)</span>
                  </th>
                </tr>
              </thead>

              <tbody>
                <!-- Item rows -->
                <tr v-for="item in itemDetails" :key="item.name">
                  <td>
                    {{ item.item_name }}
                    <span class="badge bg-secondary">{{ item.quantity }} {{ item.unit_of_measure }}</span>
                  </td>
                  <td v-for="vendor in vendorDetails" :key="vendor.vendor_name">
                    ₹ {{ getVendorItemPrice(vendor, item.name) }}
                  </td>
                </tr>

                <!-- Total row -->
                <tr>
                  <td>Total</td>
                  <td v-for="vendor in vendorDetails" :key="vendor.vendor_name">
                    <b>₹ {{ getVendorTotal(vendor) }}</b> /total qty
                  </td>
                </tr>

                <!-- Separator row -->
                <tr>
                  <td :colspan="vendorDetails.length + 1" class="text-muted text-center ">
                    Additional Information
                  </td>
                </tr>

                <!-- Company detail rows -->
                <tr>
                  <td>Payment Terms</td>
                  <td v-for="vendor in vendorDetails" :key="vendor.vendor_name">
                    {{ vendor.paymentTerms || '-' }}
                  </td>
                </tr>
                <tr>
                  <td>GST</td>
                  <td v-for="vendor in vendorDetails" :key="vendor.vendor_name">
                    {{ vendor.gst_number || '-' }}
                  </td>
                </tr>
                <tr>
                  <td>Delivery</td>
                  <td v-for="vendor in vendorDetails" :key="vendor.vendor_name">
                    {{ vendor.deliveryTime || '-' }}
                  </td>
                </tr>
                <tr>
                  <td>Bid Rank</td>
                  <td v-for="vendor in vendorDetails" :key="vendor.vendor_name">
                    {{ vendor.rank }}
                  </td>
                </tr>
                <tr>
                  <td>Transport Charges</td>
                  <td v-for="vendor in vendorDetails" :key="vendor.vendor_name">
                    {{ vendor.transport || '-' }}
                  </td>
                </tr>
                <tr>
                  <td>

                    Attachments</td>

                  <td v-for="vendor in vendorDetails" :key="vendor.vendor_name">
                    <span class="text-primary" style="cursor: pointer" @click="openPreview(vendor.attachments)">
                      Preview attachment
                    </span>
                  </td>
                </tr>
                <tr>
                  <td>Comments</td>
                  <td v-for="vendor in vendorDetails" :key="vendor.vendor_name">
                    {{ vendor.remark || '-' }}
                  </td>
                </tr>
              </tbody>
            </table>

          </div>
        </div>
        <div v-else-if="currentStep === 2">
          <div class="d-flex justify-content-between align-items-center back_div mb-2">
            <div><button class="font-12 m-0 btn" @click="prevStep" :disabled="currentStep === 0"> <i
                  class="bi bi-chevron-left"></i>
                Back</button>
            </div>
            <div>


            </div>
          </div>

          <div>
            <!-- Workflow Table -->
            <div class="container-fluid mt-4">
              <div class="workflow-container">
                <!-- Header -->
                <div class="workflow-header">
                  <div>Approval Level</div>
                  <div>Approver Designation</div>
                  <div>On Reject</div>
                  <div>Actions</div>
                </div>

                <!-- Draggable List -->

                <draggable v-model="workflowApprovalLevels" item-key="id" handle=".drag-handle" :animation="150">
                  <template #item="{ element, index }">
                    <div class="workflow-row ">
                      <div>
                        <i class="bi bi-grip-vertical drag-handle fs-6 me-2"></i>
                        Level {{ index + 1 }}
                      </div>

                      <div>
                        <Vue3Select :append-to-body="true" v-if="workflowEditIndex === index"
                          v-model="element.designation" :options="designationOptions"
                          label="label" class="form-control-sm" @keydown.enter="stopWorkflowEditing" />
                        <!-- <input v-if="workflowEditIndex === index" :ref="el => setWorkflowInputRef(el, index)"
                          v-model="element.designation" class="form-control form-control-sm"
                          placeholder="Enter Designation" @keydown.enter="stopWorkflowEditing" /> -->
                        <span v-else>{{ element.designation || '-' }}</span>
                      </div>

                      <div>
                        <select v-if="workflowEditIndex === index" v-model="element.onReject"
                          @keydown.enter="stopWorkflowEditing" class="form-select rounded-0 form-select">
                          <option value="">Level 0</option>
                          <option v-for="(prev, i) in getPreviousWorkflowLevels(index)" :key="prev.id"
                            :value="prev.designation">
                            Level {{ i + 1 }}
                          </option>
                        </select>
                        <span v-else>{{ getRejectLabel(element.onReject) }}</span>
                      </div>

                      <div>
                        <button class="btn  me-1" @click="editWorkflowRow(index)" v-if="workflowEditIndex !== index">
                          <i class="bi bi-pencil font-13"></i>
                        </button>
                        <button class="btn btn-sm me-1" v-if="workflowEditIndex === index" @click="stopWorkflowEditing">
                          <i class="bi bi-check fs-5"></i>
                        </button>
                        <button class="btn btn-sm" @click="removeWorkflowRow(index)">
                          <i class="bi bi-trash"></i>
                        </button>
                      </div>
                    </div>
                  </template>
                </draggable>

                <div class="workflow-footer">
                  <button class="btn border-0  " @click="addWorkflowRow">
                    <i class="bi bi-plus-circle"></i> Add Approver
                  </button>
                </div>
              </div>



            </div>
          </div>
        </div>
      </div>
      <!-- Stepper Navigation -->
      <div
        class="position-fixed bottom-0 font-14 start-0 end-0 d-flex stepper-bottom p-2 m-2 justify-content-between align-items-center ">
        <!-- Stepper Navigation -->
        <div class="d-flex">
          <div v-for="(step, index) in steps" :key="index" class="px-3 py-2" :class="[
            'step-item',
            { active: currentStep === index, completed: index < currentStep }
          ]" style="cursor: pointer;" @click="goToStep(index)">
            <span>
              <i v-if="index < currentStep" class="ms-1  check-icon bi bi-check-circle-fill"></i>
              <i v-else :class="step.icon" class="me-1"></i>
              {{ step.label }}
            </span>
          </div>
        </div>

        <!-- Back / Next Buttons -->
        <div>
          <button class="btn btn-light stepper-back border-1 btn-sm me-2" @click="prevStep"
            :disabled="currentStep === 0">Back</button>
          <button class="btn btn-light next-Submit" @click="nextStep">
            {{ currentStep === steps.length - 1 ? 'Submit form' : 'Next' }}
          </button>
        </div>
      </div>
    </div>
    </div>
  </div>
</template>

<script setup>
import { watch } from 'vue';
import { onMounted } from 'vue';
import { onBeforeUnmount } from 'vue';
import { computed } from 'vue';
import { ref, nextTick } from 'vue';
import { useRoute, useRouter } from "vue-router";
import { apis, doctypes } from '../shared/apiurls';
import axiosInstance from '../shared/services/interceptor';
import { toast } from 'vue3-toastify';
import draggable from "vuedraggable";
import Vue3Select from 'vue3-select'
import 'vue3-select/dist/vue3-select.css';

const route = useRoute();
const router = useRouter()
const searchItem = ref('');
const selectedItems = ref([]);
const vendorSearch = ref('')
const filteredVendorOptions = ref([])
const itemDetails = ref([

]);
const editingIndex = ref(null);

const vendorDetails = ref([

]);
const availableItems = ref([
  // { item_name: 'Computer', unit_of_measure: 'Unit' },
  // { item_name: 'CPU', unit_of_measure: 'Unit' },
  // { item_name: 'Mouse', unit_of_measure: 'Unit' },
  // { item_name: 'Molds', unit_of_measure: 'Kilogram' },
  // { item_name: 'Keyboard', unit_of_measure: 'Unit' },
  // { item_name: 'Monitor', unit_of_measure: 'Unit' },
  // { item_name: 'RAM', unit_of_measure: 'GB' },
  // { item_name: 'SSD', unit_of_measure: 'GB' },
  // { item_name: 'Printer', unit_of_measure: 'Unit' },
  // { item_name: 'Scanner', unit_of_measure: 'Unit' },
  // { item_name: 'Router', unit_of_measure: 'Unit' },
  // { item_name: 'Cable', unit_of_measure: 'Meter' },
  // { item_name: 'Switch', unit_of_measure: 'Unit' },
  // { item_name: 'Hard Drive', unit_of_measure: 'TB' },

]);
const vendorMasterList = ref([
  // { rank: 3, name: 'Daniel White Pvt Ltd', gst: '32434567546554', contact: '8697237439', email: 'srinkhasu@gmail.com', total_value: '', selected: false },
  // { rank: 2, name: 'Jane Johnson Pvt Ltd', gst: '2746345345656', contact: '9954354323', email: 'venkat198@gmail.com', total_value: '', selected: false },
  // { rank: 4, name: 'Robert Wilson Pvt Ltd', gst: '330293878240', contact: '9032873873', email: 'Mail1989@gmail.com', total_value: '', selected: false },
  // { rank: 1, name: 'Sophia Martin Pvt Ltd', gst: '1NH762587654', contact: '9819675625', email: 'Badoi197@gmail.com', total_value: '', selected: false },
  // {
  //   name: 'ABC Traders',
  //   gst: '27ABCDE1234F1Z5',
  //   contact: '9876543210',
  //   email: 'abc@traders.com',
  //   rank: 'L1',
  //   total_value: '',
  //   transport: 'Free delivery',
  //   deliveryTime: '5',
  //   paymentTerms: '30',
  //   remark: 'Preferred vendor',
  //   address: '123 Main St, City, State, 123456'
  // },
  // {
  //   name: 'XYZ Supplies',
  //   gst: '29XYZAB1234C1Z9',
  //   contact: '9123456789',
  //   email: 'xyz@supplies.com',
  //   rank: 'L2',
  //   total_value: '25000',
  //   transport: 'Paid delivery',
  //   deliveryTime: '7',
  //   paymentTerms: '45',
  //   remark: '',
  //   address: '456 Elm St, City, State, 123456'
  // },
  // Add more vendor entries here...
])

const steps = [
  { label: 'Vendor & Item Details', icon: 'bi bi-box-seam' },
  { label: 'Preview Comparison', icon: 'bi bi-eye' },
  { label: 'Workflow', icon: 'bi bi-diagram-3' },
]

const currentStep = ref(0)

const goToStep = (index) => {
  currentStep.value = index
}

const nextStep = () => {
  if (currentStep.value < steps.length - 1) {
    currentStep.value++
  } else {
    // Reset after last step
    currentStep.value = 0
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}
const previewUrl = ref(null)

function openPreview(url) {
  if (vendorForm.value.attachments.length > 0) {
    previewUrl.value = vendorForm.value.attachments[0];
  } else {
    previewUrl.value = '';
  }
  const modal = new bootstrap.Modal(document.getElementById('filePreviewModal'));
  modal.show();
}

function addVendorModal() {
  vendorForm.value = {
    vendor_name: '',
    gst_number: '',
    phone_number: '',
    mail_id: '',
    transport: '',
    deliveryTime: '',
    paymentTerms: '',
    rank: '',
    remark: '',
    total_value: '',
    address: '',
    ezy_item_details: JSON.parse(JSON.stringify(itemDetails.value)),  // copy the main itemDetails
    attachments: []
  };

  let queryParams = {
    fields: JSON.stringify(['vendor_name', 'mail_id', 'contact_number', 'gst_number', 'address']),
  }

  axiosInstance.get(apis.resource + doctypes.ezyVendors, { params: queryParams })
    .then(response => {
      console.log(response.data);
      vendorMasterList.value = response.data.map(vendor => ({
        vendor_name: vendor.vendor_name,
        gst_number: vendor.gst_number,
        phone_number: vendor.contact_number,
        mail_id: vendor.mail_id,
        address: vendor.address,
        selected: false
      }));


    })
    .catch(error => {
      console.error('Error fetching items:', error);
      toast.error('Failed to fetch items.');
    });

  editingVendorIndex.value = null;  // because it's a new vendor
  new bootstrap.Modal(document.getElementById('vendorModal')).show();
}

// const submitComparison = () => {
//   const vendor_details = vendorDetails.value.map(vendor => {
//     return {
//       vendor_name: vendor.vendor_name,
//       gst_number: vendor.gst_number,
//       phone_number: vendor.phone_number,
//       mail_id: vendor.mail_id,
//       rank: vendor.rank,
//       transportation_charges: vendor.transport,
//       delivery_time: vendor.deliveryTime,
//       paymentTerms: vendor.paymentTerms,
//       remark: vendor.remark,
//       total_value: vendor.total_value,
//       address: vendor.address,
//       pricing_details: JSON.stringify(vendor.ezy_item_details)
//     };
//   });

//   const ezy_item_details = vendorDetails.value[0].ezy_item_details.map(item => ({
//     item_name: item.item_name,
//     item_unit_of_measure: item.unit_of_measure,
//     item_quantity: item.quantity
//   }));

//   const finalPayload = {
//     vendor_details,
//     ezy_item_details
//   };

//   console.log(finalPayload);

//   axiosInstance.post(apis.resource + doctypes.ezyContracts, finalPayload)
//     .then(response => {
//       console.log('Comparison submitted successfully:', response.data);
//       toast.success('Comparison submitted successfully!');
//       request_raising_fn(response.data);
//     })
//     .catch(error => {
//       console.error('Error submitting comparison:', error);
//       toast.error('Failed to submit comparison.');
//     });
// };
const submitComparison = async () => {
  const vendor_details = vendorDetails.value.map(vendor => ({
    vendor_name: vendor.vendor_name,
    gst_number: vendor.gst_number,
    phone_number: vendor.phone_number,
    mail_id: vendor.mail_id,
    biddle_rank: vendor.rank,
    transportation_charges: vendor.transport,
    delivery_time: vendor.deliveryTime,
    payment_terms: vendor.paymentTerms,
    remark: vendor.remark,
    total_value: vendor.total_value,
    address: vendor.address,
    attachments: vendor.attachments,
    pricing_details: JSON.stringify(vendor.ezy_item_details)
  }));

  const ezy_item_details = vendorDetails.value[0].ezy_item_details.map(item => ({
    item_name: item.item_name,
    item_unit_of_measure: item.unit_of_measure,
    item_quantity: item.quantity
  }));

  // Your main document to save (e.g., Ezy Contract or any other DocType)
  const form = {
    doctype: "CTO", // Replace with your actual DocType name
    vendor_details,
    ezy_item_details
  };

  const formData = new FormData();
  formData.append("doc", JSON.stringify(form));
  formData.append("action", "Save");

  try {
    const response = await axiosInstance.post(apis.savedocs, formData);
    console.log("Comparison saved successfully:", response);
    toast.success("Comparison saved successfully!");
    request_raising_fn(response.docs[0]);
  } catch (error) {
    console.error("Error saving comparison:", error);
    toast.error("Failed to save comparison.");
  }
};

function request_raising_fn(item) {
  // saveloading.value = true;
  // console.log(filepaths.value, "---filepaths");
  // const filesArray = filepaths.value
  //   ? filepaths.value.split(",").map((filePath) => filePath.trim())
  //   : [];
  let data_obj = {
    module_name: "Ezy Forms",
    doctype_name: 'CTO',
    ids: [item.name],
    reason: "Request Raised",
    url_for_request_id: "",
    files: [],
    property: 'CRR',
    ip_address: '',
    employee_id: '11111',
    // be_half_of:item.requester_name,
    // request_for:item.request_for,
  };
  axiosInstance.post(apis.raising_request, data_obj).then((resp) => {
    if (resp?.message?.success === true) {


      toast.success("Request Raised", {
        autoClose: 1000,
        transition: "zoom",

      });
    }
  })
    .catch((error) => {
      console.error("Error raising request:", error);
      toast.error("Error raising request");
    })
  // .finally(() => {
  //   saveloading.value = false;
  // });
}
const hasSelectedVendor = computed(() =>
  vendorDetails.value.some(vendor => vendor.selected)
);
function updateTotalPrice(item) {
  const qty = parseFloat(item.quantity || 0);
  const price = parseFloat(item.unitPrice || 0);
  item.totalPrice = (qty * price).toFixed(2);
}

// const addItem = () => itemDetails.value.push({ item_name: 'New Item', unit_of_measure: 'Unit', quantity: 1, selected: false });



const editItem = index => {
  editingIndex.value = index;
};

const saveItem = () => {
  editingIndex.value = null;
};

const cancelEdit = () => {
  editingIndex.value = null;
};

const deleteItem = index => itemDetails.value.splice(index, 1);

const deleteSelectedItems = () => {
  itemDetails.value = itemDetails.value.filter(item => !item.selected);
};

const hasSelectedItems = computed(() =>
  itemDetails.value.some(item => item.selected)
);

const openItemModal = () => {
  itemDetails.value.push({
  item_name: "",
  unit_of_measure: "",
  quantity: 0,
  selected: false,
});


};
// availableItems.value.forEach(item => item.selected = false);
// const modal = new bootstrap.Modal(document.getElementById('itemModal'));
// modal.show(); 


const activeDropdown = ref(null);

const itemInputs = ref([]); // Ref for focusing inputs

// Sample dropdown list
const itemOptions = ref([]);

const filteredOptions = (query) => {
  if (!query) return itemOptions.value;
  return itemOptions.value.filter((opt) =>
    opt.toLowerCase().includes(query.toLowerCase())
  );
};
const selectItem = (value, index) => {
  itemDetails.value[index].item_name = value;

  // Find the full item object from availableItems
  const matchedItem = availableItems.value.find(item => item.item_name === value);

  if (matchedItem) {
    itemDetails.value[index].unit_of_measure = matchedItem.unit_of_measure;
  }

  activeDropdown.value = null;
};
watch(itemDetails, (newItems) => {
  newItems.forEach(item => {
    if (!item.item_name) {
      item.unit_of_measure = "";
    }
  });
}, { deep: true });
// const selectItem = (value, index) => {
//   itemDetails.value[index].item_name = value;
//   console.log(value);
//   activeDropdown.value = null;
// };

const closeDropdown = (index) => {
  // delay hiding to allow click event to fire
  setTimeout(() => {
    if (activeDropdown.value === index) {
      activeDropdown.value = null;
    }
  }, 200);
};

const openNewItemModal = () => {
  const modal = new bootstrap.Modal(document.getElementById("itemModal"));
  modal.show();
};
// Reset all selections
// fetchingItemsList()
// availableItems.value.forEach(item => item.selected = false);
// const modal = new bootstrap.Modal(document.getElementById('itemModal'));
// modal.show(); 


// const openItemModal = () => {
//   availableItems.value.forEach(item => item.selected = false);
// const modal = new bootstrap.Modal(document.getElementById('itemModal'));
// modal.show(); 
// };
// itemDetails.value.push({
//   item_name: "",
//   unit_of_measure: "",
//   quantity: 0,
//   selected: false,
// });
// editingIndex.value = itemDetails.value.length - 1;

// nextTick(() => {
//   const input = document.querySelector(`#item-name-${editingIndex.value}`);
//   if (input) input.focus();
// });
const deleteSelectedVendors = () => vendorDetails.value = vendorDetails.value.filter(vendor => !vendor.selected);

const filteredItems = computed(() => {
  return availableItems.value.filter(item =>
    item.item_name.toLowerCase().includes(searchItem.value.toLowerCase())
  );
});

const toggleSelectAll = (event) => {
  const isChecked = event.target.checked;
  filteredItems.value.forEach(item => item.selected = isChecked);
};
const toggleItemSelection = (item) => {
  item.selected = !item.selected;
};
const confirmItemSelection = () => {
  const newItems = availableItems.value
    .filter(item => item.selected)
    .map(item => ({
      item_name: item.item_name,
      unit_of_measure: item.unit_of_measure,
      quantity: 0, // default quantity
      selected: false
    }));

  // Avoid duplicates (based on name)
  newItems.forEach(newItem => {
    if (!itemDetails.value.some(existing => existing.item_name === newItem.item_name)) {
      itemDetails.value.push(newItem);
    }
  });

  bootstrap.Modal.getInstance(document.getElementById('itemModal')).hide();
};

// const saveItems = () => {
//   console.log('Saved Items:', JSON.stringify(itemDetails.value, null, 2));

// };


const handleClickOutside = (e) => {
  // If the click is not inside any td or input of editing row, exit edit mode
  if (!e.target.closest('.editable-row')) {
    editingIndex.value = null;
  }
};

onMounted(() => {
  fetchingItemsList()
  window.addEventListener('click', handleClickOutside);
  fetchingWork()

});

onBeforeUnmount(() => {
  window.removeEventListener('click', handleClickOutside);
});
const newItem = ref({
  name: '',
  unit: ''
})

const addNewItem = () => {
  if (!newItem.value.name || !newItem.value.unit) return;

  let newItemObj = {
    item_name: newItem.value.name,
    unit_of_measure: newItem.value.unit,
  };
  axiosInstance.post(apis.resource + doctypes.ezyItems, newItemObj)
    .then(response => {

      toast.success('New item added successfully!');
      console.log('New item added:', response.data);
      fetchingItemsList()
      // Optionally, you can refresh the items list or show a success message
    })
    .catch(error => {
      console.error('Error adding new item:', error);
    });


  // Clear input fields
  newItem.value.item_name = '';
  newItem.value.unit_of_measure = '';
};
const editingVendorIndex = ref(null);
const vendorForm = ref({
  vendor_name: '', gst_number: '', phone_number: '', mail_id: '',
  ezy_item_details: [
    { ...itemDetails }
  ],
  transport: 'Free delivery', deliveryTime: '', paymentTerms: '', rank: 'L1', remark: '', address: '', attachments: []
});

function openVendorModal(index) {
  const vendor = vendorDetails.value[index];

  vendorForm.value = {
    vendor_name: vendor.vendor_name,
    gst_number: vendor.gst_number,
    phone_number: vendor.phone_number,
    mail_id: vendor.mail_id,
    transport: vendor.transport || 'Free delivery',
    deliveryTime: vendor.deliveryTime || '',
    paymentTerms: vendor.paymentTerms || '',
    rank: vendor.rank || '',
    remark: vendor.remark || '',
    total_value: vendor.total_value,
    address: vendor.address || '',
    attachments: vendor.attachments || [], // Ensure attachments is always an array
    // Load the vendor's own items (if any), else empty array
    ezy_item_details: vendor.ezy_item_details ? JSON.parse(JSON.stringify(vendor.ezy_item_details)) : JSON.parse(JSON.stringify(itemDetails.value))
  };

  editingVendorIndex.value = index;
  new bootstrap.Modal(document.getElementById('vendorModal')).show();
}
watch(() => vendorForm.value.ezy_item_details, () => {
  calculateVendorTotal();
}, { deep: true });
watch(() => vendorForm.value.ezy_item_details, () => {
  calculateVendorTotal();

  if (editingVendorIndex.value !== null) {
    vendorDetails.value[editingVendorIndex.value].total_value = vendorForm.value.total_value;
  }
}, { deep: true });

function calculateVendorTotal() {
  const total = vendorForm.value.ezy_item_details.reduce((sum, item) => {
    return sum + parseFloat(item.totalPrice || 0);
  }, 0);
  vendorForm.value.total_value = total.toLocaleString('en-IN');
}
function handleFileUpload(event) {
  const files = event.target.files;
  if (files.length > 0) {
    Array.from(files).forEach((file) => {
      uploadFile(file).then((fileUrl) => {
        if (fileUrl) {
          if (!Array.isArray(vendorForm.value.attachments)) {
            vendorForm.value.attachments = [];
          }
          vendorForm.value.attachments.push(fileUrl);
        }
      });
    });
  }
}


const uploadFile = async (file) => {
  const formData = new FormData();
  formData.append("file", file, file.name);
  formData.append("is_private", "0");
  formData.append("folder", "Home");

  try {
    const res = await axiosInstance.post(apis.uploadfile, formData);
    if (res?.message?.file_url) {
      console.log(res.message.file_url, "File uploaded successfully");
      return res.message.file_url;
    } else {
      console.warn("No file_url found in response:", res);
      return null;
    }
  } catch (err) {
    console.error("Upload error:", err);
    return null;
  }
};

function saveVendorDetails() {
  calculateVendorTotal(); // Update vendorForm.value.total_value first

  const vendorData = {
    vendor_name: vendorForm.value.vendor_name,
    gst_number: vendorForm.value.gst_number,
    phone_number: vendorForm.value.phone_number,
    mail_id: vendorForm.value.mail_id,
    rank: vendorForm.value.rank,
    transport: vendorForm.value.transport,
    deliveryTime: vendorForm.value.deliveryTime,
    paymentTerms: vendorForm.value.paymentTerms,
    remark: vendorForm.value.remark,
    ezy_item_details: JSON.parse(JSON.stringify(vendorForm.value.ezy_item_details)),
    total_value: vendorForm.value.total_value,
    address: vendorForm.value.address,
    attachments: vendorForm.value.attachments  // Ensure attachments is always an array
  };

  if (editingVendorIndex.value !== null) {
    // Update the existing vendor at the correct index
    vendorDetails.value[editingVendorIndex.value] = {
      ...vendorDetails.value[editingVendorIndex.value],
      ...vendorData
    };
  } else {
    // New vendor
    vendorData.rank = vendorDetails.value.length + 1;
    vendorDetails.value.push(vendorData);
  }

  if (!vendorMasterList.value.some(vendor => vendor.vendor_name === vendorForm.value.vendor_name)) {

    let MasterVendor = {
      vendor_name: vendorForm.value.vendor_name,
      mail_id: vendorForm.value.mail_id,
      contact_number: vendorForm.value.phone_number,
      gst_number: vendorForm.value.gst_number,
      address: vendorForm.value.address,
    }
    console.log(MasterVendor, "api");
    axiosInstance.post(apis.resource + doctypes.ezyVendors, MasterVendor)
      .then(response => {
        console.log('Vendor saved successfully:', response.data);
        toast.success('Vendor details saved successfully!');
      })
      .catch(error => {
        console.error('Error saving vendor:', error);
        toast.error('Failed to save vendor details.');
      });
  }


  bootstrap.Modal.getInstance(document.getElementById('vendorModal')).hide();
  vendorSearch.value = ''; // Clear search input after saving
}


const editingItemIndex = ref(null);
const backupItem = ref({});


// Start editing a row
function editItemInModal(index) {
  editingItemIndex.value = index;
  // Backup the current data
  backupItem.value = { ...vendorForm.value.ezy_item_details[index] };
}

// Save the changes
function saveEditedItem() {
  // Recalculate vendor total
  calculateVendorTotal();
  editingItemIndex.value = null;
  backupItem.value = {};
}

// Cancel the editing and restore the backup
function cancelEditItem() {

  if (editingItemIndex.value !== null) {
    vendorForm.value.items[editingItemIndex.value] = { ...backupItem.value };
  }
  editingItemIndex.value = null;
  backupItem.value = {};
}

function addChildItem() {
  vendorForm.value.ezy_item_details.push({
    name: '',
    quantity: 1,
    unitPrice: '0.00',
    totalPrice: '0.00',
    selected: false,
  });
}

function deleteChildItem(index) {
  vendorForm.value.ezy_item_details.splice(index, 1);
}

function deleteSelectedChildItems() {
  vendorForm.value.ezy_item_details = vendorForm.value.ezy_item_details.filter(item => !item.selected);
}


function getVendorItemPrice(vendor, itemName) {
  const item = vendor.ezy_item_details?.find(i => i.name === itemName);
  return item ? item.unitPrice : '0.00';
}

function getVendorTotal(vendor) {
  const total = vendor.ezy_item_details?.reduce((sum, item) => sum + parseFloat(item.totalPrice || 0), 0);
  return total ? total.toLocaleString('en-IN') : '0.00';
}


function previewComparison() {
  console.log(`object`, vendorDetails.value);
  new bootstrap.Modal(document.getElementById('comparisonModal')).show();
}


const filterVendors = () => {
  const search = vendorForm.value.vendor_name.toLowerCase();

  if (search.length === 0) {
    filteredVendorOptions.value = [];

    // Reset all fields in vendorForm when vendor_name is cleared
    vendorForm.value = {
      vendor_name: '',
      gst_number: '',
      phone_number: '',
      mail_id: '',
      address: '',
      // If you have ezy_item_details or other fields, include them here too
      ezy_item_details: [],
      selected: false,
    };

    return;
  }

  filteredVendorOptions.value = vendorMasterList.value.filter(vendor =>
    vendor.vendor_name.toLowerCase().includes(search)
  );
};



const selectVendor = (vendor) => {
  vendorForm.value = {
    ...vendor,
    ezy_item_details: JSON.parse(JSON.stringify(vendorForm.value.ezy_item_details)),
    selected: false,
  }
  filteredVendorOptions.value = []

}



function fetchingItemsList() {
  let queryParams = {
    fields: JSON.stringify(['item_name', 'unit_of_measure']),
  }
  axiosInstance.get(apis.resource + doctypes.ezyItems, { params: queryParams })
    .then(response => {
      availableItems.value = response.data.map(item => ({
        item_name: item.item_name,
        unit_of_measure: item.unit_of_measure,
        selected: false
      }));
      itemOptions.value = availableItems.value.map(item => item.item_name);
    })
    .catch(error => {
      console.error('Error fetching items:', error);
    });
}

// // Approver data
// const workflowApprovalLevels = ref([
//   // { id: 1, designation: 'Manager',  },
//   // { id: 2, designation: 'Director',  },
// ]);

// // State management
// const workflowEditIndex = ref(null);
// const workflowInputRefs = ref([]);

// // Add a new row and start editing it
// const addWorkflowRow = () => {
//   const newRow = {
//     id: Date.now(),
//     designation: '',
//     onReject: '',
//   };
//   workflowApprovalLevels.value.push(newRow);
//   workflowEditIndex.value = workflowApprovalLevels.value.length - 1;

//   nextTick(() => {
//     if (workflowInputRefs.value[workflowEditIndex.value]) {
//       workflowInputRefs.value[workflowEditIndex.value].focus();
//     }
//   });
// };

// // Edit existing row
// const editWorkflowRow = (index) => {
//   workflowEditIndex.value = index;
//   nextTick(() => {
//     if (workflowInputRefs.value[index]) {
//       workflowInputRefs.value[index].focus();
//     }
//   });
// };

// // Stop editing
// const stopWorkflowEditing = () => {
//   workflowEditIndex.value = null;
// };

// // Remove a row
// const removeWorkflowRow = (index) => {
//   workflowApprovalLevels.value.splice(index, 1);
//   if (workflowEditIndex.value === index) {
//     workflowEditIndex.value = null;
//   }
// };
// const getPreviousWorkflowLevels = computed(() => {
//   return (levelIndex) => workflowApprovalLevels.value.slice(0, levelIndex);
// });
// Approver data
const designationOptions = ref([
  // { label: 'Manager', value: 'Manager' },
  // { label: 'Supervisor', value: 'Supervisor' },
  // { label: 'Admin', value: 'Admin' },
  // Add more as needed
]);
const workflowApprovalLevels = ref([]);

// State
const workflowEditIndex = ref(null);
// const workflowInputRefs = ref([]);

// // ✅ Dynamic ref setter (instead of array of template refs)
// const setWorkflowInputRef = (el, index) => {
//   if (el) {
//     workflowInputRefs.value[index] = el;
//   }
// };

// Add a new row
// const addWorkflowRow = () => {
//   const newRow = {
//     id: Date.now(),
//     designation: '',
//     onReject: '',
//   };
//   workflowApprovalLevels.value.push(newRow);
//   workflowEditIndex.value = workflowApprovalLevels.value.length - 1;

//   nextTick(() => {
//     const inputEl = workflowInputRefs.value[workflowEditIndex.value];
//     if (inputEl) inputEl.focus();
//   });
// };
// Edit row
// const editWorkflowRow = (index) => {
//   workflowEditIndex.value = index;
//   nextTick(() => {
//     const inputEl = workflowInputRefs.value[index];
//     if (inputEl) inputEl.focus();
//   });
// };

const addWorkflowRow = () => {
  const newRow = {
    id: Date.now(),
    designation: '',
    onReject: '',
  };
  workflowApprovalLevels.value.push(newRow);
  workflowEditIndex.value = workflowApprovalLevels.value.length - 1;
};

const editWorkflowRow = (index) => {
  workflowEditIndex.value = index;
};


// Stop editing
const stopWorkflowEditing = () => {
  workflowEditIndex.value = null;
};

// Remove row
const removeWorkflowRow = (index) => {
  workflowApprovalLevels.value.splice(index, 1);
  // workflowInputRefs.value.splice(index, 1);  // ✅ also clean up ref
  if (workflowEditIndex.value === index) {
    workflowEditIndex.value = null;
  } else if (workflowEditIndex.value > index) {
    workflowEditIndex.value -= 1;
  }
};

// Get previous levels for dropdown
const getPreviousWorkflowLevels = computed(() => {
  return (levelIndex) => workflowApprovalLevels.value.slice(0, levelIndex);
});
const getRejectLabel = (designation) => {
  if (!designation) return 'Level 0';
  const levelIndex = workflowApprovalLevels.value.findIndex(item => item.designation === designation);
  return levelIndex !== -1 ? `Level ${levelIndex + 1}` : designation;
};

function fetchingWork() {
  axiosInstance
    .get(apis.resource + doctypes.wfRoadmap + '/CRR_CTO')
    .then((response) => {
      WfroleMatrix()
      const wfData = response.data;

      if (!wfData || !Array.isArray(wfData.wf_level_setup)) return;

      // Step 1: First pass - create a temporary list with basic info
      const tempLevels = wfData.wf_level_setup.map((level, index) => ({
        id: level.name,
        designation: level.role || '',
        originalIndex: index,
        on_rejection: level.on_rejection || 0,
        onReject: '', // we'll fill this next
      }));

      // Step 2: Resolve onReject using index-based matching
      tempLevels.forEach((level) => {
        const rejectIdx = level.on_rejection - 1;
        level.onReject =
          rejectIdx >= 0 && tempLevels[rejectIdx]
            ? tempLevels[rejectIdx].designation
            : '';
      });

      // Step 3: Final shape expected by your v-model (cleaned structure)
      workflowApprovalLevels.value = tempLevels.map(({ id, designation, onReject }) => ({
        id,
        designation,
        onReject,
      }));
    })
    .catch((error) => {
      console.error('Error fetching workflow:', error);
      toast.error('Failed to fetch workflow.');
    });
}
function WfroleMatrix() {

  axiosInstance
    .get(apis.resource + doctypes.WFRoleMatrix + `/CRR`)
    .then((res) => {
      if (res.data) {
        designationOptions.value = [
          ...new Set(res.data.users.map((user) => user.role_name)),
        ];
      }
    })
    .catch((error) => {
      console.error("Error fetching designations data:", error);
    });
}





</script>

<style lang="scss" scoped>
// .table {
  // border-collapse: separate;
  // border-spacing: 0;
  // border-radius: 2px;
  // overflow: hidden; 
// }


// .table thead tr:first-child th:first-child {
//   border-top-left-radius: 2px;
// }

// .table thead tr:first-child th:last-child {
//   border-top-right-radius: 2px;
// }


// .table tbody tr:last-child td:first-child {
//   border-bottom-left-radius: 2px;
// }

// .table tbody tr:last-child td:last-child {
//   border-bottom-right-radius: 2px;
// }

/* Optional: Add a subtle box shadow */
// .table {
//   box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
//   font-size: 13px;
// }
// .rounded-table {
//   border-collapse: separate;
//   border-spacing: 0;
//   border-radius: 8px;
//   overflow: hidden;
// }

.main-div{
  height: 80vh;

}
.table th {
  color: #666666;
  font-weight: 500;
  font-size: 13px;
}

.table td {
  color: #000000;
  font-weight: 500;
  font-size: 13px;
}

.btn-danger {
  border-radius: 6px;
  font-size: 11px;
}

.accordion {

  box-shadow: 2px 3px 4px 0px #0000000D;

  box-shadow: -2px -3px 14px 0px #0000000D;

}


.accordion-button.collapsed {
  background-color: #fff;
  box-shadow: none;
  font-size: 14px;
  color: #000;
}

.accordion-button {
  background-color: #fff;
  /* light background when expanded, adjust as needed */
  // height: 50px; 
  padding: 30px 20px;
}

.accordion-button:focus {
  box-shadow: none;

}

.accordion-button:not(.collapsed) {
  background-color: #fff;
  /* or any color you prefer */
  color: #333333;
  /* optional: adjust text color */
}

/* Collapsed state */
.accordion-button.collapsed {
  background-color: #fff !important;
  color: #666666;
  /* optional: adjust text color when collapsed */
  box-shadow: none;
  /* optional: remove the Bootstrap box-shadow */
}

/* Adjust spacing, if required */
.bi-pencil-square {
  font-size: 12px;
  cursor: pointer;
}

.add_item_btn {
  background-color: #F6F6F6;
  border: 1px solid #EEEEEE;
  color: #000000;
  font-size: 12px;
}

.add_vendor_btn {
  background-color: #F6F6F6;
  border: 1px solid #EEEEEE;
  color: #000000;
  font-size: 12px;
}

.form-control {
  border-radius: 10px;
  font-size: 12px;
}

.form-label {
  font-size: 12px;
}



.form-select {
  border-radius: 10px;
  font-size: 12px;
}

.btn-outline-secondary {
  font-size: 12px !important;
}

.accordion {
  box-shadow: 2px 3px 4px 0px #0000000D;
  box-shadow: -2px -3px 14px 0px #0000000D;

}

.back_div {
  background-color: #FAFAFA;
  padding: 5px;
  border-radius: 6px;
}

.selected-file {
  background-color: #e6f2ff;
  font-weight: bold;
}

.step-item {
  font-weight: 500;
  color: #6c757d;
  font-size: 14px;
  border-bottom: 2px solid transparent;
}

.step-item i {
  font-size: 16px;
  margin-right: 5px;
}

.step-item.active {
  border-bottom: 4px solid #1B14DF;
  color: #1B14DF;
  font-weight: 500;
}

.step-item.completed {
  color: #14DF22;
}

.check-icon {
  color: #14DF22;
  font-size: 16px;
}

.add-approver-row {
  background-color: #F5F6FF;

}

.add-approver-row button {
  font-size: 12px;
  padding: 5px 10px;
  color: #1B14DF;
}

// body {
//   min-height: 100vh;
// }

.table td,
.table th {
  vertical-align: middle;
  border-color: #dee2e6;
}

.stepper-bottom {
  background-color: #FAFAFA;
  border-radius: 10px;
}

.drag-handle {
  cursor: grab;
}

.export_btn {
  color: #1B14DF;
  font-weight: 600;
  font-size: 14px;
  padding: 8px 16px;
  border-radius: 10px;
  background-color: #F5F6FF;
  border: None;
}

.workflow-container {
  display: flex;
  flex-direction: column;
}

.workflow-row {
  display: grid;
  grid-template-columns: 1fr 2fr 2fr 1fr;
  align-items: center;
  gap: 8px;
  padding: 4px 8px;
  border: 1px solid #dee2e6;
  background-color: white;
  font-size: 13px;
}

.workflow-header {
  font-weight: 500;
  font-weight: 13px;
  background-color: #FAFAFA;
  border-bottom: 2px solid #ccc;
  color: #000000;
  display: grid;
  grid-template-columns: 1fr 2fr 2fr 1fr;
  border: 1px solid #dee2e6;
  border-bottom: none;
  align-items: center;
  gap: 8px;
  padding: 8px;
  font-size: 13px;
}

.workflow-header div {
  font-weight: 500;
  color: #000000;
  font-size: 13px;
  padding: 4px;
}

.workflow-row div {
  color: #444444;
}

.workflow-footer {
  padding: 5px;
  background-color: #F5F6FF;
}

.workflow-footer button {
  font-size: 13px;
  padding: 5px 10px;
  color: #1B14DF;
  font-weight: 600;
}

.next-Submit {
  background-color: #1B14DF;
  color: #fff;
  font-weight: 600;
  font-size: 14px;
  padding: 8px 16px;
  border-radius: 10px;
}

.next-Submit:hover {
  background-color: #1B14DF;
  color: #fff;
  font-weight: 600;
  font-size: 14px;
  padding: 8px 16px;
  border-radius: 10px;
}

.stepper-back {
  background-color: #F5F6FF;
  color: #222222;
  font-weight: 600;
  font-size: 14px;
  padding: 8px 16px;
  border-radius: 10px;
}
</style>
