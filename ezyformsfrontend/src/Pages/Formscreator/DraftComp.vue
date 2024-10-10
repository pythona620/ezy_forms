<template>
    <div>

        <FormFields tag="checkbox" :checkOptions="checkOptions" name="exampleCheckbox" id="exampleCheckbox"
            v-model="selectedOptions" labeltext="Choose options:" />
        <p>Selected Radio Value: {{ selectedOptions }}</p>
        <FormFields tag="dropdown" :dropDownOptions="dropDownOptions" name="exampleDropdown" id="exampleDropdown"
            v-model="selectedDropdown" labeltext="Choose an option:" />
        <p>Selected Radio Value: {{ selectedDropdown }}</p>

    </div>
</template>

<script>
import FormFields from '../../Components/FormFields.vue';
export default {
    components: {
        FormFields
    },
    data() {
        return {
            checkOptions: ['Option 1', 'Option 2', 'Option 3'],
            dropDownOptions: ['Option 1', 'Option 2', 'Option 3'],
            selectedOptions: [],
            selectedDropdown: []
        };
    },
};
</script>