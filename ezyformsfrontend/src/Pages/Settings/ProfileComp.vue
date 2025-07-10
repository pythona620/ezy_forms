<template>
    <div class="main-div">
        <div class="py-2">
            <div class="card card-div border-0">
                <div class="position-relative d-inline-block">
                    <img :src="userData?.profile_image ? userData.profile_image : defaultImage"
                        title="Upload Profile Image" class="img-fluid profile-img border"
                        @click="triggerFileInput('profile')" style="cursor: pointer;" />
                    <i v-if="userData.profile_image" class="bi bi-pencil edit-profile-icon m-2"
                        @click="triggerFileInput('profile')" style="cursor: pointer;"></i>
                </div>

                <div class="d-flex justify-content-between align-items-end mt-2 ms-1">
                    <div>
                        <h6 class="mb-3 font-15">{{ userData.emp_name }}</h6>
                        <span><i class="bi bi-person-fill me-2"></i>{{ userData.emp_code }}</span>
                    </div>
                    <span><i class="bi bi-envelope-open-fill me-2"></i>{{ userData.emp_mail_id }}</span>
                    <span class="text-secondary">Designation: <strong>{{ userData.designation }}</strong></span>
                    <span class="text-secondary">Department: <strong>{{ userData.department }}</strong></span>
                    <span class="text-secondary">Acknowledged On: <strong>{{ userData.enable_on }}</strong></span>
                    <span class="text-secondary d-flex"><p class="mt-5 m-0 me-2">Signiture:</p>
                        <div class="position-relative d-inline-block " style="top:12px">
                            <img :src="userData?.signature ? userData.signature : defaultSign" title="Upload Signature"
                                class="img-fluid profile-img signiture-image border" @click="triggerFileInput('signature')"
                                style="cursor: pointer;" />
                            <i v-if="userData?.signature" class="bi bi-pencil edit-image m-2"
                                @click="triggerFileInput('signature')" style="cursor: pointer;"></i>
                        </div>

                        <!-- Hidden File Input -->
                        <input type="file" ref="fileInput" @change="uploadImage" accept="image/*" hidden />

                    </span>

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
import defaultSign from "@/assets/Sign.png";


const employeeData = ref({});
const email = ref("");
const userData = ref([])
// const defaultImage = "../../assets/UploadProfile.jpg"; // Default profile image 

const fileInput = ref(null);
const uploadType = ref('');


function triggerFileInput(type) {
    uploadType.value = type; // 'profile' or 'signature'
    fileInput.value.click();
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
            const payload = uploadType.value === 'profile'
                ? { profile_image: imageUrl }
                : { signature: imageUrl };

            return axiosInstance.put(
                `${apis.resource}${doctypes.EzyEmployeeList}/${userData.value.name}`,
                payload
            );
        })
        .then(() => {
            userDetails(userData.value.name);
            toast.success(`${uploadType.value === 'profile' ? 'Profile' : 'Signature'} Image Updated Successfully`, { autoClose: 300 });
        })
        .catch((error) => {
            console.error("Error uploading image:", error);
        });
}

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
.signiture-image{
    height: 50px;
}

.edit-image{
    position: absolute;
    top: -18px;
    left: 58px;
    background: black;
    border-radius: 13px;
    color: white;
    padding: 4px;
    font-size: 13px;
    height: 24px;
}
.edit-profile-icon{
    position: absolute;
    top: -15px;
    left: 58px;
    background: black;
    border-radius: 13px;
    color: white;
    padding: 4px;
    font-size: 13px;
    height: 25px;
}

span {
    font-size: 14px;
    font-weight: 500;
    line-height: 19.5px;

}

.signature-upload {
    max-width: 300px;
}

.preview-section img {
    max-width: 100%;
    height: auto;
}
</style>