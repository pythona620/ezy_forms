<template>
  <div>
    <div class="backtofromPage py-2">
      <router-link
        to="/todo/receivedform"
        class="text-decoration-none text-dark font-13"
        ><span> <i class="bi bi-arrow-left"></i></span>Asset request
        form</router-link
      >
    </div>
    <div class="container">
      <div v-if="blockArr.length" class="position-relative">
        <div class="requestPreviewDiv">
          <RequestPreview
            :blockArr="blockArr"
            :formName="selectedData.selectedform"
            @updateField="handleFieldUpdate"
            @formValidation="isFormValid = $event"
          />

          <div v-if="tableName.length" class="mt-3">
            <div>
              <span class="font-13 fw-bold">{{ childTableName }}</span>
            </div>
            <table class="table table-striped" border="1" width="100%">
              <thead>
                <tr>
                  <th>#</th>
                  <th v-for="field in tableHeaders" :key="field.fieldname">
                    {{ field.label }}
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="(row, index) in tableRows" :key="index">
                  <td>{{ index + 1 }}</td>
                  <td v-for="field in tableHeaders" :key="field.fieldname">
                    <template v-if="field.fieldtype === 'Data'">
                      <input
                        type="text"
                        class="form-control"
                        v-model="row[field.fieldname]"
                      />
                    </template>
                    <template v-else-if="field.fieldtype === 'Attach'">
                      <input
                        type="file"
                        class="form-control"
                        @change="handleFileUpload($event, row, field.fieldname)"
                      />
                    </template>
                  </td>
                </tr>
              </tbody>
            </table>
            <button class="btn btn-light" @click="addRow">Add Row</button>
          </div>
        </div>
        <!-- @formValidation="isFormValid = $event" -->
        <div class="raiserequestBtnDiv">
          <div class="d-flex justify-content-end align-items-center p-3">
            <button class="btn btn-white font-13" @click="clearFrom">
              <span> <i class="bi bi-x"></i></span>Clear form
            </button>
            <!-- :disabled="!isFormValid" -->
            <button
              :disabled="!isFormValid"
              class="btn btn-dark font-12"
              type="submit"
              @click="raiseRequestSubmission"
            >
              Raise Request
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
import { onMounted, ref, watch } from "vue";
import { apis, doctypes, domain } from "../shared/apiurls";
import RequestPreview from "./RequestPreview.vue";
import Multiselect from "@vueform/multiselect";
import "@vueform/multiselect/themes/default.css";
import { rebuildToStructuredArray } from "../shared/services/field_format";
import axiosInstance from "../shared/services/interceptor";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import { EzyBusinessUnit } from "../shared/services/business_unit";
import { useRoute, useRouter } from "vue-router";

const router = useRouter();
const route = useRoute(); // Get query params from route

//  Extract query parameters from URL
const selectedData = ref({
  selectedCategory: route.query.selectedCategory || "", // Retrieve from query
  selectedform: route.query.selectedForm || "", // Retrieve from query
});
const business_unit = ref(route.query.business_unit || ""); // Retrieve from query
const isFormValid = ref(false);
const blockArr = ref([]);
const categoryOptions = ref([]);
const employeeData = ref({});
const formList = ref([]);
const emittedFormData = ref([]);
const filepaths = ref("");

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
onMounted(() => {
  formDefinations();
  raiseRequest();
});
const addRow = () => {
  const newRow = Object.fromEntries(
    tableHeaders.value.map((field) => [field.fieldname, ""])
  );
  tableRows.value.push(newRow);
};

watch(business_unit, (newBu, oldBu) => {
  EzyBusinessUnit.value = newBu;
  localStorage.setItem("Bu", EzyBusinessUnit.value);

  if (oldBu) {
    deptData(true);
  } else {
    deptData();
  }
});
function clearFrom() {}
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
      "like",
      `%${selectedData.value?.selectedform}%`,
    ]);
  }

  const queryParams = {
    fields: JSON.stringify(["*"]),
    limit_page_length: filterObj.value.limitPageLength,
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

      // console.log(form_json, typeof form_json, "=-------------");
      blockArr.value.splice(1);

      const parsedFormJson = JSON.parse(form_json);
      tableName.value = parsedFormJson.fields.filter(
        (field) => field.fieldtype === "Table"
      );
      console.log(tableName.value, "5555");
      childTableName.value = tableName.value[0]?.options.replace(/_/g, " ");

      console.log(childTableName.value, "child====");

      tableHeaders.value = parsedFormJson.child_table_fields;
      initializeTableRows();
      console.log(tableHeaders.value, "table fields");
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

        console.log("Uploaded file URL:", res.message.file_url);
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
  const fieldExists = emittedFormData.value.some(
    (item) => item.fieldname === field.fieldname
  );

  if (!fieldExists) {
    if (field.fieldtype === "Attach") {
      if (!Array.isArray(field.value)) {
        filepaths.value = field.value;
      }
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
// const ChildTableData = () => {
//   const childName = tableName.value[0].options;
//   let form = {};
//   form["doctype"] = selectedData.value.selectedform;
//   form["company_field"] = business_unit.value;
//   form[childName] = tableRows.value;

//   // form['form_json']
//   const formData = new FormData();
//   formData.append("doc", JSON.stringify(form));
//   formData.append("action", "Save");

//   console.log(form);
//   axiosInstance
//     .post(apis.savedocs, formData)
//     .then((response) => {
//       console.log(response);
//     })
//     .catch((error) => {
//       console.error("Error fetching data:", error);
//     });
// };



function raiseRequestSubmission() {
  // ChildTableData();
  const childName = tableName.value[0]?.options;
  let form = {};
  form["doctype"] = selectedData.value.selectedform;
  form["company_field"] = business_unit.value;
  if(tableName.value.length){
    form[childName] = tableRows.value;
  }
  // form['supporting_files'] = [];
  if (emittedFormData.value.length) {
    emittedFormData.value.map((each) => {
      form[each.fieldname] = each.value;
    });
  }

  // form['form_json']
  const formData = new FormData();
  formData.append("doc", JSON.stringify(form));
  formData.append("action", "Save");
  axiosInstance
    .post(apis.savedocs, formData)
    .then((response) => {
      request_raising_fn(response.docs[0]);
    })
    .catch((error) => {
      console.error("Error fetching data:", error);
    });
}

function request_raising_fn(item) {
  const filesArray = filepaths.value
    ? filepaths.value.split(",").map((filePath) => filePath.trim())
    : [];
  let data_obj = {
    module_name: "Ezy Forms",
    doctype_name: selectedData.value.selectedform,
    ids: [item.name],
    reason: "Request Raised",
    url_for_request_id: "",
    files: filesArray,
    property: business_unit.value,
  };
  axiosInstance.post(apis.raising_request, data_obj).then(async (resp) => {
    if (resp?.message?.success) {
      toast.success("Request Raised", { autoClose: 2000, transition: "zoom" });

      await router.push({ path: "/todo/raisedbyme" });
      // window.location.reload();
    }
  });
}
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