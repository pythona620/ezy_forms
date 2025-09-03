<template>
  <div class="main-div">
    <div class="py-2">
      <div class="card card-div border-0 mt-4 p-3">
        <div class="d-flex flex-column flex-md-row align-items-center align-items-md-start">
          <!-- Profile Image & Edit -->
          <div class="position-relative image-div mb-3 mb-md-0">
            <img
              :src="userData?.profile_image ? userData.profile_image : defaultImage"
              title="Upload Profile Image"
              class="img-fluid profile-pic"
              :class="userData?.profile_image ? 'profile-img' : 'default-image'"
              @click="triggerFileInput('profile')"
            />
            <i
              v-if="userData.profile_image"
              class="bi bi-pencil edit-profile-icon position-absolute top-0 end-0"
              @click="triggerFileInput('profile')"
              style="cursor: pointer;"
            ></i>
          </div>

          <!-- Employee Details -->
          <div class="ms-md-3 flex-grow-1 text-center text-md-start">
            <h6 class="mb-3 mt-2">{{ userData.emp_name }}</h6>

            <!-- Top details -->
            <div class="d-flex flex-wrap justify-content-center justify-content-md-start gap-3 role-details">
              <span><i class="bi bi-person-badge-fill me-1"></i>{{ userData.emp_code || "-" }}</span>
              <span><i class="bi bi-envelope-fill me-1"></i>{{ userData.emp_mail_id || "-" }}</span>
              <span><i class="bi bi-telephone-fill me-1"></i>{{ userData.emp_phone || "-" }}</span>
              <span><i class="bi bi-briefcase-fill me-1"></i>{{ userData.designation || "-" }}</span>
              <span><i class="bi bi-building-fill me-1"></i>{{ userData.company_field || "-" }}</span>
            </div>

            <!-- Bottom info -->
            <div class="mt-3 d-flex flex-wrap justify-content-center justify-content-md-start gap-3 font-11">
              <span>Department: {{ userData.department || "-" }}</span>
              <span>Reporting Manager: {{ userData.reporting_to || "-" }}</span>
              <span>Acknowledged On: {{ formatDateTime(userData.acknowledge_on) || "-" }}</span>
            </div>

            <!-- Signature -->
            <div class="mt-3 d-flex flex-column flex-sm-row align-items-center">
              <p class="m-0 me-sm-2">Signature:</p>
              <div class="position-relative d-inline-block mt-2 mt-sm-0">
                <img
                  v-if="userData?.signature"
                  :src="userData.signature"
                  class="img-fluid signiture-image border"
                  @click="triggerFileInput('signature')"
                  style="cursor: pointer;"
                />
                <i
                  v-if="userData?.signature"
                  class="bi bi-pencil edit-image m-2"
                  @click="triggerFileInput('signature')"
                  style="cursor: pointer;"
                ></i>

                <button
                  v-if="!userData?.signature"
                  class="upload-sign-btn"
                  @click="triggerFileInput('signature')"
                >
                  Upload signature
                </button>
              </div>
              <input type="file" ref="fileInput" @change="uploadImage" accept="image/*" hidden />
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
.profile-pic {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border-radius: 8px;
}

@media (min-width: 768px) {
  .profile-pic {
    width: 120px;
    height: 120px;
  }
}

.role-details span,
.font-11 {
  font-size: 13px;
}

.upload-sign-btn {
  padding: 5px 10px;
  border: 1px solid #ccc;
  border-radius: 6px;
  font-size: 12px;
  background-color: #f8f9fa;
  cursor: pointer;
}

.upload-sign-btn:hover {
  background-color: #e9ecef;
}

</style>