<template>
    <div class="main-div">
        <div class="py-2">
            <div class="card card-div border-0">
                <label for="fileInput" class="cursor-pointer w-25">
                    <img title="Upload Image" :src="userData?.profile_image ? userData.profile_image : defaultImage"
                        class="img-fluid profile-img" />
                </label>
                <input type="file" id="fileInput" @change="uploadImage" accept="image/*" hidden />

                <div class="d-flex justify-content-between align-items-end mt-2 ms-1">
                    <div>
                        <h6 class="mb-3 font-15">{{ userData.emp_name }}</h6>
                        <span><i class="bi bi-person-fill me-2"></i>{{ userData.emp_code }}</span>
                    </div>
                    <span><i class="bi bi-envelope-open-fill me-2"></i>{{ userData.emp_mail_id }}</span>
                    <span class="text-secondary">Designation: <strong>{{ userData.designation }}</strong></span>
                    <span class="text-secondary">Department: <strong>{{ userData.department }}</strong></span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { apis, doctypes } from "../../shared/apiurls";
import axiosInstance from "../../shared/services/interceptor";
import { onMounted, ref } from "vue";
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import defaultImage from "@/assets/UploadProfile.jpg";


const employeeData = ref({});
const email = ref("");
const userData = ref([])
// const defaultImage = "../../assets/UploadProfile.jpg"; // Default profile image

function userDetails(empEmail) {
    axiosInstance
        .get(`${apis.resource}${doctypes.EzyEmployeeList}/${empEmail}`)
        .then((res) => {
            userData.value = res.data
        })
        .catch((error) => {
            console.error("Error fetching user data:", error);
        });
}

function uploadImage(event) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("file", file);

    axiosInstance
        .post(apis.uploadfile, formData)
        .then((res) => {
            const imageUrl = res.message.file_url;

            return axiosInstance.put(
                `${apis.resource}${doctypes.EzyEmployeeList}/${userData.value.name}`,
                { profile_image: imageUrl }
            );
        })
        .then(() => {
            userDetails(userData.value.name);
            toast.success('Profile Updated Successfully', { autoClose: 300 });
        })
        .catch((error) => {
            console.error("Error uploading image:", error);
        });
}



onMounted(() => {
    employeeData.value = JSON.parse(localStorage.getItem('employeeData')) || {};
    email.value = employeeData.value.emp_mail_id || "";

    if (email.value) {
        userDetails(email.value);
    }
});
</script>

<style scoped>
.main-div {
    background-color: #fafafa;
}

.card-div {
    box-shadow: 0px 0px 4px 0px #00000040;
    border-radius: 2px;
    background: #FFFFFF;
    padding: 25px;
}

.profile-img {
    width: 80px;
    border: 1px solid #c9c9c9;
    padding: 5px;
    border-radius: 7px;
}

span {
    font-size: 14px;
    font-weight: 500;
    line-height: 19.5px;

}
</style>