<template>
    <div class="p-1 mt-3">
        <h1 class="m-0 font-13 mb-3">Two Factor Authentication</h1>
        <table class="table">
            <thead>
                <tr>
                    <th>S.No</th>
                    <th>Title</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="(item, index) in tableData" :key="index">
                    <td>{{ index + 1 }}</td>
                    <td>{{ item.title }}</td>
                    <td>
                        <!-- <input type="checkbox" v-model="item.checked" @change="handleToggle(index)" /> -->
                        <input class="form-check-input shadow-none" type="checkbox" role="switch" v-model="item.checked"
                            @change="handleToggle(index)" />
                    </td>
                </tr>
            </tbody>
        </table>
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
    { title: "send Form As a Attach Through Mail", checked: false },

]);

const employeeData = () => {
    const docName = "System Settings"; // Document name
    const queryParams = {
        fields: JSON.stringify(["*"]),
    };

    axiosInstance
        .get(`${apis.resource}${doctypes.SystemSettings}/${encodeURIComponent(docName)}`, { params: queryParams })
        .then((res) => {
            if (res.data) {
                // console.log("res.data", res.data.enable_two_factor_auth);

                // Set the checkbox state based on API response
                tableData.value[0].checked = res.data.enable_two_factor_auth == 1;
            }
        })
        .catch((error) => {
            console.error("Error fetching system settings:", error);
        });
};

// const handleToggle = (index) => {
//     if (index !== 0) return; // Only update for Two Factor Authentication

//     const docName = "System Settings";
//     const newStatus = tableData.value[index].checked ? 1 : 0;

//     axiosInstance
//         .put(`${apis.resource}${doctypes.SystemSettings}/${encodeURIComponent(docName)}`, {
//             enable_two_factor_auth: newStatus,
//         })
//         .then(() => {
//             toast.success(`Two Factor Authentication ${newStatus ? "Enabled" : "Disabled"} Successfully!`, { autoClose: 700 });
//         })
//         .catch(() => {
//             toast.error("Failed to update Two Factor Authentication!");
//         });
// };


const handleToggle = (index) => {
    const docName = index === 0 ? "System Settings" : localStorage.getItem("Bu") || "";

    if (!docName) return; // Prevent API call if docName is empty

    if (index === 0) {
        // Handle Two Factor Authentication
        const newStatus = tableData.value[index].checked ? 1 : 0;
        axiosInstance
            .put(`${apis.resource}${doctypes.SystemSettings}/${encodeURIComponent(docName)}`, {
                enable_two_factor_auth: newStatus,
            })
            .then(() => {
                toast.success(`Two Factor Authentication ${newStatus ? "Enabled" : "Disabled"} Successfully!`, { autoClose: 700 });
            })
            .catch(() => {
                toast.error("Failed to update Two Factor Authentication!");
            });
    } else if (index === 1) {
        // Handle Send Form As a Attach Through Mail
        const newStatus = tableData.value[index].checked ? 1 : 0; // Toggle value
        const queryParams = {
            send_form_as_a_attach_through_mail: newStatus,
        };

        axiosInstance
            .put(`${apis.resource}${doctypes.wfSettingEzyForms}/${encodeURIComponent(docName)}`, queryParams)
            .then(() => {
                toast.success(`Send Form As a Attach Through Mail ${newStatus ? "Disabled" : "Enabled"} Successfully!`, { autoClose: 700 });
            })
            .catch(() => {
                toast.error("Failed to update Send Form As a Attach Through Mail!");
            });
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
            }
        })
        .catch((error) => {
            console.error("Error fetching business unit settings:", error);
        });
};

onMounted(() => {
    employeeData();
    BussinesUnit();

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
