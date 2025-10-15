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
              class="bi bi-pencil-fill edit-profile-icon position-absolute "
              @click="triggerFileInput('profile')"
              style="cursor: pointer;"
            ></i>
          </div>

          <!-- Employee Details -->
          <div class="ms-md-3 flex-grow-1 text-center text-md-start">
            <h6 class="mb-3 mt-2">{{ userData.emp_name || "N/A" }}</h6>

            <!-- Top details -->
            <div class="d-flex flex-wrap justify-content-center justify-content-md-start gap-4 role-details">
              <span><i class="bi bi-person-badge-fill me-1"></i>{{ userData.emp_code || "N/A" }}</span>
              <span><i class="bi bi-envelope-fill me-1"></i>{{ userData.emp_mail_id || "N/A" }}</span>
              <span><i class="bi bi-telephone-fill me-1"></i>{{ userData.emp_phone || "N/A" }}</span>
              <span><i class="bi bi-briefcase-fill me-1"></i>{{ userData.designation || "N/A" }}</span>
              <span><i class="bi bi-building-fill me-1"></i>{{ userData.company_field || "N/A" }}</span>
            </div>

            <!-- Bottom info -->
            <div class="mt-3 d-flex flex-wrap justify-content-center justify-content-md-start gap-4 font-11">
              <span>Department: 
                <span class="fw-bold">

                {{ userData.department || "N/A" }}
                </span>

              </span>
              <span>Reporting Manager: 
                <span class="fw-bold">
                  {{ userData.reporting_to || "N/A" }}
                </span>
              </span>
              <span>Acknowledged On: 
                <span class="fw-bold">
                {{ formatDateTime(userData.acknowledge_on) || "N/A" }}
                </span>
                </span>
            </div>

            <!-- Signature -->
            <div class="mt-3 d-flex flex-column flex-sm-row align-items-end">
              <p class="m-0 me-sm-2 fw-bold font-12">Signature:</p>
              <div class="position-relative d-inline-block mt-2 mt-sm-0">
                <img
                  v-if="userData?.signature"
                  :src="userData.signature"
                  class="img-fluid signiture-image border p-1"
                  @click="triggerFileInput('signature')"
                  style="cursor: pointer;"
                />
                <i
                  v-if="userData?.signature"
                  class="bi bi-pencil-fill edit-image m-2"
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

    <div v-if="reportingData.length">
      <h6 class="font-16 my-3 ms-2 fw-bold">My Team</h6>
      <div class="container-fluid p-0">
        <div class="row">
          <div class="col-lg-4 col-md-6 col-sm-12 mb-3" v-for="(employee, index) in reportingData" :key="index">
            <div class="card p-3 shadow-sm team-card">
              <div class="d-flex align-items-center">
                <!-- Profile Image -->
                <img :src="employee.profile_image || defaultImage" class="rounded-circle me-3" alt="Profile Image"
                  width="80" height="80" />

                <div>
                  <h5 class="mb-0 font-14">{{ employee.emp_name || "N/A" }}</h5>
                  <p class="paragraph-txt mb-2">{{ employee.emp_code || "N/A"}}</p>
                  <p class="paragraph-txt">
                    <strong class="text-secondary">Designation :</strong> {{ employee.designation || "N/A" }}
                  </p>
                  <p class="paragraph-txt">
                    <strong class="text-secondary">Department :</strong> {{ employee.department || "N/A" }}
                  </p>
                  <p class="paragraph-txt">
                    <strong class="text-secondary">Email :</strong> {{ employee.emp_mail_id || "N/A" }}
                  </p>
                </div>
              </div>
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
// import { toast } from "vue3-toastify";
// import "vue3-toastify/dist/index.css";
import defaultImage from "@/assets/UploadProfile.jpg";
import defaultSign from "@/assets/Sign.png";
import { showSuccess } from "../../shared/services/toast";


const employeeData = ref({});
const email = ref("");
const userData = ref([])
// const defaultImage = "../../assets/UploadProfile.jpg"; // Default profile image 

const fileInput = ref(null);
const uploadType = ref('');
const reportingData = ref("");

function triggerFileInput(type) {
    uploadType.value = type; // 'profile' or 'signature'
    fileInput.value.click();
}

function formatDateTime(datetime) {
  if (!datetime) return "N/A";
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
            const payload = {
              ...(uploadType.value === 'profile'
                ? { profile_image: imageUrl }
                : { signature: imageUrl }),
              name: userData.value.name,
              doctype: doctypes.EzyEmployeeList
            };

            return axiosInstance.put(
                `${apis.DataUpdate}/${userData.value.name}`,
                payload
            );
        })
        .then(() => {
            // userDetails(userData.value.name);
            userDetails(userData.value.name);
            showSuccess(`${uploadType.value === 'profile' ? 'Profile' : 'Signature'} Updated Successfully`);
        })
        .catch((error) => {
            console.error("Error uploading image:", error);
        });
}

// function userDetails(empEmail) {
//     axiosInstance
//         .get(`${apis.resource}${doctypes.EzyEmployeeList}/${empEmail}`)
//         .then((res) => {
//             userData.value = res.data
//         })
//         .catch((error) => {
//             console.error("Error fetching user data:", error);
//         });
// }
function userDetails(empEmail) {
  const queryParams = {
    fields: JSON.stringify(["acknowledge_on","company_field","department","designation","emp_code","emp_mail_id",
    "emp_name","emp_phone","name","profile_image","reporting_designation","reporting_to","signature"]),
    doctype:doctypes.EzyEmployeeList,
    filters: JSON.stringify([["Ezy Employee","emp_mail_id","=",empEmail]]),

    order_by: "`tabEzy Employee`.`enable` DESC, `tabEzy Employee`.`modified` DESC",
  };

  // Data API
  axiosInstance.get(apis.GetDoctypeData, { params: queryParams })
    .then((res) => {
      if (res.message.data) {
        userData.value = res.message.data[0] || {};
          fetchReportingToData()
      }
    })
    .catch((error) => {
      console.error("Error fetching department data:", error);
    });
}

function fetchReportingToData() {
  const filters = {
    reporting_to: userData.value.emp_mail_id,
  };

  const queryParams = {
    filters: JSON.stringify(filters),
    limit_page_length: "none",
    doctype:doctypes.EzyEmployeeList,
    fields: JSON.stringify(["profile_image","name","department","designation","emp_code","emp_mail_id","emp_name"]),
  };

  axiosInstance
    .get(`${apis.GetDoctypeData}`, { params: queryParams })
    .then((res) => {
      reportingData.value = res.message.data; // make sure `data.data` is correct
    })
    .catch((error) => {
      console.error("Error fetching user data:", error);
    });
}


onMounted(() => {
    employeeData.value = JSON.parse(localStorage.getItem('employeeData')) || {};
    email.value = employeeData.value.emp_mail_id || "";

    if (email.value) {
        // userDetails(email.value);
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
    top: -20px;
    left: 79px;
    /* background: black; */
    color: black;
    border-radius: 13px;
    /* color: white; */
    padding: 4px;
    font-size: 13px;
    height: 24px;
}

.edit-profile-icon {
    /* position: absolute;
    top: -15px;
    left: 133px; */
    /* background: black; */
    border-radius: 13px;
    /* color: white; */
    color: black;
    padding: 4px;
    font-size: 13px;
    height: 25px;
    top: -14px;
    right: -11px;
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
.team-card:hover{
  box-shadow: rgba(0, 0, 0, 0.19) 0px 10px 20px, rgba(0, 0, 0, 0.23) 0px 6px 6px;
}

.paragraph-txt{
  font-size: 13px;
  margin: 0px;
}
</style>