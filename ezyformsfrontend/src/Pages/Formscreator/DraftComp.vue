<template>
    <div>

        <CheckBoxComp :checkOptions="checkOptions" name="exampleCheckbox" id="exampleCheckbox" v-model="selectedOptions"
            labeltext="Choose options:" />
        <p>Selected Radio Value: {{ selectedOptions }}</p>
        <DropDownComp :dropDownOptions="dropDownOptions" name="exampleDropdown" id="exampleDropdown"
            v-model="selectedDropdown" labeltext="Choose an option:" />
        <p>Selected Radio Value: {{ selectedDropdown }}</p>

    </div>
</template>

<script>
import CheckBoxComp from '../../Components/CheckBoxComp.vue';
// import FormFields from '../../Components/FormFields.vue';
import DropDownComp from '../../Components/DropDownComp.vue';
export default {
    components: {

        CheckBoxComp, DropDownComp
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