<template>
    <div class="p-1 mt-3">
        <h1 class="m-0 font-13 mb-3">Settings</h1>
          <table class="table">
    <thead>
      <tr>
        <th class="px-2 text-center" >S.No</th>
        <th>Title</th>
        <th class="text-end">About</th>
        <th width="15%" class="text-end pe-5">Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item, index) in tableData" :key="index">
        <td>{{ index + 1 }}</td>
        <td>{{ item.title }}</td>

        <!-- 🟦 About Column -->
        <td class=" text-end align-middle pe-3">
          <i
            class="bi bi-info-circle text-primary cursor-pointer"
            v-tooltip.top="item.about"
          ></i>
        </td>

        <td class=" px-4 text-end">
          <div v-if="item.title === 'Company Logo'">
            <div @click="handleToggle(index)" class="d-flex align-items-center justify-content-end font-12 gap-3 pe-3">
              <i class="bi bi-eye mx-2 font-13"></i>View
            </div>
          </div>

          <div v-else class="d-flex justify-content-end align-items-center gap-2 ">
            <div class="form-check form-switch ">

            <input
              class="form-check-input shadow-none"
              type="checkbox"
              role="switch"
              :checked="item.checked"
              @click.prevent="handleToggle(index)"
            />
            </div>
            <label class="form-check-label mt-1">
              {{ item.checked ? "Enabled" : "Disabled" }}
            </label>
          </div>
        </td>
      </tr>
    </tbody>
  </table>
        <!-- Modal -->
        <div class="modal fade" id="EnableDisable" tabindex="-1" data-bs-backdrop="static" aria-labelledby="EnableDisableLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="EnableDisableLabel">{{ viewImage ? 'Company Logo' : 'Confirm Action' }}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="closeModal"></button>
                    </div>
                    <div class="modal-body">
                        <div v-if="viewImage" class="logo-upload text-center">
                            <label class="btn btn-outline-secondary upload-label">
                                <i class="bi bi-upload"></i> Upload Logo
                                <input type="file" accept="image/*" id="logoInput" @change="previewLogo($event, index)"
                                    hidden />
                            </label>

                            <div v-if="companyLogo" for="logoInput" class="logo-preview mt-3 position-relative">
                                <img :src="companyLogo" alt="Company Logo" class="img-thumbnail rounded shadow"
                                    width="100" />

                                <button type="button" class="btn-close position-absolute top-0 end-10 font-12"
                                    aria-label="Close" @click="companyLogo = null">
                                </button>
                            </div>
                        </div>

                        <div v-else>
                            {{ confirmMessage }}
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal" @click="closeModal">Close</button>
                        <button type="button" class="btn btn-dark" @click="confirmAction">
                            {{ viewImage ? 'Submit' : 'Yes, Proceed' }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, computed,onMounted } from "vue";
import axiosInstance from "../../shared/services/interceptor";
import { apis, doctypes } from "../../shared/apiurls";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import { showError, showInfo, showSuccess } from "../../shared/services/toast";
const tableData = ref([
  { title: "Two Factor Authentication", checked: false, about: "User need to scan QR code using Google Authenticator and set his two factor Authentication." },
  { title: "Send Form as an Attachment Via an E-Mail", checked: false, about: "When a request is raised, an email will be triggered to all the approval members with form as an attachment." },
  { title: "Welcome E-Mail Configuration", checked: false, about: "An email will be sent to the new user." },
  { title: "Enable Sign Up in Login Page", checked: false, about: "In login page Sign up screen will be enabled so that new user can register them self." },
  { title: "Send Daily E-mail reminders", checked: false, about: "Team members will receive a daily morning notification containing a list of pending forms that require their attention." },
  { title: "Take Acknowledgement and Signature while Login", checked: false, about: "A message will be displayed at the time of Sign in by the user to Acknowledge and Sign at the time of login." },
  { title: "Take Signature while Sign Up", checked: false, about: "When enabled user need to submit his signature before doing any activity in the application." },
  { title: "Allow Approver to Edit Form?", checked: false, about: "When enabled approver can edit the form." },
  { title: "Company Logo", checked: false, about: "You can upload the company logo." },
]);
const companyLogo = ref("");
const viewImage = ref(false);
const default_mail = ref(false);
const selectedRowData = ref(null);  // stores index
const selectedCheckedState = ref(false); // stores checkbox state before toggle
const confirmMessage = ref('');  // dynamic message
const originalCheckedState = ref(false); // stores initial checkbox state
const Bussines_unit = ref('')
const businessUnit = computed(() => {
  return EzyBusinessUnit.value;
});

onMounted(() => {
    signUp();
});



const handleToggle = (index) => {
    selectedRowData.value = index;
    selectedCheckedState.value = tableData.value[index].checked;
    originalCheckedState.value = selectedCheckedState.value; // Save the initial state

    const isChecked = selectedCheckedState.value === false ? 1 : 0;

    // Set the dynamic confirmation message
    if (index === 0) {
        confirmMessage.value = isChecked
            ? "Are you sure you want to enable Two Factor Authentication?"
            : "Are you sure you want to disable Two Factor Authentication?";
    } else if (index === 1) {
        confirmMessage.value = isChecked
            ? "Are you sure you want to enable Send Form As an Attachment Through E-Mail?"
            : "Are you sure you want to disable Send Form As an Attachment Through E-Mail?";
    } else if (index === 2) {
        confirmMessage.value = isChecked
            ? "Are you sure you want to enable E-Mail Configuration?"
            : "Are you sure you want to disable E-Mail Configuration?";
    } else if (index === 3) {
        confirmMessage.value = isChecked
            ? "Are you sure you want to enable Sign up?"
            : "Are you sure you want to disable Sign up?";
    } else if (index === 4) {
        confirmMessage.value = isChecked
            ? "Are you sure you want to enable daily email reminders?"
            : "Are you sure you want to disable daily email reminders?";
    } else if (index === 5) {
        confirmMessage.value = isChecked
            ? "Are you sure you want to enable Acknowledgement and Signiture while Login?"
            : "Are you sure you want to disable Acknowledgement and Signiture while Login?";
    } else if (index === 6) {
        confirmMessage.value = isChecked
            ? "Are you sure you want to enable Signiture while Sig Up?"
            : "Are you sure you want to disable Signiture while Sig Up?";
    } else if (index === 7) {
        confirmMessage.value = isChecked
            ? "Are you sure you want to enable Approver Edit Form?"
            : "Are you sure you want to disable Approver Edit Form?";
    } else if (index === 8) {
        viewImage.value = true;
    }

    // Show the modal
    const modal = new bootstrap.Modal(document.getElementById('EnableDisable'));
    modal.show();
};

const closeModal = () => {
    // Revert checkbox state if the modal is closed or canceled
    tableData.value[selectedRowData.value].checked = originalCheckedState.value;
    viewImage.value = false;
};

const selectedFile = ref(null);

function previewLogo(event) {
    const file = event.target.files[0];
    if (file) {
        selectedFile.value = file;
        companyLogo.value = URL.createObjectURL(file);
    }
}

const confirmAction = () => {
    const index = selectedRowData.value;
    const isChecked = selectedCheckedState.value === false ? 1 : 0;
    const newStatus = isChecked ? 1 : 0;
    const webSiteStatus = isChecked ? 0 :1;

    // Toggle the checkbox state on confirm
    tableData.value[index].checked = !isChecked;

    // Define docName based on index
    const docName = index === 0 ? "System Settings" : localStorage.getItem("Bu") || "";

    if (index === 0) {
        axiosInstance
            .put(`${apis.resource}${doctypes.SystemSettings}/${encodeURIComponent(docName)}`, {
                enable_two_factor_auth: newStatus,
            })
            .then(() => {
                showSuccess(`Two Factor Authentication ${newStatus === 0 ? "Disabled" : "Enabled"} Successfully!`);
                const modal = bootstrap.Modal.getInstance(document.getElementById('EnableDisable'));
                    modal.hide();
                enable_two_factor();
            })
            .catch(() => {
                showError("Failed to update Two Factor Authentication!");
            });
    } else if (index === 1) {
        axiosInstance
            .put(`${apis.resource}${doctypes.wfSettingEzyForms}/${encodeURIComponent(docName)}`, {
                send_form_as_a_attach_through_mail: newStatus,
            })
            .then(() => {
                showSuccess(`Send Form As an Attachment Through Mail ${newStatus === 0 ? "Disabled" : "Enabled"} Successfully!`);
                const modal = bootstrap.Modal.getInstance(document.getElementById('EnableDisable'));
                    modal.hide();
                    BussinesUnit()
            })
            .catch(() => {
                showError("Failed to update Send Form As an Attachment Through Mail!");
            });
    } else if (index === 2) {
        if (default_mail.value === true) {
            axiosInstance
                .put(`${apis.resource}${doctypes.wfSettingEzyForms}/${encodeURIComponent(docName)}`, {
                    welcome_mail_to_employee: newStatus,
                })
                .then(() => {
                    showSuccess(`Welcome Mail Configuration ${newStatus === 0 ? "Disabled" : "Enabled"} Successfully!`);
                    const modal = bootstrap.Modal.getInstance(document.getElementById('EnableDisable'));
                    modal.hide();
                    BussinesUnit()
                })
                .catch(() => {
                    showError("Failed to update Welcome Mail Configuration!");
                });
        } else {
            showInfo("Please Configure Default Mail First!");
            tableData.value[index].checked = false;
        }
    } else if (index === 3) {
        axiosInstance
            .put(`${apis.resource}${doctypes.websiteSettings}/${encodeURIComponent("Website Settings")}`, {
                disable_signup: webSiteStatus,
            })
            .then(() => {
                showSuccess(`Sign up ${webSiteStatus === 1 ? "Disabled" : "Enabled"} Successfully!`);
                const modal = bootstrap.Modal.getInstance(document.getElementById('EnableDisable'));
                modal.hide();
                signUp();
            })
            .catch(() => {
                showError("Failed to update Sign up!");
            });
    } else if (index === 4) {
        axiosInstance
            .put(`${apis.resource}${doctypes.wfSettingEzyForms}/${encodeURIComponent(docName)}`, {
                send_daily_alerts: newStatus,
            })
            .then(() => {
                showSuccess(`daily email reminders ${newStatus === 0 ? "Disabled" : "Enabled"} Successfully!`);
                const modal = bootstrap.Modal.getInstance(document.getElementById('EnableDisable'));
                    modal.hide();
                    BussinesUnit()
            })
            .catch(() => {
                showError("Failed to update E-Mail Send Daily reminders");
            });
    } else if (index === 5) {
        axiosInstance
            .put(`${apis.resource}${doctypes.wfSettingEzyForms}/${encodeURIComponent(docName)}`, {
                is_acknowledge: newStatus,
            })
            .then(() => {
                showSuccess(`acknowledgement and Signiture ${newStatus === 0 ? "Disabled" : "Enabled"} Successfully!`);
                const modal = bootstrap.Modal.getInstance(document.getElementById('EnableDisable'));
                    modal.hide();
                    BussinesUnit()
            })
            .catch(() => {
                showError("Failed to update acknowledgement");
            });
    } else if (index === 6) {
        axiosInstance
            .put(`${apis.resource}${doctypes.wfSettingEzyForms}/${encodeURIComponent(docName)}`, {
                signature_required: newStatus,
            })
            .then(() => {
                showSuccess(`Signiture while Sig Up ${newStatus === 0 ? "Disabled" : "Enabled"} Successfully!`);
                const modal = bootstrap.Modal.getInstance(document.getElementById('EnableDisable'));
                    modal.hide();
                    BussinesUnit()
            })
            .catch(() => {
                showError("Failed to update Signiture while Sig Up");
            });
    }
    else if (index === 7) {
        axiosInstance
            .put(`${apis.resource}${doctypes.wfSettingEzyForms}/${encodeURIComponent(docName)}`, {
                allow_approver_to_edit_form: newStatus,
            })
            .then(() => {
               showSuccess(`Approver’s ability to edit the form has been ${newStatus === 0 ? "disabled" : "enabled"} successfully!`);
                sessionStorage.setItem("allow_approver_to_edit_form", newStatus);
                const modal = bootstrap.Modal.getInstance(document.getElementById('EnableDisable'));
                    modal.hide();
                    BussinesUnit()
            })
            .catch(() => {
                showError("Failed to update Approver Edit Form");
            });
        }
     else if (index === 8) {
        if (!selectedFile.value) return;
        const formData = new FormData();
        formData.append("file", selectedFile.value);

        axiosInstance
        .post(apis.uploadfile, formData)
        .then((res) => {
            const imageUrl = res.message.file_url;
            const payload = {
              bu_logo: imageUrl,
              doctype: doctypes.wfSettingEzyForms,
              name:docName,
            };

            return axiosInstance.put(`${apis.DataUpdate}`,payload);
        })
         .then((res) => {
            if (res.message?.success) {
                showSuccess("Logo Updated Successfully");
                const modal = bootstrap.Modal.getInstance(document.getElementById('EnableDisable'));
                modal.hide();
            }
            else{
                showError(res.message?.message);
            }
        })
        .catch((error) => {
            console.error("Error uploading image:", error);
        });
    }
};



function BussinesUnit() {
    const queryParamse = {
        fields: JSON.stringify(["name", "bu_logo", "bu_code", "send_form_as_a_attach_through_mail", "welcome_mail_to_employee", "send_daily_alerts", "is_acknowledge", "signature_required","allow_approver_to_edit_form"]),
        filters:JSON.stringify([["name",'=',Bussines_unit.value]]),
        doctype:doctypes.wfSettingEzyForms,
        limit_page_length:"none",

    };
    axiosInstance.get(apis.GetDoctypeData,  { params: queryParamse })
    .then((res) => {
        if (res?.message) {
            companyLogo.value = res.message.data[0].bu_logo;
            const status = res.message.data[0].send_form_as_a_attach_through_mail;
            tableData.value[1].checked = status == 1;
            const welcome_mail = res.message.data[0].welcome_mail_to_employee;
            tableData.value[2].checked = welcome_mail == 1;
            const send_daily_alerts = res.message.data[0].send_daily_alerts;
            tableData.value[4].checked = send_daily_alerts == 1;
            const is_acknowledge = res.message.data[0].is_acknowledge;
            tableData.value[5].checked = is_acknowledge == 1;
            const signature_required = res.message.data[0].signature_required;
            tableData.value[6].checked = signature_required == 1;
            const allow_approver_to_edit_form = res.message.data[0].allow_approver_to_edit_form;
            console.log(allow_approver_to_edit_form,'allow_approver_to_edit_form');
            tableData.value[7].checked = allow_approver_to_edit_form == 1;
        }
    }).catch((error) => {
        console.error("Error fetching ezyForms data:", error);
    });

};

const enable_two_factor = () => {
    const docName = "System Settings";
    const queryParams = {
        fields: JSON.stringify(["enable_two_factor_auth"]),
        doctype:doctypes.SystemSettings,
        doc_id:docName
    };

    axiosInstance
        .get(`${apis.GetDoctypeData}/${encodeURIComponent(docName)}`, { params: queryParams })
        .then((res) => {
            if (res.message.data) {

                tableData.value[0].checked = res.message.data.enable_two_factor_auth == 1;
            }
        })
        .catch((error) => {
            console.error("Error fetching system settings:", error);
        });
};

const signUp = () => {
    const docName = "Website Settings";
    const queryParams = {
        fields: JSON.stringify(["disable_signup"]),
        doctype:doctypes.websiteSettings,
        doc_id:docName,
    };

    axiosInstance
        .get(`${apis.GetDoctypeData}/${encodeURIComponent(docName)}`, { params: queryParams })
        .then((res) => {
            if (res.message.data) {
                tableData.value[3].checked = res.message.data.disable_signup == 0;
            }
        })
        .catch((error) => {
            console.error("Error fetching system settings:", error);
        });
};

const email_account = () => {
    const queryParams = {
        fields: JSON.stringify(["default_outgoing","enable_outgoing"]),
        filters: JSON.stringify([
            ["default_outgoing", "=", 1],
            ["enable_outgoing", "=", 1],
        ]),
        doctype:doctypes.Email_Account,
    };

    axiosInstance
        .get(`${apis.GetDoctypeData}`, { params: queryParams })
        .then((res) => {
            if (res.message.data && res.message.data.length > 0) {
                const emailData = res.message.data[0];
                // console.log(emailData, "response");

                if (emailData.default_outgoing === 1 && emailData.enable_outgoing === 1) {
                    default_mail.value = true;
                } else {
                    default_mail.value = false;
                }

                // console.log(typeof default_mail.value, default_mail.value);
            } else {
                default_mail.value = false;
            }
        })
        .catch((error) => {
            console.error("Error fetching system settings:", error);
        });
};

watch(
  businessUnit,
  (newVal) => {
    if (newVal && newVal.length) {
      Bussines_unit.value= newVal;
     
    BussinesUnit();
    email_account()
    enable_two_factor();
    }
  },
  { immediate: true }
);


</script>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
td:first-child,
th:first-child {
  width: 3%;
  text-align: center;
}
.table {
    width: 100%;
    white-space: nowrap;
    font-size: var(--font-size-xs);
    font-weight: 400;
}
.table>:not(caption)>*>* {
    padding: 6px;
}

th {
    background-color: #f2f2f2 !important;
    text-align: left;
    color: #999999 !important;
    font-size: 12px;
}

th,
td {
    max-width: 100px;
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
    color: var(--muted) !important;
    font-size: var(--twelve);
    vertical-align: middle;
    border-left: 1px solid #ececec !important;
}
tr:nth-child(even) td {
  background-color: #f9f9f9; /* Light gray background for even rows */
}

.upload-label {
    border: 1px solid #e7e1e1;
    padding: 7px 23px;
    border-radius: 10px;
    font-size: 13px;
    font-weight: 500;
    box-shadow: rgba(0, 0, 0, 0.1) 0px 0px 5px 0px, rgba(0, 0, 0, 0.1) 0px 0px 1px 0px;
}
.form-switch .form-check-input:checked {
  background-position: right center;
  background-color: rgb(103, 216, 109);
  border: 0;
}
</style>
