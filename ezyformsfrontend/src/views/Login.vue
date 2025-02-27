<template>
  <div class="bg-img">
    <div class="input-div p-5">
      <div class="d-flex gap-2 p-2 justify-content-center align-items-center">
        <div><img class="imgmix" src="../assets/favicon.jpg" /></div>
        <div class="m-0">
          <p class="fontimgtext fw-medium m-0">EZY | Forms</p>
        </div>
      </div>

      <div>
        <div class="mt-3">
          <label for="name" class="font-13">User name</label><br />
          <input type="text" class="form-control m-0 bg-white" id="name" v-model="formdata.usr" @input="validatename"
            @change="checkUserMail()" :class="{ 'is-invalid': errors.usr }" />

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
          <span v-if="!errors.pwd" class="toggle-icon" @click="togglePasswordVisibility">
            <i :class="showPassword ? 'bi bi-eye' : 'bi bi-eye-slash'"></i>
          </span>
          <div class="invalid-feedback font-10" v-if="errors.pwd">
            {{ errors.pwd }}
          </div>
        </div>


        <br />
        <button :disabled="!showPwdField" @click="Login" type="submit"
          class="border-0 btn btn-dark button w-100 py-2 font-13 text-white rounded-1">
          <span v-if="loading" class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span>
          <span v-if="!loading">Log In</span>
        </button>
      </div>
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
                placeholder="Enter Confirm Password" v-model="confirm_password" />
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
      errorMessage: "",
      // timeLeft: 60,
      // timer: null,
      // resentMessage: "",
    };
  },
  methods: {
    // ShowOtp(){
    //   this.showOtpPage=true;
    //   this.ShowLoginPage=false;
    // },
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

    checkUserMail() {
      // const user_id = {
      //   user_id: this.formdata.usr,
      // };

      axiosInstance
        .get(`${apis.loginCheckmethod}`, {
          params: { user_id: this.formdata.usr },
        })
        .then((res) => {
          if (res.message) {
            const isFirstLogin = res.message.is_first_login;
            this.user_id_name = res.message.name;
            // console.log(this.user_id_name, "======");
            if (isFirstLogin === 0) {
              const modal = new bootstrap.Modal(
                document.getElementById("changePassword")
              );
              modal.show();
              this.showPwdField = false;
            }
            if (isFirstLogin === 1) {
              this.showPwdField = true;

              // console.log("User is logging in for the first time.");
            } else {
              console.log("User has logged in before.");
            }
          } else {
            console.log("No user data found.");
            this.showPwdField = true; // Show password field when no user data is found
          }
        })
        .catch((error) => {
          console.error("Login error: ", error);
        });
    },

    checkboxChange() {
      const payload = {
        user_id_name: this.user_id_name,
      };

      axiosInstance
        .put(`${apis.loginCheckuseermethod}`, payload)
        .then((res) => {
          console.log("Password updated successfully:", res.data);
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

    Login() {
      this.validatename();
      this.validatepassword();
      if (!this.errors.usr && !this.errors.pwd) {
        this.loading = true; // Set loading to true before API call

        axiosInstance
          .post(apis.login, this.formdata)
          .then((res) => {
            if (res) {

                toast.success("Login Successfully", {
                  autoClose: 2000,
                  transition: "zoom",
                });
                localStorage.setItem("UserName", JSON.stringify(this.storeData));
                setTimeout(() => {
                  this.$router.push({ path: "/todo/receivedform" });
                }, 700);

                this.storeData=res
              localStorage.setItem("UserName", JSON.stringify(this.storeData));
              console.log("this.storeData", this.storeData);
              if (this.formdata.usr) {
                this.userData(this.formdata.usr);
              }
            }
          })
          .catch((error) => {
            console.error("Login error: ", error);
            // toast.error("Login Failed! Please try again.");
          })
          .finally(() => {
            this.loading = false; // Ensure loading is reset after request
          });
      }
    },

    userData(email) {
      // console.log(email, "1");
      axiosInstance
        .get(`${apis.resource}${doctypes.users}/${email}`)
        .then((res) => {
          this.email = res.data.email;
          // console.log(this.email, "2");
          if (this.email) {
            // const queryParams = {
            //   filters: JSON.stringify({ enable: 1 })
            // }
            axiosInstance
              .get(`${apis.resource}${doctypes.EzyEmployeeList}/${this.email}`)
              .then((responce) => {
                const employeeData = responce.data;
                localStorage.setItem("employeeData", JSON.stringify(employeeData));
                localStorage.setItem(
                  "USERROLE",
                  JSON.stringify(employeeData.designation)
                );
              })
              .catch((error) => {
                console.error("Error fetching user data:", error);
              });
          } else {
            localStorage.setItem("employeeData", JSON.stringify(this.storeData));
          }
        })
        .catch((error) => {
          console.error("Error fetching user data:", error);
        });
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

<style scoped>
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
</style>
