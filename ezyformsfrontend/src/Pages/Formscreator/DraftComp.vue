<template>
    <div>
        <!-- Render FormFields for Radio Button -->
        <FormFields tag="radio" :options="radioOptions" name="exampleRadio" id="exampleRadio" v-model="selectedRadio"
            labeltext="Choose an option:" />

        <!-- Display selected radio button value -->
        <p>Selected Radio Value: {{ selectedRadio }}</p>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import FormFields from '../../Components/FormFields.vue';  // Import your FormFields component

// Define the options for the radio buttons
const radioOptions = ref(['Option 1', 'Option 2', 'Option 3']);

// Store the selected radio value
const selectedRadio = ref('');
</script>