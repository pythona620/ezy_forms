<template>

	<div class="bg-img">
		<div class="input-div p-5">
			<div class="d-flex gap-2 p-2 justify-content-center align-items-center">
				<div><img class="imgmix" src="../assets/favicon.jpg" /></div>
				<div class="m-0">
					<p class="fontimgtext fw-medium m-0">EZY | Forms</p>
				</div>
			</div>

			<div class="mt-3">

				<label for="name" class="font-13">User name</label><br>
				<input type="text" class=" form-control m-0 bg-white " id="name" v-model="formdata.usr"
					@input="validatename" @change="checkUserMail()" :class="{ 'is-invalid': errors.usr }" />

				<div class="invalid-feedback font-11 mt-1" v-if="errors.usr">
					{{ errors.usr }}
				</div>
			</div>

			<div class="inputbox mt-3" v-if="showPwdField">
				<label for="password" class="font-13">Password</label><br>
				<!-- <span class="icon"><i class="bi bi-lock-fill"></i></span> -->
				<input class="form-control m-0" :type="showPassword ? 'text' : 'password'" id="password"
					v-model="formdata.pwd" @input="validatepassword" @keydown.enter="Login"
					:class="{ 'is-invalid': errors.pwd }" />

				<!-- Toggle icon for show/hide password -->
				<span class="toggle-icon" @click="togglePasswordVisibility">
					<i :class="showPassword ? 'bi bi-eye' : 'bi bi-eye-slash'"></i>
				</span>
				<div class="invalid-feedback font-10" v-if="errors.pwd">
					{{ errors.pwd }}
				</div>
			</div>
			<br>
			<button @click="Login" type="submit"
				class="border-0  btn btn-dark button w-100 py-2 font-13 text-white rounded-1">
				Log In
			</button>
		</div>

		<div class="modal fade" id="changePassword" data-bs-backdrop="static" data-bs-keyboard="false" tabindex="-1"
			aria-labelledby="changePasswordLabel" aria-hidden="true">
			<div class="modal-dialog modal-dialog-centered modal-sm">
				<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title font-14 fw-bold" id="changePasswordLabel">Change Password</h5>
						<button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
					</div>
					<div class="modal-body">
						<!-- <FormFields tag="select" placeholder="Category" class="mb-3" name="roles" id="roles"
                            @change="changingCategory" :Required="false" :options="categoryOptions"
                            v-model="selectedData.selectedCategory" /> -->
						<div class=" mb-2">
							<label class="raise-label" for="changepass">New Password</label>
							<FormFields class="mb-3" tag="input" type="text" name="changepass" id="changepass"
								placeholder="Enter" v-model="new_password" />
						</div>
						<div class=" mb-2">
							<label class="raise-label" for="confirmpass">Confirm Password</label>
							<FormFields class="" tag="input" type="text" name="confirmpass" id="confirmpass"
								placeholder="Enter" v-model="confirm_password" />
							<span v-if="passwordsMismatch" class="text-danger font-10 m-0 ps-2">Passwords do not
								match.</span>
						</div>
						<!-- <FormFields tag="select" placeholder="Form" class="mb-3" name="roles" id="roles"
                            :Required="false" :options="formList" v-model="selectedData.selectedform" /> -->
					</div>
					<div>
						<div class=" d-flex justify-content-center align-items-center p-3">
							<button class="btn btn-dark font-12 w-100" type="submit" @click="passwordChange()">
								Confirm New Password</button>
						</div>
					</div>

				</div>
			</div>
		</div>

	</div>
</template>

<script>
import { apis, doctypes } from '../shared/apiurls';
import axiosInstance from '../shared/services/interceptor';
import FormFields from '../Components/FormFields.vue';
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
export default {
	props: ['id'],
	components: {
		FormFields
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
			user_id: '',
			passwordsMismatch: false

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

		checkUserMail() {
			const queryParams = {
				fields: JSON.stringify(["*"]),
				filters: JSON.stringify([["user_id", "=", this.formdata.usr]]),
			};

			axiosInstance.get(`${apis.resource}${doctypes.CheckUser}`, { params: queryParams })
				.then((res) => {
					if (res.data.length > 0) {

						const isFirstLogin = res.data[0].is_first_login;
						this.user_id = res.data[0].name
						console.log(isFirstLogin, "-----");
						if (isFirstLogin === 0) {
							const modal = new bootstrap.Modal(document.getElementById('changePassword'));
							modal.show();
							this.showPwdField = false;

						}
						if (isFirstLogin === 1) {
							this.showPwdField = true;

							console.log("User is logging in for the first time.");
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
					this.showPwdField = true; // Show password field in case of an error
				});
		},


		checkboxChange() {
			const payload = {
				is_first_login: 1,
			};

			axiosInstance.put(`${apis.resource}${doctypes.CheckUser}/${this.user_id}`, payload)
				.then((res) => {
					console.log("Password updated successfully:", res.data);
					if (res.data.is_first_login === 1) {
						this.showPwdField = true;
					}
				})
				.catch((error) => {
					console.error("Error:", error);
				});
		},


		passwordChange() {
			// if (passwordsMismatch) {
			// 	console.error("Passwords do not match.");
			// 	return;
			// }
			// console.log(this.new_password);

			const payload = {
				new_password: this.new_password,
			};

			axiosInstance.put(`${apis.resource}${doctypes.users}/${this.formdata.usr}`, payload)
				.then((res) => {
					if (res.data) {
						console.log("Password updated successfully:", res.data);
						toast.success('Password changed Successfully', { autoClose: 300 });
						const modal = bootstrap.Modal.getInstance(document.getElementById('changePassword'));
						modal.hide();
						this.checkboxChange()
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
				axiosInstance.post(apis.login, this.formdata).then((res) => {
					if (res) {
						toast.success("Login Successfully", { autoClose: 2000, "transition": "zoom" });
						setTimeout(() => {
							this.$router.push({ path: '/todo/receivedform' });
						}, 700);
						this.storeData = res;
						localStorage.setItem('UserName', JSON.stringify(this.storeData));
						if (this.formdata.usr) {
							this.userData(this.formdata.usr);
						}

					}
				}).catch((error) => {
					console.error("Login error: ", error);
				});
			} else {

			}
		},

		userData(email) {
			console.log(email, "1");
			axiosInstance.get(`${apis.resource}${doctypes.users}/${email}`)
				.then((res) => {
					this.email = res.data.email
					console.log(this.email, "2");
					if (this.email) {
						axiosInstance.get(`${apis.resource}${doctypes.EzyEmployeeList}/${this.email}`)
							.then((responce) => {
								const employeeData = responce.data
								localStorage.setItem('employeeData', JSON.stringify(employeeData));
								localStorage.setItem('USERROLE', JSON.stringify(employeeData.designation));

							})
							.catch((error) => {
								console.error("Error fetching user data:", error);
							});
					}
					else {
						localStorage.setItem('employeeData', JSON.stringify(this.storeData));

					}

				})
				.catch((error) => {
					console.error("Error fetching user data:", error);
				});
		}
	},
	// computed: {
	// 	passwordsMismatch() {
	// 		return (
	// 			this.new_password &&
	// 			this.confirm_password &&
	// 			this.new_password !== this.confirm_password
	// 		);
	// 	}
	// }
};
</script>

<style scoped>
.loginpageheight {
	height: 100vh;

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
	border: 1px solid #EEEEEE;
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
	transition: .5s;
}

.input-box input:focus~label,
.input-box input:valid~label {
	top: 3px;
}

.input-box input {
	width: 100%;
	/* height: 100%; */
	background: #FFFFFF;
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