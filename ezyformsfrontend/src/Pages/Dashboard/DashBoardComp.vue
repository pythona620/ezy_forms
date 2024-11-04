<template>
    <div>
        <button class="btn btn-primary" type="button" data-bs-toggle="offcanvas" data-bs-target="#offcanvasRight"
            aria-controls="offcanvasRight">Toggle right offcanvas</button>

        <div class="offcanvas offcanvas-end" tabindex="-1" id="offcanvasRight" aria-labelledby="offcanvasRightLabel">
            <div class="offcanvas-header">
                <h5 class="offcanvas-title" id="offcanvasRightLabel">Asset Request Form

                </h5>
                <button type="button" class="btn-close" data-bs-dismiss="offcanvas" aria-label="Close"></button>
            </div>
            <div class="offcanvas-body">
                <div class="d-flex gap-3 align-items-baseline position-relative">
                    <div class="d-flex flex-column  ">
                        <span>
                            <i class="ri-checkbox-blank-circle-fill dashedcircle"></i>
                        </span>
                        <div class="dashed_line mt-4 ">
                        </div>
                        <!-- <span>
                        <i class="ri-checkbox-blank-circle-fill text-success p-1 dashedcircle"></i>
                    </span> -->

                    </div>
                    <div>
                        data
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
<script>
</script>

<style>
.dashedcircle {
    border: 1px dashed #AAAAAA;
    height: 30px;
    width: 30px;
    padding: 0;
    margin: 0;
    border-radius: 50%;
    color: #14D82B;
    ;
}

.dashed_line {
    height: 100px;
    border: 1px dashed #AAAAAA;
    width: 1px;
    position: absolute;
    left: 2%;

}
</style>
