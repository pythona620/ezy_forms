<template>
  <div class="bg-img p-0">
    <div v-if="ShowLoginPage" class="input-div p-5">
      <div class="d-flex gap-2 p-2 justify-content-center align-items-center">
        <div><img class="imgmix" src="../assets/Final-logo-ezyforms-removebg-preview.png" /></div>
      </div>

      <div>
        <div class="mt-3">
          <label for="name" class="font-13">User Name</label><br />
          <input type="text" class="form-control m-0 bg-white" id="name" v-model="formdata.usr" @input="validatename"
            @change="checkUserMail" @keydown.enter="checkUserMail" :class="{ 'is-invalid': errors.usr }" />

          <div class="invalid-feedback font-11 mt-1" v-if="errors.usr">
            {{ errors.usr }}
          </div>
        </div>

        <div class="inputbox mt-3 mb-2">
          <label for="password" class="font-13">Password</label><br />
          <!-- <span class="icon"><i class="bi bi-lock-fill"></i></span> -->
          <input :disabled="!showPwdField" class="form-control m-0" :type="showPassword ? 'text' : 'password'"
            id="password" v-model="formdata.pwd" @input="validatepassword" @keydown.enter="Login"
            :class="{ 'is-invalid': errors.pwd }" />

          <!-- Toggle icon for show/hide sas  password -->
          <span v-if="!errors.pwd && formdata.pwd" class="toggle-icon" @click="togglePasswordVisibility">
            <i :class="showPassword ? 'bi bi-eye' : 'bi bi-eye-slash'"></i>
          </span>
          <div class="invalid-feedback font-10" v-if="errors.pwd">
            {{ errors.pwd }}
          </div>
        </div>

          <div class="text-end">
            <span @click="openForgotpassword" class="font-12 p-0 text-end forgot-password">Forgot password?</span><br />
          </div>

        <button :disabled="!showPwdField" @click="Login" type="submit"
          class="border-0 btn btn-dark button w-100 py-2 mb-4 font-13 text-white rounded-1">
          <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          <span v-if="!loading">Log In</span>
        </button>

      </div>
      <!-- && today !== today -->
      <div v-if="isSignup == 0" class="font-13 m-0 cursor-pointer text-center" @click="OpenSignUp"><span
          class="sign">Not
          a user? Sign
          Up</span></div>
    </div>

    <div v-if="showOtpPage">
      <div class="d-flex gap-2 p-2 justify-content-center align-items-center">
        <div><img class="imgmix" src="../assets/Final-logo-ezyforms-removebg-preview.png" /></div>
        <!-- <div><img class="imgmix" src="../assets/favicon.jpg" /></div>
        <div class="m-0">
          <p class="fontimgtext fw-medium m-0">EZY | Forms</p>
        </div> -->
      </div>
      <div>
      </div>
      <div class="input-div mt-3">
        <div class="back-to-login">
          <span @click="backTologin()">Back to Login</span>
        </div>

        <div class="Message-div mb-1">
          Please enter OTP sent to your registered mail ID<br><strong>{{ formdata.usr }}</strong>
        </div>

        <div class="p-4 fw-medium">
          <p v-if="resentMessage && timeLeft > 0" class="text-success font-12">{{ resentMessage }}</p>

          <h6>OTP</h6>
          <div class="d-flex justify-content-between mb-3">
            <input v-for="(digit, index) in otp" :key="index" ref="otpInputs" class="input-field m-0 form-control"
              type="text" maxlength="1" v-model="otp[index]" :class="{ 'error-border': errorMessage }"
              @input="handleInput($event, index)" @keydown.delete="handleBackspace(index)"
              @paste="handlePaste($event)" />

          </div>
          <!-- Error Message -->
          <p v-if="errorMessage" class="text-danger font-13">{{ errorMessage }}</p>

          <!-- <div class="font-12 text-end">
            <p v-if="timeLeft > 0">OTP expires in <strong>{{ formattedTime }}</strong></p>
          </div> -->

          <div class="d-flex justify-content-end mb-3">
            <!-- <ButtonComp @click="resendOtp" class="resend-button" name="Resend"></ButtonComp> -->
            <ButtonComp @click="validateOtp()" class="submit-button" name="Submit"></ButtonComp>

          </div>

        </div>
      </div>
    </div>

    <div v-if="ShowSignUpPage" class="input-div1 px-lg-5 py-3">
      <div class="d-flex gap-2 p-2 justify-content-center align-items-center">
        <div><img class="imgmix" src="../assets/Final-logo-ezyforms-removebg-preview.png" /></div>
      </div>
      <div class="container">
        <div class="row">
          <div class="mb-2  col-lg-6 col-md-12 col-sm-12">
            <label class="font-13" for="email">Email<span class="text-danger ps-1">*</span></label>
            <input class="form-control m-0 bg-transparent" type="email" id="email" v-model="SignUpdata.email"
              @blur="validateEmail" :class="{ 'is-invalid': errors.email }" />
            <div class="invalid-feedback font-11 mt-1" v-if="errors.email">
              {{ errors.email }}
            </div>
          </div>
          <div class="mb-2  col-lg-6 col-md-12 col-sm-12">
            <label class="font-13" for="full_name">User Name<span class="text-danger ps-1">*</span></label>
            <input type="text" class="form-control m-0 bg-transparent text-uppercase" id="name"
              v-model="SignUpdata.full_name" @blur="validateFullName" :class="{ 'is-invalid': errors.full_name }" />
            <div class="invalid-feedback font-11 mt-1" v-if="errors.full_name">
              {{ errors.full_name }}
            </div>
          </div>
          <div class="mb-2  col-lg-6 col-md-12 col-sm-12">
            <label class="font-13" for="emp_code">Employee Id<span class="text-danger ps-1">*</span></label>
            <input type="text" class="form-control  m-0 bg-transparent" id="emp_code" v-model="SignUpdata.emp_code"
              @input="validateEmpCode" :class="{ 'is-invalid': errors.emp_code }" />
            <div class="invalid-feedback font-11 mt-1" v-if="errors.emp_code">
              {{ errors.emp_code }}
            </div>
          </div>
          <div class="mb-2  col-lg-6 col-md-12 col-sm-12">
            <label class="font-13" for="emp_phone">Phone Number<span class="text-danger ps-1">*</span></label>
            <input type="text" class="form-control m-0 bg-transparent" id="emp_phone" v-model="SignUpdata.emp_phone"
              @input="filterPhoneInput" @blur="validatePhone" :class="{ 'is-invalid': errors.emp_phone }" />
            <div class="invalid-feedback font-11 mt-1" v-if="errors.emp_phone">
              {{ errors.emp_phone }}
            </div>
          </div>
          <div class="mb-2  col-lg-6 col-md-12 col-sm-12">
            <label class="font-13" for="emp_code">Designation<span class="text-danger ps-1">*</span></label>
            <Vue3Select v-model="SignUpdata.designation" :options="this.disignationDetails"
              placeholder="Select Designation" />
          </div>
          <div class="mb-2  col-lg-6 col-md-12 col-sm-12">
            <label class="font-13" for="emp_code">Department<span class="text-danger ps-1">*</span></label>
            <Vue3Select v-model="SignUpdata.dept" :reduce="dept => dept.value" :options="this.deptDetails"
              placeholder="Select Department" />
          </div>
          <div class="mb-2  col-lg-6 col-md-12 col-sm-12">
            <label class="font-13" for="emp_code">Property Name<span class="text-danger ps-1">*</span></label>
            <Vue3Select v-model="SignUpdata.business_unit" @change="checkSignitureRequired" :options="this.propertyDetails"
              placeholder="Select Property" />
          </div>
        </div>
        <div class="mt-2 row">
          <div class="col-lg-4 col-md-6 col-sm-12 mb-2">
            <input type="radio" id="digital" value="digital" v-model="selectedOption"
              class="form-check-input mt-1 input-border" />
            <label class="font-13 ms-2" for="digital">Digital Signature</label>
          </div>

          <div class="col-lg-4 col-md-6 col-sm-12 mb-2">
            <input type="radio" id="upload" value="upload" v-model="selectedOption"
              class="form-check-input mt-1 input-border" />
            <label class="font-13 ms-2" for="upload">Upload Signature</label>
          </div>

          <div v-if="selectedOption === 'digital'">
            <DigitalSignature ref="digitalSignature" class="mt-3" @signature-saved="onSignatureSaved"
              @signature-cleared="onSignatureCleared" @signature-uploaded="onSignatureUploaded" :showSaveButton="false" />
          </div>

          <div v-if="selectedOption === 'upload'">
            <input type="file" ref="signatureInputRef" class="form-control mt-3" id="signatureInput"
              @change="selectedSignature" aria-describedby="fileHelpId" accept="image/png, image/jpeg" />

            <div v-if="SignUpdata.signature" class="mt-2">
              <label class="font-13" for="emp_code">Uploaded Signature:</label><br>
              <img :src="SignUpdata.signature" alt="Signature" class="img-thumbnail mt-1" style="max-width: 100px;" />
            </div>

          </div>

        </div>

      </div>

      <div>
        <button
          :disabled="!SignUpdata.email || !SignUpdata.full_name || !SignUpdata.emp_code || !SignUpdata.emp_phone || !SignUpdata.dept || !SignUpdata.designation || !SignUpdata.business_unit"
          type="submit" @click="handleSignUp"
          class="border-0 btn btn-dark button w-100 mb-4 py-2 font-13 text-white rounded-1">
          Sign Up
        </button>
      </div>
      <div class="font-13 m-0 cursor-pointer text-center" @click="OpenLogin"><span class="sign">Existing user? Log
          In</span></div>
    </div>

    <div v-if="ShowForgotPassword" class="input-div p-5">
      <div class="d-flex gap-2 p-2 justify-content-center align-items-center">
        <div><img class="imgmix" src="../assets/Final-logo-ezyforms-removebg-preview.png" /></div>
      </div>

      <div>
        <div class="mt-3">
          <label for="name" class="font-13">Email</label><br />
          <input type="text" placeholder="Enter Email Address" class="form-control m-0 bg-white" id="name"
            v-model="forgotPasswordMail" @input="validateForgotPassword"
            :class="{ 'is-invalid': errors.forgotPasswordMail }" />

          <div class="invalid-feedback font-11 mt-1" v-if="errors.forgotPasswordMail">
            {{ errors.forgotPasswordMail }}
          </div>
        </div>

        <br />
        <button @click="ForgotPassword" type="submit"
          class="border-0 btn btn-dark button w-100 py-2 mb-4 font-13 text-white rounded-1">
          Reset Password
        </button>

      </div>
      <div class="font-13 m-0 cursor-pointer text-center" @click="OpenLogin">
        <span class="sign">Back to Log In</span>
      </div>
    </div>

    <div class="modal fade" id="changePassword" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
      aria-labelledby="changePasswordLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-md">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title font-14 fw-bold" id="changePasswordLabel">
              Set New Password
            </h5>
            <button type="button" class="btn-close" @click="clearPassword()" data-bs-dismiss="modal"
              aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <!-- New Password Field -->
            <div class="mb-2">
              <div class="position-relative">
                <label class="raise-label font-13" for="changepass">New Password</label>
                <input class="form-control m-0 shadow-none font-13" v-model.trim="new_password"
                  placeholder="Enter New Password" :type="showNewPassword ? 'text' : 'password'"
                  @input="validatePassword" />
                <span v-if="new_password" class="new-pwd-toggle-icon" @click="toggleNewPwdVisibility">
                  <i :class="showNewPassword ? 'bi bi-eye' : 'bi bi-eye-slash'"></i>
                </span>
              </div>
              <p v-if="passwordError" class="text-danger font-10 m-0 ps-2">
                {{ passwordError }}
              </p>
            </div>

            <!-- Confirm Password Field -->
            <div class="mb-2">
              <div class="position-relative">
                <label class="raise-label font-13" for="confirmpass">Confirm Password</label>
                <input class="form-control m-0 shadow-none font-13" v-model.trim="confirm_password"
                  placeholder="Enter Confirm Password" :type="showConfPwdPassword ? 'text' : 'password'"
                  @input="checkPasswordsMatch" />
                <span v-if="confirm_password" class="cnf-pwd-toggle-icon" @click="toggleConfPwdVisibility">
                  <i :class="showConfPwdPassword ? 'bi bi-eye' : 'bi bi-eye-slash'"></i>
                </span>
              </div>
              <span v-if="passwordsMismatch" class="text-danger font-10 m-0 ps-2">Passwords do not match.</span>
            </div>

          </div>
          <div>
            <div class="d-flex justify-content-center align-items-center p-3">
              <button class="btn btn-dark font-12 w-100 mt-3" type="submit" @click="passwordChange"
                :disabled="isButtonDisabled">
                Confirm New Password
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="EmployeeToggleModal" tabindex="-1" aria-hidden="true">
      <div class="modal-dialog modal-lg modal-dialog-centered ">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Acknowledgement</h5>
            <button type="button" class="btn-close" @click="acknowledge = ''" data-bs-dismiss="modal"
              aria-label="Close"></button>
          </div>
          <div class="modal-body font-11">
            <div class="ql-editor read-mode" v-html="acknowledgementHtml"></div>
            <div class="mt-4 d-flex align-items-center">
              <input type="checkbox" id="acknowledge" v-model="acknowledge" class="me-1 m-0" />
              <label for="acknowledge">I acknowledge that the information provided is correct.</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" @click="acknowledge = ''"
              data-bs-dismiss="modal">Cancel</button>
            <button type="button" @click="SignUp" :disabled="!acknowledge || saveloading" class="btn btn-dark"
              style="min-width:120px;">
              <span v-if="saveloading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
              <span v-if="!saveloading" class="font-13 text-white">Yes, Proceed</span>
            </button>

          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="EmployeeAcknowledgementModal" data-bs-backdrop="static" tabindex="-1"
      aria-hidden="true">
      <div class="modal-dialog modal-lg modal-dialog-centered ">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">Acknowledgement</h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" @click="ClearAcknowledge"
              aria-label="Close"></button>
          </div>
          <div class="modal-body font-11">
            <div v-if="this.isAcknowledge == 0" class="ql-editor read-mode" v-html="acknowledgementHtml"></div>
          
            <div class="mt-2 row" v-if="this.isAcknowledgeSign == 0">
              <div class="col-lg-4 col-md-6 col-sm-12 mb-2">
                <input type="radio" id="digital" value="digital" v-model="selectedOption"
                  class="form-check-input mt-0 input-border" />
                <label class="font-13 ms-2" for="digital">Digital Signature</label>
              </div>

              <div class="col-lg-4 col-md-6 col-sm-12 mb-2">
                <input type="radio" id="upload" value="upload" v-model="selectedOption"
                  class="form-check-input mt-0 input-border" />
                <label class="font-13 ms-2" for="upload">Upload Signature</label>
              </div>

              <div v-if="selectedOption === 'digital'">
                <DigitalSignature ref="digitalAcknowledgeSignature" class="mt-3" :showSaveButton="true" @signature-saved="acknowledgeSignSaved"
                  @signature-cleared="onSignatureCleared" @signature-uploaded="acknowledgeSignUploaded" />
              </div>

              <div v-if="selectedOption === 'upload'">
                <input type="file" ref="signatureInput" class="form-control mt-3" id="signatureInput"
                  @change="handleSignatureUpload" aria-describedby="fileHelpId" accept="image/png, image/jpeg" />

                <div v-if="acknowledge_signature" class="mt-2">
                  <label class="font-13" for="emp_code">Uploaded Signature:</label><br>
                  <img :src="acknowledge_signature" alt="Signature" class="img-thumbnail mt-1"
                    style="max-width: 100px;" />
                </div>
              </div>
            </div>

            <div class="mt-4 d-flex align-items-center">
              <input type="checkbox" id="acknowledge" v-model="acknowledge" class="me-1 m-0" />
              <label for="acknowledge">I acknowledge that the information provided is correct.</label>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-outline-secondary" @click="ClearAcknowledge"
              data-bs-dismiss="modal">Cancel</button>
            <button type="button" @click="employeeAcknowledge"
              :disabled="!acknowledge" class="btn btn-dark"
              style="min-width:120px;">
              Yes, Proceed
            </button>

          </div>
        </div>
      </div>
    </div>

    <div class="modal fade" id="subscriptionModal" data-bs-backdrop="static" tabindex="-1"
      aria-labelledby="subscriptionLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-body text-black text-center fw-bold font-15" id="modal-body-content">
            <i class="bi text-dark fs-1 bi-exclamation-octagon"></i><br>
            Your subscription has expired. <br>Please contact our sales team at +91 7386295558
          </div>
          <div class="modal-footer">
            <button type="button" data-bs-dismiss="modal" class="btn subBtn">Ok</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { apis, doctypes } from "../shared/apiurls";
import axiosInstance from "../shared/services/interceptor";
import FormFields from "../Components/FormFields.vue";
import ButtonComp from '../Components/ButtonComp.vue'
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
import { nextTick } from "vue";
import Vue3Select from 'vue3-select'
import 'vue3-select/dist/vue3-select.css';
import DigitalSignature from '../views/DigitalSignature.vue';

export default {
  props: ["id"],
  components: {
    Vue3Select,
    FormFields,
    ButtonComp,
    DigitalSignature
  },
  data() {
    return {
      formdata: {
        usr: "",
        pwd: "",
      },
      SignUpdata: {
        redirect_to: '/app/website-settings/Website Settings',
        acknowledge_on: null,
      },
      forgotPasswordMail: "",
      storeData: [],
      errors: {},
      email: "",
      showPassword: false,
      new_password: '',
      confirm_password: '',
      showNewPassword: false,
      showConfPwdPassword: false,
      passwordError: '',
      passwordsMismatch: false,
      showPwdField: false,
      user_id_name: "",
      //   passwordsMismatch: false,
      loading: false,
      showOtpPage: false,
      ShowLoginPage: true,
      ShowForgotPassword: false,
      ShowSignUpPage: false,
      otp: ["", "", "", "", "", ""],
      errorMessage: "",
      storeData: [],
      deptDetails: [],
      disignationDetails: [],
      propertyDetails:[],
      isFirstLogin: "",
      twoFactorAuth: "",
      enable_check: "",
      acknowledge: '',
      designation: '',
      signature: null,
      isSignup: null,
      isActivate: null,
      acknowledgementHtml: "",
      acknowledge: false,
      acknowledgementName: "",
      isDigital: false,
      isUploadImage: false,
      selectedOption: "",
      saveloading: false,
      isAcknowledge: "",
      ShowAcknowledgement: "",
      acknowledge_signature: null,
      isAcknowledgeSign: "",
      LoginAcknowledge: "",
      signatureInput: null,
      subEndDate: "",
      today: "",
      selectedScore: "",
      signRequired: "",
      // timeLeft: 60,
      // timer: null,
      // resentMessage: "",
    };
  },
  methods: {
    validatename() {
      if (!this.formdata.usr) {
        this.errors.usr = "Please Enter Valid Email Address *";
      } else {
        delete this.errors.usr;
      }
    },
    validatepassword() {
      if (!this.formdata.pwd) {
        this.errors.pwd = "Please Enter Password *";
      } else {
        delete this.errors.pwd;
      }
    },
    validateForgotPassword() {
      const email = this.forgotPasswordMail?.trim().toLowerCase();
      const emailPattern = /^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$/;

      if (!email) {
        this.errors.forgotPasswordMail = "Email is required *";
      } else if (!emailPattern.test(email)) {
        this.errors.forgotPasswordMail = "Please enter a valid email address *";
      } else {
        delete this.errors.forgotPasswordMail;
      }
    },
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },

    toggleNewPwdVisibility() {
      this.showNewPassword = !this.showNewPassword;
    },
    toggleConfPwdVisibility() {
      this.showConfPwdPassword = !this.showConfPwdPassword;
    },
    validatePassword() {
      if (!this.passwordRule.regex.test(this.new_password)) {
        this.passwordError = this.passwordRule.message;
      } else {
        this.passwordError = '';
      }

      this.checkPasswordsMatch();
    },
    checkPasswordsMatch() {
      this.passwordsMismatch =
        this.confirm_password && this.new_password !== this.confirm_password;
    },

    clearPassword() {
      this.new_password = ""
      this.confirm_password = ""
      this.passwordsMismatch = ""
      this.passwordError = ""
      this.formdata.usr = "";
    },
    validateEmail() {
      if(this.SignUpdata.email){
        this.SignUpdata.email = this.SignUpdata.email.trim().toLowerCase();
      
      const email = this.SignUpdata.email;
      const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      if (!email) {
        this.errors.email = "Email is required *";

      } else if (!regex.test(email)) {
        this.errors.email = "Please enter a valid email address *";
      }
      else {
        delete this.errors.email;
      }
      axiosInstance
        .get(`${apis.loginCheckmethod}`, {
          params: { user_id: this.SignUpdata.email},
        })
        .then((res) => {
          // Case: User not found – clear error
          if (res.message === "User not found") {
            this.errors.email = '';
          }
          // Case: res.message is an object (user exists) – show error
          else if (typeof res.message === 'object' && res.message.user_id) {
            this.errors.email = "Already Registered User";
          }
        })
        .catch((error) => {
          console.error("Login error: ", error);
          this.errors.email = "Error checking email";
        });
        }



    },
    validatePhone() {
      const phone = this.SignUpdata.emp_phone;
      if (!phone) {
        this.errors.emp_phone = "Phone number is required *";
      } else if (phone.length !== 10) {
        this.errors.emp_phone = "Phone number must be 10 digits *";
      } else {
        delete this.errors.emp_phone;
      }
    },

    filterPhoneInput() {
      // Allow only digits and limit to 10 characters
      this.SignUpdata.emp_phone = this.SignUpdata.emp_phone.replace(/\D/g, '').slice(0, 10);
    },

    validateEmpCode() {
      const url = window.location.href;
      // const url="ncomr.ezyforms.co"

      // Trim spaces and update the actual data
      this.SignUpdata.emp_code = this.SignUpdata.emp_code.trim();

      if (!this.SignUpdata.emp_code) {
        this.errors.emp_code = "Employee Id is required *";
      } else {
        this.errors.emp_code = '';
      }
    },


    validateFullName() {
      this.SignUpdata.full_name = this.SignUpdata.full_name.trim().toUpperCase();
      if (!this.SignUpdata.full_name) {
        this.errors.full_name = "User Name is required *";
      }
      else {
        delete this.errors.full_name;
      }
    },

    handleInput(event, index) {
      const value = event.target.value;

      if (!/^\d*$/.test(value)) {
        this.otp[index] = "";
        return;
      }
      if (value && index < this.otp.length - 1) {
        this.$refs.otpInputs[index + 1].focus();
      }

      this.errorMessage = "";
    },
    handleBackspace(index) {
      if (index > 0 && this.otp[index] === "") {
        this.$refs.otpInputs[index - 1].focus();
      }
    },
    handlePaste(event) {
      event.preventDefault();
      const pastedData = event.clipboardData.getData("text").trim();

      if (/^\d{6}$/.test(pastedData)) {
        this.otp = pastedData.split("");

        this.$refs.otpInputs[5].focus();
        this.errorMessage = "";
      } else {
        this.errorMessage = "Invalid OTP. Please enter a 6-digit number.";
      }
    },
    preventUndo(event, index) {
      if (event.ctrlKey && event.key === "Z") {
        event.preventDefault();
        this.otp[index] = "";
      }
    },
    OpenSignUp() {
      this.ShowLoginPage = false;
      this.showOtpPage = false;
      this.ShowSignUpPage = true;
      this.ShowForgotPassword = false;
      // this.deptData()
      // this.designationData()

      //  const formdata= {
      //     usr: "",
      //     pwd: "",
      //   },
      this.formdata.usr = ""
      this.formdata.pwd = ""
      this.errors.usr = ""
      this.errors.pwd = ""
      this.acknowledge = ""

    },
    OpenLogin() {
      this.ShowLoginPage = true;
      this.showOtpPage = false;
      this.ShowSignUpPage = false;
      this.ShowForgotPassword = false;

      this.SignUpdata.email = "";
      this.SignUpdata.full_name = "";
      this.SignUpdata.emp_code = "";
      this.SignUpdata.emp_phone = "";
      this.SignUpdata.designation = null;
      this.SignUpdata.business_unit=null;
      this.SignUpdata.dept = null;
      this.SignUpdata.signature = null;
      this.selectedOption = null;
      this.signatureInputRef = null;
      this.acknowledge = ""
      this.errors = {};
      this.forgotPasswordMail = "";
      this.errors.forgotPasswordMail = "";

    },

    openForgotpassword() {
      this.ShowLoginPage = false;
      this.showOtpPage = false;
      this.ShowSignUpPage = false;
      this.ShowForgotPassword = true;
      this.showPwdField = false;
      this.formdata.usr = ""
      this.formdata.pwd = ""
      this.errors.usr = ""
      this.errors.pwd = ""
      this.acknowledge = ""
    },
    ClearAcknowledge() {
      this.acknowledge = "",
        this.acknowledge_signature = ""
      if (this.$refs.signatureInput) {
        this.$refs.signatureInput.value = null; // Clear file input
      }
      if (this.$refs.digitalAcknowledgeSignature) {
        this.$refs.digitalAcknowledgeSignature.clearSignature();
      }
    },
    // validateOtp() {
    //   const otpValue = this.otp.join("");

    //   if (otpValue.length < 6) {
    //     this.errorMessage = "OTP must be 6 digits.";
    //   } else {
    //     this.errorMessage = "";
    //     localStorage.setItem("UserName", JSON.stringify(this.storeData));
    //     setTimeout(() => {
    //       this.$router.push({ path: "/todo/receivedform" });
    //     }, 700);
    //   }
    // },

    // startCountdown() {
    //   if (this.timer) clearInterval(this.timer);

    //   this.timer = setInterval(() => {
    //     if (this.timeLeft > 0) {
    //       this.timeLeft--;
    //     } else {
    //       clearInterval(this.timer);
    //     }
    //   }, 1000);
    // },
    // resendOtp() {
    //   this.otp = ["", "", "", "", "", ""];
    //   this.timeLeft = 60;
    //   this.errorMessage = "";
    //   this.resentMessage = "Resent OTP successfully!";
    //   this.startCountdown();
    // },
    ForgotPassword() {
      this.validateForgotPassword()
      if (!this.errors.forgotPasswordMail) {
        const payload = {
          cmd: "frappe.core.doctype.user.user.reset_password",
          user: this.forgotPasswordMail,
        }
        axiosInstance.post(apis.forgotPassword, payload)
          .then((res) => {
            if (res) {
              const messages = JSON.parse(res._server_messages);
              const messageObj = JSON.parse(messages[0]);
              if (messageObj.message) {
                toast.success(messageObj.message);
                this.forgotPasswordMail = "";
                this.ShowLoginPage = true;
                this.showOtpPage = false;
                this.ShowSignUpPage = false;
                this.ShowForgotPassword = false;
              }
            }
          })
          .catch((error) => {
            console.error("Upload error:", error);
          })
      }
    },
    SignUp() {
      this.validateEmail()
      this.validatePhone()
      this.validateEmpCode()
      if (!this.errors.email && !this.errors.emp_phone && !this.errors.emp_code) {
        this.saveloading = true;
        axiosInstance
          .post(apis.signUp, this.SignUpdata)
          .then((res) => {
            if (res) {
              // console.log("signup=", res);
              if (res.message == 'Already Registered') {
                toast.error(res.message)
              }
              else if (res.message == 'Please contact your IT Manager to verify your sign-up') {
                toast.success(res.message)
              }
              else if (res.message == 'Already registered but currently disabled') {
                toast.error(res.message)
              }
              else {
                toast.error(res.message)
              }
              const modal = bootstrap.Modal.getInstance(
                document.getElementById("EmployeeToggleModal")
              );
              modal.hide();
              this.ShowLoginPage = true;
              this.showOtpPage = false;
              this.ShowSignUpPage = false;

              this.SignUpdata.email = "";
              this.SignUpdata.full_name = "";
              this.SignUpdata.emp_code = "";
              this.SignUpdata.emp_phone = "";
              this.SignUpdata.designation = null;
              this.SignUpdata.business_unit=null;
              this.SignUpdata.dept = null;
              this.SignUpdata.signature = null;
              this.selectedOption = null;
              this.signatureInputRef = null;
              this.acknowledge = ""
            }

          })
          .catch((error) => {
            console.error("Login error: ", error);
          })
          .finally(() => {
            this.saveloading = false;
          })
      }
    },

    acknowledgeSignUploaded(signatureData) {
      this.acknowledge_signature = signatureData;
      this.errors.signature = null;
    },

  acknowledgeSignSaved(signatureData) {
  return new Promise((resolve, reject) => {
    try {
      const base64 = signatureData.dataUrl;

      // Convert base64 to File
      const arr = base64.split(',');
      const mime = arr[0].match(/:(.*?);/)[1];
      const bstr = atob(arr[1]);
      let n = bstr.length;
      const u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }

      const file = new File([u8arr], "signature.png", { type: mime });

      // Call upload function
      this.uploadFile(file, "acknowledge signature");
    
      this.errors.signature = null;

      resolve(); // Success
    } catch (error) {
      reject(error); // Failure
    }
  });
},


    employeeAcknowledge() {
      if (this.isAcknowledgeSign === 0 && !this.acknowledge_signature) {
        toast.error("Signature not Saved");
        return;
      }
      const payload = {
        user_id: this.formdata.usr,
        ...(this.isAcknowledge === 0 && { acknowledgement: this.SignUpdata.acknowledgement }),
        ...(this.isAcknowledgeSign === 0 && { is_signature: this.acknowledge_signature })
      };
      axiosInstance
        .post(apis.loginCheckmethod, payload)
        .then((res) => {
          if (res.message.success == true) {
            // toast.success("");
            const modal = bootstrap.Modal.getInstance(
              document.getElementById("EmployeeAcknowledgementModal")
            );
            modal.hide();
            this.isAcknowledge = 1;
            this.isAcknowledgeSign = 1
            this.Login()
          }
        })
        .catch((error) => {
          console.error("Login error: ", error);
        })
    },

    checkSignUpPage() {
      axiosInstance
        .get(`${apis.GetsignUp}`)
        .then((res) => {
          if (res.message) {
            this.isSignup = res.message.is_signup;
            this.propertyDetails = res.message.business_unit.map((prty) => prty.name);
            this.disignationDetails = res.message.designation.map((disg) => disg.name);
            this.deptDetails = res.message.department.map((dept) => ({
              label: dept.department_name,
              value: dept.name,
            }));
            const active = res.message.acknowledgement;
            const firstActive = active[0];
            this.acknowledgementHtml = firstActive.acknowledgement;
            this.SignUpdata.acknowledgement = firstActive.name;
          }
        })
        .catch((error) => {
          console.error("error:", error);
        });
    },

    // acknowledgeData() {
    //   const queryParams = {
    //     fields: JSON.stringify(["*"]),
    //     limit_page_length: "none"
    //   };

    //   axiosInstance
    //     .get(apis.resource + doctypes.acknowledgement, { params: queryParams })
    //     .then((res) => {
    //       if (res?.data?.length) {
    //         const active = res.data.filter(item => item.enable == 1);
    //         if (active.length > 0) {
    //           const firstActive = active[0];
    //           this.acknowledgementHtml = firstActive.acknowledgement;
    //           this.SignUpdata.acknowledgement = firstActive.name;
    //         }
    //       }
    //     })
    //     .catch((error) => {
    //       console.error("Error fetching acknowledgement data:", error);
    //     });
    // },


    //  getFormattedDateTime() {
    //   const now = new Date();
    //   const day = now.getDate().toString().padStart(2, '0');
    //   const month = (now.getMonth() + 1).toString().padStart(2, '0');
    //   const year = now.getFullYear();
    //   const hours = now.getHours().toString().padStart(2, '0');
    //   const minutes = now.getMinutes().toString().padStart(2, '0');
    //   const seconds = now.getSeconds().toString().padStart(2, '0');

    //   return `${day}-${month}-${year} ${hours}:${minutes}:${seconds}`;
    // },

    backTologin() {
      this.ShowLoginPage = true;
      this.showOtpPage = false;
      this.formdata = {};
    },

    checkboxChange() {
      const payload = {
        user_id_name: this.user_id_name,
      };

      axiosInstance
        .put(`${apis.loginCheckuseermethod}`, payload)
        .then((res) => {
          if (res.message.is_first_login === 1) {
            this.showPwdField = true;
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    },

    passwordChange() {
      if (this.passwordsMismatch) {
        console.error("Passwords do not match.");
        return;
      }

      const payload = {
        user_id: this.formdata.usr,
        new_password: this.new_password,
      };

      axiosInstance
        .put(`${apis.loginUpdatePassword}`, payload)
        .then((res) => {
          if (res.message) {
            toast.success("Password updated Successfully", { autoClose: 300 });
            const modal = bootstrap.Modal.getInstance(
              document.getElementById("changePassword")
            );
            modal.hide();
            this.checkboxChange();
          }
          if (res._server_messages) {
            const messages = JSON.parse(res._server_messages);
            messages.forEach((msg) => {
              const parsed = JSON.parse(msg);
              toast.error(parsed.message, { autoClose: 2000 });
            });
          }
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    },

    checkUserMail() {
      axiosInstance
        .get(`${apis.loginCheckmethod}`, {
          params: { user_id: this.formdata.usr },
        })
        .then((res) => {
          if (res.message) {
            this.isFirstLogin = res.message.is_first_login;
            this.twoFactorAuth = res.message.enable_two_factor_auth
            this.user_id_name = res.message.name;
            this.enableCheck = res.message.enable_check
            this.isAcknowledge = res.message.is_acknowledge
            this.ShowAcknowledgement = res.message.show_acknowledgement
            this.isAcknowledgeSign = res.message.is_signature;
            this.LoginAcknowledge = res.message.login_acknowledge;
            this.subEndDate = res.message.subscription_end_date;
            this.selectedScore = res.message.minimum_password_score;

            if (this.isFirstLogin === 0 && this.enableCheck === 1) {
              const modal = new bootstrap.Modal(
                document.getElementById("changePassword")
              );
              modal.show();
              this.showPwdField = false;
              this.showOtpPage = false;
            }
            if (this.isFirstLogin === 0 && this.enableCheck == 0) {
              toast.error("User is disabled. Please contact your IT Manager to verify your sign-up")
            }
            if (this.isFirstLogin === 1) {
              this.showPwdField = true;
              this.showOtpPage = false;

              // Ensure the DOM updates before focusing the input
              nextTick(() => {
                document.getElementById("password")?.focus();
              });

              // console.log("User is logging in for the first time.");
            }
            if (this.subEndDate === this.today) {
              const modal = new bootstrap.Modal(
                document.getElementById("subscriptionModal")
              );
              modal.show();
              this.showPwdField = false;
            }
            else {
              console.log("User has logged in before.");
            }
          } else {
            // console.log("No user data found.");
            this.showPwdField = true; // Show password field when no user data is found
          }
        })
        .catch((error) => {
          console.error("Login error: ", error);
        });
    },

    Login() {
      this.validatename();
      this.validatepassword();
      if (!this.errors.usr && !this.errors.pwd) {
        this.loading = true;
        axiosInstance
          .post(apis.login, this.formdata)
          .then((res) => {
            if (res) {
              this.storeData = res;
              if (this.twoFactorAuth === "1") {
                this.ShowLoginPage = false;
                this.showOtpPage = true;
              }
              else {
                this.showOtpPage = false;
                this.ShowLoginPage = true;
                this.otp = ["", "", "", "", "", ""];
                if (this.LoginAcknowledge === 1 && (this.isAcknowledge == 0 || this.isAcknowledgeSign == 0)) {
                  const modal = new bootstrap.Modal(document.getElementById('EmployeeAcknowledgementModal'));
                  modal.show();
                }
                else {
                  console.log(res.employee_doc);
                   const employeeData = res.employee_doc;

                // Extract only the required fields
                const filteredEmployeeData = {
                  name: employeeData.name,
                  company_field: employeeData.company_field,
                  emp_name: employeeData.emp_name,
                  emp_mail_id: employeeData.emp_mail_id,
                  designation: employeeData.designation,
                  department: employeeData.department,
                  emp_code: employeeData.emp_code,
                  emp_signature: employeeData.signature,
                  is_admin: employeeData.is_admin,
                  responsible_units: employeeData.responsible_units,
                  // department: employeeData.department,
                };
                localStorage.setItem("subEndDate", this.subEndDate)
                localStorage.setItem("UserName", JSON.stringify(this.storeData));
                sessionStorage.setItem("UserName", JSON.stringify(this.storeData));

                localStorage.setItem("employeeData", JSON.stringify(filteredEmployeeData));
                sessionStorage.setItem("employeeData", JSON.stringify(filteredEmployeeData));

                localStorage.setItem("USERROLE", JSON.stringify(filteredEmployeeData.designation));
                sessionStorage.setItem("USERROLE", JSON.stringify(filteredEmployeeData.designation));

                toast.success("Login successfull", { autoClose: 2000 });

                setTimeout(() => {
                  this.$router.push({ path: "/dashboard/maindash" });
                }, 500);

                  // this.userData(this.formdata.usr);
                }
              }
            }
          })
          .catch((error) => {
            console.error("Login error: ", error);
          })
          .finally(() => {
            this.loading = false;
          });

      }
    },

    // userData(email) {
    //   axiosInstance
    //     .get(`${apis.resource}${doctypes.users}/${email}`)
    //     .then((res) => {
    //       this.email = res.data.email;
    //       if (this.email) {
    //         axiosInstance
    //           .get(`${apis.resource}${doctypes.EzyEmployeeList}/${this.email}`)
    //           .then((responce) => {
    //             const employeeData = responce.data;

    //             // Extract only the required fields
    //             const filteredEmployeeData = {
    //               name: employeeData.name,
    //               company_field: employeeData.company_field,
    //               emp_name: employeeData.emp_name,
    //               emp_mail_id: employeeData.emp_mail_id,
    //               designation: employeeData.designation,
    //               department: employeeData.department,
    //               emp_code: employeeData.emp_code,
    //               emp_signature: employeeData.signature,
    //               is_admin: employeeData.is_admin,
    //               responsible_units: employeeData.responsible_units,
    //               // department: employeeData.department,
    //             };
    //             localStorage.setItem("subEndDate", this.subEndDate)
    //             localStorage.setItem("UserName", JSON.stringify(this.storeData));
    //             sessionStorage.setItem("UserName", JSON.stringify(this.storeData));

    //             localStorage.setItem("employeeData", JSON.stringify(filteredEmployeeData));
    //             sessionStorage.setItem("employeeData", JSON.stringify(filteredEmployeeData));

    //             localStorage.setItem("USERROLE", JSON.stringify(filteredEmployeeData.designation));
    //             sessionStorage.setItem("USERROLE", JSON.stringify(filteredEmployeeData.designation));

    //             toast.success("Login successfull", { autoClose: 2000 });

    //             setTimeout(() => {
    //               this.$router.push({ path: "/dashboard/maindash" });
    //             }, 500);

    //           })
    //           .catch((error) => {
    //             console.error("Error fetching employee data:", error);
    //           });
    //       } else {
    //         localStorage.setItem("employeeData", JSON.stringify(this.employeeData));
    //       }
    //     })
    //     .catch((error) => {
    //       console.error("Error fetching user data:", error);
    //     });
    // },


    validateOtp() {
      const otpValue = this.otp.join("");

      if (otpValue.length < 6) {
        this.errorMessage = "OTP must be 6 digits.";
      } else {
        this.errorMessage = "";

        const params = {
          user: String(this.formdata.usr),
          otp: this.otp.join(""),
          tmp_id: String(this.storeData.tmp_id),
          cmd: "login",
        };

        axiosInstance
          .post(apis.login, params)
          .then((message) => {
            if (message) {
              // console.log("message", message);
              this.storeData = message;
              // localStorage.setItem("UserName", JSON.stringify(this.storeData));
              // if (this.formdata.usr) {
              //   this.userData(this.formdata.usr);
              // }
            }
          })
          .catch((error) => {
            console.error("Login error: ", error);
          });
      }
    },
    // deptData() {
    //   const queryParams = {
    //     fields: JSON.stringify(["name", "department_name"]),
    //     limit_page_length: "none"
    //   };

    //   axiosInstance
    //     .get(apis.resource + doctypes.departments, { params: queryParams })
    //     .then((res) => {
    //       if (res?.data?.length) {
    //         this.deptDetails = res.data.map((dept) => ({
    //           label: dept.department_name,
    //           value: dept.name,
    //         }));
    //       }
    //     })
    //     .catch((error) => {
    //       console.error("Error fetching department data:", error);
    //     });
    // },
    // designationData() {
    //   const queryParams = {
    //     fields: JSON.stringify(["name"]),
    //     limit_page_length: "none"
    //   };

    //   axiosInstance
    //     .get(apis.resource + doctypes.designations, { params: queryParams })
    //     .then((res) => {
    //       if (res?.data?.length) {
    //         this.disignationDetails = res.data.map((disg) => disg.name);
    //         // console.log(this.disignationDetails);
    //       }
    //     })
    //     .catch((error) => {
    //       console.error("Error fetching department data:", error);
    //     });
    // },

    onSignatureSaved(signatureData) {
      const base64 = signatureData.dataUrl;

      // Convert base64 to File
      const arr = base64.split(',');
      const mime = arr[0].match(/:(.*?);/)[1];
      const bstr = atob(arr[1]);
      let n = bstr.length;
      const u8arr = new Uint8Array(n);
      while (n--) {
        u8arr[n] = bstr.charCodeAt(n);
      }

      const file = new File([u8arr], "signature.png", { type: mime });

      // Call upload function
      this.uploadFile(file, "signature");

      // Optional: clear error or store locally
      this.errors.signature = null;
      // console.log("Signature ready for upload:", file);
    },

    checkSignitureRequired() {
    axiosInstance
      .get(`${apis.GetsignUp}`, { params: { business_unit: this.SignUpdata.business_unit } })
      .then((res) => {
        if (res.message) {
          this.signRequired = res.message.signature_required;
          console.log('Signature Required:', this.signRequired);
        }
      })
      .catch((error) => {
        console.error('Error:', error);
      });
  },

    handleSignUp() {
      const signatureComponent = this.$refs.digitalSignature;
      if (this.signRequired == 1) {
        if (signatureComponent && signatureComponent.getSignatureData) {
          const signatureData = signatureComponent.getSignatureData();
          // this.onSignatureSaved(signatureData);
          if (signatureData.hasSignature==true) {
        this.onSignatureSaved(signatureData);
             const modal = new bootstrap.Modal(document.getElementById('EmployeeToggleModal'));
            modal.show();
          } else {
            toast.error("signature Not Added");
          }
        }
        else if (this.SignUpdata.signature) {
      const modal = new bootstrap.Modal(document.getElementById('EmployeeToggleModal'));
      modal.show();
        }
        else {
          toast.error("signature Not Added")
        }
      }
      else {
        const modal = new bootstrap.Modal(document.getElementById('EmployeeToggleModal'));
        modal.show();
      }
    },
    openDigitakSignature() {
      this.isDigital = true;
    },
    openSignatureInput() {
      this.$refs.signatureInputRef.click();
      this.isDigital = false;
    },

    selectedSignature(event) {
      const file = event.target.files[0];
      if (file) {
        uploadFile(file, "signature");
      }
    },

    handleSignatureUpload(event) {
      const file = event.target.files[0];
      if (file) {
        this.uploadFile(file, "acknowledge signature");
      }
    },

    uploadFile(file, field) {
      let fileName = `${file.name}`;

      const formData = new FormData();
      formData.append("file", file, fileName);
      formData.append("is_private", "0");
      formData.append("folder", "Home");

      axiosInstance
        .post(apis.uploadfile, formData)
        .then((res) => {
          if (res.message && res.message.file_url) {
            if (field === "signature") {
              this.SignUpdata.signature = res.message.file_url;
            }
            if (field === "acknowledge signature") {
              this.acknowledge_signature = res.message.file_url;
            }
          } else {
            console.error("file_url not found in the response.");
          }
        })
        .catch((error) => {
          console.error("Upload error:", error);
        });
    },

    selectedSignature(event) {
      const file = event.target.files[0];
      if (file) {
        this.uploadFile(file, "signature");
      }
    },

    onSignatureCleared() {
      this.SignUpdata.signature = "";
      this.acknowledge_signature = "";
      this.errors.signature = 'Signature is required';
    },


    onSignatureUploaded(signatureData) {
      this.SignUpdata.signature = signatureData;
      this.errors.signature = null;
      // console.log('Signature uploaded:', signatureData);
    },


    // Form submission
    submitForm() {
      // Validate all fields
      this.validateEmail();
      this.validateFullName();
      this.validateEmpCode();
      this.validatePhone();

      // Validate signature
      if (!this.SignUpdata.signature) {
        this.errors.signature = 'Digital signature is required';
        return;
      }

      if (this.isFormValid) {
        // Prepare form data for submission
        const formData = new FormData();

        // Add text fields
        Object.keys(this.SignUpdata).forEach(key => {
          if (key !== 'signature') {
            formData.append(key, this.SignUpdata[key]);
          }
        });

        // Add signature as blob
        if (this.SignUpdata.signature && this.SignUpdata.signature.blob) {
          formData.append('signature', this.SignUpdata.signature.blob, 'signature.png');
        }

        // Submit to your backend
        this.submitToServer(formData);
      }
    },

    async submitToServer(formData) {
      try {
        // Replace with your actual API endpoint
        const response = await fetch('/api/employee-signup', {
          method: 'POST',
          body: formData
        });

        if (response.ok) {
          this.successMessage = 'Registration successful!';
          // Reset form or redirect as needed
        } else {
          throw new Error('Registration failed');
        }
      } catch (error) {
        console.error('Submission error:', error);
        this.successMessage = 'Registration failed. Please try again.';
      }
    },

  },
  watch: {
  'SignUpdata.business_unit'(newVal) {
    if (newVal) {
      this.checkSignitureRequired();
    }
  }
  },
  mounted() {
    this.checkSignUpPage();
    //this.acknowledgeData();
    this.today = new Date().toISOString().split("T")[0];

    const url = window.location.href;
    if (url.includes('ncomr')) {
      this.SignUpdata.emp_code = 'NICO-';
    }
  },

  computed: {
    passwordRule() {
      if (this.selectedScore == 2) {
        return {
          regex: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{8,}$/,
          message:
            "Password must be at least 8 characters with at least one uppercase, lowercase, number, and special character.",
        };
      } else if (this.selectedScore == 3) {
        return {
          regex: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{10,}$/,
          message:
            "Password must be at least 10 characters and fully mixed (uppercase, lowercase, numbers, special characters).",
        };
      } else if (this.selectedScore == 4) {
        return {
          regex: /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&]).{14,}$/,
          message:
            "Password must be at least 14 characters with a random mix of all character types.",
        };
      }
      return {
        regex: /.*/,
        message: "Password must meet the system's security requirements.",
      };
    },
    isPasswordValid() {
      return this.passwordRule.regex.test(this.new_password);
    },
    isButtonDisabled() {
      return (
        !this.new_password ||
        !this.confirm_password ||
        !this.isPasswordValid ||
        this.new_password !== this.confirm_password
      );
    },
  },
};
</script>

<style lang="scss" scoped>
.loginpageheight {
  height: 100vh;
}

.checkbox-input {
  width: 50px;
}

.input-border {
  border: 1px solid black;
}

.Message-div {
  background-color: #DEFDE9;
  padding: 20px 50px;
  text-align: center;
  font-size: 12px;
}

// .add-signiture {
//   position: relative;
//   bottom: 77px;
//   left: 205px;
// }
.add-signiture-btn {
  border: 1px solid #dc3545;
  color: #dc3545;
  border-radius: 5px;
  background: transparent;
  font-size: 13px;
  font-weight: 400;
}

.input-field {
  font-size: 18px;
  font-weight: 500;
  width: 38px;
  height: 38px;
  border-radius: 6px;
  border-width: 1px;
  border: 1px solid #EEEEEE;
  box-shadow: 0px 1px 8px 0px #00000017;
  text-align: center;
}

.resend-button {
  border: 1px solid #EEEEEE !important;
  background: transparent;
  border-radius: 10px;
  text-align: center;
  font-weight: 500;
  font-size: 13px;
  padding: 10px 30px;
}

.submit-button {
  background-color: #1B14DF;
  border-radius: 10px;
  text-align: center;
  font-weight: 500;
  font-size: 13px;
  color: white;
  padding: 10px 30px;
}

.otp-input.error-border {
  border: 1px solid red !important;
}

.back-to-login {
  color: #1B14DF;
  padding: 15px 20px;
  font-size: 14px;
  font-weight: 500;
  text-decoration: underline;
  cursor: pointer;
}

.fontimgtext {
  font-size: 17px;
  color: #111111;
  margin: 0;
}

.bg-img {
  position: relative;
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.bg-img::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url(../assets/backgroundimage.jpeg);
  background-size: cover;
  background-position: center;
  opacity: 0.1;
  /* Set your desired opacity */
  z-index: -1;
}

.input-div {
  border: 1px solid #eeeeee;
  box-shadow: 0px 2px 14px 0px #00000017;
  background-color: #ffffff59;
  border-radius: 6px;
  z-index: 1;
  /* Ensure it's above the background */
  position: relative;
  min-width: 420px;
}

.input-div1 {
  border: 1px solid #eeeeee;
  box-shadow: 0px 2px 14px 0px #00000017;
  background-color: #ffffff59;
  border-radius: 6px;
  z-index: 1;
  position: relative;
  width: 50% !important;
  padding: 20px;
}

.label {
  color: #111111;
}

input {
  padding: 7px;
  margin-top: 16px;
  border-radius: 6px;
  font-size: 13px;
}

button {
  /* padding: 9px; */
  margin-top: 25px;
  /* background-color: rgb(231, 90, 90); */
  font-weight: bold;
}

.inputbox {
  position: relative;
  width: 100%;
  height: 50px;

  font-size: 13px;
}

.forgot-password:hover {
  text-decoration: underline;
  transition: all 0.3s ease;
}

.toggle-icon {
  position: absolute;
  top: 77%;
  right: 10px;
  transform: translateY(-50%);
  cursor: pointer;
}

.input-box label {
  position: absolute;
  top: 50%;
  left: 5px;
  transform: translateY(-50%);
  font-size: 1em;
  color: white;
  font-weight: 500;
  pointer-events: none;
  transition: 0.5s;
}

.input-box input:focus~label,
.input-box input:valid~label {
  top: 3px;
}

.input-box input {
  width: 100%;
  /* height: 100%; */
  background: #ffffff;
  /* border: none; */
  /* outline: none; */
  font-size: 1em;
  font-weight: 600;
  padding: 0 35px 0 5px;
}

input:focus {
  border: 1px solid #999999;
  outline: none;
  box-shadow: none;
}

.input-box .icon {
  position: absolute;
  right: 8px;
  font-size: 1.2em;
  color: white;
  line-height: 57px;
}

/* Add media query for mobile view */
@media (max-width: 768px) {
  .input-div {
    width: 80vw;
    margin-right: 0;
    margin-left: 0;
    margin: 0 auto;
    height: auto;
  }

  .input-div1 {
    width: 90vw !important;
  }
}

@media (max-width: 480px) {
  .input-div {
    width: 90vw;
    padding: 20px;
  }

  .input-div1 {
    width: 1000vw !important;
  }

  .input-box {
    height: 60px;
    font-size: 16px;
  }

  .input-box input {
    padding: 0 25px 0 5px;
    font-size: 16px;
  }

  .input-box .icon {
    font-size: 1.5em;
    line-height: 60px;
  }

  .invalid-feedback {
    width: 100%;
    margin-top: 5px;
    font-size: 12px;
    color: var(--bs-danger-text);
  }
}

.invalid-feedback {
  color: #dc3545;
}

.nico-text {
  position: relative;
  left: 53px;
}

.empId {
  position: relative;
  right: 45px;
  width: 100%;
}


.sign:hover {
  // border-bottom: 1px solid black;
  cursor: pointer;
}

.vs__selected-options {
  font-size: 13px !important;
}

.v-select * {
  box-sizing: border-box;
  font-size: 13px !important;
  // background-color: white;
}

.new-pwd-toggle-icon {
  position: absolute;
  top: 73%;
  right: 20px;
  transform: translateY(-50%);
  cursor: pointer;
}

.cnf-pwd-toggle-icon {
  position: absolute;
  top: 73%;
  right: 20px;
  transform: translateY(-50%);
  cursor: pointer;
}

.subBtn {
  background-color: #212529;
  color: white;
}
</style>
