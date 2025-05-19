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
import { ref, onMounted } from "vue";
import axiosInstance from "../../shared/services/interceptor";
import { apis, doctypes } from "../../shared/apiurls";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";

const tableData = ref([
    { title: "Two Factor Authentication", checked: false },
    { title: "Send Form as an Attachment Via an E-Mail ", checked: false },
    { title: "Welcome E-Mail Configuration", checked: false },
]);

const default_mail = ref(false);
const selectedRowData = ref(null);  // stores index
const selectedCheckedState = ref(false); // stores checkbox state before toggle
const confirmMessage = ref('');  // dynamic message
const originalCheckedState = ref(false); // stores initial checkbox state

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
    console.log(selectedCheckedState.value);
    const newStatus = isChecked ? 1 : 0;

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
    }
};



const BussinesUnit = () => {
    const buData = localStorage.getItem('Bu') || ''; // Ensure buData is parsed correctly

    const queryParams = {
        fields: JSON.stringify(["*"]),
        filters: JSON.stringify([["bu_name", "=", buData]]) // Apply filter based on buData
    };

    axiosInstance
        .get(`${apis.resource}${doctypes.wfSettingEzyForms}`, { params: queryParams })
        .then((res) => {
            if (res.data.length > 0) {
                const status = res.data[0].send_form_as_a_attach_through_mail;
                tableData.value[1].checked = status == 1; // Check if 0, uncheck if 1
                const welcome_mail = res.data[0].welcome_mail_to_employee;
                tableData.value[2].checked = welcome_mail == 1; // Check if 0
            }
        })
        .catch((error) => {
            console.error("Error fetching business unit settings:", error);
        });
};

const enable_two_factor = () => {
    const docName = "System Settings"; // Document name
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
                console.log(emailData, "response");

                if (emailData.default_outgoing === 1 && emailData.enable_outgoing === 1) {
                    default_mail.value = true;
                } else {
                    default_mail.value = false;
                }

                console.log(typeof default_mail.value, default_mail.value);
            } else {
                default_mail.value = false;
            }
        })
        .catch((error) => {
            console.error("Error fetching system settings:", error);
        });
};

onMounted(() => {
    enable_two_factor();
    BussinesUnit();
    email_account()

});
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
