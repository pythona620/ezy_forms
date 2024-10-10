<template>
    <div class="form-group">
        <label :for="id">{{ labeltext }}</label>
        <select :id="id" :name="name" v-model="localModel" class="form-control">
            <option v-for="(option, index) in dropDownOptions" :key="index" :value="option">
                {{ option }}
            </option>
        </select>
    </div>
</template>
<script setup>
import { defineProps, defineEmits, ref, watch, computed } from "vue";

const props = defineProps({



    dropDownOptions: { type: Array, default: () => [] },

    labeltext: { type: String },
    name: { type: String, required: true },
    id: { type: String, required: true },
    modelValue: { type: [String, Number, Boolean, Array, null], required: true },
    value: { type: String, default: "" },
    validation: String,
    Required: {
        type: Boolean,
    },

    label: {
        type: Boolean,
        default: false,
    },
    validationStar: {
        type: String
    }
});

const emit = defineEmits(["update:modelValue"]);

const localModel = ref(props.modelValue);

watch(
    () => props.modelValue,
    (newVal) => {
        localModel.value = newVal;
    }
);

watch(localModel, (newVal) => {
    emit("update:modelValue", newVal);
});

const clearDate = () => {
    localModel.value = "";
};


</script>
<style scoped>
.form-control {
    width: 100%;
    height: 32px;
    font-size: var(--ten);

}
</style>