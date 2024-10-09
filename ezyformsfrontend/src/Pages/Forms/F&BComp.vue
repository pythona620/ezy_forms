<template>
    <div>
        <div class="ps-1 m-0 d-flex align-items-center">
            <h1 class="font-13"><i class="bi bi-arrow-left"></i><span class="ms-2">Asset request form</span></h1>
        </div>
    </div>
    <div class="d-flex justify-content-center mt-3">
        <div>
            <h1 class="font-12 fw-normal text-center">
                You are requesting for asset.<br> <span class="mt-5">Hope your request be approved. Good luck!</span>
            </h1>

        </div>

    </div>
    <div class="row">
        <div class="col-4">

        </div>
        <div class="col-4">
            <div class="card mt-4">
                <div class="card-body">
                    <FormFields tag="radio" :options="radioOptions" name="exampleRadio" id="exampleRadio"
                        v-model="selectedRadio" labeltext="Raising For:" />
                </div>
            </div>
            <div class="card mt-4">
                <div class="card-body">

                    <FormFields labeltext="Name of the Employee" class="mb-3" type="text" tag="input" name="Value"
                        id="Value" placeholder="Enter Name" v-model="name" />

                </div>
            </div>
            <div class="card mt-4">
                <div class="card-body">

                    <FormFields labeltext="Employee Code" class="mb-3" type="text" tag="input" name="Value" id="Value"
                        placeholder="Enter Code" v-model="code" />

                </div>
            </div>
            <div class="card mt-4">
                <div class="card-body">

                    <FormFields labeltext="Employee Department" class="mb-3 w-100" tag="select" name="dept" id="dept"
                        placeholder="Select Department"
                        :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']"
                        v-model="code" />

                </div>
            </div>
            <div class="card mt-4">
                <div class="card-body">

                    <FormFields labeltext="Employee Desigination" class="mb-3" tag="select" name="desgination"
                        id="desgination" placeholder="Select Desigination"
                        :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']"
                        v-model="code" />

                </div>
            </div>
            <div class="card mt-4 ">
                <div class="card-body">

                    <FormFields labeltext="Employee Desigination" class="mb-3" tag="select" name="desgination"
                        id="desgination" placeholder="Select Desigination"
                        :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']"
                        v-model="code" />

                </div>
            </div>
            <div class="d-flex justify-content-between align-items-center mt-3 mb-4">
                <div>
                    <ButtonComp class="buttoncomp font-10" name="Create Form"></ButtonComp>
                </div>
                <div>
                    <ButtonComp class=" font-10" name="Clear Form"></ButtonComp>
                </div>
            </div>
        </div>

        <div class="col-4"></div>
    </div>

</template>
<script setup>
import FormFields from '../../Components/FormFields.vue';
import ButtonComp from '../../Components/ButtonComp.vue';
import { ref } from 'vue';
const name = ref('')
const radioOptions = ref(['Self',
    'Others']);

// Store the selected radio value
const selectedRadio = ref('');
</script>
<style scoped>
.card-body {
    background-color: var(--sidebar-color);
    border: 1px solid #EEEEEE;
    border-radius: 4px;
}

.form-control {
    width: none;
}
</style>