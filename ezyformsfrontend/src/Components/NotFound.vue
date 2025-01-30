<template>
    <div class=" h-100 mt-5">
        <div class="d-flex justify-content-center align-items-center">
            <div class="text-center">
                <img src="../assets/404.png" alt="" class="w-50 img-fluid" />

                <router-link to="/">
                    <h6 class=" d-flex align-items-center justify-content-center mt-4"><span><i
                                class="bi bi-arrow-left me-1"></i></span>Go to
                        Home</h6>
                </router-link>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "NotFound",
    data() {
        return {};
    },
};
</script>

<style scoped></style>
