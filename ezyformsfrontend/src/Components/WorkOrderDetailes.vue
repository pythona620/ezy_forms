<template>
  <div class="container-fluid">
    <div class=" p-3">
      
      <div class="d-flex justify-content-between align-items-center back_div mb-2">
                <div><button class="font-12 m-0 btn" @click="router.back()"> <i class="bi bi-chevron-left"></i> Back</button></div>
                <div>
                  <button class="btn btn-outline-secondary btn-sm me-2" @click="previewComparison">Preview
                    comparison</button>
                  <button class="btn btn-secondary btn-sm" @click="submitComparison">Submit comparison</button>
                </div>
              </div>

      <div class="accordion " id="accordionExample">
        <!-- Item Details Accordion -->
        <div class="accordion-item">
          <h2 class="accordion-header">
            <button class="accordion-button" type="button" data-bs-toggle="collapse" data-bs-target="#collapseItems"
              aria-expanded="true">
              Item details
            </button>
          </h2>
          <div id="collapseItems" class="accordion-collapse collapse show">
            <div class="accordion-body">
              
              <table class="table table-bordered shadow rounded-table">
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
                    <td>
                      <template v-if="editingIndex === index">
                        <input v-model="item.name" class="form-control form-control-sm">
                      </template>
                      <template v-else>
                        {{ item.name }}
                      </template>
                    </td>
                    <td>
                      <template v-if="editingIndex === index">
                        <input v-model="item.unit" class="form-control form-control-sm">
                      </template>
                      <template v-else>
                        {{ item.unit }}
                      </template>
                    </td>
                    <td>
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
                        <i class="bi bi-pencil-square me-2" @click="editItem(index)"></i>
                        <i class="bi bi-trash" @click="deleteItem(index)"></i>
                      </template>
                    </td>
                  </tr>
                </tbody>
              </table>

              <div>
                <button  class="btn btn-danger btn-sm" @click="deleteSelectedItems"><i class="bi bi-trash"></i> Delete Item</button>
                <button class="btn btn-outline-secondary btn-sm ms-2" @click="addItem">+ Add Item</button>
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
             

              <table class="table table-bordered shadow rounded-table">
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
                    <td>{{ vendor.rank }}</td>
                    <td>{{ vendor.name }}</td>
                    <td>{{ vendor.gst }}</td>
                    <td>{{ vendor.contact }}</td>
                    <td>{{ vendor.email }}</td>
                    <td>{{ vendor.totalValue }}</td>
                    <td>
                      <i class="bi bi-pencil-square" @click="openVendorModal(index)"></i>
                    </td>
                  </tr>
                </tbody>
              </table>

              <div>
                <button class="btn btn-danger btn-sm" @click="deleteSelectedVendors"><i class="bi bi-trash"></i> Delete Vendor</button>
                <button class="btn btn-outline-secondary btn-sm ms-2" @click="addVendorModal">+ Add Vendor</button>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Vendor Edit Modal -->
      <div class="modal fade" id="vendorModal" tabindex="-1">
        <div class="modal-dialog modal-xl">
          <div class="modal-content p-4">
            <div class="d-flex justify-content-between mb-3">
              <h6 class="fw-bold">Editing Row #{{ editingVendorIndex + 1 }}</h6>
              <div>
                <button class="btn btn-outline-danger btn-sm me-2" data-bs-dismiss="modal">Close</button>
                <button class="btn btn-primary save_vendor btn-sm" @click="saveVendorDetails">Save Vendor details</button>
              </div>
            </div>

            <div class="row g-2 mb-3">
              <div class="col-md-3">
                <label class="form-label">Vendor name</label>
                <input v-model="vendorForm.name" class="form-control form-control-sm">
              </div>
              <div class="col-md-3">
                <label class="form-label">GST number</label>
                <input v-model="vendorForm.gst" class="form-control form-control-sm">
              </div>
              <div class="col-md-3">
                <label class="form-label">Phone number</label>
                <input v-model="vendorForm.contact" class="form-control form-control-sm">
              </div>
            </div>
            <div class=" row g-2 mb-3">
              <div class="col-md-6">
                <label class="form-label">Email ID</label>
                <input v-model="vendorForm.email" class="form-control form-control-sm">
              </div>


            <div class="col-md-6">
              <label class="form-label">Attachments</label>
              <input type="file" multiple class="form-control form-control-sm">
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
                  <tr v-for="(item, index) in vendorForm.items" :key="index">
                    <td width="3%"><input type="checkbox" v-model="item.selected"></td>
                    <td>
                      
                        {{ item.name }}
                      
                    </td>
                    <td>
                     
                        {{ item.quantity }}
                    
                    </td>
                   <td @click="editItemInModal(index)">
                      <template v-if="editingItemIndex === index">
                        <input @blur="saveEditedItem" @focus="editItemInModal(index)"
                          v-model.number="item.unitPrice"
                          @change="updateTotalPrice(item)"
                          type="number"
                          class="form-control form-control-sm"
                        >
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
                <input v-model="vendorForm.totalValue" class="form-control form-control-sm" readonly>
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
              <input v-model="vendorForm.remark" class="form-control form-control-sm">
            </div>

          </div>
        </div>
      </div>
    </div>
    <!-- Comparison Modal -->
<div class="modal fade" id="comparisonModal" tabindex="-1">
  <div class="modal-dialog modal-xl">
    <div class="modal-content p-4">
      <div class="d-flex justify-content-between mb-3">
        <h6 class="fw-bold">Preview Comparison</h6>
        <button class="btn btn-outline-danger btn-sm" data-bs-dismiss="modal">Close</button>
      </div>

      <!-- Dynamic Comparison Table -->
      <table class="table table-bordered">
        <thead class="table-light">
          <tr>
            <th>Item name</th>
            <th v-for="vendor in vendorDetails" :key="vendor.name">
              {{ vendor.name }} <span class="text-muted">(rate/unit)</span>
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in itemDetails" :key="item.name">
            <td>
              {{ item.name }} <span class="badge bg-secondary">{{ item.quantity }} {{ item.unit }}</span>
            </td>
            <td v-for="vendor in vendorDetails" :key="vendor.name">
              ₹ {{ getVendorItemPrice(vendor, item.name) }}
            </td>
          </tr>
          <tr>
            <td>Total</td>
            <td v-for="vendor in vendorDetails" :key="vendor.name">
              <b>₹ {{ getVendorTotal(vendor) }}</b> /total qty
            </td>
          </tr>
        </tbody>
      </table>

      <!-- Company Details -->
      <h6 class="mt-4">Company Details</h6>
      <table class="table table-bordered">
        <thead class="table-light">
          <tr>
            <th>Vendor name</th>
            <th>Payment terms</th>
            <th>GST</th>
            <th>Delivery</th>
            <th>Biddle rank</th>
            <th>Transport charges</th>
            <th>Attachments</th>
            <th>Comments</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="vendor in vendorDetails" :key="vendor.name">
            <td>{{ vendor.name }}</td>
            <td>{{ vendor.paymentTerms || '-' }}</td>
            <td>{{ vendor.gst || '-' }}</td>
            <td>{{ vendor.deliveryTime || '-' }}</td>
            <td>{{ vendor.rank }}</td>
            <td>{{ vendor.transport || '-' }}</td>
            <td><span class="text-primary">Preview attachment</span></td>
            <td>{{ vendor.remark || '-' }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</div>

  </div>
</template>

<script setup>
import { watch } from 'vue';
import { ref } from 'vue';
import { useRoute, useRouter} from "vue-router";

const route = useRoute();
const router = useRouter()

const itemDetails = ref([
  { name: 'Computer', unit: 'Unit', quantity: 4, selected: false },
  { name: 'CPU', unit: 'Unit', quantity: 5, selected: false },
  { name: 'Mouse', unit: 'Unit', quantity: 2, selected: false },
  { name: 'Molds', unit: 'Kilogram', quantity: 6, selected: false }
]);

const vendorDetails = ref([
  { rank: 3, name: 'Daniel White Pvt Ltd', gst: '32434567546554', contact: '8697237439', email: 'srinkhasu@gmail.com', totalValue: '', selected: false },
  { rank: 2, name: 'Jane Johnson Pvt Ltd', gst: '2746345345656', contact: '9954354323', email: 'venkat198@gmail.com', totalValue: '', selected: false },
  { rank: 4, name: 'Robert Wilson Pvt Ltd', gst: '330293878240', contact: '9032873873', email: 'Mail1989@gmail.com', totalValue: '', selected: false },
  { rank: 1, name: 'Sophia Martin Pvt Ltd', gst: '1NH762587654', contact: '9819675625', email: 'Badoi197@gmail.com', totalValue: '', selected: false }
]);
 

const editingIndex = ref(null); 
function addVendorModal() {
  vendorForm.value = {
    name: '',
    gst: '',
    contact: '',
    email: '',
    transport: 'Free delivery',
    deliveryTime: '',
    paymentTerms: '',
    rank: 'L1',
    remark: '',
    totalValue:'',
    items: JSON.parse(JSON.stringify(itemDetails.value))  // copy the main itemDetails
  };

  editingVendorIndex.value = null;  // because it's a new vendor
  new bootstrap.Modal(document.getElementById('vendorModal')).show();
}

const submitComparison = () => alert('Submit comparison clicked');
const addItem = () => itemDetails.value.push({ name: 'New Item', unit: 'Unit', quantity: 1, selected: false });
const deleteItem = index => itemDetails.value.splice(index, 1);
const deleteSelectedItems = () => itemDetails.value = itemDetails.value.filter(item => !item.selected);

const editItem = index => {
  editingIndex.value = index;
};

const saveItem = () => {
  editingIndex.value = null;
};

const cancelEdit = () => {
  editingIndex.value = null;
};

function updateTotalPrice(item) {
  const qty = parseFloat(item.quantity || 0);
  const price = parseFloat(item.unitPrice || 0);
  item.totalPrice = (qty * price).toFixed(2);
}

const deleteSelectedVendors = () => vendorDetails.value = vendorDetails.value.filter(vendor => !vendor.selected);


const editingVendorIndex = ref(null);
const vendorForm = ref({
  name: '', gst: '', contact: '', email: '',
  items: [
    { ...itemDetails }
  ],
  transport: 'Free delivery', deliveryTime: '', paymentTerms: '', rank: 'L1', remark: ''
});

function openVendorModal(index) {
  const vendor = vendorDetails.value[index];

  vendorForm.value = {
    name: vendor.name,
    gst: vendor.gst,
    contact: vendor.contact,
    email: vendor.email,
    transport: vendor.transport || 'Free delivery',
    deliveryTime: vendor.deliveryTime || '',
    paymentTerms: vendor.paymentTerms || '',
    rank: vendor.rank || 'L1',
    remark: vendor.remark || '',
    totalValue: vendor.totalValue,
    // Load the vendor's own items (if any), else empty array
    items: vendor.items ? JSON.parse(JSON.stringify(vendor.items)) : JSON.parse(JSON.stringify(itemDetails.value))
  };

  editingVendorIndex.value = index;
  new bootstrap.Modal(document.getElementById('vendorModal')).show();
}
watch(() => vendorForm.value.items, () => {
  calculateVendorTotal();
}, { deep: true });
watch(() => vendorForm.value.items, () => {
  calculateVendorTotal();

  if (editingVendorIndex.value !== null) {
    vendorDetails.value[editingVendorIndex.value].totalValue = vendorForm.value.totalValue;
  }
}, { deep: true });

function calculateVendorTotal() {
  const total = vendorForm.value.items.reduce((sum, item) => {
    return sum + parseFloat(item.totalPrice || 0);
  }, 0);
  vendorForm.value.totalValue = total.toLocaleString('en-IN');
}
function saveVendorDetails() {
  calculateVendorTotal(); // Update vendorForm.value.totalValue first

  const vendorData = {
    name: vendorForm.value.name,
    gst: vendorForm.value.gst,
    contact: vendorForm.value.contact,
    email: vendorForm.value.email,
    rank: vendorForm.value.rank,
    transport: vendorForm.value.transport,
    deliveryTime: vendorForm.value.deliveryTime,
    paymentTerms: vendorForm.value.paymentTerms,
    remark: vendorForm.value.remark,
    items: JSON.parse(JSON.stringify(vendorForm.value.items)),
    totalValue: vendorForm.value.totalValue, // <--- the calculated total value
    selected: false
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

  bootstrap.Modal.getInstance(document.getElementById('vendorModal')).hide();
}


const editingItemIndex = ref(null);
const backupItem = ref({});


// Start editing a row
function editItemInModal(index) {
  editingItemIndex.value = index;
  // Backup the current data
  backupItem.value = { ...vendorForm.value.items[index] };
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
  vendorForm.value.items.push({
    name: 'New Item',
    quantity: 1,
    unitPrice: '0.00',
    totalPrice: '0.00',
    selected: false,
  });
}

function deleteChildItem(index) {
  vendorForm.value.items.splice(index, 1);
}

function deleteSelectedChildItems() {
  vendorForm.value.items = vendorForm.value.items.filter(item => !item.selected);
}


function getVendorItemPrice(vendor, itemName) {
  const item = vendor.items?.find(i => i.name === itemName);
  return item ? item.unitPrice : '0.00';
}

function getVendorTotal(vendor) {
  const total = vendor.items?.reduce((sum, item) => sum + parseFloat(item.totalPrice || 0), 0);
  return total ? total.toLocaleString('en-IN') : '0.00';
}


function previewComparison() {
  new bootstrap.Modal(document.getElementById('comparisonModal')).show();
}

</script>

<style lang="scss" scoped>

/* Add rounded corners to the entire table */
.table {
  // border-collapse: separate;
  // border-spacing: 0;
  border-radius: 8px;
  overflow: hidden;
}

/* Optional: Add rounded corners to the top header row */
.table thead tr:first-child th:first-child {
  border-top-left-radius: 8px;
}

.table thead tr:first-child th:last-child {
  border-top-right-radius: 8px;
}

/* Optional: Add rounded corners to the bottom row */
.table tbody tr:last-child td:first-child {
  border-bottom-left-radius: 8px;
}

.table tbody tr:last-child td:last-child {
  border-bottom-right-radius: 8px;
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
.table th {
  color: #666666;
  font-weight: 500;
  font-size: 13px;
}
.table td{
  color: #000000;
  font-weight: 500;
  font-size: 13px;
}
.btn-danger{
  border-radius:6px ;
  font-size: 11px;
}
.accordion-button.collapsed {
  background-color: #fff;
  box-shadow: none; /* Optional: remove the default shadow */
  font-size: 14px;
  color: #000;
}
.accordion-button {
  background-color: #fff; /* light background when expanded, adjust as needed */
  height: 50px;
}
.accordion-button:focus{
  box-shadow: none;

}
.accordion-button:not(.collapsed) {
  background-color: #fff; /* or any color you prefer */
  color: #333333;            /* optional: adjust text color */
}

/* Collapsed state */
.accordion-button.collapsed {
  background-color: #fff !important;
  color: #666666;            /* optional: adjust text color when collapsed */
  box-shadow: none;          /* optional: remove the Bootstrap box-shadow */
}
/* Adjust spacing, if required */
.bi-pencil-square{
  font-size: 12px;
  cursor: pointer;
}
.form-control{
  border-radius: 10px;
  font-size: 12px;
}
.form-label{
font-size: 12px;
}
.save_vendor{
  background-color: #1B14DF !important;
}
.form-select{
    border-radius: 10px;
  font-size: 12px;
}
.btn-outline-secondary{
  font-size: 12px !important;
}
.accordion{
  box-shadow: 2px 3px 4px 0px #0000000D;
box-shadow: -2px -3px 14px 0px #0000000D;

}
.back_div{
  background-color: #FAFAFA;
  padding: 5px;
  border-radius: 6px;
}

</style>
