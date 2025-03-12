<template>
    <div>

        <div class="ps-2">
            <div class="d-flex justify-content-between align-items-center py-2 ">
                <div>
                    <!-- <h1 class="m-0 font-13">
                    Archived forms
                </h1>
                <p class="m-0 font-11 pt-1">
                    1239 Requests
                </p> -->
                </div>
                <div class="d-flex p-1 gap-3 align-items-center">
                    <div class="d-flex  gap-2">
                        <!-- <div class=" d-flex align-items-center">
                            <FormFields labeltext="" class="" tag="input" type="search" placeholder="Search File Name"
                                name="Value" id="Value" v-model="filterObj.search" isCheckbox='true' />
                        </div> -->
                        <!-- <div>
                        <FormFields tag="select" placeholder="Filter By" class="p-1" name="roles"
                            v-model="filterObj.selectoption" id="roles" :Required="false"
                            :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']" />
                    </div> -->
                    </div>
                    <!-- <div v-if="tableShow" class="d-flex align-items-center mb-1">
                    <ButtonComp class="buttoncomp font-10" data-bs-toggle="modal" data-bs-target="#exampleModal"
                        name="Apply filters"></ButtonComp>
                </div>
                <div class="d-flex align-items-center mb-1">
                    <ButtonComp class="buttoncomp font-10" name="Create form"></ButtonComp>
                </div> -->
                </div>
            </div>
        </div>
        <!-- <div v-if="formarchived" class="form_archived">
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

        </div> -->
        <!-- Modal -->
        <!-- <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-xl">
                <div class="modal-content">

                    <div class="modal-body">
                        <div class="row">
                            <div class="col-3">
                                <label class="font-13 ps-1" for="Requested">Requested By:</label>
                                <FormFields class="mb-3" tag="input" type="search" name="Requested" id="Requested"
                                    placeholder="Search" v-model="filterObj.search" />
                            </div>
                            <div class="col-3">
                                <label class="font-13 ps-1 fw-medium" for="dept">Requested Dept:</label>
                                <FormFields tag="select" placeholder="Select Department" class="mb-3" name="dept"
                                    v-model="filterObj.selectoption" id="dept" :Required="false"
                                    :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']" />
                            </div>
                            <div class="col-3">
                                <label class="font-13 ps-1" for="dept">Owner OF Form:</label>
                                <FormFields tag="select" placeholder="Select Department" class="mb-3" name="dept"
                                    v-model="filterObj.selectoption" id="dept" :Required="false"
                                    :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']" />
                            </div>
                            <div class="col-3">
                                <label class="font-13 ps-1" for="dept">Form Category:</label>
                                <FormFields tag="select" placeholder="Select Department" class="mb-3" name="dept"
                                    v-model="filterObj.selectoption" id="dept" :Required="false"
                                    :options="['JW Marriott Golfshire Banglore', 'JW Marriott Golfshire Banglore']" />
                            </div>
                            <div class="col-3">
                                <label class="font-13 ps-1" for="Requested">Form Name:</label>
                                <FormFields class="mb-3" tag="input" type="search" name="Requested" id="Requested"
                                    placeholder="Search" v-model="filterObj.search" />
                            </div>
                            <div class="col-3">
                                <label class="font-13 ps-1" for="Requested">Requested Period:</label>
                                <FormFields class="mb-3" tag="input" type="date" name="Requested" id="Requested"
                                    placeholder="Jan-2024-Dec-2024" v-model="filterObj.search" />
                            </div>
                            <div class="col-3">
                                <FormFields tag="radio" :options="radioOptions" name="exampleRadio" id="exampleRadio"
                                    v-model="filterObj.selectedRadio" labeltext="Approval Status" />
                            </div>
                            <div class="col-3">
                                <label class="font-13 ps-1" for="Requested">Requested Id:</label>
                                <FormFields class="mb-3" tag="input" type="search" name="Requested" id="Requested"
                                    placeholder="Search" v-model="filterObj.search" />
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="cancelfilter border-0 text-nowrap font-10 "
                            data-bs-dismiss="modal"><span class="font-14 me-1">x</span>Cancel Filter</button>

                        <button type="button"
                            class="applyfilter text-nowrap border-0 btn btn-dark text-white font-10 d-flex justify-content-center align-items-center"
                            data-bs-dismiss="modal" @click="applyFilter()"><span class="font-16 me-1"><i
                                    class="bi bi-check2 "></i></span>
                            Apply
                            Filter</button>
                    </div>
                </div>
            </div>
        </div> -->
        <div>
            <div class="mt-2">
                <GlobalTable :tHeaders="tableheaders" :tData="tableData" isAction='true' actionType="dropdown" />
            </div>
        </div>
    </div>

</template>
<script setup>
// import FormFields from '../../Components/FormFields.vue';
import ButtonComp from '../../Components/ButtonComp.vue';
import GlobalTable from '../../Components/GlobalTable.vue';
import axiosInstance from "../../shared/services/interceptor";
import { apis, doctypes } from "../../shared/apiurls";
import { EzyBusinessUnit } from "../../shared/services/business_unit";
import { ref, onMounted,computed } from 'vue';

const businessUnit = computed(() => {
  return EzyBusinessUnit.value;
});
const newBusinessUnit = ref({ business_unit: "" });

const filterObj = ref({
    requested_by: '',
    doctype_name: '', 
    status: '',
    name: '',
})
const tableShow = ref(false);
const formarchived = ref(true);
const tableData = ref([]);
const totalRecords = ref(0);
const idDta = ref([]);
const docTypeName = ref([]);
const statusOptions = ref([]);


const tableheaders = ref([
  { th: "Request ID", td_key: "name" },
  { th: "Form name", td_key: "doctype_name" },
  { th: "Owner of form", td_key: "role" },
  { th: "Requested on", td_key: "requested_on" },
  { th: "Requested department", td_key: "role" },
  { th: "Approval Status", td_key: "status" },
]);

// function applyFilter() {
//     tableShow.value = true;
//     formarchived.value = false;
// }

onMounted(()=>{
    receivedForMe()
})


function receivedForMe(data) {
    // Initialize filters array for building dynamic query parameters
    const EmpRequestMail = JSON.parse(localStorage.getItem("employeeData"));

    // Calculate the date one month ago
    const oneMonthAgo = new Date();
    oneMonthAgo.setMonth(oneMonthAgo.getMonth() - 1);
    const formattedDate = oneMonthAgo.toISOString().split('T')[0];

    const filters = [
        ["requested_by", "like", EmpRequestMail.emp_mail_id],
        ["property", "like", `%${newBusinessUnit.value.business_unit}%`],
        ["status", "=", "Completed"],
        ["creation", "<", formattedDate] // Filter to include records before the last month
    ];

    if (data) {
        filters.push(data);
    }

    // Define query parameters for data and count retrieval
    const queryParams = {
        fields: JSON.stringify(["*"]),
        limit_page_length: filterObj.value?.limitPageLength,
        limit_start: filterObj.value?.limit_start,
        filters: JSON.stringify(filters),
        order_by: "`tabWF Workflow Requests`.`creation` desc",
    };

    const queryParamsCount = {
        fields: JSON.stringify(["count(name) AS total_count"]),
        limitPageLength: "None",
        filters: JSON.stringify(filters),
    };

    // Fetch total count of records matching filters
    axiosInstance
        .get(`${apis?.resource}${doctypes?.WFWorkflowRequests}`, { params: queryParamsCount })
        .then((res) => {
            totalRecords.value = res.data[0].total_count;
        })
        .catch((error) => {
            console.error("Error fetching total count:", error);
        });

    // Fetch the records matching filters
    axiosInstance
        .get(`${apis.resource}${doctypes.WFWorkflowRequests}`, { params: queryParams })
        .then((res) => {
            tableData.value = res.data;
            idDta.value = [...new Set(res.data.map((id) => id.name))];
            docTypeName.value = [
                ...new Set(res.data.map((docTypeName) => docTypeName.doctype_name)),
            ];
            statusOptions.value = [...new Set(res.data.map((status) => status.status))];
        })
        .catch((error) => {
            console.error("Error fetching records:", error);
        });
}


const radioOptions = ref(['All',
    'Approved', 'Rejected']);
</script>
<style scoped>
.form_archived {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 100vh;
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
</style>