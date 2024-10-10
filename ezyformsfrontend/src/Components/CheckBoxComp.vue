<template>
    <div class="form-check">
        <div v-for="(item, index) in checkOptions" :key="index">
            <label :for="`${id}-${index}`" class="form-check-label">
                <input type="checkbox" :name="name" :id="`${id}-${index}`" :value="item" v-model="localModel"
                    class="form-check-input" />
                {{ item }}
            </label>
        </div>
    </div>
</template>
<script setup>
import { defineProps, defineEmits, ref, watch, computed } from "vue";

const props = defineProps({
    type: {
        type: String,
    },
    isFlex: {
        type: Boolean,
        default: true,
    },


    checkOptions: { type: Array, default: () => [] },

    placeholder: { type: String },
    labeltext: { type: String },
    name: { type: String, required: true },
    id: { type: String, required: true },
    modelValue: { type: [String, Number, Boolean, Array, null], required: true },
    value: { type: String, default: "" },


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




</script>
<style lang="scss" scoped>
.form-check {
    margin-bottom: 10px;
}

.form-check-label {
    margin-right: 15px;
    font-size: var(--thirteen);
}
</style>
