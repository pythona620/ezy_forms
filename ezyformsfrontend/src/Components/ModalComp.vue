<template>
  <div>
    <ButtonComp icon="upload" name="Upload" type="button" class="btn-outline-primary me-1" data-bs-toggle="modal"
      data-bs-target="#staticBackdrop">
    </ButtonComp>

    <div class="modal fade" id="staticBackdrop" tabindex="-1" role="dialog" aria-labelledby="staticBackdropLabel"
      aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered modal-dialog-scrollable">
        <div class="modal-content">
          <div class="modal-header">
            <h6 class="modal-title" id="staticBackdropLabel">

            </h6>
            <button type="button" class="btn-close shadow-none" data-bs-dismiss="modal" aria-label="Close"></button>
          </div>
          <div class="modal-body">
            <div>

            </div>


          </div>
          <div class="modal-footer">

          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import ButtonComp from "./ButtonComp.vue";

export default {
  components: {

    ButtonComp,
  },
  data() {
    return {

    };
  },

  methods: {


  }

};
</script>

<style scoped></style>
