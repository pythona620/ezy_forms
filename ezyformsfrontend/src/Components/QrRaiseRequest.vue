<template>
    <div>
        <div v-if="!raiseResponse">
        <div class="container">
            <div class="backtofromPage text-center my-2 py-2">
            <h6 class="m-0">{{ fetchDetails.name }}</h6>
            </div>
            <div v-if="blockArr.length" class="position-relative">
                <div class="requestPreviewDiv" ref="mainBlockRef">
                    <RequestPreview :blockArr="blockArr" :formName="selectedData.selectedform"
                        :tableHeaders="tableHeaders" ref="childRef" :linked_id="linkedId"
                        :LinkedChildTableData="LinkedChildTableData" @updateField="handleFieldUpdate"
                        @updateRemovedFiles="handleRemovedFiles" :tableRowsdata="tableRows"
                        @formValidation="isFormValid = $event" @updateTableData="handleTableData" />

                </div>
                <div class="raiserequestBtnDiv">
                    <div class="d-flex justify-content-end align-items-center gap-2 mb-3">
                        <button v-if="!selectedData.selectedFormId" class="btn btn-white font-13" @click="clearFrom">
                            <span> <i class="bi bi-x"></i></span>Clear form
                        </button>
                        <button v-if="!selectedData.selectedFormId" @click="toRaiseReqBtn" class="btn btn-dark font-12"
                            type="submit">
                            {{ selectedData.hasWorkflow == 'No' ? 'Save' : 'Raise Request' }}
                        </button>
                        <button
                            v-if="$route.query.selectedFormStatus && ($route.query.selectedFormStatus == 'Request Raised' || $route.query.selectedFormStatus == 'Request Cancelled')"
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
        <div class="modal fade " id="ExportEmployeeModal" data-bs-backdrop="static" tabindex="-1" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Acknowledgement</h5>
                        <button type="button" class="btn-close" @click="acknowledge = ''" data-bs-dismiss="modal"
                            aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <input type="checkbox" v-model="acknowledge" id="Acknowledgement" value="Acknowledgement"
                            class="me-2 mt-1 form-check-input Acknowledgement-check " />
                        <label for="Acknowledgement">
                            I acknowledge that the information provided is correct.
                        </label>
                    </div>
                    <div class="modal-footer">
                        <button type="button" @click="acknowledge = ''" class="btn btn-outline-secondary font-12"
                            data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class="btn btn-dark" style="min-width: 120px;"
                            :disabled="!acknowledge || saveloading" @click="raiseRequestSubmission">
                            <span v-if="saveloading" class="spinner-border spinner-border-sm" role="status"
                                aria-hidden="true"></span>
                            <span v-else class="font-12 fw-bold">Yes, Proceed</span>
                        </button>

                    </div>
                </div>
            </div>
        </div>

        </div>

        <div class="res_div" v-if="raiseResponse">
            <div class="res_message text-center">
              <i class="bi bi-check2-circle fs-1 mb-4"></i>
              <h6 class="font-16">{{ raiseResponse || "No Data" }}</h6>

              <div class="d-flex gap-4 justify-content-center mt-4">
                <button @click="reloadPage()" class="btn add-res-btn"><i class="bi bi-plus-lg me-2"></i>Add Another Response</button>
                <!-- <button class="btn add-res-btn"><i class="bi bi-download me-2"></i>Download your Response ad pdf</button> -->
              </div>

            </div>
        </div>
        </div>
</template>

<script setup>
import { computed, onMounted, ref, watch, } from "vue";
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
const route = useRoute();

//  Extract query parameters from URL
const selectedData = ref({
    routepath: route.query.routepath || "",
    selectedCategory: route.query.selectedCategory || "",
    selectedform: route.query.selectedForm || "",
    selectedFormId: route.query.selectedFormId || "",
    selectedBusiness_unit: route.query.business_unit || "",
    hasWorkflow: route.query.has_workflow || "",
    linkedDocName: route.query.linkedForm || "",
    main_form_Id: route.query.main_form_Id || "",
    type: route.query.type || "",
    main_form: route.query.main_form || "",
});

const acknowledge = ref('')
const saveloading = ref(false)
const business_unit = ref(localStorage.getItem('Bu'));
const isFormValid = ref(false);
// const isFormValid = computed(() => allFieldsFilled.value);
const blockArr = ref([]);
const employeeData = ref({});
const emittedFormData = ref([]);
const filepaths = ref([]);
const backTo = ref(selectedData.value.routepath);
const tableRows = ref([]);
const tableHeaders = ref([]);
const childTableName = ref("");
const tableName = ref("");
const mainBlockRef = ref("");
const childtablesData = ref({});
const filterObj = ref({
    limit_start: 0,
    limitPageLength: 100,
});
const newMainId = ref('')
const checkingIs_linked = ref([]);
const LinkedChildTableData = ref([]);
const Token = ref("")

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

function reloadPage() {
  window.location.reload()
}

onMounted(() => {
    loadInitialData();
    logout()
    Token.value = route.query.ftid;
    if (Token.value) {
        fetchData();
    }
});

const loadInitialData = () => {
    if (selectedData.value.main_form_Id) {
        gettingDataToLink();
    }
    // formDefinations();
    const storedData = localStorage.getItem("employeeData");
    if (storedData) {
        employeeData.value = JSON.parse(storedData);
    }
};

function logout() {
  axiosInstance.post(apis.logout)
    .then((response) => {
      if (response) {
        localStorage.clear();
        sessionStorage.clear();
      }
    })
}

const fetchDetails=ref("");

function fetchData() {
    const data = {
        token: Token.value,
    };

    axiosInstance
        .get(apis.getQrCodeData, { params: data })
        .then((res) => {
            fetchDetails.value=res.message.data;
            const form_json = res.message.data.form_json;

            blockArr.value = rebuildToStructuredArray(JSON.parse(form_json).fields);
            // if (selectedData.value.selectedFormId) {
            //     WfRequestUpdate();
            // }
            blockArr.value.splice(1);

            const parsedFormJson = JSON.parse(form_json);
            tableName.value = parsedFormJson.fields.filter(
                (field) => field.fieldtype === "Table"
            );
            childTableName.value = tableName.value[0]?.options.replace(/_/g, " ");

            const originalChildTableFields = parsedFormJson.child_table_fields;
            const transformedChildTableFields = {};

            for (const key in originalChildTableFields) {
                const lowerKey = key.toLowerCase();
                transformedChildTableFields[lowerKey] = originalChildTableFields[key];
            }

            tableHeaders.value = transformedChildTableFields;

        })
        .catch((error) => {
            console.error("Error fetching records:", error);
        })
}

watch(business_unit, (newBu, oldBu) => {
    console.log(newBu);

    if (oldBu) {
        deptData(true);
    } else {
        deptData();
    }
});

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
        document_type: route.query.selectedForm,
        property: business_unit.value,
        //  status: route.query.selectedFormStatus === 'Request Cancelled' ? 'Request Raised' : null,
        // current_level:route.query.selectedFormStatus === 'Request Cancelled' ? 1 : null
    };
    axiosInstance.post(apis.edit_form_before_approve, data_obj).then((resp) => {
        if (resp?.message?.success === true) {
            toast.success(resp.message.message, {
                autoClose: 2000,
                transition: "zoom",
                onClose: () => {
                    router.push({ path: "/todo/raisedbyme" });
                },
            });
        } else {
            toast.error(resp.message.message || "Failed to update request", {
                autoClose: 2000,
                transition: "zoom",
            });
        }
    });
}

function clearFrom() {
    emittedFormData.value = []
    window.location.reload()
    tableRows.value = []
}

function deptData(value = null) {
    const filters = [["business_unit", "=", `${business_unit.value}`]];
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

// function formDefinations() {
//     const filters = [["business_unit", "like", `%${selectedData.value.selectedBusiness_unit}%`]];
//     if (selectedData.value.selectedCategory) {
//         filters.push([
//             "form_category",
//             "like",
//             `${selectedData.value?.selectedCategory}`,
//         ]);
//     }
//     if (selectedData.value.selectedform || selectedData.value.linkedDocName) {
//         filters.push([
//             "form_short_name",
//             "=",
//             `${selectedData.value?.selectedform || selectedData.value.linkedDocName}`,
//         ]);
//     }

//     const queryParams = {
//         fields: JSON.stringify(["*"]),
//         limit_page_length: 'None',
//         limit_start: filterObj.value.limit_start,
//         filters: JSON.stringify(filters),
//         order_by: "`tabEzy Form Definitions`.`creation` desc",
//     };

//     axiosInstance
//         .get(`${apis.resource}${doctypes.EzyFormDefinitions || selectedData.value.linkedDocName}`, {
//             params: queryParams,
//         })
//         .then((res) => {
//             checkingIs_linked.value = res.data[0];
//             const form_json = res.data[0].form_json;

//             blockArr.value = rebuildToStructuredArray(JSON.parse(form_json).fields);
//             if (selectedData.value.selectedFormId) {
//                 WfRequestUpdate();
//             }
//             blockArr.value.splice(1);

//             const parsedFormJson = JSON.parse(form_json);
//             tableName.value = parsedFormJson.fields.filter(
//                 (field) => field.fieldtype === "Table"
//             );
//             childTableName.value = tableName.value[0]?.options.replace(/_/g, " ");

//             const originalChildTableFields = parsedFormJson.child_table_fields;
//             const transformedChildTableFields = {};

//             for (const key in originalChildTableFields) {
//                 const lowerKey = key.toLowerCase();
//                 transformedChildTableFields[lowerKey] = originalChildTableFields[key];
//             }

//             tableHeaders.value = transformedChildTableFields;
//             initializeTableRows();
//         })
//         .catch((error) => {
//             console.error("Error fetching ezyForms data:", error);
//         });
// }

function initializeTableRows() {
    if (tableHeaders.value?.length > 0) {
        const newRow = Object.fromEntries(
            tableHeaders.value?.map((field) => [field.fieldname, ""])
        );
        childtablesData.value.push(newRow);
    }
}

function handleTableData(data) {
  childtablesData.value = data;
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
            } else {
                console.error("file_url not found in the response.");
            }
        })
        .catch((error) => {
            console.error("Upload error:", error);
        });
};
const handleFieldUpdate = (field) => {
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

const linkedId = ref("");

const childRef = ref(null);
const raiseResponse=ref("");

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

    const childEntries = Object.entries(childtablesData.value);

    const form = {
        // doctype: selectedData.value.selectedform
        //     ? selectedData.value.selectedform
        //     : selectedData.value.linkedDocName,
        // company_field: business_unit.value,
    };


    // Append all child tables
    childEntries.forEach(([tableName, rows]) => {
        if (rows && rows.length) {
            form[tableName.toLowerCase().replace(/ /g,"_")] = rows;
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
    formData.append("save_doc", JSON.stringify(form));
    formData.append("token", Token.value);

    try {
        const response = await axiosInstance.post(apis.getQrCodeData, formData);
        raiseResponse.value=response.message.message;
        if (raiseResponse.value) {
            // request_raising_fn(response);
            const modal = bootstrap.Modal.getInstance(document.getElementById('ExportEmployeeModal'));
            modal.hide();
        } else {
            console.error("Submission successful but no response data.");
        }
    } catch (error) {
        console.error("❌ Error submitting main form:", error);
    }
}

function gettingDataToLink() {
    const dataObj = {
        wf_request: selectedData.value.main_form_Id,
    };

    axiosInstance
        .post(apis.gettingDataTo, dataObj)
        .then((response) => {
            const responseData = response.message;
            linkedId.value = responseData.returnable_gate_pass_id;

            const tableKey = Object.keys(responseData).find(
                (key) => key !== 'returnable_gate_pass_id'
            );

            if (tableKey) {
                LinkedChildTableData.value = {
                    table_name: tableKey,
                    rows: responseData[tableKey],
                };
            }
        })
        .catch((error) => {
            console.error("Error fetching data:", error);
        });
}
const child_id_name = ref((''))

// function WfRequestUpdate() {
//     const filters = [
//         [
//             "wf_generated_request_id",
//             "like",
//             `%${selectedData.value.selectedFormId}%`,
//         ],
//     ];

//     const queryParams = {
//         fields: JSON.stringify(["*"]),
//         limit_page_length: null,
//         limit_start: 0,
//         filters: JSON.stringify(filters),
//         order_by: `\`tab${selectedData.value.selectedform}\`.\`creation\` desc`,
//     };

//     axiosInstance
//         .get(`${apis.resource}${selectedData.value.selectedform}`, {
//             params: queryParams,
//         })
//         .then((res) => {
//             if (res.data && res.data.length > 0) {
//                 const doctypeForm = res.data[0];

//                 mapFormFieldsToRequest(doctypeForm, blockArr.value);

//                 axiosInstance
//                     .get(`${apis.resource}${selectedData.value.selectedform}`)
//                     .then((res) => {
//                         newMainId.value = res.data[0].name

//                     })
//                     .catch((error) => {
//                         console.error(`Error fetching data for :`, error);
//                     });
//                 axiosInstance
//                     .get(
//                         `${apis.resource}${selectedData.value.selectedform}/${res.data[0].name}`
//                     )
//                     .then((res) => {
//                         const childTables = Object.keys(res.data).filter((key) =>
//                             Array.isArray(res.data[key])
//                         );

//                         if (childTables.length) {
//                             tableRows.value = {};

//                             childTables.forEach((tableKey) => {
//                                 tableRows.value[tableKey] = res.data[tableKey] || [];
//                             });
//                             child_id_name.value = res.data.name
//                         }
//                     })
//                     .catch((error) => {
//                         console.error(`Error fetching data for :`, error);
//                     });
//             }
//         })
//         .catch((error) => {
//             console.error("Error fetching data:", error);
//         });
// }

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
// function request_raising_fn(item) {
//     const ItemData=item.message

//     saveloading.value = true;
//     // console.log(filepaths.value, "---filepaths");
//     // const filesArray = filepaths.value
//     //   ? filepaths.value.split(",").map((filePath) => filePath.trim())
//     //   : [];
//     let data_obj = {
//         module_name: "Ezy Forms",
//         doctype_name: ItemData.doctype_name,
//         ids: [ItemData.docname],
//         reason: selectedData.value.hasWorkflow === 'No' ? "Completed" : "Request Raised Via QR Code",
//         url_for_request_id: "",
//         files: [],
//         property: fetchDetails.value.business_unit,
//         employee_id: employeeData.value.emp_code,
//         be_half_of: ItemData.request_for === 'Others' ? ItemData.employee_name : '',
//         request_for: ItemData.request_for,
//         unwanted_files: removeAttachFiles.value
//     };


//     axiosInstance.post(apis.raising_request, data_obj).then((resp) => {
//         if (resp?.message?.success === true) {
//             if (selectedData.value.main_form_Id) {
//                 linked_id_adding_method(item.name)
//             }
//             const modal = bootstrap.Modal.getInstance(
//                 document.getElementById("ExportEmployeeModal")
//             );
//             modal.hide();

//             toast.success(resp?.message?.message, {
//                 autoClose: 1000,
//                 transition: "zoom",
//             });
//         }
//     })
//         .catch((error) => {
//             console.error("Error raising request:", error);
//             toast.error("Error raising request");
//         })
//         .finally(() => {
//             saveloading.value = false;
//         });
// }

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

</script>

<style lang="scss" scoped>
.zindex-dropdown {
    z-index: 1050;
    max-height: 200px;
    overflow-y: auto;
}

.requestPreviewDiv {
    height: 80vh;
    overflow-y: auto;
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

.Acknowledgement-check {
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
@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translateY(-20px);
  }
  100% {
    opacity: 1;
    transform: translateY(0);
  }
}

.res_div {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f0f0f0;
  color: #389e0d;
  font-size: 18px;
  animation: fadeIn 3s ease forwards;
}
.res_message{
  padding: 25px 25px;
  border: 1px solid #b7eb8f;
  border-radius: 12px;
  box-shadow: 0 3px 8px rgba(183, 235, 143, 0.24);
}
.add-res-btn{
    padding: 0px 13px;
    font-size: 12px;
    border: 1px solid blue;
    color: blue;
    border-radius: 20px;
}
</style>