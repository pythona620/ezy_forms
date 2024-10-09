<template>
    <div>

    </div>
</template>
<script setup>

// import axios from 'axios';
import { onMounted } from 'vue';
import axiosInstance from '../../shared/services/interceptor';
import { apis, doctypes } from '../../shared/apiurls';

function fetchData() {
    axiosInstance.get(apis.resource + doctypes.users).then((res) => {
        console.log(res);
    })
}
onMounted(() => {
    fetchData()
})
</script>