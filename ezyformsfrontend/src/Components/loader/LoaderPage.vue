<template>
    <div class="loader-main">
        <div class="loader-circles">
            <div class="circle"></div>
            <div class="circle"></div>
            <div class="circle"></div>
            <div class="circle"></div>
        </div>
        <!-- <div class="loader-text">Loading...</div> -->
    </div>
</template>

<script>
export default {
    name: "LoadingScreen",
};
</script>

<style scoped>
.loader-main {
    width: 100%;
    height: 100vh;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    background-color: #00000041;
    opacity: 0.9;
    position: absolute;
    z-index: 1007;
}

.loader-circles {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100px;
}

.circle {
    width: 15px;
    height: 15px;
    border-radius: 50%;
    background-color: #00000041;
    animation: bounce 1s infinite ease-in-out;
}

.circle:nth-child(1) {
    animation-delay: 0s;
}

.circle:nth-child(2) {
    animation-delay: 0.2s;
}

.circle:nth-child(3) {
    animation-delay: 0.4s;
}

.circle:nth-child(4) {
    animation-delay: 0.6s;
}

@keyframes bounce {

    0%,
    100% {
        transform: translateY(0);
    }

    50% {
        transform: translateY(-15px);
    }
}

.loader-text {
    margin-top: 20px;
    font-size: 1.5rem;
    font-weight: bold;
    animation: textAnimation 2s infinite ease-in-out;
    color: var(--highlightColor);
}

@keyframes textAnimation {

    0%,
    100% {
        transform: scale(1);
        color: var(--redColor);
    }

    50% {
        transform: scale(1.1);
        color: var(--highlightColor);
    }
}
</style>