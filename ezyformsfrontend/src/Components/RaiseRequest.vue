<template>
  <div>
    <div class="backtofromPage py-2">
      <router-link :to="backTo" @click="backToForm" class="text-decoration-none text-dark  ps-3 font-13"><span> <i
            class="bi bi-arrow-left pe-2"></i></span>Back</router-link>
    </div>
    <div class="container">
      <div v-if="blockArr.length" class="position-relative">
        <div class="requestPreviewDiv">
          <RequestPreview :blockArr="blockArr" :formName="selectedData.selectedform" @updateField="handleFieldUpdate"
            @formValidation="isFormValid = $event" />
          <!-- @formValidation="isFormValid = $event" -->

          <!-- <span class="font-13 fw-bold">{{ table.childTableName.replace(/_/g, " ") }}</span> -->
          <div  class="mt-3">
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
                      <template v-else-if="field.fieldtype === 'Attach'">
                        <input type="file" class="form-control font-12"
                          @change="handleFileUpload($event, row, field.fieldname)" />
                      </template>
                    </td>
                  </tr>
                </tbody>
              </table>

              <button class="btn btn-light font-12" @click="addRow(tableIndex)">Add Row</button>
            </div>
          </div>


        </div>
        <!-- @formValidation="isFormValid = $event" -->
        <div class="raiserequestBtnDiv">
          <div class="d-flex justify-content-end align-items-center gap-2 p-3">
            <button class="btn btn-white font-13" @click="clearFrom">
              <span> <i class="bi bi-x"></i></span>Clear form
            </button>
            <!-- :disabled="!isFormValid" -->
            <button v-if="!selectedData.selectedFormId" class="btn btn-dark font-12" type="submit"
              @click="raiseRequestSubmission">
              Raise Request
            </button>
            <button v-if="selectedData.selectedFormId && $route.query.selectedFormStatus == 'Request Cancelled'"
              @click="RequestUpdate" class="btn btn-dark font-12" type="submit">
              Update Request
            </button>
            <button v-if="$route.query.selectedFormStatus && $route.query.selectedFormStatus == 'Request Raised'"
              @click="EditRequestUpdate" class="btn btn-dark font-12" type="submit">
              Update Request
            </button>

          </div>
        </div>
      </div>
      <div v-else>
        <div class="no-form">No Form</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from "vue";
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
});


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

const filterObj = ref({
  limit_start: 0,
  limitPageLength: 100,
});

function backToForm() {
  blockArr.value = [];
}


onMounted(() => {
  formDefinations();
  raiseRequest();
});

watch(business_unit.value, (newBu, oldBu) => {
  
  business_unit.value = newBu;
  console.log(newBu);
  console.log("[[[[]]]]", newBu,oldBu);
  // localStorage.setItem("Bu", EzyBusinessUnit.value);

  if (oldBu) {
    deptData(true);
  } else {
    deptData();
  }
});
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
      console.log(`Updated Record for All Child Tables:`, response.data);
    })
    .catch((error) => {
      console.error(`Error updating records:`, error);
    });
}

function EditRequestUpdate() {
  // Filter valid tables that have child data
  const validTables = tableName.value.filter((table) => {
    const childData = tableRows.value[table.options];
    return childData && childData.length;
  });

  let childTables = [];

  // Iterate through valid tables and collect their fields
  validTables.forEach((table) => {
    const childTableName = table.options;
    const childFields = tableRows.value[childTableName] || [];

    childTables.push({
      child_table: childTableName,
      child_fields: childFields,
    });
  });

  console.log(childTables, childTables.length,"Child Tables Data");

  // Call function to update child records
  if(childTables.length){
    updateChildRecords(childTables, child_id_name.value);
  }


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
  console.log(data_obj,"lll");

  axiosInstance
    .post(apis.edit_form_before_approve, data_obj)
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



// async function EditRequestUpdate() {
//   let form = {};
//   if (emittedFormData.value.length) {
//     emittedFormData.value.forEach((each) => {
//       form[each.fieldname] = each.value;
//     });
//   }

//   // Filter valid tables that have child data
//   const validTables = tableName.value.filter((table) => {
//     const childData = tableRows.value[table.options];
//     return childData && childData.length;
//   });

//   let child_table = "";
//   let child_fields = [];

//   // Ensure we process only the first valid table
//   if (validTables.length) {
//     const table = validTables[0]; // Picking the first valid table
//     child_table = table.options;
//     child_fields = tableRows.value[child_table] || [];
//   }

//   let data_obj = {
//     form_id: route.query.selectedFormId,
//     updated_fields: form, // Form updates
//     child_table, // Single child table name
//     child_fields // Corresponding child table fields
//   };

//   console.log(data_obj, "lll");

//   axiosInstance.post(apis.edit_form_before_approve, data_obj).then((resp) => {
//     if (resp?.message?.success) {
//       toast.success("Request Raised", {
//         autoClose: 2000,
//         transition: "zoom",
//         onClose: () => {
//           router.push({ path: "/todo/raisedbyme" });
//         },
//       });
//     }
//   });
// }





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
  const filters = [["business_unit", "like", `%${business_unit.value}%`]];
  if (selectedData.value.selectedCategory) {
    filters.push([
      "form_category",
      "like",
      `${selectedData.value?.selectedCategory}`,
    ]);
  }
  if (selectedData.value.selectedform) {
    filters.push([
      "form_short_name",
      "=",
      `${selectedData.value?.selectedform}`,
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
    .get(`${apis.resource}${doctypes.EzyFormDefinitions}`, {
      params: queryParams,
    })
    .then((res) => {
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
      console.log(tableName.value);
      // console.log(tableName.value, "5555");
      childTableName.value = tableName.value[0]?.options.replace(/_/g, " ");

      // console.log(childTableName.value, "child====");

      tableHeaders.value = parsedFormJson.child_table_fields;
      initializeTableRows();
      // console.log(tableHeaders.value, "table fields");
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
    tableRows.value.push(newRow);
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

const ChildTableData = async () => {
  if (!tableName.value.length) return;



  // **Loop through each child table and send separate API requests**
  const formPromises = tableName.value.map((table) => {
    const childName = table.options;
    const childData = tableRows.value[childName];

    if (!childData || !childData.length) {
      console.warn(`⚠ Skipping empty child table: ${childName}`);
      return null; // Skip empty tables
    }

    const form = {
      doctype: selectedData.value.selectedform,
      company_field: business_unit.value,
      [childName]: childData, // Only this child table's data
    };

    const formData = new FormData();
    formData.append("doc", JSON.stringify(form));
    formData.append("action", "Save");
console.log(formData,"[[[[]]]]");


    // **Return API call promise**
    return axiosInstance.post(apis.savedocs, formData);
  }).filter(Boolean); // Remove null entries

  try {
    const responses = await Promise.all(formPromises);

  } catch (error) {
    console.error("Error submitting child tables:", error);
  }
};

async function raiseRequestSubmission() {
  if (!isFormValid.value) {
    toast.error("Please Fill Mandatory Fields");
    return;
  }

  //  First, submit child tables separately
  await ChildTableData();

  //  Collect all child tables for the main submission
  let childTables = {};
  tableName.value.forEach((table) => {
    const childName = table.options;
    const childData = tableRows.value[childName];

    if (childData && childData.length) {
      childTables[childName] = childData;
    }
  });

  //  Merge child tables with main form
  let form = {
    doctype: selectedData.value.selectedform,
    company_field: business_unit.value,
    ...childTables, // Add all child tables
  };
  if (emittedFormData.value.length) {
    emittedFormData.value.forEach((each) => {
      form[each.fieldname] = each.value;
    });
  }

  const formData = new FormData();
  formData.append("doc", JSON.stringify(form));
  formData.append("action", "Save");

  axiosInstance
    .post(apis.savedocs, formData)
    .then((response) => {
      request_raising_fn(response.docs[0]);
    })
    .catch((error) => {
      console.error("Error submitting main form:", error);
    });
}



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
          })
          .catch((error) => {
            console.error(`Error fetching data for :`, error);
          });
        axiosInstance
          .get(
            `${apis.resource}${selectedData.value.selectedform}/${res.data[0].name}`
          )
          .then((res) => {
            console.log(`Data for :`, res.data);
            // Identify the child table key dynamically
            const childTables = Object.keys(res.data).filter((key) =>
              Array.isArray(res.data[key])
            );
            
            if (childTables.length) {
              tableRows.value = {};

              childTables.forEach((tableKey) => {
                tableRows.value[tableKey] = res.data[tableKey] || [];
              });
              child_id_name.value = res.data.name
              console.log(res.data,"000000");
              
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
  console.log(filepaths.value, "---filepaths");
  // const filesArray = filepaths.value
  //   ? filepaths.value.split(",").map((filePath) => filePath.trim())
  //   : [];
  let data_obj = {
    module_name: "Ezy Forms",
    doctype_name: selectedData.value.selectedform,
    ids: [item.name],
    reason: "Request Raised",
    url_for_request_id: "",
    files: filepaths.value.length > 0 ? filepaths.value : [],
    property: business_unit.value,
  };
  axiosInstance.post(apis.raising_request, data_obj).then((resp) => {
    if (resp?.message?.success === true) {
      toast.success("Request Raised", {
        autoClose: 1000,
        transition: "zoom",
        onClose: () => {
          router.push({ path: "/todo/raisedbyme" });
        },
      });
    }
  });
}


// window.location.reload();
</script>

<style scoped>
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
</style>