<template>
  <b-modal class="modal right fade" id="sidebar" ref="sidebar" cancel-disabled>
    <template slot="modal-title">
      <h2>{{ display_title }}</h2>
    </template>

    <img v-if="img_url" :src="img_url" class="img-fluid caption-img" :alt="display_title" />

    <div class="d-block" v-if="payload">
      <slot v-bind:hit="payload"></slot>
    </div>

    <template slot="modal-footer" slot-scope="{ ok, cancel, hide }">
      <!-- Emulate built in modal footer ok and cancel button actions -->
      <b-button variant="primary" @click="ok()">Close</b-button>
    </template>
  </b-modal>
</template>

<script>
export default {
    name: "Sidebar",
    props: {
        title: { type: String, required: false }
    },
    data() {
        return {
            display_title: this.title,
            img_url: null,
            payload: null
        }
    },
    methods: {
        showModal(options) {
            const {title, img_url} = options;

            if (title) { this.display_title = title; }
            if (img_url) { this.img_url = img_url; }
            this.payload = options;
            console.log(options);

            this.$refs.sidebar.show();
        }
    }
}
</script>

<style scoped>
/*******************************
* MODAL AS LEFT/RIGHT SIDEBAR
* Add "left" or "right" in modal parent div, after class="modal".
* Get free snippets on bootpen.com
*******************************/
.modal.left .modal-dialog,
.modal.right .modal-dialog {
  position: fixed;
  margin: auto;
  width: 320px;
  height: 100%;
  -webkit-transform: translate3d(0%, 0, 0);
  -ms-transform: translate3d(0%, 0, 0);
  -o-transform: translate3d(0%, 0, 0);
  transform: translate3d(0%, 0, 0);
}

.modal.left .modal-content,
.modal.right .modal-content {
  height: 100%;
  overflow-y: auto;
}

.modal.left .modal-body,
.modal.right .modal-body {
  padding: 15px 15px 80px;
}

/*Left*/
.modal.left.fade .modal-dialog{
  left: -320px;
  -webkit-transition: opacity 0.3s linear, left 0.3s ease-out;
  -moz-transition: opacity 0.3s linear, left 0.3s ease-out;
  -o-transition: opacity 0.3s linear, left 0.3s ease-out;
  transition: opacity 0.3s linear, left 0.3s ease-out;
}

.modal.left.fade.in .modal-dialog{
  left: 0;
}

/*Right*/
.modal.right.fade .modal-dialog {
  right: -320px;
  -webkit-transition: opacity 0.3s linear, right 0.3s ease-out;
  -moz-transition: opacity 0.3s linear, right 0.3s ease-out;
  -o-transition: opacity 0.3s linear, right 0.3s ease-out;
  transition: opacity 0.3s linear, right 0.3s ease-out;
}

.modal.right.fade.in .modal-dialog {
  right: 0;
}

/* ----- MODAL STYLE ----- */
.modal-content {
  border-radius: 0;
  border: none;
}

.modal-header {
  border-bottom-color: #EEEEEE;
  background-color: #FAFAFA;
}

.caption-img {
  object-fit: cover;
  max-height: 250px;
  width: 100%; margin-bottom: 1em;
  /*width: 100%;*/
  /*position: absolute;*/
  /*top: 0; left: 0; right: 0;*/
}
</style>