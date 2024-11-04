<template>
    <div class="card">
        <div v-if="header" class="card-header">
            <slot name="header">{{ header }}</slot>
        </div>
        <div class="card-body">
            <slot>{{ body }}</slot>
        </div>
        <div v-if="footer" class="card-footer">
            <slot name="footer">{{ footer }}</slot>
        </div>
    </div>
</template>

<script>
export default {
    name: 'CardComponent',
    props: {
        header: {
            type: String,
            default: ''
        },
        body: {
            type: String,
            default: ''
        },
        footer: {
            type: String,
            default: ''
        }
    }
};
</script>

<style scoped>
.card {
    border: 1px solid #ddd;
    border-radius: 4px;
    padding: 16px;
    margin: 16px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.card-header,
.card-footer {
    background-color: #f5f5f5;
    padding: 8px;
    border-bottom: 1px solid #ddd;
}

.card-body {
    padding: 16px;
}
</style>