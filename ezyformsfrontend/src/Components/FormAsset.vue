<template>
    <div class="d-flex  align-items-center">
        <div class="ps-1 m-0 d-flex align-items-center">
            <h1 class="font-13">
                <i class="bi bi-arrow-left"></i><span class="ms-2">Asset Form</span>
            </h1>
        </div>

    </div>
    <div>
        <p class="font-12 text-center">Requested by Noshitha (Assistant HR)</p>

    </div>
    <div class="d-flex justify-content-center align-items-center">
        <div class="mainheight">

            <div class="raising mb-2">
                <p class="font-12 ps-3">Raising For Self</p>
            </div>
            <div class="raising mt-2 mb-2 p-2">
                <p class="font-12 ps-3 m-0">Hanumantha Rao</p>
                <p class="font-11 ps-3 m-0">Assistant Manager || #234567 || Food And Beverages</p>

            </div>
            <div class="d-flex justify-content-between align-items-center mt-3">
                <div>
                    <ButtonComp type="button" icon="check2" class="approvebtn border-1 text-nowrap font-10 "
                        name="Approve" />
                </div>
                <div>
                    <ButtonComp type="button" icon="x" class="rejectbtn border-1 text-nowrap font-10 " name="Reject" />
                </div>
            </div>


        </div>

    </div>
</template>
<script setup>
import ButtonComp from '../Components/ButtonComp.vue';
</script>
<style>
.mainheight {
    height: 100vh;
}

.raising {
    border: 1px solid #EEEEEE;
    background-color: #FAFAFA;
    font-size: 12px;
    padding: 8px 0px 0px 7px;
    width: 460px;
}

.approvebtn {
    width: 146px;
    height: 30px;
    background: #14D82B;
    color: white;
    padding: 5px 15px 5px 15px;
    gap: 7px;
    border-radius: 4px 0px 0px 0px;
    opacity: 0px;

}

.rejectbtn {
    width: 146px;
    height: 30px;
    background: #FE212E;
    color: white;
    padding: 5px 15px 5px 15px;
    gap: 7px;
    border-radius: 4px 0px 0px 0px;
    opacity: 0px;

}
</style>