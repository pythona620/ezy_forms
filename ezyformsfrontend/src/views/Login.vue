<template>
	
	<div class="bg-img">
		<div class="input-div p-5">
			<div class="d-flex gap-2 p-2 justify-content-center align-items-center">
                                <div><img class="imgmix" src="../assets/favicon.jpg" /></div>
                                <div class="m-0">
                                    <p class="fontimgtext fw-bold m-0">EZY | Forms</p>
                                </div>
                            </div>
				
			<div class="mt-3">
				
				<label for="name" class="font-13">UserName</label><br>
				<input type="text" class=" form-control m-0 " id="name" v-model="formdata.usr" @input="validatename"
					:class="{ 'is-invalid': errors.usr }" />
				
				<div class="invalid-feedback font-11 mt-1" v-if="errors.usr">
					{{ errors.usr }}
				</div>
			</div>

			<div class="inputbox mt-3">
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
			<button @click="Login" type="submit" class="border-0  btn btn-dark button w-100 py-2 text-white rounded-1">
				Log In
			</button>
		</div>
	</div>
</template>

<script>
import { apis, doctypes } from '../shared/apiurls';
import axiosInstance from '../shared/services/interceptor';
import { toast } from "vue3-toastify";
import "vue3-toastify/dist/index.css";
export default {
	props: ['id'],
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
		Login() {
			this.validatename();
			this.validatepassword();

			if (!this.errors.usr && !this.errors.pwd) {
				axiosInstance.post(apis.login, this.formdata).then((res) => {
					if (res) {
						toast.success("Login Successfully", { autoClose: 2000 });
						setTimeout(() => {
							this.$router.push({ path: '/forms/department/:id' });
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
				console.log('Form is invalid');
			}
		},
		userData(email) {
			axiosInstance.get(`${apis.resource}${doctypes.users}/${email}`)
				.then((res) => {
					this.email = res.data.email
					console.log(this.email);


					axiosInstance.get(`${apis.resource}${doctypes.EzyEmployeeList}/${this.email}`)
						.then((responce) => {
							const employeeData = responce.data
							localStorage.setItem('employeeData', JSON.stringify(employeeData));
							console.log(employeeData, "11111111111111111111");

						})
						.catch((error) => {
							console.error("Error fetching user data:", error);
						});

				})
				.catch((error) => {
					console.error("Error fetching user data:", error);
				});
		}
	},
};
</script>

<style scoped>
.loginpageheight{
	height: 100vh;

}
.fontimgtext{
	font-size: 17px;
	color: #111111;
	margin: 0;
}
.bg-img {
	/* background-image: url(../assets/ElektronicsDevice.webp) !important; */
	background-size: 100vw 100vh;
	/* width: 100vw; */
	height: 100vh;
	color: #111111;
	display: flex;
	justify-content: center;
	align-items: center;
}

.label{
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
	background: transparent;
	/* border: none; */
	/* outline: none; */
	font-size: 1em;
	font-weight: 600;
	padding: 0 35px 0 5px;
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