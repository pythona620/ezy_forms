<template>
    <div class="mt-2">
        <div v-if="showFilters" class="form_archived">
            <div>
                <img class="m-auto d-flex" src="../../assets/box with files.svg" />
                <h1 class="font-14 fw-bold m-0 text-center">
                    The forms are archived.
                </h1>
                <p class="m-0 fw-normal font-12">You can access your archived forms by filtering.</p>
                <div class=" mt-3">
                    <button type="button" class=" filterbtn d-flex m-auto align-items-center" data-bs-toggle="modal"
                        data-bs-target="#exampleModal">
                        <h1 class="font-12 d-flex align-items-center p-0 m-0"> <span class=""><i
                                    class="bi bi-funnel"></i></span> Filters</h1>

                    </button>


                </div>

            </div>

        </div>
        <!-- Modal -->
        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">

                    <div class="modal-body">
                        <div class="row mt-3">
                            <div class="col-6">
                                <!-- doctype_name -->
                                <label class="font-13 ps-1" for="Requested">Form name:</label>
                                <FormFields class="mb-3" tag="input" type="search" name="Requested" id="Requested"
                                    placeholder="Search Form name" v-model="filterObj.doctype_name" />
                            </div>
                            <div class="col-6">
                                <!-- doctype_name -->
                                <label class="font-13 ps-1" for="Requested">Requested By:</label>
                                <FormFields class="mb-3" tag="input" type="search" name="Requested" id="Requested"
                                    placeholder="Search" v-model="filterObj.requested_by" />
                            </div>
                            <div class="col-6">
                                <label class="font-13 ps-1 fw-medium" for="dept">Requested Dept:</label>
                                <FormFields type="search" tag="input" placeholder="search Department" class="mb-3"
                                    name="dept" v-model="filterObj.role" id="dept" :Required="false" />
                            </div>
                            <!-- <div class=" col-6">
                                <label class="font-13 ps-1" for="Requested">Requested Period:</label>

                                <FormFields class="mb-3" tag="input" type="date" name="Requested" id="Requested"
                                     v-model="filterObj.date" />
                            </div> -->
                            <!-- <div class="col-6">
                                <label class="font-13 ps-1" for="Requested">Requested Period:</label>
                                <DatePicker class="datePicker" :enable-time-picker="false" :format="'yyyy-MM-dd'" v-model="filterObj.dateRange" range
                                    placeholder="Select From - To Date" />
                            </div>  -->
                            <div class="col-6">
                                <label class="font-13 ps-1 fw-medium" for="dept">Approval Status:</label><br>
                                <!-- <FormFields tag="select" type="select" :options="radioOptions" name="exampleRadio" id="exampleRadio"
                                    v-model="filterObj.selectedRadio" /> -->

                                <select class="status-select" v-model="filterObj.selectedRadio" name="exampleRadio"
                                    id="exampleRadio">
                                    <option value="" disabled selected>Select an option</option>
                                    <option v-for="option in radioOptions" :key="option" :value="option">
                                        {{ option }}
                                    </option>
                                </select>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" @click="clearFilter" class="cancelfilter border-0 text-nowrap font-10 "
                            data-bs-dismiss="modal"><span class="font-14 me-1">x</span>Cancel Filter</button>

                        <button type="button" :disabled="isFilterEmpty"
                            class="applyfilter text-nowrap border-0 btn btn-dark text-white font-10 d-flex justify-content-center align-items-center"
                            data-bs-dismiss="modal" @click="applyFilter"><span class="font-16 me-1"><i
                                    class="bi bi-check2 "></i></span>
                            Apply
                            Filter</button>
                    </div>
                </div>
            </div>
        </div>
        <div v-if="tableShow">
            <div class="mt-2">
                <div class="d-flex justify-content-end me-3">
                    <button data-bs-toggle="modal" data-bs-target="#exampleModal" class="filter-btn">
                        <i class="bi bi-funnel me-2"></i> Filters
                        <span v-if="appliedFilterCount" class="badge bg-primary ms-2">
                            {{ appliedFilterCount }}
                        </span>
                    </button>
                </div>
                <GlobalTable class="mt-2" :tHeaders="tableheaders" :tData="tableData" />
            </div>
        </div>
    </div>

</template>

<script setup>
import FormFields from '../../Components/FormFields.vue';
import GlobalTable from '../../Components/GlobalTable.vue';
import axiosInstance from "../../shared/services/interceptor";
import { apis, doctypes } from "../../shared/apiurls";
import { ref, computed } from 'vue';
// import DatePicker from "@vuepic/vue-datepicker"; 
// import "@vuepic/vue-datepicker/dist/main.css";

// import { format } from "date-fns";
// const dateRange = ref();

const showFilters = ref(true);
const tableShow = ref(false);
const tableData = ref([]);

const filterObj = ref({
    doctype_name: "",
    requested_by: "",
    role: "",
    date: "",
    selectedRadio: "",
    dateRange: ""
});

const tableheaders = ref([
    { th: "Request ID", td_key: "name" },
    { th: "Form name", td_key: "doctype_name" },
    { th: "Owner of form", td_key: "role" },
    { th: "Requested on", td_key: "requested_on" },
    { th: "Requested By", td_key: "requested_by" },
    { th: "Approval Status", td_key: "status" },
]);

const radioOptions = ref(['All', 'Completed', 'Request Raised', 'In Progress', 'Request Cancelled']);

const isFilterEmpty = computed(() => {
    return !Object.values(filterObj.value).some(val => val);
});

const appliedFilterCount = ref(0);

const activeFilterCount = computed(() => {
    let count = 0;
    if (filterObj.value.doctype_name?.trim()) count++;
    if (filterObj.value.requested_by?.trim()) count++;
    if (filterObj.value.role?.trim()) count++;
    if (filterObj.value.dateRange?.length === 2 && filterObj.value.dateRange[0] && filterObj.value.dateRange[1]) count++;
    if (filterObj.value.selectedRadio) count++;

    return count;
});

const clearFilter = () => {
    filterObj.value = {
        doctype_name: "",
        requested_by: "",
        role: "",
        date: null,
        selectedRadio: "",
        dateRange: ""

    };
    showFilters.value = true;
    tableShow.value = false;

};

// const formatDate = (date) => format(new Date(date), "yyyy/M/d");

const applyFilter = () => {
    tableShow.value = true;
    showFilters.value = false;
    appliedFilterCount.value = activeFilterCount.value;

    const filters = [];
    if (filterObj.value.requested_by) {
        filters.push(["requested_by", "like", `%${filterObj.value.requested_by}%`]);
    }
    if (filterObj.value.doctype_name) {
        filters.push(["doctype_name", "like", `%${filterObj.value.doctype_name}%`]);
    }
    if (filterObj.value.role) {
        filters.push(["role", "like", `%${filterObj.value.role}%`]);
    }
    if (filterObj.value.date) {
        filters.push(["requested_on", ">=", formatDate(filterObj.value.date)]);
    }
    if (filterObj.value.selectedRadio && filterObj.value.selectedRadio !== "All") {
        filters.push(["status", "=", filterObj.value.selectedRadio]);
    }
    // if (filterObj.value.dateRange && filterObj.value.dateRange.length === 2) {
    //     const [startDate, endDate] = filterObj.value.dateRange.map(formatDate);
    //     filters.push(["requested_on", ">=", startDate]);
    //     filters.push(["requested_on", "<=", endDate]);
    // }

    axiosInstance
        .get(`${apis.resource}${doctypes.WFWorkflowRequests}`, {
            params: {
                fields: JSON.stringify(["*"]),
                filters: JSON.stringify(filters),
            },
        })
        .then((res) => {
            tableData.value = res.data;
        })
        .catch((error) => {
            console.error("Error fetching records:", error);
        });
};

// onMounted(() => {
//     tableShow.value = false; // Initially hide the table
// });
</script>

<style scoped>
.form_archived {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
}

.status-select {
    height: 32px !important;
    width: 100%;
    line-height: 30px;
    outline: none;
    box-shadow: none;
    border: 1px solid #dee2e6;
    background: transparent;
    border-radius: 4px;
    font-size: 13px;
    padding:0px 10px;
    transition: border 0.3s ease-in-out, border-radius 0.3s ease-in-out;
}

.status-select option {
    font-size: 13px;
}

.filter-btn {
    background-color: var(--sidebar-color);
    border: 1px solid #D8D6FF;
    font-size: var(--fourteen);
    padding: 5px 23px;
    border-radius: 4px;
    color: #3021FE;
    display: flex;
    align-items: center;
}

.filterbtn {
    background-color: var(--sidebar-color);
    border: 1px solid #D8D6FF;
    height: 34px;
    width: 90px;
    font-size: var(--fourteen);
    padding: 5px 23px;
    border-radius: 4px;
    color: #3021FE;
}

.cancelfilter {
    width: 150px;
    height: 34px;
    border-radius: 6px;
    background-color: #f1f1f1;
    color: #111111;
    padding: 8px 20px;
}

.applyfilter {
    width: 150px;
    height: 34px;
    border-radius: 6px;
    /* background-color: #f1f1f1; */
    /* color: #111111; */
    padding: 8px 20px;
}

.datePicker {
    cursor: pointer;
    height: 32px !important;
}
</style>