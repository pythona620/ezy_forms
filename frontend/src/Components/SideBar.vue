<template>
    <div class="container-fluid">
        <div class="sidebar pt-2">
            <h1 class="font-12 m-0 text-muted ps-2">Master</h1>
            <aside>
                <ul class=" list-unstyled ">
                    <router-link v-for="(list, index) in sideBarData" :key="index"
                        :to="`/master/${list.name.toLowerCase()}`" class="text-decoration-none text-black"
                        active-class="active-link">

                        <li :title="list.name"><i :class="`bi-icon ps-1 bg-transparent bi ${list.icon} me-3`"></i>
                            {{ list.name }}</li>
                    </router-link>
                </ul>
            </aside>
        </div>
    </div>

</template>
<script setup>

const sideBarData = [
    { name: 'Archive', icon: 'bi bi-archive ' },
    { name: 'Forms', icon: 'bi bi-file-earmark-ruled' },
    { name: 'Trash', icon: 'bi bi-trash' },
    { name: 'Activity-Log', icon: 'bi bi-stopwatch' },
    { name: 'Users', icon: 'bi bi-people' },
    { name: 'E-Signature', icon: 'bi bi-pencil' },


]


</script>
<style scoped>
li {
    font-size: var(--twelve);
    font-weight: var(--font-weight-medium);
    color: var(--text-color);
    padding: 8px 0px;
    white-space: nowrap;
    text-overflow: ellipsis;
    overflow: hidden;
    margin: 0px 0px 0px 11px
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
    color: var(--text-color);
    font-size: var(--thirteen);
    font-weight: var(--font-weight-normal);
    line-height: 26px;
    text-align: left;
    border-radius: 4px;
    padding: 5px 0px;
    margin-top: 8px;


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