<template>
    <div class="headerbackgound">
        <div class="px-3 d-flex gap-2 align-items-center text-white">
            <i class="bi bi-arrow-left"></i>
            <h4 class=" m-0  header-title">
                {{ headertext }}
            </h4>
        </div>
    </div>
</template>
<script>
export default {
    props: {
        headertext: {
            type: String,
            default: ''
        },
    }
}
</script>
<style scoped>
.headerbackgound {
    height: 50px;
    background-color: #fe5358;
    display: flex;
    align-items: center;
}

i {
    font-size: 20px;
    font-weight: 600;
}

.header-title {
    font-size: var(--font-size-md);
    font-weight: var(--font-weight-bold);
    color: #fff;
}
</style>
