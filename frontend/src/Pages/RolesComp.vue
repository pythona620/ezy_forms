<template>
    <div class="mt-4 ps-2">
        <!-- Button trigger modal -->
        <div class="d-flex gap-2 align-items-center">
            <h6 class="m-0 fw-bolder">Roles</h6>
            <button type="button" class="buttoncomp modalbtn " data-bs-toggle="modal" data-bs-target="#exampleModal">
                +
            </button>
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
                        <FormFields tag="select" placeholder="" class="mb-3 form-control" name="roles" id="roles"
                            :Required="false" />
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-outline-danger px-4"
                            data-bs-dismiss="modal">Cancel</button>
                        <button type="button" class=" buttoncomp px-4">Save</button>
                    </div>
                </div>
            </div>
        </div>
        <div class="mt-3">
            <GlobalTable class="custom-table" :tHeaders="tableHeaders" :tData="listdata" />
        </div>
    </div>
</template>
<style scoped>
.modalbtn {
    padding: 1px 7px;

}
</style>
<script setup>
import { ref } from 'vue';
import FormFields from '../Components/FormFields.vue';
import GlobalTable from '../Components/GlobalTable.vue';
const tableHeaders = ref([
    { th: "Roles", td_key: "", icon: "" },

]);
const listdata = ref([])
</script>