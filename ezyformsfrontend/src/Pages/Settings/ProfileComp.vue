<template>
    <div class="main-div">
        <div class="py-2">
            <div class="card card-div border-0 mt-4">
                <div class="d-flex ">
                    <!-- Profile Image & Edit -->
                    <div class="position-relative d-inline-block image-div">
                        <img :src="userData?.profile_image ? userData.profile_image : defaultImage"
                            title="Upload Profile Image" class="img-fluid" 
                            :class="userData?.profile_image ? 'profile-img' : 'default-image'"
                            @click="triggerFileInput('profile')"
                            style="object-fit: cover;" />
                        <i v-if="userData.profile_image"
                            class="bi bi-pencil edit-profile-icon position-absolute top-0 end-0 "
                            @click="triggerFileInput('profile')" style="cursor: pointer;"></i>
                    </div>

                    <!-- Employee Details -->
                    <div class="ms-3 flex-grow-1">
                        <h6 class="mb-3 mt-2">{{ userData.emp_name }}</h6>
                        <div class="d-flex flex-wrap align-items-center gap-5 role-details">
                            <span><i class="bi bi-person-badge-fill me-1"></i>{{ userData.emp_code || "-" }}</span>
                            <span><i class="bi bi-envelope-fill me-1"></i>{{ userData.emp_mail_id || "-" }}</span>
                            <span><i class="bi bi-telephone-fill me-1"></i>{{ userData.emp_phone || "-" }}</span>
                            <span style="font-size:13px"><i class="bi bi-briefcase-fill me-1"></i>{{ userData.designation || "-" }}</span>
                        </div>

                        <!-- Bottom Info -->
                        <div class="mt-3 d-flex flex-wrap gap-4">
                            <span class=" font-11">
                                Department  : {{ userData.department || "-" }}
                            </span>
                            <span class=" font-11">
                                Reporting Manager : 
                                {{ userData.reporting_to || "-" }}
                            </span>
                            <span class=" font-11">Acknowledged On :
                                {{ formatDateTime(userData.acknowledge_on) || "-" }}
                            </span>
                        </div>
                        <div class="mt-3">
                            <span class=" d-flex text-center align-items-center">
                                <p class="mt-3 m-0 me-2">Signiture:</p>
                                <div class="position-relative d-inline-block " style="top:12px">
                                    <img v-if="userData?.signature" :src="userData?.signature ? userData.signature : defaultSign"
                                        title="Upload Signature" class="img-fluid signiture-image border"
                                        @click="triggerFileInput('signature')" style="cursor: pointer;" />
                                    <i v-if="userData?.signature" class="bi bi-pencil edit-image m-2"
                                        @click="triggerFileInput('signature')" style="cursor: pointer;"></i>
                                    
                                    <button class="uploas-sign-btn" v-if="!userData?.signature" @click="triggerFileInput('signature')">Upload signiture</button>
                                </div>

                                <!-- Hidden File Input -->
                                <input type="file" ref="fileInput" @change="uploadImage" accept="image/*" hidden />

                            </span>
                        </div>
                    </div>
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

function formatDateTime(datetime) {
  if (!datetime) return "-";
  const options = {
    year: 'numeric',
    month: 'short',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  };
  return new Date(datetime).toLocaleString(undefined, options);
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
            toast.success(`${uploadType.value === 'profile' ? 'Profile' : 'Signature'} Updated Successfully`, { autoClose: 300 });
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
    /* border-radius: 7px; */
    cursor: pointer;
    width: 150px !important;
    height: 193px !important;
}
.image-div{
    border: 1px solid #c9c9c9;
    padding: 5px;
    border-radius: 7px;
    cursor: pointer;
    height: 205px !important;
}

.default-image {
    border-radius: 7px;
    height: 150px;
    width: 150px !important;
}

.signiture-image {
    height: 60px;
    width: 100px;
}

.edit-image {
    position: absolute;
    top: -15px;
    left: 79px;
    background: black;
    border-radius: 13px;
    color: white;
    padding: 4px;
    font-size: 13px;
    height: 24px;
}

.edit-profile-icon {
    /* position: absolute;
    top: -15px;
    left: 133px; */
    background: black;
    border-radius: 13px;
    color: white;
    padding: 4px;
    font-size: 13px;
    height: 25px;
}

span {
    font-size: 13px;
    line-height: 19.5px;

}

.signature-upload {
    max-width: 300px;
}

.preview-section img {
    max-width: 100%;
    height: auto;
}

.role-details {
    border-bottom: 1px solid #c5baba9c;
    padding-bottom: 17px;
}
.uploas-sign-btn{
  border: 1px solid #cccccc;
  font-size: 13px;
  border-radius: 4px;
  color: #0e0b0b;
  padding: 5px;
  width: 100%;
}
</style>