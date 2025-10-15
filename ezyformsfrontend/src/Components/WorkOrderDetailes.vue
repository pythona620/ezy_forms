<template>
  <div class="container-fluid">

    <div class="main-div position-relative">


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
              <div v-if="previewUrl" style="flex-grow: 1;">
                <iframe v-if="previewUrl" :src="previewUrl" style="width: 100%; height: 600px;"
                  frameborder="0"></iframe>
                <p v-else>No preview available.</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class=" main_back d-flex justify-content-between align-items-center back_di mb-2">
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
      <div class="container-fluid ">
        <div class="row">
          <div class="col-2 ps-1 vendor_sidebar">
            <ul class="nav flex-column" id="myTab" role="tablist">
              <li class="nav-item" role="presentation">
                <button class="nav-link active" id="tab1-tab" data-bs-toggle="tab" data-bs-target="#tab1" type="button"
                  role="tab" aria-controls="tab1" aria-selected="true">
                  Vendor Comparison
                </button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="tab2-tab" data-bs-toggle="tab" data-bs-target="#tab2" type="button"
                  role="tab" aria-controls="tab2" aria-selected="false">
                  Items Master
                </button>
              </li>
              <li class="nav-item" role="presentation">
                <button class="nav-link" id="tab3-tab" data-bs-toggle="tab" data-bs-target="#tab3" type="button"
                  role="tab" aria-controls="tab3" aria-selected="false">
                  Vendor Master
                </button>
              </li>
            </ul>
          </div>

          <div class="col-10">
            <div class="tab-content" id="myTabContent">
              <div class="tab-pane fade show active  " id="tab1" role="tabpanel" aria-labelledby="tab1-tab">
                <div>




                  <div
                    class="font-12 start-0 end-0 d-flex stepper-bottom p-2 mb-2 justify-content-between align-items-center">
                    <!-- Stepper Navigation -->
                    <div class="d-flex">
                      <div v-for="(step, index) in steps" :key="index" class="px-3 py-2" :class="[
                        'step-item',
                        { active: currentStep === index, completed: index < currentStep }
                      ]" style="cursor: pointer;" @click="goToStep(index)">
                        <span class="font-12">
                          <!-- Icon fade transition -->
                          <transition name="icon-fade" mode="out-in">
                            <i v-if="index < currentStep" key="done"
                              class="me-1 check-icon bi bi-check-circle-fill"></i>
                            <i v-else :class="['me-1', step.icon]" key="todo"></i>
                          </transition>
                          {{ step.label }}
                        </span>
                      </div>
                    </div>

                    <!-- Back / Next Buttons -->
                    <div>
                      <button class="btn btn-light stepper-back border-1 btn-sm me-2" @click="prevStep"
                        :disabled="currentStep === 0">
                        Back
                      </button>
                      <button class="btn btn-light next-Submit" @click="nextStep">
                        {{ currentStep === steps.length - 1 ? "Submit form" : "Next" }}
                      </button>
                    </div>
                  </div>


                  <div class="d-flex flex-column justify-content-between" style="min-height: 300px">
                    <!-- Main Content Area Based on Step -->
                    <div class="flex-grow-1 ">
                      <div class="card mb-3 work_order_card">
                        <div class="py-2 px-3">
                          <div class="form-check form-check-inline">
                            <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio1"
                              :value="1" v-model="comparisonType" />
                            <label class="form-check-label font-13" for="inlineRadio1">
                              Work Order
                            </label>
                          </div>

                          <div class="form-check form-check-inline">
                            <input class="form-check-input" type="radio" name="inlineRadioOptions" id="inlineRadio2"
                              :value="0" v-model="comparisonType" />
                            <label class="form-check-label font-13" for="inlineRadio2">
                              Purchase Order
                            </label>
                          </div>
                        </div>
                      </div>

                      <transition name="fade-slide" mode="out-in">

                        <div v-if="currentStep === 0">

                          <!-- Step 1: Vendor & Item Details -->
                          <!-- <h5>Step 1: Vendor & Item Details</h5> -->
                          <!-- Put Item & Vendor Accordions Here -->
                          <!-- <div class="d-flex justify-content-between align-items-center back_di mb-2">
              <div><button class="font-12 m-0 btn" @click="router.back()"> <i class="bi bi-chevron-left"></i>
                  Back</button>
              </div>
              <div>
              </div>
            </div> -->
                          <!-- <button class="btn btn-outline-secondary btn-sm me-2" @click="previewComparison">Preview
            comparison</button>
            <button class="btn btn-dark btn-sm" :class="{ 'bg-dark': itemDetails.length && vendorMasterList.length }"
            @click="submitComparison">Submit comparison</button> -->
                          <div class="">
                            <div style="border:1px solid #ccc;background-color: #f5f5f5;"
                              class="main-accordion   border-1 rounded-1">



                              <div class="">
                                <div class="accordion  " id="accordionExample">
                                  <!-- Item Details Accordion -->
                                  <div class="accordion-item">
                                    <h2 class="accordion-header">
                                      <button class="accordion-button " type="button" data-bs-toggle="collapse"
                                        data-bs-target="#collapseItems" aria-expanded="true">
                                        Items
                                      </button>
                                    </h2>
                                    <div id="collapseItems" class="accordion-collapse collapse show">
                                      <div class="accordion-body">

                                        <table class="table shadow-sm item-table  rounded-table">
                                          <thead class="table-light  ">
                                            <tr>
                                              <th class="fw-bold" scope="col"><input type="checkbox"></th>
                                              <th class="fw-bold">Item name</th>
                                              <th class="fw-bold">Unit of measure</th>
                                              <th class="fw-bold">Item Quantity</th>
                                              <th class="fw-bold">Action</th>
                                            </tr>
                                          </thead>
                                          <tbody>
                                            <tr v-for="(item, index) in itemDetails" :key="index">
                                              <td width="3%"><input type="checkbox" v-model="item.selected"></td>
                                              <td class="editable-row  position-relative " @click="editItem(index)">
                                                <template v-if="editingIndex === index">

                                                  <input :id="`item-name-${index}`" class="form-control form-control-sm"
                                                    v-model="item.item_name" @focus="activeDropdown = index"
                                                    @input="activeDropdown = index" @blur="closeDropdown(index)"
                                                    placeholder="Search item" :ref="el => setItemInputRef(el, index)" />

                                                  <ul v-if="activeDropdown === index" class="dropdown-menu show w-100"
                                                    style="position: absolute; top: 100%; left: 0; max-height: 200px; overflow-y: auto; z-index: 1055;">
                                                    <li v-for="option in filteredOptions(item.item_name)" :key="option"
                                                      class="dropdown-item font-12"
                                                      @mousedown.prevent="selectItem(option, index)">
                                                      {{ option }}
                                                    </li>
                                                    <!-- <li class="dropdown-item text-primary font-12"
                                                      @mousedown.prevent="openNewItemModal">
                                                      + Add new item
                                                    </li> -->
                                                  </ul>

                                                </template>
                                                <!-- <template v-if="editingIndex === index">
                              <input v-model="item.item_name" class="form-control form-control-sm">

                            </template>  -->
                                                <template v-else>{{ item.item_name }}</template>
                                              </td>
                                              <td class="editable-row" @click="editItem(index)">
                                                <template v-if="editingIndex === index">
                                                  <input v-model="item.item_unit_of_measure"
                                                    class="form-control form-control-sm">
                                                </template>
                                                <template v-else>
                                                  {{ item.item_unit_of_measure }}
                                                </template>
                                              </td>
                                              <td class="editable-row" @click="editItem(index)">
                                                <template v-if="editingIndex === index">
                                                  <input v-model="item.item_quantity" type="number"
                                                    class="form-control form-control-sm">
                                                </template>
                                                <template v-else>
                                                  {{ item.item_quantity }}
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
                                          <button v-if="hasSelectedItems" class="btn btn-danger btn-sm"
                                            @click="deleteSelectedItems"><i class="bi bi-trash"></i>
                                            Delete Item</button>
                                          <button class="btn  add_item_btn  ms-2" @click="openItemModal"><i
                                              class="bi bi-plus "></i>
                                            Add
                                            Item</button>
                                        </div>
                                        <!-- <button v-if="itemDetails.length" class="btn btn-success btn-sm ms-2" @click="saveItems">Save
                  Items</button> -->

                                      </div>
                                    </div>
                                  </div>
                                  <!-- Add Item Modal -->
                                  <div class="modal fade" id="itemModal" tabindex="-1" aria-labelledby="itemModalLabel"
                                    aria-hidden="true">
                                    <div class="modal-dialog modal-lg modal-dialog-scrollable">
                                      <div class="modal-content">
                                        <div class="modal-header">
                                          <h5 class="modal-title">Select Items</h5>
                                          <button type="button" class="btn-close" data-bs-dismiss="modal"
                                            aria-label="Close"></button>
                                        </div>
                                        <div class="modal-body">
                                          <!-- Search Input -->
                                          <!-- <input type="text" class="form-control mb-3" placeholder="Search items..." v-model="searchItem" /> -->

                                          <!-- Add New Item -->
                                          <div class="d-flex gap-2 mb-3">
                                            <input type="text" class="form-control" placeholder="Item name"
                                              v-model="newItem.name" />
                                            <input type="text" class="form-control" placeholder="Unit"
                                              v-model="newItem.unit" />
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
                                                  <td @click="toggleItemSelection(item)">{{ item.item_unit_of_measure }}
                                                  </td>
                                                </tr>
                                              </tbody>
                                            </table>
                                          </div>
                                        </div>

                                        <div class="modal-footer">
                                          <button class="btn btn-outline-secondary"
                                            data-bs-dismiss="modal">Cancel</button>
                                          <button class="btn btn-dark" @click="confirmItemSelection">Add Selected
                                            Items</button>
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


                                        <table class="table vendor-table shadow-sm rounded-table">
                                          <thead class="table-light">
                                            <tr>
                                              <th scope="col"><input type="checkbox"></th>
                                              <th>Bidder Rank</th>
                                              <th>Vendor name</th>
                                              <th>GST number</th>
                                              <th>Contact</th>
                                              <th>Email</th>
                                              <th>Total value in <i class="bi bi-currency-rupee fw-bold"></i></th>
                                              <th>Action</th>
                                            </tr>
                                          </thead>
                                          <tbody>
                                            <tr v-for="(vendor, index) in vendorDetails" :key="index">
                                              <td width="3%"><input type="checkbox" v-model="vendor.selected"></td>
                                              <td>
                                                <div class="d-flex justify-content-between">
                                                  <span>

                                                    {{ vendor.rank }}
                                                  </span>

                                                  <span v-if="vendor.rank === 'L1'" class="badge font-12 "> <i
                                                      class=" text-success bi bi-check-circle-fill"></i></span>
                                                </div>
                                              </td>
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
                                          <button v-if="hasSelectedVendor" class="btn btn-danger btn-sm"
                                            @click="deleteSelectedVendors"><i class="bi bi-trash"></i> Delete
                                            Vendor</button>
                                          <!-- :disabled="!itemDetails.length" -->
                                          <button :disabled="!itemDetails.length" class="btn  add_vendor_btn btn-sm ms-2" @click="addVendorModal"><i
                                              class="bi bi-plus"></i>
                                            Add
                                            Vendor</button>
                                        </div>
                                      </div>
                                    </div>
                                  </div>
                                </div>
                              </div>
                            </div>
                            <!-- Vendor Edit Modal -->
                            <div class="modal fade" id="vendorModal" data-bs-backdrop="static" data-bs-keyboard="false"
                              tabindex="-1">
                              <div class="modal-dialog modal-xl">
                                <div class="modal-content p-4 position-relative">
                                  <div class="vendor-details pt-0 ">

                                    <div class="d-flex justify-content-between mb-3"
                                      style="position: sticky; top: 0; background: white;">
                                      <h6 class="fw-bold">#{{ vendorDetails.length + 1 }} Vendor </h6>
                                      <div>
                                        <button class="btn btn-outline-danger btn-sm me-2" @click="clearVendorForm"
                                          data-bs-dismiss="modal">Close</button>
                                        <button class="btn btn-dark  btn-sm" @click="saveVendorDetails">Save Vendor
                                          details</button>
                                      </div>
                                    </div>



                                    <div class="row g-2 mb-2">
                                      <div class="col-md-3">

                                        <label class="form-label">GST Number</label>
                                        <input type="text" class="form-control form-control-sm"
                                          placeholder="Type GST no..." v-model="vendorForm.gst_number"
                                          @input="filterVendors" />
                                        <div v-if="filteredVendorOptions.length" class="border rounded mt-1 bg-light"
                                          style="max-height: 150px; overflow-y: auto;z-index: 1000;">
                                          <div v-for="vendor in filteredVendorOptions" :key="vendor.gst_number"
                                            class="py-2 px-2  border-1   font-12"
                                            style="cursor: pointer; border-bottom: 1px solid #ccc;"
                                            @click="selectVendor(vendor)">
                                            {{ vendor.gst_number }}
                                          </div>
                                        </div>

                                        <!-- <label class="form-label">Vendor name</label>
                        <input v-model="vendorForm.vendor_name" class="form-control form-control-sm"> -->
                                      </div>
                                      <div class="col-md-3">
                                        <label class="form-label">Vendor Name</label>
                                        <input v-model="vendorForm.vendor_name" class="form-control form-control-sm">
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
                                        <textarea v-model="vendorForm.address"
                                          class="form-control form-control-sm"></textarea>
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
                                            <th>Gst%</th>
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
                                            <td style="min-width: 100px;" @click="editItemInModal(index)">
                                              <!-- <template v-if="editingItemIndex === index">
                                      <input type="number" v-model="item.item_quantity"
                                        class="form-control form-control-sm">
                                    </template>
                                    <template v-else> -->


                                              {{ item.item_quantity }}
                                              <!-- </template> -->

                                            </td>
                                            <td style="min-width: 100px;" @click="editItemInModal(index)">
                                              <template v-if="editingItemIndex === index">
                                                <input style="min-width: 100px;" @blur="saveEditedItem"
                                                  @focus="editItemInModal(index)" v-model.number="item.unitPrice"
                                                  @change="updateTotalPrice(item)" type="number"
                                                  class="form-control form-control-sm">
                                              </template>
                                              <template v-else>
                                                <i class="bi bi-currency-rupee"></i> {{ item.unitPrice }}
                                              </template>
                                            </td>

                                            <td style="min-width: 100px;" @click="editItemInModal(index)"
                                              class=" text-center">
                                              <template v-if="editingItemIndex === index">
                                                <input style="min-width: 100px;" @blur="saveEditedItem"
                                                  @focus="editItemInModal(index)" v-model.number="item.item_gst"
                                                  @change="updateTotalPrice(item)" type="number" class="form-control ">
                                              </template>
                                              <template v-else>
                                                {{ item.item_gst }} %
                                              </template>
                                            </td>
                                            <td>
                                              <i class="bi bi-currency-rupee"></i>{{ item.totalPrice }}
                                            </td>

                                            <td>
                                              <template v-if="editingItemIndex === index">
                                                <i class="bi bi-check-lg text-success me-2" @click="saveEditedItem"></i>
                                                <i class="bi bi-x-lg text-danger" @click="cancelEditItem"></i>
                                              </template>
                                              <template v-else>
                                                <i class="bi bi-pencil-square" @click="editItemInModal(index)"></i>
                                                <i class="bi bi-trash text-danger ms-2"
                                                  @click="deleteChildItem(index)"></i>
                                              </template>
                                            </td>
                                          </tr>
                                        </tbody>
                                      </table>

                                      <!-- <button class="btn btn-danger btn-sm" @click="deleteSelectedChildItems">Delete Item</button>
              <button class="btn btn-outline-secondary btn-sm ms-2" @click="addChildItem">+ Add Item</button> -->
                                    </div>
                                    <div class="row">
                                      <div class="col">
                                        <div class="">
                                          <label class="form-label">Selected Vendor</label>
                                          <select v-model="vendorForm.rank" class="form-select form-select-sm">
                                            <option value="">Select Vendor</option>
                                            <option>L1</option>
                                            <option>L2</option>
                                            <option>L3</option>
                                            <option>L4</option>
                                          </select>
                                        </div>

                                        <div class="">
                                          <label class="form-label">Delivery time (in days)</label>
                                          <input v-model="vendorForm.delivery_time"
                                            class="form-control form-control-sm">
                                        </div>
                                        <div class="">
                                          <label class="form-label">Payment terms</label>
                                          <input v-model="vendorForm.payment_terms"
                                            class="form-control form-control-sm">
                                        </div>
                                        <div class="mt-3">
                                          <label class="form-label">Remark</label>
                                          <textarea v-model="vendorForm.remark" name="remarks" class=" form-control"
                                            id=""></textarea>

                                        </div>



                                      </div>
                                      <div class="col">


                                        <div class="">
                                          <label class="form-label">Total price</label>
                                          <input 
  :value="(vendorForm.total_value || 0).toLocaleString('en-IN', { minimumFractionDigits: 2 })" 
  readonly 
  class="form-control form-control-sm"
/>


                                        </div>
                                       
                                        <div class="row">
                                          <div class="col">
                                            <label class="form-label">Transportation/freight</label>
                                            <input type="number" v-model.number="vendorForm.transportation_charges"
                                              class="form-control form-control-sm" @input="calculateTaxes" />
                                          </div>
                                        </div>


                                        <div class="row">


                                          <div class="col">
                                            <label class="form-label"> CGST %</label>
                                            <input type="number" v-model.number="vendorForm.transportation_cgst_percent" :disabled="disableCGST_UTGST" 
                                              class="form-control form-control-sm" @input="calculateTaxes" />
                                            <small class="font-13">Amt: <i class="bi bi-currency-rupee"></i> {{
                                              vendorForm.transportation_cgst_amount }}</small>
                                          </div>

                                          <div class="col">
                                            <label class="form-label"> UTGST %</label>
                                            <input type="number"
                                              v-model.number="vendorForm.transportation_utgst_percent" :disabled="disableCGST_UTGST" 
                                              class="form-control form-control-sm" @input="calculateTaxes" />
                                            <small class="font-13">Amt:<i class="bi bi-currency-rupee"></i>{{
                                              vendorForm.transportation_utgst_amount
                                              }}</small>
                                          </div>

                                          <div class="col">
                                            <label class="form-label"> IGST %</label>
                                            <select :disabled="disableIGST"  v-model.number="vendorForm.transportation_igst_percent"
                                              class="form-select form-select-sm" @change="calculateTaxes">
                                              <option :value="0">0%</option>
                                              <option :value="5">5%</option>
                                              <option :value="12">12%</option>
                                              <option :value="18">18%</option>
                                              <option :value="28">28%</option>
                                            </select>
                                            <small class="font-13">Amt: <i class="bi bi-currency-rupee"></i> {{
                                              vendorForm.transportation_igst_amount }}</small>
                                          </div>
                                        </div>
                                        <div class="row">

                                          <div class="col">
                                            <label class="form-label">Transport Total</label>
                                            <input class="form-control form-control-sm" type="text"
                                              v-model="vendorForm.transportation_total_amount" readonly />

                                          </div>
                                        </div>
                                        <div class="mt-2">
                                          <label class="form-label">Additional Charges</label>
                                          <input type="number" v-model.number="vendorForm.additional_charges"
                                            class="form-control form-control-sm" @input="calculateTaxes" />
                                        </div>


                                        <div class="mt-2">
                                          <label class="form-label fw-bold">Grand Total</label>
                                          <input v-model="vendorForm.grand_total"
                                            class="form-control form-control-sm fw-bold" readonly />
                                        </div>

                                      </div>
                                    </div>
                                  </div>

                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div v-else-if="currentStep === 1">
                          <!-- <div class="d-flex justify-content-between align-items-center back_div mb-2">
              <div><button class="font-12 m-0 btn" @click="prevStep" :disabled="currentStep === 0"> <i
                    class="bi bi-chevron-left"></i>
                  Back</button>
              </div>
              <div>

              </div>
            </div> -->
                          <!-- <button @click="exportfile" class="btn export_btn btn-sm me-2"><i class="bi bi-download me-2"></i> Export
                </button> -->
                          <!-- Step 2: Preview Comparison -->
                          <!-- <h5>Step 2: Preview Comparison</h5> -->
                          <div class="">
                            <!-- v-if="vendorDetails.length" -->
                            <table
                              style="width: 100%;   margin-top: 5px; font-size: 12px; background-color: white;font-family: Poppins, sans-serif;"
                              class="preview_table">
                              <thead>
                                <!-- Row 1: Item name + vendor names -->
                                <tr style="background-color: #fff7d6;">
                                  <th style="padding: 10px;">Item Name</th>
                                  <th style="padding: 10px;">UOM</th>
                                  <th style="padding: 10px;">Qty</th>
                                  <th v-for="vendor in sortedVendors" :key="vendor.vendor_name" colspan="2"
                                    style=" padding: 10px; text-align: center;">
                                    {{ vendor.vendor_name }}
                                  </th>
                                </tr>

                                <!-- Row 2: Rate + Total labels -->
                                <tr style="background-color: #fff7d6;">
                                  <th colspan="3" style=" padding: 10px;"></th>
                                  <template v-for="vendor in sortedVendors"
                                    :key="'vendor-labels-' + vendor.vendor_name">
                                    <th style=" padding: 10px; text-align: center;">Rate</th>
                                    <th style=" padding: 10px; text-align: center;">Total</th>
                                  </template>
                                </tr>
                              </thead>

                              <tbody>
                                <!-- Item rows -->
                                <tr v-for="item in itemDetails" :key="item.name">
                                  <td style=" padding: 10px;">{{ item.item_name }}</td>
                                  <td style=" padding: 10px; text-align: center;">{{ item.item_unit_of_measure }}</td>
                                  <td style=" padding: 10px; text-align: center;">{{ item.item_quantity }}</td>

                                  <template v-for="vendor in sortedVendors"
                                    :key="vendor.vendor_name + '-' + item.item_name">
                                    <td style=" padding: 10px; text-align: right;">
                                      <i class="bi bi-currency-rupee"></i> {{ getVendorItemPrice(vendor, item.item_name)
                                      }}
                                    </td>
                                    <td style=" padding: 10px; text-align: right;">
                                      <i class="bi bi-currency-rupee"></i> {{ getVendorItemTotal(vendor, item.item_name)
                                      }}
                                    </td>
                                  </template>
                                </tr>

                                <!-- Total row -->
                                <tr>
                                  <td colspan="3" style=" padding: 10px;"><b>Total</b></td>
                                  <td v-for="vendor in sortedVendors" :key="'total-' + vendor.vendor_name" colspan="2"
                                    style=" padding: 10px; text-align: right;font-weight:bold;">
                                    <i class="bi bi-currency-rupee"></i> {{ vendor.total_value }}/-
                                  </td>
                                </tr>

                                <!-- Additional Info Heading -->
                                <tr>
                                  <td colspan="100%"
                                    style=" padding: 10px; background-color: #f0f0f0; text-align: center;">
                                    Additional Information
                                  </td>
                                </tr>

                                <!-- Info rows -->
                                <tr>
                                  <td colspan="3" style=" font-weight:bold; padding: 10px;">Payment Terms</td>
                                  <td v-for="vendor in sortedVendors" :key="'pay-' + vendor.vendor_name" colspan="2"
                                    style=" padding: 10px;">
                                    {{ vendor.payment_terms || '-' }}
                                  </td>
                                </tr>
                                <tr>
                                  <td colspan="3" style=" font-weight:bold; padding: 10px;">GST %
                                    <div>
                                      <span class=" font-11">(CGST/UTGST/IGST)</span>
                                    </div>
                                  </td>
                                  <td v-for="vendor in sortedVendors" :key="'gst-' + vendor.vendor_name" colspan="2"
                                    style=" padding: 10px;">
                                    <div>

                                      <span class="font-11">
                                        {{
                                          (Number(vendor.transportation_cgst_percent) || 0) +
                                          (Number(vendor.transportation_utgst_percent) || 0) +
                                          (Number(vendor.transportation_igst_percent) || 0)
                                        }}%
                                      </span>
                                    </div>

                                  </td>
                                </tr>
                                <tr>
                                  <td colspan="3" style=" font-weight:bold; padding: 10px;">Delivery(in days)</td>
                                  <td v-for="vendor in sortedVendors" :key="'delivery-' + vendor.vendor_name"
                                    colspan="2" style=" padding: 10px;">
                                    {{ vendor.delivery_time || '-' }}
                                  </td>
                                </tr>
                                <tr>
                                  <td colspan="3" style=" font-weight:bold; padding: 10px;">Bid Rank</td>
                                  <td v-for="vendor in sortedVendors" :key="'rank-' + vendor.vendor_name" colspan="2"
                                    style=" padding: 10px;">
                                    {{ vendor.rank }}
                                    <span v-if="vendor.rank === 'L1'"
                                      style="color: green; font-weight: bold; margin-left: 4px;">
                                      <i class="bi bi-check-circle-fill"></i>
                                    </span>
                                  </td>
                                </tr>
                                <tr>
                                  <td colspan="3" style=" font-weight:bold; padding: 10px;">Transport Charges</td>
                                  <td v-for="vendor in sortedVendors" :key="'transport-' + vendor.vendor_name"
                                    colspan="2" style=" padding: 10px;">
                                    {{ vendor.transportation_total_amount || '-' }}
                                  </td>
                                </tr>
                                <tr>
                                  <td colspan="3" style=" font-weight:bold; padding: 10px;">Attachments</td>
                                  <td v-for="vendor in sortedVendors" :key="'att-' + vendor.vendor_name" colspan="2"
                                    style=" padding: 10px;">
                                    <span v-if="vendor.attachments" class="text-primary text-decoration-underline"
                                      style="cursor: pointer" @click="openPreview(vendor.attachments)">Preview
                                      attachment</span>
                                    <span v-else>-</span>
                                  </td>
                                </tr>
                                <tr>
                                  <td colspan="3" style=" font-weight:bold; padding: 10px;">Comments</td>
                                  <td v-for="vendor in sortedVendors" :key="'remark-' + vendor.vendor_name" colspan="2"
                                    style=" padding: 10px;">
                                    {{ vendor.remark || '-' }}
                                  </td>
                                </tr>
                              </tbody>
                            </table>


                          </div>
                        </div>
                        <div v-else-if="currentStep === 2">
                          <div class="">
                            <!-- Workflow Table -->
                            <div class="">
                              <div class="workflow-container">
                                <!-- Header -->
                                <div class="workflow-header">
                                  <div>Approval Level</div>
                                  <div>Approver Designation</div>
                                  <div>On Reject</div>
                                  <div>Actions</div>
                                </div>

                                <!-- Draggable List -->

                                <draggable :disabled="true" v-model="workflowApprovalLevels" item-key="id" handle=".drag-handle"
                                  :animation="150">
                                  <template #item="{ element, index }">
                                    <div class="workflow-row ">
                                      <div>
                                        <i class="bi bi-grip-vertical drag-handle fs-6 me-2"></i>
                                        Level {{ element.level }}
                                      </div>

                                      <div>
                                        <Vue3Select :append-to-body="true" v-if="workflowEditIndex === index"
                                          :multiple="true" v-model="element.designation" :options="designationOptions"
                                          label="label" @keydown.enter="stopWorkflowEditing" />
                                        <!-- <input v-if="workflowEditIndex === index" :ref="el => setWorkflowInputRef(el, index)"
                          v-model="element.designation" class="form-control form-control-sm"
                          placeholder="Enter Designation" @keydown.enter="stopWorkflowEditing" /> -->
                                        <span v-else>
                                          {{ element.designation.length ? element.designation.join(', ') : '-' }}
                                        </span>
                                      </div>

                                      <div>
                                        <select v-if="workflowEditIndex === index" v-model="element.onReject"
                                          @keydown.enter="stopWorkflowEditing"
                                          class="form-select rounded-0 form-select">
                                          <option value="">Level 0</option>
                                          <option v-for="(prev, i) in getPreviousWorkflowLevels(index)" :key="prev.id"
                                            :value="prev.designation">
                                            Level {{ i + 1 }}
                                          </option>
                                        </select>
                                        <span v-else>{{ getRejectLabel(element.onReject) }}</span>
                                      </div>

                                      <div class="not-allowed">
                                        <button disabled class="btn border-0 not-allowed me-1"
                                          @click="editWorkflowRow(index)" v-if="workflowEditIndex !== index">
                                          <i class="bi bi-pencil font-13"></i>
                                        </button>
                                        <button disabled class="btn btn-sm not-allowed me-1"
                                          v-if="workflowEditIndex === index" @click="stopWorkflowEditing">
                                          <i class="bi bi-check fs-5"></i>
                                        </button>
                                        <button disabled class="btn border-0 not-allowed btn-sm"
                                          @click="removeWorkflowRow(index)">
                                          <i class="bi bi-trash"></i>
                                        </button>
                                      </div>
                                    </div>
                                  </template>
                                </draggable>

                                <!-- <div class="workflow-footer">
                    <button class="btn border-0" @click="addWorkflowRow">
                      <i class="bi bi-plus-circle"></i> Add Approver
                    </button>
                  </div> -->
                              </div>




                            </div>
                          </div>
                        </div>
                        <div v-else-if="currentStep === 3">
                          <div class="row gap-3 my-3">
                            <div class="col">
                              <label class="font-13" for="">Requested by</label>
                              <input disabled type="text" class="form-control rounded-1 "
                                v-model="employeeData.emp_name" placeholder="Enter your name">
                            </div>
                            <div class="col">
                              <label class="font-13" for="">Requested On</label>
                              <input readonly disabled type="text" class="form-control rounded-1 "
                                v-model="employeeData.requested_on" placeholder="Enter requested date">
                            </div>
                            <div class="col">
                              <label class="font-13" for="">Employee ID</label>
                              <input disabled type="text" class="form-control rounded-1 "
                                v-model="employeeData.emp_code" placeholder="Enter employee ID">
                            </div>
                          </div>
                          <div class="row">
                            <div class="col">
                              <div>
                                <label class="font-13" for="">Expense Code</label>
                                <Vue3Select :append-to-body="true" v-model="expense_code" @open="fetchExpenseCodes"
                                  :multiple="false" :options="expenseCodeOptions" label="label" />
                              </div>
                            </div>
                            <div class="col">
                              <label class="font-13" for="">Cost Center</label>
                              <Vue3Select :append-to-body="true" v-model="cost_center" @open="fetchCostCenters"
                                :multiple="false" :options="costCenterOptions" label="label" />

                            </div>
                            <div class="col">
                              <label class="font-13" for="">Division</label>

                            </div>

                          </div>


                          <div v-if="comparisonType === 1">
                            <div v-if="sortedVendors.length">
                              <h6 class="text-success fw-bold mb-3">Vendor Details</h6>

                              <!-- Vendor Info -->
                              <div class="border rounded p-3">
                                <table class="table table-borderless">
                                  <tr>
                                    <td>Vendor Name:</td>
                                    <td>
                                      <div class="value">{{ vendor.vendor_name }}</div>
                                    </td>
                                    <td>GST Number:</td>
                                    <td>
                                      <div class="value">{{ vendor.gst_number }}</div>
                                    </td>
                                  </tr>
                                  <tr>
                                    <td>Vendor Address:</td>
                                    <td>
                                      <div class="value">{{ vendor.address }}</div>
                                    </td>
                                    <td>Phone:</td>
                                    <td>
                                      <div class="value">{{ vendor.phone_number }}</div>
                                    </td>
                                  </tr>
                                  <tr>
                                    <td>Mail ID:</td>
                                    <td>
                                      <div class="value">{{ vendor.mail_id }}</div>
                                    </td>
                                    <td>Bid Rank:</td>
                                    <td>
                                      <div class="value">{{ vendor.rank }}</div>
                                    </td>
                                  </tr>
                                </table>
                              </div>

                              <!-- Pricing Details -->
                              <div class="details-table mt-3">
                                <table class="table table-bordered">
                                  <thead>
                                    <tr>
                                      <th>ITEM NAME</th>
                                      <th>UNIT</th>
                                      <th style="text-align: center;">QUANTITY</th>
                                      <th style="text-align: center;">GST %</th>
                                      <th style="text-align: center;">UNIT PRICE</th>
                                      <th style="text-align: center;">TOTAL PRICE</th>
                                    </tr>
                                  </thead>
                                  <tbody>
                                    <tr v-for="(item, i) in vendor.ezy_item_details" :key="i">
                                      <td>{{ item.item_name }}</td>
                                      <td>{{ item.item_unit_of_measure }}</td>
                                      <td style="text-align: center;">{{ item.item_quantity }}</td>
                                      <td style="text-align: center;">{{ item.item_gst }}%</td>
                                      <td style="text-align: right;">{{ item.unitPrice }}</td>
                                      <td style="text-align: right;">{{ item.totalPrice }}</td>
                                    </tr>
                                    <tr>
                                      <td colspan="5" style="text-align: right; font-weight: bold;">TOTAL:</td>
                                      <td style="text-align: right;">{{ vendor.total_value }}/-</td>
                                    </tr>
                                  </tbody>
                                </table>
                              </div>

                              <!-- Footer (Taxes + Charges) -->
                              <div class="footer mt-3">
                                <table class="table table-borderless">
                                  <tr>
                                    <td>Delivery Time:</td>
                                    <td>
                                      <div class="value">{{ vendor.delivery_time }}</div>
                                    </td>
                                    <td>CGST ({{ vendor.transportation_cgst_percent }}%):</td>
                                    <td>
                                      <div class="value">{{ vendor.transportation_cgst_amount }}</div>
                                    </td>
                                  </tr>
                                  <tr>
                                    <td>Payment Terms:</td>
                                    <td>
                                      <div class="value">{{ vendor.payment_terms }}</div>
                                    </td>
                                    <td>UTGST ({{ vendor.transportation_utgst_percent }}%):</td>
                                    <td>
                                      <div class="value">{{ vendor.transportation_utgst_amount }}</div>
                                    </td>
                                  </tr>
                                  <tr>
                                    <td colspan="2" rowspan="4">
                                      <small class="font-11">
                                        Note: At Hyatt, we view our suppliers as business partners who are committed to
                                        legal
                                        compliance
                                        and ethical conduct. By executing this Work Order, you acknowledge that your
                                        company
                                        abides
                                        by
                                        Hyatt's Supplier Code of Conduct, available at
                                        Hyatt.com/supplier-code-of-conduct.
                                        Please contact your point person should you require this Code in your language.
                                      </small>
                                    </td>
                                    <td>IGST ({{ vendor.transportation_igst_percent }}%):</td>
                                    <td>
                                      <div class="value">{{ vendor.transportation_igst_amount }}</div>
                                    </td>
                                  </tr>
                                  <tr>
                                    <td>Freight:<br>
                                      <span style="font-size: smaller;">(Transportation/Shipping)</span>
                                    </td>
                                    <td>
                                      <div class="value">

                                        {{ vendor.transportation_total_amount }}
                                      </div>
                                    </td>
                                  </tr>
                                  <tr>
                                    <td>Additional Charges:</td>
                                    <td>
                                      <div class="value">{{ vendor.additional_charges }}/-</div>
                                    </td>
                                  </tr>
                                  <tr>
                                    <td style="font-weight: bold;">Grand Total:</td>
                                    <td>
                                      <div class="value">{{ vendor.grand_total }}/-</div>
                                    </td>
                                  </tr>
                                </table>
                              </div>
                            </div>
                            <div v-else>
                              <p class="text-danger">No vendors available.</p>
                            </div>
                          </div>
                          <div v-else>
                            <div class="mt-2">
                              <div class="card">
                                <div class=" text-center mt-2 p-5">

                                  <p class="text-danger font-13">No Work Order Creating For Purchase order</p>

                                </div>
                              </div>
                            </div>
                          </div>
                        </div>
                      </transition>
                    </div>
                    <!-- Stepper Navigation -->

                  </div>
                </div>
              </div>
              <div class="tab-pane fade  " id="tab2" role="tabpanel" aria-labelledby="tab2-tab">
                <div>
                  <div>
                    <div class="d-flex justify-content-between align-items-center">
                      <span class="font-13">Item Details</span>
                      <div>
                        <button class="btn btn-dark font-12" @click="openItemModalMaster('create')">Create Item</button>
                      </div>
                    </div>
                    <div class="table-responsive mt-2">
                      <table class="table item-table  rounded-table">
                        <thead>
                          <tr>
                            <th>Item Name</th>
                            <th>Unit of Measure</th>
                            <th class=" text-center">Actions</th>

                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="(item, index) in availableItems" :key="index">
                            <td>{{ item.item_name }}</td>
                            <td>{{ item.item_unit_of_measure }}</td>
                            <td class="text-center" >
                              <span v-tooltip.top="'Edit'"  @click="openItemModalMaster('edit', item, index)" class="text-center ">

                              <i class="bi bi-pencil-fill mx-2 "></i>
                              </span>
                              <span v-tooltip.top="'Delete'"  @click="deleteMasterItem(item, index)"><i class="bi bi-trash-fill mx-1 text-danger" ></i></span>
                            
                            </td>

                          </tr>
                        </tbody>
                      </table>
                    </div>
                    <div class="modal fade" id="NewItemModalMaster" tabindex="-1" aria-labelledby="NewItemModalMaster"
                    aria-hidden="true">
                    <div class="modal-dialog modal-lg modal-dialog-scrollable">
                      <div class="modal-content">
                        <div class="modal-header">
                          <h5 class="modal-title" id="NewItemModalMaster">Add New Item</h5>
                          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">

                          <div class="d-flex gap-2 mb-5 mt-3">
                            <div class="flex-grow-1 ">
                             
                              <label class="font-13" for="itemName">Item Name</label>
                              <input :disabled="modalType ==='edit'" type="text" class="form-control" placeholder="Item name" v-model="newItem.name" />
                            </div>
                            
                            <div class="flex-grow-1">
                              <label class="font-13" for="itemUnit">Unit</label>
                              <select class="form-select" v-model="newItem.unit">
                                <option value="" disabled>Select Unit</option>
                                <option value="kg">Kg</option>
                                <option value="g">G</option>
                                <option value="l">L</option>
                                <option value="Nos">Nos</option>

                              </select>

                            </div>
                            
                          </div>

                        </div>

                        <div class="modal-footer">
                          <button class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button>
                           <button class="btn btn-sm btn-dark" @click="saveItemMaster">
                              {{ modalType === 'create' ? 'Add Item' : 'Update Item' }}
                            </button>

                        </div>
                      </div>
                    </div>
                  </div>

                  </div>


                </div>
              </div>
              <div class="tab-pane fade  " id="tab3" role="tabpanel" aria-labelledby="tab3-tab">
                <div>
                  <div class="d-flex justify-content-between align-items-center">
                    <span class="font-13">Vendor Details</span>
                    <div>
                      <button class="btn btn-dark font-12" @click="NewMasterVendorCreate('create')">
                        Create vendor
                      </button>

                    </div>
                  </div>
                  <div class="table-responsive mt-2">
                    <table class="table vendor-table shadow-sm rounded-table">
                      <thead>
                        <tr>
                          <th>GST</th>
                          <th>Name</th>
                          <th>Contact</th>
                          <th>Email</th>
                          <th>Address</th>
                          <th class="text-center px-4">Actions</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="(vendor, index) in vendorMasterList" :key="index">
                          <td>{{ vendor.gst_number }}</td>
                          <td>{{ vendor.vendor_name }}</td>
                          <td>{{ vendor.phone_number }}</td>
                          <td>{{ vendor.mail_id }}</td>
                          <td>
                            {{ vendor.address }}
                          </td>
                          <td class="text-center">
                          <span v-tooltip.top="'Edit'" class="font-12 btn-light" @click="NewMasterVendorCreate('edit', vendor)">
                           <i class="bi bi-pencil-fill"></i>
                          </span>
                        </td>

                        </tr>
                      </tbody>
                    </table>
                  </div>
                   <div class="modal fade" id="NewVendorMasterData" tabindex="-1" aria-labelledby="NewVendorMasterData"
                    aria-hidden="true">
                    <div class="modal-dialog modal-lg modal-dialog-scrollable">
                      <div class="modal-content">
                        <div class="modal-header">
                          <h5 class="modal-title font-14" id="NewVendorMasterData">{{ isEditingVendor ? 'Edit Vendor': 'Add New Vendor'}}</h5>
                          <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                        </div>
                        <div class="modal-body">

                          <div class="p-1 mb-3">
                            <div class="row">
                              <div class="col-md-6">
                                <label class="font-13 fw-medium" for="itemGST">GST Number</label>
                              <input :disabled="isEditingVendor"  type="text" class="form-control" placeholder="GST" v-model="NewMasterVendor.gst_number" />
                              </div>
                               <div class="col-md-6">
                              <label class="font-13 fw-medium" for="itemContact">Contact Number</label>
                              <input type="text" class="form-control" placeholder="Contact Number" v-model="NewMasterVendor.contact_number" />
                            </div>
                             
                            </div>
                            <div class="row">
                               <div class="col-md-6">
                                <label class="font-13 fw-medium" for="itemName">Vendor Name</label>
                                <input type="text" class="form-control" placeholder="Vendor name" v-model="NewMasterVendor.vendor_name" />
                              </div>
                               

                            <div class="col-md-6">
                              <label class="font-13 fw-medium" for="itemEmail">Email</label>
                              <input type="email" class="form-control" placeholder="Email" v-model="NewMasterVendor.mail_id" />
                            </div>

                            </div>
                            <div class="row">
                            <div class="col-md-6">
                              <label class="font-13 fw-medium" for="itemAddress">Address</label>
                              <textarea class="form-control" placeholder="Address" v-model="NewMasterVendor.address"></textarea>
                            </div>

                            </div>
                            

                          


                          </div>

                        </div>

                        <div class="modal-footer">
                          <!-- <button class="btn btn-outline-secondary" data-bs-dismiss="modal">Cancel</button> -->
                          <!-- <button class="btn btn-sm btn-dark" @click="AddNewVendor">Add Vendor</button> -->
                          <div class="modal-footer">
                          <button class="btn btn-outline-secondary" data-bs-dismiss="modal" @click="resetVendorForm">Cancel</button>
                          <button class="btn btn-sm btn-dark font-13 text-white" @click="AddOrUpdateVendor">
                            {{ isEditingVendor ? 'Update Vendor' : 'Add Vendor' }}
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
// import { toast } from 'vue3-toastify';
import draggable from "vuedraggable";
import Vue3Select from 'vue3-select'
import 'vue3-select/dist/vue3-select.css';
import { showError, showInfo, showSuccess } from '../shared/services/toast';


const route = useRoute();
const router = useRouter()
const searchItem = ref('');
const selectedItems = ref([]);
const vendorSearch = ref('')
const filteredVendorOptions = ref([])

  // { id: 1, item_name: 'Cable',quantity: 10,item_unit_of_measure:'Nos'},
  // { id: 1, item_name: 'Desktop',quantity: 10,item_unit_of_measure:'Nos'}  
const itemDetails = ref([

]);
const disableIGST = ref(false);
const disableCGST_UTGST = ref(false);
const expenseCodeOptions = ref([]);
const costCenterOptions = ref([]);
const editingIndex = ref(null);
const employeeData = ref([])
const vendorDetails = ref([

]);
const expense_code = ref('')
const cost_center = ref('')

// { item_name: 'Computer', item_unit_of_measure: 'Unit' },
// { item_name: 'CPU', item_unit_of_measure: 'Unit' },
// { item_name: 'Mouse', item_unit_of_measure: 'Unit' },
// { item_name: 'Molds', item_unit_of_measure: 'Kilogram' },
// { item_name: 'Keyboard', item_unit_of_measure: 'Unit' },
// { item_name: 'Monitor', item_unit_of_measure: 'Unit' },
// { item_name: 'RAM', item_unit_of_measure: 'GB' },
// { item_name: 'SSD', item_unit_of_measure: 'GB' },
// { item_name: 'Printer', item_unit_of_measure: 'Unit' },
// { item_name: 'Scanner', item_unit_of_measure: 'Unit' },
// { item_name: 'Router', item_unit_of_measure: 'Unit' },
// { item_name: 'Cable', item_unit_of_measure: 'Meter' },
// { item_name: 'Switch', item_unit_of_measure: 'Unit' },
// { item_name: 'Hard Drive', item_unit_of_measure: 'TB' },
const availableItems = ref([

]);
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
//   delivery_time: '5',
//   payment_terms: '30',
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
//   delivery_time: '7',
//   payment_terms: '45',
//   remark: '',
//   address: '456 Elm St, City, State, 123456'
// },
// Add more vendor entries here...
const vendorMasterList = ref([
])
const NewMasterVendor = ref({
  vendor_name: '',
  gst_number: '',
  contact_number: '',
  mail_id: '',
  address: ''

})

const vendorForm = ref({
  vendor_name: '', gst_number: '', phone_number: '', mail_id: '',
  ezy_item_details: [
    { ...itemDetails }
  ],
  transport: '',
  delivery_time: '',
  payment_terms: '',
  rank: '',
  remark: '',
  address: '',
  attachments: [],
  total_value: '',
  // taxes
  cgst_percent: 0,
  utgst_percent: 0,
  igst_percent: 0,

  // freight fields
  transportation_charges: 0,
  transportation_cgst_percent: 0,
  transportation_cgst_amount: 0,
  transportation_utgst_percent: 0,
  transportation_utgst_amount: 0,
  transportation_igst_percent: 0,
  transportation_igst_amount: 0,
  transportation_total_amount: 0,

  // additional charges
  additional_charges: 0,

  // computed amounts
  cgst_amount: 0,
  utgst_amount: 0,
  igst_amount: 0,
  transportation_gst_amount: 0,

  grand_total: 0
});
const modalType = ref("create"); 
const isEditingVendor = ref(false);
const editingVendorName = ref(null);

const steps = [
  { label: 'Vendor & Item Details', icon: 'bi bi-box-seam' },
  { label: 'Preview Comparison', icon: 'bi bi-eye' },
  { label: 'Workflow', icon: 'bi bi-diagram-3' },
  { label: 'Work Order', icon: 'bi bi-file-earmark-text' },
]
const sortedVendors = computed(() => {
  return [...vendorDetails.value].sort((a, b) => {
    // Extract the numeric part of "L1", "L2", etc.
    const rankA = parseInt(a.rank?.replace('L', '') || 999, 10);
    const rankB = parseInt(b.rank?.replace('L', '') || 999, 10);
    return rankA - rankB;
  });
});
const vendor = computed(() => {
  return sortedVendors.value.find(v => v.rank === 'L1') || {};
});

const l1Fields = [
  { label: 'Vendor Name', key: 'vendor_name' },
  { label: 'GST Number', key: 'gst_number' },
  { label: 'Phone Number', key: 'phone_number' },
  { label: 'Email', key: 'mail_id' },
  { label: 'Total Value', key: 'total_value' },
  { label: 'Payment Terms', key: 'payment_terms' },
  { label: 'Delivery Time', key: 'delivery_time' },
  { label: 'Transport Charges', key: 'transportation_total_amount' },
  { label: 'Remark', key: 'remark' },
  { label: 'Address', key: 'address' },
  { label: 'Attachments', key: 'attachments' }
];
onMounted(() => {
  employeeData.value = JSON.parse(localStorage.getItem('employeeData') || '{}');

  // console.log(employeeData.value, "[[[[[[[[[[[[]]]]]]]]]]]]");
  fetchingItemsList()
  fetchingVendorMasterData()
  window.addEventListener('click', handleClickOutside);
  fetchingWork()
  if (route.query.selectedFormId) {
    getWorkflowRequest()
  }
  const now = new Date();
  const requestedOn = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;
  employeeData.value.requested_on = requestedOn;
  employeeData.value.emp_code = employeeData.value.emp_code || 'EMP' + Math.floor(Math.random() * 10000);

});
const comparisonType = ref(1); // ✅ default Vendor Comparison

// Watcher if you want to react to changes
watch(comparisonType, (newVal) => {
  console.log("Selected Comparison Type:", newVal);
});
const currentStep = ref(0)

const goToStep = (index) => {
  // Block going to step 1 (Preview) if conditions not met
  // if (index === 1 && (!vendorDetails.value.length || !itemDetails.value.length)) {
  //   showInfo("Please add vendor and item details before previewing.")
  //   return
  // }
  currentStep.value = index
}

const nextStep = () => {
  // If moving from step 0 to step 1, check conditions
  // if (currentStep.value === 0 && (!vendorDetails.value.length || !itemDetails.value.length)) {
  //   showInfo("Please add vendor and item details before previewing.")
  //   return
  // }

  if (currentStep.value < steps.length - 1) {
    currentStep.value++
  } else {
    submitComparison()
  }
}

const prevStep = () => {
  if (currentStep.value > 0) {
    currentStep.value--
  }
}
const previewUrl = ref(null)

function openPreview(url) {
  console.log(url);
  console.log(vendorForm.value.attachments);
  if (vendorForm.value.attachments.length > 0) {
    previewUrl.value = vendorForm.value.attachments;
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
    delivery_time: '',
    payment_terms: '',
    rank: '',
    remark: '',
    total_value: '',
    address: '',
    ezy_item_details: JSON.parse(JSON.stringify(itemDetails.value)),  // copy the main itemDetails
    attachments: [],
    cgst_percent: 0,
    utgst_percent: 0,
    igst_percent: 0,
    transportation_charges: 0,
    transportation_cgst_percent: 0,
    transportation_cgst_amount: '',
    transportation_utgst_percent: 0,
    transportation_utgst_amount: '',
    transportation_igst_percent: 0,
    transportation_igst_amount: '',
    transportation_total_amount: 0,
    additional_charges: 0,
    cgst_amount: '',
    utgst_amount: '',
    igst_amount: '',
    grand_total: ''


  };



  editingVendorIndex.value = null;  // because it's a new vendor
  new bootstrap.Modal(document.getElementById('vendorModal')).show();
}
function fetchingVendorMasterData() {
  let queryParams = {
    fields: JSON.stringify(['vendor_name', 'mail_id', 'contact_number', 'gst_number', 'address']),
    limit_page_length: 'None'
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
      showError('Failed to fetch items.');
    });
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
//       delivery_time: vendor.delivery_time,
//       payment_terms: vendor.payment_terms,
//       remark: vendor.remark,
//       total_value: vendor.total_value,
//       address: vendor.address,
//       pricing_details: JSON.stringify(vendor.ezy_item_details)
//     };
//   });

//   const ezy_item_details = vendorDetails.value[0].ezy_item_details.map(item => ({
//     item_name: item.item_name,
//     item_unit_of_measure: item.item_unit_of_measure,
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
//       showSuccess('Comparison submitted successfully!');
//       request_raising_fn(response.data);
//     })
//     .catch(error => {
//       console.error('Error submitting comparison:', error);
//       showError('Failed to submit comparison.');
//     });
// };
// const submitComparison = async () => {
//   const vendor_details = vendorDetails.value.map(vendor => ({
//     vendor_name: vendor.vendor_name,
//     gst_number: vendor.gst_number,
//     phone_number: vendor.phone_number,
//     mail_id: vendor.mail_id,
//     biddle_rank: vendor.rank,
//     transportation_charges: vendor.transport,
//     delivery_time: vendor.delivery_time,
//     payment_terms: vendor.payment_terms,
//     remark: vendor.remark,
//     total_value: vendor.total_value,
//     address: vendor.address,
//     attachments: JSON.stringify(vendor.attachments),
//     pricing_details: JSON.stringify(vendor.ezy_item_details),

//   }));

//   const ezy_item_details = vendorDetails.value[0].ezy_item_details.map(item => ({
//     item_name: item.item_name,
//     item_unit_of_measure: item.item_unit_of_measure,
//     item_quantity: item.quantity
//   }));

//   // Your main document to save (e.g., Ezy Contract or any other DocType)
//   const form = {
//     doctype: "CTO", // Replace with your actual DocType name
//     vendor_details,
//     ezy_item_details
//   };

//   const formData = new FormData();
//   formData.append("doc", JSON.stringify(form));
//   formData.append("action", "Save");
//   console.log(form);

//   try {
//     const response = await axiosInstance.post(apis.savedocs, formData);
//     console.log("Comparison saved successfully:", response);
//     showSuccess("Comparison saved successfully!");
//     request_raising_fn(response.docs[0]);
//   } catch (error) {
//     console.error("Error saving comparison:", error);
//     showError("Failed to save comparison.");
//   }
// };


// function exportfile() {

// }
// function sortVendors() {
//   // Sort vendors by total_value ascending (lowest first)
//   sortedVendors.value.sort((a, b) => parseFloat(a.grand_total) - parseFloat(b.grand_total));
// }

const submitComparison = async () => {
  // sortVendors();
  // Format: "2025-08-06 17:28"
  const now = new Date();
  const requestedOn = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')} ${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}`;

  const employeeData = JSON.parse(localStorage.getItem('employeeData') || '{}');
  const requestedBy = employeeData.emp_name || 'Unknown';

  const vendor_details = sortedVendors.value.map(vendor => ({
    vendor_name: vendor.vendor_name,
    gst_number: vendor.gst_number,
    phone_number: vendor.phone_number,
    mail_id: vendor.mail_id,
    biddle_rank: vendor.rank,
    delivery_time: vendor.delivery_time,
    payment_terms: vendor.payment_terms,
    remark: vendor.remark,
    total_value: vendor.total_value,
    address: vendor.address,
    attachments: JSON.stringify(vendor.attachments),
    pricing_details: JSON.stringify(vendor.ezy_item_details),
    cgst_percent: vendor.cgst_percent,
    utgst_percent: vendor.utgst_percent,
    igst_percent: vendor.igst_percent,
    transportation_charges: vendor.transportation_charges,
    transportation_cgst_percent: vendor.transportation_cgst_percent,
    transportation_utgst_percent: vendor.transportation_utgst_percent,
    transportation_igst_percent: vendor.transportation_igst_percent,
    transportation_cgst_amount: vendor.transportation_cgst_amount,
    transportation_utgst_amount: vendor.transportation_utgst_amount,
    transportation_igst_amount: vendor.transportation_igst_amount,
    transportation_total_amount: vendor.transportation_total_amount,
    cgst_amount: vendor.cgst_amount,
    utgst_amount: vendor.utgst_amount,
    igst_amount: vendor.igst_amount,
    additional_charges: vendor.additional_charges,
    grand_total: vendor.grand_total,

  }));

  const ezy_item_details = vendorDetails.value[0].ezy_item_details.map(item => ({
    item_name: item.item_name,
    item_unit_of_measure: item.item_unit_of_measure,
    item_quantity: item.item_quantity
  }));
    const pricing_details = vendorDetails.value.flatMap(vendor =>
      vendor.ezy_item_details.map(item => ({
        vendor_name: vendor.vendor_name,   // include vendor_name
        item_name: item.item_name,
        item_unit_of_measure: item.item_unit_of_measure,
        item_quantity: item.item_quantity,
        item_gst: item.item_gst,
        unitprice: item.unitPrice,         // keep naming consistent
        totalprice: item.totalPrice,
        doctype: "Pricing Details"         // if required by backend
      }))
    );

  const form = {
    doctype: "VENDOR COMPARISON",
    vendor_details,
    ezy_item_details,
    pricing_details,
    requested_by: requestedBy,
    requested_on: requestedOn,
    work_order: comparisonType.value === 1 ? 1 : 0,
    purchase_order: comparisonType.value === 0 ? 1 : 0,
    expense_code: expense_code.value || '',
    cost_center: cost_center.value || '',
  };

  const formData = new FormData();
  formData.append("doc", JSON.stringify(form));
  formData.append("action", "Save");

  console.log(form);

  try { 
    const response = await axiosInstance.post(apis.savedocs, formData);
    console.log("Comparison saved successfully:", response);
    showSuccess("Comparison saved successfully!");
    request_raising_fn(response.docs[0]);
  } catch (error) {
    console.error("Error saving comparison:", error);
    showError("Failed to save comparison.");
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
    doctype_name: 'VENDOR COMPARISON',
    ids: [item.name],
    reason: "Request Raised",
    url_for_request_id: "",
    files: [],
    property: employeeData.value.company_field,
    ip_address: '',
    employee_id: employeeData.value.emp_code,
    // be_half_of:item.requester_name,
    // request_for:item.request_for,
  };
  axiosInstance.post(apis.raising_request, data_obj).then((resp) => {
    if (resp?.message?.success === true) {


      showSuccess("Request Raised");
      setTimeout(() => {
        router.push({ path: '/todo/raisedbyme' });
      }, 300);
    }
  })
    .catch((error) => {
      console.error("Error raising request:", error);
      showError("Error raising request");
    })
  // .finally(() => {
  //   saveloading.value = false;
  // });
}
const hasSelectedVendor = computed(() =>
  vendorDetails.value.some(vendor => vendor.selected)
);
// function updateTotalPrice(item) {
//   const qty = parseFloat(item.quantity || 0);
//   const price = parseFloat(item.unitPrice || 0);
//   item.totalPrice = (qty * price).toFixed(2);
// }
// function updateTotalPrice(item) {
//   const qty = parseFloat(item.quantity || 0);
//   const price = parseFloat(item.unitPrice || 0);
//   const total = qty * price;

//   item.totalPrice = total.toLocaleString('en-IN', {
//     minimumFractionDigits: 2,
//     maximumFractionDigits: 2
//   });
// }
// function updateTotalPrice(item) {
//   const qty = parseFloat(item.item_quantity || 0);
//   const price = parseFloat((item.unitPrice || "0").toString().replace(/,/g, "")); // remove commas before calc
//   const total = qty * price;

//   // Format unit price
//   item.unitPrice = price.toLocaleString('en-IN', {
//     minimumFractionDigits: 2,
//     maximumFractionDigits: 2
//   });

//   // Format total price
//   item.totalPrice = total.toLocaleString('en-IN', {
//     minimumFractionDigits: 2,
//     maximumFractionDigits: 2
//   });
// }
// function updateTotalPrice(item) {
//   const qty = parseFloat(item.item_quantity || 0);
//   const price = parseFloat((item.unitPrice || "0").toString().replace(/,/g, ""));
//   const total = qty * price;

//   item.unitPrice = price.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
//   item.totalPrice = total.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

//   // update vendorForm total_value
//   vendorForm.value.total_value = vendorForm.value.ezy_item_details.reduce((sum, i) => {
//     const val = parseFloat((i.totalPrice || "0").toString().replace(/,/g, "")) || 0;
//     return sum + val;
//   }, 0).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

//   calculateTaxes(); // ✅ include taxes in grand total
// }
// function updateTotalPrice(item) {
//   const qty = parseFloat(item.item_quantity || 0);
//   const price = parseFloat((item.unitPrice || "0").toString().replace(/,/g, ""));
//   const gstPercent = parseFloat(item.item_gst || 0);

//   // base total for this item
//   const itemBaseTotal = qty * price;

//   // item GST
//   const itemGST = (itemBaseTotal * gstPercent) / 100;

//   // store formatted values
//   item.unitPrice = price.toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
//   item.itemBaseTotal = itemBaseTotal; // keep raw number
//   item.itemGSTAmount = itemGST;       // keep raw number

//   // final total for item (base + gst)
//   item.totalPrice = (itemBaseTotal + itemGST).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

//   // update vendorForm total_value (sum of item base amounts only)
//   vendorForm.value.total_value = vendorForm.value.ezy_item_details.reduce((sum, i) => {
//     const val = parseFloat(i.itemBaseTotal || 0) || 0;
//     return sum + val;
//   }, 0).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });

//   calculateTaxes(); // ✅ include item GST + transportation GST + others
// }
function calculateTaxes() {
  // 1️⃣ Item Calculations
  let itemBaseTotal = 0;
  let itemGSTTotal = 0;

  vendorForm.value.ezy_item_details.forEach((item) => {
    const qty = Number(item.item_quantity) || 0;
    const rate = Number(item.unitPrice) || 0;
    const gstPercent = Number(item.item_gst) || 0;

    const baseAmount = qty * rate;
    const gstAmount = (baseAmount * gstPercent) / 100;
    const total = baseAmount + gstAmount;

    // update each item
    item.totalPrice = total.toFixed(2);

    // accumulate
    itemBaseTotal += baseAmount;
    itemGSTTotal += gstAmount;
  });

  // ✅ total_value should include item price + item GST
  vendorForm.value.total_value = (itemBaseTotal + itemGSTTotal).toFixed(2);

  // 2️⃣ Transportation Calculation
  const transBase = Number(vendorForm.value.transportation_charges) || 0;
  const tCGST = (transBase * (vendorForm.value.transportation_cgst_percent || 0)) / 100;
  const tUTGST = (transBase * (vendorForm.value.transportation_utgst_percent || 0)) / 100;
  const tIGST = (transBase * (vendorForm.value.transportation_igst_percent || 0)) / 100;

  const transTotal = transBase + tCGST + tUTGST + tIGST;

  vendorForm.value.transportation_cgst_amount = tCGST.toFixed(2);
  vendorForm.value.transportation_utgst_amount = tUTGST.toFixed(2);
  vendorForm.value.transportation_igst_amount = tIGST.toFixed(2);
  vendorForm.value.transportation_total_amount = transTotal.toFixed(2);

  // 3️⃣ Additional Charges
  const additional = Number(vendorForm.value.additional_charges) || 0;

  // 4️⃣ Grand Total = Items (Base + GST) + Transport (Base + GST) + Additional
  const grandTotal = (itemBaseTotal + itemGSTTotal) + transTotal + additional;
  vendorForm.value.grand_total = grandTotal.toFixed(2);
}


function updateTotalPrice(item) {
  const qty = Number(item.item_quantity) || 0;
  const rate = Number(item.unitPrice) || 0;
  const gstPercent = Number(item.item_gst) || 0;

  const base = qty * rate;
  const gst = (base * gstPercent) / 100;
  const total = base + gst;
  item.totalPrice = total.toFixed(2);

  calculateTaxes(); // auto-recalculate totals
}


// function calculateTaxes() {
//   const baseTotal = parseFloat((vendorForm.value.total_value || "0").toString().replace(/,/g, "")) || 0;

//   // item-wise GST (sum of all GST from items)
//   const totalItemGST = vendorForm.value.ezy_item_details.reduce((sum, i) => {
//     return sum + (parseFloat(i.itemGSTAmount || 0));
//   }, 0);

//   // transportation charges + gst
//   const transportCharges = parseFloat(vendorForm.value.transportation_charges || 0);
//   const t_cgst = (transportCharges * (vendorForm.value.transportation_cgst_percent || 0)) / 100;
//   const t_utgst = (transportCharges * (vendorForm.value.transportation_utgst_percent || 0)) / 100;
//   const t_igst = (transportCharges * (vendorForm.value.transportation_igst_percent || 0)) / 100;

//   const transportationTotal = transportCharges + t_cgst + t_utgst + t_igst;

//   // additional
//   const additionalCharges = parseFloat(vendorForm.value.additional_charges || 0);

//   // store values
//   vendorForm.value.item_gst_total = totalItemGST.toFixed(2);
//   vendorForm.value.transportation_cgst_amount = t_cgst.toFixed(2);
//   vendorForm.value.transportation_utgst_amount = t_utgst.toFixed(2);
//   vendorForm.value.transportation_igst_amount = t_igst.toFixed(2);
//   vendorForm.value.transportation_total_amount = transportationTotal.toFixed(2);

//   // final grand total
//   vendorForm.value.grand_total = (
//     baseTotal +
//     totalItemGST +      // ✅ add item-wise gst
//     transportationTotal +
//     additionalCharges
//   ).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
// }

// function calculateTaxes() {
//   const baseTotal = parseFloat((vendorForm.value.total_value || "0").toString().replace(/,/g, "")) || 0;

//   // item GST
//   const cgst = (baseTotal * (vendorForm.value.cgst_percent || 0)) / 100;
//   const utgst = (baseTotal * (vendorForm.value.utgst_percent || 0)) / 100;
//   const igst = (baseTotal * (vendorForm.value.igst_percent || 0)) / 100;

//   // transport
//   const transportCharges = parseFloat(vendorForm.value.transportation_charges || 0);
//   const t_cgst = (transportCharges * (vendorForm.value.transportation_cgst_percent || 0)) / 100;
//   const t_utgst = (transportCharges * (vendorForm.value.transportation_utgst_percent || 0)) / 100;
//   const t_igst = (transportCharges * (vendorForm.value.transportation_igst_percent || 0)) / 100;

//   // additional
//   const additionalCharges = parseFloat(vendorForm.value.additional_charges || 0);

//   // store amounts
//   vendorForm.value.cgst_amount = cgst.toFixed(2);
//   vendorForm.value.utgst_amount = utgst.toFixed(2);
//   vendorForm.value.igst_amount = igst.toFixed(2);

//   vendorForm.value.transportation_cgst_amount = t_cgst.toFixed(2);
//   vendorForm.value.transportation_utgst_amount = t_utgst.toFixed(2);
//   vendorForm.value.transportation_igst_amount = t_igst.toFixed(2);

//   //  Transportation total (readonly field)
//   const transportationTotal = transportCharges + t_cgst + t_utgst + t_igst;
//   vendorForm.value.transportation_total_amount = transportationTotal.toFixed(2);

//   // final grand total
//   vendorForm.value.grand_total = (
//     baseTotal + cgst + utgst + igst +
//     transportationTotal +
//     additionalCharges
//   ).toLocaleString('en-IN', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
// }




// function calculateTaxes() {
//   const baseTotal = parseFloat((vendorForm.value.total_value || "0").toString().replace(/,/g, "")) || 0;

//   const cgst = (baseTotal * (vendorForm.value.cgst_percent || 0)) / 100;
//   const utgst = (baseTotal * (vendorForm.value.utgst_percent || 0)) / 100;
//   const igst = (baseTotal * (vendorForm.value.igst_percent || 0)) / 100;
//   const freight = parseFloat(vendorForm.value.freight || 0);
//   // const transportation_charges = parseFloat(vendorForm.value.transportation_charges || 0);

//   vendorForm.value.cgst_amount = cgst.toFixed(2);
//   vendorForm.value.utgst_amount = utgst.toFixed(2);
//   vendorForm.value.igst_amount = igst.toFixed(2);
// // + transportation_charges

//   vendorForm.value.grand_total = (baseTotal + cgst + utgst + igst + freight ).toLocaleString('en-IN', {
//     minimumFractionDigits: 2,
//     maximumFractionDigits: 2
//   });
// }



// const addItem = () => itemDetails.value.push({ item_name: 'New Item', item_unit_of_measure: 'Unit', quantity: 1, selected: false });



// const editItem = index => {
//   editingIndex.value = index;
// };
const itemInputRefs = ref({});

const setItemInputRef = (el, index) => {
  if (el) {
    itemInputRefs.value[index] = el;
  }
};
const editItem = async (index) => {
  editingIndex.value = index;
  // await nextTick();
  // const input = document.getElementById(`item-name-${index}`);
  // if (input) input.focus();
};

const saveItem = () => {
  console.log(  editingIndex.value);
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
const openItemModal = async () => {
  // Add the new blank item
  itemDetails.value.push({
    item_name: "",
    item_unit_of_measure: "",
    item_quantity: 0,
    selected: false,
  });

  const newIndex = itemDetails.value.length - 1;

  // Trigger edit mode for new row
  editingIndex.value = newIndex;

  // Wait for DOM to render the new row + input
  await nextTick();

  // Manually call editItem so input shows
  // or directly focus the input
  const input = document.getElementById(`item-name-${newIndex}`);
  if (input) input.focus();

  // fetchingItemsList();
};

// const openItemModal = () => {
//   itemDetails.value.push({
//   item_name: "",
//   item_unit_of_measure: "",
//   quantity: 0,
//   selected: false,
// });


// };

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
    itemDetails.value[index].item_unit_of_measure = matchedItem.item_unit_of_measure;
  }

  activeDropdown.value = null;
};
watch(itemDetails, (newItems) => {
  newItems.forEach(item => {
    if (!item.item_name) {
      item.item_unit_of_measure = "";
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
//   item_unit_of_measure: "",
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
  const selectedItems = availableItems.value.filter(item => item.selected);

  if (selectedItems.length === 0) {
    bootstrap.Modal.getInstance(document.getElementById("itemModal")).hide();
    return;
  }

  if (editingIndex.value !== null) {
    // Fill the currently edited row with the first selected item
    const selectedItem = selectedItems[0];
    itemDetails.value[editingIndex.value] = {
      ...itemDetails.value[editingIndex.value], // keep existing qty, etc.
      item_name: selectedItem.item_name,
      item_unit_of_measure: selectedItem.item_unit_of_measure,
    };

    // Exit edit mode
    editingIndex.value = null;
  } else {
    // If not editing → add all selected items as new rows
    const newItems = selectedItems.map(item => ({
      item_name: item.item_name,
      item_unit_of_measure: item.item_unit_of_measure,
      item_quantity: 0,
      selected: false,
    }));

    newItems.forEach(newItem => {
      if (!itemDetails.value.some(existing => existing.item_name === newItem.item_name)) {
        itemDetails.value.push(newItem);
      }
    });
  }

  // Close modal
  bootstrap.Modal.getInstance(document.getElementById("itemModal")).hide();
};

// Watch CGST & UTGST
watch(
  [() => vendorForm.value.transportation_cgst_percent, () => vendorForm.value.transportation_utgst_percent],
  ([newCgst, newUtgst]) => {
    if (newCgst > 0 || newUtgst > 0) {
      disableIGST.value = true;
      vendorForm.value.transportation_igst_percent = 0;
      vendorForm.value.transportation_igst_amount = 0;
    } else {
      disableIGST.value = false;
    }
  }
);

// Watch IGST
watch(
  () => vendorForm.value.transportation_igst_percent,
  (newIgst) => {
    if (newIgst > 0) {
      disableCGST_UTGST.value = true;
      vendorForm.value.transportation_cgst_percent = 0;
      vendorForm.value.transportation_cgst_amount = 0;
      vendorForm.value.transportation_utgst_percent = 0;
      vendorForm.value.transportation_utgst_amount = 0;
    } else {
      disableCGST_UTGST.value = false;
    }
  }
);
// const saveItems = () => {
//   console.log('Saved Items:', JSON.stringify(itemDetails.value, null, 2));

// };


const handleClickOutside = (e) => {
  // If the click is not inside any td or input of editing row, exit edit mode
  if (!e.target.closest('.editable-row')) {
    editingIndex.value = null;
  }
};



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
    item_unit_of_measure: newItem.value.unit,
  };
  console.log(newItemObj);
  axiosInstance.post(apis.resource + doctypes.ezyItems, newItemObj)
    .then(response => {

      showSuccess('New item added successfully!');
      // console.log('New item added:', response.data);
      newItem.value = { name: '', unit: '' };
      fetchingItemsList()
      const modal = bootstrap.Modal.getInstance(document.getElementById('NewItemModalMaster'));
      modal.hide();
      // Optionally, you can refresh the items list or show a success message
    })
    .catch(error => {
      console.error('Error adding new item:', error);
    });


};

const NewMasterVendorCreate = (type = 'create', vendor = null) => {
  // Reset modal mode
  isEditingVendor.value = type === 'edit';
  
  if (type === 'edit' && vendor) {
    // Editing existing vendor
    editingVendorName.value = vendor.gst_number;
    NewMasterVendor.value = {
      vendor_name: vendor.vendor_name,
      gst_number: vendor.gst_number,
      contact_number: vendor.phone_number,
      mail_id: vendor.mail_id,
      address: vendor.address,
    };
  } else {
    // Creating new vendor
    resetVendorForm();
  }

  const modal = new bootstrap.Modal(document.getElementById('NewVendorMasterData'));
  modal.show();
};
const resetVendorForm = () => {
  NewMasterVendor.value = {
    vendor_name: '',
    gst_number: '',
    contact_number: '',
    mail_id: '',
    address: '',
  };
};
const AddOrUpdateVendor = () => {
  // Basic validation
  if (!NewMasterVendor.value.vendor_name || !NewMasterVendor.value.gst_number) {
    showError('Please fill required fields.');
    return;
  }

  // Vendor payload
  const vendorData = {
    vendor_name: NewMasterVendor.value.vendor_name,
    gst_number: NewMasterVendor.value.gst_number,
    contact_number: NewMasterVendor.value.contact_number,
    mail_id: NewMasterVendor.value.mail_id,
    address: NewMasterVendor.value.address,
  };

  // 🔄 EDIT existing vendor
  if (isEditingVendor.value) {
    axiosInstance
      .put(`${apis.resource + doctypes.ezyVendors}/${editingVendorName.value}`, vendorData)
      .then(() => {
        showSuccess('Vendor updated successfully!');
        resetVendorForm();
        fetchingVendorMasterData();
        const modal = bootstrap.Modal.getInstance(document.getElementById('NewVendorMasterData'));
        modal.hide();
      })
      .catch(err => {
        console.error('Error updating vendor:', err);
        showError('Failed to update vendor.');
      });
  }

  // ➕ CREATE new vendor
  else {
    axiosInstance
      .post(apis.resource + doctypes.ezyVendors, vendorData)
      .then(() => {
        showSuccess('New vendor added successfully!');
        resetVendorForm();
        fetchingVendorMasterData();
        const modal = bootstrap.Modal.getInstance(document.getElementById('NewVendorMasterData'));
        modal.hide();
      })
      .catch(err => {
        console.error('Error adding vendor:', err);
        showError('Failed to add vendor.');
      });
  }
};



// function AddNewVendor(){
//   let MasterVendor = {
//       vendor_name: NewMasterVendor.value.vendor_name,
//       mail_id: NewMasterVendor.value.mail_id,
//       contact_number: NewMasterVendor.value.contact_number,
//       gst_number: NewMasterVendor.value.gst_number,
//       address: NewMasterVendor.value.address,
//     }
//     // console.log(MasterVendor, "api"); 
//     axiosInstance.post(apis.resource + doctypes.ezyVendors, MasterVendor)
//       .then(response => {
//         console.log('Vendor saved successfully:', response.data);
//         showSuccess('Vendor details saved successfully!');
//         const modal = bootstrap.Modal.getInstance(document.getElementById('NewVendorMasterData'));
//         modal.hide();
//         fetchingVendorMasterData()
//       })
//       .catch(error => {
//         console.error('Error saving vendor:', error);
//         showError('Failed to save vendor details.');
//       });

// }
const editingVendorIndex = ref(null);


function openVendorModal(index) {
  const vendor = vendorDetails.value[index];
  const currentItemNames = vendor.ezy_item_details.map(i => i.item_name);
  const newItems = itemDetails.value.filter(i => !currentItemNames.includes(i.item_name));

  vendorForm.value = {
    vendor_name: vendor.vendor_name,
    gst_number: vendor.gst_number,
    phone_number: vendor.phone_number,
    mail_id: vendor.mail_id,
    transport: vendor.transport || 'Free delivery',
    delivery_time: vendor.delivery_time || '',
    payment_terms: vendor.payment_terms || '',
    rank: vendor.rank || '',
    remark: vendor.remark || '',
    total_value: vendor.total_value,
    address: vendor.address || '',
    attachments: vendor.attachments, // Ensure attachments is always an array
    cgst_percent: vendor.cgst_percent || 0,
    cgst_amount: vendor.cgst_amount || 0,
    utgst_percent: vendor.utgst_percent || 0,
    utgst_amount: vendor.utgst_amount || 0,
    igst_percent: vendor.igst_percent || 0,
    igst_amount: vendor.igst_amount || 0,
    transportation_charges: vendor.transportation_charges || 0,
    transportation_cgst_percent: vendor.transportation_cgst_percent || 0,
    transportation_cgst_amount: vendor.transportation_cgst_amount || 0,
    transportation_utgst_percent: vendor.transportation_utgst_percent || 0,
    transportation_utgst_amount: vendor.transportation_utgst_amount || 0,
    transportation_igst_percent: vendor.transportation_igst_percent || 0,
    transportation_igst_amount: vendor.transportation_igst_amount || 0,
    transportation_total_amount: vendor.transportation_total_amount || 0,
    additional_charges: vendor.additional_charges || 0,
    grand_total: vendor.grand_total || 0,
    // Load the vendor's own items (if any), else empty array
    ezy_item_details: [...vendor.ezy_item_details, ...JSON.parse(JSON.stringify(newItems))]
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
// function calculateVendorTotal() {
//   const total = vendorForm.value.ezy_item_details.reduce((sum, item) => {
//     // remove commas before parsing
//     return sum + parseFloat((item.totalPrice || "0").replace(/,/g, ""));
//   }, 0);

//   vendorForm.value.total_value = total.toLocaleString('en-IN', {
//     minimumFractionDigits: 2,
//     maximumFractionDigits: 2
//   });
// }
function calculateVendorTotal() {
  const total = vendorForm.value.ezy_item_details.reduce((sum, item) => {
    return sum + (parseFloat(item.totalPrice) || 0); // totalPrice should be a number, not string
  }, 0);

  // store as number
  vendorForm.value.total_value = total;
}



// function calculateVendorTotal() {
//   const total = vendorForm.value.ezy_item_details.reduce((sum, item) => {
//     console.log( item.totalPrice);
//     return sum + parseFloat(item.totalPrice || 0);
//   }, 0);
//   vendorForm.value.total_value = total.toLocaleString('en-IN');
// }
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
const toAmount = (v) => {
  if (typeof v === 'number') return v;
  if (v == null) return 0;
  const n = String(v).replace(/[^\d.-]/g, ''); // remove ₹, commas, spaces
  const num = parseFloat(n);
  return Number.isFinite(num) ? num : 0;
};

// Assign L1/L2/L3... (lowest total_value = L1)
// NOTE: this does NOT reorder the table, it only sets vendor.rank.
const recomputeRanks = () => {
  // Keep original object references, sort by normalized total
  const sorted = [...vendorDetails.value]
    .map(v => ({ v, amt: toAmount(v.total_value) }))
    .sort((a, b) => a.amt - b.amt);

  // Simple ranks (no tie handling)
  sorted.forEach((entry, idx) => {
    entry.v.rank = `L${idx + 1}`;
  });
};

// Re-run whenever anything inside vendorDetails changes
watch(
  vendorDetails,
  () => {
    recomputeRanks();
  },
  { deep: true, immediate: true }
);
function saveVendorDetails() {

  calculateVendorTotal(); // Update vendorForm.value.total first
  // console.log(vendorForm.value, "[[[]]]");
  if (!vendorForm.value.vendor_name?.trim()) {
    showInfo("Vendor name is required.");
    return;
  }
  // if (!vendorForm.value.gst_number?.trim()) {
  //   showInfo("GST number is required.");
  //   return;
  // }
  // if (!vendorForm.value.phone_number?.trim()) {
  //   showInfo("Phone number is required.");
  //   return;
  // }
  // if (!vendorForm.value.mail_id?.trim()) {
  //   showInfo("Email is required.");
  //   return;
  // }
  // if (!vendorForm.value.ezy_item_details?.length) {
  //   showInfo("Please add at least one item detail.");
  //   return;
  // } 
  const vendorData = {
    vendor_name: vendorForm.value.vendor_name,
    gst_number: vendorForm.value.gst_number,
    phone_number: vendorForm.value.phone_number,
    mail_id: vendorForm.value.mail_id,
    rank: vendorForm.value.rank,
    // transport: vendorForm.value.transport,
    delivery_time: vendorForm.value.delivery_time,
    payment_terms: vendorForm.value.payment_terms,
    remark: vendorForm.value.remark,
    ezy_item_details: JSON.parse(JSON.stringify(vendorForm.value.ezy_item_details)),
    total_value: vendorForm.value.total_value,
    address: vendorForm.value.address,
    attachments: vendorForm.value.attachments,  // Ensure attachments is always an array
    cgst_percent: vendorForm.value.cgst_percent,
    cgst_amount: vendorForm.value.cgst_amount,
    utgst_percent: vendorForm.value.utgst_percent,
    utgst_amount: vendorForm.value.utgst_amount,
    igst_percent: vendorForm.value.igst_percent ? vendorForm.value.igst_percent : "0",
    igst_amount: vendorForm.value.igst_amount,
    transportation_charges: vendorForm.value.transportation_charges,
    transportation_cgst_percent: vendorForm.value.transportation_cgst_percent,
    transportation_cgst_amount: vendorForm.value.transportation_cgst_amount,
    transportation_utgst_percent: vendorForm.value.transportation_utgst_percent,
    transportation_utgst_amount: vendorForm.value.transportation_utgst_amount,
    transportation_igst_percent: vendorForm.value.transportation_igst_percent,
    transportation_igst_amount: vendorForm.value.transportation_igst_amount,
    transportation_total_amount: vendorForm.value.transportation_total_amount,
    additional_charges: vendorForm.value.additional_charges,

    grand_total: vendorForm.value.grand_total,

  };
  console.log(vendorData, "vendorData");

  if (editingVendorIndex.value !== null) {
    // Update the existing vendor at the correct index
    vendorDetails.value[editingVendorIndex.value] = {
      ...vendorDetails.value[editingVendorIndex.value],
      ...vendorData
    };
  } else {
    // New vendor
    // vendorData.rank = vendorDetails.value.length + 1;
    vendorDetails.value.push(vendorData);
  }


  // if (!vendorMasterList.value.some(vendor => vendor.gst_number === vendorForm.value.gst_number)) {

  //   let MasterVendor = {
  //     vendor_name: vendorForm.value.vendor_name,
  //     mail_id: vendorForm.value.mail_id,
  //     contact_number: vendorForm.value.phone_number,
  //     gst_number: vendorForm.value.gst_number,
  //     address: vendorForm.value.address,
  //   }
  //   console.log(MasterVendor, "api");
  //   axiosInstance.post(apis.resource + doctypes.ezyVendors, MasterVendor)
  //     .then(response => {
  //       console.log('Vendor saved successfully:', response.data);
  //       showSuccess('Vendor details saved successfully!');
  //     })
  //     .catch(error => {
  //       console.error('Error saving vendor:', error);
  //       showError('Failed to save vendor details.');
  //     });
  // }


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
  editingItemIndex.value = null;
  backupItem.value = {};
  calculateVendorTotal();
  calculateTaxes()
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
    item_gst: '0.00',
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

function getVendorItemTotal(vendor, itemName) {
  const item = vendor.ezy_item_details?.find(i => i.item_name === itemName);
  return item ? item.totalPrice : '0.00';
}

function getVendorItemPrice(vendor, itemName) {

  const item = vendor.ezy_item_details?.find(i => i.item_name === itemName);
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



// const filterVendors = () => {
//   const search = vendorForm.value.gst_number;

//   if (search.length === 0) {
//     filteredVendorOptions.value = [];

//     // Reset all fields in vendorForm when vendor_name is cleared
//     vendorForm.value = {
//       vendor_name: '',
//       gst_number: '',
//       phone_number: '',
//       mail_id: '',
//       address: '',
//       // If you have ezy_item_details or other fields, include them here too
//       ezy_item_details: [], 
//       selected: false,
//     };

//     return;
//   }

//   filteredVendorOptions.value = vendorMasterList.value.filter(vendor =>
//     vendor.gst_number.toLowerCase().includes(search)
//   );
// };

const clearVendorForm = () => {
  vendorForm.value = {
    ...vendorForm.value, // keep existing properties like ezy_item_details
    vendor_name: '',
    gst_number: '',
    phone_number: '',
    mail_id: '',
    address: '',
    selected: false,
  };
  filteredVendorOptions.value = [];
};

const filterVendors = () => {
  const search = vendorForm.value.gst_number;

  if (!search || search.trim().length === 0) {
    filteredVendorOptions.value = [];
    clearVendorForm();

    return;
  }

  filteredVendorOptions.value = vendorMasterList.value.filter(vendor =>
    vendor.gst_number.toLowerCase().includes(search.toLowerCase())
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
const editingItem = ref(null);

const openItemModalMaster = (type, item = null, index = null) => {
  modalType.value = type;

  if (type === "edit" && item) {
    newItem.value = { 
      name: item.item_name, 
      unit: item.item_unit_of_measure 
    };
    editingItem.value = item; // 👈 store the full item
  } else {
    newItem.value = { name: "", unit: "" };
    editingItem.value = null;
  }

  const modal = new bootstrap.Modal(document.getElementById("NewItemModalMaster"));
  modal.show();
};

const saveItemMaster = () => {
  if (!newItem.value.name || !newItem.value.unit) return;

  const newItemObj = {
    item_name: newItem.value.name,
    item_unit_of_measure: newItem.value.unit,
  };

  // CREATE
  if (modalType.value === "create") {
    axiosInstance
      .post(apis.resource + doctypes.ezyItems, newItemObj)
      .then(() => {
        showSuccess("New item added successfully!");
        const modal = bootstrap.Modal.getInstance(document.getElementById("NewItemModalMaster"));
        modal.hide();
        newItem.value = { name: "", unit: "" };
        fetchingItemsList();
      })
      .catch((error) => console.error("Error adding new item:", error));
  }

  // EDIT
  else if (modalType.value === "edit" && editingItem.value) {
    console.log(editingItem.value);
    axiosInstance
      .put(
        `${apis.resource + doctypes.ezyItems}/${editingItem.value.name}`, // 👈 Frappe document name
        newItemObj
      )
      .then(() => {
        showSuccess("Item updated successfully!");
        const modal = bootstrap.Modal.getInstance(document.getElementById("NewItemModalMaster"));
        modal.hide();
        newItem.value = { name: "", unit: "" };
        fetchingItemsList();
      })
      .catch((error) => console.error("Error updating item:", error));
  }
};

const deleteMasterItem = (item, index) => {
  if (!confirm(`Are you sure you want to delete "${item.item_name}"?`)) return;

  // Call your backend API to delete
  axiosInstance.delete(`${apis.resource + doctypes.ezyItems}/${item.name}`)
    .then(() => {
      showSuccess(`Item "${item.item_name}" deleted successfully!`);
      // Remove from local list without refetching (optional)
      availableItems.value.splice(index, 1);
    })
    .catch(err => {
      console.error('Error deleting item:', err);
      showError('Failed to delete item.');
    });
};


function fetchingItemsList() {
  let queryParams = {
    fields: JSON.stringify(['item_name', 'item_unit_of_measure','name']),
    limit_page_length: 'None'
  }
  axiosInstance.get(apis.resource + doctypes.ezyItems, { params: queryParams })
    .then(response => {
      availableItems.value = response.data.map(item => ({
        item_name: item.item_name,
        item_unit_of_measure: item.item_unit_of_measure,
        name:item.name,
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
    .get(apis.resource + doctypes.wfRoadmap + `/${employeeData.value.company_field}_${'VENDOR_COMPARISON'}`)
    .then((response) => {
      WfroleMatrix();
      const wfData = response.data;
      if (!wfData || !Array.isArray(wfData.wf_level_setup)) return;

      // Group levels by their "level" number
      const groupedLevels = {};

      wfData.wf_level_setup.forEach((level) => {
        const lvl = level.level || 0;

        if (!groupedLevels[lvl]) {
          groupedLevels[lvl] = {
            id: level.name || lvl,
            designation: [],
            onReject: '',
            level: lvl
          };
        }

        if (level.role) {
          groupedLevels[lvl].designation.push(level.role);
        }

        // Handle onReject mapping (convert index to designation)
        const rejectIdx = level.on_rejection - 1;
        if (rejectIdx >= 0 && wfData.wf_level_setup[rejectIdx]) {
          groupedLevels[lvl].onReject = wfData.wf_level_setup[rejectIdx].role || '';
        }
      });

      workflowApprovalLevels.value = Object.values(groupedLevels);
    })
    .catch((error) => {
      console.error('Error fetching workflow:', error);
      showError('Failed to fetch workflow.');
    });
}

function WfroleMatrix() {

  axiosInstance
    .get(apis.resource + doctypes.WFRoleMatrix + `/${employeeData.value.company_field}`)
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


function getWorkflowRequest() {
  axiosInstance
    .get(apis.resource + doctypes.WFWorkflowRequests + `/${route.query.selectedFormId}`)
    .then((res) => {
      if (res.data) {
        console.log(res.data.reference_id[0].doctype_name_wf);
        axiosInstance
          .get(apis.resource + `${res.data.doctype_name}` + `/${res.data.reference_id[0].doctype_name_wf}`)
          .then((res) => {
            if (res.data) {
              console.log(res.data);

              // assign vendor details
              vendorDetails.value = res.data.vendor_details;
              console.log("Vendor Details:", vendorDetails.value);

              // parse pricing_details for each vendor
              const parsedData = res.data.vendor_details.map((vendor) => {
                return {
                  ...vendor,
                  pricing_details: JSON.parse(vendor.pricing_details),
                };
              });

              let allItems = parsedData.flatMap(vendor => vendor.pricing_details);

              // ✅ Deduplicate based on vendor_name + item_name
              const uniqueItemsMap = new Map();
              allItems.forEach(item => {
                const key = `${item.vendor_name}-${item.item_name}`;
                if (!uniqueItemsMap.has(key)) {
                  uniqueItemsMap.set(key, item);
                }
              });

              itemDetails.value = Array.from(uniqueItemsMap.values());

              console.log("Ezy Items:", res.data.ezy_item_details, "0000");
              console.log("Parsed Vendor Data:", parsedData);
            }
          })
          .catch((error) => {
            console.error("Error fetching workflow request data:", error);
          });
      }
    })
    .catch((error) => {
      console.error("Error fetching workflow request data:", error);
    })
}
function fetchExpenseCodes() {
  const params = {
    limit_page_length: "None",
  };
  axiosInstance
    .get(apis.resource + doctypes.ExpenseCodes, { params })
    .then((response) => {
      if (response.data) {
        // console.log(response.data, "Expense Codes");
        expenseCodeOptions.value = response.data.map((item) => (
           item.name
        ));
      }
    })
    .catch((error) => {
      console.error("Error fetching expense codes:", error);
    });
}
function fetchCostCenters() {
  axiosInstance
    .get(apis.resource + doctypes.CostCenter)
    .then((response) => {
      if (response.data) {
        // console.log(response.data, "Cost Centers");
        costCenterOptions.value = response.data.map((item) => ( item.name ));
      }
    })
    .catch((error) => {
      console.error("Error fetching cost centers:", error);
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

.vendor-details {
  max-height: 80vh;
  overflow-y: scroll;
  overflow-x: hidden;
  padding: 5px;
}

.item-table thead tr:first-child th:first-child {
  border-top-left-radius: 2px;
  border: 1px solid #EEEEEE
}

.item-table thead tr:first-child th:last-child {
  border-top-right-radius: 2px;
  border: 1px solid #EEEEEE
}


.item-table tbody tr:last-child td:first-child {
  border-bottom-left-radius: 2px;
  border: 1px solid #EEEEEE
}

.item-table tbody tr:last-child td:last-child {
  border-bottom-right-radius: 2px;
  border: 1px solid #EEEEEE
}

.vendor-table thead tr:first-child th:first-child {
  border-top-left-radius: 2px;
  border: 1px solid #EEEEEE
}

.vendor-table thead tr:first-child th:last-child {
  border-top-right-radius: 2px;
  border: 1px solid #EEEEEE
}


.vendor-table tbody tr:last-child td:first-child {
  border-bottom-left-radius: 2px;
  border: 1px solid #EEEEEE
}

.vendor-table tbody tr:last-child td:last-child {
  border-bottom-right-radius: 2px;
  border: 1px solid #EEEEEE
}

.vendor-table {
  border: 1px solid #EEEEEE;

}

.vendor-table thead th {
  font-weight: bold;
}

.preview_table {
  border-collapse: separate !important;
  border-spacing: 0;
  border-radius: 5px;
  overflow: hidden;
  border: 1px solid rgb(197, 197, 197);
  /* Outer border only */
}

.preview_table th,
.preview_table td {
  border: none;
  /* Remove double borders */
  border-right: 1px solid rgb(197, 197, 197);
  border-bottom: 1px solid rgb(197, 197, 197);
}

/* Remove the last right/bottom borders so it doesn't double the outer border */
.preview_table tr th:last-child,
.preview_table tr td:last-child {
  border-right: none;
}

.preview_table tbody tr:last-child td {
  border-bottom: none;
}

.main-accordion {
  box-shadow: 2px 3px 4px 0px #0000000D;

  box-shadow: -2px -3px 14px 0px #0000000D;

}

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
.item-table {
  border: 1px solid #EEEEEE;
}

.item-table thead tr th {
  background-color: #F7F7F7;
  border: 1px solid #EEEEEE;
  padding: 10px;
  text-align: left;
  vertical-align: middle;
  border-top: none;
  border-bottom: none;
}

.item-table tbody tr td {

  border: 1px solid #EEEEEE;
  padding: 10px;
  text-align: left;
  vertical-align: middle;

}

// .main-div {
//   height: 80vh;

// } 

.vendor-table thead tr th {
  background-color: #F7F7F7;
  border: 1px solid #EEEEEE;
  padding: 4px;
  text-align: left;
  vertical-align: middle;
  border-top: none;
  border-bottom: none;
}

.vendor-table tbody tr td {

  border: 1px solid #EEEEEE;
  padding: 10px;
  text-align: left;
  vertical-align: middle;

}

.table th {
  color: #666666;
  font-weight: 500;
  font-size: 13px;
}

.table td {
  color: #000000;
  font-weight: 400;
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
  font-size: 14px;
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
  margin-bottom: 2px;

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
  position: relative;
  font-weight: 500;
  color: #6c757d;
  font-size: 14px;
  transition: color 0.25s ease;
}

/* Underline animation */
.step-item::after {
  content: "";
  position: absolute;
  left: 0;
  right: 0;
  bottom: -2px;
  height: 4px;
  background: #dc3545;
  transform: scaleX(0);
  transform-origin: left center;
  transition: transform 0.25s ease;
}

.step-item i {
  font-size: 16px;
  // margin-right: 5px;
}

.step-item.active {
  color: #dc3545;
}

.step-item.active::after {
  transform: scaleX(1);
}

.step-item.completed {
  color: #000;
}

.check-icon {
  color: #14df22;
  font-size: 16px;

}

/* Icon fade animation */
.icon-fade-enter-active,
.icon-fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.icon-fade-enter-from,
.icon-fade-leave-to {
  opacity: 0;
  transform: translateY(2px);
}

.add-approver-row {
  background-color: #F5F6FF;

}

.add-approver-row button {
  font-size: 12px;
  padding: 5px 10px;
  color: #dc3545;
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
  color: #dc3545;
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
  background-color: #fff5f5;
}

.workflow-footer button {
  font-size: 13px;
  padding: 5px 10px;
  color: #dc3545;
  font-weight: 600;
}

.next-Submit {
  background-color: #dc3545;
  color: #fff;
  font-weight: 600;
  font-size: 14px;
  padding: 8px 16px;
  border-radius: 10px;
}

.next-Submit:hover {
  background-color: #dc3545;
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

.not-allowed {
  cursor: not-allowed;
  // opacity: 0;
}

/* Scope only inside the workflow table */
.workflow-container .vue-select .vs__selected {
  background: #f1f3f5;
  border: 1px solid #dee2e6;
  border-radius: 16px;
  padding: 2px 8px;
  font-size: 12px;
  color: #495057;
  display: flex;
  align-items: center;
  gap: 4px;
  height: auto;
  /* no fixed height */
}

.workflow-container .vue-select .vs__selected-options {
  display: flex;
  flex-wrap: wrap;
  /* allow multiple rows */
  gap: 4px;
}

.workflow-container .vue-select .vs__deselect {
  font-size: 14px;
  margin-left: 4px;
  color: #6c757d;
}

.workflow-container .vue-select .vs__dropdown-toggle {
  // min-height: 36px; /* match row height */
  border-radius: 6px;
  height: auto !important;
}

.editable-row {
  color: #000;
  font-weight: normal;
}

/* Fade + slide animation */
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: opacity 0.3s ease, transform 0.3s ease;
}

.fade-slide-enter-from {
  opacity: 0;
  transform: translateY(10px);
}

.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

// /* Change dropdown selected item background */
// :deep(.vs__dropdown-option--selected) {
//   background-color: #ffefc1 !important; /* light yellow background */
//   color: #333 !important; /* text color */
// }

// /* Also change hover color for better UX */
// :deep(.vs__dropdown-option--highlight) {
//   background-color: #ffe18a !important; /* hover background */
//   color: #000 !important;
// } 
:deep(.vs__selected) {
  background: #f1f3f5;
  border: 1px solid #dee2e6;
  border-radius: 16px;
  padding: 0px 8px;
  font-size: 12px;

}

:deep(.vs__selected-options) {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
  padding: 5px;
}

:deep(.vs__dropdown-toggle) {
  height: auto !important;
}


:deep(.vs__deselect) svg {
  color: #555;
  margin-left: 4px;
  margin-top: 2px;
  font-size: 10px !important;
  height: 15px;
}

:deep(.vs__deselect:hover) {
  color: #000;
}

.main_back {
  background-color: #f8f9fa;
  box-shadow: rgba(0, 0, 0, 0.1) 0px 3px 3px -3px, rgba(0, 0, 0, 0.05) 0px 4px 6px -2px;

  padding: 0.6rem;
  position: sticky;
  top: 0;
  z-index: 10;


}

.work_order_card {
  // border: 1px solid #dee2e6;
  // border-radius: 0.25rem;
  padding: 0.5rem;
  box-shadow: 2px 3px 4px 0px #0000000D;

  box-shadow: -2px -3px 14px 0px #0000000D;
}

.nav-link {
  // border-bottom: 2px solid transparent;
  border-left: 5px solid transparent;

  color: #333;
  text-align: left;
  font-size: 13px;
  width: 100%;
}

.nav-link.active {
  // border-bottom: 2px solid red;
  border-left: 5px solid #DC3E45;
  color: red !important;
  font-weight: 600;
  background-color: var(--white-color);
}

// .vendor_sidebar ul li{
//   padding: 8px 12px;

//   font-size: 13px;
// }
.vendor_sidebar {
  height: 90dvh;
  background-color: #FAFAFA !important;
  padding-top: 12px;
  border-radius: 10px;
  overflow-y: auto;
  overflow-x: hidden;
}
.bi-pencil-fill{
  cursor: pointer;
}
.bi-trash-fill{
 cursor: pointer;
}
</style>
