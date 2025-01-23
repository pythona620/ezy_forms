<template>
    <div class="grid place-items-center w-full min-h-screen">
        <div class="flex flex-col items-center space-y-4">
            <div class="bg-gray-100 p-6">
                <!-- <VueSignaturePad ref="signature" height="400px" width="1280px" :maxWidth="2" :minWidth="2"
                    :disabled="state.disabled" :options="{
                    penColor: state.options.penColor, backgroundColor: state.options.backgroundColor
                }" /> -->

            </div>

            <button type="button" class=" btn btn-outline-dark mx-1 my-1"
                @click="handleSave('image/jpeg')">Save</button>
            <button type="button" class=" btn btn-outline-dark mx-1 my-1" @click="handleClear">Clear</button>
            <button type="button" class=" btn btn-outline-dark mx-1 my-1" @click="handleUndo">Undo</button>
            <button type="button" class=" btn btn-outline-dark mx-1 my-1" @click="handleDisabled">Disabled</button>
            <button type="button" class=" btn btn-outline-dark mx-1 my-1"
                @click="handleFromDataURL('https://github.com/selemondev.png')">
                FronData URL
            </button>
            <button type="button" class=" btn btn-outline-dark mx-1 my-1" @click="handleAddWaterMark">Add
                watermark</button>
        </div>
    </div>
</template>

<script setup>
// import { VueSignaturePad } from "@selemondev/vue3-signature-pad"
import { onMounted, ref } from "vue";

const state = ref({
    options: {
        penColor: 'rgb(0, 0, 0)',
        backgroundColor: 'rgb(255, 255, 255)'
    },
    disabled: false,
})

const signature1 = ref(null)
const colors = [
    {
        color: 'rgb(51, 133, 255)'
    },

    {
        color: 'rgb(85, 255, 51)'
    },

    {
        color: 'rgb(255, 85, 51)'
    }
];

const activeColor = ref();

const signature = ref();

const handleSave = () => {
    return console.log(signature.value.undo())
};
const handleClear = () => {
    return signature.value.clearCanvas()
};
const handleUndo = () => {
    return signature.value.undo()
};

const handleDisabled = () => {
    return state.disabled = !state.disabled;
};

const handleFromDataURL = (url) => {
    return signature.value.fromDataURL(url);
};

const handleAddWaterMark = () => {
    return signature1.value.addWaterMark({
        text: "Selemondev",          // watermark text, > default ''
        font: "20px Arial",         // mark font, > default '20px sans-serif'
        style: 'all',               // fillText and strokeText,  'all'/'stroke'/'fill', > default 'fill
        fillStyle: "red",           // fillcolor, > default '#333'
        strokeStyle: "blue",      // strokecolor, > default '#333'
        x: 100,                     // fill positionX, > default 20
        y: 200,                     // fill positionY, > default 20
        sx: 100,                    // stroke positionX, > default 40
        sy: 200                     // stroke positionY, > default 40
    });
}
</script>
