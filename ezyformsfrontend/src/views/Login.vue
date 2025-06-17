<template>
  <div class="bg-img">
    <div v-if="ShowLoginPage" class="input-div p-5">
      <div class="d-flex gap-2 p-2 justify-content-center align-items-center">
        <div><img class="imgmix" src="../assets/Final-logo-ezyforms-removebg-preview.png" /></div>
        <!-- <div class="m-0">
          <p class="fontimgtext fw-medium m-0">EZY | Forms</p>
        </div> -->
      </div>

      <div>
        <div class="mt-3">
          <label for="name" class="font-13">User name</label><br />
          <input type="text" class="form-control m-0 bg-white" id="name" v-model="formdata.usr" @input="validatename"
            @change="checkUserMail" :class="{ 'is-invalid': errors.usr }" />

          <div class="invalid-feedback font-11 mt-1" v-if="errors.usr">
            {{ errors.usr }}
          </div>
        </div>

        <div class="inputbox mt-3">
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


        <br />
        <button :disabled="!showPwdField" @click="Login" type="submit"
          class="border-0 btn btn-dark button w-100 py-2 mb-4 font-13 text-white rounded-1">
          <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          <span v-if="!loading">Log In</span>
        </button>

      </div>
      <div class="font-13 m-0 cursor-pointer text-center" @click="OpenSignUp"><span class="sign">Not a user? Sign Up</span></div>
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

     <div v-if="ShowSignUpPage" class="input-div p-5">
      <div class="d-flex gap-2 p-2 justify-content-center align-items-center">
        <div><img class="imgmix" src="../assets/Final-logo-ezyforms-removebg-preview.png" /></div>
      </div>
      <div>
        <div class="mb-2">
          <label class="font-13" for="email">Email</label>
          <input class="form-control m-0" type="email" id="email" v-model="SignUpdata.email" @blur="validateEmail" :class="{ 'is-invalid': errors.email }" />
          <div class="invalid-feedback font-11 mt-1" v-if="errors.email">
            {{ errors.email }}
          </div>
        </div>
        <div class="mb-2">
          <label class="font-13" for="full_name">User Name</label>
          <input type="text" class="form-control m-0 bg-white" id="name" v-model="SignUpdata.full_name" />
        </div>
        <div class="mb-2">
          <label class="font-13" for="emp_code">Employee Id</label>
          <input type="text" class="form-control m-0 bg-white" id="emp_code" v-model="SignUpdata.emp_code" @blur="validateEmpCode" :class="{ 'is-invalid': errors.emp_code }" />
          <div class="invalid-feedback font-11 mt-1" v-if="errors.emp_code">
            {{ errors.emp_code }}
          </div>
        </div>
        <div class="mb-2">
          <label class="font-13" for="emp_phone">Phone Number</label>
          <input type="text" class="form-control m-0 bg-white" id="emp_phone" v-model="SignUpdata.emp_phone" @input="filterPhoneInput" @blur="validatePhone" :class="{ 'is-invalid': errors.emp_phone }" />
          <div class="invalid-feedback font-11 mt-1" v-if="errors.emp_phone">
            {{ errors.emp_phone }}
          </div>
        </div>
        
      </div>
      <div>
        <button type="submit" :disabled="!SignUpdata.email || !SignUpdata.full_name || !SignUpdata.emp_code || !SignUpdata.emp_phone" @click="SignUp()" class="border-0 btn btn-dark button w-100 mb-4 py-2 font-13 text-white rounded-1">
          Sign Up
        </button>
      </div>
      <div class="font-13 m-0 cursor-pointer text-center" @click="OpenLogin"><span class="sign">Existing user? Log In</span></div>
    </div>

    <div class="modal fade" id="changePassword" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
      aria-labelledby="changePasswordLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-sm">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title font-14 fw-bold" id="changePasswordLabel">
              Set New Password
            </h5>
            <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <!-- <FormFields tag="select" placeholder="Category" class="mb-3" name="roles" id="roles"
                            @change="changingCategory" :Required="false" :options="categoryOptions"
                            v-model="selectedData.selectedCategory" /> -->
            <div class="mb-3">
              <label class="raise-label" for="changepass">New Password</label>
              <FormFields class="mb-1" tag="input" type="text" name="changepass" id="changepass"
                placeholder="Enter New Password" v-model="new_password" @change="validateNewPassword" />

              <p v-if="passwordError" class="text-danger font-11 m-0 ps-2">
                {{ passwordError }}
              </p>
            </div>
            <div class="mb-2">
              <label class="raise-label" for="confirmpass">Confirm Password</label>
              <FormFields class="" tag="input" type="text" name="confirmpass" id="confirmpass"
                placeholder="Enter Confirm Password" v-model="confirm_password" @keydown.enter="passwordChange" />
              <span v-if="passwordsMismatch" class="text-danger font-11 m-0 ps-2">Passwords do not match.</span>
            </div>
            <!-- <FormFields tag="select" placeholder="Form" class="mb-3" name="roles" id="roles"
                            :Required="false" :options="formList" v-model="selectedData.selectedform" /> -->
          </div>
          <div>
            <div class="d-flex justify-content-center align-items-center p-3">
              <button :disabled="!isFormValid" class="btn btn-dark font-12 w-100" type="submit" @click="passwordChange">
                Create New Password
              </button>
            </div>
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
export default {
  props: ["id"],
  components: {
    FormFields,
    ButtonComp
  },
  data() {
    return {
      formdata: {
        usr: "",
        pwd: "",
      },
      SignUpdata: {
        redirect_to: '/app/website-settings/Website Settings',
      },
      storeData: [],
      errors: {},
      email: "",
      showPassword: false,
      new_password: "",
      confirm_password: "",
      showPwdField: false,
      user_id_name: "",
      //   passwordsMismatch: false,
      passwordError: "",
      loading: false,
      showOtpPage: false,
      ShowLoginPage: true,
      ShowSignUpPage: false,
      otp: ["", "", "", "", "", ""],
      errorMessage: "",
      storeData: [],
      isFirstLogin: "",
      twoFactorAuth: "",
      enable_check:""
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
    togglePasswordVisibility() {
      this.showPassword = !this.showPassword;
    },

    validateNewPassword() {
      if (!this.new_password) {
        this.passwordError = "Password is required.";
      } else if (this.new_password.length < 6) {
        this.passwordError = "Password must be at least 6 characters long.";
      } else {
        this.passwordError = "";
      }
    },
     validateEmail() {
      const email = this.SignUpdata.email;
      const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

      if (!email) {
        this.errors.email = "Email is required *";
      } else if (!regex.test(email)) {
        this.errors.email = "Please enter a valid email address *";
      } else {
        delete this.errors.email;
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
      // const url="ncomr.ezyforms.co/ezyformsfrontend#/";

        if(!this.SignUpdata.emp_code){
            this.errors.emp_code = "Employee Id is required *";
        } 
      // Apply validation only if URL contains 'ncomr'
        else if (url.includes('ncomr')) {
        const code = this.SignUpdata.emp_code.trim();
        if (!code.startsWith('NICO-')) {
          this.errors.emp_code = "Employee Id must start with 'NICO-'";
        } else {
          this.errors.emp_code = '';
        }
      }
      else {
        this.errors.emp_code = '';
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
    OpenSignUp(){
      this.ShowLoginPage = false;
      this.showOtpPage = false;
      this.ShowSignUpPage=true
    },
    OpenLogin(){
      this.ShowLoginPage = true;
      this.showOtpPage = false;
      this.ShowSignUpPage=false;
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

    SignUp() {
      this.validateEmail()
      this.validatePhone()
      this.validateEmpCode()
      if (!this.errors.email && !this.errors.emp_phone && !this.errors.emp_code) {
        axiosInstance
          .post(apis.signUp, this.SignUpdata)
          .then((res) => {
            if (res) {
              // console.log("signup=", res);
              this.ShowLoginPage = true;
              this.showOtpPage = false;
              this.ShowSignUpPage=false;
              toast.success("Please contact your IT Manager to verify your sign-up")
              const modal = bootstrap.Modal.getInstance(
                document.getElementById("EmployeeToggleModal")
              );
              modal.hide();
            }
  
          })
          .catch((error) => {
            console.error("Login error: ", error);
          })
      }
    },

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
          // console.log("Password updated successfully:", res.data);
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
            this.enableCheck=res.message.enable_check
            if (this.isFirstLogin === 0 && this.enableCheck===1) {
              const modal = new bootstrap.Modal(
                document.getElementById("changePassword")
              );
              modal.show();
              this.showPwdField = false;
              this.showOtpPage = false;
            }
            if(this.isFirstLogin===0 && this.enableCheck==0){
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
            } else {
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
                // localStorage.setItem("UserName", JSON.stringify(this.storeData));
                this.userData(this.formdata.usr);
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

    userData(email) {
      axiosInstance
        .get(`${apis.resource}${doctypes.users}/${email}`)
        .then((res) => {
          this.email = res.data.email;
          if (this.email) {
            axiosInstance
              .get(`${apis.resource}${doctypes.EzyEmployeeList}/${this.email}`)
              .then((responce) => {
                const employeeData = responce.data;

                // Extract only the required fields
                const filteredEmployeeData = {
                  name: employeeData.name,
                  company_field: employeeData.company_field,
                  emp_name: employeeData.emp_name,
                  emp_mail_id: employeeData.emp_mail_id,
                  designation: employeeData.designation,
                  department: employeeData.department,
                  // department: employeeData.department,
                };

                // Store required data only
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
              })
              .catch((error) => {
                console.error("Error fetching employee data:", error);
              });
          } else {
            localStorage.setItem("employeeData", JSON.stringify(this.employeeData));
          }
        })
        .catch((error) => {
          console.error("Error fetching user data:", error);
        });
    }
    ,


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
              if (this.formdata.usr) {
                this.userData(this.formdata.usr);
              }
            }
          })
          .catch((error) => {
            console.error("Login error: ", error);
          });
      }
    },

  },

  computed: {
    passwordsMismatch() {
      return (
        this.new_password &&
        this.confirm_password &&
        this.new_password !== this.confirm_password
      );
    },
    isFormValid() {
      return this.new_password.length >= 6 && this.new_password === this.confirm_password;
    },
  },
};
</script>

<style lang="scss" scoped>
.loginpageheight {
  height: 100vh;
}

.Message-div {
  background-color: #DEFDE9;
  padding: 20px 50px;
  text-align: center;
  font-size: 12px;
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
}

@media (max-width: 480px) {
  .input-div {
    width: 90vw;
    padding: 20px;
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
.sign:hover{
  // border-bottom: 1px solid black;
  cursor: pointer;
}
</style>
