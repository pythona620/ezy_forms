<template>
    <div class="main-div">
        <div class="py-2">
            <div class="card card-div border-0">
                <span>
                    <img src="../../assets/profile.svg" class="img-fluid profile-img">
                </span>

                <div class="d-flex justify-content-between align-items-end mt-4 ms-1">
                    <div>
                        <h6>{{ employeeData.emp_name }}</h6>
                        <span><i class="bi bi-person-fill me-2"></i>{{ employeeData.emp_code }}</span>
                    </div>
                    <span><i class="bi bi-envelope-open-fill me-2"></i>{{ employeeData.emp_mail_id }}</span>
                    <span class="text-secondary">Designation: <strong>{{ employeeData.designation }}</strong></span>
                    <span class="text-secondary">Department: <strong>{{ employeeData.department }}</strong></span>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted, ref } from "vue";

const employeeData = ref({});


onMounted(() => {
    employeeData.value = JSON.parse(localStorage.getItem('employeeData')) || [];
})
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
    width: 60px;
}

span {
    font-size: 14px;
    font-weight: 500;
    line-height: 19.5px;

}
</style>