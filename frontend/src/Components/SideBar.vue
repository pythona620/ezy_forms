<template>
    <div class="sidebar pt-3">
        <aside>
            <ul class=" list-unstyled ">
                <router-link v-for="(list, index) in sideBarData" :key="index" :to="`/${list.name}`"
                    class="text-decoration-none text-black " active-class="active-link">
                    <li :title="list.name"><i :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                        {{ list.name }}</li>
                </router-link>
            </ul>
        </aside>
    </div>
</template>
<script setup>

const sideBarData = [
    { name: 'Roles', icon: 'bi-person-fill ' },
    { name: 'RoleMatrix', icon: 'bi-bag-fill' },
    { name: 'Workflows', icon: 'bi-diagram-2' },

]


</script>
<style scoped>
li {
    font-size: var(--thirteen);
    font-weight: var(--font-weight-medium);
    color: var(--black-color);
    padding: 8px 17px;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
    margin: 0px 0px 0px 25px
}



.bi-icon {
    font-size: var(--sixteen);
}

.sidebar {
    height: 93.5dvh;
    background-color: var(--sidebar-color);
}

.active-link>li {
    background-color: var(--white-color);
    color: var(--black-color);
    font-size: var(--thirteen);
    font-weight: var(--font-weight-normal);
    line-height: 26px;
    text-align: left;
    border-radius: 4px;


}

.active-link>li:hover {
    background-color: var(--white-color);
    color: var(--black-color);
    font-size: var(--thirteen);
    font-weight: var(--font-weight-normal);
    line-height: 26px;
    text-align: left;
    border-radius: 4px;


}
</style>