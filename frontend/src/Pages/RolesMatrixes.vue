<template>
    <div class="mt-2 ps-2">
        <!-- Button trigger modal -->
        <div class="d-flex justify-content-between align-items-center">
            <div class="d-flex gap-2 align-items-center">
                <h6 class="m-0 fw-bolder">Role Matrix</h6>
                <button type="button" class="buttoncomp modalbtn " data-bs-toggle="modal"
                    data-bs-target="#exampleModal">
                    +
                </button>
            </div>
            <div class="d-flex align-items-center w-50">
                <FormFields tag="select" placeholder="" class="mb-3 w-100" name="roles" id="roles" :Required="false" />

                <FormFields tag="select" placeholder="" class="mb-3 w-100" name="roles" id="roles" :Required="false" />
            </div>
        </div>


        <!-- Modal -->
        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title" id="exampleModalLabel">Select Role</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <!-- :options="options" v-model="table_filters.outletOption"  -->
                        <label for="roles">Role:</label>
                        <FormFields tag="select" placeholder="" class="mb-3 w-100" name="roles" id="roles"
                            :Required="false" />
                        <label for="roles">User:</label>
                        <FormFields tag="select" placeholder="" class="mb-3 w-100" name="User" id="user"
                            :Required="false" />
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-danger px-4"
                            data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class=" buttoncomp px-4">Save changes</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="mt-3">
            <GlobalTable class="custom-table" :tHeaders="tableHeaders" :tData="listdata" />
        </div>
    </div>
</template>
<script setup>
import { ref } from 'vue';
import FormFields from '../Components/FormFields.vue';
import GlobalTable from '../Components/GlobalTable.vue';
const tableHeaders = ref([
    { th: "Roles", td_key: "", icon: "" },
    { th: "Users", td_key: "", icon: "" },
]);
const listdata = ref([])
</script>
<style scoped>
.modalbtn {
    padding: 1px 7px;

}
</style>