<template>
    <div>help
        <div class="text-center position-relative">
        </div>
        <div class="dropdown">
            <p class="p-0 actions" data-bs-toggle="dropdown" aria-expanded="false">
                <span>...</span>
            </p>
            <ul class="dropdown-menu actionsdropdown">
                <li v-for="(action, index) in actions" :key="index">
                    <a class="dropdown-item "> <i :class="action.icon"></i> {{ action.name }}</a>
                </li>
            </ul>
        </div>
    </div>

</template>
<script setup>
import { ref } from 'vue';
const actions = ref(
    [
        { name: 'View form', icon: 'fa-solid fa-eye' },
        { name: 'Edit accessibility to dept.', icon: 'fa-solid fa-users' },
        { name: 'Share this form', icon: 'fa-solid fa-share-alt' },
        { name: 'Download Print format', icon: 'fa-solid fa-download' },
        { name: 'Edit Form', icon: 'fa-solid fa-edit' },
        { name: 'In-active this form', icon: 'fa-solid fa-ban' }
    ]
)
</script>