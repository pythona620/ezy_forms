<template>
    <div class="card">
      <div class="col-12">
        <div class="d-flex input-div align-items-center gap-3">
          <div v-if="subView" class="d-flex justify-content-between align-items-center gap-2 flex-wrap ps-1 p-2">
            <div class="d-flex align-items-center gap-2">
              <i class="ri-arrow-left-line fw-bold fs-6" @click="backToBacthList"></i>
              <p class="m-0 batchname text-nowrap">
                <b class="fw-bold">{{ currentBatchRecord.batch_data }} </b>
                (<b class=" fw-bold">{{
                  currentBatchRecord.pos_checks_history?.length
                  }}</b>)<br>
              </p>
            </div>
          </div>
  
          <div class=" d-flex align-items-center justify-content-end w-100">
            <div class="d-flex align-items-center me-3">
              <div class="me-2">
                <span v-if="table_filters.dateId && table_filters.applieddate" class="process-date">
                  {{ table_filters.dateId }}
                  <span v-if="table_filters.dateId" class="badge badge-icon rounded-3   text-white ms-2"
                    @click="clearFilter('date')">
                    <i class="ri-close-line close-icon text-dark rounded-3"></i>
                  </span>
                </span>
  
                <span v-if="table_filters.statusOption && table_filters.appliedstatus" class="process-date"> {{
                  table_filters.statusOption }}
                  <span v-if="table_filters.statusOption" class="badge badge-icon rounded-3   text-white ms-2"
                    @click="clearFilter('status')">
                    <i class="ri-close-line close-icon text-dark rounded-3"></i>
                  </span>
                </span>
              </div>
              <button v-if='!subView' class=" border-0 me-2 bg-transparent rounded-1 p-2 reload-btn" title="Refresh"
                @click="realoadPage()">
                <i class="ri-refresh-line"></i>
              </button>
  
              <button v-if='!subView' type="button"
                class="btn btn-outline-light text-dark p-0 ms-1 me-1 position-relative" data-bs-toggle="modal"
                data-bs-target="#filtermodal">
                <i title="Filters" class="ri-filter-line filter-icon fs-5"></i>
                <span v-if="appliedFiltersCount !== 0"
                  class="position-absolute top-0 start-100 translate-middle badge rounded-pill bg-danger">
                  {{ appliedFiltersCount }}
                </span>
              </button>
              <ButtonComp v-if="!subView || (subView && currentBatchRecord.status !== 'Completed')"
                :class="{ 'not-allowed': !selectedBatch.length }" @click="reprocessChecks"
                :disabled="selectedBatch.length === 0" name="Re-Process"
                class="btn-primary d-flex justify-content-end px-2 "
                :count="!subView && selectedBatch.length > 0 ? selectedBatch.length : null" />
  
              <ModalComp v-if="!subView"></ModalComp>
              <!-- @message-from-child="handleMessageFromChild" -->
            </div>
          </div>
          <!-- Modal -->
          <div class="modal fade" id="filtermodal" tabindex="-1" aria-labelledby="filetermodalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered  modal-dialog-scrollable">
              <div class="modal-content">
                <div class="modal-header">
                  <h6 class="modal-title " id="filetermodalLabel"> Apply Filters (<b class=" fw-bold">{{
                    filtersBeforeApplyingCount
                      }}</b>)</h6>
                  <button type="button" class="btn-close shadow-none" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                  <div class="row">
                    <div class="col-6">
                      <FormFields labeltext="" class="mb-3 w-auto" tag="input" type="date" name="dateId"
                        placeholder="Check Date" id="dateId" v-model="table_filters.dateId" :Required="false" />
                    </div>
                    <div class="col-6">
                      <FormFields labeltext="" tag="select" class="mb-3 selectStatus w-auto" placeholder="Status"
                        name="Status" id="status" :options="['Pending', 'Completed']" v-model="table_filters.statusOption"
                        :Required="false" />
                    </div>
                  </div>
                </div>
                <div class="modal-footer">
                  <div class="d-flex gap-3 justify-content-end">
                    <ButtonComp @click="clearFilters" data-bs-dismiss="modal" class="btn-outline-primary"
                      name="Clear Filters" />
  
                    <ButtonComp @click="applyfilters" class="btn-primary" data-bs-dismiss="modal"
                      :disabled="!table_filters.dateId && !table_filters.statusOption" name="Apply Filters" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  
    <div>
      <div v-if="viewType">
        <div class="card">
          <div class="p-3 pb-0">
            <!-- isCheckbox="true" -->
            <GlobalTable class="custom-table" :tHeaders="tableHeaders" :tData="listdata" actionType="viewPdf"
              isCheckbox="true" isAction="true" @cell-click="handleCellClick" @checkbox-click="selectedCheckList"
              @all-Check="SelectedAll" />
          </div>
          <hr class="all-side-border" />
          <div v-if="!listdata.length && !viewType">
            <div class="no_data">
              <span class="text-muted fw-bold"> No Data Found</span>
            </div>
          </div>
          <div v-if="listdata.length"
            class="d-flex align-items-center justify-content-between position-sticky bottom-0 bg-white px-3 p-2">
            <PaginationComp @updateValue="handleUpdateValue" @limitStart="handleLimitStart"
              :currentRecords="listdata.length" :totalRecords="totalRecords[0]?.total_count" />
          </div>
        </div>
      </div>
      <div v-if="!viewType" class="main-list-div">
        <div class="card">
          <div class="container-fluid">
            <div v-if="listdata.length" class="row">
              <div class="row">
                <div class="col-lg-2 ps-0">
                  <ListView @checkedValue="handleCheckedNo" :checks="listdata" :selectedCheck="selectedCheck"
                    :itemIndex="currentIndex" listType="url" />
                </div>
  
                <div class="col-lg-10">
                  <div class="row">
                    <div class="col-lg-8">
                      <div>
                        <iframe v-if="!ImgeView" type="application/pdf" class="bg-white pdfview"
                          style="background: #ffffff" :src="getPDFUrl(selectedCheck.check_file)"
                          alt="Pdf as image"></iframe>
                        <ImageViewer v-if="ImgeView" :downloadImg="downloadImg" checkType="name"
                          :pdfImageUrls="pdfImageUrls" :selectedCheck="selectedCheck" :loadPdfView="loadPdfView" />
                      </div>
                    </div>
                    <div class="col-lg-4 checkEditDiv">
                      <CheckDetailsEdit :selectedcheckDetails="selectedCheck" />
                      <div v-if="listdata.length" class="btns-div d-flex justify-content-between bg-white">
                        <ButtonComp @click="PreviousNext('Previous')" icon="chevron-double-left" name="Prev" id="previous"
                          class="btn-outline-secondary p-0" />
                        <div v-if="false" class="text-secondary d-flex justify-content-center align-items-center more">
                          <span>{{ totalCount }} /
                            {{ totalRecords[0]?.total_count }}</span>
                          <span class="more text-decoration-underline ms-1" @click="moreChecks()"
                            v-if="listdata.length < totalRecords[0]?.total_count">
                            more..
                          </span>
                        </div>
                        <ButtonComp @click="PreviousNext('Next')" aferIcon="chevron-double-right" name="Next" id="next"
                          class="btn-primary p-0" />
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script setup>
  import FormFields from "@/components/FormFields.vue";
  import ModalComp from "@/components/ModalComp.vue";
  import GlobalTable from "@/components/GlobalTable.vue";
  import PaginationComp from "@/components/PaginationComp.vue";
  
  // import socket from "@/socketservice";
  import {
    ref,
    onMounted,
    watch,
    onBeforeUnmount,
    reactive,
    onUnmounted,
    computed,
    // inject,
    // getCurrentInstance,
  } from "vue";
  import ButtonComp from "@/components/ButtonComp.vue";
  import ListView from "@/components/ListView.vue";
  import getResourceData from "@/shared/services/api_req_data";
  import CheckDetailsEdit from "@/components/CheckDetailsEdit.vue";
  import { doctypes, apis, domain } from "@/shared/apiurls";
  
  import axiosInstance from "../../shared/services/interceptor";
  import { useRoute } from "vue-router";
  import { toast } from "vue3-toastify";
  import "vue3-toastify/dist/index.css";
  import ImageViewer from "@/components/ImageViewer.vue";
  
  import "pdfjs-dist/legacy/build/pdf.worker";
  import { PdfRenderService } from "@/service";
  import eventBus from "@/eventEmit";
  // import { sidebarToggle } from "@/components/loader/loader";
  
  const listdata = ref([]);
  const selectedCheck = ref({});
  const ImgeView = ref(process.env.VUE_APP_PDF_VIEW === "false");
  
  const edittype = ref(true);
  const currentIndex = ref(0);
  
  const totalRecords = ref(0);
  const totalCount = ref(0);
  const viewType = ref();
  
  const pdfImageUrls = ref([]);
  
  const carouselIndex = ref(0);
  const loadPdfView = ref();
  
  const route = useRoute();
  // const router = useRouter();
  const currentBatchRecord = ref({});
  
  // const sub_batch_list = ref([]);
  const subView = ref(false);
  // const checkedValues=ref([])
  const selectedBatch = ref([]);
  // let inputDate = ref([])
  
  const tableHeaders = ref([
    { th: "Batch Name", td_key: "batch_data" },
    { th: "Total", td_key: "total_files" },
    { th: "Completed", td_key: "completed_files" },
    { th: "Error", td_key: "error_files" },
    { th: "Status", td_key: "status" },
    // { th: "Uploaded Date", td_key: "modified" },
    { th: "Check Date", td_key: "upload_date" },
    // { th: "Actions", td_key: "upload_date" },
  ]);
  // const actions = ["Check View", "Text View", "Download"];
  const table_filters = reactive({
    applieddate: false,
  
    appliedstatus: false,
  
    dateId: "",
    statusOption: "",
  });
  watch(
    () => route.params.id,
    (url) => {
      filters_obj.value.filters = [];
      if (url) {
        fetchData(url);
        table_filters.dateId = "";
  
        table_filters.statusOption = "";
  
        viewType.value = true;
      }
    }
  );
  
  function realoadPage() {
    selectedBatch.value = [];
    document.querySelectorAll('input[type="checkbox"]').forEach(checkbox => {
      checkbox.checked = false;
    });
    fetchData();
  }
  
  onMounted(async () => {
    viewType.value = route.query?.view ? JSON.parse(route.query?.view) : true;
    window.addEventListener("keydown", handleKeydown);
    await fetchData();
    selectedCheck.value = listdata.value[currentIndex.value];
  
    eventBus.on('pos_upload_batch_created', (data) => {
      if (data) {
        fetchData();
      }
    });
  
    eventBus.on('pos_upload_batch_ended', (data) => {
      if (data) {
        toast.success("Files Uploaded", { autoClose: 2000 })
        fetchData();
      }
    });
  
    // eventBus.on('Reprocess_BatchId', (data) => {
    //   if (data) {
    //     fetchData();
    //     // console.log(data,'---======')
    //   }
    // });
  
    eventBus.on('pos_upload_reprocess_started', (data) => {
      if (data) {
        if (!viewType.value) {
          handleCellClick(currentBatchRecord.value);
        }
        else {
          fetchData();
        }
      }
    });
  
    eventBus.on('Reprocess_Completed', (data) => {
      if (data) {
        toast.success('Reprocess Completed')
        if (!viewType.value) {
          handleCellClick(currentBatchRecord.value);
        }
        else {
          fetchData();
        }
      }
    })
  });
  onUnmounted(() => {
    eventBus.off('pos_upload_reprocess_started', {})
    eventBus.off('Reprocess_Completed', {})
    eventBus.off('pos_upload_batch_created', {})
    eventBus.off('pos_upload_batch_ended', {})
  })
  const filtersBeforeApplyingCount = computed(() => {
    return [table_filters.statusOption, table_filters.dateId].filter(
      (value) => value
    ).length;
  });
  
  // Count of filters that are both applied and have non-empty values
  const appliedFiltersCount = computed(() => {
    return [
      { value: table_filters.dateId, applied: table_filters.applieddate },
      {
        value: table_filters.appliedstatus,
        applied: table_filters.appliedstatus,
      },
    ].filter((filter) => filter.applied && filter.value).length;
  });
  
  onMounted(() => {
    window.addEventListener("keydown", handleKeyDown);
  });
  
  onBeforeUnmount(() => {
    window.removeEventListener("keydown", handleKeyDown);
  });
  
  function handleKeyDown(event) {
    if (table_filters.dateId || table_filters.statusOption) {
      if (event.key === "Enter") {
        const modalElement = document.getElementById("filtermodal");
        if (modalElement && modalElement.classList.contains('show')) {
          applyfilters();
          const bootstrapModal = this.bootstrap.Modal.getInstance(modalElement);
          if (bootstrapModal) {
            bootstrapModal.hide();
          }
        }
      }
    }
  }
  
  
  
  function applyfilters() {
    filters_obj.value.filters = [];
    filters_obj.value.limitstart = 0;
    if (table_filters.dateId) {
      filters_obj.value.filters.push([
        "upload_date",
        "like",
        table_filters.dateId,
      ]);
      table_filters.applieddate = true;
    } else {
      table_filters.applieddate = false;
    }
    if (table_filters.statusOption) {
      filters_obj.value.filters.push(["status", "=", table_filters.statusOption]);
      table_filters.appliedstatus = true;
    } else {
      table_filters.appliedstatus = false;
    }
    fetchData();
  }
  function clearFilter(type) {
    if (type === "date") {
      table_filters.dateId = "";
      table_filters.applieddate = false;
    } else if (type === "status") {
      table_filters.statusOption = "";
      table_filters.appliedstatus = false;
    }
    applyfilters();
  }
  function clearFilters() {
    table_filters.dateId = "";
    table_filters.statusOption = "";
  
    table_filters.applieddate = false;
    table_filters.appliedstatus = false;
  
    applyfilters();
  }
  // function activeViewType(type) {
  
  //   viewType.value = type;
  //   router.push({
  //     path: "/PosCheckModule/checkuploads",
  //     query: { view: type },
  //   });
  //   sidebarToggle.value = type;
  // }
  
  function downloadImg() {
    const url = getPDFUrl(selectedCheck.value.check_file);
    const a = document.createElement("a");
    a.href = url;
    a.download = "";
    a.click();
    toast.success("Downloaded", { autoClose: 2000 });
  }
  
  const filters_obj = ref({
    limitPageLength: 100,
    fields: ["*"],
    filters: [],
    limitstart: 0,
    order_by: "`tabPOS Uploads`.`status` desc, `tabPOS Uploads`.`modified` desc",
  });
  
  // Function to fetch data from the pagination component
  const handleUpdateValue = (itemsPerPage) => {
    // listdata.value = [];
    filters_obj.value.limitPageLength = itemsPerPage;
    filters_obj.value.limitstart = 0;
    fetchData();
    // console.log(itemsPerPage,'=====')
  
  };
  
  const handleLimitStart = ([itemsPerPage, start]) => {
    filters_obj.value.limitPageLength = itemsPerPage;
    filters_obj.value.limitstart = start;
    fetchData();
    // console.log(itemsPerPage,'=====')
  };
  
  const handleCheckedNo = (check, index) => {
    selectedCheck.value = check;
    currentIndex.value = index;
    carouselIndex.value = 0;
    edittype.value = true;
    loadPdf(getPDFUrl(selectedCheck.value.check_file));
  };
  const moreChecks = async () => {
    filters_obj.value.limitPageLength = 100;
    await fetchData();
  };
  
  function getPDFUrl(filePath) {
    return `${domain}${filePath}`;
  }
  
  async function loadPdf(fileUrl) {
    try {
      pdfImageUrls.value = [];
  
      loadPdfView.value = true;
      if (process.env.VUE_APP_PDF_VIEW) {
        pdfImageUrls.value = await PdfRenderService.renderPdfToImages(fileUrl);
      } else {
        getPDFUrl();
      }
      loadPdfView.value = false;
    } catch (error) {
      console.error("Error loading PDF:", error);
    }
  }
  function PreviousNext(type) {
    if (type === "Previous" && currentIndex.value > 0) {
      currentIndex.value--;
      // loadPdf(getPDFUrl(selectedCheck.value.check_file));
    } else if (
      type === "Next" &&
      currentIndex.value < listdata.value.length - 1
    ) {
      currentIndex.value++;
    }
    selectedCheck.value = listdata.value[currentIndex.value];
    loadPdf(getPDFUrl(selectedCheck.value.check_file));
  }
  
  async function backToBacthList() {
    selectedBatch.value = [];
    viewType.value = true;
    subView.value = false;
    // sidebarToggle.value = true
    await fetchData();
  }
  
  function SelectedAll(isChecked) {
    if (isChecked) {
      const values = new Map();
      const batchDataSet = new Set();
  
      listdata.value.map((item) => {
        if (!values.has(item.name)) {
          values.set(item.name, { ...item, isSelected: true });
          if (item.status == "Pending") {
            batchDataSet.add(item.batch_id);
          }
        }
      });
      selectedBatch.value = Array.from(batchDataSet);
      listdata.value = Array.from(values.values());
    } else {
      listdata.value.map((item) => (item.isSelected = false));
      selectedBatch.value = [];
    }
  }
  
  function selectedCheckList(check) {
    const batchIndex = selectedBatch.value.indexOf(check.batch_id);
    if (batchIndex > -1) {
      selectedBatch.value.splice(batchIndex, 1);
    } else {
      selectedBatch.value.push(check.batch_id);
    }
  }
  
  //Re process
  async function reprocessChecks() {
    let data = {
      processing_id: [selectedBatch.value],
    };
    try {
      const response = await axiosInstance.post(apis.reprocessingChecks, data);
      if (response) {
        console.log(response)
      }
      // if (!viewType.value) {
      //   handleCellClick(currentBatchRecord.value);
      // }
    } catch (error) {
      console.error("Error :", error);
    } finally {
      selectedBatch.value = [];
      const checkboxes = document.querySelectorAll(
        'input[type="checkbox"]:checked'
      );
      checkboxes.forEach((checkbox) => {
        checkbox.checked = false;
      });
    }
  }
  
  // function handleMessageFromChild(message) {
  //   if (message == "All files uploaded successfully") {
  //     setTimeout(() => {
  //       fetchData();
  //     }, 5000);
  //   }
  // }
  
  async function handleCellClick(check) {
    const newData = await getResourceData(
      doctypes.posUploads + "/" + check.batch_id,
      filters_obj.value.fields,
      filters_obj.value.filters,
      filters_obj.value.limitPageLength,
      filters_obj.value.limitstart,
      filters_obj.value.order_by
    );
  
    if (newData?.pos_checks_history.length > 0) {
      newData.pos_checks_history.sort((a, b) => {
        if (a.status === "Error" && b.status !== "Error") return -1;
        if (a.status !== "Error" && b.status === "Error") return 1;
        if (a.status === "Completed" && b.status !== "Completed") return 1;
        if (a.status !== "Completed" && b.status === "Completed") return -1;
        return 0;
      });
      viewType.value = false;
      subView.value = true;
      currentBatchRecord.value = newData;
      if (currentBatchRecord.value.status == "Pending") {
        selectedBatch.value = [currentBatchRecord.value.batch_id];
      }
      // console.log(currentBatchRecord.value.batch_id, "batchdata");
      listdata.value = newData.pos_checks_history;
      selectedCheck.value = listdata.value[0];
      currentIndex.value = 0;
      loadPdf(getPDFUrl(selectedCheck.value.check_file));
      // sidebarToggle.value = false;
    }
  }
  
  async function fetchData() {
    // subView.value = false;
    // viewType.value = true;
  
    // listdata.value = [];
    try {
      const fields = ["count( `tabPOS Uploads`.`name`) AS total_count"];
      const limitPageLength = "None";
      totalRecords.value = await getResourceData(
        doctypes.posUploads,
        fields,
        filters_obj.value.filters,
        limitPageLength
      );
      const newData = await getResourceData(
        doctypes.posUploads,
        filters_obj.value.fields,
        filters_obj.value.filters,
        filters_obj.value.limitPageLength,
        filters_obj.value.limitstart,
        filters_obj.value.order_by
      );
      if (filters_obj.value.limitstart !== 0) {
        listdata.value = listdata.value.concat(newData);
      } else {
        listdata.value = newData;
        // selectedCheck.value = listdata.value[currentIndex.value];
        // loadPdf(getPDFUrl(selectedCheck.value.check_file));
      }
      // listdata.value.push(...newData);
      totalCount.value = listdata.value.length;
      // loadPdf(getPDFUrl(selectedCheck.value.check_file));
    } catch (error) {
      console.error("Error fetching data:", error);
    }
  }
  
  // const uploadFiles = () => { };
  
  const handleKeydown = (event) => {
    if (event.key === "ArrowLeft") {
      PreviousNext("Previous");
    } else if (event.key === "ArrowRight") {
      PreviousNext("Next");
    }
  };
  
  onBeforeUnmount(() => {
    window.removeEventListener("keydown", handleKeydown);
  });
  </script>
  
  <style lang="scss" scoped>
  .not-allowed {
    cursor: not-allowed;
  }
  
  th {
    background-color: var(--thcolor) !important;
  }
  
  td {
    border: none !important;
  }
  
  .filterinput {
    border-bottom: 1px solid var(--border-bottom);
  }
  
  .more {
    cursor: pointer;
    font-size: var(--eleven);
  }
  
  .no_data {
    height: 70vh;
    display: flex;
    justify-content: center;
    align-items: center;
  }
  
  .reload-btn {
    // box-shadow: 2px 2px 3px var(--secondary);
    border: 0.1px solid transparent;
    border-radius: 3px;
    box-shadow: 1px 1px 3px 0px rgba(0, 0, 0, 0.48);
    padding: 5px;
    transition: all 0.8s ease;
    cursor: pointer;
  }
  
  .reload-btn:hover {
    border: 0.1px solid rgba(0, 0, 0, 0.28);
    box-shadow: inset 1px 1px 1px 0px rgba(0, 0, 0, 0.18);
    color: #525252;
  }
  
  .checkEditDiv {
    position: relative;
    height: 76vh;
    // margin-top: 15px;
  }
  
  .input-div {
    // box-shadow: var(--box-shadow2);
    border: 1px solid var(--border-bottom);
    // border-radius: 4px;
  }
  
  // .iframe-pdf {
  //   height: 600px;
  //   width: 100%;
  // }
  
  // @media (max-width: 1440px) {
  //   .iframe-pdf {
  //     height: 450px;
  //     width: 100%;
  //   }
  // }
  .carousel-item {
    height: 74vh;
    overflow: scroll;
    overflow-x: scroll;
    border: 2px solid rgb(82, 86, 89);
  }
  
  s .zoombtn {
    // background-color: var(--secondary);
    background: transparent;
    color: #7c7b7b;
    margin: 3px;
    border-radius: 10px;
    padding: 0px 5px;
    font-size: 18px;
    font-weight: 600;
    transition: all 0.3s linear;
  }
  
  .zoombtn:hover {
    color: black;
  }
  
  .zoom-div {
    margin-right: 19%;
  }
  
  .not-allowed {
    cursor: not-allowed;
  }
  
  .btns {
    button {
      // background-color: blue;
      position: absolute;
      top: -38px;
      left: 82%;
      width: 30px;
      height: 30px;
      border-radius: 50%;
      color: black;
      font-size: 24px;
    }
  
    button:disabled {
      color: grey;
    }
  
    button:nth-child(2) {
      left: 94%;
    }
  
    p {
      position: absolute;
      right: 5%;
      top: -35px;
    }
  }
  
  .batchname {
    font-size: var(--thirteen);
  }
  
  .statusupload {
    font-size: 11px;
  }
  
  @media (max-width: 1200px) {
    .checkEditDiv {
      position: relative;
      height: 81vh;
    }
  }
  
  @media (min-width: 1401px) and (max-width: 1800px) {
    .checkEditDiv {
      position: relative;
      height: 81vh;
    }
  }
  
  @media (min-width: 1801px) and (max-width: 2560px) {
    .checkEditDiv {
      position: relative;
      height: 84vh;
    }
  }
  
  @media (min-width: 2561px) and (max-width: 2817px) {
    .checkEditDiv {
      position: relative;
      height: 87vh;
    }
  }
  </style>
  