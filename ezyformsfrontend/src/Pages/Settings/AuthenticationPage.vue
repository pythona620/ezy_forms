<template>
    <div class="p-1 mt-3">
        <h1 class="m-0 font-13 mb-3">Settings</h1>
        <table class="table">
            <thead>
                <tr>
                    <th>S.No</th>
                    <th>Title</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in tableData" :key="index">
                    <td>{{ index + 1 }}</td>
                    <td>{{ item.title }}</td>
                    <td>
                        <div class="form-check form-switch">
                            <input class="form-check-input shadow-none" type="checkbox" role="switch"
                                :checked="item.checked" @click.prevent="handleToggle(index)" />
                            <label class="form-check-label mt-1">
                                {{ item.checked ? "Enabled" : "Disabled" }}
                            </label>
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>

        <!-- Modal -->
        <div class="modal fade" id="EnableDisable" tabindex="-1" aria-labelledby="EnableDisableLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="EnableDisableLabel">Confirm Action</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" @click="closeModal"></button>
                    </div>
                    <div class="modal-body">
                        {{ confirmMessage }}
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-secondary" data-bs-dismiss="modal" @click="closeModal">Close</button>
                        <button type="button" class="btn btn-dark" @click="confirmAction">Yes, Proceed</button>
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
const tableData = ref([
    { title: "Two Factor Authentication", checked: false },
    { title: "Send Form as an Attachment Via an E-Mail ", checked: false },
    { title: "Welcome E-Mail Configuration", checked: false },
    { title: "Enable Sign Up in Login Page", checked: false },
    { title: "Send Daily E-mail reminders", checked: false },
    { title: "Take Acknowledgement and Signiture while Login", checked: false },
    { title: "Take Signiture while Sig Up", checked: false },
]);

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
    }

    // Show the modal
    const modal = new bootstrap.Modal(document.getElementById('EnableDisable'));
    modal.show();
};

const closeModal = () => {
    // Revert checkbox state if the modal is closed or canceled
    tableData.value[selectedRowData.value].checked = originalCheckedState.value;
};

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
                toast.success(`Two Factor Authentication ${newStatus === 0 ? "Disabled" : "Enabled"} Successfully!`, { autoClose: 700 });
                const modal = bootstrap.Modal.getInstance(document.getElementById('EnableDisable'));
                    modal.hide();
                enable_two_factor();
            })
            .catch(() => {
                toast.error("Failed to update Two Factor Authentication!");
            });
    } else if (index === 1) {
        axiosInstance
            .put(`${apis.resource}${doctypes.wfSettingEzyForms}/${encodeURIComponent(docName)}`, {
                send_form_as_a_attach_through_mail: newStatus,
            })
            .then(() => {
                toast.success(`Send Form As an Attachment Through Mail ${newStatus === 0 ? "Disabled" : "Enabled"} Successfully!`, { autoClose: 700 });
                const modal = bootstrap.Modal.getInstance(document.getElementById('EnableDisable'));
                    modal.hide();
                    BussinesUnit()
            })
            .catch(() => {
                toast.error("Failed to update Send Form As an Attachment Through Mail!");
            });
    } else if (index === 2) {
        if (default_mail.value === true) {
            axiosInstance
                .put(`${apis.resource}${doctypes.wfSettingEzyForms}/${encodeURIComponent(docName)}`, {
                    welcome_mail_to_employee: newStatus,
                })
                .then(() => {
                    toast.success(`Welcome Mail Configuration ${newStatus === 0 ? "Disabled" : "Enabled"} Successfully!`, { autoClose: 700 });
                    const modal = bootstrap.Modal.getInstance(document.getElementById('EnableDisable'));
                    modal.hide();
                    BussinesUnit()
                })
                .catch(() => {
                    toast.error("Failed to update Welcome Mail Configuration!");
                });
        } else {
            toast.info("Please Configure Default Mail First!");
            tableData.value[index].checked = false;
        }
    } else if (index === 3) {
        axiosInstance
            .put(`${apis.resource}${doctypes.websiteSettings}/${encodeURIComponent("Website Settings")}`, {
                disable_signup: webSiteStatus,
            })
            .then(() => {
                toast.success(`Sign up ${webSiteStatus === 1 ? "Disabled" : "Enabled"} Successfully!`, { autoClose: 700 });
                const modal = bootstrap.Modal.getInstance(document.getElementById('EnableDisable'));
                modal.hide();
                signUp();
            })
            .catch(() => {
                toast.error("Failed to update Sign up!");
            });
    } else if (index === 4) {
        axiosInstance
            .put(`${apis.resource}${doctypes.wfSettingEzyForms}/${encodeURIComponent(docName)}`, {
                send_daily_alerts: newStatus,
            })
            .then(() => {
                toast.success(`daily email reminders ${newStatus === 0 ? "Disabled" : "Enabled"} Successfully!`, { autoClose: 700 });
                const modal = bootstrap.Modal.getInstance(document.getElementById('EnableDisable'));
                    modal.hide();
                    BussinesUnit()
            })
            .catch(() => {
                toast.error("Failed to update E-Mail Send Daily reminders");
            });
    } else if (index === 5) {
        axiosInstance
            .put(`${apis.resource}${doctypes.wfSettingEzyForms}/${encodeURIComponent(docName)}`, {
                is_acknowledge: newStatus,
            })
            .then(() => {
                toast.success(`acknowledgement and Signiture ${newStatus === 0 ? "Disabled" : "Enabled"} Successfully!`, { autoClose: 700 });
                const modal = bootstrap.Modal.getInstance(document.getElementById('EnableDisable'));
                    modal.hide();
                    BussinesUnit()
            })
            .catch(() => {
                toast.error("Failed to update acknowledgement");
            });
    } else if (index === 6) {
        axiosInstance
            .put(`${apis.resource}${doctypes.wfSettingEzyForms}/${encodeURIComponent(docName)}`, {
                signature_required: newStatus,
            })
            .then(() => {
                toast.success(`Signiture while Sig Up ${newStatus === 0 ? "Disabled" : "Enabled"} Successfully!`, { autoClose: 700 });
                const modal = bootstrap.Modal.getInstance(document.getElementById('EnableDisable'));
                    modal.hide();
                    BussinesUnit()
            })
            .catch(() => {
                toast.error("Failed to update Signiture while Sig Up");
            });
    }
};



function BussinesUnit() {
    // const queryParams = {
    //     fields: JSON.stringify(["*"]),
    //     filters: JSON.stringify([["name", "=", Bussines_unit.value]])
    // };

    // axiosInstance
    //     .get(`${apis.resource}${doctypes.wfSettingEzyForms}`, { params: queryParams })
    //     .then((res) => {
    //         if (res.data.length > 0) {
    //             const status = res.data[0].send_form_as_a_attach_through_mail;
    //             tableData.value[1].checked = status == 1;
    //             const welcome_mail = res.data[0].welcome_mail_to_employee;
    //             tableData.value[2].checked = welcome_mail == 1;
    //             const send_daily_alerts = res.data[0].send_daily_alerts;
    //             tableData.value[4].checked = send_daily_alerts == 1;
    //             const is_acknowledge = res.data[0].is_acknowledge;
    //             tableData.value[5].checked = is_acknowledge == 1;
    //             const signature_required = res.data[0].signature_required;
    //             tableData.value[6].checked = signature_required == 1;
    //         }
    //     })
    //     .catch((error) => {
    //         console.error("Error fetching business unit settings:", error);
    //     });

    const queryParamse = {
        fields: ["name", "bu_code", "send_form_as_a_attach_through_mail", "welcome_mail_to_employee", "send_daily_alerts", "is_acknowledge", "signature_required"],
        filters:[["name",'=',Bussines_unit.value]],
        doctype:doctypes.wfSettingEzyForms,
        limit_page_length:"none",

    };
    axiosInstance.post(apis.GetDoctypeData, queryParamse)
    .then((res) => {
        if (res?.message) {
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
        }
    }).catch((error) => {
        console.error("Error fetching ezyForms data:", error);
    });

};

const enable_two_factor = () => {
    const docName = "System Settings";
    const queryParams = {
        fields: JSON.stringify(["*"]),
    };

    axiosInstance
        .get(`${apis.resource}${doctypes.SystemSettings}/${encodeURIComponent(docName)}`, { params: queryParams })
        .then((res) => {
            if (res.data) {

                tableData.value[0].checked = res.data.enable_two_factor_auth == 1;
            }
        })
        .catch((error) => {
            console.error("Error fetching system settings:", error);
        });
};

const signUp = () => {
    const docName = "Website Settings";
    const queryParams = {
        fields: JSON.stringify(["*"]),
    };

    axiosInstance
        .get(`${apis.resource}${doctypes.websiteSettings}/${encodeURIComponent(docName)}`, { params: queryParams })
        .then((res) => {
            if (res.data) {
                tableData.value[3].checked = res.data.disable_signup == 0;
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
    };

    axiosInstance
        .get(`${apis.resource}${doctypes.Email_Account}`, { params: queryParams })
        .then((res) => {
            if (res.data && res.data.length > 0) {
                const emailData = res.data[0];
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
.table {
    width: 100%;
    white-space: nowrap;
    font-size: var(--font-size-xs);
    font-weight: 400;
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
}
</style>
