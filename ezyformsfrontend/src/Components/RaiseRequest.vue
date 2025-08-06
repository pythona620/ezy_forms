<template>
  <div>
    <div class="backtofromPage py-2">
      <router-link :to="backTo" @click="backToForm" class="text-decoration-none text-dark  ps-3 font-13"><span> <i
            class="bi bi-arrow-left pe-2"></i></span>Back</router-link>
    </div>
    <div class="container">
      <div v-if="blockArr.length" class="position-relative">
        <div class="requestPreviewDiv" ref="mainBlockRef">
          <div>
            <!-- Open Modal -->
            <!-- <button class="btn btn-outline-secondary" @click="openModal">Open Modal</button> -->

            <!-- Modal -->
            <div v-if="showModal" class="modal d-block " tabindex="-1">
              <div class="modal-dialog">
                <div class="modal-content">

                  <!-- Header -->
                  <div class="modal-header">
                    <h5 class="modal-title">Select Form</h5>
                    <button type="button" class="btn-close" @click="showModal = false"></button>
                  </div>

                  <!-- Body -->
                  <div class="modal-body ">
                    <div class="position-relative ">
                      <input type="text" class="form-control mb-2" v-model="searchQuery"
                        placeholder="Search and select form..." @input="fetchDepartmentDetails"
                        @focus="showDropdown = true" @blur="hideDropdownWithDelay" />

                      <ul v-if="showDropdown && formOptions.length"
                        class="list-group position-absolute w-100 zindex-dropdown">
                        <li v-for="option in formOptions" :key="option.value"
                          class="list-group-item list-group-item-action font-12"
                          @mousedown.prevent="selectOption(option)">
                          {{ option.label }}
                        </li>
                      </ul>
                    </div>

                  </div>

                  <!-- Footer -->
                  <div class="modal-footer">
                    <button class="btn btn-dark" @click="toSelectedFormRaise">Raise</button>
                  </div>

                </div>
              </div>
            </div>
          </div>
          <RequestPreview :blockArr="blockArr" :formName="selectedData.selectedform" :tableHeaders="tableHeaders"  ref="childRef"
            :linked_id="linkedId" :LinkedChildTableData="LinkedChildTableData" @updateField="handleFieldUpdate" @updateRemovedFiles="handleRemovedFiles"
            :tableRowsdata="tableRows" @formValidation="isFormValid = $event" @updateTableData="handleTableData" />
          <!-- @formValidation="isFormValid = $event" -->

          <!-- <span class="font-13 fw-bold">{{ table.childTableName.replace(/_/g, " ") }}</span> -->
          <!-- <div v-if="!tableHeaders" class="mt-3">
            <div v-for="(table, tableIndex) in tableHeaders" :key="tableIndex" class="mt-3">
              <div>
                <span class="font-13 fw-bold">{{ tableIndex.replace(/_/g, " ") }}</span>
              </div>

              <table class="table table-striped" border="1" width="100%">
                <thead>
                  <tr>
                    <th>#</th>
                    <th v-for="field in table" :key="field.fieldname">
                      {{ field.label }}
                    </th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="(row, rowIndex) in tableRows[tableIndex]" :key="rowIndex">
                    <td style="text-align: center;">{{ rowIndex + 1 }}</td>
                    <td v-for="field in table" :key="field.fieldname">
                      <template v-if="field.fieldtype === 'Data'">
                        <input type="text" class="form-control font-12" v-model="row[field.fieldname]" />
                      </template>
<template v-if="field.fieldtype === 'Date'">
                        <input type="date" class="form-control font-12" v-model="row[field.fieldname]" />
                      </template>
<template v-if="field.fieldtype === 'Datetime'">
                        <input type="datetime-local" class="form-control font-12" v-model="row[field.fieldname]" />
                      </template>
<template v-else-if="field.fieldtype === 'Attach'">
                        <input type="file" class="form-control font-12"
                          @change="handleFileUpload($event, row, field.fieldname)" />
                      </template>
</td>
<td>
  <span @click="removeRow(tableIndex, rowIndex)"><i class="bi bi-x-lg"></i></span>
</td>
</tr>
</tbody>
</table>

<button class="btn btn-light font-12" @click="addRow(tableIndex)">Add Row</button>
</div>
</div> -->


        </div>
        <!-- @formValidation="isFormValid = $event" -->
        <div class="raiserequestBtnDiv">
          <div class="d-flex justify-content-end align-items-center gap-2 p-3">
            <button v-if="!selectedData.selectedFormId" class="btn btn-white font-13" @click="clearFrom">
              <span> <i class="bi bi-x"></i></span>Clear form
            </button>
            <!-- :disabled="!isFormValid" -->
            <button v-if="!selectedData.selectedFormId"  @click="toRaiseReqBtn"
              class="btn btn-dark font-12" type="submit">
              {{ selectedData.hasWorkflow == 'No' ? 'Save' : 'Raise Request' }}
            </button>
            <!-- <button  class="btn btn-dark font-12" type="submit"
              @click="raiseRequestSubmission">
              {{ selectedData.hasWorkflow == 'No' ? 'Save' : 'Raise Request' }}
            </button> -->
            <!-- <button v-if="selectedData.selectedFormId && $route.query.selectedFormStatus == 'Request Cancelled'"
              @click="RequestUpdate" class="btn btn-dark font-12" type="submit">
              Update Request
            </button> -->
           <button
  v-if="$route.query.selectedFormStatus && ($route.query.selectedFormStatus == 'Request Raised' || $route.query.selectedFormStatus == 'Request Cancelled')"
  @click="EditRequestUpdate"
  class="btn btn-dark font-12"
  type="submit"
>
  Update Request
</button>


          </div>
        </div>
      </div>
      <div v-else>
        <div class="no-form">No Form</div>
      </div>
    </div>
    <!-- :class="{'z-1':saveloading}" -->
    <div class="modal fade " id="ExportEmployeeModal" data-bs-backdrop="static"  tabindex="-1" aria-hidden="true" >
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Acknowledgement</h5>
            <button type="button" class="btn-close" @click="acknowledge=''" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <input type="checkbox" v-model="acknowledge" id="Acknowledgement" value="Acknowledgement" class="me-2 mt-1 form-check-input Acknowledgement-check " />
            <label for="Acknowledgement">

            I acknowledge that the information provided is correct.
            </label>
          </div>
          <div class="modal-footer">
            <button type="button" @click="acknowledge=''" class="btn btn-outline-secondary font-12" data-bs-dismiss="modal">Cancel</button>
           <button
              type="button"
              class="btn btn-dark"
              style="min-width: 120px;"  
              :disabled="!acknowledge || saveloading"
              @click="raiseRequestSubmission"
            >
              <span v-if="saveloading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              <span v-else class="font-12 fw-bold">Yes, Proceed</span>
            </button>

          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch, nextTick } from "vue";
import { apis, doctypes, domain } from "../shared/apiurls";
import RequestPreview from "./RequestPreview.vue";
import Multiselect from "@vueform/multiselect";
import "@vueform/multiselect/themes/default.css";
import { rebuildToStructuredArray } from "../shared/services/field_format";
import axiosInstance from "../shared/services/interceptor";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
// import { EzyBusinessUnit } from "../shared/services/business_unit";
import { useRoute, useRouter } from "vue-router";

const router = useRouter();
const route = useRoute(); // Get query params from route

//  Extract query parameters from URL
const selectedData = ref({
  routepath: route.query.routepath || "",
  selectedCategory: route.query.selectedCategory || "", // Retrieve from query
  selectedform: route.query.selectedForm || "", // Retrieve from query
  selectedFormId: route.query.selectedFormId || "", // Retrieve from query
  selectedBusiness_unit: route.query.business_unit || "", // Retrieve from query
  hasWorkflow: route.query.has_workflow || "", // Retrieve from query
  linkedDocName: route.query.linkedForm || "", // Retrieve from query
  main_form_Id: route.query.main_form_Id || "", // Retrieve from query
  type: route.query.type || "", // Retrieve from query
  main_form: route.query.main_form || "", // Retrieve from query
});

const retun_id_from_linked_doc = ref("");
const acknowledge = ref('')
const saveloading = ref(false)
const business_unit = ref(localStorage.getItem('Bu')); // Retrieve from query
const isFormValid = ref(false);
// const isFormValid = computed(() => allFieldsFilled.value);
const blockArr = ref([]);
const categoryOptions = ref([]);
const employeeData = ref({});
const formList = ref([]);
const emittedFormData = ref([]);
const filepaths = ref([]);
const backTo = ref(selectedData.value.routepath);
const tableRows = ref([]);
const tableHeaders = ref([]);
const childTableName = ref("");
const tableName = ref("");
// const tableKey = ref('');
// const responseData = ref([]);
// const childIDs = ref("");
const mainBlockRef = ref("");
const childtablesData = ref({});
const filterObj = ref({
  limit_start: 0,
  limitPageLength: 100,
});
const newMainId = ref('')
const checkingIs_linked = ref([]);
const is_linked_form = ref("");
const LinkedChildTableData = ref([]);
function backToForm() {
  blockArr.value = [];
  router.push({
    path: selectedData.value.routepath,
    query: {

      routepath: '/todo/raisedbyme',
      doctype_name: route.query.main_form,
      business_unit: selectedData.value.selectedBusiness_unit,
      name: selectedData.value.main_form_Id,
      type: selectedData.value.type,
    },
  });
}

const ip_address = ref(null)

const getClientIP = async () => {
  try {
    const response = await fetch('https://api.ipify.org?format=json')
    const data = await response.json()
    ip_address.value = data.ip
    // console.log("ip_address.value", ip_address.value);

  } catch (error) {
    console.error('Error fetching IP:', error)
  }
}



onMounted(() => {
  loadInitialData();
  // console.log(route.query);
});

const loadInitialData = () => {
  if (selectedData.value.main_form_Id) {
    gettingDataToLink();
  }
  getClientIP()
  formDefinations();
  const storedData = localStorage.getItem("employeeData");
  if (storedData) {
    employeeData.value = JSON.parse(storedData);
    // console.log("employeeData======================",employeeData.value);
  }

  // raiseRequest();
};

watch(business_unit, (newBu, oldBu) => {
  console.log(newBu);

  if (oldBu) {
    deptData(true);
  } else {
    deptData();
  }
});
const showModal = ref(false)
const showDropdown = ref(false)
const searchQuery = ref('')
const formOptions = ref([])
const selectedFormName = ref('')



function openModal() {
  showModal.value = true
  searchQuery.value = ''
  fetchDepartmentDetails()
}

function hideDropdownWithDelay() {
  setTimeout(() => {
    showDropdown.value = false
  }, 150)
}

function selectOption(option) {
  selectedFormName.value = option.value
  searchQuery.value = option.label
  showDropdown.value = false
}

function fetchDepartmentDetails() {
  const filters = [
    ['business_unit', 'like', `%${selectedData.value.selectedBusiness_unit}%`]
  ]

  if (searchQuery.value.trim()) {
    filters.push(['form_short_name', 'like', `%${searchQuery.value.trim()}%`])

  }

  const queryParams = {
    fields: JSON.stringify(['name', 'form_short_name']), // ✅ Add this field
    limit_page_length: 'None',
    filters: JSON.stringify(filters),
    order_by:
      '`tabEzy Form Definitions`.`enable` DESC, `tabEzy Form Definitions`.`creation` DESC'
  }

  axiosInstance
    .get(`${apis.resource}${doctypes.EzyFormDefinitions}`, { params: queryParams })
    .then((response) => {
      // console.log("API Response:", response) // ✅ check this
      const data = response.data
      formOptions.value = data.map(item => ({
        label: item.form_short_name || item.name,
        value: item.name
      }))
    })

    .catch((error) => {
      console.error('Error fetching department details:', error)
    })
}


function toSelectedFormRaise() {
  router.push({
    name: 'RaiseRequest',
    query: {
      routepath: selectedData.value.routepath,
      selectedForm: selectedFormName.value,
      business_unit: selectedData.value.selectedBusiness_unit
    }
  })


  selectedData.value.selectedform = selectedFormName.value
  formDefinations()
  showModal.value = false
}


function RequestUpdate() {
  // const filesArray = filepaths.value
  //   ? filepaths.value.split(",").map((filePath) => filePath.trim())
  //   : [];
  let form = {};
  if (emittedFormData.value.length) {
    emittedFormData.value.map((each) => {
      form[each.fieldname] = each.value;
    });
  }

  let data_obj = {
    form_id: route.query.selectedFormId,
    updated_fields: form, // Pass the form JSON here
  };

  axiosInstance
    .post(apis.Update_raising_request, data_obj)
    .then((resp) => {
      if (resp?.message?.success) {

        toast.success("Request Raised", {
          autoClose: 2000,
          transition: "zoom",
          onClose: () => {
            router.push({ path: "/todo/raisedbyme" });
          },
        });
      }
    });
}

function updateChildRecords(childTables, child_id_name) {
  let requestData = {};

  // Add each child table and its fields dynamically
  childTables.forEach(({ child_table, child_fields }) => {
    requestData[child_table] = child_fields.map(({ name, ...fields }) => fields);
  });

  axiosInstance
    .put(`${apis.resource}${selectedData.value.selectedform}/${child_id_name}`, requestData)
    .then((response) => {
      // console.log(`Updated Record for All Child Tables:`, response.data);
    })
    .catch((error) => {
      console.error(`Error updating records:`, error);
    });
}

function handleTableData(data) {
  childtablesData.value = data;
  console.log('Updated Table Data:', childtablesData.value);
}

// function EditRequestUpdate() {
//   const validTables = tableName.value.filter((table) => {
//     const childData = tableRows.value[table.options];
//     return childData && childData.length;
//   });
//   console.log("tableName.value==",tableName.value);
//   console.log("tableRows=",tableRows.value);

//   let childTables = [];

//   // Iterate through valid tables and collect their fields
//   validTables.forEach((table) => {
//     const childTableName = table.options;
//     const childFields = tableRows.value[childTableName] || [];

//     childTables.push({
//       child_table: childTableName,
//       child_fields: childFields,
//     });
//   });

//   // console.log(childTables, childTables.length,"Child Tables Data");

//   // Call function to update child records
//   if(childTables.length){
//     updateChildRecords(childTables, child_id_name.value);
//   }


//   let form = {};
//   if (emittedFormData.value.length) {
//     emittedFormData.value.map((each) => {
//       form[each.fieldname] = each.value;
//     });
//   }

//   let data_obj = {
//     form_id: route.query.selectedFormId,
//     updated_fields: form, // Pass the form JSON here

//   };
//   // console.log(data_obj,"lll");

//   axiosInstance
//     .post(apis.edit_form_before_approve, data_obj)
//     .then((resp) => {
//       if (resp?.message?.success) {

//         toast.success("Request Raised", {
//           autoClose: 2000,
//           transition: "zoom",
//           onClose: () => {
//             router.push({ path: "/todo/raisedbyme" });
//           },
//         });
//       }
//     });
// }



function EditRequestUpdate() {
  let form = {};

  // Include normal form fields
  if (emittedFormData.value.length) {
    emittedFormData.value.forEach((each) => {
      form[each.fieldname] = each.value;
    });
  }

  // Dynamically include all child tables
  for (const [childTableKey, childRows] of Object.entries(childtablesData.value)) {
    if (Array.isArray(childRows) && childRows.length) {
      form[childTableKey] = childRows.map(row => ({ ...row }));
    }
  }

  const data_obj = {
    form_id: route.query.selectedFormId,
    updated_fields: form,
    document_type :route.query.selectedForm,
    property: business_unit.value,
    //  status: route.query.selectedFormStatus === 'Request Cancelled' ? 'Request Raised' : null,
    // current_level:route.query.selectedFormStatus === 'Request Cancelled' ? 1 : null
  };
  // console.log(data_obj, "data_obj for EditRequestUpdate");
  axiosInstance.post(apis.edit_form_before_approve, data_obj).then((resp) => {
    if (resp?.message?.success === true) {
    // console.log(resp, "EditRequestUpdate response");
      toast.success(resp.message.message, {
        autoClose: 2000,
        transition: "zoom",
        onClose: () => {
          router.push({ path: "/todo/raisedbyme" });
        },
      });
    }else {
      toast.error(resp.message.message || "Failed to update request", {
        autoClose: 2000,
        transition: "zoom",
      });
    }
  });
}

// const tableRows = ref([]);

// Initialize tableRows for each table
// onMounted(() => {
//   tableRows.value = tableHeaders.value.map(() => []);
// }); 

const addRow = (tableIndex) => {
  if (!tableRows.value[tableIndex]) {
    tableRows.value[tableIndex] = []; // Initialize it if undefined
  }

  const newRow = Object.fromEntries(
    tableHeaders.value[tableIndex].map((field) => [field.fieldname, ""])
  );

  tableRows.value[tableIndex].push(newRow);

  nextTick(() => {
    if (mainBlockRef.value) {
      mainBlockRef.value.scrollTo({
        top: mainBlockRef.value.scrollHeight,
        behavior: "smooth",
      });
    }
  });

};

const removeRow = (tableIndex, rowIndex) => {
  tableRows.value[tableIndex].splice(rowIndex, 1);
};





function clearFrom() {

  emittedFormData.value = []
  window.location.reload()
  tableRows.value = []

}
function deptData(value = null) {
  const filters = [["business_unit", "like", `%${business_unit.value}%`]];
  const queryParams = {
    fields: JSON.stringify(["*"]),
    filters: JSON.stringify(filters),
  };

  axiosInstance
    .get(apis.resource + doctypes.departments, { params: queryParams })
    .then((res) => {
      if (res.data) {
        deptartmentData.value = res.data;

        // Update the route for the "Forms" tab with the first department's route
        const newFormsRoute =
          deptartmentData.value.length > 0
            ? `/forms/department/${deptartmentData.value[0].name
              .replace(/\s+/g, "-")
              .toLowerCase()}`
            : "/forms";

        tabsData.value = tabsData.value.map((tab) => {
          if (tab.name === "Forms") {
            return { ...tab, route: newFormsRoute };
          }
          return tab;
        });

        formSideBarData.value = deptartmentData.value.map((department) => ({
          route: department.name.replace(/\s+/g, "-").toLowerCase(),
        }));

        if (value && activeTab.value.includes("/forms")) {
          handleBuChange({ route: newFormsRoute });
        }
      }
    })
    .catch((error) => {
      console.error("Error fetching department data:", error);
    });
}
function raiseRequest() {
  const storedData = localStorage.getItem("employeeData");
  if (storedData) {
    employeeData.value = JSON.parse(storedData);
    categoriesdata(employeeData?.value.department);
  } else {
    console.error("No employee data found in local storage.");
  }
}
function categoriesdata(departmentId) {
  axiosInstance
    .get(`${apis.resource}${doctypes.departments}/${departmentId}`)
    .then((res) => {
      if (res.data && res.data.ezy_departments_items) {
        categoryOptions.value = res.data.ezy_departments_items.map(
          (item) => item.category
        );
      }
    })
    .catch((error) => {
      console.error("Error fetching categories data:", error);
    });
}
// const queryParamsCount = {
//     fields: JSON.stringify(["count( `tabEzy Form Definitions`.`name`) AS total_count"]),
//     limitPageLength: "None",
//     filters: JSON.stringify(filters),
// }
// axiosInstance.get(`${apis.resource}${doctypes.EzyFormDefinitions}`, { params: queryParamsCount })
//     .then((res) => {
//
//         totalRecords.value = res.data[0].total_count

//     })
//     .catch((error) => {
//         console.error("Error fetching ezyForms data:", error);
//     });

function formDefinations() {
  const filters = [["business_unit", "like", `%${selectedData.value.selectedBusiness_unit}%`]];
  if (selectedData.value.selectedCategory) {
    filters.push([
      "form_category",
      "like",
      `${selectedData.value?.selectedCategory}`,
    ]);
  }
  if (selectedData.value.selectedform || selectedData.value.linkedDocName) {
    filters.push([
      "form_short_name",
      "=",
      `${selectedData.value?.selectedform || selectedData.value.linkedDocName}`,
    ]);
  }

  const queryParams = {
    fields: JSON.stringify(["*"]),
    limit_page_length: 'None',
    limit_start: filterObj.value.limit_start,
    filters: JSON.stringify(filters),
    order_by: "`tabEzy Form Definitions`.`creation` desc",
  };

  axiosInstance
    .get(`${apis.resource}${doctypes.EzyFormDefinitions || selectedData.value.linkedDocName}`, {
      params: queryParams,
    })
    .then((res) => {
      checkingIs_linked.value = res.data[0];
      const form_json = res.data[0].form_json;

      blockArr.value = rebuildToStructuredArray(JSON.parse(form_json).fields);
      if (selectedData.value.selectedFormId) {
        WfRequestUpdate();
      }

      // console.log(form_json, typeof form_json, "=-------------");
      blockArr.value.splice(1);

      const parsedFormJson = JSON.parse(form_json);
      tableName.value = parsedFormJson.fields.filter(
        (field) => field.fieldtype === "Table"
      );
      // console.log(tableName.value);
      // console.log(tableName.value, "5555");
      childTableName.value = tableName.value[0]?.options.replace(/_/g, " ");

      // console.log(childTableName.value, "child====");
// const lowerCaseChildTableFields = {};
// for (const key in parsedFormJson.child_table_fields) {
//   lowerCaseChildTableFields[key] = parsedFormJson.child_table_fields[key].map((field) => ({
//     ...field,
//     label: field.label?.toLowerCase() || "",
//   }));
// }

// tableHeaders.value = lowerCaseChildTableFields;
const originalChildTableFields = parsedFormJson.child_table_fields;
const transformedChildTableFields = {};

for (const key in originalChildTableFields) {
  const lowerKey = key.toLowerCase();
  transformedChildTableFields[lowerKey] = originalChildTableFields[key];
}

tableHeaders.value = transformedChildTableFields;

      // tableHeaders.value = parsedFormJson.child_table_fields; 
      initializeTableRows();
      //console.log(tableHeaders.value, "table fields"); 
    })
    .catch((error) => {
      console.error("Error fetching ezyForms data:", error);
    });
}

function initializeTableRows() {
  if (tableHeaders.value?.length > 0) {
    const newRow = Object.fromEntries(
      tableHeaders.value?.map((field) => [field.fieldname, ""])
    );
    childtablesData.value.push(newRow);
  }
}

const handleFileUpload = (event, row, fieldname) => {
  const file = event.target.files[0];
  if (file) {
    row[fieldname] = file;
    uploadFile(row, fieldname, file);
  }
};
const uploadFile = (row, fieldname, file) => {
  let fileName = `${file.name}`;

  const formData = new FormData();
  formData.append("file", file, fileName);
  formData.append("is_private", "0");
  formData.append("folder", "Home");

  axiosInstance
    .post(apis.uploadfile, formData)
    .then((res) => {
      if (res.message && res.message.file_url) {
        row[fieldname] = res.message.file_url;

        // console.log("Uploaded file URL:", res.message.file_url);
      } else {
        console.error("file_url not found in the response.");
      }
    })
    .catch((error) => {
      console.error("Upload error:", error);
    });
};
// axiosInstance
//   .get(`${apis.resource}/${selectedData.value?.selectedform}`)
//   .then((res) => {
//     if (res) {
//       childIDs.value = res.data[0].name;

//       childFunction();
//     }
//   })
//   .catch((error) => {
//     console.error("Error fetching categories data:", error);
//   });
//   if (!parsedFormJson.fields) {
//     console.error("fields key is missing in form_json");
//     return;
//   }
//   const tableFields = parsedFormJson.fields.filter(
//     (field) => field.fieldtype === "Table"
//   );

// Fetch data for each Table field
//   tableFields.forEach((tableField) => {
// if (tableField.options) {

// }
//   });

// function childFunction() {
//   axiosInstance
//     .get(
//       `${apis.resource}${selectedData.value?.selectedform}/${childIDs.value}`
//     )
//     .then((res) => {
//       console.log(`Data for :`, res.data);
//       responseData.value = res.data;
//     })
//     .catch((error) => {
//       console.error(`Error fetching data for :`, error);
//     });
// }
const handleFieldUpdate = (field) => {
  // console.log(field,"field");
  const fieldExists = emittedFormData.value.some(
    (item) => item.fieldname === field.fieldname
  );
  if (!fieldExists) {
    if (field.fieldtype === "Attach") {

      if (field.value && typeof field.value === "string") {
        filepaths.value = field.value
          .split(",")
          .map((filePath, index) => ({ [index]: filePath.trim() })) // Assign numeric keys
          .filter((file) => Object.values(file)[0] !== ""); // Remove empty entries
      } else {
        filepaths.value = [];
      }
      // console.log(filepaths.value,"oooo");
      // console.log(emittedFormData.value,"emitteddata");
      emittedFormData.value.push(field);
    } else {
      emittedFormData.value = emittedFormData.value.concat(field);
    }
  } else {
    console.log(
      `Field with name "${field.fieldname}" already exists in emittedFormData.`
    );
  }
};

const removeAttachFiles = ref([])

const handleRemovedFiles = (removedFiles) => {
  removeAttachFiles.value = removedFiles;
}




const ChildTableData = async () => {
  const childEntries = Object.entries(childtablesData.value);

  if (!childEntries.length) return;

  const formPromises = childEntries.map(([tableName, rows]) => {
    if (!rows || !rows.length) {
      console.warn(`⚠ Skipping empty child table: ${tableName}`);
      return null;
    }

    const form = {
      doctype: selectedData.value.selectedform ? selectedData.value.selectedform : selectedData.value.linkedDocName,
      company_field: business_unit.value,
      [tableName.toLowerCase()]: rows
    };
    // .toLowerCase()

    const formData = new FormData();
    formData.append("doc", JSON.stringify(form));
    formData.append("action", "Save");

    return axiosInstance.post(apis.savedocs, formData);
  }).filter(Boolean);

  try {
    const responses = await Promise.all(formPromises);
    return responses; // Return if needed
  } catch (error) {
    console.error("❌ Error submitting child tables:", error);
    throw error; // Important: so raiseRequestSubmission halts
  }
};
const linkedId = ref("");

const childRef = ref(null)

function toRaiseReqBtn() {
  const hasError = childRef.value?.errorStatus ?? false;

  if (hasError) {
    toast.error('Please fix errors before submitting.');
    return;
  }

  if (!isFormValid.value) {
    toast.error("Please Fill All Mandatory Fields");
    return;
  }

  const modal = new bootstrap.Modal(document.getElementById('ExportEmployeeModal'));
  modal.show();
}



async function raiseRequestSubmission() {
  // if (!isFormValid.value) {
  //   toast.error("Please Fill All Mandatory Fields");
  //   return;
  // }

  const childEntries = Object.entries(childtablesData.value);

  // if (!childEntries.length) {
  //   toast.error("No child table data found!");
  //   return;
  // }

  // Prepare the form data
  const form = {
    doctype: selectedData.value.selectedform
      ? selectedData.value.selectedform
      : selectedData.value.linkedDocName,
    company_field: business_unit.value,
  };


  // Append all child tables
  childEntries.forEach(([tableName, rows]) => {
    if (rows && rows.length) {
      form[tableName.toLowerCase()] = rows;
    } else {
      console.warn(`⚠ Skipping empty child table: ${tableName}`);
    }
  });

  // Append emitted form data
  if (emittedFormData.value.length) {
    emittedFormData.value.forEach((each) => {
      form[each.fieldname] = each.value;
    });
  }

  // Append linked ID if exists
  if (linkedId.value) {
    form.returnable_gate_pass_id = linkedId.value;
  }

  const formData = new FormData();
  formData.append("doc", JSON.stringify(form));
  formData.append("action", "Save");

  try {
    const response = await axiosInstance.post(apis.savedocs, formData);
    // console.log(response, "✅ Form submitted successfully");

    if (response) {
      request_raising_fn(response.docs[0]);
    } else {
      toast.error("Submission successful but no response data.");
    }
  } catch (error) {
    console.error("❌ Error submitting main form:", error);
    toast.error("Error submitting the form.");
  }
}

// async function raiseRequestSubmission() {
//   if (!isFormValid.value) {
//     toast.error("Please Check Fields");
//     return;
//   }

//   // try {
//   //   await ChildTableData(); // ✅ Wait until all child table APIs are done
//   // } catch (error) {
//   //   toast.error("Child table submission failed");
//   //   return; // Stop main form submission
//   // }  
//   const childEntries = Object.entries(childtablesData.value);

//   if (!childEntries.length) return;

//   const formPromises = childEntries.map(([tableName, rows]) => {
//     if (!rows || !rows.length) {
//       console.warn(`⚠ Skipping empty child table: ${tableName}`);
//       return null;
//     }

//     // Merge all child tables into main form
//     let form = {
//       doctype: selectedData.value.selectedform ? selectedData.value.selectedform : selectedData.value.linkedDocName,
//       company_field: business_unit.value,
//       [tableName.toLowerCase()]: rows // ✅ use collected tableData directly
//     };

//     // Append other form fields
//     if (emittedFormData.value.length) {
//       emittedFormData.value.forEach((each) => {
//         form[each.fieldname] = each.value;
//       });
//     }
//     if (linkedId.value) {
//       form.linked_id = linkedId.value;
//     }
//     console.log(form, "Final Form Data to Submit");
//   });
//     const formData = new FormData();
//     formData.append("doc", JSON.stringify(form));
//     formData.append("action", "Save");
//     console.log(form, "formData");
//     axiosInstance
//       .post(apis.savedocs, formData)
//       .then((response) => {
//         request_raising_fn(response.docs[0]);
//       })
//       .catch((error) => {
//         console.error("❌ Error submitting main form:", error);
//       });
//   }
function gettingDataToLink() {
  const dataObj = {
    wf_request: selectedData.value.main_form_Id,
  };

  axiosInstance
    .post(apis.gettingDataTo, dataObj)
    .then((response) => {
      const responseData = response.message;
      linkedId.value = responseData.returnable_gate_pass_id;

      // ✅ Find table name dynamically (excluding 'linked_id')
      const tableKey = Object.keys(responseData).find(
        (key) => key !== 'returnable_gate_pass_id'
      );

      if (tableKey) {
        LinkedChildTableData.value = {
          table_name: tableKey,
          rows: responseData[tableKey],
        };

        // console.log(LinkedChildTableData.value, "Linked Child Table Data");
      }
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

// const ChildTableData = async () => {
//   if (!tableName.value.length) return;



//   // **Loop through each child table and send separate API requests**
//   const formPromises = tableName.value.map((table) => {
//     const childName = table.options;
//     const childData = tableRows.value[childName];

//     if (!childData || !childData.length) {
//       console.warn(`⚠ Skipping empty child table: ${childName}`);
//       return null; // Skip empty tables
//     }

//     const form = {
//       doctype: selectedData.value.selectedform,
//       company_field: business_unit.value,
//       [childName]: childData, // Only this child table's data
//     };

//     const formData = new FormData();
//     formData.append("doc", JSON.stringify(form));
//     formData.append("action", "Save");
// // console.log(formData,"[[[[]]]]");


//     // **Return API call promise**
//     return axiosInstance.post(apis.savedocs, formData);
//   }).filter(Boolean); // Remove null entries

//   try {
//     const responses = await Promise.all(formPromises);

//   } catch (error) {
//     console.error("Error submitting child tables:", error);
//   }
// };

// async function raiseRequestSubmission() {
//   if (!isFormValid.value) {
//     toast.error("Please Fill Mandatory Fields");
//     return;
//   }

//   //  First, submit child tables separately
//   await ChildTableData();

//   //  Collect all child tables for the main submission
//   let childTables = {};
//   tableName.value.forEach((table) => {
//     const childName = table.options;
//     const childData = tableRows.value[childName];

//     if (childData && childData.length) {
//       childTables[childName] = childData;
//     }
//   });

//   //  Merge child tables with main form
//   let form = {
//     doctype: selectedData.value.selectedform,
//     company_field: business_unit.value,
//     ...childTables, // Add all child tables
//   };
//   if (emittedFormData.value.length) {
//     emittedFormData.value.forEach((each) => {
//       form[each.fieldname] = each.value;
//     });
//   }

//   const formData = new FormData();
//   formData.append("doc", JSON.stringify(form));
//   formData.append("action", "Save");

//   axiosInstance
//     .post(apis.savedocs, formData)
//     .then((response) => {
//       request_raising_fn(response.docs[0]);
//     })
//     .catch((error) => {
//       console.error("Error submitting main form:", error);
//     });
// }



// const ChildTableData = async () => {
//   if (!tableName.value.length) return;

//   console.log("✅ Sending Child Tables Data...");

//   // **Loop through each child table and send separate API requests**
//   const formPromises = tableName.value.map((table, index) => {
//     const childName = table.options;

//     // if (!tableRows.value[childName] || !tableRows.value[childName].length) {
//     //   console.warn(`⚠ Skipping empty child table: ${childName}`);
//     //   return null; // Skip if no data
//     // }

//     const form = {
//       doctype: selectedData.value.selectedform,
//       company_field: business_unit.value,
//       [childName]: tableRows.value[childName], // Ensure we use the correct childName key
//     };

//     console.log(`🚀 Submitting Child Table: ${childName}`, form);

//     const formData = new FormData();
//     formData.append("doc", JSON.stringify(form));
//     formData.append("action", "Save");

//     // **Return API call promise**
//     return axiosInstance.post(apis.savedocs, formData);
//   }).filter(Boolean); // Remove `null` values (empty tables)

//   try {
//     // **Await all API requests**
//     const responses = await Promise.all(formPromises);
//     console.log("✅ Child Tables Submitted:", responses);
//   } catch (error) {
//     console.error("❌ Error submitting child table data:", error);
//   }
// };

// async function raiseRequestSubmission() {
//   if (!isFormValid.value) {
//     toast.error("Please Fill Mandatory Fields");
//     return;
//   }

//   // **Submit each child table separately**
//   const childTables = ChildTableData();  // Wait for all child tables to be submitted

//   // **Now, submit the main form WITHOUT child tables**
//   let form = {
//     doctype: selectedData.value.selectedform,
//     company_field: business_unit.value,
//     ...childTables,
//   };

//   // ✅ Include additional form data if available
//   if (emittedFormData.value.length) {
//     emittedFormData.value.forEach((each) => {
//       form[each.fieldname] = each.value;
//     });
//   }

//   const formData = new FormData();
//   formData.append("doc", JSON.stringify(form));
//   formData.append("action", "Save");

//   console.log("🚀 Submitting Main Form", form);

//   axiosInstance
//     .post(apis.savedocs, formData)
//     .then((response) => {
//       request_raising_fn(response.docs[0]); // Process response
//     })
//     .catch((error) => {
//       console.error("❌ Error submitting main form:", error);
//     });
// }

const child_id_name = ref((''))

function WfRequestUpdate() {
  const filters = [
    [
      "wf_generated_request_id",
      "like",
      `%${selectedData.value.selectedFormId}%`,
    ],
  ];

  const queryParams = {
    fields: JSON.stringify(["*"]),
    limit_page_length: null,
    limit_start: 0,
    filters: JSON.stringify(filters),
    order_by: `\`tab${selectedData.value.selectedform}\`.\`creation\` desc`,
  };

  axiosInstance
    .get(`${apis.resource}${selectedData.value.selectedform}`, {
      params: queryParams,
    })
    .then((res) => {
      if (res.data && res.data.length > 0) {
        const doctypeForm = res.data[0];

        // console.log( blockArr.value);

        // Map response data to UI fields
        mapFormFieldsToRequest(doctypeForm, blockArr.value);


        axiosInstance
          .get(`${apis.resource}${selectedData.value.selectedform}`)
          .then((res) => {
            console.log(`Data for :`, res.data[0]);
            newMainId.value = res.data[0].name

          })
          .catch((error) => {
            console.error(`Error fetching data for :`, error);
          });
        axiosInstance
          .get(
            `${apis.resource}${selectedData.value.selectedform}/${res.data[0].name}`
          )
          .then((res) => {
            // console.log(`Data for :`, res.data);
            // Identify the child table key dynamically
            const childTables = Object.keys(res.data).filter((key) =>
              Array.isArray(res.data[key])
            );
            // console.log(childTables);


            if (childTables.length) {
              tableRows.value = {};

              childTables.forEach((tableKey) => {
                tableRows.value[tableKey] = res.data[tableKey] || [];
              });
              child_id_name.value = res.data.name
              // console.log(res.data,"000000");

            }
          })
          .catch((error) => {
            console.error(`Error fetching data for :`, error);
          });
      }
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

function mapFormFieldsToRequest(doctypeData, blockArr) {
  if (!doctypeData) return; // Ensure valid data

  blockArr.forEach((block) => {
    block.sections?.forEach((section) => {
      section.rows?.forEach((row) => {
        row.columns?.forEach((column) => {
          column.fields?.forEach((field) => {
            // Check if the field exists in the API response
            if (doctypeData.hasOwnProperty(field.fieldname)) {
              field.value = doctypeData[field.fieldname] ?? ""; // Set value reactively
            }
          });
        });
      });
    });
  });
}
function request_raising_fn(item) {
  saveloading.value = true;
  // console.log(filepaths.value, "---filepaths");
  // const filesArray = filepaths.value
  //   ? filepaths.value.split(",").map((filePath) => filePath.trim())
  //   : [];
  let data_obj = {
    module_name: "Ezy Forms",
    doctype_name: selectedData.value.selectedform ? selectedData.value.selectedform : selectedData.value.linkedDocName,
    ids: [item.name],
    reason: selectedData.value.hasWorkflow === 'No' ? "Completed" : "Request Raised",
    url_for_request_id: "",
    files: [],
    property: business_unit.value,
    ip_address: ip_address.value,
    employee_id: employeeData.value.emp_code,
    be_half_of:item.employee_name,
    request_for:item.request_for,
    unwanted_files: removeAttachFiles.value
  };
  axiosInstance.post(apis.raising_request, data_obj).then((resp) => {
    if (resp?.message?.success === true) {
      if(selectedData.value.main_form_Id){
        linked_id_adding_method(item.name)
      }
      const modal = bootstrap.Modal.getInstance(
        document.getElementById("ExportEmployeeModal")
      );
      modal.hide();
      // saveloading.value = false;

      toast.success(resp?.message?.message, {
        autoClose: 1000,
        transition: "zoom",
        onClose: () => {
          router.push({ path: "/todo/raisedbyme" });
        },
      });
    }
  })
   .catch((error) => {
      console.error("Error raising request:", error);
      toast.error("Error raising request");
    })
    .finally(() => {
      saveloading.value = false;
    });
}
function linked_id_adding_method(name) {
  
  let data_obj = {
   request_id: selectedData.value.main_form_Id,
   linked_form: name,
  };
  axiosInstance.post(apis.linked_form_id_update, data_obj).then((resp) => {
    if (resp?.message) {
      console.log(resp);
     
    }
  })
   .catch((error) => {
      console.error("Error updating linked form ID:", error);
    });
}




// window.location.reload();
</script>

<style lang="scss" scoped>
.zindex-dropdown {
  z-index: 1050;
  max-height: 200px;
  overflow-y: auto;
}

/* .modal {
  background: rgba(0, 0, 0, 0.5);
  position: fixed;
  top: 0; left: 0;
  width: 100vw; height: 100vh;
  display: flex; 
  align-items: center;
  justify-content: center;
} */
.requestPreviewDiv {
  height: 80vh;
  overflow-y: auto;
  padding: 20px 0px;
}

.raiserequestBtnDiv {
  position: sticky;
  bottom: 0;
  left: 0;
  right: 0;
  background-color: #fff;
  z-index: 1;
}

.raisePreview {
  background-color: #eeeeee;
  padding: 10px;
  border: 1px solid #cccccc;
  border-radius: 10px;
  margin-bottom: 5px;
  margin-top: 15px;
}

.raisefrom {
  background-color: #ffffff;
  padding: 10px;
  border-radius: 10px;
  border: 1px solid #cccccc;
}

.raise-label {
  font-size: 12px;
  font-weight: 500;
  margin-bottom: 2px;
}

.backtofromPage {
  background-color: #ffffff;
  padding: 5px;
}

.no-form {
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  font-size: 15px;
  font-weight: 500;
}
.Acknowledgement-check{
  border: 1px solid rgb(64, 62, 62);
  box-shadow: rgba(60, 64, 67, 0.3) 0px 1px 2px 0px, rgba(60, 64, 67, 0.15) 0px 2px 6px 2px;
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

button {
  margin-top: 10px;
  padding: 5px 10px;
  cursor: pointer;
}

.bi-x-lg::before {
  content: "\f659";
  margin-top: 8px;
}
</style>